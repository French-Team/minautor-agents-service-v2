# Index -- Regles pour les Fichiers
---

## Definition

Un **fichier** est un orchestrateur qui :
- Vit dans un dossier (son niveau)
- Est le point d'entree unique de ce dossier
- Contient une liste d'**appels** aux sous-composants
- Ne contient **pas** de logique metier inline

---

## Regles des fichiers

### 1. Jamais de code inline

Un fichier point d'entree ne contient **jamais** de fonctions, de classes, ou de logique metier directe.

Son role unique : **appeler** les composants qui vivent dans ses sous-dossiers.

```
# [OK] Correct -- orchestration par appels
mon-module.md:
1. Appeler fonction-A
2. Appeler fonction-B
3. Appeler fonction-C

# [NON] Incorrect -- code inline
mon-module.md:
function A() { ... }     <- interdit
function B() { ... }     <- interdit
```

### 2. Reordonnancement facile

La structure par appels permet de changer l'ordre d'execution en deplacant simplement les lignes d'appel.

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

### 3. Parametres d'activation

Chaque appel peut recevoir des arguments type pour activer/desactiver un composant :

```markdown
1. Appeler heure (activer: true)
2. Appeler minute (activer: true)
3. Appeler seconde (activer: false)    <- desactive
```

Cela permet de :
- Desactiver temporairement un composant
- Configurer le comportement sans modifier le code
- Tester differentes configurations

### 4. Tracabilite par le chemin

Le chemin du fichier indique exactement ou l'on se trouve dans la hierarchie :

| Chemin | Signification |
|---|---|
| `module-A/module-A.md` | Point d'entree du module A |
| `module-A/fonction-X/fonction-X.md` | Fonction X dans le module A |
| `module-A/fonction-X/sous-fonction-Y/sous-fonction-Y.md` | Sous-fonction Y de la fonction X |

### 5. Single responsibility

Un fichier a **un seul role** : orchestrer.

Il ne fait rien d'autre. Pas de calcul, pas de transformation, pas de logique.

---

## Structure type d'un fichier point d'entree

```markdown
# Nom du Module

## Description
[Brief description du module]

## Composants

| # | Composant | Role | Actif |
|---|---|---|---|
| 1 | [fonction-A](fonction-A/fonction-A.md) | [Description] | [OK] |
| 2 | [fonction-B](fonction-B/fonction-B.md) | [Description] | [OK] |
| 3 | [fonction-C](fonction-C/fonction-C.md) | [Description] | [NON] |

## Orchestration

1. Appeler fonction-A
2. Appeler fonction-B
3. ~~Appeler fonction-C~~ (desactive)

## Configuration

| Parametre | Valeur | Description |
|---|---|---|
| [param] | [valeur] | [description] |
```

---

## Relation avec les dossiers

-> Consulter `../dossiers/index-dossiers.md` pour les regles des dossiers.
