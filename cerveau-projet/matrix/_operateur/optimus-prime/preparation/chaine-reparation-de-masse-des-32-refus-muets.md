---
identite:
  type: chaine
  appartient_a: optimus-prime
  commun: false
  titre: Reparation de masse des 32 refus muets
  statut: spec
  pense-bete: PB-002
  spec: SP-002
---

# Reparation de masse des 32 refus muets

## Pense-bete -- la demande clarifiee

CONSTAT MESURE (MO-202/MO-239) : 32 des 35 outils de la Matrice rendent un refus MUET -- code 2 et usage SEUL, l option fautive n est jamais NOMMEE ; l appel doit alors deviner parmi toutes les options, et le refus coute trois essais (friction 77). Le motif vit DEJA au domicile partage matrice/data/commun/options.py (signaler_inconnues, EO-179 -- le parseur RETIENT l inconnue) mais c est l APPELANT qui doit la DIRE : mesure, 110 fichiers appellent extraire_options et 3 lieux seulement la disent. PISTE A EXAMINER : que le domicile rende le refus IMPOSSIBLE A OUBLIER (signaler par DEFAUT au lieu d une fonction a appeler), puis generaliser par FAMILLE d outils au lieu de 32 rounds separes. PORTEE A MESURER AVANT TOUTE ECRITURE : 83 a 110 appelants, dont des appels qui acceptent des arguments LIBRES (refuser=False) et qui casseraient sur un refus global. INTERDIT : recopier le motif outil par outil (M-076, un seul domicile).

## Ce qui est deja mesure

(a ecrire)

## Ce qui reste a mesurer

(a ecrire)

