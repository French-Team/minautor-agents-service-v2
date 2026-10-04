---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# DECISION -- l ARRIERE DU BRIN (question ouverte depuis MO-460)

Date : 2026-09-29. Tranchee par la MESURE, pas par gout.
Demandee au createur le 2026-09-28, la question etait : faut-il vider
l arriere du brin (servir les tetes une par une) ou regrouper les dormeurs
en un seul lot ?

## LA MESURE

1. LE BRIN FAIT 11 ITEMS. Le rouge `item-qui-dort` en nomme 2 dormeurs :
   EO-475 (depose depuis 2199 min) et EO-476 (depuis 2194 min).

2. LES DEUX DORMEURS SONT EN TETE. `position_brin` vaut 1 pour EO-475 et 2
   pour EO-476. Ce ne sont pas les derniers de la file : ce sont les
   premiers. Il n y a donc RIEN a vider derriere eux -- ils passent en tete
   des que la serie striche les libere.

3. ILS VIENNENT DE LA MEME MESURE. Deposes a 5 minutes d intervalle
   (2026-09-28 09:31 et 09:36), meme source (MO-498), meme zone, meme
   remede. Ce n est pas une coincidence de fond : c est UN ECART vu de deux
   fois.

4. LE LOT NE PEUT PAS LES CHOISIR. Le verbe que le remede nomme --
   `file verser --lot` -- verse LE BRIN ENTIER (mesure sur
   `commun.verser_tresse` : la fonction prend `etat["brin"]` en entier et
   n ouvre aucun filtre). Applique aujourd hui, il entrainerait 9 items
   NON dormeurs dans le lot, dont 4 auto-valides. L option B ne peut donc
   pas faire ce qu elle promet.

5. LE LOT NE DEBLOQUERIAIT RIEN. Les 2 items portent
   `auto_validation: non`, et les DEUX sont bloques par le meme axe :
   `perimetre`, motif "zone CRITIQUE nommee : parcours". Un lot n est pas
   une validation. Ces 2 items attendent le createur, pas un geste de file.

6. LA CHAINE A COULE. 7 missions ont ete servies depuis le depot de EO-475
   (MO-499 a MO-505). La tete n a donc JAMAIS bloque le flux : les
   dormeurs dorment parce qu ils n ont pas ete pris, pas parce qu ils
   etaient coinces.

## LA DECISION

**On ne vide pas l arriere, et on ne fait pas de lot. On sert les tetes,
une par une -- ce qui est deja la voie naturelle, puisqu elles SONT les
tetes.**

Autrement dit : l option A, mais pour une raison opposee a celle que
l on lui donnait. Il ne s agit pas de decomprimer une file : il n y a
rien a decomprimer. Il s agit de servir ce qui vient ensuite, dans
l ordre, et de laisser le createur valider ce qui doit l etre.

Concretement, pour les 2 dormeurs :

- EO-475 et EO-476 sont servis un par un, en tete, sans lot.
- Leur axe `perimetre` reste CONTRE : ils nomment une zone critique
  (`parcours/`), la validation reste au createur. Ce n est pas un
  defaut, c est la regle qui joue.
- Aucune selection par lot : le verbe existant ne sait pas selectionner, et
  un lot ne vaudrait pas validation.

## LE VRAI DEFERT, TROUVE AU PASSAGE

Le detecteur `item-qui-dort` ne dort plus : EO-420 (2026-09-25) l avait
corrige pour qu il scanne TOUT le brin. Mais sa LANGAGE n a pas suivi la
reparation. Il parle encore de "l ARRIERE", de "vider l arriere", alors
qu il mesure une file entiere dont il ne distingue plus la tete. Il
recommande donc un geste sur un endroit qui n existe plus -- et le seul
geste qu il nomme (`verser --lot`) ne peut pas non plus etre selective.

Autrement dit : le rouge ne tient pas parce qu il n a pas de remede. Il
tient parce qu il prescrit un remede que ses propres mains ne savent pas
executer. C est un ecart de TEXTE, a part de la decision ci-dessus :
depoter, il n est pas traite par cette decision.

## CE QUE LE ROUGE DIRAIT DESORS

`item-qui-dort` restera ROUGE tant que EO-475 et EO-476 ne seront pas
servies. C est le comportement CORRECT : il nomme un etat reel, non
resolu. Il ne peut plus etre accuse de ne pas savoir quoi faire --
desormais il dit ce qu il faut faire, et ce qu il faut faire est connu.

Le rouge s everera quand le createur validera EO-475 : la chaine
s arretera la, par construction (MO-175).

## OU EN EST CETTE PREDICTION (MO-513 / EO-490, 2026-10-01)

La section ci-dessus est une PREDICTION ecrite le 2026-09-29. Elle est
Faussee sur un point, et la mesure le dit.

Ce qui s est confirme : la regle elle-meme. Le brin se sert par la tete,
une par une, et le createur l a confirme par arbitrage le meme jour
(servir les dormeurs un par un). Le rouge nomme bien un etat reel.

Ce qui est faux : le declencheur annonce. Le texte dit que le rouge
s everera a la validation de EO-475. Or EO-475 n attendait pas une
validation : il a ete consomme et servi, et le rouge s est deplace
plutot qu ete leve. Au 2026-10-01, la mesure donne 8 dormeurs, le plus
vieux etant EO-485 au rang 9/43.

La CORRECTION du texte n est donc pas cosmetique : une decision qui
annonce un declencheur faux apprend au lecteur a ne plus croire ses
annonces. La regle dit < nommer un etat reel > ; nommer un declencheur
qui n a pas eu lieu, c est nommer un etat qui n existe pas.

CE QUE LA MESURE CORRIGE : le rouge ne s everera pas sur la validation
d UN dormeur, il s everera quand le dernier dormeur aura ete servi ou
solde. Son extinction est un COMPTE (0 dormeur), pas un evenement
(validation). C est la meme correction que celle du detecteur, portee
jusqu au texte de la decision.

ETAT AU MOMENT DE LA CORRECTION : la mesure du 2026-10-01 donne 7
dormeurs, le plus vieux EO-485 au rang 8/42 (EO-490 vient d etre servi
par la tete, ce qui a fait baisser le compte de 8 a 7). Ce nombre bougera
a chaque service : c est un etat vivant, donc le fichier le nomme comme
tel plutot que de le figer.
