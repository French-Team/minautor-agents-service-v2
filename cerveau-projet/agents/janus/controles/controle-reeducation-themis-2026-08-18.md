---
identite:
  type: controle
  appartient_a: janus
  commun: false
---

# CONTROLE JANUS -- REEDUCATION DE THEMIS

**Date** : 2026-08-18
**Objet** : controle du diagnostic de Chiron sur la carte de Themis v0.4.9 initiale (corrigee vers v0.4.10)
et des 3 corrections de formation proposees (rapport chiron/rapports/
rapport-reeducation-themis-2026-08-18.md)
**Diagnostic par** : Chiron (educateur)
**Verdict Chiron** : A REVOIR (3 corrections proposees, 2 hautes, 1 moyenne)

## Contexte

Session-llm-2 (kilo-llm) : Themis a recu la mission 'Inventaire et audit des
outils de performance' qui ne correspond a aucune branche de sa case c1. Elle
a improvise au lieu de repondre 'autre' -> c21 (hors perimetre), et a tente
editer-parcours (outil reserve a Buffy), bloque 2x par le verrou a 17:44:00.

Chiron a verifie : fiche CONFORME, parcours PROPRE (37/37 atteignables),
versions alignees (149/149, 0 divergence). Diagnostic : carte SAINE mais
GUIDAGE PEDAGOGIQUE MANQUANT.

## Corrections proposees par Chiron (a appliquer par Buffy)

1. **INC-1 (HAUTE)** : c1 (Mission) sans indice de classification - ajouter
   un indice regle modele GARDE-FOU C1 de Cerberus : une demande hors branches
   -> reponse 'autre' -> c21. JAMAIS improviser, JAMAIS outil hors carte.
2. **INC-2 (HAUTE)** : aucune redirection quand le verrou bloque un outil
   (message BLOQUE) - ajouter dans c21 un indice regle : verrou bloque = la
   demande concerne un autre agent -> OUI -> c22 (activer l agent habilite) ;
   ajouter dans c22 la liste des agents habilites (Buffy cartes, Vulcain
   outils, Morpheus tests, Hygie suppression, Janus controle).
3. **INC-3 (MOYENNE)** : c21 sans liste des domaines des autres agents -
   ajouter un indice regle : inventaire/exploration -> Atlas, contenu/cartes
   -> Buffy, outil -> Vulcain, tests -> Morpheus, suppression -> Hygie,
   controle -> Janus.

## Points de controle

1. Diagnostic Chiron valide (fiche + parcours + versions verifies)
2. Buffy activee et a applique les 3 corrections via editer-parcours
3. Carte themis revalidee : valider-cartes-decision themis CONFORME
4. Joignabilite : detecter-cablages themis PROPRE apres modification
5. Version parcours themis bumpee + fiche themis.md synchronisee (Pattern 14)
6. Normes : ASCII strict + LF pur sur carte + fiche + rapport
7. Evaluateur : 0 probleme de processus
8. Residus : 0

## Verdict final

<!-- a remplir en fin de controle -->
