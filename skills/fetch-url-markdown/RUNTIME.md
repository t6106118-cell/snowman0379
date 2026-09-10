# Firecrawl runtime provisioning

This file documents the two local adapter commands used by
`fetch-url-markdown`. They are not upstream Firecrawl command packages. Keep
normal skill execution in `SKILL.md`; use this file only to provision, verify,
rebuild, or upgrade the adapters.

## Pinned sources

| Command | Upstream library | Pinned revision |
|---|---|---|
| `firecrawl-html-to-markdown` | `https://github.com/firecrawl/html-to-markdown` | `1af9901a5d6101621120204f7ea3f5355fd5ea31` |
| `firecrawl-html-extractor` | `https://github.com/firecrawl/html-extractor` | `0a2b7432a20e356c2254f17e1b0acb2e79d88917` |

The Go manifest uses pseudo-version
`v0.0.0-20260312013131-1af9901a5d61`, whose module checksum is
`h1:UBDJu23HX7g13QTJGMf1PlI1MVPTQk9o/AISxgt2axo=`. The Rust manifest pins the
full Git revision and resolves upstream package `html-extractor 0.1.0`.

## Wrapper source

The exact recovered source tree on nova is:

```text
/home/nova/.ssh/codex-state/firecrawl-wrappers/
|-- firecrawl-html-to-markdown/
|   |-- go.mod
|   `-- main.go
`-- firecrawl-html-extractor/
    |-- Cargo.toml
    `-- src/
        `-- main.rs
```

Copy both complete project directories to the host being provisioned. The
authored recovery does not contain the original generated `go.sum` or
`Cargo.lock`. A later Fedora build on `crafty-rope` generated and retained both
under `/root/.local/src/firecrawl-wrappers/`; use those lockfiles when locked
dependency reproduction is required. Do not substitute unrelated packages
that happen to have similar command names.

## Command interfaces

```text
firecrawl-html-to-markdown [--url URL] [FILE|-]
firecrawl-html-extractor [--url URL] [--text|--json] [--metadata] [FILE|-]
```

Both commands read one file, `-`, or stdin and write content to stdout. The Go
adapter uses Firecrawl's GitHub-Flavored Markdown plugin. Its optional `--url`
must be absolute and resolves relative links; `data:` URLs remain unchanged.

The Rust adapter emits extracted Markdown by default. `--json` adds page type,
extraction quality, and fallback status; `--metadata` writes those fields to
stderr; `--text` requests upstream plain text; and `--text` and `--json` are
mutually exclusive. The skill uses only Markdown. At the pinned revision,
plain text can be absent, inline text can be misordered, relative links can
remain unresolved, listing links can be discarded, and page chrome can
remain. Clean extraction must remain explicit rather than an automatic
fallback.

## Build dependencies

- Both: Git, HTTPS CA certificates, and network access to the Go or Cargo
  dependency sources.
- Go adapter: Go 1.20 or newer. Nova used Fedora Go
  `go1.26.7-X:nodwarf5` on Linux/amd64.
- Rust adapter: stable Cargo and rustc 1.78 or newer, plus a working C linker.
  Nova used Fedora Cargo/rustc 1.98.0 (`1.98.0-1.fc44`) on Linux/amd64. Rust
  nightly and `rustup` are not required.

Use host-local cache directories if desired. Caches are build inputs, not
installed runtime files.

## Build

From the copied source tree:

```bash
cd /path/to/firecrawl-wrappers/firecrawl-html-to-markdown
go mod tidy
CGO_ENABLED=0 go build -trimpath -ldflags='-s -w' \
  -o /tmp/firecrawl-html-to-markdown .

cd /path/to/firecrawl-wrappers/firecrawl-html-extractor
cargo build --release
```

`go mod tidy` generates `go.sum` and may add direct or indirect requirements
to `go.mod`. `cargo build --release` generates `Cargo.lock` when absent. Retain
both resulting manifests with the source used for the build. For a locked
rebuild, restore those files first and use `go mod download` followed by the
same `go build` command and `cargo build --release --locked`.

Nova's original Go build additionally scoped `GOPATH`, `GOMODCACHE`, and
`GOCACHE` beneath `/tmp/firecrawl-converter-build/`. Its Rust build scoped
`CARGO_HOME` and `CARGO_TARGET_DIR` there. Those locations are not required;
the commands above preserve the material build settings.

## Install and expose on PATH

Install into versioned user-local roots named by the full upstream revision,
then expose only the tested executables through `~/.local/bin`:

```bash
install -d "$HOME/.local/opt/fedora-tools/firecrawl-html-to-markdown/1af9901a5d6101621120204f7ea3f5355fd5ea31/bin"
install -m 0755 /tmp/firecrawl-html-to-markdown \
  "$HOME/.local/opt/fedora-tools/firecrawl-html-to-markdown/1af9901a5d6101621120204f7ea3f5355fd5ea31/bin/firecrawl-html-to-markdown"

install -d "$HOME/.local/opt/fedora-tools/firecrawl-html-extractor/0a2b7432a20e356c2254f17e1b0acb2e79d88917/bin"
install -m 0755 /path/to/firecrawl-wrappers/firecrawl-html-extractor/target/release/firecrawl-html-extractor \
  "$HOME/.local/opt/fedora-tools/firecrawl-html-extractor/0a2b7432a20e356c2254f17e1b0acb2e79d88917/bin/firecrawl-html-extractor"

install -d "$HOME/.local/bin"
ln -s "$HOME/.local/opt/fedora-tools/firecrawl-html-to-markdown/1af9901a5d6101621120204f7ea3f5355fd5ea31/bin/firecrawl-html-to-markdown" \
  "$HOME/.local/bin/firecrawl-html-to-markdown"
ln -s "$HOME/.local/opt/fedora-tools/firecrawl-html-extractor/0a2b7432a20e356c2254f17e1b0acb2e79d88917/bin/firecrawl-html-extractor" \
  "$HOME/.local/bin/firecrawl-html-extractor"
```

Nova uses `~/.local/opt/fedora44-tools/` rather than the generic
`~/.local/opt/fedora-tools/` shown above. Preserve the host's established root
naming convention. Ensure `~/.local/bin` is already on `PATH`; do not change a
shell profile blindly. Inspect existing targets before creating or replacing
symlinks.

## Verify

```bash
type -a firecrawl-html-to-markdown
type -a firecrawl-html-extractor

printf '<h1>Title</h1><p><a href="/docs">Docs</a></p>' | \
  firecrawl-html-to-markdown --url https://example.com/base/ -

printf '<nav>Discard</nav><main><h1>Research Title</h1><p>This is the first substantive article paragraph.</p><p>This is the second substantive article paragraph.</p></main>' | \
  firecrawl-html-extractor -
```

The first output must contain `# Title` and
`https://example.com/docs`. The second must be nonempty, contain
`# Research Title` and both article paragraphs, and omit `Discard`. Also run
the skill's HTML and clean routes against known pages, with explicit
`--expect` and an appropriate `--min-chars` threshold.

On nova, the installed SHA-256 values are:

```text
firecrawl-html-to-markdown  8d67ecc24ea25955435b33e2bb6fede4bcd0377017e386f172c0fab3d07ab439
firecrawl-html-extractor    b81a2018827caac3360b0af195aa417c4314066419a59f450c69db2500a25a14
```

Hashes can differ across compiler and linker versions. Verify the pinned
dependency identities, interfaces, linkage expectations, and end-to-end
outputs; do not use hash equality as the only portability check.

## Upgrade or rebuild

For a rebuild of the same revisions, keep the manifests unchanged, use the
retained lockfiles, build with `--locked` where supported, install into the
existing revision roots only after successful verification, and record the
new toolchain and hashes.

For an upgrade, inspect each upstream repository and select explicit new full
commits. Change one wrapper dependency at a time, regenerate and retain its
lockfile, run upstream tests where practical, build, run the direct and skill
route checks, and install into new revision-named roots. Switch PATH symlinks
only after validation. Retain the previous roots until rollback is no longer
needed, then update this file and the workstation inventory with the new
commits, toolchains, paths, hashes, behavior changes, and known limitations.
