---
name: tdd
description: Use for explicit TDD requests, regression-test-first bug fixes, or bugs with an obvious cheap local executable check. Do not force TDD when the useful test path is expensive, mock-heavy, or less direct than a real reproduction.
---

# TDD bug fix

Explicit user and project instructions take precedence over this skill.

Make the broken behavior executable before changing production code when there is a cheap, meaningful test path.

This is a debugging workflow, not a requirement to test everything first. The objective is a focused red-to-green check that gives fast localization and useful regression evidence.

Apply `research-code` for unreleased research software.

## 1. Define observable failure

State the intended behavior, current behavior, smallest reproducing input or sequence, and boundary where the wrong result becomes observable.

Do not begin by changing implementation details.

## 2. Choose the cheapest meaningful executable check

Prefer an existing test level close to the bug. A focused unit or component test is good when it exercises real behavior. Otherwise use a focused integration test, small executable script, CLI or HTTP reproduction, or the real end-to-end path.

Choose the narrowest check that still observes the defect.

Do not create a large harness, broad fixture system, or mock architecture only to satisfy TDD.

## 3. Prove red before the production edit

Write or select the smallest check that would have caught the defect and run it before the fix.

The failure must be the intended failure. If the check passes or fails for setup, fixture, import, timing, or unrelated reasons, fix the check first.

Record the exact failing command and failure signal.

## 4. Find the root cause

A red test establishes the behavior boundary. It does not identify the cause automatically.

Trace the failing path. Instrument when needed.

Do not add a nil check, retry, catch, fallback, or default merely to make the test green when that would hide an invariant violation.

Fail loudly on programmer errors and impossible internal states. Handle realistic external failures at the appropriate boundary.

## 5. Make the smallest root-cause change

Change only what is needed to make the intended behavior true.

For unreleased research code, backward compatibility is not a requirement unless explicitly identified. Do not add a flag, compatibility shim, deprecated path, alias, or fallback only to preserve obsolete behavior.

If the correct fix changes an internal API, migrate the current callers and delete the obsolete path.

Do not weaken the fix to preserve a legacy test whose only purpose is obsolete behavior.

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

## Output

Report Red, Cause, Fix, Green, Adjacent verification, and Unverified.

Report evidence, not ceremony.

Do not hide technical detail merely to simplify the language. Optimize for technical precision.
