# -*- coding: utf-8 -*-
"""Contenu éditorial des pages nationales. Les chiffres proviennent de data.js
et des sources officielles citées en bas de chaque page."""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import labels

V = "2026-09-08"
CTA_STD = ('<div class="cta"><p class="t">Le montant dépend de vos revenus, de votre commune et de la voiture</p>'
           '<p>Quatre informations suffisent : code postal, revenu fiscal de référence, nombre de parts, prix du véhicule. '
           'Aucun compte à créer, rien n’est enregistré.</p>'
           '<a class="btn btn-lg" href="/">Calculer mes aides</a></div>')


def cta(title, text):
    return ('<div class="cta"><p class="t">%s</p><p>%s</p>'
            '<a class="btn btn-lg" href="/">Lancer le simulateur</a></div>' % (title, text))


HUB = dict(
    slug="aides-voiture-electrique-2026",
    nav_active="/aides-voiture-electrique-2026/",
    title="Aides voiture électrique 2026 : montants et conditions",
    og_title="Toutes les aides voiture électrique en 2026",
    desc="Prime d’État « Coup de pouce », leasing social, prime occasion et aides locales : montants, conditions de revenus et simulation personnalisée.",
    h1="Quelles aides pour acheter une voiture électrique en 2026 ?",
    crumbs=[("Accueil", "/"), ("Aides voiture électrique 2026", "/aides-voiture-electrique-2026/")],
    lede="En 2026, quatre dispositifs nationaux subsistent — et une quinzaine d’aides locales s’y ajoutent selon votre commune. Voici ce qui existe réellement, pour qui, et à quelles conditions.",
    verified=V,
    body="""
<div class="answer">
<p><strong>La réponse courte.</strong> Pour une voiture électrique <strong>neuve</strong>, l’aide principale est la <a href="/prime-coup-de-pouce-voiture-electrique/">prime d’État « Coup de pouce »</a> : de l’ordre de <strong>3 300 € à 7 700 €</strong> selon vos revenus et l’origine européenne du véhicule. Si vous utilisez votre voiture pour aller travailler et que votre revenu fiscal ne dépasse pas 16 880 € par part, le <a href="/leasing-social-2026/">leasing social</a> peut être plus avantageux — mais les deux ne se cumulent pas. Pour une <strong>occasion</strong>, une <a href="/aide-voiture-electrique-occasion/">nouvelle prime</a> existe depuis le 1<sup>er</sup> septembre 2026. À cela s’ajoutent les <a href="/aides-voiture-electrique/">aides de votre collectivité</a>, qui, elles, se cumulent avec l’aide de l’État.</p>
</div>

<h2 id="montants">Quelles aides existent encore en 2026 ? Quatre dispositifs</h2>
<div class="table-wrap">
<table>
<caption class="sr-only">Aides nationales à l’achat d’une voiture électrique en 2026</caption>
<thead><tr><th>Aide</th><th>Montant</th><th>Conditions principales</th><th>Véhicule</th></tr></thead>
<tbody>
<tr><td><a href="/prime-coup-de-pouce-voiture-electrique/">Prime d’État « Coup de pouce »</a></td><td class="num">3 300 – 7 700 €</td><td>Achat chez un professionnel partenaire, prix ≤ 47 000 €, demande <strong>avant</strong> le bon de commande, véhicule gardé 2 ans</td><td>Électrique neuve</td></tr>
<tr><td><a href="/aide-voiture-electrique-occasion/">Prime d’État occasion</a></td><td class="num">≈ 300 – 500 € <span class="badge badge-warn">à confirmer</span></td><td>1<sup>re</sup> immatriculation 2017-2023, batterie en bon état, achat chez un professionnel, véhicule gardé 3 ans</td><td>Électrique d’occasion</td></tr>
<tr><td><a href="/leasing-social-2026/">Leasing social 2026</a></td><td class="num">jusqu’à 9 000 €</td><td>Revenu fiscal ≤ 16 880 €/part, usage professionnel, location longue durée de 3 ans minimum, loyer ≤ 200 €/mois</td><td>Électrique neuve, en location</td></tr>
<tr><td>Prime au rétrofit</td><td class="num">jusqu’à 5 000 €</td><td>Revenu fiscal ≤ 24 900 €/part, 80 % du coût de la transformation, demande sous 6 mois</td><td>Transformation d’une thermique</td></tr>
</tbody>
</table>
</div>
<p class="note note-warn"><strong>Un point à comprendre avant tout le reste.</strong> La prime « Coup de pouce » et le leasing social ne sont pas financés par le budget de l’État mais par les fournisseurs d’énergie, dans le cadre des certificats d’économies d’énergie. La réglementation fixe des <em>coefficients</em>, pas des euros : le montant réel dépend du fournisseur partenaire de votre vendeur. C’est pourquoi nous affichons des fourchettes et non un chiffre unique — et pourquoi il faut toujours demander son offre au concessionnaire avant de signer.</p>

<h2 id="bareme">Combien selon vos revenus ? De 3 300 à 7 700 €</h2>
<p>Toutes les aides nationales se calculent sur le <strong>revenu fiscal de référence par part</strong> : vous prenez la ligne « revenu fiscal de référence » de votre dernier avis d’imposition et vous la divisez par votre nombre de parts. Ce résultat vous place dans une tranche de 1 à 10.</p>
<div class="table-wrap">
<table>
<thead><tr><th>Votre situation</th><th>Revenu fiscal par part</th><th>Prime « Coup de pouce » (voiture neuve)</th></tr></thead>
<tbody>
<tr><td>Revenus très modestes (tranches 1 à 3)</td><td>jusqu’à 11 250 €</td><td class="num">5 082 – 5 700 €<br><span style="font-weight:400;color:#64748b">6 776 – 7 700 € si véhicule et batterie européens</span></td></tr>
<tr><td>Revenus modestes (tranches 4 et 5)</td><td>11 250 à 16 880 €</td><td class="num">4 700 – 5 524 €<br><span style="font-weight:400;color:#64748b">5 900 – 7 365 € si véhicule et batterie européens</span></td></tr>
<tr><td>Revenus intermédiaires, gros rouleur (tranches 6 à 8, au moins 12 000 km/an pour le travail)</td><td>16 880 à 27 310 €</td><td class="num">4 700 – 5 524 €<br><span style="font-weight:400;color:#64748b">7 365 – 7 700 € si véhicule et batterie européens</span></td></tr>
<tr><td>Autres ménages</td><td>au-delà</td><td class="num">3 300 – 3 314 €<br><span style="font-weight:400;color:#64748b">4 419 – 4 700 € si véhicule et batterie européens</span></td></tr>
</tbody>
</table>
</div>
<p>Les seuils 2026 de revenu fiscal par part sont : 1 970 € (tranche 1), 7 640 €, 11 250 €, 14 130 €, 16 880 €, 19 600 €, 22 770 €, 27 310 €, 35 880 € (tranche 9), puis au-delà pour la tranche 10.</p>

<h2 id="locales">Votre collectivité ajoute-t-elle quelque chose ? Treize le font</h2>
<p>Treize collectivités versent encore une aide à l’achat aux particuliers : Grand Paris, Métropole de Lyon, Aix-Marseille-Provence, Toulouse, Strasbourg, Rouen, Bordeaux, Reims, Grand Annecy, Pays du Mont-Blanc, Seine-Maritime, Région Occitanie, et Grenoble (aide suspendue). Elles se cumulent avec la prime d’État, mais imposent souvent leurs propres conditions : mise à la casse d’une ancienne voiture, plafond de revenus, dossier à déposer avant ou après l’achat.</p>
<div class="grid grid-3">
<a class="tile" href="/aides-voiture-electrique/paris/"><b>Paris et Grand Paris</b><span>jusqu’à 6 000 €, 131 communes</span></a>
<a class="tile" href="/aides-voiture-electrique/lyon/"><b>Lyon</b><span>500 à 3 000 €, dossier avant l’achat</span></a>
<a class="tile" href="/aides-voiture-electrique/toulouse/"><b>Toulouse</b><span>jusqu’à 5 000 €, achat entre particuliers accepté</span></a>
</div>
<p><a href="/aides-voiture-electrique/">Voir toutes les aides locales, territoire par territoire →</a></p>

<h2 id="supprimees">Qu’est-ce qui a disparu ? Le bonus, la prime à la conversion, le crédit d’impôt borne</h2>
<ul>
<li><strong>Le bonus écologique</strong> a été supprimé le 1<sup>er</sup> juillet 2025 et remplacé par la prime « Coup de pouce ». <a href="/bonus-ecologique-2026/">Ce qu’il faut savoir si vous cherchiez le bonus</a>.</li>
<li><strong>La prime à la conversion</strong> et sa surprime « zone à faibles émissions » de 1 000 € ont disparu le 2 décembre 2024.</li>
<li><strong>Le crédit d’impôt pour une borne de recharge</strong> s’est arrêté le 31 décembre 2025.</li>
<li><strong>Le prêt à taux zéro mobilité</strong> était une expérimentation prévue jusqu’à fin 2025 ; aucune prolongation n’a été trouvée.</li>
</ul>

<h2 id="cumul">Peut-on tout cumuler ? Une seule aide d’État, plus les aides locales</h2>
<p>Non. La règle est simple à retenir : <strong>une seule aide d’État</strong> (prime neuf, prime occasion ou leasing social — jamais deux), à laquelle <strong>s’ajoutent les aides locales</strong>, chacune avec son plafond. Certaines collectivités limitent en plus le total de toutes les aides publiques à 80 % du prix de la voiture. <a href="/cumul-aides-voiture-electrique/">Le détail des cumuls possibles, aide par aide →</a></p>
""" + CTA_STD,
    faq=[
        ("Quelle est l’aide la plus élevée pour une voiture électrique en 2026 ?",
         "Pour un achat, la prime d’État « Coup de pouce » atteint 7 700 € pour un ménage aux revenus très modestes achetant une voiture et une batterie fabriquées en Europe. En location longue durée, le leasing social peut aller jusqu’à 9 000 € d’aide de l’État. Ces deux aides ne se cumulent pas entre elles, mais se cumulent avec l’aide de votre collectivité."),
        ("Faut-il mettre une ancienne voiture à la casse pour avoir une aide en 2026 ?",
         "Pas pour les aides nationales : la prime à la conversion, qui l’exigeait, a été supprimée le 2 décembre 2024. En revanche, la plupart des aides locales (Lyon, Grand Paris, Toulouse, Strasbourg, Rouen, Marseille, Annecy, Bordeaux, Reims) imposent de faire détruire, vendre ou transformer une ancienne voiture."),
        ("Puis-je avoir une aide si j’achète à un particulier ?",
         "Non pour la prime d’État, qui passe obligatoirement par un professionnel partenaire d’un fournisseur d’énergie. Certaines aides locales l’acceptent malgré tout : c’est le cas à Toulouse et à Strasbourg. Le simulateur le signale selon votre commune."),
        ("Les aides s’appliquent-elles aux voitures hybrides ?",
         "Les aides nationales sont réservées aux voitures 100 % électriques. Quelques aides locales acceptent une vignette Crit’Air 1, donc certaines hybrides ou essences récentes : Grand Paris (3 000 € maximum), Toulouse, Strasbourg et Rouen."),
        ("À quelle fréquence ces montants changent-ils ?",
         "Les barèmes nationaux évoluent par arrêté, parfois en cours d’année : le bonus écologique a disparu au 1er juillet 2025, la prime occasion est apparue au 1er septembre 2026. Les règlements locaux sont révisés chaque année et peuvent être suspendus en cours d’exercice, comme à Grenoble depuis le 26 septembre 2025."),
    ],
    sources=[("Prime « Coup de pouce » — service-public.fr, fiche F39188", "https://www.service-public.gouv.fr/particuliers/vosdroits/F39188"),
             ("Récapitulatif des aides nationales — jechangemavoiture.gouv.fr", "https://jechangemavoiture.gouv.fr/jcmv/aide-achat.html"),
             ("Leasing social 2026 — primealaconversion.gouv.fr", "https://www.primealaconversion.gouv.fr/dboneco/accueil/leasingsocial2026.html"),
             ("Arrêté du 10 août 2026 créant la fiche TRA-EQ-133 (voiture électrique d’occasion) — Légifrance", "https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000054666103")],
    related=[("Prime « Coup de pouce » : conditions, montant et démarches", "/prime-coup-de-pouce-voiture-electrique/"),
             ("Leasing social 2026 : revenus et véhicules éligibles", "/leasing-social-2026/"),
             ("Aides pour une voiture électrique d’occasion", "/aide-voiture-electrique-occasion/"),
             ("Peut-on cumuler plusieurs aides ?", "/cumul-aides-voiture-electrique/"),
             ("Les aides près de chez vous", "/aides-voiture-electrique/"),
             ("Le bonus écologique existe-t-il encore ?", "/bonus-ecologique-2026/")],
)

CDP = dict(
    slug="prime-coup-de-pouce-voiture-electrique",
    title="Prime « Coup de pouce » voiture électrique 2026 : montants",
    og_title="Prime « Coup de pouce » voiture électrique 2026",
    desc="L’aide qui remplace le bonus écologique : 3 300 à 7 700 € selon vos revenus, conditions, véhicules éligibles et démarche avant le bon de commande.",
    h1="Prime « Coup de pouce » voiture électrique : conditions, montant et démarches",
    crumbs=[("Accueil", "/"), ("Aides voiture électrique 2026", "/aides-voiture-electrique-2026/"), ("Prime « Coup de pouce »", "/prime-coup-de-pouce-voiture-electrique/")],
    lede="C’est l’aide qui a remplacé le bonus écologique le 1ᵉʳ juillet 2025. Elle n’est pas versée par l’État mais par les fournisseurs d’énergie, et cela change tout à la façon de la demander.",
    verified=V,
    body="""
<div class="answer">
<p><strong>L’essentiel.</strong> La prime « Coup de pouce véhicules particuliers électriques » finance l’achat ou la location longue durée d’une <strong>voiture électrique neuve de 47 000 € au maximum</strong>. Son montant va d’environ <strong>3 300 € à 7 700 €</strong> selon votre revenu fiscal par part et selon que la voiture et sa batterie sont fabriquées en Europe. Point capital : <strong>la demande doit être faite avant la signature du bon de commande</strong>. Une commande déjà signée n’y donne plus droit.</p>
</div>

<h2 id="definition">Qu’est-ce que cette prime, exactement ? Un dispositif payé par les fournisseurs d’énergie</h2>
<p>Elle ne relève pas d’un budget public mais du dispositif des <strong>certificats d’économies d’énergie</strong> : la loi oblige les fournisseurs d’énergie à financer des actions qui réduisent la consommation, et l’achat d’une voiture électrique en fait partie. Concrètement, un fournisseur partenaire de votre concessionnaire verse la prime, le plus souvent en déduction directe sur la facture.</p>
<p>La conséquence pratique est déroutante : <strong>la réglementation ne fixe pas un montant en euros</strong>, mais des coefficients. Le montant réel dépend de l’offre commerciale du fournisseur partenaire de votre vendeur, et deux concessionnaires voisins peuvent proposer des montants différents pour la même voiture et le même acheteur. D’où la règle à retenir : demandez son offre chiffrée au vendeur, par écrit, avant de vous engager.</p>

<h2 id="montants">Quel montant selon vos revenus ? De 3 300 à 7 700 €</h2>
<p>Le calcul se fait sur votre <strong>revenu fiscal de référence divisé par votre nombre de parts</strong>, tel qu’il figure sur votre dernier avis d’imposition. Les fourchettes ci-dessous correspondent aux offres publiées par les fournisseurs partenaires (barème Hellio du 31 juillet 2026, mis à jour le 24 août 2026, et chargeguru 2026).</p>
<div class="table-wrap">
<table>
<thead><tr><th>Catégorie</th><th>Revenu fiscal par part</th><th>Voiture hors critère européen</th><th>Voiture <em>et</em> batterie européennes</th></tr></thead>
<tbody>
<tr><td>Revenus très modestes (tranches 1 à 3)</td><td>&lt; 11 250 €</td><td class="num">5 082 – 5 700 €</td><td class="num">6 776 – 7 700 €</td></tr>
<tr><td>Revenus modestes (tranches 4 et 5)</td><td>&lt; 16 880 €</td><td class="num">4 700 – 5 524 €</td><td class="num">5 900 – 7 365 €</td></tr>
<tr><td>Gros rouleur (tranches 6 à 8)</td><td>&lt; 27 310 €</td><td class="num">4 700 – 5 524 €</td><td class="num">7 365 – 7 700 €</td></tr>
<tr><td>Autres ménages</td><td>au-delà</td><td class="num">3 300 – 3 314 €</td><td class="num">4 419 – 4 700 €</td></tr>
</tbody>
</table>
</div>
<p>Le volet « gros rouleurs » vise les ménages aux revenus intermédiaires qui parcourent <strong>au moins 12 000 km par an à titre professionnel</strong> avec leur voiture personnelle. Il faut s’engager avant le 1<sup>er</sup> janvier 2027 et pouvoir le justifier (attestation de l’employeur ou justificatif de kilométrage).</p>

<h2 id="droits">Qui peut en bénéficier ? Tous les ménages, avec un montant dégressif</h2>
<ul>
<li>Vous êtes un <strong>particulier</strong>, quelle que soit votre tranche de revenus — le montant varie, mais personne n’en est exclu par ses revenus.</li>
<li>Vous achetez ou louez une <strong>voiture particulière 100 % électrique neuve</strong>. Les hybrides, même rechargeables, sont exclues.</li>
<li>Le <strong>prix ne dépasse pas 47 000 €</strong>, batterie comprise.</li>
<li>Le modèle figure sur la <strong>liste officielle des véhicules éligibles</strong> : score environnemental d’au moins 60 points (calculé par l’ADEME sur l’ensemble du cycle de vie) et masse inférieure à 2,4 tonnes.</li>
<li>Vous achetez <strong>chez un professionnel partenaire</strong> d’un fournisseur d’énergie. Un achat entre particuliers n’ouvre aucun droit.</li>
<li>Vous vous engagez à <strong>garder la voiture au moins 2 ans</strong>, ou à signer une location d’au moins 24 mois.</li>
</ul>

<h2 id="demarches">Comment la demander ? Avant de signer le bon de commande</h2>
<ol>
<li>Avant toute chose, demandez au concessionnaire ou au loueur <strong>avec quel fournisseur d’énergie il travaille</strong> et quel montant il vous propose.</li>
<li>Faites établir la demande de prime <strong>avant de signer le bon de commande</strong>. C’est l’erreur la plus fréquente et elle est irrattrapable.</li>
<li>Signez le bon de commande une fois la prime validée : elle est déduite de la facture, ou versée après la livraison selon le partenaire.</li>
<li>Conservez la voiture au moins deux ans.</li>
</ol>
<h3>Les documents à préparer</h3>
<ul>
<li>Pièce d’identité ;</li>
<li>dernier avis d’imposition (revenu fiscal de référence et nombre de parts) ;</li>
<li>devis ou bon de commande, ou contrat de location ;</li>
<li>attestation sur l’honneur fournie par le partenaire ;</li>
<li>si vous êtes gros rouleur : attestation de l’employeur ou justificatif d’au moins 12 000 km par an pour le travail.</li>
</ul>

<h2 id="cumul">Se cumule-t-elle avec les autres aides ? Oui avec les aides locales, non avec le leasing social</h2>
<p class="note note-stop"><strong>Non cumulable</strong> avec le <a href="/leasing-social-2026/">leasing social</a> ni avec la <a href="/aide-voiture-electrique-occasion/">prime occasion</a> : ces trois aides relèvent de la même enveloppe et vous ne pouvez en obtenir qu’une seule.</p>
<p class="note note-ok"><strong>Cumulable</strong> avec les aides de votre région, de votre département ou de votre métropole. Un ménage modeste lyonnais peut ainsi additionner la prime d’État et l’aide de la Métropole de Lyon. <a href="/cumul-aides-voiture-electrique/">Voir le tableau complet des cumuls</a>.</p>
""" + cta("Quel montant dans votre cas ?", "Le simulateur applique votre tranche de revenus, votre commune et les règles de cumul, et vous dit dans quel ordre faire les démarches."),
    faq=[
        ("La prime « Coup de pouce » remplace-t-elle le bonus écologique ?",
         "Oui. Le bonus écologique a été supprimé le 1er juillet 2025 et la prime « Coup de pouce véhicules particuliers électriques », financée par les certificats d’économies d’énergie, l’a remplacé. La différence majeure est que le montant n’est plus fixé par un barème public unique mais dépend du fournisseur d’énergie partenaire du vendeur."),
        ("Pourquoi le montant annoncé varie-t-il d’un concessionnaire à l’autre ?",
         "Parce que la réglementation fixe des coefficients de bonification en kWh cumac, pas des euros. Chaque fournisseur d’énergie obligé convertit ces coefficients en une offre commerciale, en fonction du cours des certificats d’économies d’énergie. Il est donc normal, et parfaitement légal, que deux vendeurs proposent des montants différents."),
        ("Peut-on avoir la prime pour une location avec option d’achat ?",
         "Oui, à condition que le contrat de location dure au moins 24 mois. Attention à ne pas confondre avec le leasing social, qui est un dispositif distinct, réservé aux revenus modestes et qui impose une location de 3 ans minimum."),
        ("Que se passe-t-il si je revends la voiture avant deux ans ?",
         "L’engagement de conservation de deux ans fait partie des conditions de la prime. Une revente anticipée peut entraîner une demande de remboursement par l’organisme qui a versé l’aide. Les modalités figurent dans l’attestation sur l’honneur que vous signez."),
        ("Un véhicule de démonstration est-il éligible ?",
         "Un véhicule de démonstration peut être éligible s’il est acquis entre 3 et 12 mois après sa première immatriculation. Vérifiez ce point précis avec le vendeur, car il conditionne le classement du véhicule en neuf ou en occasion, et donc l’aide applicable."),
    ],
    sources=[("Service-public.fr — fiche F39188, mise à jour du 1er septembre 2026", "https://www.service-public.gouv.fr/particuliers/vosdroits/F39188"),
             ("jechangemavoiture.gouv.fr — aides à l’achat", "https://jechangemavoiture.gouv.fr/jcmv/aide-achat.html"),
             ("ADEME — score environnemental des véhicules", "https://www.ademe.fr/")],
    related=[("Toutes les aides voiture électrique 2026", "/aides-voiture-electrique-2026/"),
             ("Le bonus écologique existe-t-il encore ?", "/bonus-ecologique-2026/"),
             ("Leasing social 2026", "/leasing-social-2026/"),
             ("Peut-on cumuler plusieurs aides ?", "/cumul-aides-voiture-electrique/"),
             ("Les aides de votre collectivité", "/aides-voiture-electrique/"),
             ("Notre méthodologie", "/notre-methodologie/")],
)

LEASING = dict(
    slug="leasing-social-2026",
    title="Leasing social 2026 : conditions, revenus et montants",
    og_title="Leasing social 2026 : conditions et montants",
    desc="Revenu fiscal ≤ 16 880 €/part, usage professionnel, loyer ≤ 200 €/mois : l’État prend en charge 29 % du prix, jusqu’à 6 500 € (9 000 € si européen).",
    h1="Leasing social 2026 : conditions, revenus et véhicules éligibles",
    crumbs=[("Accueil", "/"), ("Aides voiture électrique 2026", "/aides-voiture-electrique-2026/"), ("Leasing social 2026", "/leasing-social-2026/")],
    lede="Louer une voiture électrique neuve pour 200 € par mois au maximum, sans apport : c’est la promesse du leasing social, réservé aux actifs modestes qui roulent pour travailler. Campagne ouverte depuis le 16 juillet 2026, 50 000 places.",
    verified=V,
    body="""
<div class="answer">
<p><strong>L’essentiel.</strong> L’État prend en charge <strong>29 % du prix de la voiture, dans la limite de 6 500 €</strong>. Ce plafond est porté à <strong>9 000 € lorsque le véhicule et sa batterie sont fabriqués dans l’Espace économique européen</strong>, et une surprime de 500 € s’ajoute si le moteur électrique est produit en Europe. Conditions d’accès : revenu fiscal de référence de <strong>16 880 € par part au maximum</strong> et usage professionnel du véhicule.</p>
</div>
<p class="note note-ok"><strong>Correction d’une confusion fréquente.</strong> De nombreux sites présentent « 6 500 € » et « 9 000 € » comme deux chiffres contradictoires. Ce n’en sont pas : 6 500 € est le plafond de droit commun, 9 000 € le plafond majoré pour un véhicule et une batterie fabriqués dans l’Espace économique européen. Source : le téléservice officiel primealaconversion.gouv.fr.</p>

<h2 id="droits">Qui peut en bénéficier ? Revenu fiscal de 16 880 € par part au maximum</h2>
<ul>
<li><strong>Revenu fiscal de référence par part inférieur ou égal à 16 880 €</strong> (avis d’imposition N-2), soit les cinq premières tranches de revenus sur dix.</li>
<li><strong>Être actif</strong> et utiliser sa voiture pour travailler : plus de 10 km entre le domicile et le travail, <em>ou</em> plus de 8 000 km par an à titre professionnel.</li>
<li><strong>Ne pas avoir déjà bénéficié</strong> du leasing social en 2024 ou en 2025.</li>
<li>Résider en France métropolitaine, dans les départements et régions d’outre-mer ou à Saint-Pierre-et-Miquelon.</li>
</ul>

<h2 id="montants">Quel loyer et quelle durée ? Trois ans au minimum</h2>
<div class="table-wrap">
<table>
<thead><tr><th>Critère</th><th>Règle 2026</th></tr></thead>
<tbody>
<tr><td>Durée</td><td>Location longue durée de <strong>36 mois minimum</strong></td></tr>
<tr><td>Loyer</td><td><strong>200 € par mois maximum</strong>, hors services et options</td></tr>
<tr><td>Apport</td><td>Aucun apport exigé</td></tr>
<tr><td>Kilométrage inclus</td><td>Au moins <strong>15 000 km par an</strong></td></tr>
<tr><td>Véhicule</td><td>Voiture particulière <strong>neuve, 100 % électrique</strong>, figurant sur la liste officielle</td></tr>
<tr><td>Prix et masse</td><td>Prix ≤ 47 000 €, masse inférieure à 1,8 tonne — un seuil <strong>plus strict</strong> que celui de la prime « Coup de pouce » (2,4 t)</td></tr>
<tr><td>Enveloppe</td><td><strong>50 000 places</strong>, campagne ouverte le 16 juillet 2026</td></tr>
</tbody>
</table>
</div>
<p class="note note-warn">Le nombre de places restantes n’est pas publié en temps réel. Une éligibilité théorique ne garantit donc pas l’obtention du contrat : les dossiers sont traités dans l’ordre d’arrivée, jusqu’à épuisement de l’enveloppe.</p>

<h2 id="cumul">Leasing social ou prime « Coup de pouce » ? Les deux ne se cumulent pas</h2>
<p>Les deux dispositifs sont <strong>exclusifs l’un de l’autre</strong>. La comparaison dépend surtout de votre projet :</p>
<div class="table-wrap">
<table>
<thead><tr><th></th><th>Leasing social</th><th>Prime « Coup de pouce »</th></tr></thead>
<tbody>
<tr><td>Vous devenez propriétaire</td><td>Non (location)</td><td>Oui (ou location au choix)</td></tr>
<tr><td>Plafond de revenus</td><td>16 880 € par part</td><td>Aucun (le montant baisse avec les revenus élevés)</td></tr>
<tr><td>Usage professionnel exigé</td><td>Oui</td><td>Seulement pour le volet gros rouleurs</td></tr>
<tr><td>Aide maximale</td><td>9 000 € (+ 500 € moteur européen)</td><td>7 700 €</td></tr>
<tr><td>Engagement</td><td>36 mois</td><td>24 mois</td></tr>
</tbody>
</table>
</div>
<p>Le simulateur affiche systématiquement le leasing social comme <em>alternative</em> lorsque vous y êtes éligible, même si vous avez indiqué vouloir acheter : c’est souvent l’option la plus avantageuse pour un ménage modeste qui roule beaucoup.</p>

<h2 id="demarches">Comment faire la demande ?</h2>
<ol>
<li>Vérifiez votre éligibilité et choisissez un modèle sur le site officiel du leasing social.</li>
<li>Contactez un loueur ou un concessionnaire référencé : l’aide de l’État est directement intégrée au contrat, vous n’avancez rien.</li>
<li>Signez le contrat de location longue durée de trois ans minimum.</li>
</ol>
<h3>Les documents à préparer</h3>
<ul>
<li>Pièce d’identité et justificatif de domicile ;</li>
<li>dernier avis d’imposition (revenu fiscal de référence de 16 880 € par part au maximum) ;</li>
<li>attestation de l’employeur (trajet de plus de 10 km) ou déclaration sur l’honneur des kilomètres parcourus pour le travail (plus de 8 000 km par an).</li>
</ul>
""" + cta("Êtes-vous éligible au leasing social ?", "Le simulateur vérifie vos revenus par part, votre usage professionnel et compare automatiquement le leasing social avec la prime d’État."),
    faq=[
        ("Quel revenu maximum pour le leasing social 2026 ?",
         "Le revenu fiscal de référence par part ne doit pas dépasser 16 880 €, d’après l’avis d’imposition N-2. Pour un couple avec deux enfants (3 parts), cela correspond à un revenu fiscal de référence d’environ 50 640 €."),
        ("Peut-on bénéficier du leasing social sans être salarié ?",
         "Le dispositif vise les actifs. Un travailleur indépendant qui utilise son véhicule personnel pour son activité et parcourt plus de 8 000 km par an à ce titre peut donc y prétendre, en le justifiant par une déclaration sur l’honneur. En revanche, une personne sans activité professionnelle n’y est pas éligible."),
        ("Le leasing social est-il cumulable avec l’aide de ma métropole ?",
         "Oui dans la plupart des cas : les aides locales se cumulent avec les aides nationales. Deux exceptions repérées dans les règlements : la Métropole de Rouen exclut explicitement le cumul avec le leasing social, et la Métropole Aix-Marseille-Provence exclut toute location longue durée."),
        ("Que se passe-t-il si les 50 000 places sont épuisées ?",
         "La campagne se ferme. Il reste alors la prime « Coup de pouce » pour un achat ou une location classique d’au moins 24 mois, ainsi que les aides de votre collectivité. Le simulateur les calcule dans tous les cas."),
        ("Le loyer de 200 € comprend-il l’assurance et l’entretien ?",
         "Non. Le plafond de 200 € par mois porte sur le loyer du véhicule hors services annexes. L’assurance, l’entretien ou une éventuelle extension de kilométrage sont facturés en plus par le loueur."),
    ],
    sources=[("Aide au leasing social 2026 — primealaconversion.gouv.fr (téléservice officiel)", "https://www.primealaconversion.gouv.fr/dboneco/accueil/leasingsocial2026.html"),
             ("Leasing social — service-public.fr, fiche F39280", "https://www.service-public.gouv.fr/particuliers/vosdroits/F39280"),
             ("Liste des véhicules éligibles — ecologie.gouv.fr", "https://www.ecologie.gouv.fr/"),
             ("jechangemavoiture.gouv.fr", "https://jechangemavoiture.gouv.fr/jcmv/aide-achat.html")],
    related=[("Prime « Coup de pouce » voiture électrique", "/prime-coup-de-pouce-voiture-electrique/"),
             ("Toutes les aides voiture électrique 2026", "/aides-voiture-electrique-2026/"),
             ("Peut-on cumuler plusieurs aides ?", "/cumul-aides-voiture-electrique/"),
             ("Les aides près de chez vous", "/aides-voiture-electrique/")],
)


def pages():
    return [HUB, CDP, LEASING]


BONUS = dict(
    slug="bonus-ecologique-2026",
    title="Bonus écologique 2026 : existe-t-il encore ?",
    og_title="Le bonus écologique existe-t-il encore en 2026 ?",
    desc="Le bonus écologique a été supprimé le 1er juillet 2025. Ce qui existe à sa place en 2026 : prime « Coup de pouce », leasing social, prime occasion.",
    h1="Le bonus écologique existe-t-il encore en 2026 ?",
    crumbs=[("Accueil", "/"), ("Aides voiture électrique 2026", "/aides-voiture-electrique-2026/"), ("Bonus écologique 2026", "/bonus-ecologique-2026/")],
    lede="Beaucoup de sites continuent d’annoncer un « bonus écologique 2026 ». Voici l’état réel du droit, et ce à quoi vous avez droit aujourd’hui.",
    verified=V,
    body="""
<div class="answer">
<p><strong>Non, le bonus écologique n’existe plus.</strong> Il a été supprimé le <strong>1<sup>er</sup> juillet 2025</strong>. Pour une voiture électrique neuve, il est remplacé par la <a href="/prime-coup-de-pouce-voiture-electrique/">prime d’État « Coup de pouce »</a>, financée par les fournisseurs d’énergie : de <strong>3 300 € à 7 700 €</strong> selon vos revenus. La <strong>prime à la conversion</strong> a elle aussi disparu, le 2 décembre 2024.</p>
</div>

<h2 id="definition">Que valait le bonus écologique avant sa suppression ?</h2>
<p>Jusqu’au 30 juin 2025, le bonus écologique était une aide directe de l’État, versée sur un barème public unique : le même montant pour tout le monde à situation identique, quel que soit le vendeur. C’est ce qui explique que la formule reste dans les mémoires et dans les moteurs de recherche.</p>

<h2 id="supprimees">Qu’est-ce qui a changé ? Le bonus a été remplacé le 1<sup>er</sup> juillet 2025</h2>
<p>La logique de financement a été inversée. L’aide ne vient plus du budget de l’État mais des <strong>certificats d’économies d’énergie</strong> : les fournisseurs d’énergie sont tenus par la loi de financer des actions d’économie d’énergie, et l’achat d’une voiture électrique en fait désormais partie. Trois conséquences très concrètes pour vous :</p>
<ul>
<li><strong>Le montant n’est plus garanti à l’euro près</strong> : la réglementation fixe des coefficients, pas des euros. Deux concessionnaires peuvent proposer deux montants différents.</li>
<li><strong>La demande passe par le vendeur</strong>, partenaire d’un fournisseur d’énergie — et non plus par une plateforme de l’État.</li>
<li><strong>Elle doit être demandée avant la signature du bon de commande.</strong> C’est la principale cause de refus.</li>
</ul>

<h2 id="piege">Quels dispositifs ont disparu, et à quelle date ?</h2>
<div class="table-wrap">
<table>
<thead><tr><th>Dispositif</th><th>Statut</th><th>Ce qui le remplace</th></tr></thead>
<tbody>
<tr><td>Bonus écologique</td><td><span class="badge badge-stop">supprimé le 01/07/2025</span></td><td><a href="/prime-coup-de-pouce-voiture-electrique/">Prime d’État « Coup de pouce »</a></td></tr>
<tr><td>Prime à la conversion</td><td><span class="badge badge-stop">supprimée le 02/12/2024</span></td><td>Aucun équivalent national ; les aides locales ont pris le relais</td></tr>
<tr><td>Surprime zone à faibles émissions (1 000 €)</td><td><span class="badge badge-stop">supprimée le 02/12/2024</span></td><td>Aides des métropoles concernées</td></tr>
<tr><td>Crédit d’impôt borne de recharge (500 €)</td><td><span class="badge badge-stop">terminé le 31/12/2025</span></td><td>Non reconduit par la loi de finances 2026</td></tr>
<tr><td>Prêt à taux zéro mobilité</td><td><span class="badge badge-warn">expérimentation échue fin 2025</span></td><td>Aucune prolongation trouvée</td></tr>
<tr><td>Aide de la Région Île-de-France à l’achat</td><td><span class="badge badge-stop">supprimée le 02/03/2025</span></td><td>Prime « non-casse » pour la transformation en électrique, jusqu’à 6 000 €</td></tr>
</tbody>
</table>
</div>

<h2 id="droits">À quoi avez-vous droit aujourd’hui ? À la prime « Coup de pouce », de 3 300 à 7 700 €</h2>
<div class="grid grid-2">
<a class="tile" href="/prime-coup-de-pouce-voiture-electrique/"><b>Voiture électrique neuve</b><span>Prime d’État « Coup de pouce » : 3 300 à 7 700 € selon vos revenus</span></a>
<a class="tile" href="/leasing-social-2026/"><b>Vous roulez pour travailler, revenus modestes</b><span>Leasing social : jusqu’à 9 000 € d’aide, loyer 200 €/mois maximum</span></a>
<a class="tile" href="/aide-voiture-electrique-occasion/"><b>Voiture électrique d’occasion</b><span>Nouvelle prime d’État depuis le 1<sup>er</sup> septembre 2026</span></a>
<a class="tile" href="/aides-voiture-electrique/"><b>Votre commune</b><span>13 collectivités versent encore une aide, jusqu’à 6 000 €</span></a>
</div>
""" + cta("Ne cherchez plus le bonus : regardez ce à quoi vous avez droit", "Le simulateur applique les règles en vigueur aujourd’hui, pas celles d’avant 2025, et cite la source de chaque montant."),
    faq=[
        ("Le bonus écologique revient-il en 2027 ?",
         "Aucun texte annonçant un rétablissement du bonus écologique n’a été trouvé à la date de vérification de cette page. Les aides à l’achat passent aujourd’hui par les certificats d’économies d’énergie. Toute évolution sera consignée dans notre historique des changements."),
        ("J’ai commandé ma voiture avant le 1er juillet 2025, ai-je encore droit au bonus ?",
         "Les conditions d’extinction dépendent de la date de commande et de facturation prévues par les textes de suppression. Si votre commande est antérieure, rapprochez-vous de l’Agence de services et de paiement, qui gérait le dispositif, avec votre bon de commande daté."),
        ("La prime à la conversion existe-t-elle encore ?",
         "Non, elle a été supprimée le 2 décembre 2024 par le décret 2024-1084, en même temps que sa surprime « zone à faibles émissions » de 1 000 €. Mettre une ancienne voiture à la casse ne donne donc plus droit à aucune aide nationale — mais reste exigé par la majorité des aides locales."),
        ("Pourquoi certains sites annoncent-ils encore un bonus écologique 2026 ?",
         "Parce que la requête reste très fréquente et que beaucoup de contenus n’ont pas été mis à jour depuis 2024. Vérifiez systématiquement la date de mise à jour et la source citée : sur les aides, une page non datée n’a aucune valeur."),
    ],
    sources=[("jechangemavoiture.gouv.fr — aides à l’achat en vigueur", "https://jechangemavoiture.gouv.fr/jcmv/aide-achat.html"),
             ("Service-public.fr — prime « Coup de pouce », fiche F39188", "https://www.service-public.gouv.fr/particuliers/vosdroits/F39188"),
             ("Suppression de la prime à la conversion (décret 2024-1084)", "https://www.quelles-aides.fr/transport-mobilite/aides-transport/prime-conversion/"),
             ("Région Île-de-France — fin de l’aide à l’achat", "https://www.iledefrance.fr/toutes-les-faq/aides-vehicules-propres-faq")],
    related=[("Prime « Coup de pouce » : le dispositif qui remplace le bonus", "/prime-coup-de-pouce-voiture-electrique/"),
             ("Toutes les aides voiture électrique 2026", "/aides-voiture-electrique-2026/"),
             ("Historique des changements réglementaires", "/historique-aides-auto/"),
             ("Les aides de votre collectivité", "/aides-voiture-electrique/")],
)

OCCASION = dict(
    slug="aide-voiture-electrique-occasion",
    title="Aide voiture électrique d’occasion 2026 : la nouvelle prime",
    og_title="Aides pour une voiture électrique d’occasion en 2026",
    desc="Depuis le 1er septembre 2026, une prime d’État existe pour l’occasion électrique : conditions, véhicules concernés et aides locales cumulables.",
    h1="Quelles aides pour acheter une voiture électrique d’occasion ?",
    crumbs=[("Accueil", "/"), ("Aides voiture électrique 2026", "/aides-voiture-electrique-2026/"), ("Voiture électrique d’occasion", "/aide-voiture-electrique-occasion/")],
    lede="L’occasion électrique était le grand angle mort des aides publiques. Un arrêté du 10 août 2026 a créé une prime dédiée, en vigueur depuis le 1ᵉʳ septembre 2026.",
    verified=V,
    body="""
<div class="answer">
<p><strong>Oui, il existe désormais une aide.</strong> L’arrêté du 10 août 2026 a créé la fiche « Achat ou location d’une voiture particulière électrique d’occasion » (TRA-EQ-133), applicable depuis le <strong>1<sup>er</sup> septembre 2026</strong>. Elle vise les voitures <strong>immatriculées pour la première fois entre 2017 et 2023</strong>, dont la <strong>batterie a conservé plus de 80 % de sa capacité</strong>, achetées <strong>chez un professionnel</strong> et gardées <strong>trois ans</strong>. Les aides locales, elles, existaient déjà et restent souvent plus élevées.</p>
</div>
<p class="note note-warn"><strong>Sur le montant, nous préférons dire ce que nous savons.</strong> Comme pour le neuf, la réglementation raisonne en coefficients et non en euros : le montant dépend du fournisseur d’énergie partenaire du vendeur. Les premiers barèmes publiés par un opérateur partenaire (Hellio, mis à jour le 24 août 2026) situent l’aide autour de <strong>300 à 500 €</strong> pour les ménages précaires et modestes ⚠️ — un ordre de grandeur bien inférieur à la prime du neuf, à confirmer offre en main. Nous mettrons cette page à jour dès que des barèmes plus larges seront publiés.</p>

<h2 id="droits">Qui a droit à la prime occasion ? Une électrique immatriculée entre 2017 et 2023</h2>
<div class="table-wrap">
<table>
<thead><tr><th>Critère</th><th>Règle</th></tr></thead>
<tbody>
<tr><td>Véhicule</td><td>Voiture particulière <strong>100 % électrique</strong> d’occasion</td></tr>
<tr><td>Première immatriculation</td><td>Entre le <strong>1<sup>er</sup> janvier 2017 et le 31 décembre 2023</strong> (pour éviter une double valorisation des certificats d’économies d’énergie)</td></tr>
<tr><td>État de la batterie</td><td>Capacité restante <strong>supérieure à 80 %</strong>, ou autonomie résiduelle d’au moins 200 km</td></tr>
<tr><td>Vendeur</td><td><strong>Professionnel habilité</strong> — un achat entre particuliers n’ouvre aucun droit</td></tr>
<tr><td>Conservation</td><td><strong>36 mois</strong></td></tr>
<tr><td>Bonification</td><td>Prix ≤ 25 000 € TTC et masse &lt; 1 800 kg ⚠️ <em>(conditions du projet d’arrêté soumis à consultation publique)</em></td></tr>
<tr><td>Entrée en vigueur</td><td>1<sup>er</sup> septembre 2026</td></tr>
</tbody>
</table>
</div>

<h2 id="locales">Les aides locales font-elles mieux ? Souvent oui</h2>
<p>Sur l’occasion, ce sont les collectivités qui portent l’essentiel de l’effort. Quelques exemples tirés des règlements en vigueur :</p>
<div class="table-wrap">
<table>
<thead><tr><th>Territoire</th><th>Aide pour une occasion électrique</th><th>Condition marquante</th></tr></thead>
<tbody>
<tr><td><a href="/aides-voiture-electrique/occitanie/">Région Occitanie</a></td><td class="num">30 % du prix, jusqu’à 1 600 €</td><td>Ménage non imposable, achat chez un professionnel agréé en Occitanie</td></tr>
<tr><td><a href="/aides-voiture-electrique/toulouse/">Toulouse Métropole</a></td><td class="num">2 000 à 3 300 €</td><td>Mise à la casse d’une Crit’Air 3 ou plus ancienne ; achat à un particulier accepté</td></tr>
<tr><td><a href="/aides-voiture-electrique/paris/">Grand Paris</a></td><td class="num">jusqu’à 6 000 €</td><td>Mise au rebut obligatoire, prix ≤ 40 000 €</td></tr>
<tr><td><a href="/aides-voiture-electrique/marseille/">Marseille (zone à faibles émissions)</a></td><td class="num">1 500 à 2 500 €</td><td>Mise à la casse d’une Crit’Air 4 ou plus ancienne, achat chez un professionnel</td></tr>
<tr><td><a href="/aides-voiture-electrique/strasbourg/">Strasbourg</a></td><td class="num">2 000 à 4 000 €</td><td>Neuf ou occasion, achat à un particulier accepté</td></tr>
</tbody>
</table>
</div>
<p>Un ménage non imposable de Toulouse achetant une électrique d’occasion à 15 000 € peut ainsi additionner l’éco-chèque régional et la prime métropolitaine — le simulateur applique automatiquement les règles de cumul et les plafonds.</p>

<h2 id="piege">Acheter à un particulier : ce que vous perdez</h2>
<p>C’est le point le plus mal compris de l’occasion électrique. Un achat entre particuliers vous prive de <strong>toute prime d’État</strong> et de l’éco-chèque d’Occitanie, qui exige un professionnel agréé. Restent quelques aides locales qui l’acceptent explicitement — Toulouse et Strasbourg notamment — à condition de déposer le dossier vous-même, avec l’acte de vente (formulaire Cerfa 15776), la carte grise et, le cas échéant, le certificat de destruction de l’ancienne voiture.</p>

<h2 id="demarches">Que vérifier avant d’acheter ?</h2>
<ul>
<li><strong>L’état de santé de la batterie</strong> : demandez un certificat de contrôle. C’est la condition qui décide de l’aide, et le principal risque financier d’une occasion électrique.</li>
<li><strong>La date de première immatriculation</strong> : hors de la fenêtre 2017-2023, pas de prime d’État.</li>
<li><strong>Le statut du vendeur</strong> : professionnel habilité, ou particulier.</li>
<li><strong>Le règlement de votre collectivité</strong> : certaines exigent le dépôt du dossier avant l’achat (Lyon, Grand Annecy).</li>
</ul>
""" + cta("Quelles aides pour votre occasion ?", "Indiquez votre code postal, vos revenus et le prix : le simulateur distingue le neuf de l’occasion et le vendeur professionnel du particulier."),
    faq=[
        ("Y a-t-il une prime pour une voiture électrique d’occasion en 2026 ?",
         "Oui. L’arrêté du 10 août 2026 a créé la fiche standardisée TRA-EQ-133 « Achat ou location d’une voiture particulière électrique d’occasion », entrée en vigueur le 1er septembre 2026. Son montant dépend du fournisseur d’énergie partenaire du vendeur ; les premiers barèmes publiés se situent autour de 300 à 500 €."),
        ("Quelles voitures d’occasion sont éligibles ?",
         "Les voitures particulières 100 % électriques immatriculées pour la première fois entre le 1er janvier 2017 et le 31 décembre 2023, dont la batterie a conservé plus de 80 % de sa capacité ou offre au moins 200 km d’autonomie, achetées chez un professionnel habilité et conservées 36 mois."),
        ("Puis-je cumuler la prime occasion avec la prime du neuf ?",
         "Non. Prime neuf, prime occasion et leasing social relèvent de la même enveloppe et sont exclusifs les uns des autres. En revanche, la prime occasion se cumule avec les aides de votre collectivité."),
        ("L’aide est-elle plus élevée pour une occasion ou pour une neuve ?",
         "Pour l’aide nationale, le neuf reste nettement plus avantageux. Sur l’occasion, ce sont les aides locales qui font la différence : jusqu’à 6 000 € dans le Grand Paris ou 3 300 € à Toulouse, contre quelques centaines d’euros pour la prime d’État."),
        ("Comment prouver l’état de la batterie ?",
         "Par un certificat d’état de santé de la batterie établi lors de la vente. Les professionnels du véhicule électrique d’occasion le fournissent de plus en plus souvent ; exigez-le, car il conditionne à la fois l’aide et la valeur réelle du véhicule."),
    ],
    sources=[("Arrêté du 10 août 2026 créant la fiche TRA-EQ-133 — Légifrance", "https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000054666103"),
             ("Projet d’arrêté TRA-EQ-133 — consultation publique, ministère de la Transition écologique", "https://www.consultations-publiques.developpement-durable.gouv.fr/projet-d-arrete-creant-la-fiche-d-operation-a3394.html?lang=fr"),
             ("Éco-chèque mobilité — Région Occitanie", "https://www.laregion.fr/Eco-cheque-mobilite-voiture-electrique-ou-hybride"),
             ("Barèmes publiés par un opérateur partenaire (Hellio, 24/08/2026) ⚠️ source commerciale", "https://www.hellio.com/actualites/conseils/prime-cee-voiture-electrique-occasion")],
    related=[("Toutes les aides voiture électrique 2026", "/aides-voiture-electrique-2026/"),
             ("Prime « Coup de pouce » (voiture neuve)", "/prime-coup-de-pouce-voiture-electrique/"),
             ("Peut-on cumuler plusieurs aides ?", "/cumul-aides-voiture-electrique/"),
             ("Éco-chèque de la Région Occitanie", "/aides-voiture-electrique/occitanie/")],
)

CUMUL = dict(
    slug="cumul-aides-voiture-electrique",
    title="Cumul des aides voiture électrique : ce qui se cumule",
    og_title="Peut-on cumuler les aides voiture électrique ?",
    desc="Prime d’État, leasing social, aides des métropoles et régions : le tableau complet des cumuls possibles, des exclusions et des plafonds à 80 %.",
    h1="Peut-on cumuler plusieurs aides pour acheter une voiture électrique ?",
    crumbs=[("Accueil", "/"), ("Aides voiture électrique 2026", "/aides-voiture-electrique-2026/"), ("Cumul des aides", "/cumul-aides-voiture-electrique/")],
    lede="Une aide d’État, et une seule. Autant d’aides locales que votre territoire en propose. Et des plafonds qui rabotent le total. Voici la mécanique exacte.",
    verified=V,
    body="""
<div class="answer">
<p><strong>La règle en une phrase.</strong> Vous ne pouvez obtenir qu’<strong>une seule aide nationale</strong> — prime « Coup de pouce » neuf, prime occasion ou leasing social — mais elle <strong>se cumule avec les aides de votre région, de votre département et de votre métropole</strong>. Certaines collectivités plafonnent ensuite le total de toutes les aides publiques à un pourcentage du prix de la voiture.</p>
</div>

<h2 id="montants">Quelles aides se cumulent, aide par aide ?</h2>
<div class="table-wrap">
<table>
<thead><tr><th>Aide A</th><th>Aide B</th><th>Cumul</th><th>Conditions</th></tr></thead>
<tbody>
<tr><td>Prime « Coup de pouce » neuf</td><td>Leasing social</td><td><span class="badge badge-stop">Impossible</span></td><td>Même enveloppe (certificats d’économies d’énergie) : il faut choisir</td></tr>
<tr><td>Prime « Coup de pouce » neuf</td><td>Prime occasion</td><td><span class="badge badge-stop">Impossible</span></td><td>Exclusives par nature (neuf ou occasion)</td></tr>
<tr><td>Prime d’État (quelle qu’elle soit)</td><td>Aide d’une métropole</td><td><span class="badge badge-ok">Oui</span></td><td>Sauf mention contraire du règlement local</td></tr>
<tr><td>Prime d’État</td><td>Aide d’une région</td><td><span class="badge badge-ok">Oui</span></td><td>Occitanie : réservée aux ménages non imposables</td></tr>
<tr><td>Aide d’une métropole</td><td>Aide d’une région</td><td><span class="badge badge-ok">Oui</span></td><td>Toulouse Métropole et éco-chèque Occitanie se cumulent explicitement</td></tr>
<tr><td>Leasing social</td><td>Aide de la Métropole de Rouen</td><td><span class="badge badge-stop">Impossible</span></td><td>Exclusion écrite dans le règlement de la Métropole</td></tr>
<tr><td>Leasing social</td><td>Aide d’Aix-Marseille-Provence</td><td><span class="badge badge-stop">Impossible</span></td><td>La location longue durée est exclue du règlement métropolitain</td></tr>
<tr><td>Aide départementale (Seine-Maritime)</td><td>Aide de la Métropole de Rouen</td><td><span class="badge badge-stop">Impossible</span></td><td>L’aide départementale vise les habitants <em>hors</em> Métropole de Rouen</td></tr>
<tr><td>Prime au rétrofit</td><td>Aides locales</td><td><span class="badge badge-ok">Oui</span></td><td>Île-de-France ajoute jusqu’à 6 000 €, Strasbourg 2 500 €, Rouen 2 000 €</td></tr>
</tbody>
</table>
</div>

<h2 id="cumul">Quels plafonds rabotent le total ? Jusqu’à 80 % du prix</h2>
<p>Trois collectivités appliquent un plafond global : <strong>le total de toutes les aides publiques ne peut pas dépasser un pourcentage du prix</strong> de la voiture. Si ce plafond est atteint, c’est l’aide locale qui est réduite, jamais l’aide d’État.</p>
<div class="table-wrap">
<table>
<thead><tr><th>Territoire</th><th>Plafond du total des aides</th></tr></thead>
<tbody>
<tr><td>Eurométropole de Strasbourg</td><td class="num">80 % du prix</td></tr>
<tr><td>Métropole Rouen Normandie</td><td class="num">80 % du prix</td></tr>
<tr><td>Département de la Seine-Maritime</td><td class="num">80 % du prix</td></tr>
<tr><td>Grand Annecy</td><td class="num">100 % du prix</td></tr>
<tr><td>Communauté de communes Pays du Mont-Blanc</td><td class="num">40 % du prix (sur sa propre aide)</td></tr>
</tbody>
</table>
</div>
<p><strong>Exemple concret.</strong> Une voiture d’occasion à 10 000 € achetée par un ménage rouennais de la tranche la plus modeste : 4 000 € d’aide métropolitaine + la prime d’État. Le plafond de 80 % limite le total à 8 000 € : l’aide de la Métropole est écrêtée en conséquence. Le simulateur effectue ce calcul automatiquement et affiche la mention « montant réduit ».</p>

<h2 id="piege">Trois pièges de cumul à connaître</h2>
<ul>
<li><strong>L’ordre des démarches.</strong> À Lyon et au Grand Annecy, le dossier local doit être déposé <em>avant</em> l’achat ; la prime d’État aussi doit être demandée avant le bon de commande. Une seule signature prématurée fait tomber les deux.</li>
<li><strong>Le vendeur.</strong> Acheter à un particulier supprime toute prime d’État et l’éco-chèque d’Occitanie, mais reste compatible avec Toulouse et Strasbourg.</li>
<li><strong>Le nombre d’aides par foyer.</strong> Plusieurs règlements limitent l’aide à une voiture par personne ou par foyer, parfois sur plusieurs années (une aide tous les 4 ans au Pays du Mont-Blanc).</li>
</ul>
""" + cta("Le calcul du cumul, fait pour vous", "Le simulateur applique les exclusions, les plafonds locaux et l’écrêtement, puis affiche le total réellement atteignable — et non une addition théorique."),
    faq=[
        ("Peut-on cumuler la prime d’État et l’aide de sa métropole ?",
         "Oui, dans la quasi-totalité des cas : les aides locales sont conçues pour s’ajouter aux aides nationales. Deux exceptions repérées : la Métropole de Rouen exclut le cumul avec le leasing social, et Aix-Marseille-Provence exclut la location longue durée."),
        ("Peut-on toucher deux aides nationales ?",
         "Non. La prime « Coup de pouce » pour un véhicule neuf, la prime pour un véhicule d’occasion et le leasing social relèvent du même mécanisme de certificats d’économies d’énergie et sont exclusifs les uns des autres."),
        ("Que se passe-t-il si le total dépasse le plafond de 80 % ?",
         "L’aide locale est réduite du dépassement. À Strasbourg, Rouen et en Seine-Maritime, le total des aides publiques ne peut pas dépasser 80 % du prix de la voiture ; la collectivité verse donc la différence entre ce plafond et les aides déjà obtenues."),
        ("Peut-on cumuler une aide de la région et une aide de la métropole ?",
         "Oui. Le cas le plus courant est l’Occitanie : l’éco-chèque mobilité régional se cumule explicitement avec la prime « véhicule + propre » de Toulouse Métropole, à condition de remplir les critères des deux règlements."),
    ],
    sources=[("Service-public.fr — prime « Coup de pouce », fiche F39188", "https://www.service-public.gouv.fr/particuliers/vosdroits/F39188"),
             ("Aide au leasing social 2026 — primealaconversion.gouv.fr", "https://www.primealaconversion.gouv.fr/dboneco/accueil/leasingsocial2026.html"),
             ("Règlement des aides — Eurométropole de Strasbourg", "https://www.strasbourg.eu/aides-conversion"),
             ("Règlement du 29/09/2025 — Métropole Rouen Normandie", "https://zfe.metropole-rouen-normandie.fr/sites/default/files/2025-10/B2025_0429_annexe.pdf")],
    related=[("Toutes les aides voiture électrique 2026", "/aides-voiture-electrique-2026/"),
             ("Prime « Coup de pouce »", "/prime-coup-de-pouce-voiture-electrique/"),
             ("Leasing social 2026", "/leasing-social-2026/"),
             ("Les aides de votre collectivité", "/aides-voiture-electrique/"),
             ("Notre méthodologie", "/notre-methodologie/")],
)


def pages():
    return [HUB, CDP, LEASING, BONUS, OCCASION, CUMUL]


# ---------------------------------------------------------------------------
# Pages générées à partir de data.js (la donnée reste la source unique de vérité)
# ---------------------------------------------------------------------------
import os, re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def aids_from_datajs():
    src = open(os.path.join(_ROOT, "data.js"), encoding="utf-8").read()
    out = []
    for block in src.split("\n  {")[1:]:
        block = block.split("\n  },")[0]
        g = lambda k: (re.search(k + r":\s*'([^']*)'", block) or [None, None])[1]
        if not g("id"):
            continue
        out.append(dict(id=g("id"), scope=g("scope"), status=g("status"), label=g("label"),
                        territory=g("territoryLabel"), url=g("sourceUrl"),
                        src=g("sourceLabel"), verified=g("lastVerified"),
                        info="info: true" in block))
    return out


STATUS_BADGE = {
    "active": '<span class="badge badge-ok">règle vérifiée</span>',
    "active_unverified": '<span class="badge badge-warn">à confirmer</span>',
    "suspended": '<span class="badge badge-stop">aide suspendue</span>',
    "ended": '<span class="badge badge-stop">dispositif terminé</span>',
}


def sources_table():
    rows_nat, rows_loc = [], []
    for a in aids_from_datajs():
        if not a["url"]:
            continue
        row = ("<tr><td><strong>%s</strong>%s</td><td>%s</td><td><a href=\"%s\" target=\"_blank\" rel=\"noopener\">%s</a></td>"
               "<td class=\"num\">%s</td></tr>") % (
            a["label"], ('<br><span style="color:#64748b;font-weight:400">%s</span>' % a["territory"]) if a["territory"] else "",
            STATUS_BADGE.get(a["status"], ""), a["url"], a["src"] or a["url"],
            "/".join(reversed(a["verified"].split("-"))) if a["verified"] else "—")
        (rows_nat if a["scope"] == "national" else rows_loc).append(row)
    head = '<thead><tr><th>Dispositif</th><th>Statut</th><th>Source citée</th><th>Vérifié le</th></tr></thead>'
    t = lambda rows: '<div class="table-wrap"><table>%s<tbody>%s</tbody></table></div>' % (head, "".join(rows))
    return t(rows_nat), t(rows_loc)


def _sources_page():
    nat, loc = sources_table()
    body = """
<div class="answer">
<p>Chaque règle utilisée par le simulateur cite le texte ou la page officielle dont elle est issue, et la date à laquelle nous l’avons vérifiée. Ce tableau est produit automatiquement à partir de la base de règles du simulateur : il ne peut donc pas diverger de ce que l’outil calcule.</p>
</div>

<h2>Dispositifs nationaux</h2>
""" + nat + """
<h2>Aides des collectivités</h2>
<p>Chaque règlement local est cité avec son lien direct. Lorsque la page officielle était inaccessible ou le barème non publié à la date de vérification, la règle porte la mention « à confirmer » et le simulateur l’affiche comme telle plutôt que d’avancer un montant.</p>
""" + loc + """
<h2>Territoires vérifiés sans aide</h2>
<p>Une réponse négative a autant de valeur qu’un montant, à condition d’être sourcée. Nous avons vérifié et documenté l’absence d’aide à l’achat pour les particuliers sur : Montpellier Méditerranée Métropole, Métropole Nice Côte d’Azur, Saint-Étienne Métropole, Métropole Toulon-Provence-Méditerranée, le Département des Bouches-du-Rhône (hors zone à faibles émissions de Marseille), la Région Normandie et la Région Île-de-France.</p>
<p>Plusieurs fiches gouvernementales encore en ligne mentionnent des aides supprimées depuis (Nice en 2023, Normandie, Bouches-du-Rhône). Nous documentons ces écarts plutôt que de les recopier.</p>

<h2>Données géographiques</h2>
<p>Les 35 493 couples code postal / commune, avec commune de rattachement, intercommunalité, département et région, proviennent du <strong>code officiel géographique de l’INSEE</strong>, via le jeu de données public Etalab « découpage administratif » version 6.0.0. Toutes les règles territoriales s’appuient sur le code SIREN officiel de l’intercommunalité, et non sur des listes de communes saisies à la main.</p>
<p class="note note-warn">Limite assumée : les zones à faibles émissions ne couvrent parfois qu’une partie d’une commune (Lyon, Marseille, Reims). Nous les approximons à la commune entière et l’indiquons sur chaque résultat concerné.</p>
"""
    return dict(
        slug="sources", schema_type="WebPage",
        title="Sources officielles des aides à l’achat automobile",
        og_title="Nos sources officielles",
        desc="Toutes les sources du simulateur : textes réglementaires, fiches service-public.fr, règlements des collectivités, avec la date de vérification.",
        h1="Les sources de chaque règle du simulateur",
        crumbs=[("Accueil", "/"), ("Sources officielles", "/sources/")],
        lede="Un simulateur d’aides ne vaut que par ses sources. Voici les nôtres, dispositif par dispositif, avec la date de dernière vérification.",
        verified=V, body=body,
        faq=[("Que signifie la mention « à confirmer » ?",
              "Elle indique que la règle est appliquée par le simulateur mais que la page officielle était inaccessible, non datée ou incomplète lors de la vérification. Le montant affiché repose alors sur des sources secondaires concordantes, et nous le signalons au lieu de le présenter comme certain."),
             ("À quelle fréquence les sources sont-elles revérifiées ?",
              "Chaque règle porte sa date de vérification. Nous reprenons en priorité celles dont la date dépasse 90 jours, ainsi que toutes celles concernées par un changement réglementaire annoncé."),
             ("Puis-je réutiliser ces données ?",
              "Les règlements et textes cités sont des documents publics. Pour toute réutilisation de notre base consolidée ou toute demande de journaliste, écrivez à contact@mes-aides-auto.fr.")],
        sources=[("Service-public.fr", "https://www.service-public.gouv.fr/particuliers/vosdroits/F39188"),
                 ("jechangemavoiture.gouv.fr", "https://jechangemavoiture.gouv.fr/jcmv/aide-achat.html"),
                 ("primealaconversion.gouv.fr", "https://www.primealaconversion.gouv.fr/"),
                 ("Légifrance", "https://www.legifrance.gouv.fr/"),
                 ("Code officiel géographique — INSEE", "https://www.insee.fr/fr/information/2560452")],
        related=[("Notre méthodologie", "/notre-methodologie/"),
                 ("Historique des changements", "/historique-aides-auto/"),
                 ("Toutes les aides 2026", "/aides-voiture-electrique-2026/")])


METHODO = dict(
    slug="notre-methodologie", schema_type="WebPage", nav_active="/notre-methodologie/",
    title="Notre méthodologie : comment Mes Aides Auto calcule vos aides",
    og_title="Comment nous calculons vos aides",
    desc="Comment les règles sont collectées, vérifiées et datées, comment le simulateur calcule, et ce qu’il ne peut pas savoir. Transparence sur les limites.",
    h1="Comment Mes Aides Auto calcule vos aides",
    crumbs=[("Accueil", "/"), ("Notre méthodologie", "/notre-methodologie/")],
    lede="Un simulateur d’aides publiques manipule de l’argent, des revenus et du droit. Voici précisément comment il fonctionne, et où s’arrêtent ses certitudes.",
    verified=V,
    body="""
<div class="answer">
<p>Le simulateur fournit une <strong>estimation</strong> établie à partir des informations que vous renseignez et des règles connues à la date de vérification indiquée. <strong>L’éligibilité définitive dépend toujours de l’organisme qui attribue l’aide.</strong></p>
</div>

<h2 id="collecte">Comment les règles sont-elles collectées ?</h2>
<p>Chaque dispositif est saisi à partir de sa <strong>source officielle</strong> : texte publié au Journal officiel, fiche service-public.fr, portail de l’État, ou règlement d’attribution voté par la collectivité. Lorsqu’une source officielle existe, nous ne construisons jamais une règle sur une source secondaire. Lorsqu’elle n’existe pas ou n’est pas accessible, la règle est marquée « à confirmer » et l’outil l’affiche comme telle.</p>

<h2 id="verification">Comment sont-elles vérifiées et datées ?</h2>
<p>Chaque règle porte trois attributs : un <strong>statut</strong> (vérifiée, à confirmer, suspendue, terminée), un <strong>lien vers sa source</strong> et une <strong>date de dernière vérification</strong>. Ces trois éléments sont affichés sur chaque carte de résultat. Une règle sans date est une règle sans valeur : c’est le principe de base de ce site.</p>

<h2 id="calcul">Comment le calcul est-il fait ?</h2>
<ul>
<li>Votre <strong>revenu fiscal de référence est divisé par votre nombre de parts</strong>, puis situé dans les tranches officielles 2026 (de 1 970 € à 35 880 € par part).</li>
<li>Votre <strong>code postal est converti en commune</strong>, puis en intercommunalité, département et région, à partir du code officiel géographique de l’INSEE. Les règles locales s’appliquent sur le code SIREN de l’intercommunalité, jamais sur une liste de villes écrite à la main.</li>
<li>Chaque règle est évaluée indépendamment, avec la raison précise de chaque refus.</li>
<li>Les <strong>exclusions mutuelles</strong> sont appliquées (une seule aide d’État), puis les <strong>plafonds de cumul</strong> propres à certaines collectivités, qui écrêtent le montant local.</li>
<li>Le total additionne uniquement les aides retenues. Les alternatives et les aides informatives sont affichées mais exclues du total.</li>
</ul>
<p>Le calcul s’exécute <strong>entièrement dans votre navigateur</strong>, en 1 à 3 millisecondes. Aucune donnée fiscale n’est envoyée à un serveur, ni enregistrée : vos réponses restent sur votre appareil, et vous pouvez les effacer d’un clic.</p>

<h2 id="fourchette">Pourquoi certains montants sont-ils affichés en fourchette ?</h2>
<p>La prime « Coup de pouce » et le leasing social sont financés par les certificats d’économies d’énergie. La réglementation fixe des <strong>coefficients en kilowattheures cumac</strong>, que chaque fournisseur d’énergie convertit en offre commerciale. Il n’existe donc pas de montant légal unique. Nous affichons la fourchette des offres publiées par les partenaires, en citant leur date. Afficher un chiffre unique serait plus confortable, mais faux.</p>

<h2 id="limites">Ce que le simulateur ne peut pas savoir</h2>
<ul>
<li><strong>Le périmètre exact des zones à faibles émissions.</strong> À Lyon, Marseille ou Reims, la zone ne couvre qu’une partie de la commune. Nous approximons à la commune entière et le signalons.</li>
<li><strong>Les enveloppes restantes.</strong> Le leasing social compte 50 000 places, l’éco-chèque d’Occitanie 5 000 aides : ces compteurs ne sont pas publiés en temps réel.</li>
<li><strong>L’éligibilité du modèle précis.</strong> Le score environnemental et la masse dépendent de la version exacte du véhicule : nous renvoyons à la liste officielle plutôt que de deviner.</li>
<li><strong>Le montant que votre concessionnaire vous proposera</strong>, puisqu’il dépend de son fournisseur partenaire.</li>
<li><strong>Votre situation fiscale fine</strong> (imposable ou non), que certaines aides exigent et que nous signalons comme condition à vérifier sur votre avis d’imposition.</li>
</ul>

<h2 id="maj">Comment les changements réglementaires sont-ils traités ?</h2>
<ol>
<li>Identification du changement (veille sur les sources officielles) ;</li>
<li>vérification sur le texte ou le règlement lui-même ;</li>
<li>mise à jour de la règle dans le moteur, et de sa date de vérification ;</li>
<li>mise à jour des pages concernées ;</li>
<li>inscription dans l’<a href="/historique-aides-auto/">historique des changements</a>, qui reste consultable.</li>
</ol>
<p>Les anciennes pages ne sont pas supprimées : une aide disparue reste documentée, parce que la question « existe-t-elle encore ? » est légitime et mérite une réponse datée.</p>

<h2 id="erreur">Comment signaler une erreur ?</h2>
<p>Si vous constatez un écart entre une règle affichée et le règlement en vigueur — en particulier si vous travaillez dans une collectivité — écrivez à <a href="mailto:contact@mes-aides-auto.fr">contact@mes-aides-auto.fr</a> avec le lien du texte. Les corrections sont traitées en priorité et consignées dans l’historique.</p>
""" + cta("Voir la méthode à l’œuvre", "Chaque résultat affiche sa source, sa date de vérification et la raison exacte d’un refus."),
    faq=[("Mes données fiscales sont-elles envoyées quelque part ?",
          "Non. Le calcul est exécuté dans votre navigateur : revenu fiscal, nombre de parts et prix du véhicule ne quittent pas votre appareil et ne sont jamais enregistrés sur un serveur. Seule une mesure d’audience anonyme, soumise à votre accord, enregistre le code postal saisi et le montant maximal estimé."),
         ("Le résultat a-t-il une valeur officielle ?",
          "Non. C’est une estimation fondée sur les règles publiées et sur vos réponses. Seule la décision de l’organisme qui verse l’aide fait foi : concessionnaire partenaire d’un fournisseur d’énergie pour la prime d’État, collectivité pour les aides locales."),
         ("Pourquoi certaines aides sont-elles affichées « à confirmer » ?",
          "Parce que leur règlement n’était pas accessible ou pas daté lors de la vérification. Nous préférons afficher l’incertitude plutôt que de présenter un montant incertain comme acquis."),
         ("Qui édite ce site ?",
          "Mes Aides Auto est édité à titre personnel par David Rival, directeur de la publication. Le site est gratuit, sans publicité, sans inscription et ne revend aucune donnée. Voir les mentions légales pour l’identité complète de l’éditeur et de l’hébergeur.")],
    sources=[("Service-public.fr", "https://www.service-public.gouv.fr/particuliers/vosdroits/F39188"),
             ("Code officiel géographique — INSEE", "https://www.insee.fr/fr/information/2560452"),
             ("Score environnemental — ADEME", "https://www.ademe.fr/")],
    related=[("Nos sources, dispositif par dispositif", "/sources/"),
             ("Historique des changements", "/historique-aides-auto/"),
             ("Qui sommes-nous ?", "/qui-sommes-nous.html"),
             ("Toutes les aides 2026", "/aides-voiture-electrique-2026/")],
)

HISTORIQUE = dict(
    slug="historique-aides-auto", schema_type="WebPage",
    title="Historique des aides à l’achat automobile (2024-2026)",
    og_title="Historique des aides automobiles",
    desc="Journal daté des évolutions : fin du bonus écologique et de la prime à la conversion, création de la prime « Coup de pouce », prime occasion 2026.",
    h1="Historique des changements sur les aides à l’achat automobile",
    crumbs=[("Accueil", "/"), ("Historique des aides", "/historique-aides-auto/")],
    lede="Les aides changent vite, et les contenus périmés circulent longtemps. Ce journal daté recense les évolutions que nous avons vérifiées, du plus récent au plus ancien.",
    verified=V,
    body="""
<h2 id="a2026">Ce qui a changé en 2026</h2>
<div class="card card-soft">
<h3>1<sup>er</sup> septembre 2026 — création de la prime pour les voitures électriques d’occasion</h3>
<p>L’arrêté du 10 août 2026 crée la fiche standardisée TRA-EQ-133 « Achat ou location d’une voiture particulière électrique d’occasion ». Premières conditions : immatriculation initiale entre 2017 et 2023, batterie ayant conservé plus de 80 % de sa capacité, achat chez un professionnel, conservation trois ans. <a href="/aide-voiture-electrique-occasion/">Détail de la prime occasion</a></p>
</div>
<div class="card card-soft">
<h3>16 juillet 2026 — ouverture du leasing social 2026</h3>
<p>50 000 places. Aide de l’État de 29 % du prix, plafonnée à 6 500 €, portée à 9 000 € pour un véhicule et une batterie fabriqués dans l’Espace économique européen, avec une surprime de 500 € pour un moteur produit en Europe. <a href="/leasing-social-2026/">Conditions du leasing social</a></p>
</div>
<div class="card card-soft">
<h3>1<sup>er</sup> juillet 2026 — nouvelle campagne de l’éco-chèque mobilité en Occitanie</h3>
<p>5 000 aides disponibles entre juillet 2026 et juin 2027 pour l’achat d’une voiture électrique d’occasion par un ménage non imposable : 30 % du prix, dans la limite de 1 600 €. <a href="/aides-voiture-electrique/occitanie/">Éco-chèque Occitanie</a></p>
</div>

<h2 id="a2025">Ce qui a changé en 2025</h2>
<div class="card card-soft">
<h3>26 septembre 2025 — suspension de l’aide de Grenoble-Alpes Métropole</h3>
<p>Le dispositif est suspendu sans date de reprise annoncée. Le simulateur l’affiche comme suspendu et l’exclut du total, en rappelant le barème qui s’appliquerait en cas de reprise. <a href="/aides-voiture-electrique/grenoble/">Situation à Grenoble</a></p>
</div>
<div class="card card-soft">
<h3>1<sup>er</sup> juillet 2025 — suppression du bonus écologique</h3>
<p>Le bonus écologique disparaît et la prime « Coup de pouce véhicules particuliers électriques », financée par les certificats d’économies d’énergie, prend le relais. Changement majeur : le montant n’est plus fixé par un barème public unique. <a href="/bonus-ecologique-2026/">Ce qui remplace le bonus</a></p>
</div>
<div class="card card-soft">
<h3>2 mars 2025 — fin de l’aide à l’achat de la Région Île-de-France</h3>
<p>L’aide régionale aux particuliers est supprimée. Subsiste la prime « non-casse » pour la transformation d’un véhicule thermique en électrique, jusqu’à 6 000 €.</p>
</div>
<div class="card card-soft">
<h3>1<sup>er</sup> janvier 2025 — nouveaux règlements locaux</h3>
<p>Entrée en vigueur du règlement de l’Eurométropole de Strasbourg et ouverture du guichet de Bordeaux Métropole.</p>
</div>
<div class="card card-soft">
<h3>31 décembre 2025 — fin du crédit d’impôt pour borne de recharge</h3>
<p>Le crédit d’impôt de 500 € n’est pas reconduit par la loi de finances 2026. L’expérimentation du prêt à taux zéro mobilité arrive également à échéance, sans prolongation trouvée.</p>
</div>

<h2 id="a2024">Ce qui a changé en 2024</h2>
<div class="card card-soft">
<h3>2 décembre 2024 — suppression de la prime à la conversion et de la surprime ZFE</h3>
<p>Le décret 2024-1084 met fin à la prime à la conversion et à sa surprime « zone à faibles émissions » de 1 000 €. Mettre une ancienne voiture à la casse ne donne plus droit à aucune aide nationale — mais reste exigé par la plupart des règlements locaux.</p>
</div>

<h2 id="journal">Comment nous tenons ce journal</h2>
<p>Chaque entrée correspond à un changement vérifié sur sa source officielle, avec mise à jour simultanée du moteur de calcul et des pages concernées. Les pages relatives à des dispositifs supprimés sont conservées : elles répondent à une question réelle. Voir <a href="/notre-methodologie/">notre méthodologie</a> et <a href="/sources/">nos sources</a>.</p>
""" + cta("Vos aides, à jour", "Le simulateur applique les règles en vigueur aujourd’hui, chacune datée et sourcée."),
    faq=[("Où voir la date de mise à jour d’une règle précise ?",
          "Sur chaque carte de résultat du simulateur : la date de dernière vérification et le lien vers la source y figurent. La page Sources en donne la liste complète."),
         ("Une aide supprimée peut-elle revenir ?",
          "Oui, cela s’est déjà produit pour des dispositifs locaux. C’est le cas notamment des aides suspendues, comme celle de Grenoble-Alpes Métropole depuis le 26 septembre 2025 : le règlement existe toujours, seul le versement est interrompu.")],
    sources=[("jechangemavoiture.gouv.fr", "https://jechangemavoiture.gouv.fr/jcmv/aide-achat.html"),
             ("Arrêté du 10 août 2026 (TRA-EQ-133) — Légifrance", "https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000054666103"),
             ("Aide au leasing social 2026 — primealaconversion.gouv.fr", "https://www.primealaconversion.gouv.fr/dboneco/accueil/leasingsocial2026.html"),
             ("Zone à faibles émissions — Grenoble-Alpes Métropole", "https://zfe.grenoblealpesmetropole.fr/684-aides-et-parcours.htm")],
    related=[("Toutes les aides 2026", "/aides-voiture-electrique-2026/"),
             ("Le bonus écologique existe-t-il encore ?", "/bonus-ecologique-2026/"),
             ("Notre méthodologie", "/notre-methodologie/"),
             ("Nos sources", "/sources/")],
)




# ---------------------------------------------------------------------------
# v1.1 — Signalétique des pages nationales.
# Mêmes quatre familles que les pages territoires : une étiquette veut dire la
# même chose partout. Les valeurs suivent data.js (scope / roadmap / status).
# ---------------------------------------------------------------------------
HEAD = {
    "aides-voiture-electrique-2026": (
        labels.bar(scope="national", status="active", tags=["particulier", "neuve", "occasion"]),
        labels.id_card([("Aides nationales en vigueur", "4"),
                        ("Montant de la principale", "3 300 à 7 700 €"),
                        ("Territoires qui ajoutent une aide", "13")]),
        labels.criteres([
            ("ok", "Voiture 100 % électrique neuve : prime « Coup de pouce », de 3 300 à 7 700 €"),
            ("ok", "Revenu fiscal de 16 880 € par part au maximum et usage professionnel : leasing social, jusqu’à 9 000 €"),
            ("ok", "Électrique d’occasion immatriculée entre 2017 et 2023 : prime occasion"),
            ("stop", "Une seule aide d’État à la fois : les trois sont exclusives les unes des autres"),
            ("time", "La prime d’État se demande avant la signature du bon de commande"),
        ], "Quelle aide est pour vous")),

    "prime-coup-de-pouce-voiture-electrique": (
        labels.bar(scope="national", roadmap="dealer_cee", status="active", tags=["neuve", "particulier"]),
        labels.id_card([("Montant", "3 300 à 7 700 €"),
                        ("Condition qui élimine", "Prix supérieur à 47 000 €"),
                        ("Quand demander", "Avant le bon de commande")]),
        labels.criteres([
            ("ok", "Voiture 100 % électrique neuve, prix inférieur ou égal à 47 000 €"),
            ("ok", "Achat chez un professionnel partenaire d’un fournisseur d’énergie"),
            ("ok", "Montant majoré si le véhicule et la batterie sont assemblés en Europe"),
            ("stop", "Véhicule à conserver deux ans"),
            ("time", "Demande à faire avant la signature du bon de commande, jamais après"),
        ])),

    "leasing-social-2026": (
        labels.bar(scope="national", roadmap="leasing_social", status="active", tags=["location", "neuve", "revenus"]),
        labels.id_card([("Montant", "jusqu’à 9 000 €"),
                        ("Condition qui élimine", "Revenu supérieur à 16 880 € par part"),
                        ("Quand demander", "Avant la signature")]),
        labels.criteres([
            ("ok", "Revenu fiscal de référence de 16 880 € par part au maximum"),
            ("ok", "Utiliser sa voiture pour aller travailler"),
            ("ok", "Location longue durée de trois ans au minimum"),
            ("stop", "Pas de cumul avec la prime « Coup de pouce » : il faut choisir"),
        ])),

    "bonus-ecologique-2026": (
        labels.bar(scope="national", status="ended", tags=["neuve"]),
        labels.id_card([("Montant aujourd’hui", "0 €"),
                        ("Supprimé le", "1<sup>er</sup> juillet 2025"),
                        ("Ce qui l’a remplacé", "Prime « Coup de pouce »")]),
        labels.criteres([
            ("stop", "Le bonus écologique n’existe plus depuis le 1<sup>er</sup> juillet 2025"),
            ("stop", "La prime à la conversion a disparu le 2 décembre 2024"),
            ("ok", "La prime « Coup de pouce » l’a remplacé : de 3 300 à 7 700 € selon vos revenus"),
        ], "Ce qu’il faut savoir")),

    "aide-voiture-electrique-occasion": (
        labels.bar(scope="national", roadmap="dealer_cee", status="active_unverified", tags=["occasion", "particulier"]),
        labels.id_card([("Montant", "environ 300 à 500 €"),
                        ("Condition qui élimine", "Immatriculation hors 2017-2023"),
                        ("Quand demander", "Avant le bon de commande")]),
        labels.criteres([
            ("ok", "Voiture électrique d’occasion, première immatriculation entre 2017 et 2023"),
            ("ok", "Achat chez un professionnel, batterie en bon état"),
            ("stop", "Véhicule à conserver trois ans"),
            ("stop", "Montant encore à confirmer : le barème définitif n’est pas publié"),
        ])),

    "cumul-aides-voiture-electrique": (
        labels.bar(scope="national", status="active", tags=["particulier"]),
        labels.id_card([("Deux aides d’État ensemble", "Jamais"),
                        ("Aide d’État + aide locale", "Cumul possible"),
                        ("Plafond local fréquent", "80 % du prix")]),
        labels.criteres([
            ("ok", "Une aide d’État, à laquelle s’ajoutent les aides de votre collectivité"),
            ("stop", "Jamais deux aides d’État : prime neuf, prime occasion et leasing social sont exclusifs"),
            ("time", "Chaque aide a son propre moment de dépôt — c’est là que les dossiers tombent"),
        ], "La règle en trois lignes")),
}

# Une aide nationale = un MonetaryGrant. Aucun rich result Google sur ce type :
# l'objectif est la citation par les moteurs conversationnels.
GRANTS = {
    "aides-voiture-electrique-2026": [
        dict(name="Prime « Coup de pouce » voiture électrique", funder="État",
             desc="Aide à l’achat d’une voiture électrique neuve, financée par les certificats d’économies d’énergie.",
             min=3300, max=7700, area="France", url="https://mes-aides-auto.fr/prime-coup-de-pouce-voiture-electrique/"),
        dict(name="Leasing social 2026", funder="État",
             desc="Location longue durée d’une voiture électrique pour les ménages modestes qui roulent pour travailler.",
             max=9000, area="France", url="https://mes-aides-auto.fr/leasing-social-2026/"),
        dict(name="Prime d’État pour une voiture électrique d’occasion", funder="État",
             desc="Aide à l’achat d’une électrique d’occasion immatriculée entre 2017 et 2023.",
             min=300, max=500, area="France", url="https://mes-aides-auto.fr/aide-voiture-electrique-occasion/"),
        dict(name="Prime au rétrofit", funder="État",
             desc="Aide à la transformation d’une voiture thermique en électrique.",
             max=5000, area="France"),
    ],
    "prime-coup-de-pouce-voiture-electrique": [
        dict(name="Prime « Coup de pouce » voiture électrique", funder="État",
             desc="Aide à l’achat d’une voiture électrique neuve de 47 000 € au maximum, à demander avant le bon de commande.",
             min=3300, max=7700, area="France")],
    "leasing-social-2026": [
        dict(name="Leasing social 2026", funder="État",
             desc="Location longue durée de trois ans minimum, sous condition de revenu fiscal de 16 880 € par part.",
             max=9000, area="France")],
    "aide-voiture-electrique-occasion": [
        dict(name="Prime d’État pour une voiture électrique d’occasion", funder="État",
             desc="Première immatriculation entre 2017 et 2023, achat chez un professionnel, véhicule conservé trois ans.",
             min=300, max=500, area="France")],
}

LEGENDE_METHODO = """
<h2 id="legende">Que veulent dire les étiquettes de couleur ?</h2>
<p>Chaque page porte des étiquettes qui répondent, sans lecture, aux quatre questions
qui reviennent toujours. Elles sont produites automatiquement à partir de notre base de
règles : une étiquette veut donc dire exactement la même chose sur toutes les pages du site.</p>
<div class="table-wrap"><table>
<thead><tr><th>Famille</th><th>Étiquettes</th><th>Ce qu’elle vous dit</th></tr></thead>
<tbody>
<tr><td>Qui paie</td><td>%s</td><td>L’échelon qui verse l’aide. Une aide d’État et une aide locale se cumulent presque toujours.</td></tr>
<tr><td>Quand demander</td><td>%s</td><td>Le moment du dépôt du dossier. C’est la première cause de refus : une demande déposée trop tard est perdue.</td></tr>
<tr><td>Fiabilité de la règle</td><td>%s</td><td>Ce que vaut notre information : règle lue dans un texte officiel à jour, règle dont la reconduction n’est pas confirmée, ou dispositif arrêté.</td></tr>
<tr><td>Pour qui</td><td>%s</td><td>Le type de véhicule et de bénéficiaire visés, et les conditions structurantes.</td></tr>
</tbody></table></div>
<p>Le bloc <strong>« Vous y avez droit si »</strong> en haut de chaque page reprend les conditions
du règlement telles que le simulateur les applique : ✓ une condition à remplir, ✗ une condition
qui élimine un dossier, ⏱ le moment de la démarche.</p>
""" % (
    labels.payeur("national") + labels.payeur("epci") + labels.payeur("region") + labels.payeur("dept"),
    labels.quand("dealer_cee") + labels.quand("local_before") + labels.quand("local_after"),
    labels.fiabilite("active") + labels.fiabilite("active_unverified") + labels.fiabilite("suspended") + labels.fiabilite("ended"),
    labels.profils(["neuve", "occasion", "casse"], 3),
)

def pages():
    METHODO["body"] = METHODO["body"] + LEGENDE_METHODO
    ps = [HUB, CDP, LEASING, BONUS, OCCASION, CUMUL, METHODO, _sources_page(), HISTORIQUE]
    for pg in ps:
        h = HEAD.get(pg["slug"])
        if h:
            pg["labels"], pg["idcard"], pg["criteres"] = h
        if GRANTS.get(pg["slug"]):
            pg["grants"] = GRANTS[pg["slug"]]
    return ps
