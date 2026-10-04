---
identite:
  type: protocole
  appartient_a: optimus-prime
  commun: false
---

# Proto 11 -- RAISONNEMENT PROGRESSIF PAR SEGMENTS

> DEMANDE CREATEUR du 2026-09-24 (mission MO-395, item EO-398) : < un raisonnement
> ne peut pas etre continu et sans traces : il doit etre progressif et trace > ;
> < quand on raisonne en continu, on accumule des donnees qui finissent par devenir
> inutiles et perdues pour les raisonnements futurs sur les memes sujets > ;
> < chaque partie du raisonnement devient un SEGMENT, plus concret et plus concis,
> et ces segments peuvent etre reutilises par un raisonnement futur sur le meme
> sujet > ; < les segments doivent etre retrouvables par notre moteur de recherche,
> et chacun doit avoir sa carte d identite >.

## La regle

**Un raisonnement s ECRIT en SEGMENTS, jamais d un trait.**

- Un SEGMENT est une PARTIE du raisonnement : il a un AVANT (le segment precedent)
  et un APRES (celui qui le suivra).
- Il DIT ce qui est ETABLI (le gain, CONCIS) et ce qui RESTE OUVERT (ce que le
  segment suivant prendra).
- Il est TRACE : il vit HORS de la fenetre de contexte, donc il survit a la session,
  a la coupure et au redemarrage.
- Il est REUTILISABLE : un raisonnement futur sur le MEME sujet part de ses segments
  au lieu de repartir de zero.
- Il porte sa CARTE D IDENTITE (`type: segment`) et se retrouve par LE MOTEUR DU
  PROJET, jamais par un outil natif (regle immuable `moteur-recherche-d-abord.md`).

## Le defaut que la regle ferme

Un raisonnement CONTINU consomme la fenetre de contexte et n en laisse RIEN : quand
le sujet revient, il faut tout refaire, et ce qui a ete accumule entre-temps est
perdu ou illisible. Un raisonnement PROGRESSIF echange du VOLUME contre de la DUREE :
chaque segment est plus court que le raisonnement qui l a produit, et il reste APRES.

## Ce que la regle n est PAS (trois voisins a ne pas confondre)

| Voisin | Ce qu il porte | Qui le porte |
|---|---|---|
| journal de mission | des EVENEMENTS (debut, fin, ecart) | `suivi-optimus` |
| lecon | une REGLE generale tiree d une experience, valable ailleurs | BDD `lecons` |
| segment | un ETAT de raisonnement sur UN sujet, avec son avant et son apres | ce protocole |

Le SEGMENT et la LECON se consomment ENSEMBLE : le segment dit OU on en est, la
lecon dit CE QU on en a appris. Une lecon sans segment se relit sans contexte ; un
segment sans lecon ne profite qu a son sujet.

## Quand (le declencheur, jamais une obligation)

La regle vise les sujets qui DURENT : plus d un tour, plus d une session, ou un sujet
sur lequel un raisonnement futur reviendra. Un raisonnement court qui rend un
resultat directement utilisable se note au BILAN de la mission, il ne fabrique pas un
segment de ceremonie (action minimale).

## Le geste (une seule porte, un seul moule)

1. POSER le segment : le moule invisible est servi par la porte des gabarits.

```
python3 cerveau-projet/matrix/lancer.py poser-template-pilote poser \
  --moule raisonnement/segment.md.moule \
  --cible _operateur/optimus-prime/raisonnement/segments/RS-XXX-sujet.md \
  --jeton APPARTIENT_A=optimus-prime --jeton DATE=AAAAMMJJ \
  --jeton LIENS=AUCUN --jeton ID_SEGMENT=RS-XXX --jeton SUJET=<sujet> \
  --jeton MISSION=MO-XXX --jeton QUESTION=<la question posee> \
  --jeton PRECEDENT=<RS-YYY ou AUCUN> --jeton ETAT=ouvert \
  --jeton ETABLI=<le gain> --jeton RESTE=<ce qui reste ouvert> \
  --jeton PREUVE=<la commande qui rejoue le constat>
```

2. RETROUVER le raisonnement : le moteur du projet, par la CARTE (c est ce qui la
   rend REUTILISABLE, donc ce qui la separe d un fichier de notes).

```
python3 cerveau-projet/matrix/lancer.py rechercher rechercher --champ "type=segment" --prive
python3 cerveau-projet/matrix/lancer.py rechercher rechercher --requete "<sujet>" --dans fichiers --prive
```

3. ENCHAINER : un raisonnement neuf LIT la chaine des segments (champ
   `Segment precedent`) avant de la refaire.

## Ou la regle se LIT

1. Ce protocole (`protocoles/proto-11-raisonnement-progressif.md`).
2. `protocoles-readme.md` : l index des protocoles.
3. Le MOULE : `suivi-pilote/templates/raisonnement/segment.md.moule`.
4. Les segments : `_operateur/optimus-prime/raisonnement/segments/`.

## Limite DITE

Les segments vivent dans la zone INVISIBLE (L-016) : le moteur les retrouve avec
`--prive`, et JAMAIS sans. Ce choix protege la separation cameleon/Optimus ; il a un
cout, dit ici : la commande sans `--prive` rend 0, et ce 0 est un FAIT (la zone est
hors perimetre), pas une cecite.
