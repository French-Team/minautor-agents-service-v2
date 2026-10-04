---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# Outils de Base - Analyse Reelle

> **Objectif** : Identifier les outils fondamentaux MANQUANTS (analyse historique).
> **Etat actuel** : les 18 outils P0/P1/P2 identifies ci-dessous sont TOUS crees (voir la section Statut en bas).

---

## Ce que nous AVONS deja

| Operation | Outils existants |
|---|---|
| **Lister des fichiers** | `lister-fichiers`, `lister-dossiers`, `lister-statuts` |
| **Lister des agents/outils** | `lister-agents`, `lister-outils`, `lister-appels`, `lister-fonctions` |
| **Rechercher des fichiers** | `rechercher-fichiers-vides`, `rechercher-templates`, `rechercher-pense-betes`, `rechercher-specs`, `rechercher-todos` |
| **Rechercher du texte** | `rechercher-accents-sensibles` (specialise) |
| **Corriger des accents** | `corriger-accents-zones-sensibles`, `corriger-emojis` |
| **Corriger des liens** | `corriger-liens` |
| **Corriger le nommage** | `corriger-nommage` |
| **Valider la conformite** | `valider-conformite-ascii`, `valider-nommage`, `valider-liens`, `valider-conventions`, `valider-ebauche`, etc. |
| **Changer le statut** | `changer-statut` (renomme un fichier) |
| **Purifier/Condenser** | `nettoyer-fichier`, `condenser-fichier` |
| **Creer des documents** | `generateurs-squelette-pense-bete`, `generateurs-squelette-spec`, `generateurs-squelette-todo`, `creer-remplir-pense-bete`, `creer-remplir-spec`, `creer-remplir-todo` |

---

## Ce qui MANQUE vraiment

### 1. LIRE un fichier (pas juste lister)

| Besoin | Existant | Manque |
|---|---|---|
| Lire le contenu d'un fichier | `lister-fichiers` (liste les noms) | `lire-fichier` (retourne le contenu) |
| Lire des lignes specifiques | - | `lire-lignes` |
| Extraire le frontmatter YAML | - | `lire-frontmatter` |

### 2. ECRIRE / CREER un fichier

| Besoin | Existant | Manque |
|---|---|---|
| Creer un fichier nouveau | - | `creer-fichier` |
| Ecraser le contenu | - | `ecrire-fichier` |
| Ajouter a la fin (append) | - | `ajouter-contenu-fichier` |

### 3. EDITER un fichier (remplacer du texte)

| Besoin | Existant | Manque |
|---|---|---|
| Remplacer une chaine | `corriger-liens`, `corriger-nommage` (specialises) | `editer-fichier` (generique) |
| Inserer a une position | - | `inserer-contenu-fichier` |
| Supprimer une ligne | - | `supprimer-ligne` |

### 4. COPIER / DEPLACER

| Besoin | Existant | Manque |
|---|---|---|
| Copier un fichier | - | `copier-fichier` |
| Copier un dossier | - | `copier-dossier` |
| Deplacer/renommer | `changer-statut` (specialise) | `deplacer-fichier` (generique) |

### 5. SUPPRIMER

| Besoin | Existant | Manque |
|---|---|---|
| Supprimer un fichier | - | `supprimer-fichier` |
| Supprimer un dossier | - | `supprimer-dossier` |

### 6. NAVIGATION BASIQUE

| Besoin | Existant | Manque |
|---|---|---|
| Verifier existence fichier | - | `rechercher-fichier` |
| Verifier existence dossier | - | `rechercher-dossier` |
| Obtenir extension | - | `rechercher-extension-fichier` |

### 7. RECHERCHE DANS UN FICHIER

| Besoin | Existant | Manque |
|---|---|---|
| Grep generique | `rechercher-accents-sensibles` (specialise) | `rechercher-texte` (generique) |

---

## Liste complete des outils a creer

### Priorite P0 (essentiels - utiliser tous les jours)

| Outil | Categorie | Description |
|---|---|---|
| `lire-fichier` | Lire | Lire le contenu complet d'un fichier | X |
| `creer-fichier` | Creer | Creer un nouveau fichier (erreur si existe) | X |
| `ecrire-fichier` | Ecrire | Ecrire/echraser le contenu d'un fichier | X |
| `editer-fichier` | Editer | Remplacer une chaine par une autre | X |
| `copier-fichier` | Copier | Copier un fichier | X |
| `supprimer-fichier` | Supprimer | Supprimer un fichier | X |
| `rechercher-fichier` | Rechercher | Verifier si un fichier existe | X |
| `rechercher-texte` | Rechercher | Rechercher un pattern dans un fichier | X |

### Priorite P1 (utiles - moins frequents)

| Outil | Categorie | Description |
|---|---|---|
| `lire-lignes` | Lire | Lire des lignes specifiques | X |
| `ajouter-contenu-fichier` | Ajouter | Ajouter du contenu a la fin | X |
| `inserer-contenu-fichier` | Inserer | Inserer du contenu a une position | X |
| `copier-dossier` | Copier | Copier un dossier recursivement | X |
| `deplacer-fichier` | Deplacer | Deplacer ou renommer un fichier | X |
| `supprimer-dossier` | Supprimer | Supprimer un dossier recursivement | X |
| `rechercher-dossier` | Rechercher | Verifier si un dossier existe | X |

### Priorite P2 (confort - quand besoin)

| Outil | Categorie | Description |
|---|---|---|
| `lire-frontmatter` | Lire | Extraire le YAML en tete | X |
| `supprimer-ligne` | Supprimer | Supprimer une ligne par numero | X |
| `rechercher-extension-fichier` | Rechercher | Extraire l'extension | X |

---

## Total

| Priorite | Nombre |
|---|---|
| P0 | 8 (termine) |
| P1 | 7 (termine) |
| P2 | 3 (termine) |
| **Total** | **18 (termine)** |

---

## Remarques

1. **Nous avons deja** des outils specialises qui font certaines de ces operations :
   - `changer-statut` = deplacer/renommer (specialise)
   - `corriger-liens` = editer (specialise)
   - `lister-fichiers` = lister (pas lire le contenu)

2. **La difference** : les outils de base sont GENERIQUES et utilisables par TOUS les agents pour TOUTES les operations simples.

3. **L'avantage** : pouvoir modifier ces outils pour ajouter des verifications, du logging, des sauvegardes, etc.

---

## Statut

| Etape | Statut |
|---|---|
| Analyse de l'existant | Termine |
| Identification des manques | Termine |
| Creation des outils P0 | Termine |
| Creation des outils P1 | Termine |
| Creation des outils P2 | Termine |
| Integration aux agents | Termine (11 cartes de decision : cerberus, buffy, vulcain, atlas, athena, promethee, minerve, morpheus, janus, clio, themis) |