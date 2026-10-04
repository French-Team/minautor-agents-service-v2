---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# CADRAGE EO-505 / MO-517 -- LE FORMULAIRE ET LES SUPER-COMBOS DEDIES A LA ZONE DE TRAVAIL

Demande du createur (cadrage, donc on cadre) :
"comment ameliorer le process pour les fichiers tmp-optimus (old/new, cobayes) ?
Je ne vois pas ce que tu fais. Si on creait des combos entierement dedies aux
fichiers tmp de l operateur (invisible pour le cameleon) ou du cameleon (qui a
deja ses propres outils). J imagine l operateur comme un user : il remplirait un
formulaire ; le super-combo fournit les cases a remplir ; l operateur les
remplit ; le combo transforme les fichiers a sa place, verifie en dry/wet avant
de modifier, et fournit le rapport. On conserve le concept old & new pour mieux
cerner les modifications."

## 1. LA MESURE D ABORD : LE FORMULAIRE EXISTE DEJA, C EST LE MOULE

Le createur reinvente un mecanisme deja livre. Le `moule` (porte par
poser-template-pilote.py et par la porte des templates) EST le formulaire
demande : un moule DECLARE ses jetons, l agent les REMPLIT, et un controle
REFUSE tout jeton recu qui ne correspond a aucun jeton du moule ("chaque jeton
RECU correspond a un jeton du moule"). C est exactement la posture "user qui
remplit un formulaire, et le systeme verifie avant d appliquer".

Trois briques deja en place, mesurees :
- le MOULE (formulaire type, a jetons, avec refus du jeton inconnu) :
  poser-template-pilote.py ;
- la CHAINE de raisonnement.formalisation, pense-bete -> spec -> todolist
  (PB-/SP-/TD-), qui est un formulaire de PENSEE deja cable :
  preparation/chaine-doctrine-de-la-chaine.md, decision ecrite en
  spec-chaine-pense-bete.md section 13 ;
- la PORTE de zone, qui nomme, classe et purge les fichiers de travail d une
  mission : super-combos/combos/outils/fichiers-travail.py (+ son jumeau cameleon
  dans data/outils/fichiers-travail-cameleon/).

## 2. CE QUI EST GENUINEMENT NOUVEAU

Le createur ne reinvente pas le formulaire : il demande la CHOREGRAPHIE. Trois
briques manquent pour que "l operateur remplit, le combo applique" devienne un
geste d un seul appel :
1. un SUPER-COMBO DEDIE A LA ZONE, dont le deroulement EST le formulaire : il
   presente les cases (le moule), recoit les reponses, joue le dry (verifie
   sans ecrire), puis le wet (ecrit par la porte ecrire/editer), puis rend le
   rapport ;
2. le FIL DU TEMPS dry/wet explicite, pour que la verification dry AVANT
   l ecriture soit un etat nomme du combo, pas une promesse ;
3. un RAPPORT de changements, produit par le combo et non par l agent.

## 3. LA TENSION A TRANCHER (old & new contre .bak)

Le createur veut conserver old & new "pour mieux cerner les modifications". Mais
la porte ecrire a deja tranche l inverse : editer accepte des contenus
bit-exact (--ancien-base64 / --nouveau-base64), et le concept old/new par
FICHIERS est devenu inutile -- la porte cree un .bak date, et le.bit-exact evite
la copie de travail. Le formulaire doit donc se brancher sur ecrire/editer
(bit-exact) plutot que sur des fichiers old/new : sinon on reintroduit la copie
de travail que la porte a supprimee. Ce n est pas un desaccord de gout, c est
une decision deja prise qu on ne peut pas re-ouvrir par le bas.

## 4. VERDICT DE CADRAGE

La vision est realisable et les 3/4 des briques existent (moule = formulaire,
chaine PB/SP/TD = formulaire de pensee, porte de zone = gestion des fichiers).
Le travail REEL se concentre sur la CHOREGRAPHIE (le combo qui enchaine
moule -> dry -> wet -> rapport), plus une decision a trancher (old&new contre
bit-exact, deja tranchee cote porte). Ce cadrage ne construit rien : il cadre
ce qui reste, pour que la construction (mission dediee) parte du bon endroit.
