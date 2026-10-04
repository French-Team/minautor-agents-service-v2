---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# cartographier-parcours

| Champ | Valeur |
|---|---|
| **Version** | 0.1.0 |
| **Statut** | ebauche |
| **Categorie** | cartographier |
| **Derniere mise a jour** | 2026-08-09 |
| **Python** | cartographier-parcours.py |
| **Bash** | cartographier-parcours.sh (parite) |

---

## Description

**Genere la CARTOGRAPHIE d'un parcours de decision (parcours JSON) dans un
fichier markdown** : arbre ASCII des cases (indentation par profondeur, types,
titres, branches marquees et fins) + sections detaillees (impasses, boucles,
chemins principaux de la case Mission aux fins).

**Pour qui ?** Atlas (explorateur/cartographe) cartographie le parcours d'un
agent dans un fichier pour ses analyses rapides. L'outil est en LECTURE SEULE :
il ne modifie JAMAIS le parcours source.

**Pourquoi cet outil ?** `guider-parcours --liste` donne un inventaire lineaire
des cases, `generateurs-carte analyser` donne les chemins en console -- mais
aucun outil ne produit une CARTE VISUELLE PERSISTEE en fichier. Cet outil comble
le vide : un document ouvrable, survolable, a garder a cote du parcours.

**Reutilisation** : la detection des chemins (BFS) reprend la logique validee de
`generateurs-carte analyser` (anti-boucle, impasses marquees).

---

## Utilisation

### CLI Python

```
python3 cartographier-parcours.py <parcours.json> [options]

Options :
  -o, --sortie <fichier>  Chemin du fichier markdown de sortie
                          (defaut: <dossier-du-parcours>/cartographie-<agent>.md)
  --dry-run               Simuler sans ecrire le fichier
  --verbose               Afficher les details
  --version               Afficher la version
```

### CLI bash

```
bash cartographier-parcours.sh <parcours.json> [options]
```

Memes options que la version Python (parite par construction : wrapper pur).

---

## Rendu genere

Le fichier markdown contient :

### 1. En-tete (tableau)

| Champ | Valeur |
|---|---|
| Agent | nom de l'agent |
| Version du parcours | version du JSON |
| Case de depart | c0 |
| Nombre de cases | total |
| Nombre de chemins | depart -> fins |

### 2. Arbre des cases (bloc ```)

```
-- [c0] (question) Relecture : ta fiche et tes corrections en memoire ?
|   |-- [c0c] (indice) CONTEXTE OBLIGATOIRE  (branche OUI)
|       `-- [c1] (question) Mission  (suivant)
```

- Chaque case est affichee UNE fois (premiere occurrence)
- Les branches portent leur reponse : `(branche OUI)`, `(branche explorer)`
- Les sorties directes portent `(suivant)`
- Les convergences (case deja affichee) sont marquees `[convergence]` sans descendre

### 3. Cases sans sortie (impasses)

Liste des cases non-`fin` sans `suivant` ni `branches` (ou 'Aucune impasse').

### 4. Boucles detectees

Liste des cases qui pointent vers elles-memes (ou 'Aucune boucle').

### 5. Chemins principaux (depart -> fins)

Chaque chemin avec sa case finale (titre de la fin) et la suite des cases
traversees, marque `[impasse]` le cas echeant.

---

## Exemples

### Cartographier le parcours d'Atlas (sortie par defaut)

```bash
python3 cerveau-projet/agents/tools/cartographier/cartographier-parcours/cartographier-parcours.py \
  cerveau-projet/agents/atlas/parcours/parcours-atlas.json
```

Cree `cerveau-projet/agents/atlas/parcours/cartographie-atlas.md`.

### Sortie personnalisee (--sortie)

```bash
python3 cerveau-projet/agents/tools/cartographier/cartographier-parcours/cartographier-parcours.py \
  cerveau-projet/agents/cerberus/parcours/parcours-cerberus.json -o .tmp-cartographie-cerberus.md
```

### Simuler sans ecrire (--dry-run)

```bash
python3 cerveau-projet/agents/tools/cartographier/cartographier-parcours/cartographier-parcours.py \
  cerveau-projet/agents/atlas/parcours/parcours-atlas.json --dry-run
```

---

## Regles

1. Le nom de l'outil DOIT commencer par le prefixe du dossier (`cartographier-`) -- controle au demarrage (verifier_nommage)
2. L'outil est en LECTURE SEULE : il ne modifie JAMAIS le parcours source
3. Le fichier genere est ecrit en ASCII strict (regle immuable) -- un contenu non-ASCII est refuse avant ecriture
4. Le fichier de sortie est cree dans le DOSSIER DU PARCOURS AUDITE par defaut (decision utilisateur 2026-08-09) -- `--sortie` pour un chemin personnalise
5. Parite py/sh : le .sh est un wrapper pur (exec python3) -- aucune divergence de logique possible
6. La detection des chemins (BFS) reprend la logique de `generateurs-carte analyser` (reutilisation, pas de reimplementation)

---

## Emplacement des fichiers

| Fichier | Chemin |
|---|---|
| Outil python | `agents/tools/cartographier/cartographier-parcours/cartographier-parcours.py` |
| Outil bash | `agents/tools/cartographier/cartographier-parcours/cartographier-parcours.sh` (parite) |
| Documentation | `agents/tools/cartographier/cartographier-parcours/cartographier-parcours.md` |

---

## Versionning

| Version | Statut | Changements |
|---|---|---|
| 0.1.0 | ebauche | Creation : cartographie d'un parcours en fichier markdown (arbre ASCII avec types/branches/fins + convergences marquees, impasses, boucles, chemins BFS), sortie par defaut dans le dossier du parcours audite, --sortie, --dry-run, parite py/sh (wrapper pur), lecture seule | 
