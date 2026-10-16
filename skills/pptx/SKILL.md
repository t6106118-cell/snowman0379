---
name: pptx
description: Create, edit, inspect, and validate local PowerPoint presentations (.pptx) and templates (.potx), including editable slides, native charts, existing layouts, speaker notes, and rendered previews. Use for PowerPoint file work; native Google Slides and HTML presentations follow their own workflows.
license: Proprietary
---

# PowerPoint presentations

Keep the requested content and native editable elements. Work on task-specific files in the user's workspace; preserve the source deck and keep installed skill resources unchanged during ordinary presentation work.

## Choose the required workflow

Read only the references needed for the task:

| Task | Reference |
| --- | --- |
| Create a new deck from notes, a topic, or data | [references/create.md](references/create.md) |
| Edit an existing deck, reuse its layouts, or work with a template | [references/edit.md](references/edit.md) |
| Choose visual structure, typography, spacing, and imagery | [references/design.md](references/design.md) |
| Check content, package structure, charts, and rendered output | [references/qa.md](references/qa.md) |
| Resolve or restore local dependencies | [RUNTIME.md](RUNTIME.md) |

For a content-only inspection, `scripts/qa_deck.py` prints slide text in presentation order. Use `scripts/thumbnail.py` for a labeled visual overview. These do not extract every note, comment, or embedded object; inspect the relevant package parts when requested. Broad document-to-Markdown conversion can use the installed conversion skill.

## Runtime and paths

Set the directory containing this file; on this workstation:

```bash
PPTX_SKILL_DIR=/home/nova/.codex/skills/pptx
```

Run Python helpers with `"$PPTX_SKILL_DIR/.venv/bin/python"`. A copied CommonJS generator resolves the pinned PptxGenJS runtime with:

```bash
NODE_PATH="$PPTX_SKILL_DIR/node_modules" node build_deck.cjs output.pptx
```

Do not infer missing dependencies from a different Python environment or Node resolution without this path. Restore only the relevant runtime as described in RUNTIME.md; do not install globally or into a temporary folder.

## Preserve the requested result

- Infer audience, slide count, and style from the request and supplied material. Ask only when missing information materially changes the result. Follow an existing template or user brand before choosing a new visual system.
- Keep text, shapes, tables, and supported charts editable. Use images where they serve the content or a native representation is unsuitable; avoid rasterizing whole slides merely to reproduce a layout.
- Brand-color extraction is not template-layout reuse. Use the editing route when original layouts, masters, or embedded content must be preserved.
- Keep one coherent design system. Use visuals, banners, bars, or accents when the content, brand, or user asks for them; neither add them to every slide nor forbid them universally. Text-only and image-only slides can be intentional.
- Separate review from changes. Inspecting a deck does not authorize altering its source. Use a new output file for edits unless replacement was requested.

## Verify and deliver

After creating or editing a deck, follow references/qa.md: review content, run the Office validator, render, and inspect slides. Use the original as the validator baseline for template-derived work. Fix observed defects and repeat affected checks after a change.

A successful generator, content scan, or LibreOffice render alone is not complete verification. Report the output path, checks actually performed, and material limits such as font substitution or lack of native Microsoft PowerPoint testing. Deliver useful requested source generators or previews alongside the editable file.
