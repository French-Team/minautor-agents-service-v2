---
identite:
  type: spec
  appartient_a: commun
  commun: true
---
# Spec -- Cartographier-parcours (cartographie d'un parcours en fichier)

**Version** : 0.1.0
**Statut** : ebauche
**Date creation** : 2026-08-09
**Agent** : Vulcain (creation)
**Historique** : v0.1.0 (creation, 2026-08-09)

---

## Objectif

Produire la **CARTOGRAPHIE d'un parcours de decision (parcours JSON) dans un
fichier markdown**, pour les analyses rapides du parcours d'un agent. Le
fichier devient un document ouvrable et survolable : arbre ASCII des cases,
impasses, boucles, chemins principaux de la case Mission aux fins.

**Besoin utilisateur (2026-08-09)** : Atlas a besoin de cartographier le
parcours d'un agent dans un fichier pour ses analyses rapides. Decisions :
(1) sortie = fichier dans le DOSSIER DU PARCOURS AUDITE
(`<dossier>/cartographie-<agent>.md`) ; (2) format = ARBRE ASCII lisible dans
tout editeur ; (3) branchement dans le parcours Atlas = mission Buffy
ulterieure (hors perimetre de cette spec).

## Pourquoi cet outil ?

| Probleme | Solution |
|---|---|
| `guider-parcours --liste` = inventaire lineaire, pas de vue structurelle | Arbre ASCII par profondeur avec branches et fins |
| `generateurs-carte analyser` = chemins en CONSOLE, rien de persiste | Fichier markdown persistable dans le dossier du parcours |
| Aucun document de survol du parcours d'un agent | Cartographie complete : en-tete, arbre, impasses, boucles, chemins |

## Vue d'ensemble

```
parcours-<agent>.json  (source, LECTURE SEULE)
    |
    v
cartographier-parcours.py <parcours.json> [--sortie <fichier>] [--dry-run]
    |
    v
<dossier-du-parcours>/cartographie-<agent>.md   (rendu markdown)
```

## Rendu genere

### 1. En-tete (tableau)

Agent, version du parcours, case de depart, nombre de cases, nombre de chemins.

### 2. Arbre des cases (bloc ```)

- Chaque case affichee UNE fois (premiere occurrence) : `[id] (type) titre`
- Branches marquees `(branche <reponse>)`, sorties directes `(suivant)`
- Convergences (case deja affichee) marquees `[convergence]` sans descendre
- Symboles de branche ASCII : `|--` (enfant non dernier), `` `-- `` (dernier)

### 3. Cases sans sortie (impasses)

Cases non-`fin` sans `suivant` ni `branches` (ou 'Aucune impasse').

### 4. Boucles detectees

Cases qui pointent vers elles-memes (ou 'Aucune boucle').

### 5. Chemins principaux (depart -> fins)

Chaque chemin avec sa case finale (titre) et la suite des cases traversees
(BFS anti-boucle, logique reutilisee de generateurs-carte analyser).

## Interface CLI

```
cartographier-parcours.py <parcours.json> [options]
  -o, --sortie <fichier>   Fichier markdown de sortie
                           (defaut: <dossier-du-parcours>/cartographie-<agent>.md)
  --dry-run                Simuler sans ecrire
  --verbose                Afficher les details
  --version                Afficher la version
```

Parite py/sh : le .sh est un wrapper pur (`exec python3 "$PY_SCRIPT" "$@"`) --
aucune divergence de logique possible entre les 2 versions.

## Regles

1. **LECTURE SEULE** : l'outil ne modifie JAMAIS le parcours source (aucune
   sauvegarde, aucun recablage) -- il lit et produit un fichier derive.
2. **ASCII strict** : le fichier genere est ecrit en ASCII (regle immuable) ;
   un contenu non-ASCII est refuse avant ecriture.
3. **Sortie par defaut** : dossier du parcours audite
   (`<dossier>/cartographie-<agent>.md`) -- decision utilisateur 2026-08-09.
4. **Parite py/sh** : wrapper pur, memes resultats sur le meme parcours.
5. **Reutilisation** : la detection des chemins (BFS) reprend la logique
   validee de `generateurs-carte analyser` (anti-boucle, impasses) -- jamais de
   reimplementation.
6. **Regle des 5 fichiers** : py, sh, md, spec, tests/ (tests formels ecrits
   par Morpheus -- delegation des tests, REGLE ABSOLUE Vulcain).

## Emplacement des fichiers

| Fichier | Chemin |
|---|---|
| Outil python | `agents/tools/cartographier/cartographier-parcours/cartographier-parcours.py` |
| Outil bash | `agents/tools/cartographier/cartographier-parcours/cartographier-parcours.sh` |
| Documentation | `agents/tools/cartographier/cartographier-parcours/cartographier-parcours.md` |
| Spec | `agents/tools/cartographier/cartographier-parcours/spec/spec-cartographier-parcours.001.01.ebauche.md` |
