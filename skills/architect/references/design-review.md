# Review module and state boundaries

Use these checks when a design introduces or changes a meaningful boundary. Follow an actual caller and state change through the proposed shape. Look for a change that seems correct in one file but silently requires coordinated edits elsewhere. Check the relevant consumers; do not infer whole-system correctness from the nearest example.

A flag identifies a question to investigate, not an automatic defect or a reason to add infrastructure. Revise the shape when evidence shows unnecessary coupling or a current correctness risk. Preserve required external contracts, user data, and justified adapters.

| Signal | Concrete check and smallest useful response |
| --- | --- |
| Shallow interface | Must callers coordinate internal stages to complete one operation? Keep related policy with the module that can finish it; hide complexity without creating a general-purpose facade. |
| Leaked representation | Would changing storage, transport, or framework details force unrelated business callers to change? Keep those details behind the responsible boundary when this removes real coupling. Introduce a domain representation only when the distinction earns its translation cost; preserve protocols that are themselves required public contracts. |
| Modules split only by execution stage | Do load, validate, transform, and save modules repeat the same representation and invariants? Group knowledge that changes together. Keep separate stages when streaming, resource lifetimes, independent behavior, or another current requirement justifies them. |
| Pass-through layers | Does a wrapper merely forward the same arguments? Remove it unless it provides required policy, adaptation, or a meaningful contract. |
| Split state ownership | Can several modules write the same state or maintain independent authoritative copies? Identify one owner for each value. For actual concurrent writers, consider separate state and an explicit merge only when domain semantics permit; otherwise define the required coordination and conflict behavior. |
| Equivalent competing paths | Can callers perform the same operation through obsolete or inconsistent interfaces? Migrate current callers and remove the redundant path within scope. Keep distinct paths that serve required consumers or semantics. |
| Importable internals | Can a caller bypass a required invariant by importing implementation details? Use existing visibility or package-export controls where supported. Do not create a new build system merely to enforce privacy; verify the relevant callers and boundary checks instead. |
| Hand-maintained duplicate lists | Must one fact be edited in several registries or configuration lists? Derive them from one authoritative source where practical. If independent lists are required and divergence is consequential, use a focused consistency check. |

For a state-changing operation that can actually be retried, interrupted, or resumed, trace a second invocation and a failure halfway through. Identify what is committed and what the caller sees. Choose idempotence, explicit conflict handling, or recovery that satisfies the required behavior; do not assume every operation is naturally repeatable.

Prefer types and structural ownership that make invalid use difficult when the language supports them. Validate external inputs at the responsible boundary, and fail explicitly if a required internal invariant is violated. Comments explain intent; they do not replace necessary enforcement.
