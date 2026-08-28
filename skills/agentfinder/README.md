# Agent Finder / ARD

Agentic Resource Discovery (ARD) lets Codex discover MCP servers, Skills,
agents, APIs, tools, and workflows when an existing capability or ordinary web
search is not enough. Discovery is on demand and never installs a result
automatically.

The executable Codex Skill is installed globally at
`~/.codex/skills/agentfinder/SKILL.md`. Mutable runtime finder selection and
entries live at `~/.agentfinder/finders.json`; this repository does not manage
or synchronize that file.

`finders.example.json` is the public/default example. The Skill creates the
runtime file if it is absent. Users may switch finders or add their own entries,
but the repository example must not overwrite an existing user configuration.

Before installing a selected resource, inspect it and obtain explicit
authorization. ARD discovery alone does not install, enable, connect, download,
or execute discovered resources.
