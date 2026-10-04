---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
# Convention de Protocoles -- Mise en Place
---

## Principe Fondamental
---

## Quand creer un protocole ?

Creer un protocole des qu'une situation **se repete** ou **doit etre standardisee** :

| Signal | Action |
|---|---|
| Meme tache effectuee 2+ fois | Creer un protocole |
| Decision structurelle importante | Creer un protocole |
| Processus qui doit etre reproductible | Creer un protocole |
| Regle qui s'applique "partout" | Creer un protocole |

---

## Structure d'un protocole

Chaque protocole suit un **template standard** :

```
protocole-[nom].[id].[class].[statut].md
```

### En-tete obligatoire

```markdown
# Protocole de [Nom]
**Portee :** [Ou ce protocole s'applique]
**Prerequis :** [Ce qu'il faut avoir avant de l'appliquer]
```

### Sections standard

| # | Section | Obligatoire | Description |
|---|---|---|---|
| 1 | **Objectif** | [OUI] | Ce que le protocole permet d'atteindre |
| 2 | **Prerequis** | [OUI] | Conditions necessaires avant application |
| 3 | **Etapes** | [OUI] | Liste ordonnee des actions a effectuer |
| 4 | **RVAV** | [OUI] | Verification a chaque etape critique |
| 5 | **Exemples** | [NON] | Cas d'usage concrets (optionnel) |
| 6 | **Pieges courants** | [NON] | Erreurs frequentes a eviter (optionnel) |
| 7 | **Liens** | [OUI] | References aux conventions et regles applicables |

---

## Processus de creation

### Etape 1 -- Identifier le besoin

```
1. La tache se repete-elle ? -> OUI = protocole
2. Doit-elle etre standardisee ? -> OUI = protocole
3. Est-elle reproductible ? -> OUI = protocole
```

### Etape 2 -- Verifier l'existence

```
1. Chercher dans regles-immuables/general/protocole-*/
2. Chercher dans conventions/protocoles/
3. Si un protocole similaire existe -> l'etendre, pas en creer un nouveau
```

### Etape 3 -- Creer le protocole

```
1. Copier le template (ci-dessus)
2. Nommer selon la convention : protocole-[nom].[id].[class].[statut].md
3. Placer dans : regles-immuables/general/protocole-[nom]/
4. Creer le dossier avec :
   |-- protocole-[nom].[id].[class].[statut].md  <- le protocole
   |-- spec/                                       <- spec technique (si besoin)
   ``-- todo/                                       <- taches liees (si besoin)
```

### Etape 4 -- Documenter la conception

```
1. Creer une note dans conventions/protocoles/
2. Expliquer POURQUOI ce protocole a ete cree
3. Lier vers le protocole dans regles-immuables/
```

### Etape 5 -- Passer par RVAV

Appliquer le cycle complet :
- [rechercher] -- verifier les dependances et prerequis
- [verifier] -- confirmer que le template est respecte
- [analyser] -- valider la coherence avec les autres protocoles
- [valider] -- approuver pour utilisation

---

## Integration des protocoles

### Ou placer un protocole ?

| Type de protocole | Emplacement |
|---|---|
| Protocole general (process, workflow) | `regles-immuables/general/protocole-[nom]/` |
| Protocole hierarchique | `regles-immuables/hierarchie/protocole-[nom]/` |
| Protocole specifique a un module | `agents/[module]/protocole-[nom]/` |

### Comment referencer un protocole ?

Dans tout fichier qui utilise le protocole, ajouter :

```markdown
## Protocoles applicables

- [protocole-[nom]](../../regles-immuables/general/protocole-[nom]/)
```

### Comment devenir un automatisme ?

1. **Documenter** dans le protocole les cas d'usage
2. **Lier** le protocole dans les fichiers concernes
3. **Repeter** jusqu'a ce que l'habitude soit prise
4. **Verifier** lors des RVAV que les protocoles sont respectes

---

## Patterns courants

### Pattern 1 -- Protocole de creation

```
Quand creer : un nouveau composant/dossier/fichier
Etapes :
1. Verifier la convention de structures
2. Creer le dossier au bon niveau
3. Creer la plateforme (point d'entree)
4. Creer les sous-dossiers necessaires
5. Passer par RVAV
```

### Pattern 2 -- Protocole de modification

```
Quand creer : modifier un composant existant
Etapes :
1. Lire le protocole existant
2. Verifier les dependances
3. Modifier la plateforme (pas le code inline)
4. Mettre a jour les liens
5. Passer par RVAV
```

### Pattern 3 -- Protocole d'integration

```
Quand creer : integrer un protocole dans un nouveau contexte
Etapes :
1. Identifier le protocole a integrer
2. Verifier la compatibilite
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

## Recapitulatif

| Element | Regle |
|---|---|
| **Quand** | Des qu'une tache se repete ou doit etre standardisee |
| **Ou creer** | `regles-immuables/general/protocole-[nom]/` |
| **Ou documenter** | `conventions/protocoles/` |
| **Template** | En-tete + 7 sections (voir ci-dessus) |
| **Nom** | `protocole-[nom].[id].[class].[statut].md` |
| **Validation** | Toujours passer par RVAV |
| **Integration** | Lier dans les fichiers concernes |
| **Automatisme** | Documenter -> Lier -> Repeter -> Verifier |
