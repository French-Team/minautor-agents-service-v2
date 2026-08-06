# Boucle de Rétro-action — Cohérence

**Agent** : Vulcain
**Date création** : 2026-08-05
**Date mise à jour** : 2026-08-05
**Statut** : Active
**Version** : 2.0 (avec sous-missions)

---

## Objectif

S'assurer que Vulcain suit TOUJOURS sa carte de décision.
**NOUVEAU** : Si un outil est nécessaire mais inexistant, CRÉEZ-LE avant de continuer.

---

## Le problème résolu

**Avant** : Vulcain sautait des étapes et supposait
**Après** : Vulcain vérifie chaque étape et crée les outils manquants

---

## La boucle dynamique

### QUAND s'applique la boucle ?

```
À CHAQUE étape de la carte de décision
AVANT de passer à l'étape suivante
```

### COMMENT exécuter la boucle ?

```
1. Lire la carte de décision
2. Identifier l'étape en cours
3. Vérifier que l'étape précédente est terminée
4. Si non → Terminer l'étape précédente
5. Vérifier si un outil est nécessaire pour cette étape
6. Si outil manquant → SOUS-MISSION obligatoire
7. Si oui → Continuer
8. Documenter le résultat
```

---

## SOUS-MISSION : Créer un outil manquant

### Détection

```
CONDITION : Un outil est nécessaire pour l'étape en cours mais n'existe pas
ACTION : Sortir du flux principal
```

### Étapes de la sous-mission

| Étape | Action | Sortie |
|---|---|---|
| **1** | **SAUVEGARDER** la position | Position sauvegardée |
| **2** | **IDENTIFIER** l'outil nécessaire | Outil identifié |
| **3** | **VÉRIFIER** si des specs existent | Specs trouvées ou non |
| **4** | **CRÉER** les specs si nécessaire | Specs créées |
| **5** | **DÉVELOPPER** l'outil | Outil créé |
| **6** | **TESTER** l'outil | Tests passés |
| **7** | **REVENIR** au flux principal | Flux repris |

### Détail des étapes

#### Étape 1 : Sauvegarder

```bash
gerer-sous-mission sauvegarder \
  --mission "[mission en cours]" \
  --etape "[numéro]" \
  --donnees "[ce qui a été collecté]"
```

#### Étape 2 : Identifier l'outil

```
Question : Quel outil est nécessaire pour cette étape ?
Réponse : [nom-outil]
```

#### Étape 3 : Vérifier les specs

```
Fichier : cerveau-projet/agents/tools/[categorie]/[outil]/spec/spec-[outil].001.01.ebauche.md
Condition : Le fichier existe-t-il ?
```

#### Étape 4 : Créer les specs (si nécessaire)

```
Si les specs n'existent pas → Les créer
Format : Suivre le template spec-template.md
```

#### Étape 5 : Développer l'outil

```
Fichier : cerveau-projet/agents/tools/[categorie]/[outil]/[outil].sh
Contenu : Script qui répond aux spécifications
```

#### Étape 6 : Tester l'outil

```bash
chmod +x cerveau-projet/agents/tools/[categorie]/[outil]/[outil].sh
cerveau-projet/agents/tools/[categorie]/[outil]/[outil].sh --aide
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
1. L'outil existe maintenant
2. Utiliser l'outil pour l'étape en cours
3. Continuer à l'étape suivante de la carte de décision
```

---

## Règle d'or

> **TOUJOURS suivre la carte de décision dans l'ordre.**

---

## Fréquence

- **À chaque étape** : Toujours
- **Après une interruption** : Toujours
- **Après une erreur** : Toujours
- **Si outil manquant** : Sous-mission obligatoire

---

