# Rapport Morpheus -- Non-regression de la chaine tokens + coexistence

**Date** : 2026-08-19
**Chaine** : Vulcain -> Morpheus -> Janus -> Cerberus

## Corrections testees

| Defaut | Correctif | Verdict |
|---|---|---|
| D1 catalogue+combos (Vulcain) | audit-general defaut '.', combos-valider-cerveau sans argument, 3 combos | CONFORME |
| D2/D5 carte themis (Buffy) | chemins c3/c25 + outils c17, v0.5.1, fiche sync | CONFORME |
| Coexistence chrono v0.1.2 (Vulcain) | etat par session + liste tous les actifs | CONFORME |

## Adaptations de tests (SEUL Morpheus, regle immuable)

Pins obsoletes apres bumps (catalogue 0.2.14->0.2.16, index-tools 203->204) :
- test-005 : version catalogue 0.2.15 -> 0.2.16 (3 mentions) -> 27/28 (1 KO = verrou)
- test-060 : Total 203->204, catalogue 185->186 -> 12/12
- test-079 : Total 203->204, catalogue 185->186 -> 15/15
- test-007 : Total 203->204, catalogue 185->186 -> 15/15
- test-024 : catalogue 185->186 -> 17/17 (le KO preexistant tmp-janus a disparu)

## Correction de donnees

Registre : 3 entrees de la session llm-4 (opencode) avec agents en MAJUSCULES (Cerberus, Vulcain) -> normalisees en minuscules + contexte marque + re-tri. analyser-noms-maj --zone registre : KO -> OK (0 probleme). Regle : agents du registre toujours en minuscules.

## Non-regression (tests individuels, le lanceur est exclusif Janus)

- Profil cartes : 006 VALIDE, 013 22/22, 016 20/20, 058 CONFORME
- Profil outils : 067 PROPRE, 092 9/9, 098 7/7, 060 12/12, 079 15/15, 007 15/15, 024 17/17, 001 11/11, 002 37/37
- Generateurs/catalogue : 005 27/28 (1 KO verrou attendu), 040 5/5, 095 8/8
- Documentation : 048 8/8, 035 10/10, 028 8/8
- evaluer-processus global : 0 probleme
- Bumper (test-067) : PROPRE
- ASCII/LF : tous les fichiers modifies purs

## KO restant (attendu, verrou)

- test-005 point 21 : valider-cartes-decision --agent atlas -> KO pour Morpheus (outil habilite argus/buffy/janus/themis/vulcain uniquement). Verrou d habilitation, pas une regression. A verifier par Janus.

## Verdict

**CONFORME** -- toutes les corrections de la chaine passent la non-regression. Les pins obsoletes sont adaptes, le registre est normalise. Relais : JANUS (controle final) -> Cerberus (bilan consolide).
