---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
---

# c-002-variables

> **Combo numerote c-002** -- le numero est OBLIGATOIRE et jamais reutilise
> (contrat de nommage obligatoire CV-008 -- BDD conventions-matrice,
> decision createur 2026-09-13).

Combo dedie a la BDD **Classeur des variables (classeur-variables.json)** (`variables`).

> Classeur des variables : valeurs vivantes de la Matrice (defcon, perimetre-cameleon, etc.), lues par cle ou par tag.
> Genere par `creer-combo.py` (imperatif 46) le 2026-09-13 10:43:41.

## Chaine

1. **lire** : outil `matrice/data/outils/bdd-variables/main.py`, commande `lire` (filtre `--tag <tag>`)
2. **normaliser** : compte les lignes utiles
3. **noter usage** : piste dans `matrice/data/outils/bdd-usages/main.py` (tags `combo,bdd,variables`)

## Usage

```bash
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/c-002-variables/main.py executer [--tag <tag>] [--mission <id>]
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/c-002-variables/main.py lire [--tag <tag>]
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/c-002-variables/main.py status
```

## Tags de la BDD

defcon,perimetre
