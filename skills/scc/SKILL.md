---
name: scc
description: Codebase measurement and source line counting with scc. Use when Codex needs to install or verify scc, triage an unfamiliar repository, count files/lines/code/comments/blanks by language, rank files by size or estimated complexity, inspect generated/minified/ignored-file counting behavior, compute ULOC/DRYness duplication signals, export code metrics as JSON/CSV/HTML/SQL/OpenMetrics, or decide whether scc is better than rg/fd/find/tokei/cloc for a codebase metrics task.
---

# scc

## Core Workflow

Use `scc` for repository measurement, not text search.

Default to:

```bash
scc --no-cocomo PATH
```

Use `rg` for content search, `fd`/`find` for path discovery, and `scc` for language mix, LOC, code/comment/blank counts, rough complexity, ULOC/DRYness, and machine-readable metrics.

## Install Or Verify

First verify:

```bash
command -v scc
scc --version
```

If missing, prefer the best available install path for the host:

```bash
# Fedora/RHEL family, when packaged or COPR is configured
dnf install -y scc

# GitHub prebuilt fallback
curl -fsSL https://api.github.com/repos/boyter/scc/releases/latest
```

For detailed install choices, release-binary workflow, and verification commands, read [references/command-guide.md](references/command-guide.md).

## Fast Command Selection

| Need | Command |
|---|---|
| Repo summary | `scc --no-cocomo PATH` |
| ASCII-safe output | `scc --ci --no-cocomo PATH` |
| Per-file rows | `scc --by-file --no-cocomo PATH` |
| Largest code areas | `scc --sort code --no-cocomo PATH` |
| Highest rough complexity files | `scc --by-file --sort complexity --no-cocomo PATH` |
| Faster large-repo first pass | `scc --no-complexity --no-cocomo PATH` |
| Only some extensions | `scc --include-ext go,rs,py --no-cocomo PATH` |
| Exclude extensions | `scc --exclude-ext md,csv --no-cocomo PATH` |
| Exclude directories | `scc --exclude-dir vendor,node_modules --no-cocomo PATH` |
| JSON for `jq` | `scc --format json --no-cocomo PATH` |
| CSV for tabular tools | `scc --format csv --no-cocomo PATH` |
| Duplicate/unique line signal | `scc --dryness --no-cocomo PATH` |
| Multiple reports | `scc --format-multi 'tabular:stdout,json:report.json,csv:report.csv' --no-cocomo PATH` |

## Automation Patterns

Use JSON when exact paths or later filtering matter:

```bash
scc --format json --by-file --no-cocomo PATH \
  | jq '.[].Files | sort_by(-.Complexity)[:10]'
```

Use CSV when handing results to `qsv`, `mlr`, spreadsheets, or reports:

```bash
scc --format csv --no-cocomo PATH > scc-report.csv
```

Use `--no-cocomo` unless the user explicitly wants cost/schedule/people estimates.

Use `--no-complexity` for a faster first pass when complexity is not needed.

## Interpretation Rules

- Treat complexity as a rough triage signal, not proof of risk or bad code.
- Treat `--dryness`/ULOC as a duplication smell, not a design verdict.
- Use JSON/CSV instead of terminal tables when exact paths matter because terminal paths can be truncated.
- Check ignore/generated/minified flags when metrics must be auditable.
- After `scc` identifies target areas, inspect files normally with `rg`, code reading, tests, language tools, or AST/static-analysis tools.

## Detailed Reference

Read [references/command-guide.md](references/command-guide.md) when a task needs:

- Installation from GitHub release binaries.
- Full command examples and output formats.
- Include/exclude, ignore, generated, minified, and remap behavior.
- JSON/CSV/OpenMetrics/SQL export details.
- Practical examples from real repos.
- Comparison against `rg`, `fd`, `find`, `tokei`, and `cloc`.
