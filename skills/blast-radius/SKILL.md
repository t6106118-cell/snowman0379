---
name: blast-radius
description: Find what a code change can break beyond the visible diff, then prove the important safety assumptions with real execution. Use for "blast radius", "what could this break", risky refactors, or a diff you do not trust yet.
---

# Blast radius

Explicit user and project instructions take precedence over this skill.

Determine what a change can break outside the edited lines. The objective is not a long risk list. Find the real affected contracts and verify the facts that make the change safe or unsafe.

Use `how` when the runtime path is unclear. Use `why` when historical constraints may still matter. Apply `research-code` for unreleased research software.

## 1. Establish the exact behavioral change

Read the full diff and enough surrounding code to state what behavior changed, what was deleted, which symbols or formats changed, what callers now observe differently, and any effect that is not obvious from the diff itself.

Do not review only added lines.

## 2. Find visible dependents

Search callers, implementations, imports, exports, constructors, config keys, environment variables, serialized fields, command-line flags, routes, persisted keys, filenames, generated artifacts, tests, and fixtures.

This is the visible dependency set, not the complete blast radius.

## 3. Follow hidden contracts

Check contracts that symbol search may not connect directly to the changed code: wire and file formats, database or cache data, another process or language reading the same bytes, reflection or string registration, dynamic loading, subprocess behavior, environment inheritance, ordering, timing, teardown, concurrency, shared state, third-party library semantics, build generation, external services, and persisted user data.

Inspect the pinned third-party version when its behavior is part of the safety argument.

## 4. Distinguish real boundaries from obsolete internal compatibility

For unreleased research code, existing internal callers are migration work. They are not a reason to preserve the old API.

Migrate current callers and delete the legacy path when the old path has no other requirement. Do not propose a flag, shim, fallback parser, alias, adapter, or dual implementation only to reduce internal migration work.

Real compatibility boundaries still count. Examples include a current external consumer, existing persisted data, a protocol peer, a third-party API, or user-owned files. Name these explicitly.

## 5. Identify the critical safety facts

Reduce the review to one to three facts that determine whether the change is safe.

Examples include all live callers were migrated, no external process reads the removed field, cleanup happens after every consumer releases the object, or a dependency copies an input rather than retaining it.

Do not hide uncertainty behind "looks safe".

## 6. Prove the critical facts

Use the strongest cheap evidence available:

1. Located in concrete code or authoritative dependency source.
2. Traced through the failure path.
3. Executed with a focused test, script, or command that fails loudly if the fact is false.
4. Reproduced through the running end-to-end path.

Aim for execution when the fact determines correctness. If a fact remains only statically supported, say so.

Temporary proof code should be minimal. Keep it only when it has continuing verification value.

## 7. Report only reachable risks

For each remaining risk, state the exact failure mode, affected boundary or consumer, evidence that the path exists, likelihood based on observed state, impact, and cheapest resolving check.

Do not fill the report with theoretical edge cases that have no reachable path.

List investigated and cleared concerns separately.

## Output

Use these sections: What changed, Critical safety facts, Real risks, Cleared, Compatibility boundary, Verification.

Do not trust the diff author's summary as proof. Do not invent consumers or APIs. Do not preserve dead compatibility code to make the review look safer. Do not add defensive branches instead of fixing a root cause. Do not declare safety from compilation alone.

Do not hide technical detail merely to simplify the language. Optimize for technical precision.
