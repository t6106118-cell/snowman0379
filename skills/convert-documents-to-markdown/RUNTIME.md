# Runtime provisioning

This file documents the AnyDoc runtime used by
`convert-documents-to-markdown`. Keep conversion procedure in `SKILL.md`; use
this file for installation, verification, and upgrades.

## Source and installed state

- Upstream: `https://github.com/firecrawl/anydoc`
- Nova release: tag `v0.2.4`, commit
  `42bf1c5ecdde9eb0d96d6bd75a9e6698cf93b14c`, verified 2026-10-10.
- CLI package: `@firecrawl/anydoc@0.2.4` from npm.
- Native package: `@firecrawl/anydoc-linux-x64-gnu@0.2.4`.
- Runtime: Node 20 or newer; nova uses Fedora Node 24.18.0 and npm 11.16.0.
- Root: `~/.local/opt/fedora44-tools/anydoc/0.2.4/`.
- PATH: `~/.local/bin/anydoc` points to the root's `bin/anydoc`, which resolves
  to `node_modules/@firecrawl/anydoc/cli.js`.

The CLI is JavaScript loading a platform-specific N-API native addon. Nova's
`anydoc.linux-x64-gnu.node` SHA-256 is
`1c7927a844f33adac68279e8116585002fd125195f10330f9024e62f2c90b643`,
matching the published Linux x64 GNU release asset digest;
the installed `cli.js` SHA-256 is
`cc50a40f8710fc365230fb56625340f012b9ddd02315078e2947199f70652bd5`.
The native addon is glibc-linked. Select a platform package matching the host
OS, architecture, and libc rather than copying nova's addon blindly.

## Install

Use a supported Node release and a versioned user-local npm prefix. Pin both
packages explicitly so npm cannot select a different platform package:

```bash
anydoc_version=0.2.4
anydoc_root="$HOME/.local/opt/fedora44-tools/anydoc/$anydoc_version"
install -d "$anydoc_root" "$HOME/.local/bin"
npm install --prefix "$anydoc_root" --save-exact --omit=dev --omit=optional \
  --ignore-scripts --no-audit --no-fund \
  "@firecrawl/anydoc@$anydoc_version" \
  "@firecrawl/anydoc-linux-x64-gnu@$anydoc_version"
install -d "$anydoc_root/bin"
ln -s ../node_modules/@firecrawl/anydoc/cli.js "$anydoc_root/bin/anydoc"
"$anydoc_root/bin/anydoc" --version
```

Adapt the versioned-root name to the host convention and platform package to
the actual target. Inspect existing paths first. Do not use global npm or
write into `/usr/local`; do not mutate system Python. Retain the generated
`package.json` and `package-lock.json`. `--ignore-scripts` is intentional because
the exact prebuilt native package is installed explicitly; `--omit=optional`
avoids installing other platform variants. The matching native package is a
direct dependency, so it remains installed. Verify the candidate before
exposing or replacing the public command.

AnyDoc does not call PATH `pdf2md`; release 0.2.4's tagged Cargo.lock resolves
its Rust PDF dependency to `pdf-inspector` 1.14.2. The separately provisioned pdf-inspector
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

Expect `anydoc --version` to report 0.2.4 and the CLI to work from a directory
outside the installation root. Test representative DOCX, XLSX, PPTX, CSV
stdin, and one failure case. Confirm output contains expected headings, cells,
or slide text rather than accepting exit 0 alone. Include text, scanned, and
mixed PDF fixtures: text converts locally; scanned and mixed documents needing
OCR exit 3 without incomplete Markdown. Usage errors exit 2, and unreadable or
invalid inputs exit 1. AnyDoc does not perform local OCR. Its optional
`--ocr hosted` route uploads the whole PDF to Firecrawl Parse; keep it disabled
for local verification and follow the dedicated PDF skill for local OCR.

## Upgrade or rebuild

Upstream may publish a newer release than nova's installed version. Verify the
GitHub tag, npm package versions, Node engine requirement, supported platform
addon, and published addon digest. Install both packages into a new versioned
root, retain its lockfile, and run the format matrix using that root's command.
After the candidate passes, expose it with:

```bash
ln -sfnT "$anydoc_root/bin/anydoc" "$HOME/.local/bin/anydoc"
anydoc --version
```

Verify the public command from an unrelated directory, then delete superseded
installation roots. Do not create backup or rollback copies or keep obsolete
binaries. Preserve user data and local customizations directly. Update
`SKILL.md` when the CLI contract or supported formats change; update this file
and the inventory with accepted versions, commit, platform package, Node/npm
versions, paths, and hashes.
