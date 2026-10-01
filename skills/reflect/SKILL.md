---
name: reflect
description: Review a completed or interrupted task for durable lessons, distinguish missing skill guidance from execution failures, and propose or apply scoped improvements to skills or project instructions. Use for workflow retrospectives and requests to learn from a session; ordinary status summaries or inventories do not need it.
license: MIT; see LICENSE
metadata:
  adapted-from: cursor/plugins/pstack/skills/reflect
  upstream-revision: 2eb7ed4613cfc8f098dfe464a23680ea44d84c5e
---

# Reflect on a task

Turn demonstrated failures and explicit preferences into useful future decisions. Do not turn an entire transcript into more instructions.

## Gather the relevant evidence

Use the scoped conversation when available, the authoritative task worklog, concrete outputs and failures, and the instructions actually used. Read only the skill or project files needed to evaluate a proposed lesson. Do not scan unrelated private sessions or assume a Cursor transcript path exists.

If context is missing, state the limit and use the available evidence. Request a session digest only when its absence prevents a useful conclusion. A digest is evidence supplied by its author, not a substitute for an execution result.

For each candidate lesson, identify the event, observed consequence, relevant existing guidance, and the future decision that different guidance or tooling would change.

## Identify the actual gap

- Compare the failure with the instructions that were in force. If they already clearly required the correct action, classify it as an execution failure. Do not duplicate the rule to create the appearance of learning.
- A demonstrated discovery or ambiguous-trigger problem can justify a narrow trigger or wording change even when the body already has useful guidance. Establish that problem before editing.
- Distinguish an explicit user preference from an inferred pattern. An explicit preference does not need repeated failures; one unexplained incident does not establish a general rule.
- Check whether the cause was missing guidance, missing evidence, an implementation defect, a tool limitation, or an invalid assumption. A skill edit does not repair code or grant a tool capability.
- Prefer an existing suitable skill or the relevant project's instructions over creating a new skill. Put a project-specific fact where that project owns it; put a reusable method in the skill that already covers it.
- For a recurring failure that can be detected mechanically, consider the smallest executable check instead of a growing paragraph of cautions. Do not build a verification framework without a concrete need.

Keep only lessons that are supported, sufficiently specific to guide an action, and likely to matter again. Separate unresolved hypotheses from accepted improvements. Reject duplicate, speculative, or overly broad rules explicitly when they are material to the requested retrospective.

## Make improvements concrete

For each supported proposal, record:

- The observed evidence and the gap it establishes.
- The exact target file and section.
- The replacement or added text, or the smallest useful executable check.
- The future trigger and expected change in behavior.
- A proportionate way to check that the improvement works.

Keep the change narrow. Preserve user-authored instructions, local policies, exact technical meaning, and established authorization. Do not edit vendor plugin caches or install a new capability just to close a retrospective item.

## Respect the requested action

For a reflection-only request, produce concrete proposals without changing instruction files. Save a long result in a local file under the user's output policy. Do not automatically file tracker issues, send messages, create PRs, or make global configuration changes.

If the user has already authorized edits to specified skills or project instructions, carry those edits through without asking again. Read and apply the installed `skill-creator` workflow for skill changes. Implement one meaningful change at a time, run the relevant structural or behavioral check, and record the result in the existing task state.

State what was accepted, rejected, or left unresolved and why. Distinguish a proposed improvement, an applied change, and behavior actually demonstrated by a check. End with any remaining limitation or next action that affects the user's goal.
