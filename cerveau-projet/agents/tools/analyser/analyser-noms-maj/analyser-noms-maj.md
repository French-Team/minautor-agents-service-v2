---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# analyser-noms-maj

**Categorie** : Analyser
**Version** : 0.1.0
**Statut** : ebauche

---

## Objectif

Analyser la **casse et la forme des NOMS references** dans les fichiers du
cerveau-projet (registre-usages-outils, historique, catalogue-commandes,
index-tools) pour denicher les **orphelins** (nom reference sans cible
reelle) et les **erreurs de nommage** (casse min/MAJ incoherente, chemin
au lieu d un nom d outil normalise, nom de fonction dans une commande).

Contexte (demande utilisateur 2026-08-16) : les conventions de nommage
existantes (`detecter-convention-nommage`, `corriger-nommage`) verifient le
nommage des FICHIERS mais jamais la casse/forme des NOMS REFERENCES dans le
contenu. Diagnostic Cerberus : 17 entrees du registre ont le champ `outil`
= chemin de script temp (`tmp-buffy/resync-lock-et-appliquer.py`) au lieu
d un nom kebab-case ; l historique cite des noms de fonctions
(`lancer_protege`, `charger_protections`, `detecter_compagnons`).

---

## Detections

| Code | Zone | Description |
|---|---|---|
| **OUTIL_CHEMIN** | registre | champ `outil` contenant un chemin, une extension `.py/.sh` ou un prefixe temp (`tmp-`, `.tmp-`, `.zz-`) : forme non normalisee |
| **OUTIL_ORPHELIN** | registre, catalogue, index | nom d outil reference sans dossier reel (`tools/<categorie>/<outil>/`) correspondant |
| **OUTIL_CASSE** | registre, catalogue | nom d outil en casse differente de la forme canonique (kebab-case minuscule) |
| **AGENT_INCONNU** | registre | champ `agent` sans dossier agent reel (`agents/<agent>/`) |
| **FONCTION_DANS_COMMANDE** | registre, historique | motif snake_case (`lancer_protege`, `charger_`, `detecter_`...) dans les commandes/raisons - **AVERTISSEMENT** (non bloquant) |

Verdict : 0 probleme = **OK** ; sinon **KO** avec le nombre (les
avertissements FONCTION_DANS_COMMANDE sont comptes mais marques).

---

## Usage

```bash
# Analyse complete (4 zones)
python3 analyser-noms-maj.py --tous

# Zone unique
python3 analyser-noms-maj.py --zone registre
python3 analyser-noms-maj.py --zone historique
python3 analyser-noms-maj.py --zone catalogue
python3 analyser-noms-maj.py --zone index

# Rapport markdown
python3 analyser-noms-maj.py --tous --rapport rapport-noms-maj.md

# Detail
python3 analyser-noms-maj.py --tous --verbose

# Version
python3 analyser-noms-maj.py --version
```

## Options

| Option | Description |
|---|---|
| `--tous` | analyse les 4 zones |
| `--zone <nom>` | zone unique (`registre`, `historique`, `catalogue`, `index`) |
| `--rapport <fichier>` | ecrit le rapport markdown |
| `--verbose` | detail des problemes |
| `--no-chrono` | coupe le chrono de l outil |
| `--version` | affiche la version |

---

## Limites

- `OUTIL_ORPHELIN` sur le registre ignore les entrees declarees
  `mode=script-temporaire` (scripts temp legitimes, pas des outils durables).
- Les noms de categories et generiques (`detecter`, `analyser`, `index-tools`,
  `outil-template`...) sont exclus de l analyse de l index.
- `FONCTION_DANS_COMMANDE` est un avertissement : les lecons et raisons
  peuvent legitiment citer des noms de fonctions pour documenter un bug.
