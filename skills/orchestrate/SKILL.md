---
name: orchestrate
description: Coordinate substantial work with continuous Luna-first evidence gathering and Sol execution. Use for explicit multi-agent requests and for complex research, engineering, debugging, verification, or analysis involving material uncertainty, broad repository discovery, internet research, large documents, multiple files, or noisy command output. Skip trivial tasks and tightly coupled work that cannot benefit from delegation.
---

# Luna-first orchestration

Keep the primary Sol/xhigh coordinator focused on decomposition, architecture,
consequential judgment, escalation, and final synthesis. Use Sol/high for
implementation. Use Luna/max as the read-only high-volume evidence service for
both Sol roles throughout the task.

## Route by uncertainty and authority

- Send evidence uncertainty to Luna/max: search, read, map, extract, compare,
  classify, or distill what is true.
- Keep decision uncertainty with sufficient evidence in Sol/xhigh: interpret
  contracts, choose architecture, and resolve consequential tradeoffs.
- Send execution after the decision is established to Sol/high: mutate state,
  implement, test, debug, and verify the focused solution.

Never assign Luna solution ownership, writes, mutations, final verification
judgment, or the user-facing answer. Luna may run noisy read-only diagnostics
itself so their raw output remains in its context. Sol owns every mutation and
focused verification command.

When Sol discovers a genuine new evidence gap, assign Luna a bounded,
reproducible read-only follow-up. If the workflow naturally produced an
artifact or log, give Luna its exact path and question. Do not create an
artificial wrapper or extra artifact merely to transfer output.

## Enforce explicit runtime pins

- For every Luna spawn, explicitly set `model: "gpt-5.6-luna"`,
  `reasoning_effort: "max"`, and `fork_turns: "none"`. Never use any Luna
  effort other than `max`, and never rely on a role or task name to select the
  model. Use a unique semantic task name beginning with `luna_preflight_`,
  `luna_contract_`, `luna_research_`, `luna_falsify_`, `luna_failure_`,
  `luna_verify_`, or `luna_provenance_`, according to its evidence lens.
  Repeat the read-only leaf boundary and evidence-packet contract in the
  self-contained assignment.
- For every implementation spawn, explicitly set `model: "gpt-5.6-sol"`,
  `reasoning_effort: "high"`, and `fork_turns: "none"` or a small positive
  count. Never rely on inheritance for the model or effort. Permit Sol/high to
  spawn only explicitly pinned Luna/max agents for evidence work.
- Keep Sol/xhigh responsible for the uncertainty map, architecture, scope and
  ownership, escalation, approvals, final verification judgment, and user
  communication.

Treat global defaults and custom agent files only as safety nets and catalog
definitions. Spawn-time model, effort, and context pins are permanent runtime
invariants.

Use the concise [Luna assignment patterns](references/luna-assignment-patterns.md)
to frame each semantic evidence lens without weakening these invariants.

## Frame and challenge Luna investigations

For every nontrivial Luna assignment, Sol must define the material uncertainty,
the pending decision it informs, the bounded search surface, and the success or
stopping condition. Include the leading hypothesis and strongest known
competing hypothesis when they are already known.

Before returning `sufficient` on a materially ambiguous question, Luna must
seek counterevidence, run or propose one bounded read-only discriminating
probe, and report coverage of the assigned surface. Continue bounded
investigation while each next probe materially reduces uncertainty; stop when
the evidence is decision-ready, another probe is unlikely to change the pending
decision, or progress is externally blocked.

Distinguish observed facts, inferred conclusions, and unverified assumptions or
unknowns. Surface low-frequency evidence that could overturn the decision, not
only dominant patterns. Sol still owns interpretation and the final decision.

## Apply the offload gate continuously

Before either Sol role consumes any of the following, delegate the bounded
evidence question to Luna/max:

- internet or external-document research;
- broad repository discovery or more than three potentially relevant files;
- roughly 20 KB or more of source, documents, history, or generated text;
- command output expected to exceed roughly 100 lines or 10 KB;
- multiple logs or before/after runs, or conflicting evidence.

Let Sol read a known small code region and Luna's cited decisive fragments.
Reapply the gate after edits, failures, warnings, unexpected behavior, and
verification runs. For a noisy read-only probe, delegate the command itself to
Luna. For a Sol-owned mutation or focused verification, keep its output bounded;
if that run naturally creates a large log or report and opens a material new
question, send Luna the path and exact question.

These thresholds are the canonical defaults. Use judgment near a boundary, but
do not duplicate or silently redefine them in role profiles.

## Preflight each consequential phase

Before consequential architecture or plan selection, Sol/high implementation,
the first broad diagnostic pass after an unexpected result, focused
verification expected to produce noisy evidence, or final synthesis across
multiple sources or artifacts, forecast the phase's complete evidence surface.

Count related reads, searches, logs, queries, and artifacts cumulatively across
the anticipated phase. Treat fragmented operations that jointly map one
subsystem, compare several logs, research one external decision, or synthesize
one claim set as one surface. Apply the canonical offload gate to that phase
total. If it crosses the gate, dispatch a bounded Luna lens before Sol consumes
the surface. Re-run this preflight whenever the phase or evidence surface
materially changes.

## Hand off the first uncertain failure

After the first unexpected focused implementation or verification failure
creates material uncertainty, require `luna_failure_*` to produce a bounded
read-only differential before Sol performs another broad evidence pass or a
speculative retry. Give Luna the expected and observed behavior, failed
hypothesis, changed and unchanged evidence, failures or warnings to cluster,
strongest competing explanation, and one discriminating read-only probe.

Sol may first run one known small decisive probe when its bounded result can
resolve the uncertainty without broad evidence. If it does not, perform the
Luna handoff. Sol then chooses whether to retry, revise, or escalate; Luna does
not select the next action.

## Demand bounded evidence packets

Require every Luna handoff to contain:

1. `status`: `sufficient`, `partial`, or `blocked`.
2. A direct answer to the assigned evidence question.
3. Confidence in that answer.
4. Decisive evidence and provenance: paths plus line numbers, log offsets, or
   direct URLs; use at most 15 short excerpts and paraphrase the rest.
5. A brief coverage statement, with findings labeled `observed`, `inferred`,
   or `unverified`, including low-frequency evidence that could overturn the
   pending decision.
6. Contradictions, source-quality concerns, and remaining material unknowns.
7. At most one next decisive probe, only when the current packet is not
   sufficient.

Stop evidence work when the packet is sufficient for the pending Sol decision.
Do not impose arbitrary hard token minimization that harms evidence quality.
Bound each probe, command, time range, file set, and output instead; partition a
broad surface across independent, non-overlapping Luna agents.

## Use concurrency only for real decomposition

The five spawned-thread cap excludes the primary coordinator. Do not claim the
cap itself creates speedup; parallelism helps only when evidence questions are
independent, disjoint, and free of concurrent writes.

- Research phase: use up to four disjoint Luna/max children and keep one child
  slot reserved for a newly discovered decisive probe.
- Implementation phase: use one Sol/high executor plus up to three disjoint
  Luna/max children and keep one child slot reserved for executor follow-up.

When parallel Luna agents examine the same material uncertainty, give them
distinct investigative lenses or non-overlapping surfaces rather than
duplicating one broad search.

Close completed agents promptly. Let agents message dependency findings
directly while the coordinator tracks ownership and remains available to the
user.

## Compose safely with other skills

When another selected skill requests panels, subagents, instrumentation,
rendering, installation, compilation, writing, or output-file creation, assign
Luna only independent read-only evidence work. Keep instrumentation, writes,
synthesis, mutations, and final verification judgment with Sol, and preserve
this skill's runtime pins, evidence boundary, and concurrency cap.

## Control scope changes and waiting

When the user or evidence changes scope:

1. Identify and interrupt superseded agents promptly.
2. Preserve useful partial evidence packets.
3. Update the plan and reconcile revised scope, dependencies, and file
   ownership.
4. Prevent new writes until that reconciliation is complete.

Wait adaptively. After one meaningful wait timeout, request a checkpoint or a
bounded conclusion from the running agent. Do not repeat fixed polling without
new information.

## Prove operational readiness

For work that installs, builds, or configures a capability, track the lifecycle:

`Discovered -> Installed -> Runnable -> Behavior-verified`

Do not call the work complete before a real core-path smoke test reaches
Behavior-verified. Classify dependencies as `required core`, `optional
enhancement`, `cloud/credential-dependent`, `already available`, or `deferred`.
Install or enable the smallest effective set; do not select every bundle by
default.

Where relevant, record before/after provenance and persistent state for system
packages, user-global packages, caches or downloads, credentials or
configuration, workspace files, and temporary artifacts. Report the pinned
source or version, material persistent changes, cleanup or recoverability, and
residual uncertainty. Keep this proportional; do not bloat trivial tasks.

## Run the continuous loop

1. Frame the problem, success behavior, material uncertainties, and ownership.
2. Assign independent evidence questions to explicitly pinned Luna/max agents.
3. Resolve contradictions and choose the architecture from auditable evidence.
4. Assign the focused implementation to explicitly pinned Sol/high.
5. Route every genuine new bulk evidence gap back to Luna without surrendering
   mutation or verification judgment.
6. Have Sol inspect decisive cited fragments and continue or correct the work.
7. Stop speculative patching after repeated failure or architectural ambiguity;
   escalate evidence, attempts, and the unresolved decision to Sol/xhigh.
8. Verify actual behavior, inspect final scope and persistent state, and
   synthesize one coherent result.
