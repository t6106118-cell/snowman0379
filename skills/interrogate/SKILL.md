---
name: interrogate
description: Review a code diff or proposed implementation with evidence-based judgment, independent reviewers when useful, and a synthesis of actionable defects and unresolved disagreements. Use for rigorous reviews, competing review opinions, or requests to interrogate a change; use blast-radius for a focused investigation of what a change can break.
license: MIT; see LICENSE
metadata:
  adapted-from: cursor/plugins/pstack/skills/interrogate
  upstream-revision: f713f14203cd6420cec13cd7c55c32d598dbab68
---

# Interrogate a change

Determine which concerns are real, reachable, and worth acting on. Review the requested change without modifying the reviewed source unless fixes are also authorized.

## Establish the review input

- Read the relevant repository instructions and authoritative task state. Infer the intended behavior from the request, contracts, examples, and tests. Label any assumption that affects a finding.
- For a diff, identify the intended base and target. Use the correct merge base for branch review; include staged, unstaged, or untracked work only within the requested scope. Record the revisions or working-tree snapshot reviewed.
- Inspect changed code and enough callers, data flow, and boundary behavior to judge it. A diff alone often omits the contract that makes a change wrong.
- For code review, read the installed [review-agent criteria](../.system/review-agent/SKILL.md). For a proposal without executable code, evaluate its concrete assumptions and dependencies; label untested predictions as such.
- Evaluate the user's exact technical claims. If a premise is false, state the correction directly. Keep a factual defect separate from a design preference or a change in requested behavior.

Before reviewing, make the intended behavior and material constraints explicit in the review input. Give delegated reviewers the same intent. Resolve ambiguity from the available evidence; ask only when an unresolved distinction would materially change the review. Treat the author's summary as a claim to check against the requested outcome. Keep findings first in the final response.

## Choose the useful review effort

Use a direct pass for a small, localized change. Use independent reviewers when delegation is authorized and separate reasoning is likely to expose a missed defect or resolve material uncertainty. Choose relevant areas such as behavioral correctness, state and concurrency, trust boundaries, or computational validity; do not require a fixed reviewer count.

When delegating, use the native collaboration tools actually exposed in the session. Give each reviewer the same scope and expected behavior, relevant project instructions, raw code and context, and any specific area to examine. Use a fresh context when independence matters; do not supply another reviewer's conclusions or a suspected answer.

Tell reviewers to leave source unchanged, return evidence and precise locations, and distinguish reproduced defects from unresolved concerns. Keep their scratch outputs in isolated paths. A read-only instruction is a behavioral constraint, not an enforced filesystem sandbox.

Native agents may use the same model. Do not label them as different models or invent unsupported model, cloud, or read-only parameters. If the user requests actual model diversity, use a backend that exposes it, such as the existing surf consultation workflow, and report the real services used. Do not send code to an external service merely to satisfy a reviewer count.

## Apply only relevant risk lenses

- For operations that may be retried or interrupted, trace a repeat invocation and a failure after a partial effect. Check whether the required behavior needs idempotence, reconciliation, or an explicit conflict. Do not assume every operation must be repeatable.
- For actual concurrent writers, identify state ownership and a reachable interleaving. Check that coordination or separation enforces the required semantics; a comment or assumed ordering alone may not do so. Do not prescribe a lock without establishing the shared-state problem.
- For integrations, delegated work, or async completion, inspect the actual result and required output artifacts. A success summary, cached status, timestamp, or process exit is insufficient when the contract requires a particular value or artifact. Use evidence from the real boundary rather than a proxy for it.
- For guards, retries, casts, and repeated special cases, trace the violated invariant and the layer that owns it. Distinguish legitimate external-failure handling from hiding an internal defect. Suggest structural simplification when it removes a demonstrated cause or maintenance burden; a different preferred shape alone is not a finding.

## Require a concrete causal argument

For each proposed finding, establish:

- The input, caller, state, or sequence that reaches the affected code.
- The expected behavior and evidence for that expectation.
- The changed operation that causes the failure or violates the contract.
- The observable consequence and a precise location in the reviewed change.

Prefer the cheapest real reproduction when it settles a material concern. Use existing tests, a small input, or an isolated execution rather than building a broad mock harness. Record what ran, what it showed, and what remains untested. If execution is unavailable, retain only findings supported by a concrete reachable path and state the verification limit.

Judge the implementation against the requested behavior and established current contracts, using the smallest complete end-to-end path that satisfies them. Require backward compatibility, adapters, feature gates, or defensive behavior only when an explicit requirement or demonstrated current condition justifies them. Do not demand arbitrary file-length limits or speculative architecture. Internal assertions can expose programmer errors; realistic external failures still need explicit handling.

Use existing blast-radius or specialist mathematical skills for the corresponding question. Do not treat a code reviewer vote as validation of a theorem or research claim.

## Synthesize and decide

- Merge duplicate concerns by cause and consequence, retaining the strongest evidence and reviewer origins when needed to explain competing opinions. Several reviewers agreeing is a signal to investigate, not proof; silence is not agreement.
- Resolve disagreements against the implementation, contract, and reproduction. Keep an unresolved disagreement visible when the evidence does not decide it.
- Give a credible lone correctness or security finding the same causal scrutiny as a shared finding. Do not dismiss it because of reviewer count or accept it because of severity language.
- Lead with the actionable findings, ordered by consequence. Include the affected location, trigger, actual versus expected behavior, and proportionate fix direction when clear. Report every concrete actionable issue; do not truncate to an arbitrary count.
- Keep optional improvements separate from defects. Briefly explain dismissed or unresolved material concerns when the user needs to assess the competing opinions.
- State the reviewed scope and verification limits. If there are no actionable findings, say so without claiming the change is proven correct.

Follow the user's output policy for long reviews. Apply fixes only when requested or already authorized, then verify the affected behavior before reporting completion.
