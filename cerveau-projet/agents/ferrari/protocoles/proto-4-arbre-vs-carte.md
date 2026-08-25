# PROTOCOLE 4 -- Arbre de decisions v2 vs Carte de decisions v1

> Ce protocole s'applique QUAND Mecano modifie un FICHIER DE DECISION
> dans freelance/ (arbre-*.json, theme-*.json, fins.json).
> C'est le protocole LE PLUS IMPORTANT : la difference v1/v2 est ici
> maximale et les erreurs sont fatales.

---

## DIFFERENCE FONDAMENTALE

| Caracteristique | Carte v1 (agents/) | Arbre v2 (freelance/) |
|---|---|---|
| **Fichier principal** | parcours-<agent>.json | arbre-<agent>.json |
| **Structure** | cases c0 -> c1 -> c2 -> ... -> cN | racine -> themes -> fins |
| **Types de cases** | question, indice, controle, fin | question, action |
| **Navigation** | "vers": "c3" (ligneaire) | "vers": "theme-*.json" (branchement) |
| **Fins** | Inline dans le fichier | Centralisees dans fins.json |
| **Version** | "version": "0.5.7" | "version": "0.1.0" |
| **Nommage** | parcours-<agent>.json | arbre-<agent>.json + theme-*.json |

---

## REGLE ABSOLUE

> JE NE CONVERTIS JAMAIS un arbre v2 en carte v1 ni l'inverse.
> Si un agent v2 a un arbre, je garde la structure arbre.
> Si un agent v1 a une carte, je garde la structure carte.
> JAMAIS de melange.

---

## AVANT de modifier un arbre v2

1. **Lire arbre-<agent>.json** : comprendre la racine et les branches
2. **Lire CHAQUE theme-*.json** : comprendre les redirections
3. **Lire fins.json** : comprendre les fins centralisees
4. **Verifier la coherence** : chaque "vers" pointe vers un fichier qui existe ?
5. **Verifier le format JSON** : indentation, guillemets, virgules

---

## STRUCTURE TYPE d'un arbre v2

```json
{
  "identite": {
    "type": "arbre",
    "appartient_a": "<agent>",
    "version": "0.1.0",
    "commun": false
  },
  "arbre": {
    "nom": "arbre-<agent>",
    "agent": "<agent>",
    "description": "...",
    "regles": {
      "D1": "...",
      "D5": "...",
      "D6": "...",
      "D3": "..."
    }
  },
  "racine": {
    "titre": "...",
    "type": "question",
    "question": "...",
    "branches": [
      {"reponse": "...", "vers": "theme-*.json"},
      {"reponse": "...", "description": "...", "vers": "theme-*.json"}
    ]
  },
  "fins": {
    "fichier": "fins.json",
    "description": "Toutes les fins possibles centralisees"
  }
}
```

---

## STRUCTURE TYPE d'un theme v2

```json
{
  "identite": {
    "type": "theme",
    "appartient_a": "<agent>",
    "nom": "<THEME>",
    "description": "..."
  },
  "theme": {
    "nom": "<THEME>",
    "but": "...",
    "redirects": [
      {
        "besoin": "...",
        "action": "procedure",
        "description": "...",
        "etapes": ["etape1", "etape2", "..."],
        "regle": "..."
      }
    ]
  },
  "fin": {"type": "lien", "vers": "fins.json", "case": "fin-theme"}
}
```

---

## ECRIRE la modification

| Element | Regle |
|---|---|
| **Encodage** | UTF-8 + CRLF |
| **Format** | JSON valide (indentation 2 espaces) |
| **Structure** | Garder la structure arbre (racine -> themes -> fins) |
| **Liens** | Chaque "vers" doit pointer vers un fichier qui existe |
| **Fins** | Centralisees dans fins.json, pas inline |
| **Version** | Bumper si modification structurelle |

---

## VERIFIER apres modification

1. **JSON valide** : python3 -c "import json; json.load(open('fichier.json'))"
2. **Liens** : chaque "vers" pointe vers un fichier qui existe ?
3. **Fins** : chaque theme a-t-il une "fin" qui pointe vers fins.json ?
4. **Racine** : la racine a-t-elle des branches qui pointent vers des themes qui existent ?
5. **Coherence** : le theme modifie est-il coherent avec les autres themes ?

---

## INTERDICTIONS

| Interdiction | Raison |
|---|---|
| **Convertir arbre en carte** | Les agents v2 ont des ARBRES, pas des cartes |
| **Ajouter des cases c0, c1, c2** | C'est la structure v1, pas v2 |
| **Supprimer fins.json** | Les fins doivent rester centralisees |
| **Changer le format des liens** | "vers": "theme-*.json" toujours |
| **Changer l'encodage** | UTF-8 + CRLF toujours |
