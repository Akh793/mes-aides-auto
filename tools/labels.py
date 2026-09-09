# -*- coding: utf-8 -*-
"""Taxonomie d'étiquettes de Mes Aides Auto — quatre familles, liste fermée.

Règle de discipline (v1.1) :
  1. quatre familles, pas cinq ;
  2. une teinte par famille, jamais une couleur par valeur ;
  3. trois étiquettes visibles au maximum par élément ;
  4. jamais la couleur seule — chaque étiquette porte son texte ;
  5. les valeurs viennent de data.js (scope / roadmap / status), elles ne se
     saisissent pas à la main : c'est ce qui garantit qu'une étiquette veut dire
     la même chose sur les 28 pages.
"""

# --- Famille A — qui paie (champ `scope` de data.js) -----------------------
PAYEUR = {
    "national": "État",
    "epci": "Métropole",
    "region": "Région",
    "dept": "Département",
}

# --- Famille B — quand demander (champ `roadmap` de data.js) ---------------
QUAND = {
    "dealer_cee": "Avant le bon de commande",
    "leasing_social": "Avant la signature",
    "local_before": "Avant l’achat",
    "local_after": "Après l’achat",
}

# --- Famille C — fiabilité de la règle (champ `status` de data.js) ---------
FIABILITE = {
    "active": ("Règle vérifiée", "ok"),
    "active_unverified": ("À confirmer", "warn"),
    "suspended": ("Aide suspendue", "stop"),
    "ended": ("Dispositif supprimé", "stop"),
    "none": ("Aucune aide locale", "none"),
}

# --- Famille D — pour qui / quel véhicule (champ `tags` de data.js) --------
PROFIL = {
    "neuve": "Voiture neuve",
    "occasion": "Occasion",
    "location": "Location",
    "utilitaire": "Utilitaire",
    "retrofit": "Transformation en électrique",
    "particulier": "Particulier",
    "pro": "Professionnel",
    "casse": "Casse obligatoire",
    "cession": "Cession acceptée",
    "revenus": "Sous condition de revenus",
    "zfe": "Zone à faibles émissions",
}


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def badge(family, text, variant=""):
    """Une étiquette. family ∈ pay|when|rule|who."""
    cls = "lb lb-%s%s" % (family, (" lb-%s-%s" % (family, variant)) if variant else "")
    return '<span class="%s">%s</span>' % (cls, _esc(text))


def payeur(scope):
    v = PAYEUR.get(scope)
    return badge("pay", v) if v else ""


def quand(roadmap):
    v = QUAND.get(roadmap)
    return badge("when", v) if v else ""


def fiabilite(status):
    v = FIABILITE.get(status)
    return badge("rule", v[0], v[1]) if v else ""


def profils(tags, limit=3):
    tags = [t for t in (tags or []) if t in PROFIL][:limit]
    return "".join(badge("who", PROFIL[t]) for t in tags)


def bar(scope=None, roadmap=None, status=None, tags=None, tags_limit=2):
    """La ligne d'étiquettes : au plus 3 étiquettes fortes + 2 neutres."""
    out = [payeur(scope), quand(roadmap), fiabilite(status), profils(tags, tags_limit)]
    out = [o for o in out if o]
    return '<div class="lbbar">%s</div>' % "".join(out) if out else ""


def id_card(rows):
    """Carte d'identité : liste de couples (intitulé, valeur HTML). 2 à 4 lignes."""
    rows = [(k, v) for k, v in rows if v]
    if not rows:
        return ""
    cells = "".join(
        '<div class="idc-i"><dt>%s</dt><dd>%s</dd></div>' % (k, v) for k, v in rows)
    return '<dl class="idcard">%s</dl>' % cells


CRIT_ICON = {"ok": "✓", "stop": "✗", "time": "⏱", "info": "•"}


def criteres(items, title="Vous y avez droit si"):
    """Bloc d'éligibilité : liste de couples (type, texte). type ∈ ok|stop|time|info."""
    items = [(t, x) for t, x in items if x]
    if not items:
        return ""
    lis = "".join('<li class="c-%s"><span aria-hidden="true">%s</span>%s</li>'
                  % (t, CRIT_ICON.get(t, "•"), x) for t, x in items)
    return ('<div class="crit-box"><p class="crit-t">%s</p><ul class="crit">%s</ul></div>'
            % (title, lis))


LEGEND = (
    '<details class="lblegend"><summary>Comment lire les étiquettes de cette page</summary>'
    '<dl>'
    '<dt>' + badge("pay", "État") + badge("pay", "Métropole") + '</dt>'
    '<dd>Qui verse l’aide : État, métropole, région ou département. '
    'Une aide d’État et une aide locale se cumulent presque toujours.</dd>'
    '<dt>' + badge("when", "Avant l’achat") + '</dt>'
    '<dd>À quel moment déposer le dossier. C’est la première cause de refus : '
    'une demande déposée trop tard est perdue.</dd>'
    '<dt>' + badge("rule", "Règle vérifiée", "ok") + badge("rule", "À confirmer", "warn") + '</dt>'
    '<dd>Ce que vaut notre information : règle lue dans un texte officiel à jour, '
    'ou règle dont la reconduction n’est pas confirmée.</dd>'
    '<dt>' + badge("who", "Voiture neuve") + badge("who", "Casse obligatoire") + '</dt>'
    '<dd>À qui et à quel véhicule l’aide s’adresse.</dd>'
    '</dl>'
    '<p><a href="/notre-methodologie/">La légende complète et notre méthode</a></p>'
    '</details>'
)
