# valider-pense-bete

**Version :** 0.1.0-beta
**Statut :** ebauche
**Categorie :** Valider
**Chemin :** `agents/tools/valider/valider-pense-bete/`

## Description

Verifie l'integrite d'un pense-bete : structure, header, sections, nommage, placeholders et conformite ASCII. Athena l'utilise a la fin de sa mission pour s'assurer que le fichier n'est pas casse, corrompu ou incomplet avant de reactiver Cerberus.

## Utilisation

```bash
# Valider un pense-bete
valider-pense-bete.sh pense-bete-pipeline.001.01.ebauche.md

# Avec details de chaque verification
valider-pense-bete.sh --verbose pense-bete-pipeline.001.01.ebauche.md
```

## Options

| Option | Description |
|---|---|
| `--verbose` | Afficher les details de chaque verification |
| `--help` | Afficher l'aide |

## Verifications effectuees

| # | Verification | Critere |
|---|---|---|
| 1 | **Fichier** | Existe et n'est pas vide |
| 2 | **Header** | Statut, ID, Class, Cree, Theme presents |
| 3 | **Sections** | Les 6 sections du template presentes |
| 4 | **Nommage** | `pense-bete-[theme].[id].[class].[statut].md` |
| 5 | **Placeholders** | Aucun `[...]` non rempli (attention, non bloquant) |
| 6 | **ASCII** | Aucun accent, aucun emoji |

## Ce que l'outil fait

1. **Existence** - Verifie que le fichier existe et n'est pas vide
2. **Header** - Verifie les 5 champs (Statut, ID, Class, Cree, Theme)
3. **Sections** - Verifie les 6 sections (1. Idee ... 6. RVAV)
4. **Nommage** - Verifie le pattern du nom de fichier
5. **Placeholders** - Detecte les `[...]` non remplis (indicateur d'incompletude)
6. **ASCII** - Detecte les caracteres non-ASCII (accents, emojis)

## Exemples de sortie

```bash
$ valider-pense-bete.sh pense-bete-pipeline.001.01.ebauche.md

=== Validation du pense-bete ===
Fichier : pense-bete-pipeline.001.01.ebauche.md

=== Resume ===
[OK] Le pense-bete est valide
```

Avec un probleme :

```bash
$ valider-pense-bete.sh pense-bete-incomplet.001.01.ebauche.md

=== Validation du pense-bete ===
Fichier : pense-bete-incomplet.001.01.ebauche.md

  [ERREUR] Header manquant : Theme
  [ERREUR] Section manquante : ## 6. RVAV du pense-bete
  [ATTENTION] Placeholders non remplis :
    3:[L'essence du concept - ce que ce pense-bete apporte de nouveau ou resout]

=== Resume ===
[ERREUR] 2 probleme(s) detecte(s)
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Fin de mission d'Athena** | Verification avant de reactiver Cerberus |
| **Apres remplissage** | S'assurer que toutes les sections sont completes |
| **Avant changement de statut** | Verifier que le pense-bete est pret pour `prepare` |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `squelette-pense-bete` | Cree le squelette avant le remplissage |
| `remplir-pense-bete` | Remplit les sections avant la validation |
| `valider-conformite-ascii` | Verification ASCII globale du projet |
| `changer-statut` | Change le statut apres validation |
