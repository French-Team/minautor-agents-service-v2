---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
---

# c-006-activites

> **Combo numerote c-006** -- le numero est OBLIGATOIRE et jamais reutilise
> (contrat de nommage obligatoire CV-008 -- BDD conventions-matrice,
> decision createur 2026-09-13).

Combo dedie a la BDD **Activites recentes (activites-recentes.json)** (`activites`).

> Activites recentes par section (missions, alertes, passes, decisions), filtrables par tag.
> Genere par `creer-combo.py` (imperatif 46) le 2026-09-13 10:43:42.

## Chaine

1. **lire** : outil `matrice/data/outils/bdd-activites/main.py`, commande `lire` (filtre `--tag <tag>`)
2. **normaliser** : compte les lignes utiles
3. **noter usage** : piste dans `matrice/data/outils/bdd-usages/main.py` (tags `combo,bdd,activites`)

## Usage

```bash
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/c-006-activites/main.py executer [--tag <tag>] [--mission <id>]
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/c-006-activites/main.py lire [--tag <tag>]
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/c-006-activites/main.py status
```

## Tags de la BDD

missions,alertes
