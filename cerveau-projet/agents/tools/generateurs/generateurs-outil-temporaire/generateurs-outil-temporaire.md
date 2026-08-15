---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# generateurs-outil-temporaire

**Version :** 0.2.2
**Statut :** prepare
**Categorie :** Generateurs
**Chemin :** `agents/tools/generateurs/generateurs-outil-temporaire/`

## Description

Genere un **outil temporaire** (script Python jetable) dans le workspace pour repondre a un besoin ponctuel d'une mission. L'outil temporaire est cree **DANS le workspace uniquement** (jamais hors workspace, jamais dans `tools/`), porte un en-tete standard (identite `type: outil-temporaire`, ASCII strict, LF, 100% stdlib) et se termine par la **question de PROMOTION** : si le besoin se reproduit (2e utilisation), l'agent **active Vulcain** pour creer l'outil durable (protocole 5 fichiers) ; Vulcain reactive ensuite l'agent precedent.

**Quand l'utiliser ?** Des qu'une mission a besoin d'un script jetable (`tmp-*.py`) : recherche, transformation de fichiers, analyse ponctuelle. Le besoin recurrent (2e occurrence) n'a pas le droit de rester temporaire -> **PROMOTION** (activer Vulcain).

## Utilisation

```bash
# Apercu du script sans creer de fichier (dry-run par defaut)
generateurs-outil-temporaire.sh --nom mesurer-taille-dossiers

# Version Python (recommandee)
python3 generateurs-outil-temporaire.py --nom mesurer-taille-dossiers

# Avec description et dossier de destination
generateurs-outil-temporaire.py --nom mesurer-taille-dossiers \
    --description "Mesure la taille de chaque dossier du workspace" \
    --dossier .tmp-outil/

# Ecriture reelle (--force obligatoire apres le dry-run)
generateurs-outil-temporaire.py --nom mesurer-taille-dossiers --force
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--nom <besoin>` | Nom du besoin (obligatoire, minuscules sans accents, prefixe `tmp-` automatique) | - |
| `--description <texte>` | Description courte de l'outil | vide |
| `--dossier <chemin>` | Dossier de destination DANS le workspace | racine workspace |
| `--force` | Ecrire reellement le fichier (sans : dry-run) | false |
| `--version` | Afficher la version | - |
| `--aide`, `-h` | Afficher l'aide | - |

## Comportement

| # | Fonctionnalite | Detail |
|---|---|---|
| 1 | **Dry-run par defaut** | Sans `--force`, l'outil affiche le contenu genere sans creer de fichier (pattern securite du projet) |
| 2 | **Perimetre workspace** | Le dossier de destination DOIT etre dans le workspace (refus sinon) |
| 3 | **Jamais dans tools/** | L'outil temporaire est jetable, il ne remplace pas l'outil durable (role Vulcain) |
| 4 | **En-tete standard** | identite `type: outil-temporaire`, ASCII strict, LF, 100% stdlib, version `0.1.0-tmp` |
| 5 | **Question PROMOTION** | Affichee a la fin : besoin recurrent (2e utilisation) ? -> OUI = activer Vulcain |
| 6 | **Refus d'ecrasement** | Le fichier existant n'est jamais ecrase (erreur si present) |
| 7 | **Parite .py/.sh** | Les deux versions ont le meme comportement (dry-run, workspace, promotion) |
| 8 | **TRIPLET (v0.2.0)** | Le script genere embarque les PROTECTIONS (nommage, dry-run, gestion erreur) + OPTIONS ON/OFF (--isoler/--desactiver) + CHRONO (--chrono par defaut, --no-chrono) - meme triplet que le template-test v0.3.0 |
| 9 | **DECLARATION USAGES (v0.2.1)** | Le script genere embarque le bloc DECLARATION : variable AGENT + fonctions `declarer_usage()` / `declarer_usages()` qui appellent `enregistrer-usage-outil --mode script-temporaire` pour le script lui-meme et chaque outil utilise (appele en fin de main, erreur si AGENT non renseigne) |
| 10 | **CHRONO EN HAUT (v0.2.2)** | BUFFER TOTAL (decision utilisateur 2026-08-15) : toute la sortie du script (y compris les sous-processus de declaration, dont la sortie est capturee) est retenue en memoire, le chrono `=== CHRONO ===` est affiche EN PREMIER puis le contenu - le chrono est TOUJOURS la premiere ligne, visible a chaque execution |

## Cycle de vie de l'outil temporaire

```
Mission -> besoin -> outil existe ?
   |-- OUI  -> j'utilise l'outil existant (index-tools / catalogue)
   |-- NON  -> DECISION
       |-- TEMPORAIRE (usage ponctuel)
       |   |-- generateurs-outil-temporaire (cree tmp-*.py dans le workspace)
       |   |-- utilisation + RVAV
       |   |-- SUPPRIME en fin de mission (0 residu)
       |   +-- si le besoin se reproduit -> PROMOTION
       +-- DURABLE (besoin recurrent, 2e utilisation)
           |-- l'agent ACTIVE VULCAIN directement (maillon de chaine)
           |-- Vulcain cree l'outil durable (protocole 5 fichiers)
           |-- Vulcain REACTIVE L'AGENT PRECEDENT
           +-- l'agent precedent reprend SA mission
```

## Validation

- `valider-conformite-ascii` : 0 caractere non-ASCII sur le script genere
- LF pur (jamais de CRLF)
- `valider-nommage --type outil` : nommage conforme

## Historique

| Version | Date | Changement |
|---|---|---|
| 0.2.2 | 2026-08-15 | Template : CHRONO EN HAUT (buffer total) - toute la sortie retenue, chrono affiche en premier, sous-processus de declaration captures |
| 0.2.1 | 2026-08-14 | Template enrichi : bloc DECLARATION USAGES dans le script genere (anti-recurrence registre a 0 ligne) |
| 0.2.0 | 2026-08-14 | Template enrichi : triplet (protections + options on/off + chrono) dans le script genere |
| 0.1.0 | 2026-08-09 | Creation : generateur d'outil temporaire (dry-run, workspace, question promotion, parite py/sh) |
