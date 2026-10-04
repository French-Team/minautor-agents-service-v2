---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
---

# c-007-frictions

> **Combo numerote c-007** -- le numero est OBLIGATOIRE et jamais reutilise
> (contrat de nommage obligatoire CV-008 -- BDD conventions-matrice,
> decision createur 2026-09-13).

Combo dedie a la BDD **Frictions detectees (frictions.db)** (`frictions`).

> BDD des frictions : ce qui se repete et coute du temps, qualifie (type, gravite, frequence) pour cibler les corrections.
> Genere par `creer-combo.py` (imperatif 46) le 2026-09-13 10:43:42.

## Chaine

1. **lire** : outil `_operateur/optimus-prime/super-combos/combos/outils/bdd-frictions/main.py`, commande `lister` (filtre `--mission-id <tag>`)
2. **normaliser** : compte les lignes utiles
3. **noter usage** : piste dans `matrice/data/outils/bdd-usages/main.py` (tags `combo,bdd,frictions`)

## Usage

```bash
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/c-007-frictions/main.py executer [--tag <tag>] [--mission <id>]
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/c-007-frictions/main.py lire [--tag <tag>]
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/c-007-frictions/main.py status
```

## Tags de la BDD

ordre,outil,frequence
