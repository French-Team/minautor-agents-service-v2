---
identite:
  type: protocole
  appartient_a: optimus-prime
  commun: false
---

# Proto 5 -- Auto-amelioration (Optimus Prime)

> Doctrine du createur (lecon 2026-09-06) : les outils natifs ne donnent
> pas de resultats 100% corrects. Des qu'on GALERE avec un outil natif,
> on ne subit pas : on declenche la creation de l'outil equivalent.
> Corriger a la main, encore et encore, est le signe qu'on a rate le
> declenchement, pas une methode de travail.

## PRINCIPE

- Un correctif manuel est un signal d'alarme, jamais une routine.
- Le bon reflexe : galere native -> theme "creer l'outil".
- L'outil cree devient la PORTE UNIQUE : apres lui, l'outil natif n'a
  plus le droit de toucher cette tache.
- Doctrine etendue : l'outil natif produit le reste, la Matrice possede
  et verifie ce qui compte (etat, verification).

## ETAPE 1 -- DETECTER (des que ca coince)

1. Deuxieme fois que le meme outil natif me fait perdre du temps ou
   m'oblige a reparer a la main -> seuil atteint (une galere isolee
   se note en BDD ; une galere repetee declenche le protocole).
2. Nommer en une phrase : "Quand <tache>, l'outil natif <probleme>,
   car <cause>."
3. Noter la friction en BDD SANS interrompre la mission en cours.

## ETAPE 2 -- TRANCHER (fin de mission, avec le createur)

1. La tache est-elle RECURRENTE ? (une fois = note BDD, pas d'outil)
2. Le resultat natif est-il fiable a 100% ? (si non -> outil)
3. Des correctifs a la main sont-ils prevus ? (si oui -> outil :
   c'est le signal fort, corriger a la main est interdit en serie)
4. Le createur valide le declenchement (son mot fait foi, toujours).

## ETAPE 3 -- CREER (mission DISTINCTE, jamais en marge)

1. La creation devient UNE MISSION du pilote (theme dedie), jamais une
   tache cachee dans une autre mission (serie stricte).
2. Conventions obligatoires : convention-architecture-outils (point
   d'entree global -> categories -> fonctions simples), zero valeur
   en dur, py_compile global, tests reels, relecture sur disque.
3. Des sa naissance, l'outil ecrit son etat via la porte unique (BDD).

## ETAPE 4 -- BASCULER (la porte change de main)

1. Tester l'outil sur les VRAIES donnees (migration comprise).
2. Verifier l'equivalence : tout ce que l'outil natif faisait,
   l'outil le fait (sinon il n'est pas pret a basculer).
3. Mettre a jour les contrats (readme) : l'usage natif de cette tache
   devient INTERDIT (porte unique).
4. Noter la bascule en BDD ; l'espion surveille le nouvel etat.

## INTERDICTIONS

- JAMAIS enchainer les correctifs a la main sans declencher :
  2 correctifs sur la meme tache native = protocole viole.
- JAMAIS creer l'outil DANS une autre mission (serie stricte).
- JAMAIS garder deux portes pour la meme tache : apres bascule,
  l'outil natif ne touche plus cette tache.
- JAMAIS basculer sans verification : l'outil est teste AVANT
  que l'ancien usage soit interdit.
