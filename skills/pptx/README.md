# PPTX upstream reference and system overlay

The base skill is maintained by Anthropic:

- [Official PPTX skill directory](https://github.com/anthropics/skills/tree/main/skills/pptx)
- [Current instructions](https://raw.githubusercontent.com/anthropics/skills/main/skills/pptx/SKILL.md)
- [Upstream license](https://github.com/anthropics/skills/blob/main/skills/pptx/LICENSE.txt)

This directory has three original documents: a thin SKILL.md entrypoint, this
README, and SYSTEM_OVERLAY.md. It carries no Anthropic scripts, schemas, or
copied guide. Keep upstream improvements in the base and environment-specific
adjustments in the overlay.

## Use

Install the official bundle separately using your usual skill installer and
Anthropic's repository path `skills/pptx`. Keep this overlay outside that base
installation so an upstream refresh cannot overwrite it. The entrypoint can
also be read directly from this repository; it delegates to the current guide
and then applies the overlay.

If installing this entrypoint as your registered `pptx` skill, keep the official
helper bundle in a different directory and update its location in the overlay.
Do not overwrite the official bundle with this script-free reference directory.
On the author's workstation, the existing official bundle remains at
`/home/nova/.codex/skills/pptx`; this repository replacement did not change it.

## Updates

The links follow upstream's `main` branch, and the entrypoint instructs the agent
to read the current guide at use time. A hyperlink does not automatically update
installed scripts or dependencies. Refresh the official bundle when needed to
use new helpers or changed interfaces; this repository's overlay stays separate.
There is no background updater or vendored snapshot here. Re-check environment
facts when they affect a task; edit SYSTEM_OVERLAY.md when your system changes.

Anthropic's materials retain their upstream license. This replacement removes
the copied bundle from the current repository tree, without rewriting history.
