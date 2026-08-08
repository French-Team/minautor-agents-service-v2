---
identite:
  type: spec
  appartient_a: commun
  commun: true
---
# SPEC - migrer-identite v0.2.2 (ebauche)

| Champ | Valeur |
|---|---|
| **Nom** | migrer-identite |
| **Version** | 0.2.2 |
| **Statut** | ebauche |
| **Categorie** | Migrer |
| **Proprietaire** | outil partage (Vulcain) |
| **Spec parente** | detecter-impacts (schema hybride v0.2.0) |

## Objectif

Migrer les fichiers du cerveau vers le **schema hybride v0.2.0** de
detecter-impacts : ajouter le bloc identite (`type` / `appartient_a` /
`commun`) dans chaque fichier, dans le format adapte a son type
(.md frontmatter, .py/.sh commentaires, .json cle top-level).

## Contexte

- Le cerveau grandit : l'identification doit vivre DANS chaque fichier.
- ~300 fichiers dans `agents/tools/` a migrer (decision utilisateur :
  vague 2, tous declares `commun: true`).
- La migration manuelle est impossible et source d'erreurs repetitives.
- L'outil doit etre **idempotent** (un fichier deja migre est saute) et
  **sur** (mode `--dry-run` pour previsualiser avant d'ecrire).

## Regles de l'outil

### R1. Formats supports

| Type | Format identite |
|---|---|
| `.md` | Frontmatter YAML `---` / `identite:` / `---` en tete |
| `.py` / `.sh` | Commentaires `# identite:` dans les 12 premieres lignes |
| `.json` | Cle top-level `"identite": {...}` |

### R2. Attribution des types (v0.2.0 : extension a tout le cerveau)

| Situation | Type | Appartient_a |
|---|---|---|
| Sous-dossier `spec/` | `spec` | defaut (commun) |
| `combos/<combo>/definition-combo.json` | `combo` | defaut (commun) |
| Nom `combos-*` (outils du dossier combos/) | `outil` | defaut (commun) |
| Nom `tester-*` (fichiers de test) | `test` | defaut (commun) |
| `catalogue-commandes.json` | `outil` | defaut (commun) |
| `exemple-combo.json` | `combo` | defaut (commun) |
| Nom `AGENTS.md` (racine) | `racine` | commun |
| Nom `AGENTS-historique.md` (journal) | `historique` | commun |
| Dossier `classeur-variables/` | `classeur` | commun |
| Dossier `pense-betes/` | `pense-bete` | commun |
| Nom contenant `-template` | `template` | commun |
| `.md` hors `agents/tools/` | `note` | dossier parent (ex: vulcain) |
| Defaut | `outil` | defaut (commun) |

Regle : un `.md` vivant dans `agents/tools/` reste un `outil` ; les
`outil-template.*` et `template-test.md` restent `outil` (exclus).

### R3. Exclusions (perimetre decision utilisateur)

- **Traces historisees (v0.2.0)** : dossiers `controles/`, `rapports/`,
  `retro-actions/` (rapports dates figes, jamais a jour)
- **Hors perimetre (v0.2.1)** : `exemples/` (test pollue),
  `recherches-web/` (recherches), `sauvegardes/` (artefacts)
- `outil-template.py`, `outil-template.sh`, `outil-template.md`
- `template-test.md` (template de test)
- Fichiers `.sh` ET `.md` dans un dossier `tests/`
- `__pycache__`

### R3b. Protection frontmatter sans identite

Un `.md` commencant par un frontmatter `---` qui ne contient PAS
`identite:` est un fichier special : il est **ignore** (message
`[IGNORE] ... frontmatter-sans-identite`), jamais modifie, aucun double
frontmatter possible.

### R4. Options

| Option | Defaut | Effet |
|---|---|---|
| `--racine` | `agents/tools/` | Dossier a migrer |
| `--dry-run` | false | Afficher sans ecrire |
| `--liste` | false | Lister les fichiers a migrer |
| `--appartient-a` | `commun` | Valeur appartient_a |
| `--commun` | `true` | Valeur commun |
| `--force` | false | Reinserer meme si present |

### R5. Garanties

- Idempotence : second passage -> tout DEJA, aucun changement.
- ASCII strict : un contenu genere non-ASCII est rejete (erreur).
- `--dry-run` et `--liste` n'ecrivent jamais.
- 100% stdlib Python.
- Parite stricte py/sh (code identique embarque dans le .sh).

### R6. Rapport de sortie

```
=== RAPPORT (REEL) ===
  Migres:        N
  Deja presents:N
  Ignores:      N
  Erreurs:      N
  Total:        N
```

Code de retour : 0 si aucune erreur, 1 sinon.

## Critere d'acceptation

| # | Critere |
|---|---|
| 1 | `--liste` liste les fichiers cibles avec leur type (exclusions respectees) |
| 2 | `--dry-run` n'ecrit AUCUN fichier |
| 3 | Migration reelle : bloc identite correct pour .py/.sh/.md/.json |
| 4 | Idempotence : second passage -> 0 migre, tout DEJA |
| 5 | Parite py/sh : sorties identiques |
| 6 | ASCII strict sur tout le contenu genere |
| 7 | Bloc .py/.sh dans les 12 premieres lignes |
| 8 | Tests et templates jamais modifies |
| 9 | Frontmatter existant sans identite -> IGNORE, jamais de double frontmatter |
| 10 | Bloc .py/.sh toujours dans les 12 premieres lignes (meme avec long en-tete ou commentaires sans ligne vide) |
| 11 | Bloc present hors fenetre 12 -> REPARER (deplace sans doublon) |
| 12 | Insertion apres la ligne # Statut (ou # Version), fallback 1re ligne vide |

## Historique

| Version | Date | Changements |
|---|---|---|
| 0.2.2 | 2026-08-08 | CORRECTION REGLE (decision utilisateur) : regle v0.2.1 trop large (combos- OU dossier combos/) typait a tort les outils combos-moteur/audit/corriger/valider en combo -> definition-combo.json = combo uniquement, combos-* = outil, NOUVEAU type test pour tester-* (priorite haute) |
| 0.2.1 | 2026-08-08 | Corrections dry-run reel : type combo par dossier combos/ ; exclusions exemples/, recherches-web/, sauvegardes/ |
| 0.2.0 | 2026-08-08 | EXTENSION VAGUE 3 : migration sur tout le cerveau - types racine/classeur/pense-bete/template/note (appartient_a dynamique) ; exclusions traces historisees (controles/, rapports/, retro-actions/) ; compatibilite retrograde agents/tools/ |
| 0.1.0 | 2026-08-08 | Creation (vague 2 : migration schema hybride v0.2.0) |
| 0.1.1 | 2026-08-08 | Correction bug _a_identite_md (frontmatter sans identite marque DEJA a tort) ; protection R3b ; exclusion elargie |
| 0.1.2 | 2026-08-08 | Correction bug _migrer_py_sh (bloc hors fenetre 12 pour long en-tete) ; mode REPARER ; jamais de doublon |
| 0.1.3 | 2026-08-08 | Correction bug residuel (commentaires sans ligne vide) : insertion apres # Statut / # Version |
