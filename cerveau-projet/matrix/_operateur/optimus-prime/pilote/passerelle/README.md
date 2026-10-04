---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
---

# Porte `passerelle` -- l extraction des demandes du user

> **Le passage entre le canal du user et la Matrice.** Le user ecrit ses demandes
> dans `user-demandes/user-demandes.md` (la PASSERELLE USER) ; cette porte les LIT,
> en fait des ITEMS, et RETIRE du canal ce qui a ete servi.

## Les deux verbes

| Verbe | Ce qu il fait |
|---|---|
| `main.py passerelle lire` | LIT le canal et DIT tout : head, demandes (etat, crochet, bornes de lignes, titre), etats, crochets, ANOMALIES. **Aucune ecriture** |
| `main.py passerelle extraire [--rang N \| --tout] [--appliquer]` | DEPOSE un item par la porte de l entonnoir, ARCHIVE les mots EXACTS du user au journal du canal, puis RETIRE la demande du canal. **DRY par defaut** |

Si on ne retient qu une chose : `extraire` sans `--appliquer` **n ecrit rien**, il
DIT ce qu il ferait. Le canal est ecrit par le user EN CONTINU ; une porte qui
ecrit sans le dire serait la pire des portes.

## La convention du canal (MESUREE, jamais devinee)

Le FORMAT du canal vit a son domicile unique (`matrice/data/commun/passerelle_user.py`,
`decouper_demandes`) : la porte le CONSOMME, elle ne le recopie pas (M-076).

Mesure du 2026-09-29 sur le corpus : **34 blocs de patternes pour 34 demandes**.
Chaque demande est PRECEDEE d un bloc de lignes de patternes consecutives ; le
PREMIER mot du bloc est son ETAT ; les lignes suivantes sont son ECHELLE (les
etapes preparees) ; une ligne de patternes sans mot est le pattern a lire declare
par l en-tete. Mesure : les 34 blocs commencaient par `A-FAIRE` -- aucune demande
n avait donc ete extraite.

Seul `A-FAIRE` s extrait : les autres etats (FAIT, A-CONTROLER, CERTIFIER) se
SUIVENT, ils ne se sautent pas -- un pattern ne franchit pas deux etapes dans la
meme mission (regle du user).

## Ce que l extraction ne perd JAMAIS, et ce qu elle TRANSPOSE

- Les MOTS EXACTS du user partent au **journal du canal**
  (`user-demandes/archives/demandes-extraites.md`) AVANT le retrait : cette zone
  est hors jugement, ses accents y sont legitimes. Le canal est aussi suivi par git.
- L ITEM, lui, porte une **transcription ASCII** (`carte_ascii.convertir_texte`) :
  la Matrice est ASCII, et l item voyage dans ses BDD. La transcription est DITE a
  chaque extraction, avec les caracteres non convertibles -- jamais silencieuse.

## Ce que la porte ne fait PAS

1. Elle ne CLASSE pas la demande : le type et le role sont proposes par la porte de
   l entonnoir (la table type/categorie). Elle transporte, elle ne juge pas.
2. Elle n ecrit JAMAIS un item elle-meme : un item se depose par sa porte.
3. Elle ne RETIRE rien qu elle n a pas depose : si l entonnoir refuse, la demande
   RESTE dans le canal.
