---
identite:
  type: outil
  appartient_a: matrice
  commun: true
  version: 1
  date: 2026-09-26
  liens: matrice/data/commun/carte_identite.py, matrice/data/outils/carte-modifier/DESCRIPTION.md, matrice/templates/carte-identite/README.md
---

# carte-comparer -- la carte face a SON MODELE (MO-430)

Decision createur MO-430 : la REFERENCE de comparaison est le MODELE de la
carte (`matrice/templates/carte-identite`) -- l outil dit si ses champs sont
PRESENTS et si la carte est CONFORME. Les cles du modele donnent les champs ;
la conformite vient du DOMICILE partage (`matrice/data/commun/carte_identite.py`
: trois cles obligatoires, vocabulaire ferme des types, commun qui dit true ou
false, liens canoniques et vivants) -- les memes jugements que le garde
`verifier-cartes-identite`, consommes jamais copie (M-076). L outil est en
LECTURE SEULE : il ne change rien, il REND un rapport.

## Commandes

| Commande | Usage |
|---|---|
| `comparer` (une carte) | `python3 cerveau-projet/matrix/lancer.py carte-comparer comparer --fichier <chemin> [--modele complet\|minimal]` |
| `comparer` (le corpus) | `python3 cerveau-projet/matrix/lancer.py carte-comparer comparer --corpus [--dans <dossier>] [--modele ...]` |

## Codes

| code | signification |
|---|---|
| 0 | CONFORME : z ecart, presence dite champ par champ |
| 1 | NON CONFORME : les ecarts sont LISTES (le rapport les nomme) |
| 2 | refus d usage (sujet absent ou double, document sans carte, perimetre vide) -- le refus NOMME son remede |

## Ce que le rapport dit

- **une carte** : presence des champs du modele (`presents 6/8`, `absents : ...`)
  puis conformite (CONFORME ou les ecarts un par un) ;
- **le corpus** : total des documents, presence PAR CHAMP (`liens : 11/113`),
  les documents sans carte, puis les ecarts (liste bornee).

Les cles absentes du modele ne sont pas des ecarts : une carte sans `liens`
est NORMALE (tout document n a pas de voisin) -- elles sont DITES, pas jugees.
Les documents sans carte sont COMPTEs, pas accuses : accuse-les, c est le
travail du garde `verifier-cartes-identite`.

## Quand l utiliser

Avant de livrer une carte (je suis conforme ?), pour mesurer un corpus
(ou manque-t-il des champs ?), et pour retrouver ce que le modele exige.
