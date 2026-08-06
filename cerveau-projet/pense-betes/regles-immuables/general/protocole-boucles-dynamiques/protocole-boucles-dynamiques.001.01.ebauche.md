---
# Protocole -- Boucles Dynamiques (Sous-missions)
# Sortie et retour du flux principal

protocole:
  nom: "protocole-boucles-dynamiques"
  version: "001.01"
  statut: "ebauche"
  cree: "2026-08-05"
  auteur: "Buffy"
  immutable: true
---

# Boucles Dynamiques -- Sous-missions

> **REGLE ABSOLUE** : Les boucles permettent de SORTIR du flux principal

---

## Objectif

Resoudre le probleme des outils manquants en permettant a l'agent de :
1. **Detecter** qu'un outil est necessaire mais inexistant
2. **Sortir** du flux principal
3. **Creer/reprendre** l'outil manquant
4. **Revenir** au flux principal avec l'outil disponible

---

## Le concept

### Avant (boucles statiques)

```
Mission principale
    |
Etape 1 : Verifier le systeme
    |
PROBLEME : verifier-systeme n'existe pas
    |
Vulcain continue quand meme (ERREUR !)
```

### Apres (boucles dynamiques)

```
Mission principale
    |
Etape 1 : Verifier le systeme
    |
DETECTE : verifier-systeme n'existe pas
    |
[SOUS-MISSION] Creer verifier-systeme
    |
    1. Lire les specs de l'outil
    2. Developper l'outil
    3. Tester l'outil
    4. Valider l'outil
    |
[RETOUR] Mission principale reprend
    |
Etape 1 : Verifier le systeme (MAIS MAINTENANT L'OUTIL EXISTE !)
    |
Continuer normalement
```

---

## Structure d'une boucle dynamique

### 1. Detection

**QUAND** : A chaque etape de la carte de decision

**COMMENT** :
```
1. Identifier l'outil necessaire pour cette etape
2. Verifier si l'outil existe
3. Si non -> SOUS-MISSION obligatoire
4. Si oui -> Continuer
```

### 2. Sortie du flux

**ACTION** :
```
1. Sauvegarder la position dans la mission principale
   - Etape en cours
   - Donnees collectees
   - Objectif final
2. Marquer la sous-mission comme "en cours"
3. Commencer la sous-mission
```

### 3. Execution de la sous-mission

**MISSION** : Creer/reprendre l'outil manquant

**Etapes** :
```
1. Lire la specification de l'outil
2. Verifier le systeme (si necessaire)
3. Developper l'outil
4. Tester l'outil
5. Valider l'outil
6. Documenter l'outil
```

### 4. Retour au flux principal

**ACTION** :
```
1. Confirmer que l'outil est disponible
2. Reprendre a l'etape sauvegardee
3. Continuer la mission principale
```

---

## Regles d'or

| Regle | Description |
|---|---|
| **R1** | Toujours sauvegarder avant de sortir |
| **R2** | Toujours revenir apres une sous-mission |
| **R3** | Ne jamais abandonner la mission principale |
| **R4** | Documenter chaque sortie/retree |

---

## Format de documentation

### Sortie

```markdown
## SOUS-MISSION DETECTEE

| Champ | Valeur |
|---|---|
| **Mission principale** | [description] |
| **Etape en cours** | [etape] |
| **Outil necessaire** | [nom-outil] |
| **Raison** | [pourquoi cet outil est necessaire] |

### Position sauvegardee
- Etape : [numero]
- Donnees : [ce qui a ete collecte]
- Objectif : [ce qu'on essayait de faire]
```

### Retour

```markdown
## RETOUR AU FLUX PRINCIPAL

| Champ | Valeur |
|---|---|
| **Sous-mission** | [description] |
| **Resultat** | [succes/echec] |
| **Outil cree** | [oui/non] |
| **Duree** | [temps] |

### Reprise
- On reprend a l'etape : [numero]
- L'outil est maintenant disponible : [oui/non]
```

---

## Outils necessaires

| Outil | Usage | Statut |
|---|---|---|
| `gerer-sous-mission` | Gerer les sorties/retrees du flux principal | Cree |
| `verifier-systeme` | Verifier le systeme utilisateur | Cree |
| `valider-cartes-decision` | Valider les cartes de decision des agents | Cree |

---

## Frequence

- **A chaque etape** : Verifier si un outil est necessaire
- **Si outil manquant** : Sous-mission obligatoire
- **Apres chaque sous-mission** : Toujours revenir
