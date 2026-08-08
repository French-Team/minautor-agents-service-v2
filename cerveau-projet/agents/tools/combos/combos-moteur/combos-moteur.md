# combos-moteur

| Champ | Valeur |
|---|---|
| **Version** | 0.1.0-beta |
| **Statut** | ebauche |
| **Categorie** | combos |
| **Derniere mise a jour** | 2026-08-08 |
| **Spec** | [spec-combos-moteur.001.01.ebauche.md](spec/spec-combos-moteur.001.01.ebauche.md) (v0.1.0) |

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
CASE 3 : controle    -> question + branches (OUI/NON/choix)
        |  reponse     -> si le resultat peut etre utilise BRUT, il est
        v              -> transmis directement ; sinon un generateur s'intercale
CASE 4 : fin         -> message de fin, retourne le resultat final
```

---

## Utilisation

### CLI Python (version 0.1.0-py)

```
python3 combos-moteur.py <definition-combo.json> [options]

Options :
  --liste           Lister les cases de la definition sans executer
  --reponses <liste> Reponses des controles d'un coup : case=reponse;case2=reponse2
  --dry-run         Afficher les commandes a executer sans les lancer
  --verbose         Afficher les details de chaque case
  --version         Afficher la version
  --help            Afficher l'aide
```

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
| `controle` | `question`, `branches` | Pose une question ; la reponse (via `--reponses` ou interaction) selectionne la branche | aucune (branche vers `vers`) |
| `fin` | `message` | Termine le combo et affiche le message | aucune |

### Case `generateur` -- mode AUTO

La case ne pose AUCUNE question : le moteur appelle `generateurs-commande`
avec `--reponses "cle=valeur;..."` alimente par les `entrees` (elles-memes
interpolees avec les variables precedentes). La commande composee est stockee
dans la variable `sortie` et servira a la case `outil` suivante via `{cmd}`.

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

Un combo (fichier `definition-combo.json`) est un **fichier du cerveau**,
cree par Buffy, dans le dossier de l'agent concerne
(`agents/<agent>/combos/definition-combo.json`) ou dans un dossier combos
dedie. Le moteur, lui, vit dans `agents/tools/combos/combos-moteur/`.

---

## Versionning

| Version | Statut | Changements |
|---|---|---|
| 0.1.0 | ebauche | Creation : moteur generique de combos declaratifs (py + sh parite), 4 types de cases (generateur AUTO / outil / controle / fin), variables + interpolation {var}, persistance optionnelle vers classeur (persistant: true), modes --liste/--reponses/--dry-run/--verbose/--version, spec-combos-moteur v0.1.0 |
