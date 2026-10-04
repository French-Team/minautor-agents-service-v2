# PROTOCOLE 5 -- Modifier les outils et combos (freelance/)

> Ce protocole s'applique QUAND Mecano modifie un OUTIL dans
> freelance/tools-commun/ ou freelance/<agent>/tools/.
> LIRE CE PROTOCOLE AVANT TOUTE ECRITURE.

---

## DIFFERENCE FONDAMENTALE

| Caracteristique | Outil v1 (agents/tools/) | Outil v2 (freelance/tools-commun/) |
|---|---|---|
| **Structure** | <outil>.py + <outil>.sh + spec/ | <outil>.md + entry.py + fonctions/ + <outil>-data.json |
| **Racine** | os_path (compteur de niveaux) | os_path (compteur de niveaux) |
| **Encodage** | ASCII + LF | UTF-8 + CRLF |
| **Catalogue** | registre-usages-outils.jsonl | Pas de catalogue v1 |
| **D15** | Pas toujours respecte | OBLIGATOIRE (separation code/donnees) |

---

## REGLE ABSOLUE

> Les outils v2 suivent le template EXACT :
> <outil>.md + entry.py + fonctions/ + <outil>-data.json.
> JE NE MODIFIE JAMAIS la structure d'un outil v2.
> Si un outil v2 n'a pas cette structure, je le SIGNAL mais ne le convertis pas.

---

## AVANT de commencer

1. **Lire le mode d'emploi** (<outil>.md) : comprendre l'outil
2. **Lire entry.py** : comprendre le point d'entree
3. **Lire les fonctions/** : comprendre la logique
4. **Lire <outil>-data.json** : comprendre les donnees (D15)
5. **Verifier la structure** : <outil>.md + entry.py + fonctions/ + <outil>-data.json ?

---

## ECRIRE la modification

| Element | Regle |
|---|---|
| **Encodage** | UTF-8 + CRLF |
| **D15** | Separation code/donnees OBLIGATOIRE |
| **Structure** | entry.py = orchestrateur (zero logique), fonctions/ = logique |
| **Donnees** | Tout dans <outil>-data.json, zero valeur en dur dans le .py |
| **Racine** | Utiliser os_path (trouver_racine), jamais de "../.." |

---

## STRUCTURE TYPE d'un outil v2

```
<outil>/
|-- <outil>.md         <- mode d'emploi (contrat)
|-- entry.py           <- point d'entree orchestrateur
|-- fonctions/         <- fonctions simples
|   `-- <fonction>.py  <- une tache par fonction
`-- <outil>-data.json  <- donnees editables (D15)
```

---

## VERIFIER apres modification

1. **Structure** : <outil>.md + entry.py + fonctions/ + <outil>-data.json ?
2. **D15** : les donnees sont-elles dans le fichier .json, pas en dur ?
3. **Racine** : utilise-t-il os_path (trouver_racine) ?
4. **Encodage** : UTF-8 + CRLF ?
5. **entry.py** : est-il un orchestrateur (zero logique) ?

---

## INTERDICTIONS

| Interdiction | Raison |
|---|---|
| **Mettre de la logique dans entry.py** | entry.py = orchestrateur seulement |
| **Mettre des valeurs en dur dans le .py** | D15 : tout dans le .json |
| **Utiliser "../.." pour la racine** | os_path obligatoire |
| **Melanger v1 et v2** | Les outils v2 n'utilisent PAS d'outils v1 |
| **Changer l'encodage** | UTF-8 + CRLF toujours |
| **Supprimer <outil>-data.json** | D15 : separation code/donnees obligatoire |
