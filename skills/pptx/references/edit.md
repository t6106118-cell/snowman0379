# Edit a presentation or reuse a template

Inspect relevant slides before changing content. Use `scripts/qa_deck.py` for slide text and `scripts/thumbnail.py source.pptx source-overview` for a labeled grid. Run helpers with the Python interpreter and paths in SKILL.md. The thumbnail helper accepts .pptx; for .potx inspection, make a task-local .pptx view of the template without overwriting it.

Reuse the actual package for faithful layouts, masters, images and embedded content. Extracting brand colors/fonts alone does not reproduce a template. Preserve the source; output to a distinct file unless replacement is requested.

## Structural changes

Perform needed duplication, insertion, deletion and reordering before editing slide content so a later duplication does not clone already-replaced text.

```bash
"$PPTX_SKILL_DIR/.venv/bin/python" "$PPTX_SKILL_DIR/scripts/add_slide.py" source.pptx slide2.xml --after slide2.xml -o edited.pptx
```

Always pass `-o` when the source must be preserved. The helper also accepts an unpacked directory or a `slideLayoutN.xml` source. It updates package registration and relationships; do not copy slide XML alone. A duplicate can share chart/SmartArt/embedded-object parts with the source slide, so editing a shared part affects both. Separate those parts before an independent edit is required.

For several package edits, use a fresh task-specific unpacked directory. The existing Office helpers preserve package bookkeeping and reject unsafe archive paths:

```bash
PYTHONPATH="$PPTX_SKILL_DIR/scripts" "$PPTX_SKILL_DIR/.venv/bin/python" - <<'PY'
from pathlib import Path
from zipfile import ZipFile
from office.helpers import safe_extract
with ZipFile('source.pptx') as archive:
    safe_extract(archive, Path('unpacked'))
PY
```

Reorder/delete slides by changing `<p:sldIdLst>` in `ppt/presentation.xml`; run `scripts/clean.py unpacked` after the final slide list to remove orphaned slides/media/relationships. Do not clean before registering slides that should remain. Repack to a new output, rather than updating a ZIP that could retain deleted members:

```bash
PYTHONPATH="$PPTX_SKILL_DIR/scripts" "$PPTX_SKILL_DIR/.venv/bin/python" - <<'PY'
from pathlib import Path
from office.helpers import rezip
rezip(Path('unpacked'), Path('edited.pptx'))
PY
```

## Preserve the document's meaning and formatting

- Use `defusedxml.minidom` for XML transforms, preserving namespace prefixes and document structure. Do not round-trip slide XML through a writer that replaces its prefixes blindly.
- Keep presentation child order intact, including notes/master ordering; see create.md for the generator-specific constraint. Maintain required package relationships and content types.
- Replace text runs while retaining the styles that should survive. In python-pptx, assigning `text_frame.text` collapses formatting; assigning individual `run.text` preserves run styles. That optional library is not bundled and does not provide arbitrary package editing or automatic slide duplication.
- Template slots are not source items. If a four-person layout now contains three people, remove the unused person's whole group, including its artwork, rather than leaving an empty picture.
- Keep one `<a:p>` per list item and preserve its `<a:pPr>`. Let bullets inherit from the layout unless deliberately overriding with `<a:buChar>`, `<a:buAutoNum>` or `<a:buNone>`; do not insert a literal bullet character into already-bulleted text.
- Set `xml:space="preserve"` on `<a:t>` when leading/trailing spaces matter. Preserve required emphasis, source citations, notes, chart data and relationships within the task's scope.
- Reuse existing SVG/EMF artwork through its slide/layout when an optional image library cannot read it.

Legacy .ppt inputs need conversion through the Office wrapper before package editing. Native .potx packages can be unpacked/repacked like .pptx; retain the requested template type and extension on output.

## Verify

Use [qa.md](qa.md), passing `--original source.pptx` (or the original template) to the validator. Inspect edited slides and shared elements affected by the change, and confirm the original is preserved. A successful XML transform alone does not prove correct rendering.
