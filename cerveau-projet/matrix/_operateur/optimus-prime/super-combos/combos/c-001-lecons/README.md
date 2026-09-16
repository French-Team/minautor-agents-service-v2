---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
---

# c-001-lecons

> **Combo numerote c-001** -- le numero est OBLIGATOIRE et jamais reutilise
> (contrat de nommage obligatoire CV-008 -- BDD conventions-matrice,
> decision createur 2026-09-13).

Combo dedie a la BDD **Lecons (lecons.json)** (`lecons`).

> Lecons gravees (L-XXX) : le pilote peut injecter les dernieres lecons qui concernent la mission, triees par tags.
> Genere par `creer-combo.py` (imperatif 46) le 2026-09-13 10:43:41.

## Chaine

1. **lire** : outil `matrice/data/outils/bdd-lecons/main.py`, commande `lire` (filtre `--tag <tag>`)
2. **normaliser** : compte les lignes utiles
3. **noter usage** : piste dans `matrice/data/outils/bdd-usages/main.py` (tags `combo,bdd,lecons`)

## Usage

```bash
python main.py executer [--tag <tag>] [--mission <id>]
python main.py lire [--tag <tag>]
python main.py status
```

## Tags de la BDD

lecon,regle,piege
