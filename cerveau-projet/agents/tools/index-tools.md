# Index des Outils Partages

**Version** : v0.1.0
**Statut** : initial
**Protocole** : protocole-outils

---

## Point d'entree

Bienvenue dans la **boite a outils partagee** du cerveau-projet.
---

## Categories d'outils

### Explorer

| Outil | Description | Chemin |
|---|---|---|
| `lister-dossiers` | Lister les dossiers d'un chemin | [explorer/lister-dossiers/](explorer/lister-dossiers/) |
| `lister-fichiers` | Lister les fichiers d'un chemin | [explorer/lister-fichiers/](explorer/lister-fichiers/) |
| `lister-fonctions` | Lister les fonctions d'un fichier | [explorer/lister-fonctions/](explorer/lister-fonctions/) |
| `lister-appels` | Lister les appels de fonctions | [explorer/lister-appels/](explorer/lister-appels/) |
| `lister-agents` | Lister les agents avec leurs infos | [explorer/lister-agents/](explorer/lister-agents/) |
| `lister-outils` | Lister les outils partages | [explorer/lister-outils/](explorer/lister-outils/) |
| `lister-statuts` | Lister les fichiers par statut | [explorer/lister-statuts/](explorer/lister-statuts/) |
| `rechercher-fichiers-vides` | Rechercher les fichiers markdown vides ou quasi vides | [explorer/rechercher-fichiers-vides/](explorer/rechercher-fichiers-vides/) |
| `rechercher-templates` | Rechercher les fichiers template du projet | [explorer/rechercher-templates/](explorer/rechercher-templates/) |
| `rechercher-pense-betes` | Rechercher les pense-betes existants (anti-doublon) | [explorer/rechercher-pense-betes/](explorer/rechercher-pense-betes/) |
| `rechercher-specs` | Rechercher les specs existantes (anti-doublon) | [explorer/rechercher-specs/](explorer/rechercher-specs/) |
| `rechercher-todos` | Rechercher les todos existants (anti-doublon) | [explorer/rechercher-todos/](explorer/rechercher-todos/) |
| `rechercher-accents-sensibles` | Rechercher les accents dans les zones sensibles (frontmatter, noms, blocs, code, liens) | [explorer/rechercher-accents-sensibles/](explorer/rechercher-accents-sensibles/) |

### Valider

| Outil | Description | Chemin |
|---|---|---|
| `valider-liens` | Verifier que les liens sont valides | [valider/valider-liens/](valider/valider-liens/) |
| `valider-nommage` | Verifier que le nommage est correct | [valider/valider-nommage/](valider/valider-nommage/) |
| `valider-conventions` | Verifier que les conventions sont respectees | [valider/valider-conventions/](valider/valider-conventions/) |
| `valider-cartes-decision` | Verifier les cartes de decision des agents | [valider/valider-cartes-decision/](valider/valider-cartes-decision/) |
| `valider-ebauche` | Verifier les exigences minimales d'un ebauche | [valider/valider-ebauche/](valider/valider-ebauche/) |
| `detecter-erreur-statut` | Detecter les fichiers dont le statut ne correspond pas au contenu | [valider/detecter-erreur-statut/](valider/detecter-erreur-statut/) |
| `verifier-role-fichier` | Verifier qu'un fichier est utilise pour sa fonction | [valider/verifier-role-fichier/](valider/verifier-role-fichier/) |
| `verifier-surcharge-fichier` | Detecter les fichiers qui grossissent trop | [valider/verifier-surcharge-fichier/](valider/verifier-surcharge-fichier/) |
| `verifier-separation-preoccupations` | Verifier la separation des preoccupations | [valider/verifier-separation-preoccupations/](valider/verifier-separation-preoccupations/) |
| `valider-conformite-ascii` | Valider la conformite ASCII de tous les fichiers | [valider/valider-conformite-ascii/](valider/valider-conformite-ascii/) |
| `verifier-documents-manquants` | Verifier les .sh sans .md et inversement | [valider/verifier-documents-manquants/](valider/verifier-documents-manquants/) |
| `valider-pense-bete` | Verifier l'integrite d'un pense-bete (structure, sections, ASCII) | [valider/valider-pense-bete/](valider/valider-pense-bete/) |
| `valider-spec` | Verifier l'integrite d'une spec (structure, sections, ASCII) | [valider/valider-spec/](valider/valider-spec/) |
| `valider-todo` | Verifier l'integrite d'un todo (phases 0-9, obligations) | [valider/valider-todo/](valider/valider-todo/) |

### Analyser

| Outil | Description | Chemin |
|---|---|---|
| `analyser-structure` | Analyser la structure du projet | [analyser/analyser-structure/](analyser/analyser-structure/) |
| `analyser-dependances` | Analyser les dependances | [analyser/analyser-dependances/](analyser/analyser-dependances/) |
| `verifier-systeme` | Verifier le systeme utilisateur | [analyser/verifier-systeme/](analyser/verifier-systeme/) |
| `decomposeur` | Decomposer les fichiers markdown | [analyser/decomposeur/](analyser/decomposeur/) |
| `lister-prepares` | Lister les fichiers 'prepare' et verifier les specs | [analyser/lister-prepares/](analyser/lister-prepares/) |

### Creer

| Outil | Description | Chemin |
|---|---|---|
| `remplir-pense-bete` | Creer le contenu des sections d'un pense-bete | [creer/remplir-pense-bete/](creer/remplir-pense-bete/) |
| `remplir-spec` | Creer le contenu des sections d'une spec | [creer/remplir-spec/](creer/remplir-spec/) |
| `remplir-todo` | Creer le contenu des phases d'un todo | [creer/remplir-todo/](creer/remplir-todo/) |

### Generateurs

| Outil | Description | Chemin |
|---|---|---|
| `squelette-pense-bete` | Generer le squelette d'un pense-bete conforme au template | [generateurs/squelette-pense-bete/](generateurs/squelette-pense-bete/) |
| `squelette-spec` | Generer le squelette d'une spec conforme au spec-template | [generateurs/squelette-spec/](generateurs/squelette-spec/) |
| `squelette-todo` | Generer le squelette d'un todo conforme au todo-template | [generateurs/squelette-todo/](generateurs/squelette-todo/) |

### Corriger

| Outil | Description | Chemin |
|---|---|---|
| `corriger-liens` | Corriger les liens casses | [corriger/corriger-liens/](corriger/corriger-liens/) |
| `corriger-nommage` | Corriger le nommage | [corriger/corriger-nommage/](corriger/corriger-nommage/) |
| `modifier-agents-md` | Modifier AGENTS.md de maniere fiable | [corriger/modifier-agents-md/](corriger/modifier-agents-md/) |
| `gerer-sous-mission` | Gerer les sorties/reentrees du flux principal | [corriger/gerer-sous-mission/](corriger/gerer-sous-mission/) |
| `purifier-fichier` | Purifier un fichier en supprimant le contenu non essentiel | [corriger/purifier-fichier/](corriger/purifier-fichier/) |
| `condenseur` | Condenser les fichiers markdown | [corriger/condenseur/](corriger/condenseur/) |
| `changer-statut` | Changer le statut d'un fichier en le renommant | [corriger/changer-statut/](corriger/changer-statut/) |
| `corriger-emojis` | Detecter et remplacer les emojis par des symboles ASCII | [corriger/corriger-emojis/](corriger/corriger-emojis/) |
| `corriger-accents` | Detecter et corriger les accents et caracteres non-ASCII | [corriger/corriger-accents/](corriger/corriger-accents/) |
| `mettre-a-jour-readme` | Mettre a jour le README depuis les sources de verite (agents, outils, chronologie) | [corriger/mettre-a-jour-readme/](corriger/mettre-a-jour-readme/) |

---

## Comment utiliser un outil

### Via le script bash

```bash
# 1. Chercher dans cet index -> trouver l'outil
# 2. Lire la documentation de l'outil
# 3. Executer le script
./[categorie]/[outil]/[outil].sh [OPTIONS]
# 4. Verifier le resultat
```

### Exemples

```bash
# Verifier le systeme
cerveau-projet/agents/tools/analyser/verifier-systeme/verifier-systeme.sh

# Lister les dossiers
cerveau-projet/agents/tools/explorer/lister-dossiers/lister-dossiers.sh

# Valider les liens
cerveau-projet/agents/tools/valider/valider-liens/valider-liens.sh fichier.md

# Valider un fichier ebauche
cerveau-projet/agents/tools/valider/valider-ebauche/valider-ebauche.sh fichier.md

# Detecter les erreurs de statut
cerveau-projet/agents/tools/valider/detecter-erreur-statut/detecter-erreur-statut.sh

# Changer le statut d'un fichier
cerveau-projet/agents/tools/corriger/changer-statut/changer-statut.sh fichier.md prepare

# Corriger les emojis
cerveau-projet/agents/tools/corriger/corriger-emojis/corriger-emojis.sh fichier.md

# Corriger les accents et caracteres non-ASCII
cerveau-projet/agents/tools/corriger/corriger-accents/corriger-accents.sh fichier.md

# Lister les fichiers 'prepare'
cerveau-projet/agents/tools/analyser/lister-prepares/lister-prepares.sh
```

---

## Comment creer un outil

```
1. Identifier le besoin (commande frequente)
2. Creer le dossier agents/tools/[categorie]/[nom-outil]/
3. Creer le fichier [nom-outil].md
4. Documenter l'outil
5. Tester l'outil
6. Ajouter dans cet index
```

---

### Tests

| Outil | Description | Chemin |
|---|---|---|
| `protection-boucles-infinies` | Protection contre les boucles infinies | [tests/protections/](protections/) |
| `protection-erreurs-silencieuses` | Protection contre les erreurs silencieuses | [tests/protections/](protections/) |
| `protection-blocage` | Protection contre les tests qui bloquent | [tests/protections/](protections/) |
| `template-test` | Template pour creer des tests | [tests/template-test.md](template-test.md) |

### Templates

| Template | Description | Chemin |
|---|---|---|
| `outil-template` | Modele standard de creation d'outils (script + doc) | [outil-template/](outil-template/) |

---

## Comment utiliser le outil-template

1. Copier le dossier `outil-template/` vers `agents/tools/[categorie]/[nom-outil]/`
2. Renommer les fichiers avec le nom reel de l'outil
3. Remplacer les marqueurs `[nom-outil]` dans les deux fichiers
4. Completer la logique du script et la documentation
5. Ajouter l'outil dans cet index
6. Tester en `--dry-run` avant toute utilisation

---

## Statistiques

| Categorie | Nombre d'outils |
|---|---|
| Explorer | 13 |
| Valider | 14 |
| Analyser | 5 |
| Corriger | 10 |
| Creer | 3 |
| Generateurs | 3 |
| Tests | 4 |
| Templates | 1 |
| **Total** | **53** |

---
