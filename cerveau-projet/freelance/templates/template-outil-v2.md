---
identite:
  nom: <outil>
  version: 0.1.0
  cree: YYYY-MM-DD
  type: outil
  appartient_a: <agent ou "commun">
  commun: true/false
  grade: silver
  mot-cles: ["<outil>", "<fonction>", "<domaine>", "v2", "outils"]
  session: freelance
  tags: outil, <domaine>, v2, freelance
---
# <Outil> -- <Description>

> COMMANDE : `python3 <outil>.py --help`

## Vue d'ensemble

| Champ | Valeur |
|---|---|
| **Nom** | <Outil> |
| **Version** | 0.1.0 |
| **Role** | <Description concise> |
| **Emplacement** | `<chemin>` |
| **Grade requis** | silver |
| **Dedie/Commun** | <agent> / tools-commun |

---

## Formulaire (D7)

Le formulaire EST le contrat. L'agent remplit, l'outil execute.

```json
{
  "outil": "<outil>",
  "version": "0.1.0",
  "champs": [
    {
      "nom": "<champ1>",
      "type": "texte|nombre|boolean|liste|fichier|enum",
      "requis": true,
      "defaut": "<valeur>",
      "description": "<description>",
      "valeurs": ["<si enum>"]
    }
  ]
}
```

### Champs

| Champ | Type | Requis | Defaut | Description |
|---|---|---|---|---|
| `<champ1>` | `<type>` | <oui/non> | `<defaut>` | <description> |

---

## Commandes

| Commande | Description | Exemple |
|---|---|---|
| `--help` | Afficher l'aide | `python3 <outil>.py --help` |
| `--<action>` | <Description> | `python3 <outil>.py --<action> --<champ> <val>` |

---

## Donnees (D15)

Fichier `<outil>-data.json` : TOUTES les donnees editables.
Le .py ne contient AUCUNE valeur en dur (P4).

```json
{
  "version": "0.1.0",
  "description": "<description>",
  "elements": []
}
```

**Modifier** = editer le -data.json. JAMAIS le .py.

---

## Regles

| Regle | Detail |
|---|---|
| **D15** | Separation code/donnees. .py = logique. .json = valeurs. |
| **D7** | Formulaire = contrat. Champs definis, validation avant execution. |
| **P4** | Zero valeur en dur. Tout dans le fichier de donnees. |
| **P1** | Un seul .md + un seul .py + un seul .json. |


---

## REGLE RAPPEL (protocole 18/20)

Apres toute correction sur cet outil, consulter :
    python3 tools-commun/rappel/entry.py pour --contexte correction-outil
et verifier : parite .sh/.py, serveur MCP equivalent, tests, index.
