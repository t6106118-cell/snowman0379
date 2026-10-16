# Presentation design

Use for new slides or deliberate restyling. Preserve an existing template when the task is content replacement rather than redesign.

- Give each slide a purpose and reading order. Choose text, charts, images or diagrams for that purpose. A short text-only slide or a photograph without text can be appropriate.
- Follow the user's brand, template or subject. [brand_config.md](brand_config.md) contains starting palettes. Do not stop for a color question when the request already gives enough direction.
- Repeat typography and spacing for consistency; vary layout where content changes. [slide_patterns.md](slide_patterns.md) contains two-column, card, metric, timeline and flow examples.
- Use banners, rules, accent bars or dark backgrounds when the brand or communication requires them. Avoid decoration added merely to fill space. These are design choices, not universal requirements or forbidden shapes.
- Keep native text, shapes, tables and supported charts editable. Use images when a native representation is unsuitable, preserving requested source assets.

## Typography and fit

Approximately 28-40 pt titles and 16-24 pt body text are useful starting points, scaled to the canvas and viewing conditions. Keep captions legible. Shorten, split or enlarge a container before making important text unreadably small.

Font rendering depends on the recipient and local renderer. Substitution can change glyph widths. Check local matching when fit matters; do not assume a fixed safe-font list renders identically everywhere. Respect requested fonts and leave appropriate space when metrics cannot be reproduced. Check shaping, reading direction and wrapping for non-Latin text when relevant.

Align body paragraphs for their reading direction. Use adequate contrast and consistent gaps. About 0.4-0.5 inches at edges and 0.2-0.4 between blocks are starting points, not grounds to reject an intentional template layout. Text boxes have internal padding; set `margin: 0` for precise alignment or account for the padding.

## Visual review

Inspect rendered slides for clipped text, overlaps, off-canvas content, crowded labels, uneven gaps, misaligned columns, leftover template slots, wrong order and poor contrast. Replacement text may wrap differently from the template. Fix actual defects, not an invented issue to satisfy a review ritual. See [qa.md](qa.md) for commands and limits.
