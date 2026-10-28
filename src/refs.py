"""Test-only cliché silhouettes for the shelf test (hand-drawn generics, not copies of any brand file)."""
import os, math
from build import circle, lens, rect, d_of

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "refs")
os.makedirs(D, exist_ok=True)

def save(name, subs):
    open(os.path.join(D, name + ".svg"), "w").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"><path fill="#000" d="{d_of(subs)}"/></svg>\n')

# rounded quatrefoil flower (monogram-print cliché)
save("ref-quatrefoil", [circle(128 + dx, 128 + dy, 52) for dx, dy in ((0, -56), (56, 0), (0, 56), (-56, 0))] + [circle(128, 128, 30)])
# four-leaf clover
u = 0.7071
save("ref-clover", [lens((128, 128), (128 + dx * 110 * u, 128 + dy * 110 * u), 40) for dx, dy in ((1, 1), (1, -1), (-1, 1), (-1, -1))]
     + [rect(122, 150, 134, 236)])
# plus / medical-ish
save("ref-plus", [rect(98, 28, 158, 228), rect(28, 98, 228, 158)])
# generic tote-bag icon
save("ref-bag", [rect(40, 92, 216, 232), rect(78, 40, 94, 96), rect(162, 40, 178, 96), rect(78, 40, 178, 56)])
print("ok")
