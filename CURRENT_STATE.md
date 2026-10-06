# Current state
Updated: 2026-10-06.

Goal and completion criterion: Split `g.pdf` into exactly four consecutive PDF files, covering every original page once, and verify the resulting files.
Constraints: Preserve `g.pdf`. Communicate in English. Write questions and design friction to `rock.md` during work; proceed with reasonable assumptions if unanswered.
Assumption: Use nearly equal page counts, with any extra pages assigned to earlier parts.
Observed: `g.pdf` exists (6,595,375 bytes). No pre-existing local `AGENTS.md` or `rock.md` was found. Both have now been created.
Available tools: `/usr/bin/qpdf`, `/usr/bin/pdfinfo`, `/usr/bin/pdfseparate`, `/usr/bin/python3`, and `/usr/bin/uv` were verified directly; no installation is needed.
Verified source: 134 pages; `qpdf --check g.pdf` exited 0 with no syntax or stream encoding errors detected.
Status: Complete. Four output PDFs were created using qpdf page selection, preserving source page order.

| Output | Source pages | Verified page count |
| --- | --- | --- |
| `g-part-1.pdf` | 1-34 | 34 |
| `g-part-2.pdf` | 35-68 | 34 |
| `g-part-3.pdf` | 69-101 | 33 |
| `g-part-4.pdf` | 102-134 | 33 |

Verification: Each output passed `qpdf --check` with exit 0 and the expected `--show-npages` result. Counts total 134; ranges are consecutive, cover the entire source, and do not overlap. All four output files exist.
Original SHA-256 before and after: `51b358cb04d696de994a6c00689c426fe709a774c7487237513e4fcb28d93829`; source unchanged.
Limits: Structure and page counts were checked; no visual review of every page was performed.
Questions and friction: `rock.md` records the boundary question and progress; no answer or design friction was observed during splitting.
Next action: None required. If the user supplies different boundaries, treat that as a requested revision and inspect their answer before changing outputs.
