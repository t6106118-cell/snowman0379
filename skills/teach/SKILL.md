---
name: teach
description: Explain how code, systems, or technical ideas work at a depth suited to the reader, using concrete examples and evidence for design rationale. Use for learning requests, walkthroughs, and combined how-and-why explanations; use how alone for focused runtime tracing and why alone for historical investigation.
license: MIT; see LICENSE
metadata:
  adapted-from: cursor/plugins/pstack/skills/teach
  upstream-revision: 2eb7ed4613cfc8f098dfe464a23680ea44d84c5e
---

# Teach a technical mechanism

Help the reader understand the actual mechanism well enough to follow an input, predict an output, and explain a relevant design choice. Keep the technical detail that makes the explanation correct.

## Set the depth and evidence

Infer the reader's goal and prior knowledge from the request. Honor explicit requests for low-level detail, brevity, or a complete walkthrough. Ask about missing context only when it changes the explanation; continue independent inspection meanwhile.

For code or system behavior, read and apply the existing [how skill](../how/SKILL.md) to trace the relevant path. When the question includes design rationale, use the [why skill](../why/SKILL.md) for the evidence needed to explain it. Do not run a broad history investigation when the reader only needs current behavior.

These skills contribute investigation methods, not mandatory parallel agents or model roles. Reuse evidence already available in the authorized task state rather than repeating the same inspection.

## Build the explanation from a concrete path

- Start with the mechanism or result the reader asked about. Define only the terms needed to understand that point.
- Pick a representative input and trace it through the actual entry point, relevant calls, transformations, state changes, and output. Use real identifiers and value shapes.
- At each important boundary, identify who owns the value or state, what is copied or referenced, which operation happens, and what failure or synchronization behavior matters.
- Distinguish language semantics, runtime behavior, operating-system interaction, and hardware behavior when that distinction explains the result. Inspect lower layers if needed; do not invent allocation, instruction, or network details from a high-level API name.
- Explain the observed design choice using source or history evidence. Label a plausible reason as inference and an unavailable reason as unknown. Do not attribute intent to an author without evidence.
- Correct a false premise directly before building on it. Do not substitute a different claim to make the reader's statement appear true.

For a mathematical or scientific concept, give the exact definitions, assumptions, claim, and a small example that satisfies them. Explain which step depends on which hypothesis. Keep a proof, a numerical experiment, and an intuition distinct; use the existing specialist math workflow when proof or citation verification is requested.

## Make the relationships visible

Use a compact ASCII diagram for control flow, ownership, dependencies, or state transitions when it makes the explanation easier to follow. Use a table for exact mappings or comparisons. Keep labels tied to the actual code or definitions.

For example, an explanation of a queue might use this structure only after checking that it matches the implementation:

```text
caller -> enqueue(value) -> queue state -> consumer -> result
```

Use the installed diagram or visual-explanation skills when the user needs an exported or interactive artifact. Do not make image generation a default step in an ordinary explanation.

## Deliver the requested depth

- Connect each example to the general rule it demonstrates. Show a boundary case when it exposes a real limit or common misconception.
- Validate a central, uncertain behavior with the cheapest meaningful execution when feasible. Say whether an example was executed or is illustrative.
- If the user asks for an interactive lesson, teach one coherent part and let their answer guide the next part. Otherwise deliver the complete requested explanation without forced quizzes or pauses after a fixed sentence count.
- End with any material uncertainty or a relevant next step, without adding unrelated exercises, architecture changes, or code edits.

Follow the user's output policy: save a long explanation to a file and return a short summary and path. Preserve precise mechanisms and uncertainty while editing the prose.
