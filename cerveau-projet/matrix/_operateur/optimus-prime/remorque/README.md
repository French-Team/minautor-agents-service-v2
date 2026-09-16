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
- `etat` vert avant chaque mission d envergure (bilan-matrice le rappelle).
