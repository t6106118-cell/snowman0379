---
name: architect
description: Use for software architecture, design decisions, or structural refactoring. Ground the design in current requirements and contracts; when implementation is authorized, validate and revise it through small executable end-to-end slices.
---

# Architect

Explicit user and project instructions take precedence over this skill.

This skill adds a design workflow. When implementation is authorized, follow applicable project instructions and standing implementation and verification rules.

For design-only requests, inspect existing code and evidence, propose the minimal shape and next validation step, and label untested assumptions. Use the implementation steps below only when implementation is within the authorized task.

The design is provisional. Runtime evidence has authority over the sketch.

## 1. Ground the minimum system

Trace only the existing code needed to understand the first real path. Identify the entry point, exit point, data movement, ownership, side effects, mutable state, and external boundaries.

Use `how` when the runtime path is not already clear. Use `why` only when historical rationale could change a current design decision.

Do not study unrelated subsystems before the first executable slice needs them.

## 2. Define the thin slice

Write the smallest caller-visible behavior that can prove the mechanism works end to end.

Before deriving types, write a concrete caller example: what is supplied, what is called, what comes back, and how failure is observed. Check that the proposed signatures support that usage directly; revise the sketch rather than making callers accommodate accidental internals.

When a working path already exists, use it to investigate the design rather than rebuilding it without a concrete reason.

Derive only the types, signatures, and module boundaries required by that behavior.

A useful slice reaches the real unknown. Examples include one real request through parsing and output, one real file through load and write, one protocol message through encode and decode, or one command through parsing and its observable side effect.

Do not replace the essential unknown with mocks merely to make the slice pass.

## 3. Sketch only what the next run needs

Write a small usage sketch or type/signature sketch only when it makes the next executable step clearer.

Prefer concrete types, explicit ownership, one authoritative representation of each state value, direct data flow, and short call paths.

Trace the required reads, writes, and lookups through the proposed data structures. Address a demonstrated access requirement now; do not defer it to an unspecified future index or cache, or add either for hypothetical scale.

Prefer an interface that hides meaningful policy and complexity with few concepts for the caller to coordinate. Interface depth means useful behavior behind a simple surface, not more layers or a larger general-purpose API. Include caller effort and maintenance in the cost comparison.

Avoid speculative interfaces, factories for one implementation, generic registries, extension points, compatibility layers, pass-through wrappers, and modules created only because a future feature might need them.

When choosing or changing module, API, or state boundaries, use [references/design-review.md](references/design-review.md) to check concrete coupling and misuse risks. Do not turn every small change into a full architecture audit.

The sketch is not a contract.

## 4. Implement and run immediately

Implement the thin slice and run it before expanding the design.

Record what worked, what failed, which assumptions were confirmed, which assumptions were false, and the next smallest change.

If the mechanism itself does not work, stop building surrounding architecture. Fix or replace the mechanism first.

## 5. Extend one behavior at a time

For each addition, state the exact behavior, make the smallest coherent change, run the narrowest useful check, and confirm the existing path still works when relevant.

Do not batch several unverified design changes.

When a new requirement does not fit the current shape, first ask whether the current shape is wrong. Do not automatically add another mode, flag, adapter, optional field, or layer.

## 6. Simplify after evidence

Once behavior works, remove structure that no longer has a current reason to exist.

Delete one-implementation abstractions with no current substitution need, pass-through wrappers, duplicate state, compatibility branches, fallback parsers for obsolete internal formats, dead configuration paths, and defensive branches that hide programmer errors.

Require backward compatibility only when an explicit task requirement or established current contract needs it, including active external consumers, required formats, or persisted user data. When changing an internal API within scope, migrate current callers and remove the obsolete path.

## 7. Redesign when the pattern is wrong

One awkward line is not enough. Repeated friction is evidence.

Strong signals include the same workaround in several places, repeated special cases caused by one boundary, callers needing hidden internal knowledge, state repeatedly escaping its assumed owner, repeated casts or escape hatches, or a simple behavior requiring increasingly indirect call chains.

When that pattern appears, stop extending the current shape. Re-ground the path that now exists, state which assumption was false, remove obsolete structure, and build the new smallest end-to-end path.

Do not preserve the old internal architecture for consistency.

## Expensive-to-reverse decisions

Explore multiple designs only when a decision is materially expensive to reverse. Examples include a durable public protocol, persistent external data format, externally consumed API, destructive migration, or a major ownership boundary with several plausible shapes.

For decisions that are inexpensive to reverse, validate the smallest plausible shape when implementation is authorized.

## Output

For design-only work, provide the proposed usage, minimal shape, relevant contracts, untested assumptions, and next validation step. For small implementation tasks, provide the concrete usage, minimal shape, implementation, and verification result.

For larger work, maintain a concise map of the current executable path and the assumptions that remain unverified.

For consequential decisions, briefly record why this shape fits, its material tradeoffs, and the strongest realistic objection. When comparing alternatives is warranted, name the viable alternative and why it lost. Keep this rationale with the existing design or project record; no fixed template, page count, or separate document is required for a small change.

Do not produce a large architecture document merely because the task is non-trivial.
