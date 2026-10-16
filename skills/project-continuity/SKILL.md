---
name: project-continuity
description: Maintain and resume durable project context through a local AGENTS index, concise current state, checkpoints, and material unresolved questions. Use at project entry or resumption, after consequential progress, before handoff, and when state needs compaction; recover missing context through recall only when needed.
license: MIT
---

# Project continuity

Leave enough durable context for an agent without the previous conversation to continue the authorized work from the project's local AGENTS.md. This skill owns the save/resume and unresolved-item procedures. Project records hold the data; installing the skill does not replace persistent storage.

## Enter or resume a project

1. Establish the project root from the user's designated folder or the existing project entrypoint. For a new project, use the initial working folder. A new session or nested directory normally continues that project; changing directories does not create a new root. A project need not use Git. Honor an explicit new user goal and applicable nested instructions.
2. Explicitly read the root's local AGENTS.md and its required references in order before acting. Reuse its authoritative state and existing record conventions. If the entrypoint, index or authoritative state is absent, read [the record contract](references/records.md) and bootstrap the missing parts before substantial work, preserving existing instructions and data.
3. Reconcile the recorded objective, accepted constraints, done versus pending work, evidence, unresolved items and next action with the latest user messages and relevant live files or operation status. Inspect only what can affect the next action. Reuse checks that still apply; recheck claims made stale by changed inputs, artifacts or requirements.
4. Inspect pending operations by their recorded identifier and expected outputs. An operation may have completed after the checkpoint. Do not assume a previous process survived, repeat a mutation blindly, or restart a job just to learn its status. Record unknown status and resolve it before dependent work or a duplicate action.
5. If a material context gap remains, use [recall](../recall/SKILL.md) for that specific gap. Return the supported result to the authoritative state with its source and uncertainty. Sufficient records need no transcript search. Missing context is not permission to invent an answer or inspect unrelated histories.
6. Resume the current authorized objective at the next executable action. If complete, deliver its outcome rather than reopening finished work. A checkpoint supports continuation; it is not completion of the user's task.

## Save meaningful progress

Keep one maintained current-state summary and a compact local entrypoint. Read [the record contract](references/records.md) when creating, restructuring or compacting records, or resolving uncertainty about what belongs where.

- Save accepted constraints and consequential decisions promptly; assume the session can end without a final handoff.
- Before a long-running or consequential operation, record the intended action as pending, expected outputs, and any available identifier or inspection method. Update with the identifier and observed result as they become available.
- After a meaningful change, experiment, failure, discovery or completed dependency, update the state and next action before dependent work. Label changed but unverified work and the limits of inherited checks.
- At a planned stop or completion, record the outcome, checks actually performed, remaining limitations and next action or explicit completion. Confirm the local index reaches the necessary records. Checkpointing during ongoing work does not itself pause the task.
- Keep detailed artifacts and useful failure evidence in linked records. Use [show-me-your-work](../show-me-your-work/SKILL.md) when a consequential decision trail or audit is needed, reusing a suitable existing trail. That skill owns historical log format; this skill owns the current summary. Avoid a second history for the same work.

The checkpoint must let a cold-start agent identify the goal, constraints, verified and unverified work, pending operations or decisions, important evidence, and the first useful action. Store project data inside the project, never inside this global skill or the global AGENTS.md. If persistence is restricted, explain what could not be saved and provide the best permitted handoff. Never claim the last in-flight change is recoverable without evidence.

## Track material questions and design friction

- When a question or observed design difficulty needs tracking, proactively use one shared project-local unresolved-items record. Reuse a designated path or existing equivalent; otherwise use OPEN_ITEMS.md. Announce its path and make it required through the local AGENTS index while relevant items remain. Keep empty queues and trivial choices out of the project.
- Use stable IDs and distinguish a question from an observation. Record affected work, why it matters, evidence or uncertainty, a proposed default and tradeoff when useful, status, and the user's answer. For design friction, identify the observed difficulty, its design cause and the smallest plausible improvement; distinguish a defect from a design observation and a hypothesis from established evidence.
- Continue independent authorized work while an answer is pending. Make routine reversible choices within accepted requirements and record a material assumption. If a required fact or decision blocks correctness or changes an explicit constraint or authorization, pause only dependent work and surface the specific blocker. Silence supplies neither facts nor required approval.
- Read the latest unresolved-items record at entry/resumption, between meaningful steps, before an affected decision and before editing it. Reconcile user answers and concurrent edits instead of overwriting a stale snapshot; no continuous polling is required.
- Review relevance against current requirements and evidence. Correct outdated status; mark uncertain items for revalidation before relying on them. Neither age nor lack of an answer alone makes an item obsolete.
- Incorporate answers at the next relevant checkpoint and recheck affected work. Preserve accepted constraints, rationale and useful evidence in their authoritative record, then promptly remove resolved, obsolete or superseded entries and consolidate duplicates. Retain relevant unanswered items and responses not yet incorporated.

## Compact or reorganize records

Keep current state proportional to the work and useful for resumption. Replace completed-task narration with concise outcomes and links to the evidence that still matters. Preserve unique evidence and durable knowledge in suitable references before removing redundant text; stability alone does not make a constraint dispensable.

Reuse existing filenames and formats when they work. current-state.md and OPEN_ITEMS.md are defaults, not required universal names; a small project can keep unresolved items in a clearly indexed section of its current record. Maintain one authoritative location for each fact. A decision-history log remains distinct from the maintained current summary, even when linked from it.

Read the latest records before restructuring. Preserve unrelated content and user answers; update incoming links and reading requirements when paths change. Verify root-to-state reachability and the concrete next action after compaction. Do not create a backup tree or duplicate transcript to compensate for an unclear ownership decision.

## Scope and sources

Routine local index/state maintenance follows applicable project instructions and the task's authorization. This skill does not authorize commits, pushes, publication, account changes, job restarts, delegation or unrelated code changes. Use actual exposed tools and identifiers; no Cursor-specific paths, fixed model policies or orchestration engine are required.

Adapted from pstack's [Session pickup](https://github.com/cursor/plugins/blob/f713f14203cd6420cec13cd7c55c32d598dbab68/pstack/skills/poteto-mode/playbooks/session-pickup.md), [Pause safely](https://github.com/cursor/plugins/blob/f713f14203cd6420cec13cd7c55c32d598dbab68/pstack/skills/poteto-mode/playbooks/pause-safely.md), and the store/gates ideas in [Orchestrate](https://github.com/cursor/plugins/blob/f713f14203cd6420cec13cd7c55c32d598dbab68/pstack/skills/poteto-mode/playbooks/orchestrate.md), plus the user's established continuity contract. Source pin: f713f14203cd6420cec13cd7c55c32d598dbab68. This is a custom Codex skill, not a renamed upstream skill. Original MIT notice: [LICENSE](LICENSE). Installed resources and the linked global helper skills are sufficient; no dependency on the source clone or the project used to author this skill.
