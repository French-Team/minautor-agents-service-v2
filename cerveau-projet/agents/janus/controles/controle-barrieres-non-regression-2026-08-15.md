# Controle croise -- BARRIERES DE PASSAGE v0.4.0 (non-regression)

**Date** : 2026-08-15
**Controleur** : Janus (chaine Cerberus -> Vulcain -> Morpheus -> Janus)
**Verdict** : VALIDE (55 OK / 0 KO, 5 barrieres franchies)

## Philosophie (demande utilisateur)
Les series sont classees par IMPORTANCE (FONDATIONS D ABORD), chaque serie doit etre 100% verte pour FRANCHIR la barriere vers la suivante. Si une serie a un KO, la barriere appelle la protection STOP : la suite s arrete, le rapport de la serie est fourni pour constater/analyser/reparer. Toutes les barrieres passees -> rapport GLOBAL POSITIF.

## Deroulement observe (preuve reelle)
| Barriere | Serie | Resultat |
|---|---|---|
| A | Fondations (nommage, ASCII/LF, template, protections) | 11/11 FRANCHIE |
| B | Parcours et validateurs | 13/13 FRANCHIE |
| C | Outils et combos | 15/15 FRANCHIE |
| D | Registre et traces | 11/11 FRANCHIE |
| E | Anti-recurrence et garde-fous specifiques | 5/5 FRANCHIE |
| **GLOBAL** | | **55 OK / 0 KO** |

Le 1er run a prouve le STOP : BARRIERE B BLOQUEE (12/13, KO test-037) -> C/D/E non lancees, rapport immediat.

## Corrections Janus en controle
1. **Registre** : retrait de la declaration erronee vulcain/tester-lancer-non-regression (vulcain l a modifie, ne l a jamais lance - seul janus habilite). test-037 6/6.
2. **Fix chrono (reference partielle)** : la reference de temps n est geree QUE par un run COMPLET ET 100% VERT (reference_globale = not args.tests AND tot_ko == 0 AND tot_non_lances == 0). Un run bloque par une barriere ne touche pas la reference. Reference rebasee a 97.1 s (temps reel 55/55) -> CONFORME +0%, plus de SIGNAL +531% fantome. test-031 10/10, test-027 11/11.

## Adaptations Morpheus (verifiees)
test-027 11/11, test-032 10/10, test-031 10/10, test-024 16/16, test-051 12/12 (versions v0.4.0 + defaut BARRIERES + serie c pour test-001).

## Signal documente
Le mode barriere serie stricte est plus long que le pool (97.1 s vs 91.2 s historique) - CHOIX UTILISATEUR (plus direct, plus lisible, un KO visible immediatement). --parallele conserve le pool en option.

## Livrables
- tester-lancer-non-regression v0.4.0 (barrieres + fix reference partielle)
- 5 tests adaptes (027/032/031/024/051)
- Lecons : vulcain, morpheus, janus
