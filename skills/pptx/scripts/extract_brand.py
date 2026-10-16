#!/usr/bin/env python3
"""
extract_brand.py — Extract brand colors and fonts from any .potx or .pptx file.

Usage:
    python3 extract_brand.py template.potx
    python3 extract_brand.py existing-deck.pptx

Output:
    Prints a ready-to-paste BRAND config block for build_deck_template.js
"""
import sys, zipfile, xml.etree.ElementTree as ET, re


def extract_brand(path: str):
    tc, fonts, bg = {}, set(), set()

    with zipfile.ZipFile(path) as z:
        # Theme colors
        for tf in [n for n in z.namelist() if re.match(r"ppt/theme/theme\d+\.xml", n)][:1]:
            root = ET.fromstring(z.read(tf).decode())
            ns = "http://schemas.openxmlformats.org/drawingml/2006/main"
            scheme = root.find(f".//{{{ns}}}clrScheme")
            if scheme is not None:
                for child in scheme:
                    role = child.tag.split("}")[-1]
                    for el in child:
                        # sysClr.val is a name such as 'window', not RGB.
                        v = el.get("lastClr") if el.tag.split("}")[-1] == "sysClr" else el.get("val")
                        if v and re.fullmatch(r"[0-9A-Fa-f]{6}", v):
                            tc[role] = v.upper()

        # Fonts and bg colors from slide masters
        for mf in [n for n in z.namelist() if n.startswith("ppt/slideMasters/") and n.endswith(".xml")][:2]:
            root = ET.fromstring(z.read(mf).decode())
            for el in root.iter():
                tag = el.tag.split("}")[-1]
                if tag == "srgbClr":
                    v = el.get("val", "")
                    if re.fullmatch(r"[0-9A-Fa-f]{6}", v):
                        bg.add(v.upper())
                if tag in ("latin", "ea", "cs"):
                    f = el.get("typeface", "")
                    if f and not f.startswith("+"):
                        fonts.add(f)

    primary   = tc.get("accent1") or tc.get("dk2") or "0070C0"
    secondary = tc.get("accent2") or tc.get("accent3") or "003087"
    dark      = tc.get("dk1") or "1A1A1A"
    light     = tc.get("lt1") or "FFFFFF"
    light_bg  = tc.get("lt2") or "F5F5F5"
    accent    = tc.get("accent3") or tc.get("accent4") or "FF6B35"
    font      = sorted(fonts)[0] if fonts else "Calibri"

    print("\n" + "=" * 60)
    print("Paste this BRAND block into build_deck_template.js")
    print("=" * 60)
    print(f"""
const BRAND = {{
  primary:   "{primary}",
  secondary: "{secondary}",
  dark:      "{dark}",
  light:     "{light}",
  lightBg:   "{light_bg}",
  accent:    "{accent}",
  font:      "{font}",
}};
""")
    print("All detected theme colors:")
    for role, val in sorted(tc.items()):
        print(f"  {role:<12} #{val}")
    if fonts:
        print(f"\nFonts: {', '.join(sorted(fonts))}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 extract_brand.py template.potx")
        sys.exit(1)
    extract_brand(sys.argv[1])
