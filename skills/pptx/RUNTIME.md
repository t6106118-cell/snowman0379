# Local PowerPoint runtime

Generated decks, source generators, and previews belong in the task workspace. Set this skill's directory:

```bash
PPTX_SKILL_DIR=/home/nova/.codex/skills/pptx
```

## Node

The package manifest and lockfile pin PptxGenJS 4.0.1. Preserve the image-size 2.0.4 override when restoring dependencies.

```bash
NODE_PATH="$PPTX_SKILL_DIR/node_modules" node build_deck.cjs output.pptx
```

Use `.cjs` for a copied generator so it also works inside projects configured as ES modules. Dependencies are skill-local. Restore them only if missing or broken:

```bash
npm ci --prefix "$PPTX_SKILL_DIR"
```

React, react-icons, react-dom and sharp are not bundled. Prefer suitable existing image/vector assets. If a required workflow needs optional packages, use an appropriate task-local dependency environment and preserve its lockfile; do not install globally or assume an API example's packages are present.

## Python

Use the skill-local uv environment for bundled helpers. Its locked dependencies include defusedxml, lxml and Pillow for package inspection, schema validation and thumbnails.

```bash
"$PPTX_SKILL_DIR/.venv/bin/python" "$PPTX_SKILL_DIR/scripts/qa_deck.py" output.pptx
```

Restore at this path, rather than moving a virtual environment with old launcher paths:

```bash
uv sync --project "$PPTX_SKILL_DIR" --locked
```

## External executables

Rendering uses `soffice` and `pdftoppm` on the active PATH. The Office wrapper creates an isolated LibreOffice profile and applies its socket workaround only if the environment requires it. No permanent user-profile change is needed.

`markitdown` is not required. Use the content helper for slide text or a suitable installed document converter for broader extraction. Check actual local font matching when fit matters; a font name in the deck neither embeds nor installs it.
