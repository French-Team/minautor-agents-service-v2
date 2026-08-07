# combos-corriger-non-ascii

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** combos
**Chemin :** `agents/tools/combos/combos-corriger-non-ascii/`
**Proprietaire :** Themis (outil partage)

## Description

Combo qui detecte et corrige les accents et emojis dans les fichiers du cerveau.

## Utilisation

### CLI Python (version 0.2.0-py)

```
python3 combos-corriger-non-ascii.py [DOSSIER] [OPTIONS]

Options :
  --dry-run     Afficher les changements sans les appliquer
  --all         Corriger TOUS les accents (texte francais et titres)
  --rapport     Sauvegarder un rapport dans themis/rapports/
  --version     Afficher la version
```

### CLI bash (version originale)

```bash
bash combos-corriger-non-ascii.sh [DOSSIER] [OPTIONS]
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

## Code retour

| Code | Signification |
|---|---|
| 0 | Le combo s'est execute avec succes |
| 1 | Le dossier cible n'existe pas |

## Dependances

- rechercher-accents-sensibles, corriger-emojis, corriger-accents-zones-sensibles

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0-py | 2026-08-07 | Version Python creee (orchestrateur subprocess des 4 etapes : detection, emojis, accents, verification, meme logique que le .sh) |
| 0.1.0 | 2026-08-06 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter ajoute, VERSION 0.2.0, en-tete corrige (combos-combos- -> combos-) |

---
