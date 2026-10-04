---
titre: Controle croise final du garde-fou test-042 (combos-variables-quotees)
date: 2026-08-13
controleur: Janus
verdict: VALIDE
---

# Controle croise final : test-042 + correction des 8 commandes de combos

## Contexte

Morpheus a cree test-042 (les {var} des commandes de cases outil des
definitions-combo.json doivent etre quotes, sauf commande = exactement
{var}) et corrige 8 commandes existantes. Themis a audite (9/9 VALIDE).

## Verifications J1-J4 (8/8)

| Point | Verification | Resultat |
|---|---|---|
| J1a | test-029 conformite template : 14/14 (42 tests) | VALIDE |
| J1b | test-042 : 4/4 | VALIDE |
| J2 | 8 commandes corrigees (0 {var} non quote) | VALIDE |
| J3a | lanceur : 1 seul bloc SERIES | VALIDE |
| J3b | test-042 dans la serie e | VALIDE |
| J3c | test-042 dans DUREES_CONNUES | VALIDE |
| J3d | lanceur compile OK | VALIDE |
| J4 | normes ASCII/LF 0/0 (5 fichiers) | VALIDE |

## Non-regression complete (J5)

**42/42 OK** - chrono : nombre de tests change (41 -> 42), nouvelle base
enregistree : 45.9 s. Aucun KO.

## Verdict

**VALIDE** : le garde-fou test-042 est conforme, les 8 commandes sont
corrigees, le lanceur est sain. La non-regression complete passe avec
42/42 tests.
