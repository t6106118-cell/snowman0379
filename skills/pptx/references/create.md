# Create an editable presentation

Choose the intended audience, content and output before designing slides. Follow [design.md](design.md) for layout/typography decisions. Read [brand_config.md](brand_config.md) for palette choices, [slide_patterns.md](slide_patterns.md) for a needed layout, and [pptxgenjs_api.md](pptxgenjs_api.md) only for relevant API examples.

## Start in the task workspace

```bash
cp "$PPTX_SKILL_DIR/scripts/build_deck_template.js" build_deck.cjs
```

Replace example text and author/title metadata; adapt layouts and use the requested slide count. The starter's helpers are shared with the layout examples. Keep generators and outputs in the user's workspace, not in the installed skill.

```bash
NODE_PATH="$PPTX_SKILL_DIR/node_modules" node build_deck.cjs output.pptx
```

The optional filename argument is supported by the bundled starter. A different generator must handle its own output path. If resolution fails, use [../RUNTIME.md](../RUNTIME.md), not a global npm installation.

For brand hints from a supplied PowerPoint file:

```bash
"$PPTX_SKILL_DIR/.venv/bin/python" "$PPTX_SKILL_DIR/scripts/extract_brand.py" source.potx
```

This extracts selected colors/fonts, not the layout or all artwork. Use [edit.md](edit.md) to preserve a real template's structure. Keep supported charts, shapes, tables and text native and editable; use images when appropriate to the content.

## Generation constraints

Use the pinned skill-local runtime as shown above. These are generation constraints that ordinary API examples can miss:

- **Set `pres.layout` before adding slides.** The default canvas is `LAYOUT_16x9` = **10" × 5.625"**, not 13.3" wide. Coordinates past the edge are written, not clamped — the shape just isn't on the slide. (`LAYOUT_WIDE` is 13.3" × 7.5".)
- **Hex colors: never `#`, never 8 digits.** `color: "FF0000"`. Both `"#FF0000"` and alpha baked into the hex (`"00000020"`) **corrupt the file**. For translucency: `transparency: 0-100` on fills and images, `opacity: 0.0-1.0` on shadows — each is silently ignored on the other.
- **pptxgenjs mutates option objects in place** (converts values to EMU on first use). Never share one `shadow`/options object across two `add*` calls — build a fresh object each time.
- **Shadow `offset` must be ≥ 0** — a negative offset corrupts the file. To cast a shadow upward, use `angle: 270` with a positive offset.
- **`letterSpacing` is silently ignored** — the real option is `charSpacing`.
- **Lists:** `bullet: true` on each item, never a literal `•` (renders double bullets). Set `breakLine: true` on every array item except the last. Space bulleted paragraphs with `paraSpaceAfter`, not `lineSpacing` (huge gaps).
- **One `new pptxgen()` per output file** — never reuse an instance.
- **`rectRadius` only works on `ROUNDED_RECTANGLE`**, not `RECTANGLE`.
- **Gradient fills aren't supported** — use a gradient image as the background instead.
- **Text boxes have built-in internal padding** — set `margin: 0` whenever text must align with a shape, line, or icon at the same x.
- **Speaker notes go in `slide.addNotes("...")`** (plain text, once per slide), never in a text box on the slide.
- **Keep charts native.** Use `addChart()` for everything PowerPoint can chart (pass an array of `{type, data, options}` for combos). For PowerPoint-native features the library doesn't expose (trendlines, error bars), compute the extra series yourself or post-process the generated OOXML — do not fall back to a rendered image. Only chart types PowerPoint has no native form for (Sankey, network, chord) go in as images.
- **Default charts render bare** — no title, no data labels, dated palette. Set `showTitle` + `title`, `showValue: true` + `dataLabelPosition`, `chartColors: [...]` from your palette, and quiet the frame (`catAxisLabelColor`/`valAxisLabelColor`, `valGridLine: { color, size }`, `catGridLine: { style: "none" }`, `showLegend: false` for a single series).
- **On a stacked bar or column chart, `dataLabelPosition` must be `ctr`, `inEnd`, or `inBase`.** `outEnd` **corrupts the file**.
- **A combo series using `secondaryValAxis`/`secondaryCatAxis` needs both `valAxes` and `catAxes` on the chart options, two entries each.** Without them pptxgenjs writes axis *ids* it never declares, and PowerPoint **discards that chart** and reports the file as corrupt. Supplying only `valAxes` is not enough.
- **After `writeFile()`, run the skill-local Office validator as shown in [qa.md](qa.md).** It reports the two chart faults above and the slide-XML defects PowerPoint refuses, and names the fix for each. Fix them in your generator, not by hand-editing the packed XML.
- **Never reorder the children of `<p:presentation>`.** pptxgenjs writes `<p:notesMasterIdLst>` right after `<p:sldIdLst>` and points both masters at one theme part. PowerPoint reads that happily — move the element and the same deck becomes unopenable.
- **Icons:** use suitable existing SVG/PNG assets, or a verified rendering route. React/react-icons/sharp examples require optional packages that are not bundled; see RUNTIME.md before choosing that route.

## Verify

Use [qa.md](qa.md) after generation: content, package/chart validation, rendering and visual inspection. A source script running successfully does not establish a valid or readable deck.
