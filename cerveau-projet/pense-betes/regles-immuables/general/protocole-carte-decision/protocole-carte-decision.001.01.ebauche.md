# Protocole -- Carte de Decision pour les Agents

**Version** : 0.1.0
**Statut** : Ebauche
**Date creation** : 2026-08-05
**Agent** : Buffy (creation)

---

## Objectif

Transformer les fichiers d'agent en **cartes de decision** ou chaque mission a un chemin precis avec les protocoles a lire a chaque etape.

**Pourquoi ce protocole ?**
- Les agents supposent au lieu de verifier
- Les agents lisent trop de contexte inutilement
- Les agents ne respectent pas les protocoles
- Le contexte devient trop lourd

---

## Le probleme actuel

### Avant (methode actuelle)

```
1. Agent lit TOUT le fichier d'agent (100+ lignes)
2. Agent lit TOUTES les corrections (100+ lignes)
3. Agent a 200+ lignes en memoire
4. Agent execute la mission
5. Beaucoup de contexte inutile
```

### Problemes

| Probleme | Consequence |
|---|---|
| **Trop de contexte** | L'agent est submerge |
| **Suppositions** | L'agent ne verifie pas |
| **Protocoles oublies** | L'agent ne les lit pas |
| **Erreurs repetees** | L'agent ne corrige pas |

---

## La solution : Carte de Decision

### Principe

Le fichier d'agent devient une **carte de decision** :

```
SI [mission X] ALORS [ligne X] -> [etapes] -> [protocoles a lire]
```

### Structure

```markdown
## Carte de Decision

### Mission : Construire un outil

| Etape | Action | Protocole | Contexte |
|---|---|---|---|
| 1 | Verifier le systeme | verifier-systeme | Systeme utilisateur |
| 2 | Choisir la technologie | protocole-technologies | Technologies disponibles |
| 3 | Developper l'outil | protocole-outils | Specifications |
| 4 | Tester l'outil | protocole-tests | Resultats des tests |
| 5 | Valider l'outil | sous-protocole-validation | Criteres de validation |
```

---

## Comment ca fonctionne

### Etape 1 : Identification de la mission

```
1. L'agent recoit une mission
2. Il cherche dans sa carte de decision
3. Il trouve la ligne correspondante
4. Il suit les etapes de cette ligne
```

### Etape 2 : Execution progressive

```
ETAPE 1 : Verifier le systeme
  -> Lire : verifier-systeme
  -> Resultat : Systeme connu
  -> Contexte : [systeme utilisateur]

ETAPE 2 : Choisir la technologie
  -> Lire : protocole-technologies
  -> Resultat : Technologie choisie
  -> Contexte : [technologies disponibles]

ETAPE 3 : Developper l'outil
  -> Lire : protocole-outils
  -> Resultat : Outil cree
  -> Contexte : [specifications]
```

### Etape 3 : Gestion du contexte

**Avant** : 200+ lignes en memoire tout le temps
**Apres** : 20-30 lignes par etape (uniquement le protocole en cours)

---

## Format de la carte de decision

### Template

```markdown
## Carte de Decision

### Missions disponibles

| Mission | Etapes | Protocoles |
|---|---|---|
| [Mission 1] | [etape1] -> [etape2] -> [etape3] | [proto1], [proto2], [proto3] |
| [Mission 2] | [etape1] -> [etape2] | [proto1], [proto2] |

### Detail des missions

#### Mission : [Nom de la mission]

| Etape | Action | Protocole | Sortie |
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

## Role
- Transformer les outils.md en outils reels
- Choisir les technologies
- Developper les outils
- Tester les outils
- Documenter les choix

## Processus
1. Lire l'outil.md
2. Analyser les besoins
3. Choisir la technologie
4. Developper
5. Tester
6. Valider
```

**Probleme** : Vulcain ne sait PAS qu'il doit d'abord verifier le systeme.

### Apres (carte de decision)

```markdown
# Vulcain

## Carte de Decision

### Mission : Construire un outil

| Etape | Action | Protocole | Sortie |
|---|---|---|---|
| 1 | Verifier le systeme | verifier-systeme | Systeme connu |
| 2 | Lire l'outil.md | - | Besoins connus |
| 3 | Choisir la technologie | protocole-technologies | Technologie choisie |
| 4 | Developper l'outil | protocole-outils | Outil cree |
| 5 | Tester l'outil | protocole-tests | Tests passes |
| 6 | Valider l'outil | sous-protocole-validation | Outil valide |

### Regle absolue

> **ETAPE 1 OBLIGATOIRE** : Toujours verifier le systeme AVANT de choisir une technologie.
```

---

## Avantages

| Avant | Apres |
|---|---|
| L'agent lit tout au debut | L'agent lit a chaque etape |
| 200+ lignes en memoire | 20-30 lignes par etape |
| L'agent suppose | L'agent verifie |
| Protocoles oublies | Protocoles lus a chaque etape |
| Erreurs repetees | Erreurs corrigees |

---

## Implementation

### Pour chaque agent

1. Creer une section "Carte de Decision"
2. Lister toutes les missions possibles
3. Pour chaque mission, lister les etapes
4. Pour chaque etape, lister le protocole a lire
5. Ajouter des regles absolues

### Pour chaque mission

1. Identifier les etapes
2. Identifier les protocoles
3. Identifier les sorties de chaque etape
4. Documenter les dependances

---

## Notes importantes

- **Chaque etape a UN protocole** a lire
- **Le contexte est remplace** a chaque etape
- **Les regles absolues** sont mises en avant
- **Les erreurs sont documentees** dans les corrections

---

> **Ce protocole est IMMUABLE.**
