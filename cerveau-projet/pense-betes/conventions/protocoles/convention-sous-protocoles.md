# Convention — Sous-Protocoles
---

## Principe Fondamental
---

## Pourquoi des sous-protocoles ?

| Problème | Solution |
|---|---|
| Protocoles trop vagues | Sous-protocoles avec étapes détaillées |
| Manque de guidance | Questions structurées pour clarifier |
| Erreurs fréquentes | Étapes de vérification détaillées |
| Incohérence | Sous-protocoles standardisés |

---

## Structure d'un sous-protocole

```
sous-protocole-[nom].md
├── Objectif
├── Prérequis
├── Étapes détaillées
├── Questions (si applicable)
├── Vérifications
└── Liens vers le protocole parent
```

---

## Types de sous-protocoles

| Type | Description | Exemple |
|---|---|---|
| **Questions** | Série de questions pour clarifier | `sous-protocole-questions-clartification.md` |
| **Évaluation** | Évaluer une situation | `sous-protocole-evaluer-projet.md` |
| **Diagnostic** | Diagnostiquer un problème | `sous-protocole-diagnostic.md` |
| **Vérification** | Vérifier la conformité | `sous-protocole-verifier-conformite.md` |
| **Validation** | Valider un résultat | `sous-protocole-valider-travail.md` |

---

## Comment intégrer un sous-protocole

### Dans un protocole principal

```markdown
## Étape 1 — Clarifier les besoins
1. Poser les questions de clarification
2. Documenter les réponses
3. Valider avec l'utilisateur
```

### Dans demarrer.md

```markdown
## Étape 1 — Nouveau projet
1. Poser les questions de clarification
2. Créer le cerveau-projet
3. ...
```

---

## Liste des sous-protocoles

| Sous-protocole | Protocole parent | Description |
|---|---|---|
| `sous-protocole-questions-clartification.md` | `protocole-demarrer-projet` | Questions pour clarifier les besoins |
| `sous-protocole-evaluer-projet.md` | `protocole-reprendre-projet` | Évaluer l'état d'un projet |
| `sous-protocole-diagnostic.md` | `protocole-gestion-defaillances` | Diagnostiquer les problèmes |
| `sous-protocole-validation.md` | Tous les protocoles | Valider le résultat |

---

## Règles des sous-protocoles

| Règle | Description |
|---|---|
| **Clarté** | Chaque étape est claire et précise |
| **Complétude** | Tous les cas sont couverts |
| **Traçabilité** | Les résultats sont documentés |
| **Validation** | Chaque étape est validée |

---

## Relation avec les protocoles

| Concept | Rôle | Exemple |
|---|---|---|
| **Protocole** | QUOI faire | `protocole-demarrer-projet.md` |
| **Sous-protocole** | COMMENT le faire en détail | `sous-protocole-questions-clartification.md` |

---

## Navigation

- **Parent** : [index-protocoles.md](index-protocoles.md)
- **Protocoles** : [regles-immuables/general/](../../regles-immuables/general/index-regles-general.md)

---

*Convention conforme aux règles du cerveau-projet*
