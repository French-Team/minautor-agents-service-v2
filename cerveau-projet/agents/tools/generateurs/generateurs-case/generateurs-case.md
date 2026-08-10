---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# generateurs-case

| Champ | Valeur |
|---|---|
| **Version** | 0.4.0 |
| **Statut** | ebauche |
| **Categorie** | generateurs |
| **Derniere mise a jour** | 2026-08-08 |
| **Python** | generateurs-case.py |
| **Bash** | generateurs-case.sh (parite) |

---

## Description

**Generateur de cases pour cartes de decision (parcours JSON).** Permet de
charger la carte de decision d'un agent (`parcours-<agent>.json`), d'ajouter
une case a la position voulue, d'editer une case existante et de supprimer une
case AVEC RECABLAGE AUTOMATIQUE des references (suivant / branches[].vers /
case_depart). Chaque operation declenche une VALIDATION AUTO COMPLETE :
json.load + references + case_depart + `guider-parcours --liste`.

**Pourquoi cet outil ?** Buffy modifie regulierement les cartes de decision
des agents. Un editeur naif casse les liens entre cases (suivant, vers). Ce
generateur garantit l'integrite des references et le respect du format
documente dans la spec-guider-parcours (v0.2.5, 4 patterns).

**Quand l'utiliser ?** Quand un agent doit ajouter, editer ou supprimer une
case dans sa carte de decision. C'est Buffy qui utilise cet outil pour
modifier les cartes des agents (fichiers du cerveau).

---

## Utilisation

### CLI Python

```
python3 generateurs-case.py <parcours.json> <action> [options]

Actions :
  liste           Lister les cases de la carte
  ajouter         Ajouter une case (position + contenu)
  ajouter-bloc    Ajouter un bloc modele compose (decision + deviation + rejoint, Pattern 7)
  editer          Editer une case existante
  supprimer       Supprimer une case avec recablage auto

Options globales :
  --dry-run  Simuler sans rien modifier
  --verbose  Afficher les details
  --version  Afficher la version
```

### CLI bash

```
bash generateurs-case.sh <parcours.json> <action> [options]
```

Memes actions et options que la version Python (parite).

---

## Actions detaillees

### 1. Lister les cases (charger la carte)

```
python3 generateurs-case.py cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json liste
```

Affiche le nom du parcours, sa version, l'agent, la case de depart et la liste
des cases (id, type, titre) -- la case de depart est marquee (depart).

### 2. Ajouter une case

```
python3 generateurs-case.py <parcours.json> ajouter \
  --type indice --titre "Verifier le rapport" \
  --suivant c9 \
  --indice-regle "REGLE : verifier avant d'agir" \
  --apres c8
```

| Option | Role |
|---|---|
| `--type <question\|indice\|controle\|fin>` | Type de la case (obligatoire) |
| `--case <id>` | Id de la nouvelle case (defaut: prochain cN libre) |
| `--titre <texte>` | Titre de la case |
| `--question <texte>` | Question (types question/controle) |
| `--message <texte>` | Message (type fin) |
| `--suivant <id>` | Case suivante (types indice/question/controle) |
| `--apres <id>` | Inserer apres cette case (recablage auto du suivant) |
| `--branche <reponse>:<vers>` | Branche (repetable) |
| `--indice-regle <texte>` | Indice regle (repetable) |
| `--ref <ref>` | Indice REFERENCE (repetable) -- allegement (spec-refonte-cartes-decision 7.1) : `pattern-<N>`, `protocole-<x>`, `regle-<x>` ou chemin relatif ; verifie par `valider-case --references` |
| `--indice-outil <nom>:<chemin>[:commande]>` | Indice outil (repetable) -- ajoute automatiquement l'indice fichier du `.md` (Pattern 9 : LIRE AVANT USAGE) si la doc existe |
| `--indice-fichier <chemin>:<raison>` | Indice fichier (repetable) |

**Types et contraintes :**

| Type | Contraintes |
|---|---|
| `question` | `--question` obligatoire ; `--branche` ou `--suivant` |
| `indice` | `--suivant` obligatoire ; indices libres |
| `controle` | `--question` + `--branche` ou `--suivant` obligatoires |
| `fin` | Aucune contrainte (message optionnel) |

### 3. Editer une case existante

```
python3 generateurs-case.py <parcours.json> editer c6 \
  --titre "Developper l'outil (v2)" --question "Python est-il disponible ?"
```

| Option | Role |
|---|---|
| `case_id` | Id de la case a editer (positionnel) |
| `--titre / --question / --message / --suivant / --type` | Champs a modifier |
| `--branche <reponse>:<vers>` | Remplace TOUTES les branches |
| `--indice-regle <texte>` | Remplace les indices par des regles |
| `--remove-indices` | Vider les indices |

### 5. Ajouter un bloc modele compose COMPLET (Pattern 7 + spec-refonte 7.1) -- action `ajouter-bloc`

Cree d'un coup les 3 cases du MODELE COMPOSE COMPLET : decision (question,
branches min 2, extensible) + deviation + rejoint. Les indices deviation et
rejoint portent des REFERENCES (`pattern-7` par defaut) au lieu de textes
inline -- c'est l'allegement : `valider-case` ne signale plus de surcharge.

```
python3 generateurs-case.py <parcours.json> ajouter-bloc \
  --titre "Erreurs hors mission ?" \
  --question "Des erreurs HORS MISSION ont-elles ete signalees ?" \
  --suite c13 \
  --apres c12 \
  --branche "PEUT_ETRE:c14"
```

Structure creee (ids par defaut : prochains cN libres + suffixes a/b) :

```
<decision> (question, branches min 2) :
  OUI -> <deviation> (indice, ref pattern-7) -> <rejoint> (indice) -> <suite>
  NON -> <suite>  (flux principal)
  <branches supplementaires --branche reponse:vers>
```

| Option | Role |
|---|---|
| `--decision <id>` | Id de la case decision (defaut: prochain cN libre) |
| `--deviation <id>` | Id de la deviation (defaut: <decision>a) |
| `--rejoint <id>` | Id du rejoint (defaut: <decision>b) |
| `--titre <texte>` | Titre de la decision |
| `--question <texte>` | Question de la decision (defaut: Quelle est la decision ?) |
| `--titre-deviation <texte>` | Titre de la deviation (defaut: DEVIATION : workflow secondaire) |
| `--titre-rejoint <texte>` | Titre du rejoint (defaut: REJOINT : retour au flux principal) |
| `--suite <id>` | Case suite du flux principal (OBLIGATOIRE, cible des branches NON et du rejoint) |
| `--branche <reponse>:<vers>` | Branche SUPPLEMENTAIRE (repetable, en plus de OUI/NON) |
| `--ref-deviation <ref>` | Reference de l indice deviation (defaut: pattern-7) |
| `--ref-rejoint <ref>` | Reference de l indice rejoint (defaut: pattern-7) |
| `--apres <id>` | Inserer apres cette case (recablage auto du suivant) |

> La deviation porte l indice REFERENCE `pattern-7` : jamais une fin au milieu,
> jamais une boucle d'attente (regle 10) -- le workflow secondaire se termine
> toujours par le REJOINT vers la suite du flux. Chaque commande declenche la
> validation auto, y compris `valider-case --modele` (spec-refonte 7.1).

### 4. Supprimer une case (recablage auto)

```
python3 generateurs-case.py <parcours.json> supprimer c7
```

**Recablage automatique** (decision utilisateur) :
- Toutes les references `suivant` / `branches[].vers` qui pointaient vers la
  case supprimee sont REDIRIGEES vers la cible (par defaut : le `suivant` de
  la case supprimee, sinon `--vers <id>`).
- Si la case supprimee est la `case_depart`, le depart devient la cible.
- Une case `fin` sans `suivant` exige `--vers <id>` (impossible de recabler
  automatiquement vers un vide).

| Option | Role |
|---|---|
| `case_id` | Id de la case a supprimer (positionnel) |
| `--vers <id>` | Cible de recablage (defaut: le suivant de la case supprimee) |
| `--force` | Forcer malgre les references (recablage auto quand meme) |

---

### 6. Convertir en masse (mode batch) -- action `convertir` (v0.4.0)

Migration de parcours : convertit TOUTES les cases `indice` en `action`
(elles n attendent pas de reponse) et remplace les regles longues (> seuil,
defaut 160 caracteres) par des references via un fichier de mapping JSON.

    python3 generateurs-case.py <parcours.json> convertir [--refs <mapping.json>]
                                [--seuil N] [--version-parcours <v>] [--dry-run]

- `--refs <mapping.json>` : mapping des refs. Format :
  { "motifs": [ {"contient": "<motif>", "ref": "pattern-2"}, ... ],
    "cases": { "<case_id>": "protocole-tests" } }
  Les refs par case_id ont priorite ; sinon premier motif contenu gagnant.
- `--seuil` : longueur max d une regle avant remplacement par ref (defaut 160).
- `--version-parcours <v>` : bump de la version du parcours.
- `--dry-run` : simule et affiche le rapport SANS ecrire (dry/wet).
- Rapport final : X cases converties, Y regles remplacees, Z avertissements
  (regles longues sans mapping, cases > 3 indices) - l agent raccourcit ou
  complete le mapping puis relance.

Le recablage (suivant/branches) est conserve A L IDENTIQUE : une conversion
indice -> action ne change pas la navigation. Validation auto lancee apres
l ecriture (references + guider-parcours --liste + valider-case --modele).

## Garde-fou Pattern 5 (v0.1.1-beta) -- jamais de fin passive

Quand on cree ou edite une case de type `fin` (ajouter/editer avec --message),
l'outil detecte les formulations passives bloquantes qui COUPENT LA CHAINE de
delegation (Pattern 5, spec-guider-parcours v0.2.6) : `te reactive`,
`il/elle me reactive`, `j'attends`, `attend le retour`, `attendre le retour`,
`en attente de`, `tu seras reactive`...

Si une telle formulation est trouvee, l'outil affiche un AVERTISSEMENT (jaune,
non bloquant) rappelant la regle : une delegation ne se termine JAMAIS par une
fin passive ('X te reactive') -- materialiser la boucle RELAIS -> RETOUR ->
CLOTURE dans le parcours (voir parcours-vulcain v0.2.1). L'utilisateur decide
ensuite : corriger le message ou assumer le choix.

```bash
# Exemple : creation d'une fin passive -> avertissement affiche
python3 generateurs-case.py <parcours.json> ajouter --type fin \
  --titre 'FIN test' --message 'Morpheus teste et te reactive, attends le retour'
# -> ATTENTION (Pattern 5...) : le message de fin contient une formulation passive
```

## Garde-fou REGLES IMMUABLES (v0.2.1) -- RVAV + delegation + ASCII

**Constat utilisateur 2026-08-08** : RVAV et la delegation (tests -> Morpheus,
controle -> Janus) etaient absents des generateurs -> les nouvelles cartes et
cases produites ne rappelaient plus les regles immuables, et la chaine de
delegation se degradait silencieusement (l'agent testait lui-meme au lieu de
deleger a Morpheus, Janus n'etait jamais active).

A chaque creation/edition d'une case, l'outil affiche un AVERTISSEMENT (jaune,
NON BLOQUANT -- l'utilisateur decide) selon le type de case :

| Cas detecte | Rappel affiche |
|---|---|
| Case d'ECRITURE (indice outil d'ecriture : creer-fichier, ecrire-fichier, editer-fichier, ajouter-contenu-fichier, inserer-contenu-fichier, copier-fichier) sans rappel ASCII en tete | **RAPPEL ASCII** (Pattern 2) : la case DOIT porter en TETE de ses indices un indice regle `REGLE IMMUABLE ASCII` (100%% ASCII, guillemets ASCII, jamais de guillemets francais) |
| Case d'ecriture (ci-dessus) | **RAPPEL RVAV** : je ne valide JAMAIS sans avoir passe la boucle RVAV complete (Rechercher, Verifier, Analyser, Valider) sur mon travail |
| Case `fin` avec message de delegation (morpheus/janus/active/reactive) | **RAPPEL DELEGATION** (chaine bout-en-bout, spec-guider-parcours v0.2.15) : j ACTIVE le maillon suivant a MA fin (Vulcain active Morpheus -> Morpheus active Janus -> Janus REACTIVE Cerberus avec le bilan consolide) ; chaque maillon passe la boucle RVAV AVANT d'activer le suivant ; une activation directe par Cerberus reste valide |
| Case `fin` (autre) | **RAPPEL RVAV** avant d'activer le maillon suivant |

```bash
# Exemple : ajouter une fin de delegation -> rappel delegation + RVAV
python3 generateurs-case.py <parcours.json> ajouter --type fin \
  --message 'J ACTIVE MORPHEUS pour les tests'
# -> ATTENTION (GARDE-FOU REGLES IMMUABLES...) : RAPPEL DELEGATION ...
```

> Le rappel est NON BLOQUANT : l'operation reussit quand meme. L'agent qui
> utilise l'outil est averti et doit appliquer la regle (ajouter l'indice
> ASCII/RVAV ou materialiser la chaine) dans le contenu de sa case.

## Validation auto complete (apres chaque operation)

1. **json.load** : le fichier est recharge et valide (JSON valide)
2. **References** : `suivant` / `branches[].vers` / `case_depart` pointent vers
   des cases existantes -- erreur listee sinon
3. **guider-parcours --liste** : l'outil guider-parcours est relance sur le
   fichier modifie pour confirmer que la structure est chargeable

> **REGLE ASCII** : le contenu JSON est ecrit en ASCII strict (ensure_ascii).
> Un contenu non-ASCII est refuse avant ecriture (regle immuable).

### Validateur-case (v0.3.0, spec-refonte 7.1)

Chaque commande de modification declenche la validation auto, qui inclut
maintenant `valider-case <parcours> --modele --dry-run` : le modele compose
(branches min 2, rejoint present, deviation sans rejoint signalee) est verifie
a chaque fois. Un verdict NON CONFORME bloque l'operation (retour != 0).

---

## Exemples

### Ajouter une case apres c8 dans parcours-vulcain

```bash
python3 cerveau-projet/agents/tools/generateurs/generateurs-case/generateurs-case.py \
  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json ajouter \
  --type indice --titre "Verifier le rapport" --suivant c9 --apres c8 \
  --ref pattern-9
```

### Ajouter un bloc modele compose complet (allege par references)

```bash
python3 cerveau-projet/agents/tools/generateurs/generateurs-case/generateurs-case.py \
  cerveau-projet/agents/cerberus/parcours/parcours-cerberus.json ajouter-bloc \
  --titre "Erreurs hors mission ?" --question "Des erreurs HORS MISSION ?" \
  --suite c13 --apres c12 --branche "PEUT_ETRE:c14"
```

### Editer le titre d'une case

```bash
python3 cerveau-projet/agents/tools/generateurs/generateurs-case/generateurs-case.py \
  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json editer c6 \
  --titre "Developper l'outil (v2)"
```

### Supprimer une case (recablage auto)

```bash
python3 cerveau-projet/agents/tools/generateurs/generateurs-case/generateurs-case.py \
  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json supprimer c7
```

### Simuler sans modifier (--dry-run)

```bash
python3 cerveau-projet/agents/tools/generateurs/generateurs-case/generateurs-case.py \
  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json supprimer c7 --dry-run
```

---

## Regles

1. Le nom de l'outil DOIT commencer par le prefixe du dossier (`generateurs-`) -- controle au demarrage (verifier_nommage)
2. Le JSON est ecrit en ASCII strict (ensure_ascii + verif avant ecriture)
3. Toute suppression recable les references vers la cible (suivant de la case ou --vers)
4. Chaque operation lance la validation auto (json + references + guider-parcours --liste)
5. Les actions sont testees en --dry-run avant toute modification reelle
6. Format des cases : spec-guider-parcours v0.5.0 (types question/indice/controle/fin/action, indices, branches, suivant)
7. Garde-fou REGLES IMMUABLES (v0.2.1) : toute case d'ecriture rappelle ASCII (position 1) + RVAV ; toute fin de delegation rappelle la chaine bout-en-bout (spec v0.2.15)

---

## Emplacement des fichiers

| Fichier | Chemin |
|---|---|
| Outil python | `agents/tools/generateurs/generateurs-case/generateurs-case.py` |
| Outil bash | `agents/tools/generateurs/generateurs-case/generateurs-case.sh` (parite) |
| Documentation | `agents/tools/generateurs/generateurs-case/generateurs-case.md` |

---

## Versionning

| Version | Statut | Changements |
|---|---|---|
| 0.1.0-beta | ebauche | Creation : charger une carte, ajouter/editer/supprimer une case, recablage auto des references, validation auto complete (json + refs + guider-parcours --liste), parite py/sh |
| 0.1.1-beta | ebauche | Garde-fou Pattern 5 : detection des formulations passives a la creation/edition d'une case fin |
| 0.2.0 | ebauche | Action ajouter-bloc : bloc MODELE COMPOSE (Pattern 7) cree d'un coup (decision 2 branches + deviation + rejoint), spec-guider-parcours v0.2.13 |
| 0.2.1 | ebauche | Garde-fou REGLES IMMUABLES : a la creation/edition d'une case d'ecriture ou d'une fin, rappel ASCII (Pattern 2, position 1) + RVAV + delegation (chaine bout-en-bout spec-guider-parcours v0.2.15 : tests -> Morpheus, controle -> Janus, bilan consolide a Cerberus) |
| 0.2.2 | ebauche | Pattern 9 (spec-guider-parcours v0.2.16) : tout `--indice-outil` ajoute automatiquement l'indice fichier du `.md` de l'outil (LIRE AVANT USAGE) si la doc existe -- portee SYSTEMATIQUE, decision utilisateur 2026-08-08 |
