---
identite:
  type: outil
  appartient_a: matrice
  commun: true
  version: 1
  date: 2026-09-26
  liens: matrice/data/commun/carte_identite.py, matrice/data/outils/carte-creer/DESCRIPTION.md, matrice/data/outils/carte-modifier/DESCRIPTION.md
---

# carte-editer -- remplacer une carte entiere (MO-430)

Remplace le front-matter `identite:` d un document par un NOUVEAU bloc fourni
par fichier. Le bloc est valide par le DOMICILE partage
(`matrice/data/commun/carte_identite.py` : trois cles obligatoires, vocabulaire
ferme des types, liens canoniques et vivants) AVANT toute ecriture, puis passe
PAR LA PORTE `ecrire` (decision createur MO-430) : fragments puis cible, donc
validation, point de restauration et refus a occurrence unique -- si la porte
refuse, la cible reste INTACTE. Le garde de provenance (controle attribution)
jauge chaque carte remplacee.

## Commandes

| Commande | Usage |
|---|---|
| `editer` | `python3 cerveau-projet/matrix/lancer.py carte-editer editer --fichier <chemin> --nouveau-fichier <chemin du nouveau front-matter>` |

## Codes

| code | signification |
|---|---|
| 0 | carte remplacee (ou deja identique : RIEN A FAIRE, non pas une erreur) |
| 1 | ecart (ecriture refusee par la porte) |
| 2 | refus d usage (options manquantes, document sans carte, bloc non valide ou non conforme) -- le refus NOMME son remede |

## Protections

- un document SANS carte est REFUSE : la carte se POSE d abord (`carte-creer`) ;
- le nouveau bloc est juge par le domicile partage, jamais par l outil : un
  type hors vocabulaire, une cle obligatoire vide ou un lien mort arretent
  l edition AVANT ecriture ;
- le corps du document n est jamais touche : seul le bloc entre `---` change.

## Quand l utiliser

Changer plusieurs champs d un coup, migrer une carte vers une autre forme
(minimale -> complete), ou corriger une carte non conforme apres mesure.
