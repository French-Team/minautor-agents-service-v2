---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# generateurs-carte

| Champ | Valeur |
|---|---|
| **Version** | 0.3.0 |
| **Statut** | ebauche |
| **Categorie** | generateurs |
| **Derniere mise a jour** | 2026-08-09 |
| **Python** | generateurs-carte.py |
| **Bash** | generateurs-carte.sh (parite) |

---

## Description

**Agit sur une CARTE DE DECISION COMPLETE (parcours JSON)** : creer un
squelette conforme aux 11 patterns (dont 4-5-6-7-8-10-3), analyser les
chemins de `case_depart` aux fins, detecter les anomalies (boucles, cases
inatteignables, impasses, references cassees), dupliquer un chemin (groupe de
cases) avec recablage et prefixe.

**Complementaire de `generateurs-case`** : `generateurs-case` agit sur UNE case
(ajouter/editer/supprimer), `generateurs-carte` agit sur la carte COMPLETE
(creer/analyser/detecter/dupliquer-chemin).

**Pourquoi cet outil ?** Le Pattern 7 (modele compose, spec-guider-parcours
v0.2.13) rend les cartes plus dynamiques (decisions a 2+ branches, deviations
avec retour). Construire et maintenir ces cartes a la main est source d'erreurs
(boucles, cases orphelines) : cet outil automatise la creation, l'analyse et la
duplication avec validation auto.

---

## Utilisation

### CLI Python

```
python3 generateurs-carte.py <action> [options]

Actions :
  creer              Creer une carte squelette complete (patterns 4-5-6-7)
  analyser           Lister tous les chemins de case_depart aux fins
  detecter           Detecter les anomalies (boucles, inatteignables, impasses)
  dupliquer-chemin   Dupliquer un chemin (groupe de cases) avec recablage
```

### CLI bash

```
bash generateurs-carte.sh <action> [options]
```

Memes actions et options que la version Python (parite).

---

## Actions detaillees

### 1. Creer une carte squelette

```
python3 generateurs-carte.py creer <chemin> --agent <nom> [--nom <parcours>] [--version 0.1.0] [--description "..."] [--force]
```

Cree une carte complete avec les cases conformes aux patterns. Les indices
portent des REFERENCES (cle `ref`, resolues par `valider-case --references`) au
lieu de textes inline : le squelette nait ALLEGE (verdict CONFORME, 0 a alleger).

| Case | Type | Role |
|---|---|---|
| `c0` | question | Relecture honnete (Pattern 4) : OUI -> c0c, INCERTAIN/NON -> c0b (ref protocole-activation) |
| `c0b` | indice | RELIRE OBLIGATOIRE : corrections puis fiche (ref protocole-activation + 2 outils lire-fichier) |
| `c0c` | indice | CONTEXTE temps reel (ref pattern-6 + outil lire-activite-recente + AGENTS.md) |
| `c1` | question | Mission (ref pattern-10 UNE CARTE = UN ROLE) : branches a definir |
| `c2` | indice | Exemple d'action a completer (refs pattern-3, pattern-7, pattern-2) |
| `c2b` | indice | RVAV avant activation (ref rvav-workflow.md) |
| `c9` | fin | FIN - Mission terminee (Pattern 5 : fin active) |

`case_depart` vaut `c0`. Le fichier doit etre cree dans
`cerveau-projet/agents/<agent>/parcours/parcours-<agent>.json`.

### 2. Analyser les chemins

```
python3 generateurs-carte.py analyser <parcours.json>
```

Liste TOUS les chemins de `case_depart` vers les cases `fin` (BFS avec limite
anti-boucle). Affiche pour chaque chemin : la case finale et la suite des cases
traversees. Les impasses (case sans sortie) sont marquees `[impasse]`.

### 3. Detecter les anomalies

```
python3 generateurs-carte.py detecter <parcours.json>
```

Detecte et affiche :

1. **Anomalies structurelles locales** (boucles d'attente, cases inatteignables,
   sans sortie, references cassees, decision a branche unique)
2. **Verifications deleguees au validateur-case** (spec-refonte 7.2, source
   unique de verite) : modele compose, surcharge des indices, references des
   indices -- le verdict `valider-case` est affiche en complement

### 4. Dupliquer un chemin

```
python3 generateurs-carte.py dupliquer-chemin <parcours.json> --debut <case> --fin <case> [--prefixe d] [--brancher-debut]
```

Duplique le groupe de cases du chemin `--debut` -> `--fin` (BFS) :

- Les nouveaux ids = `<prefixe><id>` (ex: `dc5`, `dc6`...)
- Les references INTERNES au chemin sont recablees vers les copies
- Les references externes restent sur les originales (sauf `--brancher-debut`
  qui fait pointer l'original du debut vers la copie)
- Les indices REFERENCES sont CONSERVES tels quels (aucun texte inline a
  dupliquer -- spec-refonte 7.2 : la copie porte les memes refs, rien ne derive)
- Validation auto complete (json + references + guider-parcours --liste +
  validateur-case --modele --references)

---

## Validation auto complete (apres chaque operation d'ecriture)

1. **json.load** : le fichier est recharge et valide (JSON valide)
2. **References** : `suivant` / `branches[].vers` / `case_depart` pointent vers
   des cases existantes -- erreur listee sinon
3. **guider-parcours --liste** : l'outil guider-parcours est relance sur le
   fichier modifie pour confirmer que la structure est chargeable
4. **validateur-case --modele --references** : verifications du modele compose
   et des references d'indices (spec-refonte 7.2) -- un verdict NON CONFORME
   bloque l'operation

> **REGLE ASCII** : le contenu JSON est ecrit en ASCII strict (ensure_ascii).
> Un contenu non-ASCII est refuse avant ecriture (regle immuable).

---

## Exemples

### Creer le squelette d'une carte pour un nouvel agent

```bash
python3 cerveau-projet/agents/tools/generateurs/generateurs-carte/generateurs-carte.py \
  cerveau-projet/agents/<agent>/parcours/parcours-<agent>.json creer --agent <agent>
```

### Analyser les chemins d'une carte existante

```bash
python3 cerveau-projet/agents/tools/generateurs/generateurs-carte/generateurs-carte.py \
  cerveau-projet/agents/cerberus/parcours/parcours-cerberus.json analyser
```

### Detecter les anomalies avant un audit

```bash
python3 cerveau-projet/agents/tools/generateurs/generateurs-carte/generateurs-carte.py \
  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json detecter
```

### Dupliquer un chemin (deviation) avec prefixe

```bash
python3 cerveau-projet/agents/tools/generateurs/generateurs-carte/generateurs-carte.py \
  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json dupliquer-chemin \
  --debut c4 --fin c6 --prefixe d --dry-run
```

### Simuler sans modifier (--dry-run)

```bash
python3 cerveau-projet/agents/tools/generateurs/generateurs-carte/generateurs-carte.py \
  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json creer <chemin> --dry-run
```

---

## Regles

1. Le nom de l'outil DOIT commencer par le prefixe du dossier (`generateurs-`) -- controle au demarrage (verifier_nommage)
2. Le JSON est ecrit en ASCII strict (ensure_ascii + verif avant ecriture)
3. Chaque operation de creation/duplication lance la validation auto (json + references + guider-parcours --liste)
4. Les actions sont testees en --dry-run avant toute modification reelle
5. L'analyse et la detection sont en LECTURE SEULE (aucune modification)
6. Format des cases : spec-guider-parcours v0.5.0 (types question/indice/controle/fin/action, indices, branches, suivant, Pattern 7 modele compose)

---

## Emplacement des fichiers

| Fichier | Chemin |
|---|---|
| Outil python | `agents/tools/generateurs/generateurs-carte/generateurs-carte.py` |
| Outil bash | `agents/tools/generateurs/generateurs-carte/generateurs-carte.sh` (parite) |
| Documentation | `agents/tools/generateurs/generateurs-carte/generateurs-carte.md` |

---

## Versionning

| Version | Statut | Changements |
|---|---|---|
| 0.1.0 | ebauche | Creation : creer (squelette patterns 4-5-6-7), analyser (chemins BFS), detecter (5 types d'anomalies), dupliquer-chemin (recablage + prefixe), validation auto, parite py/sh |
| 0.1.1 | ebauche | Squelette creer ENRICHI (regles immuables) : case c2b RVAV avant la fin (boucle Rechercher/Verifier/Analyser/Valider + fichier rvav-workflow) + rappel ASCII dans c2 + fin c9 rappelant la chaine bout-en-bout (spec-guider-parcours v0.2.15 : J ACTIVE le maillon suivant a MA fin, dernier maillon REACTIVE Cerberus avec bilan consolide) -- constat utilisateur 2026-08-08 : les nouvelles cartes ne rappelaient plus RVAV ni la delegation |
| 0.2.0 | ebauche | Squelette creer CONFORME AUX 11 PATTERNS : indice Pattern 10 UNE CARTE = UN ROLE ajoute en tete des indices de c1 (la carte ne contient QUE des actions propres au role de l agent, jamais d outils d analyse/execution d un autre role, piege du glissement lire pour decider vs lire pour executer) + indice Pattern 3 RAPPEL DES COMBOS ajoute en tete des indices de c2 (une suite lineaire d outils repetee ou longue doit etre encapsulee dans un combo Lancer le combo X : combos-moteur + definition-combo.json, protocole-creation-combos) -- decision utilisateur 2026-08-08 : les nouvelles cartes doivent naitre conformes au Pattern 10 et au Pattern 3 (spec-guider-parcours v0.2.19) |
