---
name: interrogate
description: Review a code diff or proposed implementation with evidence-based judgment, independent reviewers when useful, and a synthesis of actionable defects and unresolved disagreements. Use for rigorous reviews, competing review opinions, or requests to interrogate a change; use blast-radius for a focused investigation of what a change can break.
license: MIT; see LICENSE
metadata:
  adapted-from: cursor/plugins/pstack/skills/interrogate
  upstream-revision: 2eb7ed4613cfc8f098dfe464a23680ea44d84c5e
---

# Interrogate a change

Determine which concerns are real, reachable, and worth acting on. Review the requested change without modifying the reviewed source unless fixes are also authorized.

## Establish the review input

- Read the relevant repository instructions and authoritative task state. Infer the intended behavior from the request, contracts, examples, and tests. Label any assumption that affects a finding.
- For a diff, identify the intended base and target. Use the correct merge base for branch review; include staged, unstaged, or untracked work only within the requested scope. Record the revisions or working-tree snapshot reviewed.
- Inspect changed code and enough callers, data flow, and boundary behavior to judge it. A diff alone often omits the contract that makes a change wrong.
- For code review, read the installed `review-agent` criteria when available, normally at `~/.codex/skills/.system/review-agent/SKILL.md`. For a proposal without executable code, evaluate its concrete assumptions and dependencies; label untested predictions as such.
- Evaluate the user's exact technical claims. If a premise is false, state the correction directly. Keep a factual defect separate from a design preference or a change in requested behavior.

## Choose the useful review effort

Use a direct pass for a small, localized change. Use independent reviewers when separate reasoning is likely to expose a missed defect or resolve material uncertainty. Choose relevant areas such as behavioral correctness, state and concurrency, trust boundaries, or computational validity; do not require a fixed reviewer count.

When delegating, use the native collaboration tools actually exposed in the session. Give each reviewer the same scope and expected behavior, relevant project instructions, raw code and context, and any specific area to examine. Use a fresh context when independence matters; do not supply another reviewer's conclusions or a suspected answer.

Tell reviewers to leave source unchanged, return evidence and precise locations, and distinguish reproduced defects from unresolved concerns. Keep their scratch outputs in isolated paths. A read-only instruction is a behavioral constraint, not an enforced filesystem sandbox.

Native agents may use the same model. Do not label them as different models or invent unsupported model, cloud, or read-only parameters. If the user requests actual model diversity, use a backend that exposes it, such as the existing surf consultation workflow, and report the real services used. Do not send code to an external service merely to satisfy a reviewer count.

## Require a concrete causal argument

For each proposed finding, establish:

- The input, caller, state, or sequence that reaches the affected code.
- The expected behavior and evidence for that expectation.
- The changed operation that causes the failure or violates the contract.
- The observable consequence and a precise location in the reviewed change.

Prefer the cheapest real reproduction when it settles a material concern. Use existing tests, a small input, or an isolated execution rather than building a broad mock harness. Record what ran, what it showed, and what remains untested. If execution is unavailable, retain only findings supported by a concrete reachable path and state the verification limit.

For unreleased research software, judge the smallest working end-to-end implementation. Do not demand backward compatibility, adapters, feature gates, broad defensive code, arbitrary file-length limits, or speculative architecture. Internal assertions can expose programmer errors; realistic external failures still need explicit handling.

Use existing blast-radius or specialist mathematical skills for the corresponding question. Do not treat a code reviewer vote as validation of a theorem or research claim.

## Synthesize and decide

- Merge duplicate concerns by cause and consequence, retaining the strongest evidence. Several reviewers agreeing is a signal to investigate, not proof.
- Resolve disagreements against the implementation, contract, and reproduction. Keep an unresolved disagreement visible when the evidence does not decide it.
- Lead with the actionable findings, ordered by consequence. Include the affected location, trigger, actual versus expected behavior, and proportionate fix direction when clear. Report every concrete actionable issue; do not truncate to an arbitrary count.
- Keep optional improvements separate from defects. Briefly explain dismissed or unresolved material concerns when the user needs to assess the competing opinions.
- State the reviewed scope and verification limits. If there are no actionable findings, say so without claiming the change is proven correct.

Follow the user's output policy for long reviews. Apply fixes only when requested or already authorized, then verify the affected behavior before reporting completion.
