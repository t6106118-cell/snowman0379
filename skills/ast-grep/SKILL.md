---
name: ast-grep
description: Syntax-aware code search, inspection, lint scanning, and code rewriting with ast-grep. Use when Codex needs to install or verify ast-grep, find code by AST structure instead of text, avoid matches in comments/strings, capture metavariables such as call arguments or receivers, write YAML scan rules, perform interactive or in-place structural rewrites, debug ast-grep patterns, or decide whether ast-grep is better than rg for a code-search task.
---

# ast-grep

## Decision Rule

Use `rg` first for broad discovery and plain text. Use `ast-grep` when the request depends on code structure.

| Task | Prefer |
|---|---|
| Find names, strings, docs, comments, paths, config keys | `rg` |
| Find real syntax nodes and avoid comments/strings | `ast-grep` |
| Capture call arguments, receivers, function names, or bodies | `ast-grep` |
| Run reusable syntax checks across many files | `ast-grep scan` |
| Rewrite code by syntax shape | `ast-grep run -r` |

## Workflow

1. Verify availability:

```bash
ast-grep --version
ast-grep --help
```

2. If missing, choose an install method from `references/commands.md`.

3. Start with `rg` unless the target is a syntax shape. Use `ast-grep` once the language and pattern are clear.

4. For Go selector calls, avoid bare selector-call patterns. Wrap them in valid code context and add `--selector call_expression`.

5. Before rewriting in place, inspect matches first. Prefer `--interactive` for broad edits.

6. When command syntax is uncertain, read `references/commands.md`.

## Quick Commands

```bash
ast-grep run -l go -p 'panic($ARG)' PATH
ast-grep run -l go -p 'func t() { panic($ARG) }' --selector call_expression PATH
ast-grep run -l go -p 'func t() { errors.New($MSG) }' --selector call_expression PATH
ast-grep run -l go -p 'func t() { if err != nil { return $$$ } }' --selector if_statement PATH
ast-grep run -l go -p 'old($A)' -r 'new($A)' PATH
ast-grep scan -r rule.yml PATH
```

## References

Read [references/commands.md](references/commands.md) when the task asks about installation, exact command usage, YAML rules, rewrites, language-specific caveats, or practical examples.
