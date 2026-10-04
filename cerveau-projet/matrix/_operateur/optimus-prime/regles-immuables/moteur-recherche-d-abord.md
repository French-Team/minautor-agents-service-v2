---
identite:
  type: regle-immuable
  appartient_a: optimus-prime
  commun: false
---

# REGLE IMMUABLE -- NOTRE MOTEUR D ABORD, L OUTIL NATIF EN DERNIER RECOURS

> Grave le 2026-09-24 (mission MO-375, chaine [???] 3/4 ; mesure MO-368,
> audit-moteur-et-cartes.md ; demande du createur : comprendre pourquoi l agent
> emploie son outil natif de recherche au lieu de NOTRE moteur, et le rendre
> impossible).

## La regle

**Toute recherche dans le projet commence par NOTRE moteur** (la porte unique
`rechercher` : fichiers, BDD et cartes d identite). **L outil natif de recherche
est le DERNIER RECOURS**, et tout emploi de ce dernier est DIT.

- Le moteur du projet est SERVI dans TOUTE mission, par les deux voies, avec sa
  carte de mode d emploi : le plancher OUTILS_TOUJOURS (checklist/listes.py) est
  pose par injection/fonctions.py (_avec_plancher) et sa carte vient de
  injection/modes_emploi.py. Je n ai donc aucune raison de l ignorer.
- Un outil natif ne connait NI les cartes d identite, NI les BDD, NI les zones
  invisibles (L-016) : chercher avec lui d abord, c est interroger un corpus
  incomplet et lire un 0 comme un fait (lecon MO-055).
- Si le moteur est indisponible, ou si la recherche sort de son perimetre, je
  PEUX employer l outil natif : je le DIS alors dans mon bilan (quel outil,
  pourquoi, ce qu il a rendu). Un dernier recours muet redevient un premier
  reflexe.
- Un moteur qui rend 0 sur une requete en LANGAGE NATUREL se REPARE DANS le
  moteur (mots vides retires, pluriel tolere) : jamais a cote
  (defaut-outil-repare-sur-place.md).

## Ou la regle se LIT (les points que l agent relit)

1. Ce fichier (regle immuable, relue a chaque demarrage).
2. `regles-immuables-readme.md` : l index des regles immuables.
3. `optimus-prime.md` : la fiche (REGLES ABSOLUES), sa colonne Domicile.
4. Le CODE qui la SERT : `_avec_plancher` (injection/fonctions.py) sert le
   moteur en tete de toute mission ; `charger_modes_emploi` en joint la carte.

Sources : audit-moteur-et-cartes.md (MO-368) + OUTILS_TOUJOURS
(checklist/listes.py) + la regle `defaut-outil-repare-sur-place.md`.
