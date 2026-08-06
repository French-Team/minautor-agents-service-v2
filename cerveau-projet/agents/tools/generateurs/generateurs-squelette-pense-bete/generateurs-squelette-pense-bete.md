# generateurs-squelette-pense-bete

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** Generateurs
**Chemin :** `agents/tools/generateurs/generateurs-squelette-pense-bete/`

## Description

Genere le squelette d'un pense-bete conforme au `pense-bete-template`. Athena n'a pas besoin de copier le template ni de construire la structure : l'outil cree le fichier avec le bon nommage (`[theme].[id].[class].[statut].md`) et toutes les sections vides pretes a remplir.

## Utilisation

```bash
# Creer un pense-bete avec les valeurs par defaut (id 001, class 01, ebauche)
generateurs-squelette-pense-bete.sh --theme pipeline

# Avec toutes les options
generateurs-squelette-pense-bete.sh --theme pipeline --id 002 --class 02 --dossier cerveau-projet/pense-betes/

# Apercu sans creer le fichier
generateurs-squelette-pense-bete.sh --theme pipeline --dry-run
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--theme <theme>` | Theme du pense-bete (obligatoire, minuscules sans accents) | - |
| `--id <id>` | Identifiant numerique | 001 |
| `--class <class>` | Classe numerique | 01 |
| `--statut <statut>` | Statut | ebauche |
| `--dossier <dossier>` | Dossier de destination | . |
| `--dry-run` | Afficher le squelette sans creer le fichier | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. **Valide** - Le theme (obligatoire, sans accents ni espaces)
2. **Nomme** - Construit le nom du fichier selon la convention `pense-bete-[theme].[id].[class].[statut].md`
3. **Genere** - Le squelette complet avec les 6 sections du template
4. **Protege** - Refuse d'ecraser un fichier existant
5. **Cree** - Le fichier et confirme

## Sections generees

| Section | Contenu |
|---|---|
| Header | Statut, ID, Class, Cree, Theme |
| 1. Idee | Placeholder `[L'essence du concept...]` |
| 2. Probleme / Question | Placeholder |
| 3. Contexte | Placeholder |
| 4. Liens | Structure a completer (connexes, conventions, regles) |
| 5. Structure prevue | Tableau RVAV avec les sous-fichiers cibles |
| 6. RVAV du pense-bete | Checklist a cocher |

## Exemples de sortie

```bash
$ generateurs-squelette-pense-bete.sh --theme pipeline
[OK] Squelette cree : ./pense-bete-pipeline.001.01.ebauche.md
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Creation d'un pense-bete** | Etape 1 de la mission d'Athena |
| **Nouveau theme** | Preparer le fichier avant de le remplir |
| **Dry-run** | Verifier la structure avant creation |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `creer-remplir-pense-bete` | Remplit les sections du squelette |
| `valider-pense-bete` | Verifie le fichier final |
| `changer-statut` | Change le statut quand le pense-bete evolue |

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels, corrections, promotion |
