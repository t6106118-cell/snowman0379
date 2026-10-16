# TypeScript patterns

Examples illustrate choices, not required abstractions. Reuse repository conventions. The TypeScript blocks below can be combined in order into one module; no packages are needed. They are intended for strict typing and `noUncheckedIndexedAccess`; a real project must use its own compiler/configuration.

## Variants and exhaustive failure

Use a union when a state determines which fields exist. An independently optional field does not need a state machine.

```ts
type Job =
  | { kind: "queued" }
  | { kind: "done"; result: string }
  | { kind: "failed"; message: string };

function describeJob(job: Job): string {
  switch (job.kind) {
    case "queued": return "Waiting";
    case "done": return job.result;
    case "failed": return job.message;
    default: {
      const unreachable: never = job;
      void unreachable;
      throw new Error("Unexpected job variant");
    }
  }
}
```

Adding a variant requires handling it. The error also prevents a silently successful return if malformed runtime input bypasses the boundary. This function is not a replacement for parsing untrusted data.

## Useful collection constraints

```ts
type NonEmpty<T> = readonly [T, ...T[]];

function first<T>(values: NonEmpty<T>): T {
  return values[0];
}

function sum(values: readonly number[]): number {
  return values.reduce((total, value) => total + value, 0);
}

function atIndex<T>(values: NonEmpty<T>, index: number): T | undefined {
  return values[index];
}
```

Empty input is valid for `sum`. A nonempty tuple proves that index zero exists; it does not prove a random or caller-supplied numeric index exists. If absence violates the caller's contract, check it explicitly there. Use pairs only when the real data is a sequence of pairs; preserve a required external flat format at its boundary.

## Validate numeric invariants explicitly

```ts
function rangeEnd(startMs: number, durationMs: number): number {
  if (!Number.isFinite(startMs) ||
      !Number.isFinite(durationMs) || durationMs < 0) {
    throw new Error("Expected a finite start and nonnegative finite duration");
  }
  const endMs = startMs + durationMs;
  if (!Number.isFinite(endMs)) {
    throw new Error("Range end exceeds finite numeric bounds");
  }
  return endMs;
}
```

Representing a range with a duration removes one relationship between two endpoints, but plain `number` does not enforce nonnegativity. Date validity, integer precision, units, and application limits require checks if the contract needs them. A reusable validated value type can help when repeated confusion justifies it.

## Truthful boundary checks

Use the schema library already present when appropriate and infer its parsed output type. For a small shape with no such dependency, a guard can be enough:

```ts
type User = { id: string; active: boolean };

function isUser(value: unknown): value is User {
  return typeof value === "object" && value !== null &&
    "id" in value && typeof value.id === "string" &&
    "active" in value && typeof value.active === "boolean";
}

function parseUser(value: unknown): User {
  if (!isUser(value)) throw new Error("Invalid user payload");
  return value;
}

type UserSummary = Pick<User, "id">;
```

This example permits empty IDs and additional properties because its stated `User` shape permits them. Add stricter value/unknown-field rules only when the actual contract requires them. A handwritten predicate is a promise by the author; the compiler does not prove its implementation truthful.

## A justified brand assertion

```ts
type AgentId = string & { readonly __brand: "AgentId" };

function parseAgentId(value: unknown): AgentId {
  if (typeof value !== "string" || !/^agent_[a-z0-9]+$/.test(value)) {
    throw new Error("Invalid agent ID");
  }
  // The preceding check establishes this example's complete ID contract.
  return value as AgentId;
}

function agentPath(id: AgentId): string {
  return `/agents/${id}`;
}
```

The prefix grammar is illustrative, not a UUID rule or workstation-wide ID convention. Keep the assertion at the validated constructor; do not scatter casts among callers. Brands protect ordinary typed assignments, not arbitrary JavaScript or deliberate assertions.

## Compatibility checking and literal inference

```ts
type RetryOptions = { mode: "bounded" | "disabled"; attempts: number };

const retryOptions = {
  mode: "bounded",
  attempts: 3,
} as const satisfies RetryOptions;
```

`satisfies` checks compatibility during typechecking. `as const` intentionally requests readonly literal inference here; neither checks a JSON payload at runtime. Use them only when the supported compiler and desired mutability fit. An annotation is also valid when a widened public type is intended.

## Language references

- [TypeScript narrowing and exhaustiveness](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)
- [satisfies, TypeScript 4.9](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html)
- [noUncheckedIndexedAccess](https://www.typescriptlang.org/tsconfig/noUncheckedIndexedAccess.html)
