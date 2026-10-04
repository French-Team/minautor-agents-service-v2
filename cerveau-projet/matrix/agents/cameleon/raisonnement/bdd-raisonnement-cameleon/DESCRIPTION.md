---
identite:
  type: outil
  appartient_a: cameleon
  commun: true
---

# OUTIL -- bdd-raisonnement-cameleon (domicile du CAMELEON)

> Outil Python dedie a la BDD `segments-cameleon.json`, dans le DOMICILE du CAMELEON
> (`agents/cameleon/raisonnement/`) : VISIBLE et PARTAGE (decision createur
> 2026-09-27 : la BDD de raisonnement du cameleon est PARTAGEE dans la Matrice,
> distincte de celle d Optimus qui vit dans la zone invisible L-016). Genere
> depuis le moule templates/outil-bdd avec la SURCHARGE templates/outil-bdd-cameleon
> (modele-mere : bdd-lecons).

## Options

```
python3 cerveau-projet/matrix/lancer.py <chemin-vers-bdd-raisonnement-cameleon>/main.py ajouter --segment "..." --tags "tag1,tag2" [--source "..."]
python3 cerveau-projet/matrix/lancer.py <chemin-vers-bdd-raisonnement-cameleon>/main.py lire [--tag <tag>]
python3 cerveau-projet/matrix/lancer.py <chemin-vers-bdd-raisonnement-cameleon>/main.py verifier
```

- `--segment` : segment (le contenu lui-meme, obligatoire).
- `--tags` : liste separee par des virgules -- obligatoire : pas d'element orphelin.
- `--source` : mission, outil ou fichier d'origine (facultatif).
- `lire --tag X` : filtre les entrees portant le tag X.

APPEL PAR CHEMIN : l outil n est PAS sous `data/outils/` : le lanceur ne le
resout donc PAS par son nom nu -- on donne le chemin de son `main.py`. La carte
est `commun: true` (porte COMMUNE : servie sans identite declaree), et le moteur
de recherche la sert en SOURCE PARTAGEE (sans `--prive`).

## Format de la BDD

`{"identite": {...}, "segments": [{"id", "date", "segment", "tags", "source"}, ...]}`

## Architecture (convention-architecture-outils)

| Piece | Role |
|---|---|
| DESCRIPTION.md | la facade (ce fichier) |
| main.py | point d'entree global : DIRIGE |
| constants.py | chemins, valeurs (variante CAMELEON) |
| commun.py | fonctions communes : charger, enregistrer (atomique, LF), empreinte, options |
| ajouter/ | ajouter un segment tague |
| lire/ | lister (tout ou par tag) |
| verifier/ | integrite SHA-256 (etalon-or) |

## Protections

- Ecriture atomique (tmp + remplacement), fins de ligne LF forcees (determinisme).
- Empreinte SHA-256 recalculee et enregistree A CHAQUE ecriture.
- Contenu et tags obligatoires : pas d'entree orpheline sans tag.
- PARTAGEE : visible des DEUX agents (aucune exclusion L-016 sur ce domicile).
