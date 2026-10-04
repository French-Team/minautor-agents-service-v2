# Controle croise : test-023 branche dans le parcours vulcain v0.3.7

**Date** : 2026-08-11
**Controleur** : Janus (second controle, chaine Cerberus -> Buffy -> Janus)
**Objet** : verification croisee du branchement du test-023-grep-budget-pondere dans le parcours vulcain (v0.3.6 -> v0.3.7) par Buffy

---

## Verdict : VALIDE

## Controles J1-J7

| # | Controle | Resultat |
|---|---|---|
| J1 | Parcours vulcain v0.3.7 : c6d/c12d presents, navigation c6c->c6d->c7 et c12c->c12d->c13 | OK |
| J2 | Poids des nouvelles cases : regles <= 100 car. (79/94/90) + outil = 2,0 <= budget 3,0 | OK |
| J3 | valider-cartes-decision --agent vulcain | OK (CONFORME) |
| J4 | Navigation reelle : flux construire atteint c6d ([43/47]), flux modifier atteint c12d ([46/47]), fins c9/c15 atteintes | OK |
| J5 | Fiche vulcain.md : 3x v0.3.7, 0x v0.3.6, 0 non-ASCII, 0 CRLF | OK |
| J6 | Non-regression complete (test-001 a test-023) | OK (23/23) |
| J7 | Diff minimal : 0 modification c6c/c12c par Buffy ; ecart 198 car. des cases c6c/c12c CONFIRME PREEXISTANT (git HEAD deja NON CONFORME) | OK |

## Detail du travail verifie

1. **parcours-vulcain.json v0.3.7** : 2 nouvelles cases action ajoutees,
   pattern c6c/c12c respecte (3 regles courtes + 1 indice outil) :
   - c6d (flux CONSTRUIRE) : "Lancer le test-023-grep-budget-pondere
     (coherence budget pondere)", c6c.suivant = c6d, c6d.suivant = c7
   - c12d (flux MODIFIER) : idem, c12c.suivant = c12d, c12d.suivant = c13
   - Chaque case : poids 2,0 (3 regles <= 100 car. + 1 outil), 0 non-ASCII,
     0 CRLF, JSON valide, indent 1 + LF pur (round-trip identique).
2. **vulcain.md** : 3 mentions PARCOURS v0.3.6 -> v0.3.7 (REGLE ABSOLUE PARCOURS,
   lien Parcours, bloc FINS REELLES) -> croisement fiche/parcours conforme.
3. **Navigation reelle** : les 2 flux atteignent la nouvelle case et l'outil
   test-023 est affiche avec PASSE PAR LE GENERATEUR + LIRE AVANT USAGE.

## Observation (hors perimetre de la mission, preexistante)

Les cases c6c/c12c (scan detecter-decalages) ont un indice regle de 198 car.
(> 160) -> A ALLEGER. Confirme PREEXISTANT : git HEAD deja NON CONFORME avant
la mission Buffy. A traiter dans une mission ulterieure (alleger les textes
vers des references) -- pas un ecart de la mission.

## Lecons Janus

1. Le branchement d'un garde-fou dans un parcours passe par le pattern des
   cases scan/controle existantes (c6c/c12c) : CREATION LIMITEE + PASSE PAR
   LE GENERATEUR + indice outil.
2. Le budget pondere s'applique AUSSI aux cases de parcours : 3 regles
   longues + 1 outil = 3,5 > 3,0 -> il faut des textes <= 100 car. (poids 0,5).
3. Tout bump de parcours exige la mise a jour de la fiche dans la MEME mission
   (valider-cartes-decision croise fiche/parcours, Pattern 14 / E5b).

## Fichiers verifies

- cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json (v0.3.7)
- cerveau-projet/agents/vulcain/vulcain.md (3x v0.3.7)
- cerveau-projet/agents/tools/tester/tests/test-023-grep-budget-pondere/ (outil branche)
