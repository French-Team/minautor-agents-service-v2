# Convention -- Sous-Protocoles
---

## Principe Fondamental
---

## Pourquoi des sous-protocoles ?

| Probleme | Solution |
|---|---|
| Protocoles trop vagues | Sous-protocoles avec etapes detaillees |
| Manque de guidance | Questions structurees pour clarifier |
| Erreurs frequentes | Etapes de verification detaillees |
| Incoherence | Sous-protocoles standardises |

---

## Structure d'un sous-protocole

```
sous-protocole-[nom].md
|-- Objectif
|-- Prerequis
|-- Etapes detaillees
|-- Questions (si applicable)
|-- Verifications
``-- Liens vers le protocole parent
```

---

## Types de sous-protocoles

| Type | Description | Exemple |
|---|---|---|
| **Questions** | Serie de questions pour clarifier | `sous-protocole-questions-clartification.md` |
| **Evaluation** | Evaluer une situation | `sous-protocole-evaluer-projet.md` |
| **Diagnostic** | Diagnostiquer un probleme | `sous-protocole-diagnostic.md` |
| **Verification** | Verifier la conformite | `sous-protocole-verifier-conformite.md` |
| **Validation** | Valider un resultat | `sous-protocole-valider-travail.md` |

---

## Comment integrer un sous-protocole

### Dans un protocole principal

```markdown
## Etape 1 -- Clarifier les besoins
1. Poser les questions de clarification
2. Documenter les reponses
3. Valider avec l'utilisateur
```

### Dans un protocole de projet (ex: demarrer-projet)

```markdown
## Etape 1 -- Nouveau projet
1. Poser les questions de clarification
2. Creer le cerveau-projet
3. ...
```

> Note : `demarrer.md` est la porte d'entree de session (identification + parcours) --
> les etapes de projet vivent dans `protocole-demarrer-projet`, pas dans demarrer.md.

---

## Liste des sous-protocoles

| Sous-protocole | Protocole parent | Description |
|---|---|---|
| `sous-protocole-questions-clartification.md` | `protocole-demarrer-projet` | Questions pour clarifier les besoins |
| `sous-protocole-evaluer-projet.md` | `protocole-reprendre-projet` | Evaluer l'etat d'un projet |
| `sous-protocole-diagnostic.md` | `protocole-gestion-defaillances` | Diagnostiquer les problemes |
| `sous-protocole-validation.md` | Tous les protocoles | Valider le resultat |

---

## Regles des sous-protocoles

| Regle | Description |
|---|---|
| **Clarte** | Chaque etape est claire et precise |
| **Completude** | Tous les cas sont couverts |
| **Tracabilite** | Les resultats sont documentes |
| **Validation** | Chaque etape est validee |

---

## Relation avec les protocoles

| Concept | Role | Exemple |
|---|---|---|
| **Protocole** | QUOI faire | `protocole-demarrer-projet.md` |
| **Sous-protocole** | COMMENT le faire en detail | `sous-protocole-questions-clartification.md` |

---

## Navigation

- **Parent** : [index-protocoles.md](index-protocoles.md)
- **Protocoles** : [regles-immuables/general/](../../regles-immuables/general/index-regles-general.md)

---

*Convention conforme aux regles du cerveau-projet*
