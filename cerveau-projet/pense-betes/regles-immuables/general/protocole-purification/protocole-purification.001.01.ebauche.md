# Protocole — Purification des Fichiers
---

## Principe Fondamental
---

## Pourquoi ?

| Problème | Solution |
|---|---|
| Fichiers trop longs | Supprimer le contenu non essentiel |
| Agent fainéant à la lecture | Réduire le nombre de lignes |
| Informations redondantes | Garder uniquement l'essentiel |
| Notes de développement | Supprimer après validation |

---

## Quand purifier ?

```
APRÈS la validation d'un fichier
AVANT de considérer le fichier comme "valide"
```

### Cycle de vie d'un fichier

```
1. Création (ebauche) → contenu complet avec remarques
2. Développement (dev) → contenu en cours
3. Test → validation
4. Purification → nettoyage
5. Validé → fichier pur
```

---

## Ce qu'il faut garder

| Contenu | Raison |
|---|---|
| **Règles absolues** | L'agent DOIT les suivre |
| **Protocoles applicables** | L'agent doit savoir quoi lire |
| **Instructions claires** | L'agent doit comprendre quoi faire |
| **Limites** | L'agent doit savoir ce qu'il ne PEUT PAS faire |
| **Tables de décision** | L'agent doit choisir rapidement |

---

## Ce qu'il faut supprimer

| Contenu | Raison |
|---|---|
| **Blockquotes explicatifs** | Trop de texte, pas essentiel |
| **Exemples détaillés** | Suffit de mentionner l'existence |
| **Notes historiques** | Pas besoin pour fonctionner |
| **Justifications** | Les règles parlent d'elles-mêmes |
| **Rappels de contexte** | Le fichier doit être autonome |

---

## Comment purifier

### Étape 1 — Identifier le contenu à supprimer

```
1. Lire le fichier
2. Identifier les blockquotes avec des explications
3. Identifier les exemples trop détaillés
4. Identifier les notes historiques
5. Lister ce qui peut être supprimé
```

### Étape 2 — Vérifier la cohérence

```
1. Le fichier reste compréhensible ?
2. Les instructions restent claires ?
3. Les dépendances restent visibles ?
4. Les limites restent définies ?
```

### Étape 3 — Supprimer

```
1. Supprimer les blockquotes inutiles
2. Réduire les exemples au minimum
3. Supprimer les notes historiques
4. Simplifier les justifications
```

### Étape 4 — Valider

```
1. Relire le fichier purifié
2. Vérifier que l'agent peut fonctionner avec
3. Confirmer avec l'utilisateur si nécessaire
```

---

## Exemple

### Avant (non purifié)

```markdown
## Règle 1
### Comment vérifier

1. Exécuter verifier-systeme
2. Noter les résultats
3. Utiliser les résultats pour le choix
```

### Après (purifié)

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

## Résumé

| Élément | Règle |
|---|---|
| **Quand** | Après validation |
| **Quoi garder** | Règles, protocoles, instructions |
| **Quoi supprimer** | Remarks, exemples, notes |
| **Comment** | Étape par étape |
| **Validation** | Relire après purification |

---

