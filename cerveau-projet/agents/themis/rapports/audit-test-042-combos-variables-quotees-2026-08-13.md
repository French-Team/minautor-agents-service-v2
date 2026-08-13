---
titre: Audit croise du garde-fou test-042 (combos-variables-quotees)
date: 2026-08-13
auditeur: Themis
verdict: VALIDE
---

# Audit croise : test-042 + correction des 8 commandes de combos

## Contexte

Morpheus a cree test-042 (les {var} des commandes de cases outil des
definitions-combo.json doivent etre quotes, sauf commande = exactement
{var}) et corrige 8 commandes existantes non conformes.

## Verifications (9/9)

| Point | Verification | Resultat |
|---|---|---|
| T1a | test-029 conformite template : 14/14 (42 tests) | VALIDE |
| T1b | test-042 : 4/4 | VALIDE |
| T2 | 8 commandes corrigees (0 {var} non quote restant) | VALIDE |
| T3a | lanceur : 1 seul bloc SERIES | VALIDE |
| T3b | test-042 dans la serie e | VALIDE |
| T3c | test-042 dans DUREES_CONNUES | VALIDE |
| T3d | lanceur compile OK | VALIDE |
| T4 | test-024 : 13/13 en commande directe (artefact ecarte) | VALIDE |
| T5 | normes ASCII/LF 0/0 (test-042 + 3 definitions) | VALIDE |

## Verdict

**VALIDE** : le garde-fou test-042 est conforme, les 8 commandes sont
corrigees, le lanceur est sain. Aucun ecart.
