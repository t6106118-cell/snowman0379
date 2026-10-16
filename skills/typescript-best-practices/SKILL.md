---
name: typescript-best-practices
description: Write, refactor, or review TypeScript and TSX with accurate domain types, boundary validation, narrowing, and explicit failure behavior. Use for TypeScript implementation or type-safety questions; complements the implementation, debugging, and review workflows.
license: MIT
---

# TypeScript best practices

Use the simplest types and code that satisfy the current contract. Apply to ordinary application, library, CLI, production, and research code without a release-status gate. A review or explanation does not authorize edits.

## Start from the actual project

- Read applicable project instructions, relevant code, package scripts, and the effective `tsconfig` including inherited settings. Reuse its compiler version, framework, package manager, schema library, generated types, logger, and test conventions.
- Use the project's existing runtime and local dependencies. Do not assume a global `tsc`, create another environment, install a schema library, change compiler settings, or rewrite public APIs just to satisfy this skill.
- Work on the behavior and types affected by the request. Keep `tdd`, when applicable, or the selected implementation/review workflow responsible for execution strategy; this skill supplies TypeScript-specific decisions. It does not require any other skill to be installed or invoked first.

## Choose types that express real constraints

| Concern | Guidance |
| --- | --- |
| Variants | Use a discriminated union when fields depend on a state or variant. Optional fields are appropriate when independently optional. |
| Primitive identities | Reuse existing branded/opaque IDs when confusing equal-shaped values is a real risk. Validate at construction; a brand alone provides no runtime protection. Do not brand every primitive. |
| Collection shape | Keep `T[]` when empty input has valid behavior. Use nonempty tuples or fixed pairs when the actual contract requires that shape; return `undefined` or an explicit result when absence is legitimate. |
| Numeric invariants | A `number` can be negative, nonfinite, or out of range. A start-plus-duration representation still needs required numeric/date validation. |
| Existing type sources | Derive from the authoritative schema, generated API, or existing type using inference or suitable utility types. Avoid manually synchronized duplicates; do not add code generation or elaborate generics for a trivial shape. |
| API arguments | Use named object parameters when they clarify ambiguous arguments. Preserve clear positional conventions and current contracts; measure allocation concerns before optimizing. |

## Validate and narrow where the evidence supports it

- Treat genuinely untrusted input as `unknown`: decoded JSON, user input, storage, or external messages whose shape has not been checked. Typed APIs are useful evidence, but TypeScript annotations do not validate runtime data.
- At a trust boundary, parse the required shape and values using the repository's existing schema library or a small truthful guard. Infer the type from the schema when supported. Avoid repeated validation inside established invariants; retain hard errors for impossible internal states.
- A guard must establish every property its predicate promises, including nullability and relevant value constraints. `in` checks property presence, not its value type. Choose narrowing that proves the needed fact; there is no universally correct ranking of narrowing operators.
- Prefer narrowing or correcting the model to unsafe `any`, non-null assertions, or double casts. A narrow, documented assertion is acceptable where a validated invariant or real interoperability constraint cannot be expressed directly. Assertions and `as const` add no runtime checks; a cast does not itself execute or necessarily cause a crash.
- For known finite variants, make missing cases a compile error with `never`; also throw explicitly if the impossible branch executes. Reuse an existing exhaustiveness helper when suitable.
- Use `satisfies` for compile-time compatibility checks when the project's TypeScript version supports it. It does not validate external input at runtime or guarantee preservation of every literal under contextual inference. Use `as const` when readonly literal inference is intended.
- Decide unknown-field handling, format versions, and recovery from the current input/data contract. Do not automatically ignore fields, swallow parse errors, introduce migration layers, or convert every transport object into a separate domain model.

## Verify the affected behavior

- Run the relevant existing typecheck/build and the smallest useful behavioral check. Successful transpilation or a dev server does not necessarily run the typechecker. Respect existing strictness; do not silence diagnostics with broader types or disabled checks.
- Under `noUncheckedIndexedAccess`, an arbitrary numeric index can still yield `undefined` even for a nonempty tuple. Verify the actual access, bounds, or failure behavior instead of adding `!`.
- Prefer the real local component or framework primitive when practical. Use focused fakes at genuine external boundaries when that is the smallest faithful check. Do not build a mock-heavy harness or add tests solely for a mechanical type edit.
- Follow the project's logging and output contract. Structured diagnostics help when available; CLI stdout, intentional console output, and structured logging each have valid uses. Avoid leaking secrets or contaminating machine-readable output.
- Report the checks actually run and their limits. Typechecking, runtime behavior, and UI inspection establish different facts; none alone proves every input is safe.

Read [patterns](references/patterns.md) only for examples relevant to the current change.

## Source

Adapted for Codex CLI from [pstack/typescript-best-practices](https://github.com/cursor/plugins/tree/f713f14203cd6420cec13cd7c55c32d598dbab68/pstack/skills/typescript-best-practices), commit `f713f14203cd6420cec13cd7c55c32d598dbab68`. Original copyright and MIT terms: [LICENSE](LICENSE). This installation is self-contained and has no dependency on project audit records or uninstalled principle skills.
