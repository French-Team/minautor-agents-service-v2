# valider-todo

**Version :** 0.1.0-beta
**Statut :** ebauche
**Categorie :** Valider
**Chemin :** `agents/tools/valider/valider-todo/`

## Description

Verifie l'integrite d'un todo : presence des 10 phases (dont la **Phase 0 — Activation de l'agent** et la **Phase 9 — Reactivation de Cerberus** qui sont OBLIGATOIRES), nommage, placeholders et conformite ASCII. L'agent l'utilise pour s'assurer que le todo respecte le cycle complet avant de le considerer termine.

## Utilisation

```bash
# Valider un todo
valider-todo.sh todo-pipeline.001.01.ebauche.md

# Avec details de chaque verification
valider-todo.sh --verbose todo-pipeline.001.01.ebauche.md
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
| 2 | **Phase 0** | Activation de l'agent (OBLIGATOIRE) |
| 3 | **Phases 1-8** | Presentes (attention si manquantes) |
| 4 | **Phase 9** | Reactivation de Cerberus (OBLIGATOIRE) |
| 5 | **Nommage** | `todo-[theme].[id].[class].[statut].md` |
| 6 | **Placeholders** | Aucun `[...]` non rempli (attention, non bloquant) |
| 7 | **ASCII** | Aucun accent, aucun emoji |

## Le cycle valide

```
Phase 0 — Activation de l'agent   <- OBLIGATOIRE (premiere action)
Phase 1 — Analyse de la demande
Phase 2 — Verification du cerveau
Phase 3 — Recherches
Phase 4 — Preparation des outils
Phase 5 — Developpement
Phase 6 — Tests et validation
Phase 7 — Controle secondaire
Phase 8 — Finalisation
Phase 9 — Reactivation de Cerberus <- OBLIGATOIRE (derniere action)
```

## Ce que l'outil fait

1. **Existence** - Verifie que le fichier existe et n'est pas vide
2. **Phases** - Verifie les 10 phases du todo-template (0 a 9)
3. **Obligations** - Phase 0 et Phase 9 sont des erreurs si absentes
4. **Nommage** - Verifie le pattern du nom de fichier
5. **Placeholders** - Detecte les `[...]` non remplis
6. **ASCII** - Detecte les caracteres non-ASCII (accents, emojis)

## Exemples de sortie

```bash
$ valider-todo.sh todo-pipeline.001.01.ebauche.md

=== Validation du todo ===
Fichier : todo-pipeline.001.01.ebauche.md

=== Resume ===
[OK] Le todo est valide
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Fin de mission todo** | Verification avant de reactiver Cerberus |
| **Avant finalisation** | S'assurer que le cycle est complet (0 -> 9) |
| **Controle de qualite** | Verifier qu'aucune phase obligatoire n'est absente |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `squelette-todo` | Genere le squelette avant le remplissage |
| `remplir-todo` | Remplit les phases avant la validation |
| `valider-pense-bete` | Meme logique pour les pense-betes |
| `valider-spec` | Meme logique pour les specs |
| `changer-statut` | Change le statut apres validation |
