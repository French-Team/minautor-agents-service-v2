---
identite:
  type: outil
  appartient_a: matrice
  commun: true
  version: 1
  date: 2026-09-26
  liens: matrice/data/commun/carte_identite.py, matrice/data/outils/carte-editer/DESCRIPTION.md, matrice/data/outils/carte-comparer/DESCRIPTION.md
---

# carte-modifier -- changer UN champ de carte (MO-430)

Change une seule cle de la carte d un document : la valeur est REMPLACEE, une
cle absente est INSEREE (avec l indentation des voisines), `--supprimer`
RETIRE le champ (jamais une cle obligatoire). Le vocabulaire des cles vient du
MODELE de reference (`matrice/templates/carte-identite`) : une cle qui n est ni
du modele ni deja dans la carte est une faute de frappe, et elle est NOMMEE.
Le bloc RESULTAT est valide par le DOMICILE partage
(`matrice/data/commun/carte_identite.py`) AVANT toute ecriture, puis passe PAR
LA PORTE `ecrire` (decision createur MO-430) : fragments puis cible, donc
validation, point de restauration et refus a occurrence unique -- si la porte
refuse, la cible reste INTACTE. Le garde de provenance (controle attribution)
jauge chaque carte modifiee.

## Commandes

| Commande | Usage |
|---|---|
| `modifier` | `python3 cerveau-projet/matrix/lancer.py carte-modifier modifier --fichier <chemin> --cle <nom> --valeur <valeur>` |
| `modifier` (retirer) | `python3 cerveau-projet/matrix/lancer.py carte-modifier modifier --fichier <chemin> --cle <nom> --supprimer` |

## Codes

| code | signification |
|---|---|
| 0 | champ change (ou deja identique : RIEN A FAIRE, non pas une erreur) |
| 1 | ecart (ecriture refusee par la porte) |
| 2 | refus d usage (gestes absents ou exclusifs, document sans carte, cle inconnue, resultat non conforme) -- le refus NOMME son remede |

## Protections

- `--valeur` et `--supprimer` sont EXCLUSIFS : un seul geste par appel ;
- une cle obligatoire n est jamais retiree ;
- le changement rendu est VALIDE avant ecriture : `--type type-invente` ou
  `--commun peut-etre` arretent l appel sans rien toucher ;
- pour les cles listees (`liens`, `tags`), `--valeur` remplace la LISTE
  entiere (separateur : virgule) -- ajouter un lien, c est relire la liste et
  la reposer.

## Quand l utiliser

Mettre a jour un champ au fil de l eau : statut, date, version, liens --
sans remplacer la carte entiere (carte-editer).
