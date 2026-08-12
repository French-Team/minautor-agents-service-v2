# Controle croise -- Round 10 : series du lanceur de non-regression

**Date** : 2026-08-12
**Controleur** : Janus (session-llm-1)
**Objet** : tester-lancer-non-regression v0.1.2 (--series + --parallele) + test-024 adapte + test-027 cree
**Verdict** : VALIDE (J1-J7 verts)

---

## Verifications

| # | Verification | Resultat |
|---|---|---|
| J1 | 4 series couvrant les 27 tests (A=6, B=10, C=6, D=5), 27 prefixes, 0 doublon, version 0.1.2 | VALIDE |
| J2 | --series z -> code 2 (message usage, sans traceback) | VALIDE |
| J3 | test-024 13/13 (version v0.1.2) + test-027 9/9 (couverture, chevauchement, isolation, normes) | VALIDE |
| J4 | Non-regression 27/27 en mode serie ET en mode --parallele (A=6, B=10, C=6, D=5) | VALIDE |
| J5 | Catalogue : 0 a ajouter (dry-run), 146 commandes intactes | VALIDE |
| J6 | Normes ASCII 0 + LF 0 (lanceur .py/.md, test-024, test-027, lecons Vulcain/Morpheus) | VALIDE |
| J7 | Parite : outil py seul (pas de .sh), entree catalogue intacte | VALIDE |

## Bilan

Le round 10 est conforme : la suite de non-regression est decoupee en
4 series thematiques, le mode --parallele donne exactement le meme resultat
que le mode serie (27/27), le registre reste protege (archive une seule fois
par le processus parent), et le garde-fou test-027 verrouille la couverture
des series (tout futur test sans serie fera KO). Gain mesure : 45s -> 21s.
