# Boucle de Rétro-action — Vérification Système

**Agent** : Vulcain
**Date création** : 2026-08-05
**Date mise à jour** : 2026-08-05
**Statut** : Active
**Version** : 2.0 (avec sous-missions)

---

## Objectif

S'assurer que Vulcain vérifie TOUJOURS le système AVANT de choisir une technologie.
**NOUVEAU** : Si verifier-systeme n'existe pas, CREEZ-LE avant de continuer.

---

## Le problème résolu

**Avant** : Vulcain supposait que Bash était disponible
**Après** : Vulcain vérifie TOUJOURS, et crée l'outil si nécessaire

---

## La boucle dynamique

### QUAND s'applique la boucle ?

```
AVANT de choisir une technologie (étape 3 de la carte de décision)
APRÈS avoir lu l'outil.md (étape 2)
```

### COMMENT exécuter la boucle ?

```
1. Lire la carte de décision
2. Vérifier si l'étape 1 (VÉRIFIER LE SYSTÈME) est faite
3. Si non → EXÉCUTER : verifier-systeme
4. Si l'outil n'existe pas → SOUS-MISSION obligatoire
5. Si oui → Continuer
6. Documenter le résultat
```

---

## SOUS-MISSION : Créer verifier-systeme

### Détection

```
CONDITION : verifier-systeme n'existe pas
ACTION : Sortir du flux principal
```

### Étapes de la sous-mission

| Étape | Action | Sortie |
|---|---|---|
| **1** | **SAUVEGARDER** la position | Position sauvegardée |
| **2** | **LIRE** les specs de verifier-systeme | Specs lues |
| **3** | **VÉRIFIER** le système avec les outils de base | Système connu |
| **4** | **DÉVELOPPER** verifier-systeme | Outil créé |
| **5** | **TESTER** verifier-systeme | Tests passés |
| **6** | **VALIDER** verifier-systeme | Outil validé |
| **7** | **REVENIR** au flux principal | Flux repris |

### Détail des étapes

#### Étape 1 : Sauvegarder

```bash
gerer-sous-mission sauvegarder \
  --mission "Créer verifier-systeme" \
  --etape "1" \
  --donnees "Vulcain en train de créer un outil"
```

#### Étape 2 : Lire les specs

```
Fichier : cerveau-projet/agents/tools/analyser/verifier-systeme/spec/spec-verifier-systeme.001.01.ebauche.md
Action : Lire et comprendre les spécifications
```

#### Étape 3 : Vérifier le système (avec outils de base)

```
Commande : uname -a
Objectif : Connaître l'OS, l'architecture, le shell disponible
Résultat : Système identifié
```

#### Étape 4 : Développer l'outil

```
Fichier à créer : cerveau-projet/agents/tools/analyser/verifier-systeme/verifier-systeme.sh
Contenu : Script qui vérifie le système automatiquement
```

#### Étape 5 : Tester l'outil

```bash
chmod +x cerveau-projet/agents/tools/analyser/verifier-systeme/verifier-systeme.sh
cerveau-projet/agents/tools/analyser/verifier-systeme/verifier-systeme.sh
```

#### Étape 6 : Valider l'outil

```
Vérifier que l'outil :
- Fonctionne correctement
- Retourne les bonnes informations
- Est documenté
```

#### Étape 7 : Revenir au flux principal

```bash
gerer-sous-mission revenir \
  --resultat "succès" \
  --outil-créé "oui"
```

---

## Après la sous-mission

```
1. verifier-systeme existe maintenant
2. Exécuter verifier-systeme
3. Noter : OS, shells, langages disponibles
4. Continuer à l'étape 3 de la carte de décision
```

---

## Règle d'or

> **TOUJOURS exécuter verifier-systeme AVANT de choisir une technologie.**

---

## Fréquence

- **Début de mission** : Toujours
- **Choix technologique** : Toujours
- **Après une erreur** : Toujours
- **Si outil manquant** : Sous-mission obligatoire

---

