---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
# Protocole -- Carte de Decision pour les Agents

**Version** : 0.2.0
**Statut** : prepare
**Date creation** : 2026-08-05
**Agent** : Buffy (creation + evolution parcours 2026-08-07)

---

## EVOLUTION 2026-08-07 -- LA CARTE DEVIENT UN PARCOURS (jeu de piste)

> **Ce protocole est IMMUABLE mais il a EVOLUE** : la carte de decision statique
> (tableaux `Etape | Action | Protocole | Outil`) est **SUPERSEDEE par le PARCOURS**
> (jeu de piste). L'agent ne lit plus la carte d'avance : il suit son parcours
> **case par case** avec l'outil `guider-parcours`, qui lui donne a chaque etape
> l'indice exact (outil, fichier, regle) et les branches selon ses reponses.

### Le principe du parcours

```
demarrer.md (CASE 0 : point d'entree de tous les parcours)
    |
    v
parcours-<agent>.json  (source de verite du guidage, dans agents/<agent>/parcours/)
    |
    v
guider-parcours.py <parcours.json>  (l'outil fait avancer case par case)
    |
    v
CASE N : question + indices (outil / fichier / regle / controle)
    |  reponse
    v
CASE N+1 : ... jusqu'a la case FIN
```

### Les 5 modeles de cases

| Type de case | Ce qu'elle fait | Quand |
|---|---|---|
| **Question** | Pose UNE question, l'agent repond, branches OUI/NON/choix | Une simple decision suffit |
| **Indice-outil** | Affiche l'outil exact a lancer (nom + chemin + commande) | Une action outil necessaire |
| **Indice-fichier** | Affiche LE fichier/protocole a lire a cette etape (un seul) | Besoin de lire une reference |
| **Regle** | Rappelle LA regle absolue pertinente pour cette case | Point sensible identifie |
| **Controle** | Verification obligatoire avant de continuer (OUI/NON) | Garde-fou de fin d'etape |

Une case peut **combiner** plusieurs modeles quand le moment l'exige, ou n'etre
qu'une simple question quand ca suffit. Chaque reponse mene a une **branche**
vers la case suivante.

### Le modele compose (Pattern 7, v0.2.13)

> Philosophie : "alleger ne veut pas dire supprimer : decomposer pour
> faciliter" (agents/philosophie/). Une case n'est plus un cul-de-sac a
> reponse unique : c'est le debut d'un MODELE COMPOSE.

1. Toute case de **decision** (`question` ou `controle`) porte AU MINIMUM
   **2 branches** (sauf action directe : une case `indice` a `suivant` est
   une ACTION, pas une decision). Deux branches = deux solutions
   alternatives, ou une decision + une deviation.
2. Une **DEVIATION** est une branche vers un WORKFLOW SECONDAIRE (un groupe
   de cases qui traite un sous-probleme). La derniere case du workflow
   secondaire a un `suivant` qui **REJOINT** le workflow principal (case de
   rejoint) -- jamais une fin au milieu, jamais une boucle d'attente
   (regle 10 de la spec-guider-parcours).
3. Exemple reel : la boucle Cerberus/Buffy -- si Buffy trouve des erreurs
   HORS MISSION pendant sa mission, elle le signale a Cerberus ; la carte de
   Cerberus porte une decision "erreur hors mission signalee" : OUI
   (reparation immediate -> deviation : reactiver Buffy, elle repare, revient
   au flux) / NON (differer -> le flux principal continue).

Details, schema JSON et procedure d'audit : spec-guider-parcours v0.2.13
(Pattern 7 + procedure 4e).

### Format du parcours (JSON)

```json
{
  "parcours": { "nom": "parcours-<agent>", "agent": "<agent>", "version": "0.1.0", "case_depart": "c1" },
  "cases": {
    "c1": { "titre": "Mission", "type": "question", "question": "...", "branches": [ { "reponse": "X", "vers": "c2" } ] },
    "c2": { "titre": "...", "type": "indice", "indices": [ { "type": "outil", "nom": "...", "chemin": "..." } ], "suivant": "c3" },
    "cN": { "titre": "FIN", "type": "fin" }
  }
}
```

### Spec et outil de reference

| Element | Chemin |
|---|---|
| Outil `guider-parcours` | `agents/tools/guider/guider-parcours/guider-parcours.py` (+ .sh parite) |
| Spec du format | `agents/tools/guider/guider-parcours/spec/spec-guider-parcours.001.01.ebauche.md` |
| Parcours existants | `agents/vulcain/parcours/`, `agents/morpheus/parcours/`, `agents/clio/parcours/` |

### Regles du parcours (v0.2.0)

1. Chaque agent a SON parcours dans `agents/<agent>/parcours/parcours-<agent>.json`
2. `demarrer.md` est la **CASE 0** commune : apres l'identification, l'agent lance SON parcours
3. La fiche de l'agent est **allegee** : identite, regles absolues, connexions -- le guidage vit dans le JSON
4. Le parcours est la **source de verite** du guidage (remplace les tableaux de missions de la fiche)
5. Une mission hors parcours : branche vers l'activation de l'agent habilite ou signalement du besoin
6. Les lecons des corrections peuvent devenir des **cases** du parcours (ex: parcours-clio case c7)
7. **CASE DE NETTOYAGE OBLIGATOIRE (IMMUABLE, lecon 2026-08-16) :** toute carte
   qui contient une case CREANT des fichiers/dossiers temporaires (`tmp-<agent>/`,
   preuves, scripts) DOIT avoir une case de NETTOYAGE avant la fin (suppression
   du dossier 0 residu + declaration registre `enregistrer-usage-outil
   --mode script-temporaire`). Une carte sans nettoyage alors qu'elle cree des
   fichiers temp est INCOMPLETE (anti-recurrence : carte argus v0.1.1 sans case
   de nettoyage, bloquee par test-024).

> Le contenu ci-dessous (sections historiques) documente la carte de decision
> statique qui a precede le parcours. Il est conserve comme reference historique
> et pour la comprehension du format. Le PARCOURS ci-dessus est la methode actuelle.

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

## EVOLUTION FINALE (v0.2.0 -- 2026-08-07)

> La methode actuelle est le **PARCOURS (jeu de piste)** decrit en tete de ce
> protocole : la carte statique (tableaux) est la version historique. Pour toute
> nouvelle mission ou evolution d'agent :
> 1. Creer/faire evoluer le parcours JSON (`agents/<agent>/parcours/parcours-<agent>.json`)
> 2. Alleger la fiche (parcours = source de verite du guidage)
> 3. Tester la navigation avec `guider-parcours --liste` et `--reponses`

---

> **Ce protocole est IMMUABLE.** Le parcours (jeu de piste) est l'evolution
> officielle de la carte de decision (v0.2.0, 2026-08-07).
