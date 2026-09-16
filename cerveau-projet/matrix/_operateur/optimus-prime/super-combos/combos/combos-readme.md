---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
---

### definition d'un combos:
    un combos est un ensemble de de mini-missions raccorder ensemble pour former un mission unique (traitement de fichier, correctif, test, etc)

## CONTRAT DE NOMMAGE (obligatoire, convention CV-008 -- BDD conventions-matrice)

> Decision createur 2026-09-13 : **un combo porte TOUJOURS un numero, visible
> dans le nom** (`c-001-<slug>/`, id `c-001`). Meme regle pour les super-combos
> (`sc-001-<slug>/`, id `sc-001`) : voir `../super-combos-readme.md`.
> IDs en MINUSCULES (regle CV-009) : le `C-` majuscule est reserve au champ
> `constat` fige de `historiques-missions.jsonl`.
> Numero zero-padde sur 3, **jamais reutilise**. Source de verite :
> `registry.json` (section `combos`, compteur `c`) -- **la notre** : depuis le
> 2026-09-13 (MO-067) chaque famille a SON registre, a cote de ses objets. Les
> super-combos sont un cran au-dessus, dans `../` (`../registry.json`).
> Les outils (`outils/`) ne sont pas numerotes, et les objets d'une AUTRE famille
> (les super-combos) n'y sont pas listes : un objet se juge contre le registre de
> SA famille.

## Combos disponibles

| Numero | Nom | BDD | Point d'entree |
|---|---|---|---|
| `c-001` | `c-001-lecons/` | lecons.json | `c-001-lecons/main.py` |
| `c-002` | `c-002-variables/` | classeur-variables.json | `c-002-variables/main.py` |
| `c-003` | `c-003-historique/` | historiques-missions.jsonl | `c-003-historique/main.py` |
| `c-004` | `c-004-modifications/` | modifications-par-fichier.json | `c-004-modifications/main.py` |
| `c-005` | `c-005-usages/` | usages-outils-combos.jsonl | `c-005-usages/main.py` |
| `c-006` | `c-006-activites/` | activites-recentes.json | `c-006-activites/main.py` |
| `c-007` | `c-007-frictions/` | frictions.db | `c-007-frictions/main.py` |

Ces sept combos sont generes par `outils/creer-combo.py` a partir de la banque
`outils/banque-combos-bdd.json` (imperatif 46). Chacun chaine :
**lire** (filtre par tags) -> **normaliser** -> **noter usage**.

## Verifier le nommage

```bash
python outils/creer-combo.py lister            # etat numerote (disque vs registre)
python outils/creer-combo.py verifier c-001-lecons
```

> `outils/` n'est PAS un combo : c'est la boite a outils (generateurs, BDD,
> validation), non numerotee.