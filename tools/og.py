"""tools/out/og.html: the 1200x630 sharing card (the count on the left, the lead photo on the right).

python -I tools/og.py
node --experimental-websocket tools/shot.mjs http://localhost:8189/tools/out/og.html assets/og.png 1200 630 view
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # python -I drops the script dir

import shell as sh
from shell import C, E, S, esc, day

CT = E['count']
lead = S[E['home']['lead']]
C.R = '../../'
html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>og</title>
<link rel="stylesheet" href="../../assets/css/ti.css?v={sh.V}">
<style>
html,body{{margin:0;width:1200px;height:630px;overflow:hidden;background:var(--paper)}}
.og{{display:grid;grid-template-columns:640px 560px;height:630px}}
.l{{padding:46px 48px 40px;display:flex;flex-direction:column;background:repeating-linear-gradient(to bottom,transparent 0 27px,var(--feint) 27px 28px)}}
.l .brand{{width:470px}}
.l .n{{margin-top:auto;font:850 250px/.78 var(--reg);font-stretch:75%;color:var(--red);letter-spacing:-.035em}}
.l p{{margin-top:22px;font:600 26px/1.22 var(--serif);max-width:24ch}}
.l .s{{margin-top:12px;font:500 15px/1.3 var(--reg);color:var(--ink2)}}
.r{{position:relative}}
.r img{{width:100%;height:100%;object-fit:cover}}
.r b{{position:absolute;left:24px;right:24px;bottom:24px;font:700 25px/1.18 var(--serif);color:#fff;text-shadow:0 1px 18px rgba(0,0,0,.55)}}
</style></head><body><div class="og"><div class="l"><div class="brand">{sh.wordmark()}</div>
<div class="n">{CT["n"]}</div><p>{esc(CT["lede"])}</p><p class="s">As of {day(CT["asof"], year=True)} · The Abraham Initiatives</p></div>
<div class="r"><img src="../../assets/img/photo/{lead["photo"]}.webp" alt=""><b>{esc(lead["headline"])}</b></div></div></body></html>'''
sh.write('tools/out/og.html', html)
print('tools/out/og.html')
