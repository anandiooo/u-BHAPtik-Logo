"""Simple test sheet: the final kit (one file per version, no colour repeats), then the last version of every
draft concept per round (symbols only), plus the round-5b milestones. Identical drawings are shown once.
Open from projects/bhaptik. Run: python src/test_sheet.py"""
import hashlib, html, os, re

PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FINAL = [("bhaptik-horizontal-black", "Horizontal"), ("bhaptik-stacked-black", "Stacked"),
         ("bhaptik-symbol-black", "Symbol"), ("bhaptik-symbol-small-black", "Small-size symbol"),
         ("bhaptik-wordmark-black", "Wordmark"), ("bhaptik-horizontal-accent-on-black", "Accent on black"),
         ("app-icon", "App icon")]
ROUNDS = [("", "Round 1"), ("r2", "Round 2"), ("r4", "Round 4"), ("r5", "Round 5"), ("r5b", "Round 5b")]
MILESTONES = {15: "A3 (liked)", 18: "A4 (refined)", 22: "A6 (most minimal)"}   # v19 = the final, shown above
SKIP = re.compile(r"lockup|pattern|wordmark|colour|hint")

def card(rel, label, dark=False):
    return (f'<figure><div class="t{" d" if dark else ""}"><img src="{html.escape(rel)}" alt=""></div>'
            f'<figcaption>{html.escape(label)}</figcaption></figure>')

def section(title, cards):
    return f'<h2>{title}</h2><div class="g">{"".join(cards)}</div>'

parts = [section("Final", [card(f"final/svg/{f}.svg", label) for f, label in FINAL])]

out = os.path.join(PROJ, "draft", "out")
latest, seen = {}, set()
for f in os.listdir(out):
    m = re.match(r"(.+?)-(r\d+b?)?v(\d+)\.svg$", f)
    if not m or SKIP.search(m.group(1)):
        continue
    name, rnd, v = m.group(1), m.group(2) or "", int(m.group(3))
    key = (rnd, name)
    if key not in latest or v > latest[key][0]:
        latest[key] = (v, f)

def unique(f):
    h = hashlib.md5(open(os.path.join(out, f), "rb").read()).hexdigest()
    if h in seen:
        return False
    seen.add(h)
    return True

for rnd, title in ROUNDS:
    cards = [card(f"draft/out/{f}", f"{name.replace('-symbol', '')} · v{v}")
             for (r, name), (v, f) in sorted(latest.items())
             if r == rnd and not (rnd == "r5b" and name in ("m1-symbol", "m1s-symbol")) and unique(f)]
    if rnd == "r5b":   # the A-direction steps that led to the final
        cards += [card(f"draft/out/m1-symbol-r5bv{v}.svg", f"m1 · v{v} · {note}") for v, note in MILESTONES.items()
                  if os.path.exists(os.path.join(out, f"m1-symbol-r5bv{v}.svg")) and unique(f"m1-symbol-r5bv{v}.svg")]
    if cards:
        parts.append(section(title, cards))

page = f"""<!doctype html><html lang="en"><meta charset="utf-8"><title>BHAPtik - test sheet</title>
<style>
body{{margin:0;padding:24px 32px 48px;font:14px/1.4 system-ui,sans-serif;color:#1A1614;background:#faf8f4}}
h1{{font-size:22px;margin:0 0 4px}}h2{{font-size:16px;margin:28px 0 10px}}p{{margin:0;color:#8a8178;font-size:12px}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:12px}}figure{{margin:0}}
.t{{background:#F3EBDD;border-radius:10px;aspect-ratio:1.3;display:flex;align-items:center;justify-content:center;padding:14px}}
.t img{{max-width:100%;max-height:100%}}figcaption{{font-size:11px;color:#6b635b;margin-top:4px}}
</style>
<h1>BHAPtik - test sheet</h1><p>Final kit, then the last version of each draft concept per round. Full files: final/svg, draft/out.</p>
{"".join(parts)}
</html>
"""
open(os.path.join(PROJ, "test-sheets.html"), "w", encoding="utf-8").write(page)
print("cards:", page.count("<figure>"))
