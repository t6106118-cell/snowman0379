# Mindmap runtime provisioning

Read this file only when installing, repairing, verifying, or upgrading the
optional Markmap HTML renderer. Ordinary Markdown generation needs no runtime.

## Provenance

Nova uses Node.js 24.18.0, npm/npx 11.16.0, and `markmap-cli` 0.18.12 from the
[`markmap/markmap`](https://github.com/markmap/markmap) monorepo. Release tag
`v0.18.12` resolves to commit
`205367a24603dc187f67da1658940c6cade20dce`. The npm package requires Node 18 or
newer and exposes the `markmap` executable.

No global `markmap` command is installed on nova. The package is held in npm's
per-user execution cache under `/home/nova/.npm/_npx/`; the observed package
manifest is
`/home/nova/.npm/_npx/f655081d0b3e1563/node_modules/markmap-cli/package.json`.
That cache key is npm-generated and must not be treated as a portable path.

## Provisioning

Use the target account's npm cache; do not install this development package
globally. Populate and verify the pinned package while network access is
available:

```bash
npm exec --yes --package=markmap-cli@0.18.12 -- markmap --version
```

The expected output is `0.18.12`. The skill renderer then runs:

```bash
bash /home/nova/.codex/skills/mindmap/scripts/render.sh input.md output.html
```

Internally, `render.sh` currently invokes:

```bash
npx --yes markmap-cli input.md -o output.html --no-open
```

The script's package request is not version-pinned. Deterministic provisioning
therefore depends on pre-populating and verifying 0.18.12 as above. If npm later
resolves another version, verify it before accepting the change or update the
script and this reference together.

## Offline behavior

Rendering is offline only after npm has cached the package and all transitive
dependencies. Verify that state explicitly:

```bash
npm_config_offline=true npm exec --yes --package=markmap-cli@0.18.12 -- markmap --version
npm_config_offline=true bash /home/nova/.codex/skills/mindmap/scripts/render.sh input.md output.html
```

On nova both commands succeed with 0.18.12. On a fresh host, an offline cache
miss fails; it cannot install Markmap without prior network provisioning. The
Markdown input remains usable even when HTML rendering fails.

## Verification and upgrades

Use a small Markdown file containing one H1, one H2, and a bullet. Render it,
confirm exit status zero and a non-empty standalone HTML output, then repeat
with `npm_config_offline=true` if offline operation is required.

For an upgrade, inspect the upstream release and npm package, choose an explicit
version, populate the cache with the pinned `npm exec` command, run online and
offline smoke tests, and only then update the documented version, commit, and
any pinned renderer command. Cache presence alone is not provenance.
