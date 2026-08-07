# rechercher-texte

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** Rechercher
**Chemin :** `agents/tools/rechercher/rechercher-texte/`
**Proprietaire :** outil partage

## Description

Rechercher un pattern dans un fichier (grep generique).

## Utilisation

Version Python (recommandee) :

```bash
# Rechercher un mot
python3 rechercher-texte.py "mot" fichier.md

# Insensible a la casse avec numeros
python3 rechercher-texte.py --insensible --numeros "texte" fichier.md

# Compter
python3 rechercher-texte.py --compter "mot" fichier.md
```

Version bash equivalente : `rechercher-texte.sh` (meme logique).

## Options

| Option | Description | Defaut |
|---|---|---|
| `--insensible` | Ignorer la casse | false |
| `--numeros` | Afficher les numeros de ligne | false |
| `--inverser` | Lignes non-match | false |
| `--compter` | Compter les occurrences | false |
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-05 | Creation initiale |
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels (pattern simple, --insensible, --numeros, --compter), promotion prepare |
| 0.2.0-py | 2026-08-07 | Version Python creee (rechercher-texte.py), basee sur outil-template.py. Equivalent grep : --insensible/--numeros/--inverser/--compter |

## Notes de creation

- [x] L'outil est conforme ASCII
- [x] L'outil est reference dans index-tools.md
- [x] Le statut est passe de `ebauche` a `prepare`