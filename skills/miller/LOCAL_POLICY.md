# Miller direct-shell policy

When Codex uses Miller (`mlr`) directly through the shell for agent-generated
data inspection, transformation, validation, or exploratory analysis, prefer:

    mlr --no-shell ...

unless the task genuinely requires Miller to invoke an external command.

Do not persistently set `MLR_NO_SHELL=1`; keep the restriction command-scoped
so legitimate user-requested `system()`, `exec()`, or `--prepipe` workflows
remain available.

Before allowing Miller shell-outs, require a concrete task need rather than
using them as an implementation convenience.

Keep the official Miller Agent Skill under `~/.codex/skills/miller/`
unchanged and upstream-identical.
