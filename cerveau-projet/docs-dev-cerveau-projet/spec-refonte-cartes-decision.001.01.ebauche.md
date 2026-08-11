---
identite:
  type: spec
  appartient_a: commun
  commun: true
---
# Spec -- Refonte du concept des cartes de decision et des cases

**Version** : 0.1.3
**Statut** : ebauche
**Date creation** : 2026-08-09
**Agent** : Promethee (spec)
**Historique** : v0.1.0 (creation, 2026-08-09) ; v0.1.1 (clarification : type action declare NOUVEAU du modele cible, suite audit Themis 2026-08-09) ; v0.1.2 (alignement convention de nommage ETENDUE cT*, decouverte detecter-convention-nommage 2026-08-11) ; v0.1.3 (documentation du BUDGET PONDERE des indices : court <= 100 car. = 0,5 unite, long > 100 car. = 1 unite, budget 3,0 unites par case, plafond absolu 160 car. inchange, suite implementation valider-case v1.1.0 / generateurs-case v0.4.2, 2026-08-11)

---

## 1. Objectif

Refonder le concept des **cartes de decision** (parcours JSON) et des **cases**
pour stopper la degradation constatee a mesure que l'on ajoute des pistes, et
garantir que les cartes soient **EXECUTEES** (case fournie a la demande) au
lieu d'etre seulement **documentees** (lues en bloc par l'agent).

Le principe directeur : **l'agent recit UNE case, l'execute, valide -- c'est
le SYSTEME qui fournit la case suivante**, dans le meme principe que le
catalogue de commande. On constitue des **fichiers catalogues de cases**, et on
cree l'outil **validateur-case** qui allege completement les cartes de
decision, les rendant largement plus lisibles et suivies.

## 2. Contexte

### 2.1 Origine

Constat utilisateur (2026-08-09), confirme par le diagnostic Cerberus :

1. **Conformite d'execution manquee** : quand Vulcain a cree
   `generateurs-amelioration`, la chaine Morpheus (tests) puis Janus (second
   controle) n'a PAS ete declenchee. La chaine a du etre rejouee a rebours en
   reparation. Les cartes de Vulcain (c8/c14), Morpheus (c9/c10) et Cerberus
   (c13/c14/c15) ETAIENT cablees -- mais l'execution reelle ne les a pas
   suivies. Le LLM recoit une mission et court-circuite sa carte.

2. **Degradation conceptuelle** : les parcours grossissent (buffy 49 cases /
   45 Ko, atlas 40, vulcain 32, cerberus 28) ; chaque ajout de piste ajoute des
   cases et des indices empiles (jusqu'a 5-6 indices par case) ; la
   spec-guider-parcours compte 15 patterns (v0.2.23). Le concept porte trop de
   choses par case, et les chaines inter-agents vivent dans les MESSAGES de
   fins (invisibles) au lieu d'etre des ETAPES visibles.

### 2.2 Vision utilisateur (verbatim)

> "quand l'agent se place sur une case, il recoit le contenu de la case,
> execute le contenu, valide la fin de son travail qui l'informe de la case
> suivante. au lieu de l'obliger a lire la carte pour trouver la case suivante,
> a chaque fois qu'il valide une case, c'est NOUS qui fournissons la case,
> dans le meme principe que le catalogue de commande. on constitue des
> fichiers qui contiennent les catalogues, on cree le validateur-case qui va
> completement alleger la carte de decision qui sera largement plus lisible et
> suivie."

### 2.3 Perimetre

COUVERT par cette spec :
- Le modele cible de **case composee** (decision + branches min 2 + deviation + rejoint)
- Le principe **case fournie a la demande** (execution obligatoire via guider-parcours)
- Le format des **catalogues de cases alleges** (references au lieu de contenus)
- Le contrat de l'outil **validateur-case** (a creer)
- L'evolution des **generateurs-case** et **generateurs-carte**
- Le plan d'implementation par etapes (spec d'abord : valider le concept AVANT de coder)

HORS perimetre (a traiter en missions ulterieures) :
- La migration effective des 11 parcours existants vers le nouveau format
- La modification de la spec-guider-parcours (les patterns seront references,
  pas reecrits dans cette spec)

## 3. Probleme

| Probleme | Impact |
|---|---|
| Cartes cablees mais NON EXECUTEES | La chaine Morpheus/Janus est sautee, les livrables partent non testes |
| Indices empiles (5-6 par case) | Cartes illisibles, l'agent se noie dans la documentation |
| 15 patterns disperses | La connaissance est trop eparpillee, chaque case repete les regles |
| Chainage inter-agents dans les messages de fins | Invisible, non execute |
| Fichiers JSON massifs (45 Ko) | Lourds a editer, diff difficiles |

## 4. Modele cible : la CASE COMPOSEE

Une case du nouveau modele est un OBJET COMPOSE, fourni a la demande :

```
case <id>  (un type : question | controle | indice | action | fin)
    contenu : titre + question/message + indices ALLEGES (references)
    choix   : branches (min 2 pour les decisions, sauf action directe)
    sortie  : suivant | branches
```

### 4.1 Types de cases (existants + 1 NOUVEAU)

| Type | Role | Sortie |
|---|---|---|
| `question` | Decision (l'agent choisit une branche) | `branches` (min 2) |
| `controle` | Verification (OUI/NON) | `branches` (min 2) |
| `indice` | Action directe guidee (outil/regle/fichier) | `suivant` |
| `action` | Action simple sans question | `suivant` | *(NOUVEAU - modele cible, a implementer a l etape 5 dans guider-parcours)* |
| `fin` | Terminaison (message de cloture) | aucune |

### 4.2 Indices ALLEGES (references, pas contenus)

Un indice ne porte PLUS le texte complet des regles : il porte une REFERENCE.

```json
{ "type": "regle", "ref": "pattern-12" }        // au lieu du texte inline
{ "type": "outil", "nom": "activer-agent-principal", "catalogue": "..." }
{ "type": "fichier", "chemin": "...", "raison": "courte" }
```

Les references (`pattern-12`, `regle-immaculee-ascii`, `protocole-tests`) sont
resolues par guider-parcours/validateur-case vers les fichiers sources
(protocoles, patterns de la spec-guider-parcours). **UNE PLACE POUR CHAQUE
CHOSE & CHAQUE CHOSE A SA PLACE** : la regle vit dans le protocole, la case la
reference.

### 4.3 Modele compose (Pattern 7 generalise)

Toute decision du nouveau modele est generee en B LOC COMPLET :

```
case 1 (decision)  >>> branche A -> case 2   (traitement A)
                   >>> branche B -> case 3   (traitement B)
                   >>> branche D -> case 4   (DEVIATION, workflow secondaire)
case 4 (deviation) >>> ... -> case 5 (REJOINT -> retour au flux principal)
```

Le generateur cree le bloc entier (decision + branches + deviation + rejoint)
en UNE commande, avec garde-fous : branches min 2, rejoint obligatoire pour
toute deviation, pas de boucle directe sur soi-meme.

## 5. Principe : case fournie a la demande (EXECUTION OBLIGATOIRE)

Le principe catalogue applique aux cartes :

1. Quand un agent est ACTIVE (par Cerberus ou un autre agent), sa mission
   inclut l'ordre : **suivre SA carte via guider-parcours, case par case**.
2. L'agent ne lit JAMAIS la carte en entier : a chaque etape, il recoit LA
   case courante (contenu + indices resolus), l'execute, repond/valide, et le
   systeme fournit la case suivante.
3. L'arret de la navigation = la fin de la mission (case `fin`) avec son
   message de cloture (reactivation de l'agent suivant inclus).

guider-parcours est l'outil d'execution (il fournit deja la case courante et
la suivante). La refonte le consolide comme SEUL point d'entree d'execution
d'une carte, avec resolution des references d'indices.

## 6. Contrat de l'outil VALIDATEUR-CASE (a creer)

Nouvel outil `validateur-case` (categorie valider/) :

```
validateur-case.py <parcours.json> [options]
  --complet      Valider TOUTES les cases (defaut)
  --case <id>    Valider UNE case
  --surcharge    Signaler les cases hors BUDGET PONDERE (poids > 3,0 unites)
  --modele       Verifier le modele compose (branches min 2, rejoint present)
  --references   Verifier que chaque reference d indice est resolvable
  --dry-run / --rapport <fichier>
```

Verifications (garde-fous) :
- **Structure** : id uniques, types valides, depart existante, fins joignables
- **Modele** : decision = branches min 2 ; deviation = rejoint present ;
  aucune boucle directe ; impasses signalees
- **Allegement** : BUDGET PONDERE des indices par case : indice COURT
  (texte <= 100 caracteres, ou sans texte : ref/outil) = 0,5 unite ; indice
  LONG (texte > 100 caracteres) = 1 unite ; budget = 3,0 unites par case ;
  plafond absolu d un indice = 160 caracteres (independant du budget). Toute
  case hors budget (poids > 3,0) ou avec un indice > 160 car. est SIGNALEE
  avec proposition de reference (pattern/protocole)
- **References** : chaque `ref` doit resoudre vers un fichier existant
- **Normes** : ASCII, LF, nommage des cases (convention ETENDUE
  `c[<prefixe-alpha-maj>]<numero>[a-z]?` : cas normal `c<numero>[a-z]?` +
  prefixe majuscule optionnel `cT1`..`cT10` -- valider-case v1.1.0,
  spec-guider-parcours v0.6.2 regle 11)

Sortie : verdict CONFORME / A ALLEGER / NON CONFORME, rapport markdown.

## 7. Evolution des generateurs

### 7.1 generateurs-case (v0.4.2 actuel)

- Generaliser `ajouter-bloc` (Pattern 7) en **modele compose complet** :
  une commande cree decision + branches (min 2) + deviation + rejoint.
- Ajouter l'option `--ref` pour poser des indices de type reference
  (au lieu du texte inline).
- Verifier le modele apres chaque commande (appel interne au validateur-case).
- Respecter le BUDGET PONDERE des indices : court <= 100 car. = 0,5 unite ;
  long > 100 car. = 1 unite ; budget 3,0 unites par case ; plafond 160 car.

### 7.2 generateurs-carte (v0.3.0 actuel)

- `creer` : squelette allege (indices = references de base uniquement).
- `detecter` / `analyser` : reutiliser les verifications du validateur-case.
- `dupliquer-chemin` : conserve les references (aucun texte inline a dupliquer).

## 8. Plan d'implementation (par etapes)

Chaque etape est une mission d'un agent habilite, validee par Morpheus (tests)
puis Janus (second controle) -- la chaine est OBLIGATOIRE (lecon de la
conformite manquee).

| Etape | Mission | Agent |
|---|---|---|
| 1 | Valider cette spec (concept valide avant de coder) | Themis (audit) ou Cerberus (presentation utilisateur) |
| 2 | Creer `validateur-case` (outil + md + spec + tests) | Vulcain (+ Morpheus tests + Janus controle) |
| 3 | Refondre `generateurs-case` (modele compose complet + --ref) | Vulcain (+ Morpheus + Janus) |
| 4 | Refondre `generateurs-carte` (squelette allege) | Vulcain (+ Morpheus + Janus) |
| 5 | Consolider guider-parcours : resolution des references d'indices + ordre d'execution obligatoire + IMPLEMENTER LE TYPE action (nouveau, aujourd hui non gere : seul fin/indice/question-controle) | Vulcain (+ Morpheus + Janus) |
| 6 | Migration pilote d'UN parcours (ex: cerberus) au nouveau format, puis generalisation | Buffy |
| 7 | Mettre a jour la spec-guider-parcours (patterns references, pas dupliques) | Promethee |

## 9. Criteres d'acceptation

1. Un agent active recit sa case une par une (guider-parcours) et n'a jamais
   besoin de lire la carte en entier pour trouver la case suivante.
2. Aucune case du nouveau format ne depasse le budget pondere des indices :
   3,0 unites par case (indice court <= 100 car. = 0,5 ; indice long = 1 ;
   plafond absolu d un indice = 160 car.) -- les regles sont des references.
3. `validateur-case` detecte toute violation (modele, surcharge, reference
   morte) et rend un verdict exploitable.
4. Le modele compose (decision + branches min 2 + deviation + rejoint) est
   genere en une seule commande par generateurs-case.
5. La chaine Morpheus (tests) -> Janus (controle) est declenchee pour chaque
   outil cree/modifie par cette refonte (conformite d'execution).
6. ASCII strict + LF sur tous les fichiers produits.
7. Le type `action` est implemente dans guider-parcours (etape 5) : une case
   `action` avec `suivant` s execute sans question et enchaine sur la case
   suivante (comportement identique a `indice` sans indices).

## 10. Emplacement des fichiers

| Fichier | Chemin |
|---|---|
| Spec (ce document) | `pense-betes/specs/spec-refonte-cartes-decision.001.01.ebauche.md` |
| Index des specs (maj) | `pense-betes/specs/index-spec.md` |
| Outil (etape 2) | `agents/tools/valider/validateur-case/` |
| Generateurs (etapes 3-4) | `agents/tools/generateurs/generateurs-case/` + `generateurs-carte/` |
| Spec de reference | `agents/tools/guider/guider-parcours/spec/spec-guider-parcours.001.01.ebauche.md` |
