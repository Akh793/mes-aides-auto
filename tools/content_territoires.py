# -*- coding: utf-8 -*-
"""Hub territorial + pages par territoire.

Règle d'indexabilité appliquée : une page n'existe que si le territoire porte
une règle propre (aide en vigueur, aide suspendue, ou suppression documentée).
Aucune page n'est générée pour une commune sans donnée spécifique — c'est le
simulateur qui répond dans ce cas.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import labels

V = "2026-09-07"          # date de vérification des règlements locaux
VN = "2026-09-08"         # date de vérification des règles nationales

NAT_BLOCK = """<h2 id="national">Et les aides de l’État ? De 3 300 à 7 700 €, partout en France</h2>
<p>Quelle que soit votre commune, vous pouvez prétendre à une aide de l’État, qui <strong>s’ajoute</strong> à l’aide locale :</p>
<ul>
<li><a href="/prime-coup-de-pouce-voiture-electrique/">Prime « Coup de pouce »</a> pour une voiture électrique neuve : 3 300 à 7 700 € selon vos revenus, à demander <strong>avant</strong> le bon de commande ;</li>
<li><a href="/leasing-social-2026/">leasing social</a> si votre revenu fiscal ne dépasse pas 16 880 € par part et que vous roulez pour travailler : jusqu’à 9 000 € ;</li>
<li><a href="/aide-voiture-electrique-occasion/">prime occasion</a> depuis le 1<sup>er</sup> septembre 2026, pour une électrique immatriculée entre 2017 et 2023.</li>
</ul>
<p>Ces trois aides sont exclusives les unes des autres : <a href="/cumul-aides-voiture-electrique/">voir les règles de cumul</a>.</p>"""


def cta(city):
    return ('<div class="cta"><p class="t">Vos aides à %s, en quelques secondes</p>'
            '<p>Le simulateur croise votre code postal, vos revenus et le prix du véhicule, '
            'applique les plafonds locaux et vous indique dans quel ordre faire les démarches.</p>'
            '<a class="btn btn-lg" href="/">Calculer mes aides à %s</a></div>' % (city, city))


def table(head, rows):
    return ('<div class="table-wrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            % ("".join("<th>%s</th>" % h for h in head),
               "".join("<tr>%s</tr>" % "".join(c for c in r) for r in rows)))


# ---------------------------------------------------------------------------
# Territoires : la donnée chiffrée vient de data.js, l'angle éditorial est écrit
# ---------------------------------------------------------------------------
T = []

T.append(dict(
    slug="paris", city="Paris", epci="200054781", indexable=True,
    title="Aide voiture électrique Paris 2026 : jusqu’à 6 000 €",
    desc="L’aide « Métropole roule propre » atteint 6 000 € dans les 131 communes du Grand Paris, sous condition de revenus et de mise au rebut.",
    h1="Quelles aides pour acheter une voiture électrique à Paris en 2026 ?",
    lede="Paris relève de la Métropole du Grand Paris, qui verse l’aide locale la plus élevée de France : jusqu’à 6 000 €. La Région Île-de-France, elle, n’aide plus l’achat depuis mars 2025.",
    answer="""<p><strong>Oui, jusqu’à 6 000 €.</strong> L’aide « Métropole roule propre » du Grand Paris s’adresse aux habitants des <strong>131 communes</strong> de la métropole, dont Paris. Conditions : revenu fiscal de référence de <strong>24 900 € par part au maximum</strong>, <strong>mise au rebut définitive d’une ancienne voiture</strong>, et prix du véhicule inférieur à <strong>40 000 €</strong>. Elle se cumule avec la prime d’État.</p>""",
    detail="""<h2 id="montants">Les montants de l’aide « Métropole roule propre »</h2>
""" + table(["Véhicule acheté", "Montant maximal", "Précision"], [
        ['<td>Voiture <strong>100 % électrique</strong>, neuve ou d’occasion</td>', '<td class="num">jusqu’à 6 000 €</td>', '<td>+ 1 000 € si elle est assemblée dans un pays d’Europe à l’électricité peu carbonée</td>'],
        ['<td>Hybride ou essence <strong>vignette Crit’Air 1</strong></td>', '<td class="num">jusqu’à 3 000 €</td>', '<td>Les autres motorisations sont exclues</td>'],
    ]) + """
<p class="note note-warn">« Jusqu’à » : le montant exact dépend de votre niveau de revenus, selon un barème que la Métropole détaille sur son guichet en ligne. Nous affichons donc un plafond, pas un montant garanti. Par ailleurs, le règlement consulté est celui de 2025 : <strong>sa reconduction en 2026 n’est pas confirmée noir sur blanc</strong> sur la page officielle. Vérifiez l’ouverture du guichet avant de vous engager.</p>
<h3>Les conditions à remplir</h3>
<ul>
<li>Résider dans l’une des 131 communes de la Métropole du Grand Paris ;</li>
<li>revenu fiscal de référence <strong>inférieur ou égal à 24 900 € par part</strong> ;</li>
<li><strong>faire détruire définitivement une ancienne voiture</strong> — la vente ne suffit pas, contrairement à Lyon ou Strasbourg ;</li>
<li>prix d’achat <strong>inférieur à 40 000 €</strong>, un plafond plus bas que celui de la prime d’État (47 000 €) : c’est souvent lui qui bloque un dossier ;</li>
<li>neuf ou occasion, les deux sont acceptés.</li>
</ul>""",
    demarche="""<h2 id="demarches">Comment demander l’aide du Grand Paris</h2>
<p>La demande se fait <strong>après l’achat</strong>, sur le guichet en ligne « Métropole roule propre ». Prévoyez : carte grise du nouveau véhicule à votre nom, facture, justificatif de domicile, dernier avis d’imposition, certificat de destruction de l’ancienne voiture délivré par un centre agréé, et un RIB.</p>
<p class="note note-ok"><strong>Ordre à respecter :</strong> la prime d’État, elle, se demande <em>avant</em> la signature du bon de commande, auprès du concessionnaire. Faites-la d’abord, puis achetez, puis déposez le dossier métropolitain.</p>""",
    cumul="""<h2 id="cumul">Cumul et particularités franciliennes</h2>
<p>L’aide métropolitaine se cumule avec la prime d’État. En revanche, deux dispositifs franciliens ont disparu :</p>
<ul>
<li><strong>l’aide à l’achat de la Région Île-de-France</strong>, supprimée le 2 mars 2025 ;</li>
<li><strong>la surprime « zone à faibles émissions » de 1 000 €</strong>, supprimée avec la prime à la conversion le 2 décembre 2024.</li>
</ul>
<p>Subsiste en revanche la <strong>prime « non-casse » de la Région Île-de-France</strong>, jusqu’à 6 000 €, si vous faites transformer votre voiture thermique en électrique au lieu d’en acheter une autre.</p>""",
    exemple="""<h2 id="exemple">Exemple de calcul</h2>
<p>Un couple parisien avec un enfant (2,5 parts), 45 000 € de revenu fiscal de référence, soit 18 000 € par part, achète une électrique neuve à 32 000 € et fait détruire sa vieille diesel. Il est sous le plafond de 24 900 € par part et sous celui de 40 000 € : l’aide métropolitaine est ouverte, jusqu’à 6 000 €. Avec la prime d’État de la tranche « autres ménages » (3 300 à 3 314 €), le total peut approcher 9 300 €, soit près de 30 % du prix.</p>""",
    faq=[("Existe-t-il une aide de la Ville de Paris pour acheter une voiture électrique ?",
          "La Ville de Paris ne verse pas d’aide propre à l’achat d’une voiture pour les particuliers : c’est la Métropole du Grand Paris qui porte le dispositif, avec son aide « Métropole roule propre » pouvant atteindre 6 000 €."),
         ("Ma commune fait-elle partie du Grand Paris ?",
          "La Métropole du Grand Paris regroupe 131 communes : Paris et une grande partie des Hauts-de-Seine, de la Seine-Saint-Denis et du Val-de-Marne, ainsi que quelques communes de l’Essonne et du Val-d’Oise. La liste complète figure sur cette page, et le simulateur le vérifie automatiquement à partir de votre code postal."),
         ("La Région Île-de-France aide-t-elle encore à l’achat d’une voiture électrique ?",
          "Non, son aide à l’achat pour les particuliers a été supprimée le 2 mars 2025. Elle finance en revanche toujours la transformation d’un véhicule thermique en électrique, avec une prime « non-casse » pouvant atteindre 6 000 €."),
         ("Faut-il obligatoirement mettre une voiture à la casse ?",
          "Oui pour l’aide du Grand Paris : la destruction définitive d’une ancienne voiture, attestée par un centre de véhicules hors d’usage agréé, est une condition du règlement. Les aides nationales, elles, ne l’exigent plus depuis la fin de la prime à la conversion.")],
    sources=[("Métropole roule propre — metropolegrandparis.fr (règlement 2025)", "https://www.metropolegrandparis.fr/fr/metropole-roule-propre-0"),
             ("Fin de l’aide régionale — iledefrance.fr", "https://www.iledefrance.fr/toutes-les-faq/aides-vehicules-propres-faq"),
             ("Prime d’État — service-public.fr, fiche F39188", "https://www.service-public.gouv.fr/particuliers/vosdroits/F39188")],
))

T.append(dict(
    slug="lyon", city="Lyon", epci="200046977", indexable=True,
    title="Aide voiture électrique Lyon 2026 : 500 à 3 000 €",
    desc="La Métropole de Lyon verse 500 à 3 000 €, à condition de céder une Crit’Air 2, 3 ou 4 et de déposer le dossier avant l’achat sur Toodego.",
    h1="Quelles aides pour acheter une voiture électrique à Lyon en 2026 ?",
    lede="À Lyon, l’aide vient de la Métropole, elle va de 500 à 3 000 € — et elle a une particularité qui fait échouer beaucoup de dossiers : elle se demande avant l’achat.",
    answer="""<p><strong>Oui, de 500 à 3 000 €.</strong> La Métropole de Lyon aide les habitants et les personnes qui travaillent dans sa <strong>zone à faibles émissions</strong> à changer de voiture. Deux conditions déterminantes : un revenu fiscal de référence <strong>inférieur à 26 200 € par part</strong>, et surtout le fait de <strong>se séparer d’une voiture Crit’Air 2, 3 ou 4</strong> (destruction, vente ou transformation). Le dossier doit être déposé <strong>avant</strong> l’achat, sur demarches.toodego.com.</p>""",
    detail="""<h2 id="montants">Le montant de l’aide de la Métropole de Lyon</h2>
<p>De <strong>500 à 3 000 €</strong> selon vos revenus et la voiture choisie. Le barème détaillé est publié sur le guichet Toodego ; le simulateur affiche la fourchette plutôt qu’un chiffre unique, faute de barème complet publié.</p>
<h3>Les conditions à remplir</h3>
<ul>
<li><strong>Habiter ou travailler dans la zone à faibles émissions</strong> de la Métropole ;</li>
<li>revenu fiscal de référence <strong>inférieur à 26 200 € par part</strong> ;</li>
<li><strong>se séparer d’une voiture vignette Crit’Air 2, 3 ou 4</strong> : la destruction n’est pas la seule option, la vente ou la transformation en électrique sont acceptées — c’est plus souple que dans le Grand Paris ;</li>
<li>déposer la demande <strong>avant</strong> l’achat.</li>
</ul>
<p class="note note-warn"><strong>Une limite que nous assumons.</strong> La condition porte sur la zone à faibles émissions, dont le périmètre est <em>infra-communal</em> : il ne couvre pas l’intégralité de certaines communes. Le simulateur l’approxime à la commune entière. Vérifiez votre adresse précise sur le site de la Métropole avant de déposer votre dossier.</p>""",
    demarche="""<h2 id="demarches">Comment demander l’aide à Lyon</h2>
<ol>
<li>Faites la simulation, puis <strong>déposez votre demande sur demarches.toodego.com avant tout achat</strong> ;</li>
<li>attendez l’accord de principe ;</li>
<li>achetez la voiture ;</li>
<li>faites détruire, vendez ou faites transformer l’ancienne, puis transmettez les justificatifs.</li>
</ol>
<p class="note note-stop"><strong>L’erreur à ne pas commettre :</strong> une demande déposée après l’achat est refusée. Et comme la prime d’État doit elle aussi être demandée avant la signature du bon de commande, une seule signature prématurée fait tomber les deux aides.</p>
<h3>Les documents à préparer</h3>
<ul>
<li>Justificatif de domicile, ou justificatif de travail dans la zone à faibles émissions ;</li>
<li>dernier avis d’imposition ;</li>
<li>carte grise de l’ancienne voiture ;</li>
<li>devis de la nouvelle voiture ;</li>
<li>après l’achat : carte grise du nouveau véhicule, certificat de destruction ou de cession, facture, RIB.</li>
</ul>""",
    cumul="""<h2 id="cumul">Cumul avec les aides nationales</h2>
<p>L’aide de la Métropole de Lyon <strong>se cumule avec la prime d’État</strong>. Aucun plafond global de cumul n’est prévu par son règlement, contrairement à Strasbourg ou Rouen (80 % du prix). En revanche, la prime d’État et le leasing social restent exclusifs l’un de l’autre.</p>""",
    exemple="""<h2 id="exemple">Exemple de calcul</h2>
<p>Une personne seule habitant le 3<sup>e</sup> arrondissement de Lyon, 15 000 € de revenu fiscal de référence pour une part, revend sa Crit’Air 3 et achète une électrique neuve à 30 000 € chez un concessionnaire. Elle est dans la tranche 4 sur 10 : la prime d’État se situe entre 4 700 et 5 524 €, et l’aide métropolitaine s’y ajoute, entre 500 et 3 000 €. Total possible : de 5 200 à 8 500 €.</p>""",
    faq=[("Y a-t-il une aide de la Ville de Lyon pour une voiture électrique ?",
          "Non, la Ville de Lyon ne verse pas d’aide propre. Le dispositif est porté par la Métropole de Lyon, pour les habitants et les actifs de sa zone à faibles émissions, avec un montant de 500 à 3 000 €."),
         ("Faut-il détruire son ancienne voiture pour avoir l’aide à Lyon ?",
          "Pas nécessairement : la Métropole accepte la destruction, mais aussi la vente ou la transformation en électrique du véhicule Crit’Air 2, 3 ou 4 dont vous vous séparez. C’est une souplesse rare parmi les règlements locaux."),
         ("Puis-je demander l’aide si je travaille à Lyon sans y habiter ?",
          "Oui : le règlement vise les personnes qui habitent ou qui travaillent dans la zone à faibles émissions. Il faut alors fournir un justificatif d’activité dans le périmètre."),
         ("Puis-je cumuler l’aide de la Métropole de Lyon avec la prime d’État ?",
          "Oui, les deux se cumulent. Attention à l’ordre : la prime d’État se demande auprès du concessionnaire avant le bon de commande, et l’aide métropolitaine sur Toodego avant l’achat également.")],
    sources=[("Les aides pour l’achat d’un véhicule moins polluant — grandlyon.com (page mise à jour le 20/02/2026)", "https://www.grandlyon.com/mes-services-au-quotidien/se-deplacer/les-aides-pour-lachat-dun-vehicule-moins-polluant"),
             ("Guichet de dépôt — demarches.toodego.com", "https://demarches.toodego.com/"),
             ("Prime d’État — service-public.fr, fiche F39188", "https://www.service-public.gouv.fr/particuliers/vosdroits/F39188")],
))

T.append(dict(
    slug="marseille", city="Marseille", epci="200054807", commune_note="marseille", indexable=True,
    title="Aide voiture électrique Marseille 2026 : jusqu’à 5 000 €",
    desc="Aix-Marseille-Provence verse jusqu’à 5 000 € en neuf et 2 500 € en occasion aux habitants de la zone à faibles émissions de Marseille.",
    h1="Quelles aides pour acheter une voiture électrique à Marseille en 2026 ?",
    lede="L’aide existe, elle est parmi les plus généreuses de France pour les revenus très modestes — mais elle est réservée aux habitants de la zone à faibles émissions de Marseille, et exclut la location.",
    answer="""<p><strong>Oui, jusqu’à 5 000 € en neuf et 2 500 € en occasion.</strong> La Métropole Aix-Marseille-Provence réserve cette aide aux <strong>habitants de la zone à faibles émissions de Marseille</strong>. Il faut faire détruire une voiture <strong>Crit’Air 4, 5 ou non classée</strong>, acheter une <strong>électrique ou une voiture à hydrogène</strong> (les hybrides sont exclues) de moins de 47 000 €, et la garder deux ans. Le dispositif est ouvert jusqu’au <strong>31 octobre 2027</strong>.</p>""",
    detail="""<h2 id="montants">Le barème d’Aix-Marseille-Provence</h2>
""" + table(["Revenu fiscal par part", "Voiture neuve", "Voiture d’occasion"], [
        ['<td>jusqu’à 7 100 €</td>', '<td class="num">5 000 €</td>', '<td class="num">2 500 €</td>'],
        ['<td>de 7 100 à 15 400 €</td>', '<td class="num">3 000 €</td>', '<td class="num">1 500 €</td>'],
        ['<td>de 15 400 à 24 900 €</td>', '<td class="num">1 000 €</td>', '<td class="num">0 €</td>'],
        ['<td>au-delà de 24 900 €</td>', '<td class="num">—</td>', '<td class="num">—</td>'],
    ]) + """
<p>Ce barème est celui du règlement métropolitain d’octobre 2024, annexe « particuliers » ; aucune version plus récente n’a été trouvée à la date de vérification.</p>
<h3>Les conditions à remplir</h3>
<ul>
<li><strong>Habiter dans la zone à faibles émissions de Marseille</strong> ;</li>
<li>faire détruire une voiture <strong>Crit’Air 4, 5 ou non classée</strong>, entre 3 mois avant et 6 mois après l’achat ;</li>
<li>acheter une voiture <strong>électrique ou à hydrogène</strong> — les hybrides ne sont pas éligibles, contrairement au Grand Paris ou à Toulouse ;</li>
<li>prix inférieur ou égal à 47 000 € ;</li>
<li>pour une occasion, <strong>achat chez un professionnel</strong> obligatoire ;</li>
<li><strong>la location longue durée et la location avec option d’achat sont exclues</strong> — donc pas de cumul possible avec le leasing social ;</li>
<li>conserver la voiture 2 ans.</li>
</ul>
<p class="note note-warn">La zone à faibles émissions ne couvre qu’une partie de Marseille. Le simulateur l’approxime à la commune entière : vérifiez votre adresse sur le site de la Métropole avant de déposer un dossier.</p>""",
    demarche="""<h2 id="demarches">Comment demander l’aide à Marseille</h2>
<p>Dépôt du dossier <strong>après l’achat</strong>, dans les 6 mois, sur subvention.ampmetropole.fr. Documents : carte grise du nouveau véhicule, facture, justificatif de domicile dans la zone, dernier avis d’imposition, certificat de destruction de l’ancienne voiture et RIB.</p>""",
    cumul="""<h2 id="cumul">Cumul, et le cas des autres communes des Bouches-du-Rhône</h2>
<p>L’aide se cumule avec la prime d’État. Elle est en revanche <strong>incompatible avec le leasing social</strong>, puisque la location est exclue du règlement.</p>
<p class="note note-stop"><strong>Hors Marseille, il n’y a plus rien.</strong> L’aide du Département des Bouches-du-Rhône (5 000 €) est terminée : les achats postérieurs au 31 janvier 2022 en sont exclus. Un habitant d’Aix-en-Provence, de Martigues ou d’Aubagne ne peut donc compter que sur les aides nationales — la fiche gouvernementale régionale qui mentionne encore ces aides est périmée.</p>""",
    exemple="""<h2 id="exemple">Exemple de calcul</h2>
<p>Une personne seule habitant le 1<sup>er</sup> arrondissement de Marseille, 6 000 € de revenu fiscal de référence pour une part, fait détruire une Crit’Air 4 et achète une électrique neuve à 30 000 € : <strong>5 000 €</strong> d’aide métropolitaine, auxquels s’ajoute la prime d’État de la tranche « revenus très modestes » (5 082 à 5 700 €). Total possible : plus de 10 000 €, soit un tiers du prix.</p>""",
    faq=[("Qui peut bénéficier de l’aide d’Aix-Marseille-Provence ?",
          "Les habitants de la zone à faibles émissions de Marseille, avec un revenu fiscal de référence par part inférieur ou égal à 24 900 €, qui font détruire une voiture Crit’Air 4, 5 ou non classée et achètent une voiture électrique ou à hydrogène de moins de 47 000 €."),
         ("Habitant d’Aix-en-Provence, ai-je droit à une aide ?",
          "Non, pas d’aide locale : l’aide métropolitaine est réservée aux résidents de la zone à faibles émissions de Marseille, et l’aide du Département des Bouches-du-Rhône est terminée depuis le 31 janvier 2022. Restent les aides nationales, que le simulateur calcule."),
         ("Puis-je avoir l’aide pour une hybride rechargeable ?",
          "Non. Contrairement à d’autres métropoles, Aix-Marseille-Provence réserve son aide aux voitures électriques et à hydrogène. Les hybrides, même rechargeables, en sont exclues."),
         ("L’aide fonctionne-t-elle avec une location longue durée ?",
          "Non, la location longue durée et la location avec option d’achat sont explicitement exclues du règlement. Si vous visez le leasing social, vous ne pourrez pas y ajouter l’aide métropolitaine.")],
    sources=[("Règlement des aides aux particuliers — Métropole Aix-Marseille-Provence (annexe, aides ouvertes jusqu’au 31/10/2027)", "https://ampmetropole.fr/wp-content/uploads/2024/11/96120_Annexe-1-2-particulier-1.pdf"),
             ("Guichet de dépôt — subvention.ampmetropole.fr", "https://subvention.ampmetropole.fr/"),
             ("Fiche gouvernementale PACA (périmée pour le Département 13)", "https://jechangemavoiture.gouv.fr/jcmv/simulateur/assets/media/aides-locales/provence-alpes-cote-d-azur.pdf")],
))

T.append(dict(
    slug="toulouse", city="Toulouse", epci="243100518", indexable=True,
    title="Aide voiture électrique Toulouse 2026 : jusqu’à 5 000 €",
    desc="Prime « véhicule + propre » : 3 000 à 5 000 € en neuf, 2 000 à 3 300 € en occasion, achat à un particulier accepté, cumul avec l’éco-chèque régional.",
    h1="Quelles aides pour acheter une voiture électrique à Toulouse en 2026 ?",
    lede="Toulouse est le territoire le plus favorable de France au cumul : la prime métropolitaine, l’éco-chèque régional et la prime d’État peuvent s’additionner — et l’achat à un particulier reste accepté.",
    answer="""<p><strong>Oui, de 2 000 à 5 000 €.</strong> La prime « véhicule + propre » de Toulouse Métropole est ouverte jusqu’à un revenu fiscal de <strong>35 052 € par part</strong>, un plafond bien plus haut qu’ailleurs. Il faut faire détruire une voiture <strong>Crit’Air 3, 4, 5 ou non classée</strong> possédée depuis au moins un an. Particularité : <strong>l’achat à un particulier est accepté</strong>, et la location aussi.</p>""",
    detail="""<h2 id="montants">Le barème de Toulouse Métropole</h2>
""" + table(["Revenu fiscal par part", "Voiture neuve", "Voiture d’occasion"], [
        ['<td>moins de 6 300 €</td>', '<td class="num">5 000 €</td>', '<td class="num">3 300 €</td>'],
        ['<td>moins de 14 089 €</td>', '<td class="num">4 500 €</td>', '<td class="num">3 000 €</td>'],
        ['<td>moins de 18 800 €</td>', '<td class="num">4 000 €</td>', '<td class="num">2 700 €</td>'],
        ['<td>moins de 35 052 €</td>', '<td class="num">3 000 €</td>', '<td class="num">2 000 €</td>'],
    ]) + """
<h3>Les conditions à remplir</h3>
<ul>
<li>Habiter l’une des communes de Toulouse Métropole ;</li>
<li>faire détruire une voiture <strong>Crit’Air 3, 4, 5 ou non classée</strong>, possédée depuis au moins un an, entre 3 mois avant et 6 mois après l’achat ;</li>
<li>acheter une voiture <strong>Crit’Air 0 ou 1</strong> : électrique, hybride, hydrogène ou gaz — le périmètre le plus large des règlements que nous avons vérifiés ;</li>
<li>une seule voiture par personne.</li>
</ul>
<p class="note note-ok"><strong>Deux souplesses rares :</strong> l’achat auprès d’un particulier est accepté, et la location aussi. C’est important, car un achat entre particuliers vous prive de toute prime d’État : à Toulouse, il vous reste malgré tout la prime métropolitaine.</p>""",
    demarche="""<h2 id="demarches">Comment demander la prime « véhicule + propre »</h2>
<p>Dépôt <strong>après l’achat</strong>, sur demarches-tm.eservices.toulouse-metropole.fr, avec la facture (ou l’acte de vente Cerfa 15776 en cas d’achat à un particulier), la carte grise à votre nom, le certificat de destruction de l’ancienne voiture, votre avis d’imposition, un justificatif de domicile et un RIB.</p>""",
    cumul="""<h2 id="cumul">Le triple cumul toulousain</h2>
<p>Le règlement le précise explicitement : la prime de Toulouse Métropole <strong>se cumule avec les aides de l’État et avec l’éco-chèque mobilité de la Région Occitanie</strong>.</p>
<ul>
<li><strong>Prime d’État</strong> : 3 300 à 7 700 € en neuf, si achat chez un professionnel partenaire ;</li>
<li><strong>éco-chèque Occitanie</strong> : 30 % du prix, jusqu’à 1 600 €, pour une <a href="/aides-voiture-electrique/occitanie/">voiture électrique d’occasion</a> achetée chez un professionnel agréé en Occitanie par un ménage non imposable ;</li>
<li><strong>prime métropolitaine</strong> : 2 000 à 5 000 €.</li>
</ul>""",
    exemple="""<h2 id="exemple">Exemple de calcul</h2>
<p>Un ménage toulousain non imposable, 12 000 € de revenu fiscal par part, fait détruire sa Crit’Air 4 et achète une électrique d’occasion à 15 000 € chez un professionnel agréé en Occitanie : <strong>3 000 €</strong> de prime métropolitaine + <strong>1 600 €</strong> d’éco-chèque régional (30 % plafonnés), soit 4 600 € d’aides locales, avant la prime d’État occasion. Près d’un tiers du prix du véhicule.</p>""",
    faq=[("Quel revenu maximum pour la prime de Toulouse Métropole ?",
          "Le plafond est de 35 052 € de revenu fiscal de référence par part, très supérieur à celui des autres métropoles (24 900 € dans le Grand Paris, 26 200 € à Lyon et Strasbourg). La prime reste donc accessible à des ménages aux revenus intermédiaires."),
         ("Puis-je acheter à un particulier et garder la prime ?",
          "Oui pour la prime de Toulouse Métropole, qui accepte l’achat auprès d’un particulier. En revanche vous perdrez la prime d’État et l’éco-chèque d’Occitanie, tous deux conditionnés à un vendeur professionnel."),
         ("Une hybride est-elle éligible à Toulouse ?",
          "Oui, à condition qu’elle soit classée Crit’Air 0 ou 1. Le règlement toulousain accepte l’électrique, l’hybride, l’hydrogène et le gaz — un périmètre plus large que la plupart des autres métropoles."),
         ("Peut-on cumuler la prime de Toulouse et l’éco-chèque d’Occitanie ?",
          "Oui, le cumul est prévu explicitement par le règlement métropolitain. L’éco-chèque régional ne concerne toutefois que les voitures électriques d’occasion achetées chez un professionnel agréé en Occitanie, par un ménage non imposable.")],
    sources=[("Prime « véhicule + propre » — metropole.toulouse.fr", "https://metropole.toulouse.fr/demarches/demander-la-prime-vehicule-propre"),
             ("Éco-chèque mobilité — laregion.fr (page mise à jour le 23/07/2026)", "https://www.laregion.fr/Eco-cheque-mobilite-voiture-electrique-ou-hybride"),
             ("Prime d’État — service-public.fr, fiche F39188", "https://www.service-public.gouv.fr/particuliers/vosdroits/F39188")],
))

T.append(dict(
    slug="strasbourg", city="Strasbourg", epci="246700488", indexable=True,
    title="Aide voiture électrique Strasbourg 2026 : 2 000 à 4 000 €",
    desc="L’Eurométropole verse 2 000 à 4 000 € selon vos revenus pour une Crit’Air 0 ou 1, achat entre particuliers accepté. Cumul plafonné à 80 % du prix.",
    h1="Quelles aides pour acheter une voiture électrique à Strasbourg en 2026 ?",
    lede="Strasbourg applique un barème clair à trois tranches, accepte l’achat entre particuliers et n’impose pas la destruction du véhicule cédé — mais plafonne le total des aides publiques à 80 % du prix.",
    answer="""<p><strong>Oui, 2 000, 3 000 ou 4 000 €</strong> selon votre revenu fiscal par part. L’aide à la conversion de l’Eurométropole finance une voiture <strong>Crit’Air 0 ou 1</strong>, neuve ou d’occasion, achetée <strong>à un professionnel comme à un particulier</strong>. Il faut <strong>vendre ou faire détruire</strong> une voiture Crit’Air 2 ou plus ancienne, possédée depuis au moins un an.</p>""",
    detail="""<h2 id="montants">Le barème de l’Eurométropole de Strasbourg</h2>
""" + table(["Revenu fiscal par part", "Montant de l’aide"], [
        ['<td>moins de 7 500 €</td>', '<td class="num">4 000 €</td>'],
        ['<td>de 7 500 à 16 300 €</td>', '<td class="num">3 000 €</td>'],
        ['<td>de 16 300 à 26 200 €</td>', '<td class="num">2 000 €</td>'],
        ['<td>26 200 € et au-delà</td>', '<td class="num">aucune aide</td>'],
    ]) + """
<h3>Les conditions à remplir</h3>
<ul>
<li>Habiter l’une des communes de l’Eurométropole ;</li>
<li><strong>céder une voiture Crit’Air 2, 3, 4, 5 ou non classée</strong>, possédée depuis au moins un an — la vente suffit, la destruction n’est pas obligatoire ;</li>
<li>cession réalisée entre 3 mois avant et 6 mois après l’achat ;</li>
<li>acheter une voiture <strong>Crit’Air 0 ou 1</strong>, neuve ou d’occasion ;</li>
<li>en location, contrat d’au moins 24 mois.</li>
</ul>
<p class="note note-warn">Le règlement en vigueur date du 1<sup>er</sup> janvier 2025 et <strong>aucune date de fin n’est publiée</strong> : sa reconduction en 2026 n’est pas confirmée noir sur blanc. Vérifiez l’ouverture du guichet avant d’acheter.</p>""",
    demarche="""<h2 id="demarches">Comment demander l’aide à Strasbourg</h2>
<p>Dépôt du dossier sur aides.strasbourg.eu, <strong>au plus tard 6 mois après l’achat</strong>. Prévoyez la facture ou l’acte de vente, la carte grise du nouveau véhicule, le justificatif de cession ou de destruction de l’ancien, un justificatif de domicile, votre avis d’imposition et un RIB.</p>""",
    cumul="""<h2 id="cumul">Le plafond des 80 %</h2>
<p>L’aide se cumule avec la prime d’État, mais <strong>le total de toutes les aides publiques ne peut pas dépasser 80 % du prix de la voiture</strong>. Sur un véhicule d’occasion bon marché, c’est ce plafond qui limite le montant final : le simulateur applique automatiquement cet écrêtement et affiche la mention « montant réduit ».</p>
<p>À noter également : l’Eurométropole ajoute <strong>2 500 € sans condition de revenus</strong> pour la transformation d’une voiture thermique en électrique (rétrofit).</p>""",
    exemple="""<h2 id="exemple">Exemple de calcul</h2>
<p>Un ménage strasbourgeois avec 12 000 € de revenu fiscal par part cède sa Crit’Air 2 et achète une électrique d’occasion à 12 000 € : <strong>3 000 €</strong> d’aide métropolitaine. Le plafond de 80 % (soit 9 600 €) n’est pas atteint. Si le même ménage achetait une occasion à 5 000 €, le total des aides serait ramené à 4 000 €.</p>""",
    faq=[("Faut-il détruire son ancienne voiture à Strasbourg ?",
          "Non, la vente suffit. L’Eurométropole demande de céder une voiture Crit’Air 2 ou plus ancienne, possédée depuis au moins un an, entre 3 mois avant et 6 mois après l’achat — la destruction n’est qu’une des options."),
         ("Puis-je acheter à un particulier ?",
          "Oui, le règlement l’accepte, ce qui est rare. Vous perdrez en revanche la prime d’État, réservée aux achats chez un professionnel partenaire d’un fournisseur d’énergie."),
         ("Que signifie le plafond de 80 % ?",
          "Le total de toutes les aides publiques perçues pour ce véhicule ne peut pas dépasser 80 % de son prix. Si la prime d’État et l’aide métropolitaine dépassent ce seuil, c’est l’aide métropolitaine qui est réduite."),
         ("L’aide existe-t-elle toujours en 2026 ?",
          "Le règlement en vigueur depuis le 1er janvier 2025 ne comporte pas de date de fin publiée. Nous affichons donc la règle comme applicable, tout en signalant que sa reconduction en 2026 n’est pas confirmée explicitement par la page officielle.")],
    sources=[("Aides à la conversion — strasbourg.eu (règlement en vigueur depuis le 01/01/2025)", "https://www.strasbourg.eu/aides-conversion"),
             ("Guichet de dépôt — aides.strasbourg.eu", "https://aides.strasbourg.eu/"),
             ("Prime d’État — service-public.fr, fiche F39188", "https://www.service-public.gouv.fr/particuliers/vosdroits/F39188")],
))

T.append(dict(
    slug="rouen", city="Rouen", epci="200023414", indexable=True,
    title="Aide voiture électrique Rouen 2026 : 2 000 à 5 000 €",
    desc="La Métropole Rouen Normandie verse 2 000 à 4 000 € selon vos revenus, majorés de 25 % en zone à faibles émissions. Règlement valable jusqu’en 2027.",
    h1="Quelles aides pour acheter une voiture électrique à Rouen en 2026 ?",
    lede="Rouen combine un barème par tranches de revenus et une majoration de 25 % pour les communes de sa zone à faibles émissions. Le dispositif court jusqu’au 30 juin 2027, avec une facture avant fin 2026.",
    answer="""<p><strong>Oui, de 2 000 à 5 000 €.</strong> L’aide de la Métropole Rouen Normandie s’adresse aux ménages jusqu’à <strong>22 000 € de revenu fiscal par part</strong>, qui font <strong>détruire une voiture diesel d’avant 2011 ou essence d’avant 2006</strong> et achètent une voiture <strong>Crit’Air 0 ou 1 chez un professionnel</strong>. La majoration de 25 % s’applique dans les communes de la zone à faibles émissions.</p>""",
    detail="""<h2 id="montants">Le barème de la Métropole Rouen Normandie</h2>
""" + table(["Revenu fiscal par part", "Montant", "Avec la majoration zone à faibles émissions"], [
        ['<td>jusqu’à 7 100 €</td>', '<td class="num">4 000 €</td>', '<td class="num">jusqu’à 5 000 €</td>'],
        ['<td>de 7 100 à 15 400 €</td>', '<td class="num">3 000 €</td>', '<td class="num">3 750 €</td>'],
        ['<td>de 15 400 à 22 000 €</td>', '<td class="num">2 000 €</td>', '<td class="num">2 500 €</td>'],
    ]) + """
<p class="note note-warn">La majoration de 25 % (plafonnée à 5 000 €) est réservée aux habitants des communes de la zone à faibles émissions. <strong>Nous ne la calculons pas automatiquement</strong> : la liste officielle de ces communes n’est pas embarquée dans le simulateur. Le montant affiché est donc une fourchette entre le montant de base et le montant majoré.</p>
<h3>Les conditions à remplir</h3>
<ul>
<li>Faire détruire une voiture <strong>diesel d’avant 2011 ou essence d’avant 2006</strong> (Crit’Air 3 ou plus ancienne) ;</li>
<li>acheter <strong>chez un professionnel</strong> — l’achat à un particulier est exclu ;</li>
<li>voiture neuve (moins de 6 mois) ou d’occasion, <strong>Crit’Air 0 ou 1</strong> ;</li>
<li>prix inférieur à 60 000 € pour une électrique, 50 000 € sinon ;</li>
<li>en location, contrat d’au moins 24 mois ;</li>
<li><strong>facture avant le 31 décembre 2026</strong>, dispositif ouvert jusqu’au 30 juin 2027.</li>
</ul>""",
    demarche="""<h2 id="demarches">Comment demander l’aide à Rouen</h2>
<p>Dépôt sur demarches.metropole-rouen-normandie.fr, <strong>dans les 6 mois suivant la facture</strong>. Documents : facture, carte grise, certificat de destruction, avis d’imposition, justificatif de domicile, RIB.</p>""",
    cumul="""<h2 id="cumul">Cumul : deux règles à connaître</h2>
<ul>
<li><strong>Plafond de 80 %</strong> : le total des aides publiques ne peut pas dépasser 80 % du prix de la voiture. Le simulateur écrête automatiquement.</li>
<li><strong>Pas de cumul avec le leasing social</strong> : le règlement l’exclut explicitement. Il faut choisir entre l’aide métropolitaine (avec la prime d’État à l’achat) et le leasing social.</li>
</ul>
<p>La Métropole ajoute par ailleurs <strong>2 000 € sans condition de revenus</strong> pour la transformation d’un véhicule thermique en électrique.</p>
<p>Vous habitez la Seine-Maritime mais pas la Métropole ? Voir <a href="/aides-voiture-electrique/seine-maritime/">l’aide du Département de la Seine-Maritime</a>.</p>""",
    exemple="""<h2 id="exemple">Exemple de calcul avec écrêtement</h2>
<p>Un ménage rouennais très modeste (6 000 € de revenu fiscal par part) fait détruire sa vieille diesel et achète une électrique d’occasion à <strong>10 000 €</strong>. L’aide métropolitaine est de 4 000 €, la prime d’État s’y ajoute — mais le plafond de 80 % limite le total des aides publiques à 8 000 €. L’aide métropolitaine est donc réduite pour respecter ce plafond, ce que le simulateur indique par la mention « montant réduit ».</p>""",
    faq=[("Quelle est la majoration « zone à faibles émissions » à Rouen ?",
          "Les habitants des communes de la zone à faibles émissions bénéficient d’une majoration de 25 % de l’aide, dans la limite de 5 000 €. La liste de ces communes figure sur le site de la Métropole ; nous ne l’appliquons pas automatiquement, faute de liste officielle exploitable."),
         ("Puis-je cumuler l’aide de Rouen avec le leasing social ?",
          "Non, le règlement de la Métropole exclut explicitement ce cumul. Vous pouvez en revanche cumuler l’aide métropolitaine avec la prime d’État « Coup de pouce » en cas d’achat."),
         ("Jusqu’à quand l’aide est-elle disponible ?",
          "Le règlement du 29 septembre 2025 court jusqu’au 30 juin 2027, avec une condition importante : la facture du véhicule doit être établie avant le 31 décembre 2026."),
         ("Quels véhicules faut-il mettre à la casse ?",
          "Une voiture diesel immatriculée avant 2011 ou essence avant 2006, c’est-à-dire une Crit’Air 3 ou plus ancienne. La destruction doit être réalisée dans un centre agréé.")],
    sources=[("Règlement du 29/09/2025 — zfe.metropole-rouen-normandie.fr", "https://zfe.metropole-rouen-normandie.fr/sites/default/files/2025-10/B2025_0429_annexe.pdf"),
             ("Guichet de dépôt — demarches.metropole-rouen-normandie.fr", "https://demarches.metropole-rouen-normandie.fr/"),
             ("Prime d’État — service-public.fr, fiche F39188", "https://www.service-public.gouv.fr/particuliers/vosdroits/F39188")],
))

T.append(dict(
    slug="bordeaux", city="Bordeaux", epci="243300316", indexable=True,
    title="Aide voiture électrique Bordeaux 2026 : jusqu’à 6 000 €",
    desc="Bordeaux Métropole annonce jusqu’à 6 000 € pour remplacer un véhicule non classé. Ce qui est vérifié, et ce qui reste à confirmer au guichet.",
    h1="Quelles aides pour acheter une voiture électrique à Bordeaux en 2026 ?",
    lede="Bordeaux Métropole a ouvert son guichet en janvier 2025 et annonce « jusqu’à 6 000 € ». Nous n’avons pas trouvé le barème détaillé sur la page officielle : voici exactement ce qui est établi, et ce qui ne l’est pas.",
    answer="""<p><strong>Oui, une aide existe, annoncée « jusqu’à 6 000 € ».</strong> Elle suppose de <strong>vendre ou faire détruire une voiture non classée</strong> (trop ancienne pour une vignette Crit’Air) et d’acheter une électrique — une Crit’Air 1 n’est acceptée qu’en occasion. <strong>Le barème par tranches de revenus et le plafond de revenus ne sont pas publiés</strong> sur la page officielle consultée : le montant réel doit être vérifié sur le guichet.</p>""",
    detail="""<h2 id="montants">Ce qui est établi, et ce qui ne l’est pas</h2>
""" + table(["Élément", "Statut"], [
        ['<td>Existence de l’aide et guichet ouvert depuis le 1<sup>er</sup> janvier 2025</td>', '<td><span class="badge badge-ok">vérifié</span></td>'],
        ['<td>Mise au rebut ou cession d’un véhicule non classé exigée</td>', '<td><span class="badge badge-ok">vérifié</span></td>'],
        ['<td>Crit’Air 1 acceptée uniquement pour une occasion</td>', '<td><span class="badge badge-ok">vérifié</span></td>'],
        ['<td>Montant « jusqu’à 6 000 € »</td>', '<td><span class="badge badge-warn">presse de décembre 2024, non confirmé par la page officielle</span></td>'],
        ['<td>Barème par tranches de revenus, plafond de revenus</td>', '<td><span class="badge badge-stop">non publié sur la page consultée</span></td>'],
    ]) + """
<p class="note note-warn">Nous préférons afficher cette incertitude plutôt qu’un montant inventé. Le simulateur classe cette aide comme « à confirmer » et n’en additionne que la borne haute au total, en le signalant.</p>""",
    demarche="""<h2 id="demarches">Comment demander l’aide à Bordeaux</h2>
<p>Le dépôt se fait sur mesdemarches.bordeaux-metropole.fr, guichet ouvert depuis le 1<sup>er</sup> janvier 2025, après l’achat. Demandez le règlement complet et le barème avant d’acheter : c’est la seule façon d’obtenir un montant fiable aujourd’hui.</p>""",
    cumul="""<h2 id="cumul">Cumul</h2>
<p>Comme les autres aides locales, elle se cumule avec la prime d’État. Aucun plafond global de cumul n’a été identifié dans les documents consultés.</p>""",
    exemple="",
    faq=[("Quel est le montant exact de l’aide de Bordeaux Métropole ?",
          "Le montant maximal annoncé est de 6 000 €, mais il provient d’articles de presse de décembre 2024 : le barème détaillé selon les revenus n’est pas publié sur la page officielle que nous avons consultée. Demandez le règlement au guichet métropolitain avant d’acheter."),
         ("Quel véhicule faut-il mettre au rebut ?",
          "Un véhicule non classé, c’est-à-dire trop ancien pour recevoir une vignette Crit’Air. La cession comme la destruction sont acceptées."),
         ("Une hybride est-elle éligible à Bordeaux ?",
          "Pour un véhicule neuf, l’aide est réservée à l’électrique. Une Crit’Air 1, donc certaines hybrides ou essences récentes, n’est acceptée que pour un achat d’occasion.")],
    sources=[("Zone à faibles émissions — sedeplacer.bordeaux-metropole.fr", "https://sedeplacer.bordeaux-metropole.fr/en-voiture/zfe-ce-quil-faut-savoir"),
             ("Guichet de dépôt — mesdemarches.bordeaux-metropole.fr", "https://mesdemarches.bordeaux-metropole.fr/"),
             ("Prime d’État — service-public.fr, fiche F39188", "https://www.service-public.gouv.fr/particuliers/vosdroits/F39188")],
))

T.append(dict(
    slug="reims", city="Reims", epci="200067213", indexable=True,
    title="Aide voiture électrique Reims 2026 : 2 000 à 6 000 €",
    desc="Le Grand Reims aide au changement de véhicule dans sa zone à faibles émissions. Les sources publiques se contredisent : voici ce qui est établi.",
    h1="Quelles aides pour acheter une voiture électrique à Reims en 2026 ?",
    lede="Le Grand Reims verse une aide au changement de voiture liée à sa zone à faibles émissions. Les montants publiés par les sources secondaires se contredisent, et nous le disons plutôt que de trancher à leur place.",
    answer="""<p><strong>Oui, une aide existe</strong> pour les habitants ou salariés de la zone à faibles émissions du Grand Reims, à condition de faire détruire une voiture <strong>Crit’Air 3, 4, 5 ou non classée</strong>. Les montants annoncés vont de <strong>2 000 à 6 000 €</strong> selon les sources — qui ne concordent pas. Une seule voiture par foyer.</p>""",
    detail="""<h2 id="montants">Pourquoi nous affichons une fourchette large</h2>
<p>Les pages officielles du Grand Reims et de la Ville de Reims étaient <strong>inaccessibles lors de notre vérification</strong>. Les sources secondaires disponibles donnent deux versions incompatibles :</p>
<ul>
<li>2 000 à 3 000 € pour les ménages disposant de moins de 13 489 € de revenu fiscal par part, dans la limite de 40 % du prix ;</li>
<li>2 000 à 6 000 € selon un autre barème.</li>
</ul>
<p class="note note-warn">Nous affichons donc l’aide comme « à confirmer », avec la fourchette complète. Avant tout achat, demandez le règlement d’attribution en vigueur au Grand Reims : c’est la seule source qui fasse foi.</p>
<h3>Ce qui est établi</h3>
<ul>
<li>Aide réservée aux <strong>habitants ou salariés de la zone à faibles émissions</strong> — nous l’approximons au territoire du Grand Reims ;</li>
<li>destruction d’une voiture <strong>Crit’Air 3 ou plus ancienne</strong> ;</li>
<li>une seule voiture par foyer.</li>
</ul>""",
    demarche="""<h2 id="demarches">Où déposer le dossier</h2>
<p>Le guichet dépend de la collectivité (Grand Reims ou Ville de Reims selon les sources) : à confirmer directement auprès de la collectivité, avec le règlement en vigueur.</p>""",
    cumul="""<h2 id="cumul">Cumul</h2>
<p>L’aide se cumule avec la prime d’État. Attention toutefois au plafond de 40 % du prix mentionné par l’une des sources : s’il est confirmé, il limite fortement l’aide sur les véhicules d’occasion bon marché.</p>""",
    exemple="",
    faq=[("Quel est le montant de l’aide du Grand Reims ?",
          "Les sources publiques disponibles se contredisent : de 2 000 à 3 000 € selon l’une, jusqu’à 6 000 € selon l’autre. Les pages officielles étaient inaccessibles lors de notre vérification. Demandez le règlement en vigueur à la collectivité avant d’acheter."),
         ("Faut-il habiter la zone à faibles émissions de Reims ?",
          "L’aide vise les habitants ou les salariés de la zone à faibles émissions. Comme le périmètre est infra-communal, nous l’approximons au territoire du Grand Reims et le signalons dans le résultat."),
         ("Combien de véhicules par foyer ?",
          "Une seule voiture par foyer, selon les sources consultées.")],
    sources=[("Grand Reims — grandreims.fr (page inaccessible lors de la vérification)", "https://www.grandreims.fr/"),
             ("Prime d’État — service-public.fr, fiche F39188", "https://www.service-public.gouv.fr/particuliers/vosdroits/F39188")],
))

T.append(dict(
    slug="grenoble", city="Grenoble", epci="200040715", indexable=True, status="suspended",
    title="Aide voiture électrique Grenoble : dispositif suspendu",
    desc="L’aide de Grenoble-Alpes Métropole est suspendue depuis le 26 septembre 2025. Ce qui reste possible et le barème applicable en cas de reprise.",
    h1="Aide voiture électrique à Grenoble : où en est-on en 2026 ?",
    lede="C’est l’information que personne n’affiche clairement : l’aide de Grenoble-Alpes Métropole est suspendue depuis le 26 septembre 2025. Voici ce qu’il vous reste, et ce qui reprendrait si le dispositif rouvrait.",
    answer="""<p><strong>Non, pas actuellement.</strong> L’aide au renouvellement de véhicule de Grenoble-Alpes Métropole est <strong>suspendue depuis le 26 septembre 2025</strong>, sans date de reprise annoncée. Les habitants de la métropole grenobloise ne peuvent donc compter, à ce jour, que sur les <a href="/aides-voiture-electrique-2026/">aides nationales</a> — qui restent substantielles.</p>""",
    detail="""<h2 id="montants">Le barème qui s’appliquerait en cas de reprise</h2>
<p>Le règlement de juin 2025, toujours publié, prévoyait :</p>
""" + table(["Revenu fiscal par part", "Montant"], [
        ['<td>moins de 16 300 €</td>', '<td class="num">3 500 €</td>'],
        ['<td>de 16 300 à 26 200 €</td>', '<td class="num">2 500 €</td>'],
        ['<td>26 200 € et au-delà</td>', '<td class="num">aucune aide</td>'],
    ]) + """
<p>Avec les conditions suivantes : destruction d’une voiture Crit’Air 3 ou plus ancienne possédée depuis au moins un an, limite de poids du véhicule acheté, neuf ou occasion acceptés, location d’au moins 3 ans acceptée, entretien mobilité préalable.</p>
<p class="note note-stop">Le simulateur affiche cette aide comme <strong>suspendue</strong> et ne l’ajoute jamais au total. Nous préférons le dire clairement : construire un budget d’achat sur une aide suspendue est le meilleur moyen de se retrouver à découvert.</p>""",
    demarche="""<h2 id="demarches">Que faire aujourd’hui à Grenoble</h2>
<ul>
<li>Surveiller la page « aides et parcours » de la zone à faibles émissions de la Métropole, qui annoncera une éventuelle reprise ;</li>
<li>mobiliser les aides nationales, qui ne dépendent pas de la collectivité : <a href="/prime-coup-de-pouce-voiture-electrique/">prime « Coup de pouce »</a> ou <a href="/leasing-social-2026/">leasing social</a> ;</li>
<li>si vous envisagez de transformer votre voiture thermique en électrique, la prime nationale au rétrofit reste accessible jusqu’à 5 000 €.</li>
</ul>""",
    cumul="",
    exemple="",
    faq=[("L’aide de Grenoble-Alpes Métropole va-t-elle reprendre ?",
          "Aucune date de reprise n’a été annoncée sur la page officielle de la Métropole à la date de vérification de cette page. Nous mettrons cette page à jour dès qu’une décision sera publiée ; elle est également consignée dans notre historique des changements."),
         ("Puis-je déposer un dossier malgré la suspension ?",
          "Non. La suspension signifie que le guichet ne traite plus de nouvelles demandes. Seules les aides nationales restent mobilisables pour un achat aujourd’hui."),
         ("Quelles aides restent disponibles à Grenoble en 2026 ?",
          "La prime d’État « Coup de pouce » pour une voiture électrique neuve (3 300 à 7 700 € selon vos revenus), le leasing social si vous roulez pour travailler avec un revenu fiscal inférieur à 16 880 € par part, la prime pour une électrique d’occasion depuis septembre 2026, et la prime au rétrofit.")],
    sources=[("Aides et parcours — zfe.grenoblealpesmetropole.fr (« actuellement suspendu depuis le 26/09/2025 »)", "https://zfe.grenoblealpesmetropole.fr/684-aides-et-parcours.htm"),
             ("Prime d’État — service-public.fr, fiche F39188", "https://www.service-public.gouv.fr/particuliers/vosdroits/F39188")],
))

T.append(dict(
    slug="annecy", city="Annecy", epci="200066793", indexable=True,
    title="Aide voiture électrique Annecy 2026 : 3 000 € du Grand Annecy",
    desc="Le Grand Annecy verse 3 000 € pour remplacer une voiture non classée par une électrique. Dossier à déposer avant la commande, revenu ≤ 16 300 €/part.",
    h1="Quelles aides pour acheter une voiture électrique à Annecy en 2026 ?",
    lede="Le Grand Annecy verse un forfait de 3 000 €, simple à comprendre — mais avec deux conditions strictes : un véhicule non classé à détruire, et un dossier déposé avant la commande.",
    answer="""<p><strong>Oui, 3 000 €.</strong> L’aide au renouvellement de voiture du Grand Annecy est un forfait, pour une voiture neuve comme d’occasion. Conditions : revenu fiscal <strong>inférieur à 16 300 € par part</strong>, destruction d’une voiture <strong>non classée</strong> (trop ancienne pour une vignette Crit’Air), et <strong>dossier déposé avant la commande</strong>.</p>""",
    detail="""<h2 id="montants">Les conditions du Grand Annecy</h2>
<ul>
<li><strong>3 000 €</strong>, forfaitaires, neuf ou occasion ;</li>
<li>revenu fiscal de référence <strong>inférieur à 16 300 € par part</strong> ;</li>
<li>faire détruire une voiture <strong>non classée</strong> — la condition la plus stricte de tous les règlements que nous avons vérifiés : une Crit’Air 3 ou 4 ne suffit pas ;</li>
<li>pour une voiture neuve : <strong>électrique ou hydrogène uniquement</strong>. Une Crit’Air 1 n’est acceptée qu’en occasion ;</li>
<li>en location, contrat d’au moins 24 mois ;</li>
<li>conserver la voiture 2 ans ;</li>
<li>le total des aides ne peut pas dépasser le prix de la voiture.</li>
</ul>""",
    demarche="""<h2 id="demarches">Comment demander l’aide à Annecy</h2>
<p class="note note-stop"><strong>Le dossier doit être déposé avant la commande ou la signature du contrat.</strong> C’est, avec Lyon, l’un des deux territoires où une demande postérieure à l’achat est refusée sans recours.</p>
<ol>
<li>Déposez la demande sur grandannecy.fr ;</li>
<li>attendez l’accord ;</li>
<li>commandez la voiture ;</li>
<li>faites détruire l’ancienne et transmettez la facture, la carte grise et le certificat de destruction.</li>
</ol>""",
    cumul="""<h2 id="cumul">Cumul</h2>
<p>L’aide se cumule avec la prime d’État, dans la limite du prix total de la voiture. Sur un véhicule d’occasion à petit prix, ce plafond peut réduire le montant versé : le simulateur applique l’écrêtement.</p>
<p>Vous habitez la vallée de l’Arve plutôt que le bassin annécien ? Voir <a href="/aides-voiture-electrique/pays-du-mont-blanc/">l’aide du Pays du Mont-Blanc</a>.</p>""",
    exemple="""<h2 id="exemple">Exemple de calcul</h2>
<p>Une personne seule à Annecy, 10 000 € de revenu fiscal pour une part, fait détruire une voiture non classée et achète une électrique d’occasion à 14 000 € : <strong>3 000 €</strong> du Grand Annecy, auxquels s’ajoute la prime d’État occasion. Le plafond « total ≤ prix du véhicule » n’est pas atteint.</p>""",
    faq=[("Quel véhicule faut-il détruire pour l’aide du Grand Annecy ?",
          "Un véhicule non classé, c’est-à-dire trop ancien pour recevoir une vignette Crit’Air. Une Crit’Air 3, 4 ou 5 ne suffit pas, contrairement à d’autres métropoles."),
         ("Peut-on déposer le dossier après l’achat ?",
          "Non. Le règlement impose un dépôt avant la commande ou la signature du contrat de location. Une demande postérieure est refusée."),
         ("L’aide fonctionne-t-elle pour une voiture d’occasion ?",
          "Oui, et c’est même le seul cas où une Crit’Air 1 est acceptée. Pour une voiture neuve, seules l’électrique et l’hydrogène ouvrent droit à l’aide.")],
    sources=[("Aides et conseils en mobilité — grandannecy.fr (règlement du 13/02/2025)", "https://www.grandannecy.fr/zfem/aides-et-conseils-en-mobilite"),
             ("Prime d’État — service-public.fr, fiche F39188", "https://www.service-public.gouv.fr/particuliers/vosdroits/F39188")],
))

T.append(dict(
    slug="pays-du-mont-blanc", city="la vallée de l’Arve", epci="200034882", indexable=True,
    title="Aide voiture électrique Pays du Mont-Blanc : 4 000 à 4 500 €",
    desc="Le Fonds Air Véhicules de la vallée de l’Arve verse 4 000 €, + 500 € en cas de casse, dans la limite de 40 % du prix. Revenu ≤ 31 200 €/part.",
    h1="Quelles aides pour acheter une voiture électrique au Pays du Mont-Blanc ?",
    lede="Le Fonds Air Véhicules de la vallée de l’Arve est l’une des rares aides ouvertes aux revenus intermédiaires : jusqu’à 31 200 € de revenu fiscal par part.",
    answer="""<p><strong>Oui, 4 000 €, portés à 4 500 € si vous mettez une ancienne voiture à la casse</strong>, dans la limite de <strong>40 % du prix</strong> du véhicule. Le plafond de revenus est haut — <strong>31 200 € par part</strong> — mais les hybrides sont exclues et la location longue durée aussi.</p>""",
    detail="""<h2 id="montants">Les conditions du Fonds Air Véhicules</h2>
<ul>
<li><strong>4 000 €</strong>, <strong>+ 500 €</strong> en cas de mise à la casse d’une ancienne voiture ;</li>
<li>plafonné à <strong>40 % du prix</strong> du véhicule ;</li>
<li>revenu fiscal de référence <strong>inférieur à 31 200 € par part</strong> ;</li>
<li>voiture <strong>électrique, hydrogène ou gaz</strong> — <strong>les hybrides sont exclues</strong> ;</li>
<li>prix inférieur ou égal à 45 000 € ;</li>
<li><strong>la location longue durée est exclue</strong> ;</li>
<li>score environnemental d’au moins 60 points, voiture à conserver 4 ans, une aide par foyer tous les 4 ans.</li>
</ul>
<p class="note note-warn">Le site de la Communauté de communes était inaccessible lors de notre vérification : ces conditions proviennent du règlement de février 2026 relayé par des sources secondaires. L’aide est classée « à confirmer » dans le simulateur.</p>""",
    demarche="""<h2 id="demarches">Où déposer le dossier</h2>
<p>Sur le site de la Communauté de communes Pays du Mont-Blanc, après l’achat, avec la facture et la carte grise.</p>""",
    cumul="""<h2 id="cumul">Cumul</h2>
<p>L’aide se cumule avec la prime d’État. Le plafond de 40 % du prix s’applique au montant du Fonds Air Véhicules lui-même : sur une voiture à 10 000 €, l’aide est ramenée à 4 000 €.</p>""",
    exemple="",
    faq=[("Qui peut bénéficier du Fonds Air Véhicules du Pays du Mont-Blanc ?",
          "Les habitants des dix communes de la Communauté de communes Pays du Mont-Blanc, avec un revenu fiscal de référence inférieur à 31 200 € par part, qui achètent une voiture électrique, à hydrogène ou au gaz de 45 000 € maximum, hors location longue durée."),
         ("Les hybrides sont-elles éligibles ?",
          "Non, elles sont explicitement exclues du dispositif, y compris les hybrides rechargeables."),
         ("Peut-on en bénéficier plusieurs fois ?",
          "Une seule aide par foyer tous les quatre ans, et la voiture doit être conservée quatre ans.")],
    sources=[("Communauté de communes Pays du Mont-Blanc — ccpmb.fr (règlement de février 2026, site inaccessible lors de la vérification)", "https://www.ccpmb.fr/"),
             ("Prime d’État — service-public.fr, fiche F39188", "https://www.service-public.gouv.fr/particuliers/vosdroits/F39188")],
))

T.append(dict(
    slug="occitanie", city="Occitanie", region="76", indexable=True, kind="region",
    title="Éco-chèque mobilité Occitanie : jusqu’à 1 600 €",
    desc="La Région Occitanie verse 30 % du prix, jusqu’à 1 600 €, pour une électrique d’occasion achetée par un ménage non imposable chez un pro agréé.",
    h1="Éco-chèque mobilité Occitanie : quelles aides pour une voiture électrique ?",
    lede="L’Occitanie est la seule région française à financer encore directement l’achat d’une voiture par les particuliers. Son éco-chèque vise l’occasion électrique et les ménages non imposables.",
    answer="""<p><strong>Oui : 30 % du prix, jusqu’à 1 600 €.</strong> L’éco-chèque mobilité de la Région Occitanie s’adresse aux <strong>ménages non imposables</strong> qui achètent une <strong>voiture électrique d’occasion</strong> (immatriculée depuis au moins 12 mois), de <strong>30 000 € maximum</strong>, <strong>chez un professionnel agréé situé en Occitanie</strong>. <strong>5 000 aides</strong> sont disponibles entre juillet 2026 et juin 2027.</p>""",
    detail="""<h2 id="montants">Les conditions de l’éco-chèque mobilité</h2>
<ul>
<li><strong>30 % du prix, plafonné à 1 600 €</strong> ;</li>
<li>voiture <strong>100 % électrique d’occasion</strong>, immatriculée depuis au moins 12 mois ;</li>
<li>prix <strong>inférieur ou égal à 30 000 €</strong> ;</li>
<li>achat <strong>chez un professionnel agréé situé en Occitanie</strong> — un achat à un particulier ou hors région n’ouvre aucun droit ;</li>
<li>ménage <strong>non imposable</strong> sur le revenu (à vérifier sur votre avis d’imposition) ;</li>
<li>une seule fois par personne, contrôle technique favorable exigé ;</li>
<li><strong>5 000 aides</strong> pour la campagne de juillet 2026 à juin 2027.</li>
</ul>
<p class="note note-warn">L’enveloppe est limitée et le nombre d’aides restantes n’est pas publié en temps réel : une éligibilité ne garantit pas l’obtention.</p>""",
    demarche="""<h2 id="demarches">Comment demander l’éco-chèque</h2>
<p>Demande sur le site « Mes Aides en Ligne » de la Région, <strong>dans les 6 mois suivant l’achat</strong>, avec la facture du professionnel agréé, la carte grise, l’avis d’imposition établissant la non-imposition et un contrôle technique favorable.</p>""",
    cumul="""<h2 id="cumul">Cumul avec les aides des métropoles</h2>
<p>L’éco-chèque régional <strong>se cumule avec la prime d’État et avec les aides métropolitaines</strong>. Le cas le plus favorable est <a href="/aides-voiture-electrique/toulouse/">Toulouse</a>, dont le règlement prévoit explicitement ce cumul : jusqu’à 3 300 € de prime métropolitaine + 1 600 € d’éco-chèque sur une même voiture d’occasion.</p>
<p>À <a href="/aides-voiture-electrique/montpellier/">Montpellier</a>, la métropole ne verse aucune aide à l’achat : l’éco-chèque régional est alors la seule aide locale mobilisable.</p>""",
    exemple="""<h2 id="exemple">Exemple de calcul</h2>
<p>Un ménage non imposable de l’Hérault achète une électrique d’occasion à 12 000 € chez un concessionnaire agréé en Occitanie : 30 % du prix, soit 3 600 €, ramenés au plafond de <strong>1 600 €</strong>. S’il habitait Toulouse Métropole et faisait détruire une Crit’Air 4, il pourrait y ajouter 2 700 à 3 300 €.</p>""",
    faq=[("Qui peut bénéficier de l’éco-chèque mobilité en Occitanie ?",
          "Les ménages non imposables sur le revenu, résidant en Occitanie, qui achètent une voiture électrique d’occasion de 30 000 € maximum chez un professionnel agréé situé dans la région. L’aide est de 30 % du prix, plafonnée à 1 600 €."),
         ("L’éco-chèque fonctionne-t-il pour une voiture neuve ?",
          "Non, il est réservé aux véhicules d’occasion immatriculés depuis au moins 12 mois. Pour une voiture neuve, ce sont les aides nationales et, le cas échéant, celles de votre métropole qui s’appliquent."),
         ("Puis-je acheter hors d’Occitanie ?",
          "Non. Le vendeur doit être un professionnel agréé situé en Occitanie ; c’est une condition du règlement régional."),
         ("Combien de temps ai-je pour déposer ma demande ?",
          "Six mois après l’achat, avec un contrôle technique favorable. L’enveloppe est limitée à 5 000 aides pour la campagne de juillet 2026 à juin 2027.")],
    sources=[("Éco-chèque mobilité — laregion.fr (page mise à jour le 23/07/2026)", "https://www.laregion.fr/Eco-cheque-mobilite-voiture-electrique-ou-hybride"),
             ("Prime d’État — service-public.fr, fiche F39188", "https://www.service-public.gouv.fr/particuliers/vosdroits/F39188")],
))

T.append(dict(
    slug="seine-maritime", city="la Seine-Maritime", dept="76", indexable=True, kind="dept",
    title="Aide voiture électrique Seine-Maritime : 2 000 à 4 000 €",
    desc="Le Département subventionne les habitants hors Métropole de Rouen qui travaillent dans la zone à faibles émissions rouennaise. Barème à confirmer.",
    h1="Quelles aides pour acheter une voiture électrique en Seine-Maritime ?",
    lede="Le Département complète l’action de la Métropole de Rouen, pour ceux qui habitent ailleurs dans le département mais travaillent dans la zone à faibles émissions rouennaise.",
    answer="""<p><strong>Oui, de 2 000 à 4 000 €</strong> — mais avec une condition très ciblée : cette subvention vise les habitants de la Seine-Maritime <strong>hors Métropole Rouen Normandie</strong> qui <strong>travaillent dans la zone à faibles émissions de Rouen</strong>. Plafond de revenus : <strong>21 000 € par part</strong>, avec destruction d’une voiture Crit’Air 3 ou plus ancienne.</p>""",
    detail="""<h2 id="montants">Ce que prévoit le Département</h2>
<ul>
<li><strong>2 000, 3 000 ou 4 000 €</strong> selon les revenus ⚠️ montants issus de sources non officielles, le barème 2026 n’étant pas consultable ;</li>
<li>revenu fiscal de référence <strong>inférieur ou égal à 21 000 € par part</strong> ;</li>
<li>destruction d’une voiture diesel d’avant 2011 ou essence d’avant 2006 ;</li>
<li>total des aides publiques limité à <strong>80 % du prix</strong> ;</li>
<li>budget voté « jusqu’en 2025 » : <strong>le maintien en 2026 reste à confirmer</strong>.</li>
</ul>
<p class="note note-warn">La condition d’activité professionnelle dans la zone à faibles émissions de Rouen ne peut pas être vérifiée par le simulateur : il affiche donc cette aide comme conditionnelle.</p>
<p>Si vous habitez l’une des 71 communes de la Métropole Rouen Normandie, c’est <a href="/aides-voiture-electrique/rouen/">l’aide métropolitaine</a> qui s’applique — les deux ne se cumulent pas.</p>""",
    demarche="""<h2 id="demarches">Où déposer le dossier</h2>
<p>Sur seinemaritime.fr, dans les 6 mois suivant la facture.</p>""",
    cumul="""<h2 id="cumul">Cumul</h2>
<p>Cumulable avec la prime d’État, dans la limite de 80 % du prix du véhicule, toutes aides publiques confondues.</p>""",
    exemple="",
    faq=[("Qui peut bénéficier de l’aide du Département de la Seine-Maritime ?",
          "Les habitants du département situés hors Métropole Rouen Normandie qui travaillent dans la zone à faibles émissions de Rouen, avec un revenu fiscal inférieur ou égal à 21 000 € par part et la destruction d’une voiture Crit’Air 3 ou plus ancienne."),
         ("Peut-on cumuler l’aide départementale et celle de la Métropole de Rouen ?",
          "Non : l’aide départementale s’adresse précisément aux habitants situés hors de la Métropole. Selon votre commune, c’est l’une ou l’autre."),
         ("Le dispositif existe-t-il toujours en 2026 ?",
          "Le règlement consulté date de mars 2023 et le budget était voté « jusqu’en 2025 ». Le maintien en 2026 n’a pas pu être confirmé : contactez le Département avant d’engager un achat.")],
    sources=[("Subvention ZFE-m — seinemaritime.fr (règlement du 20/03/2023)", "https://www.seinemaritime.fr/mon-cadre-de-vie/routes-bacs/subvention-zfe-m.html"),
             ("Métropole Rouen Normandie — règlement du 29/09/2025", "https://zfe.metropole-rouen-normandie.fr/sites/default/files/2025-10/B2025_0429_annexe.pdf")],
))

# --- Territoires vérifiés SANS aide locale (la réponse négative datée est le contenu) ---
T.append(dict(
    slug="nice", city="Nice", epci="200030195", indexable=True, no_aid=True,
    title="Aide voiture électrique Nice : l’aide a été supprimée",
    desc="La Métropole Nice Côte d’Azur ne verse plus d’aide à l’achat depuis le 30 juin 2023. Ce qui reste accessible aux habitants en 2026.",
    h1="Existe-t-il une aide voiture électrique à Nice en 2026 ?",
    lede="La réponse est non, et elle mérite d’être datée : l’aide de la Métropole Nice Côte d’Azur s’est arrêtée le 30 juin 2023. Plusieurs sites, y compris une fiche gouvernementale, l’affichent pourtant encore.",
    answer="""<p><strong>Non, il n’y a plus d’aide locale à Nice.</strong> L’aide de la Métropole Nice Côte d’Azur pour les voitures électriques a été <strong>supprimée le 30 juin 2023</strong> et la page officielle correspondante a été retirée. Les habitants des 51 communes de la métropole conservent en revanche l’accès à toutes les <a href="/aides-voiture-electrique-2026/">aides nationales</a>.</p>""",
    detail="""<h2 id="attention">Attention aux informations périmées</h2>
<p class="note note-warn">La fiche « aides locales » du portail gouvernemental jechangemavoiture.gouv.fr concernant cette région <strong>n’est plus à jour</strong> : elle mentionne encore des dispositifs supprimés. C’est l’un des cas qui nous ont conduits à vérifier chaque règlement à la source plutôt qu’à recopier les fiches nationales.</p>""",
    demarche="", cumul="", exemple="",
    faq=[("Y a-t-il une aide de la Ville de Nice pour une voiture électrique ?",
          "Non. Ni la Ville de Nice ni la Métropole Nice Côte d’Azur ne versent aujourd’hui d’aide à l’achat d’une voiture pour les particuliers. Le dispositif métropolitain a pris fin le 30 juin 2023."),
         ("Que reste-t-il pour un habitant de Nice qui achète une électrique ?",
          "Les aides nationales : la prime d’État « Coup de pouce » (3 300 à 7 700 € selon vos revenus) pour une voiture neuve, le leasing social si vous roulez pour travailler avec un revenu fiscal inférieur à 16 880 € par part, et la prime pour une électrique d’occasion depuis le 1er septembre 2026."),
         ("La Région Provence-Alpes-Côte d’Azur aide-t-elle à l’achat ?",
          "Aucune aide régionale à l’achat d’une voiture pour les particuliers n’a été trouvée lors de notre vérification. L’aide du Département des Bouches-du-Rhône, souvent citée, est terminée depuis le 31 janvier 2022 et ne concernait pas les Alpes-Maritimes.")],
    sources=[("Métropole Nice Côte d’Azur — nicecotedazur.org (page de l’aide retirée)", "https://www.nicecotedazur.org/"),
             ("Prime d’État — service-public.fr, fiche F39188", "https://www.service-public.gouv.fr/particuliers/vosdroits/F39188")],
))

T.append(dict(
    slug="montpellier", city="Montpellier", epci="243400017", indexable=True, no_aid=True,
    title="Aide voiture électrique Montpellier : à quoi avez-vous droit",
    desc="La métropole n’aide pas l’achat d’une voiture, mais l’éco-chèque de la Région Occitanie reste accessible : jusqu’à 1 600 € en occasion électrique.",
    h1="Existe-t-il une aide voiture électrique à Montpellier en 2026 ?",
    lede="La métropole n’aide pas l’achat d’une voiture — mais la Région Occitanie, oui. C’est la distinction que la plupart des pages sur le sujet ne font pas.",
    answer="""<p><strong>Pas d’aide de la métropole, mais une aide régionale.</strong> Montpellier Méditerranée Métropole ne subventionne pas l’achat d’une voiture pour les particuliers : son dispositif porte sur les vélos à assistance électrique. En revanche, l’<a href="/aides-voiture-electrique/occitanie/">éco-chèque mobilité de la Région Occitanie</a> est accessible aux Montpelliérains : <strong>30 % du prix, jusqu’à 1 600 €</strong>, pour une électrique d’occasion achetée par un ménage non imposable chez un professionnel agréé en Occitanie.</p>""",
    detail="""<h2 id="regional">L’éco-chèque régional en bref</h2>
<ul>
<li>Voiture <strong>100 % électrique d’occasion</strong>, immatriculée depuis au moins 12 mois, 30 000 € maximum ;</li>
<li>ménage <strong>non imposable</strong> ;</li>
<li>achat <strong>chez un professionnel agréé situé en Occitanie</strong> ;</li>
<li>demande dans les 6 mois, 5 000 aides disponibles de juillet 2026 à juin 2027.</li>
</ul>
<p><a href="/aides-voiture-electrique/occitanie/">Toutes les conditions de l’éco-chèque mobilité →</a></p>""",
    demarche="", cumul="", exemple="",
    faq=[("Montpellier Méditerranée Métropole aide-t-elle à acheter une voiture électrique ?",
          "Non. La métropole finance les vélos à assistance électrique, mais pas l’achat d’une voiture par un particulier, d’après les informations vérifiées en septembre 2026."),
         ("Quelle aide reste-t-il à un habitant de Montpellier ?",
          "L’éco-chèque mobilité de la Région Occitanie, jusqu’à 1 600 € pour une voiture électrique d’occasion achetée par un ménage non imposable, ainsi que toutes les aides nationales."),
         ("L’éco-chèque marche-t-il pour une voiture neuve ?",
          "Non, il est réservé à l’occasion. Pour une neuve, il reste la prime d’État « Coup de pouce » ou le leasing social.")],
    sources=[("Recensement des aides — mes-aides.francetravail.fr (mis à jour le 10/07/2026)", "https://mes-aides.francetravail.fr/"),
             ("Éco-chèque mobilité — laregion.fr", "https://www.laregion.fr/Eco-cheque-mobilite-voiture-electrique-ou-hybride")],
))

T.append(dict(
    slug="saint-etienne", city="Saint-Étienne", epci="244200770", indexable=True, no_aid=True,
    title="Aide voiture électrique Saint-Étienne : aucune aide locale",
    desc="Saint-Étienne Métropole n’aide pas l’achat d’une voiture : son Fonds air véhicule vise les utilitaires. Les aides nationales restent accessibles.",
    h1="Existe-t-il une aide voiture électrique à Saint-Étienne en 2026 ?",
    lede="Le « Fonds air véhicule » stéphanois est régulièrement cité pour les voitures. Il ne les concerne pas : il vise les utilitaires légers.",
    answer="""<p><strong>Non, pas pour les voitures.</strong> Saint-Étienne Métropole ne verse aucune aide à l’achat d’une voiture particulière. Son <strong>Fonds air véhicule</strong> destiné aux particuliers (1 000 €) porte uniquement sur la <strong>destruction ou la transformation d’un utilitaire léger</strong>. Restent les <a href="/aides-voiture-electrique-2026/">aides nationales</a>, accessibles à tous.</p>""",
    detail="", demarche="", cumul="", exemple="",
    faq=[("Le Fonds air véhicule de Saint-Étienne concerne-t-il les voitures ?",
          "Non. Pour les particuliers, il porte sur la mise au rebut ou la transformation d’un utilitaire léger, à hauteur de 1 000 €, et non sur l’achat d’une voiture particulière."),
         ("Quelles aides pour un habitant de Saint-Étienne qui achète une électrique ?",
          "Les aides nationales : prime d’État « Coup de pouce » de 3 300 à 7 700 € selon vos revenus pour une voiture neuve, leasing social si vous roulez pour travailler, prime occasion depuis septembre 2026, prime au rétrofit.")],
    sources=[("Aides de la Métropole — saint-etienne-metropole.fr", "https://www.saint-etienne-metropole.fr/preserver-recycler/qualite-de-lair/aides-de-la-metropole"),
             ("Prime d’État — service-public.fr, fiche F39188", "https://www.service-public.gouv.fr/particuliers/vosdroits/F39188")],
))

T.append(dict(
    slug="toulon", city="Toulon", epci="248300543", indexable=True, no_aid=True,
    title="Aide voiture électrique Toulon : aucune aide locale",
    desc="La Métropole Toulon-Provence-Méditerranée n’aide pas l’achat d’une voiture. Ce à quoi les habitants ont droit en 2026 : les aides nationales.",
    h1="Existe-t-il une aide voiture électrique à Toulon en 2026 ?",
    lede="La métropole toulonnaise finance la mobilité autrement : vélos électriques, permis de conduire, tarifs réduits des transports. Pas l’achat d’une voiture.",
    answer="""<p><strong>Non.</strong> La Métropole Toulon-Provence-Méditerranée ne verse aucune aide à l’achat d’une voiture pour les particuliers. Ses dispositifs concernent les vélos à assistance électrique, l’aide au permis de conduire et les tarifs réduits des transports en commun. Les <a href="/aides-voiture-electrique-2026/">aides nationales</a> restent, elles, pleinement accessibles.</p>""",
    detail="", demarche="", cumul="", exemple="",
    faq=[("La Métropole de Toulon aide-t-elle à acheter une voiture électrique ?",
          "Non. Ses aides à la mobilité portent sur les vélos à assistance électrique, le permis de conduire et les tarifs de transport, pas sur l’achat d’une voiture."),
         ("Quelles aides restent accessibles à Toulon ?",
          "Toutes les aides nationales : prime d’État « Coup de pouce » pour une voiture électrique neuve, leasing social sous conditions de revenus et d’usage professionnel, prime pour une électrique d’occasion depuis septembre 2026, et prime au rétrofit.")],
    sources=[("Aider les usagers à financer leur mobilité — metropoletpm.fr", "https://metropoletpm.fr/nos-missions/transports-mobilite/aider-les-usagers-financer-leur-mobilite"),
             ("Prime d’État — service-public.fr, fiche F39188", "https://www.service-public.gouv.fr/particuliers/vosdroits/F39188")],
))


# ---------------------------------------------------------------------------
# Assemblage
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# v1.1 — Signalétique par territoire.
# Les valeurs proviennent de data.js (scope / roadmap / status, plafonds lus
# dans les messages du moteur) et du tableau HUB_ROWS. Rien n'est inventé ici :
# si une règle change dans data.js, cette table doit être reprise avec elle.
# ---------------------------------------------------------------------------
M = {}

M["paris"] = dict(
    coll="la Métropole du Grand Paris", scope="epci", roadmap="local_after",
    status="active_unverified", montant="jusqu’à 6 000 €",
    cond="Mise au rebut obligatoire, prix &lt; 40 000 €",
    tags=["casse", "revenus", "neuve"], cumul="oui, avec la prime d’État",
    crit=[("ok", "Habiter l’une des 131 communes du Grand Paris"),
          ("ok", "Revenu fiscal de référence de 24 900 € par part au maximum"),
          ("stop", "Faire détruire définitivement une ancienne voiture : la vente ne suffit pas"),
          ("stop", "Prix du véhicule inférieur à 40 000 €"),
          ("time", "Dossier à déposer après l’achat")])

M["lyon"] = dict(
    coll="la Métropole de Lyon", scope="epci", roadmap="local_before",
    status="active", montant="500 à 3 000 €",
    cond="Crit’Air 2, 3 ou 4 à céder",
    tags=["zfe", "cession", "revenus"], cumul="oui, sans plafond global",
    crit=[("ok", "Habiter ou travailler dans la zone à faibles émissions de la Métropole"),
          ("ok", "Revenu fiscal de référence inférieur à 26 200 € par part"),
          ("ok", "Se séparer d’une voiture Crit’Air 2, 3 ou 4 : destruction, vente ou transformation"),
          ("time", "Dossier à déposer avant l’achat, sur demarches.toodego.com")])

M["marseille"] = dict(
    coll="Aix-Marseille-Provence", scope="epci", roadmap="local_after",
    status="active", montant="jusqu’à 5 000 €",
    cond="Crit’Air 4, 5 ou non classée à détruire",
    tags=["casse", "zfe", "revenus"], cumul="oui, mais la location est exclue",
    crit=[("ok", "Habiter la zone à faibles émissions de Marseille"),
          ("ok", "Revenu fiscal de référence de 24 900 € par part au maximum"),
          ("ok", "Voiture 100 % électrique ou à hydrogène : les hybrides sont exclues"),
          ("stop", "Faire détruire une voiture Crit’Air 4, 5 ou non classée"),
          ("stop", "Location longue durée ou avec option d’achat exclue")])

M["toulouse"] = dict(
    coll="Toulouse Métropole", scope="epci", roadmap="local_after",
    status="active", montant="2 000 à 5 000 €",
    cond="Crit’Air 3 ou plus ancienne à détruire",
    tags=["casse", "revenus", "particulier"], cumul="oui, avec la prime d’État",
    crit=[("ok", "Revenu fiscal de référence inférieur à 35 052 € par part"),
          ("ok", "Achat à un particulier accepté, contrairement à la plupart des territoires"),
          ("stop", "Faire détruire une voiture Crit’Air 3, 4, 5 ou non classée, possédée depuis un an"),
          ("time", "Dossier à déposer après l’achat")])

M["strasbourg"] = dict(
    coll="l’Eurométropole de Strasbourg", scope="epci", roadmap="local_after",
    status="active", montant="2 000 à 4 000 €",
    cond="Cession suffisante, total plafonné à 80 % du prix",
    tags=["cession", "revenus", "particulier"], cumul="oui, dans la limite de 80 % du prix",
    crit=[("ok", "Revenu fiscal de référence inférieur à 26 200 € par part"),
          ("ok", "Vendre ou faire détruire une voiture Crit’Air 2 ou plus ancienne, possédée depuis un an"),
          ("ok", "Achat à un particulier accepté"),
          ("stop", "Total des aides publiques plafonné à 80 % du prix"),
          ("time", "Dossier à déposer après l’achat")])

M["rouen"] = dict(
    coll="la Métropole Rouen Normandie", scope="epci", roadmap="local_after",
    status="active", montant="2 000 à 5 000 €",
    cond="+ 25 % en zone à faibles émissions",
    tags=["casse", "revenus"], cumul="oui, sauf avec le leasing social",
    crit=[("ok", "Revenu fiscal de référence de 22 000 € par part au maximum"),
          ("ok", "Majoration de 25 % si vous habitez la zone à faibles émissions"),
          ("stop", "Faire détruire un diesel d’avant 2011 ou une essence d’avant 2006"),
          ("stop", "Achat chez un professionnel obligatoire"),
          ("stop", "Pas de cumul avec le leasing social")])

M["bordeaux"] = dict(
    coll="Bordeaux Métropole", scope="epci", roadmap="local_after",
    status="active_unverified", montant="jusqu’à 6 000 €",
    cond="Barème non publié",
    tags=["casse", "neuve"], cumul="oui, avec la prime d’État",
    crit=[("ok", "Vendre ou faire détruire une voiture non classée"),
          ("ok", "En neuf : électrique uniquement — la vignette Crit’Air 1 n’est acceptée qu’en occasion"),
          ("stop", "Barème non publié : le montant est à confirmer au guichet"),
          ("time", "Dossier à déposer après l’achat")])

M["reims"] = dict(
    coll="le Grand Reims", scope="epci", roadmap="local_after",
    status="active_unverified", montant="2 000 à 6 000 €",
    cond="Sources contradictoires",
    tags=["casse", "zfe"], cumul="oui, avec la prime d’État",
    crit=[("ok", "Faire détruire une voiture Crit’Air 3, 4, 5 ou non classée"),
          ("stop", "Les sources publiques se contredisent : montant à confirmer auprès du Grand Reims"),
          ("time", "Dossier à déposer après l’achat")])

M["annecy"] = dict(
    coll="le Grand Annecy", scope="epci", roadmap="local_before",
    status="active", montant="3 000 €",
    cond="Véhicule non classé à détruire",
    tags=["casse", "revenus", "neuve"], cumul="oui, avec la prime d’État",
    crit=[("ok", "Revenu fiscal de référence inférieur à 16 300 € par part"),
          ("ok", "En neuf : électrique ou hydrogène uniquement"),
          ("stop", "Faire détruire une voiture non classée, trop ancienne pour une vignette Crit’Air"),
          ("stop", "En location : contrat d’au moins 24 mois"),
          ("time", "Dossier à déposer avant la commande")])

M["pays-du-mont-blanc"] = dict(
    coll="la communauté de communes Pays du Mont-Blanc", scope="epci", roadmap="local_after",
    status="active_unverified", montant="4 000 à 4 500 €",
    cond="40 % du prix au maximum",
    tags=["revenus", "neuve"], cumul="oui, avec la prime d’État",
    crit=[("ok", "Revenu fiscal de référence inférieur à 31 200 € par part"),
          ("ok", "Électrique, hydrogène ou gaz : les hybrides sont exclues"),
          ("stop", "Prix du véhicule inférieur à 45 000 €"),
          ("stop", "Location longue durée exclue"),
          ("time", "Dossier à déposer après l’achat")])

M["occitanie"] = dict(
    coll="la Région Occitanie", scope="region", roadmap="local_after",
    status="active", montant="jusqu’à 1 600 €",
    cond="Occasion électrique uniquement",
    tags=["occasion", "revenus"], cumul="oui, avec la prime d’État",
    crit=[("ok", "Voiture d’occasion 100 % électrique, immatriculée depuis au moins douze mois"),
          ("ok", "Ménage non imposable"),
          ("stop", "Achat chez un professionnel agréé situé en Occitanie"),
          ("stop", "Prix du véhicule inférieur à 30 000 €"),
          ("time", "Dossier à déposer après l’achat")])

M["seine-maritime"] = dict(
    coll="le Département de la Seine-Maritime", scope="dept", roadmap="local_after",
    status="active_unverified", montant="2 000 à 4 000 €",
    cond="Hors Métropole Rouen Normandie",
    tags=["casse", "revenus"], cumul="oui, avec la prime d’État",
    crit=[("ok", "Revenu fiscal de référence de 21 000 € par part au maximum"),
          ("ok", "Habiter le département hors Métropole Rouen Normandie"),
          ("stop", "Faire détruire un diesel d’avant 2011 ou une essence d’avant 2006"),
          ("time", "Dossier à déposer après l’achat")])

M["grenoble"] = dict(
    coll="Grenoble-Alpes Métropole", scope="epci", roadmap=None,
    status="suspended", montant="aide suspendue",
    cond="Suspendue depuis le 26 septembre 2025",
    tags=[], cumul=None, keep_h2=True,
    crit=[("stop", "Dispositif suspendu depuis le 26 septembre 2025 : aucune nouvelle demande n’est acceptée"),
          ("info", "Les aides de l’État, elles, restent accessibles aux habitants de la métropole")])

_NO_AID = {
    "nice": ("la Métropole Nice Côte d’Azur", "Aide supprimée le 30 juin 2023"),
    "montpellier": ("Montpellier Méditerranée Métropole", "Aucune aide voiture ; éco-chèque régional accessible"),
    "saint-etienne": ("Saint-Étienne Métropole", "Fonds air véhicule réservé aux utilitaires légers"),
    "toulon": ("la Métropole Toulon-Provence-Méditerranée", "Aucune aide à l’achat d’une voiture"),
}
for _s, (_c, _situ) in _NO_AID.items():
    M[_s] = dict(coll=_c, scope="epci", roadmap=None, status="none",
                 montant="Aucune aide locale", cond=_situ, tags=[], cumul=None, keep_h2=True,
                 crit=[("stop", _situ),
                       ("info", "Les aides de l’État restent accessibles : de 3 300 à 7 700 € pour une voiture neuve")])

QUAND_COURT = {"local_before": "avant l’achat", "local_after": "après l’achat", None: "—"}


def _strip_h2(html):
    """Retire le H2 d'ouverture d'un bloc : il est régénéré sous forme de question."""
    return re.sub(r"(?is)^\s*<h2[^>]*>.*?</h2>\s*", "", html or "")


def _strip_conditions(html):
    """Supprime la liste « Les conditions à remplir » : elle est désormais rendue
    en tête de page par le bloc d'éligibilité ✓/✗, la répéter allongeait la page
    sans rien apporter."""
    return re.sub(r"(?is)<h3>\s*Les conditions à remplir\s*</h3>\s*<ul>.*?</ul>\s*", "", html or "")


def _h2(hid, text):
    return '<h2 id="%s">%s</h2>\n' % (hid, text)


def head_blocks(t):
    """Étiquettes, carte d'identité et bloc d'éligibilité d'une page territoire."""
    m = M.get(t["slug"])
    if not m:
        return "", "", ""
    bar = labels.bar(scope=m["scope"], roadmap=m["roadmap"], status=m["status"], tags=m["tags"])
    card = labels.id_card([
        ("Montant", m["montant"]),
        ("Condition qui élimine", m["cond"]),
        ("Quand demander", labels.QUAND.get(m["roadmap"], "Sans objet")),
    ])
    crit_title = ("Vous y avez droit si" if m["status"] in ("active", "active_unverified")
                  else "Ce qu’il faut savoir")
    crit = labels.criteres(m["crit"], crit_title)
    return bar, card, crit


def grants(t):
    m = M.get(t["slug"])
    if not m or m["status"] not in ("active", "active_unverified"):
        return []
    vals = [int(re.sub(r"\D", "", n)) for n in re.findall(r"\d[\d\s  ]*", m["montant"])]
    g = dict(name="Aide à l’achat d’une voiture électrique — %s" % re.sub(r"^(la |le |l’|les )", "", m["coll"]).strip(),
             desc=m["cond"].replace("&lt;", "moins de").replace("&gt;", "plus de"), funder=m["coll"].strip(), area=t["city"])
    if len(vals) == 2:
        g["min"], g["max"] = vals[0], vals[1]
    elif len(vals) == 1:
        g["max"] = vals[0]
    return [g]


def _n(v):
    """Séparateur de milliers à la française (espace insécable fine)."""
    return format(int(v), ",d").replace(",", "\u202f")


def communes_block(t, by_epci, by_region, by_dept):
    """Liste des communes couvertes — donnée unique par page, tirée du COG INSEE."""
    if t.get("commune_note") == "marseille":
        return ("""<h2 id="communes">Ma commune est-elle concernée ?</h2>
<p>L’aide vise la <strong>zone à faibles émissions de Marseille</strong> : les 16 arrondissements de la commune de Marseille (codes postaux 13001 à 13016) en font partie, le périmètre exact restant infra-communal. Les 106 autres communes de la Métropole Aix-Marseille-Provence — Aix-en-Provence, Aubagne, Martigues, Vitrolles, Istres, Salon-de-Provence… — <strong>ne sont pas concernées</strong> par cette aide.</p>""")
    if t.get("kind") == "region":
        depts = sorted(set(d for d in by_dept if any(i in by_region.get("76", set()) for i in list(by_dept[d])[:1])))
        n = len(by_region.get("76", set()))
        return ("""<h2 id="communes">Ma commune est-elle concernée ? Les %s communes d’Occitanie</h2>
<p>L’éco-chèque s’applique à l’ensemble des <strong>%s communes de la région Occitanie</strong>, soit les 13 départements : Ariège, Aude, Aveyron, Gard, Haute-Garonne, Gers, Hérault, Lot, Lozère, Hautes-Pyrénées, Pyrénées-Orientales, Tarn et Tarn-et-Garonne.</p>""" % (_n(n), _n(n)))
    if t.get("kind") == "dept":
        n_dept = len(by_dept.get("76", set()))
        n_mrn = len(by_epci.get("200023414", {}))
        return ("""<h2 id="communes">Ma commune est-elle concernée ? Hors Métropole de Rouen</h2>
<p>Le département compte <strong>%s communes</strong>. L’aide départementale vise celles qui ne font <em>pas</em> partie des <strong>%s communes de la Métropole Rouen Normandie</strong> : pour ces dernières, c’est <a href="/aides-voiture-electrique/rouen/">l’aide métropolitaine</a> qui s’applique.</p>""" % (_n(n_dept), _n(n_mrn)))
    epci = t.get("epci")
    if not epci:
        return ""
    communes = sorted(set(n for n, _ in by_epci.get(epci, {}).values()), key=lambda s: s.lower())
    if not communes:
        return ""
    label = "concernées par l’aide" if not t.get("no_aid") else "de cette intercommunalité"
    return ("""<h2 id="communes">Ma commune est-elle concernée ?</h2>
<details class="communes"><summary>Voir la liste des %s communes %s</summary>
<p>%s</p></details>
<p style="font-size:.9rem;color:#64748b">Source : code officiel géographique de l’INSEE (jeu de données Etalab « découpage administratif »). Le simulateur identifie automatiquement votre intercommunalité à partir de votre code postal.</p>"""
            % (_n(len(communes)), label, " · ".join(communes)))


def build_page(t, geo):
    by_epci, by_region, by_dept = geo
    city = t["city"]
    m = M.get(t["slug"], {})
    keep = m.get("keep_h2", False) or not m
    parts = ['<div class="answer">%s</div>' % t["answer"]]

    # Titres réécrits en question + chiffre. Les territoires au dispositif
    # atypique (aide suspendue, aucune aide) gardent leur titre d'origine.
    titres = {
        "detail": ("montants", "Combien verse %s ? %s" % (m.get("coll", ""), m.get("montant", ""))),
        "demarche": ("demarches", "Quand et comment déposer le dossier ? %s"
                     % QUAND_COURT.get(m.get("roadmap"), "").capitalize()),
        "cumul": ("cumul", "Se cumule-t-elle avec la prime d’État ? %s"
                  % (m.get("cumul") or "").capitalize()),
        "exemple": ("exemple", "Combien au total, sur un cas concret ?"),
    }
    for key in ("detail", "demarche", "cumul", "exemple"):
        if not t.get(key):
            continue
        if keep:
            parts.append(t[key])
        else:
            hid, txt = titres[key]
            blk = _strip_h2(t[key])
            if key == "detail":
                blk = _strip_conditions(blk)
            parts.append(_h2(hid, txt) + blk)
    parts.append(NAT_BLOCK)
    parts.append(communes_block(t, by_epci, by_region, by_dept))
    parts.append(cta(city))
    crumbs = [("Accueil", "/"), ("Aides près de chez vous", "/aides-voiture-electrique/"),
              (city[0].upper() + city[1:], "/aides-voiture-electrique/%s/" % t["slug"])]
    bar, card, crit = head_blocks(t)
    return dict(
        slug="aides-voiture-electrique/" + t["slug"],
        nav_active="/aides-voiture-electrique/",
        title=t["title"], desc=t["desc"], h1=t["h1"], og_title=t["h1"],
        crumbs=crumbs, lede=t["lede"], body="\n".join(p for p in parts if p),
        labels=bar, idcard=card, criteres=crit, grants=grants(t),
        faq=t.get("faq"), sources=t.get("sources"), verified=V,
        related=[("Toutes les aides près de chez vous", "/aides-voiture-electrique/"),
                 ("Les aides nationales 2026", "/aides-voiture-electrique-2026/"),
                 ("Prime « Coup de pouce »", "/prime-coup-de-pouce-voiture-electrique/"),
                 ("Peut-on cumuler les aides ?", "/cumul-aides-voiture-electrique/")],
    )


HUB_ROWS = [
    ("paris", "Grand Paris", "jusqu’à 6 000 €", "Mise au rebut obligatoire, revenu ≤ 24 900 €/part, prix &lt; 40 000 €", "ok"),
    ("marseille", "Marseille (zone à faibles émissions)", "jusqu’à 5 000 €", "Crit’Air 4+ à détruire, électrique ou hydrogène, location exclue", "ok"),
    ("toulouse", "Toulouse Métropole", "2 000 à 5 000 €", "Revenu ≤ 35 052 €/part, achat à un particulier accepté", "ok"),
    ("lyon", "Métropole de Lyon", "500 à 3 000 €", "Crit’Air 2/3/4 à céder, dossier avant l’achat", "ok"),
    ("strasbourg", "Eurométropole de Strasbourg", "2 000 à 4 000 €", "Cession suffisante, cumul plafonné à 80 % du prix", "ok"),
    ("rouen", "Métropole Rouen Normandie", "2 000 à 5 000 €", "+25 % en zone à faibles émissions, pas de cumul avec le leasing social", "ok"),
    ("annecy", "Grand Annecy", "3 000 €", "Véhicule non classé à détruire, dossier avant la commande", "ok"),
    ("bordeaux", "Bordeaux Métropole", "jusqu’à 6 000 €", "Barème non publié — à confirmer au guichet", "warn"),
    ("reims", "Grand Reims", "2 000 à 6 000 €", "Sources contradictoires — à confirmer", "warn"),
    ("pays-du-mont-blanc", "Pays du Mont-Blanc", "4 000 à 4 500 €", "Hybrides et location exclues, 40 % du prix maximum", "warn"),
    ("occitanie", "Région Occitanie", "jusqu’à 1 600 €", "Occasion électrique, ménage non imposable, professionnel agréé", "ok"),
    ("seine-maritime", "Département Seine-Maritime", "2 000 à 4 000 €", "Hors Métropole de Rouen, travail en zone à faibles émissions", "warn"),
    ("grenoble", "Grenoble-Alpes Métropole", "suspendue", "Dispositif suspendu depuis le 26 septembre 2025", "stop"),
]
NO_AID_ROWS = [("nice", "Métropole Nice Côte d’Azur", "Aide supprimée le 30 juin 2023"),
               ("montpellier", "Montpellier Méditerranée Métropole", "Aucune aide voiture ; éco-chèque régional accessible"),
               ("saint-etienne", "Saint-Étienne Métropole", "Fonds air véhicule réservé aux utilitaires légers"),
               ("toulon", "Métropole Toulon-Provence-Méditerranée", "Aucune aide à l’achat d’une voiture")]


def hub_page():
    badge = {"ok": labels.fiabilite("active"),
             "warn": labels.fiabilite("active_unverified"),
             "stop": labels.fiabilite("suspended")}
    rows = "".join(
        '<tr><td><a href="/aides-voiture-electrique/%s/">%s</a>%s</td>'
        '<td class="num">%s</td><td>%s</td><td>%s</td></tr>'
        % (s, n, '<div class="lbbar">%s%s</div>' % (
            labels.payeur(M.get(s, {}).get("scope")),
            labels.quand(M.get(s, {}).get("roadmap"))),
           m, c, badge[st]) for s, n, m, c, st in HUB_ROWS)
    norows = "".join(
        '<tr><td><a href="/aides-voiture-electrique/%s/">%s</a></td><td>%s</td></tr>' % r for r in NO_AID_ROWS)
    body = """
<div class="answer">
<p><strong>Treize collectivités</strong> versent encore une aide à l’achat d’une voiture aux particuliers, et <strong>sept territoires</strong> que nous avons vérifiés n’en versent aucune. Ces aides <strong>s’ajoutent</strong> à celles de l’État. Partout ailleurs en France, seules les aides nationales s’appliquent — et le simulateur vous le dit explicitement plutôt que de vous laisser chercher.</p>
</div>

<h2 id="liste">Les territoires qui versent une aide</h2>
<div class="table-wrap"><table>
<thead><tr><th>Territoire</th><th>Montant</th><th>Condition marquante</th><th>Statut</th></tr></thead>
<tbody>""" + rows + """</tbody></table></div>

<h2 id="sans-aide">Les territoires vérifiés sans aide locale</h2>
<p>Une réponse négative sourcée vaut mieux qu’une recherche sans fin. Ces quatre métropoles sont régulièrement citées comme versant une aide : ce n’est plus le cas.</p>
<div class="table-wrap"><table>
<thead><tr><th>Territoire</th><th>Situation</th></tr></thead>
<tbody>""" + norows + """</tbody></table></div>
<p>Trois autres collectivités ont été vérifiées sans aide à l’achat pour les particuliers : le <strong>Département des Bouches-du-Rhône</strong> (aide terminée depuis le 31 janvier 2022, hors zone à faibles émissions de Marseille), la <strong>Région Normandie</strong> et la <strong>Région Île-de-France</strong> (aide supprimée le 2 mars 2025, prime « non-casse » maintenue pour le rétrofit).</p>

<h2 id="methode">Comment lire ces aides</h2>
<p>Quatre paramètres décident presque toujours de votre éligibilité :</p>
<ul>
<li><strong>Le plafond de revenus</strong>, exprimé en revenu fiscal de référence par part : de 16 300 € au Grand Annecy à 35 052 € à Toulouse.</li>
<li><strong>Le sort de l’ancienne voiture</strong> : destruction obligatoire (Grand Paris, Toulouse, Marseille, Rouen, Annecy), ou simple cession acceptée (Lyon, Strasbourg).</li>
<li><strong>Le moment de la demande</strong> : avant l’achat à Lyon et au Grand Annecy, après ailleurs. C’est la première cause de refus.</li>
<li><strong>Le statut du vendeur</strong> : professionnel exigé presque partout, particulier accepté à Toulouse et Strasbourg.</li>
</ul>

<h2 id="ailleurs">Et si ma commune n’est pas dans la liste ?</h2>
<p>C’est le cas de la grande majorité des communes françaises. Vous conservez l’intégralité des aides nationales, qui représentent l’essentiel du montant : de 3 300 à 7 700 € pour une voiture neuve. Nous ne créons pas de page pour un territoire sans dispositif propre — cela n’apporterait rien. Le simulateur, lui, répond pour les 35 493 couples code postal / commune de France.</p>
""" + cta("votre commune")
    return dict(
        slug="aides-voiture-electrique", nav_active="/aides-voiture-electrique/",
        schema_type="WebPage",
        title="Aides voiture électrique par ville et région en France",
        og_title="Les aides voiture électrique près de chez vous",
        desc="Les 13 collectivités qui aident encore à l’achat d’une voiture électrique : montants, conditions et démarches, territoire par territoire.",
        h1="Les aides à l’achat d’une voiture électrique près de chez vous",
        crumbs=[("Accueil", "/"), ("Aides près de chez vous", "/aides-voiture-electrique/")],
        lede="Métropoles, régions, départements : voici les treize territoires français qui versent encore une aide à l’achat, les sept qui n’en versent plus, et ce que cela change pour vous.",
        verified=V, body=body,
        labels=labels.bar(scope="epci", status="active", tags=["particulier"]),
        idcard=labels.id_card([
            ("Territoires qui versent une aide", "13"),
            ("Territoires vérifiés sans aide", "7"),
            ("Communes couvertes par le simulateur", "35 493"),
        ]),
        criteres=labels.criteres([
            ("ok", "Votre territoire figure dans le tableau ci-dessous : l’aide locale s’ajoute à celle de l’État"),
            ("ok", "Votre territoire n’y figure pas : vous gardez l’intégralité des aides nationales, de 3 300 à 7 700 €"),
            ("time", "Le moment du dépôt change selon les territoires : avant l’achat à Lyon et au Grand Annecy, après ailleurs"),
        ], "Comment vous situer en dix secondes"),
        faq=[("Quelles villes aident encore à acheter une voiture électrique en 2026 ?",
              "Treize collectivités : Grand Paris, Métropole de Lyon, Marseille (zone à faibles émissions), Toulouse, Strasbourg, Rouen, Bordeaux, Reims, Grand Annecy, Pays du Mont-Blanc, Seine-Maritime, Région Occitanie, et Grenoble dont l’aide est suspendue depuis septembre 2025."),
             ("Les aides locales se cumulent-elles avec la prime d’État ?",
              "Oui dans la quasi-totalité des cas. Deux exceptions : la Métropole de Rouen exclut le cumul avec le leasing social, et Aix-Marseille-Provence exclut la location longue durée. Certaines collectivités plafonnent en outre le total des aides publiques à 80 % du prix."),
             ("Ma commune n’a pas de page dédiée, ai-je droit à quelque chose ?",
              "Oui, aux aides nationales, qui représentent l’essentiel du montant. Nous ne créons de page que pour les territoires disposant d’un dispositif propre ; pour toutes les autres communes, le simulateur donne la réponse à partir de votre code postal."),
             ("Comment savoir si j’habite dans une zone à faibles émissions ?",
              "Le périmètre est parfois infra-communal, notamment à Lyon, Marseille et Reims : une partie seulement de la commune est concernée. Le simulateur approxime à la commune entière et le signale ; vérifiez votre adresse exacte sur le site de votre collectivité avant de déposer un dossier.")],
        sources=[("Prime d’État — service-public.fr, fiche F39188", "https://www.service-public.gouv.fr/particuliers/vosdroits/F39188"),
                 ("Recensement des aides locales — jechangemavoiture.gouv.fr", "https://jechangemavoiture.gouv.fr/jcmv/aide-achat.html"),
                 ("Nos sources, règlement par règlement", "/sources/")],
        related=[("Toutes les aides nationales 2026", "/aides-voiture-electrique-2026/"),
                 ("Peut-on cumuler plusieurs aides ?", "/cumul-aides-voiture-electrique/"),
                 ("Aides pour une voiture d’occasion", "/aide-voiture-electrique-occasion/"),
                 ("Notre méthodologie", "/notre-methodologie/")],
    )


def pages(geo):
    return [hub_page()] + [build_page(t, geo) for t in T]
