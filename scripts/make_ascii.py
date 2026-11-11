from PIL import Image, ImageOps
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "toufeeq-bw.png"
OUT = ROOT / "data" / "ascii.json"

ROWS = 80                 # total rows (portrait height)
CROP = (260, 20, 1060, 820)   # (left, top, right, bottom) in px of toufeeq-bw.png
GAMMA = 1.5               # >1 darkens midtones -> more face detail
CHAR_ASPECT = 0.5         # monospace char is ~2x taller than wide

def main():
    im = Image.open(SRC).convert("L")
    im = im.crop(CROP)                      # square around head + shoulders
    # equalize using subject pixels only (ignore the white bg) so face detail survives
    px = [v for v in im.get_flattened_data() if v < 245]
    lo, hi = sorted(px)[int(len(px)*0.02)], sorted(px)[int(len(px)*0.98)]
    lut = [0 if v < lo else 255 if v > hi else int(((v-lo)/(hi-lo))**GAMMA*255) for v in range(256)]
    im = im.point(lambda v: 255 if v >= 245 else lut[v])
    cols = round(ROWS * (im.width / im.height) / CHAR_ASPECT)
    im = im.resize((cols, ROWS), Image.LANCZOS)
    ramp = " .:-=+*#%@"                     # white bg -> space, dark -> dense
    n = len(ramp) - 1
    rows = []
    for y in range(ROWS):
        line = ""
        for x in range(cols):
            v = im.getpixel((x, y))         # 0 dark .. 255 white
            line += ramp[round((255 - v) / 255 * n)]
        rows.append(line.rstrip())
    OUT.write_text(json.dumps({"cols": cols, "rows": rows}))
    print(f"ok: {cols} cols x {ROWS} rows -> {OUT}")

if __name__ == "__main__":
    main()
