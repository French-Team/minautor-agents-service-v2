---
identite:
  type: journal
  appartient_a: optimus-prime
  commun: false
---

# MO-580 -- AUDIT DES BLOCANTS : les 10 items bloquants du vrac sont-ils encore vivants ?

Date : 2026-10-04. Aucun fichier de production modifie. Ce dossier est la MESURE.

## 1. PERIMETRE MESURE

Le vrac de l'entonnoir contient 15 items, dont **10 `bloquante`**. Le brin
(21 items, deja versables en lot) n'en contient **aucun** : ces 10 n'ont jamais
ete tisses. Les prioriser est donc la seule tache qui bloquait le round.

## 2. MESURE PAR ITEM

| Item | Cible | Etat reel | Verdict |
|---|---|---|---|
| EO-578 | `bdd-conservation/archiver/entry.py` compile | compile (code 0) | **FAUX POSITIF** |
| EO-444 | traceback critique dans l'espion | 0 critique, run dynamique 0 | **RESORBE** |
| EO-495 | U+4E0D | absent | **RESORBE** |
| EO-496 | U+5BF9 | absent | **RESORBE** |
| EO-497 | U+5E38 | absent | **RESORBE** |
| EO-498 | U+7684 | absent | **RESORBE** |
| EO-499 | U+79F0 | absent | **RESORBE** |
| EO-500 | U+89C1 | absent | **RESORBE** |
| EO-540 | U+6162 | absent | **RESORBE** |
| EO-541 | U+FF0C | absent | **RESORBE** |

Mesure executable : sur les **674 .py** du perimetre de la veille
(`commun.lister_fichiers_python()`), le nombre de fichiers comportant un
octet >= 128 est **ZERO**. Aucun des 8 caracteres n'existe plus.

## 3. LA CAUSE RACINE DE EO-578 (faux positif instructif)

`py_compile` isole dit code 0. `commun.lancer_py_compile()` -- le CHEMIN DU
PRODUCTEUR -- dit aussi **CODE=0** sur les 674 fichiers. La veille n'a donc
rien accuse a tort sur l'etat du code : elle a lu le fichier **pendant son
ecriture**.

Horodatage mesure :
- item EO-578 depose a **11:30:25**
- `archiver/entry.py` ecrit a **11:30:28**

Le fichier a ete fini 3 secondes APRES le depot de l'alerte. Son re-test
(`PAUSE_REPRISE_SECONDES = 2`) n'a pas rattrape la fenetre : 2 secondes ne
couvrent pas une ecle d'agent de plusieurs secondes.

**Ce qu'il faut corriger, a la SOURCE** : le garde confirme doit mesurer
l'AGE DU FICHIER au moment de la detection. Un fichier modifie il y a moins de
N secondes ne peut pas etre accuse de defaut durable -- c'est exactement le
meme arbitrage que la fenetre d'absorption (EO-559) et que les zones jetables
(EO-175, deja traitees).

## 4. CE QUE LA MESURE NE DIT PAS

Elle ne dit pas que la veille a tort : elle dit que la veille ne peut pas
distinguer un fichier casse d'un fichier en cours d'ecriture. L'angle mort
est la fenetre de course, pas la detection.

## 5. MOYEN DE PREUVE

`lancer_py_compile()` code 0 ; `lister_fichiers_python()` 674 fichiers, 0
octet >= 128 ; rapport-tracebacks du 2026-10-04 17:56 : `critique` absent,
`run_signaux=0`.
