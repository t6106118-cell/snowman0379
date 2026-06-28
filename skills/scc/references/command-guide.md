# scc Detailed Command Guide

Use this reference when the task needs exact install commands, less-common flags, machine-readable output, or judgment about whether `scc` is the right tool.

Source basis:
- Local command help: `scc --help`
- Local version tested: `scc version 3.7.0`
- Upstream project: <https://github.com/boyter/scc>
- Practice guide source: `/root/bk3/continuous-note-taking/research/scc-command-guide-and-practice.md`

## What scc Does

`scc` means Sloc, Cloc and Code.

It reports:
- Files by language.
- Total lines, blank lines, comment lines, code lines.
- Bytes processed.
- Estimated complexity.
- Unique lines of code and DRYness with `--dryness` or `--uloc`.
- Generated/minified file handling.
- Many output formats for automation and reports.

It does not search inside files. Use `rg` for content search.

## Install And Verify

Always verify before installing:

```bash
command -v scc
scc --version
```

Expected version format:

```text
scc version 3.7.0
```

### Fedora/RHEL Family

Try the package manager first if `scc` is packaged or a COPR repo is already enabled:

```bash
dnf install -y scc
```

If the normal repo does not provide `scc`, use the GitHub prebuilt release workflow below.

### GitHub Prebuilt Binary Fallback

Use the upstream release page:

```text
https://github.com/boyter/scc/releases
```

Generic workflow:

```bash
tmpdir="$(mktemp -d)"
cd "$tmpdir"
curl -fLO "RELEASE_ASSET_URL_FOR_THIS_OS_AND_ARCH"
tar -xzf "DOWNLOADED_ARCHIVE.tar.gz"
install -m 0755 scc /usr/local/bin/scc
scc --version
```

Pick the release asset matching the host OS and architecture, for example Linux x86_64/amd64 on this environment.

If the archive format is `.zip`, use:

```bash
unzip DOWNLOADED_ARCHIVE.zip
install -m 0755 scc /usr/local/bin/scc
```

### Other Common Install Paths

Use only when appropriate for the host:

```bash
# Go toolchain
go install github.com/boyter/scc/v3@latest

# macOS Homebrew, if available
brew install scc

# Arch, if available
pacman -S scc
```

After install, record what was installed and from where.

## Best Defaults

Use this as the normal first command:

```bash
scc --no-cocomo PATH
```

Why:
- Keeps output focused on code metrics.
- Avoids rough cost/schedule/people estimates that usually do not help Codex tasks.
- Gives language/file/line/code/comment/complexity summary quickly.

Use ASCII output when terminal rendering matters:

```bash
scc --ci --no-cocomo PATH
```

Use faster counting on large repos when complexity is not needed:

```bash
scc --no-complexity --no-cocomo PATH
```

## Core Commands

| Task | Command |
|---|---|
| Quick repo summary | `scc --no-cocomo PATH` |
| Wide table | `scc --wide --no-cocomo PATH` |
| ASCII table | `scc --ci --no-cocomo PATH` |
| Per-file table | `scc --by-file --no-cocomo PATH` |
| Sort by files | `scc --sort files --no-cocomo PATH` |
| Sort by language name | `scc --sort name --no-cocomo PATH` |
| Sort by lines | `scc --sort lines --no-cocomo PATH` |
| Sort by blanks | `scc --sort blanks --no-cocomo PATH` |
| Sort by code | `scc --sort code --no-cocomo PATH` |
| Sort by comments | `scc --sort comments --no-cocomo PATH` |
| Sort by complexity | `scc --by-file --sort complexity --no-cocomo PATH` |
| Disable complexity | `scc --no-complexity --no-cocomo PATH` |
| Disable duplicate-file ignore | `scc --no-duplicates --no-cocomo PATH` |
| Show percentages | `scc --percent --no-cocomo PATH` |
| List languages | `scc --languages` |

## Include, Exclude, And Matching

| Task | Command |
|---|---|
| Include extensions | `scc --include-ext go,rs,py --no-cocomo PATH` |
| Exclude extensions | `scc --exclude-ext md,csv --no-cocomo PATH` |
| Exclude files | `scc --exclude-file package-lock.json --no-cocomo PATH` |
| Exclude dirs | `scc --exclude-dir vendor,node_modules --no-cocomo PATH` |
| Exclude path regex | `scc --not-match '(_test\\.go|vendor/)' --no-cocomo PATH` |
| Count unknown ext as a language | `scc --count-as foo:Go --no-cocomo PATH` |
| Count ignored files | `scc --count-ignore --no-cocomo PATH` |

Ignore controls:

```bash
scc --no-gitignore --no-cocomo PATH
scc --no-ignore --no-cocomo PATH
scc --no-scc-ignore --no-cocomo PATH
```

Use these only when intentionally auditing ignored files.

## Generated, Minified, And Large Files

| Task | Command |
|---|---|
| Include generated files | `scc --gen --no-cocomo PATH` |
| Exclude generated files | `scc --no-gen --no-cocomo PATH` |
| Print generated markers | `scc --generated-markers` |
| Include minified files | `scc --min --no-cocomo PATH` |
| Exclude minified files | `scc --no-min --no-cocomo PATH` |
| Exclude minified generated files | `scc --no-min-gen --no-cocomo PATH` |
| Include large files | `scc --no-large --no-cocomo PATH` |
| Set large-byte threshold | `scc --large-byte-count 2000000 --no-cocomo PATH` |
| Set large-line threshold | `scc --large-line-count 50000 --no-cocomo PATH` |

Before comparing metrics across runs, keep generated/minified/large-file policy the same.

## Output Formats

Use `--format FORMAT`.

| Format | Use |
|---|---|
| `tabular` | Human terminal summary. |
| `wide` | Wider terminal summary. |
| `json` | Best general automation format. |
| `json2` | Alternate schema with `languageSummary` and estimates. |
| `csv` | Spreadsheets, `qsv`, `mlr`, simple reports. |
| `csv-stream` | Streaming CSV pipelines. |
| `html` | Standalone HTML report. |
| `html-table` | Embeddable HTML table. |
| `sql` | SQL output. |
| `sql-insert` | SQL insert statements. |
| `openmetrics` | Prometheus/OpenMetrics scraping. |
| `cloc-yaml` | Compatibility. |
| `sloccount-format` | Compatibility. |

Examples:

```bash
scc --format json --no-cocomo PATH > scc-report.json
scc --format csv --no-cocomo PATH > scc-report.csv
scc --format openmetrics --no-cocomo PATH > scc.prom
```

Write several formats at once:

```bash
scc --format-multi 'tabular:stdout,json:report.json,csv:report.csv' --no-cocomo PATH
```

## JSON Patterns

Top languages by code:

```bash
scc --format json --no-cocomo PATH \
  | jq 'sort_by(-.Code) | .[:10] | map({Name, Files, Lines, Code, Comments, Complexity})'
```

Highest complexity files:

```bash
scc --format json --by-file --no-cocomo PATH \
  | jq '[.[].Files[]] | sort_by(-.Complexity)[:20] | map({Location, Lines, Code, Comment, Complexity})'
```

Specific extension and exact file paths:

```bash
scc --format json --by-file --include-ext go --no-cocomo PATH \
  | jq '.[0].Files | sort_by(-.Code)[:20] | map({Location, Code, Complexity})'
```

## CSV Patterns

Write a CSV report:

```bash
scc --format csv --no-cocomo PATH > scc-report.csv
```

Expected header:

```text
Language,Lines,Code,Comments,Blanks,Complexity,Bytes,Files,ULOC
```

Use CSV when the next tool is `qsv`, `mlr`, a spreadsheet, or a persistent report.

## ULOC And DRYness

Use:

```bash
scc --dryness --no-cocomo PATH
```

or:

```bash
scc --uloc --no-cocomo PATH
```

Interpretation:
- ULOC means unique lines of code.
- DRYness is a duplication signal.
- Low DRYness is a reason to inspect, not proof that the repo is poorly designed.

## Real Practice Results

Small mixed fixture:

```bash
scc --no-cocomo continuous-note-taking/data/srgn-practice
```

Observed:

| Language | Files | Lines | Code | Comments | Complexity |
|---|---:|---:|---:|---:|---:|
| Python | 1 | 25 | 14 | 3 | 0 |
| Go | 1 | 17 | 13 | 0 | 0 |
| Rust | 1 | 15 | 12 | 0 | 0 |
| Scheme | 1 | 5 | 5 | 0 | 0 |
| Plain Text | 1 | 3 | 3 | 0 | 0 |

`awesome-cli-apps-in-a-csv`:

```bash
scc --no-cocomo awesome-cli-apps-in-a-csv
```

Observed:

| Language | Files | Lines | Code | Complexity |
|---|---:|---:|---:|---:|
| Markdown | 3 | 2816 | 2503 | 0 |
| CSV | 5 | 2366 | 2366 | 0 |
| Python | 1 | 122 | 93 | 29 |

This told us the repo is mostly docs/data with one Python script to inspect.

`xray-core` Go-only pass:

```bash
scc --no-cocomo --include-ext go xray-core
```

Observed:

| Language | Files | Lines | Code | Comments | Complexity |
|---|---:|---:|---:|---:|---:|
| Go | 889 | 143602 | 121108 | 5427 | 22716 |

Highest rough complexity files:

| File | Lines | Code | Complexity |
|---|---:|---:|---:|
| `xray-core/infra/conf/transport_internet.go` | 2317 | 2105 | 634 |
| `xray-core/common/geodata/ip_matcher.go` | 1023 | 887 | 316 |
| `xray-core/proxy/freedom/freedom.go` | 826 | 744 | 252 |
| `xray-core/proxy/proxy.go` | 809 | 709 | 240 |
| `xray-core/proxy/vless/inbound/inbound.go` | 700 | 601 | 236 |

## Decision Guide

| Task | Best Tool |
|---|---|
| Find text or symbols by text | `rg` |
| Find file paths by name/type | `fd` or `find` |
| Count repo size by language | `scc` |
| Rank files by code lines | `scc --by-file --sort code` |
| Rank files by rough complexity | `scc --by-file --sort complexity` |
| Structural code search/rewrite | `ast-grep` |
| Static rule scanning | `semgrep` |
| Exact code behavior/root cause | Read code, run tests, use language tools |

Rating for Codex automation: 8/10.

Use `scc` early for repo triage. Do not use it as proof of correctness, bug location, or refactor necessity.

## Common Mistakes

- Do not use `scc` when the task is to find text. Use `rg`.
- Do not trust terminal table paths for exact file names. Use JSON/CSV.
- Do not compare two reports unless generated/minified/ignore policies match.
- Do not leave COCOMO estimates in notes unless the user asked for them.
- Do not treat complexity or DRYness as a final diagnosis.
