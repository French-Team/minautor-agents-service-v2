# rechercher-fichier

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** Rechercher
**Chemin :** `agents/tools/rechercher/rechercher-fichier/`
**Proprietaire :** outil partage

## Description

Verifier si un fichier existe. Retourne 0 (vrai) ou 1 (faux).

## Utilisation

```bash
# Verifier et afficher
rechercher-fichier.sh --verbose fichier.md

# Dans un script
if rechercher-fichier.sh fichier.md; then
    echo "Le fichier existe"
fi
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--verbose` | Afficher le resultat | false |
| `--help` | Afficher l'aide | - |

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-05 | Creation initiale |
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels (fichier existe code 0, inexistant code 1), promotion prepare |

## Notes de creation

- [x] L'outil est conforme ASCII
- [x] L'outil est reference dans index-tools.md
- [x] Le statut est passe de `ebauche` a `prepare`