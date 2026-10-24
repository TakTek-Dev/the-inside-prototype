"""Build home.html from tools/edition.json.

python -I tools/build.py

The front page is the count. Everything below it is entered against it: what has been reported
since the last count, the election in three days, the fortnight's entries, how the count climbed,
the people named, the life of the towns, and the files behind it all. ti.js only animates.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # python -I drops the script dir

import shell as sh
from shell import C, E, S, esc, day, gate, tally_svg, link, fig, thumb, photo, icon, SEC

CT = E['count']
EL = E['election']
H = E['home']


def num_row(sid):
    s = S[sid]
    if s.get('n'):
        return f'<div class="e-no">{esc(str(s["n"]))}<small>{esc(s.get("nlabel", "count on the day"))}</small></div>'
    return f'<div class="e-no blank">—<small>{esc(s.get("nlabel", "no count"))}</small></div>'


def src_cell(sid):
    s = S[sid]
    a = s['sources'][0]
    more = f' and {len(s["sources"]) - 1} more' if len(s['sources']) > 1 else ''
    st = (f'<p class="st">{gate()}Entered</p>' if s.get('n') else '')
    return f'<div class="e-src vr">{st}{esc(a["outlet"])}, {day(a["date"])}{more}.<br><a href="{link(sid)}">Read the entry {icon("i-right")}</a></div>'


def sec_lbl(sid):
    k = S[sid]['section']
    return f'<span class="lbl"><a href="{C.R}{k}.html">{esc(SEC[k][1])}</a></span>'


def entry(sid, cls=''):
    s = S[sid]
    t = thumb(s.get('photo'))
    return (f'<article class="entry cols {cls} rise">{num_row(sid)}'
            f'<div class="e-date vr">{day(s["date"])}{sec_lbl(sid)}</div>'
            f'<div class="e-body vr mg"><div class="tx"><h3><a href="{link(sid)}">{esc(s["headline"])}</a></h3><p>{esc(s["dek"])}</p></div>{t}</div>'
            f'{src_cell(sid)}</article>')


def lead_entry(sid):
    s = S[sid]
    facts = ''.join(f'<li><b>{esc(f["v"])}</b><span>{esc(f["label"])}</span></li>' for f in s.get('figures', [])[:3])
    return (f'<article class="entry lead cols rise">{num_row(sid)}'
            f'<div class="e-date vr">{day(s["date"])}{sec_lbl(sid)}</div>'
            f'<div class="e-body vr mg"><h3><a href="{link(sid)}">{esc(s["headline"])}</a></h3>'
            f'<div class="lead-grid"><div><p class="dek">{esc(s["dek"])}</p>{f"<ul class=facts>{facts}</ul>" if facts else ""}</div>'
            f'{fig(s.get("photo"), sizes="(max-width:1100px) 100vw, 46vw", eager=True)}</div></div>'
            f'{src_cell(sid)}</article>')


def count_block():
    trail = ''.join(
        f'<li class="{"now" if i == len(CT["trail"]) - 1 else "old"}"><span class="v">{esc(t["v"])}</span><span class="w">{day(t["date"])}</span></li>'
        for i, t in enumerate(CT['trail']))
    cmp_rows = ''.join(
        f'<tr{" class=turn" if r.get("turn") else ""}><td>{day(r["date"])}</td><td class="k">{esc(str(r["y26"]))}</td>'
        f'<td>{esc(str(r["y25"]))}</td><td>{esc(r["chg"])}</td></tr>' for r in CT['compare'])
    bk = ''.join(f'<div{" class=red" if b.get("red") else ""}><b>{esc(str(b["n"]))}</b><span>{esc(b["label"])}</span></div>' for b in CT['breakdown'])
    return f'''<section class="count" id="count" aria-labelledby="count-h">
<div class="wrap">
<div class="grid">
<div>
<p class="eyebrow lbl">{gate()}<b>The count · 2026</b><span>Folio {sh.folio()}</span></p>
<h1 class="num" id="count-h" data-n="{CT["n"]}">{CT["n"]}</h1>
<p class="lede">{esc(CT["lede"])}</p>
<p class="asof src">As of {day(CT["asof"], year=True)}. {esc(CT["source"])}</p>
<ol class="trail" aria-label="Earlier published counts, struck through as each was superseded">{trail}</ol>
</div>
<div class="cmp">
<table><caption class="lbl">{esc(CT["cmp_caption"])}</caption>
<thead><tr><th scope="col">Update</th><th scope="col">2026</th><th scope="col">2025</th><th scope="col">Change</th></tr></thead>
<tbody>{cmp_rows}</tbody></table>
<p class="note">{esc(CT["note"])}</p>
</div>
</div>
<div class="bk" aria-label="How they died, as the watchdog lists it">{bk}</div>
{field()}
</div>
</section>'''


def field():
    rows = ''
    mon = CT['monthly']
    for i, m in enumerate(mon):
        n = m['n']
        gates = ''.join(tally_svg(5) for _ in range(n // 5)) + (tally_svg(n % 5) if n % 5 else '')
        cls = 'now' if i == len(mon) - 1 else ('est' if m.get('est') else '')
        rows += (f'<div class="mrow {cls}"><span class="m">to {esc(m["m"])}</span><div class="tal">{gates}</div>'
                 f'<span class="t">{n}</span></div>')
    return f'''<div class="field draw">
<div class="months" role="img" aria-label="{esc(CT["field_label"])}">{rows}</div>
<div class="side"><p class="cap"><strong>One stroke, one life.</strong> {esc(CT["field_cap"])}</p>
<div class="key"><p>{tally_svg(5)}A closed gate: five people.</p><p><svg viewBox="0 0 28 26" aria-hidden="true" style="width:31px"><path d="M4 3V23M10 3V23" stroke="var(--red)" stroke-width="2.4" stroke-linecap="round"/></svg>The current month, still open.</p></div>
<p class="src" style="margin-top:16px">{esc(CT["monthly_note"])}</p></div>
</div>'''


def open_band():
    items = ''.join(
        f'<li><span class="lbl">{day(o["date"], wd=True)} · {esc(o["place"])}</span>'
        + (f'<a href="{link(o["sid"])}"><p>{esc(o["text"])}</p></a>' if o.get('sid') else f'<p>{esc(o["text"])}</p>') + '</li>'
        for o in E['open'][:3])
    return f'''<section class="open" aria-labelledby="open-h">
<div class="wrap">
<div><h2 id="open-h">{gate(False)}Since the last count</h2><p>{esc(E["open_note"])}</p></div>
<ol>{items}</ol>
</div>
</section>'''


def board():
    days = (sh.D(EL['date']) - sh.TODAY).days
    slates = ''
    for sl in EL['slates']:
        rows = ''.join(
            f'<div class="row"><div class="bar" aria-hidden="true"><i style="--s:{p["s"]}"></i><span class="thr"></span></div><span class="v">{p["s"]}</span>'
            f'<span class="p">{esc(p["poll"])}, {day(p["date"])}</span></div>' for p in sl.get('polls', [])[:3])
        slates += (f'<article class="slate"><h3>{esc(sl["name"])}</h3><p class="who">{esc(sl["who"])}</p>'
                   + (f'<div class="seats" aria-label="Seat projections">{rows}</div>' if rows else '')
                   + f'<p class="st">{esc(sl["status"])}</p></article>')
    facts = ''.join(f'<div><b>{esc(f["v"])}</b><span>{esc(f["label"])}</span></div>' for f in EL['facts'][:4])
    return f'''<section class="board seats-in" aria-labelledby="el-h">
<div class="wrap">
<div class="head">
<div><p class="lbl">The 2026 election · {sh.long_day(EL["date"])}</p><h2 id="el-h">{esc(EL["title"])}</h2></div>
<div class="days"><b>{days}</b><span>days<br>to the vote</span></div>
</div>
<div class="slates">{slates}</div>
<p class="src" style="margin-top:12px">Bars: projected seats, scale to twelve; the red mark is four seats, the size of the electoral threshold. {esc(EL["src"])}</p>
<div class="foot">{facts}</div>
<p style="margin-top:26px"><a class="btn" href="{C.R}elections.html">The election desk {icon("i-right")}</a></p>
</div>
</section>'''


def pace_svg():
    """2026 and 2025 year-to-date at each published update, drawn on one date axis."""
    pts = CT['pairs']
    W, Hh, L, Rr, T, Bm = 600, 290, 44, 70, 18, 34
    d0, d1 = sh.D('2026-03-01'), sh.D('2026-11-01')
    X = lambda d: L + (sh.D(d) - d0).days / (d1 - d0).days * (W - L - Rr)
    Y = lambda v: T + (1 - v / 220) * (Hh - T - Bm)
    grid = ''.join(f'<path d="M{L} {Y(v):.1f}H{W - Rr}" stroke="var(--feint)" stroke-width="1"/>'
                   f'<text x="{L - 8}" y="{Y(v) + 5:.1f}" text-anchor="end">{v}</text>' for v in (0, 50, 100, 150, 200))
    months = ''.join(f'<text x="{X(f"2026-{m:02d}-01"):.1f}" y="{Hh - 10}" text-anchor="middle">{sh.D(f"2026-{m:02d}-01").strftime("%b")}</text>'
                     for m in range(3, 12))
    line = lambda k: ' '.join(f'{X(p["d"]):.1f},{Y(p[k]):.1f}' for p in pts)
    dots = ''.join(f'<circle cx="{X(p["d"]):.1f}" cy="{Y(p["a"]):.1f}" r="4" fill="var(--red)"/>' for p in pts)
    last = pts[-1]
    return (f'<svg class="pace" viewBox="0 0 {W} {Hh}" role="img" aria-label="2026 ran ahead of 2025 until September, then fell behind: '
            f'{last["a"]} against {last["p"]} on {day(last["d"])}.">{grid}{months}'
            f'<polyline points="{line("p")}" fill="none" stroke="var(--rule2)" stroke-width="2.5" stroke-dasharray="6 5" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<polyline class="ln" points="{line("a")}" fill="none" stroke="var(--red)" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>{dots}'
            f'<text x="{X(last["d"]) + 10:.1f}" y="{Y(last["a"]) + 18:.1f}" class="v r">{last["a"]}</text>'
            f'<text x="{X(last["d"]) + 10:.1f}" y="{Y(last["p"]) - 6:.1f}" class="v">{last["p"]}</text></svg>')


def climb():
    hund = ''.join(
        f'<div class="hrow{" now" if h.get("now") else ""}"><span>{h["y"]}</span><div class="t"><i style="--w:{h["pct"]}%"></i></div><span class="w">{esc(h["w"])}</span></div>'
        for h in CT['hundred'])
    return f'''<section aria-label="How the count climbed">
<div class="wrap">
<div class="sec-h"><h2>How the count <em>climbed</em></h2><p>Two readings of the same record. Left: the count at each published update, against the same date in 2025. Right: the day of the year each count reached one hundred.</p></div>
<div class="climb">
<section class="bars-in"><h3>{esc(CT["climb_h"])}</h3><p>{esc(CT["climb_p"])}</p>
{pace_svg()}
<div class="key2"><span><i class="n"></i>2026</span><span><i class="p"></i>2025, same date</span></div></section>
<section class="bars-in"><h3>The hundredth death came sooner</h3><p>{esc(CT["hundred_p"])}</p>
<div class="hund">{hund}</div>
<div class="hmon" aria-hidden="true"><span></span><div><span>1 Jan</span><span>1 Jul</span><span>31 Dec</span></div><span></span></div></section>
</div>
</div>
</section>'''


def register():
    evs = ''
    for g in E['named'][:3]:
        lis = ''.join(f'<li><b>{esc(p["name"])}</b><span>{esc(p["meta"])}</span></li>' for p in g['people'])
        evs += f'<div class="ev"><p class="lbl red">{esc(g["label"])}</p><p class="ctx">{esc(g["ctx"])}</p><ul>{lis}</ul><p class="src">{esc(g["src"])}</p></div>'
    return f'''<section aria-labelledby="reg-h">
<div class="wrap">
<div class="reg rise">
<div><h2 id="reg-h">{esc(E["named_h"])}</h2><p>People whose names were published in news reports, with age and town as reported, and what was reported about how they died. No photographs. A ledger that keeps only totals forgets who was in it.</p>
<p style="margin-top:16px"><a class="btn" href="{C.R}names.html">The register of names {icon("i-right")}</a></p></div>
<div class="evs">{evs}</div>
</div>
</div>
</section>'''


def life():
    cards = ''
    for sid in H['life'][:4]:
        s = S[sid]
        cards += (f'<article class="card rise">{photo(s.get("photo"), sizes="(max-width:720px) 100vw, 25vw", cls="ph")}'
                  f'<p class="lbl">{esc(SEC[s["section"]][1])} · {esc(s["place"])} · {day(s["date"])}</p>'
                  f'<h3><a href="{link(sid)}">{esc(s["headline"])}</a></h3><p>{esc(s["dek"])}</p></article>')
    return f'''<section aria-labelledby="life-h">
<div class="wrap">
<div class="sec-h"><h2 id="life-h">Also in the record <em>this month</em></h2><a class="more" href="{C.R}life.html">Life in the towns {icon("i-right")}</a></div>
<div class="life">{cards}</div>
</div>
</section>'''


def street():
    st = H['street']
    return f'''<section id="street" aria-labelledby="street-h">
<div class="wrap">
<div class="street">
{fig(st["photo"], sizes="(max-width:720px) 100vw, 58vw")}
<div class="txt rise"><p class="lbl">{esc(st["lbl"])}</p>
<h2 id="street-h">{esc(st["h"])}</h2>
{''.join(f'<p>{esc(p)}</p>' for p in st["p"])}
<p class="src" style="margin-top:12px">{esc(st["src"])}</p>
{fig(st["photo2"], cls="ph r32", sizes="(max-width:720px) 100vw, 36vw") if st.get("photo2") else ""}
</div>
</div>
</div>
</section>'''


def files():
    arts = ''
    for f in E['files'][:3]:
        h = f'<a href="{link(f["sid"])}">{esc(f["h"])}</a>' if f.get('sid') else esc(f['h'])
        if f.get('href'):
            h = f'<a href="{C.R}{f["href"]}">{esc(f["h"])}</a>'
        arts += (f'<article class="rise"><p class="lbl">{esc(f["lbl"])}</p><h3{" class=fig" if f.get("fig") else ""}>{h}</h3>'
                 f'<p>{esc(f["p"])}</p><p class="src" style="margin-top:10px">{esc(f["src"])}</p></article>')
    return f'<section id="method" aria-label="Background and method"><div class="wrap"><div class="files">{arts}</div></div></section>'


def entries():
    rows = lead_entry(H['lead']) + ''.join(entry(sid, 'minor' if S[sid].get('minor') else '') for sid in H['entries'])
    return f'''<section id="entries" aria-labelledby="entries-h">
<div class="wrap">
<div class="sec-h"><h2 id="entries-h">Entries <em>this fortnight</em></h2><p>Each story is posted against the count on the day it happened. Where no count was published that day, the No. column stays blank.</p></div>
<div class="cols colhead" aria-hidden="true"><div class="lbl">No.</div><div class="lbl vr">Date</div><div class="lbl vr mg">Entry</div><div class="lbl vr c4">Source</div></div>
{rows}
<p style="padding-top:22px"><a class="btn" href="{C.R}archive.html">Every entry, by day {icon("i-right")}</a></p>
</div>
</section>'''


def main():
    C.R = ''
    body = count_block() + open_band() + entries() + board() + climb() + register() + life() + street() + files()
    html = sh.page(sh.SITE, E['description'], body, current='', with_loader=True)
    sh.write('home.html', html)
    print('home.html', len(html) // 1024, 'KB')


if __name__ == '__main__':
    main()
