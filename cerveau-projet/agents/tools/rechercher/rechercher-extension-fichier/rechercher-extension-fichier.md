---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# rechercher-extension-fichier

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** rechercher
**Chemin :** `agents/tools/rechercher/rechercher-extension-fichier/`
**Proprietaire :** Buffy (outil partage)

## Description

Extraire l'extension d'un fichier (la partie apres le dernier point), ou verifier si un fichier a une extension donnee. Utilitaire de base pour les scripts qui doivent connaitre le type d'un fichier avant de le traiter (ex: `.sh`, `.md`, `.py`).

## Utilisation

Version Python (recommandee) :

```bash
# Afficher l'extension
python3 rechercher-extension-fichier.py fichier.md

# Verifier si le fichier a une extension donnee
python3 rechercher-extension-fichier.py --verifier sh script.sh
echo $?   # 0 si .sh, 1 sinon

# Avec details
python3 rechercher-extension-fichier.py --verbose fichier.md
```

Version bash equivalente : `rechercher-extension-fichier.sh` (meme logique).

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

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-06 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter, VERSION 0.2.0, statut prepare |
| 0.2.0-py | 2026-08-07 | Version Python creee (rechercher-extension-fichier.py), basee sur outil-template.py. Extraction d'extension + --verifier (exit 0/1) |

---
