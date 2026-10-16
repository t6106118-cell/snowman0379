#!/usr/bin/env python3
"""Print slide text in presentation order and check an optional slide count.

Possible leftover wording is a review warning, not proof that requested content
is wrong. Image-only/text-free slides are valid. Use the Office validator and
rendered inspection for package structure and visual QA.
"""

import argparse
from pathlib import Path
import re
import sys
import zipfile

from defusedxml import ElementTree as ET
from defusedxml.common import DefusedXmlException
from office.helpers import SLIDE_REL_TYPE, opc_target

P = "http://schemas.openxmlformats.org/presentationml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
POSSIBLE_EXAMPLE = re.compile(r"\b(TODO|XXX|lorem|ipsum|TBD|PLACEHOLDER)\b|\[insert", re.I)


def slide_texts(path):
    with zipfile.ZipFile(path) as archive:
        presentation = ET.fromstring(archive.read("ppt/presentation.xml"))
        relationships = ET.fromstring(archive.read("ppt/_rels/presentation.xml.rels"))
        by_id = {rel.get("Id"): rel for rel in relationships}
        result = []
        for slide in presentation.findall(f"{{{P}}}sldIdLst/{{{P}}}sldId"):
            rid = slide.get(f"{{{R}}}id")
            rel = by_id.get(rid)
            if rel is None or rel.get("Type") != SLIDE_REL_TYPE:
                raise ValueError(f"Slide relationship {rid!r} is missing or has the wrong type")
            part = opc_target(rel.get("Target", ""), "ppt/presentation.xml", rel.get("TargetMode", ""))
            if part is None:
                raise ValueError(f"Slide relationship {rid!r} has no internal target")
            root = ET.fromstring(archive.read(part))
            text = " ".join(el.text.strip() for el in root.iter(f"{{{A}}}t") if el.text and el.text.strip())
            result.append((part, text))
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--expected-slides", type=int)
    args = parser.parse_args()
    try:
        slides = slide_texts(args.path)
    except (OSError, zipfile.BadZipFile, KeyError, ValueError, ET.ParseError, DefusedXmlException) as error:
        print(f"Content scan failed: {error}", file=sys.stderr)
        return 2

    print(f"Content scan: {args.path} ({len(slides)} slides)")
    warnings = []
    for number, (part, text) in enumerate(slides, 1):
        print(f"  {number}: {text or '[no slide text; inspect visuals]'}")
        if match := POSSIBLE_EXAMPLE.search(text):
            warnings.append(f"Slide {number} ({part}): review possible example wording {match.group()!r}")
    for warning in warnings:
        print(f"REVIEW: {warning}")
    if args.expected_slides is not None and len(slides) != args.expected_slides:
        print(f"Slide count mismatch: expected {args.expected_slides}, got {len(slides)}", file=sys.stderr)
        return 1
    if not slides:
        print("No slides found", file=sys.stderr)
        return 1
    print("Count/slide-text scan complete; review content and rendered output before delivery.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
