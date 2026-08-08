# Index des Outils Partages

**Version** : v0.2.0
**Statut** : reorganise
**Protocole** : protocole-outils

---

## Point d'entree

Bienvenue dans la **boite a outils partagee** du cerveau-projet.
Les outils sont organises par **CATEGORIE** (le dossier = ce que fait l'outil : ajouter, analyser, corriger, lister, ...), chaque outil porte le nom de son action.

---

## Categories d'outils (par action)

### Ajouter

| Outil | Description | Chemin |
|---|---|---|
| `ajouter-contenu-fichier` | Ajouter du contenu a la fin d'un fichier (append) | [ajouter/ajouter-contenu-fichier/](ajouter/ajouter-contenu-fichier/) |

### Activer

| Outil | Description | Chemin |
|---|---|---|
| `activer-agent-principal` | Activer/reactiver l agent principal dans AGENTS.md | [activer/activer-agent-principal/](activer/activer-agent-principal/) |

### Analyser

| Outil | Description | Chemin |
|---|---|---|
| `analyser-dependances` | Analyser les dependances | [analyser/analyser-dependances/](analyser/analyser-dependances/) |
| `analyser-structure` | Analyser la structure du projet | [analyser/analyser-structure/](analyser/analyser-structure/) |

### Changer

| Outil | Description | Chemin |
|---|---|---|
| `changer-statut` | Changer le statut d'un fichier en le renommant | [changer/changer-statut/](changer/changer-statut/) |

### Combos

| Combo | Description | Chemin |
|---|---|---|
| `combos-audit-general` | Chainage des 4 evaluateurs + synthese | [combos/combos-audit-general/](combos/combos-audit-general/) |
| `combos-corriger-non-ascii` | Chainer rechercher-accents-sensibles + corriger-emojis + corriger-accents-zones-sensibles | [combos/combos-corriger-non-ascii/](combos/combos-corriger-non-ascii/) |
| `combos-valider-cerveau` | Etat de sante du cerveau : relecture + cartes + ASCII en 1 rapport | [combos/combos-valider-cerveau/](combos/combos-valider-cerveau/) |
| `combos-moteur` | Moteur generique de combos declaratifs : execute une definition-combo.json case par case (generateur/outil/controle/fin), variables + interpolation | [combos/combos-moteur/](combos/combos-moteur/) |

### Condenser

| Outil | Description | Chemin |
|---|---|---|
| `condenser-fichier` | Condenser les fichiers markdown | [condenser/condenser-fichier/](condenser/condenser-fichier/) |

### Copier

| Outil | Description | Chemin |
|---|---|---|
| `copier-dossier` | Copier un dossier recursivement | [copier/copier-dossier/](copier/copier-dossier/) |
| `copier-fichier` | Copier un fichier vers une destination | [copier/copier-fichier/](copier/copier-fichier/) |

### Corriger

| Outil | Description | Chemin |
|---|---|---|
| `corriger-dictionnaire-accents` | Dictionnaire accent -> ASCII (source de donnees pour corriger-accents-zones-sensibles) | [corriger/corriger-dictionnaire-accents/](corriger/corriger-dictionnaire-accents/) |
| `corriger-accents-zones-sensibles` | Corriger les accents (mode --all : purge totale, regle immuable) | [corriger/corriger-accents-zones-sensibles/](corriger/corriger-accents-zones-sensibles/) |
| `corriger-emojis` | Detecter et remplacer les emojis par des symboles ASCII | [corriger/corriger-emojis/](corriger/corriger-emojis/) |
| `corriger-liens` | Corriger les liens casses | [corriger/corriger-liens/](corriger/corriger-liens/) |
| `corriger-nommage` | Corriger le nommage | [corriger/corriger-nommage/](corriger/corriger-nommage/) |

### Creer

| Outil | Description | Chemin |
|---|---|---|
| `creer-fichier` | Creer un nouveau fichier avec verification | [creer/creer-fichier/](creer/creer-fichier/) |
| `creer-remplir-pense-bete` | Creer le contenu des sections d'un pense-bete | [creer/creer-remplir-pense-bete/](creer/creer-remplir-pense-bete/) |
| `creer-remplir-spec` | Creer le contenu des sections d'une spec | [creer/creer-remplir-spec/](creer/creer-remplir-spec/) |
| `creer-remplir-todo` | Creer le contenu des phases d'un todo | [creer/creer-remplir-todo/](creer/creer-remplir-todo/) |

### Decomposer

| Outil | Description | Chemin |
|---|---|---|
| `decomposer-fichier` | Decomposer les fichiers markdown | [decomposer/decomposer-fichier/](decomposer/decomposer-fichier/) |

### Deplacer

| Outil | Description | Chemin |
|---|---|---|
| `deplacer-fichier` | Deplacer ou renommer un fichier | [deplacer/deplacer-fichier/](deplacer/deplacer-fichier/) |

### Detecter

| Outil | Description | Chemin |
|---|---|---|
| `detecter-erreur-statut` | Detecter les fichiers dont le statut ne correspond pas au contenu | [detecter/detecter-erreur-statut/](detecter/detecter-erreur-statut/) |
| `detecter-surcharge-fichier` | Detecter les fichiers qui grossissent trop | [detecter/detecter-surcharge-fichier/](detecter/detecter-surcharge-fichier/) |
| `detecter-local-hors-fonction` | Detecter les local utilises hors fonction dans les scripts bash | [detecter/detecter-local-hors-fonction/](detecter/detecter-local-hors-fonction/) |
| `detecter-usage-outils-externes` | Detecter les traces d'outils externes dans les fichiers (CRLF, non-ASCII, BOM) | [detecter/detecter-usage-outils-externes/](detecter/detecter-usage-outils-externes/) |

### Ecrire

| Outil | Description | Chemin |
|---|---|---|
| `ecrire-fichier` | Ecrire/echraser le contenu d'un fichier | [ecrire/ecrire-fichier/](ecrire/ecrire-fichier/) |

### Editer

| Outil | Description | Chemin |
|---|---|---|
| `editer-fichier` | Remplacer une chaine par une autre dans un fichier | [editer/editer-fichier/](editer/editer-fichier/) |

### Evaluer

| Outil | Description | Chemin |
|---|---|---|
| `evaluer-agents` | Verifier que les agents suivent leurs protocoles | [evaluer/evaluer-agents/](evaluer/evaluer-agents/) |
| `evaluer-coherence` | Verifier les liens et references croisees | [evaluer/evaluer-coherence/](evaluer/evaluer-coherence/) |
| `evaluer-conventions` | Verifier le nommage, l'ASCII, le format | [evaluer/evaluer-conventions/](evaluer/evaluer-conventions/) |
| `evaluer-structure` | Verifier l'arborescence et les fichiers critiques | [evaluer/evaluer-structure/](evaluer/evaluer-structure/) |

### Generateurs

| Outil | Description | Chemin |
|---|---|---|
| `generateurs-squelette-pense-bete` | Generer le squelette d'un pense-bete conforme au template | [generateurs/generateurs-squelette-pense-bete/](generateurs/generateurs-squelette-pense-bete/) |
| `generateurs-squelette-spec` | Generer le squelette d'une spec conforme au spec-template | [generateurs/generateurs-squelette-spec/](generateurs/generateurs-squelette-spec/) |
| `generateurs-squelette-todo` | Generer le squelette d'un todo conforme au todo-template | [generateurs/generateurs-squelette-todo/](generateurs/generateurs-squelette-todo/) |
| `generateurs-commande` | Composer et generer une commande complexe en posant une question par parametre | [generateurs/generateurs-commande/](generateurs/generateurs-commande/) |

### Gerer

| Outil | Description | Chemin |
|---|---|---|
| `gerer-sous-mission` | Gerer les sorties/reentrees du flux principal | [gerer/gerer-sous-mission/](gerer/gerer-sous-mission/) |

### Guider

| Outil | Description | Chemin |
|---|---|---|
| `guider-parcours` | Guider l'agent case par case (jeu de piste) dans son parcours JSON : indices outil/fichier/regle + branches selon les reponses | [guider/guider-parcours/](guider/guider-parcours/) |

### Inserer

| Outil | Description | Chemin |
|---|---|---|
| `inserer-contenu-fichier` | Inserer du contenu a une position precise dans un fichier | [inserer/inserer-contenu-fichier/](inserer/inserer-contenu-fichier/) |

### Lire

| Outil | Description | Chemin |
|---|---|---|
| `lire-fichier` | Lire le contenu complet (ou partiel) d'un fichier | [lire/lire-fichier/](lire/lire-fichier/) |
| `lire-lignes` | Lire des lignes specifiques d'un fichier (par numero ou plage) | [lire/lire-lignes/](lire/lire-lignes/) |
| `lire-frontmatter` | Extraire le frontmatter YAML en tete d'un fichier markdown | [lire/lire-frontmatter/](lire/lire-frontmatter/) |

### Lister

| Outil | Description | Chemin |
|---|---|---|
| `lister-agents` | Lister les agents avec leurs infos | [lister/lister-agents/](lister/lister-agents/) |
| `lister-appels` | Lister les appels de fonctions | [lister/lister-appels/](lister/lister-appels/) |
| `lister-dossiers` | Lister les dossiers d'un chemin | [lister/lister-dossiers/](lister/lister-dossiers/) |
| `lister-fichiers` | Lister les fichiers d'un chemin | [lister/lister-fichiers/](lister/lister-fichiers/) |
| `lister-fonctions` | Lister les fonctions d'un fichier | [lister/lister-fonctions/](lister/lister-fonctions/) |
| `lister-outils` | Lister les outils partages | [lister/lister-outils/](lister/lister-outils/) |
| `lister-prepares` | Lister les fichiers 'prepare' et verifier les specs | [lister/lister-prepares/](lister/lister-prepares/) |
| `lister-statuts` | Lister les fichiers par statut | [lister/lister-statuts/](lister/lister-statuts/) |

### Mettre a jour

| Outil | Description | Chemin |
|---|---|---|
| `mettre-a-jour-readme` | Mettre a jour le README depuis les sources de verite (agents, outils, chronologie) | [mettre-a-jour/mettre-a-jour-readme/](mettre-a-jour/mettre-a-jour-readme/) |


### Nettoyer

| Outil | Description | Chemin |
|---|---|---|
| `nettoyer-fichier` | Purifier un fichier en supprimant le contenu non essentiel | [nettoyer/nettoyer-fichier/](nettoyer/nettoyer-fichier/) |

### Rechercher

| Outil | Description | Chemin |
|---|---|---|
| `rechercher-accents-sensibles` | Rechercher les accents dans les zones sensibles (frontmatter, noms, blocs, code, liens) | [rechercher/rechercher-accents-sensibles/](rechercher/rechercher-accents-sensibles/) |
| `rechercher-dossier` | Verifier si un dossier existe (retourne 0/1) | [rechercher/rechercher-dossier/](rechercher/rechercher-dossier/) |
| `rechercher-fichier` | Verifier si un fichier existe (retourne 0/1) | [rechercher/rechercher-fichier/](rechercher/rechercher-fichier/) |
| `rechercher-fichiers-vides` | Rechercher les fichiers markdown vides ou quasi vides | [rechercher/rechercher-fichiers-vides/](rechercher/rechercher-fichiers-vides/) |
| `rechercher-pense-betes` | Rechercher les pense-betes existants (anti-doublon) | [rechercher/rechercher-pense-betes/](rechercher/rechercher-pense-betes/) |
| `rechercher-specs` | Rechercher les specs existantes (anti-doublon) | [rechercher/rechercher-specs/](rechercher/rechercher-specs/) |
| `rechercher-templates` | Rechercher les fichiers template du projet | [rechercher/rechercher-templates/](rechercher/rechercher-templates/) |
| `rechercher-texte` | Rechercher un pattern dans un fichier (grep generique) | [rechercher/rechercher-texte/](rechercher/rechercher-texte/) |
| `rechercher-todos` | Rechercher les todos existants (anti-doublon) | [rechercher/rechercher-todos/](rechercher/rechercher-todos/) |
| `rechercher-extension-fichier` | Extraire l'extension d'un fichier (ou verifier une extension) | [rechercher/rechercher-extension-fichier/](rechercher/rechercher-extension-fichier/) |

### Remplacer

| Outil | Description | Chemin |
|---|---|---|
| `remplacer-texte` | Remplacer une liste de paires ancien->nouveau dans plusieurs fichiers (renommages massifs) | [remplacer/remplacer-texte/](remplacer/remplacer-texte/) |
### Supprimer

| Outil | Description | Chemin |
|---|---|---|
| `supprimer-dossier` | Supprimer un dossier recursivement (avec protections) | [supprimer/supprimer-dossier/](supprimer/supprimer-dossier/) |
| `supprimer-fichier` | Supprimer un fichier avec verification | [supprimer/supprimer-fichier/](supprimer/supprimer-fichier/) |
| `supprimer-ligne` | Supprimer une ligne (ou une plage) par numero dans un fichier | [supprimer/supprimer-ligne/](supprimer/supprimer-ligne/) |

### Valider

| Outil | Description | Chemin |
|---|---|---|
| `valider-cartes-decision` | Verifier les cartes de decision des agents | [valider/valider-cartes-decision/](valider/valider-cartes-decision/) |
| `valider-conformite-ascii` | Valider la conformite ASCII de tous les fichiers | [valider/valider-conformite-ascii/](valider/valider-conformite-ascii/) |
| `valider-conventions` | Verifier que les conventions sont respectees | [valider/valider-conventions/](valider/valider-conventions/) |
| `valider-ebauche` | Verifier les exigences minimales d'un ebauche | [valider/valider-ebauche/](valider/valider-ebauche/) |
| `valider-liens` | Verifier que les liens sont valides | [valider/valider-liens/](valider/valider-liens/) |
| `valider-nommage` | Verifier que le nommage est correct | [valider/valider-nommage/](valider/valider-nommage/) |
| `valider-pense-bete` | Verifier l'integrite d'un pense-bete (structure, sections, ASCII) | [valider/valider-pense-bete/](valider/valider-pense-bete/) |
| `valider-relecture` | Verifier que chaque fiche agent + corrections contient la regle de relecture | [valider/valider-relecture/](valider/valider-relecture/) |
| `valider-numerotation` | Detecter les doublons d'etapes (etape X x2) dans les tableaux de mission des fiches agents | [valider/valider-numerotation/](valider/valider-numerotation/) |
| `valider-tableaux` | Verifier la coherence des tableaux des fiches agents : nombres annonces vs lignes, numerotation continue, completude des listes | [valider/valider-tableaux/](valider/valider-tableaux/) |
| `valider-spec` | Verifier l'integrite d'une spec (structure, sections, ASCII) | [valider/valider-spec/](valider/valider-spec/) |
| `valider-todo` | Verifier l'integrite d'un todo (phases 0-9, obligations) | [valider/valider-todo/](valider/valider-todo/) |

### Verifier

| Outil | Description | Chemin |
|---|---|---|
| `verifier-documents-manquants` | Verifier les .sh sans .md et inversement | [verifier/verifier-documents-manquants/](verifier/verifier-documents-manquants/) |
| `verifier-role-fichier` | Verifier qu'un fichier est utilise pour sa fonction | [verifier/verifier-role-fichier/](verifier/verifier-role-fichier/) |
| `verifier-separation-preoccupations` | Verifier la separation des preoccupations | [verifier/verifier-separation-preoccupations/](verifier/verifier-separation-preoccupations/) |
| `verifier-systeme` | Verifier le systeme utilisateur | [verifier/verifier-systeme/](verifier/verifier-systeme/) |

---

## Comment utiliser un outil

### Via le script bash

```bash
# 1. Chercher dans cet index -> trouver l'outil
# 2. Lire la documentation de l'outil
# 3. Executer le script
./[action]/[outil]/[outil].sh [OPTIONS]
# 4. Verifier le resultat
```

### Exemples

```bash
# Verifier le systeme
cerveau-projet/agents/tools/verifier/verifier-systeme/verifier-systeme.sh

# Lister les dossiers
cerveau-projet/agents/tools/lister/lister-dossiers/lister-dossiers.sh

# Lire un fichier
cerveau-projet/agents/tools/lire/lire-fichier/lire-fichier.sh fichier.md

# Rechercher un pattern
cerveau-projet/agents/tools/rechercher/rechercher-texte/rechercher-texte.sh "mot" fichier.md

# Valider les liens
cerveau-projet/agents/tools/valider/valider-liens/valider-liens.sh fichier.md

# Valider un fichier ebauche
cerveau-projet/agents/tools/valider/valider-ebauche/valider-ebauche.sh fichier.md

# Detecter les erreurs de statut
cerveau-projet/agents/tools/detecter/detecter-erreur-statut/detecter-erreur-statut.sh

# Changer le statut d'un fichier
cerveau-projet/agents/tools/changer/changer-statut/changer-statut.sh fichier.md prepare

# Corriger les emojis
cerveau-projet/agents/tools/corriger/corriger-emojis/corriger-emojis.sh fichier.md

# Corriger les accents (mode --all : purge totale, regle immuable)
cerveau-projet/agents/tools/corriger/corriger-accents-zones-sensibles/corriger-accents-zones-sensibles.sh --all fichier.md

# Lister les fichiers 'prepare'
cerveau-projet/agents/tools/lister/lister-prepares/lister-prepares.sh
```

---

## Comment creer un outil

> **REGLE OBLIGATOIRE** (protocole-outils) : toute creation d'outil passe par le `outil-template` (voir section ci-dessous).

```
1. Identifier le besoin (commande frequente)
2. Concevoir l'outil (objectif, parametres)
3. Copier le outil-template vers agents/tools/[categorie]/[nom-outil]/
4. Remplacer les placeholders [nom-outil] (script + documentation)
5. Developper la logique dans [nom-outil].sh
6. Completer la documentation dans [nom-outil].md
7. Tester en --dry-run (obligatoire)
8. Ajouter dans cet index
9. Assigner l'outil a l'agent concerne (protocole-outils Regle 6)
10. Valider la conformite ASCII (valider-conformite-ascii)
```

---

## Tests et Protections

### Protections (tester/)

| Protection | Description | Chemin |
|---|---|---|
| `tester-protection-blocage` | Protection contre les tests qui bloquent | [tester/protections/tester-protection-blocage/](tester/protections/tester-protection-blocage/) |
| `tester-protection-boucles-infinies` | Protection contre les boucles infinies | [tester/protections/tester-protection-boucles-infinies/](tester/protections/tester-protection-boucles-infinies/) |
| `tester-protection-erreurs-silencieuses` | Protection contre les erreurs silencieuses | [tester/protections/tester-protection-erreurs-silencieuses/](tester/protections/tester-protection-erreurs-silencieuses/) |

---

## Templates

| Template | Description | Chemin |
|---|---|---|
| `outil-template` | Modele standard de creation d'outils (script + doc) | [outil-template.md](outil-template.md) + [outil-template.sh](outil-template.sh) |

---

## Comment utiliser le outil-template

Le `outil-template` est constitue de deux fichiers a la racine de `tools/` :
- `outil-template.md` : modele de documentation
- `outil-template.sh` : modele de script

1. Copier `outil-template.md` et `outil-template.sh` vers `agents/tools/[categorie]/[nom-outil]/`
2. Renommer les fichiers avec le nom reel de l'outil (`[nom-outil].md`, `[nom-outil].sh`)
3. Remplacer les marqueurs `[nom-outil]` dans les deux fichiers
4. Completer la logique du script et la documentation
5. Ajouter l'outil dans cet index
6. Tester en `--dry-run` avant toute utilisation

---

## Documents de reference

| Document | Description | Chemin |
|---|---|---|
| `outils-base.md` | Analyse des outils de base : inventaire des 18 outils P0/P1/P2 (tous crees) | [outils-base.md](outils-base.md) |

---

## Statistiques

| Categorie | Nombre d'outils |
|---|---|
| Ajouter | 1 |
| Analyser | 2 |
| Changer | 1 |
| Combos | 4 |
| Condenser | 1 |
| Copier | 2 |
| Corriger | 5 |
| Creer | 4 |
| Decomposer | 1 |
| Deplacer | 1 |
| Detecter | 2 |
| Ecrire | 1 |
| Editer | 1 |
| Evaluer | 4 |
| Generateurs | 4 |
| Gerer | 1 |
| Guider | 1 |
| Inserer | 1 |
| Lire | 3 |
| Lister | 8 |
| Mettre a jour | 1 |
| Activer | 1 |
| Nettoyer | 1 |
| Rechercher | 10 |
| Remplacer | 1 |
| Supprimer | 3 |
| Valider | 9 |
| Verifier | 4 |
| Protections | 3 |
| Templates | 1 |
| **Total** | **82** |

> **Note sur le decompte** : 73 outils d'action + 4 combos sont inclus dans les categories ci-dessus ; `lister-outils.sh` affiche 73 car il exclut `combos/` et `tester/` de son comptage.

---
