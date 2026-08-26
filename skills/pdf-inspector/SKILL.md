---
name: pdf-inspector
description: Use when Codex needs to convert a local PDF to Markdown, read or inspect PDF content, classify text-based, mixed, or scanned documents, extract selected pages or positioned-text JSON, inspect tables, columns, and encoding, determine whether OCR is needed, or debug pdf-inspector extraction. Do not use for creating, merging, rotating, or editing PDFs.
---

# PDF Inspector

Use the installed Firecrawl `pdf-inspector` CLI for local PDF classification and
native-text extraction. Treat conversion as extraction with validation: a
successful command is not proof that reading order, tables, or encoding are
correct.

The installed build exposes `pdf2md` and `detect-pdf` through
`/home/nova/.local/bin`. It has the default features only and does not perform
OCR.

```text
PDF
├── native/extractable ── detect-pdf ── pdf2md ── mechanical checks ── Markdown + review
└── scanned/image-only ── OCR needed ── workflow decision ── OCRmyPDF/Tesseract
```

## Decision flow

1. Preserve the source PDF. Never overwrite it. For a remote PDF, download it
   once to a scoped temporary path and verify that the bytes are a PDF before
   comparing or converting it.
2. Classify before converting:

   ```bash
   detect-pdf "$input" --json > detect.json
   jq '{pdf_type, page_count, pages_sampled, pages_with_text, confidence,
        ocr_recommended, pages_needing_ocr, ocr_reasons_by_page}' detect.json
   ```

   The fast JSON contract includes the fields above (some may be absent for a
   particular document). `text_based` permits native extraction; `scanned` or
   `image_based` requires an OCR decision; `mixed` may contain usable text plus
   pages that need OCR. Classification is routing evidence, not a completeness
   guarantee.
3. Run layout analysis only when it can change the decision:

   ```bash
   detect-pdf "$input" --analyze --json > analysis.json
   jq '{pdf_type, page_count, pages_needing_ocr, ocr_reasons_by_page,
        is_complex, pages_with_tables, pages_with_columns}' analysis.json
   ```

   This is the dedicated analysis command. Its observed schema uses `is_complex`,
   not `is_complex_layout`, and does not promise `has_encoding_issues`. The
   `has_encoding_issues` field is available in `pdf2md --json` extraction metadata
   when emitted by that command.
4. Convert only when the result is appropriate for the task. For a mechanically
   validated Markdown artifact, use the bundled helper:

   ```bash
   /home/nova/.codex/skills/pdf-inspector/scripts/convert_pdf_to_markdown.sh \
     "$input" "$output_md"
   ```

   It classifies first, refuses scanned/image-only input and mixed input with
   OCR-needed pages, writes beside the destination, requires successful nonempty
   raw Markdown, and atomically moves the result. These are mechanical checks;
   they do not establish reading order, table structure, or encoding quality. It
   does not install software or run OCR. For a pipeline or a selected-page probe,
   use raw stdout directly and perform the same checks:

   ```bash
   tmp_md=$(mktemp)
   if pdf2md "$input" --raw --select-pages 1 >"$tmp_md"; then
     test -s "$tmp_md"
   else
     status=$?
     rm -f -- "$tmp_md"
     exit "$status"
   fi
   ```

   The page selector is one-based and accepts values such as `1`, `1,3`, or
   `5-10`. Useful opt-in modes are:

   ```bash
   pdf2md "$input" --raw > output.md                 # Markdown to stdout
   pdf2md "$input" --raw --compact > compact.md      # compact Markdown
   pdf2md "$input" --raw --pages > pages.md          # page markers
   pdf2md "$input" --json > result.json              # metadata plus Markdown
   pdf2md "$input" --items-json > items.json         # positioned text items
   ```

   The default-mode positional form `pdf2md input.pdf output.md` is supported,
   but `--raw` always writes Markdown to stdout and ignores a positional output
   path. Prefer the helper for final artifacts so failure cannot leave a
   plausible empty/truncated destination.

## OCR boundary and failure semantics

`pdf2md "$input" --raw` exits 2 and emits no Markdown when the input is scanned
or image-only. Conversely, `pdf2md "$input" --json` can exit 0 while reporting
`has_text: false` and `markdown_length: 0`. Never accept an empty Markdown file
as a successful conversion, regardless of exit status.

If OCR is authorized, preserve the original and create a separate searchable
PDF with the existing OCRmyPDF/Tesseract/Poppler/Ghostscript workflow. Re-run
`detect-pdf` and then `pdf2md` on that copy. Do not imply that `pdf-inspector`
automatically routes to OCR, do not OCR in place, and do not add PDFium, ONNX
Runtime, model files, or the optional Firecrawl OCR feature for this baseline.
For mixed PDFs, use the reported pages and OCR reasons plus the task's required
coverage before deciding whether to OCR selected pages or the whole copy. The
bundled final-artifact helper exits 2 without publishing when `mixed` includes
`pages_needing_ocr`; use direct `pdf2md --raw` only for an intentionally partial
inspection, and label that output as partial rather than validated.

## Acceptance and escalation

For every delivered artifact, check the result rather than only the exit code:

```bash
test -s output.md
rg -n -m 40 '^#{1,6} |^\|' output.md || true
rg -n -m 20 'expected title or section' output.md || true
```

Record the classification, selected pages, command/options, output path, and
validation performed. For complex, multi-column, table-heavy, legal, financial,
or scientific PDFs, compare bounded sections with the installed Poppler
extractor before escalating:

```bash
pdftotext -layout "$input" - | sed -n '1,160p'
```

Use `--items-json` when coordinates or font evidence matter. If low-level parser
evidence is needed, resolve the unpromoted sibling binary from the currently
selected installation instead of assuming `dump_ops` is on `PATH`:

```bash
pdf2md_real=$(readlink -f "$(command -v pdf2md)")
dump_ops="$(dirname "$pdf2md_real")/dump_ops"
test -x "$dump_ops"
"$dump_ops" "$input" 1
```

The current host does not provide `markitdown`; do not assume or install it just
for comparison. If a future host has it, probe with `command -v markitdown` and
use it only as a bounded secondary comparator. Do not feed two full-document
conversions into model context. Report interleaved columns, false tables,
garbled text, missing pages, or other structural uncertainty instead of silently
repairing it.

This CLI does not implement conventional `--help` or `--version`: those tokens
are treated as PDF paths. Invoking either command with no arguments prints usage
and exits nonzero; do not use `--help` as an installation health check.

If the user's objective is authoritative research or citation rather than PDF
conversion, a publisher's equivalent structured HTML/XML can be preferable. An
explicit request to convert or inspect the supplied PDF remains a local PDF
workflow.

## Handoff

State the source, classification, pages needing review/OCR, chosen command and
options, output path, validation evidence, and known reading-order or structure
limits. Distinguish extracted text from verified document meaning.
