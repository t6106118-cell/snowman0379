---
name: scc
description: Repository measurement and Git-history signals with scc. Use when Codex needs language/LOC composition, per-file size or complexity triage, ULOC/DRYness or LOCOMO signals, machine-readable metrics, HTML reports, hotspots, coupling, or author/timeline history from an installed scc 4.x binary.
---

# scc

Use `scc` for repository structure and history measurement. It is not a
replacement for `rg` (content search), `fd`/`find` (path discovery), `git`
(ordinary version-control operations), profilers (runtime performance), or
linters/static analyzers (correctness and style).

## Before running

Verify the executable and release before selecting version-specific flags:

```bash
command -v scc
scc --version
scc --help
```

This package is validated against scc 4.0.0. If `scc` is absent or an older
release lacks a needed flag, report that rather than silently installing a
binary. This skill does not install scc or register an MCP server.

Set `repo=/path/to/repository` and choose the narrowest route that answers the
question:

| Repository question | v4 route |
|---|---|
| Language mix, files, lines, code/comments/blanks | `scc --no-cocomo "$repo"` |
| Fast size pass without complexity | `scc --no-complexity --no-cocomo "$repo"` |
| Exact file rows or largest/most complex files | `scc --format json --by-file --no-cocomo "$repo"`, then filter JSON with `jq` |
| Cyclomatic/structural complexity | `scc --format json --by-file --no-cocomo "$repo"` |
| Nesting-weighted cognitive complexity | add `--cognitive` |
| Duplication/uniqueness signal | `scc --dryness --no-cocomo "$repo"` or `--uloc` |
| LLM regeneration-cost signal | `scc --locomo --no-cocomo "$repo"`; use `--cost-comparison` only when both estimates are wanted |
| Historical ownership/activity | from a Git repository root, `--by-author` and/or `--timeline` |
| Frequently changed, complex files | `--hotspots` (bound history with `--depth N`) |
| Files that change together / likely blast radius | `--coupling` or `--coupling-for FILE` |
| Additional exclusion rules | repeat `--ignore-file FILE` |
| Agent/tool integration | optional `scc --mcp` stdio only when direct CLI output is insufficient |

For Codex processing, prefer `--format json`; add `--percent` for percentage
fields. Use `--format csv` for tabular pipelines and an explicit
`--report=PATH.html` for a shareable HTML report. Read
[references/command-guide.md](references/command-guide.md) for v4 schemas,
history/configuration/ignore details, MCP messages, and worked command forms.

## Interpret results in context

- Complexity, cognitive complexity, ULOC/DRYness, LOCOMO, hotspots, and
  coupling are evidence or triage signals; none alone proves a defect, poor
  design, quality score, ownership risk, or required refactor.
- Git reports depend on repository history and can be much slower than a
  working-tree count. Use `--depth` deliberately and say what window was used.
- Keep generated/minified/large-file and ignore policies consistent before
  comparing runs.
- Use exact paths from JSON/CSV rather than parsing human tables; investigate
  flagged files with normal code reading, tests, `rg`, and language tooling.

MCP is an optional process-local stdio surface. If used, initialize it and
inspect `tools/list` before calling a tool; do not add it to Codex
configuration merely because the binary supports it.
