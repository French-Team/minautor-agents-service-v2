---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
# Sous-Protocole -- Diagnostic
---

## Objectif

Identifier la cause racine d'un probleme et proposer une solution.

---

## Prerequis

- Un probleme a ete identifie
- L'agent est identifie et pret

---

## Etapes de diagnostic

### Etape 1 -- Identifier les symptomes

| # | Question | Objectif |
|---|---|---|
| 1.1 | **Quel est le probleme ?** | Decrire le symptome |
| 1.2 | **Quand est-il survenu ?** | Situer dans le temps |
| 1.3 | **Qu'est-ce qui a change ?** | Identifier la cause potentielle |
| 1.4 | **Quel est l'impact ?** | Evaluer la gravite |

### Etape 2 -- Explorer les causes possibles

| # | Cause | Verification |
|---|---|---|
| 2.1 | **Erreur humaine** | Verifier les actions recentes |
| 2.2 | **Configuration** | Verifier les parametres |
| 2.3 | **Dependance** | Verifier les liens |
| 2.4 | **Version** | Verifier les mises a jour |
| 2.5 | **Environnement** | Verifier le contexte |

### Etape 3 -- Tester les hypotheses

| # | Hypothese | Test | Resultat |
|---|---|---|---|
| 3.1 | [Hypothese 1] | [Test 1] | [Resultat 1] |
| 3.2 | [Hypothese 2] | [Test 2] | [Resultat 2] |
| 3.3 | [Hypothese 3] | [Test 3] | [Resultat 3] |

### Etape 4 -- Identifier la cause racine

| # | Cause racine | Confiance | Impact |
|---|---|---|---|
| 4.1 | [Cause 1] | [Haute/Moyenne/Basse] | [Eleve/Moyen/Faible] |
| 4.2 | [Cause 2] | [Haute/Moyenne/Basse] | [Eleve/Moyen/Faible] |
| 4.3 | [Cause 3] | [Haute/Moyenne/Basse] | [Eleve/Moyen/Faible] |

### Etape 5 -- Proposer une solution

| # | Solution | Complexite | Impact |
|---|---|---|---|
| 5.1 | [Solution 1] | [Faible/Moyenne/Elevee] | [Positif/Neutre/Negatif] |
| 5.2 | [Solution 2] | [Faible/Moyenne/Elevee] | [Positif/Neutre/Negatif] |
| 5.3 | [Solution 3] | [Faible/Moyenne/Elevee] | [Positif/Neutre/Negatif] |

---

## Utiliser nos outils

| Besoin | Outil du cerveau |
|---|---|
| Lister les fichiers | `lister-fichiers` |
| Lister les dossiers | `lister-dossiers` |
| Valider les liens | `valider-liens` |
| Analyser la structure | `analyser-structure` |
| Demander a l'utilisateur | Question directe (pas d'outil tiers) |

---

## Template de diagnostic

```markdown
# Diagnostic -- [Nom du probleme]

## Symptomes
- **Probleme** : [description]
- **Quand** : [moment]
- **Changements** : [ce qui a change]
- **Impact** : [gravite]

## Causes possibles
1. [Cause 1] : [verification]
2. [Cause 2] : [verification]
3. [Cause 3] : [verification]

## Tests effectues
1. [Test 1] : [resultat]
2. [Test 2] : [resultat]
3. [Test 3] : [resultat]

## Cause racine identifiee
**Cause** : [description]
**Confiance** : [Haute/Moyenne/Basse]
**Impact** : [Eleve/Moyen/Faible]

## Solutions proposees
1. [Solution 1] : [complexite] / [impact]
2. [Solution 2] : [complexite] / [impact]
3. [Solution 3] : [complexite] / [impact]

## Recommandation
**Solution recommandee** : [description]
**Justification** : [pourquoi cette solution]
```

---

## Validation

Avant de valider le diagnostic, verifier :

- [ ] Les symptomes sont decrits
- [ ] Les causes sont identifiees
- [ ] Les tests sont effectues
- [ ] La cause racine est identifiee
- [ ] Les solutions sont proposees

---

## Liens

- **Protocole parent** : `protocole-gestion-defaillances.md`
- **Convention** : `convention-sous-protocoles.md`
- **Evaluation** : `sous-protocole-evaluer-projet.md`

---

*Sous-protocole conforme aux conventions du cerveau-projet*
