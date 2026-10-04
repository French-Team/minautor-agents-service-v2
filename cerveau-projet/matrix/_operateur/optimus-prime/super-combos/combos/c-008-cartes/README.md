---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
  version: 1
  date: 2026-09-26
---

# c-008-cartes

> **Combo numerote c-008** -- le numero est OBLIGATOIRE et jamais reutilise
> (contrat de nommage obligatoire CV-008 -- BDD conventions-matrice,
> decision createur 2026-09-13).

Combo dedie a la BDD **Cartes d identite (corpus .md)** (`cartes`).

> Cartes d identite du corpus comparees a leur modele (MO-430) : presence des champs et conformite, rendue par carte-comparer. SOURCE NON BDD (decision createur 2026-09-26) : la source est le corpus .md de la Matrice ; sans tag, le combo rend l inventaire du corpus entier.
> Genere par `creer-combo.py` (imperatif 46) le 2026-09-26 19:50:46.

## Chaine

1. **lire** : outil `matrice/data/outils/carte-comparer/main.py`, commande `comparer` (filtre `--modele <tag>`)
2. **normaliser** : compte les lignes utiles
3. **noter usage** : piste dans `matrice/data/outils/bdd-usages/main.py` (tags `combo,bdd,cartes`)

## Usage

```bash
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/c-008-cartes/main.py executer [--tag <tag>] [--mission <id>]
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/c-008-cartes/main.py lire [--tag <tag>]
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/c-008-cartes/main.py status
```

## Tags de la BDD

complet, minimal
