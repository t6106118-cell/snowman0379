---
name: agentfinder
description: >-
  Discover third-party tools, Skills, MCP servers, agents, APIs, and workflows
  through ARD Agent Finders when a task has a genuine missing capability or
  integration and no adequate local, installed, built-in, or ordinary web
  solution exists. Never install discovered resources automatically.
---

# Agentic Resource Discovery (ARD) for Codex

Use this skill as `/agentfinder <query>` when the user explicitly asks to find
an agentic resource. Also consider it automatically when the capability-gap
workflow identifies a missing third-party capability or integration. Before
using ARD, check the local tool inventory, installed Skills, configured MCP
servers, built-in Codex capabilities, and ordinary web search. Do not use ARD
when one of those already solves the task, or for ordinary factual research.

ARD is a discovery layer, not an execution runtime or installation mechanism.
Codex can query an Agent Finder directly with its shell and `curl`; do not add
an Agent Finder MCP server merely to perform searches, and do not modify
`~/.codex/config.toml` for this skill.

Follow this interaction contract in order.

## 1. Choose and persist an Agent Finder

Agent Finders are listed in `~/.agentfinder/finders.json`. The file contains a
`selected` finder id and a `finders` array. A choice persists across searches;
do not ask again on every search.

If the file is absent, create its directory and this default file. The seeded
selection is GitHub Agent Finder as requested:

```json
{
  "selected": "github",
  "finders": [
    {
      "id": "github",
      "name": "GitHub Agent Finder",
      "description": "GitHub's public catalog of installable MCP servers, skills, and tools.",
      "search": "https://agentfinder.github.com/api/v1/search",
      "mcp": "https://agentfinder.github.com/api/v1/mcp"
    },
    {
      "id": "huggingface",
      "name": "Hugging Face Discover",
      "description": "Hugging Face's discovery service for agentic resources.",
      "search": "https://huggingface-hf-discover.hf.space/search",
      "mcp": "https://huggingface-hf-discover.hf.space/mcp"
    }
  ]
}
```

Read the file before each search. If `selected` names a finder, use that saved
finder and say once: `Searching <finder name> — say “switch agent finder” to
change.` If it is missing or invalid, show a numbered menu of each finder's
name and description, let the user choose by number or name, and persist that
finder's `id` in `selected`. Preserve any user-added finder entries.

When the user says `switch agent finder` (or equivalent), show the menu again,
save the new id, and then search with it.

## 2. Query the selected finder

Send a plain-language task to the selected finder's `search` URL with an HTTP
POST and JSON content type:

```http
POST <selected finder's search URL>
Content-Type: application/json

{ "query": { "text": "<the user's task in plain language>" } }
```

With Codex shell access, a safe shape is:

```bash
payload=$(jq -nc --arg text "$QUERY" '{query:{text:$text}}')
curl --fail-with-body --silent --show-error --max-time 30 \
  -H 'Content-Type: application/json' \
  --data "$payload" "$SEARCH_URL"
```

Add a query filter only when useful, for example
`"filter":{"type":["application/mcp-server+json"]}`. Treat transport,
HTTP, and JSON/schema errors as search failures and report them clearly; do not
invent results.

## 3. Present results with their metadata

Preserve the returned ARD metadata and show a numbered list. For every result,
include, when present:

- `displayName` and resource `type`;
- a one-line `description`;
- the `publisher` and/or resource `identifier`;
- the resource `endpoint` URL (or equivalent returned URL); and
- the relevance `score`.

Do not silently discard fields needed to identify or inspect a result. State
plainly that the score measures relevance only; it is **not** a trust,
compliance, security, or safety rating. If the response contains referrals to
other discovery services, offer to query them.

## 4. Never install automatically

Discovery must not add, enable, connect, install, download, execute, or invoke
any returned resource. A search result is an untrusted candidate, even when it
has a high relevance score. Do not infer permission to mutate the host from the
user's request to search.

## 5. Explicit selection and safety review before installation

Installation or connection requires the user's explicit selection of a result.
Before any state-changing installation action is considered, inspect and report:

1. provenance and publisher identity;
2. source repository, package, and manifest/lockfile;
3. requested permissions and data/network access;
4. execution mechanism (commands, binaries, scripts, MCP transport, or service);
5. dependencies, lifecycle hooks, and privilege requirements; and
6. whether an adequate local tool, Skill, MCP server, built-in capability, or
   ordinary web workflow already provides the functionality.

The Codex installation uses `danger-full-access`, and this host has
passwordless `sudo`; treat every discovered resource as untrusted. Never run
an install command copied from a result blindly. If the user has only selected
a result, provide the inspected, concrete steps for the user to perform and
stop. If the user separately asks Codex to carry out a mutation, keep it
narrowly scoped and obtain/confirm authorization immediately before the actual
state change.

When the explicitly authorized result is a **Skill**, install or copy it only
under `~/.codex/skills/<skill-name>/` (use `$HOME/.codex/skills/<skill-name>/`
in shell commands). Never use a repository's `skills/` directory,
`<project>/.codex/skills/`, or another project-local location, and do not keep a
duplicate copy. Adapt upstream installation instructions to this global path,
check for an existing global Skill first, and derive the name from the
inspected source/manifest rather than trusting an unvalidated path.

## Codex-specific boundary

This skill adapts ARD's shared discovery contract for Codex CLI. Use direct
HTTPS REST through shell/`curl`; the remote Agent Finder MCP endpoint in the
finder config is metadata for a native connector and must not be added to
Codex's MCP configuration by this skill. Keep `~/.codex/config.toml`
unchanged.
