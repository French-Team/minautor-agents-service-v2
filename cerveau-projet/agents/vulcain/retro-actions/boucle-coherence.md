# Boucle de Retro-action -- Coherence

**Agent** : Vulcain
**Date creation** : 2026-08-05
**Date mise a jour** : 2026-08-05
**Statut** : Active
**Version** : 2.0 (avec sous-missions)

---

## Objectif

S'assurer que Vulcain suit TOUJOURS sa carte de decision.
**NOUVEAU** : Si un outil est necessaire mais inexistant, CREEZ-LE avant de continuer.

---

## Le probleme resolu

**Avant** : Vulcain sautait des etapes et supposait
**Apres** : Vulcain verifie chaque etape et cree les outils manquants

---

## La boucle dynamique

### QUAND s'applique la boucle ?

```
A CHAQUE etape de la carte de decision
AVANT de passer a l'etape suivante
```

### COMMENT executer la boucle ?

```
1. Lire la carte de decision
2. Identifier l'etape en cours
3. Verifier que l'etape precedente est terminee
4. Si non -> Terminer l'etape precedente
5. Verifier si un outil est necessaire pour cette etape
6. Si outil manquant -> SOUS-MISSION obligatoire
7. Si oui -> Continuer
8. Documenter le resultat
```

---

## SOUS-MISSION : Creer un outil manquant

### Detection

```
CONDITION : Un outil est necessaire pour l'etape en cours mais n'existe pas
ACTION : Sortir du flux principal
```

### Etapes de la sous-mission

| Etape | Action | Sortie |
|---|---|---|
| **1** | **SAUVEGARDER** la position | Position sauvegardee |
| **2** | **IDENTIFIER** l'outil necessaire | Outil identifie |
| **3** | **VERIFIER** si des specs existent | Specs trouvees ou non |
| **4** | **CREER** les specs si necessaire | Specs creees |
| **5** | **DEVELOPPER** l'outil | Outil cree |
| **6** | **TESTER** l'outil | Tests passes |
| **7** | **REVENIR** au flux principal | Flux repris |

### Detail des etapes

#### Etape 1 : Sauvegarder

```bash
gerer-sous-mission sauvegarder \
  --mission "[mission en cours]" \
  --etape "[numero]" \
  --donnees "[ce qui a ete collecte]"
```

#### Etape 2 : Identifier l'outil

```
Question : Quel outil est necessaire pour cette etape ?
Reponse : [nom-outil]
```

#### Etape 3 : Verifier les specs

```
Fichier : cerveau-projet/agents/tools/[categorie]/[outil]/spec/spec-[outil].001.01.ebauche.md
Condition : Le fichier existe-t-il ?
```

#### Etape 4 : Creer les specs (si necessaire)

```
Si les specs n'existent pas -> Les creer
Format : Suivre le template spec-template.md
```

#### Etape 5 : Developper l'outil

```
Fichier : cerveau-projet/agents/tools/[categorie]/[outil]/[outil].sh
Contenu : Script qui repond aux specifications
```

#### Etape 6 : Tester l'outil

```bash
chmod +x cerveau-projet/agents/tools/[categorie]/[outil]/[outil].sh
cerveau-projet/agents/tools/[categorie]/[outil]/[outil].sh --aide
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
1. L'outil existe maintenant
2. Utiliser l'outil pour l'etape en cours
3. Continuer a l'etape suivante de la carte de decision
```

---

## Regle d'or

> **TOUJOURS suivre la carte de decision dans l'ordre.**

---

## Frequence

- **A chaque etape** : Toujours
- **Apres une interruption** : Toujours
- **Apres une erreur** : Toujours
- **Si outil manquant** : Sous-mission obligatoire

---

