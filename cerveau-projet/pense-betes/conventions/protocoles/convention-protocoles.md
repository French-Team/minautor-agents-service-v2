# Convention de Protocoles — Mise en Place
---

## Principe Fondamental
---

## Quand créer un protocole ?

Créer un protocole dès qu'une situation **se répète** ou **doit être standardisée** :

| Signal | Action |
|---|---|
| Même tâche effectuée 2+ fois | Créer un protocole |
| Décision structurelle importante | Créer un protocole |
| Processus qui doit être reproductible | Créer un protocole |
| Règle qui s'applique "partout" | Créer un protocole |

---

## Structure d'un protocole

Chaque protocole suit un **template standard** :

```
protocole-[nom].[id].[class].[statut].md
```

### En-tête obligatoire

```markdown
# Protocole de [Nom]
**Portée :** [Où ce protocole s'applique]
**Prérequis :** [Ce qu'il faut avoir avant de l'appliquer]
```

### Sections standard

| # | Section | Obligatoire | Description |
|---|---|---|---|
| 1 | **Objectif** | [OUI] | Ce que le protocole permet d'atteindre |
| 2 | **Prérequis** | [OUI] | Conditions nécessaires avant application |
| 3 | **Étapes** | [OUI] | Liste ordonnée des actions à effectuer |
| 4 | **RVAV** | [OUI] | Vérification à chaque étape critique |
| 5 | **Exemples** | [NON] | Cas d'usage concrets (optionnel) |
| 6 | **Pièges courants** | [NON] | Erreurs fréquentes à éviter (optionnel) |
| 7 | **Liens** | [OUI] | Références aux conventions et règles applicables |

---

## Processus de création

### Étape 1 — Identifier le besoin

```
1. La tâche se répète-elle ? → OUI = protocole
2. Doit-elle être standardisée ? → OUI = protocole
3. Est-elle reproductible ? → OUI = protocole
```

### Étape 2 — Vérifier l'existence

```
1. Chercher dans regles-immuables/general/protocole-*/
2. Chercher dans conventions/protocoles/
3. Si un protocole similaire existe → l'étendre, pas en créer un nouveau
```

### Étape 3 — Créer le protocole

```
1. Copier le template (ci-dessus)
2. Nommer selon la convention : protocole-[nom].[id].[class].[statut].md
3. Placer dans : regles-immuables/general/protocole-[nom]/
4. Créer le dossier avec :
   ├── protocole-[nom].[id].[class].[statut].md  ← le protocole
   ├── spec/                                       ← spec technique (si besoin)
   └── todo/                                       ← tâches liées (si besoin)
```

### Étape 4 — Documenter la conception

```
1. Créer une note dans conventions/protocoles/
2. Expliquer POURQUOI ce protocole a été créé
3. Lier vers le protocole dans regles-immuables/
```

### Étape 5 — Passer par RVAV

Appliquer le cycle complet :
- [rechercher] — vérifier les dépendances et prérequis
- [vérifier] — confirmer que le template est respecté
- [analyser] — valider la cohérence avec les autres protocoles
- [valider] — approuver pour utilisation

---

## Intégration des protocoles

### Où placer un protocole ?

| Type de protocole | Emplacement |
|---|---|
| Protocole général (process, workflow) | `regles-immuables/general/protocole-[nom]/` |
| Protocole hiérarchique | `regles-immuables/hierarchie/protocole-[nom]/` |
| Protocole spécifique à un module | `pense-betes/[module]/protocole-[nom]/` |

### Comment référencer un protocole ?

Dans tout fichier qui utilise le protocole, ajouter :

```markdown
## Protocoles applicables

- [protocole-[nom]](../../regles-immuables/general/protocole-[nom]/)
```

### Comment devenir un automatisme ?

1. **Documenter** dans le protocole les cas d'usage
2. **Lier** le protocole dans les fichiers concernés
3. **Répéter** jusqu'à ce que l'habitude soit prise
4. **Vérifier** lors des RVAV que les protocoles sont respectés

---

## Patterns courants

### Pattern 1 — Protocole de création

```
Quand créer : un nouveau composant/dossier/fichier
Étapes :
1. Vérifier la convention de structures
2. Créer le dossier au bon niveau
3. Créer la plateforme (point d'entrée)
4. Créer les sous-dossiers nécessaires
5. Passer par RVAV
```

### Pattern 2 — Protocole de modification

```
Quand créer : modifier un composant existant
Étapes :
1. Lire le protocole existant
2. Vérifier les dépendances
3. Modifier la plateforme (pas le code inline)
4. Mettre à jour les liens
5. Passer par RVAV
```

### Pattern 3 — Protocole d'intégration

```
Quand créer : intégrer un protocole dans un nouveau contexte
Étapes :
1. Identifier le protocole à intégrer
2. Vérifier la compatibilité
3. Adapter le protocole au contexte
4. Documenter l'adaptation
5. Passer par RVAV
```

---

## Protocoles existants

| Protocole | Description | Emplacement |
|---|---|---|
| [protocole-composition](../../regles-immuables/general/protocole-composition/) | Composition du squelette de base | general/ |
| [protocole-auto-correction](../../regles-immuables/general/protocole-auto-correction/) | Auto-correction des agents | general/ |

---

## Récapitulatif

| Élément | Règle |
|---|---|
| **Quand** | Dès qu'une tâche se répète ou doit être standardisée |
| **Où créer** | `regles-immuables/general/protocole-[nom]/` |
| **Où documenter** | `conventions/protocoles/` |
| **Template** | En-tête + 7 sections (voir ci-dessus) |
| **Nom** | `protocole-[nom].[id].[class].[statut].md` |
| **Validation** | Toujours passer par RVAV |
| **Intégration** | Lier dans les fichiers concernés |
| **Automatisme** | Documenter → Lier → Répéter → Vérifier |
