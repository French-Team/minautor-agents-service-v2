# Index — Règles pour les Fichiers
---

## Définition

Un **fichier** est un orchestrateur qui :
- Vit dans un dossier (son niveau)
- Est le point d'entrée unique de ce dossier
- Contient une liste d'**appels** aux sous-composants
- Ne contient **pas** de logique métier inline

---

## Règles des fichiers

### 1. Jamais de code inline

Un fichier point d'entrée ne contient **jamais** de fonctions, de classes, ou de logique métier directe.

Son rôle unique : **appeler** les composants qui vivent dans ses sous-dossiers.

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

### 2. Réordonnancement facile

La structure par appels permet de changer l'ordre d'exécution en déplaçant simplement les lignes d'appel.

**Avant :**
```markdown
1. Appeler heure
2. Appeler minute
3. Appeler seconde
```

**Après :**
```markdown
1. Appeler minute
2. Appeler heure
3. Appeler seconde
```

Aucun code n'est déplacé. Seul l'**ordre des appels** change.

### 3. Paramètres d'activation

Chaque appel peut recevoir des arguments type pour activer/désactiver un composant :

```markdown
1. Appeler heure (activer: true)
2. Appeler minute (activer: true)
3. Appeler seconde (activer: false)    <- désactivé
```

Cela permet de :
- Désactiver temporairement un composant
- Configurer le comportement sans modifier le code
- Tester différentes configurations

### 4. Traçabilité par le chemin

Le chemin du fichier indique exactement où l'on se trouve dans la hiérarchie :

| Chemin | Signification |
|---|---|
| `module-A/module-A.md` | Point d'entrée du module A |
| `module-A/fonction-X/fonction-X.md` | Fonction X dans le module A |
| `module-A/fonction-X/sous-fonction-Y/sous-fonction-Y.md` | Sous-fonction Y de la fonction X |

### 5. Single responsibility

Un fichier a **un seul rôle** : orchestrer.

Il ne fait rien d'autre. Pas de calcul, pas de transformation, pas de logique.

---

## Structure type d'un fichier point d'entrée

```markdown
# Nom du Module

## Description
[Brief description du module]

## Composants

| # | Composant | Rôle | Actif |
|---|---|---|---|
| 1 | [fonction-A](fonction-A/fonction-A.md) | [Description] | [OK] |
| 2 | [fonction-B](fonction-B/fonction-B.md) | [Description] | [OK] |
| 3 | [fonction-C](fonction-C/fonction-C.md) | [Description] | [NON] |

## Orchestration

1. Appeler fonction-A
2. Appeler fonction-B
3. ~~Appeler fonction-C~~ (désactivé)

## Configuration

| Paramètre | Valeur | Description |
|---|---|---|
| [param] | [valeur] | [description] |
```

---

## Relation avec les dossiers

-> Consulter `../dossiers/index-dossiers.md` pour les règles des dossiers.
