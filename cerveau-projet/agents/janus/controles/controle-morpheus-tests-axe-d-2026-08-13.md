---
identite:
  type: rapport-janus
  date: 2026-08-13
  objet: controle croise mission Morpheus (tests adaptes axe D Themis)
---

# Controle Janus : mission Morpheus (tests adaptes + non-regression)

**Contexte** : mission Janus (dernier maillon, active par Themis) - controle
croise final de l adaptation des 5 tests de version par Morpheus apres les
bumps des parcours (axe D Themis de Buffy).

## Verifications (J1-J5)

| Check | Resultat |
|---|---|
| J1. 5 tests adaptes (versions exactes) | test-004 morpheus v0.4.4 (0.4.3 absent), test-005 atlas v0.4.2, test-006 48 cases, test-016 action 40, test-017 contrat outil |
| J2. Compteurs parcours reels | buffy v0.4.2 : 8/40/10/5 (q/a/f/c) - coherent avec test-016 |
| J3. Normes ASCII/LF | 0/0 (rapport Themis, corrections Morpheus/Themis, 5 tests) |
| J4. Non-regression complete | 36/36 OK (pool-16, 42.5 s, chrono conforme) - apres relance sans script temporaire (artefact test-024 elimine) |
| J5. Residus temporaires | 0 script .tmp-* a la racine |

## Analyse

1. Les 5 adaptations sont exactes et coherentes avec les parcours reels
   (les compteurs du test-016 = types reels de buffy v0.4.2).
2. Le KO test-024 observe pendant l audit etait un artefact de methode : la
   non-regression etait lancee DEPUIS un script .tmp-* encore present a la
   racine (le garde-fou anti-scripts-temporaires le detectait). Relance
   propre : 36/36 OK. Aucun vrai ecart.
3. La cause racine test-017 (fenetre 6 lignes de generateurs-ligne) est bien
   documentee et l adaptation (contrat reel de l outil) est la bonne approche.

## Verdict : VALIDE

Mission Morpheus conforme, Themis VALIDE, non-regression 36/36 OK. Aucun
ecart. Fin de chaine : reactivation Cerberus avec le bilan consolide.
