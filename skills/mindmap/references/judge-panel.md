# Judge Panel — Codex collaboration prompts

This file is loaded only when `/mindmap` is invoked with `--panel`. It defines the
multi-agent panel that designs the mindmap structure and per-node format. The
prompts below define the tasks; interpolate the source content without changing
the hard constraints.

## Shared context block

Prepend this to every proposer and to the synthesizer:

```
SOURCE CONTENT:
<full resolved input content>

SKILL RULES (hard constraints):
- Exactly one H1 (the central topic).
- 4–7 main branches (## H2).
- Depth 3–4 levels total.
- Every node is a short phrase (<= ~8 words), never a sentence.
- Condense aggressively; legibility over completeness.
- When the source is already structured, mirror its outline.

PER-NODE FORMAT — assign each node a format and a render tier:
- bullet list  (core)  — parallel facts
- table        (rich)  — comparisons / benchmark numbers
- code block   (rich)  — formulas, reward functions, code
- checkbox     (rich)  — tasks, limitations, checklist items
- link         (core)  — references, repo, arXiv
- bold inline  (core)  — emphasis / headline metric
"core" renders on every path; "rich" renders only in standard markmap.
```

## Proposer prompts (×3 — one lens each)

Each proposer receives the shared block plus ONE lens directive, then the common closer.

- **Proposer A — Narrative-first:** "Design the mindmap by mirroring the source's
  own arc and outline. Follow the document's natural order; each main branch
  should correspond to a major section of the source. Preserve the author's
  logical flow."
- **Proposer B — Data-first:** "Design the mindmap organized around the headline
  numbers and evidence. Lead with the strongest quantitative results; group nodes
  so the key figures and the claims they support are front and center. Bold every
  headline metric."
- **Proposer C — Audience-first:** "Design the mindmap to be SHOWN to an audience
  on a projector. Put the punchline first — the single most important takeaway is
  branch 1. Optimize every leaf node for at-a-glance legibility; ruthlessly cut
  anything that wouldn't read clearly on a slide."

Common closer (all three): "Return a complete structure: the H1, 4–7 branches,
nested nodes 3–4 deep, and for each node its text, format, and render tier. Do
not write the final markdown — return structured data only."

## Judge prompt (×3 — identical, run independently)

"You are scoring 3 candidate mindmap structures for the same source. Score EACH
proposal 1–5 on every dimension below. Be a strict, independent critic; do not
assume the proposals are good.

Dimensions: branch count (4–7), depth (3–4 levels), phrasing (phrases not
sentences), legibility (condensed), source fidelity (mirrors a structured
source), punchline-first (payoff surfaced early), headline numbers (big figures
bolded), leaf legibility (readable when projected), visual balance (branches
roughly even), format fit (right format per node).

For each proposal also name the SINGLE best idea it contributes — a branch,
framing, or node the winner should steal. Return scores + best-idea per proposal
as structured data. Default to lower scores when uncertain."

## Synthesizer prompt (×1)

"You are given 3 candidate mindmap structures and 3 judges' scorecards. Take the
proposal with the highest aggregate score as the SPINE. Then graft in the
specific best ideas the judges flagged from the other two proposals, wherever
they strengthen the spine without breaking the 4–7 branch / 3–4 depth limits.
Resolve format conflicts using the per-node format table.

Emit the FINAL Markmap `.md`: frontmatter (colorFreezeLevel: 2, maxWidth: 300),
one H1, the chosen branches and nodes, with each node in its selected format. For
any node tagged 'rich', this is the standard-path output — keep the rich format.
Return the complete markdown."

## Expected result shapes

- **Proposer** → `{ title, branches: [{ heading, nodes: [{ text, format, tier, children: [...] }] }] }`
  where `format` ∈ `list|table|code|checkbox|link|bold`, `tier` ∈ `core|rich`.
- **Judge** → `{ scores: [{ proposalId, dimensions: { branchCount, depth, phrasing, legibility, sourceFidelity, punchlineFirst, headlineNumbers, leafLegibility, visualBalance, formatFit }, total }], bestIdeas: [{ proposalId, idea }] }`
- **Final synthesis** → the main agent returns the final Markmap `.md` as text.

## Codex collaboration sequence

1. Call `spawn_agent` three times for independent proposer tasks. Use distinct
   task names and include the shared context, one lens directive, and common
   closer in each message.
2. Call `wait_agent` until all proposer agents finish. Keep every successful
   proposal; record failures instead of inventing their output.
3. Call `spawn_agent` three times for independent judge tasks. Give each judge
   the complete successful proposal set plus the judge prompt.
4. Call `wait_agent` until all judges finish. Keep every successful scorecard.
5. In the main agent, apply the synthesizer prompt to the collected proposals
   and scorecards, validate the Markmap constraints, and continue with Step 3
   in `SKILL.md`.

Codex collaboration calls do not enforce the JSON shapes automatically. Ask for
JSON-shaped text, reject malformed results, and synthesize from the remaining
valid results. If all proposers fail, use the single-pass fallback documented in
`SKILL.md`.
