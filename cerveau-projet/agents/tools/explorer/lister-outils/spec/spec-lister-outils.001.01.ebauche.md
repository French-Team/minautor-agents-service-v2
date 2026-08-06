# Specification -- Lister les Outils

**Outil** : lister-outils
**Version** : 0.1.0-beta
**Date** : 2026-08-05

---

## Objectif technique

Fournir une interface standardisee pour interroger la boite a outils partagee.

---

## Architecture

```
lister-outils
    │
    ├── Entree (parametres)
    │   ├── format : string
    │   ├── categorie : string
    │   └── champs : string
    │
    ├── Traitement
    │   ├── Lecture de index-tools.md
    │   ├── Extraction des outils
    │   ├── Filtrage par categorie
    │   └── Formatage
    │
    └── Sortie (resultat)
        └── string (table, liste, ou JSON)
```

---

## Source de donnees

**Fichier** : `cerveau-projet/agents/tools/index-tools.md`

**Structure attendue** :

```markdown
| Outil | Description | Chemin |
|---|---|---|
| `lister-dossiers` | Lister les dossiers d'un chemin | [explorer/lister-dossiers/](explorer/lister-dossiers/) |
```

---

## Algorithme

```
1. Lire index-tools.md
2. Trouver les sections par categorie (Explorer, Valider, Analyser, Corriger)
3. Extraire les lignes de chaque tableau
4. Pour chaque ligne :
   a. Extraire le nom (colonne 1)
   b. Extraire la description (colonne 2)
   c. Determiner la categorie (section parent)
5. Appliquer le filtre categorie si present
6. Formater selon le parametre format
7. Retourner le resultat
```

---

## Tests

### Test 1 -- Liste complete

**Entree** : `lister-outils()`
**Sortie attendue** : 13 outils
**Statut** : En attente

### Test 2 -- Filtre par categorie

**Entree** : `lister-outils(categorie="explorer")`
**Sortie attendue** : 6 outils (Explorer)
**Statut** : En attente

### Test 3 -- Format JSON

**Entree** : `lister-outils(format="json")`
**Sortie attendue** : Tableau JSON valide
**Statut** : En attente

---

## Evolutions futures

| Version | Fonctionnalite |
|---|---|
| 0.2.0 | Ajouter le statut (beta/stable) |
| 0.3.0 | Ajouter le proprietaire |
| 0.4.0 | Ajouter les dependances |
| 1.0.0 | Version stable |

---

