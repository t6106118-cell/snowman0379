# Brand Configuration Guide

## How to Configure Any Brand

The bundled starter uses a `BRAND` block. Replace the values:

```javascript
const BRAND = {
  primary:   "0070C0",   // Main brand color — used in headers, accents
  secondary: "404040",   // Secondary — used in subheadings, icons
  dark:      "1A1A1A",   // Near-black — body text, dark backgrounds
  light:     "FFFFFF",   // White — light backgrounds, text on dark
  lightBg:   "F5F5F5",   // Soft off-white — slide backgrounds, cards
  accent:    "FF6B35",   // Pop color — CTAs, highlights, badges
  font:      "Calibri",  // Font face — use brand font if available
};
```

> **Rule:** NEVER use `#` prefix on hex colors — PptxGenJS will corrupt the file.

---

## LLM Color Palette Selection

When the user has no brand colors, infer a suitable direction from the audience, subject and existing requirements. Ask only if the missing choice materially changes the result. These palettes are optional starting points:

| Theme | Primary | Secondary | Accent | Dark | Light BG | Font | Best for |
|---|---|---|---|---|---|---|---|
| **Corporate Blue** | `0070C0` | `003087` | `00B0F0` | `1A1A1A` | `F0F4F8` | Calibri | Finance, enterprise |
| **Executive Dark** | `1E2761` | `408EC6` | `7A2048` | `0A0A0A` | `F5F5F5` | Calibri | C-suite, board decks |
| **Tech Green** | `00897B` | `00695C` | `FF6F00` | `212121` | `F1F8F6` | Calibri | Engineering, DevOps |
| **Startup Bold** | `6C63FF` | `3D5AFE` | `FF6584` | `1A1A2E` | `F8F8FF` | Calibri | Product, pitch decks |
| **Minimal Mono** | `212121` | `616161` | `FF5252` | `000000` | `FAFAFA` | Calibri | Design, consulting |
| **Warm Business** | `B85042` | `E7E8D1` | `A7BEAE` | `2C2C2C` | `FDF6F0` | Georgia | Retail, HR, culture |
| **Deep Navy** | `003153` | `005F73` | `EE9B00` | `001220` | `F0F4F8` | Calibri | Healthcare, legal |
| **Vivid Orange** | `E85D04` | `F48C06` | `023E8A` | `1A1A1A` | `FFF8F2` | Calibri | Marketing, sales |

---

## Common Brand Fonts

| Font | Feel | Notes |
|---|---|---|
| `Calibri` | Clean, modern | Common Office font; verify local rendering |
| `Arial` | Corporate, neutral | Common alternative; verify actual matching |
| `Georgia` | Warm, editorial | Good for culture/HR |
| `Trebuchet MS` | Friendly, rounded | Good for product/startup |
| `Cambria` | Formal, serif | Good for legal/finance |

Missing fonts may be substituted differently by each viewer. Check actual rendering; do not assume a specific fallback. Follow design.md for typography and non-Latin text.

---

## Helper: Common Color Roles

```javascript
// Header background      → BRAND.primary
// Header text            → BRAND.light
// Slide background       → BRAND.lightBg  (or BRAND.light)
// Card border accent     → BRAND.primary  (or BRAND.accent)
// Body text              → BRAND.dark
// Muted / caption text   → "888888"
// Success / done         → "2E7D32"
// Warning / pending      → BRAND.accent
// Divider lines          → "E0E0E0"
```

## Additional palette starting points

Preserved from the original PowerPoint design guide; choose only when appropriate to the content or brand.

| Theme | Primary | Secondary | Accent |
|-------|---------|-----------|--------|
| **Midnight Executive** | `1E2761` (navy) | `CADCFC` (ice blue) | `FFFFFF` (white) |
| **Forest & Moss** | `2C5F2D` (forest) | `97BC62` (moss) | `F5F5F5` (cream) |
| **Coral Energy** | `F96167` (coral) | `F9E795` (gold) | `2F3C7E` (navy) |
| **Warm Terracotta** | `B85042` (terracotta) | `E7E8D1` (sand) | `A7BEAE` (sage) |
| **Ocean Gradient** | `065A82` (deep blue) | `1C7293` (teal) | `21295C` (midnight) |
| **Charcoal Minimal** | `36454F` (charcoal) | `F2F2F2` (off-white) | `212121` (black) |
| **Teal Trust** | `028090` (teal) | `00A896` (seafoam) | `02C39A` (mint) |
| **Berry & Cream** | `6D2E46` (berry) | `A26769` (dusty rose) | `ECE2D0` (cream) |
| **Sage Calm** | `84B59F` (sage) | `69A297` (eucalyptus) | `50808E` (slate) |
| **Cherry Bold** | `990011` (cherry) | `FCF6F5` (off-white) | `2F3C7E` (navy) |
