# Boucle de Rétro-action — Validation d'Outil

**Agent** : Vulcain
**Date création** : 2026-08-05
**Date mise à jour** : 2026-08-05
**Statut** : Active
**Version** : 2.0 (avec sous-missions)

---

## Objectif

S'assurer que Vulcain teste TOUJOURS un outil avec ses propres outils AVANT de le valider.
**NOUVEAU** : Si les outils de test n'existent pas, CRÉEZ-LES avant de continuer.

---

## Le problème résolu

**Avant** : Vulcain utilisait des outils génériques pour tester
**Après** : Vulcain utilise ses propres outils, et les crée si nécessaire

---

## La boucle dynamique

### QUAND s'applique la boucle ?

```
APRÈS avoir créé un outil (étape 4 de la carte de décision)
AVANT de le valider (étape 6)
```

### COMMENT exécuter la boucle ?

```
1. Lire la carte de décision
2. Vérifier si l'étape 5 (Tester l'outil) est faite
3. Si non -> EXÉCUTER : valider-cartes-decision
4. Si l'outil n'existe pas -> SOUS-MISSION obligatoire
5. Si oui -> Continuer
6. Documenter le résultat
```

---

## SOUS-MISSION : Créer valider-cartes-decision

### Détection

```
CONDITION : valider-cartes-decision n'existe pas
ACTION : Sortir du flux principal
```

### Étapes de la sous-mission

| Étape | Action | Sortie |
|---|---|---|
| **1** | **SAUVEGARDER** la position | Position sauvegardée |
| **2** | **LIRE** les specs de valider-cartes-decision | Specs lues |
| **3** | **DÉVELOPPER** valider-cartes-decision | Outil créé |
| **4** | **TESTER** valider-cartes-decision | Tests passés |
| **5** | **VALIDER** valider-cartes-decision | Outil validé |
| **6** | **REVENIR** au flux principal | Flux repris |

### Détail des étapes

#### Étape 1 : Sauvegarder

```bash
gerer-sous-mission sauvegarder \
  --mission "Créer valider-cartes-decision" \
  --etape "1" \
  --donnees "Vulcain en train de créer un outil de test"
```

#### Étape 2 : Lire les specs

```
Fichier : cerveau-projet/agents/tools/valider/valider-cartes-decision/spec/spec-valider-cartes-decision.001.01.ebauche.md
Action : Lire et comprendre les spécifications
```

#### Étape 3 : Développer l'outil

```
Fichier à créer : cerveau-projet/agents/tools/valider/valider-cartes-decision/valider-cartes-decision.sh
Contenu : Script qui valide les cartes de décision
```

#### Étape 4 : Tester l'outil

```bash
chmod +x cerveau-projet/agents/tools/valider/valider-cartes-decision/valider-cartes-decision.sh
cerveau-projet/agents/tools/valider/valider-cartes-decision/valider-cartes-decision.sh --aide
```

#### Étape 5 : Valider l'outil

```
Vérifier que l'outil :
- Fonctionne correctement
- Valide les cartes de décision
- Est documenté
```

#### Étape 6 : Revenir au flux principal

```bash
gerer-sous-mission revenir \
  --resultat "succès" \
  --outil-créé "oui"
```

---

## Après la sous-mission

```
1. valider-cartes-decision existe maintenant
2. Exécuter valider-cartes-decision sur l'outil créé
3. Vérifier que l'outil respecte la carte de décision
4. Continuer à l'étape 6 de la carte de décision
```

---

## Règle d'or

> **TOUJOURS tester un outil avec ses propres outils AVANT de le valider.**

---

## Fréquence

- **Création d'outil** : Toujours
- **Modification d'outil** : Toujours
- **Après une erreur** : Toujours
- **Si outil manquant** : Sous-mission obligatoire

---

