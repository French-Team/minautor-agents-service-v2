---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# guider-arbre

**Version :** 0.1.0
**Statut :** ebauche
**Categorie :** guider
**Chemin :** `agents/tools/guider/guider-arbre/`
**Proprietaire :** Vulcain (outil partage)

## Description

Piloter un **arbre de decisions v2-like** (format cible de la refonte
2026-08-27 : les cartes v1 `parcours-<agent>.json` sont migrees en arbres).
L'arbre est le format v2-like : **racine -> themes -> fins centralisees**.

```
arbre-<agent>.json  racine (question + branches) -> theme-*.json
theme-<nom>.json    but + redirects (besoin -> action/procedure + regle)
fins.json           fins CENTRALISEES (redirection / activer / reactiver)
```

Principe (identique a guider-parcours) : l'agent ne lit JAMAIS l'arbre en
entier. Il recoit LA case courante (racine ou theme), repond/choisit, et
l'outil fournit la suivante. Mode AGENT non-bloquant : jamais d'input()
clavier ; sans `--reponses`, la question est affichee et l'outil s'arrete
proprement (l'agent repond puis relance).

## Utilisation

```bash
# Naviguer dans l'arbre (mode agent : questions affichees, arret propre)
python3 guider-arbre.py cerveau-projet/agents/vulcain/parcours/arbre-vulcain.json

# Reponses fournies d'un coup (racine | theme | besoin), separees par |
python3 guider-arbre.py cerveau-projet/agents/vulcain/parcours/arbre-vulcain.json \
  --reponses 'construire|Construire un outil'

# Lister la structure (racine, branches, themes, besoins) sans naviguer
python3 guider-arbre.py cerveau-projet/agents/vulcain/parcours/arbre-vulcain.json --liste

# Valider la structure : liens racine -> themes resolus, chaque theme a une
# fin vers une case existante de fins.json
python3 guider-arbre.py cerveau-projet/agents/vulcain/parcours/arbre-vulcain.json --valider
```

## Navigation

1. **Racine** : question + branches (reponses -> `theme-*.json`).
2. **Theme** : nom + but + liste des besoins (redirects). L'agent choisit
   le besoin correspondant a sa situation.
3. **Besoin** : action (procedure), etapes, regle -> la procedure a suivre.
4. **Fin** : la fin du theme pointe vers une case de `fins.json`
   (redirection vers la racine, ou action activer/reactiver avec commande).

## Format de l'arbre

### arbre-<agent>.json

```json
{
  "identite": { "type": "arbre", "appartient_a": "<agent>", "commun": false },
  "arbre": {
    "nom": "arbre-<agent>",
    "agent": "<agent>",
    "description": "...",
    "regles": { "D1": "...", "D5": "...", "D6": "...", "D3": "..." }
  },
  "racine": {
    "titre": "...",
    "type": "question",
    "question": "...",
    "branches": [
      { "reponse": "<THEME>", "description": "...", "vers": "theme-<theme>.json" }
    ]
  },
  "fins": { "fichier": "fins.json", "description": "Fins centralisees" }
}
```

### theme-<nom>.json

```json
{
  "identite": { "type": "theme", "appartient_a": "<agent>", "nom": "<THEME>" },
  "theme": {
    "nom": "<THEME>",
    "but": "...",
    "redirects": [
      {
        "besoin": "...",
        "action": "procedure",
        "description": "...",
        "etapes": ["etape1", "etape2"],
        "regle": "..."
      }
    ]
  },
  "fin": { "type": "lien", "vers": "fins.json", "case": "fin-<case>" }
}
```

### fins.json

```json
{
  "identite": { "type": "fins", "appartient_a": "<agent>" },
  "fins": {
    "fin-theme": { "titre": "Retour a la racine", "action": "redirection", "vers": "arbre-<agent>.json" },
    "fin-cerberus": {
      "titre": "FIN - Reactiver Cerberus",
      "description": "...",
      "action": "reactiver",
      "cible": "cerberus",
      "commande": "python3 ... reactiver <session> '<bilan>' <agent>",
      "regle": "..."
    }
  }
}
```

## Regles

| Regle | Description |
|---|---|
| **Une carte = un role** | L'arbre d'un agent ne contient que des actions de SON role |
| **Fins centralisees** | Jamais de fin inline : toutes les fins vivent dans `fins.json` |
| **Liens resolus** | Chaque `vers` pointe vers un fichier/case qui existe |
| **Mode agent** | Jamais d'input clavier : question affichee, arret propre, relance avec `--reponses` |
| **Conventions v1** | ASCII strict, LF, nommage `guider-` |

## Retour

| Code | Signification |
|---|---|
| 0 | Succes (navigation terminee, liste, ou arbre valide) |
| 1 | Erreur (fichier introuvable, JSON invalide, lien casse, reponse inconnue) |

## Historique

| Version | Date | Modification |
|---|---|---|
| 0.1.0 | 2026-08-27 | Creation : lecteur/validateur des arbres v2-like (racine -> themes -> fins centralisees), mode agent non-bloquant, --liste, --valider |
