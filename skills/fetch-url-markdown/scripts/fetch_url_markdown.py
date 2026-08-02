#!/usr/bin/env python3
"""Fetch a public URL as Markdown using local tools only."""

from __future__ import annotations

import argparse
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
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit


SENSITIVE_QUERY_KEYS = {
    "access_token",
    "api_key",
    "apikey",
    "auth",
    "authorization",
    "code",
    "credential",
    "key",
    "password",
    "secret",
    "sig",
    "signature",
    "token",
    "x-amz-credential",
    "x-amz-signature",
    "x-goog-credential",
    "x-goog-signature",
}

MARKDOWN_CONTENT_TYPES = {
    "application/markdown",
    "text/markdown",
    "text/x-markdown",
}


class ConversionError(RuntimeError):
    """A conversion route failed or returned unusable content."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch an HTTP(S) URL as Markdown using local tools only."
    )
    parser.add_argument("url", help="Public HTTP(S) URL to fetch")
    parser.add_argument("-o", "--output", type=Path, help="Markdown output path")
    parser.add_argument(
        "--mode",
        choices=("auto", "native", "markitdown", "browser"),
        default="auto",
        help="Conversion route (default: auto)",
    )
    parser.add_argument(
        "--expect",
        help="Case-insensitive regex that must occur in extracted Markdown",
    )
    parser.add_argument(
        "--min-chars",
        type=int,
        default=200,
        help="Minimum non-whitespace characters for usable output (default: 200)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=45,
        help="Per-command timeout in seconds (default: 45)",
    )
    parser.add_argument("--force", action="store_true", help="Replace output file")
    parser.add_argument(
        "--allow-private",
        action="store_true",
        help="Allow localhost/private-network targets",
    )
    parser.add_argument(
        "--allow-sensitive-query",
        action="store_true",
        help="Allow query keys commonly used for credentials or signatures",
    )
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
    address = ipaddress.ip_address(value)
    return not address.is_global


def validate_url(
    url: str, *, allow_private: bool, allow_sensitive_query: bool
) -> None:
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
            raise ConversionError(
                "sensitive query key(s) rejected: " + ", ".join(sensitive)
            )

    if allow_private:
        return

    host = parsed.hostname.rstrip(".").casefold()
    if host == "localhost" or host.endswith((".localhost", ".local", ".internal")):
        raise ConversionError("localhost/private-network host rejected")

    try:
        if is_nonpublic_address(host):
            raise ConversionError("non-public IP address rejected")
        return
    except ValueError:
        pass

    try:
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
    except ValueError as exc:
        raise ConversionError(f"invalid URL port: {exc}") from exc

    try:
        answers = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise ConversionError(f"hostname resolution failed: {exc}") from exc

    addresses = {answer[4][0] for answer in answers}
    if not addresses:
        raise ConversionError("hostname resolved to no addresses")
    blocked = sorted(address for address in addresses if is_nonpublic_address(address))
    if blocked:
        raise ConversionError(
            "hostname resolves to non-public address(es): " + ", ".join(blocked)
        )


def require_command(names: tuple[str, ...]) -> str:
    for name in names:
        command = shutil.which(name)
        if command:
            return command
    raise ConversionError("required command not found: " + " or ".join(names))


def run_command(
    command: list[str],
    *,
    timeout: int,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            env=env,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise ConversionError(f"command timed out after {timeout}s: {command[0]}") from exc


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def validate_content(
    content: str, *, min_chars: int, expected: re.Pattern[str] | None
) -> None:
    visible = content.strip()
    if len(visible) < min_chars:
        raise ConversionError(
            f"output too small: {len(visible)} characters; minimum is {min_chars}"
        )
    if expected and not expected.search(content):
        raise ConversionError(f"output does not match --expect regex: {expected.pattern}")


def convert_native(
    url: str,
    workdir: Path,
    *,
    timeout: int,
    min_chars: int,
    expected: re.Pattern[str] | None,
    allow_private: bool,
    allow_sensitive_query: bool,
) -> tuple[str, str]:
    curl = require_command(("curl",))
    body = workdir / "native-body"
    result = run_command(
        [
            curl,
            "--silent",
            "--show-error",
            "--location",
            "--fail-with-body",
            "--compressed",
            "--max-time",
            str(timeout),
            "--proto",
            "=http,https",
            "--proto-redir",
            "=http,https",
            "--header",
            "Accept: text/markdown",
            "--output",
            str(body),
            "--write-out",
            "%{http_code}\n%{content_type}\n%{url_effective}",
            url,
        ],
        timeout=timeout + 5,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or f"curl exit {result.returncode}"
        raise ConversionError(detail)
    lines = result.stdout.splitlines()
    if len(lines) < 3:
        raise ConversionError("curl returned incomplete response metadata")
    status, content_type = lines[0], lines[1].split(";", 1)[0].strip().lower()
    final_url = "\n".join(lines[2:]).strip()
    if status != "200":
        raise ConversionError(f"unexpected HTTP status: {status}")
    validate_url(
        final_url,
        allow_private=allow_private,
        allow_sensitive_query=allow_sensitive_query,
    )
    if content_type not in MARKDOWN_CONTENT_TYPES:
        raise ConversionError(f"origin did not return Markdown: {content_type or 'unknown'}")
    content = read_text(body)
    validate_content(content, min_chars=min_chars, expected=expected)
    return content, final_url


def convert_markitdown(
    url: str,
    workdir: Path,
    *,
    timeout: int,
    min_chars: int,
    expected: re.Pattern[str] | None,
) -> tuple[str, str]:
    markitdown = require_command(("markitdown",))
    output = workdir / "markitdown.md"
    result = run_command(
        [markitdown, url, "--output", str(output)],
        timeout=timeout,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or f"markitdown exit {result.returncode}"
        raise ConversionError(detail)
    content = read_text(output)
    validate_content(content, min_chars=min_chars, expected=expected)
    return content, url


def browser_command(workdir: Path, url: str) -> tuple[list[str], dict[str, str]]:
    browser = require_command(("chromium-browser", "chromium", "google-chrome"))
    profile = workdir / "browser-profile"
    profile.mkdir(mode=0o700)
    env = os.environ.copy()
    command = [
        browser,
        "--headless",
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--no-first-run",
        "--no-default-browser-check",
        f"--user-data-dir={profile}",
        "--dump-dom",
        url,
    ]

    if os.geteuid() != 0:
        return command, env

    runuser = require_command(("runuser",))
    try:
        nobody = pwd.getpwnam("nobody")
    except KeyError as exc:
        raise ConversionError("cannot run Chromium safely as root: nobody user missing") from exc
    os.chown(workdir, nobody.pw_uid, nobody.pw_gid)
    os.chown(profile, nobody.pw_uid, nobody.pw_gid)
    env.update(
        {
            "HOME": str(profile),
            "XDG_CACHE_HOME": str(profile / "cache"),
            "XDG_CONFIG_HOME": str(profile / "config"),
        }
    )
    return [runuser, "--user", "nobody", "--", *command], env


def convert_browser(
    url: str,
    workdir: Path,
    *,
    timeout: int,
    min_chars: int,
    expected: re.Pattern[str] | None,
) -> tuple[str, str]:
    command, env = browser_command(workdir, url)
    rendered = run_command(command, timeout=timeout, cwd=workdir, env=env)
    if rendered.returncode != 0:
        detail = rendered.stderr.strip() or f"Chromium exit {rendered.returncode}"
        raise ConversionError(detail)
    if not rendered.stdout.strip():
        raise ConversionError("Chromium returned an empty DOM")

    html = workdir / "rendered.html"
    html.write_text(rendered.stdout, encoding="utf-8")
    output = workdir / "browser.md"
    pandoc = require_command(("pandoc",))
    converted = run_command(
        [
            pandoc,
            "--from",
            "html",
            "--to",
            "gfm-raw_html",
            "--wrap=none",
            str(html),
            "--output",
            str(output),
        ],
        timeout=timeout,
    )
    if converted.returncode != 0:
        detail = converted.stderr.strip() or f"pandoc exit {converted.returncode}"
        raise ConversionError(detail)
    content = read_text(output)
    validate_content(content, min_chars=min_chars, expected=expected)
    return content, url


def write_output(content: str, output: Path | None) -> None:
    if output is None:
        sys.stdout.write(content)
        if content and not content.endswith("\n"):
            sys.stdout.write("\n")
        return

    destination = output.expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=destination.parent,
        prefix=f".{destination.name}.",
        delete=False,
    ) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    os.replace(temporary, destination)


def main() -> int:
    args = parse_args()
    try:
        validate_url(
            args.url,
            allow_private=args.allow_private,
            allow_sensitive_query=args.allow_sensitive_query,
        )
        expected = (
            re.compile(args.expect, re.IGNORECASE | re.MULTILINE) if args.expect else None
        )
        routes = (
            ("native", "markitdown", "browser")
            if args.mode == "auto"
            else (args.mode,)
        )
        failures: list[str] = []
        with tempfile.TemporaryDirectory(prefix="fetch-url-markdown.") as directory:
            workdir = Path(directory)
            for route in routes:
                try:
                    if route == "native":
                        content, final_url = convert_native(
                            args.url,
                            workdir,
                            timeout=args.timeout,
                            min_chars=args.min_chars,
                            expected=expected,
                            allow_private=args.allow_private,
                            allow_sensitive_query=args.allow_sensitive_query,
                        )
                    elif route == "markitdown":
                        content, final_url = convert_markitdown(
                            args.url,
                            workdir,
                            timeout=args.timeout,
                            min_chars=args.min_chars,
                            expected=expected,
                        )
                    else:
                        content, final_url = convert_browser(
                            args.url,
                            workdir,
                            timeout=args.timeout,
                            min_chars=args.min_chars,
                            expected=expected,
                        )
                    write_output(content, args.output)
                    metadata = {
                        "bytes": len(content.encode("utf-8")),
                        "final_url": final_url,
                        "method": route,
                        "output": str(args.output.resolve()) if args.output else None,
                        "source_url": args.url,
                    }
                    print(json.dumps(metadata, ensure_ascii=False), file=sys.stderr)
                    return 0
                except (ConversionError, OSError) as exc:
                    failures.append(f"{route}: {exc}")
        raise ConversionError("; ".join(failures))
    except ConversionError as exc:
        print(f"fetch-url-markdown: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
