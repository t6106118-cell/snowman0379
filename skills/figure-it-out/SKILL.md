---
name: figure-it-out
description: Design and execute a verifiable workflow for substantial unfamiliar or multi-part work when no suitable narrower workflow fits. Use for complex migrations, long autonomous tasks, or explicit figure-it-out requests; define completion, test consequential unknowns early, and maintain a reviewable decision trail through show-me-your-work.
license: MIT
---

# Figure it out

Build a task-specific workflow, then carry authorized work through execution and verification. The plan is a means to the requested result; a planning-only request remains planning-only. Use a suitable narrower workflow when it already fits, and keep routine tasks direct.

Read [show-me-your-work](../show-me-your-work/SKILL.md) at the start. Delegate the decision-trail format, writing and audit to that skill throughout the run; do not invent a competing log. This is a deliberate one-way dependency: show-me-your-work can also serve other workflows independently.

## Frame the actual task

- Read applicable project instructions and continuation records. Reconcile relevant live state before extending prior work; do not reconstruct private chat history by default.
- Identify the requested outcome, explicit constraints, scope of authorization, and an observable completion criterion that could be falsified. Distinguish facts, hypotheses, missing evidence and requirements that need a user decision.
- Ground enough of the real path to identify inputs, outputs, ownership, external boundaries and important side effects. Estimate scope only as far as the evidence supports; do not invent precise effort numbers.
- Scale checks and records to impact, uncertainty and reversibility. Explain material tradeoffs before a long or consequential operation; routine reversible work proceeds within existing authorization. Missing approval for a dependent action does not stop independent authorized work.

## Design the smallest useful sequence

- Write a concise phase list in the existing project plan/current-state record. Each unit should produce an observable result and have a useful check; avoid a second planning record without a concrete need.
- Test the unknown most likely to invalidate the approach early. Reuse a working end-to-end path, test runner or direct operation; otherwise run the smallest complete experiment that reaches the relevant boundary.
- Capture the pre-change baseline when it materially supports the required comparison. Build or repair a harness only when existing checks cannot establish the needed fact and its cost is justified.
- Use architect for genuine software design uncertainty and tdd for a suitable regression-first fix. Neither a model panel nor a particular architecture workflow is required for mechanical work.
- Delegate only when applicable instructions or the user authorize it and independent seams make it worthwhile. If using workers, isolate their mutable work and inspect their actual outputs; no fixed team, model family or worktree ritual is required.

## Execute as bounded experiments

For each meaningful unit, identify the hypothesis or expected behavior, make the smallest useful change, run the relevant check, inspect the real result, and update the plan from evidence before proceeding.

- Verify each meaningful increment before building dependent changes on it. Keep useful failure evidence and pause work that relies on a disproved assumption; continue unrelated authorized progress.
- If the unit fails, distinguish an implementation defect, design defect, environment issue and conflicting requirement. Revert or revise only your in-scope changes when appropriate; preserve unrelated user work and data. An obstacle alone does not prove the design wrong.
- If a check passes suspiciously easily or contradicts other evidence, verify the observation method: current version/path, nonempty relevant artifact, actual execution and ability to detect the target failure. A cheap baseline or negative control can help; do not invent a harness solely for ceremony.
- Keep success, observed failure, inconclusive evidence and checks not run distinct. Check exit status and actual artifacts, including delegated outputs; a summary claiming success is not verification.
- If an expectation or gate is wrong, correct it against the real requirement. Do not weaken a valid check or hide a real failure to claim progress.
- Simplify or replace structure invalidated by evidence instead of accumulating workarounds. Keep recurrence checks only when they prevent a demonstrated class of mistakes at reasonable cost.

## Keep the decision trail and current state aligned

Use show-me-your-work to record consequential choices, pivots, failures, completed units and evidence as they happen. Its trail is supporting history; the maintained project state remains authoritative for the current goal, status and next action. Link the trail from that state so continuation reaches it.

Record pending consequential operations before starting and reconcile their actual outcome on resumption. Do not commit, publish, contact others, or access unrelated records merely because the workflow is ambitious; follow the authorization already established for the task.

## Verify and deliver

Check the assembled result against the original completion criterion on the real product/artifact. Reuse sufficient current evidence; repeat or broaden checks only for a new change, failure, stale evidence or specific unresolved concern.

Have show-me-your-work audit the material trail against available task evidence. Then deliver the outcome, decisive checks and evidence pointers, relevant tradeoffs, remaining uncertainty and the next action if incomplete. Link the phase/decision records when they help review; do not dump the whole log or impose a fixed final section template. An unrun decisive path remains unverified.

## Source

Adapted for Codex CLI and the workstation's standing policy from [pstack/figure-it-out](https://github.com/cursor/plugins/tree/f713f14203cd6420cec13cd7c55c32d598dbab68/pstack/skills/figure-it-out), commit `f713f14203cd6420cec13cd7c55c32d598dbab68`. Original copyright and MIT terms: [LICENSE](LICENSE). No dependency on Cursor, poteto-mode, arena, uninstalled principle skills or project audit artifacts.
