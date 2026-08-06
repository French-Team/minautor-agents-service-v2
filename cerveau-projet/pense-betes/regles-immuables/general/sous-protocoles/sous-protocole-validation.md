# Sous-Protocole -- Validation

---

## Objectif

S'assurer que le travail est complet, correct et conforme aux conventions.

---

## Prerequis

- Un travail a ete effectue
- L'agent est identifie et pret

---

## Niveaux de validation

| Niveau | Description | Quand l'utiliser |
|---|---|---|
| **Niveau 1** | Validation rapide | Modifications mineures |
| **Niveau 2** | Validation standard | Modifications moyennes |
| **Niveau 3** | Validation complete | Modifications majeures |
| **Niveau 4** | Validation critique | Changements d'architecture |

---

## Checklists par niveau

### Niveau 1 -- Validation rapide

| # | Verification | Critere |
|---|---|---|
| 1.1 | **Fichier cree/modifie** | Le fichier existe et est accessible |
| 1.2 | **Contenu coherent** | Le contenu a du sens |
| 1.3 | **Pas d'erreur visible** | Pas de faute d'orthographe evidente |

### Niveau 2 -- Validation standard

| # | Verification | Critere |
|---|---|---|
| 2.1 | **Fichier cree/modifie** | Le fichier existe et est accessible |
| 2.2 | **Contenu coherent** | Le contenu a du sens |
| 2.3 | **Convention respectee** | Le nommage est correct |
| 2.4 | **Liens valides** | Les liens internes fonctionnent |
| 2.5 | **Statut a jour** | Le statut est correct |
| 2.6 | **Historique documente** | Les changements sont notes |

### Niveau 3 -- Validation complete

| # | Verification | Critere |
|---|---|---|
| 3.1-3.6 | **Toutes les verifications niveau 2** | [OK] |
| 3.7 | **Structure coherente** | La structure est logique |
| 3.8 | **References a jour** | Les references sont correctes |
| 3.9 | **Index mis a jour** | Les index sont a jour |
| 3.10 | **RVAV applique** | Le cycle RVAV est respecte |

### Niveau 4 -- Validation critique

| # | Verification | Critere |
|---|---|---|
| 4.1 | **Toutes les verifications niveau 3** | [OK] |
| 4.2 | **Tests effectues** | Les tests passent |
| 4.3 | **Documentation complete** | La documentation est a jour |
| 4.4 | **Dependances verifiees** | Les dependances sont a jour |
| 4.5 | **Impact evalue** | L'est impact est compris |
| 4.6 | **Rollback planifie** | Un plan de retour arriere existe |
| 4.7 | **Validation utilisateur** | L'utilisateur a valide |

---

## Matrice de decision

| Type de modification | Niveau de validation |
|---|---|
| Correction de faute | Niveau 1 |
| Ajout de contenu simple | Niveau 2 |
| Modification de convention | Niveau 3 |
| Creation de protocole | Niveau 3 |
| Changement d'architecture | Niveau 4 |
| Modification de regles immuables | Niveau 4 |

---

## Template de validation

```markdown
# Validation -- [Nom de la modification]

## Niveau de validation
**Niveau** : [1/2/3/4]

## Checklist

| # | Verification | Statut |
|---|---|---|
| 1 | [Verification 1] | [OK] / [NON] / [PARTIEL] |
| 2 | [Verification 2] | [OK] / [NON] / [PARTIEL] |
| 3 | [Verification 3] | [OK] / [NON] / [PARTIEL] |

## Resultat
**Statut** : [Valide / Non valide / A corriger]

## Commentaires
[Notes et observations]
```

---

## Validation par RVAV

### Rechercher

```
1. Identifier les impacts de la modification
2. Verifier les dependances
3. Lister les fichiers concernes
```

### Verifier

```
1. Confirmer que la modification est conforme
2. Verifier que les conventions sont respectees
3. Valider que les liens sont corrects
```

### Analyser

```
1. Evaluer les consequences
2. Identifier les risques
3. Proposer des mesures d'attenuation
```

### Valider

```
1. Accepter la modification
2. Ou demander des corrections
3. Documenter la decision
```

---

## Erreurs courantes de validation

| Erreur | Consequence | Prevention |
|---|---|---|
| **Valider trop vite** | Erreurs non detectees | Suivre la checklist complete |
| **Oublier les liens** | Liens casses | Verifier tous les liens |
| **Oublier les index** | Index incoherents | Mettre a jour les index |
| **Oublier l'historique** | Pas de tracabilite | Documenter les changements |

---

## Liens

- **Convention** : `convention-sous-protocoles.md`
- **RVAV** : `rvav-workflow.md`
- **Validation rigoureuse** : `regles-validation-rigoureuse.md`

---

*Sous-protocole conforme aux conventions du cerveau-projet*
