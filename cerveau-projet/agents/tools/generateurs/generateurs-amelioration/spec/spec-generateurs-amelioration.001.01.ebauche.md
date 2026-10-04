---
identite:
  type: spec
  appartient_a: commun
  commun: true
---
# Spec -- Generateurs-amelioration (checklist de questions par theme)

**Version** : 2.1.0
**Statut** : ebauche
**Date creation** : 2026-08-09
**Agent** : Vulcain (creation)
**Historique** : v2.1.0 (alignement spec/outil, round 11 coherence documentaire : version de la spec synchronisee avec la version de l outil 2.1.0) -> v1.0.0 (creation, 2026-08-09). v2.0.0 (2026-08-09) -- theme `ameliorer-outil` reformule (10 -> 14 questions) : 5 RAPPELS STRATEGIQUES en tete (q1 diagnostic de l existant, q2 horloge = anticiper les extensions naturelles, q3 formats = couvrir la famille de cas, q4 ameliorer vs evoluer = eviter patch puis refonte, q5 perimetre) + 9 questions techniques renumerees (q6-q14). Principe utilisateur : les questions doivent pousser l agent a reflechir a CE qui doit etre ameliore et a anticiper l evolution plutot que de patcher aujourd hui et refondre plus tard.

---

## Objectif

Poser des **LISTES DE QUESTIONS par THEME** avant toute mission d'amelioration
et d'optimisation (outil, combo, generateur, carte de decision, case, regle).
L'agent lance ce processus pour garantir la coherence et de meilleures
analyses/resultats avant d'agir. Les listes de questions sont **faciles a
editer** : elles vivent dans un fichier JSON (`themes-amelioration.json`),
chaque theme etant un ensemble de questions avec leur raison.

**Besoin utilisateur (2026-08-09)** : un generateur d'amelioration et
d'optimisation pour nos outils, combos, generateurs, cartes de decision,
cases, etc. Quand une demande d'amelioration arrive, la carte de decision doit
declencher l'utilisation de ce generateur qui fournit des listes de questions
en fonction du theme de la demande.

**Decisions utilisateur (2026-08-09)** :
1. Format des listes de questions = **JSON** ;
2. Ce que produit le generateur = **checklist interrogee** (questions posees
   une a une, reponses, recapitulatif) ;
3. Perimetre v1 = **minimal (outil seul)** : outil + theme `ameliorer-outil` ;
4. Branchement de la piste = **Cerberus seul** (une case dans le parcours
   Cerberus, mission Buffy ulterieure hors perimetre de cette spec).

## Pourquoi cet outil ?

| Probleme | Solution |
|---|---|
| L'amelioration se fait sans questionnement prealable | Checklist de questions par theme, posee AVANT d'agir |
| Les cartes de decision accumulent toutes les reflexions | La reflexion est deplacee dans l'outil (cartes allegees) |
| Les bonnes questions sont dispersees dans les lecons | Listes centralisees dans un JSON editeur par theme |

## Vue d'ensemble

```
themes-amelioration.json  (liste de themes + questions, EDITION SIMPLE)
    |
    v
generateurs-amelioration.py --theme <nom> [--reponses 'q1=...;q2=...']
    |
    v
Checklist interrogee : questions posees une a une (avec raison)
    -> RECAPITULATIF (question -> reponse)
    -> AUCUN fichier cree (reflexion en session)
```

## Interface CLI

```
generateurs-amelioration.py [options]
  --theme <nom>            Theme d'amelioration a parcourir (obligatoire)
  --reponses 'q1=...;q2=...'  Reponses fournies (mode non-interactif, testable)
  --liste                  Lister les themes disponibles
  --version                Afficher la version
```

Parite py/sh : le .sh est un wrapper pur (`exec python3 "$PY_SCRIPT" "$@"`) --
aucune divergence de logique possible entre les 2 versions.

## Format du fichier de themes

```json
{
  "version": "1.0.0",
  "themes": [
    {
      "nom": "ameliorer-outil",
      "description": "...",
      "questions": [
        { "id": "q1", "question": "...", "raison": "..." }
      ]
    }
  ]
}
```

- `nom` : identifiant du theme (utilise avec `--theme <nom>`).
- `questions[].id` : unique dans le theme (cle des reponses `--reponses`).
- `questions[].raison` : pourquoi cette question (affichee en mode interactif).

## Regles

1. **AUCUN fichier cree** : la reflexion reste en session (checklist
   parcourue + recapitulatif) -- decision utilisateur 2026-08-09.
2. **ASCII strict** : code et themes en ASCII (regle immuable) ; un contenu
   non-ASCII est refuse avant lecture.
3. **LF** : tous les fichiers de l'outil en LF (standard projet).
4. **Parite py/sh** : wrapper pur, memes resultats sur les memes arguments.
5. **Mode non-interactif** (`--reponses`) : indispensable pour les tests
   formels (Morpheus) sans saisie interactive.
6. **Regle des 5 fichiers** : py, sh, md, spec + enregistrements
   (index-tools.md, catalogue generateurs-commande).

## Emplacement des fichiers

| Fichier | Chemin |
|---|---|
| Outil python | `agents/tools/generateurs/generateurs-amelioration/generateurs-amelioration.py` |
| Outil bash | `agents/tools/generateurs/generateurs-amelioration/generateurs-amelioration.sh` |
| Documentation | `agents/tools/generateurs/generateurs-amelioration/generateurs-amelioration.md` |
| Spec | `agents/tools/generateurs/generateurs-amelioration/spec/spec-generateurs-amelioration.001.01.ebauche.md` |
| Themes | `agents/tools/generateurs/generateurs-amelioration/themes-amelioration.json` |
