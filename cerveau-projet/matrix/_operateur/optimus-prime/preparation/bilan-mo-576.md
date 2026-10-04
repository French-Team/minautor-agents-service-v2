---
identite:
  type: journal
  appartient_a: optimus-prime
  commun: false
---

# BILAN MO-576 -- SIX FICHIERS ACCUSES SANS NOTE : L ECRITURE FANTOME DU 2026-10-03

> Ce texte est la CONSIGNE que la machine ne gardera pas. Il est ecrit AVANT la
> repose du registre, parce que la repose remplace les 998 empreintes et que rien
> dans la machine ne les retiendra apres. Decision createur : consigner, puis
> reposer.

## CE QUI EST ACCUSE

Le controle d attribution refuse six fichiers de la zone : leur contenu sur
disque ne porte plus l empreinte que le registre a gelee, et aucune note
posterieure a la pose ne l atteste.

| fichier | registre (pose du 2026-10-02 22:17:14) | sur disque | derniere note |
|---|---|---|---|
| `theme-auto-audit-nemesis.json` | `96f626a10c3f` | `b1bb3e2264e7` | AUCUNE |
| `theme-auto-evolution.json` | `2b6996cc4f43` | `a989d60628e3` | 2026-09-11 14:05 sans empreinte |
| `theme-contre-analyse.json` | `26146c4cb227` | `e4a560ca8024` | 2026-09-11 14:05 sans empreinte |
| `theme-reprise-mission.json` | `0b5887baba09` | `60086c4d4cfb` | 2026-09-13 09:11 sans empreinte |
| `checklist/listes.py` | `c1ab929c75d2` | `d4c6633076b1` | 2026-09-21 08:37 sans empreinte |
| `combos/outils/garde-segment.py` | `39ecf12e6981` | `c31f80d947da` | 2026-10-02 20:27 **avec** empreinte |

Le registre porte 998 empreintes. Les six sont les seules en desaccord.

## LA FENETRE, ET ELLE EST ETROITE

`garde-segment.py` est la preuve la plus nette, parce que sa derniere note
**porte** une empreinte. Cette note, du 2026-10-02 a 20:27, annonce exactement
`39ecf12e6981` -- l empreinte que le registre retrouvera encore a 22:17, soit
**1 h 50 plus tard**. Le contenu `c31f80d947da` n est annonce par personne.

Toute l ecriture fantome est donc comprise entre le **2026-10-02 22:17:14** (la
pose) et le **2026-10-03 10:55:13** (le commit `f13f0480`, qui fige le resultat).

Sur cette fenetre :

- **aucune note** au domicile `bdd-modifications` pour aucun des six ;
- **aucun evenement** au journal `suivi-optimus.jsonl` qui cite l un d entre eux
  (balayage sur tous les champs, mission, action, fichiers, detail, corrections).

## CE QUI N EST PAS LA CAUSE

Trois hypotheses ont ete mesurees et ecartees :

1. **L incident du 2026-10-03.** Non. `git status` est PROPRE sur les six ET sur le
   registre : le commit lui-meme est incoherent. L ecart existe dans l historique,
   avant la restauration de 21:40.
2. **Une version de travail jamais commitee.** C est vrai pour quatre des six
   (`theme-*` : dernier commit le 2026-09-16), mais pas pour `garde-segment.py`
   (commite le 2026-10-03 10:55, donc posterieur a la pose).
3. **Des notes perimees.** Non : cinq des six n ont pas de note posterieure a la
   pose, et la sixieme (`garde-segment.py`) n a pas de note du tout apres le
   2026-10-02 20:27.

Une seule cause reste, et elle est muette : une ecriture reelle, par un moyen qui
n est ni la porte ni le journal.

## LA PERTE EST IRRECOVERABLE

Aucun `.bak` du parc ne porte l empreinte attendue, pour aucun des six. Le
registre est donc le **seul** temoin de la version perdue -- et un sha256 ne se
dechiffre pas : il prouve qu une version a existe, pas ce qu elle contenait.
Ce qui est perdu est perdu ; ce qui reste, c est la preuve qu il y avait quelque
chose.

## LA REPOSE, ET CE QU ELLE EFFACE

`controle-attribution.py` ne sait que `poser` et `verifier`. Il n existe aucune
porte qui declare une ecriture non attribuee. La seule facon de lever
l accusation est donc de **reposer la reference** : le registre reprend le
contenu du disque comme etat de depart, et la date de pose devient celle de la
repose.

Ce que la repose **efface** : les 998 empreintes du 2026-10-02 22:17, dont les
six qui portaient la trace de la perte.

Ce qu elle **conserve**, parce que la decision du createur les a fait consigner
d ABORD :

- ce bilan ;
- une copie datee de l ancien registre, deposee a cote de lui.

Apres la repose, l accusation est levee parce que le contenu actuel EST la
reference -- pas parce que l ecriture fantome a ete attribuee. **Elle ne l a
jamais ete et n sera pas.** Personne ne peut dire qui a ecrit ces six fichiers.
Ce controle avait raison de crier ; on a choisi de cesser de l ecouter, en
sachant pourquoi.


## CE QUE LA REPOSE A REVELE, ET QU IL A FALLU REPARER

Le controle d attribution ne lisait qu UNE vue par porte (`CHEMIN_VUE` ou
`NOM_VUE`). La porte des parties maitresses en pose **CINQ** : elle n etait pas
dans la liste des domiciles lus, donc quatre de ses vues etaient accusees comme
des sources -- et l accusation revenait a chaque rafraichissement. La pose les a
fait basculer de `source neuve` a `changee` : meme dossier, verdict plus net.

Une vue ne peut pas s attester elle-meme : elle se RECALCULE a chaque passe, donc
une note d avant la passe est perimee des la passe suivante, et une note d apres
n peut pas exister. Le remede n est donc pas une note, c est une DECLARATION :

- la porte expose `VUES_PRODUITES`, **derivee** de `DOSSIER_VUES`, `NOM_INDEX` et
  `PARTIES` -- jamais une liste recopiee (L-029) ;
- le controle lit cette declaration, au meme titre que `PRODUCTIONS` pour les
  routines, et nomme la porte dans son exclusion.

Mesure : `hors jugement : vue recalculee par sa propre porte
(suivi-parties-maitresses) -- 5 fichier(s)`. Les cinq sont nommees, et la porte
qui les ecrit est celle que le controle cite. Auto-test du controle : 37/37.

C est le meme vice que MO-575 -- une famille declaree a un endroit, la realite a un
autre -- et il etait invisible tant que la pose ne les rendait pas visibles.

## L EXECUTION, APRES LA CONSIGNE

Dans l ordre decide : la consigne ci-dessus a ete ecrite, puis l ancien
registre archive, puis la reference reposee.

```
attribution-registre.json.bak.20261002_221714   998 empreintes, date_pose 2026-10-02 22:17:14
  (contenu identique au bit pres a l origine, a UN saut de ligne final pres :
   la porte ecrire force les LF et l original n en avait pas)

attribution-registre.json                     1026 empreintes, date_pose 2026-10-04 08:49:22
  verification : 0 changee, 0 source neuve, 0 disparue
```

Les 28 empreintes supplementaires sont les fichiers nes depuis la pose : les
bilans, les vues de suivi, les portes reconstruites. Rien n a ete ajoute a la
main pour faire disparaitre les six : la reference est celle du DISQUE, mesuree
par la porte, pas une liste choisie.

Le garde signale au passage **599 notes sans empreinte** : elles ne peuvent plus
attester aucun changement. C est une dette de fond, mesuree et nommee par la
porte, distincte de l accusation levee.

**Non-regression : VERTE.** Un seul KO la rendait KO depuis des mois ; il est
solde. Aucun autre maillon n a bouge.
