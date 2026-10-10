# Runtime provisioning

This file documents the native runtime used by `pdf-inspector`. Keep document
routing and extraction procedure in `SKILL.md`; use this file for installation,
verification, rebuilds, and upgrades.

## Source and installed state

- Upstream: `https://github.com/firecrawl/pdf-inspector`
- Published crate: `https://crates.io/crates/pdf-inspector`
- Nova version: crates.io `pdf-inspector` 1.25.2, installed with its published
  lockfile and default features only.
- Source: tag `v1.25.2`, commit `ef52f77850b29189048797a48b24862251f54fe7`;
  the published crate's `.cargo_vcs_info.json` matches that commit.
- Minimum Rust: 1.88. Build toolchain: Fedora rustc/Cargo 1.98.1
  (`1.98.1-1.fc44`) and a C linker;
  target `x86_64-unknown-linux-gnu`.
- Root: `~/.local/opt/fedora44-tools/pdf-inspector/1.25.2/`.
- Binaries: `bin/pdf2md`, `bin/detect-pdf`, and `bin/dump_ops`.
- PATH: only `pdf2md` and `detect-pdf` are symlinked into `~/.local/bin`.

The binaries are dynamically linked Linux PIE executables. The install record
in `.crates2.json` records version 1.25.2, release profile, no explicit
features, and the compiler above. The optional upstream OCR feature, PDFium,
ONNX Runtime, and model files are not part of this baseline.

Nova's installed SHA-256 values are:

```text
pdf2md      e1d97cba129aaec1bb902d69ec45d5455a16c54752eb027d80578c472b3a4dad
detect-pdf  efb4367bee533bea40f564a06deb0586a69554b3493a8a0beed0bc01b0464e09
dump_ops    78a48e0704aca6da88fef77f224a834aacd44018c8d6e467b1a41f70a542b706
```

## Install

Use a supported stable Fedora Rust toolchain. Install the exact crate into a
new versioned user-local root:

```bash
pdf_version=1.25.2
pdf_root="$HOME/.local/opt/fedora44-tools/pdf-inspector/$pdf_version"
cargo install --version "=$pdf_version" --locked --root "$pdf_root" pdf-inspector
```

Run the verification below with that root's `bin/` directory prepended to
PATH for the verification process before promoting the commands. Otherwise
the public links would still test the previous version. Then promote:

```bash
install -d "$HOME/.local/bin"
ln -sfn "$pdf_root/bin/pdf2md" "$HOME/.local/bin/pdf2md"
ln -sfn "$pdf_root/bin/detect-pdf" "$HOME/.local/bin/detect-pdf"
```

Adapt `fedora44-tools` to the host convention. Inspect existing roots and links
before changing them. Do not expose `dump_ops` globally; the skill resolves it
beside the active `pdf2md` only for low-level inspection. Ensure
`~/.local/bin` is already on PATH rather than changing shell profiles blindly.

The helper script also requires Bash, `jq`, and ordinary core utilities. The
optional comparison/OCR route uses separately managed Poppler (`pdftotext`),
OCRmyPDF, Tesseract, and Ghostscript; these are not dependencies of native
text extraction and must not be installed automatically by this skill.

## Expected commands and verification

Both CLIs recognize `--help` and `-h`, print usage to stderr, and exit 1.
Neither implements a version-reporting flag; `--version` alone also prints
usage and exits 1. Verify path identity and Cargo metadata, then use a real
small text-native PDF:

```bash
type -a pdf2md detect-pdf
readlink -f "$(command -v pdf2md)"
rg 'pdf-inspector 1.25.2' \
  "$HOME/.local/opt/fedora44-tools/pdf-inspector/1.25.2/.crates.toml"
detect-pdf sample.pdf --json > detect.json
jq '{pdf_type,page_count,pages_with_text,ocr_recommended}' detect.json
pdf2md sample.pdf --raw > sample.md
test -s sample.md
```

Expect a text-native fixture to classify as `text_based` and produce nonempty
Markdown. Also test a scanned fixture: classification must recommend OCR, and
`pdf2md --raw` must not publish plausible empty Markdown. Run the bundled
`scripts/convert_pdf_to_markdown.sh` once to verify its atomic output and
failure behavior.

Verified on 2026-10-10: text-native, scanned, mixed, page selection, JSON,
positioned items, CLI argument handling, and helper success/refusal checks.
Analysis and extraction JSON include `cmap_gaps`; positioned items include
rotation, weight, colors, and rendering mode. The helper rejects directory
destinations and uses GNU `mv -T` for exact file replacement. These checks do
not establish extraction quality for arbitrary real-world PDFs.

Only the active installation is kept. Do not create backup or rollback copies;
delete superseded installation roots after verifying the replacement.

## Upgrade or rebuild

Upstream releases can exceed nova's installed version. Before upgrading,
inspect the new crate's MSRV, feature defaults, published lockfile, CLI/schema
changes, and OCR behavior. Install into a new version root with `--locked` and
without optional OCR features; run text-native, scanned, mixed, page-selection,
JSON, items-JSON, and helper tests. Repoint the two public symlinks only after
validation, then delete the superseded root. Preserve local customizations
directly without backup copies. Record the new crate,
compiler, target, features, hashes, paths, and observed schema in this file and
the workstation inventory.
