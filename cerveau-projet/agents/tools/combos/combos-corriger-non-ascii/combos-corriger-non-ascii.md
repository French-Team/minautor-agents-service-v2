# combos-corriger-non-ascii

Combo qui detecte et corrige les accents et emojis dans les fichiers du cerveau.

## Usage

```bash
bash combos-combos-corriger-non-ascii.sh [DOSSIER] [OPTIONS]
```

## Options

- `--dry-run` : afficher les changements sans les appliquer
- `--rapport` : sauvegarder un rapport dans `themis/rapports/`

## Chainage

| Etape | Outil | Action |
|---|---|---|
| 1 | `rechercher-accents-sensibles` | Detecter les problemes |
| 2 | `corriger-emojis` | Remplacer les emojis par ASCII |
| 3 | `corriger-accents-zones-sensibles` | Remplacer les accents par ASCII |
| 4 | `rechercher-accents-sensibles` | Verifier le nettoyage |

## Exclusions automatiques

- Dictionnaires d'outils (`dictionnaire-*.txt`)
- Fichier de regles (`regles-emojis-ascii.md`)
- Dossier `exemples/`

## Quand l'utiliser

- Apres la creation de fichiers qui contiennent des accents
- En phase de purification du cerveau
- Par tout agent qui a besoin de fichiers ASCII purs
