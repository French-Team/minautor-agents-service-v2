---
identite:
  type: outil
  appartient_a: commun
  commun: true
  tags: verification, restauration, git, securite
---
# verifier-restauration-sure

**Version :** 0.1.0
**Statut :** prepare
**Categorie :** verifier
**Chemin :** `agents/tools/verifier/verifier-restauration-sure/`
**Proprietaire :** Vulcain (outil partage)

## Description

Detecte les fichiers non commites avant toute restauration git (git status
automatique). Il applique la regle **Restauration securisee** (regle immuable
documentee dans `regles-general-global.md` et `protocole-gestion-defaillances`
Etape 3) : **JAMAIS de `git checkout` / `git restore` / `git reset --hard` sur
des fichiers NON COMMITES** -- cela ecrase le travail en cours.

L'outil est a lancer AVANT toute restauration git pour verifier qu'aucune
modification non commitee ne serait perdue.

## REGLE IMMUABLE : prefixe du dossier

> Le nom de l'outil DOIT commencer par le prefixe du dossier de categorie.
> Dossier `verifier/` -> nom attendu `verifier-xxx`. C'est une regle immuable.

| Dossier | Nom attendu |
|---|---|
| `verifier/` | `verifier-restauration-sure` |

## Utilisation

```bash
# Mode global : liste tous les fichiers non commites du workspace et rend un verdict
verifier-restauration-sure.sh

# Mode fichier : verifie si LE fichier cible a des modifications non commitees
verifier-restauration-sure.sh --fichier cerveau-projet/agents/buffy/corrections.md

# Aide et version
verifier-restauration-sure.sh --aide
verifier-restauration-sure.sh --version
```

## Codes de retour

| Code | Signification |
|---|---|
| 0 | AUCUN fichier non commite (mode global) OU le fichier cible est sur (mode fichier) -- restauration git sure |
| 1 | Des fichiers non commites existent (mode global) OU le fichier cible a des modifications non commitees (mode fichier) -- restauration git INTERDITE |
| 2 | Erreur d'utilisation (fichier hors workspace, nommage invalide) |
| 3 | Erreur d'execution git (git status a echoue) |

## Exemples

```bash
# Avant une restauration, verifier qu'aucun fichier non commite ne serait perdu
verifier-restauration-sure.sh
# => [OK] AUCUN fichier non commite - la restauration git est sure.

# Verifier un fichier precis avant de le restaurer
verifier-restauration-sure.sh --fichier cerveau-projet/agents/buffy/corrections.md
# => [OK] Le fichier '...' est SUR (aucune modification non commitee).
# ou => [ATTENTION] Le fichier '...' a des modifications NON COMMITEES :
#      [ M] cerveau-projet/agents/buffy/corrections.md
#      REGLE RESTAURATION SECURISEE : JAMAIS de git checkout / git restore /
#      git reset --hard si des fichiers non commites existent. Verifier git status
#      avant, sauvegarder (cp) ou git stash.
```

## Rappel de la regle

> **REGLE RESTAURATION SECURISEE** : JAMAIS de `git checkout` / `git restore` /
> `git reset --hard` si des fichiers non commites existent. Verifier `git status`
> avant, sauvegarder (cp) ou `git stash`.

## Dependances

- `git` (disponible dans l'environnement, verifie par `verifier-systeme`)
- Python 3 (stdlib uniquement)

## Versionning

- 0.1.0 : creation -- modes global et --fichier, git status --porcelain automatique, rappel de la regle Restauration securisee.
