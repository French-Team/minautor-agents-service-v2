---
identite:
  type: outil
  appartient_a: commun
  commun: true
  combos:
    - combos-corriger-non-ascii
---
# corriger-dictionnaire-accents

**Version :** 0.2.2
**Statut :** prepare
**Categorie :** corriger
**Chemin :** `agents/tools/corriger/corriger-dictionnaire-accents/`
**Proprietaire :** Buffy (outil partage)

## Description

Source de donnees : dictionnaire de correspondance `accent -> ASCII` utilise par les outils de correction d'accents (`corriger-accents-zones-sensibles`, `valider-conformite-ascii`). Fournit aussi un script utilitaire de correction simple.

## Role reel

| Usage | Outil consommateur |
|---|---|
| Dictionnaire de correspondance | `corriger-accents-zones-sensibles` |
| Source des remplacements | `valider-conformite-ascii` |
| Script utilitaire standalone | `corriger-dictionnaire-accents.sh` |

## Dictionnaire

Le fichier `corriger-dictionnaire-accents.txt` (meme dossier) contient les correspondances au format :

```
accent|remplacement
```

Caracteres couverts : accents francais (e, e, a, c...), ligatures (oe, ae), apostrophes et guillemets courbes (U+2018, U+2019, U+201C, U+201D...), **guillemets francais U+00AB/U+00BB** (remplaces par le guillemet droit double, coherent avec les courbes), symboles courants (..., --, <=, >=), **fleches horizontales, verticales et doubles** (U+2190, U+2191, U+2192, U+2193, U+2194, U+21D0, U+21D2, U+21D4), **box drawing** (traits et coins de schemas U+2500, U+2502, U+250C, U+2510, U+2514, U+2518, U+251C, U+2524), **espace inse cable U+00A0** (remplace par l espace simple).

> **EXCEPTION VOLONTAIRE** : ce dictionnaire contient volontairement des caracteres non-ASCII (c'est sa fonction). Il est marque du bandeau `EXCEPTION VOLONTAIRE` et exclu des outils de validation ASCII. Voir `regles-emojis-ascii.md` section "Exceptions volontaires". Ne jamais le purger.

## Utilisation du script utilitaire

### CLI Python (version 0.2.2-py)

```
python3 corriger-dictionnaire-accents.py [OPTIONS] <fichier>

Options :
  --dry-run         Afficher les changements sans les appliquer
  --verbose         Afficher les details
  --dictionnaire    Chemin vers un dictionnaire personnalise
  --version         Afficher la version
```

### CLI bash (version originale)

```bash
# Apercu des changements sans appliquer
corriger-dictionnaire-accents.sh --dry-run fichier.md

# Corriger les accents d'un fichier
corriger-dictionnaire-accents.sh fichier.md

# Dictionnaire personnalise
corriger-dictionnaire-accents.sh --dictionnaire mon-dictionnaire.txt fichier.md
```

## Options

| Option | Description |
|---|---|
| `--dry-run` | Afficher les changements sans les appliquer |
| `--verbose` | Afficher les details des remplacements |
| `--dictionnaire` | Chemin vers un dictionnaire personnalise |
| `--help` | Afficher l'aide |

## Securite

| Mesure | Description |
|---|---|
| Sauvegarde | Cree `fichier.md.bak` avant modification |
| Dry-run | Apercu possible sans modification |
| Verification | Compte les caracteres restants |

## Voir aussi

- `corriger-accents-zones-sensibles` - Outil de correction intelligent qui consomme ce dictionnaire
- `corriger-emojis` - Pour les emojis Unicode
- `regles-emojis-ascii.md` - Regle immuable

## Navigation

- **Index** : [index-tools.md](../../index-tools.md)

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0-py | 2026-08-07 | Version Python creee (meme dossier, meme nom, base sur outil-template.py, lit le dictionnaire .txt existant) |
| 0.2.1-py | 2026-08-09 | Guillemets francais U+00AB/U+00BB ajoutes au dictionnaire partage (corriger-dictionnaire-accents.txt) -> guillemet droit double, coherent avec les guillemets courbes U+201C/U+201D |
| 0.2.2-py | 2026-08-09 | Fleches verticales et doubles (U+2191/U+2193/U+2194/U+21D0/U+21D2/U+21D4), box drawing (U+2500/U+2502/U+250C/U+2510/U+2514/U+2518/U+251C/U+2524) et espace inse cable U+00A0 ajoutes au dictionnaire partage |
| 0.1.0 | 2026-08-06 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter, VERSION 0.2.0, statut prepare |

---
