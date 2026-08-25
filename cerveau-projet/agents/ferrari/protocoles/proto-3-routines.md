# PROTOCOLE 3 -- Modifier les routines (freelance/)

> Ce protocole s'applique QUAND Mecano modifie les routines dans
> freelance/routines/. LIRE CE PROTOCOLE AVANT TOUTE ECRITURE.

---

## REGLE ABSOLUE

> Les routines sont des EXECUTIONS PLANIFIEES qui dependant de JARVIS.
> Modifier une routine = modifier le comportement d'un agent freelance
> a un moment donne. Impact potentiel sur tout le systeme.

---

## AVANT de commencer

1. **Lire etat-executions.json** : comprendre l'etat actuel des routines
2. **Lire les routines concernees** : comprendre ce qu'elles font
3. **Verifier les dependances** : la routine depend-elle de jarvis.py ?
   Si oui, lire aussi le protocole 2 (JARVIS)
4. **Verifier les triggers** : quand la routine se declenche-t-elle ?

---

## ECRIRE la modification

| Element | Regle |
|---|---|
| **Encodage** | UTF-8 + CRLF |
| **Format JSON** | Valider le JSON avant d'ecrire |
| **Dependances** | Documenter les dependances avec JARVIS |
| **Backward compatibility** | NE PAS casser les routines existantes |

---

## VERIFIER apres modification

1. **JSON valide** : python3 -c "import json; json.load(open('fichier.json'))"
2. **Coherence** : les routines sont-elles toujours coherentes entre elles ?
3. **Dependances** : les routines modifiees dependent-elles toujours de JARVIS ?

---

## INTERDICTIONS

| Interdiction | Raison |
|---|---|
| **Supprimer une routine existante** | Casserait le comportement attendu |
| **Modifier etat-executions.json sans raison** | C'est un fichier d'etat, pas de donnees |
| **Changer l'encodage** | UTF-8 + CRLF toujours |
