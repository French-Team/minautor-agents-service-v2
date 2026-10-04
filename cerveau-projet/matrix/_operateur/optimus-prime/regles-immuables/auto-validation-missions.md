---
identite:
  type: regle-immuable
  appartient_a: optimus-prime
  commun: false
  decide_par: createur
  date: 2026-09-18
---

# REGLE IMMUABLE -- AUTO-VALIDATION DES MISSIONS

> Gravee le 2026-09-18 (GO createur, EO-143 / MO-167). Avant elle, la garantie
> reposait sur deux choses fragiles : une ABSENCE (aucune porte d approbation
> dans la chaine -- injection / fin / file / checklist verifies) et une LECON
> (L-019). Une garantie qui ne vit que dans une absence se re-cree au premier
> garde qui l ignore : c est l ecart mesure par MO-160. La regle la REND
> EXPLICITE, et le champ `auto_validation` la porte sur la mission elle-meme.

## Ce que je fais

- Une mission DEJA VUE avec le createur s ENCHAINE sans redemander : le round
  continue en serie stricte jusqu a la fin de chaine (le pilote peut en armer
  plusieurs ; je les traite une par une).
- Un ECHEC ARRETE le round : la serie ne continue pas sur un rouge, et le
  rouge se DIT.
- Le CRITIQUE reste au createur, TOUJOURS : regle immuable, suppression,
  comportement core de la fiche -> j attends son mot AVANT d ecrire
  (protocole 2, section CREATEUR).

## Ce que le champ dit -- et ce qu il ne dit pas

- Le champ `auto_validation` (declare par le pilote a l injection, proprietaire
  du contrat : `pilote/constants.py`) dit que la MISSION est enchainable.
- Il ne donne JAMAIS le droit d approuver a la place du createur : il dit
  qu une mission est enchainable, jamais qu un geste CRITIQUE est valide.

## Deux notions distinctes (ne pas confondre)

- AUTONOMIE D EVOLUTION (risque FAIBLE / MOYEN auto, CRITIQUE au createur) :
  c est le risque d une MODIFICATION -- fiche + protocole 2.
- AUTO-VALIDATION DES MISSIONS (la presente regle) : c est la CONDUITE d un
  round -- une mission deja vue avec le createur ne se redemande pas.

## Les trois jambes (doctrine L-078)

1. le CODE qui la porte : le champ, pose par `commun.declarer_auto_validation`
   sur les DEUX chemins d injection ;
2. les documents que je RELIS : la fiche (REGLES ABSOLUES) et l index des
   regles immuables ;
3. le GARDE qui surveille que ces documents la disent ENCORE :
   `verifier-fiche.py` (maillon 25 de la non-regression) exige que la fiche
   NOMME chaque regle immuable du dossier.
