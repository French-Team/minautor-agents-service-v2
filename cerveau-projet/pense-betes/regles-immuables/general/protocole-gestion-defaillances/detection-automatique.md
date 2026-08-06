# Détection Automatique des Défaillances
---

## Vérifications obligatoires

### 1. Fichier AGENTS.md

| Vérification | Critère | Action si échec |
|---|---|---|
| **AGENTS.md existe** | Fichier présent à la racine | Créer le fichier |
| **Agent principal identifié** | Section "Agent Principal Actuel" remplie | Mettre à jour |
| **Agent actuel identifié** | Mon nom est dans le fichier | Se présenter |
| **Historique à jour** | Dernière entrée récente | Ajouter une entrée |

### 2. Fiche d'agent

| Vérification | Critère | Action si échec |
|---|---|---|
| **Fiche existe** | `agents/[nom]/[nom].md` existe | Créer la fiche |
| **Fiche à jour** | Dernière session documentée | Mettre à jour |
| **Corrections lues** | `corrections.md` lu en priorité | Lire les corrections |
| **Corrections appliquées** | Règles spécifiques appliquées | Appliquer les règles |

### 3. Index principaux

| Vérification | Critère | Action si échec |
|---|---|---|
| **index-cerveau.md** | Statut à jour | Mettre à jour |
| **index-regles-general.md** | Tous les protocoles listés | Ajouter les manquants |
| **index-conventions.md** | Toutes les conventions listées | Ajouter les manquantes |

### 4. Conventions

| Vérification | Critère | Action si échec |
|---|---|---|
| **Fichiers existent** | Tous les fichiers référencés existent | Créer les fichiers |
| **Liens valides** | Tous les liens pointent vers des fichiers existants | Corriger les liens |
| **Statut à jour** | Statut correct dans chaque fichier | Mettre à jour |

### 5. Protocoles

| Vérification | Critère | Action si échec |
|---|---|---|
| **Protocoles existent** | Tous les protocoles référencés existent | Créer les protocoles |
| **Protocoles à jour** | Dernière modification documentée | Mettre à jour |
| **Protocoles respectés** | Les étapes sont suivies | Suivre le protocole |

---

## Vérifications périodiques

### Hebdomadaires

| Vérification | Critère | Action si échec |
|---|---|---|
| **Cohérence générale** | Toutes les sections cohérentes | Harmoniser |
| **Liens cassés** | Tous les liens valides | Corriger |
| **Statuts à jour** | Tous les statuts corrects | Mettre à jour |

### Mensuelles

| Vérification | Critère | Action si échec |
|---|---|---|
| **Archivage** | Éléments obsolètes archivés | Archiver |
| **Amélioration** | Protocoles améliorés si nécessaire | Améliorer |
| **Documentation** | Documentation complète | Compléter |

---

## Déclencheurs automatiques

### Déclenchement immédiat

| Déclencheur | Action |
|---|---|
| **AGENTS.md manquant** | Créer immédiatement |
| **Fiche agent manquante** | Créer immédiatement |
| **Incohérence majeure** | Corriger immédiatement |
| **Protocole non suivi** | Appliquer immédiatement |

### Déclenche à la prochaine session

| Déclencheur | Action |
|---|---|
| **Index pas à jour** | Mettre à jour |
| **Lien cassé** | Corriger |
| **Statut incorrect** | Corriger |

### Déclenche quand possible

| Déclencheur | Action |
|---|---|
| **Amélioration mineure** | Appliquer |
| **Documentation incomplète** | Compléter |
| **Archivage nécessaire** | Archiver |

---

## Comment signaler une défaillance

### Si tu détectes une défaillance

```
1. Noter la défaillance :
   - Type (oubli, erreur, incohérence, manque, obsolète)
   - Fichier concerné
   - Priorité (haute, moyenne, basse)
   - Description

2. Appliquer la correction si possible

3. Si la correction nécessite une validation :
   - Créer un pense-bête
   - Demander validation à l'utilisateur

4. Documenter la défaillance et la correction
```

### Si tu es l'auteur de la défaillance

```
1. Accepter la défaillance
2. Appliquer la correction
3. Ajouter une règle dans corrections.md si nécessaire
4. Documenter l'amélioration
```

---

## Priorités

| Priorité | Délai | Exemple |
|---|---|---|
| **Haute** | Immédiat | AGENTS.md manquant, incohérence majeure |
| **Moyenne** | Avant prochaine session | Index pas à jour, lien cassé |
| **Basse** | Quand possible | Amélioration mineure |

---

## Navigation

- **Parent** : [protocole-gestion-defaillances.md](protocole-gestion-defaillances.001.01.ebauche.md)
- **Protocoles** : [index-regles-general.md](../../index-regles-general.md)

---

*Détection automatique conforme aux conventions du cerveau-projet*
