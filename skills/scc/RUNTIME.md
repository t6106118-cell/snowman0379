# Runtime provisioning

This file documents the scc runtime used by the `scc` skill. Keep repository
measurement procedure in `SKILL.md`; use this file for installation,
verification, and upgrades.

## Source and installed state

- Upstream: `https://github.com/boyter/scc`
- Nova version: official release/tag `v4.0.0`, annotated tag peeled to commit
  `032a71fabf62e2651bdf9f920e4e9a7372c2582e`.
- Asset: `scc_Linux_x86_64.tar.gz`.
- Asset SHA-256:
  `b8535fb0714dd33c5434c24de181e4d1a632e6a1f869e1985bbd10ad8b838545`.
- Root: `~/.local/opt/fedora44-tools/scc/4.0.0/` containing `scc`, `README.md`,
  and `LICENSE`.
- PATH: `~/.local/bin/scc` points to the versioned executable.
- Installed binary SHA-256:
  `c45f2eb1f33a621f12aefeacacf4684ec71b9ff63d6a3e911f7e7ee208509409`.

The installed command is a stripped static Linux x86-64 Go executable. It is
not RPM-owned. The skill is validated against the 4.0.0 CLI and schemas;
upstream can have newer releases without changing nova's recorded state.

## Install

Download the exact official asset, verify the upstream-published digest, and
inspect archive member paths before extraction:

```bash
curl --fail --location --output /tmp/scc_Linux_x86_64.tar.gz \
  https://github.com/boyter/scc/releases/download/v4.0.0/scc_Linux_x86_64.tar.gz
printf '%s  %s\n' \
  b8535fb0714dd33c5434c24de181e4d1a632e6a1f869e1985bbd10ad8b838545 \
  /tmp/scc_Linux_x86_64.tar.gz | sha256sum --check
tar -tzf /tmp/scc_Linux_x86_64.tar.gz
install -d "$HOME/.local/opt/fedora44-tools/scc/4.0.0" "$HOME/.local/bin"
tar -xzf /tmp/scc_Linux_x86_64.tar.gz \
  -C "$HOME/.local/opt/fedora44-tools/scc/4.0.0"
ln -s "$HOME/.local/opt/fedora44-tools/scc/4.0.0/scc" \
  "$HOME/.local/bin/scc"
```

The expected archive contains only `scc`, `README.md`, and `LICENSE`. Use the
asset matching the target OS and architecture, adapt `fedora44-tools` to the
host convention, and inspect existing roots and links before changing them.
Ensure `~/.local/bin` is already on PATH. Building from source is unnecessary
for this baseline; if required, pin the same tag/commit and record the Go
toolchain because the resulting binary hash can differ.

## Expected commands and verification

```bash
type -a scc
scc --version
scc --help
scc --no-cocomo /path/to/small/repository
scc --format json --by-file --no-cocomo /path/to/small/repository
```

Expect `scc version 4.0.0`, valid human and JSON output, and exact file rows in
the by-file result. Before promoting a build, also exercise complexity,
`--cognitive`, `--percent`, `--dryness` or `--uloc`, `--locomo`, bounded Git
history (`--by-author`, `--timeline`, `--hotspots`, and `--coupling`), repeated
`--ignore-file`, configuration precedence, and an explicit HTML report.

The optional MCP surface is process-local stdio. Verify it with
`scc --mcp`, an MCP initialize request, `tools/list`, and one bounded tool call;
do not add it to Codex configuration merely because the binary supports it.

## Upgrade or rebuild

Inspect upstream release notes, tag provenance, asset digest, archive paths,
and CLI/schema changes. Install a candidate into a new versioned root and run
the full representative matrix above before switching the public symlink.
Retain the prior root until rollback is unnecessary. Update `SKILL.md` and its
command guide only when accepted behavior or schemas change; update this file
and the inventory with the release, commit, asset, digest, path, binary hash,
and verification result.
