---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
---

# remorque-optimus -- L attelage d Optimus

> Pendant du sac-a-dos du cameleon (qui note les usages), la remorque
> contient TOUS les equipements d Optimus : outils, combos, themes,
> protocoles, conventions. Strictement SEPAREE du sac-a-dos
> (convention-separation-cameleon-optimus) : jamais d equipement commun
> non declare.

## Contenu

- `inventaire.json` : liste generee des equipements (nom, type, chemin)
- `remorque-optimus.py` : `inventorier` (regenere) / `etat` (compare
  inventaire vs reel, signale manquants/inattendus)

## Regle

- Inventaire regenere APRES chaque naissance/suppression d equipement.
- `etat` vert avant chaque mission d envergure -- joue par le PRE-VOL du lanceur de
  non-regression (il REFUSE la suite en nommant l'ecart), par le bilan
  (`bilan-matrice.py`, section `[remorque]`) et par `/flux2` (cockpit). Mesure du
  2026-09-21 : cette ligne promettait ce rappel du bilan alors que
  `bilan-matrice.py` ne prononcait pas le mot ; la section `[remorque]` rend
  desormais la promesse VRAIE.

- Si le MOTIF des points de restauration est ILLISIBLE (domicile absent, import
  casse, nom disparu, motif invalide), la remorque REFUSE (code 2) et NOMME la
  cause et le remede : elle ne rend aucun verdict plutot que de compter un .bak
  comme equipement (L-121).
