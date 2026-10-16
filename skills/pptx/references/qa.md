# Verify a PowerPoint file

Use the skill-local runtime. Set `PPTX_SKILL_DIR` as in SKILL.md. Give outputs deck-specific names so previews do not overwrite another deck's files.

## Content

```bash
"$PPTX_SKILL_DIR/.venv/bin/python" "$PPTX_SKILL_DIR/scripts/qa_deck.py" output.pptx --expected-slides 5
```

Use the planned count or omit it when unknown. The helper prints text in presentation order and flags possible leftover wording. Review matches against the request: a literal mention of TODO or placeholders may be intentional. It reports non-text slides without rejecting them solely for lacking text. The scan does not check notes, comments, full package structure or visual layout.

## Structure

```bash
"$PPTX_SKILL_DIR/.venv/bin/python" "$PPTX_SKILL_DIR/scripts/office/validate.py" output.pptx
```

For edits or template-derived files:

```bash
"$PPTX_SKILL_DIR/.venv/bin/python" "$PPTX_SKILL_DIR/scripts/office/validate.py" output.pptx --original source.pptx
```

The validator checks schemas, package relationships, content types, slides and charts. An original file baselines inherited schema/slide issues; relationship, content-type and chart failures still need interpretation. Do not dismiss a new defect because the source has other problems. Fix generation defects in the generator and rebuild. Package validity is not proof of correct content or visual layout.

## Render and inspect

For a labeled overview, pass a distinct prefix:

```bash
"$PPTX_SKILL_DIR/.venv/bin/python" "$PPTX_SKILL_DIR/scripts/thumbnail.py" output.pptx output-overview
```

For readable individual slides:

```bash
mkdir -p output-preview
"$PPTX_SKILL_DIR/.venv/bin/python" "$PPTX_SKILL_DIR/scripts/office/soffice.py" --headless --convert-to pdf --outdir output-preview output.pptx
pdftoppm -png -r 150 output-preview/output.pdf output-preview/slide
```

Inspect images with the available image-viewing tool. Confirm the PDF exists and the page count matches visible slides; account separately for hidden slides. Use the overview for navigation and individual images when text, charts or detail cannot be judged at thumbnail size.

After an edit, regenerate the PDF before inspecting new images. Remove only known stale task previews or use a fresh task-specific directory, not a broad deletion pattern. Recheck changed output and affected shared elements without repeating sufficient checks for an unchanged condition.

## Delivery

Report the editable file path and checks actually performed. State material limits such as font substitution or lack of native PowerPoint testing. A LibreOffice render does not establish identical behavior in all Microsoft PowerPoint versions. Preserve the source and useful task artifacts, not obsolete installations or backup copies.
