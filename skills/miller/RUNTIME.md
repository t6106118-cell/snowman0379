# Runtime provisioning

This file documents the Miller runtime used by the `miller` skill. Keep data
workflow instructions in `SKILL.md`. Keep `LOCAL_POLICY.md` as a separate,
authoritative local policy layer; do not merge it into either file.

## Source and installed state

- Upstream: `https://github.com/johnkerl/miller`
- Nova version: upstream release 6.21.0.
- Package: official `miller-6.21.0-linux-amd64.rpm`, installed as RPM
  `miller-6.21.0-1.x86_64`.
- Executable: `/usr/bin/mlr`, a stripped static x86-64 ELF.
- Installed binary SHA-256:
  `dc6692d37d7e42faeda7b09cf0861b7cd757f6c538072d95590a9c2aec9ed63a`.
- Release RPM SHA-256:
  `a169accdd615215ffd1b6b92aa7995c1853259493752b5559d9fde5a348750ba`.

The RPM is upstream-produced, not a Fedora build: its release is `1`, its
packager is John Kerl, and it is unsigned. Verify the downloaded digest before
installing and record that trust decision.

## Runtime modes

Miller 6.21.0 provides both the ordinary CLI and an MCP stdio server:

```text
mlr <flags> <verb> ...
mlr mcp [--allow-shell] [--timeout SECONDS] [--max-output-bytes N]
```

`mlr mcp` exposes `list_capabilities`, `which`, `validate_dsl`,
`describe_data`, and `run`, plus the Miller playbook prompt/resource. By
default its subprocesses set `MLR_NO_SHELL=1` and `MLR_ERRORS_JSON=1`, which
disables DSL `system`/`exec`, piped redirects, and `--prepipe` while returning
structured errors. Register an MCP server only when the client needs that
structured surface; its command must be `/usr/bin/mlr mcp`. Nova's installed
binary supports the server, but the current Codex configuration does not
register it.

Direct shell use remains valid. On nova, follow `LOCAL_POLICY.md`: use
`mlr --no-shell ...` for agent-generated inspection or transformation unless
a concrete user requirement needs Miller to invoke an external command. Do
not persist `MLR_NO_SHELL=1`, and do not change or publish away this local
policy layer.

## Install

On Fedora x86-64, download the pinned official RPM and verify it before the
local package transaction:

```bash
curl --fail --location --output /tmp/miller-6.21.0-linux-amd64.rpm \
  https://github.com/johnkerl/miller/releases/download/v6.21.0/miller-6.21.0-linux-amd64.rpm
printf '%s  %s\n' \
  a169accdd615215ffd1b6b92aa7995c1853259493752b5559d9fde5a348750ba \
  /tmp/miller-6.21.0-linux-amd64.rpm | sha256sum --check
sudo dnf install /tmp/miller-6.21.0-linux-amd64.rpm
```

Use the asset matching the target architecture. Do not add an external package
repository for this standalone RPM. If a maintained distribution package is
used instead, verify that it provides the required 6.21-era `mlr mcp` surface.

## Verify

```bash
type -a mlr
mlr --version
mlr mcp --help
printf 'name,value\na,1\nb,2\n' | \
  mlr --no-shell --icsv --ojson sort -f value
```

Expect version 6.21.0, the five MCP tool names in `mlr mcp --help`, and two
ordered JSON records. For an MCP registration, initialize the stdio server,
call `tools/list`, validate a small DSL expression, describe a small fixture,
and run one bounded conversion. Confirm shell-outs fail unless
`--allow-shell` was deliberately selected.

## Upgrade or rebuild

Review upstream release notes and official asset digests. Upgrade only to a
version that preserves or deliberately changes the CLI, MCP tools, structured
errors, and shell-isolation behavior expected by the skill. Install the new
RPM, rerun direct and MCP checks, and confirm `LOCAL_POLICY.md` remains separate
and unchanged. Record the new package metadata, asset and binary hashes, path,
tool catalog/schema version, and behavior in this file and the inventory.
