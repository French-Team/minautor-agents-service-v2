---
identite:
  type: journal
  appartient_a: optimus-prime
  commun: false
---

# BILAN MO-575 -- ONZE BRIQUES DECLAREES SERVIES, ONZE NOMS QUE LE LANCEUR REFUSAIT

> L'enonce annoncait trois BDD. La mesure en a trouve onze : meme cause, un cran
> plus bas. Le remede a donc ete elargi -- au DOMICILE, pas a la profondeur.

## LE FAIT MESURE, AVANT

Le registre des outils dit `servi_a_l_injection` pour 135 briques. Le lanceur en
joignait 144 noms. Le croisement des deux listes n'existait nulle part, donc
l'angle mort ne se voyait pas :

| brique declaree servie | lanceur |
|---|---|
| `bdd-frictions` | `REFUS : nom inconnu` |
| `bdd-lecons-matrice` | `REFUS : nom inconnu` |
| `bdd-modifs` | `REFUS : nom inconnu` |
| `c-001-lecons` ... `c-008-cartes` | (meme sort, mesure sur le registre) |

**Cause racine** : `matrice/data/commun/resolution_outils.py` collecte quatre
familles. La famille `operateur` borne sa profondeur a 2 crans, et la famille
`script` ne glob que les `.py` du dossier LUI-MEME. Les briques du parc des combos
sont des **DOSSIERS** un cran plus bas : `super-combos/combos/<nom>/main.py` et
`super-combos/combos/outils/<nom>/main.py`. Ni l une ni l autre ne les voyait. Le
registre, lui, les declarait servies a l'injection -- donc l'agent pouvait se voir
proposer un outil que le flux ne savait pas jouer.

## LA REPARATION, A LA SOURCE

Une famille **declaree**, pas une profondeur elargie :

- `DOMICILE_COMBOS = ("super-combos", "combos")`
- `DOMICILE_OUTILS_TRANSVERSES = ("super-combos", "combos", "outils")`
- `MOTIFS_COMBO = ("*/main.py", "outils/*/main.py")`

Un dossier n'est une brique que s'il porte un `main.py` -- le meme contrat que les
quatre autres familles --, la zone jetable est ecartee comme partout ailleurs, et
la profondeur de la famille `operateur` n'a pas bouge d'un cran (mesure : toujours
10 briques).

**Le maillon 83** est ne avec la reparation : une brique DECLAREE servie a
l'injection et INTRouvable au lanceur est accusee, avec sa porte. Il joue d'abord
sa decision pure sur cinq cobayes, puis la donnee reelle. Il lit `resolution_outils`
par IMPORT -- jamais recopie -- et sans ecrire de bytecode.

## LA PREUVE

| | avant | apres |
|---|---|---|
| briques servies introuvables | 11 | **0** |
| noms joignables par le lanceur | 144 | 152 |
| profondeur famille `operateur` | 10 | 10 |

Contre-temoins joues, tous tenus :

- un dossier-SANS-`main.py` : non resolu
- un cobaye pose dans la zone jetable avec son `main.py` : non resolu
- le cache `__pycache__` : non resolu
- les 74 scripts a plat du dossier des outils : toujours resolus

Nominalement joue : `bdd-frictions stats` repond (102 frictions au registre).

## DEUX CORRECTIONS QUE LA MISSION S'EST INFLIGEE

1. **Le contre-temoin a mordu sur la source.** `briques_combos` attendait un
   `Path` sans le dire : une chaine chemins levait `AttributeError`. Le parametre
   est desormais converti. Un contre-temoin qui meurt sur une betise d'API n'a rien
   prouve sur la panne -- il l'a d'abord laissee passer.
2. **Le maillon accusait 80 briques sur 135.** Le registre nomme une brique-scripts
   par son nom de FICHIER (`x.py`), le lanceur rend le nom de la brique (`x`).
   Comparer les formes brutes produit un maillon qu on coupe. La forme comparable
   est desormais normalisee, et le contre-temoin couvre les DEUX ecritures.

Ces deux corrections sont celles de la premiere famille (3 BDD). Elles sont
arrivees parce que la premiere reparation a ete prouvee par des contre-temoins et
non par un chiffre de doc.

## CE QUE LA MISSION LAISSE OUVERT

- Le maillon 83 couvre le sens **declarees et introuvables**. Le sens oppose
  (briques du parc absentes du registre) a son propre controle ; les deux classes
  restent distinctes et ne doivent pas etre confondues dans un compte unique.
- Les trois BDD et les huit combos n'ont pas de `DESCRIPTION.md` a cote de leur
  `main.py` : le lanceur le signale a chaque appel (`[SANS CARTE]`). Ce n'est pas
  un blocage, mais une declaration de carte manque sur onze briques servies.

## NON-REGRESSION

Un seul KO, **anterieur a la mission et mesure avant de commencer** : le controle
d'attribution accuse six fichiers d'une ecriture fantome du 2026-10-03. Elle est
instruits par EO-577, qui attend son tour en tete du brin. Aucun KO ajoute, aucun
KO resolu par accident.
