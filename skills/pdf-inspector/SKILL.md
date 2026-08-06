---
name: pdf-inspector
description: Fast local PDF classification, layout analysis, text extraction, and structured Markdown conversion with the installed PDF Inspector CLI. Use when Codex needs to convert a native-text PDF to Markdown, identify scanned or mixed pages that require OCR, inspect tables or multi-column layout, extract selected pages, obtain positioned text JSON, compare PDF extraction quality, or debug PDF content operators. Prefer publisher HTML/XML for authoritative research text and use OCR before conversion for image-only PDFs.
---

# PDF Inspector

Use the installed `pdf2md`, `detect-pdf`, and `dump_ops` commands. Treat PDF
conversion as extraction with validation, not as proof that reading order or
structure is correct.

## Core workflow

### 1. Preserve source identity

Download a remote PDF once to a scoped temporary path, then run every comparison
against the same bytes. Record the final URL and checksum when provenance matters.
Reject an HTML challenge page or error response before conversion.

For cited research, prefer built-in web research over converted PDF text. Prefer a
publisher's structured HTML or XML when it represents the same article; use the PDF
when page-specific content is required.

### 2. Classify before converting

Request bounded JSON suitable for agent decisions:

```bash
pdf2md input.pdf --analyze --json > analysis.json
jq '{pdf_type, page_count, pages_needing_ocr, ocr_reasons_by_page,
     is_complex, pages_with_tables, pages_with_columns,
     has_encoding_issues}' analysis.json
```

Use `detect-pdf input.pdf --json` instead when only fast scanned-versus-text routing
is needed and layout or encoding evidence cannot affect the decision.

Interpret the result as follows:

| Result | Action |
|---|---|
| `text_based`, simple | Convert directly. |
| `text_based`, complex | Convert, then inspect reading order, headings, and tables. |
| `mixed` | Treat the Markdown as partial; identify and OCR the missing pages when the task requires complete text. |
| `scanned` or `image_based` | Stop direct conversion and run an authorized OCR workflow first. |
| `has_encoding_issues: true` | Treat extracted text as suspect and compare with another extractor or OCR. |

CLI page lists and `--select-pages` use one-based page numbers.

Treat OCR and layout classifications as routing hints, not ground truth. Sparse pages,
vertical text, charts, and publication furniture can cause false OCR, table, or column
signals.

### 3. Convert atomically

Use raw mode for a Markdown artifact because it emits only Markdown to stdout:

```bash
pdf2md input.pdf --raw > output.md
```

Do not accept an empty file merely because shell redirection created it. Convert to a
temporary sibling, require exit status zero and nonempty content, then move it to the
requested output path. `pdf2md --raw` exits with status 2 for a scanned or image-based
PDF.

Use optional modes only when they answer the task:

```bash
# Token-efficient cleanup
pdf2md input.pdf --raw --compact > output.md

# Preserve page boundaries
pdf2md input.pdf --raw --pages > output.md

# Extract selected pages
pdf2md input.pdf --raw --select-pages 1,3,5-10 > output.md

# Return metadata and Markdown together
pdf2md input.pdf --json > result.json

# Write Markdown through the CLI's output-file argument
pdf2md input.pdf output.md
```

Use `--password PW` only with authorization. It exposes the value in process
arguments, so do not log or surface the command and do not store the password in the
skill or output artifact.

### 4. Validate the artifact

Check the final file directly:

```bash
test -s output.md
rg -n -m 40 '^#{1,6} |^\|' output.md
rg -n -m 20 'expected title or section' output.md
```

For complex, multi-column, table-heavy, legal, financial, or scientific PDFs:

1. Compare a bounded selection with `pdftotext -layout` or MarkItDown.
1. Inspect the title, first body transition, representative section boundaries,
   tables, captions, references, and final page.
1. Render and inspect only the decisive source pages when text comparison cannot
   establish reading order.
1. Report structural errors instead of silently cleaning content into a misleading
   result.

Prefer PDF Inspector for fast native-text PDF conversion. Use MarkItDown as a
fallback when PDF Inspector splits titles, invents tables, or loses text. Do not feed
both complete outputs into model context; compare bounded sections and mechanical
summaries first.

## OCR routing

PDF Inspector performs no OCR. When complete conversion of a scanned or mixed PDF is
authorized, preserve the original and create a separate searchable copy with the
installed OCRmyPDF/Tesseract pipeline. Re-run `detect-pdf` and convert the searchable
copy. Verify critical names, numbers, equations, and tables because OCR can introduce
confident recognition errors.

Do not OCR merely because one sparse page appears in `pages_needing_ocr`; inspect the
reason and whether that page contains required visible text.

## Diagnostic extraction

Use positioned items when layout coordinates or font evidence can decide a question:

```bash
pdf2md input.pdf --items-json > items.json
pdf2md input.pdf --items-json --select-pages 2-3 > items.json
jq '{total_items, underlined_count, items: .items[:20]}' items.json
```

Use `dump_ops input.pdf [page] [search]` only for low-level parser debugging. Its
unfiltered output can be large; specify one page and a search term when possible,
capture complete output outside model context, and surface only the relevant PDF
operators and errors.

This CLI build does not implement conventional `--help` or `--version` flags; those
tokens are interpreted as PDF paths. Invoke a command with no arguments for its usage
text. Check Cargo installation metadata only when the exact installed version matters.

## Known failure patterns

- Multi-column prose may be interleaved even when column detection succeeds.
- Charts, figure panels, author lists, and aligned page furniture may become false
  Markdown tables.
- A title can be split between a heading and a detached fragment.
- Headers, footers, DOI strings, download notices, and vertical text may remain or be
  reversed.
- Successful extraction and high token overlap do not establish correct reading order.
- Scanned and image-only PDFs require a separate OCR step.

## Handoff

Report the source file or URL, checksum when relevant, selected command and options,
PDF classification, pages requiring review or OCR, output path, validation performed,
and any known reading-order or structure defects. Distinguish tool output from verified
document meaning.
