---
name: technical-writing
description: Write or revise technical documentation, tutorials, how-to guides, references, design explanations, RFCs, and PR descriptions for precise, usable prose. Use for documentation structure and substantive technical editing; use proofread-math for conservative mathematical proofreading.
license: MIT; see LICENSE
metadata:
  adapted-from: cursor/plugins/pstack/skills/technical-writing
  upstream-revision: 2eb7ed4613cfc8f098dfe464a23680ea44d84c5e
---

# Technical writing

Make the reader's task clear and preserve the exact technical meaning. Use plain words where they express the same claim. Keep necessary terminology, symbols, qualifications, and uncertainty.

## Choose the document's purpose

Infer the audience and purpose from the request and existing document. Ask only when the missing distinction changes what should be written.

| Reader's need | Primary structure |
| --- | --- |
| Learn by doing | Tutorial: a runnable path, observable results, and enough explanation to understand each step. |
| Complete a specific task | How-to: prerequisites, conditional steps, commands, and checks of the result. |
| Look up exact behavior | Reference: consistent entries for inputs, outputs, defaults, errors, and constraints. |
| Understand a mechanism or decision | Explanation: the mechanism, evidence, alternatives that matter, and consequences. |

Choose a primary purpose; include supporting examples or reference material when they help. Do not force a document label, an outline, or a separate file for every purpose.

## Establish what is true

- For source-dependent claims, inspect the relevant implementation, configuration, tests, runtime evidence, or primary documentation. Read only what the document needs.
- Separate observed behavior, intended behavior, inference, and unresolved questions. Do not write that a command was run or a claim verified unless it was.
- When editing supplied text, preserve its meaning unless the user asks for substantive changes. Flag a false technical claim directly and support the correction; do not reinterpret it into a different, defensible claim.
- Preserve bounds, versions, units, identifiers, failure conditions, and distinctions such as necessary versus sufficient. Shorter wording must not broaden the claim.
- In mathematical or scientific writing, preserve hypotheses, quantifiers, equation meaning, and proof status. A style edit is not a proof repair. Use the existing math skills when substantive mathematical work is requested.

## Write the mechanism precisely

- Name the actor and operation: which function reads which input, changes which state, and produces which output. Replace vague claims such as "handles processing" with the actual behavior.
- Use active voice when it identifies responsibility. Use passive voice when the actor is irrelevant or unknown.
- Keep one main point per paragraph. Split a sentence when doing so clarifies dependencies; do not enforce arbitrary word limits.
- Use the same name for the same concept. Define an unfamiliar term once, near its first use. Keep identifiers exact and format them as code.
- Place modifiers and conditions next to what they constrain. Replace ambiguous pronouns with the relevant object. Make conjunctions explicit when "and" or "or" changes the required behavior.
- Remove filler, marketing claims, rhetorical questions, forced contrasts, and metaphors when a literal statement is available. Retain uncertainty when the evidence requires it.

## Make instructions executable

- State prerequisites before dependent steps. Put a condition before the action it controls.
- Start steps with the action. Show the common path first, then exceptions that affect completion.
- Keep commands faithful to the actual shell, working directory, and environment. Mark placeholders and pseudocode clearly; do not present them as tested commands.
- Describe the observable result of a consequential step and what a realistic failure means. Do not add recovery branches for imagined failures.
- Put destructive operations and their necessary authorization at the relevant step. Preserve the user's existing authorization rather than adding a second approval flow.
- Use lists for sequences and tables for exact mappings or comparisons. On a terminal, use ASCII diagrams when relationships need a visual explanation. Create richer artifacts only when they serve the request.

## Adapt to the requested artifact

- For a design document or RFC, explain the concrete problem, the smallest viable mechanism, evidence supporting the choice, and material unresolved decisions. Do not invent a complete architecture for unreleased research code.
- For a PR description, lead with the triggering problem and resulting behavior. Include meaningful validation and limitations. Use a repository template when one exists.
- For a commit message, state the concrete change and its reason; avoid copying the whole implementation narrative.
- Preserve an existing document's useful structure and scope. Do not make code changes merely to make the prose true.

Before finishing, check the result against the source for semantic changes, broken references, unsupported claims, and unusable steps. Follow the user's output policy: put a long result in a file and return its path with a short summary.
