---
identite:
  type: journal
  appartient_a: optimus-prime
  commun: false
---

# MO-581 -- LE REMEDE EST DEJA LIVRE : EO-559 EST UN DOUBLON DE MO-550

Mission REPARATION (item EO-559, verse du brin en lot le 2026-10-04).
Aucun fichier de production modifie : il n y avait rien a reparer.

## 1. LE CONSTAT, MESURE D AVANT

L enonce demande de faire consommer aux deux gardes le battement MEDIAN
(`battement.py`, lecon L-076) au lieu de la cadence declaree.

Avant de reparation : `recul_insuffisant` ouvrait la fenetre sur
`age < INTERVALLE_DECLARE_SECONDES`. Mesure rejouee sur routeur-maintenance
(cadence declaree 30 s, serie publiee `dernieres_passes` du 2026-10-04).

Le REMEDE EST DEJA IMPLEMENTE :

- `recul_insuffisant` accepte un quatrieme argument
  `battement_mesure_secondes` et ouvre sur le PLUS GRAND des deux ;
- `battement_de_passes` lit la mediane par le moteur partage
  `battement.py` sur la serie que la routine publie deja ;
- les DEUX gardes (`verifier-historique-non-redondant.py` ligne 559,
  `verifier-observations-non-redondantes.py` ligne 386) CONSOMMENT la
  mesure, sans la recalculer.

## 2. LA PREUVE, REJOUEE SUR LE SERVICE REEL

Battement median mesure : **61,0 s** sur les 5 dernieres passes publiees.

| age | ancien (fenetre 30 s) | corrige (fenetre 61 s) |
|---|---|---|
| 29 s | epargne | epargne |
| 30 s | **accuse** | epargne |
| 31 s | **accuse** | epargne |
| 45 s | **accuse** | epargne |
| 60 s | **accuse** | epargne |
| 61 s | accuse | accuse |

La bande de **31 s de faux positif** decrite par l enonce est SUPPRIMEE :
l ancien garde accusait un service sain de 30 a 60 s, le garde corrige
n accuse qu au-dela du battement mesure.

Le motif nomme la fenetre accordee :
`recul-insuffisant : etat vieux de 45 s pour un battement MESURE de 61.0 s`.

## 3. LE FAIL-CLOS EST INTACT (exigence de l enonce)

- cadence `None` ou `0` -> AUCUNE epargne ;
- age `None` -> AUCUNE epargne ;
- battement non mesurable -> repli sur la cadence declaree ;
- battement aberrant (`0`, `-5`) -> ECARTE, la cadence reste le plancher ;
- une passe absorbee accuse toujours.

## 4. QUI A LIVRE, ET QUAND

`matrice/data/sessions.json`, session **S-476** du **2026-10-02 21:32:58**,
source **MO-550**, theme REPARATION : la fenetre d absorption vaut le
battement MESURE. Ses preuves sont les memes que celles rejouees ici
(mediane 61 s, 45 s epargne, 70 s referme, maillon 70 verte).

## 5. TROIS PREUVES DE MA MAIN ETAIENT FAUSSES

J ecrisais `battement=0` et `battement=-5` comme des cas qui NE doivent pas
epargner. Le moteur les ecarte et applique le plancher de 30 s : a 10 s
d age l epargne est donc correcte. C etaient MES attentes qui etaient
fausses, pas le moteur. Le maillon 70 teste le cas aberrant `5`
(inferieur a la cadence), pas `0` ni `-5` : il couvre la discrimination
utile.

## 6. CE QUE LA MISSION NE FAIT PAS

Elle ne corrige rien, et c est le bon verdict : le travail est fait. Le
defaut REEL qui a produit ce doublon est ailleurs : une demande identique
a ete deposee DEUX FOIS dans la memoire de naissance. C est precisement
l objet de EO-564 (depose le 2026-10-03), qui devient la mission MO-585 --
le doublon se reproduira tant que ce garde n existe pas.

## 7. MOYEN DE PREUVE

`battement_de_passes` sur le service reel ; `recul_insuffisant` rejoue sur
11 ages ; maillon 70 de la non-regression ; session S-476.
