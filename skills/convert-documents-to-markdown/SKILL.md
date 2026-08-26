---
name: convert-documents-to-markdown
description: Use the installed AnyDoc CLI to convert Word (.doc, .docx), PowerPoint (.ppt, .pptx), Excel (.xls, .xlsx), OpenDocument (.odt, .ods, .odp), RTF, EPUB, CSV, and text-native PDF files to GitHub-Flavored Markdown for broad office/document conversion. For PDF-specific inspection, layout analysis, scanned or mixed PDFs, or OCR routing, prefer the dedicated pdf-inspector skill.
license: MIT
metadata:
  author: firecrawl
---

# Convert documents to Markdown

Run the installed `anydoc` CLI. It needs Node 20+:

```bash
anydoc <file>              # Markdown to stdout
anydoc <file> -o out.md    # write to a file
anydoc - --format csv < f  # read stdin
```

Rules:

1. Supported inputs: `.doc`, `.docx`, `.docm`, `.odt`, `.rtf`, `.epub`, `.pdf`, `.ppt`, `.pps`, `.pot`, `.pptx`, `.pptm`, `.ppsx`, `.ppsm`, `.odp`, `.xls`, `.xlsx`, `.xlsm`, `.xlsb`, `.ods`, `.csv`.
2. The format is detected from the file content. Pass `--format <name>` only when detection cannot work: CSV from stdin, or a missing or wrong extension.
3. Exit codes: 0 success, 1 the document could not be converted, 2 usage error. Failures print one `anydoc: <message>` line to stderr. The CLI never prompts.
4. For a large document, write to a file with `-o` and read the parts you need instead of streaming everything into context.
5. Scanned and image-only PDFs need OCR, which anydoc does not do; they fail as unsupported. For scanned, image-only, mixed, or otherwise serious PDF work, prefer the dedicated pdf-inspector skill with the local `detect-pdf`/`pdf2md` and OCRmyPDF/Tesseract/Poppler/Ghostscript workflow.
6. Inside a Node, Python, or Rust codebase, prefer the library over shelling out: `@firecrawl/anydoc` on npm, `firecrawl-anydoc` on PyPI, `anydoc` on crates.io. Each exposes the same `to_markdown` / `toMarkdown` API.
