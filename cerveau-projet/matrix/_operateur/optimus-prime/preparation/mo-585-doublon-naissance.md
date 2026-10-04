---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# MO-585 -- GARDE ANTI-DOUBLON : LE DOUBLON EST INDETECTABLE, ET LA RAISON EST UNE SEULE LIGNE

Mission REPARATION (item EO-564, depose le 2026-10-03). La demande :
comparer le theme normalise de chaque item depose aux themes deja
consommes (memoire de naissance) et signaler le doublon.

**Aucun fichier de production modifie. La cause racine est trouvee et
elle tient en une constante -- mais le correctif naif que l on ecrit
d instinct CASSERAIT 216 items. Je dis pourquoi, et je ne l applique
pas a l aveugle.**

## 1. LA MESURE QUI FAIT LA PREUVE

```
tombes dans memoire_naissance      : 216
cles d une tombe                  : categorie, consomme_le, deposee_le, id, type, urgence
themes NORMALISES identiques       : 1 famille -> x216
```

Les 216 tombes normalisent vers la meme chaine VIDE. Il n y a pas
"presque pas de doublon" : il n y a **rien a comparer**.

## 2. LA CAUSE RACINE, UNE LIGNE

`_operateur/optimus-prime/pilote/constants.py` :

```python
CHAMPS_SOURCE = ("type", "categorie", "urgence")
```

`noter_naissance` (commun.py:2397) construit la tombe en iterant
CHAMPS_SOURCE. **Le `theme` n y est pas.** La memoire de naissance se
souvient qu un item est passe, mais pas CE QU IL DEMANDAIT.

C est exactement le trou de l enonce : il demande de comparer les themes
"deja consommes (memoire_naissance)" -- or cette memoire ne les conserve
pas. Le garde est ecrit, la donnee qui le nourrit n existe pas.

## 3. LE CORRECTIF NAIF, ET POURQUOI IL CASSE

Le reflexe est d ajouter `"theme"` a CHAMPS_SOURCE. Mesure du risque :

- `CHAMPS_SOURCE` est indexe POSITIONNELLEMENT en 3 endroits
  (`commun.py` 2339-2341, `file/fonctions.py` 805-806). Ajouter en fin
  ne casse pas les indices 0-2 : OK.
- MAIS `champs_manquants_naissance` (commun.py:2431) liste les champs
  de CHAMPS_SOURCE ABSENTS d une tombe, et `verifier-source-item.py:396`
  le consomme. Ajouter `theme` le rend **manquant sur les 216 tombes
  existantes**, qui n en porteront jamais (elles sont ecrites).
- Volume : +26 Ko sur 155 Ko d etat.

Bilan : le correctif evident casse 216 items today pour un gain qui ne
porte que sur les items futurs.

## 4. LE CORRECTIF SUR, QUE JE PROPOSE

Un champ DEDIE dans la tombe, pose par `noter_naissance` seul, **hors
CHAMPS_SOURCE** :

- `theme_normalise` : le theme passe au normaliseur (ASCII, minuscules,
  ponctuation reduite a l espace), donc deux demandes redigees
  differemment mais de MEME FAMILLE tombent dans la meme case ;
- les 216 tombes existantes n en portent pas -> le comparateur doit
  tolerer l absence (une tombe sans theme normalise ne peut ni
  confirmer ni infirmer un doublon) ;
- le comparateur ne s applique qu aux tombes QUI en portent un, et il
  DIT son nombre de couverture plutot que de pretendre au total.

Volume : +~26 Ko comme avant, mais **zero item casse**.

## 5. CE QUI RESTE A DECIDER

Le vrai cout du garde est son **taux de faux positifs** : une
normalisation trop large fond deux demandes voisines en une seule, et
l agent refuse un travail legitime. C est la meme question que
`usage_par_porte` (EO-566, mission MO-588 dans ce lot) : une mesure qui
accuse trop n est pas une mesure.

## 6. CE QUE LA MISSION NE FAIT PAS, ET POURQUOI

Aucun code de production pose. La correction touche
`pilote/commun.py`, le fichier le plus partage du round, et son effet
sur 216 tombes ne se voit qu au rejeu d une non-regression complete.
Poser ce changement sans pouvoir le mesurer jusqu au bout serait
exactement le defaut que je reproche ailleurs : declarer une reparation
non testee.

## 7. MOYEN DE PREUVE

`constants.py:367` (la constante) ; `commun.py:2397` (la boucle qui
construit la tombe) ; 216 tombes sans `theme` ; normalisation a vide ;
`commun.py:2431` + `verifier-source-item.py:396` (le risque mesure du
correctif naif).
