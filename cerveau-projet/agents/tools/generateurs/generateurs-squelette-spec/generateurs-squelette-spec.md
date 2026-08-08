---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# generateurs-squelette-spec

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** Generateurs
**Chemin :** `agents/tools/generateurs/generateurs-squelette-spec/`

## Description

Genere le squelette d'une specification technique conforme au `spec-template` et a la `convention-renommage`. Le fichier est nomme `spec-[theme].[id].[class].[statut].md` et place dans le dossier `spec/` (cree automatiquement si absent).

## Utilisation

```bash
# Creer une spec avec les valeurs par defaut
generateurs-squelette-spec.sh --theme pipeline

# Version Python (recommandee)
python3 generateurs-squelette-spec.py --theme pipeline

# Avec toutes les options
generateurs-squelette-spec.sh --theme pipeline --id 001 --class 01 --dossier spec/ --parent pense-bete-pipeline.001.01.ebauche.md

# Apercu sans creer le fichier
generateurs-squelette-spec.sh --theme pipeline --dry-run
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--theme <theme>` | Theme de la spec (obligatoire, minuscules sans accents) | - |
| `--id <id>` | Identifiant numerique | 001 |
| `--class <class>` | Classe numerique | 01 |
| `--statut <statut>` | Statut | ebauche |
| `--dossier <dossier>` | Dossier de destination | spec |
| `--parent <lien>` | Lien vers le pense-bete source | vide |
| `--dry-run` | Afficher le squelette sans creer le fichier | false |
| `--help` | Afficher l'aide | - |

## Sections generees

| Section | Contenu |
|---|---|
| Header | Statut, ID, Class, Cree, Theme, Pense-bete source |
| 1. Objectif | Objectif precis de la spec |
| 2. Contexte | Origine, perimetre, public cible |
| 3. Exigences Fonctionnelles | Tableau par exigence (priorite, description, acceptation) |
| 4. Exigences Non-Fonctionnelles | Performance, securite, maintenabilite, accessibilite |
| 5. Architecture | Vue d'ensemble, composants, modele, interfaces, flux |
| 6. Contraintes et Risques | Tableaux contraintes + risques |
| 7. Livrables attendus | Format et destination |
| 8. Plan de validation | Criteres, methode, responsables |
| 9. Liens et References | Pense-bete source, specs connexes, conventions |
| 10. RVAV | Checklist Rechercher-Verifier-Analyser-Valider |
| Historique | Tableau des modifications |

## Ce que l'outil fait

1. **Valide** - Le theme (obligatoire, sans accents ni espaces)
2. **Nomme** - `spec-[theme].[id].[class].[statut].md` selon la convention-renommage
3. **Genere** - Les 11 sections du spec-template
4. **Protege** - Refuse d'ecraser un fichier existant
5. **Cree** - Le dossier `spec/` et le fichier

## Exemples de sortie

```bash
$ generateurs-squelette-spec.sh --theme pipeline --parent pense-bete-pipeline.001.01.ebauche.md
[OK] Squelette cree : spec/spec-pipeline.001.01.ebauche.md
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Passage pense-bete -> spec** | Quand le pense-bete est pret (prepare) |
| **Creation d'une spec** | Generer la structure avant de la remplir |
| **Dry-run** | Verifier la structure avant creation |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `squelette-pense-bete` | Genere le pense-bete parent |
| `squelette-todo` | Genere le todo associe (dans spec/todo/) |
| `creer-remplir-pense-bete` | Modele pour creer un outil de remplissage equivalent |
| `changer-statut` | Change le statut quand la spec evolue |

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels, corrections, promotion |
| 0.2.0-py | 2026-08-07 | Version Python creee (meme logique, --parent integre, --version) |
