# Sous-Protocole — Diagnostic
---

## Objectif

Identifier la cause racine d'un problème et proposer une solution.

---

## Prérequis

- Un problème a été identifié
- L'agent est identifié et prêt

---

## Étapes de diagnostic

### Étape 1 — Identifier les symptômes

| # | Question | Objectif |
|---|---|---|
| 1.1 | **Quel est le problème ?** | Décrire le symptôme |
| 1.2 | **Quand est-il survenu ?** | Situer dans le temps |
| 1.3 | **Qu'est-ce qui a changé ?** | Identifier la cause potentielle |
| 1.4 | **Quel est l'impact ?** | Évaluer la gravité |

### Étape 2 — Explorer les causes possibles

| # | Cause | Vérification |
|---|---|---|
| 2.1 | **Erreur humaine** | Vérifier les actions récentes |
| 2.2 | **Configuration** | Vérifier les paramètres |
| 2.3 | **Dépendance** | Vérifier les liens |
| 2.4 | **Version** | Vérifier les mises à jour |
| 2.5 | **Environnement** | Vérifier le contexte |

### Étape 3 — Tester les hypothèses

| # | Hypothèse | Test | Résultat |
|---|---|---|---|
| 3.1 | [Hypothèse 1] | [Test 1] | [Résultat 1] |
| 3.2 | [Hypothèse 2] | [Test 2] | [Résultat 2] |
| 3.3 | [Hypothèse 3] | [Test 3] | [Résultat 3] |

### Étape 4 — Identifier la cause racine

| # | Cause racine | Confiance | Impact |
|---|---|---|---|
| 4.1 | [Cause 1] | [Haute/Moyenne/Basse] | [Élevé/Moyen/Faible] |
| 4.2 | [Cause 2] | [Haute/Moyenne/Basse] | [Élevé/Moyen/Faible] |
| 4.3 | [Cause 3] | [Haute/Moyenne/Basse] | [Élevé/Moyen/Faible] |

### Étape 5 — Proposer une solution

| # | Solution | Complexité | Impact |
|---|---|---|---|
| 5.1 | [Solution 1] | [Faible/Moyenne/Élevée] | [Positif/Neutre/Négatif] |
| 5.2 | [Solution 2] | [Faible/Moyenne/Élevée] | [Positif/Neutre/Négatif] |
| 5.3 | [Solution 3] | [Faible/Moyenne/Élevée] | [Positif/Neutre/Négatif] |

---

## Utiliser nos outils
| Besoin | Outil du cerveau |
|---|---|
| Lister les fichiers | `lister-fichiers` |
| Lister les dossiers | `lister-dossiers` |
| Valider les liens | `valider-liens` |
| Analyser la structure | `analyser-structure` |
| Demander à l'utilisateur | `ask_user` |

---

## Template de diagnostic

```markdown
# Diagnostic — [Nom du problème]

## Symptômes
- **Problème** : [description]
- **Quand** : [moment]
- **Changements** : [ce qui a changé]
- **Impact** : [gravité]

## Causes possibles
1. [Cause 1] : [vérification]
2. [Cause 2] : [vérification]
3. [Cause 3] : [vérification]

## Tests effectués
1. [Test 1] : [résultat]
2. [Test 2] : [résultat]
3. [Test 3] : [résultat]

## Cause racine identifiée
**Cause** : [description]
**Confiance** : [Haute/Moyenne/Basse]
**Impact** : [Élevé/Moyen/Faible]

## Solutions proposées
1. [Solution 1] : [complexité] / [impact]
2. [Solution 2] : [complexité] / [impact]
3. [Solution 3] : [complexité] / [impact]

## Recommandation
**Solution recommandée** : [description]
**Justification** : [pourquoi cette solution]
```

---

## Validation

Avant de valider le diagnostic, vérifier :

- [ ] Les symptômes sont décrits
- [ ] Les causes sont identifiées
- [ ] Les tests sont effectués
- [ ] La cause racine est identifiée
- [ ] Les solutions sont proposées

---

## Liens

- **Protocole parent** : `protocole-gestion-defaillances.md`
- **Convention** : `convention-sous-protocoles.md`
- **Évaluation** : `sous-protocole-evaluer-projet.md`

---

*Sous-protocole conforme aux conventions du cerveau-projet*
