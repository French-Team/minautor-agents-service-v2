# Spécification — Protocole de Contrôle des Statuts

**Version** : 0.1.0
**Statut** : Ébauche
**Date création** : 2026-08-05
**Agent** : Buffy (création)

---

## Objectif

Spécifier le protocole de contrôle des statuts pour Janus.

---

## Besoins fonctionnels

### Entrées

| Entrée | Type | Description |
|---|---|---|
| `fichier` | string | Chemin du fichier à contrôler |
| `action` | string | Type de contrôle (transition, audit, ponctuel) |

### Sorties

| Sortie | Type | Description |
|---|---|---|
| `decision` | string | Validé / Rejeté / Reporté |
| `justification` | string | Raison de la décision |
| `action` | string | Prochaine étape |

---

## Besoins techniques

### Vérifications

```python
def verifier_boucle_rvav(fichier):
    # 1. Vérifier les références
    # 2. Vérifier la checklist
    # 3. Vérifier la cohérence
    # 4. Retourner les résultats
    pass
```

### Décision

```python
def prendre_decision(resultats):
    if tout_correct(resultats):
        return "validé"
    elif erreur_mineure(resultats):
        return "rejeté"
    elif erreur_majeure(resultats):
        return "rejeté"
    else:
        return "reporté"
```

---

## Spécification des tests

### Test 1 : Validation réussie

**Entrée** : Fichier avec boucle RVAV complète
**Résultat attendu** : Decision = "validé"

### Test 2 : Rejet pour erreur

**Entrée** : Fichier avec erreur détectée
**Résultat attendu** : Decision = "rejeté"

### Test 3 : Report pour information manquante

**Entrée** : Fichier avec informations manquantes
**Résultat attendu** : Decision = "reporté"

---

## Architecture

```
protocole-controle-statuts/
|-- protocole-controle-statuts.md      # Le protocole
|-- spec/
|   ``-- spec-protocole-controle-statuts.md  # Cette spécification
``-- todo/
    ``-- todo-protocole-controle-statuts.md   # Tâches
```

---

## Contraintes

- Janus doit être indépendant de Buffy
- Le contrôle doit être documenté
- Le cycle Cerberus -> Janus -> Cerberus doit être respecté
- Les outils de validation doivent être utilisés

---

## Critères de succès

| Critère | Mesure |
|---|---|
| **Indépendance** | Janus ne dépend pas de Buffy |
| **Complétude** | Toutes les vérifications sont faites |
| **Documentation** | Chaque décision est justifiée |
| **Intégration** | Le cycle est respecté |

---

