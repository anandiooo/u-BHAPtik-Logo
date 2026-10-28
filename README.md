# BHAPtik logo project

| Folder | What's inside |
|---|---|
| `final/` | **The approved logo kit**: round 5b, direction A "Furoshiki Bundle, minimal". It holds the SVG masters (`svg/`), PNGs (`png/`), favicon and web icons (`icons/`), the presentation (`board.html`, `slides/`), `guidelines.md`, and the handover notes in `README.md`. |
| `draft/` | Work in progress from rounds 1 to 5. `concepts/` holds the concept sheets, `tests/` the HTML preview and shelf tests, `colour/` the colour hints and pattern previews, `out/` every generated SVG version, `renders/` the PNG renders, and `refs/` the reference logos. |
| `src/` | The scripts. `build.py` has the shared helpers and wordmark, `r2.py` the BHAPtik wordmark, `r4.py`, `r5.py` and `r5b.py` the concept rounds (the final mark is `r5b.m1g()` and `m1gs()`), and `kit.py` builds `final/`. |
| `docs/` | `brief.md`, `research.md`, `concepts.md` and `test-log.md`. |

To rebuild, run these from this folder:
- `python src/kit.py` regenerates `final/svg`.
- `python src/r5b.py <version>` writes drafts to `draft/out`.

Mood references are in `../../bhaptik-reference/`.
