---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# DECISION -- BDD DE RAISONNEMENT (MO-443 / EO-399)

> Decision du CREATEUR, 2026-09-27, en reponse a MO-443 (question du stockage des
> SEGMENTS de raisonnement et du couplage lecon/segment). Ce document TRACE la
> decision ; il ne l execute pas (l execution se depose en missions, 4.1).

## LE FAIT MESURE (MO-395)
Les segments se trouvent par CARTE (moteur : --champ type segment --prive rend un
document) mais PAS par la liste des SOURCES du moteur (BDD_SOURCES) -- un segment
n est pas une entree de JSONL.

## LA DECISION DU CREATEUR (2026-09-27)
1. OPTIMUS A SON CONCEPT PROPRE : une BDD DE RAISONNEMENT pour Optimus.
2. LE CAMELEON AURA UN CONCEPT SEMBLABLE MAIS DISTINCT : sa propre BDD de
   raisonnement, SEPAREE de celle d Optimus.
3. Le COUPLAGE lecon/segment (raisonnement et lecons utilises ensemble) se traite
   PAR CE POINT 1 : chaque agent a sa BDD de raisonnement distincte, et le
   couplage vit dans cet ensemble.

## CE QUE CELA TRANCHE
Ni (a) seul, ni (b) seul : une BDD DE RAISONNEMENT PAR AGENT (une pour Optimus,
une pour le cameleon), DISTINCTES. L invisibilite L-016 reste tenue : la BDD
d Optimus vit dans la zone invisible ; celle du cameleon, dans la sienne.

## EXECUTION (deposee en items)
- construire la BDD de raisonnement d OPTIMUS (outil-bdd, zone invisible) ;
- construire la BDD de raisonnement du CAMELEON (concept distinct).

## COMMENT (decision du createur 2026-09-27, reprise de MO-482)
- A) ETENDRE `dupliquer-template` : option `--zone privee`, surcharge
  `templates/outil-bdd-prive/` (constants + DESCRIPTION prives) ; la cible est la
  ZONE INVISIBLE `_operateur/optimus-prime/raisonnement/` (frere de `matrice/`).
- DECLARER une SOURCE PRIVEE dans le moteur (`BDD_SOURCES_PRIVEES`), servie
  SEULEMENT sous `--prive`, refusee sans (L-016).

## EXECUTE (MO-482)
- EO-458 : outil `bdd-raisonnement` + BDD `segments.json` dans
  `_operateur/optimus-prime/raisonnement/` ; source privee `segments` declaree au
  moteur ; MAILLON 53 de la suite ; fiche 41 du manuel. PREUVE : mouvement.
- EO-459 (BDD du CAMELEON, concept distinct) : EXECUTE par MO-483. La BDD du
  cameleon vit dans SON domicile `agents/cameleon/raisonnement/` (VISIBLE et
  PARTAGEE entre les deux agents, decision createur 2026-09-27, precisee en
  seance) ; le moteur la sert en SOURCE PARTAGEE `segments-cameleon`, SANS
  `--prive`. Le generateur gagne une zone NOMMEE `cameleon` (table ZONES) a cote
  de `privee`.
