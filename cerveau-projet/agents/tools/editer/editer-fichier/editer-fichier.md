---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# editer-fichier

**Version :** 0.2.0-py
**Statut :** prepare
**Categorie :** Editer
**Chemin :** `agents/tools/editer/editer-fichier/`
**Proprietaire :** outil partage

## Description

Remplacer une chaine par une autre dans un fichier. Version generique de corriger-liens et corriger-nommage.

## Utilisation

```bash
# Remplacer la premiere occurrence
editer-fichier.sh fichier.md "ancien" "nouveau"

# Remplacer toutes les occurrences
editer-fichier.sh --global fichier.md "texte" "remplacement"
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--global` | Remplacer toutes les occurrences | false (premiere seule) |
| `--backup` | Creer une sauvegarde .bak | false |
| `--dry-run` | Simuler sans modifier | false |
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. Verifie que le fichier existe
2. Compte les occurrences
3. Remplace selon le mode (premiere ou global)

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| Corriger un mot | `editer-fichier.sh f.md "faux" "vrai"` |
| Tout remplacer | `editer-fichier.sh --global f.md "X" "Y"` |

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-05 | Creation initiale |
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels (premiere occurrence, --global, --dry-run, fichier inexistant), promotion prepare |

## Notes de creation

- [x] L'outil est conforme ASCII
- [x] L'outil est reference dans index-tools.md
- [x] Le statut est passe de `ebauche` a `prepare`