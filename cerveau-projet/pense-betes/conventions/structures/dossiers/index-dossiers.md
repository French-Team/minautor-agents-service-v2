# Index -- Regles pour les Dossiers
---

## Definition

Un **dossier** est un conteneur qui :
- Abaisse d'un niveau la profondeur d'imbrication
- Contient exactement **un fichier point d'entree** (plateforme)
- Contient des **sous-dossiers** pour chaque composant
- Est **autonome** (pas de dependances externes)

---

## Regles des dossiers

### 1. Un dossier = un niveau

Creer un dossier descend d'un niveau dans la hierarchie.

```
niveau-0/
|-- niveau-1/           <- niveau +1
|   |-- niveau-2/       <- niveau +2
|   |   ``-- niveau-3/   <- niveau +3
```

Le nom du dossier n'a aucune incidence sur le niveau. Seule la **profondeur** compte.

### 2. Plateforme obligatoire

Chaque dossier **doit** contenir un fichier point d'entree :

| Type de dossier | Pattern de plateforme |
|---|---|
| Dossier racine (L0) | `index-[categorie].md` ou `[nom].md` |
| Dossier intermediaire | `index-[categorie].md` |
| Dossier module | `[nom-module].md` |
| Dossier fonction | `[nom-fonction].md` |

La plateforme est le **seul point d'entree** du dossier.

### 3. Pas de fichiers orphelins

Un fichier ne vit **jamais** directement dans un dossier sans etre la plateforme.

```
# [OK] Correct
mon-dossier/
|-- mon-dossier.md        <- plateforme
|-- sous-fonction-A/      <- dossier enfant
``-- sous-fonction-B/      <- dossier enfant

# [NON] Incorrect
mon-dossier/
|-- mon-dossier.md
|-- fichier-quelconque.md    <- orphan = interdit
```

### 4. Autonomie totale

Un dossier ne partage **jamais** de ressources avec un autre dossier.

Si deux dossiers ont besoin du meme type de contenu (ex: `data/`), chacun a **son propre** dossier.

```
# [OK] Correct -- chaque module a son propre data/
module-A/
|-- module-A.md
``-- data/
    ``-- data.md

module-B/
|-- module-B.md
``-- data/
    ``-- data.md

# [NON] Incorrect -- data partage = couplage
module-A/
``-- module-B/
    ``-- data/          <- partage = dangereux
```

### 5. Extension verticale

On ajoute un niveau **uniquement** par un sous-dossier.

On ne place **jamais** de fichier au meme niveau que la plateforme.

---

## Structure type d'un dossier

```
mon-dossier/
|-- mon-dossier.md          <- plateforme (point d'entree)
|-- composant-A/            <- sous-dossier niveau +1
|   |-- composant-A.md      <- plateforme du sous-dossier
|   |-- sous-a1/
|   |   ``-- sous-a1.md
|   ``-- sous-a2/
|       ``-- sous-a2.md
``-- composant-B/
    ``-- composant-B.md
```

---

## Relation avec les fichiers

-> Consulter `../fichiers/index-fichiers.md` pour les regles des fichiers.
