# lire-frontmatter

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** lire
**Chemin :** `agents/tools/lire/lire-frontmatter/`
**Proprietaire :** Buffy (outil partage)

## Description

Extraire le frontmatter YAML en tete d'un fichier markdown (le bloc delimite par `---` en premieres lignes). Utile pour lire rapidement les metadonnees d'un fichier du cerveau (nom, role, version, statut...) sans ouvrir tout le fichier.

## Utilisation

```bash
# Afficher tout le frontmatter
lire-frontmatter.sh fichier.md

# Version Python (recommandee)
python3 lire-frontmatter.py fichier.md

# Afficher uniquement la valeur d'un champ
lire-frontmatter.sh --champ statut fichier.md

# Avec details (presence/absence)
lire-frontmatter.sh --verbose fichier.md
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--champ <nom>` | Afficher uniquement la valeur d'un champ (ex: statut) | - |
| `--verbose` | Afficher les details (presence/absence) | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. Verifie que le fichier existe
2. Extrait le bloc frontmatter (delimite par `---` en premiere et troisieme ligne)
3. Affiche le contenu, ou la valeur d'un champ avec `--champ`

## Exemples de sortie

```bash
$ lire-frontmatter.sh --champ statut fichier.md
ebauche

$ lire-frontmatter.sh fichier.md
nom: exemple
version: 0.1.0
statut: ebauche
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| Lire les metadonnees d'un fichier avant de le traiter | `lire-frontmatter.sh --champ statut fichier.md` |
| Verifier le role d'un outil avant de l'utiliser | `lire-frontmatter.sh --champ nom outil.md` |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `lire-fichier` | Lire tout le contenu d'un fichier |
| `lire-lignes` | Lire des lignes specifiques |
| `valider-ebauche` | Verifier les exigences minimales d'un ebauche (frontmatter) |

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
| 0.2.0-py | 2026-08-07 | Version Python creee (--champ, --verbose, --version) |

---
