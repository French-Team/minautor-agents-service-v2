# Sous-Protocole — Validation

---

## Objectif

S'assurer que le travail est complet, correct et conforme aux conventions.

---

## Prérequis

- Un travail a été effectué
- L'agent est identifié et prêt

---

## Niveaux de validation

| Niveau | Description | Quand l'utiliser |
|---|---|---|
| **Niveau 1** | Validation rapide | Modifications mineures |
| **Niveau 2** | Validation standard | Modifications moyennes |
| **Niveau 3** | Validation complète | Modifications majeures |
| **Niveau 4** | Validation critique | Changements d'architecture |

---

## Checklists par niveau

### Niveau 1 — Validation rapide

| # | Vérification | Critère |
|---|---|---|
| 1.1 | **Fichier créé/modifié** | Le fichier existe et est accessible |
| 1.2 | **Contenu cohérent** | Le contenu a du sens |
| 1.3 | **Pas d'erreur visible** | Pas de faute d'orthographe évidente |

### Niveau 2 — Validation standard

| # | Vérification | Critère |
|---|---|---|
| 2.1 | **Fichier créé/modifié** | Le fichier existe et est accessible |
| 2.2 | **Contenu cohérent** | Le contenu a du sens |
| 2.3 | **Convention respectée** | Le nommage est correct |
| 2.4 | **Liens valides** | Les liens internes fonctionnent |
| 2.5 | **Statut à jour** | Le statut est correct |
| 2.6 | **Historique documenté** | Les changements sont notés |

### Niveau 3 — Validation complète

| # | Vérification | Critère |
|---|---|---|
| 3.1-3.6 | **Toutes les vérifications niveau 2** | [OK] |
| 3.7 | **Structure cohérente** | La structure est logique |
| 3.8 | **Références à jour** | Les références sont correctes |
| 3.9 | **Index mis à jour** | Les index sont à jour |
| 3.10 | **RVAV appliqué** | Le cycle RVAV est respecté |

### Niveau 4 — Validation critique

| # | Vérification | Critère |
|---|---|---|
| 4.1 | **Toutes les vérifications niveau 3** | [OK] |
| 4.2 | **Tests effectués** | Les tests passent |
| 4.3 | **Documentation complète** | La documentation est à jour |
| 4.4 | **Dépendances vérifiées** | Les dépendances sont à jour |
| 4.5 | **Impact évalué** | L'est impact est compris |
| 4.6 | **Rollback planifié** | Un plan de retour arrière existe |
| 4.7 | **Validation utilisateur** | L'utilisateur a validé |

---

## Matrice de décision

| Type de modification | Niveau de validation |
|---|---|
| Correction de faute | Niveau 1 |
| Ajout de contenu simple | Niveau 2 |
| Modification de convention | Niveau 3 |
| Création de protocole | Niveau 3 |
| Changement d'architecture | Niveau 4 |
| Modification de règles immuables | Niveau 4 |

---

## Template de validation

```markdown
# Validation — [Nom de la modification]

## Niveau de validation
**Niveau** : [1/2/3/4]

## Checklist

| # | Vérification | Statut |
|---|---|---|
| 1 | [Vérification 1] | [OK] / [NON] / [PARTIEL] |
| 2 | [Vérification 2] | [OK] / [NON] / [PARTIEL] |
| 3 | [Vérification 3] | [OK] / [NON] / [PARTIEL] |

## Résultat
**Statut** : [Validé / Non validé / À corriger]

## Commentaires
[Notes et observations]
```

---

## Validation par RVAV

### Rechercher

```
1. Identifier les impacts de la modification
2. Vérifier les dépendances
3. Lister les fichiers concernés
```

### Vérifier

```
1. Confirmer que la modification est conforme
2. Vérifier que les conventions sont respectées
3. Valider que les liens sont corrects
```

### Analyser

```
1. Évaluer les conséquences
2. Identifier les risques
3. Proposer des mesures d'atténuation
```

### Valider

```
1. Accepter la modification
2. Ou demander des corrections
3. Documenter la décision
```

---

## Erreurs courantes de validation

| Erreur | Conséquence | Prévention |
|---|---|---|
| **Valider trop vite** | Erreurs non détectées | Suivre la checklist complète |
| **Oublier les liens** | Liens cassés | Vérifier tous les liens |
| **Oublier les index** | Index incohérents | Mettre à jour les index |
| **Oublier l'historique** | Pas de traçabilité | Documenter les changements |

---

## Liens

- **Convention** : `convention-sous-protocoles.md`
- **RVAV** : `rvav-workflow.md`
- **Validation rigoureuse** : `regles-validation-rigoureuse.md`

---

*Sous-protocole conforme aux conventions du cerveau-projet*
