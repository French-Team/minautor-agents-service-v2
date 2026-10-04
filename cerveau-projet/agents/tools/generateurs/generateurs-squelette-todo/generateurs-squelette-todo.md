---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# generateurs-squelette-todo

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** Generateurs
**Chemin :** `agents/tools/generateurs/generateurs-squelette-todo/`

## Description

Genere le squelette d'un todo conforme au `todo-template` et a la `convention-renommage`. Le fichier est nomme `todo-[theme].[id].[class].[statut].md` et place dans le dossier `spec/todo/` (cree automatiquement si absent). Le squelette integre les 10 phases du template, dont la **Phase 0 (activation de l'agent)** et la **Phase 9 (reactivation de Cerberus)** qui sont obligatoires.

## Utilisation

```bash
# Creer un todo avec les valeurs par defaut
generateurs-squelette-todo.sh --theme pipeline

# Version Python (recommandee)
python3 generateurs-squelette-todo.py --theme pipeline

# Avec toutes les options
generateurs-squelette-todo.sh --theme pipeline --id 001 --class 01 --dossier spec/todo/

# Apercu sans creer le fichier
generateurs-squelette-todo.sh --theme pipeline --dry-run
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--theme <theme>` | Theme du todo (obligatoire, minuscules sans accents) | - |
| `--id <id>` | Identifiant numerique | 001 |
| `--class <class>` | Classe numerique | 01 |
| `--statut <statut>` | Statut | ebauche |
| `--dossier <dossier>` | Dossier de destination | spec/todo |
| `--dry-run` | Afficher le squelette sans creer le fichier | false |
| `--help` | Afficher l'aide | - |

## Phases generees

| Phase | Contenu |
|---|---|
| **Phase 0** | **Activation de l'agent** (OBLIGATOIRE, premiere action) |
| Header | Frontmatter YAML de la mission |
| Statut | Tableau pense-bete / spec / todo |
| Phase 1 | Analyse de la demande |
| Phase 2 | Verification du cerveau |
| Phase 3 | Recherches |
| Phase 4 | Preparation des outils |
| Phase 5 | Developpement |
| Phase 6 | Tests et validation |
| Phase 7 | Controle secondaire |
| Phase 8 | Finalisation |
| **Phase 9** | **Reactivation de Cerberus** (OBLIGATOIRE, derniere action) |
| Historique | Tableau des etapes |
| Notes + Liens | Sections de fermeture |

## Ce que l'outil fait

1. **Valide** - Le theme (obligatoire, sans accents ni espaces)
2. **Nomme** - `todo-[theme].[id].[class].[statut].md` selon la convention-renommage
3. **Genere** - Les 10 phases du todo-template (0 a 9)
4. **Protege** - Refuse d'ecraser un fichier existant
5. **Cree** - Le dossier `spec/todo/` et le fichier

## Exemples de sortie

```bash
$ generateurs-squelette-todo.sh --theme pipeline
[OK] Squelette cree : spec/todo/todo-pipeline.001.01.ebauche.md
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Passage spec -> todo** | Quand la spec est prete |
| **Creation d'un todo** | Generer la structure avant de la remplir |
| **Dry-run** | Verifier la structure avant creation |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `squelette-pense-bete` | Genere le pense-bete parent |
| `squelette-spec` | Genere la spec parente |
| `creer-remplir-pense-bete` | Modele pour creer un outil de remplissage equivalent |
| `changer-statut` | Change le statut quand le todo evolue |

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels, corrections, promotion |
| 0.2.0-py | 2026-08-07 | Version Python creee (10 phases, dossier cree, --version) |
