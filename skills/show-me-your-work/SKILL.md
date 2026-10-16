---
name: show-me-your-work
description: Keep and audit a reviewable trail of consequential decisions, reasons, evidence, and outcomes during long or unattended work, or when the user requests an audit trail. Supports figure-it-out and other coding, analysis, or research workflows; use existing project records and keep current state distinct from decision history.
license: MIT
---

# Show me your work

Maintain one canonical decision trail for the in-scope effort so someone can inspect why important choices were made and what actually happened. Record decisions and checkpoints, not every tool call. A trail supports verification; it does not replace running the work or proving the result.

## Choose the canonical record

- Read the project's local instructions and current-state record. Reuse an existing suitable decision/evidence trail and its conventions; do not create a rival history or duplicate the maintained current-state summary.
- If no suitable trail exists, use a project-local `decisions.tsv`, or a focused `.audit/<task>.tsv` for a distinct effort. Put no project state under the global skill directory. Keep the path explicit and link it from the authoritative project state, reachable through the local AGENTS index.
- The current-state record remains a maintained summary of the current objective, status and next action. The decision trail records relevant history, including abandoned approaches and corrections. Keep both consistent without copying every row into the summary.
- Do not commit or publish a trail merely because it exists. Follow existing repository conventions and actual task authorization; do not change ignore rules automatically. Keep secrets and unrelated private content out of records.

## TSV format when creating a new trail

Use [the template](references/decision-log-template.tsv). One row per material decision/checkpoint; cells are single-line.

| Column | Content |
| --- | --- |
| ts | UTC ISO8601 timestamp |
| phase | Workstream or phase; start identifies entry/resumption provenance |
| decision | What was chosen or done, in plain concrete words |
| why | Reason and material tradeoff |
| evidence | Resolvable pointer: exact command/log, file and revision, artifact, trace or authorized PR/issue reference |
| result | Actual observed outcome or explicit pending/inconclusive/unrun state |

Resolve [scripts/log.sh](scripts/log.sh) relative to this skill's directory and run it with Bash. It takes six arguments: log path, phase, decision, why, evidence, result. Use an absolute project-local log path and pass each field as one quoted argument. Do not interpolate untrusted values into shell command text.

The helper creates parent directories and the header when needed, appends a timestamped row, replaces tabs/newlines/carriage returns in fields with spaces, and prefixes formula-leading cells with a single quote for spreadsheet reading. It formats data; it does not verify claims, redact secrets, validate an existing file's schema or coordinate concurrent writers. Inspect an existing file before appending; use its established format rather than blindly treating another table as this TSV.

## Write while the work happens

- Record a meaningful fork, completed unit and its verification result, failed attempt, pivot, change of expectation, blocker or corrected gate promptly. Skip trivial actions and self-evident choices.
- Evidence must support the claim and actually exist. A script path shows an implementation; a command/result or output artifact shows execution. State if something is only planned, inferred, inconclusive or not run.
- On entry or resumption, read relevant recent rows and the current state, then check actual files/processes before trusting previous status. Do not infer chronology from random identifiers or claim authorship of another run's rows.
- For this TSV, start a new run's segment with phase start; if returning after another writer's start, add a new start row. Identify the actual exposed session/run ID when available, otherwise label a task-local run explicitly as such. Name the earlier row/time range used for context; do not invent host-issued identities.
- Use a single writer for a shared trail. Authorized workers can return evidence to the coordinator; the helper does not make unsynchronized multi-process appends safe.
- Preserve audit history when correcting it: append a superseding row that identifies the earlier row/time and the corrected fact/evidence. Do not rewrite a wrong decision into apparent success. This history rule does not make the current-state summary append-only.

## Audit the material trail

Before handoff or a meaningful review checkpoint, inspect the relevant rows against available task evidence:

- Does each consequential row describe an actual action or an explicitly labeled proposal?
- Does its pointer resolve, and does the artifact or command result establish the stated result for the relevant version/input?
- Are important failures, changed requirements, pivots and unverified steps represented without a misleading success claim?
- Do current state, pending operations and the trail agree?

Read only what is necessary to answer those questions. Use visible task messages, files, outputs and logs first. Consult a transcript only when its content is necessary, access is authorized and the host exposes the relevant session; never assume Cursor paths or sweep unrelated chats. Missing evidence remains a limitation, not a reason to invent a row.

Add explicit corrections for unsupported rows, and relevant missing decisions when established by evidence. Do not alter other runs' history based only on suspicion. Prefer an existing reproducible check when useful; a new committed script is not required for every evidence item.

Independent review is optional and must be authorized and proportionate. No mandatory subagent, model family, transcript scan or externally sent review is part of this skill. Report only review actually performed.

## Deliver a usable trail

Link the canonical trail and any decisive artifacts; summarize material flags, corrections and remaining evidence gaps at the requested level of detail. Do not force an Attention section, reviewer label or log dump into every answer. Never imply that the audit proves more than the underlying checks establish.

This skill works independently of figure-it-out. Other workflows can delegate trail ownership here without repeating its format.

## Source

Adapted from [pstack/show-me-your-work](https://github.com/cursor/plugins/tree/f713f14203cd6420cec13cd7c55c32d598dbab68/pstack/skills/show-me-your-work), commit `f713f14203cd6420cec13cd7c55c32d598dbab68`. The Bash helper and TSV template are preserved from that source. Original copyright and MIT terms: [LICENSE](LICENSE). No dependency on Cursor, poteto-mode, unslop, uninstalled principle skills or project audit artifacts.
