# Spec — Protocole Gestion des Défaillances
---

## Objectif technique

Détecter et corriger automatiquement les défaillances du cerveau-projet.

---

## Architecture

```
protocole-gestion-defaillances/
|-- protocole-gestion-defaillances.001.01.ebauche.md  <- le protocole
|-- spec/                                               <- CE FICHIER
``-- todo/                                               <- tâches liées
```

---

## Données d'entrée

| Donnée | Source | Obligatoire |
|---|---|---|
| État du cerveau | `index-cerveau.md` | [OK] |
| Protocoles existants | `regles-immuables/general/` | [OK] |
| Conventions existantes | `conventions/` | [OK] |
| Fichiers d'agent | `agents/` | [OK] |

---

## Données de sortie

| Donnée | Destination | Format |
|---|---|---|
| Défaillances détectées | Log interne | Liste |
| Corrections appliquées | Fichiers concernés | Modifications |
| Historique | Fichiers concernés | Entrées |

---

## Algorithme de détection

```markdown
1. LIRE index-cerveau.md
2. POUR CHAQUE fichier référencé :
   a. VÉRIFIER que le fichier existe
   b. VÉRIFIER que le lien est correct
   c. VÉRIFIER que le statut est à jour
3. POUR CHAQUE protocole :
   a. VÉRIFIER que le protocole est à jour
   b. VÉRIFIER que le protocole est respecté
4. POUR CHAQUE agent :
   a. VÉRIFIER que la fiche est à jour
   b. VÉRIFIER que les corrections sont appliquées
5. SI défaillance détectée :
   a. CLASSER la défaillance
   b. APPLIQUER la correction
   c. TRAITER la cause racine
   d. DOCUMENTER
```

---

## Algorithme de correction

```markdown
1. CLASSER la défaillance (oubli, erreur, incohérence, manque, obsolète)
2. ÉVALUER la priorité (haute, moyenne, basse)
3. APPLIQUER la correction appropriée :
   - Oubli -> Mettre à jour
   - Erreur -> Corriger
   - Incohérence -> Harmoniser
   - Manque -> Créer
   - Obsolète -> Mettre à jour ou archiver
4. VÉRIFIER que la correction est conforme
5. METTRE À JOUR les fichiers concernés
6. METTRE À JOUR les index
7. DOCUMENTER
```

---

## Contraintes

| Contrainte | Description |
|---|---|
| **Automatique** | La détection doit être automatique |
| **Immédiat** | Les défaillances hautes priorité sont corrigées immédiatement |
| **Traçable** | Chaque correction est documentée |
| **Préventif** | Les causes racines sont traitées |

---

## Tests

| Test | Critère |
|---|---|
| **Test de détection** | Les défaillances sont détectées |
| **Test de correction** | Les corrections sont appliquées |
| **Test de traçabilité** | Les corrections sont documentées |
| **Test de prévention** | Les récidives sont évitées |

---

## Navigation

- **Parent** : [protocole-gestion-defaillances.md](../protocole-gestion-defaillances.001.01.ebauche.md)
- **Todo** : [todo-protocole-gestion-defaillances.md](../todo/todo-protocole-gestion-defaillances.001.01.ebauche.md)

---

*Spécification conforme aux conventions du cerveau-projet*
