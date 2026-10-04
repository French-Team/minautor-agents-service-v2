---
identite:
  type: outil
  appartient_a: matrice
  commun: true
  version: 1
  date: 2026-09-26
  liens: matrice/data/commun/carte_identite.py, matrice/data/outils/carte-editer/DESCRIPTION.md
---

# carte-creer -- poser une carte d identite (MO-430)

Pose un front-matter `identite:` en tete d un document qui n en a pas. Le bloc
vient du MODELE de reference (`matrice/templates/carte-identite`), les regles du
DOMICILE partage (`matrice/data/commun/carte_identite.py`) : vocabulaire ferme
des types, trois cles obligatoires, liens a la forme canonique, cible vivante,
jamais d auto-reference. Toute ecriture passe PAR LA PORTE `ecrire`
(decision createur MO-430) : fragments puis cible, donc validation, point de
restauration et refus a occurrence unique -- le garde de provenance
(controle attribution) jauge chaque carte posee.

## Commandes

| Commande | Usage |
|---|---|
| `creer` | `python3 cerveau-projet/matrix/lancer.py carte-creer creer --fichier <chemin> --type <type> --appartient-a <nom> [--commun true\|false] [--liens "<c1>, <c2>"] [--version <n>] [--date AAAA-MM-JJ] [--statut <etat>] [--tags "<m1>, <m2>"] [--modele complet\|minimal]` |

## Codes

| code | signification |
|---|---|
| 0 | carte posee (ou operation reussie) |
| 1 | ecart (modele illisible, ecriture refusee par la porte) |
| 2 | refus d usage (option inconnue ou privee de valeur, fichier absent, carte deja presente, carte non conforme) -- le refus NOMME son remede |

## Protections

- le document qui porte DEJA une carte est REFUSE : `carte-modifier` change un
  champ, `carte-editer` remplace la carte entiere ;
- `--type` et `--appartient-a` sont obligatoires : ce sont les deux cles qui ne
  se devinent pas ;
- la carte est validee AVANT ecriture (memes jugements que le garde
  `verifier-cartes-identite`) : une carte non conforme n est jamais posee ;
- sans `--modele`, le modele COMPLET sert (les champs du modele sont la
  reference ; un champ sans valeur est OMIS et DIT, jamais rempli d un
  placeholder).

## Quand l utiliser

Premiere mise en cartes d un document sans carte, ou fabrication d un document
retrouvable par `rechercher --champ` / `--lien`.
