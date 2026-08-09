---
identite:
  type: spec
  appartient_a: commun
  commun: true
---
# Specification -- verifier-restauration-sure

**Statut :** prepare
**ID :** 001
**Class :** 01
**Cree :** 2026-08-08
**Theme :** verifier-restauration-sure
**Pense-bete source :** Spec directe (pas de pense-bete parent)

---

## 1. Objectif

Detecter les fichiers non commites avant toute restauration git (git status
automatique) et appliquer la regle **Restauration securisee** : JAMAIS de
`git checkout` / `git restore` / `git reset --hard` sur des fichiers NON
COMMITES (perte de travail definie).

---

## 2. Contexte

### 2.1 Origine

L'incident piste B : un `git checkout` de restauration a ecrase les modifications
NON COMMITEES de la piste B (11 indices PASSE PAR LE GENERATEUR perdus puis
repares). Lecon : ne JAMAIS restaurer par git des fichiers non commites. La regle
a ete inscrite dans `regles-general-global.md` (tableau des regles globales) et
`protocole-gestion-defaillances` (Etape 3 -- Regle de restauration). Il manquait
un OUTIL pour appliquer cette regle automatiquement : `verifier-restauration-sure`.

### 2.2 Perimetre

- Mode global : liste tous les fichiers non commites du workspace et rend un verdict.
- Mode `--fichier <chemin>` : verifie si le fichier cible a des modifications non commitees.
- Rappel de la regle Restauration securisee dans les messages d'attention.

### 2.3 Hors perimetre

- Ne PAS executer de restauration : l'outil VERIFIE uniquement.
- Ne PAS modifier les fichiers : lecture seule de git status.
- Ne PAS couvrir les branches non fusionnees ni les stashes (git status --porcelain).

---

## 3. Fonctionnalites

### 3.1 Detection automatique de la racine du workspace

L'outil remonte depuis le repertoire courant jusqu'au premier parent contenant
`.git` (fichier ou dossier). C'est la racine du workspace.

### 3.2 Mode global (defaut)

1. Execute `git status --porcelain` depuis la racine du workspace.
2. Analyse chaque ligne : code (2 caracteres) + chemin.
3. Verdict :
   - 0 fichier non commite -> `[OK] AUCUN fichier non commite - la restauration git est sure.` (code 0)
   - N fichiers non commites -> `[ATTENTION] N fichier(s) non commite(s) - restauration git INTERDITE.` + liste + rappel de la regle (code 1)

### 3.3 Mode --fichier

1. Normalise le chemin cible en relatif au workspace.
2. Compare au chemin des fichiers non commites.
3. Verdict :
   - non touche -> `[OK] Le fichier '...' est SUR (aucune modification non commitee).` (code 0)
   - touche -> `[ATTENTION] Le fichier '...' a des modifications NON COMMITEES :` + codes + rappel de la regle (code 1)

### 3.4 Codes de retour

| Code | Signification |
|---|---|
| 0 | Aucun fichier non commite (global) / fichier sur (mode fichier) |
| 1 | Fichiers non commites detectes -- restauration git interdite |
| 2 | Erreur d'utilisation (fichier hors workspace, nommage invalide) |
| 3 | Erreur d'execution git (git status a echoue) |

---

## 4. Contraintes techniques

- Python 3 stdlib uniquement (subprocess, pathlib, argparse).
- ASCII strict (aucun accent, emoji ou caractere Unicode).
- Compatibilite Git Bash : wrapper `.sh` qui appelle le `.py` (parite).
- `verifier_nommage` au demarrage : nom doit commencer par `verifier-` (dossier).

---

## 5. Validation

- `python3 -m py_compile` sur le `.py`.
- `bash -n` sur le `.sh`.
- `valider-nommage --type outil` sur les 3 fichiers (.py/.sh/.md).
- `valider-conformite-ascii` sur tous les fichiers.
- Tests fonctionnels : mode global sur le workspace (contient des modifs non commitees),
  mode --fichier sur un fichier modifie (code 1) et sur un fichier sur (code 0),
  fichier hors workspace (erreur 2), --version, --aide.
- Parite py/sh : memes sorties avec .py et .sh.

---

## 6. Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-08 | Creation : modes global et --fichier, git status --porcelain, rappel regle Restauration securisee |
