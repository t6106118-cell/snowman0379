# Runtime provisioning

This file documents the native runtime used by `pdf-inspector`. Keep document
routing and extraction procedure in `SKILL.md`; use this file for installation,
verification, rebuilds, and upgrades.

## Source and installed state

- Upstream: `https://github.com/firecrawl/pdf-inspector`
- Published crate: `https://crates.io/crates/pdf-inspector`
- Nova version: crates.io `pdf-inspector` 1.17.0, installed with its published
  lockfile and default features only.
- Build toolchain: Fedora rustc 1.97.1 (`1.97.1-1.fc44`), Cargo, and a C linker;
  target `x86_64-unknown-linux-gnu`.
- Root: `~/.local/opt/fedora44-tools/pdf-inspector/1.17.0/`.
- Binaries: `bin/pdf2md`, `bin/detect-pdf`, and `bin/dump_ops`.
- PATH: only `pdf2md` and `detect-pdf` are symlinked into `~/.local/bin`.

The binaries are dynamically linked Linux PIE executables. The install record
in `.crates2.json` records version 1.17.0, release profile, no explicit
features, and the compiler above. The optional upstream OCR feature, PDFium,
ONNX Runtime, and model files are not part of this baseline.

Nova's installed SHA-256 values are:

```text
pdf2md      d69db803a48c6e9684a2a7054a77f0b1eacadda1537525451b00c7cd1e3e83e4
detect-pdf  595765086254e8c50a10edf8b054c35ba50751c038f1b6a8cf7b6cb53ba2cf23
dump_ops    613581e93f90a948f6ff0656b7f4fcdfc810c3dfe8efe7b750ef7ceb6c6c3a52
```

## Install

Use a supported stable Fedora Rust toolchain. Install the exact crate into a
new versioned user-local root:

```bash
pdf_version=1.17.0
pdf_root="$HOME/.local/opt/fedora44-tools/pdf-inspector/$pdf_version"
cargo install --version "$pdf_version" --locked --root "$pdf_root" pdf-inspector
install -d "$HOME/.local/bin"
ln -s "$pdf_root/bin/pdf2md" "$HOME/.local/bin/pdf2md"
ln -s "$pdf_root/bin/detect-pdf" "$HOME/.local/bin/detect-pdf"
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

Do not probe `pdf2md` or `detect-pdf` with `--help` or `--version`; those tokens
are treated as PDF paths. Verify path identity and Cargo metadata, then use a
real small text-native PDF:

```bash
type -a pdf2md detect-pdf
readlink -f "$(command -v pdf2md)"
rg 'pdf-inspector 1.17.0' \
  "$HOME/.local/opt/fedora44-tools/pdf-inspector/1.17.0/.crates.toml"
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

## Upgrade or rebuild

Upstream releases can exceed nova's installed version. Before upgrading,
inspect the new crate's MSRV, feature defaults, published lockfile, CLI/schema
changes, and OCR behavior. Install into a new version root with `--locked` and
without optional OCR features; run text-native, scanned, mixed, page-selection,
JSON, items-JSON, and helper tests. Repoint the two public symlinks only after
validation and retain the prior root for rollback. Record the new crate,
compiler, target, features, hashes, paths, and observed schema in this file and
the workstation inventory.
