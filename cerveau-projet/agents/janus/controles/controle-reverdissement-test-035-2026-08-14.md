# Controle croise : reverdissement test-035 (Buffy -> Janus)

**Date** : 2026-08-14
**Agent controle** : Janus
**Mission controlee** : reverdissement test-035 (suite correction evaluer-processus par Vulcain)

## Contexte

Le test-035 (evaluer-processus) echouait sur 5 problemes. Vulcain a corrige l outil
evaluer-processus (v0.1.1 : missions les plus recentes au lieu des plus anciennes +
ignorer mode script-temporaire). Buffy a ensuite : retire les entrees erronnees
tester-lancer-non-regression du registre (morpheus/vulcain/buffy - seul Janus est
habilitE a lancer la non-regression), ajoute 3 outils a la carte janus (detecter-residus,
detecter-divergences-version, evaluer-processus en case c21, v0.4.3), ajoute
valider-cartes-decision a sa propre carte (case c14, v0.4.3) et adapte test-016.

## Verifications

| # | Verification | Resultat |
|---|---|---|
| J1 | evaluer-processus : 0 probleme de processus | OK |
| J2 | test-035 : 8 OK / 0 KO | OK |
| J3 | test-016 : 20 OK / 0 KO | OK |
| J4 | valider-cartes-decision --agent buffy : CONFORME | OK |
| J5a | Carte buffy version 0.4.3 | OK |
| J5b | valider-cartes-decision present en case c14 | OK |
| J5c | Normes ASCII 0 + LF pur (parcours, fiche, test-016) | OK |
| J6 | Registre : aucune entree tester-lancer non-janus | OK |
| J7 | Carte janus 0.4.3 : 3 outils presents en c21 | OK |
| J8 | Aucun test ne verifie la version de la carte janus (pas de KO induit) | OK |

## Verdict

**VALIDER : 10/10 OK** - test-035 reverdi, registre propre, cartes synchronisees,
normes respectees. La regle "seul Janus lance la non-regression" est respectee.
