# Mes Aides Auto — dossier complet v0.9 (refonte SEO du 08/09/2026 + mode Professionnel)

Ce dossier est le site **entier**, prêt à être déposé tel quel sur GitHub
(« Add file » → « Upload files » → glisser tout le contenu du dossier → « Commit changes »).
Il remplace les fichiers existants et n'en supprime aucun.

## Ce qui change par rapport au dernier dépôt (mes-aides-auto-github-pages_1)

| Fichier | Statut | Détail |
|---|---|---|
| `data-pro.js` | **nouveau** | Règles du mode professionnel (prime utilitaire, avantages fiscaux, aides locales pro). |
| `app.js` | remplacé | Moteur v0.9 : bouton Particulier / Professionnel, lien direct `#pro`, quantité de véhicules, 38 tests. Le mode particulier est inchangé. |
| `index.html` | remplacé | Version de la refonte SEO **conservée** (navigation, bande « Nos guides », pied de page, og:image) + bouton Particulier / Professionnel et champs pro dans la bande 1, feuille de style recompilée. Mention « Version 0.9 ». |
| `llms.txt` | remplacé | Version de la refonte SEO conservée + paragraphe « Mode professionnel » et lien `#pro`. |
| `communes.js`, `favicon.svg` | inchangés | Présents pour que le dossier soit complet ; identiques à ceux déjà en ligne. |
| Tout le reste (`data.js` v0.5.0, 27 pages, `assets/`, sitemaps, `404.html`, `tools/`…) | inchangé | Copié tel quel depuis le dernier dépôt. |

Le fichier `.htaccess` n'était pas dans le zip fourni (fichier caché) : il n'est pas ici non plus. S'il est déjà sur le serveur, il reste en place.

## Vérification après mise en ligne

1. Ouvrir https://mes-aides-auto.fr/ : le bouton « Particulier / Professionnel » apparaît à droite du titre « Votre situation ».
2. Console du navigateur (F12) : `runTests()` → `38/38 tests OK`.
3. Ouvrir https://mes-aides-auto.fr/#pro : la page s'ouvre directement en mode professionnel (bordure corail).
4. Exemple de contrôle : mode professionnel, 69003, 35 000 €, utilitaire petit, assemblé en Europe, ancien véhicule à la casse → total « 8 800 € – 13 160 € ».
5. Mode particulier, 69003, revenu 15 000 €, 1 part, 30 000 €, casse → « 5 200 € – 8 524 € » (inchangé).
