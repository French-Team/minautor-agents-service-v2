---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# rechercher-fichier

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** Rechercher
**Chemin :** `agents/tools/rechercher/rechercher-fichier/`
**Proprietaire :** outil partage

## Description

Verifier si un fichier existe. Retourne 0 (vrai) ou 1 (faux).

## Utilisation

Version Python (recommandee) :

```bash
# Verifier et afficher
python3 rechercher-fichier.py --verbose fichier.md

# Dans un script
if python3 rechercher-fichier.py fichier.md; then
    echo "Le fichier existe"
fi
```

Version bash equivalente : `rechercher-fichier.sh` (meme logique).

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
| 0.2.0-py | 2026-08-07 | Version Python creee (rechercher-fichier.py), basee sur outil-template.py. Verifie l'existence d'un fichier, exit 0/1 |

## Notes de creation

- [x] L'outil est conforme ASCII
- [x] L'outil est reference dans index-tools.md
- [x] Le statut est passe de `ebauche` a `prepare`