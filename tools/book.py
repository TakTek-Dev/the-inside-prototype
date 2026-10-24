"""index.html: the identity book, and assets/the-inside-identity.zip.

python -I tools/book.py   (after brand.py and build.py)
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # python -I drops the script dir

import os
import zipfile

import shell as sh
from shell import C, esc, gate, wordmark, tally_svg, MARKS

ROOT = sh.ROOT
G = MARKS['gate']

COLOURS = [  # token, name, hex, role
    ('--paper', 'Paper', '#F6F8F8', 'The page. Cool, never cream.'),
    ('--sheet', 'Sheet', '#FFFFFF', 'Fields and chips that sit on the page.'),
    ('--wash', 'Wash', '#EAF0F1', 'Bands that hold what is not yet entered.'),
    ('--feint', 'Feint', '#D3E0E4', 'The faint ruling between entries.'),
    ('--rule', 'Rule', '#A9BEC6', 'Column rules and dividers.'),
    ('--ink2', 'Ink, second', '#4B585E', 'Sources, dates, captions.'),
    ('--ink', 'Ink', '#121518', 'Text, strokes, the gate.'),
    ('--red', 'Rule red', '#B3202A', 'The count, the closing stroke, a correction. Nothing else.'),
    ('--cloth', 'Binding', '#0E2424', 'Footer, election board, avatar.'),
    ('--onc', 'On binding', '#E6EEEC', 'Text on the binding.'),
    ('--red-on', 'Red on binding', '#F2705F', 'The rule where the ground is dark.'),
]


def lum(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4 for v in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + .05) / (lb + .05)


def construction():
    """The gate on its 64 grid with its dimensions written in."""
    s = ''.join(f'<path d="M{x} {G["top"]}V{G["foot"]}" stroke="var(--ink)" stroke-width="{G["w"]}" stroke-linecap="round"/>' for x in G['strokes'])
    grid = ''.join(f'<path d="M{i} 0V64M0 {i}H64" stroke="var(--feint)" stroke-width=".18"/>' for i in range(0, 65, 4))
    x0, y0, x1, y1 = G['rule']
    rd = f'M{x0} {y0}L{x1} {y1}'
    import math
    ang = math.degrees(math.atan2(y0 - y1, x1 - x0))
    axes = ''.join(f'<path d="M{x} 4V60" stroke="var(--red)" stroke-width=".22" stroke-dasharray="1 1"/>' for x in G['strokes'])
    t = 'font-family="Pathway" font-size="2.3" fill="var(--ink2)" font-weight="600"'
    return (f'<svg viewBox="-6 -4 76 72" class="cons" role="img" aria-label="Construction of the gate on a 64-unit grid">{grid}{axes}{s}'
            f'<path d="{rd}" stroke="var(--paper)" stroke-width="{G["w"] + G["halo"]}" stroke-linecap="round"/>'
            f'<path d="{rd}" stroke="var(--red)" stroke-width="{G["w"]}" stroke-linecap="round" opacity=".92"/>'
            f'<text x="{G["strokes"][1] + 5.5}" y="{G["top"] - 4}" {t} text-anchor="middle">↔ 11 u</text>'
            f'<text x="-1" y="{(G["top"] + G["foot"]) / 2}" {t} text-anchor="end">38 u</text>'
            f'<text x="60" y="{y1 - 3}" {t}>{ang:.1f}°</text>'
            f'<text x="32" y="63" {t} text-anchor="middle">stroke {G["w"]} u · paper cut {G["halo"]} u · round caps</text></svg>')


def main():
    C.R = ''
    sw = ''.join(
        f'<li><span class="chip-c" style="background:{h}{";box-shadow:inset 0 0 0 1px var(--rule)" if h in ("#FFFFFF", "#F6F8F8") else ""}"></span>'
        f'<b>{n}</b><code>{h}</code><span>{esc(r)}</span>'
        f'<span class="cr">{contrast(h, "#F6F8F8" if h not in ("#F6F8F8", "#FFFFFF", "#EAF0F1") else "#121518"):.1f}:1 '
        f'{"on paper" if h not in ("#F6F8F8", "#FFFFFF", "#EAF0F1") else "with ink"}</span></li>' for t, n, h, r in COLOURS)
    fig = sh.E['count']['n']
    body = f'''
<section class="bk-cover">
<div class="wrap">
<p class="lbl">Identity · TakTek design proposal · {sh.long_day(sh.TODAY)}</p>
<div class="bk-word">{wordmark()}</div>
<p class="bk-lede">News of Palestinian citizens of Israel, kept as a record. The identity is drawn from the oldest record there is: a tally, closed by a red rule.</p>
<div class="bk-go"><a class="btn solid" href="home.html">Open the front page {sh.icon("i-right")}</a><a class="btn" href="assets/the-inside-identity.zip" download>Download the marks (zip)</a></div>
</div>
</section>

<section class="bk-ch" id="idea"><div class="wrap bk-two">
<div><p class="lbl">01 · The idea</p><h2>Four strokes, closed by a fifth</h2></div>
<div class="prose">
<p>The client chose the ledger: a front page that starts from the count and enters every story against it. The identity takes that ledger at its word. Its mark is a tally gate, the way people have kept count for as long as they have kept anything: four strokes for four entries, and a fifth drawn across them to close the group.</p>
<p>The fifth stroke is red, and it does three jobs a bookkeeper would recognise. It closes a count. It underlines a total. And it is the only honest way to correct a ledger: one line through the old figure, so it stays legible, with the new figure beside it. The site promises the same thing in its masthead: <em>corrected, never erased</em>.</p>
<p>Laid flat, the same rule is the dash in the name. Five strokes are also a hand, and the hands carried at the marches against the killing in 2026 were painted red.</p>
</div></div></section>

<section class="bk-ch"><div class="wrap">
<div class="bk-two"><div><p class="lbl">02 · The mark</p><h2>Drawn on a 64 grid</h2></div>
<div class="prose"><p>Four strokes eleven units apart, thirty-eight tall, all with round ends. The rule rises at the angle of a quick hand and stands proud of the strokes on both sides. Where it crosses them, a thin cut of paper separates rule from stroke, so the gate stays clear at sixteen pixels and in one colour.</p></div></div>
<div class="bk-cons">{construction()}<div class="bk-sizes"><div>{gate()}<span>64</span></div><div style="font-size:32px">{gate()}<span>32</span></div><div style="font-size:20px">{gate()}<span>20</span></div><div style="font-size:14px">{gate()}<span>14</span></div><img src="favicon.svg" width="48" height="48" alt="The favicon: the gate on the binding colour"><img src="assets/brand/avatar.svg" width="96" height="96" alt="The avatar"></div></div>
</div></section>

<section class="bk-ch"><div class="wrap">
<div class="bk-two"><div><p class="lbl">03 · Three states</p><h2>The gate is also the site’s grammar</h2></div>
<div class="prose"><p>The mark is not only a logo; it tells the reader where a fact stands.</p></div></div>
<ol class="bk-states">
<li>{gate(False)}<h3>Open</h3><p>Reported, not yet entered. Shootings and deaths after the last published count sit here, in the wash band, until the watchdog counts them.</p></li>
<li>{gate()}<h3>Entered</h3><p>Counted and sourced. A story carries the count on the day it happened in its first column.</p></li>
<li><span class="bk-corr"><s>184</s> 186</span><h3>Corrected</h3><p>A figure that changed. The old one is struck once in red and stays readable, with the new one and its date beside it.</p></li>
</ol>
</div></section>

<section class="bk-ch"><div class="wrap">
<div class="bk-two"><div><p class="lbl">04 · The name</p><h2>Lockups</h2></div>
<div class="prose"><p>The name is set in Andada Pro at 760 and outlined, the gate standing a little taller than the capitals with its foot just under the baseline. The dash is the rule at the same weight as the strokes. Keep clear space of one stroke-gap (11 units) all round; below 160 px wide, use the gate alone.</p></div></div>
<div class="bk-locks">
<figure class="on-paper"><img src="assets/brand/wordmark.svg" alt="Horizontal lockup"><figcaption>Horizontal · masthead, letterhead</figcaption></figure>
<figure class="on-paper sq"><img src="assets/brand/stacked.svg" alt="Stacked lockup"><figcaption>Stacked · square places</figcaption></figure>
<figure class="on-cloth"><img src="assets/brand/wordmark-reverse.svg" alt="Reverse lockup on the binding colour"><figcaption>Reverse · on the binding</figcaption></figure>
</div>
<ul class="bk-dont">
<li><span>Don’t</span> recolour the strokes red: red is the rule alone.</li>
<li><span>Don’t</span> tilt the dash in the name; it lies flat.</li>
<li><span>Don’t</span> add strokes or remove the paper cut.</li>
<li><span>Don’t</span> set the name in another face, or put the gate behind a box on the page.</li>
</ul>
</div></section>

<section class="bk-ch"><div class="wrap">
<div class="bk-two"><div><p class="lbl">05 · Type</p><h2>A written voice and a numbering machine</h2></div>
<div class="prose"><p><b>Andada Pro</b> (Huerta Tipográfica, OFL) carries headlines and reading text. Its serifs are sturdy and its figures keep a pen’s swell, so a number in a sentence reads as written. <b>Pathway Extreme</b> (Eduardo Tunni, OFL) is the register: condensed and heavy, its figures are the figures of the machine that numbers ledger pages, and at text width it sets labels, dates and sources. Neither has been used by another TakTek prototype or by the three samples.</p></div></div>
<div class="bk-type">
<div class="tA"><p class="lbl">Andada Pro · 400–840</p><p class="big">A third of this year’s crime money was still unspent</p><p class="txt">The Central District Court gave her brother, 14½ at the time, 22 years; a cousin 17. Umm al-Fahm, Rahat, Baqa al-Gharbiya, Kafr Qasim. <i>Italic for the asides.</i> <span class="sm">Small caps for sources</span>.</p></div>
<div class="tB"><p class="lbl">Pathway Extreme · wdth 75–100</p><p class="num2">{fig}</p><p class="lbls">Police · Courts · Since the last count · 25 Sep 2026</p><p class="tab">152 · 157 · 181 · 2025: 128 139 187 · NIS 950m</p></div>
</div>
</div></section>

<section class="bk-ch"><div class="wrap">
<div class="bk-two"><div><p class="lbl">06 · Colour</p><h2>Paper, ink, feint and one red</h2></div>
<div class="prose"><p>The ground is cool white with the faint blue-grey ruling of account-book paper. Ink is near black. Red is the bookkeeper’s rule and appears only where something is counted, closed or corrected. The binding, a deep green-black, holds the footer, the election board and the avatar. Contrast is measured against paper or, for light tones, against ink.</p></div></div>
<ul class="bk-sw">{sw}</ul>
</div></section>

<section class="bk-ch"><div class="wrap">
<div class="bk-two"><div><p class="lbl">07 · The sheet</p><h2>Every section shares the ledger’s columns</h2></div>
<div class="prose"><p>No. · Date · Entry · Source. The first column holds the count on the day a story happened, or stays blank when none was published. A double red rule marks the margin where the entry begins, as on ruled ledger paper. Corners on photographs and controls are soft (8–16 px); rules and strokes have round ends.</p></div></div>
<div class="bk-sheet"><div class="cols colhead"><div class="lbl">No.</div><div class="lbl vr">Date</div><div class="lbl vr mg">Entry</div><div class="lbl vr c4">Source</div></div>
<div class="cols entry minor"><div class="e-no">181<small>count on the day</small></div><div class="e-date vr">25 Sep<span class="lbl">Government</span></div><div class="e-body vr mg"><div class="tx"><h3>A third of this year’s crime-fighting money for Arab towns was still unspent</h3></div></div><div class="e-src vr">PMO document via Arab48</div></div>
<div class="cols entry minor"><div class="e-no blank">—<small>no count</small></div><div class="e-date vr">2 Oct<span class="lbl">Election</span></div><div class="e-body vr mg"><div class="tx"><h3>Supreme Court lifts the election committee’s ban on Arab lists</h3></div></div><div class="e-src vr">Times of Israel</div></div>
</div>
<div class="bk-tally"><p class="lbl">The tally field · one stroke, one life</p><div class="tal">{"".join(tally_svg(5) for _ in range(9))}{tally_svg(3)}</div></div>
</div></section>

<section class="bk-ch"><div class="wrap">
<div class="bk-two"><div><p class="lbl">08 · Motion</p><h2>Things are entered, not animated</h2></div>
<div class="prose">
<p><b>Entering the day</b>, the loader, plays once a session: four strokes drop in 120 ms apart, the rule is drawn across them, the date is stamped, and the gate flies to its place in the masthead. A click or key skips it.</p>
<p><b>The numbering machine</b>: the count’s digits roll one full turn and stop on their figure, each wheel a beat after the last.</p>
<p><b>The correction</b>: earlier counts are struck through one after another before the current one settles. <b>The tally</b> writes itself in gate by gate as it scrolls into view. Pages cross-fade. With reduced motion all of it is still.</p>
<p><a href="home.html?loader">Watch the loader again {sh.icon("i-right")}</a></p>
</div></div>
</div></section>

<section class="bk-ch"><div class="wrap">
<div class="bk-two"><div><p class="lbl">09 · Photographs</p><h2>Natural colour, honest captions</h2></div>
<div class="prose"><p>Photographs are shown as taken, with soft corners and a caption that names the place, the date, the photographer and the licence. A photo appears only with a story it actually shows: a town, a building, a march. The register of names carries no photographs of the dead.</p></div></div>
</div></section>
'''
    css = f'<link rel="stylesheet" href="assets/css/book.css?v={sh.V}">'
    html = sh.page('Identity', 'The identity of The Inside – Palestine: a tally gate closed by a red rule.', body, current='', og=None)
    html = html.replace('</head>', css + '\n</head>', 1)
    sh.write('index.html', html)

    z = os.path.join(ROOT, 'assets', 'the-inside-identity.zip')
    with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(os.listdir(os.path.join(ROOT, 'assets', 'brand'))):
            zf.write(os.path.join(ROOT, 'assets', 'brand', f), 'the-inside/' + f)
        zf.write(os.path.join(ROOT, 'favicon.svg'), 'the-inside/favicon.svg')
        for f in ('OFL-AndadaPro.txt', 'OFL-PathwayExtreme.txt'):
            zf.write(os.path.join(ROOT, 'assets', 'fonts', f), 'the-inside/fonts/' + f)
    print('index.html + zip', os.path.getsize(z) // 1024, 'KB')


if __name__ == '__main__':
    main()
