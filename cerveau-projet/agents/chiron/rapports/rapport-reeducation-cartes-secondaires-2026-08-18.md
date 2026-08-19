---
identite:
  type: rapport
  appartient_a: commun
  commun: true
---
# Rapport de re-education Chiron -- cartes des agents secondaires

**Date** : 2026-08-18
**Demande** : Cerberus (via audit Themis A REVOIR) - verifier si les agents
secondaires ont leur carte conforme au modele pedagogique.

## Diagnostic

Les 10 cartes secondaires sont **structurellement saines** :
- versions sync (carte = fiche PARCOURS) : atlas 0.4.9, argus 0.1.12,
  hygie 0.1.8, clio 0.5.13, hermes 0.1.5, gardien 0.1.3, chiron 0.1.2,
  athena 0.3.6, promethee 0.3.7, minerve 0.3.7
- verifier-conformite-fiche : CONFORME pour les 10
- bumper --tous : 0 outil incoherent
- cases "Mission hors parcours" et d activation presentes

MAIS **pedagogiquement en retard** (exactement le diagnostic des cartes
principales avant re-education) :

| Agent | c1 indices | GARDE-FOU C1 | Redirection outil bloque | AGENTS HABILITES |
|---|---|---|---|---|
| atlas (0.4.9) | 0 | KO | KO | KO |
| argus (0.1.12) | 0 | KO | KO | KO |
| hygie (0.1.8) | 0 | KO | KO | KO |
| clio (0.5.13) | 0 | KO | KO | KO |
| hermes (0.1.5) | 0 | KO | KO | KO |
| gardien (0.1.3) | 0 | KO | KO | KO |
| chiron (0.1.2) | 1 (c1 action) | NA | OK (c10/c11) | KO (liste manquante) |
| athena (0.3.6) | 0 | KO | KO | KO |
| promethee (0.3.7) | 0 | KO | KO | KO |
| minerve (0.3.7) | 0 | KO | KO | KO |

Cas particulier : **chiron** - sa c1 est une ACTION (mission unique, pas de
branches de classification), donc le GARDE-FOU C1 classique ne s applique pas.
Ses redirections existent (c10 signaler a Buffy, c11 signaler a Vulcain) mais
l indice AGENTS HABILITES manque. Adaptation : completer c10/c11 avec la liste
des agents habilites.

## Corrections de formation proposees (modele Themis v0.4.10 / Janus v0.5.0)

Pour CHACUNE des 10 cartes :
1. **c1 : ajouter l indice GARDE-FOU C1** (branches exactes de chaque carte +
   case cible "autre"). Pour chiron : c1 est deja une action avec un indice
   "mission pas claire -> demander a Cerberus" - a completer, pas a remplacer.
2. **Ajouter la redirection "outil bloque"** dans la case "Mission hors
   parcours" (argus/gardien/hermes/hygie c29, clio c13, atlas c26,
   athena/promethee/minerve c18, chiron c10/c11 existantes).
3. **Ajouter l indice AGENTS HABILITES** dans les cases d activation (atlas
   c27, athena/promethee/minerve c19, clio c14, hygie c7/c9, argus c7/c8,
   chiron c10/c11) : Buffy cartes, Vulcain outils, Morpheus tests, Hygie
   suppression, Chiron education.
4. **Bump de version** + synchronisation fiche (Pattern 14) + resync lock.
5. **Limite : textes regle < 160 caracteres** (lecon Buffy, test-016).

## Verdict

**A REVOIR** - 10 cartes a re-eduquer (9 avec les 3 corrections, chiron avec
adaptation : completer les indices existants + liste AGENTS HABILITES).
CHIRON NE CORRIGE PAS : les corrections de carte vont a Buffy (seule
habilitee editer-parcours).

## Signale a Buffy

Re-education des 10 cartes secondaires sur le modele etabli :
1. c1 : indice GARDE-FOU C1 (adaptation pour chiron : c1 action).
2. Redirection "outil bloque" -> activer l agent habilite.
3. Indice AGENTS HABILITES dans les cases d activation.
4. Bump de version + sync fiche + resync lock + textes < 160 caracteres.
