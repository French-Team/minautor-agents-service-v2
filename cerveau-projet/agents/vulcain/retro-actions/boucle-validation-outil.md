# Boucle de Retro-action -- Validation d'Outil

**Agent** : Vulcain
**Date creation** : 2026-08-05
**Date mise a jour** : 2026-08-05
**Statut** : Active
**Version** : 2.0 (avec sous-missions)

---

## Objectif

S'assurer que Vulcain teste TOUJOURS un outil avec ses propres outils AVANT de le valider.
**NOUVEAU** : Si les outils de test n'existent pas, CREEZ-LES avant de continuer.

---

## Le probleme resolu

**Avant** : Vulcain utilisait des outils generiques pour tester
**Apres** : Vulcain utilise ses propres outils, et les cree si necessaire

---

## La boucle dynamique

### QUAND s'applique la boucle ?

```
APRES avoir cree un outil (etape 4 de la carte de decision)
AVANT de le valider (etape 6)
```

### COMMENT executer la boucle ?

```
1. Lire la carte de decision
2. Verifier si l'etape 5 (Tester l'outil) est faite
3. Si non -> EXECUTER : valider-cartes-decision
4. Si l'outil n'existe pas -> SOUS-MISSION obligatoire
5. Si oui -> Continuer
6. Documenter le resultat
```

---

## SOUS-MISSION : Creer valider-cartes-decision

### Detection

```
CONDITION : valider-cartes-decision n'existe pas
ACTION : Sortir du flux principal
```

### Etapes de la sous-mission

| Etape | Action | Sortie |
|---|---|---|
| **1** | **SAUVEGARDER** la position | Position sauvegardee |
| **2** | **LIRE** les specs de valider-cartes-decision | Specs lues |
| **3** | **DEVELOPPER** valider-cartes-decision | Outil cree |
| **4** | **TESTER** valider-cartes-decision | Tests passes |
| **5** | **VALIDER** valider-cartes-decision | Outil valide |
| **6** | **REVENIR** au flux principal | Flux repris |

### Detail des etapes

#### Etape 1 : Sauvegarder

```bash
gerer-sous-mission sauvegarder \
  --mission "Creer valider-cartes-decision" \
  --etape "1" \
  --donnees "Vulcain en train de creer un outil de test"
```

#### Etape 2 : Lire les specs

```
Fichier : cerveau-projet/agents/tools/valider/valider-cartes-decision/spec/spec-valider-cartes-decision.001.01.ebauche.md
Action : Lire et comprendre les specifications
```

#### Etape 3 : Developper l'outil

```
Fichier a creer : cerveau-projet/agents/tools/valider/valider-cartes-decision/valider-cartes-decision.sh
Contenu : Script qui valide les cartes de decision
```

#### Etape 4 : Tester l'outil

```bash
chmod +x cerveau-projet/agents/tools/valider/valider-cartes-decision/valider-cartes-decision.sh
cerveau-projet/agents/tools/valider/valider-cartes-decision/valider-cartes-decision.sh --aide
```

#### Etape 5 : Valider l'outil

```
Verifier que l'outil :
- Fonctionne correctement
- Valide les cartes de decision
- Est documente
```

#### Etape 6 : Revenir au flux principal

```bash
gerer-sous-mission revenir \
  --resultat "succes" \
  --outil-cree "oui"
```

---

## Apres la sous-mission

```
1. valider-cartes-decision existe maintenant
2. Executer valider-cartes-decision sur l'outil cree
3. Verifier que l'outil respecte la carte de decision
4. Continuer a l'etape 6 de la carte de decision
```

---

## Regle d'or

> **TOUJOURS tester un outil avec ses propres outils AVANT de le valider.**

---

## Frequence

- **Creation d'outil** : Toujours
- **Modification d'outil** : Toujours
- **Apres une erreur** : Toujours
- **Si outil manquant** : Sous-mission obligatoire

---

