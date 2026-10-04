---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# BILAN -- EO-489 : le remede du detecteur ne disait plus la ou il regarde

## LE FAIT

Le detecteur `item-qui-dort` (suivi-pilote.py) a ete CORRIGE par EO-420 le
2026-09-25 : il scanne desormais TOUT le brin, plus la seule tete. Son
LANGAGE, lui, n avait pas suivi la reparation. Le docstring et la sortie
parlaient encore de "l ARRIERE" et proposaient pour remede "vider l arriere
du brin ... ou file verser --lot pour grouper les dormeurs".

## POURQUOI C ETAIT COUTEUX

Ce n etait pas une faute de scan, mais une faute de PAROLE, et elle a
produit une question sans reponse. Mesures du 2026-09-29 :

1. Les 2 dormeurs accuses ce jour-la (EO-475, EO-476) portaient
   `position_brin` 1 et 2. Ils etaient les TETES. Le createur a donc pose
   la question -- "faut-il vider l arriere du brin, ou regrouper les
   dormeurs en un seul lot ?" -- sur un endroit qui n existait pas.

2. Le lot ne pouvait pas etre selectif : `commun.verser_tresse` verse
   `etat["brin"]` ENTIER, sans le moindre filtre. Applique, il aurait
   entrain 9 items NON dormeurs, dont 4 auto-valides.

3. Un lot n aurait debloque rien : les 2 items sont `auto_validation: non`,
   bloques par le meme axe `perimetre` (zone critique `parcours/`). Ils
   attendaient le createur, pas un geste de file.

Le cout reel : un remede qui nomme un lieu inexistant, ou un geste que la
porte ne sait pas faire, transmet une confiance qu il ne peut pas
honourer -- et il dispense son lecteur de chercher. Lecon L-224.

## LA REPARATION

Le detecteur accuse des ETATS et propose un geste dont l EXECUTABILITE a
ete mesuree :

- le docstring dit LA FILE ENTIERE, et retrace pourquoi le mot a change ;
- la sortie NOMME LE RANG du dormeur ("rang 1/12"), ce qui manquait
  exactement et qui avait permis d inventer un arriere ;
- le remede propose `file consommer` (servir par la tete), qui est le geste
  que la porte sait reellement faire -- et il se LIT differemment selon
  que le dormeur est la tete ("c est la tete, il part des la liberation de
  la serie stricte") ou non ("il part apres les N item(s) qui le
  precedent") ;
- le lot disparait du texte : il n est pas selectif, et un lot n est pas
  une validation.

## PREUVES

Cinq controles dans l auto-test de l outil (EO-489) :

- le remede DIT LE RANG (cobaye : dormeur en tete, "rang 1/2" + "c est
  la tete") ;
- un dormeur REELLEMENT en fond est dit comme tel (contre-temoin du cas
  masque : "rang 3/3", "apres les 2 item(s)") ;
- le remede ne prescrit PLUS le lot ("lot" et "arriere" absents) ;
- MALGRE ce texte change, la DETECTION reste la MEME : le constat porte
  toujours le nombre, l id et la date de depot -- c est le contre-temoin
  exige par l item, il distingue une reparation de TEXTE d une reparation
  de COMPORTEMENT ;
- les contre-temoins existants tiennent toujours (brin frais, brin vide,
  dormeur en arriere tete fraiche).

## TRACES ET ETAT

- auto-test de l outil : tous verts, 0 KO ;
- non-regression : 75 maillons, seul KO = `item-qui-dort` LUI-MEME, sur
  l etat REEL (2 dormeurs non servis) -- pas une regression : le
  diagnostic tient sur le brin reel (rang 1/12 verifie par lecture du
  JSON) ;
- sc-002 : friction 98 ajoutee ; sc-003 : auto-test vert ;
- segment de raisonnement depose : RS-029 ;
- zone jetable vide.

## MES FAUTES, DITES

1. En ajoutant le frontmatter de carte au document de decision, j ai
   REMPLACE le titre au lieu de l inserer. Le point de restauration
   (`.bak.20260930_070135`) a rendu le fichier intact, et j ai refait
   l operation correctement. Sans le point de restauration, le titre du
   document de decision aurait disparu.
2. Le premier jet du maillon EO-489 attendait "rang 1/2" alors que sa
   fixture placait le DORMEUR en second -- le test a echoue, et son
   echec a montre que je n avais pas verifie ma propre fixture. Corrige.
3. Mon depot de EO-489 a rendu le brin PERIME (le maillon 5 l a vu) :
   j ai refait le tissage. Effet de bord normal, mais il a fait rougir deux
   lignes de la suite que j avais cassees.

## CE QUI RESTE

`item-qui-dort` restera ROUGE tant que EO-475 et EO-476 ne seront pas
servies. C est le comportement correct : il nomme un etat reel. Ce qu il
ne peut PLUS faire, c est prescrire un remede inatteignable. Le rouge
s everera quand le createur validera EO-475 : la chaine s arretera la, par
construction (MO-175).
