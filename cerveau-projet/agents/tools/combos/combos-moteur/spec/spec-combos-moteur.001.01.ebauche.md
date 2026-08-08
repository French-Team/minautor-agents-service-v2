---
identite:
  type: spec
  appartient_a: commun
  commun: true
---
# Specification -- combos-moteur

**Statut :** ebauche
**Version :** 0.2.0-ebauche
**Categorie :** combos
**Date :** 2026-08-08

---

## Objectif

Executer des **chaines d'outils declaratives** (combos) avec passage de variables
entre les cases. L'agent lance UN combo au lieu d'une suite d'outils : plus
transparent, plus fiable, plus digeste.

**Principe fondateur** : un combo est un fichier `definition-combo.json` lu par un
**moteur generique** (`combos-moteur`), exactement comme `guider-parcours` lit un
`parcours-<agent>.json`. Chaque case fournit un resultat dans une variable, la
variable est transmise a la case suivante. Le generateur de commande
(`generateurs-commande`) est utilise en mode **AUTO** dans les cases `generateur` :
le moteur l'appelle avec `--reponses` alimente par les variables du combo. Le
generateur n'est PAS modifie : c'est le moteur qui fait le lien.

## Architecture (decision utilisateur 2026-08-08)

| Decision | Choix |
|---|---|
| **Architecture** | Combo DECLARATIF (JSON) + moteur generique (un moteur pour tous les combos) |
| **Variables** | Memoire INTERNE du combo (dict) ; persistance optionnelle vers classeur-variables |
| **Generateur** | INCHANGE -- le moteur l'appelle avec `--reponses` (mode AUTO) |

## Fonctionnalites

| # | Fonctionnalite | Detail |
|---|---|---|
| 1 | Definition | `definition-combo.json` : combo + cases + entrees/sorties |
| 2 | Case generateur | Appelle `generateurs-commande --commande <nom> --reponses "cle=valeur;..."` avec les entrees -> sortie = commande composee |
| 3 | Case outil | Execute la commande (subprocess), capture la sortie -> sortie = resultat |
| 4 | Case critere | Evalue une condition AUTOMATIQUEMENT (fichier-existe, sortie-contient, egalite, non-vide) et suit vers-vrai/vers-faux SANS question humaine |
| 5 | Case controle | Question + branches (OUI/NON/choix) selon la reponse ou une variable |
| 6 | Case fin | Message de fin, retourne le resultat final |
| 7 | Variables | Memoire interne : chaque sortie alimente une variable, interpolation `{var}` |
| 8 | Interpolation | `{nom}` remplace par la valeur de la variable dans commandes, entrees et conditions (lettres, chiffres, tirets, underscores) |
| 9 | Mode liste | `--liste` : afficher les cases sans executer |
| 10 | Mode reponses | `--reponses 'cle=valeur;...'` : resoudre les controles sans interaction |
| 11 | Mode dry-run | `--dry-run` : afficher les commandes a executer sans les lancer |
| 12 | Parite .py/.sh | Les deux versions lisent la meme definition et produisent la meme execution |
| 13 | Persistance | Option `persistant: true` sur une sortie -> ecriture dans classeur-variables |

## Format de la definition (definition-combo.json)

```json
{
  "combo": {
    "nom": "combo-activation",
    "description": "Cycle d'activation : sidentifier -> activer -> reactiver",
    "version": "0.1.0",
    "case_depart": "c1"
  },
  "cases": {
    "c1": {
      "titre": "Generer la commande sidentifier",
      "type": "generateur",
      "catalogue": "activer-sidentifier",
      "entrees": { "id_llm": "llm-1" },
      "sortie": "cmd1",
      "suivant": "c2"
    },
    "c2": {
      "titre": "Executer sidentifier",
      "type": "outil",
      "commande": "{cmd1}",
      "sortie": "session",
      "suivant": "c3"
    },
    "c3": {
      "titre": "Generer la commande activer",
      "type": "generateur",
      "catalogue": "activer-activer",
      "entrees": { "session": "{session}", "agent": "Buffy", "raison": "Mission" },
      "sortie": "cmd2",
      "suivant": "c4"
    },
    "c4": {
      "titre": "Executer activer",
      "type": "outil",
      "commande": "{cmd2}",
      "sortie": "ok",
      "suivant": "c5"
    },
    "c5": {
      "titre": "FIN",
      "type": "fin",
      "message": "Cycle d'activation termine."
    }
  }
}
```

## Types de cases

| Type | Champ(s) requis | Comportement | Sortie |
|---|---|---|---|
| `generateur` | `catalogue`, `entrees`, `sortie` | Appelle `generateurs-commande --commande <catalogue> --reponses "<entrees>"` | commande composee (texte) |
| `outil` | `commande`, `sortie` | Execute la commande (subprocess), capture stdout+stderr | resultat (texte) |
| `critere` | `condition`, `vers-vrai`, `vers-faux` | Evalue une condition AUTOMATIQUEMENT et suit la branche sans question humaine | aucune (branche vers `vers-vrai`/`vers-faux`) |
| `controle` | `question`, `branches` | Pose une question ; la reponse (via `--reponses` ou interaction) selectionne la branche | aucune (branche vers `vers`) |
| `fin` | `message` | Termine le combo et affiche le message | aucune |

### Case critere -- branchement automatique (v0.2.0)

La case **critere** repond a la decision utilisateur "les criteres ne seront pas
utilises dans les cartes de decision mais plutot dans les combos et les outils" :
le moteur evalue une condition sur les donnees (fichiers, variables, sorties)
et suit `vers-vrai` ou `vers-faux` -- sans poser de question a l'agent.

```json
{
  "titre": "Le fichier existe ?",
  "type": "critere",
  "condition": {
    "type": "fichier-existe",
    "chemin": "{chemin-cible}"
  },
  "vers-vrai": "c4",
  "vers-faux": "c5"
}
```

**Conditions supportees** (`condition.type`) :

| Condition | Champs | VRAI quand |
|---|---|---|
| `fichier-existe` | `chemin` | le fichier (interpole) existe sur le disque |
| `fichier-contient` | `chemin`, `texte` | le fichier contient le texte |
| `sortie-contient` | `source`, `texte` | la valeur de `source` contient `texte` |
| `egalite` | `variable`, `valeur` | la variable vaut exactement `valeur` |
| `non-vide` | `variable` | la variable existe et n'est pas vide |

Validation : une case `critere` DOIT avoir `condition.type` connu et `vers-vrai`
et `vers-faux` pointant vers des cases existantes (sinon erreur au chargement).

### Case controle -- branches

```json
{
  "titre": "Resultat utilisable brut ?",
  "type": "controle",
  "question": "Le resultat peut-il etre utilise directement par l'outil suivant ?",
  "branches": [
    { "reponse": "OUI", "vers": "c6" },
    { "reponse": "NON", "vers": "c5b" }
  ]
}
```

Le principe du dataflow : si le resultat d'une case peut etre utilise **brut**
par la case outil suivante, il est envoye directement (la variable est
interpolee dans la commande suivante). Si un generateur est necessaire pour
composer la commande de l'outil suivant, une case `generateur` s'intercale.

## Variables et interpolation

- Chaque case `generateur` / `outil` declare une `sortie` (nom de variable).
- Le moteur stocke les sorties dans une memoire interne (dict).
- Dans les `commande` et `entrees` des cases suivantes, `{nom}` est remplace
  par la valeur de la variable `nom`.
- Une variable non trouvee -> erreur claire (code retour 1).
- Option `persistant: true` sur une sortie -> la valeur est ecrite dans le
  classeur-variables (`stockage/variables-actuelles.md`) apres execution.

## Interface

```bash
python3 combos-moteur.py <definition-combo.json> [--liste] [--reponses 'cle=valeur;...'] [--dry-run] [--version]
bash combos-moteur.sh <definition-combo.json> [--liste] [--reponses 'cle=valeur;...'] [--dry-run] [--version]
```

| Option | Description | Defaut |
|---|---|---|
| `<definition>` | Chemin du fichier definition-combo.json | obligatoire |
| `--liste` | Lister les cases sans executer | false |
| `--reponses 'a=b;c=d'` | Reponses des controles fournies en une fois | - |
| `--dry-run` | Afficher les commandes sans les executer | false |
| `--verbose` | Afficher les details de chaque case | false |
| `--version` | Afficher la version | - |

## Relation avec les autres outils

| Outil | Role dans le combo |
|---|---|
| `generateurs-commande` | Compose les commandes (mode AUTO via `--reponses`) dans les cases `generateur` |
| `guider-parcours` | Guide l'agent case par case ; une case de parcours peut pointer vers un combo |
| `classeur-variables` | Persistance optionnelle des sorties (`persistant: true`) |
| `combos-audit-general` | Exemple de combo existant (orchestrateur subprocess) |

## Regle d'utilisation : citer le combo avant de le lancer

> **REGLE (IMMUABLE, protocole-creation-combos 9.5)** : avant d'executer un
> combo, l'agent ANNOUNCE le nom du combo et le chemin de sa definition.
> Format : `Je lance le combo <nom> : <chemin> - il enchaine <outils>.`

**Pourquoi** : tracabilite des executions -- l'utilisateur, Cerberus et Janus
voient QUEL combo est lance, pas seulement la commande combos-moteur.

**Exemple** :

```
Je lance le combo combo-controle-outil : cerveau-projet/combos/combo-controle-outil/definition-combo.json - il enchaine : valider-conformite-ascii -> valider-cartes-decision -> valider-liens.
```

**Rappel** : en tete des indices des cases combo des parcours (Pattern 3) :
themis c3, janus c5/c22, vulcain c7/c13, buffy c28.

---

## Tests requis

| Cas | Attendu |
|---|---|
| Liste | `--liste` affiche toutes les cases de la definition |
| Navigation | Les cases s'enchainent de `case_depart` jusqu'a une case `fin` |
| Interpolation | `{var}` remplace par la valeur de la variable dans la commande |
| Generateur AUTO | Le moteur appelle `generateurs-commande --reponses` et obtient la commande |
| Critere fichier-existe | fichier present -> vers-vrai ; absent -> vers-faux |
| Critere egalite/non-vide | variable == valeur -> vers-vrai ; sinon vers-faux |
| Critere sortie-contient | source contient texte -> vers-vrai ; sinon vers-faux |
| Critere fichier-contient | fichier contient texte -> vers-vrai ; sinon vers-faux |
| Interpolation tirets | `{ma-variable}` (kebab-case) remplace par la valeur |
| Controle branches | `--reponses 'resultat=OUI'` -> branche OUI ; 'NON' -> branche NON |
| Variable manquante | Erreur claire, code retour 1 |
| Fin | Le combo s'arrete a la case `fin` et affiche le message |
| Dry-run | Aucune commande executee, toutes affichees |
| Parite | `.py` et `.sh` produisent la meme navigation et les memes commandes |
| Nommage | valider-nommage OK (dossier combos/ -> prefixe combos-) |
| ASCII | 0 caractere non-ASCII |
| Syntaxe | bash -n OK, python3 -m py_compile OK |

## Livrables

- `combos-moteur.sh` (bash)
- `combos-moteur.py` (python)
- `spec/spec-combos-moteur.001.01.ebauche.md` (ce fichier)
- (la definition d'un combo est un fichier du cerveau, cree par Buffy selon
  le protocole-creation-combos : `cerveau-projet/combos/<combo-nom>/definition-combo.json`
  -- voir [protocole-creation-combos](../../../../../agents/regles-immuables/general/protocole-creation-combos/protocole-creation-combos.001.01.ebauche.md))

## Notes de creation

- [ ] Le moteur a ete teste sur un combo pilote (ex: combo-activation)
- [ ] Le moteur est conforme ASCII -- valider avec `valider-conformite-ascii`
- [ ] Le moteur est reference dans `index-tools.md`
- [ ] Le Pattern 3 (generateur -> execution) est documente dans spec-guider-parcours
