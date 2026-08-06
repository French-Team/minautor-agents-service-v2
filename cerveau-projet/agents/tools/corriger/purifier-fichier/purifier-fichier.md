# Outil — Purifier un Fichier

**Catégorie** : Corriger
**Version** : 0.1.0-beta
**Statut** : beta
**Date création** : 2026-08-05
**Propriétaire** : Vulcain (outil partagé)

---

## Objectif

Purifier un fichier en supprimant le contenu non essentiel.

**Pourquoi cet outil ?**
- Les fichiers contiennent trop de remarques et blockquotes
- Les agents sont fainéants à la lecture
- Un fichier pur est plus facile à lire et à maintenir

---

## Utilisation

```
purifier-fichier [fichier] [options]
```

---

## Paramètres

| Paramètre | Type | Obligatoire | Description |
|---|---|---|---|
| `fichier` | string | Oui | Chemin du fichier à purifier |
| `--dry-run` | flag | Non | Afficher les changements sans les appliquer |
| `--verbose` | flag | Non | Afficher les détails |
| `--aide` | flag | Non | Afficher l'aide |

---

## Ce que fait l'outil

### 1. Supprimer les blockquotes explicatifs

```
-> Supprimé
```

### 2. Réduire les exemples

```
### Exemple

1. Étape 1
2. Étape 2
3. Étape 3
4. Étape 4
5. Étape 5
-> Réduit au minimum
```

### 3. Supprimer les notes historiques

```
## Historique

| Date | Événement |
|---|---|
| 2026-08-01 | Création |
-> Supprimé
```

### 4. Simplifier les justifications

```
-> Supprimé
```

---

## Exemple

### Avant

```markdown
## Règle 1
### Comment vérifier

1. Exécuter verifier-systeme
2. Noter les résultats
3. Utiliser les résultats pour le choix
```

### Après

```markdown
## Règle 1

VÉRIFIER le système AVANT de choisir une technologie.

| Étape | Action |
|---|---|
| 1 | Exécuter `verifier-systeme` |
| 2 | Noter les résultats |
| 3 | Utiliser pour le choix |
```

---

## Dépendances

- Aucune dépendance externe

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-05 | Création initiale |

---

