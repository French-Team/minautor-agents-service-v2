---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# ecrire-fichier

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** Ecrire
**Chemin :** `agents/tools/ecrire/ecrire-fichier/`
**Proprietaire :** outil partage

## Description

Ecrire ou ecraser le contenu d'un fichier. Supporte l'ecriture depuis un argument ou depuis stdin.

## Utilisation

```bash
# Ecrire du contenu
ecrire-fichier.sh fichier.md "# Nouveau contenu"

# Version Python (recommandee)
python3 ecrire-fichier.py fichier.md "# Nouveau contenu"

# Ecrire depuis stdin
echo "texte" | ecrire-fichier.sh fichier.md -

# Version Python depuis stdin
echo "texte" | python3 ecrire-fichier.py fichier.md -

# Avec sauvegarde
ecrire-fichier.sh --backup fichier.md "# Nouveau"
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--backup` | Creer une sauvegarde .bak avant | false |
| `--dry-run` | Simuler sans ecrire | false |
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. Verifie les arguments
2. Cree une sauvegarde si demandee
3. Ecrase le contenu du fichier

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| Remplacer tout le contenu | `ecrire-fichier.sh fichier.md "nouveau"` |
| Ecrire depuis un pipe | `commande \| ecrire-fichier.sh fichier.md -` |

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-05 | Creation initiale |
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels (ecriture contenu, stdin, --dry-run), promotion prepare |
| 0.2.0-py | 2026-08-07 | Version Python creee (ecriture, ecrasement, --backup, --dry-run, stdin) |

## Notes de creation

- [x] L'outil est conforme ASCII
- [x] L'outil est reference dans index-tools.md
- [x] Le statut est passe de `ebauche` a `prepare`