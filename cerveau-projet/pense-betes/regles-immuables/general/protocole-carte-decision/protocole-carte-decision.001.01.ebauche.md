# Protocole — Carte de Décision pour les Agents

**Version** : 0.1.0
**Statut** : Ébauche
**Date création** : 2026-08-05
**Agent** : Buffy (création)

---

## Objectif

Transformer les fichiers d'agent en **cartes de décision** où chaque mission a un chemin précis avec les protocoles à lire à chaque étape.

**Pourquoi ce protocole ?**
- Les agents supposent au lieu de vérifier
- Les agents lisent trop de contexte inutilement
- Les agents ne respectent pas les protocoles
- Le contexte devient trop lourd

---

## Le problème actuel

### Avant (méthode actuelle)

```
1. Agent lit TOUT le fichier d'agent (100+ lignes)
2. Agent lit TOUTES les corrections (100+ lignes)
3. Agent a 200+ lignes en mémoire
4. Agent exécute la mission
5. Beaucoup de contexte inutile
```

### Problèmes

| Problème | Conséquence |
|---|---|
| **Trop de contexte** | L'agent est submergé |
| **Suppositions** | L'agent ne vérifie pas |
| **Protocoles oubliés** | L'agent ne les lit pas |
| **Erreurs répétées** | L'agent ne corrige pas |

---

## La solution : Carte de Décision

### Principe

Le fichier d'agent devient une **carte de décision** :

```
SI [mission X] ALORS [ligne X] → [étapes] → [protocoles à lire]
```

### Structure

```markdown
## Carte de Décision

### Mission : Construire un outil

| Étape | Action | Protocole | Contexte |
|---|---|---|---|
| 1 | Vérifier le système | verifier-systeme | Système utilisateur |
| 2 | Choisir la technologie | protocole-technologies | Technologies disponibles |
| 3 | Développer l'outil | protocole-outils | Spécifications |
| 4 | Tester l'outil | protocole-tests | Résultats des tests |
| 5 | Valider l'outil | protocole-validation | Critères de validation |
```

---

## Comment ça fonctionne

### Étape 1 : Identification de la mission

```
1. L'agent reçoit une mission
2. Il cherche dans sa carte de décision
3. Il trouve la ligne correspondante
4. Il suit les étapes de cette ligne
```

### Étape 2 : Exécution progressive

```
ÉTAPE 1 : Vérifier le système
  → Lire : verifier-systeme
  → Résultat : Système connu
  → Contexte : [système utilisateur]

ÉTAPE 2 : Choisir la technologie
  → Lire : protocole-technologies
  → Résultat : Technologie choisie
  → Contexte : [technologies disponibles]

ÉTAPE 3 : Développer l'outil
  → Lire : protocole-outils
  → Résultat : Outil créé
  → Contexte : [spécifications]
```

### Étape 3 : Gestion du contexte

**Avant** : 200+ lignes en mémoire tout le temps
**Après** : 20-30 lignes par étape (uniquement le protocole en cours)

---

## Format de la carte de décision

### Template

```markdown
## Carte de Décision

### Missions disponibles

| Mission | Étapes | Protocoles |
|---|---|---|
| [Mission 1] | [étape1] → [étape2] → [étape3] | [proto1], [proto2], [proto3] |
| [Mission 2] | [étape1] → [étape2] | [proto1], [proto2] |

### Détail des missions

#### Mission : [Nom de la mission]

| Étape | Action | Protocole | Sortie |
|---|---|---|---|
| 1 | [Action 1] | [protocole-1] | [sortie-1] |
| 2 | [Action 2] | [protocole-2] | [sortie-2] |
| 3 | [Action 3] | [protocole-3] | [sortie-3] |
```

---

## Exemple : Vulcain

### Avant (fichier actuel)

```markdown
# Vulcain

## Rôle
- Transformer les outils.md en outils réels
- Choisir les technologies
- Développer les outils
- Tester les outils
- Documenter les choix

## Processus
1. Lire l'outil.md
2. Analyser les besoins
3. Choisir la technologie
4. Développer
5. Tester
6. Valider
```

**Problème** : Vulcain ne sait PAS qu'il doit d'abord vérifier le système.

### Après (carte de décision)

```markdown
# Vulcain

## Carte de Décision

### Mission : Construire un outil

| Étape | Action | Protocole | Sortie |
|---|---|---|---|
| 1 | Vérifier le système | verifier-systeme | Système connu |
| 2 | Lire l'outil.md | - | Besoins connus |
| 3 | Choisir la technologie | protocole-technologies | Technologie choisie |
| 4 | Développer l'outil | protocole-outils | Outil créé |
| 5 | Tester l'outil | protocole-tests | Tests passés |
| 6 | Valider l'outil | protocole-validation | Outil validé |

### Règle absolue

> **ÉTAPE 1 OBLIGATOIRE** : Toujours vérifier le système AVANT de choisir une technologie.
```

---

## Avantages

| Avant | Après |
|---|---|
| L'agent lit tout au début | L'agent lit à chaque étape |
| 200+ lignes en mémoire | 20-30 lignes par étape |
| L'agent suppose | L'agent vérifie |
| Protocoles oubliés | Protocoles lus à chaque étape |
| Erreurs répétées | Erreurs corrigées |

---

## Implémentation

### Pour chaque agent

1. Créer une section "Carte de Décision"
2. Lister toutes les missions possibles
3. Pour chaque mission, lister les étapes
4. Pour chaque étape, lister le protocole à lire
5. Ajouter des règles absolues

### Pour chaque mission

1. Identifier les étapes
2. Identifier les protocoles
3. Identifier les sorties de chaque étape
4. Documenter les dépendances

---

## Notes importantes

- **Chaque étape a UN protocole** à lire
- **Le contexte est remplacé** à chaque étape
- **Les règles absolues** sont mises en avant
- **Les erreurs sont documentées** dans les corrections

---

> **Ce protocole est IMMUABLE.**
