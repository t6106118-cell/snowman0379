# scc 4.0.0 command guide

This reference describes the released scc 4.0.0 command surface exercised for
this package. Start with `scc --help` and `scc --version` on the live machine:
packaged binaries may be older or newer. These commands measure a working tree
or Git history; they do not prove correctness, runtime performance, or security.

## Choose the analysis

Set a quoted path before running examples:

```bash
repo=/path/to/repository
```

| Question | Command |
|---|---|
| Language composition and line counts | `scc --no-cocomo "$repo"` |
| Fast count without complexity calculation | `scc --no-complexity --no-cocomo "$repo"` |
| Per-file rows | `scc --format json --by-file --no-cocomo "$repo"` |
| Largest files | per-file JSON, then sort by `.Lines` or `.Code` with `jq` |
| Cyclomatic/structural complexity | per-file JSON, sort by `.Complexity` with `jq` |
| Cognitive complexity | add `--cognitive`; inspect `.Cognitive` in the same JSON rows |
| ULOC/DRYness signal | `scc --dryness --no-cocomo "$repo"` (or `--uloc`) |
| LLM regeneration-cost estimate | `scc --locomo --no-cocomo "$repo"` |
| COCOMO plus LOCOMO | `scc --cost-comparison "$repo"` |
| Files with high complexity and churn | `scc --hotspots --depth 100 "$repo"` |
| Repository-wide temporal coupling | `scc --coupling --depth 100 "$repo"` |
| Blast radius of one file | `scc --coupling-for path/to/file.go --depth 100 "$repo"` |
| Author ownership rollup | `scc --by-author --depth 100 "$repo"` |
| Language or author activity over time | `scc --timeline --depth 100 "$repo"` (add `--by-author` for author timeline) |

The Git reports are mutually exclusive. They need a path inside a Git
repository and walk history in-process; they do not invoke the `git` executable.
Use `--depth N` to bound work (`0` means the entire history). A short or shallow
history can legitimately produce empty hotspots/coupling rows.

Do not pass working-tree-only flags such as `--no-cocomo` to history reports;
the released binary rejects that combination. The history reports use their
own JSON envelopes and window metadata.

## Structured output

Prefer JSON whenever Codex needs exact paths or further filtering:

```bash
scc --format json --by-file --no-cocomo "$repo" > counts.json
jq '[.[].Files[]] | sort_by(-.Complexity)[:20] |
    map({location: .Location, language: .Language, lines: .Lines,
         code: .Code, complexity: .Complexity})' counts.json
```

Without `--by-file`, `--format json` is an array of per-language objects. The
observed v4 fields include `Name`, `Bytes`, `Lines`, `Code`, `Comment`, `Blank`,
`Complexity`, `Count`, `WeightedComplexity`, `Files`, `LineLength`, and `ULOC`.
With `--by-file`, each language object's `Files` array contains rows including
`Location`, `Filename`, `Language`, `Lines`, `Code`, `Comment`, `Blank`,
`Complexity`, `WeightedComplexity`, `Generated`, `Minified`, and `Uloc`.
Treat additional fields as versioned output, not a reason to parse terminal
tables.

Add `--cognitive` to include `Cognitive` at language and file level. Add
`--percent` to include `CodePercent`, `CommentPercent`, `BlankPercent`,
`LinePercent`, `ComplexityPercent`, `BytePercent`, and `FilePercent`. Percentages
are relative to the current scan and policy; they are not quality scores.

Other stable machine-oriented formats include `csv`, `csv-stream`, `json2`,
`openmetrics`, `sql`, `sql-insert`, and `cloc-yaml`. Use `--format-multi` only
when explicit command-line output paths are wanted, for example:

```bash
scc --format-multi 'tabular:stdout,json:counts.json,csv:counts.csv' \
  --no-cocomo "$repo"
```

## Scope and exclusion policy

Keep scope explicit and consistent when comparing runs:

```bash
scc --include-ext go,rs,py --no-cocomo "$repo"
scc --exclude-ext md,csv --no-cocomo "$repo"
scc --exclude-dir vendor,node_modules --no-cocomo "$repo"
scc --exclude-file package-lock.json --no-cocomo "$repo"
scc --not-match '(_test\.go|vendor/)' --no-cocomo "$repo"
```

Generated, minified, duplicate, and large-file policies affect totals. Make
them explicit with `--gen`/`--no-gen`, `--min`/`--no-min`, `--no-duplicates`,
`--no-large`, and the corresponding size thresholds when an audit requires it.
Use `--count-ignore` only when the ignore files themselves should be counted.

An additional ignore file uses gitignore syntax and is anchored at the scan
root:

```bash
scc --ignore-file "$repo/team.ignore" --ignore-file "$repo/personal.ignore" \
  --no-cocomo "$repo"
```

The flag is repeatable; later supplied files can re-include an earlier match.
In-tree `.gitignore`, `.ignore`, and `.sccignore` rules take precedence over
supplied files. `--no-gitignore`, `--no-ignore`, and `--no-scc-ignore` disable
those respective in-tree rule sources when intentionally auditing ignored
content.

## Configuration

Configuration files are option lists (one flag per line; comments and quoted
values are supported). They cannot inject positional count paths. Precedence is
global source < project source < command line:

- There is no implicit global file. Set `SCC_CONFIG_PATH` or pass
  `--config PATH`; `--config` overrides the environment value.
- By default the project file is `./.sccconfig` relative to the current working
  directory. Path arguments do not change that anchor.
- `--find-root-config` walks upward to the Git/Hg root to find the project file.
- `--no-config` disables automatic global/project discovery. An explicit
  `--config PATH` is still honored and is the sole config source in that mode.
- Config can select formats and analysis flags but cannot make scc write files;
  `--output`, `--report`, and `--format-multi` file destinations are honored
  only when supplied on the command line.

Example:

```bash
printf '%s\n' '--no-cocomo' '--exclude-dir vendor' > "$repo/team.sccconfig"
(cd "$repo" && scc --config team.sccconfig .)
```

For a user-global option list, use an explicit path and keep it reviewable:

```bash
export SCC_CONFIG_PATH="$HOME/.config/scc/global.sccconfig"
scc --format json "$repo"
```

Do not assume a project config in a parent directory is read unless
`--find-root-config` is present. Keep file-writing flags on the command line.

## ULOC, complexity, and LOCOMO

`--dryness` implies `--uloc` and reports unique lines plus a DRYness percentage.
Use it to find duplication/uniqueness signals, then inspect the code; a low or
high value is not a design verdict.

Cyclomatic complexity is a rough structural triage measure. `--cognitive`
adds a nesting-weighted signal. Both depend on language parsers and scan policy.

LOCOMO (`--locomo`) estimates the cost to regenerate known code with an LLM;
`--cost-comparison` shows it beside COCOMO. LOCOMO is an experimental heuristic,
not an industry-standard quality or project-cost forecast. Presets are
`large`, `medium`, `small`, and `local`; override pricing or review assumptions
only when the resulting assumptions are recorded.

## Git insight reports

The JSON envelopes observed in v4 include a `report` name and a `window` with
`depth`, commit count, and date range. The report-specific payloads are:

- `--hotspots`: `files` rows with `file`, `language`, `complexity`, `commits`,
  `linesChanged`, `authors`, `codeChurn`, `commentChurn`, and normalized `score`.
  The score identifies high complexity × churn candidates, not defect
  probability.
- `--coupling`: `pairs` with `fileA`, `fileB`, `shared`, `commitsA`, `commitsB`,
  and `degree`; pairs need repeated shared history to appear.
- `--coupling-for FILE`: `target`, `targetCommits`, and `partners` with shared
  commits and conditional/reverse coupling values. This is a historical blast
  radius signal, not a dependency graph.
- `--by-author`: `busFactor` and `authors` ownership/last-touch fields.
- `--timeline`: language activity series; adding `--by-author` changes it to an
  author timeline.

History is evidence about the selected window. It can be incomplete in shallow
clones, distorted by mass rewrites, or unrepresentative of current ownership.

## HTML reports

Use an explicit destination in automation:

```bash
scc --report="$repo/scc-report.html" --report-title "repository" \
  --report-skip cocomo "$repo"
```

The report is a self-contained HTML document. Bare `--report` defaults to
`scc-report.html` and prompts before overwriting; explicit `--report=PATH` is
deterministic. `--report-skip` accepts comma-separated sections such as
`cocomo`, `locomo`, `hotspots`, `coupling`, `authors`, `timeline`, `files`,
`uloc`, `linelength`, and `card`.

## Optional MCP stdio

Use MCP only when a process-local structured tool surface materially improves
an agent workflow over direct shell calls. Start it as a child process:

```bash
scc --mcp
```

It speaks newline-delimited JSON-RPC over stdin/stdout. Initialize first, then
call `tools/list`; the v4.0.0 binary exposes `analyze`, `hotspots`, and
`coupling`. The `analyze` tool accepts fields such as `path`, `by_file`,
`cognitive`, `locomo`, `include_ext`, `exclude_ext`, `no_duplicates`, `no_min_gen`,
`sort`, and `limit`. The `hotspots` tool accepts `path`, `depth`, and `limit`;
`coupling` accepts `path`, `depth`, `limit`, and an optional `file` for a
per-file blast-radius view.

Inspect each returned schema rather than guessing argument names. MCP does not
change the no-install boundary: do not add this process to
`~/.codex/config.toml`, and do not leave a background server running merely
because the binary supports stdio mode.

## Boundaries and follow-up

Use the metrics to choose what to read or test next. Use `rg`, `fd`/`find`,
`git`, AST tools, linters, tests, and profilers for the questions they answer
better. Preserve the scan path, release, flags, ignore rules, and history depth
when recording or comparing results.
