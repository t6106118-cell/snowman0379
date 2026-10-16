# Slide Patterns — Copy-Paste Templates

All patterns use a `BRAND` object and `FONT` constant.
Replace with your values (see `brand_config.md`).


---

## Shared helpers

Use addHeader, addFooter and addCard from [the bundled starter](../scripts/build_deck_template.js). Their signatures match the calls below; do not paste a second incompatible helper implementation. Examples assume the starter's 10 by 5.625-inch canvas. Adapt content, coordinates and typography rather than treating every pattern or accent as mandatory.

## Pattern: Title Slide

```javascript
{
  const s = pres.addSlide();
  s.background = { color: BRAND.dark };

  // Optional brand accents: omit if they do not serve the requested design
  s.addShape(pres.ShapeType.rect, {
    x: 0, y: 0, w: 0.55, h: 5.625,
    fill: { color: BRAND.primary }, line: { color: BRAND.primary }
  });
  s.addShape(pres.ShapeType.rect, {
    x: 0.55, y: 0, w: 0.12, h: 5.625,
    fill: { color: BRAND.accent }, line: { color: BRAND.accent }
  });

  s.addText("Your Presentation Title", {
    x: 1.0, y: 1.3, w: 8.5, h: 0.75,
    fontSize: 38, fontFace: FONT, bold: true, color: BRAND.light, margin: 0
  });
  s.addText("Subtitle or Tagline Here", {
    x: 1.0, y: 2.15, w: 8.5, h: 0.4,
    fontSize: 18, fontFace: FONT, color: BRAND.primary, margin: 0
  });
  // Divider
  s.addShape(pres.ShapeType.rect, {
    x: 1.0, y: 2.7, w: 3.5, h: 0.05,
    fill: { color: BRAND.accent }, line: { color: BRAND.accent }
  });
  s.addText("Presenter Name  |  Department  |  Date", {
    x: 1.0, y: 4.9, w: 8, h: 0.3,
    fontSize: 11, fontFace: FONT, color: "888888", margin: 0
  });
}
```

---

## Pattern: Two-Column (Problem / Info)

```javascript
{
  const s = pres.addSlide();
  s.background = { color: BRAND.light };
  addHeader(s, "Slide Title", "Optional subtitle");
  addFooter(s, "Company  |  Date", 2);

  // Left column
  s.addText("Left Heading", {
    x: 0.35, y: 1.05, w: 4.4, h: 0.35,
    fontSize: 14, fontFace: FONT, bold: true, color: BRAND.dark, margin: 0
  });
  s.addText([
    { text: "First point here", options: { bullet: true, breakLine: true } },
    { text: "Second point here", options: { bullet: true, breakLine: true } },
    { text: "Third point here", options: { bullet: true } },
  ], {
    x: 0.35, y: 1.45, w: 4.4, h: 2.5,
    fontSize: 11, fontFace: FONT, color: BRAND.dark
  });

  // Right column (card style)
  s.addShape(pres.ShapeType.rect, {
    x: 5.1, y: 1.05, w: 4.55, h: 3.9,
    fill: { color: BRAND.lightBg }, line: { color: "E0E0E0" }
  });
  s.addShape(pres.ShapeType.rect, {
    x: 5.1, y: 1.05, w: 4.55, h: 0.06,
    fill: { color: BRAND.primary }, line: { color: BRAND.primary }
  });
  s.addText("Right Heading", {
    x: 5.25, y: 1.15, w: 4.2, h: 0.35,
    fontSize: 13, fontFace: FONT, bold: true, color: BRAND.primary, margin: 0
  });
  s.addText("Content for the right column goes here.", {
    x: 5.25, y: 1.6, w: 4.2, h: 3.2,
    fontSize: 10.5, fontFace: FONT, color: "555555", wrap: true, margin: 0
  });
}
```

---

## Pattern: Flow Diagram (Process Steps)

```javascript
{
  const s = pres.addSlide();
  s.background = { color: BRAND.light };
  addHeader(s, "Process Flow", "How it works");
  addFooter(s, "Company  |  Date", 3);

  const steps = [
    { label: "Step 1\nInput",     color: BRAND.primary },
    { label: "Step 2\nProcess",   color: BRAND.secondary },
    { label: "Step 3\nValidate",  color: BRAND.accent },
    { label: "Step 4\nOutput",    color: "2E7D32" },
  ];

  steps.forEach((step, i) => {
    const x = 0.5 + i * 2.3;
    s.addShape(pres.ShapeType.rect, {
      x, y: 1.8, w: 2.0, h: 0.9,
      fill: { color: BRAND.lightBg }, line: { color: step.color, width: 1.5 },
      shadow: { type: "outer", color: "000000", blur: 3, offset: 1, angle: 135, opacity: 0.1 }
    });
    s.addText(step.label, {
      x, y: 1.8, w: 2.0, h: 0.9,
      fontSize: 11, fontFace: FONT, bold: true, color: step.color,
      align: "center", valign: "middle", margin: 0
    });
    // Arrow (except last)
    if (i < steps.length - 1) {
      s.addShape(pres.ShapeType.rect, {
        x: x + 2.0, y: 2.2, w: 0.28, h: 0.06,
        fill: { color: "888888" }, line: { color: "888888" }
      });
      s.addText("▶", {
        x: x + 2.16, y: 2.12, w: 0.18, h: 0.22,
        fontSize: 9, fontFace: FONT, color: "888888", margin: 0
      });
    }
  });
}
```

---

## Pattern: 2×2 Cards

```javascript
{
  const s = pres.addSlide();
  s.background = { color: BRAND.light };
  addHeader(s, "Key Points", "Four highlights");
  addFooter(s, "Company  |  Date", 4);

  const cards = [
    { title: "Point One",   body: "Description for point one goes here.",   color: BRAND.primary },
    { title: "Point Two",   body: "Description for point two goes here.",   color: BRAND.accent },
    { title: "Point Three", body: "Description for point three goes here.", color: "2E7D32" },
    { title: "Point Four",  body: "Description for point four goes here.",  color: BRAND.secondary },
  ];

  cards.forEach((card, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    addCard(s,
      0.3 + col * 4.85,   // x
      1.1 + row * 1.9,    // y
      4.5, 1.7,            // w, h
      card.title, card.body, card.color
    );
  });
}
```

---

## Pattern: Metrics (Large Number Callouts)

```javascript
{
  const s = pres.addSlide();
  s.background = { color: BRAND.light };
  addHeader(s, "Key Metrics", "Numbers at a glance");
  addFooter(s, "Company  |  Date", 5);

  const metrics = [
    { val: "98%",   label: "Uptime",         sub: "Last 30 days",  color: "2E7D32" },
    { val: "1.2s",  label: "Response Time",  sub: "P99 latency",   color: BRAND.primary },
    { val: "400+",  label: "Tests Passing",  sub: "Automated",     color: BRAND.accent },
    { val: "12",    label: "Rules Active",   sub: "Enforced",      color: BRAND.secondary },
    { val: "< 5m",  label: "Deploy Time",    sub: "Per service",   color: "6A1B9A" },
    { val: "Zero",  label: "Incidents",      sub: "This quarter",  color: "E65100" },
  ];

  metrics.forEach((m, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const x = 0.3 + col * 3.2;
    const y = 1.1 + row * 1.9;

    s.addShape(pres.ShapeType.rect, {
      x, y, w: 3.0, h: 1.6,
      fill: { color: BRAND.light }, line: { color: "E0E0E0" },
      shadow: { type: "outer", color: "000000", blur: 3, offset: 1, angle: 135, opacity: 0.08 }
    });
    // Optional accent for this metric card
    s.addShape(pres.ShapeType.rect, {
      x, y, w: 3.0, h: 0.07,
      fill: { color: m.color }, line: { color: m.color }
    });
    s.addText(m.val, {
      x: x + 0.15, y: y + 0.15, w: 2.7, h: 0.65,
      fontSize: 30, fontFace: FONT, bold: true, color: m.color, margin: 0
    });
    s.addText(m.label, {
      x: x + 0.15, y: y + 0.82, w: 2.7, h: 0.3,
      fontSize: 11.5, fontFace: FONT, bold: true, color: BRAND.dark, margin: 0
    });
    s.addText(m.sub, {
      x: x + 0.15, y: y + 1.15, w: 2.7, h: 0.3,
      fontSize: 9, fontFace: FONT, color: "888888", margin: 0
    });
  });
}
```

---

## Pattern: Timeline / Next Steps (3 Phases)

```javascript
{
  const s = pres.addSlide();
  s.background = { color: BRAND.light };
  addHeader(s, "Next Steps", "Three phases");
  addFooter(s, "Company  |  Date", 6);

  const phases = [
    {
      label: "PHASE 1\nImmediate",
      color: BRAND.primary, bg: BRAND.lightBg,
      items: ["Action item one", "Action item two", "Action item three"],
    },
    {
      label: "PHASE 2\nShort Term",
      color: BRAND.accent, bg: BRAND.lightBg,
      items: ["Action item one", "Action item two", "Action item three"],
    },
    {
      label: "PHASE 3\nLong Term",
      color: BRAND.secondary, bg: BRAND.lightBg,
      items: ["Action item one", "Action item two", "Action item three"],
    },
  ];

  phases.forEach((ph, i) => {
    const x = 0.3 + i * 3.2;
    s.addShape(pres.ShapeType.rect, {
      x, y: 1.05, w: 3.0, h: 3.8,
      fill: { color: ph.bg }, line: { color: ph.color, width: 1 },
      shadow: { type: "outer", color: "000000", blur: 4, offset: 2, angle: 135, opacity: 0.08 }
    });
    s.addShape(pres.ShapeType.rect, {
      x, y: 1.05, w: 3.0, h: 0.65,
      fill: { color: ph.color }, line: { color: ph.color }
    });
    s.addText(ph.label, {
      x: x + 0.12, y: 1.1, w: 2.76, h: 0.55,
      fontSize: 11, fontFace: FONT, bold: true, color: BRAND.light,
      align: "center", valign: "middle", margin: 0
    });
    ph.items.forEach((item, j) => {
      s.addShape(pres.ShapeType.rect, {
        x: x + 0.15, y: 1.85 + j * 0.82, w: 0.07, h: 0.42,
        fill: { color: ph.color }, line: { color: ph.color }
      });
      s.addText(item, {
        x: x + 0.32, y: 1.82 + j * 0.82, w: 2.5, h: 0.52,
        fontSize: 10.5, fontFace: FONT, color: BRAND.dark, wrap: true, margin: 0
      });
    });
  });
}
```

---

## Pattern: Summary / Closing Slide

```javascript
{
  const s = pres.addSlide();
  s.background = { color: BRAND.primary };

  // Optional brand accent
  s.addShape(pres.ShapeType.rect, {
    x: 9.5, y: 0, w: 0.5, h: 5.625,
    fill: { color: BRAND.accent }, line: { color: BRAND.accent }
  });

  s.addText("Summary", {
    x: 0.5, y: 0.4, w: 8, h: 0.65,
    fontSize: 32, fontFace: FONT, bold: true, color: BRAND.light, margin: 0
  });
  s.addShape(pres.ShapeType.rect, {
    x: 0.5, y: 1.1, w: 5, h: 0.05,
    fill: { color: BRAND.light }, line: { color: BRAND.light }
  });

  const done = ["Completed item 1", "Completed item 2", "Completed item 3"];
  const todo = ["Pending item 1", "Pending item 2"];

  s.addText("Done", {
    x: 0.5, y: 1.25, w: 4.2, h: 0.32,
    fontSize: 13, fontFace: FONT, bold: true, color: "FFCCCC", margin: 0
  });
  done.forEach((d, i) => {
    s.addText("✓  " + d, {
      x: 0.5, y: 1.62 + i * 0.42, w: 4.5, h: 0.34,
      fontSize: 11, fontFace: FONT, color: BRAND.light, margin: 0
    });
  });

  s.addText("Pending", {
    x: 5.3, y: 1.25, w: 3.8, h: 0.32,
    fontSize: 13, fontFace: FONT, bold: true, color: "FFCCCC", margin: 0
  });
  todo.forEach((t, i) => {
    s.addText("◎  " + t, {
      x: 5.3, y: 1.62 + i * 0.42, w: 4.0, h: 0.34,
      fontSize: 11, fontFace: FONT, color: "FFE0E0", margin: 0
    });
  });

  s.addShape(pres.ShapeType.rect, {
    x: 0.5, y: 4.2, w: 8.8, h: 0.05,
    fill: { color: BRAND.light }, line: { color: BRAND.light }
  });
  s.addText("Closing message or call to action.", {
    x: 0.5, y: 4.35, w: 8.8, h: 0.32,
    fontSize: 12, fontFace: FONT, bold: true, color: BRAND.light, margin: 0
  });
  s.addText("Presenter  |  Team  |  Date", {
    x: 0.5, y: 5.0, w: 8.8, h: 0.25,
    fontSize: 9, fontFace: FONT, color: "FF9999", margin: 0
  });
}
```
