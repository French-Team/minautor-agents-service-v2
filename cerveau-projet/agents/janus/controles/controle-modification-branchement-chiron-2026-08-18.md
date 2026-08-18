---
identite:
  type: controle
  appartient_a: janus
  commun: false
---

# CONTROLE JANUS -- BRANCHEMENT CHIRON A L ACTIVATION

**Date** : 2026-08-18
**Objet** : controle de la modification de activer-agent-principal
(branchement de l agent chiron au dictionnaire AGENTS, bump 0.5.11 -> 0.5.12)
**Modifie par** : Vulcain (outil), verifie par Morpheus (tests)
**Verdict attendu** : VALIDE si tous les points conformes

## Contexte

Chiron (16e agent, educateur, cree 2026-08-17) etait INACTIVABLE : absent du
dictionnaire AGENTS de activer-agent-principal (py + sh). Meme oubli qu Argus
corrige en v0.5.8. Vulcain a ajoute l entree chiron (role, fiche, corrections)
au py + aux 3 case statements du sh, bumpe 0.5.11 -> 0.5.12 (py, sh, md, spec)
+ ligne versionning.

## Points de controle

1. **Nommage / coherence** : entree chiron presente dans le py (dictionnaire
   AGENTS) et dans les 3 fonctions du sh (role, fiche, corrections)
2. **Versions** : py, sh, md, spec tous a 0.5.12 ; ligne versionning 0.5.12
   ajoutee dans le .md ; bumper --tous 0 incoherent
3. **Resolution** : get_agent_info("chiron") retourne role + fiche + corrections
4. **Activation reelle** : activer-agent-principal activer session chiron OK
   (preuve de non-blocage "Agent inconnu")
5. **Tests** : les 10 tests utilisant l outil en interne (test-002/018/021/025/
   028/039/040/041/052/057) verts ; test-021 point 7 KO = artefact de verrou
   (valider-cartes-decision reserve a janus) -> doit reverdir sous cette session
6. **Evaluateur** : evaluer-processus 0 probleme (aucune declaration hors carte)
7. **Carte de chiron** : valider-cartes-decision chiron CONFORME (coherence
   fiche/parcours, version 0.1.2)
8. **Residus** : 0 residu (workspace propre)
9. **Normes** : ASCII strict + LF pur sur les 4 fichiers modifies + corrections
   vulcain/morpheus

## Signalements (preexistants, hors perimetre de cette mission)

- Le .sh etait en retard : argus, gardien et hermes ABSENTS des case statements
  (le .py les a, pas le .sh) -> parite py/sh a corriger par Vulcain
- Aucun test ne verifie la parite agents <-> dictionnaire AGENTS : un garde-fou
  est a prevoir pour eviter le 3e oubli de branchement

## Verdict final

<!-- a remplir en fin de controle -->
## VERDICT FINAL : VALIDE

**Points verifies (tous conformes)** :
1. Nommage/coherence : entree chiron presente dans le py (dictionnaire AGENTS)
   + dans les 3 fonctions du sh (role, fiche, corrections)
2. Versions : py/sh/md/spec tous a 0.5.12, ligne versionning 0.5.12 dans le md,
   bumper --tous 149/149 coherent
3. Resolution : get_agent_info("chiron") et "CHIRON" retournent role + fiche +
   corrections
4. Activation reelle : activer-agent-principal activer session-llm-1 chiron OK
   (plus aucun "Agent inconnu")
5. Tests : test-021 9/9 vert sous session janus (le KO morpheus etait l artefact
   de verrou valider-cartes-decision), test-037 6/6, test-002/018/025/028/039/
   040/041/052/057 verts (Morpheus)
6. Evaluateur : evaluer-processus 0 probleme (3 declarations fautives de ce
   round retirees du registre : vulcain editer-fichier + valider-conformite-ascii,
   morpheus tester - hors carte)
7. Carte chiron : valider-cartes-decision CONFORME (10/10, coherence fiche/
   parcours v0.1.2)
8. Residus : 0 (cerveau-projet + workspace)
9. Normes : ASCII 0 non-ASCII + LF pur sur les 4 fichiers outil + corrections
   vulcain/morpheus + rapport de controle

**Signalements (preexistants, hors perimetre de cette mission)** :
1. Le .sh etait en retard : argus, gardien et hermes ABSENTS des case
   statements (le .py les a, pas le .sh) -> parite py/sh a corriger par Vulcain
2. Aucun test ne verifie la parite agents <-> dictionnaire AGENTS : un garde-fou
   est a prevoir pour eviter le 3e oubli de branchement (Argus v0.5.8, Chiron v0.5.12)
3. La mission initiale de reeducation de Themis (carte en retard + redirection
   mission inconnue/outil non autorise) reste a executer par Chiron - le
   branchement de Chiron etait le PREREQUIS technique (il etait inactivable)
