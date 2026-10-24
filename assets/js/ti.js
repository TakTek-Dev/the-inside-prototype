/* The Inside – Palestine: the loader, the numbering machine, the corrections and the arrivals.
   Everything a reader needs is already in the HTML; this file only animates it. */
(() => {
  const root = document.documentElement;
  root.classList.add('js');
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const store = (k, v) => { try { return v === undefined ? sessionStorage.getItem(k) : sessionStorage.setItem(k, v); } catch { return null; } };

  /* ---- entering the day: four strokes, the red rule, then the gate flies to the masthead ---- */
  function loader(done) {
    const forced = /[?&]loader\b/.test(location.search);
    const el = document.querySelector('.ldr');
    if (!el) return done();
    if (still || (!forced && store('ti-entered'))) { el.remove(); return done(); }
    store('ti-entered', '1');
    let finished = false;
    const finish = () => {
      if (finished) return;
      finished = true;
      const svg = el.querySelector('svg');
      const target = document.querySelector('.mast .brand .gate-g');
      if (svg && target) {
        const a = svg.getBoundingClientRect(), b = target.getBoundingClientRect();
        const k = b.height / a.height;
        el.classList.add('fly');
        svg.style.transform = `translate(${b.left + b.width / 2 - (a.left + a.width / 2)}px, ${b.top + b.height / 2 - (a.top + a.height / 2)}px) scale(${k})`;
      }
      setTimeout(() => { el.classList.add('out'); done(); }, 420);
      setTimeout(() => el.remove(), 900);
    };
    setTimeout(finish, 1650);
    el.addEventListener('click', finish);
    addEventListener('keydown', finish, { once: true });
  }

  /* ---- the numbering machine: each digit wheel rolls up to the count ---- */
  function machine(el) {
    const value = el.dataset.n;
    if (!value || still) return;
    el.textContent = '';
    el.setAttribute('aria-label', value);
    [...value].forEach((ch, i) => {
      const d = document.createElement('span');
      d.className = 'd';
      d.setAttribute('aria-hidden', 'true');
      const strip = document.createElement('span');
      const target = +ch;
      const turns = 10 + target;                 // one full turn, then on to the digit
      for (let n = 0; n <= turns; n++) {
        const s = document.createElement('span');
        s.textContent = n % 10;
        strip.appendChild(s);
      }
      strip.style.transitionDelay = `${i * 120}ms`;
      strip.dataset.to = turns;
      d.appendChild(strip);
      el.appendChild(d);
    });
    return () => el.querySelectorAll('.d>span').forEach((s) => { s.style.transform = `translateY(${-s.dataset.to * 0.86}em)`; });
  }

  /* ---- corrections: earlier counts are struck through, one after the other ---- */
  function strike(list) {
    const olds = [...list.querySelectorAll('.old .v')];
    if (still) return () => {};
    olds.forEach((v) => v.style.setProperty('--k', 0));
    return () => olds.forEach((v, i) => setTimeout(() => {
      let t0;
      const step = (t) => { t0 ??= t; const p = Math.min(1, (t - t0) / 260); v.style.setProperty('--k', 1 - Math.pow(1 - p, 3)); if (p < 1) requestAnimationFrame(step); };
      requestAnimationFrame(step);
    }, 260 + i * 210));
  }

  /* ---- arrivals ---- */
  function arrivals() {
    const els = document.querySelectorAll('.rise,.draw,.bars-in,.seats-in');
    if (still || !('IntersectionObserver' in window)) { els.forEach((e) => e.classList.add('in')); return; }
    const io = new IntersectionObserver((es) => es.forEach((e) => {
      if (!e.isIntersecting) return;
      const t = e.target;
      io.unobserve(t);
      t.classList.add('in');
      if (t.classList.contains('draw')) tally(t);
    }), { rootMargin: '0px 0px -8% 0px', threshold: .08 });
    els.forEach((e) => io.observe(e));
  }

  /* the tally writes itself in: gate by gate, month by month */
  function tally(field) {
    const gates = [...field.querySelectorAll('.tal svg')];
    gates.forEach((g, i) => {
      g.style.opacity = 0;
      setTimeout(() => {
        g.style.transition = 'opacity .18s';
        g.style.opacity = 1;
        const r = g.querySelectorAll('.r,.h');
        r.forEach((p) => { const L = p.getTotalLength(); p.style.strokeDasharray = L; p.style.strokeDashoffset = L; p.getBoundingClientRect(); p.style.transition = 'stroke-dashoffset .2s ease-out .1s'; p.style.strokeDashoffset = 0; });
      }, Math.min(i * 22, 1600));
    });
  }

  /* ---- the letter: a prototype form that sends nothing ---- */
  document.querySelectorAll('form[data-proto]').forEach((f) => f.addEventListener('submit', (e) => {
    e.preventDefault();
    const m = f.querySelector('.msg');
    if (m) m.textContent = 'Design prototype: nothing was sent and no address was kept.';
  }));

  /* ---- search (search.html) over assets/data/search.json ---- */
  const sf = document.querySelector('[data-search]');
  if (sf) {
    const input = sf.querySelector('input');
    const out = document.querySelector('.results');
    const base = sf.dataset.search;
    let index = [];
    fetch(base + 'assets/data/search.json').then((r) => r.json()).then((d) => { index = d; run(); });
    const escp = (s) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    const hi = (s, q) => q ? escp(s).replace(new RegExp(`(${q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'ig'), '<mark>$1</mark>') : escp(s);
    function run() {
      const q = input.value.trim();
      const ql = q.toLowerCase();
      const hits = q ? index.filter((x) => (x.t + ' ' + x.d + ' ' + x.p + ' ' + x.s).toLowerCase().includes(ql)) : index.slice(0, 12);
      out.innerHTML = `<p class="count-line">${q ? `${hits.length} ${hits.length === 1 ? 'entry' : 'entries'} for “${escp(q)}”` : 'Latest entries'}</p>` +
        hits.slice(0, 40).map((x) => `<article class="entry cols"><div class="e-no${x.n ? '' : ' blank'}">${x.n || '—'}<small>${x.n ? 'count on the day' : 'no count'}</small></div>` +
          `<div class="e-date vr">${escp(x.dt)}<span class="lbl">${escp(x.s)}</span></div>` +
          `<div class="e-body vr"><div class="tx"><h3><a href="${base}${x.u}">${hi(x.t, q)}</a></h3><p>${hi(x.d, q)}</p></div>` +
          (x.i ? `<div class="th"><img src="${base}${x.i}" alt="" loading="lazy" width="400" height="300"></div>` : '') + `</div></article>`).join('');
      const u = new URL(location.href);
      q ? u.searchParams.set('q', q) : u.searchParams.delete('q');
      history.replaceState(null, '', u);
    }
    input.value = new URLSearchParams(location.search).get('q') || '';
    input.addEventListener('input', run);
    sf.addEventListener('submit', (e) => { e.preventDefault(); run(); });
  }

  /* ---- start ---- */
  const num = document.querySelector('.num[data-n]');
  const roll = num && machine(num);
  const trail = document.querySelector('.trail');
  const cross = trail && strike(trail);
  loader(() => {
    requestAnimationFrame(() => { roll && roll(); cross && cross(); });
    arrivals();
  });
})();
