# Persistent project records

Read this when bootstrapping, restructuring or compacting records, or when record ownership is unclear. Keep the structure proportional to the actual task. Reuse established conventions rather than migrating merely to match an example.

## Local entrypoint

Use <project-root>/AGENTS.md as the continuation entrypoint. Preserve user/project instructions. Manage the state index only inside the section titled Codex persistent-state index, bounded by:

```markdown
## Codex persistent-state index
<!-- codex-state-index:start -->
Project goal: <one sentence>.

Before acting, read these project-root-relative records in order:
1. `<state-path>` - authoritative current state; required on every resumption.
2. `<unresolved-path>` - material unresolved questions/observations; required while relevant items remain. Omit this entry if there is no such record.
3. `<reference-path>` - purpose; required for <named condition>, otherwise optional history. Include only references the project needs.

Resume the recorded objective and next action. Reconcile unfinished operations with actual state before repeating them. Update this index when paths or reading requirements change.
<!-- codex-state-index:end -->
```

Adapt the example; leave no placeholder or nonexistent path. If an unresolved section shares the state file, point to that section instead of inventing a separate file. Add the delimited section if absent; update existing entries instead of appending a new index every session. Preserve instructions outside it. Do not copy global policy into local files or create duplicate state indexes in descendants. Existing nested instructions retain their scope.

Keep the index focused on the project goal, authoritative state and ordered reading requirements. Mark each reference with its purpose and whether it is always required, conditional or optional history. The current record holds full status and next action; duplicating those in the index creates stale competing summaries. For many supporting records, use a focused secondary index. A new agent must reach required current context from the root alone, without the previous chat or a user-supplied file list.

## Authoritative current state

Create one concise maintained record if the project lacks an equivalent; current-state.md is a default. A useful summary includes the following as relevant, without empty headings or a mandatory schema:

| Information | What continuation needs |
| --- | --- |
| Goal and completion | Original/current objective, definition of done, explicit completion when reached |
| Contract | Explicit constraints, accepted clarifications, material decisions and concise rationale |
| Work | Completed and unfinished steps; distinguish changed from verified |
| Evidence | Checks and actual outcomes, limits, relevant artifact paths and versions/inputs |
| Operations | Pending action, identifier or inspection method, expected output, observed or unknown status |
| Uncertainty | Blockers, dependencies, unresolved items and source disagreements |
| Next action | First executable continuation step, or no active work |
| Freshness | Update date and the revision/files to which verification applies |

Use facts, inherited claims, hypotheses, experimental support and proof labels accurately. Keep raw logs, datasets, large outputs and useful failed cases separate, with links explaining their relevance. Preserve enough of a failed approach to avoid repeating it blindly. Keep secrets and unrelated private material out of records.

Save settled explanations and durable project knowledge in their suitable references. Keep a concise constraint or required-reading link when it still affects the next move. Reuse these records for small edits in an established project rather than creating a new worklog each time.

## Unresolved questions and observations

Create a record only when a material need arises. A concise entry can use this shape, adapted to existing conventions:

```markdown
## Q-1 - <specific unresolved decision>
- Type/status: question; pending user answer.
- Affected work and reason: <what depends on this and why it matters>.
- Evidence/uncertainty: <observed facts and remaining gap>.
- Proposed default and tradeoff: <when appropriate; not required approval>.
- User answer: <actual answer, or pending>.
```

Use an observation ID/type for design friction that needs tracking without an immediate answer. Record the observed difficulty, responsible design choice, plausible improvement and tradeoff. Keep actionable defects distinct from design observations. A recorded proposal is not authorization to implement it.

Before updating, reread the latest record and merge new responses. At meaningful reviews, check whether each item still affects the work, needs revalidation, or has been resolved by newer evidence. Store an accepted answer and its consequences in current state or the appropriate reference before removing the open entry. Preserve relevant unanswered items and unincorporated responses. Consolidate duplicates without losing their evidence or user decisions.

## Check the continuation path

After creating, moving or compacting records, inspect them as a cold-start reader:

1. From root AGENTS.md, do all required references resolve, with clear reading conditions?
2. Can the goal, accepted constraints, actual verification limits and next action be recovered without the previous conversation?
3. Are pending operations reconciled with available status/output, and relevant user answers incorporated without inventing decisions?
4. Do maintained state, unresolved items and any decision trail agree? Is useful evidence retained and historical detail clearly conditional?

Fix a demonstrated gap in the existing owner. A second summary, blanket retesting or a new storage engine does not by itself establish reliable continuation. Persistence provides recovery from the last durable checkpoint; it cannot guarantee an exact forced-termination snapshot.
