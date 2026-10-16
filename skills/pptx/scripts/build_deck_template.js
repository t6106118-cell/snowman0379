/**
 * Editable PowerPoint starter. Copy to the task workspace as build_deck.cjs.
 * Replace example content and metadata; helpers match references/slide_patterns.md.
 * NODE_PATH=/home/nova/.codex/skills/pptx/node_modules node build_deck.cjs output.pptx
 */
const pptxgen = require("pptxgenjs");
const BRAND = {
  primary: "0070C0", secondary: "003087", dark: "1A1A1A",
  light: "FFFFFF", lightBg: "F3F6FA", accent: "D97706", font: "Arial"
};
const FONT = BRAND.font;
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10 by 5.625 inches; adapt all coordinates for another canvas.
pres.author = "Presentation author";
pres.title = "Presentation title";
pres.subject = "Editable presentation";
pres.lang = "en-US";

function addHeader(slide, title, subtitle) {
  slide.addText(title, {
    x: 0.5, y: 0.35, w: 9, h: 0.55, margin: 0,
    fontFace: FONT, fontSize: 25, bold: true, color: BRAND.dark
  });
  if (subtitle) slide.addText(subtitle, {
    x: 0.5, y: 0.96, w: 9, h: 0.3, margin: 0,
    fontFace: FONT, fontSize: 13, color: "536171"
  });
}

function addFooter(slide, label, pageNum) {
  slide.addText(label || "", {
    x: 0.5, y: 5.25, w: 8, h: 0.2, margin: 0,
    fontFace: FONT, fontSize: 9, color: "64748B"
  });
  if (pageNum) slide.addText(String(pageNum), {
    x: 9, y: 5.25, w: 0.5, h: 0.2, margin: 0, align: "right",
    fontFace: FONT, fontSize: 9, color: "64748B"
  });
}

function addCard(slide, x, y, w, h, title, body, accentColor) {
  slide.addShape(pres.ShapeType.rect, {
    x, y, w, h, fill: { color: BRAND.lightBg },
    line: { color: "E2E8F0", width: 0.5 }
  });
  if (title) slide.addText(title, {
    x: x + 0.2, y: y + 0.16, w: w - 0.4, h: 0.35, margin: 0,
    fontFace: FONT, fontSize: 17, bold: true, color: accentColor || BRAND.primary
  });
  if (body) slide.addText(body, {
    x: x + 0.2, y: y + (title ? 0.65 : 0.2), w: w - 0.4,
    h: h - (title ? 0.8 : 0.4), margin: 0,
    fontFace: FONT, fontSize: 14, color: BRAND.dark, wrap: true
  });
}

// Example title: replace the content and metadata before delivery.
{
  const s = pres.addSlide();
  s.background = { color: BRAND.dark };
  s.addText("Presentation title", {
    x: 0.6, y: 1.35, w: 8.8, h: 1.2, margin: 0,
    fontFace: FONT, fontSize: 36, bold: true, color: BRAND.light
  });
  s.addText("One clear message for the intended audience", {
    x: 0.6, y: 2.9, w: 8.8, h: 0.8, margin: 0,
    fontFace: FONT, fontSize: 20, color: "DAE4EF"
  });
}
// Example cards: adapt layout and text length to actual content.
{
  const s = pres.addSlide();
  s.background = { color: BRAND.light };
  addHeader(s, "Four useful points", "Replace the examples with the actual story.");
  [
    ["First point", "Explain the first concrete finding."],
    ["Second point", "Connect the evidence to its consequence."],
    ["Third point", "Show the meaningful comparison."],
    ["Fourth point", "State the next useful action."]
  ].forEach(([title, body], i) => addCard(s,
    0.5 + (i % 2) * 4.7, 1.5 + Math.floor(i / 2) * 1.7,
    4.3, 1.5, title, body, i % 2 ? BRAND.secondary : BRAND.primary));
  addFooter(s, "Presentation title", 2);
}
// Example closing.
{
  const s = pres.addSlide();
  s.background = { color: BRAND.light };
  addHeader(s, "A concrete next step", "Close with the decision or action the audience needs.");
  s.addText("Replace this message with the intended conclusion.", {
    x: 0.6, y: 2.0, w: 8.8, h: 1.4, margin: 0,
    fontFace: FONT, fontSize: 26, color: BRAND.primary
  });
  addFooter(s, "Presentation title", 3);
}

// WRITE OUTPUT
const outputPath = process.argv[2] || "output.pptx";
pres.writeFile({ fileName: outputPath })
  .then(() => console.log("Created " + outputPath))
  .catch(error => { console.error(error); process.exitCode = 1; });
