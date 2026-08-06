# Boucle de Retro-action -- Verification Systeme

**Agent** : Vulcain
**Date creation** : 2026-08-05
**Date mise a jour** : 2026-08-05
**Statut** : Active
**Version** : 2.0 (avec sous-missions)

---

## Objectif

S'assurer que Vulcain verifie TOUJOURS le systeme AVANT de choisir une technologie.
**NOUVEAU** : Si verifier-systeme n'existe pas, CREEZ-LE avant de continuer.

---

## Le probleme resolu

**Avant** : Vulcain supposait que Bash etait disponible
**Apres** : Vulcain verifie TOUJOURS, et cree l'outil si necessaire

---

## La boucle dynamique

### QUAND s'applique la boucle ?

```
AVANT de choisir une technologie (etape 3 de la carte de decision)
APRES avoir lu l'outil.md (etape 2)
```

### COMMENT executer la boucle ?

```
1. Lire la carte de decision
2. Verifier si l'etape 1 (VERIFIER LE SYSTEME) est faite
3. Si non -> EXECUTER : verifier-systeme
4. Si l'outil n'existe pas -> SOUS-MISSION obligatoire
5. Si oui -> Continuer
6. Documenter le resultat
```

---

## SOUS-MISSION : Creer verifier-systeme

### Detection

```
CONDITION : verifier-systeme n'existe pas
ACTION : Sortir du flux principal
```

### Etapes de la sous-mission

| Etape | Action | Sortie |
|---|---|---|
| **1** | **SAUVEGARDER** la position | Position sauvegardee |
| **2** | **LIRE** les specs de verifier-systeme | Specs lues |
| **3** | **VERIFIER** le systeme avec les outils de base | Systeme connu |
| **4** | **DEVELOPPER** verifier-systeme | Outil cree |
| **5** | **TESTER** verifier-systeme | Tests passes |
| **6** | **VALIDER** verifier-systeme | Outil valide |
| **7** | **REVENIR** au flux principal | Flux repris |

### Detail des etapes

#### Etape 1 : Sauvegarder

```bash
gerer-sous-mission sauvegarder \
  --mission "Creer verifier-systeme" \
  --etape "1" \
  --donnees "Vulcain en train de creer un outil"
```

#### Etape 2 : Lire les specs

```
Fichier : cerveau-projet/agents/tools/verifier/verifier-systeme/spec/spec-verifier-systeme.001.01.ebauche.md
Action : Lire et comprendre les specifications
```

#### Etape 3 : Verifier le systeme (avec outils de base)

```
Commande : uname -a
Objectif : Connaitre l'OS, l'architecture, le shell disponible
Resultat : Systeme identifie
```

#### Etape 4 : Developper l'outil

```
Fichier a creer : cerveau-projet/agents/tools/verifier/verifier-systeme/verifier-systeme.sh
Contenu : Script qui verifie le systeme automatiquement
```

#### Etape 5 : Tester l'outil

```bash
chmod +x cerveau-projet/agents/tools/verifier/verifier-systeme/verifier-systeme.sh
cerveau-projet/agents/tools/verifier/verifier-systeme/verifier-systeme.sh
```

#### Etape 6 : Valider l'outil

```
Verifier que l'outil :
- Fonctionne correctement
- Retourne les bonnes informations
- Est documente
```

#### Etape 7 : Revenir au flux principal

```bash
gerer-sous-mission revenir \
  --resultat "succes" \
  --outil-cree "oui"
```

---

## Apres la sous-mission

```
1. verifier-systeme existe maintenant
2. Executer verifier-systeme
3. Noter : OS, shells, langages disponibles
4. Continuer a l'etape 3 de la carte de decision
```

---

## Regle d'or

> **TOUJOURS executer verifier-systeme AVANT de choisir une technologie.**

---

## Frequence

- **Debut de mission** : Toujours
- **Choix technologique** : Toujours
- **Apres une erreur** : Toujours
- **Si outil manquant** : Sous-mission obligatoire

---

