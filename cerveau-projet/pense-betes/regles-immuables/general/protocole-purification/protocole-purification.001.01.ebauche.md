# Protocole -- Purification des Fichiers
---

## Principe Fondamental
---

## Pourquoi ?

| Probleme | Solution |
|---|---|
| Fichiers trop longs | Supprimer le contenu non essentiel |
| Agent faineant a la lecture | Reduire le nombre de lignes |
| Informations redondantes | Garder uniquement l'essentiel |
| Notes de developpement | Supprimer apres validation |

---

## Quand purifier ?

```
APRES la validation d'un fichier
AVANT de considerer le fichier comme "valide"
```

### Cycle de vie d'un fichier

```
1. Creation (ebauche) -> contenu complet avec remarques
2. Developpement (dev) -> contenu en cours
3. Test -> validation
4. Purification -> nettoyage
5. Valide -> fichier pur
```

---

## Ce qu'il faut garder

| Contenu | Raison |
|---|---|
| **Regles absolues** | L'agent DOIT les suivre |
| **Protocoles applicables** | L'agent doit savoir quoi lire |
| **Instructions claires** | L'agent doit comprendre quoi faire |
| **Limites** | L'agent doit savoir ce qu'il ne PEUT PAS faire |
| **Tables de decision** | L'agent doit choisir rapidement |

---

## Ce qu'il faut supprimer

| Contenu | Raison |
|---|---|
| **Blockquotes explicatifs** | Trop de texte, pas essentiel |
| **Exemples detailles** | Suffit de mentionner l'existence |
| **Notes historiques** | Pas besoin pour fonctionner |
| **Justifications** | Les regles parlent d'elles-memes |
| **Rappels de contexte** | Le fichier doit etre autonome |

---

## Comment purifier

### Etape 1 -- Identifier le contenu a supprimer

```
1. Lire le fichier
2. Identifier les blockquotes avec des explications
3. Identifier les exemples trop detailles
4. Identifier les notes historiques
5. Lister ce qui peut etre supprime
```

### Etape 2 -- Verifier la coherence

```
1. Le fichier reste comprehensible ?
2. Les instructions restent claires ?
3. Les dependances restent visibles ?
4. Les limites restent definies ?
```

### Etape 3 -- Supprimer

```
1. Supprimer les blockquotes inutiles
2. Reduire les exemples au minimum
3. Supprimer les notes historiques
4. Simplifier les justifications
```

### Etape 4 -- Valider

```
1. Relire le fichier purifie
2. Verifier que l'agent peut fonctionner avec
3. Confirmer avec l'utilisateur si necessaire
```

---

## Exemple

### Avant (non purifie)

```markdown
## Regle 1
### Comment verifier

1. Executer verifier-systeme
2. Noter les resultats
3. Utiliser les resultats pour le choix
```

### Apres (purifie)

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

## Resume

| Element | Regle |
|---|---|
| **Quand** | Apres validation |
| **Quoi garder** | Regles, protocoles, instructions |
| **Quoi supprimer** | Remarks, exemples, notes |
| **Comment** | Etape par etape |
| **Validation** | Relire apres purification |

---

