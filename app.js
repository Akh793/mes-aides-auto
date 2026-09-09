/* =====================================================================
   app.js — Moteur de calcul temps réel (aucune dépendance réseau) — v0.9 (mode particulier + mode pro)
   ===================================================================== */
(() => {
  'use strict';

  /* ---------- Index communes ----------
     Construit hors du chemin critique, EN TRANCHES : le parsing du fichier communes
     bloquait le premier rendu (FCP/LCP) ; construit d'un bloc après le rendu, il créait
     une tâche longue (TBT). On le découpe donc en lots courts exécutés quand le
     navigateur est inactif, en rendant la main entre chaque lot.
     Un appel à cpIndex() avant la fin termine le travail restant de façon synchrone,
     donc l'API reste identique et aucun appelant n'a besoin d'attendre.
     Format compact v2 : cp|insee|nom|commune_mere (vide si == insee)|epci
     — dept déduit de l'insee, region déduite du dept (table window.COMMUNES_REG). */
  const BY_CP = new Map();
  const cpIdx = { done: false, cur: 0, raw: null, reg: null, t: 0 };

  function cpIndexStep(budgetMs) {
    if (cpIdx.done) return true;
    if (cpIdx.raw === null) {
      cpIdx.t = performance.now();
      cpIdx.raw = window.COMMUNES_RAW || '';
      cpIdx.reg = Object.create(null);
      for (const pair of (window.COMMUNES_REG || '').split(',')) {
        const i = pair.indexOf(':');
        if (i > 0) cpIdx.reg[pair.slice(0, i)] = pair.slice(i + 1);
      }
    }
    const raw = cpIdx.raw, REG = cpIdx.reg, n = raw.length, t0 = performance.now();
    let cur = cpIdx.cur;
    while (cur < n) {
      for (let k = 0; k < 1500 && cur < n; k++) {
        let nl = raw.indexOf('\n', cur);
        if (nl < 0) nl = n;
        const line = raw.slice(cur, nl);
        cur = nl + 1;
        if (!line) continue;
        const f = line.split('|');
        const insee = f[1], p2 = insee.slice(0, 2);
        const dept = (p2 === '97' || p2 === '98') ? insee.slice(0, 3) : p2;
        let arr = BY_CP.get(f[0]);
        if (!arr) BY_CP.set(f[0], (arr = []));
        arr.push({ cp: f[0], insee: insee, nom: f[2], communeMere: f[3] || insee,
                   epci: f[4], dept: dept, region: REG[dept] || '' });
      }
      if (cur < n && performance.now() - t0 >= budgetMs) { cpIdx.cur = cur; return false; }
    }
    cpIdx.cur = cur; cpIdx.done = true; cpIdx.raw = null;
    console.info(`[index] ${BY_CP.size} codes postaux indexés en ${(performance.now() - cpIdx.t).toFixed(1)} ms`);
    return true;
  }

  /* Accès synchrone : termine le reliquat si le pré-chauffage n'a pas fini. */
  function cpIndex() { if (!cpIdx.done) cpIndexStep(Infinity); return BY_CP; }

  (function scheduleCpIndex() {
    const run = (deadline) => {
      const budget = deadline && typeof deadline.timeRemaining === 'function'
        ? Math.max(6, deadline.timeRemaining() - 2) : 12;
      if (!cpIndexStep(budget)) scheduleCpIndex();
    };
    if (typeof requestIdleCallback === 'function') requestIdleCallback(run, { timeout: 1000 });
    else setTimeout(() => run(null), 60);
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
    // ---- mode professionnel (v0.9) — n'affecte pas le mode particulier ----
    mode: 'particulier',    // 'particulier' | 'pro'
    vehicleType: 'vul',     // 'vul' (utilitaire léger) | 'vp' (voiture de société)
    vulSize: 'small',       // 'small' (< 1,55 t) | 'medium' (1,55–2 t) | 'large' (> 2 t)
    smallCompany: true,     // moins de 250 salariés
    euAssembled: true,      // utilitaire assemblé en Europe (liste ADEME)
    legalForm: 'societe',   // 'societe' (personne morale) | 'nomPropre' (entreprise individuelle, micro-entreprise)
    qty: 1,                 // nombre de véhicules (mode pro)
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
      ready: s.mode === 'pro'
        ? (!!c && Number.isFinite(s.price) && s.price > 0)
        : (!!c && Number.isFinite(s.rfr) && s.rfr >= 0 && Number.isFinite(s.price) && s.price > 0),
    };
  }

  /* ---------- Évaluation ---------- */
  const euro = (n) => Math.round(n).toLocaleString('fr-FR') + ' €';

  function evaluate(ctx) {
    const results = [];
    let localRulesMatched = 0;
    const RULES = ctx.mode === 'pro' ? AIDS_PRO : AIDS;
    for (const aid of RULES) {
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
    // Mode pro : aides « par véhicule » multipliées par la quantité, dans la limite des plafonds connus
    if (ctx.mode === 'pro' && ctx.qty > 1) {
      for (const r of results) {
        if (!r.aid.perVehicle || r.status === 'ineligible' || (r.min == null && r.max == null)) continue;
        const n = Math.min(ctx.qty, r.aid.maxVehicles || ctx.qty);
        if (r.min != null) r.min *= n;
        if (r.max != null) r.max *= n;
        let note = `Pour ${n} véhicule${n > 1 ? 's' : ''}`;
        if (n < ctx.qty) note += ` (plafond : ${r.aid.maxVehicles} véhicules aidés par entreprise)`;
        if (r.aid.maxTotal) { if (r.min != null) r.min = Math.min(r.min, r.aid.maxTotal); if (r.max != null) r.max = Math.min(r.max, r.aid.maxTotal); note += `, dans la limite de ${euro(r.aid.maxTotal)} par entreprise`; }
        r.notes.unshift(note + '.');
      }
    }
    // Plafond de cumul propre à certaines aides locales (% du prix TTC, toutes aides publiques)
    const kept = results.filter((r) => r.kept);
    const sumMin = (excl) => kept.filter((r) => r !== excl).reduce((a, r) => a + (r.min ?? 0), 0);
    const sumMax = (excl) => kept.filter((r) => r !== excl).reduce((a, r) => a + (r.max ?? r.min ?? 0), 0);
    for (const r of kept) {
      if (!r.aid.totalCapPct || r.min == null) continue;
      const cap = r.aid.totalCapPct * ctx.price * (ctx.mode === 'pro' ? Math.min(ctx.qty, r.aid.maxVehicles || ctx.qty) : 1);
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
    const noAid = ctx.mode === 'pro' ? [] : NO_AID_TERRITORIES.filter((t) => t.match(ctx));
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
    note:        { cls: 'bg-blue-50 text-[#2548FF]',       txt: 'Bon à savoir' },
  };
  const VERIF_UI = {
    active:            { cls: 'bg-emerald-50 text-emerald-700', txt: '✅ règle vérifiée' },
    active_unverified: { cls: 'bg-amber-50 text-amber-700',     txt: '⚠️ à confirmer' },
    suspended:         { cls: 'bg-rose-50 text-rose-700',       txt: '⏸ aide suspendue' },
    unknown:           { cls: 'bg-slate-100 text-slate-600',    txt: '❌ incertaine' },
  };

  function amountLabel(r) {
    if (r.status === 'note' && r.min == null && r.max == null) return '';
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
      const rm = ROADMAPS[k] || ROADMAPS_PRO[k];
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
    const seller = ctx.mode === 'pro'
      ? '<p class="text-sm text-slate-600 mb-3">Vous achetez <strong>au nom de votre entreprise</strong> : la prime d’État se demande au concessionnaire avant la commande ; les aides de votre collectivité se demandent à part, avant ou après l’achat selon le territoire. Les avantages fiscaux se traitent avec votre expert-comptable.</p>'
      : ctx.sellerPro
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

  function applyModeUI() {
    const pro = state.mode === 'pro';
    document.querySelectorAll('[data-mode]').forEach((el) => { el.hidden = el.dataset.mode !== state.mode; });
    $('cp-label').textContent = pro ? 'Code postal de l’entreprise' : 'Code postal';
    $('price-label').textContent = pro ? (state.vehicleType === 'vul' ? 'Prix par véhicule (HT)' : 'Prix par véhicule (TTC)') : 'Prix de la voiture (TTC)';
    $('price-hint').textContent = pro ? (state.vehicleType === 'vul' ? 'TVA récupérable sur un utilitaire' : 'TVA non récupérable sur une voiture') : '';
    $('sub-legal').hidden = !(pro && state.vehicleType === 'vp');
    $('price').placeholder = pro ? '35 000' : '32 000';
    $('sub-vul').hidden = !(pro && state.vehicleType === 'vul');
    $('sub-eu').hidden = !(pro && state.vehicleType === 'vul' && state.motor === 'ev' && state.isNew);
    $('bande-situation').classList.toggle('pro', pro);
    try { history.replaceState(null, '', pro ? '#pro' : location.pathname.split('/').pop() || 'index.html'); } catch (e) {}
  }

  function render() {
    const t0 = performance.now();
    saveState();
    const ctx = derive(state);
    applyModeUI();
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
    const SIZE_LBL = { small: 'petit utilitaire (moins de 1,55 t)', medium: 'utilitaire moyen (1,55 à 2 t)', large: 'grand utilitaire (plus de 2 t)' };
    if (ctx.mode === 'pro') $('ctx-recap').textContent = `Votre entreprise : ${ctx.smallCompany ? 'moins de 250 salariés' : '250 salariés ou plus'}${ctx.vehicleType === 'vp' ? (ctx.legalForm === 'nomPropre' ? ', en nom propre (entreprise individuelle)' : ', société') : ''}, située à ${ctx.commune.nom}. Votre projet : ${ctx.qty > 1 ? ctx.qty + ' × ' : ''}${ctx.vehicleType === 'vul' ? SIZE_LBL[ctx.vulSize] : 'voiture de société'} ${ctx.isNew ? 'neuf' : 'd’occasion'} ${ctx.motor === 'ev' ? '100 % électrique' : '(autre motorisation)'} à ${euro(ctx.price)} ${ctx.vehicleType === 'vul' ? 'hors taxes' : 'TTC'} par véhicule${ctx.vehicleType === 'vul' && ctx.motor === 'ev' && ctx.isNew ? (ctx.euAssembled ? ', assemblé en Europe' : ', assemblage en Europe inconnu') : ''}${ctx.scrap ? `, avec mise au rebut d’un ancien véhicule vignette Crit’Air ${ctx.critair === 5 ? '5 ou non classée' : ctx.critair}` : ''}. Les avantages fiscaux sont indiqués à part, sans entrer dans le chèque.`;
    else $('ctx-recap').textContent = `Vos revenus : revenu fiscal de référence de ${euro(ctx.rfr)} pour ${ctx.parts.toLocaleString('fr-FR')} part${ctx.parts > 1 ? 's' : ''}, soit ${euro(ctx.rfrPerPart)} par part — tranche ${ctx.decile} sur 10 (${tranchesTxt}). Votre projet : voiture ${ctx.isNew ? 'neuve' : 'd’occasion'} ${ctx.motor === 'ev' ? '100 % électrique' : '(autre motorisation)'} à ${euro(ctx.price)}, achetée ${ctx.sellerPro ? 'chez un concessionnaire' : 'à un particulier'}${ctx.scrap ? `, avec mise à la casse d’une ancienne voiture vignette Crit’Air ${ctx.critair === 5 ? '5 ou non classée' : ctx.critair}` : ''}${ctx.grosRouleur ? ', en tant que gros rouleur' : ''}.`;

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
    if (noLocalData) info += `<div class="rounded-2xl bg-blue-50 border border-blue-100 p-4 text-sm text-slate-700">ℹ️ Code postal <strong>${esc(ctx.commune.cp)}</strong> (${esc(ctx.commune.nom)}) : les aides nationales sont calculées. Aucune aide supplémentaire de votre ville, métropole, département ou région n’est actuellement répertoriée pour cette commune${ctx.mode === 'pro' ? ' pour les professionnels (territoires vérifiés : Lyon, Strasbourg, Toulouse, Aix-Marseille, Grand Paris, Grenoble, Rouen)' : ''}.</div>`;
    info += noAid.map((t) => `
      <div class="rounded-2xl bg-slate-50 border border-slate-200 p-4 text-sm">
        <div class="flex flex-wrap items-center gap-2"><span class="badge bg-slate-200 text-slate-600">Vérifié : aucune aide locale</span><span class="badge bg-blue-50 text-[#2548FF]">${esc(t.label)}</span></div>
        <p class="mt-2 text-slate-600">${esc(t.detail)}</p>
        <a class="mt-1 inline-block text-xs underline text-slate-400 hover:text-[#2548FF]" href="${t.sourceUrl}" target="_blank" rel="noopener">${esc(t.sourceLabel)}</a>
      </div>`).join('');
    $('noaid').innerHTML = info;

    const order = { eligible: 0, conditional: 1, note: 2, ineligible: 3 };
    // Mode pro : les cartes d'information qui ne s'appliquent pas au véhicule choisi ne sont pas affichées (bruit)
    const shown = ctx.mode === 'pro' ? results.filter((r) => !(r.aid.info && r.status === 'ineligible')) : results;
    const sorted = [...shown].sort((a, b) => (a.aid.info - b.aid.info) || (a.hypothetical - b.hypothetical) || (b.kept - a.kept) || (order[a.status] - order[b.status]));
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
        const c = (cpIndex().get(s.commune.cp) || []).find((x) => x.insee === s.commune.insee);
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
      const sig = `${state.mode}|${state.cp}|${total.max}`;
      if (sig === lastTracked) return;           // pas de doublon pour une saisie inchangée
      lastTracked = sig;
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ 'event': 'simulation_effectuee', 'code_postal': state.cp, 'montant_max': total.max, 'mode': state.mode });
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
      const list = cpIndex().get(v) || [];
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
    $('vulSize').value = state.vulSize || 'small';
    $('qty').textContent = String(state.qty || 1);
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
    seg._sync = sync;
    sync();
  });
  const resyncSegs = () => document.querySelectorAll('[data-seg]').forEach((s) => s._sync && s._sync());
  $('critair').addEventListener('change', (e) => { state.critair = +e.target.value; render(); });
  $('vulSize').addEventListener('change', (e) => { state.vulSize = e.target.value; render(); });
  $('qty-minus').addEventListener('click', () => { state.qty = Math.max(1, state.qty - 1); $('qty').textContent = state.qty; render(); });
  $('qty-plus').addEventListener('click', () => { state.qty = Math.min(20, state.qty + 1); $('qty').textContent = state.qty; render(); });
  if (location.hash === '#pro') { state.mode = 'pro'; resyncSegs(); }
  $('print-btn').addEventListener('click', () => window.print());
  $('reset-btn').addEventListener('click', () => { clearState(); location.reload(); });

  /* ---------- Init ---------- */
  const d = META.lastVerified.split('-').reverse().join('/');
  document.querySelectorAll('.meta-date').forEach((el) => (el.textContent = d));
  $('ended').innerHTML = ENDED.map((e) => `<li class="flex gap-2 text-sm"><span>${e.unknown ? '❌' : '⛔'}</span><span><strong>${esc(e.label)}</strong> — ${esc(e.detail)} <a class="underline text-slate-400" href="${e.sourceUrl}" target="_blank" rel="noopener">source</a></span></li>`).join('');
  $('sources').innerHTML = SOURCES.concat(window.SOURCES_PRO || []).map((s) => `
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
    const C = (cp, nom) => { const l = cpIndex().get(cp) || []; const c = l.find((x) => x.nom.startsWith(nom)); if (!c) throw new Error('commune test introuvable ' + cp + ' ' + nom); return c; };
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
    const basePro = { ...base, mode: 'pro', vehicleType: 'vul', vulSize: 'small', smallCompany: true, euAssembled: true, price: 35000 };
    cases.push(
      ['PRO Lyon petit utilitaire neuf assemblé UE, rebut → CEE 2 800–6 160 + Lyon 6 000–7 000', { ...basePro, commune: C('69003', 'Lyon 3e'), scrap: true }, (o) => o.min.pro_cee_vul === 2800 && o.max.pro_cee_vul === 6160 && o.min.pro_lyon === 6000 && o.max.pro_lyon === 7000 && o.kept.includes('pro_lyon')],
      ['PRO Lyon grande entreprise → Lyon inéligible', { ...basePro, commune: C('69003', 'Lyon 3e'), smallCompany: false }, (o) => o.status.pro_lyon === 'ineligible' && o.kept.includes('pro_cee_vul')],
      ['PRO assemblage UE inconnu → CEE conditionnelle sans montant', { ...basePro, commune: C('44000', 'Nantes'), euAssembled: false }, (o) => o.status.pro_cee_vul === 'conditional' && o.min.pro_cee_vul === null],
      ['PRO Nantes → aucune aide locale pro, badge', { ...basePro, commune: C('44000', 'Nantes') }, (o) => o.noLocalData === true && o.noAid.length === 0],
      ['PRO voiture de société → 570 €, pas de VUL, taxes annuelles info', { ...basePro, commune: C('44000', 'Nantes'), vehicleType: 'vp' }, (o) => o.min.pro_cee_vp === 570 && o.status.pro_cee_vul === 'ineligible' && o.status.pro_taxes_annuelles === 'note'],
      ['PRO grand utilitaire → suramortissement info, petit → non', { ...basePro, commune: C('44000', 'Nantes'), vulSize: 'large' }, (o) => o.status.pro_suramortissement === 'note' && o.max.pro_cee_vul === 9900],
      ['PRO Strasbourg VUL rebut, prix 20 000 → 4 000–6 000 puis cap 80 %', { ...basePro, commune: C('67000', 'Strasbourg'), scrap: true, price: 20000 }, (o) => o.kept.includes('pro_strasbourg') && o.max.pro_strasbourg <= 16000 - 6160],
      ['PRO Toulouse grand VUL occasion rebut CA3 → 4 200 (6 000 × 0,7)', { ...basePro, commune: C('31000', 'Toulouse'), vulSize: 'large', isNew: false, scrap: true, critair: 3 }, (o) => o.min.pro_toulouse === 4200 && o.status.pro_cee_vul === 'ineligible'],
      ['PRO Marseille PME rebut → AMP ≤ 5 000 conditionnel', { ...basePro, commune: C('13001', 'Marseille 1er'), scrap: true }, (o) => o.status.pro_amp === 'conditional' && o.max.pro_amp === 5000],
      ['PRO Paris → carte Grand Paris non confirmé, hors total', { ...basePro, commune: C('75011', 'Paris 11e') }, (o) => o.status.pro_mgp === 'note' && !o.kept.includes('pro_mgp') && o.noLocalData === false],
      ['PRO Grenoble → suspendu', { ...basePro, commune: C('38000', 'Grenoble') }, (o) => o.status.pro_grenoble === 'ineligible'],
      ['PRO 4 utilitaires Lyon → CEE ×4, Lyon ×4 (≤ 6)', { ...basePro, commune: C('69003', 'Lyon 3e'), scrap: true, qty: 4 }, (o) => o.min.pro_cee_vul === 11200 && o.max.pro_lyon === 28000],
      ['PRO 5 utilitaires Toulouse → 3 véhicules max et 20 000 € max', { ...basePro, commune: C('31000', 'Toulouse'), vulSize: 'large', scrap: true, critair: 3, qty: 5 }, (o) => o.max.pro_toulouse === 18000],
      ['PRO voiture en nom propre → prime particulier 3 620–6 180', { ...basePro, commune: C('44000', 'Nantes'), vehicleType: 'vp', legalForm: 'nomPropre' }, (o) => o.min.pro_cee_vp === 3620 && o.max.pro_cee_vp === 6180],
      ['PRO TVA utilitaire 35 000 → 7 000 € info ; voiture → TVA non récupérable', { ...basePro, commune: C('44000', 'Nantes') }, (o) => o.min.pro_tva === 7000 && o.status.pro_amortissement === 'ineligible'],
      ['PRO voiture 40 000 → amortissement plafonné (info), AEN info, Advenir non', { ...basePro, commune: C('44000', 'Nantes'), vehicleType: 'vp', price: 40000 }, (o) => o.status.pro_amortissement === 'note' && o.status.pro_aen === 'note' && o.status.pro_advenir === 'note' && o.status.pro_tva === 'ineligible'],
      ['PARTICULIER inchangé après ajout du mode pro (Lyon)', { ...base, commune: C('69003', 'Lyon 3e'), rfr: 15000, scrap: true }, (o) => o.kept.includes('cee_vp_neuf') && o.kept.includes('lyon_metropole') && !('pro_lyon' in o.status)],
    );
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
