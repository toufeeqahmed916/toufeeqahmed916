"""Renders animated SVG cards for the GitHub profile README.
Usage:  python scripts/render_readme_cards.py            (animated)
        STATIC=1 python scripts/render_readme_cards.py  (final frame, for screenshots)
"""
import base64, json, os, pathlib
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
CARDS = ROOT / "cards"
STATIC = os.environ.get("STATIC") == "1"

C = {
    "paper": "#F4F3EF", "card": "#ECEAE4", "ink": "#111111", "mute": "#6B6A66",
    "accent": "#A3E635",   # lime (was blue)
    "web": "#FFC61A", "designer": "#EF3B2D",
}
NAME = ("Toufeeq", "Shaikh")
LABEL = "AI ENGINEER + FULL STACK DEVELOPER"
TAGLINE = ("I build AI-powered products", "and full stack web apps.")
LINK = "PORTFOLIO"
TX = 44    # left edge of the text column
PX = 510   # left edge of the portrait (right side); lower = move portrait further left


def font_css():
    """Embed subset fonts as base64 data URIs (an <img> SVG can't load web fonts)."""
    faces = [("Instrument Serif", "normal", "serif-400.woff2"),
             ("Instrument Serif", "italic", "serif-400i.woff2"),
             ("Geist Mono", "normal", "mono-400.woff2")]
    css = ""
    for fam, style, fn in faces:
        p = ROOT / "fonts" / fn
        if p.exists():
            b64 = base64.b64encode(p.read_bytes()).decode()
            css += (f"@font-face{{font-family:'{fam}';font-style:{style};"
                    f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")
    return css


BASE_CSS = """
.serif{font-family:'Instrument Serif',Georgia,serif}
.mono{font-family:'Geist Mono',ui-monospace,Menlo,Consolas,monospace}
@keyframes rise{from{opacity:0;transform:translateY(34px)}to{opacity:1;transform:none}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}
@keyframes nudge{0%,100%{transform:translate(0,0)}50%{transform:translate(2px,-2px)}}
.rise{animation:rise .9s cubic-bezier(.2,.7,.2,1) both}
.fade{animation:fade .8s ease both}
.dot{animation:pulse 2s ease-in-out infinite}
.arrow{animation:nudge 1.6s ease-in-out infinite}
@keyframes pop{from{opacity:0;transform:scale(.2)}to{opacity:1;transform:none}}
.pop{transform-box:fill-box;transform-origin:center;animation:pop .45s cubic-bezier(.2,.9,.3,1.3) both}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""


def hero():
    d = json.loads((ROOT / "data" / "ascii.json").read_text())
    rows, cols = d["rows"], d["cols"]
    W, H = 1000, 440
    # portrait box (right side)
    px, py, pw, ph = PX, 30, 400, 380
    rh = ph / len(rows)
    fs = pw / (cols * 0.6)   # Geist Mono advance = 0.6em, so the row spans exactly pw (no textLength needed)

    ascii_svg = ""
    for i, r in enumerate(rows):
        if not r.strip():
            continue
        delay = 0.9 + i * 0.05
        style = "" if STATIC else f' class="fade" style="animation-delay:{delay:.2f}s"'
        ascii_svg += (f'<text{style} x="{px}" y="{py + (i + 1) * rh:.2f}" '
                      f'xml:space="preserve">'
                      f'{escape(r.ljust(cols))}</text>')

    def rise(delay):
        return "" if STATIC else f' class="rise" style="animation-delay:{delay}s"'

    shine = "" if STATIC else (
        '<animateTransform attributeName="gradientTransform" type="translate" '
        'values="-1.2 0;1.2 0;1.2 0" keyTimes="0;0.3;1" dur="6s" begin="1.6s" repeatCount="indefinite"/>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{NAME[0]} {NAME[1]} - {LABEL.title()}">
<defs>
<style>{font_css()}{BASE_CSS}</style>
<linearGradient id="shine" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">
<stop offset="0" stop-color="{C['ink']}"/><stop offset=".42" stop-color="{C['ink']}"/>
<stop offset=".5" stop-color="{C['accent']}"/><stop offset=".58" stop-color="{C['ink']}"/>
<stop offset="1" stop-color="{C['ink']}"/>{shine}</linearGradient>
</defs>
<rect width="{W}" height="{H}" rx="14" fill="{C['card']}"/>
<g{'' if STATIC else ' class="fade"'}>
<circle class="dot" cx="{TX+4}" cy="58" r="4" fill="{C['accent']}" stroke="{C['ink']}" stroke-width="1"/>
<text class="mono" x="{TX+18}" y="62" font-size="11" letter-spacing="1.4" fill="{C['mute']}">{LABEL}</text>
</g>
<g class="serif" fill="{C['ink']}">
<text{rise(0.15)} x="{TX}" y="190" font-size="118" letter-spacing="-3">{NAME[0]}</text>
<text{rise(0.35)} x="{TX}" y="298" font-size="118" font-style="italic" letter-spacing="-3" fill="url(#shine)">{NAME[1]}</text>
</g>
<g class="serif" fill="{C['ink']}" font-size="22">
<text{rise(0.6)} x="{TX+4}" y="352">{TAGLINE[0]}</text>
<text{rise(0.7)} x="{TX+4}" y="380">{TAGLINE[1]}</text>
</g>
<g{'' if STATIC else ' class="fade" style="animation-delay:.9s"'}>
<text class="mono" x="{TX+4}" y="412" font-size="12" letter-spacing="1.6" fill="{C['ink']}">{LINK} <tspan class="arrow" fill="{C['mute']}">&#8599;</tspan></text>
</g>
<g class="mono" font-size="{fs:.2f}" fill="{C['ink']}" fill-opacity=".82">{ascii_svg}</g>
</svg>"""


# ---------------------------------------------------------------- tiles
# Edit this list to change the tiles. "count" is the animated number, "word" follows it.
USER = "toufeeqahmed916"
TILES = [
    dict(file="ai.svg", label="AI", bg=C["accent"], fg=C["ink"], count=2, word="AI apps",
         desc=("Haven and an AI image", "generator using Replicate."),
         href=f"https://github.com/{USER}/Haven"),
    dict(file="web.svg", label="WEB", bg=C["web"], fg=C["ink"], count=4, word="web apps",
         desc=("Karwann, System X, a weather", "app and a bubble game."),
         href=f"https://github.com/{USER}/Karwann"),
    dict(file="projects.svg", label="PROJECTS", bg=C["designer"], fg="#FFFFFF", count=6, word="projects",
         desc=("All public on GitHub,", "and more on the way."),
         href=f"https://github.com/{USER}?tab=repositories"),
]


def tile(t, index):
    W, H = 330, 220
    fg = t["fg"]
    n = t["count"]
    base = 0.5 + index * 0.15          # stagger: tiles enter one after another
    step = 0.12                         # seconds per number in the count-up
    t0 = base + 0.5

    def head(txt, extra):
        return (f'<text class="serif" x="26" y="118" font-size="52" letter-spacing="-1" fill="{fg}"{extra}>'
                f'{txt} <tspan font-style="italic">{escape(t["word"])}</tspan></text>')

    if STATIC:
        headline = head(n, "")
    else:
        headline = ""
        for k in range(n + 1):
            last = k == n
            begin = t0 + k * step
            dur = "" if last else f' dur="{step:.2f}s"'
            fill = ' fill="freeze"' if last else ""
            headline += (head(k, ' visibility="hidden"').replace(
                "</text>",
                f'<set attributeName="visibility" to="visible" begin="{begin:.2f}s"{dur}{fill}/></text>'))

    grp = "" if STATIC else f' class="rise" style="animation-delay:{base:.2f}s"'
    shine = "" if STATIC else (
        f'<rect x="-120" y="0" width="70" height="{H}" fill="#fff" fill-opacity=".28" transform="skewX(-18)">'
        f'<animate attributeName="x" values="-120;420;420" keyTimes="0;.35;1" dur="7s" '
        f'begin="{t0 + n * step + 0.6:.2f}s" repeatCount="indefinite"/></rect>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(t['label'])}: {n} {escape(t['word'])}">
<defs><style>{font_css()}{BASE_CSS}</style><clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath></defs>
<g{grp}>
<rect width="{W}" height="{H}" rx="14" fill="{t['bg']}"/>
<g clip-path="url(#c)">{shine}</g>
<text class="mono" x="26" y="38" font-size="11" letter-spacing="1.6" fill="{fg}" fill-opacity=".75">{escape(t['label'])}</text>
<text class="mono arrow" x="{W - 40}" y="40" font-size="16" fill="{fg}">&#8599;</text>
{headline}
<g class="serif" font-size="17" fill="{fg}" fill-opacity=".85">
<text x="26" y="160">{escape(t['desc'][0])}</text>
<text x="26" y="182">{escape(t['desc'][1])}</text>
</g>
</g>
</svg>"""


# ---------------------------------------------------------------- contribution graph
LEVELS = ["#E3E1DA", "#D9F99D", "#BEF264", "#A3E635", "#65A30D"]   # empty -> busiest


def contrib():
    f = ROOT / "data" / "contributions.json"
    if not f.exists():
        return None
    d = json.loads(f.read_text())
    weeks = d["weeks"]
    nz = sorted(x["count"] for w in weeks for x in w if x["count"] > 0)
    q = [nz[int(len(nz) * p)] for p in (0.25, 0.5, 0.75)] if nz else [1, 2, 3]

    def level(c):
        return 0 if c == 0 else 1 if c <= q[0] else 2 if c <= q[1] else 3 if c <= q[2] else 4

    W, H = 1000, 250
    cell, gap = 14, 3
    x0, y0 = 40, 100
    cells = months = ""
    last_month = None
    for wi, w in enumerate(weeks):
        x = x0 + wi * (cell + gap)
        m = w[0]["date"][5:7]
        if m != last_month and wi < len(weeks) - 2:
            months += (f'<text class="mono" x="{x}" y="{y0 - 10}" font-size="10" '
                       f'fill="{C["mute"]}">{MONTHS[int(m) - 1]}</text>')
        last_month = m
        for day in w:
            y = y0 + day["wd"] * (cell + gap)
            attr = "" if STATIC else f' class="pop" style="animation-delay:{0.6 + wi * 0.03:.2f}s"'
            cells += (f'<rect{attr} x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" '
                      f'fill="{LEVELS[level(day["count"])]}"><title>{day["date"]}: {day["count"]}</title></rect>')

    legend_x = W - 40 - 5 * (cell + 4) - 70
    legend = f'<text class="mono" x="{legend_x}" y="{H - 14}" font-size="10" fill="{C["mute"]}">less</text>'
    for i, col in enumerate(LEVELS):
        legend += f'<rect x="{legend_x + 32 + i * (cell + 4)}" y="{H - 25}" width="{cell}" height="{cell}" rx="3" fill="{col}"/>'
    legend += f'<text class="mono" x="{legend_x + 32 + 5 * (cell + 4) + 4}" y="{H - 14}" font-size="10" fill="{C["mute"]}">more</text>'

    fade = "" if STATIC else ' class="fade"'
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="GitHub contribution graph, {d['total']} contributions in the last year">
<defs><style>{font_css()}{BASE_CSS}</style></defs>
<rect width="{W}" height="{H}" rx="14" fill="{C['card']}"/>
<g{fade}>
<text class="serif" x="40" y="58" font-size="34" fill="{C['ink']}">Every day, <tspan font-style="italic" fill="#65A30D">in lime</tspan></text>
<text class="mono" x="{W - 40}" y="52" font-size="10" letter-spacing="1.4" text-anchor="end" fill="{C['mute']}">{d['total']:,} CONTRIBUTIONS &#183; REFRESHED DAILY</text>
</g>
{months}{cells}{legend}
</svg>"""

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


if __name__ == "__main__":
    CARDS.mkdir(exist_ok=True)
    (CARDS / "hero.svg").write_text(hero(), encoding="utf-8")
    for i, t in enumerate(TILES):
        (CARDS / t["file"]).write_text(tile(t, i), encoding="utf-8")
    g = contrib()
    if g:
        (CARDS / "graph.svg").write_text(g, encoding="utf-8")
    else:
        print("note: data/contributions.json not found, skipped graph.svg (run fetch_contributions.py)")
    print("ok: hero + tiles in cards/", "(static)" if STATIC else "(animated)")
