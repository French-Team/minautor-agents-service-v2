---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# ARBITRAGE MO-529 / EO-487 -- LE LANCEUR PUNIT L HONNETETE ET RECOMPENSE L ANONYMAT

## 1. LA DEMANDE, ET SON STATUT

Item EO-487 (depose le 2026-09-29 21:31, type `reparation`) : le lanceur
applique deux regimes OPPOSES au meme acte. Un appel SANS identite declaree a
une porte privee de l AUTRE flux est seulement NOMME et s execute ; le MEME
appel avec `--appelant operateur` est REFUSE (code 2). L item dit aussi que
cette asymetrie est VOLONTAIRE, notee dans `lancer.py`, et qu elle tient
18 commandes documentees dont 9 dans proto-12 -- et qu elle a ete MESUREE et
DEPOSEE par MO-496, pas corrigee en douce. MO-496 a retire la seule
prescription qui en dependait (la roue de la vigie dans ORDRE 4.6) ; rien ne
ferme la porte pour les 17 autres.

**L item demande une decision du createur (comportement CORE). Je la ne
prends pas : la regle immuable `evolution-decidee` et la charte
d auto-novation en font une decision du createur, et l auto-test du lanceur
(x5 epreuves, dont 3 COBAYES) est un contrat ecrit que je ne casse pas seul.
Ce document est l etat mesure, et les deux options, avec ce qu elles
cassent.**

## 2. LA MESURE, SUR LES CARTES REELLES (cobaye 2/2, code 0)

Le juge `juger_carte(carte, appelant)` est PUR : il est rejoue sur les cartes
lues SUR LE DISQUE, sans declencher aucune porte (une porte qui s execute est
un effet de bord, pas une preuve).

| Porte reelle | commun / flux | sans identite | operateur (flux 2) | cameleon (flux 1) |
|---|---|---|---|---|
| `matrice/routines/vigie-portes` | false / 1 | **s execute** (nomme) | **REFUSE** | s execute |
| `matrice/data/outils/dialoguer` | false / 2 | **s execute** (nomme) | s execute | **REFUSE** |
| `matrice/data/outils/rechercher` | true / (aucun) | s execute, en SILENCE | s execute | s execute |

Le contre-temoin est vert : une porte COMMUNE reste ouverte sans identite, en
silence. Le trou ne concerne donc que les portes privees qui portent la cle
`flux` -- soit, dans l etat mesure du depot, **deux portes** :
`matrice/routines/vigie-portes` et `matrice/data/outils/dialoguer`.

Le code qui produit l asymetrie est en six lignes (`lancer.py`,
`juger_carte`, lignes 163-174) :

- appelant vide + porte privee qui porte `flux` -> on rend un **signalement**
  (le passage est autorise mais NOMME), jamais un refus ;
- appelant declare + `flux` different de celui de la carte -> on rend un
  **refus** (code 2).

Autrement dit : le controle compare deux fois le meme chose -- le flux -- et
ne tranche qu UNE des deux fois.

## 3. CE QUE CELA COUTE, ET CE QUE CELA PROTEGE

**Ce que la porte ferme aujourd hui** : un appelant declare ne peut pas
ecrire chez l autre flux. C est une frontiere d ECriture entre deux agents
qui partagent le meme disque (matrice/). Elle est inscrite dans la porte
elle-meme : `lancer.py` refuse le flux etranger DECLARE et dit qu il ne
pretend pas prouver qui est l appelant reel (ligne 42).

**Ce que l anonymat laisse passer** : le meme appel, sans `--appelant`,
passe et joue. Le controle nomme le passage ("porte privee du flux 1 appelee
SANS identite declaree -- declarez : --appelant <identite>"), donc le passage
est visible dans la sortie de la porte -- mais il n est pas refuse.

Autrement dit : **la frontiere est une consigne, pas une barriere, des que
l appelant ne se declare pas.**

## 4. LES DEUX OPTIONS, ET LEURS CONTRES

### Option A -- le croisement refuse l anonymat comme il refuse l identite etrangere

Une porte privee portant `flux`, appelee sans identite, est REFUSEE (code 2),
comme elle l est deja pour un identite declaree du mauvais flux. Le message
est le meme des deux fois, avec la variante "sans identite declaree".

- ce que ca regle : le trou. Une porte d un flux ne s joue plus depuis l autre
  flux, quel que soit le degre de sincerite de l appel.
- ce que ca casse, mesure : **les 18 commandes documentees** dont 9 dans
  proto-12 qui s executent aujourd hui SANS `--appelant` vers une porte privee
  de flux. Il faut les NOMMER une a une (elles existent : ce sont les 18 que
  l auto-test et proto-12 documentent) et leur ajouter l option.
- ce que ca ne change pas : une porte privee SANS cle `flux` (pilote,
  bdd-raisonnement) reste ouverte a tout le monde, comme aujourd hui -- c est
  la regle actuelle et elle est dite.
-cout : un inventaire de 18 commandes a migrer, et une auto-test a etendre
  (une epreuve de plus : "privee du flux 1 appelee sans identite" doit
  maintenant etre un COBAYE).

### Option B -- le lanceur cesse d interdire les portes par flux

La frontiere ne se joue plus sur le `flux` de la carte mais ailleurs (le
renvoi de l item le rappelle : une porte peut etre LISIBLE sans etre
JOUABLE, le croisement se jugeant sur l ACTE). Concretement : `commun: false`
reste une porte privee, mais `flux` cesse d etre un critere d ouverture ;
l identite declaree sert a NOMMER le passage, pas a le fermer.

- ce que ca regle : rien du trou (l anonymat reste ouvert), mais la regle
  cesse d etre ambigue : elle dit enfin ce qu elle fait.
- ce que ca casse : la frontiere d ecriture entre les deux flux, qui n existe
  que la. C est le createur qui l a demandee (perimetres R-005 / CV-012 :
  la matrice est lue par les deux flux, ecrite par le flux 2).
- cout : une protection de moins, dite noir sur blanc.

### Option C -- ce que je ne recommande pas, mais qui est dit

Refuser l anonymat SANS toucher a l identite declaree (donc punir encore plus
l honnetete). Je l ecris pour que le choix soit complet : c est la seule
option qui aggrave l asymetrie au lieu de la resoudre.

## 5. CE QUE CETTE MISSION LIVRE, ET CE QU ELLE NE LIVRE PAS

LIVRE : la mesure sur cartes reelles (cobaye 2/2, code 0), le code fautif
localise et nomme (`lancer.py`, `juger_carte`, six lignes), l etat reel du
depot (deux portes concernees), le cout mesure de chaque option, et la liste
des 18 commandes documentees que l option A devrait migrer.

NON LIVRE : le comportement. Il n est pas change, il est mesure et arbitre.
Tant que la decision n est pas prise, le lanceur se comporte comme le
documente (`lancer.py`, tete de fichier) et comme son auto-test.

**Segment RS-055** : une frontiere d ecriture qui separe deux agents est une
barriere ; une frontiere qui ne punit que la declaration est une consigne.
Les deux sont des choix, mais les nommer differemment evite de croire la
matrice cloisonnee quand elle ne l est pas.
