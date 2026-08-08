---
identite:
  type: convention
  appartient_a: commun
  commun: true
---
# Convention de Structures -- Principes d'Architecture

---

## Principe Fondamental

---

## Regles

| Regle | Principe |
|---|---|
| **R1** | La racine = config + demarrage uniquement |
| **R2** | Un dossier = un niveau inferieur |
| **R3** | Tout fichier = point d'entree (orchestrateur) |
| **R4** | Une fonction = un dossier au niveau inferieur |
| **R5** | Reorganiser = reordonner les appels |
| **R6** | Modules autonomes, pas de partage de dossiers |
| **R7** | Les chemins = moyen de recherche |
| **R8** | Extension verticale uniquement |

---

## Detail des regles

### R1 -- La racine est sacree

La racine du projet ne contient **que** :

| Type | Exemples |
|---|---|
| Fichiers de config | `package.json`, `.env`, `tsconfig.json` |
| Fichiers de demarrage | `demarrer.md`, `index-cerveau.md` |
| Dossiers de contenu | `pense-betes/`, `src/` |

**Rien d'autre** ne vit a la racine.

### R2 -- Un dossier = un niveau inferieur

```
niveau-0/
|-- fichier-A.md          <- point d'entree du dossier
|-- sous-fonction-X/      <- niveau +1
|   ``-- sous-fonction-X.md
``-- sous-fonction-Y/      <- niveau +1
    ``-- sous-fonction-Y.md
```

Chaque dossier est un **conteneur autonome**.

### R3 -- Tout fichier est un point d'entree

Un fichier ne contient **jamais** de code d'implementation directe.

Son role unique : **orchestrer les appels** aux fonctions/sous-modules qu'il contient.

### R4 -- Une fonction = un dossier

Une fonction n'est **jamais** creee inline dans un fichier.

Elle vit dans son propre dossier, au **niveau inferieur** par rapport au fichier qui l'appelle.

```
mon-horloge/
|-- mon-horloge.md           <- appelle heure/, minute/, seconde/
|-- heure/
|   ``-- heure.md             <- implemente la logique "heure"
|-- minute/
|   ``-- minute.md            <- implemente la logique "minute"
``-- seconde/
    ``-- seconde.md           <- implemente la logique "seconde"
```

### R5 -- Reorganisation = reordonner les appels

Pour changer l'ordre d'execution, on deplace simplement les appels dans le fichier point d'entree.

**Avant :**
```markdown
1. Appeler heure
2. Appeler minute
3. Appeler seconde
```

**Apres :**
```markdown
1. Appeler minute
2. Appeler heure
3. Appeler seconde
```

Aucun code n'est deplace. Seul l'**ordre des appels** change.

### R6 -- Modules autonomes (pas de partage)

Si un module a besoin d'un dossier `data/`, ce dossier vit **dans sa structure**.

Si un autre module a aussi besoin d'un `data/`, il a **son propre** `data/`.

**Jamais de dossier partage entre modules.**

### R7 -- Les chemins = la recherche

| Ce que je cherche | Ou je regarde |
|---|---|
| Une fonction | Un dossier au niveau inferieur du point d'entree |
| Les sous-fonctions | Les sous-dossiers dans le dossier de la fonction |
| La config | La racine du projet |
| Les donnees | Le dossier `data/` dans le module concerne |

### R8 -- Extension verticale uniquement

On ajoute un nouveau niveau **uniquement** en creant un sous-dossier.

On ne place **jamais** de fichier directement dans un conteneur sans l'encapsuler dans un dossier.

```
# [OK] Correct
mon-module/
|-- mon-module.md
``-- ma-fonction/
    ``-- ma-fonction.md

# [ERREUR] Incorrect
mon-module/
|-- mon-module.md
``-- ma-fonction.md        <- pas de dossier = pas de niveau
```

---

## Application au cerveau-projet

```
cerveau-projet/                     <- racine (L0)
|-- index-cerveau.md                <- point d'entree global
|-- demarrer.md                     <- config/demarrage
|-- agents/                         <- dossier (L1)
|   |-- index-agents.md             <- point d'entree L1
|   |-- conventions/                <- dossier (L2)
|   |   |-- index-conventions.md    <- point d'entree L2
|   |   ``-- structures/             <- dossier (L3)
|   |       ``-- index-structures.md <- point d'entree L3
|   |-- regles-immuables/           <- dossier (L2)
|   |   ``-- index-regles-immuables.md
|   |-- classeur-variables/         <- dossier (L2)
|   |   ``-- index-classeur.md
|   ``-- tools/                     <- dossier (L2)
|-- pense-betes/                    <- dossier (L1)
|   |-- index-pense-bete.md         <- point d'entree L1
|   ``-- specs/                      <- dossier (L2)
|       ``-- index-spec.md
```

Chaque fichier est un point d'entree. Chaque dossier descend d'un niveau.

---

## Lien avec les regles de hierarchie

-> Consulter `../regles-immuables/hierarchie/regles-hierarchie-par-niveau.md`

---

## Voir aussi

- [convention-classeur-variables.md](convention-classeur-variables.md) -- stockage partage pour les pipelines
- [convention-pipelines.md](convention-pipelines.md) -- pipelines de traitement de donnees
