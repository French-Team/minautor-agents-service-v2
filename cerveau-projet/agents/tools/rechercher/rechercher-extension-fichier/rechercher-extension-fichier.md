# rechercher-extension-fichier

**Version :** 0.1.0-beta
**Statut :** ebauche
**Categorie :** Rechercher
**Chemin :** `agents/tools/rechercher/rechercher-extension-fichier/`

## Description

Extraire l'extension d'un fichier (la partie apres le dernier point), ou verifier si un fichier a une extension donnee. Utilitaire de base pour les scripts qui doivent connaitre le type d'un fichier avant de le traiter (ex: `.sh`, `.md`, `.py`).

## Utilisation

```bash
# Afficher l'extension
rechercher-extension-fichier.sh fichier.md

# Verifier si le fichier a une extension donnee
rechercher-extension-fichier.sh --verifier sh script.sh
echo $?   # 0 si .sh, 1 sinon

# Avec details
rechercher-extension-fichier.sh --verbose fichier.md
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--verifier <ext>` | Verifier si le fichier a cette extension (0 = oui, 1 = non) | - |
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. Verifie qu'un fichier est fourni
2. Extrait la partie apres le dernier point (ou rien si pas d'extension)
3. Affiche l'extension, ou compare avec `--verifier` et retourne 0/1

## Exemples de sortie

```bash
$ rechercher-extension-fichier.sh outil.md
md

$ rechercher-extension-fichier.sh archive.tar.gz
gz

$ rechercher-extension-fichier.sh --verifier sh script.sh && echo "c'est un .sh"
c'est un .sh
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| Connaitre le type d'un fichier avant traitement | `rechercher-extension-fichier.sh fichier` |
| Filtrer les fichiers par type dans un script | `rechercher-extension-fichier.sh --verifier md fichier` |
| Verifier qu'un outil a le bon format | `rechercher-extension-fichier.sh --verifier sh outil.sh` |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `rechercher-fichier` | Verifier qu'un fichier existe |
| `rechercher-fichiers-vides` | Rechercher les fichiers markdown vides |
| `verifier-documents-manquants` | Verifier les .sh sans .md et inversement |

## Notes de creation

- [x] L'outil a ete teste en `--dry-run` avant application
- [x] L'outil est conforme ASCII (aucun accent, aucun emoji) -- valider avec `valider-conformite-ascii`
- [x] L'outil est reference dans `index-tools.md`
- [x] L'outil est assigne a un agent dans sa carte de decision (protocole-outils Regle 6)
- [ ] Le statut est passe de `ebauche` a `prepare` apres validation RVAV
