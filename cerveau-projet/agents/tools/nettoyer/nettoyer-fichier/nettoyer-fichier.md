# Outil -- Purifier un Fichier

**Categorie** : Nettoyer
**Version** : 0.1.0-beta
**Statut** : beta
**Date creation** : 2026-08-05
**Proprietaire** : Vulcain (outil partage)

---

## Objectif

Purifier un fichier en supprimant le contenu non essentiel.

**Pourquoi cet outil ?**
- Les fichiers contiennent trop de remarques et blockquotes
- Les agents sont faineants a la lecture
- Un fichier pur est plus facile a lire et a maintenir

---

## Utilisation

```
nettoyer-fichier [fichier] [options]
```

---

## Parametres

| Parametre | Type | Obligatoire | Description |
|---|---|---|---|
| `fichier` | string | Oui | Chemin du fichier a purifier |
| `--dry-run` | flag | Non | Afficher les changements sans les appliquer |
| `--verbose` | flag | Non | Afficher les details |
| `--aide` | flag | Non | Afficher l'aide |

---

## Ce que fait l'outil

### 1. Supprimer les blockquotes explicatifs

```
-> Supprime
```

### 2. Reduire les exemples

```
### Exemple

1. Etape 1
2. Etape 2
3. Etape 3
4. Etape 4
5. Etape 5
-> Reduit au minimum
```

### 3. Supprimer les notes historiques

```
## Historique

| Date | Evenement |
|---|---|
| 2026-08-01 | Creation |
-> Supprime
```

### 4. Simplifier les justifications

```
-> Supprime
```

---

## Exemple

### Avant

```markdown
## Regle 1
### Comment verifier

1. Executer verifier-systeme
2. Noter les resultats
3. Utiliser les resultats pour le choix
```

### Apres

```markdown
## Regle 1

VERIFIER le systeme AVANT de choisir une technologie.

| Etape | Action |
|---|---|
| 1 | Executer `verifier-systeme` |
| 2 | Noter les resultats |
| 3 | Utiliser pour le choix |
```

---

## Dependances

- Aucune dependance externe

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-05 | Creation initiale |

---

