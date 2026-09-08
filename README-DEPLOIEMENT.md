# Mes Aides Auto — déploiement de la refonte SEO (08/09/2026)

Ce dossier contient **uniquement les fichiers à ajouter ou à remplacer**.
`app.js`, `communes.js` et `favicon.svg` ne sont pas modifiés : ne les touchez pas, ne les supprimez pas.

## 1. Fichiers modifiés (à remplacer)

| Fichier | Ce qui change |
|---|---|
| `index.html` | og:image + Twitter Card, navigation principale vers les nouvelles pages, bande « Nos guides » + « Trouvez les aides près de chez vous » avant le pied de page, pied de page enrichi, liens internes en absolu (`/` au lieu de `index.html`). **Aucune modification du simulateur, des identifiants, des scripts ni du code Google Tag Manager.** |
| `qui-sommes-nous.html` | Navigation principale, pied de page enrichi, og:image, liens absolus |
| `mentions-legales.html` | Idem (la page reste en `noindex`) |
| `data.js` | Leasing social : la contradiction 6 500 / 9 000 € est levée par le téléservice officiel (plafond de droit commun / plafond majoré pour un véhicule européen). Prime occasion : source officielle (arrêté du 10 août 2026, fiche TRA-EQ-133) au lieu d'une source secondaire, conditions complétées, statut passé en « vérifié ». `META.lastVerified` → 08/09/2026, version 0.5.0. **Aucun changement de formule : les 22 tests passent.** |
| `manifest.json` | `start_url` → `/` (cohérent avec la balise canonique) |
| `robots.txt` | Sitemap conservé, `/tools/` exclu, OAI-SearchBot ajouté |
| `llms.txt` | Réécrit : nouvelles pages, montants corrigés, sources officielles |
| `sitemap.xml` | Devient un **index** de sitemaps |

## 2. Fichiers nouveaux

- `sitemap-pages.xml`, `sitemap-guides.xml`, `sitemap-territoires.xml`
- `404.html` (page d'erreur personnalisée, en `noindex`)
- `.htaccess` (voir §4 — à tester)
- `assets/maa.css` (feuille de style des pages éditoriales, ~9 Ko, partagée)
- `assets/og-image.png` (image de partage 1200×630)
- **27 dossiers de pages**, chacun contenant un `index.html` :
  - 6 guides nationaux, 3 pages de confiance, 1 hub territorial, 17 pages territoriales.
- `tools/` : le générateur des pages (Python, sans dépendance). **À garder dans le dépôt, inutile sur le serveur.**

## 3. Ordre de mise en ligne conseillé

1. Envoyer `assets/`, puis les 27 dossiers de pages, puis `404.html` et les sitemaps.
2. Envoyer `data.js`, `manifest.json`, `robots.txt`, `llms.txt`.
3. Envoyer `index.html`, `qui-sommes-nous.html`, `mentions-legales.html` en dernier.
4. Vérifier dans le navigateur : la page d'accueil calcule toujours, la console affiche `window.runTests()` → `22/22 tests OK`, et le bandeau cookies fonctionne.
5. Dans la Search Console : soumettre `https://mes-aides-auto.fr/sitemap.xml` (l'index remplace l'ancien sitemap), puis demander l'indexation des pages prioritaires (`/aides-voiture-electrique-2026/`, `/prime-coup-de-pouce-voiture-electrique/`, `/aides-voiture-electrique/`).

## 4. À propos du `.htaccess`

Il fait trois choses : page 404 personnalisée, redirection 301 de `/index.html` vers `/` (pour supprimer le doublon d'URL), compression et cache. Toutes les directives sont encadrées par `<IfModule>`.

**Testez-le seul, avant tout le reste** : envoyez-le, ouvrez le site, vérifiez qu'il n'y a pas d'erreur 500. En cas de problème, supprimez le fichier — le site refonctionne immédiatement, tout le reste marche sans lui.

## 5. Régénérer les pages plus tard

```
python3 tools/build.py
```
Le script relit `data.js` et `communes.js` : les montants, les sources et les listes de communes des pages restent donc alignés sur le moteur de calcul. L'éditorial se trouve dans `tools/content_national.py` et `tools/content_territoires.py`.
