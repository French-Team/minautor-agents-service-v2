---
identite:
  type: outil
  appartient_a: matrice-data-outils
  commun: true
---

# OUTIL -- bdd-corvees -- ajoute et relit les corvees

> Outil Python dedie a la BDD `corvees.json` (genere depuis le moule
> templates/outil-bdd par dupliquer-template, modele-mere : bdd-lecons).

## Options

```
python3 cerveau-projet/matrix/lancer.py bdd-corvees ajouter --corvee "..." --tags "tag1,tag2" [--source "..."]
python3 cerveau-projet/matrix/lancer.py bdd-corvees lire [--tag <tag>]
python3 cerveau-projet/matrix/lancer.py bdd-corvees verifier
```

- `--corvee` : la tache ingrate elle-meme, avec son cout mesure et l'automatisation proposee (obligatoire).
- `--tags` : liste separee par des virgules -- obligatoire : pas de corvee orpheline.
- `--source` : mission, outil ou fichier d'origine (facultatif).
- `lire --tag X` : filtre les entrees portant le tag X.

## Format de la BDD

`{"identite": {...}, "corvees": [{"id", "date", "corvee", "tags", "source"}, ...]}`

## Architecture (convention-architecture-outils)

| Piece | Role |
|---|---|
| DESCRIPTION.md | la facade (ce fichier) |
| main.py | point d'entree global : DIRIGE |
| constants.py | chemins, valeurs |
| commun.py | fonctions communes : charger, enregistrer (atomique, LF), empreinte, options |
| ajouter/ | ajouter une corvee taguee |
| lire/ | lister (tout ou par tag) |
| verifier/ | integrite SHA-256 (etalon-or) |

## Protections

- Ecriture atomique (tmp + remplacement), fins de ligne LF forcees (determinisme).
- Empreinte SHA-256 recalculee et enregistree A CHAQUE ecriture.
- Contenu et tags obligatoires : pas d'entree orpheline sans tag.
