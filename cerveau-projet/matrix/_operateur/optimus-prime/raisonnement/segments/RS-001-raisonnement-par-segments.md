---
identite:
  type: segment
  appartient_a: optimus-prime
  commun: false
  version: 1
  date: 20260924
  liens: matrice/data/commun/carte_identite.py, _operateur/optimus-prime/protocoles/proto-11-raisonnement-progressif.md
---

# SEGMENT RS-001 -- raisonnement par segments

> Un SEGMENT est une PARTIE du raisonnement, jamais le raisonnement entier : il est
> PROGRESSIF (il a un AVANT -- le segment precedent -- et un APRES -- celui qui le
> suivra) et TRACE (il vit HORS de la fenetre de contexte, donc il survit a la
> session). Un raisonnement CONTINU n a pas de segments : il ne laisse rien derriere
> lui, et ce qu il a trouve se perd avec le contexte qui l a porte.

## La carte du segment (ce que le moteur retrouve)

| Champ | Valeur |
|---|---|
| **ID** | RS-001 |
| **Mission** | MO-395 |
| **Sujet du raisonnement** | raisonnement par segments |
| **Question posee** | Comment transformer un raisonnement continu en raisonnement progressif, trace et reutilisable ? |
| **Segment precedent** | AUCUN |
| **Etat** | ouvert |

## CE QUI EST ETABLI (le gain, CONCIS)

LE RAISONNEMENT PAR SEGMENTS EST ARME : (1) le TYPE segment est DECLARE dans la grammaire des cartes (matrice/data/commun/carte_identite.py) ; (2) le MOULE est pose et servi par poser-template-pilote (raisonnement/segment.md.moule, 12 jetons) ; (3) le PROTOCOLE est ecrit (proto-11) et indexe ; (4) ce segment est le PREMIER tour du cycle, pose PAR LA PORTE et non a la main. Choix tranche : un segment est un DOCUMENT a carte (un fichier par segment), pas une entree de JSONL -- c est ce qui le rend trouvable par --champ sans toucher au moteur, et c est la forme que la grammaire des cartes sait DEJA juger.

## CE QUI RESTE OUVERT (le segment suivant le prendra)

(1) la BDD RAISONNEMENT comme SOURCE du moteur : aujourd hui les segments se trouvent par CARTE (champ type segment + prive), pas par la liste des sources ; a trancher avec le cout du prive. (2) la BDD DES LECONS : pertinence sans surcharge (le plafond de 6000 tokens est atteint : 22 lecons injectees sur 141) et COUPLAGE lecon/segment. (3) un GARDE qui accuse un raisonnement long SANS segment : aujourd hui rien ne l exige.

## PREUVE (la commande qui REJOUE le constat)

python3 cerveau-projet/matrix/lancer.py rechercher rechercher --champ (type segment) --prive ; python3 cerveau-projet/matrix/lancer.py poser-template-pilote lister
