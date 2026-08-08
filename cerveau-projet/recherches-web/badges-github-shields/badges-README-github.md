# Recherche -- Badges pour README GitHub (Cerveau-projet)
---

## Header

```yaml
recherche:
  id: "[RECHERCHE-BADGES-001]"
  titre: "Liste des badges possibles pour un README GitHub (Shields.io)"
  theme: "les-badges-github"
  agent: "atlas"
  date: "2026-08-07"
  source_principale: "https://shields.io/"
  statut: "validee"
```

---

## Contexte

### Pourquoi cette recherche ?

```
Le README de Cerveau-projet est destine a GitHub. On souhaite ajouter des badges
en tete du README (au niveau du logo). Il faut d'abord dresser la liste des badges
possibles, puis faire evoluer l'outil de Clio (mettre-a-jour-readme) pour les inserer.
```

### Quelle question cherche-t-on a repondre ?

```
Quels types de badges peut-on afficher dans un README GitHub (principalement via
Shields.io), sous quel format, et avec quels parametres ?
```

---

## Sources

### Source principale

| Element | Valeur |
|---|---|
| **URL** | https://shields.io/ |
| **Titre** | Shields.io -- Badges |
| **Date d'acces** | 2026-08-07 |
| **Auteur** | Shields.io (open source) |
| **Fiabilite** | Haute |

### Sources secondaires

| Source | URL | Pertinence |
|---|---|---|
| Shields.io -- Badge statique (format et parametres) | https://shields.io/badges/static-badge | Haute |
| GitHub Docs -- Syntaxe d'ecriture de base (images) | https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax | Haute |

---

## Informations trouvees

### Resume

```
Shields.io fournit des badges (labels) pour des centaines de services. Deux grandes
familles : (1) les badges STATIQUES (valeurs fixees par l'auteur, ideaux pour licence,
plateforme, 'fait avec', nom de projet), et (2) les badges DYNAMIQUES (valeurs
recuperees en direct depuis un service : GitHub, build, version, couverture...).
Dans un README GitHub, un badge s'affiche comme une simple image Markdown.
```

### Details

#### 1. Format d'un badge Shield (statique)

```
URL de base : https://img.shields.io/badge/<label>-<message>-<couleur>
Exemple      : https://img.shields.io/badge/Plateforme-Windows-blue

Parametres (query) courants :
  ?style=flat | flat-square | plastic | for-the-badge | social   (defaut: flat)
  &logo=<slug icon simple-icons>                                 (icone)
  &logoColor=<couleur>
  &label=<texte>                                                  (texte gauche)
  &labelColor=<couleur>
  &color=<couleur>                                                (texte droit)

Codes couleurs nommes (Shields) : brightgreen, green, yellowgreen, yellow, orange,
red, blue, lightgrey, success, important, critical, blueviolet, ...
```

#### 2. Badges statiques typiques pour un README

```
- Licence      : https://img.shields.io/badge/Licence-MIT-brightgreen
- Plateforme   : https://img.shields.io/badge/Plateforme-Windows-blue
- Fait avec    : https://img.shields.io/badge/Made%20with-Bash-orange
- Nom du projet / version manuelle
- Nombre d'outils : https://img.shields.io/badge/Outils-78-blueviolet
- Etat du projet  : https://img.shields.io/badge/Statut-stable-brightgreen
```

#### 3. Badges dynamiques (services) pour GitHub

```
- GitHub (repo) : stars, forks, watchers, issues, pull requests, derniers commits
      Exemple stars  : https://img.shields.io/github/stars/<user>/<repo>
      Exemple issues : https://img.shields.io/github/issues/<user>/<repo>
- Version / release : https://img.shields.io/github/v/release/<user>/<repo>
- Licence (auto)     : https://img.shields.io/github/license/<user>/<repo>
- Build / CI (GitHub Actions, Travis, CircleCI...)
- Couverture de tests (Codecov, Coveralls)
- Langage principal  : https://img.shields.io/github/languages/top/<user>/<repo>
- Taille du repo     : https://img.shields.io/github/repo-size/<user>/<repo>
- Dependabot / dependances
```

#### 4. Affichage dans un README GitHub

```
Un badge = une image Markdown standard, syntaxe GitHub :

  ![<texte alternatif>](<url du badge>)

Le texte alternatif est important (accessibilite, et s'affiche si l'image ne
charge pas). Les badges sont generalement alignes en tete (une ligne sous le titre).
```

#### 5. Limites et recommandations

```
- Le `link` (clic) ne fonctionne QUE dans un <object> HTML, PAS dans une balise
  <img> ni en Markdown : sur GitHub un badge est purement affichage sauf HTML inline.
- Les badges dynamiques dependent de l'existence/publicite du repo GitHub (user/repo).
  Tant que le projet n'est pas publie, un badge dynamique affiche une erreur.
- Respect des regles du projet : ASCII uniquement, pas d'emojis.
```

---

## Verification

### Comparaison avec le code source

| Element | Code source | Recherche | Coherent ? |
|---|---|---|---|
| Format image Markdown | README (logo deja insere) | image Markdown | OUI |
| Regle ASCII | conformite ASCII imposee | badges ASCII | OUI |
| Emojis bannis | regles-emojis-ascii | aucun emoji | OUI |

### Validite des informations

```
[x] Informations encore valides ?
[x] Pas de changements recents ?
[x] Compatible avec le projet ?
```

---

## Utilisation

### Dans quel contexte utiliser ces informations ?

```
Servir de reference (liste) pour faire evoluer l'outil mettre-a-jour-readme de Clio
afin qu'il puisse inserer une liste de badges en tete du README.
```

### Comment appliquer ces informations ?

```
Vulcain implementera dans l'outil de Clio une capacite d'insertion de badges
(option dediee), en s'appuyant sur cette liste : format Shield statique, parametres
style/logo/couleur, et possibilite de badges dynamiques GitHub.
```

---

## Notes

```
Cette liste est une BASE. Le choix final des badges et de leurs valeurs appartient a
l'utilisateur (quels badges afficher : licence, plateforme, nombre d'outils, statut,
etc.). Pour les valeurs dynamiques (user/repo GitHub), il faudra renseigner le nom
du compte/repo lors de la configuration.
```

---

## Historique

| Date | Action | Resultat |
|---|---|---|
| 2026-08-07 | Recherche effectuee | Sources Shields.io + GitHub Docs |
| 2026-08-07 | Verification | Format et parametres confirmes |

---

## Liens

- **Index des recherches** : [index-recherches-web.md](../index-recherches-web.md)
- **Convention** : [convention-protocoles](../agents/conventions/protocoles/convention-protocoles.md)

