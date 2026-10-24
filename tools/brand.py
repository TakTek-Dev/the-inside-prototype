"""The Inside – Palestine marks.

python -I tools/brand.py   -> assets/brand/*.svg + favicon.svg + tools/out/marks.json

The mark is the oldest record there is: a tally gate. Four strokes are four entries; the fifth,
drawn across them in red, closes the group. In a ledger that same red line is the only way to
correct an entry without erasing it, and it is the line under a total. In the name it lies flat
and becomes the dash: The Inside – Palestine. Five strokes are also a hand, the red hands
carried at the marches against the killing in 2026.

The gate has three states the site uses: open (four strokes, no rule) is reported but not yet
entered; closed is entered; a red rule through a figure is a correction, the old figure still
legible under it.
"""
import io
import json
import math
import os

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'research', 'font-src')
OUT = os.path.join(ROOT, 'assets', 'brand')
os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(ROOT, 'tools', 'out'), exist_ok=True)

INK, RED, PAPER = '#121518', '#B3202A', '#F6F8F8'
CLOTH, ONC, RED_ON = '#0E2424', '#E6EEEC', '#F2705F'

# the gate on a 64 grid: four strokes 11 apart, the rule rising at the angle of a quick hand
STROKES = [15.5, 26.5, 37.5, 48.5]
TOP, FOOT, W = 13.0, 51.0, 6.4
RULE = (7.0, 44.5, 57.0, 20.0)
HALO = 3.4                              # paper cut around the rule where it crosses the strokes


def f(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')


def gate(ink=INK, red=RED, paper=PAPER, closed=True, k=1.0, x=0.0, y=0.0, halo=True):
    """The gate as SVG, scaled k and placed at x, y (top left of its 64 box)."""
    t = lambda v, o: f(o + v * k)
    s = ''.join(f'<path d="M{t(sx, x)} {t(TOP, y)}V{t(FOOT, y)}"/>' for sx in STROKES)
    out = f'<g fill="none" stroke="{ink}" stroke-width="{f(W * k)}" stroke-linecap="round">{s}</g>'
    if closed:
        d = f'M{t(RULE[0], x)} {t(RULE[1], y)}L{t(RULE[2], x)} {t(RULE[3], y)}'
        if halo and paper:
            out += f'<path d="{d}" stroke="{paper}" stroke-width="{f((W + HALO) * k)}" stroke-linecap="round" fill="none"/>'
        out += f'<path d="{d}" stroke="{red}" stroke-width="{f(W * k)}" stroke-linecap="round" fill="none"/>'
    return out


def instance(name, limits):
    font = instancer.instantiateVariableFont(TTFont(os.path.join(SRC, name)), limits)
    buf = io.BytesIO()
    font.save(buf)
    buf.seek(0)
    return TTFont(buf)


def kerning(font):
    """Pair adjustments from the GPOS kern feature (format 1 and 2 pair lookups)."""
    pairs = {}
    gpos = font['GPOS'].table
    idx = set()
    for fr in gpos.FeatureList.FeatureRecord:
        if fr.FeatureTag == 'kern':
            idx.update(fr.Feature.LookupListIndex)
    for i in idx:
        lk = gpos.LookupList.Lookup[i]
        for st in lk.SubTable:
            if lk.LookupType == 9:
                st = st.ExtSubTable
            if getattr(st, 'LookupType', 2) != 2 and lk.LookupType not in (2, 9):
                continue
            cov = st.Coverage.glyphs
            if st.Format == 1:
                for g1, ps in zip(cov, st.PairSet):
                    for r in ps.PairValueRecord:
                        v = getattr(r.Value1, 'XAdvance', 0) if r.Value1 else 0
                        if v:
                            pairs.setdefault((g1, r.SecondGlyph), v)
            elif st.Format == 2:
                c1, c2 = st.ClassDef1.classDefs, st.ClassDef2.classDefs
                for g1 in cov:
                    rec = st.Class1Record[c1.get(g1, 0)]
                    for g2 in font.getGlyphOrder():
                        r = rec.Class2Record[c2.get(g2, 0)]
                        v = getattr(r.Value1, 'XAdvance', 0) if r.Value1 else 0
                        if v and (g1, g2) not in pairs:
                            pairs[(g1, g2)] = v
    return pairs


def text_path(font, kern, text, x0, base, size, track=0.0):
    """Outline a line of text; returns (path, advance) in px."""
    gs, cmap = font.getGlyphSet(), font.getBestCmap()
    upm = font['head'].unitsPerEm
    s = size / upm
    pen = SVGPathPen(gs, ntos=lambda v: f(v))
    x, prev, parts = x0, None, []
    for ch in text:
        g = cmap[ord(ch)]
        if prev:
            x += (kern.get((prev, g), 0) + track * upm) * s
        p = SVGPathPen(gs, ntos=lambda v: f(v))
        gs[g].draw(TransformPen(p, (s, 0, 0, -s, x, base)))
        parts.append(p.getCommands())
        x += font['hmtx'][g][0] * s
        prev = g
    return ''.join(parts), x - x0


def svg(w, h, body, label='The Inside – Palestine', bg=None):
    b = f'<rect width="{f(w)}" height="{f(h)}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f(w)} {f(h)}" role="img" '
            f'aria-label="{label}">{b}{body}</svg>')


def write(name, text):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as fh:
        fh.write(text)


def main():
    roman = instance('AndadaPro[wght].ttf', {'wght': 760})
    kern = kerning(roman)
    upm = roman['head'].unitsPerEm
    cap = roman['OS/2'].sCapHeight / upm

    # horizontal lockup: gate · The Inside — Palestine, all on one baseline
    size, base = 56.0, 62.0
    gk = (size * cap * 1.26) / (FOOT - TOP + W)          # gate stands a touch taller than the caps
    gy = base - (FOOT + W / 2) * gk + 2.0                 # its foot sits just under the baseline
    gx = -(STROKES[0] - W / 2) * gk
    x = (STROKES[-1] + W / 2) * gk + gx + size * 0.42
    the, adv1 = text_path(roman, kern, 'The Inside', x, base, size, track=-0.012)
    dash_y = base - size * cap * 0.46
    d0 = x + adv1 + size * 0.24
    d1 = d0 + size * 0.50
    x2 = d1 + size * 0.24
    pal, adv2 = text_path(roman, kern, 'Palestine', x2, base, size, track=-0.012)
    width = x2 + adv2 + 2
    height = base + 14
    rw = W * gk
    rule = (d0 + rw / 2, dash_y, d1 - rw / 2, dash_y)

    def lockup(ink, red, paper):
        return (gate(ink, red, paper, k=gk, x=gx, y=gy) +
                f'<path d="{the}" fill="{ink}"/><path d="{pal}" fill="{ink}"/>'
                f'<path d="M{f(rule[0])} {f(rule[1])}H{f(rule[2])}" stroke="{red}" stroke-width="{f(rw)}" stroke-linecap="round"/>')

    write('wordmark.svg', svg(width, height, lockup(INK, RED, PAPER)))
    write('wordmark-reverse.svg', svg(width, height, lockup(ONC, RED_ON, CLOTH), bg=CLOTH))

    # stacked lockup for square places: The Inside over — Palestine, the gate above
    s2, b1 = 64.0, 150.0
    k2 = 1.6
    the2, a1 = text_path(roman, kern, 'The Inside', 0, b1, s2, track=-0.012)
    b2 = b1 + s2 * 1.02
    rule2_x0 = 6.0
    rule2_x1 = rule2_x0 + s2 * 0.46
    pal2, a2 = text_path(roman, kern, 'Palestine', rule2_x1 + s2 * 0.28, b2, s2, track=-0.012)
    rw2 = W * k2 * 0.82
    sw = max(a1, rule2_x1 + s2 * 0.28 + a2) + 4
    sh = b2 + 18

    def stacked(ink, red, paper):
        return (gate(ink, red, paper, k=k2, x=-(STROKES[0] - W / 2) * k2, y=0) +
                f'<path d="{the2}" fill="{ink}"/><path d="{pal2}" fill="{ink}"/>'
                f'<path d="M{f(rule2_x0 + rw2 / 2)} {f(b2 - s2 * cap * .46)}H{f(rule2_x1 - rw2 / 2)}" stroke="{red}" '
                f'stroke-width="{f(rw2)}" stroke-linecap="round"/>')

    write('stacked.svg', svg(sw, sh, stacked(INK, RED, PAPER)))
    write('stacked-reverse.svg', svg(sw, sh, stacked(ONC, RED_ON, CLOTH), bg=CLOTH))

    # the gate alone, and its open state
    write('mark.svg', svg(64, 64, gate()))
    write('mark-reverse.svg', svg(64, 64, gate(ONC, RED_ON, CLOTH), bg=CLOTH))
    write('mark-open.svg', svg(64, 64, gate(closed=False), label='Reported, not yet entered'))
    # favicon: the gate on the binding cloth, a soft square
    fav = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="{CLOTH}"/>'
           f'{gate(ONC, RED_ON, CLOTH, k=.86, x=4.48, y=4.2)}</svg>')
    with open(os.path.join(ROOT, 'favicon.svg'), 'w', encoding='utf-8') as fh:
        fh.write(fav)
    write('avatar.svg', svg(400, 400, gate(ONC, RED_ON, CLOTH, k=4.2, x=65.6, y=62), bg=CLOTH))

    marks = {
        'gate': {'strokes': STROKES, 'top': TOP, 'foot': FOOT, 'w': W, 'rule': RULE, 'halo': HALO},
        'wordmark': {'w': round(width, 2), 'h': round(height, 2), 'the': the, 'pal': pal,
                     'rule': [round(v, 2) for v in rule], 'rw': round(rw, 2), 'gk': round(gk, 4),
                     'gx': round(gx, 2), 'gy': round(gy, 2)},
    }
    json.dump(marks, open(os.path.join(ROOT, 'tools', 'out', 'marks.json'), 'w', encoding='utf-8'))
    print('wordmark', round(width), 'x', round(height), 'gate k', round(gk, 3), 'kern pairs', len(kern))


if __name__ == '__main__':
    main()
