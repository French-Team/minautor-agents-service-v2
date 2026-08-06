# lire-fichier

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** Lire
**Chemin :** `agents/tools/lire/lire-fichier/`
**Proprietaire :** outil partage

## Description

Lire le contenu complet (ou partiel) d'un fichier. Cet outil remplace l'utilisation de `cat` ou des outils tiers pour la lecture de fichiers.

## Utilisation

```bash
# Lire un fichier complet
lire-fichier.sh fichier.md

# Lire les 10 premieres lignes
lire-fichier.sh --lignes 10 fichier.md

# Lire de la ligne 5 a 15
lire-fichier.sh --debut 5 --fin 15 fichier.md

# Lire a partir de la ligne 20
lire-fichier.sh --debut 20 fichier.md
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--debut N` | Lire a partir de la ligne N | 1 |
| `--fin N` | Lire jusqu'a la ligne N | fin du fichier |
| `--lignes N` | Lire les N premieres lignes | tout |
| `--verbose` | Afficher le nombre de lignes | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. Verifie que le fichier existe
2. Applique les filtres de lignes si specifies
3. Affiche le contenu

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| Lire un fichier complet | `lire-fichier.sh fichier.md` |
| Voir le debut d'un fichier | `lire-fichier.sh --lignes 20 fichier.md` |
| Extraire un extrait | `lire-fichier.sh --debut 10 --fin 30 fichier.md` |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `lister-fichiers` | Trouver le fichier, puis le lire |
| `rechercher-texte` | Trouver une ligne, puis lire le contexte |

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-05 | Creation initiale |
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels (lecture complete, --lignes, --debut/--fin, fichier inexistant), categorie corrigee (Explorer -> Lire), promotion prepare |

## Notes de creation

- [x] L'outil est conforme ASCII
- [x] L'outil est reference dans index-tools.md
- [x] Le statut est passe de `ebauche` a `prepare`