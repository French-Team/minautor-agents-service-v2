---
# Protocole — Boucles Dynamiques (Sous-missions)
# Sortie et retour du flux principal

protocole:
  nom: "protocole-boucles-dynamiques"
  version: "001.01"
  statut: "ebauche"
  cree: "2026-08-05"
  auteur: "Buffy"
  immutable: true
---

# Boucles Dynamiques — Sous-missions

> **RÈGLE ABSOLUE** : Les boucles permettent de SORTIR du flux principal

---

## Objectif

Résoudre le problème des outils manquants en permettant à l'agent de :
1. **Détecter** qu'un outil est nécessaire mais inexistant
2. **Sortir** du flux principal
3. **Créer/reprendre** l'outil manquant
4. **Revenir** au flux principal avec l'outil disponible

---

## Le concept

### Avant (boucles statiques)

```
Mission principale
    ↓
Étape 1 : Vérifier le système
    ↓
PROBLÈME : verifier-systeme n'existe pas
    ↓
Vulcain continue quand même (ERREUR !)
```

### Après (boucles dynamiques)

```
Mission principale
    ↓
Étape 1 : Vérifier le système
    ↓
DETECTÉ : verifier-systeme n'existe pas
    ↓
[SOUS-MISSION] Créer verifier-systeme
    ↓
    1. Lire les specs de l'outil
    2. Développer l'outil
    3. Tester l'outil
    4. Valider l'outil
    ↓
[RETOUR] Mission principale reprend
    ↓
Étape 1 : Vérifier le système (MAIS MAINTENANT L'OUTIL EXISTE !)
    ↓
Continuer normalement
```

---

## Structure d'une boucle dynamique

### 1. Détection

**QUAND** : À chaque étape de la carte de décision

**COMMENT** :
```
1. Identifier l'outil nécessaire pour cette étape
2. Vérifier si l'outil existe
3. Si non -> SOUS-MISSION obligatoire
4. Si oui -> Continuer
```

### 2. Sortie du flux

**ACTION** :
```
1. Sauvegarder la position dans la mission principale
   - Étape en cours
   - Données collectées
   - Objectif final
2. Marquer la sous-mission comme "en cours"
3. Commencer la sous-mission
```

### 3. Exécution de la sous-mission

**MISSION** : Créer/reprendre l'outil manquant

**Étapes** :
```
1. Lire la spécification de l'outil
2. Vérifier le système (si nécessaire)
3. Développer l'outil
4. Tester l'outil
5. Valider l'outil
6. Documenter l'outil
```

### 4. Retour au flux principal

**ACTION** :
```
1. Confirmer que l'outil est disponible
2. Reprendre à l'étape sauvegardée
3. Continuer la mission principale
```

---

## Règles d'or

| Règle | Description |
|---|---|
| **R1** | Toujours sauvegarder avant de sortir |
| **R2** | Toujours revenir après une sous-mission |
| **R3** | Ne jamais abandonner la mission principale |
| **R4** | Documenter chaque sortie/retrée |

---

## Format de documentation

### Sortie

```markdown
## SOUS-MISSION DÉTECTÉE

| Champ | Valeur |
|---|---|
| **Mission principale** | [description] |
| **Étape en cours** | [étape] |
| **Outi nécessaire** | [nom-outil] |
| **Raison** | [pourquoi cet outil est nécessaire] |

### Position sauvegardée
- Étape : [numéro]
- Données : [ce qui a été collecté]
- Objectif : [ce qu'on essayait de faire]
```

### Retour

```markdown
## RETOUR AU FLUX PRINCIPAL

| Champ | Valeur |
|---|---|
| **Sous-mission** | [description] |
| **Résultat** | [succès/échec] |
| **Outil créé** | [oui/non] |
| **Durée** | [temps] |

### Reprise
- On reprend à l'étape : [numéro]
- L'outil est maintenant disponible : [oui/non]
```

---

## Outils nécessaires

| Outil | Usage | Statut |
|---|---|---|
| `gerer-sous-mission` | Gérer les sorties/retrées | À créer |
| `verifier-systeme` | Vérifier le système | À créer |
| `valider-cartes-decision` | Valider les outils | Créé |

---

## Fréquence

- **À chaque étape** : Vérifier si un outil est nécessaire
- **Si outil manquant** : Sous-mission obligatoire
- **Après chaque sous-mission** : Toujours revenir
