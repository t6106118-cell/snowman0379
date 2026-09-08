---
name: research-code
description: Use for implementation, refactoring, debugging, or design in unreleased research or prototype code where backward compatibility is not required. Build the smallest runnable end-to-end path first, verify it, then extend it through small verified changes.
---

# Research code

Explicit user and project instructions take precedence over this skill.

Treat the codebase as unreleased research software when the user or project context says it is. Do not infer a production compatibility requirement from old code alone.

The objective is a correct, observable result through the smallest implementation that is easy to inspect and debug. Executable evidence has priority over speculative design.

## Core rule

Build the smallest complete end-to-end vertical slice that reaches the real boundary that matters. Run it before designing or implementing the rest of the system.

A sketch, type design, API, or module boundary is a hypothesis. Change or delete it when implementation or runtime evidence disproves it.

Do not design the complete architecture up front when a smaller executable experiment can answer the important question.

## Work loop

1. Ground only enough of the existing system to identify the real path, ownership, inputs, outputs, side effects, and external boundaries needed for the next change.
2. Remove obsolete code first when it directly complicates the path.
3. Implement the smallest complete end-to-end slice.
4. Run that path immediately.
5. Confirm the expected observable result.
6. Add one meaningful behavior or capability.
7. Run the narrowest useful check immediately after that addition.
8. Continue only after the changed path is understood and working.
9. Simplify structure when working code exposes unnecessary complexity.
10. Before completion, run the complete affected end-to-end path again.

Do not batch several unverified behavioral changes when they can be introduced and checked separately.

## Simplicity

Prefer the least code and the fewest concepts that correctly implement the observed requirement.

Prefer deletion before addition.

Remove dead code, one-caller wrappers that hide nothing, pass-through layers, duplicated decisions, obsolete APIs, redundant validators, compatibility-only branches, and abstractions that have no current use.

Do not create an interface, registry, framework, plugin point, configuration option, factory, adapter layer, or generalized abstraction only because future work might need one.

Three explicit statements can be better than a premature abstraction.

Keep mutable state as local as practical. Keep call paths short enough that a reader can trace the mechanism directly.

Do not hide technical detail merely to simplify the language. Optimize for technical precision.

## No backward compatibility

Backward compatibility is not a requirement for unreleased internal research code unless the user identifies a real compatibility boundary.

Do not add or preserve compatibility shims, legacy API paths, deprecated aliases, fallback parsers for obsolete formats, migration layers for old internal state, dual old/new implementations, deprecation periods, or feature flags whose only purpose is preserving the old path.

When a better internal API or representation replaces an old one, migrate current callers and delete the old path in the same change sequence.

If code exists only for backward compatibility, remove it.

Delete or rewrite tests whose only purpose is preserving obsolete behavior.

Real external boundaries still matter. Examples include an existing persisted user format, a current protocol peer, a third-party API, or an explicitly supported external consumer. Preserve such contracts only when they are actual current requirements.

## Failure policy

Fail loudly on programmer errors and broken internal invariants.

Use an assertion, panic, exception, or hard error when continuing would hide a bug or create misleading state.

Do not catch an internal error only to log it and continue. Do not add a nil or null check only to suppress a crash whose cause is still unknown. Do not silently substitute defaults for impossible internal states. Do not convert an invariant violation into success.

External failures are different. Handle realistic boundary failures explicitly when they are part of the actual environment, including invalid user input, missing files, network failure, unavailable services, resource exhaustion, and conditions that can cause data loss.

Validate untrusted data at the boundary. After conversion into a valid internal representation, trust established internal invariants instead of repeating defensive validation through the call chain.

## Debugging

Reproduce before fixing when a practical reproduction exists.

Instrument instead of guessing. Inspect the actual values, errors, state transitions, files, requests, responses, timings, or system calls involved.

Fix the root cause, not the visible symptom.

If two or more attempted fixes fail while relying on the same assumption, write that assumption down and test it directly before attempting another fix based on it.

Do not add fallback behavior merely because it makes the immediate failure disappear.

## Verification

Compilation is necessary when applicable, but compilation alone is not proof that the change works.

Prefer direct proof in this order when practical:

1. Run the actual affected end-to-end path.
2. Run a focused executable reproduction or script against the real code.
3. Run a behavior-level test through the real public or user-facing entry point.
4. Use narrower unit checks when they provide useful local signal.

After every meaningful change, perform the cheapest check that would catch a failure introduced by that change.

A failing test before a bug fix is useful when it is cheap and direct. Do not build a large harness merely to satisfy TDD ceremony. If the user explicitly invokes the `tdd` skill, follow that workflow.

Test observable behavior rather than internal call choreography. Prefer no test over a test that only verifies mocks or implementation details.

## Types and structure

Use types and data structures to encode invariants that the real implementation has exposed.

Do not construct an elaborate domain model before the first runnable path unless the problem itself requires it.

When working code develops repeated branching, synchronized booleans, casts, impossible-state checks, or scattered assumptions about one shape, replace them with a simpler type or data structure that encodes the actual invariant.

Do not strengthen a type merely to make it more abstract or theoretically complete.

## Refactoring and redesign

Refactor from evidence, not aesthetics alone.

Strong triggers include repeated workarounds, repeated branches encoding one decision, callers needing hidden knowledge of an abstraction, real shared-state coordination problems, repeated casts or impossible-state checks, and repeated friction against the same module or type boundary.

When the structure is wrong, redesign as if the newly discovered constraint had been known from the start.

Remove obsolete structure before adding its replacement. Do not bridge old and new internal research architectures for compatibility unless explicitly required.

Keep each meaningful redesign step runnable or otherwise directly verifiable.

## Concurrency

Before adding a lock or serialization mechanism, ask whether the actors need to share mutable state at all.

Prefer separate ownership when the problem permits it. Add synchronization only when shared mutable state is a real invariant.

## Scope discipline

Do not solve hypothetical future requirements. Do not harden every theoretical edge case. Do not add extensibility merely because future work is imaginable. Do not optimize an unmeasured path unless the task is explicitly about performance or the cost is directly obvious on the hot path.

Do not turn a research prototype into production infrastructure without an explicit requirement.

## Completion contract

Before reporting completion, state what real path was exercised, what observable result proves the change works, what meaningful additions were verified independently, what obsolete or compatibility-only code was removed, and what remains unverified or uncertain.

If the decisive path was not run, say so. Do not present inferred success as verified.
