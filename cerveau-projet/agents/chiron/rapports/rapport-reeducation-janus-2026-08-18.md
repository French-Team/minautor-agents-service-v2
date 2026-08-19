---
identite:
  type: rapport
  appartient_a: commun
  commun: true
---
# Rapport de re-education Chiron -- Janus

**Date** : 2026-08-18
**Demande** : Cerberus (via audit Themis A REVOIR) - l utilisateur se demande
si Janus a ete eduque et si sa carte est conforme. Janus a ete observe en
train de "suivre sa carte" (enumerer les verifications puis activer le maillon
suivant) - comportement qui est CONFORME a sa carte, mais sa carte manque de
garde-fous pedagogiques pour les cas limites.

## Diagnostic

La carte de Janus (v0.4.20) est **structurellement saine** :
- version JSON = 0.4.20, fiche PARCOURS (v0.4.20) - synchronisees
- 51 cases (28 action, 7 question, 11 fin, 5 controle)
- c27 -> c28 (mission hors parcours -> activer l agent habilite)
- c9g (boucle KO : activer l agent habilite pour reparer)
- Pattern 17 (c9c/c9d : generateur d abord + delegation)
- c10 (FIN - Reactiver Cerberus, dernier maillon)
- verifier-conformite-fiche janus : CONFORME
- bumper --tous : 0 outil incoherent

MAIS elle est **pedagogiquement en retard** (exactement le diagnostic que
j avais fait pour Themis, lecon #23) :

| Garde-fou | Themis (re-eduquee v0.4.10) | Janus (v0.4.20) |
|---|---|---|
| Indice de classification en c1 (GARDE-FOU C1) | [OK] | [KO] ABSENT (0 indice) |
| Redirection "outil bloque" par le verrou (c21/c22) | [OK] | [KO] ABSENT |
| Indice AGENTS HABILITES dans la case d activation | [OK] | [KO] ABSENT (c28) |

Preuve concrete : pendant l audit Themis, le verrou a bloque Themis sur
valider-cartes-decision (habilites : argus, buffy, janus, vulcain) - sa carte
re-eduquee a correctement redirige. La carte de Janus n a pas d equivalent.

## Corrections de formation proposees (3)

1. **c1 : ajouter l indice GARDE-FOU C1** (modele Cerberus/Themis) : la case de
   classification doit porter un indice regle qui force la classification de
   la demande (branches explicites + cas "aucune branche -> autre").
2. **Ajouter une redirection "outil bloque"** (modele Themis c21/c22) : quand
   proteger-verrou-habilitation bloque un outil, la carte doit ordonner de
   signaler et d activer l agent habilite - jamais re-tenter, jamais s arreter.
3. **c28 : ajouter l indice AGENTS HABILITES** : Buffy cartes, Vulcain outils,
   Morpheus tests, Hygie suppression, Janus controle.

## Verdict

**A REVOIR** - carte structurellement saine, 3 corrections de formation
proposees (modele re-education Themis v0.4.10). CHIRON NE CORRIGE PAS : les
corrections de carte vont a Buffy (seule habilitee editer-parcours).

## Signale a Buffy

Re-education de Janus sur le modele Themis v0.4.10 :
1. c1 : indice GARDE-FOU C1.
2. Nouvelle redirection "outil bloque" -> c28 (activer l agent habilite).
3. c28 : indice AGENTS HABILITES.
4. Bump de version de la carte (0.4.20 -> 0.4.21) + synchronisation fiche.
