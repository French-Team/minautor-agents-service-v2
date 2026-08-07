# copier-fichier

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** Copier
**Chemin :** `agents/tools/copier/copier-fichier/`
**Proprietaire :** outil partage

## Description

Copier un fichier vers une destination avec verification.

## Utilisation

### CLI Python (version 0.2.0-py)

```
python3 copier-fichier.py [OPTIONS] <source> <destination>

Options :
  --forcer     Ecraser si la destination existe
  --dry-run    Simuler sans copier
  --verbose    Afficher les details
  --version    Afficher la version
```

### CLI bash (version originale)

```bash
# Copier un fichier
copier-fichier.sh source.md destination.md

# Ecraser si existe
copier-fichier.sh --forcer source.md destination.md
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--forcer` | Ecraser si la destination existe | false |
| `--dry-run` | Simuler sans copier | false |
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0-py | 2026-08-07 | Version Python creee (meme dossier, meme nom, base sur outil-template.py) |
| 0.1.0-beta | 2026-08-05 | Creation initiale |
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels (copie simple, refus si existe, --forcer, --dry-run), promotion prepare |

## Notes de creation

- [x] L'outil est conforme ASCII
- [x] L'outil est reference dans index-tools.md
- [x] Le statut est passe de `ebauche` a `prepare`