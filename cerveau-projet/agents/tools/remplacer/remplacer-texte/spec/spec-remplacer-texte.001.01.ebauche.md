---
identite:
  type: spec
  appartient_a: commun
  commun: true
---
# Specification -- remplacer-texte

**Statut :** ebauche
**Version :** 0.1.0-beta
**Categorie :** remplacer
**Date :** 2026-08-07

---

## Objectif

Fournir un outil permanent de remplacement massif de textes dans plusieurs fichiers d'un dossier (recursif), pour les renommages globaux sans re-ecrire un script temporaire a chaque fois.

## Fonctionnalites

| # | Fonctionnalite | Detail |
|---|---|---|
| 1 | Dossier racine | Premier argument : dossier a parcourir recursivement |
| 2 | Paires ancien -> nouveau | Liste de paires `ancien=nouveau` (une ou plusieurs) |
| 3 | Ordre des paires | Appliquees dans l'ordre donne (chaines longues d'abord pour eviter les collisions) |
| 4 | Extensions | Filtre par extension (defaut : md, sh, py ; configurable via `--ext`) |
| 5 | Exclusions fichiers | `--exclu-fichier` (defaut : AGENTS-historique.md) |
| 6 | Exclusions dossiers | `--exclu-dossier` (defaut : exemples, .git, __pycache__) |
| 7 | Dry-run | `--dry-run` : affiche les fichiers qui SERAIENT modifies sans rien ecrire |
| 8 | Rapport | Nombre de fichiers analyses, modifies, liste des fichiers modifies |
| 9 | Idempotence | Re-executer ne casse rien (le nouveau texte ne contient plus l'ancien) |

## Interface

```bash
remplacer-texte.sh <dossier> 'ancien=nouveau' ['ancien2=nouveau2' ...] [OPTIONS]
remplacer-texte.py <dossier> 'ancien=nouveau' ['ancien2=nouveau2' ...] [OPTIONS]
```

Options : `--dry-run`, `--ext`, `--exclu-fichier`, `--exclu-dossier`, `--verbose`, `--help`, `--version` (py)

## Tests requis

| Cas | Attendu |
|---|---|
| Nominal | Les paires sont remplacees dans les fichiers cibles |
| Dry-run | Aucun fichier modifie, les cibles sont affichees |
| Exclusions | AGENTS-historique.md et exemples/ intacts |
| Idempotence | 2e execution sans changement |
| Nommage | valider-nommage OK (dossier remplacer/ -> prefixe remplacer-) |
| ASCII | 0 caractere non-ASCII |
| Syntaxe | bash -n OK, python3 -m py_compile OK |

## Livrables

- `remplacer-texte.sh` (bash)
- `remplacer-texte.py` (python)
- `remplacer-texte.md` (documentation)
- `spec/spec-remplacer-texte.001.01.ebauche.md` (ce fichier)
