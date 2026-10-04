# Controle croise : test-023-grep-budget-pondere

**Date** : 2026-08-11
**Controleur** : Janus (second controle, chaine Cerberus -> Morpheus -> Janus)
**Objet** : verification croisee du test-023-grep-budget-pondere cree par Morpheus (garde-fou non-regression materialisant l'etape E7 du protocole-verification-coherence v0.2.0)

---

## Verdict : VALIDE

## Controles J1-J7

| # | Controle | Resultat |
|---|---|---|
| J1 | Catalogue : 141 commandes, trie, test-023 present ; index-tools coherent (les tests n'y sont pas listes individuellement, comme test-022) | OK |
| J2 | test-023 execute : 26/26 OK ; normes py + md : 0 non-ASCII, 0 CRLF | OK |
| J3 | test-007-figer-lf reverdi (point 13 : 141 + entree test-023) | OK (15/15) |
| J4 | Non-regression complete (test-001 a test-023) | OK (23/23) |
| J5 | Pertinence : 6 fichiers couverts, 4 valeurs x 4 fichiers textes (16 pts), 6 constantes code (6 pts), anti-recurrence 2 pts | OK (26 pts) |
| J6 | Autonomie : imports stdlib uniquement (io, os, sys), lit les fichiers reels | OK |
| J7 | Format sortie `=== RESULTAT : %d OK / %d KO ===` + return 1 si KO | OK |

## Detail du travail verifie

1. **test-023-grep-budget-pondere.py** (26 points) :
   - P1-P16 : '100 car' / '0,5' / '3,0' / '160' presents dans chacun des 4
     fichiers textes (spec-refonte, spec-valider-case, spec-guider-parcours,
     valider-case.md)
   - P17-P19 : valider-case.py contient SEUIL_COURT = 100, BUDGET_INDICES = 3.0,
     SEUIL_TEXTE = 160
   - P20-P22 : generateurs-case.py contient SEUIL_COURT = 100,
     BUDGET_INDICES = 3.0, SEUIL_REGLE_DEFAUT = 160
   - P23-P24 : anti-recurrence : '> 3 indices' / 'plus de 3 indices' ABSENTS
     des 6 fichiers
   - P25-P26 : normes du test (ASCII strict, LF pur)
2. **test-023-grep-budget-pondere.md** : documentation conforme (Testeur,
   Date, Objet, Contexte, tableau des 26 points, Execution, Normes).
3. **Catalogue** : entree test-023 ajoutee (modele test-022), 141 commandes
   triees, LF pur, 0 non-ASCII.
4. **test-007** : point 13 mis a jour (140 -> 141 + entree test-023).

## Lecons Janus

1. Le grep croise E7 est desormais un test AUTOMATIQUE de la suite : toute
   divergence de seuil ou retour de l'ancienne regle fera KO au test-023.
2. L'ajout d'une commande au catalogue doit toujours s'accompagner de la mise
   a jour de test-007 (compteur) dans la MEME mission -- la lecon Morpheus
   le documente.
3. Le test est autonome (stdlib) et lisible : il materialise exactement les
   exigences de l'etape E7 du protocole.

## Fichiers verifies

- cerveau-projet/agents/tools/tester/tests/test-023-grep-budget-pondere/test-023-grep-budget-pondere.py
- cerveau-projet/agents/tools/tester/tests/test-023-grep-budget-pondere/test-023-grep-budget-pondere.md
- cerveau-projet/agents/tools/generateurs/generateurs-commande/catalogue-commandes.json (141 commandes)
- cerveau-projet/agents/tools/tester/tests/test-007-figer-lf/test-007-figer-lf.py (point 13 : 141)
