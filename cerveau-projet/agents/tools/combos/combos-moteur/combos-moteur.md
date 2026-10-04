---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# combos-moteur

| Champ | Valeur |
|---|---|
| **Version** | 0.3.3 |
| **Statut** | ebauche |
| **Categorie** | combos |
| **Derniere mise a jour** | 2026-08-13 |
| **Spec** | [spec-combos-moteur.001.01.ebauche.md](spec/spec-combos-moteur.001.01.ebauche.md) (v0.2.1) |

---

## Description

**Moteur generique de combos declaratifs.** Execute une chaine d'outils
(`definition-combo.json`) case par case, avec passage de variables entre les
cases. L'agent lance UN combo au lieu d'une suite d'outils : plus transparent,
plus fiable, plus digeste.

C'est la reponse au probleme des enchainements d'outils repetes a la main :
au lieu de dire a l'agent "outil 1 puis outil 2 puis outil 3", on lui dit
"lance le combo X" et le moteur enchaine les cases en transmettant les
resultats.

---

## Principe

```
definition-combo.json   (source de verite du combo : objet combo + cases)
        |
        v
combos-moteur.py <definition-combo.json>
        |
        v
CASE 1 : generateur  -> generateurs-commande --reponses (mode AUTO)
        |              -> sortie = commande composee (variable V1)
        v
CASE 2 : outil       -> execute la commande {V1} (subprocess)
        |              -> sortie = resultat (variable V2)
        v
CASE 3 : critere     -> evalue une condition AUTOMATIQUEMENT (fichier-existe,
        |              -> sortie-contient, egalite, non-vide...) puis suit
        v              -> vers-vrai ou vers-faux SANS question humaine
CASE 4 : controle    -> question + branches (OUI/NON/choix)
        |  reponse     -> si le resultat peut etre utilise BRUT, il est
        v              -> transmis directement ; sinon un generateur s'intercale
CASE 5 : fin         -> message de fin, retourne le resultat final
```

---

## Utilisation

### CLI Python (version 0.1.0-py)

```
python3 combos-moteur.py <definition-combo.json> [options]

Options :
  --liste           Lister les cases de la definition sans executer
  --reponses <liste> Reponses des controles d'un coup : case=reponse;case2=reponse2
  --var <cle=valeur> Variable initiale disponible pour {var} (repetable)
  --dry-run         Afficher les commandes a executer sans les lancer
  --no-journal      Desactiver la journalisation d usage (generateur)
  --verbose         Afficher les details de chaque case
  --version         Afficher la version
  --help            Afficher l'aide
```

### Variables initiales (--var)

Depuis la version 0.1.3, on peut fournir des variables au combo AVANT la
premiere case : `--var fichier=chemin/vers/fichier`. Elles sont disponibles
pour l'interpolation `{fichier}` dans toutes les commandes et entrees.

```bash
python3 combos-moteur.py cerveau-projet/combos/combo-controle-impacts/definition-combo.json \
  --var fichier=cerveau-projet/agents/cerberus/cerberus.md
```

Cela permet aux combos de recevoir un parametre d'entree (ex: le fichier
modifie pour `combo-controle-impacts`).

### CLI bash (version 0.1.0-sh)

```
bash combos-moteur.sh <definition-combo.json> [options]
```

Memes options que la version Python (parite).

---

## Format de la definition (definition-combo.json)

### Structure generale

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
      "titre": "Resultat utilisable brut ?",
      "type": "controle",
      "question": "Le resultat peut-il etre utilise directement ?",
      "branches": [
        { "reponse": "OUI", "vers": "c4" },
        { "reponse": "NON", "vers": "c3b" }
      ]
    },
    "c4": {
      "titre": "FIN",
      "type": "fin",
      "message": "Cycle d'activation termine."
    }
  }
}
```

### Types de cases

| Type | Champ(s) requis | Comportement | Sortie |
|---|---|---|---|
| `generateur` | `catalogue`, `entrees`, `sortie` | Appelle `generateurs-commande --commande <catalogue> --reponses "<entrees>"` (mode AUTO) | commande composee (texte) |
| `outil` | `commande`, `sortie` | Execute la commande (subprocess), capture stdout+stderr | resultat (texte) |
| `critere` | `condition`, `vers-vrai`, `vers-faux` | Evalue une condition AUTOMATIQUEMENT et suit la branche sans question humaine | aucune (branche vers `vers-vrai`/`vers-faux`) |
| `controle` | `question`, `branches` | Pose une question ; la reponse (via `--reponses` ou interaction) selectionne la branche | aucune (branche vers `vers`) |
| `fin` | `message` | Termine le combo et affiche le message | aucune |

### Case `generateur` -- mode AUTO

La case ne pose AUCUNE question : le moteur appelle `generateurs-commande`
avec `--reponses "cle=valeur;..."` alimente par les `entrees` (elles-memes
interpolees avec les variables precedentes). La commande composee est stockee
dans la variable `sortie` et servira a la case `outil` suivante via `{cmd}`.

### GARDE-FOU v0.3.0 : cles des entrees = cles exactes du catalogue

> **REGLE (spec-combos-moteur v0.2.1, lecon du KO test-003)** : les cles des
> `entrees` d'une case `generateur` DOIVENT etre les cles EXACTES des
> `parametres` de la commande ciblee dans `catalogue-commandes.json` (source
> de verite). Interdiction d'inventer une cle.

Au CHARGEMENT de la definition, le moteur verifie pour chaque case
`generateur` :

```
[ ] le catalogue cible existe dans catalogue-commandes.json
[ ] chaque cle des entrees est un parametre exact du catalogue
[ ] chaque parametre obligatoire du catalogue est fourni dans les entrees
```

En cas d'ecart -> ERREUR claire (combo, case, cles fautives) et code retour 1,
avant toute execution. Ce garde-fou empeche la recurrence du defaut test-003
(cles obsoletes `fichier`/`source`/`destination` vs catalogue).

> **Rappel** : les cles ne suivent aucune convention universelle
> (`fichier`/`chemin`/`source`/`destination`/`type`/`contenu`...) : toujours
> verifier `catalogue-commandes.json`, jamais supposer.

### Case `critere` -- branchement automatique (v0.2.0)

La case **critere** evalue une condition **automatiquement** (aucune question
humaine) et suit `vers-vrai` ou `vers-faux`. C'est l'embranchement
multi-directions par **criteres** : le moteur decide seul, en fonction de
donnees (fichiers, variables, sorties).

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

**Conditions supportees** (champ `condition.type`) :

| Condition | Champs | VRAI quand |
|---|---|---|
| `fichier-existe` | `chemin` | le fichier (interpole) existe sur le disque |
| `fichier-contient` | `chemin`, `texte` | le fichier contient le texte |
| `sortie-contient` | `source`, `texte` | la valeur de `source` (variable ou texte) contient `texte` |
| `egalite` | `variable`, `valeur` | la variable vaut exactement `valeur` |
| `non-vide` | `variable` | la variable existe et n'est pas vide |

L'interpolation `{var}` fonctionne dans tous les champs des conditions.

### ROBUSTESSE v0.3.2 : echec = arret, sauf `echec_ok` declare

> **REGLE (round 5)** : le code retour de chaque case `outil` est verifie.
> Un echec (exit != 0) ARRETE le combo avec un message explicite (case,
> commande, code, sortie) : un agent ne doit jamais croire qu'un combo a
> reussi alors qu'une etape a echoue (lecon round 4 : jamais de 0 silencieux).

Exception : une case peut declarer `"echec_ok": true` quand le code non nul
est un RESULTAT legitime -- les outils de controle/detection (valider-*,
detecter-*, verifier-*, rechercher-*) signalent un ecart par exit 1. Le
resultat est alors stocke normalement et le combo continue (l'agent analyse
les ecarts dans la case fin).

```json
{
  "titre": "Executer valider-conformite-ascii",
  "type": "outil",
  "commande": "python3 .../valider-conformite-ascii.py cerveau-projet/agents",
  "sortie": "resultat_ascii",
  "echec_ok": true,
  "suivant": "c2"
}
```

Les 10 combos de controle du cerveau (controle-outil, controle-impacts,
sante-tableaux, audit-themis, controle-modification, corriger-ascii,
maj-readme, creer-agent, creer-fichier-cerveau, creer-protocole) ont leurs
cases outil de controle marquees `echec_ok: true`. Les combos d'action
(activation, corriger-fichier, tester-outil, controle-buffy) ne le sont pas :
leur echec doit arreter le combo.

---

### Case `controle` -- branches

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

---

## Variables et interpolation

- Chaque case `generateur` / `outil` declare une `sortie` (nom de variable).
- Le moteur stocke les sorties dans une **memoire interne** (dict).
- Dans les `commande` et `entrees` des cases suivantes, `{nom}` est remplace
  par la valeur de la variable `nom`.
- Une variable non trouvee -> erreur claire, code retour 1.
- Option `persistant: true` sur une case `outil` -> la sortie est ecrite dans
  le classeur-variables (`stockage/variables-actuelles.md`) apres execution.

### ECHAPPEMENT DES VALEURS (regle anti-echappement, v0.3.3)

> **REGLE** : l'interpolation `{var}` fait un remplacement BRUT de la valeur
> dans la commande, puis le moteur decoupe la commande avec `shlex.split`.
> Toute valeur contenant une **apostrophe non echappee** (ou des espaces non
> quotes) CASSE le decoupage -> `ValueError: Commande invalide (case X)`.
> Le catalogue (149 commandes) et les commandes actuelles des combos sont
> propres, mais la regle protege le futur.

**Regle d or** : dans le `commande` d'une case `outil`, TOUJOURS quoter les
variables avec des guillemets simples autour de `{var}`. Exemples :

```
MAUVAIS  : "commande": "python3 outil.py --raison {raison}"
           -> avec raison = "d'activation", shlex.split casse (apostrophe)

BON      : "commande": "python3 outil.py --raison '{raison}'"
           -> l'apostrophe est a l'interieur des guillemets, shlex.split OK

BON      : "commande": "python3 outil.py --raison {raison}"
           -> si la valeur ne contient JAMAIS d'apostrophe ni d'espace
```

**Cas des valeurs avec apostrophes** : si une variable peut contenir une
apostrophe (ex: une raison d'activation), NE PAS l'inserer nue dans une
commande : soit la quoter dans le modele (`'{var}'`), soit utiliser une
valeur sans apostrophe. Le message `Commande invalide` signale le cas.

**Application aux commandes bash des combos** : la meme regle vaut pour les
`.sh` des combos et pour les commandes du catalogue
(`generateurs-commande`) : toute valeur interpolee doit etre quotee, jamais
inseree brute quand elle peut contenir apostrophe ou espace.

```json
{
  "type": "outil",
  "commande": "python3 mon-outil.py --fichier '{fichier}' --raison '{raison}'",
  "sortie": "resultat",
  "persistant": true,
  "suivant": "c4"
}
```

```json
{
  "type": "outil",
  "commande": "python3 mon-outil.py --fichier {fichier}",
  "sortie": "resultat",
  "persistant": true,
  "suivant": "c4"
}
```

---

## Relation avec les autres outils

| Outil | Role dans le combo |
|---|---|
| `generateurs-commande` | Compose les commandes (mode AUTO via `--reponses`) dans les cases `generateur` -- le generateur est INCHANGE, c'est le moteur qui fait le lien |
| `guider-parcours` | Guide l'agent case par case ; une case de parcours peut pointer vers un combo (Pattern 3, spec-guider-parcours v0.2.4) |
| `classeur-variables` | Persistance optionnelle des sorties (`persistant: true`) |
| `combos-audit-general` | Exemple de combo existant (orchestrateur subprocess) |

---

## Exemples

### Lister les cases d'un combo

```bash
python3 combos-moteur.py definition-combo.json --liste
```

### Executer en mode non-interactif (reponses des controles fournies)

```bash
python3 combos-moteur.py definition-combo.json --reponses "c3=OUI"
```

### Simuler sans rien executer (dry-run)

```bash
python3 combos-moteur.py definition-combo.json --dry-run
```

### Version bash (parite)

```bash
bash combos-moteur.sh definition-combo.json --reponses "c3=OUI"
```

---

## Sortie type

```
=== Combo combo-activation v0.1.0 ===
Cycle d'activation : sidentifier -> activer -> reactiver

--- [c1] Generer la commande sidentifier ---
  -> commande generee: python3 cerveau-projet/agents/tools/activer/... sidentifier llm-1
--- [c2] Executer sidentifier ---
  -> sortie: session-llm-1
QUESTION : Le resultat peut-il etre utilise directement ?
  [1] OUI
  [2] NON
=== COMBO TERMINE ===

Fin de combo atteinte : case 'c4' (FIN)
Cycle d'activation termine.
```

---

## Emplacement des combos

> **REGLE (protocole-creation-combos)** : une DEFINITION de combo est un
> **fichier du cerveau** (domaine Buffy), place dans
> `cerveau-projet/combos/<combo-nom>/definition-combo.json` (TOUJOURS ce nom).
> Le dossier `agents/tools/combos/` est reserve aux OUTILS (moteur + combos
> executables .py/.sh/.md, domaine Vulcain). Ne jamais melanger les deux.
> Voir [protocole-creation-combos](../../../../agents/regles-immuables/general/protocole-creation-combos/protocole-creation-combos.001.01.ebauche.md).

> **REGLE TRACABILITE (protocole-creation-combos 9.5, IMMUABLE)** : avant
> d'executer un combo, l'agent CITE le combo : `Je lance le combo <nom> :
> <chemin> - il enchaine <outils>.` Le rappel est en tete des indices des
> cases combo des parcours (Pattern 3).

Le moteur, lui, vit dans `agents/tools/combos/combos-moteur/` (outil).
Les definitions de combos vivent dans `cerveau-projet/combos/` (fichiers du
cerveau). La creation suit le processus du protocole-creation-combos :
audit des suites lineaires, signatures CLI, conception, test, integration
Pattern 3, validation.

---

## Versionning

| Version | Statut | Changements |
|---|---|---|
| 0.3.3 | ebauche | ECHAPPEMENT (round anti-echappement) : doc de la regle d or - quoter {var} dans les commandes des cases outil (interpolation brute + shlex.split -> une apostrophe non echappee casse). Application aux commandes bash des combos et du catalogue. Spec et py/sh INCHANGES (documentation seule) |
| 0.3.0 | ebauche | GARDE-FOU DES CLES : au chargement, validation des entrees des cases generateur contre le catalogue de commandes (cles exactes + obligatoires fournis) -> ERREUR claire code 1. Spec alignee v0.2.1. Py/sh parite maintenue |
| 0.3.2 | ebauche | ROBUSTESSE (round 5) : verification du code retour de chaque case outil - un echec (exit != 0) ARRETE le combo avec message explicite (case, commande, code, sortie) ; nouveau champ optionnel `echec_ok: true` pour les outils de controle/detection dont le code non nul est un resultat legitime. 30 cases marquees sur 10 combos de controle. Fin de la propagation silencieuse des echecs. Py/sh parite maintenue |
| 0.3.2 | ebauche | ROBUSTESSE (round 5) : verification du code retour de chaque case outil - un echec (exit != 0) ARRETE le combo avec message explicite (case, commande, code, sortie) ; nouveau champ optionnel `echec_ok: true` pour les outils de controle/detection dont le code non nul est un resultat legitime. 30 cases marquees sur 10 combos de controle. Fin de la propagation silencieuse des echecs. Py/sh parite maintenue |
| 0.1.3 | ebauche | Ajout des variables initiales `--var cle=valeur` (repetable) : disponibles pour {var} des la case depart (ex: `--var fichier=...` pour combo-controle-impacts) |
| 0.1.2 | ebauche | Ajout de la REGLE TRACABILITE (citer le combo avant de le lancer, protocole-creation-combos 9.5) |
| 0.1.1 | ebauche | Clarification de l'emplacement canonique des definitions (cerveau-projet/combos/) vs outils (agents/tools/combos/) + reference au protocole-creation-combos |
| 0.2.0 | ebauche | Ajout de la case `critere` : branchement automatique par conditions (fichier-existe, fichier-contient, sortie-contient, egalite, non-vide) avec `vers-vrai`/`vers-faux`, sans question humaine. Interpolation {var} etendue aux tirets (kebab-case). py + sh parite |
| 0.1.0 | ebauche | Creation : moteur generique de combos declaratifs (py + sh parite), 4 types de cases (generateur AUTO / outil / controle / fin), variables + interpolation {var}, persistance optionnelle vers classeur (persistant: true), modes --liste/--reponses/--dry-run/--verbose/--version, spec-combos-moteur v0.1.0 |
