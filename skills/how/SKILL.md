---
name: how
description: 'Trace how code actually works: runtime flow, data movement, ownership, state, boundaries, and placement. Use for "how does X work", subsystem architecture overviews, code walkthroughs before changing a subsystem, or questions about where code should live.'
---

# How

Explicit user and project instructions take precedence over this skill.

Build a concrete model of how the code works. Do not modify product code unless the user also asks for a change.

Do not invent a cleaner architecture than the implementation actually has.

## 1. Fix the question

Identify the exact target and what the user wants to understand.

Use the installed [why skill](../why/SKILL.md) when historical motivation or design rationale is part of the question. Reuse the current trace and investigate history only where it can change the explanation.

If the referent is clear from context, proceed. If it is slightly ambiguous, state the interpretation and investigate it. Do not block on a clarification that the repository can resolve.

Start narrow. Expand only when the traced path requires it.

For a broad architecture question, identify the distinct execution paths and responsibilities needed to answer it. Trace each relevant path, then explain how they connect through data, state, ownership, and external boundaries. Scale the investigation to the question; a narrow question needs only its own path.

## 2. Find the real entry point

Start from the path real execution uses, not from filenames that merely sound relevant.

Examples include a CLI command through argument parsing, an HTTP route through its handler, a library export through its implementation, a scheduled task through its worker, or a UI action through its state transition and side effect.

Establish the entry point from code, configuration, tests, or runtime evidence.

## 3. Trace the path end to end

Follow execution until the requested behavior is explained.

Track calls and returns, data-shape changes, ownership and lifetime, mutable state and writers, I/O, persistence, concurrency, synchronization, error propagation, subprocesses, environment inheritance, serialization, protocol transitions, and important third-party behavior.

Use symbol search as an index, not as proof. Read the definitions and the callers that establish behavior.

When a third-party library controls a material behavior, inspect the pinned version's source or authoritative documentation when practical. Do not infer semantics from a function name.

## 4. Verify material uncertainty

When static reading leaves an ambiguity that changes the answer, obtain direct evidence.

Prefer the cheapest useful method: read the defining code, inspect a focused test, run a small command or script, add temporary instrumentation, or reproduce the real path.

Do not turn a read-only investigation into a large implementation project.

## 5. Answer ownership from the trace

For "where should this live" questions, identify where the relevant invariant, state, or body of knowledge already lives.

Prefer the location that already owns the data or invariant, avoids threading a new signal through unrelated layers, avoids one-caller wrappers, keeps external parsing at the boundary, and reduces the number of files a reader must trace.

Do not create a new layer merely because the current task needs a place to put code.

## Output

Briefly define unfamiliar types or services only when the reader needs them to follow the flow. Include Key concepts or a compact file map when useful; omit them when the mechanism is already clear.

Use only the sections that improve the answer: Overview, Runtime flow, Data and state, Boundaries, Where things live, and Gotchas.

Name real functions, types, files, commands, processes, and protocols when available.

Anchor important claims about behavior or ownership to the relevant file and symbol or line so the reader can check them. Cite the evidence that establishes the claim rather than listing every file inspected.

Distinguish observed behavior from inference. Say when a relevant path could not be traced. A search with no matches proves absence only in the searched scope.

Do not dump annotated source code. Explain the mechanism.

Do not hide technical detail merely to simplify the explanation. Optimize for technical precision.
