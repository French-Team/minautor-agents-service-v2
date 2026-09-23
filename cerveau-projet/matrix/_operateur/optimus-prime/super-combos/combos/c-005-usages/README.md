---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
---

# c-005-usages

> **Combo numerote c-005** -- le numero est OBLIGATOIRE et jamais reutilise
> (contrat de nommage obligatoire CV-008 -- BDD conventions-matrice,
> decision createur 2026-09-13).

Combo dedie a la BDD **Usages des outils et combos (usages-outils-combos.jsonl)** (`usages`).

> Utilisation des outils et combos : pistage (code, duree, tokens avant/apres) filtrable par outil ou par tag.
> Genere par `creer-combo.py` (imperatif 46) le 2026-09-13 10:43:42.

## Chaine

1. **lire** : outil `matrice/data/outils/bdd-usages/main.py`, commande `lire` (filtre `--tag <tag>`)
2. **normaliser** : compte les lignes utiles
3. **noter usage** : piste dans `matrice/data/outils/bdd-usages/main.py` (tags `combo,bdd,usages`)

## Usage

```bash
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/c-005-usages/main.py executer [--tag <tag>] [--mission <id>]
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/c-005-usages/main.py lire [--tag <tag>]
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/c-005-usages/main.py status
```

## Tags de la BDD

outil,combo
