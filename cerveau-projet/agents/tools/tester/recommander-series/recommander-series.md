---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# recommander-series

**Version :** 0.1.0
**Statut :** ebauche
**Categorie :** tester/

## Pourquoi cet outil ?

La non-regression grossit (84 tests, plus de 2 minutes). Pour reorganiser les
series efficacement, il faut des donnees : quels tests sont lents, quels tags
portent-ils, comment les regrouper pour equilibrer les series et reduire le
temps total (demande utilisateur 2026-08-16 : le rating et la performance
doivent aider a reorganiser les series).

## Ce qu il fait

Croise trois sources :
1. **Tags** : le bloc `Tags:` de la docstring de chaque test (categorisation).
2. **Durees** : registre-tests.jsonl (la duree la plus recente de chaque test).
3. **Decoupage** : suggestion de series (max tests / max duree par serie),
   les tests lents ensemble, les rapides ensemble, groupes par tag.

## Usage

```
python3 recommander-series.py
python3 recommander-series.py --test test-057
python3 recommander-series.py --max-par-serie 6 --max-duree 60 --rapport rapport-series.md
```

## Options

| Option | Role |
|---|---|
| `--test <nom>...` | Analyser un ou plusieurs tests (nom test-0XX) |
| `--max-par-serie N` | Nombre max de tests par serie suggeree (defaut 10) |
| `--max-duree N` | Duree max (secondes) par serie suggeree (defaut 60) |
| `--rapport <fichier>` | Ecrire un rapport markdown |
| `--verbose` | Detail |
| `--version` | Version de l outil |

## Contraintes

- ASCII strict, LF pur, 100% stdlib Python.
- L outil est en LECTURE SEULE : il ne modifie jamais les series du lanceur,
  il RECOMMANDE. L application se fait ensuite dans tester-lancer-non-regression
  (SERIES).
