# OUTIL -- bdd-protocoles-matrice

> Outil Python dedie a la BDD `protocoles-matrice.json` (genere depuis le moule
> templates/outil-bdd par dupliquer-template, modele-mere : bdd-lecons).

## Options

```
python main.py ajouter --protocole "..." --tags "tag1,tag2" [--source "..."]
python main.py lire    [--tag <tag>]
python main.py verifier
```

- `--protocole` : le contenu de l'le protocole (obligatoire).
- `--tags` : liste separee par des virgules -- obligatoire : pas d'le protocole orpheline.
- `--source` : mission, outil ou fichier d'origine (facultatif).
- `lire --tag X` : filtre les entrees portant le tag X.

## Format de la BDD

`{"identite": {...}, "protocoles": [{"id", "date", "protocole", "tags", "source"}, ...]}`

## Architecture (convention-architecture-outils)

| Piece | Role |
|---|---|
| DESCRIPTION.md | la facade (ce fichier) |
| main.py | point d'entree global : DIRIGE |
| constants.py | chemins, valeurs |
| commun.py | fonctions communes : charger, enregistrer (atomique, LF), empreinte, options |
| ajouter/ | ajouter une le protocole taguee |
| lire/ | lister (tout ou par tag) |
| verifier/ | integrite SHA-256 (etalon-or) |

## Protections

- Ecriture atomique (tmp + remplacement), fins de ligne LF forcees (determinisme).
- Empreinte SHA-256 recalculee et enregistree A CHAQUE ecriture.
- Contenu et tags obligatoires : pas d'entree orpheline sans tag.
