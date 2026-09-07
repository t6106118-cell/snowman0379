#!/usr/bin/env python3
"""Fetch HTTP(S) content as Markdown or a durable local document handoff."""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import os
import pwd
import re
import shutil
import socket
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qsl, unquote, urldefrag, urljoin, urlsplit

HANDOFF_EXIT = 10
MAX_REDIRECTS = 15
SENSITIVE_QUERY_KEYS = {
    "access_token", "api_key", "apikey", "auth", "authorization", "code",
    "credential", "key", "password", "secret", "sig", "signature", "token",
    "x-amz-credential", "x-amz-signature", "x-goog-credential", "x-goog-signature",
}
MARKDOWN_TYPES = {"application/markdown", "text/markdown", "text/x-markdown"}
HTML_TYPES = {"text/html", "application/xhtml+xml"}
PDF_TYPES = {"application/pdf"}
DOCUMENT_EXTENSIONS = {
    ".doc", ".docx", ".docm", ".ppt", ".pps", ".pot", ".pptx", ".pptm",
    ".ppsx", ".ppsm", ".xls", ".xlsx", ".xlsm", ".xlsb", ".odt", ".ods",
    ".odp", ".rtf", ".epub", ".csv",
}
DOCUMENT_TYPES = {
    "application/msword", "application/rtf", "text/rtf", "text/csv",
    "application/epub+zip", "application/vnd.ms-excel", "application/vnd.ms-powerpoint",
    "application/vnd.oasis.opendocument.text", "application/vnd.oasis.opendocument.spreadsheet",
    "application/vnd.oasis.opendocument.presentation",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-word.document.macroenabled.12",
    "application/vnd.ms-powerpoint.presentation.macroenabled.12",
    "application/vnd.ms-excel.sheet.macroenabled.12",
}
TYPE_EXTENSION = {
    "application/pdf": ".pdf", "text/csv": ".csv", "application/rtf": ".rtf",
    "text/rtf": ".rtf", "application/epub+zip": ".epub", "application/msword": ".doc",
    "application/vnd.ms-excel": ".xls", "application/vnd.ms-powerpoint": ".ppt",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
    "application/vnd.oasis.opendocument.text": ".odt",
    "application/vnd.oasis.opendocument.spreadsheet": ".ods",
    "application/vnd.oasis.opendocument.presentation": ".odp",
}


class ConversionError(RuntimeError):
    """A fetch, route, conversion, or validation failed."""


@dataclass(frozen=True)
class Acquisition:
    source_url: str
    final_url: str
    status: int
    content_type: str
    body: bytes
    redirects: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch an HTTP(S) URL as Markdown using local tools only.")
    parser.add_argument("url", help="Public HTTP(S) URL to fetch")
    parser.add_argument("-o", "--output", type=Path, help="Markdown output path")
    parser.add_argument("--mode", choices=("auto", "native", "html", "browser", "clean"),
                        default="auto", help="Conversion route (default: auto)")
    parser.add_argument("--expect", help="Case-insensitive regex required in extracted Markdown")
    parser.add_argument("--min-chars", type=int, default=200, help="Minimum output characters (default: 200)")
    parser.add_argument("--timeout", type=int, default=45, help="Per-command timeout seconds (default: 45)")
    parser.add_argument("--force", action="store_true", help="Replace output file")
    parser.add_argument("--allow-private", action="store_true", help="Allow localhost/private targets")
    parser.add_argument("--allow-sensitive-query", action="store_true", help="Allow credential-like query keys")
    args = parser.parse_args()
    if args.min_chars < 1:
        parser.error("--min-chars must be positive")
    if args.timeout < 1:
        parser.error("--timeout must be positive")
    if args.output and args.output.exists() and not args.force:
        parser.error(f"output exists; pass --force to replace it: {args.output}")
    if args.expect:
        try:
            re.compile(args.expect, re.IGNORECASE | re.MULTILINE)
        except re.error as exc:
            parser.error(f"invalid --expect regex: {exc}")
    return args


def is_nonpublic_address(value: str) -> bool:
    return not ipaddress.ip_address(value).is_global


def validate_url(url: str, *, allow_private: bool,
                 allow_sensitive_query: bool) -> tuple[str, int, str] | None:
    parsed = urlsplit(url)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise ConversionError("only HTTP(S) URLs are allowed")
    if not parsed.hostname:
        raise ConversionError("URL has no hostname")
    if parsed.username is not None or parsed.password is not None:
        raise ConversionError("credentials embedded in URLs are not allowed")
    if not allow_sensitive_query:
        keys = {key.casefold() for key, _ in parse_qsl(parsed.query, keep_blank_values=True)}
        sensitive = sorted(keys & SENSITIVE_QUERY_KEYS)
        if sensitive:
            raise ConversionError("sensitive query key(s) rejected: " + ", ".join(sensitive))
    host = parsed.hostname.rstrip(".").casefold()
    if not allow_private and (host == "localhost" or host.endswith((".localhost", ".local", ".internal"))):
        raise ConversionError("localhost/private-network host rejected")
    try:
        if not allow_private and is_nonpublic_address(host):
            raise ConversionError("non-public IP address rejected")
        return None
    except ValueError:
        pass
    try:
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
    except ValueError as exc:
        raise ConversionError(f"invalid URL port: {exc}") from exc
    try:
        addresses = {answer[4][0] for answer in socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)}
    except socket.gaierror as exc:
        raise ConversionError(f"hostname resolution failed: {exc}") from exc
    if not addresses:
        raise ConversionError("hostname resolved to no addresses")
    blocked = sorted(address for address in addresses if is_nonpublic_address(address))
    if blocked and not allow_private:
        raise ConversionError("hostname resolves to non-public address(es): " + ", ".join(blocked))
    # Pin hostname requests to an address from this exact validated result set.
    # --connect-to preserves URL Host/SNI and, unlike --resolve, sends this
    # numeric target through a socks5h proxy instead of asking it to re-resolve.
    return host, port, sorted(addresses)[0]


def require_command(names: tuple[str, ...]) -> str:
    for name in names:
        command = shutil.which(name)
        if command:
            return command
    raise ConversionError("required command not found: " + " or ".join(names))


def run_command(command: list[str], *, timeout: int, cwd: Path | None = None,
                env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True,
                              timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise ConversionError(f"command timed out after {timeout}s: {command[0]}") from exc


def location_from_headers(path: Path) -> str | None:
    text = path.read_text(encoding="iso-8859-1")
    blocks = [block for block in re.split(r"\r?\n\r?\n", text) if block.startswith("HTTP/")]
    if not blocks:
        raise ConversionError("curl returned no HTTP response headers")
    locations = []
    for line in blocks[-1].splitlines()[1:]:
        if line.casefold().startswith("location:"):
            locations.append(line.split(":", 1)[1].strip())
    if len(locations) > 1:
        raise ConversionError("redirect response contains multiple Location headers")
    return locations[0] if locations else None


def acquire(url: str, workdir: Path, *, timeout: int, allow_private: bool,
            allow_sensitive_query: bool, accept: str) -> Acquisition:
    source_url = url
    current = urldefrag(url).url
    seen: set[str] = set()
    connection_pin = validate_url(current, allow_private=allow_private,
                                  allow_sensitive_query=allow_sensitive_query)
    for hop in range(MAX_REDIRECTS + 1):
        normalized = urldefrag(current).url
        if normalized in seen:
            raise ConversionError("redirect loop detected")
        seen.add(normalized)
        body_path, headers_path = workdir / f"body-{hop}", workdir / f"headers-{hop}"
        command = [
            require_command(("curl",)), "--silent", "--show-error", "--compressed",
            "--max-time", str(timeout), "--proto", "=http,https",
            "--output", str(body_path), "--dump-header", str(headers_path),
            "--header", f"Accept: {accept}",
            "--write-out", "%{json}",
        ]
        if connection_pin:
            host, port, address = connection_pin
            target = f"[{address}]" if ":" in address else address
            command.extend(["--connect-to", f"{host}:{port}:{target}:{port}"])
        command.append(current)
        result = run_command(command, timeout=timeout + 5)
        if result.returncode != 0:
            raise ConversionError(result.stderr.strip() or f"curl exit {result.returncode}")
        try:
            metadata = json.loads(result.stdout)
            status = int(metadata["http_code"])
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ConversionError("curl returned invalid response metadata") from exc
        location = location_from_headers(headers_path)
        if 300 <= status < 400:
            if not location:
                raise ConversionError(f"redirect status {status} without Location")
            if hop >= MAX_REDIRECTS:
                raise ConversionError(f"too many redirects; maximum is {MAX_REDIRECTS}")
            next_url = urldefrag(urljoin(current, location)).url
            connection_pin = validate_url(next_url, allow_private=allow_private,
                                          allow_sensitive_query=allow_sensitive_query)
            current = next_url
            continue
        if status < 200 or status >= 300:
            raise ConversionError(f"unexpected HTTP status: {status}")
        content_type = str(metadata.get("content_type") or "").split(";", 1)[0].strip().lower()
        return Acquisition(source_url, current, status, content_type, body_path.read_bytes(), hop)
    raise ConversionError(f"too many redirects; maximum is {MAX_REDIRECTS}")


def validate_content(content: str, *, min_chars: int, expected: re.Pattern[str] | None) -> None:
    visible = content.strip()
    if len(visible) < min_chars:
        raise ConversionError(f"output too small: {len(visible)} characters; minimum is {min_chars}")
    if expected and not expected.search(content):
        raise ConversionError(f"output does not match --expect regex: {expected.pattern}")


def html_to_markdown(data: bytes, base_url: str, workdir: Path, *, timeout: int,
                     clean: bool = False) -> str:
    html_path = workdir / ("clean-input.html" if clean else "html-input.html")
    html_path.write_bytes(data)
    name = "firecrawl-html-extractor" if clean else "firecrawl-html-to-markdown"
    result = run_command([require_command((name,)), "--url", base_url, str(html_path)], timeout=timeout)
    if result.returncode != 0:
        raise ConversionError(result.stderr.strip() or f"{name} exit {result.returncode}")
    return result.stdout


def browser_command(workdir: Path, url: str) -> tuple[list[str], dict[str, str]]:
    browser = require_command(("chromium-browser", "chromium", "google-chrome"))
    profile = workdir / "browser-profile"
    profile.mkdir(mode=0o700)
    env = os.environ.copy()
    command = [browser, "--headless", "--disable-gpu", "--disable-dev-shm-usage", "--no-first-run",
               "--no-default-browser-check", f"--user-data-dir={profile}", "--dump-dom", url]
    if os.geteuid() != 0:
        return command, env
    runuser = require_command(("runuser",))
    try:
        nobody = pwd.getpwnam("nobody")
    except KeyError as exc:
        raise ConversionError("cannot run Chromium safely as root: nobody user missing") from exc
    os.chown(workdir, nobody.pw_uid, nobody.pw_gid)
    os.chown(profile, nobody.pw_uid, nobody.pw_gid)
    env.update({"HOME": str(profile), "XDG_CACHE_HOME": str(profile / "cache"),
                "XDG_CONFIG_HOME": str(profile / "config")})
    return [runuser, "--user", "nobody", "--", *command], env


def browser_to_markdown(url: str, workdir: Path, *, timeout: int) -> str:
    command, env = browser_command(workdir, url)
    rendered = run_command(command, timeout=timeout, cwd=workdir, env=env)
    if rendered.returncode != 0:
        raise ConversionError(rendered.stderr.strip() or f"Chromium exit {rendered.returncode}")
    if not rendered.stdout.strip():
        raise ConversionError("Chromium returned an empty DOM")
    return html_to_markdown(rendered.stdout.encode(), url, workdir, timeout=timeout)


def document_route(item: Acquisition) -> tuple[str, str] | None:
    suffix = Path(unquote(urlsplit(item.final_url).path)).suffix.casefold()
    data = item.body
    if data.startswith(b"%PDF-") or item.content_type in PDF_TYPES:
        return "pdf-inspector", ".pdf"
    if item.content_type in DOCUMENT_TYPES:
        return "convert-documents-to-markdown", suffix if suffix in DOCUMENT_EXTENSIONS else TYPE_EXTENSION.get(item.content_type, ".bin")
    if suffix in DOCUMENT_EXTENSIONS and (item.content_type == "application/octet-stream" or
            suffix == ".csv" or data.startswith((b"PK\x03\x04", b"{\\rtf", b"\xd0\xcf\x11\xe0"))):
        return "convert-documents-to-markdown", suffix
    return None


def safe_filename(url: str, extension: str) -> str:
    name = Path(unquote(urlsplit(url).path)).name or f"download{extension}"
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._") or f"download{extension}"
    if Path(name).suffix.casefold() not in DOCUMENT_EXTENSIONS | {".pdf"}:
        name += extension
    return name[:180]


def ensure_git_ignored(root: Path) -> None:
    probe = subprocess.run(["git", "-C", str(Path.cwd()), "rev-parse", "--show-toplevel"],
                           text=True, capture_output=True, check=False)
    if probe.returncode != 0:
        return
    repo = Path(probe.stdout.strip()).resolve()
    relative = root.resolve().relative_to(repo).as_posix()
    root.mkdir(parents=True, exist_ok=True)
    if subprocess.run(["git", "-C", str(repo), "check-ignore", "-q", "--", relative], check=False).returncode == 0:
        return
    rule = f"/{relative.rstrip('/')}/"
    exclude = repo / ".git" / "info" / "exclude"
    existing = exclude.read_text(encoding="utf-8") if exclude.exists() else ""
    if rule not in existing.splitlines():
        with exclude.open("a", encoding="utf-8") as handle:
            if existing and not existing.endswith("\n"):
                handle.write("\n")
            handle.write(rule + "\n")
    if subprocess.run(["git", "-C", str(repo), "check-ignore", "-q", "--", relative], check=False).returncode != 0:
        raise ConversionError("failed to exclude handoff directory from Git")


def create_handoff(item: Acquisition, skill: str, extension: str) -> dict[str, object]:
    root = Path.cwd() / ".fetch-url-markdown-handoff"
    root.mkdir(parents=True, exist_ok=True)
    ensure_git_ignored(root)
    request_dir = Path(tempfile.mkdtemp(prefix="request-", dir=root))
    destination = request_dir / safe_filename(item.final_url, extension)
    with tempfile.NamedTemporaryFile(dir=request_dir, prefix=".download.", delete=False) as handle:
        handle.write(item.body)
        temporary = Path(handle.name)
    os.replace(temporary, destination)
    return {"action": "handoff", "source_url": item.source_url, "final_url": item.final_url,
            "content_type": item.content_type, "bytes": len(item.body),
            "sha256": hashlib.sha256(item.body).hexdigest(),
            "downloaded_path": str(destination.resolve()), "suggested_skill": skill}


def write_output(content: str, output: Path | None) -> None:
    if output is None:
        sys.stdout.write(content)
        if content and not content.endswith("\n"):
            sys.stdout.write("\n")
        return
    destination = output.expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=destination.parent,
                                     prefix=f".{destination.name}.", delete=False) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    os.replace(temporary, destination)


def main() -> int:
    args = parse_args()
    try:
        validate_url(args.url, allow_private=args.allow_private,
                     allow_sensitive_query=args.allow_sensitive_query)
        expected = re.compile(args.expect, re.IGNORECASE | re.MULTILINE) if args.expect else None
        if args.mode == "native":
            accept = "text/markdown, application/markdown;q=0.9"
        elif args.mode in {"html", "browser", "clean"}:
            accept = "text/html, application/xhtml+xml;q=0.9"
        else:
            accept = "text/markdown, text/html;q=0.9, application/xhtml+xml;q=0.9, */*;q=0.1"
        with tempfile.TemporaryDirectory(prefix="fetch-url-markdown.") as directory:
            workdir = Path(directory)
            item = acquire(args.url, workdir, timeout=args.timeout, allow_private=args.allow_private,
                           allow_sensitive_query=args.allow_sensitive_query, accept=accept)
            handoff = document_route(item)
            if handoff:
                if args.mode != "auto":
                    raise ConversionError(f"document handoff is available only in auto mode, not {args.mode}")
                print(json.dumps(create_handoff(item, *handoff), ensure_ascii=False), file=sys.stderr)
                return HANDOFF_EXIT
            mode = args.mode
            if mode == "native" or (mode == "auto" and item.content_type in MARKDOWN_TYPES):
                if item.content_type not in MARKDOWN_TYPES:
                    raise ConversionError(f"native mode requires Markdown, got {item.content_type or 'unknown'}")
                content, method = item.body.decode("utf-8", errors="replace"), "native"
            elif mode == "browser":
                content, method = browser_to_markdown(item.final_url, workdir, timeout=args.timeout), "browser-firecrawl"
            elif mode == "clean":
                if item.content_type not in HTML_TYPES:
                    raise ConversionError(f"clean mode requires HTML/XHTML, got {item.content_type or 'unknown'}")
                content = html_to_markdown(item.body, item.final_url, workdir, timeout=args.timeout, clean=True)
                method = "firecrawl-clean"
            elif mode in {"html", "auto"}:
                if item.content_type not in HTML_TYPES:
                    raise ConversionError(f"unsupported content type: {item.content_type or 'unknown'}")
                content, method = html_to_markdown(item.body, item.final_url, workdir, timeout=args.timeout), "firecrawl-html"
            else:
                raise ConversionError(f"unsupported mode: {mode}")
            validate_content(content, min_chars=args.min_chars, expected=expected)
            write_output(content, args.output)
            metadata = {"action": "markdown", "source_url": args.url, "final_url": item.final_url,
                        "content_type": item.content_type, "method": method,
                        "redirects": item.redirects, "bytes": len(content.encode()),
                        "output": str(args.output.resolve()) if args.output else None}
            print(json.dumps(metadata, ensure_ascii=False), file=sys.stderr)
            return 0
    except (ConversionError, OSError, ValueError) as exc:
        print(f"fetch-url-markdown: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
