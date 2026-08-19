---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# combos-corriger-non-ascii

**Version :** 0.3.0
**Statut :** prepare
**Categorie :** combos
**Chemin :** `agents/tools/combos/combos-corriger-non-ascii/`
**Proprietaire :** Themis (outil partage)

## Description

Combo qui detecte et corrige les accents et emojis dans les fichiers du cerveau.

## Utilisation

### CLI Python (version 0.3.0-py)

```
python3 combos-corriger-non-ascii.py [DOSSIER] [OPTIONS]

Options :
  --dry-run     Afficher les changements sans les appliquer
  --all         Corriger TOUS les accents (texte francais et titres)
  --full        Scanner et corriger TOUT le projet d'un coup
                (dry OBLIGATOIRE avant wet : le wet est refuse sans
                preuve de dry recente)
  --rapport     Sauvegarder un rapport dans themis/rapports/
  --version     Afficher la version
```

### Mode --full (projet entier)

Le mode `--full` scanne le projet entier (toutes les extensions ASCII
attendues : .md, .sh, .py, .txt, .json, .yaml, .yml, .js) et corrige d'un
coup tous les fichiers non conformes. Il impose une SEQUENCE OBLIGATOIRE :

```
# 1. DRY (obligatoire) : scan complet + rapport, aucune modification
python3 combos-corriger-non-ascii.py --full --dry-run

# 2. Examiner le rapport (tous les fichiers concernes, repartition
#    accent/emoji/autre, caracteres uniques par fichier)

# 3. WET (autorise seulement si le dry a ete fait recemment)
python3 combos-corriger-non-ascii.py --full
```

**Garantie dry-obligatoire** : le wet est REFUSE (code 2) si aucune preuve
de dry recente (fichier `tmp-combos-full/preuve-dry-full.json`, valable 60
minutes) n'existe. Le dry ecrit la preuve ; le wet la verifie (presente,
recente, meme racine) avant de corriger. On ne peut PAS corriger sans avoir
vu le rapport dry.

**Rapport concis mais complet** : le dry affiche le resume global (fichiers,
lignes, caracteres, repartition accent/emoji/autre) puis TOUS les fichiers
concernes (1 ligne chacun : nb lignes, nb caracteres, caracteres uniques en
code U+XXXX). Rien n'est tronque : meme si les fichiers sont nombreux, ils
sont tous listes.

**Performance** : le scan est en Python pur (rapide). Le wet corrige
UNIQUEMENT les fichiers detectes par le dry (mode fichier direct, ~0,3 s
par fichier) au lieu de relancer une correction recursive sur tout le
projet.

**Limite connue** : les caracteres ABSENTS des dictionnaires
(corriger-dictionnaire-accents, dictionnaire-emojis) ne sont pas
corrigeables (ex : bullet U+2022, certains emojis). Le dry les liste avec
leur code : enrichir le dictionnaire ou corriger a la main.

### CLI bash (version originale)

```bash
bash combos-corriger-non-ascii.sh [DOSSIER] [OPTIONS]
```

## Options

- `--dry-run` : afficher les changements sans les appliquer
- `--full` : scanner et corriger tout le projet d'un coup (dry obligatoire avant wet)
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
| 0.3.0 | 2026-08-18 | Mode --full : scan projet entier, dry obligatoire avant wet (preuve datee, wet refuse sans elle), rapport concis mais complet (tous les fichiers, codes U+XXXX), wet cible uniquement les fichiers detectes (performance), timeout reduit a 60 s |
| 0.2.0-py | 2026-08-07 | Version Python creee (orchestrateur subprocess des 4 etapes : detection, emojis, accents, verification, meme logique que le .sh) |
| 0.1.0 | 2026-08-06 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter ajoute, VERSION 0.2.0, en-tete corrige (combos-combos- -> combos-) |

---
