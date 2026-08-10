---
identite:
  type: outil
  appartient_a: commun
  commun: true
  tags: validation, parcours, communs
---
# valider-cartes-decision

**Version :** 0.3.1
**Statut :** prepare
**Categorie :** valider
**Chemin :** `agents/tools/valider/valider-cartes-decision/`
**Proprietaire :** Vulcain (outil partage)

---

## Objectif

Verifier que les agents respectent leur **CARTE DE DECISION**. Depuis
l'allegement des fiches (v0.2.0), la carte de decision d'un agent est son
**PARCOURS JSON** (`agents/<agent>/parcours/parcours-<agent>.json`) : c'est la
SOURCE DE VERITE du guidage (jeu de piste). L'outil valide la structure, les
references et la case de relecture d'un parcours.

**Pourquoi cet outil ?**
- Les fiches allegees ne contiennent plus de section "Carte de Decision"
- Le parcours JSON est la source unique du guidage : il doit etre valide
- Il garantit la coherence des cartes de decision de tous les agents

---

## Utilisation

```
python3 valider-cartes-decision.py --agent <nom>
python3 valider-cartes-decision.py --tous
python3 valider-cartes-decision.py --fichier <parcours.json>
```

Le `.sh` est un wrapper : il transmet les arguments au `.py` (parite stricte).

---

## Parametres

| Parametre | Type | Obligatoire | Description |
|---|---|---|---|
| `--agent <nom>` | string | Non | Verifier le parcours d'un agent specifique |
| `--tous` | boolean | Non | Verifier les parcours de tous les agents |
| `--fichier <chemin>` | string | Non | Verifier un fichier parcours JSON specifique |
| `--version` | - | Non | Afficher la version |

---

## Ce que l'outil verifie (un parcours JSON)

### 1. JSON valide

```
[ ] Le fichier se parse sans erreur (json.load)
```

### 2. Structure top-level

```
[ ] Cles presentes : identite + parcours + cases
[ ] identite.type = "parcours"
```

### 3. Case de depart

```
[ ] parcours.case_depart existe
[ ] Elle designe une case reelle dans cases
```

### 4. Types de cases

```
[ ] Chaque case a un type valide : question / indice / controle / fin / action
```

### 5. References

```
[ ] chaque suivant pointe vers une case existante
[ ] chaque branche.vers pointe vers une case existante
```

### 6. Case c0 de relecture (Pattern 4)

```
[ ] La case c0 existe et est de type question (relecture honnete)
[ ] ATTENTION (non bloquant) si la question ne semble pas poser la relecture
```

---

## Format de sortie

```
=== Verification de l'agent : <agent> ===

1. JSON valide
   [OK] JSON parse sans erreur
2. Structure (identite + parcours + cases)
   [OK] Cles top-level presentes
3. Case de depart (case_depart)
   [OK] case_depart 'c0' existe
4. Types de cases (question/indice/controle/fin/action)
   [OK] 41 cases, tous types valides
5. References (suivant + branches.vers)
   [OK] Toutes les references pointent vers des cases existantes
6. Case c0 de relecture honnete (Pattern 4)
   [OK] c0 est une question de relecture

=== Resultat : CONFORME ===
```

`--tous` ajoute un resume final : Agents verifies / conformes / non conformes.

---

## Erreurs courantes

| Erreur | Correction |
|---|---|
| JSON invalide | Corriger la syntaxe du fichier parcours-<agent>.json |
| Cles manquantes | Verifier identite + parcours + cases presentes |
| case_depart introuvable | Verifier parcours.case_depart designe une case existante |
| Type invalide | Utiliser question / indice / controle / fin / action |
| Reference cassee | Corriger suivant ou branche.vers qui pointe vers une case absente |
| Case c0 absente | Ajouter la question de relecture honnete en case c0 (Pattern 4) |
| Fichier .md passe en --fichier | La cible est le parcours JSON, pas la fiche allegee |

---

## Dependances

- `agents/<agent>/parcours/parcours-<agent>.json` -- parcours de l'agent a verifier
- `python3` -- requis (le `.sh` transmet au `.py`)

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-05 | Creation initiale |
| 0.2.0-py | 2026-08-06 | Portage Python (validait la section Carte de Decision des fiches) |
| 0.3.1 | 2026-08-10 | Type action ajoute (modele cible de la refonte des cartes). Parite py/sh (wrapper) maintenue. Docstring spec v0.2.9 -> v0.5.0. |
| 0.3.0 | 2026-08-08 | Cible changee : PARCOURS JSON (source de verite) au lieu de la section des fiches allegees. 6 controles : JSON, structure, case_depart, types, references, c0 de relecture. --tous scanne tous les agents avec parcours/. .sh = wrapper vers .py (parite stricte) |

---

## Notes

- La carte de decision d'un agent = SON parcours JSON, plus jamais la fiche
- Cet outil doit etre execute apres chaque modification de parcours
- `combo-controle-outil` l'appelle via `.py --tous` (interface conservee)

---
