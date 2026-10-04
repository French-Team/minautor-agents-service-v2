---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# MO-511 / EO-508 -- LES OUTBOX ONT-ELLES DES ROTATIONS POUR NE PAS DEPASSER LES 5 Mo ?

Question du createur, posee tel quel au brin :
"verifier si les outbox ont des rotations pour eviter de depasser les 5mo."

## 1. LA REPONSE EN UNE LIGNE

OUI. La rotation existe, elle est BORNEE a 5 Mo, elle est jouee a CHAQUE cloture
de mission, et elle mord. Mais la mesure dit un chose que la question ne
supposait pas : sur les boites du jour, ce ne sont pas les 5 Mo qui mordent en
premier -- ce sont les 200 messages. Le plafond de 5 Mo n est pas la barriere
active, il en est la DERNIERE ligne.

## 2. LA MESURE (sur disque, jamais de memoire)

Boites du Flux 2 (les seules bornees par le pilote) :

| boite | octets | % du seuil 5 Mo | messages | % de la borne 200 |
|---|---|---|---|---|
| `_operateur/maintenance/pilote/outbox.jsonl` | 3 053 078 | 58,2 % | 203 | 101,5 % |
| `_operateur/maintenance/matrice/inbox.jsonl` | 162 341 | 3,1 % | 207 | 103,5 % |

Les DEUX boites sont AU-DESSUS de la borne en messages et tres en dessous de
la borne en octets. Autrement dit : si la question du createur est "est-ce que
le 5 Mo va etre depasse", la reponse mesuree est non, et pas de peu.

Moyenne mesuree : 15 039 o par message dans l outbox du pilote. A 200 messages,
la boite pese 3 007 800 o, soit 57,4 % du plafond de 5 Mo. La borne en
messages CLOSE la boite trois octets sur deux avant que la taille n ait une
raison de s inveiller.

Meme calcul pour la matrice : 784 o par message, 200 messages = 156 800 o, soit
3,0 % du plafond. La boite la plus petite est encore plus etranglemente par le
nombre que par la taille.

## 3. LA MECANIQUE (lue dans le code, pas supposee)

- Seuil : `SEUIL_OCTETS_BOITES_INTERCOM = 5 * 1024 * 1024` (pilote/constants.py:292)
- Borne en messages : `MESSAGES_GARDES_BOITES_INTERCOM = 200` (ligne 293)
- Moteur : `data/commun/rotation_journal.py` -- le MOTEUR PARTAGE des journaux
  (M-076), jamais recopie : `from rotation_journal import tourner` (commun.py:154)
- Appel : `rotation_boites_intercom(mission)` (commun.py:2925), joue par
  `fin/fonctions.py:445`, donc A CHAQUE cloture
- Archives : `boite-archive-<AAAAMMJJ>.jsonl`, posees a cote de la boite

Les trois invariants du moteur sont la raison de ne pas reecrire un rotateur
maison : ARCHIVER D ABORD (l archive est ecrite et verifiee avant que la boite
soit reecrite), LE DEJA CONNU (une rotation qui ignore ce qu elle a deja
deplace se recree des jumeaux au passage suivant), UNE COURSE SE REFUSE (on
n ecrase jamais un message arrive pendant la rotation).

Et la chaine est complete jusqu au bout : les archives datees sont elles-memes
purgees sur preuve par `purger_archives_journaux` (commun.py:1911), qui ne
supprime que ce dont l engagement dans le depot est PROUVE. Une rotation qui
deplacerait 5 Mo sans fin serait donc un trou, mais il n existe pas.

## 4. PREUVES (jouees, pas annoncees)

Cobaye : `_operateur/optimus-prime/tmp-optimus/MO511-cobaye-rotation-outbox.py`
Il importe le moteur REEL et joue sur un CLONE, avec les constantes REELLES
lues dans le pilote (jamais recopiees dans le cobaye).

- **C3, cobaye qui MORD** : seuil force a 0 sur un clone de la vraie boite.
  3 053 078 o / 203 messages -> archive `boite-archive-20261001.jsonl` ecrite
  (832 78 o sur disque), boite ramenee a 3 010 654 o / 200 messages. Le moteur
  archive, la boite s allege. Rotation reellement jouee.
- **C4, contre-temoin qui EPARGNE** : une boite de 38 o / 2 messages, sous le
  seuil reel. Le moteur refuse, motif `38 octets <= seuil 5242880 : rien a
  faire`, fichier byte-pour-byte intact. Le moteur ne touche donc pas une boite
  saine : ce n est pas une porte qui ecrase pour ecrire.
- **C1/C2** : les deux seuils mesures sur les deux boites reelles (tableau
  ci-dessus).

Verdict du cobaye : `VERDICT GLOBAL : C1 C2 C3 C4 verts`.

## 5. LE POINT QUE LA QUESTION NE VOYAIT PAS

Trois boites du depot ne sont pas bornees du tout par ce seuil :

- `_operateur/optimus-prime/intercom/pilote/outbox.jsonl` (240 473 o, 42 lignes)
  et `.../matrice/inbox.jsonl` (2 547 o, 14 lignes) : ce sont les ANCIENNES
  boites du predecesseur. Le mesureur lui-memes le dit -- `suivi-pilote.py:96` :
  "la boite `_operateur/optimus-prime/intercom/pilote/` est une ANCIENNE boite
  (derniere injection le 2026-09-12)". Elles sont mesurees, jamais purgees.
- `matrice/intercom/pilote/outbox.jsonl` (634 518 o) et
  `matrice/intercom/matrice/inbox.jsonl` (373 506 o) : le Flux 1, la boite du
  cameleon. Elles relevent de la porte de conservation du flux 1
  (`purger-archive`), pas du pilote d Optimus.

Aucune n approche 5 Mo. Ce sont trois boites fines, et aucune ne grossira
pendant que le flux 2 tourne -- les boites du predecesseur ne recevront plus
rien, par construction.

## 6. CE QUE LA MESURE LAISSE OUVERT

Rien qui bloque, deux choses a savoir :

1. Le plafond de 5 Mo est un garde-fou, pas la barriere active. Si un jour la
   taille moyenne d un message passe a 25 Ko (elle est a 15 Ko aujourd hui, et
   la plus grosse ligne mesuree fait 44 822 o), la borne en messages
   commencerait a ne plus suffire et le 5 Mo mordrait enfin. Les deux bornes
   cohabitent donc, et c est bien.
2. La plus grosse ligne de l outbox est une injection a 44 822 o. Ce n est pas
   une   anomalie (une injection porte le contexte de la mission, donc elle
   pese), mais cela veut dire qu une seule mission bavarde peut peser a elle
   seule 1,5 % du plafond. Trois cents de ces lignes et le 5 Mo serait atteint
   meme avec la borne en messages desactivee.

## 7. VERDICT

La question du createur est TRANCHEE par la mesure : les outbox ont une
rotation, elle est declaree, elle est jouee a chaque cloture, elle borne
reellement (cobaye C3), et elle epargne les boites saines (contre-temoin C4).
Aucune n approche 5 Mo : la plus grosse est a 58,2 % du plafond, et les deux
boites du flux 2 sont meme au-dessus de leur borne en messages sans que la
taille ne soit en cause.

Ce que la question ne savait pas, et que la mesure a dit : ce n est pas le
5 Mo qui tient les boites, c est les 200 messages. Le 5 Mo est la derniere
ligne, pas la premiere.
