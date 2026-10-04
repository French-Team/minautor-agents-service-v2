---
identite:
  type: spec
  appartient_a: corriger-fins-de-ligne
  commun: true
---
# Spec -- corriger-fins-de-ligne

**Version :** 0.1.1
**Statut :** ebauche
**Chemin :** `agents/tools/corriger/corriger-fins-de-ligne/`

---

## Objectif

Convertir les fins de ligne CRLF vers LF sur un fichier ou un dossier,
pour figer la regle LF (strategie FIGER LF, decision utilisateur 2026-08-09).

---

## Criteres d'acceptation

1. `--version` affiche `corriger-fins-de-ligne 0.1.0` (py et sh identiques)
2. Fichier CRLF -> converti en LF (compteur "Convertes" incremente)
3. Fichier deja LF -> non modifie (compteur "Deja en LF")
4. `--dry-run` : aucun fichier modifie, compteurs identiques a l'execution
5. `--recursive` : sous-dossiers inclus, `__pycache__/` et `*.pyc` exclus
6. Fichier binaire (octet nul) -> ignore (compteur "Binaires")
7. Chemin introuvable -> `[ERREUR]` et code de sortie 2
8. Nommage : le fichier doit commencer par `corriger-` (dossier `corriger/`)
9. ASCII strict sur tous les fichiers de l'outil (py, sh, md, spec)
10. Fins de ligne des fichiers sources : LF (signature de nos outils)

---

## Parite py/sh

Le `.sh` est un wrapper pur (`exec python3 ...`). La parite des sorties est
garantie par construction (pattern detecter-impacts, cartographier-parcours).

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.1 | 2026-08-09 | Robustesse : sequences multi-CR converties en une passe |
| 0.1.0 | 2026-08-09 | Creation |
