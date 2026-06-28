# ast-grep Commands Reference

## Sources

- Official quick start: https://ast-grep.github.io/guide/quick-start.html
- Official CLI reference: https://ast-grep.github.io/reference/cli.html
- Official Go catalog notes: https://ast-grep.github.io/catalog/go/
- GitHub repo: https://github.com/ast-grep/ast-grep
- Local tested version: `ast-grep 0.44.0`

## What ast-grep does

`ast-grep` searches and rewrites source code by abstract syntax tree shape. Patterns are written like normal code, with metavariables such as `$ARG`, `$NAME`, and `$$$BODY`.

Use it for structural code search, lint-like rule scans, codemods, and syntax-aware rewrites. Do not use it as a general replacement for `rg`.

## Installation

Check first:

```bash
ast-grep --version
ast-grep-sg --version
sg --version
ast-grep --help
```

Install options:

```bash
# Homebrew
brew install ast-grep

# MacPorts
sudo port install ast-grep

# Nix shell
nix-shell -p ast-grep

# Cargo
cargo install ast-grep --locked

# cargo-binstall
cargo binstall ast-grep

# npm
npm install --global @ast-grep/cli

# pnpm may require this after install
pnpm approve-builds

# pip
pip install ast-grep-cli

# pipx
pipx install ast-grep-cli

# Scoop on Windows
scoop install main/ast-grep

# mise
mise use -g ast-grep
```

Build from source:

```bash
git clone https://github.com/ast-grep/ast-grep.git
cd ast-grep
cargo install --path ./crates/cli --locked
```

Alias note: some installs expose `sg`, this local environment exposes `ast-grep-sg`, and Linux may already have an unrelated `sg` command. Prefer `ast-grep` in scripts, or define an explicit alias:

```bash
alias sg=ast-grep
```

## Command Map

| Need | Command |
|---|---|
| Help | `ast-grep --help` |
| List run options | `ast-grep run --help` |
| Search pattern | `ast-grep run -l go -p 'panic($ARG)' PATH` |
| Select node kind | `ast-grep run -l go -p 'func t() { panic($ARG) }' --selector call_expression PATH` |
| Print JSON | `ast-grep run -l go -p 'panic($ARG)' PATH --json=stream` |
| Print matching files | `ast-grep run -l go -p 'panic($ARG)' PATH --files-with-matches` |
| Restrict paths | `ast-grep run -l go -p 'panic($ARG)' PATH --globs '*.go'` |
| Include ignored files | `ast-grep run -l go -p 'panic($ARG)' PATH --no-ignore hidden` |
| Follow symlinks | `ast-grep run -l go -p 'panic($ARG)' PATH --follow` |
| Debug parsed query | `ast-grep run -l go -p 'errors.New($MSG)' --debug-query=ast PATH` |
| Preview rewrite | `ast-grep run -l go -p 'old($A)' -r 'new($A)' PATH` |
| Interactive rewrite | `ast-grep run -l go -p 'old($A)' -r 'new($A)' -i PATH` |
| Apply rewrite | `ast-grep run -l go -p 'old($A)' -r 'new($A)' -U PATH` |
| Search stdin | `ast-grep run --stdin -l go -p 'panic($ARG)'` |
| Scan with rule file | `ast-grep scan -r rule.yml PATH` |
| Scan with inline rule | `ast-grep scan --inline-rules "$RULE_YAML" PATH` |
| Scaffold rule | `ast-grep new rule RULE_NAME -l go` |
| Test rules | `ast-grep test -t tests` |
| Start LSP | `ast-grep lsp` |
| Shell completions | `ast-grep completions bash` |

## Pattern Basics

Single metavariable:

```bash
ast-grep run -l go -p 'panic($ARG)' .
```

Multiple nodes with `$$$`:

```bash
ast-grep run -l go -p 'if $COND { $$$BODY }' .
```

Function shape:

```bash
ast-grep run -l go -p 'func $NAME($$$PARAMS) $$$RET { $$$BODY }' .
```

Method receiver:

```bash
ast-grep run -l go -p 'func ($RECV *Config) $NAME($$$PARAMS) $$$RET { $$$BODY }' .
```

Error-return block:

```bash
ast-grep run -l go \
  -p 'func t() { if err != nil { return $$$ } }' \
  --selector if_statement \
  .
```

## Go Selector Call Caveat

In Go, bare selector calls like `errors.New($MSG)` can parse as type conversions. Use surrounding context and select the desired node.

Good:

```bash
ast-grep run -l go \
  -p 'func t() { errors.New($MSG) }' \
  --selector call_expression \
  .
```

Also good when searching returns:

```bash
ast-grep run -l go \
  -p 'func t() { return nil, errors.New($MSG) }' \
  --selector call_expression \
  .
```

Debug the parse tree when matches look wrong:

```bash
ast-grep run -l go -p 'errors.New($MSG)' --debug-query=ast .
```

## Output Modes

Human output:

```bash
ast-grep run -l go -p 'panic($ARG)' .
```

JSON stream:

```bash
ast-grep run -l go -p 'panic($ARG)' . --json=stream
```

Pretty JSON:

```bash
ast-grep run -l go -p 'panic($ARG)' . --json=pretty
```

Files with matches:

```bash
ast-grep run -l go -p 'panic($ARG)' . --files-with-matches
```

Context:

```bash
ast-grep run -l go -p 'panic($ARG)' . -A 2 -B 2
```

## Rewrite

Preview before applying:

```bash
ast-grep run -l ts -p '$PROP && $PROP()' -r '$PROP?.()' src
```

Review interactively:

```bash
ast-grep run -l ts -p '$PROP && $PROP()' -r '$PROP?.()' --interactive src
```

Apply all:

```bash
ast-grep run -l ts -p '$PROP && $PROP()' -r '$PROP?.()' --update-all src
```

Rule: never run `--update-all` on a broad pattern until the match set has been inspected.

## Rule Scan

Inline rule:

```bash
RULE_YAML='id: no-panic
language: Go
rule:
  pattern: panic($ARG)
message: avoid panic
severity: warning'

ast-grep scan --inline-rules "$RULE_YAML" . --report-style short
```

Rule file:

```yaml
id: no-panic
language: Go
rule:
  pattern: panic($ARG)
message: avoid panic
severity: warning
```

Run:

```bash
ast-grep scan -r no-panic.yml .
```

Scaffold a rule:

```bash
ast-grep new rule no-panic -l go
```

Test rule fixtures:

```bash
ast-grep test -t tests
```

## Practical Go Examples

Find panic calls:

```bash
ast-grep run -l go \
  -p 'func t() { panic($ARG) }' \
  --selector call_expression \
  .
```

Find `errors.New(...)` calls:

```bash
ast-grep run -l go \
  -p 'func t() { errors.New($MSG) }' \
  --selector call_expression \
  .
```

Find error-return blocks:

```bash
ast-grep run -l go \
  -p 'func t() { if err != nil { return $$$ } }' \
  --selector if_statement \
  .
```

Find `*Config` methods:

```bash
ast-grep run -l go \
  -p 'func ($RECV *Config) $NAME($$$PARAMS) $$$RET { $$$BODY }' \
  .
```

Find function declarations:

```bash
ast-grep run -l go \
  -p 'func $NAME($$$PARAMS) $$$RET { $$$BODY }' \
  .
```

## ast-grep vs rg

| Use case | Tool |
|---|---|
| Find a string anywhere | `rg` |
| Find code regardless of formatting | `ast-grep` |
| Avoid comments and string literals | `ast-grep` |
| Capture AST parts for review or rewrite | `ast-grep` |
| Very fast first-pass repo discovery | `rg` |
| Mechanical code rewrite by syntax pattern | `ast-grep` |

Observed local benchmark on `xray-core`: simple `panic(...)` text search was about 60x faster with `rg` than `ast-grep`. This confirms the decision rule: `rg` first for broad search, `ast-grep` for syntax-shaped questions.

## Troubleshooting

No matches:

1. Confirm language: `-l go`, `-l ts`, `-l js`, etc.
2. Run `--debug-query=ast`.
3. Add surrounding code context.
4. Add `--selector NODE_KIND`.
5. Use `rg` to confirm the text exists.

Too many matches:

1. Add `--selector`.
2. Add more surrounding syntax.
3. Restrict with `--globs`.
4. Search a smaller path first.

Rewrite looks risky:

1. Remove `-U` or `--update-all`.
2. Use `--interactive`.
3. Save JSON output for review.
4. Run tests after applying changes.
