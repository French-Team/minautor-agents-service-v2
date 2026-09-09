# OUTIL -- bdd-conventions-matrice

> Outil Python dedie a la BDD `conventions-matrice.json` (genere depuis le moule
> templates/outil-bdd par dupliquer-template, modele-mere : bdd-lecons).

## Options

```
python main.py ajouter --convention "..." --tags "tag1,tag2" [--source "..."]
python main.py lire    [--tag <tag>]
python main.py verifier
```

- `--convention` : le contenu de l'la convention (obligatoire).
- `--tags` : liste separee par des virgules -- obligatoire : pas d'la convention orpheline.
- `--source` : mission, outil ou fichier d'origine (facultatif).
- `lire --tag X` : filtre les entrees portant le tag X.

## Format de la BDD

`{"identite": {...}, "conventions": [{"id", "date", "convention", "tags", "source"}, ...]}`

## Architecture (convention-architecture-outils)

| Piece | Role |
|---|---|
| DESCRIPTION.md | la facade (ce fichier) |
| main.py | point d'entree global : DIRIGE |
| constants.py | chemins, valeurs |
| commun.py | fonctions communes : charger, enregistrer (atomique, LF), empreinte, options |
| ajouter/ | ajouter une la convention taguee |
| lire/ | lister (tout ou par tag) |
| verifier/ | integrite SHA-256 (etalon-or) |

## Protections

- Ecriture atomique (tmp + remplacement), fins de ligne LF forcees (determinisme).
- Empreinte SHA-256 recalculee et enregistree A CHAQUE ecriture.
- Contenu et tags obligatoires : pas d'entree orpheline sans tag.
