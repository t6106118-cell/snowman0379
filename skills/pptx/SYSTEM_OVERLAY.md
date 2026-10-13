# PPTX workstation overlay

Original environment notes for the Fedora workstation, checked 2026-10-13.
Use these alongside the current official guide. They adapt environment
assumptions without duplicating presentation design rules or helper code.
On another machine, replace these paths and verify its own capabilities.

## Base and environment locations

| Resource | Workstation location |
| --- | --- |
| Separately installed official bundle | /home/nova/.codex/skills/pptx |
| Tool inventory | /home/nova/a1/FEDORA44_WORKSTATION_TOOL_INVENTORY.md |
| Existing standalone Python project | /home/nova/projects/data-analysis-template |

Resolve upstream `scripts/...` paths against the official bundle. Keep task
inputs, generators, outputs, and render scratch in the task's working directory.
Keep the base installation and this overlay separate during updates.

## Dependencies

Upstream's preinstalled-package statements describe its environment. At this
check, `pptxgenjs`, `react-icons`, `react`, `react-dom`, and `sharp` were not
resolvable by Node from `/home/nova/arr`. Check resolution in the actual task
project before adding only its needed dependencies; prefer project-local npm
packages over global installs.

Prefer the task's Python environment. For standalone work, the existing shared
uv project has Pillow and defusedxml, but lacked lxml and markitdown at this
check. It cannot run every upstream helper as-is. Use it only when it satisfies
the task; put additional PPTX dependencies in the task's own uv environment,
rather than modifying the shared project or assuming the system Python has them.

## Text extraction

AnyDoc is installed at `/home/nova/.local/bin/anydoc` and supports PPTX text
conversion. It is an available route when MarkItDown is not in the selected
environment:

```bash
anydoc /absolute/task-dir/deck.pptx -o /absolute/task-dir/deck.md
```

Use this for Markdown extraction; perform rendering and validation separately
when the upstream workflow requires them. The local
`convert-documents-to-markdown` skill documents this installed converter.

## Rendering

Native LibreOffice (`/usr/bin/soffice`, 26.2.6.3) and Poppler
(`/usr/bin/pdftoppm`, 26.01.0) are installed. Native headless conversion produced
a PDF from the `pres.pptx` test fixture with a task-specific LibreOffice profile.
The upstream sandbox's plain-soffice warning is not an established workstation
limitation. Use a separate profile so the task does not reuse an interactive
LibreOffice session:

```bash
mkdir -p /absolute/task-dir/rendered
/usr/bin/soffice -env:UserInstallation=file:///absolute/task-dir/lo-profile \
  --headless --convert-to pdf --outdir /absolute/task-dir/rendered \
  /absolute/task-dir/deck.pptx
/usr/bin/pdftoppm -jpeg -r 150 /absolute/task-dir/rendered/deck.pdf \
  /absolute/task-dir/rendered/slide
```

Inspect generated slide images using their absolute paths. Use a dedicated
render directory and clean only task-owned outputs; broad cleanup globs in a
shared working directory can remove another deck's images. Upstream's content
and visual checks still apply.
