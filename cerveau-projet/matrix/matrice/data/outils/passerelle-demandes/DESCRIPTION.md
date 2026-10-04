---
identite:
  type: outil
  appartient_a: matrice
  commun: false
  flux: 2
  version: 1
  date: 2026-09-30
  liens: matrice/data/commun/passerelle_user.py, user-demandes/user-demandes.md
---

# passerelle-demandes -- extraire les demandes du createur (EO-481)

Le canal `user-demandes/user-demandes.md` est la **ZONE HORS JUGEMENT** du
createur : il y ecrit ses demandes en langage naturel, avec un CROCHET
(`[mission]`, `[???]`, `[question]`, ...) qui en donne l intention. L outil les
LIT, les TYPE, et les depose dans l entonnoir par la PORTE.

L extraction elle-meme n est pas ici : elle est lue au DOMICILE partage
(`matrice/data/commun/passerelle_user.py`), consommee jamais recopie (M-076).
La table `crochet -> type` vit dans `constants.py`, entiere, pour qu une
relecture puisse la contester d un seul regard.

## LE DRY ET LE WET

Deposer 35 items d un coup est irreversible dans les faits : un id est consomme,
un item apparait dans l entonnoir. Le DRY prepare et MONTRE ; le WET ecrit, et
**exige `--confirmer`**. Sans elle, l outil prepare, montre, et ne depose rien.

## CE QUE L OUTIL REFUSE DE FAIRE

- **Deviner un type.** Un crochet hors table n est PAS depose : la demande est
  DITEE et laissee au canal. Deposer sous un type choisi a la place du createur
  serait une decision prise a son detriment, qu il decouvrirait plus tard dans
  son entonnoir sans savoir pourquoi.
- **Retirer la demande du canal.** Le contrat du canal dit qu une demande
  extraite est retiree, mais le canal est hors jugement : ce retrait n a pas de
  voie validee, et le createur ne l a pas valide. Le canal reste INTACT, et
  l outil le dit.

## Commandes

| Commande | Usage |
|---|---|
| `lire` (LECTURE SEULE) | `python3 cerveau-projet/matrix/lancer.py --appelant operateur passerelle-demandes lire` |
| `deposer` (DRY) | `... passerelle-demandes deposer` |
| `deposer` (WET) | `... passerelle-demandes deposer --confirmer` |

## Codes

| Code | Sens |
|---|---|
| 0 | succes (ou DRY : rien depose) |
| 1 | au moins un item n a pas pu etre depose |
| 2 | appel mal forme, ou type inconnu |
