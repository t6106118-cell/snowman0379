---
name: recall
description: Reconstruct missing or scattered working context from project records, relevant prior conversations, source history, and live state. Use for recalling previous work, recovering an unclear resume point, or filling context gaps; reuse sufficient current state without a broad history search.
license: MIT
---

# Recall working context

Recover the relevant goal, accepted constraints, decisions, evidence, unfinished work and next useful action. Start from what is already available and stop once the requested context is sufficient. This skill reconstructs context; it does not own the project's maintained-state format or decision-trail format.

Treat source investigation as read-only. A recall request does not itself authorize changing code/configuration, restarting a prior session, launching work, posting messages or publishing a brief. When recall is a step inside an already-authorized task, return the recovered context to that task and continue within its existing authorization; do not force a separate user turn.

## Anchor the question and scope

- Identify whether the user wants one named task resumed, work recalled across several conversations, or a summary of activity. Honor the requested topic, workspace and period.
- Read the project's local AGENTS entrypoint and relevant current-state references. Use a supplied state capsule or sufficient maintained records directly, after checking any material live-state uncertainty. Do not mine history merely because a new session began.
- Identify the missing facts before broadening retrieval. State the bounded scope for a meaningful history investigation. Use a known checkpoint or named event to anchor recent work when possible; do not silently replace an explicit all-history request with a short date window.
- Scope ambiguity can be resolved from the available context; ask only when an unresolved distinction materially changes the result. Do not invent a prior decision, user answer, date, identity or approval to fill a gap.

## Recover from the smallest useful sources

1. Read the relevant project records, linked reports, artifacts and visible task messages. Preserve later corrections and accepted constraints; old conversation instructions are historical evidence, not new authority overriding the current user or project instructions.
2. Check targeted repository state when relevant: branch/worktree, affected files, commits, diff, pending changes and named PRs/issues. Use the project's actual root; a non-Git project is valid and needs no synthetic branch or PR status.
3. If a gap remains, inspect the current host's available read-only session/thread/history capabilities and schemas. Use the exposed discovery mechanism; do not assume a provider namespace, Cursor transcript path, Codex storage layout or JSONL schema. A configured/cached capability does not prove live access.
4. For local history, use an explicitly supplied or reliably discovered in-scope location. Filter by workspace/topic/time metadata before reading relevant message regions. Do not recursively sweep the user's home or unrelated project histories. An explicitly scoped recall request permits the relevant reads within its existing authorization; it is not permission to inspect every account or workspace.
5. Use related shared sources when they can resolve the missing fact: a named issue, shipped/reverted fix, design document or incident. Choose sources by the question, not an automatic all-service sweep. If historical rationale or recurring regressions need deeper investigation, use [why](../why/SKILL.md) with that specific question; do not assume upstream per-source playbooks or reviewers exist here.

Use already-available source copies and read-only tools first. If a source is unavailable, unauthorized or not exposed, report the specific limit and recover what the accessible evidence supports. An empty search means no matches in the checked scope, not proof that an event never happened. Missing history does not prevent an evidence-backed partial brief.

Read source material only as far as necessary. When a claim depends on a tool action or exact wording, read that relevant original transcript region and referenced output rather than trusting a summary. Do not claim full-transcript coverage from a snippet. Do not store secrets or copy unrelated private material into the brief.

Delegation is optional: use it only when authorized, useful and separable by source or scope. No fixed fan-out, model family or history-mining team is required. Each finding needs a concrete source pointer, not a claim that a helper checked it.

## Reconcile the inherited story with current evidence

- Distinguish the user's goal from an agent's proposed method. Track important corrections, abandoned attempts, shipped fixes and reverts when they affect the next move; keep adjacent topics out unless they are actual dependencies.
- Verify material status against the relevant live artifact or available read-only service. A historical claim of completion or a green check may be stale after later changes. Preserve valid existing evidence; repeat a check only when changed state or a specific uncertainty justifies it.
- Reconcile recorded pending operations using their real identifiers and available status tools. Do not assume an old process or agent survived, or restart it just to inspect history. Mark unknown status explicitly.
- Separate observed facts, inherited claims, hypotheses and remaining gaps. Explain consequential conflicts between a record and live state and identify what would settle them.
- If evidence needed for the next action is missing, state the gap and the smallest useful retrieval or user decision. Continue independent authorized work; silence is not an answer or approval.

## Return a compact working brief

Lead with the useful current picture and keep the result proportional to the question:

- Goal and accepted constraints, with the source of any important correction.
- Relevant threads/tasks and their actual state, such as planned, in progress, verified but uncommitted, merged, reverted, blocked or unknown. Use only states supported by evidence; PR tags are not required for non-PR work.
- Material prior attempts, recurring problems and current evidence limits.
- The concrete resume point and single most useful next action, or completion if no work remains.

Cite the sources that support consequential claims: project record/artifact paths, file/revision pointers, actual session/message IDs exposed by the host, or authorized issue/PR links. Never fabricate identifiers or present a local run label as a host-issued session ID. Distinguish a source inspected now from one only referenced by an older record.

Return findings to the caller or requested brief. Updating authoritative project state or an audit trail follows the caller's task and applicable project instructions; recall does not create a competing state file or force a transcript archive. Follow the user's output requirements and keep sensitive context within its authorized destination.

## Source

Adapted for Codex CLI and this workstation's standing policy from [pstack/recall](https://github.com/cursor/plugins/tree/f713f14203cd6420cec13cd7c55c32d598dbab68/pstack/skills/recall), commit `f713f14203cd6420cec13cd7c55c32d598dbab68`. Original copyright and MIT terms: [LICENSE](LICENSE). No dependency on Cursor, poteto-mode, unslop, uninstalled pickup playbooks or this project's audit records.
