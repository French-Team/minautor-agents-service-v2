# Specification -- Lister les Agents

**Outil** : lister-agents
**Version** : 0.1.0-beta
**Date** : 2026-08-05

---

## Objectif technique

Fournir une interface standardisee pour interroger la base d'agents.

---

## Architecture

```
lister-agents
    |
    |-- Entree (parametres)
    |   |-- format : string
    |   |-- champs : string
    |   `-- filtre : string
    |
    |-- Traitement
    |   |-- Lecture de index-agents.md
    |   |-- Extraction des agents
    |   |-- Filtrage
    |   `-- Formatage
    |
    `-- Sortie (resultat)
        `-- string (table, liste, ou JSON)
```

---

## Source de donnees

**Fichier** : `cerveau-projet/agents/index-agents.md`

**Structure attendue** :

```markdown
| Agent | Fiche | Corrections | Role | Statut |
|---|---|---|---|---|
| [Cerberus](cerberus/cerberus.md) | ... | ... | Gardien de l'entree | Disponible (principal) |
```

---

## Algorithme

```
1. Lire index-agents.md
2. Trouver la section "Agents existants"
3. Extraire les lignes du tableau
4. Pour chaque ligne :
   a. Extraire le nom (colonne 1)
   b. Extraire le role (colonne 4)
   c. Extraire le statut (colonne 5)
5. Appliquer le filtre si present
6. Formater selon le parametre format
7. Retourner le resultat
```

---

## Tests

### Test 1 -- Liste complete

**Entree** : `lister-agents()`
**Sortie attendue** : 4 agents (Cerberus, Buffy, Atlas, Janus)
**Statut** : En attente

### Test 2 -- Format JSON

**Entree** : `lister-agents(format="json")`
**Sortie attendue** : Tableau JSON valide
**Statut** : En attente

### Test 3 -- Filtre par statut

**Entree** : `lister-agents(filtre="statut:disponible")`
**Sortie attendue** : Uniquement Cerberus (principal)
**Statut** : En attente

---

## Evolutions futures

| Version | Fonctionnalite |
|---|---|
| 0.2.0 | Ajouter le champ "derniere-mise-a-jour" |
| 0.3.0 | Ajouter le compteur de corrections |
| 0.4.0 | Ajouter les protocoles associes |
| 1.0.0 | Version stable |

---

