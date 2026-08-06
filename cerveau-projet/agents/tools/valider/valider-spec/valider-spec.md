# valider-spec

**Version :** 0.1.0-beta
**Statut :** ebauche
**Categorie :** Valider
**Chemin :** `agents/tools/valider/valider-spec/`

## Description

Verifie l'integrite d'une spec : structure, header, sections, nommage, placeholders et conformite ASCII. L'agent l'utilise a la fin de sa mission pour s'assurer que la spec n'est pas cassee, corrompue ou incomplete avant de passer au statut suivant.

## Utilisation

```bash
# Valider une spec
valider-spec.sh spec-pipeline.001.01.ebauche.md

# Avec details de chaque verification
valider-spec.sh --verbose spec-pipeline.001.01.ebauche.md
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
| 2 | **Header** | Statut, ID, Class, Cree, Theme, Pense-bete source |
| 3 | **Sections** | Les 10 sections du spec-template presentes |
| 4 | **Nommage** | `spec-[theme].[id].[class].[statut].md` |
| 5 | **Placeholders** | Aucun `[...]` non rempli (attention, non bloquant) |
| 6 | **ASCII** | Aucun accent, aucun emoji |

## Sections verifiees

| Section | Contenu attendu |
|---|---|
| 1. Objectif | Objectif precis de la spec |
| 2. Contexte | Origine, perimetre, public cible |
| 3. Exigences Fonctionnelles | Tableau par exigence |
| 4. Exigences Non-Fonctionnelles | Performance, securite, etc. |
| 5. Architecture | Vue d'ensemble, composants |
| 6. Contraintes et Risques | Tableaux |
| 7. Livrables attendus | Format et destination |
| 8. Plan de validation | Criteres, methode, responsables |
| 9. Liens et References | Pense-bete source, conventions |
| 10. RVAV de la spec | Checklist |

## Ce que l'outil fait

1. **Existence** - Verifie que le fichier existe et n'est pas vide
2. **Header** - Verifie les 6 champs (Statut, ID, Class, Cree, Theme, Pense-bete source)
3. **Sections** - Verifie les 10 sections du spec-template
4. **Nommage** - Verifie le pattern du nom de fichier
5. **Placeholders** - Detecte les `[...]` non remplis
6. **ASCII** - Detecte les caracteres non-ASCII (accents, emojis)

## Exemples de sortie

```bash
$ valider-spec.sh spec-pipeline.001.01.ebauche.md

=== Validation de la spec ===
Fichier : spec-pipeline.001.01.ebauche.md

=== Resume ===
[OK] La spec est valide
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Fin de mission spec** | Verification avant de reactiver Cerberus |
| **Apres remplissage** | S'assurer que toutes les sections sont completes |
| **Avant changement de statut** | Verifier que la spec est pret pour `prepare` |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `generateurs-squelette-spec` | Genere le squelette avant le remplissage |
| `creer-remplir-spec` | Remplit les sections avant la validation |
| `valider-pense-bete` | Meme logique pour les pense-betes |
| `valider-todo` | Meme logique pour les todos |
| `changer-statut` | Change le statut apres validation |
