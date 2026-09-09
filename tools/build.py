# -*- coding: utf-8 -*-
"""
Mes Aides Auto — générateur des pages éditoriales et territoriales.

Principe (imposé par l'architecture SEO du projet) :
  - la DONNÉE (barèmes, conditions, sources, dates) est lue depuis data.js / communes.js ;
  - l'ÉDITORIAL (angle, exemples, FAQ) vit dans content_national.py / content_territoires.py ;
  - ce fichier ne contient que le gabarit et l'assemblage.

Usage :  python3 tools/build.py     (depuis la racine du site)
Sortie :  <slug>/index.html pour chaque page + les sitemaps.
"""
import json, os, re, sys, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import labels

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
BASE = "https://mes-aides-auto.fr"
TODAY = "2026-09-08"
GTM_ID = "GTM-P2DNNBXT"

# --------------------------------------------------------------------------
# Blocs communs (consentement + GTM : copie conforme de index.html, pour que
# la mesure d'audience fonctionne à l'identique sur toutes les pages)
# --------------------------------------------------------------------------
FONTS_HEAD = """<link rel="preload" as="font" type="font/woff2" crossorigin href="/assets/fonts/inter-var.woff2">
<link rel="preload" as="font" type="font/woff2" crossorigin href="/assets/fonts/poppins-700.woff2">
<style>/* Polices auto-hebergees (sous-ensemble latin) : zero requete tierce, zero blocage du rendu */
@font-face{font-family:'Inter';font-style:normal;font-weight:400 600;font-display:swap;src:url(/assets/fonts/inter-var.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:'Poppins';font-style:normal;font-weight:500;font-display:swap;src:url(/assets/fonts/poppins-500.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:'Poppins';font-style:normal;font-weight:600;font-display:swap;src:url(/assets/fonts/poppins-600.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:'Poppins';font-style:normal;font-weight:700;font-display:swap;src:url(/assets/fonts/poppins-700.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:'Poppins';font-style:italic;font-weight:600;font-display:swap;src:url(/assets/fonts/poppins-600-italic.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:'Poppins';font-style:italic;font-weight:700;font-display:swap;src:url(/assets/fonts/poppins-700-italic.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
</style>"""

MAA_CSS_INLINE = "<style>/* assets/maa.css inline */\n" + open(
    __import__("pathlib").Path(__file__).resolve().parent.parent / "assets" / "maa.css", encoding="utf-8"
).read() + "</style>"

CONSENT_GTM = """<!-- Consentement (Consent Mode v2) — doit précéder GTM. Aucun cookie de mesure tant que l'utilisateur n'a pas accepté (bandeau). -->
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('consent', 'default', { analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', wait_for_update: 500 });
  (function () {
    var KEY = 'aides_auto_consent', TTL = 182 * 24 * 3600 * 1000, choice = null; // choix conservé 6 mois (recommandation CNIL)
    try { var raw = localStorage.getItem(KEY); if (raw) { var o = JSON.parse(raw); if (o && o.v && Date.now() - o.t < TTL) choice = o.v; else localStorage.removeItem(KEY); } } catch (e) {}
    function apply(v) {
      gtag('consent', 'update', { analytics_storage: v === 'granted' ? 'granted' : 'denied' });
      window.dataLayer.push({ event: v === 'granted' ? 'consent_granted' : 'consent_denied' });
    }
    window.MAA_consent = {
      get: function () { return choice; },
      set: function (v) { choice = v; try { localStorage.setItem(KEY, JSON.stringify({ v: v, t: Date.now() })); } catch (e) {} apply(v); },
      reset: function () { choice = null; try { localStorage.removeItem(KEY); } catch (e) {} }
    };
    if (choice) apply(choice);
  })();
</script>
<!-- Google Tag Manager — injection differee : hors du chemin critique (LCP/TBT).
     Part au premier geste de l'internaute, sinon 1,5 s apres l'evenement load. -->
<script>(function(w,d,s,l,i){var done=false;
function load(){if(done)return;done=true;w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});
var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';
j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}
var ev=['pointerdown','keydown','touchstart','scroll'];
function go(){ev.forEach(function(e){removeEventListener(e,go,{capture:true});});load();}
ev.forEach(function(e){addEventListener(e,go,{capture:true,passive:true,once:true});});
if(d.readyState==='complete')setTimeout(load,1500);
else addEventListener('load',function(){setTimeout(load,1500);},{once:true});
w.MAA_loadGTM=load;})(window,document,'script','dataLayer','GTM-P2DNNBXT');</script>
<!-- End Google Tag Manager -->""".replace("__GTM__", GTM_ID)

GTM_NOSCRIPT = ('<!-- Google Tag Manager (noscript) -->\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=%s"\n'
                'height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n'
                '<!-- End Google Tag Manager (noscript) -->' % GTM_ID)

CONSENT_BANNER = """<div id="consent-banner" hidden>
  <div class="box">
    <p style="flex:1">Ce site utilise <strong>Google Analytics</strong> pour mesurer son audience, uniquement si vous l’acceptez. Vos données financières (revenu, parts) ne sont jamais transmises. <a href="/mentions-legales.html#cookies">En savoir plus</a></p>
    <div class="acts">
      <button type="button" id="consent-accept">Accepter</button>
      <button type="button" id="consent-refuse">Continuer sans accepter</button>
    </div>
  </div>
</div>
<script>
  (function () {
    var b = document.getElementById('consent-banner'); if (!b || !window.MAA_consent) return;
    function show() { b.hidden = false; } function hide() { b.hidden = true; }
    if (!MAA_consent.get()) show();
    document.getElementById('consent-accept').addEventListener('click', function () { MAA_consent.set('granted'); hide(); });
    document.getElementById('consent-refuse').addEventListener('click', function () { MAA_consent.set('denied'); hide(); });
    document.querySelectorAll('[data-consent-open]').forEach(function (a) { a.addEventListener('click', function (e) { e.preventDefault(); MAA_consent.reset(); show(); }); });
  })();
</script>"""

# --------------------------------------------------------------------------
# Thème clair / sombre. Le script est volontairement inline et placé avant le
# rendu : il applique le choix mémorisé sans provoquer d'éclair blanc.
# `color-scheme` empêche par ailleurs Chrome Android d'assombrir la page tout
# seul, ce qui cassait la charte.
# --------------------------------------------------------------------------
THEME_HEAD = """<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#10141b" media="(prefers-color-scheme: dark)">
<script>(function(){try{var t=localStorage.getItem('maa_theme');
if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t);}catch(e){}})();</script>"""

THEME_BTN = """<button type="button" class="theme-toggle" id="theme-toggle" aria-pressed="false" aria-label="Passer en mode sombre" title="Mode sombre">
<svg class="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
<svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
</button>"""

THEME_JS = """<script>
(function () {
  var bs = [].slice.call(document.querySelectorAll('.theme-toggle')); if (!bs.length) return;
  var mq = window.matchMedia('(prefers-color-scheme: dark)');
  function current() {
    var a = document.documentElement.getAttribute('data-theme');
    return a === 'dark' || a === 'light' ? a : (mq.matches ? 'dark' : 'light');
  }
  function sync() {
    var dark = current() === 'dark';
    var t = dark ? 'Repasser en mode clair' : 'Passer en mode sombre';
    bs.forEach(function (b) {
      b.setAttribute('aria-pressed', dark ? 'true' : 'false');
      b.setAttribute('aria-label', t); b.setAttribute('title', t);
    });
  }
  bs.forEach(function (b) { b.addEventListener('click', function () {
    var next = current() === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try { localStorage.setItem('maa_theme', next); } catch (e) {}
    sync();
    if (window.dataLayer) window.dataLayer.push({ event: 'theme_switch', theme: next });
  }); });
  mq.addEventListener && mq.addEventListener('change', sync);
  sync();
})();
</script>"""

# --------------------------------------------------------------------------
# Barre flottante : invisible en haut de page, elle apparaît au défilement.
# Son intérêt n'est pas décoratif — elle redonne accès au sommaire de la page
# et au reste du site sans remonter, ce qui manquait cruellement sur mobile.
# Le sommaire du panneau est construit en JS à partir du <nav class="toc">
# déjà présent : aucun balisage dupliqué, aucun octet de contenu en double.
# --------------------------------------------------------------------------
TOPBAR = """<div class="tb-scrim" id="tb-scrim"></div>
<div class="topbar" id="topbar">
  <div class="wrap tb-in">
    <a class="tb-brand" href="/">Mes Aides <em>Auto</em></a>
    <button type="button" class="tb-btn" id="tb-menu" aria-expanded="false" aria-controls="tb-panel">Naviguer<span class="chev" aria-hidden="true"></span></button>
    __TOGGLE__
    <a class="btn tb-cta" href="/">Calculer mes aides</a>
  </div>
  <div class="tb-prog" aria-hidden="true"><i></i></div>
</div>
<nav class="tb-panel" id="tb-panel" aria-label="Navigation rapide">
  <div class="wrap">
    <a class="btn btn-lg tb-cta-m" href="/">Calculer mes aides</a>
    <div id="tb-sections"></div>
    <p class="tb-h">Le site</p>
    <ul>
      <li><a href="/">Simulateur d’aides</a></li>
      <li><a href="/aides-voiture-electrique-2026/">Toutes les aides 2026</a></li>
      <li><a href="/aides-voiture-electrique/">Aides près de chez vous</a></li>
      <li><a href="/prime-coup-de-pouce-voiture-electrique/">Prime « Coup de pouce »</a></li>
      <li><a href="/leasing-social-2026/">Leasing social 2026</a></li>
      <li><a href="/aide-voiture-electrique-occasion/">Voiture d’occasion</a></li>
      <li><a href="/cumul-aides-voiture-electrique/">Cumuler les aides</a></li>
      <li><a href="/notre-methodologie/">Notre méthodologie</a></li>
    </ul>
  </div>
</nav>"""

TOPBAR_JS = """<script>
(function () {
  var bar = document.getElementById('topbar'); if (!bar) return;
  var panel = document.getElementById('tb-panel'), scrim = document.getElementById('tb-scrim'),
      btn = document.getElementById('tb-menu'), prog = bar.querySelector('.tb-prog i'),
      host = document.getElementById('tb-sections'), open = false, SHOW = 220;

  // Sommaire du panneau : repris du sommaire de la page, sinon des bandes numerotees.
  var items = [].map.call(document.querySelectorAll('.toc ol li a'), function (a) {
    return { href: a.getAttribute('href'), text: a.textContent.trim(),
             zone: (a.parentNode.className || '').replace('t-', 'z-') };
  });
  // Le H2 n'est pas toujours enfant direct de la bande : on part des bandes.
  if (!items.length) items = [].map.call(document.querySelectorAll('section[id]'), function (sec) {
    var h = sec.querySelector('h2'); if (!h) return null;
    return { href: '#' + sec.id, text: h.textContent.replace(/^[\\s0-9]+/, '').trim(), zone: '' };
  }).filter(Boolean);
  if (host && items.length > 2) host.innerHTML = '<p class="tb-h">Sur cette page</p><ul>' +
    items.map(function (i) { return '<li><a class="' + i.zone + '" href="' + i.href +
      '"><span class="dot"></span>' + i.text + '</a></li>'; }).join('') + '</ul>';

  function mark() {
    if (!host) return;
    var best = null, y = window.pageYOffset + 96;
    [].forEach.call(host.querySelectorAll('a'), function (a) {
      a.classList.remove('tb-cur');
      var t = document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1)));
      if (t && t.getBoundingClientRect().top + window.pageYOffset <= y) best = a;
    });
    if (best) best.classList.add('tb-cur');
  }
  function setOpen(v) {
    open = v; panel.classList.toggle('on', v); scrim.classList.toggle('on', v);
    btn.setAttribute('aria-expanded', v ? 'true' : 'false'); if (v) mark();
  }
  btn.addEventListener('click', function () { setOpen(!open); });
  scrim.addEventListener('click', function () { setOpen(false); });
  panel.addEventListener('click', function (e) { if (e.target.closest && e.target.closest('a')) setOpen(false); });
  window.addEventListener('keydown', function (e) { if (e.key === 'Escape' && open) { setOpen(false); btn.focus(); } });

  var tick = false;
  function frame() {
    tick = false;
    var y = window.pageYOffset, d = document.documentElement,
        h = (d.scrollHeight || 0) - window.innerHeight;
    if (prog) prog.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, y / h) : 0) + ')';
    var on = y > SHOW;
    bar.classList.toggle('on', on);
    if (!on && open) setOpen(false);
  }
  window.addEventListener('scroll', function () {
    if (!tick) { tick = true; requestAnimationFrame(frame); }
  }, { passive: true });
  frame();
})();
</script>"""

NAV = [("/", "Simulateur"), ("/aides-voiture-electrique-2026/", "Aides 2026"),
       ("/aides-voiture-electrique/", "Aides près de chez moi"), ("/notre-methodologie/", "Méthodologie")]

FOOTER = """<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <h4>Le simulateur</h4>
        <ul>
          <li><a href="/">Simulateur d’aides</a></li>
          <li><a href="/aides-voiture-electrique-2026/">Toutes les aides 2026</a></li>
          <li><a href="/cumul-aides-voiture-electrique/">Cumuler les aides</a></li>
        </ul>
      </div>
      <div>
        <h4>Les aides</h4>
        <ul>
          <li><a href="/prime-coup-de-pouce-voiture-electrique/">Prime « Coup de pouce »</a></li>
          <li><a href="/leasing-social-2026/">Leasing social 2026</a></li>
          <li><a href="/aide-voiture-electrique-occasion/">Voiture d’occasion</a></li>
          <li><a href="/bonus-ecologique-2026/">Bonus écologique</a></li>
        </ul>
      </div>
      <div>
        <h4>Près de chez vous</h4>
        <ul>
          <li><a href="/aides-voiture-electrique/">Toutes les aides locales</a></li>
          <li><a href="/aides-voiture-electrique/paris/">Paris et Grand Paris</a></li>
          <li><a href="/aides-voiture-electrique/lyon/">Lyon</a></li>
          <li><a href="/aides-voiture-electrique/marseille/">Marseille</a></li>
        </ul>
      </div>
      <div>
        <h4>Le site</h4>
        <ul>
          <li><a href="/qui-sommes-nous.html">Qui sommes-nous ?</a></li>
          <li><a href="/notre-methodologie/">Notre méthodologie</a></li>
          <li><a href="/sources/">Sources officielles</a></li>
          <li><a href="/historique-aides-auto/">Historique des aides</a></li>
          <li><a href="/mentions-legales.html">Mentions légales</a></li>
          <li><a href="#" data-consent-open>Gérer les cookies</a></li>
          <li><a href="mailto:contact@mes-aides-auto.fr?subject=Mes%20Aides%20Auto%20%E2%80%94%20contact">Nous écrire</a></li>
        </ul>
      </div>
    </div>
    <p class="foot-legal">© 2026 Mes Aides Auto — Calculateur d’aides à la mobilité propre. Informations à caractère indicatif, sans valeur contractuelle : seule la décision de l’organisme qui verse l’aide fait foi.</p>
  </div>
</footer>"""


def header(active=""):
    links = "".join('<a href="%s"%s>%s</a>' % (u, ' aria-current="page"' if u == active else "", t)
                    for u, t in NAV)
    return """<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="/">Mes Aides <em>Auto</em></a>
    <nav class="site-nav" aria-label="Navigation principale">%s</nav>
    %s
    <a class="btn" href="/">Calculer mes aides</a>
  </div>
</header>""" % (links, THEME_BTN)


def crumb_html(crumbs):
    lis = []
    for i, (name, url) in enumerate(crumbs):
        last = i == len(crumbs) - 1
        lis.append("<li>%s</li>" % (name if last else '<a href="%s">%s</a>' % (url, name)))
    return '<nav class="crumb wrap" aria-label="Fil d’Ariane"><ol>%s</ol></nav>' % "".join(lis)


def crumb_ld(crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u}
        for i, (n, u) in enumerate(crumbs)]}


def faq_html(faq):
    if not faq:
        return ""
    items = "".join(
        "<details><summary>%s</summary><p>%s</p></details>" % (q, a) for q, a in faq)
    return '<h2 id="faq">Questions fréquentes</h2><div class="faq">%s</div>' % items


def faq_ld(faq):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faq]}


def sources_html(sources):
    if not sources:
        return ""
    lis = "".join('<li><a href="%s" target="_blank" rel="noopener">%s</a></li>' % (u, l) for l, u in sources)
    return '<h2 id="sources">D’où viennent ces informations ?</h2><ul class="srcs">%s</ul>' % lis


def related_html(related):
    if not related:
        return ""
    lis = "".join('<li><a href="%s">%s</a></li>' % (u, t) for t, u in related)
    return '<nav class="related" aria-label="À lire aussi"><h2>À lire aussi</h2><ul>%s</ul></nav>' % lis


def fr_date(iso):
    y, m, d = iso.split("-")
    mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
            "septembre", "octobre", "novembre", "décembre"][int(m) - 1]
    return "%d %s %s" % (int(d), mois, y)


# --------------------------------------------------------------------------
# Zones typées : le squelette de la page, rendu visible sans lecture.
# La zone est déduite de l'identifiant du H2 — donc jamais saisie à la main.
# --------------------------------------------------------------------------
ZONES = {
    "droits": ("Vos droits", "droits"),
    "montants": ("Le montant", "montant"),
    "bareme": ("Le montant", "montant"),
    "piege": ("Le piège", "piege"),
    "demarches": ("La démarche", "demarche"),
    "cumul": ("Le cumul", "cumul"),
    "exemple": ("Un exemple", "exemple"),
    "national": ("Les aides d’État", "national"),
    "locales": ("Les aides locales", "national"),
    "communes": ("Le périmètre", "perimetre"),
    "liste": ("La liste", "montant"),
    "sans-aide": ("Les territoires sans aide", "piege"),
    "methode": ("Comment lire", "perimetre"),
    "ailleurs": ("Et ailleurs", "perimetre"),
    "supprimees": ("Ce qui n’existe plus", "piege"),
    "definition": ("La définition", "perimetre"),
    "collecte": ("La méthode", "perimetre"),
    "verification": ("La méthode", "perimetre"),
    "calcul": ("La méthode", "perimetre"),
    "fourchette": ("La méthode", "perimetre"),
    "limites": ("Les limites", "piege"),
    "maj": ("La mise à jour", "perimetre"),
    "erreur": ("Nous écrire", "perimetre"),
    "legende": ("La légende", "perimetre"),
    "a2026": ("Le journal", "perimetre"),
    "a2025": ("Le journal", "perimetre"),
    "a2024": ("Le journal", "perimetre"),
    "journal": ("La méthode", "perimetre"),
    "faq": ("Les questions", "faq"),
    "sources": ("Les preuves", "preuves"),
}

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def _slug(txt):
    txt = re.sub(r"<[^>]+>", "", txt)
    txt = (txt.replace("é", "e").replace("è", "e").replace("ê", "e").replace("à", "a")
              .replace("ç", "c").replace("û", "u").replace("ù", "u").replace("ô", "o")
              .replace("î", "i").replace("’", " "))
    return _SLUG_RE.sub("-", txt.lower()).strip("-")[:40] or "section"


CTA_MINI = ('<div class="cta cta-mini"><p class="t">Et pour votre situation ?</p>'
            '<p>Le simulateur applique ces règles à votre code postal, vos revenus et le prix du véhicule.</p>'
            '<a class="btn" href="/">Calculer mes aides</a></div>')


def decorate(html):
    """Ajoute l'intitulé de zone sur chaque H2, garantit les identifiants,
    insère le rappel du simulateur à mi-page, et renvoie le sommaire."""
    toc, seen = [], set()

    def one(m):
        attrs, inner = m.group(1), m.group(2)
        mid = re.search(r'id="([^"]*)"', attrs)
        hid = mid.group(1) if mid else _slug(inner)
        base, n = hid, 2
        while hid in seen:
            hid, n = "%s-%d" % (base, n), n + 1
        seen.add(hid)
        kicker, zone = ZONES.get(hid, ("", ""))
        attrs = re.sub(r'\s*id="[^"]*"', "", attrs)
        cls = ' class="z%s"' % (" z-" + zone if zone else "")
        head = '<span class="zk">%s</span>' % kicker if kicker else ""
        toc.append((hid, re.sub(r"<[^>]+>", "", inner).strip(), zone))
        return '<h2 id="%s"%s%s>%s%s</h2>' % (hid, cls, attrs, head, inner)

    out = re.sub(r"(?is)<h2([^>]*)>(.*?)</h2>", one, html)

    # rappel du simulateur à mi-page, une seule fois, avant le cumul (ou les aides d'État)
    for anchor in ("cumul", "national", "demarches"):
        tag = '<h2 id="%s"' % anchor
        if tag in out and "cta-mini" not in out:
            out = out.replace(tag, CTA_MINI + "\n" + tag, 1)
            break
    return out, toc


def toc_html(toc):
    if len(toc) < 3:
        return ""
    lis = "".join('<li class="t-%s"><a href="#%s">%s</a></li>' % (z or "x", i, t) for i, t, z in toc)
    return ('<nav class="toc" aria-label="Sommaire de la page">'
            '<p class="toc-t">Ce que vous trouverez sur cette page</p>'
            '<ol>%s</ol>%s</nav>' % (lis, labels.LEGEND))


def reading_time(html):
    n = len(re.sub(r"<[^>]+>", " ", html).split())
    return max(1, round(n / 220))


def grants_ld(grants):
    """Une aide = un MonetaryGrant. Aucun rich result Google sur ce type :
    l'objectif est la citation par les moteurs conversationnels."""
    out = []
    for g in grants or []:
        node = {"@type": "MonetaryGrant", "name": g["name"],
                "description": g.get("desc", ""),
                "funder": {"@type": "GovernmentOrganization", "name": g["funder"]}}
        if g.get("min") is not None or g.get("max") is not None:
            node["amount"] = {"@type": "MonetaryAmount", "currency": "EUR"}
            if g.get("min") is not None:
                node["amount"]["minValue"] = g["min"]
            if g.get("max") is not None:
                node["amount"]["maxValue"] = g["max"]
        if g.get("area"):
            node["eligibleRegion"] = {"@type": "AdministrativeArea", "name": g["area"]}
        if g.get("url"):
            node["url"] = g["url"]
        out.append(node)
    return out


def render(page):
    """page = dict(slug,title,desc,h1,crumbs,lede,body,faq,sources,related,verified,ld_extra,og_type)"""
    url = BASE + "/" + (page["slug"] + "/" if page["slug"] else "")
    graph = [crumb_ld(page["crumbs"])]
    if page.get("faq"):
        graph.append(faq_ld(page["faq"]))
    graph.append({
        "@type": page.get("schema_type", "Article"),
        "headline": page["h1"],
        "name": page["h1"],
        "description": page["desc"],
        "inLanguage": "fr-FR",
        "url": url,
        "datePublished": page.get("published", TODAY),
        "dateModified": page.get("verified", TODAY),
        "author": {"@type": "Person", "name": "David Rival", "url": BASE + "/qui-sommes-nous.html"},
        "publisher": {"@type": "Organization", "name": "Mes Aides Auto", "url": BASE + "/"},
        "isPartOf": {"@type": "WebSite", "name": "Mes Aides Auto", "url": BASE + "/"},
    })
    graph += grants_ld(page.get("grants"))
    graph += page.get("ld_extra", [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)

    article = "\n".join(x for x in (page["body"], faq_html(page.get("faq")),
                                     sources_html(page.get("sources"))) if x)
    m = re.match(r'(?s)\s*(<div class="answer">.*?</div>)\s*', article)
    answer, rest = (m.group(1), article[m.end():]) if m else ("", article)
    rest, toc = decorate(rest)
    meta = ('<p class="pmeta"><span>Lecture %d min</span>'
            '<span>Règles vérifiées le %s</span></p>'
            % (reading_time(article), fr_date(page.get("verified", TODAY))))

    body = [
        crumb_html(page["crumbs"]),
        '<main class="wrap"><article class="prose">',
        '<div class="hero"><h1>%s</h1>%s</div>' % (page["h1"], page.get("labels", "")),
        '<p class="lede">%s</p>' % page["lede"],
        answer,
        page.get("idcard", ""),
        page.get("criteres", ""),
        meta,
        toc_html(toc),
        rest,
        '<p class="verif">Dernière vérification des règles de cette page : <strong>%s</strong>. '
        'Nous republions cette page à chaque évolution réglementaire — voir '
        '<a href="/historique-aides-auto/">l’historique des changements</a> et '
        '<a href="/notre-methodologie/">notre méthodologie</a>.</p>' % fr_date(page.get("verified", TODAY)),
        related_html(page.get("related")),
        "</article></main>",
    ]

    html = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{theme}
{fonts}
{consent}
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Mes Aides Auto">
<meta property="og:image" content="{base}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{ogtitle}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{base}/assets/og-image.png">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="/manifest.json">
{maacss}
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
{noscript}
{topbar}
{header}
{body}
{footer}
{banner}
{themejs}
{topbarjs}
</body>
</html>
""".format(theme=THEME_HEAD, fonts=FONTS_HEAD, maacss=MAA_CSS_INLINE, consent=CONSENT_GTM, title=page["title"], desc=page["desc"], url=url, base=BASE,
           ogtitle=page.get("og_title", page["h1"]), ld=ld, noscript=GTM_NOSCRIPT, topbar=TOPBAR.replace("__TOGGLE__", THEME_BTN.replace('id="theme-toggle"', '')),
           header=header(page.get("nav_active", "")), body="\n".join(body),
           footer=FOOTER, banner=CONSENT_BANNER, themejs=THEME_JS, topbarjs=TOPBAR_JS)
    return html


def write(page):
    out_dir = os.path.join(ROOT, page["slug"])
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "index.html")
    html = render(page)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path, len(html.encode("utf-8"))


# --------------------------------------------------------------------------
# Lecture des données du moteur (data.js) et des communes (communes.js)
# --------------------------------------------------------------------------
_ARR_RE = re.compile(r"\s+\d+(?:er|e)\s+Arrondissement$", re.I)


def load_communes():
    """communes.js est au format compact v2 depuis la refonte de performance :
    `cp|insee|nom|insee_commune_mere (vide si == insee)|code_epci`, le département
    étant déduit du code INSEE et la région du département (table COMMUNES_REG).
    Le lecteur attendait encore sept champs : il ne gardait donc aucune commune,
    ce qui faisait disparaître le bloc « Ma commune est-elle concernée ? »."""
    src = open(os.path.join(ROOT, "communes.js"), encoding="utf-8").read()

    def js_string(var):
        i = src.find("window." + var)
        if i < 0:
            return ""
        a = src.index('"', i) + 1
        b = src.index('";', a)
        return src[a:b].replace("\\n", "\n")

    reg_table = {}
    for pair in js_string("COMMUNES_REG").split(","):
        if ":" in pair:
            d, r = pair.split(":", 1)
            reg_table[d] = r

    by_epci, by_region, by_dept = {}, {}, {}
    for line in js_string("COMMUNES_RAW").split("\n"):
        f = line.split("|")
        if len(f) < 5:
            continue
        cp, insee, nom, mere, epci = f[0], f[1], f[2], f[3], f[4]
        dept = insee[:3] if insee[:2] in ("97", "98") else insee[:2]
        reg = reg_table.get(dept, "")
        # Les arrondissements de Paris, Lyon et Marseille sont rattachés à leur
        # commune mère : la liste affiche « Lyon », pas « Lyon 1er… Lyon 9e ».
        key = mere or insee
        label = _ARR_RE.sub("", nom) if mere else nom
        by_epci.setdefault(epci, {}).setdefault(key, (label, cp))
        by_region.setdefault(reg, set()).add(key)
        by_dept.setdefault(dept, set()).add(key)
    return by_epci, by_region, by_dept


def sitemaps(pages):
    """Un index + trois sitemaps thématiques. Seules les URLs canoniques indexables."""
    def urlset(entries):
        body = "".join(
            '  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq><priority>%s</priority></url>\n'
            % (u, lm, cf, pr) for u, lm, cf, pr in entries)
        return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % body

    core = [(BASE + "/", TODAY, "weekly", "1.0"),
            (BASE + "/qui-sommes-nous.html", TODAY, "monthly", "0.6"),
            (BASE + "/notre-methodologie/", TODAY, "monthly", "0.7"),
            (BASE + "/sources/", TODAY, "monthly", "0.6"),
            (BASE + "/historique-aides-auto/", TODAY, "weekly", "0.6")]
    guides, territoires = [], []
    for p in pages:
        u = BASE + "/" + p["slug"] + "/"
        if p["slug"].startswith("aides-voiture-electrique/"):
            territoires.append((u, p.get("verified", TODAY), "monthly", "0.7"))
        elif p["slug"] in ("notre-methodologie", "sources", "historique-aides-auto"):
            continue
        else:
            guides.append((u, p.get("verified", TODAY), "monthly", "0.9"))
    open(os.path.join(ROOT, "sitemap-pages.xml"), "w", encoding="utf-8").write(urlset(core))
    open(os.path.join(ROOT, "sitemap-guides.xml"), "w", encoding="utf-8").write(urlset(guides))
    open(os.path.join(ROOT, "sitemap-territoires.xml"), "w", encoding="utf-8").write(urlset(territoires))
    idx = "".join('  <sitemap><loc>%s/%s</loc><lastmod>%s</lastmod></sitemap>\n' % (BASE, f, TODAY)
                  for f in ("sitemap-pages.xml", "sitemap-guides.xml", "sitemap-territoires.xml"))
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</sitemapindex>\n' % idx)
    return len(core), len(guides), len(territoires)


if __name__ == "__main__":
    import content_national, content_territoires
    pages = content_national.pages() + content_territoires.pages(load_communes())
    total = 0
    for p in pages:
        path, size = write(p)
        total += size
        print("  %-58s %5.1f Ko" % (os.path.relpath(path, ROOT), size / 1024))
    c, g, t = sitemaps(pages)
    print("\n%d pages générées, %.0f Ko au total (moyenne %.1f Ko)" % (len(pages), total / 1024, total / 1024 / len(pages)))
    print("sitemaps : %d pages, %d guides, %d territoires" % (c, g, t))
