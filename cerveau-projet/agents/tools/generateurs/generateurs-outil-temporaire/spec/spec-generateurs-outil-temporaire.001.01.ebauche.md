---
identite:
  type: spec
  appartient_a: commun
  commun: true
---
# Specification -- generateurs-outil-temporaire

**Statut :** ebauche
**Version :** 0.2.3
**Categorie :** generateurs
**Date :** 2026-08-09

---

## Objectif

Fournir un generateur d'**outil temporaire** (script Python jetable) utilisable par TOUS les agents. Quand une mission a besoin d'un script ponctuel (`tmp-*.py`), l'agent ne l'ecrit plus a la main sans standard : il utilise le generateur qui produit un script conforme (en-tete identite `type: outil-temporaire`, ASCII strict, LF, 100% stdlib), cree **DANS le workspace uniquement**, et rappelle la regle de **PROMOTION** : un besoin utilise 2x doit devenir un outil durable cree par Vulcain.

**Principe fondateur** : l'outil temporaire est JETABLE et LOCAL au workspace. Il ne remplace jamais l'outil durable (`tools/`, protocole 5 fichiers, role Vulcain). Le generateur standardise ce qui se faisait deja a la main (.tmp-*.py) pour eviter les derives (incident Atlas : ecriture d'un outil hors perimetre).

## Contexte

- **Regle immuable workspace** : ecriture = workspace seul, jamais hors workspace, meme temporaire.
- **Pattern 12 (CREATION LIMITEE)** : les agents non-Vulcain ne creent JAMAIS d'outil durable ; l'outil temporaire jetable (.tmp-*.py dans le workspace, jamais `tools/`) est autorise a tous via ce generateur.
- **Pattern 13 (LA FIN SUIT SA CARTE)** : la promotion (2e utilisation) = maillon de chaine : l'agent ACTIVE Vulcain, Vulcain REACTIVE l'agent precedent.
- **Lecons repetees** : "script temporaire -> outil durable" (Vulcain 2026-08-07, generateurs-regenerer-catalogue, detecter-divergences-version).

## Fonctionnalites

| # | Fonctionnalite | Detail |
|---|---|---|
| 1 | Generation | `--nom <besoin>` : cree `tmp-<besoin>.py` (prefixe automatique, nom normalise minuscules/tirets) |
| 2 | Description | `--description <texte>` : docstring du script genere |
| 3 | Dry-run par defaut | Sans `--force`, affiche le contenu sans creer de fichier (pattern securite) |
| 4 | Ecriture reelle | `--force` : ecrit le fichier, refuse l'ecrasement si present |
| 5 | Perimetre workspace | Dossier de destination valide DANS le workspace uniquement (refus sinon) |
| 6 | En-tete standard | identite `type: outil-temporaire`, `# -*- coding: ascii -*-`, ASCII strict, LF, 100% stdlib, version `0.1.0-tmp`, date |
| 7 | Question promotion | Affichee a la fin (mode non-bloquant, destinee a l'agent) : besoin recurrent (2e utilisation) ? -> OUI = activer Vulcain |
| 8 | Directive promotion | OUI : activer Vulcain (maillon de chaine), Vulcain cree l'outil durable, Vulcain reactive l'agent precedent |
| 9 | Parite .py/.sh | Meme comportement dans les deux versions (dry-run, workspace, promotion, refus ecrasement) |
| 10 | DECLARATION USAGES (v0.2.1) | Le script genere embarque le bloc DECLARATION : variable `AGENT` + fonctions `declarer_usage()` / `declarer_usages()` qui appellent `enregistrer-usage-outil --mode script-temporaire` pour le script lui-meme et chaque outil utilise (appele en fin de main, erreur si AGENT non renseigne) |
| 11 | CHRONO EN HAUT (v0.2.2) | BUFFER TOTAL (decision utilisateur 2026-08-15) : toute la sortie du script (y compris les sous-processus de declaration captures via `capture_output`) est retenue en memoire, le chrono `=== CHRONO ===` est affiche EN PREMIER puis le contenu - le chrono est TOUJOURS la premiere ligne |
| 12 | REDIRECTION REGISTRE (v0.2.3) | Variable d environnement `CERVEAU_REGISTRE_USAGES` : si definie, `declarer_usage` ajoute `--registre <valeur>` a la commande `enregistrer-usage-outil` (utilisee par les tests pour isoler leurs preuves du registre reel - elimine la course test-050/test-079) |

## Interface

```bash
python3 generateurs-outil-temporaire.py --nom <besoin> [--description <texte>] [--dossier <chemin>] [--force]
bash generateurs-outil-temporaire.sh --nom <besoin> [--description <texte>] [--dossier <chemin>] [--force]
```

## Criteres d'acceptation

| # | Critere |
|---|---|
| 1 | `--nom` obligatoire, normalise (minuscules, tirets), prefixe `tmp-` automatique |
| 2 | Nom invalide (accent, espace, caractere special) = erreur immediate |
| 3 | Sans `--force` : dry-run, aucun fichier cree |
| 4 | Avec `--force` : fichier cree dans le workspace, ASCII strict, LF pur |
| 5 | Dossier hors workspace = erreur (regle workspace) |
| 6 | Fichier existant = erreur (jamais d'ecrasement) |
| 7 | Question promotion affichee dans les deux modes (dry-run et reelle) |
| 8 | Script genere : identite `type: outil-temporaire`, version `0.1.0-tmp`, stdlib, executable |
| 9 | Parite .py/.sh : meme comportement sur les 8 criteres precedents |

## Plan de validation

- Test bout en bout : generation reelle dans `.tmp-*` du workspace puis suppression (0 residu)
- `valider-conformite-ascii` sur le script genere : 0 non-ASCII
- LF pur sur le script genere
- `valider-nommage --type outil` sur le generateur lui-meme

## Liens et References

- Regle immuable : `regles-immuables/general/regles-perimetre-workspace.md`
- Protocole : `regles-immuables/general/protocole-outils/protocole-outils.001.01.ebauche.md`
- Spec : `guider/guider-parcours/spec/spec-guider-parcours.001.01.ebauche.md` (Patterns 12 et 13)
- Template : `tools/outil-template.py`
