---
identite:
  type: outil
  appartient_a: commun
  commun: true
  tags: validation, parcours, communs
  combos:
    - combo-controle-outil
    - combos-valider-cerveau
---
# valider-cartes-decision

**Version :** 0.5.0
**Statut :** prepare
**Categorie :** valider
**Chemin :** `agents/tools/valider/valider-cartes-decision/`
**Proprietaire :** Vulcain (outil partage)

---

## Objectif

Verifier que les agents respectent leur **CARTE DE DECISION**. Depuis
l'allegement des fiches (v0.2.0), la carte de decision d'un agent etait son
**PARCOURS JSON** (`agents/<agent>/parcours/parcours-<agent>.json`) : la
SOURCE DE VERITE du guidage (jeu de piste). Depuis la v0.5.0, l'outil
detecte AUTOMATIQUEMENT le format : les **arbres v2**
(`arbre-<agent>.json` : racine/branches -> themes -> fins, le format servi
par le pilote Oracle) sont valides en v2 (structure, branches vers des
themes existants, themes avec redirects, fins centralisees), les parcours
v1 en v1 (structure, references, relecture). --agent valide l'arbre v2
s'il existe (repli v1 sinon).

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

### 6. Relecture obligatoire (Pattern 4 v2)

Structure cible (migration 2026-08-16) : la lecture de la fiche est TOUJOURS
obligatoire, puis la confirmation est posee.

```
[ ] c0 = action RELIRE OBLIGATOIRE : corrections puis fiche (2 outils lire-fichier), suivant = c0b
[ ] c0b = question confirmation : OUI -> c0c, NON -> c0 (relecture)
```

Une carte avec l ancienne structure (c0 question "EN MEMOIRE" avec OUI -> c0c)
est NON CONFORME : elle permettait de contourner la lecture.

### 7. Garde-fou : AUCUN SUIVANT MORT (v0.3.2)

Le champ `suivant` n'est legitime que sur une case **SANS branches** et
**NON-fin** (question/indice/action/controle qui enchaine). Deux cas sont
detectes comme ERREUR (mecanique guider-parcours) :

```
[ ] Case type 'fin' avec champ suivant -> la navigation s'arrete a la fin,
    le suivant est IGNORE (mort)
[ ] Case avec branches non vides ET champ suivant -> les branches priment,
    le suivant n'est JAMAIS lu (mort)
```

> **Pourquoi ?** Defaut decouvert par l'audit Themis du 2026-08-10 : 25
> suivant morts sur 10 parcours (themis : 210 chemins fantomes -> 48 apres
> correction). valider-cartes-decision v0.3.1 ne les detectait pas (references
> valides mais logique morte). Ce garde-fou empeche la recurrence.

### 8. COMMANDE ACTIVER EXACTE dans les fins 'Activer X' (v0.4.0)

Toute case type `fin` dont le titre commence par `FIN - Activer <agent>` doit
contenir dans son message :

```
[ ] La commande exacte : activer-agent-principal.py activer <session> <agent>
    (le placeholder <session> est remplace par SA session a l execution ;
    une session concrete session-llm-N est aussi acceptee - v0.4.6)
[ ] La mention 'PAS reactiver'
```

> **Multi-sessions (v0.4.6)** : la commande accepte le placeholder `<session>`
> (chaque LLM l utilise dans SA session) OU une session concrete
> `session-llm-N`. L ancien format fige `session-llm-1` interdisait aux
> sessions llm-2/3/4 de suivre leur carte (D6).

> **Pourquoi ?** Defaut decouvert le 2026-08-11 : les 8 fins 'FIN - Activer
> Janus' disaient 'J ACTIVE JANUS' sans la commande exacte -> les agents
> retombaient sur le reflexe reactiver (qui ramene toujours a Cerberus).
> La comparaison est insensible a la casse (titre 'Janus' vs commande 'janus').

### 9. FORMAT DE VERSION sans prefixe 'v' (v0.4.0)

```
[ ] parcours.version ne commence pas par 'v' (format canonique sans v, ex: 0.3.3)
```

> **Pourquoi ?** 4 parcours stockaient leur version avec un prefixe 'v'
> incoherent (convention : parcours sans 'v', fiches Pattern 14 avec 'v').

### 10. COHERENCE FICHE/PARCOURS (Pattern 14, v0.4.0)

Verifie via `--agent`/`--tous` que la fiche `agents/<agent>/<agent>.md` est
coherente avec le parcours :

```
[ ] Si la fiche contient 'PARCOURS (vX.Y.Z)', alors X.Y.Z == parcours.version
[ ] ATTENTION (non bloquant) si le Pattern 14 est absent de la fiche
```

> **Pourquoi ?** Les fiches des agents doivent rester synchronisees avec le
> parcours (Pattern 14). Une version differente = carte stale = guidage
> incoherent.

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
6. Relecture obligatoire (c0 action RELIRE + c0b confirmation)
   [OK] c0 est une action RELIRE OBLIGATOIRE, c0b une question de confirmation
7. Garde-fou suivant mort (fin avec suivant / branches + suivant)
   [OK] Aucun suivant mort (0 fin avec suivant, 0 branches + suivant)
8. Commande activer exacte dans les fins 'Activer X' (P8)
   [OK] Toutes les fins 'FIN - Activer X' contiennent la commande exacte + 'PAS reactiver'
9. Format de version sans prefixe 'v' (P9)
   [OK] parcours.version '0.3.3' sans prefixe v
10. Coherence fiche/parcours (Pattern 14, P10)
   [OK] Fiche PARCOURS (v0.3.3) == parcours 0.3.3

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
| Case c0 absente | Ajouter c0 = action RELIRE OBLIGATOIRE (corrections puis fiche) -> c0b, c0b = question confirmation (OUI -> c0c, NON -> c0) |
| Suivant mort : fin avec suivant | Retirer le champ suivant de la case fin (la navigation s'arrete deja a la fin) |
| Suivant mort : branches + suivant | Retirer le champ suivant de la case (les branches priment dans guider-parcours) |
| Fichier .md passe en --fichier | La cible est le parcours JSON, pas la fiche allegee |
| Fin Activer X sans commande exacte | Ajouter 'activer-agent-principal.py activer <session> <agent>' (ou session-llm-N) + 'PAS reactiver' dans le message |
| Version avec prefixe v | Retirer le 'v' de parcours.version (format canonique sans v) |
| Incoherence fiche/parcours | Aligner la fiche (Pattern 14) sur la version du parcours |

---

## Dependances

- `agents/<agent>/parcours/parcours-<agent>.json` -- parcours de l'agent a verifier
- `python3` -- requis (le `.sh` transmet au `.py`)

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.5.0 | 2026-09-04 | SUPPORT FORMAT V2 (constat Janus 8bca6f3d) : detection auto (identite.type == 'arbre' -> valider_arbre_v2) ; --agent valide l'arbre v2 (arbre-<agent>.json, celui que sert le pilote) s'il existe, repli v1 sinon ; l'arbre v2 verifie structure, version, racine/branches (vers -> fichier theme existant), themes references (type + redirects) et fins centralisees. Validation v1 inchangee (--fichier sur un parcours v1). 22/22 agents conformes. |
| 0.4.1 | 2026-08-13 | GARDE-FOU ANTI-RESIDUS : verifier_residus_racine() detecte les fichiers nommes comme des versions semver a la racine (residus de redirections accidentelles de sortie) et affiche un WARNING - sources de verite de version dans cerveau-projet/agents/clio/, JAMAIS a la racine |
| 0.1.0-beta | 2026-08-05 | Creation initiale |
| 0.2.0-py | 2026-08-06 | Portage Python (validait la section Carte de Decision des fiches) |
| 0.3.0 | 2026-08-08 | Cible changee : PARCOURS JSON (source de verite) au lieu de la section des fiches allegees. 6 controles : JSON, structure, case_depart, types, references, c0 de relecture. --tous scanne tous les agents avec parcours/. .sh = wrapper vers .py (parite stricte) |
| 0.3.1 | 2026-08-10 | Type action ajoute (modele cible de la refonte des cartes). Parite py/sh (wrapper) maintenue. Docstring spec v0.2.9 -> v0.5.0. |
| 0.3.2 | 2026-08-10 | GARDE-FOU SUIVANT MORT : controle 7 detecte (a) fin avec suivant et (b) branches + suivant (le suivant n'est legitime que sans branches et non-fin). Parite py/sh maintenue. |
| 0.4.0 | 2026-08-11 | 3 POINTS SEMANTIQUES : 8 = commande activer exacte dans les fins 'Activer X' (insensible a la casse, + PAS reactiver), 9 = format de version sans prefixe 'v', 10 = coherence fiche/parcours (Pattern 14, via --agent/--tous). 11/11 agents conformes. Parite py/sh maintenue. |

---

## Notes

- La carte de decision d'un agent = SON parcours JSON, plus jamais la fiche
- Cet outil doit etre execute apres chaque modification de parcours
- `combo-controle-outil` l'appelle via `.py --tous` (interface conservee)

---
