---
name: tdd
description: Use for explicit TDD requests, regression-test-first bug fixes, or bugs with an obvious cheap local executable check. Do not force TDD when the useful test path is expensive, mock-heavy, or less direct than a real reproduction.
---

# TDD bug fix

Explicit user and project instructions take precedence over this skill.

Make the broken behavior executable before changing production code when there is a cheap, meaningful test path.

This is a debugging workflow, not a requirement to test everything first. The objective is a focused red-to-green check that gives fast localization and useful regression evidence.

## 1. Define observable failure

State the intended behavior, current behavior, smallest reproducing input or sequence, and boundary where the wrong result becomes observable.

Do not begin by changing implementation details.

## 2. Choose the cheapest meaningful executable check

Prefer an existing test level close to the bug. A focused unit or component test is good when it exercises real behavior. Otherwise use a focused integration test, small executable script, CLI, HTTP, or browser reproduction, or the real end-to-end path.

Choose the narrowest check that still observes the defect.

Do not create a large harness, broad fixture system, or mock architecture only to satisfy TDD.

## 3. Prove red before the production edit

Write or select the smallest check that would have caught the defect and run it before the fix.

Ground its expected result in a user requirement or established current contract. A self-authored assertion is not a new product requirement; correct an unsupported expectation rather than making the implementation satisfy it.

The failure must be the intended failure. If the check passes unexpectedly, refine the reproduction or reassess the claimed defect. If it fails for an unrelated reason, correct the check or setup first. A race or timing failure that demonstrates the target defect is valid red evidence.

Record the exact failing command and failure signal.

## 4. Find the root cause

A red test establishes the behavior boundary. It does not identify the cause automatically.

Trace the failing path. Instrument when needed.

Do not add a nil check, retry, catch, fallback, or default merely to make the test green when that would hide an invariant violation.

Fail loudly on programmer errors and impossible internal states. Handle realistic external failures at the appropriate boundary.

## 5. Make the smallest root-cause change

Change only what is needed to make the intended behavior true.

Require backward compatibility only when an explicit task requirement or established current contract needs it. Preserve required external consumers, inputs, formats, and persisted user data. Do not add a flag, compatibility shim, deprecated path, alias, or fallback only to preserve obsolete behavior.

If the correct fix changes an internal API, migrate the current callers and delete the obsolete path.

Do not weaken the fix to preserve a legacy test whose only purpose is obsolete behavior.

Do not change a valid expected result merely to match a wrong implementation. Weaken or remove an existing assertion only when its expectation is unsupported or the required behavior genuinely changed; state the reason and preserve checks for the remaining contract.

## 6. Prove green immediately

Run the same red check after the fix.

Do not make unrelated changes before obtaining green. If the check remains red, continue debugging the same unit instead of piling on speculative fixes.

## 7. Run adjacent verification

After the focused check is green, run nearby checks justified by the actual blast radius. Examples include relevant package tests, type checking, linting that can catch errors in the touched area, or a focused integration or end-to-end path.

Compilation is not behavioral proof.

## When a new regression test is not useful

Skip a new durable test when it requires broad new harness setup, brittle mocks of most of the real path, slow unrelated infrastructure, inaccessible production-only state, large fixture churn, or assertions about implementation details instead of behavior.

Do not skip verification. Use the closest executable reproduction instead and state why a durable test was not useful.

Prefer no new test over a bad test.

## Test quality

A useful regression check calls the subject through a realistic boundary, uses a concrete input, asserts a concrete output, state transition, side effect, or loud failure, fails for the original defect, and does not merely verify mock choreography or restate a constant from the implementation.

For a flaky defect, identify the failure signal and control the relevant input, clock, state, or interleaving with mechanisms already available where practical. Prefer an observable event or condition to an arbitrary delay. Preserve the sequence that exposes the bug; making the test deterministic must not remove the behavior under test. Record any seed or schedule needed to reproduce it, and do not treat one passing rerun as proof that flakiness is fixed.

## Output

Report Red, Cause, Fix, Green, Adjacent verification, and Unverified.

Name the failing-before and passing-after commands and their observed signals. If failing-before evidence could not be demonstrated, say why and describe the closest executable check used. Do not label an inferred failure as observed red or a passing-after check as a completed red-to-green sequence.

Report evidence, not ceremony.

Do not hide technical detail merely to simplify the language. Optimize for technical precision.
