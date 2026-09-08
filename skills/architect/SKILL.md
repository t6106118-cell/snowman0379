---
name: architect
description: Use when the user asks to architect, design, or reshape non-trivial unreleased research code. Derive the design from the smallest executable end-to-end slice, then revise the shape from runtime evidence instead of committing to speculative architecture.
---

# Architect

Explicit user and project instructions take precedence over this skill.

Apply the `research-code` policy when it is available. This skill adds a design workflow. It does not replace the research-code rules.

The design is provisional. Runtime evidence has authority over the sketch.

## 1. Ground the minimum system

Trace only the existing code needed to understand the first real path. Identify the entry point, exit point, data movement, ownership, side effects, mutable state, and external boundaries.

Use `how` when the runtime path is not already clear. Use `why` only when historical rationale could change a current design decision.

Do not study unrelated subsystems before the first executable slice needs them.

## 2. Define the thin slice

Write the smallest caller-visible behavior that can prove the mechanism works end to end.

Derive only the types, signatures, and module boundaries required by that behavior.

A useful slice reaches the real unknown. Examples include one real request through parsing and output, one real file through load and write, one protocol message through encode and decode, or one command through parsing and its observable side effect.

Do not replace the essential unknown with mocks merely to make the slice pass.

## 3. Sketch only what the next run needs

Write a small usage sketch or type/signature sketch only when it makes the next executable step clearer.

Prefer concrete types, explicit ownership, one authoritative representation of each state value, direct data flow, and short call paths.

Avoid speculative interfaces, factories for one implementation, generic registries, extension points, compatibility layers, pass-through wrappers, and modules created only because a future feature might need them.

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

Backward compatibility is not a design constraint for unreleased internal research code unless the user identifies a real external boundary.

## 7. Redesign when the pattern is wrong

One awkward line is not enough. Repeated friction is evidence.

Strong signals include the same workaround in several places, repeated special cases caused by one boundary, callers needing hidden internal knowledge, state repeatedly escaping its assumed owner, repeated casts or escape hatches, or a simple behavior requiring increasingly indirect call chains.

When that pattern appears, stop extending the current shape. Re-ground the path that now exists, state which assumption was false, remove obsolete structure, and build the new smallest end-to-end path.

Do not preserve the old internal architecture for consistency.

## Expensive-to-reverse decisions

Explore multiple designs only when a decision is materially expensive to reverse. Examples include a durable public protocol, persistent external data format, externally consumed API, destructive migration, or a major ownership boundary with several plausible shapes.

For ordinary research code, implement the smallest plausible shape and test it.

## Output

For small work, provide the concrete usage, minimal shape, implementation, and verification result.

For larger work, maintain a concise map of the current executable path and the assumptions that remain unverified.

Do not produce a large architecture document merely because the task is non-trivial.
