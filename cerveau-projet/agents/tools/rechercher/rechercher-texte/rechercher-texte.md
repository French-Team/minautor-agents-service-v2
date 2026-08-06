# rechercher-texte

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** Rechercher
**Chemin :** `agents/tools/rechercher/rechercher-texte/`
**Proprietaire :** outil partage

## Description

Rechercher un pattern dans un fichier (grep generique).

## Utilisation

```bash
# Rechercher un mot
rechercher-texte.sh "mot" fichier.md

# Insensible a la casse avec numeros
rechercher-texte.sh --insensible --numeros "texte" fichier.md

# Compter
rechercher-texte.sh --compter "mot" fichier.md
```

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

## Notes de creation

- [x] L'outil est conforme ASCII
- [x] L'outil est reference dans index-tools.md
- [x] Le statut est passe de `ebauche` a `prepare`