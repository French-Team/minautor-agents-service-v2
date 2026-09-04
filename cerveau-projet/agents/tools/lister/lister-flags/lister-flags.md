---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# lister-flags

**Categorie** : Lister
**Version** : 0.1.1
**Statut** : prepare
**Proprietaire** : Vulcain (outil partage)

## Description

Inventorie les flags et arguments des outils et combos du cerveau-projet.
L outil lit le catalogue des commandes, les definitions de combos et les
appels `argparse` des scripts Python. Les scripts inspectes ne sont jamais
executes.

## Utilisation

```bash
python3 lister-flags.py --dry-run --tous
python3 lister-flags.py --dry-run lister-outils
python3 lister-flags.py --dry-run --outil lister-outils --outil lister-fichiers
python3 lister-flags.py --dry-run --combo combo-corriger-ascii --format json
python3 lister-flags.py --dry-run --categorie lister
python3 lister-flags.py --dry-run --flag-partage version
```

Le wrapper equivalent est `lister-flags.sh`.

## Options

| Option | Description | Defaut |
|---|---|---|
| `CIBLES...` | Noms d outils ou de combos | aucune |
| `--outil NOM` | Selectionner un outil, repetable | aucune |
| `--combo NOM` | Selectionner un combo, repetable | aucune |
| `--tous` | Lister toutes les entites | false |
| `--categorie NOM` | Filtrer par categorie, par exemple `lister` ou `combos` | toutes |
| `--flag-partage NOM` | Garder un flag utilise par plusieurs entites | aucun |
| `--source SOURCE` | `tous`, `catalogue`, `argparse` ou `definition-combo` | `tous` |
| `--format FORMAT` | `table` ou `json` | `table` |
| `--json` | Alias de `--format json` | false |
| `--inclure-vides` | Conserver les entites sans flag apres filtrage | false |
| `--verbose` | Afficher la source et le cas de chaque flag | false |
| `--dry-run` | Mode lecture explicite | false |
| `--chrono` | Afficher la duree | false |
| `--doc` | Afficher cette documentation | false |
| `--confirme-doc` | Confirmer la lecture de la documentation | false |
| `--version` | Afficher la version | - |

## Sortie

Le format table affiche une entite par bloc, puis chaque flag avec son nom,
son type, son statut requis ou optionnel et sa description. Le format JSON
retourne les cles `version`, `flags_partages` et `entites`.

Chaque flag normalise contient au minimum :

- `nom` et `flag`
- `type`
- `obligatoire`
- `description`
- `source`
- `positionnel`

Les sources sont fusionnees par nom normalise afin d eviter les doublons
entre catalogue et `argparse`.

## Sources

- `cerveau-projet/agents/tools/generateurs/generateurs-commande/catalogue-commandes.json`
- `cerveau-projet/agents/tools/combos/**/definition-combo.json`
- les scripts Python references par `script` dans le catalogue

Les declarations `add_argument` sont extraites par le module standard
`ast`. Aucun script decouvert n est lance.

## Regles

- Le nom respecte le prefixe de categorie `lister-`.
- Le code utilise uniquement la bibliotheque standard Python.
- Les chemins sont resolus depuis la racine contenant `AGENTS.md`.
- Le mode reel est protege par la lecture de cette documentation ; le mode
  `--dry-run` est libre car l outil est en lecture seule.
- Les sorties JSON sont ASCII pour rester compatibles avec Git Bash.

## Limites connues

- Les commandes de combo avec des variables deja composees sont analysees
  comme des commandes textuelles ; leur provenance exacte peut rester
  partielle.
- Les scripts Python qui construisent dynamiquement leurs arguments peuvent
  fournir moins de details AST que le catalogue.
- Les arguments positionnels sont listes comme des flags logiques avec
  `positionnel: true` et un champ `flag` vide.

## Outils proches

| Outil | Complement |
|---|---|
| `lister-outils` | Inventorie les outils par categorie |
| `generateurs-commande` | Compose des commandes a partir du catalogue |
| `combos-moteur` | Execute une definition de combo |
| `lister-fonctions` | Explore la structure d un script |

## Pistes d extension

- `lister-variables` pour les variables requises par un outil ou combo.
- `lister-categories` pour les categories et leur couverture.
- `comparer-flags` pour les intersections et differences entre cibles.
- `detecter-flags-homonymes` pour les noms proches ayant des types differents.

## Historique

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-09-03 | Creation initiale : catalogue, combos, AST argparse, filtres et JSON |
