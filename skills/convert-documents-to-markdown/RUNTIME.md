# Runtime provisioning

This file documents the AnyDoc runtime used by
`convert-documents-to-markdown`. Keep conversion procedure in `SKILL.md`; use
this file for installation, verification, and upgrades.

## Source and installed state

- Upstream: `https://github.com/firecrawl/anydoc`
- Nova release: tag `v0.2.3`, commit
  `bf3d33e61731580d1ee1c6a85e56093d715a21a6`.
- CLI package: `@firecrawl/anydoc@0.2.3` from npm.
- Native package: `@firecrawl/anydoc-linux-x64-gnu@0.2.3`.
- Runtime: Node 20 or newer; nova uses Fedora Node 24.18.0 and npm 11.16.0.
- Root: `~/.local/opt/fedora44-tools/anydoc/0.2.3/`.
- PATH: `~/.local/bin/anydoc` points to the root's `bin/anydoc`, which resolves
  to `lib/node_modules/@firecrawl/anydoc/cli.js`.

The CLI is JavaScript loading a platform-specific N-API native addon. Nova's
`anydoc.linux-x64-gnu.node` SHA-256 is
`30861432d55acfcf53e6f896f16e49a7e8017026a227bb35b9203566dd1fb17c`;
the installed `cli.js` SHA-256 is
`07d8a69e3c1594e51b86478abe9bc470ed51a6e5938492fd5dc3fdb96b81da50`.
The native addon is glibc-linked. Select a platform package matching the host
OS, architecture, and libc rather than copying nova's addon blindly.

## Install

Use a supported Node release and a versioned user-local npm prefix. Pin both
packages explicitly so npm cannot select a different platform package:

```bash
anydoc_version=0.2.3
anydoc_root="$HOME/.local/opt/fedora44-tools/anydoc/$anydoc_version"
install -d "$anydoc_root" "$HOME/.local/bin"
npm install --prefix "$anydoc_root" --omit=dev --ignore-scripts \
  "@firecrawl/anydoc@$anydoc_version" \
  "@firecrawl/anydoc-linux-x64-gnu@$anydoc_version"
ln -s "$anydoc_root/bin/anydoc" "$HOME/.local/bin/anydoc"
```

Adapt the versioned-root name to the host convention and platform package to
the actual target. Inspect existing paths first. Do not use global npm or
write into `/usr/local`; do not mutate system Python. Retain the generated npm
lockfile when available. `--ignore-scripts` is intentional because the exact
prebuilt native package is installed explicitly.

AnyDoc does not call PATH `pdf2md`; release 0.2.3 embeds its own Rust PDF
dependency (`pdf-inspector` 1.14.2). The separately provisioned pdf-inspector
CLI remains the route for serious PDF classification, layout analysis, mixed
or scanned documents, and OCR decisions.

## Expected commands and verification

```bash
type -a node npm anydoc
node --version
anydoc --version
anydoc input.docx -o output.md
test -s output.md
printf 'name,value\na,1\n' | anydoc - --format csv
```

Expect `anydoc --version` to report 0.2.3 and the CLI to work from a directory
outside the installation root. Test representative DOCX, XLSX, PPTX, CSV
stdin, and one failure case. Confirm output contains expected headings, cells,
or slide text rather than accepting exit 0 alone. A scanned PDF should not be
treated as successfully OCRed; AnyDoc has no OCR or external service runtime.

## Upgrade or rebuild

Upstream may publish a newer release than nova's installed version. Verify the
GitHub tag, npm package versions, Node engine requirement, supported platform
addon, and published addon digest. Install both packages into a new versioned
root, retain its lockfile, run the format matrix, then repoint the public link.
Keep the prior root for rollback. Update `SKILL.md` only if the CLI contract or
supported formats change; update this file and the inventory with accepted
versions, commit, platform package, Node/npm versions, paths, and hashes.
