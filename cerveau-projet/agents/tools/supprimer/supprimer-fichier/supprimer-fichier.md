# supprimer-fichier

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** Supprimer
**Chemin :** `agents/tools/supprimer/supprimer-fichier/`
**Proprietaire :** outil partage

## Description

Supprimer un fichier avec verification.

## Utilisation

```bash
# Supprimer un fichier
supprimer-fichier.sh fichier.md

# Simuler
supprimer-fichier.sh --dry-run fichier.md
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--dry-run` | Simuler sans supprimer | false |
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-05 | Creation initiale |
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels (suppression, fichier inexistant, --dry-run), promotion prepare |

## Notes de creation

- [x] L'outil est conforme ASCII
- [x] L'outil est reference dans index-tools.md
- [x] Le statut est passe de `ebauche` a `prepare`