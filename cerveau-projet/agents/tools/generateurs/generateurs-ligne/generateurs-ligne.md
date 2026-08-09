# generateurs-ligne

Ajoute une **LIGNE** (chemin de bout en bout : point d'entree -> fin) a une
carte de decision (parcours JSON) d'un agent, construite a partir de
**gabarits de groupes de cases** (configs) predefinis. Avant toute edition,
verifie que la carte cartographique d'Atlas (`cartographie-<agent>.md`)
existe et est a jour. Dry/wet pour valider l'ajout.

| | |
|---|---|
| **Chemin** | `agents/tools/generateurs/generateurs-ligne/` |
| **Python** | `generateurs-ligne.py` |
| **Bash** | `generateurs-ligne.sh` (parite) |
| **Version** | 0.3.0 |
| **Statut** | ebauche |
| **Spec** | `spec/spec-generateurs-ligne.001.01.ebauche.md` |
| **Gabarits** | `gabarits-ligne.json` (configs externalisees) |

**Complements de la suite** : `generateurs-carte` agit sur la carte COMPLETE
(creer/analyser/detecter/dupliquer), `generateurs-ligne` ajoute une LIGNE
(groupe de cases) en un bloc, `generateurs-case` agit sur UNE case
(ajouter/editer/supprimer). `generateurs-ligne` est le maillon du milieu.

---

## Usage

```
python3 generateurs-ligne.py <parcours.json> verifier
python3 generateurs-ligne.py <parcours.json> lister-configs
python3 generateurs-ligne.py <parcours.json> config <nom>
python3 generateurs-ligne.py <parcours.json> ajouter --config <nom> [options]
python3 generateurs-ligne.py ajouter-config <nom> --description "<texte>" --gabarit <fichier.json> [--force] [--dry-run]
python3 generateurs-ligne.py <parcours.json> copier --source <case> [--mode complet|branche|suite] [--branche <reponse>] [options]
python3 generateurs-ligne.py <parcours.json> copier --config <nom> [options]
```

Version bash identique (wrapper pur `exec python3`) :

```
bash generateurs-ligne.sh <parcours.json> verifier
```

---

## 1. Verifier la carte Atlas (`verifier`)

Avant d'editer une carte, verifie que la cartographie creee par Atlas est
a jour :

- **CARTE A JOUR** : `cartographie-<agent>.md` existe ET son mtime est plus
  recent que le mtime du parcours JSON.
- **CARTE A REGENERER** : carte absente OU plus ancienne que le parcours.

Si la carte n'est pas a jour, l'action `ajouter` BLOQUE et invite a activer
Atlas via SA carte (case c31 Cartographier) pour regenerer
`cartographie-<agent>.md`, puis a revenir continuer. `--force` passe outre
(decision explicite).

```
python3 generateurs-ligne.py cerveau-projet/agents/buffy/parcours/parcours-buffy.json verifier
```

---

## 2. Gabarits de lignes (`lister-configs` / `config`)

Les gabarits sont **externalises dans `gabarits-ligne.json`** (une place pour
chaque chose) : ils ne vivent plus dans le code de l'outil. Quatre gabarits
de groupes de cases sont disponibles par defaut :

| Config | Description | Cases du bloc |
|---|---|---|
| `defaut` | Decision a 2 branches + rejoint (modele compose minimal) | cX (question) -> cXa + cXb -> REJOINT |
| `config-1` | Decision + DEVIATION (workflow secondaire) + rejoint (Pattern 7 complet) | cX -> cXa (principal) / cXb (deviation) -> cXc -> REJOINT |
| `config-2` | Controle RVAV (OUI/NON) + branches + rejoint | cX (controle) -> cXa (OUI) + cXb (NON) -> REJOINT |
| `config-3` | Action simple (enchainement sans question) | cX (action) -> REJOINT |

Chaque bloc se termine par une case REJOINT qui pointe vers la case de
rejoint (retour au flux principal). Les ids sont generes automatiquement
conformes a la convention `c<numero>[a-z]?` (valider-case).

```
python3 generateurs-ligne.py <parcours.json> lister-configs
python3 generateurs-ligne.py <parcours.json> config config-1
```

## 2 bis. Ajouter une config (`ajouter-config`)

Si un gabarit manque (config utile pour la suite), **ne recompose pas
plusieurs fois la meme ligne** : ajoute une config reutilisable avec
`ajouter-config` - sans toucher au code de l'outil (Pattern 12 : creation
limitee). Le gabarit est fourni dans un fichier JSON de structure
`{"cases": [...]}` (format identique aux cases de `gabarits-ligne.json`) :

```
python3 generateurs-ligne.py ajouter-config config-4 \
  --description "Decision avec correction avant poursuite" \
  --gabarit mon-gabarit.json
```

Exemple de fichier gabarit (`mon-gabarit.json`) :

```json
{
  "cases": [
    {"suffixe": "", "type": "question", "titre": "RESULTAT VALIDE ?",
     "branches": [["OUI", ".1"], ["NON", ".2"]], "suivant": null},
    {"suffixe": ".1", "type": "action", "titre": "Valide, continuer",
     "branches": [], "suivant": "REJOINT"},
    {"suffixe": ".2", "type": "action", "titre": "Corriger puis revenir",
     "branches": [], "suivant": "REJOINT"},
    {"suffixe": "REJOINT", "type": "action",
     "titre": "REJOINT - retour au flux principal", "branches": [],
     "suivant": "REJOINT"}
  ]
}
```

Chaque case a : `suffixe` (vide pour la 1re, puis `.1`, `.2`, ... ; `REJOINT`
pour la case de retour), `type` (`question` / `controle` / `action`),
`titre`, `branches` (liste `[reponse, suffixe_destination]`, au moins 2 pour
une decision) et `suivant` (suffixe de destination pour les actions).

Le gabarit est **valide avant insertion** (types autorises, branches min 2
pour les decisions, destinations resolvables, case REJOINT presente, nom
conforme). `--dry-run` simule sans ecrire ; le wet insere la config dans
`gabarits-ligne.json` (trie par nom, ASCII, LF). `--force` ecrase une config
existante du meme nom.

---

## 3. Ajouter une ligne (`ajouter`)

```
python3 generateurs-ligne.py <parcours.json> ajouter \
  --config defaut \
  --point-attache c1 \
  --reponse ligne \
  --rejoint c8 \
  --titre "Ligne configuration"
```

### Options

| Option | Defaut | Role |
|---|---|---|
| `--config` | obligatoire | Gabarit (defaut, config-1, config-2, config-3, ou une config ajoutee) |
| `--point-attache` | case_depart | Case existante d'ou part la ligne |
| `--reponse` | `NON` | Reponse de la branche creee (sur une question/controle) |
| `--rejoint` | ancien suivant | Case ou la ligne revient au flux |
| `--titre` | `Ligne <config>` | Titre de base des cases du bloc |
| `--force` | - | Passer outre une carte Atlas absente/perimee |
| `--dry-run` | - | Simuler sans rien modifier |

### Cablage automatique

- **Attache `question`/`controle`** : une BRANCHE est ajoutee
  (`<reponse>` -> premiere case de la ligne). Le rejoint doit etre precise
  (`--rejoint`) car la question n'a pas de suivant.
- **Attache `action`/`indice`** : le `suivant` est recable vers la premiere
  case de la ligne ; l'ancien suivant devient le rejoint par defaut.

### Dry/wet

- `--dry-run` : affiche le point d'attache, le cablage, le rejoint et les
  nouvelles cases SANS rien modifier.
- Sans `--dry-run` : applique l'ajout, sauvegarde le parcours, puis VALIDE
  automatiquement (guider-parcours `--liste` + valider-case `--modele
  --references`).

---

## 3 bis. Copier une ligne existante (`copier`)

Pour composer une nouvelle ligne a partir d'une ligne deja creee (au lieu de
repartir d'un gabarit), la sous-commande `copier` duplique un GROUPE de cases
existant et le reclone sur un point d'attache. Deux sources possibles :

| Source | Commande |
|---|---|
| **Une case de la carte** | `copier <parcours> --source <case> --mode <mode>` |
| **Un gabarit** | `copier <parcours> --config <nom>` |

### Modes de detection (`--mode`, source = case)

| Mode | Comportement |
|---|---|
| `complet` (defaut) | Si la source est une decision (question/controle), elle EST le point d'entree de la ligne -> copie toute sa suite jusqu'au REJOINT. Si la source est une action, remonte a la 1re decision qui la precede (point d'entree) puis copie tout le sous-chemin |
| `branche` | Si la source est une decision, copie UNIQUEMENT la branche choisie (`--branche OUI/NON/...`) |
| `suite` | Copie le chemin qui part de la case source (sa suite) jusqu'au REJOINT ou a une fin |

Le clone reutilise la structure (branches, deviations, rejoint) avec de
NOUVEAUX ids conformes `c<numero>[a-z]?` (groupes jusqu'a 27 cases : cX +
suffixes lettres ; groupes plus grands : numeros sequentiels). Les cases
REJOINT du groupe sont remplacees par la case de rejoint externe. Ensuite,
`generateurs-case` permet d'editer les cases du clone finement.

### Exemples

```
# Copier toute la ligne (decision d'entree) sur c10c, branche ligneB
python3 generateurs-ligne.py <parcours.json> copier --source c11b \
  --mode complet --point-attache c10c --reponse ligneB --rejoint c11

# Copier UNIQUEMENT la branche OUI d'une decision
python3 generateurs-ligne.py <parcours.json> copier --source c11b \
  --mode branche --branche OUI --point-attache c0b --reponse copieOUI --rejoint c0c

# Copier la suite d'une action jusqu'au rejoint
python3 generateurs-ligne.py <parcours.json> copier --source c11c \
  --mode suite --point-attache c0b --reponse copieSuite --rejoint c0c

# Copier depuis un gabarit (fusion avec ajouter)
python3 generateurs-ligne.py <parcours.json> copier --config config-2 \
  --point-attache c1 --reponse rvavB --rejoint c8
```

Les memes garde-fous que `ajouter` s'appliquent : carte Atlas a jour exigee
(`--force` pour passer outre), dry/wet, validation auto CONFORME.

---

## 4. Philosophie

- **Une place pour chaque chose** : l'edition fine des cases est faite par
  l'agent habilite via SA carte (et ses outils). `generateurs-ligne` prepare
  le bloc de cases conforme (decision + branches + deviation + rejoint) sans
  avoir a connaitre les regles de chaque metier.
- **Carte Atlas a jour d'abord** : on edite une carte que si la cartographie
  qui la represente est a jour (sinon, on active Atlas pour la regenerer et
  on revient).

---

## Regles

1. **ASCII strict** : contenu 100% ASCII (valider-conformite-ascii).
2. **LF pur** : aucun CRLF.
3. **Nommage** : prefixe `generateurs-` controle au demarrage.
4. **100% stdlib Python** : aucune dependance externe.
5. **Dry-run avant usage** : toujours simuler avant d'ecrire.
