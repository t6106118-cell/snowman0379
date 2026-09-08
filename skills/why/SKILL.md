---
name: why
description: Investigate why code has its current shape using source history, commits, pull requests, issues, documents, tests, and runtime evidence. Use for design rationale, regressions, defensive code, thresholds, or "why do we do this".
---

# Why

Explicit user and project instructions take precedence over this skill.

Investigate the evidence behind a design decision or code shape. Do not guess intent from the current implementation and present the guess as fact.

Use `how` when the primary question is runtime behavior. Use this skill when the question is motivation, constraints, history, or tradeoffs.

## 1. Anchor the target

Identify the relevant current files, symbols, behavior, and definitions whose history matters. Trace enough of the current path to know what decision you are investigating.

If the target is slightly ambiguous, state the interpretation and proceed from evidence.

## 2. Trace source history first

Use local source-control history as the default evidence source.

Useful evidence includes blame, file history through renames, commits that introduced or changed the behavior, search by added or removed strings, and the actual patch.

For substantive merge commits, inspect the associated pull request when available. Read its body, review discussion, linked issues, and diff.

Do not assume the newest commit explains the original decision. Trace far enough back to find when the behavior was introduced or materially changed.

## 3. Expand only when another source can change the answer

Possible sources include repository issues, ADRs or design documents, README or reference documentation, tests that encode a constraint, incident records, team discussion available through connected tools, runtime or error evidence for defensive code, and measurements for data-driven thresholds.

Do not perform a ceremonial sweep of every possible source. Search a source when it plausibly contains evidence for the question.

Record unavailable evidence as a limitation only when its absence materially weakens the conclusion.

## 4. Inspect defensive and compatibility code carefully

For retries, nil checks, timeout handling, feature flags, fallback parsing, compatibility branches, and similar defenses, determine what condition they protect against now.

Classify the condition as a current external requirement, a current internal invariant violation, a historical bug that is still reachable, backward compatibility only, an obsolete condition, or unknown.

Historical existence is not a current requirement.

For unreleased research code, backward compatibility alone is not a reason to preserve code. If all current internal callers can move, migrate them and delete the legacy path.

## 5. Separate historical reason from current validity

Answer two different questions:

1. Why was this introduced?
2. Does that reason still apply now?

Check current callers, dependencies, protocol requirements, persisted data, and tests before recommending preservation.

A historically valid reason may now be obsolete.

## 6. Classify conclusions

Use these confidence classes:

- **Explicit evidence:** a commit, pull request, issue, document, test, or author statement directly gives the reason.
- **Strong inference:** several concrete facts support the explanation, but no source states it directly.
- **Hypothesis:** plausible, but evidence is incomplete or competing explanations remain.
- **Unknown:** available evidence does not support a reliable explanation.

Never rewrite an inference as historical fact.

## Output

Use a compact structure: Question, Code in question, Evidence, Conclusion, Competing explanations, What is unknown, and If changing this code.

When a change is likely, classify current constraints as Preserve, Change, Delete, and Risk.

Prefer primary sources over retrospective summaries. Cite exact commits, pull requests, issues, files, symbols, or documents when available. Do not invent author intent. Do not treat a comment as authoritative when runtime behavior contradicts it.

Do not hide technical detail merely to simplify the language. Optimize for technical precision.
