/* =====================================================================
   app.js — Moteur de calcul temps réel (aucune dépendance réseau) — v0.7
   ===================================================================== */
(() => {
  'use strict';

  /* ---------- Index communes (construit une fois au chargement) ---------- */
  const BY_CP = new Map();
  (function buildIndex() {
    const t0 = performance.now();
    for (const line of window.COMMUNES_RAW.split('\n')) {
      const [cp, insee, nom, communeMere, epci, dept, region] = line.split('|');
      let arr = BY_CP.get(cp);
      if (!arr) BY_CP.set(cp, (arr = []));
      arr.push({ cp, insee, nom, communeMere, epci, dept, region });
    }
    console.info(`[index] ${BY_CP.size} codes postaux indexés en ${(performance.now() - t0).toFixed(1)} ms`);
  })();

  /* ---------- État ---------- */
  const state = {
    cp: '', commune: null,
    rfr: NaN, parts: 1, price: NaN,
    isNew: true,
    motor: 'ev',            // 'ev' | 'other'
    scrap: false, critair: 3,
    grosRouleur: false,     // → proUse, commuteKm > 10, kmYear ≥ 12 000
    sellerPro: true,
    // constantes (filtres retirés de l'UI, valeurs par défaut prudentes)
    financing: 'achat', leaseMonths: 36, euBattery: false, prevLeasing: false, nonImposable: false,
  };

  /* ---------- Dérivation ---------- */
  function derive(s) {
    const c = s.commune;
    const rfrPerPart = s.rfr / (s.parts || 1);
    let decile = 10;
    for (let i = 0; i < DECILES_2026.length; i++) if (rfrPerPart <= DECILES_2026[i]) { decile = i + 1; break; }
    return {
      ...s,
      proUse: s.grosRouleur, commuteKm: s.grosRouleur ? 15 : 0, kmYear: s.grosRouleur ? 12000 : 0,
      insee: c ? c.insee : null, communeMere: c ? c.communeMere : null,
      epci: c ? c.epci : null, dept: c ? c.dept : null, region: c ? c.region : null,
      rfrPerPart, decile,
      ready: !!c && Number.isFinite(s.rfr) && s.rfr >= 0 && Number.isFinite(s.price) && s.price > 0,
    };
  }

  /* ---------- Évaluation ---------- */
  const euro = (n) => Math.round(n).toLocaleString('fr-FR') + ' €';

  function evaluate(ctx) {
    const results = [];
    let localRulesMatched = 0;
    for (const aid of AIDS) {
      if (aid.status === 'ended') continue;
      if (aid.territory && !aid.territory(ctx)) continue;
      if (aid.territory) localRulesMatched++;
      let r, hypothetical = false;
      if (aid.id === 'leasing_social_2026' && ctx.financing !== 'location') {
        // Le filtre « location » n'est plus proposé : on évalue le leasing social comme ALTERNATIVE en LLD ≥ 3 ans
        r = aid.check({ ...ctx, financing: 'location', leaseMonths: 36 });
        hypothetical = r.status !== 'ineligible';
      } else r = aid.check(ctx);
      results.push({ aid, ...r, kept: false, alternativeTo: null, hypothetical });
    }
    // Exclusions mutuelles : on garde la meilleure valeur (borne haute, puis basse)
    const groups = {};
    for (const r of results) {
      if (r.aid.info || r.hypothetical || r.status === 'ineligible') continue;
      const g = r.aid.exclusiveGroup;
      if (!g) { r.kept = true; continue; }
      (groups[g] = groups[g] || []).push(r);
    }
    for (const g of Object.values(groups)) {
      g.sort((a, b) => (b.max ?? -1) - (a.max ?? -1) || (b.min ?? -1) - (a.min ?? -1));
      g[0].kept = true;
      for (let i = 1; i < g.length; i++) g[i].alternativeTo = g[0].aid.short;
    }
    // Plafond de cumul propre à certaines aides locales (% du prix TTC, toutes aides publiques)
    const kept = results.filter((r) => r.kept);
    const sumMin = (excl) => kept.filter((r) => r !== excl).reduce((a, r) => a + (r.min ?? 0), 0);
    const sumMax = (excl) => kept.filter((r) => r !== excl).reduce((a, r) => a + (r.max ?? r.min ?? 0), 0);
    for (const r of kept) {
      if (!r.aid.totalCapPct || r.min == null) continue;
      const cap = r.aid.totalCapPct * ctx.price;
      const newMax = Math.max(0, Math.min(r.max ?? r.min, cap - sumMax(r)));
      const newMin = Math.max(0, Math.min(r.min, cap - sumMin(r)));
      if (newMax < (r.max ?? r.min) || newMin < r.min) {
        r.notes.push(`Montant réduit : le total des aides publiques ne peut pas dépasser ${Math.round(r.aid.totalCapPct * 100)} % du prix de la voiture, soit ${euro(cap)}.`);
        r.min = Math.round(Math.min(newMin, newMax)); r.max = Math.round(newMax);
      }
    }
    let min = 0, max = 0, hasUnknown = false;
    for (const r of kept) {
      if (r.min == null && r.max == null) { hasUnknown = true; continue; }
      min += r.min ?? 0;
      max += r.max ?? r.min ?? 0;
    }
    const noAid = NO_AID_TERRITORIES.filter((t) => t.match(ctx));
    const noLocalData = localRulesMatched === 0 && noAid.length === 0;
    return { results, noAid, noLocalData, total: { min, max, hasUnknown } };
  }

  /* ---------- Rendu ---------- */
  const $ = (id) => document.getElementById(id);
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  const STATUS_UI = {
    eligible:    { cls: 'bg-emerald-100 text-emerald-800', txt: 'Vous y avez droit' },
    conditional: { cls: 'bg-amber-100 text-amber-800',     txt: 'Possible, sous conditions' },
    ineligible:  { cls: 'bg-slate-200 text-slate-600',     txt: 'Pas pour vous' },
  };
  const VERIF_UI = {
    active:            { cls: 'bg-emerald-50 text-emerald-700', txt: '✅ règle vérifiée' },
    active_unverified: { cls: 'bg-amber-50 text-amber-700',     txt: '⚠️ à confirmer' },
    suspended:         { cls: 'bg-rose-50 text-rose-700',       txt: '⏸ aide suspendue' },
    unknown:           { cls: 'bg-slate-100 text-slate-600',    txt: '❌ incertaine' },
  };

  function amountLabel(r) {
    if (r.min == null && r.max == null) return '<span class="text-slate-500 text-base font-medium">montant pas encore publié</span>';
    if (r.min == null) return `jusqu’à ${euro(r.max)}`;
    if (r.max == null || r.min === r.max) return euro(r.min);
    return `${euro(r.min)} – ${euro(r.max)}`;
  }

  function aidCard(r) {
    const st = STATUS_UI[r.status], vf = VERIF_UI[r.aid.status] || VERIF_UI.unknown;
    const dim = r.status === 'ineligible' || (!r.kept && !r.aid.info && !r.hypothetical);
    const list = (items, cls) => items.length ? `<ul class="mt-2 space-y-1 text-sm ${cls}">${items.map((x) => `<li class="flex gap-2"><span class="shrink-0">•</span><span>${esc(x)}</span></li>`).join('')}</ul>` : '';
    return `
    <article class="card rounded-3xl bg-white shadow-lg p-5 border border-slate-100 transition-all ${dim ? 'opacity-70' : ''} ${r.status === 'ineligible' ? 'print-hide' : ''}">
      <div class="flex flex-wrap items-center gap-2">
        <span class="badge ${st.cls}">${st.txt}</span>
        <span class="badge ${vf.cls}">${vf.txt}</span>
        ${r.aid.territoryLabel ? `<span class="badge bg-blue-50 text-[#2548FF]">${esc(r.aid.territoryLabel)}</span>` : ''}
        ${r.aid.info ? '<span class="badge bg-slate-100 text-slate-600">non comptée dans le total</span>' : ''}
        ${r.hypothetical ? '<span class="badge bg-[#FF6347]/10 text-[#FF6347]">autre option : en location longue durée (3 ans minimum) — non comptée dans le total</span>' : ''}
        ${r.alternativeTo ? `<span class="badge bg-[#FF6347]/10 text-[#FF6347]">ne se cumule pas avec : ${esc(r.alternativeTo)}</span>` : ''}
      </div>
      <div class="flex items-start justify-between gap-3 mt-2">
        <h3 class="font-poppins font-semibold text-base leading-snug text-slate-900">${esc(r.aid.label)}</h3>
        <div class="font-poppins font-bold text-xl ${r.status === 'ineligible' ? 'text-slate-400' : 'text-[#2548FF]'} whitespace-nowrap">${r.status === 'ineligible' ? '—' : amountLabel(r)}</div>
      </div>
      ${list(r.reasons, 'text-rose-700')}
      ${list(r.notes, 'text-slate-600')}
      ${r.aid.platform && r.status !== 'ineligible' ? `<p class="mt-2 text-sm text-slate-700"><span class="font-medium text-[#2548FF]">Où faire la demande :</span> ${esc(r.aid.platform)}</p>` : ''}
      <div class="mt-3 text-xs text-slate-400 flex flex-wrap gap-x-3">
        <a class="underline hover:text-[#2548FF]" href="${r.aid.sourceUrl}" target="_blank" rel="noopener">${esc(r.aid.sourceLabel)}</a>
        <span>vérifié le ${r.aid.lastVerified.split('-').reverse().join('/')}</span>
      </div>
    </article>`;
  }

  function roadmapHtml(results, ctx) {
    const keys = [...new Set(results.filter((r) => r.kept && r.aid.roadmap).map((r) => r.aid.roadmap))];
    if (!keys.length) return '<p class="text-slate-500 text-sm">Aucune démarche à faire : aucune aide ne correspond à votre situation.</p>';
    const li = (a) => a.map((x) => `<li class="flex gap-2"><span class="text-[#FF6347] shrink-0">•</span><span>${esc(x)}</span></li>`).join('');
    const block = (k, i) => {
      const rm = ROADMAPS[k];
      return `
      <article class="rounded-3xl bg-[#F8F9FA] p-5 border border-slate-100 break-inside-avoid">
        <div class="flex items-center gap-3">
          <span class="w-8 h-8 shrink-0 rounded-full bg-[#FF6347] text-white font-poppins font-bold grid place-items-center">${i + 1}</span>
          <h4 class="font-poppins font-semibold text-slate-900 leading-snug">${esc(rm.title)}</h4>
        </div>
        <p class="mt-2 text-sm font-medium text-[#2548FF]">Quand ? ${esc(rm.when)}</p>
        <div class="mt-3 grid gap-x-8 gap-y-3 md:grid-cols-2">
          <div>
            <p class="text-xs uppercase tracking-wide text-slate-400">Les étapes</p>
            <ol class="mt-1 space-y-1 text-sm text-slate-700 list-decimal pl-5">${rm.steps.map((x) => `<li>${esc(x)}</li>`).join('')}</ol>
          </div>
          <div>
            <p class="text-xs uppercase tracking-wide text-slate-400">Les documents à préparer</p>
            <ul class="mt-1 space-y-1 text-sm text-slate-700">${li(rm.docs)}</ul>
          </div>
        </div>
        ${rm.warnings.length ? `<div class="mt-3 rounded-2xl bg-[#FF6347]/10 p-3 text-sm text-[#b8321a]">${rm.warnings.map(esc).join('<br>')}</div>` : ''}
      </article>`;
    };
    const seller = ctx.sellerPro
      ? '<p class="text-sm text-slate-600 mb-3">Vous achetez chez un <strong>concessionnaire ou un professionnel</strong> : la prime d’État se demande au vendeur avant la commande ; les aides de votre collectivité se demandent ensuite, en ligne.</p>'
      : '<p class="text-sm text-rose-700 mb-3">Vous achetez à un <strong>particulier</strong> : il n’y a pas de prime d’État. Seules les aides de votre collectivité qui l’acceptent restent possibles, et c’est vous qui déposez le dossier après l’achat (acte de vente, carte grise, certificat de destruction si demandé).</p>';
    return seller + `<div class="space-y-4">${keys.map(block).join('')}</div>`;
  }

  let lastTotal = 0;
  function animateTotal(el, from, to) {
    const dur = 350, t0 = performance.now();
    const step = (t) => {
      const p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = euro(from + (to - from) * e);
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }

  function render() {
    const t0 = performance.now();
    saveState();
    const ctx = derive(state);
    $('sub-scrap').hidden = !state.scrap;

    const ready = ctx.ready;
    $('results').hidden = !ready; $('empty').hidden = ready;
    $('roadmap-wrap').hidden = !ready; $('roadmap-empty').hidden = ready;
    if (!ready) return;

    const { results, noAid, noLocalData, total } = evaluate(ctx);
    const kept = results.filter((r) => r.kept);

    // Récap situation (visible aussi à l'impression)
    $('ctx-commune').textContent = `${ctx.commune.nom} (${ctx.commune.cp})`;
    const tranchesTxt = ctx.decile <= 3 ? 'revenus très modestes' : ctx.decile <= 5 ? 'revenus modestes' : ctx.decile <= 8 ? 'revenus intermédiaires' : 'revenus élevés';
    $('ctx-recap').textContent = `Vos revenus : revenu fiscal de référence de ${euro(ctx.rfr)} pour ${ctx.parts.toLocaleString('fr-FR')} part${ctx.parts > 1 ? 's' : ''}, soit ${euro(ctx.rfrPerPart)} par part — tranche ${ctx.decile} sur 10 (${tranchesTxt}). Votre projet : voiture ${ctx.isNew ? 'neuve' : 'd’occasion'} ${ctx.motor === 'ev' ? '100 % électrique' : '(autre motorisation)'} à ${euro(ctx.price)}, achetée ${ctx.sellerPro ? 'chez un concessionnaire' : 'à un particulier'}${ctx.scrap ? `, avec mise à la casse d’une ancienne voiture vignette Crit’Air ${ctx.critair === 5 ? '5 ou non classée' : ctx.critair}` : ''}${ctx.grosRouleur ? ', en tant que gros rouleur' : ''}.`;

    const totalEl = $('total-amount');
    if (kept.length === 0) totalEl.textContent = '0 €';
    else if (total.min === total.max) animateTotal(totalEl, lastTotal, total.max);
    else totalEl.textContent = `${euro(total.min)} – ${euro(total.max)}`;
    lastTotal = total.max;
    $('total-sub').textContent = kept.length
      ? `${kept.length === 1 ? '1 aide' : kept.length + ' aides qui se cumulent'}${total.hasUnknown ? ', plus 1 aide dont le montant n’est pas encore publié' : ''}`
      : 'Aucune aide ne correspond à votre situation';

    // Transparence code postal
    let info = '';
    if (noLocalData) info += `<div class="rounded-2xl bg-blue-50 border border-blue-100 p-4 text-sm text-slate-700">ℹ️ Code postal <strong>${esc(ctx.commune.cp)}</strong> (${esc(ctx.commune.nom)}) : les aides nationales sont calculées. Aucune aide supplémentaire de votre ville, métropole, département ou région n’est actuellement répertoriée pour cette commune.</div>`;
    info += noAid.map((t) => `
      <div class="rounded-2xl bg-slate-50 border border-slate-200 p-4 text-sm">
        <div class="flex flex-wrap items-center gap-2"><span class="badge bg-slate-200 text-slate-600">Vérifié : aucune aide locale</span><span class="badge bg-blue-50 text-[#2548FF]">${esc(t.label)}</span></div>
        <p class="mt-2 text-slate-600">${esc(t.detail)}</p>
        <a class="mt-1 inline-block text-xs underline text-slate-400 hover:text-[#2548FF]" href="${t.sourceUrl}" target="_blank" rel="noopener">${esc(t.sourceLabel)}</a>
      </div>`).join('');
    $('noaid').innerHTML = info;

    const order = { eligible: 0, conditional: 1, ineligible: 2 };
    const sorted = [...results].sort((a, b) => (a.aid.info - b.aid.info) || (a.hypothetical - b.hypothetical) || (b.kept - a.kept) || (order[a.status] - order[b.status]));
    $('cards').innerHTML = sorted.map(aidCard).join('');
    $('roadmap').innerHTML = roadmapHtml(results, ctx);
    $('perf').textContent = `${(performance.now() - t0).toFixed(1)} ms`;
    trackSimulation(total);
  }

  /* ---------- Persistance locale (sur l'appareil uniquement) ---------- */
  const STORE_KEY = 'aides_auto_state';
  function saveState() {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(state)); } catch (e) { /* stockage indisponible : on continue sans */ }
  }
  function loadState() {
    try {
      const raw = localStorage.getItem(STORE_KEY); if (!raw) return false;
      const s = JSON.parse(raw); if (!s || typeof s !== 'object') return false;
      // on ne restaure que les clés connues, en revalidant la commune contre l'index courant
      for (const k of Object.keys(state)) if (k in s && k !== 'commune') state[k] = s[k];
      state.commune = null;
      if (s.commune && s.commune.cp && s.commune.insee) {
        const c = (BY_CP.get(s.commune.cp) || []).find((x) => x.insee === s.commune.insee);
        if (c) state.commune = c;
      }
      return true;
    } catch (e) { return false; }
  }
  function clearState() {
    try { localStorage.removeItem(STORE_KEY); } catch (e) {}
  }

  /* ---------- Mesure d'audience (Google Tag Manager) : un événement dataLayer par simulation,
     1 s après la fin de la saisie, uniquement si l'utilisateur a accepté (bandeau) ---------- */
  let trackTimer = null, lastTracked = '';
  function trackSimulation(total) {
    clearTimeout(trackTimer);
    trackTimer = setTimeout(() => {
      const consent = window.MAA_consent && window.MAA_consent.get() === 'granted';
      if (!consent) return;
      const sig = `${state.cp}|${total.max}`;
      if (sig === lastTracked) return;           // pas de doublon pour une saisie inchangée
      lastTracked = sig;
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ 'event': 'simulation_effectuee', 'code_postal': state.cp, 'montant_max': total.max });
    }, 1000);
  }

  /* ---------- Autocomplétion commune ---------- */
  const cpInput = $('cp'), dd = $('cp-dd');
  function showCommunes(list) {
    if (!list.length) { dd.hidden = true; return; }
    dd.innerHTML = list.map((c, i) => `<button type="button" data-i="${i}" class="w-full text-left px-4 py-2 hover:bg-blue-50 text-sm">${esc(c.nom)} <span class="text-slate-400">${c.cp}</span></button>`).join('');
    dd.hidden = false; dd._list = list;
  }
  cpInput.addEventListener('input', () => {
    const v = cpInput.value.replace(/\D/g, '').slice(0, 5);
    cpInput.value = v; state.cp = v; state.commune = null;
    if (v.length === 5) {
      const list = BY_CP.get(v) || [];
      if (list.length === 1) { state.commune = list[0]; dd.hidden = true; $('commune-name').textContent = list[0].nom; }
      else { $('commune-name').textContent = list.length ? 'Choisissez votre commune ↓' : 'Code postal inconnu'; showCommunes(list); }
    } else { dd.hidden = true; $('commune-name').textContent = ''; }
    render();
  });
  dd.addEventListener('click', (e) => {
    const b = e.target.closest('button'); if (!b) return;
    state.commune = dd._list[+b.dataset.i]; dd.hidden = true;
    $('commune-name').textContent = state.commune.nom; render();
  });
  document.addEventListener('click', (e) => { if (!dd.contains(e.target) && e.target !== cpInput) dd.hidden = true; });

  /* ---------- Restauration d'une saisie précédente ---------- */
  if (loadState()) {
    if (state.commune) { cpInput.value = state.commune.cp; $('commune-name').textContent = state.commune.nom; }
    else if (state.cp) cpInput.value = state.cp;
    if (Number.isFinite(state.rfr)) $('rfr').value = state.rfr;
    if (Number.isFinite(state.price)) $('price').value = state.price;
    $('parts').textContent = (state.parts || 1).toLocaleString('fr-FR');
    $('critair').value = String(state.critair || 3);
  }

  /* ---------- Liaison des champs ---------- */
  const num = (id, key) => $(id).addEventListener('input', (e) => { state[key] = parseFloat(e.target.value.replace(/\s/g, '')); render(); });
  num('rfr', 'rfr'); num('price', 'price');
  $('parts-minus').addEventListener('click', () => { state.parts = Math.max(1, state.parts - 0.5); $('parts').textContent = state.parts.toLocaleString('fr-FR'); render(); });
  $('parts-plus').addEventListener('click', () => { state.parts = Math.min(10, state.parts + 0.5); $('parts').textContent = state.parts.toLocaleString('fr-FR'); render(); });

  /* Segments à deux positions : data-seg="clé,valeurA,valeurB" */
  document.querySelectorAll('[data-seg]').forEach((seg) => {
    const [key, a, b] = seg.dataset.seg.split(',');
    const cast = (v) => (v === 'true' ? true : v === 'false' ? false : v);
    const opts = seg.querySelectorAll('span.opt');
    const sync = () => {
      const isA = state[key] === cast(a);
      seg.querySelector('.knob').style.transform = isA ? 'translateX(0)' : 'translateX(100%)';
      opts[0].classList.toggle('active', isA); opts[1].classList.toggle('active', !isA);
      seg.setAttribute('aria-checked', String(isA));
    };
    seg.addEventListener('click', () => { state[key] = state[key] === cast(a) ? cast(b) : cast(a); sync(); render(); });
    seg.addEventListener('keydown', (e) => { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); seg.click(); } });
    sync();
  });
  $('critair').addEventListener('change', (e) => { state.critair = +e.target.value; render(); });
  $('print-btn').addEventListener('click', () => window.print());
  $('reset-btn').addEventListener('click', () => { clearState(); location.reload(); });

  /* ---------- Init ---------- */
  const d = META.lastVerified.split('-').reverse().join('/');
  document.querySelectorAll('.meta-date').forEach((el) => (el.textContent = d));
  $('ended').innerHTML = ENDED.map((e) => `<li class="flex gap-2 text-sm"><span>${e.unknown ? '❌' : '⛔'}</span><span><strong>${esc(e.label)}</strong> — ${esc(e.detail)} <a class="underline text-slate-400" href="${e.sourceUrl}" target="_blank" rel="noopener">source</a></span></li>`).join('');
  $('sources').innerHTML = SOURCES.map((s) => `
    <article class="rounded-3xl bg-white border border-slate-100 p-5">
      <h4 class="font-poppins font-semibold text-slate-900">${esc(s.cat)}</h4>
      <p class="mt-1 text-sm text-slate-600">${esc(s.what)}</p>
      <p class="mt-2 text-xs text-slate-500"><span class="font-medium">Source :</span> <a class="underline hover:text-[#2548FF]" href="${s.url}" target="_blank" rel="noopener">${esc(s.src)}</a></p>
      ${s.note ? `<p class="mt-1 text-xs text-amber-700">${esc(s.note)}</p>` : ''}
    </article>`).join('');
  render();

  /* ---------- Tests console (window.runTests()) ---------- */
  window.runTests = function () {
    const base = { cp: '', commune: null, rfr: 20000, parts: 1, price: 30000, isNew: true, motor: 'ev', scrap: false, critair: 3, grosRouleur: false, sellerPro: true, financing: 'achat', leaseMonths: 36, euBattery: false, prevLeasing: false, nonImposable: false };
    const C = (cp, nom) => { const l = BY_CP.get(cp) || []; const c = l.find((x) => x.nom.startsWith(nom)); if (!c) throw new Error('commune test introuvable ' + cp + ' ' + nom); return c; };
    const cases = [
      ['Lyon 3e, modeste, neuf, rebut CA3', { ...base, commune: C('69003', 'Lyon 3e'), rfr: 15000, scrap: true }, (o) => o.kept.includes('cee_vp_neuf') && o.kept.includes('lyon_metropole')],
      ['Lyon sans rebut → Lyon inéligible', { ...base, commune: C('69003', 'Lyon 3e'), rfr: 15000 }, (o) => o.status.lyon_metropole === 'ineligible'],
      ['Paris 11e gros rouleur D7 + MGP', { ...base, commune: C('75011', 'Paris 11e'), rfr: 21000, grosRouleur: true, scrap: true }, (o) => o.min.cee_vp_neuf === 4700 && o.kept.includes('mgp_roule_propre')],
      ['Toulouse occasion particulier → rien CEE, Toulouse oui', { ...base, commune: C('31000', 'Toulouse'), isNew: false, sellerPro: false, scrap: true, rfr: 12000 }, (o) => !o.kept.includes('cee_vo_occasion') && o.status.occitanie_ecocheque === 'ineligible' && o.min.toulouse === 3000],
      ['Montpellier occasion 20 k€ → Occitanie conditionnel 1 600 + carte pas d’aide', { ...base, commune: C('34000', 'Montpellier'), isNew: false, price: 20000 }, (o) => o.noAid.includes('Montpellier Méditerranée Métropole') && o.status.occitanie_ecocheque === 'conditional' && o.min.occitanie_ecocheque === 1600],
      ['Leasing social = alternative hypothétique, hors total (D5 gros rouleur)', { ...base, commune: C('44000', 'Nantes'), rfr: 16000, grosRouleur: true, price: 25000 }, (o) => o.hyp.includes('leasing_social_2026') && !o.kept.includes('leasing_social_2026') && o.kept.includes('cee_vp_neuf') && o.min.leasing_social_2026 === 6500],
      ['Leasing social exclu si RFR/part > 16 880', { ...base, commune: C('44000', 'Nantes'), rfr: 17000, grosRouleur: true }, (o) => o.status.leasing_social_2026 === 'ineligible' && !o.hyp.includes('leasing_social_2026')],
      ['Nantes → badge « aucune surprime locale »', { ...base, commune: C('44000', 'Nantes') }, (o) => o.noLocalData === true],
      ['Lyon → pas de badge « aucune surprime locale »', { ...base, commune: C('69003', 'Lyon 3e') }, (o) => o.noLocalData === false],
      ['Prix > 47 000 → CEE neuf inéligible', { ...base, commune: C('44000', 'Nantes'), price: 50000 }, (o) => o.status.cee_vp_neuf === 'ineligible'],
      ['D10 → autres ménages 3 300–3 314', { ...base, commune: C('44000', 'Nantes'), rfr: 60000 }, (o) => o.min.cee_vp_neuf === 3300 && o.max.cee_vp_neuf === 3314],
      ['Motorisation autre + MGP → 3 000 max, CEE non', { ...base, commune: C('92100', 'Boulogne'), motor: 'other', scrap: true, rfr: 20000 }, (o) => o.max.mgp_roule_propre === 3000 && o.status.cee_vp_neuf === 'ineligible'],
      ['Strasbourg strate 2 cession CA2 → 3 000 €', { ...base, commune: C('67000', 'Strasbourg'), rfr: 12000, scrap: true, critair: 2 }, (o) => o.min.strasbourg === 3000],
      ['Rouen tranche A, cap 80 % sur 10 000 €', { ...base, commune: C('76000', 'Rouen'), rfr: 6000, price: 10000, scrap: true, critair: 3 }, (o) => o.kept.includes('rouen') && o.max.rouen <= 8000 - o.max.cee_vp_neuf],
      ['Le Havre → CD76 conditionnel', { ...base, commune: C('76600', 'Le Havre'), rfr: 15000, scrap: true, critair: 4 }, (o) => o.status.seine_maritime === 'conditional' && !('rouen' in o.status)],
      ['Marseille 1er neuf RFR 6 000 rebut CA4 → 5 000 €', { ...base, commune: C('13001', 'Marseille 1er'), rfr: 6000, scrap: true, critair: 4 }, (o) => o.min.amp_marseille === 5000],
      ['Aix-en-Provence → carte CD13, pas AMP', { ...base, commune: C('13100', 'Aix-en-Provence'), rfr: 6000, scrap: true, critair: 5 }, (o) => !('amp_marseille' in o.status) && o.noAid.includes('Département des Bouches-du-Rhône')],
      ['Annecy NC rebut RFR 10 000 → 3 000 €', { ...base, commune: C('74000', 'Annecy'), rfr: 10000, scrap: true, critair: 5 }, (o) => o.min.grand_annecy === 3000],
      ['Grenoble → suspendu, hors total', { ...base, commune: C('38000', 'Grenoble'), rfr: 10000, scrap: true }, (o) => o.status.grenoble === 'ineligible' && !o.kept.includes('grenoble')],
      ['Nice → carte « pas d’aide locale »', { ...base, commune: C('06000', 'Nice') }, (o) => o.noAid.includes('Métropole Nice Côte d’Azur') && o.noLocalData === false],
      ['Bordeaux rebut NC → conditionnel ≤ 6 000', { ...base, commune: C('33000', 'Bordeaux'), scrap: true, critair: 5 }, (o) => o.status.bordeaux === 'conditional' && o.max.bordeaux === 6000],
    ];
    let ok = 0;
    for (const [name, s, assert] of cases) {
      const { results, noAid, noLocalData } = evaluate(derive(s));
      const o = { kept: results.filter((r) => r.kept).map((r) => r.aid.id), hyp: results.filter((r) => r.hypothetical).map((r) => r.aid.id), noAid: noAid.map((t) => t.label), noLocalData, status: {}, min: {}, max: {} };
      for (const r of results) { o.status[r.aid.id] = r.status; o.min[r.aid.id] = r.min; o.max[r.aid.id] = r.max; }
      let pass = false; try { pass = assert(o); } catch (e) { console.error(e); }
      ok += pass;
      console[pass ? 'log' : 'error'](`${pass ? '✅' : '❌'} ${name}`, pass ? '' : JSON.stringify(o));
    }
    console.log(`${ok}/${cases.length} tests OK`);
    return ok === cases.length;
  };
})();
