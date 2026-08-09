---
identite:
  type: spec
  appartient_a: commun
  commun: true
---
# Spec -- Guide-Parcours (jeu de piste) v0.2.19

**Version** : 0.2.23
**Statut** : ebauche
**Date creation** : 2026-08-07
**Agent** : Vulcain (creation + evolutions v0.2.0 : patterns multi-missions + rappel ASCII ; v0.2.1 : procedure d'audit des 2 patterns ; v0.2.2 : regle d'autonomie des parcours ; v0.2.3 : prototype vulcain documente comme cas legitime assume ; v0.2.4 : Pattern 3 - combo generateur -> execution, lien avec spec-combos-moteur ; v0.2.5 : Pattern 4 - case Question Honnete en case 0, standard de demarrage ; v0.2.6 : Pattern 5 - chaine de delegation ACTIVE, JAMAIS de fin passive ; v0.2.7 : regle de RE-AUDIT COMPLET des 5 patterns (lecon Themis : la procedure 4b seule ne teste que Pattern 5, c est la procedure 2 qui a revele les ecarts ASCII de vulcain) ; v0.2.8 : Pattern 6 - CONTEXTE TEMPS REEL : lecture OBLIGATOIRE de l historique a chaque activation, meme en memoire (le dynamique ne se memorise pas) ; v0.2.9 : MODE AGENT NON-BLOQUANT - les questions sont destinees a l AGENT, jamais a un input() clavier ; sans --reponses l outil affiche la question et s arrete proprement (cause : demarrage d un 2e LLM bloquait sur la saisie clavier) ; v0.2.12 : outil de reference generateurs-case documente (suite de l integration : l outil officiel pour creer/editer/supprimer des cases, recablage auto + validation auto) ; v0.2.13 : Pattern 7 - modele de case compose (decision a 2+ branches, solutions alternatives, deviations avec retour au flux principal ; philosophie agents/philosophie/) ; v0.2.14 : outil de reference generateurs-carte documente (carte complete : creer/analyser/detecter/dupliquer-chemin, complement de generateurs-case pour les cases) ; v0.2.17 : branche de verifier-documents-manquants v0.3.0 dans la procedure 4g (le .md deduit de CHAQUE indice outil est controle par L OUTIL - .sh ET .py couverts - au lieu d une verification manuelle) ; v0.2.18 : Pattern 10 - UNE CARTE = UN ROLE (une carte ne contient que des actions d activation/verification/decision propres a SON role, jamais d outils d analyse/execution d un autre role ; cas Cerberus = routeur pur, carte purgee des cases lister/lire qui glissent de lire pour choisir vers lire pour executer. Lecon utilisateur 2026-08-08 : Cerberus a lance des analyses lui-meme au lieu d activer Buffy) ; v0.2.19 : Pattern 11 - CONFORMITE D EXECUTION (l audit ne verifie pas seulement la STRUCTURE du JSON mais AUSSI si l EXECUTION de la mission a suivi les ordres de la carte : l agent a-t-il fait ce que sa carte ordonnait ? Lecon constat stabilite des cartes 2026-08-08 : les violations recentes - Vulcain reactive au lieu d activer Morpheus, Cerberus analyse lui-meme - laissent les JSON structurellement valides ; la conformite d execution est le SEUL vrai test de stabilite. Critere 22 + procedure 4i + integration dans le parcours-themis (case c8b entre verdict et rapport)) ; v0.2.22 : Pattern 12 - CREATION LIMITEE (garde-fou une carte = un role applique aux cases de creation : toute case qui cree/ecrit/documente porte un indice REGLE CREATION LIMITEE precisant le perimetre - rapports de mission dans le dossier de l agent ou .tmp-* du workspace, JAMAIS tools/ - et les roles exclus : outil -> Vulcain, test -> Morpheus, case de parcours -> Buffy ; besoin manquant -> case Signaler le besoin. Lecon incident Atlas 2026-08-09 : l explorateur a ecrit un outil dans son dossier explorations/ au lieu de signaler le besoin ; carte Atlas v0.1.3 portant le garde-fou en exemple) ; v0.2.23 : Pattern 13 - LA FIN SUIT SA CARTE (generalisation de la regle de retour : activation directe = reactiver Cerberus, maillon de chaine = activer le suivant, dernier maillon = reactiver Cerberus avec bilan consolide. Lecon utilisateur 2026-08-09 : l ancienne regle toujours reactiver Cerberus etait en conflit avec les cartes - Buffy a corrige 26 fichiers ; lecon technique double/triple CRLF - lire et ecrire avec newline='' pour preserver le format natif) ; v0.2.24 : Pattern 14 - VERIFICATION D IMPACT GENERALISEE (detecter-impacts v0.2.1 devient un pas OBLIGATOIRE de TOUTE procedure d audit Themis : pour chaque mission auditee, identifier les fichiers modifies puis lancer detecter-impacts sur un echantillon representatif et verifier que TOUS les fichiers impactes listes ont ete mis a jour. Lecon utilisateur 2026-08-09 : seul le rapport-audit-janus utilisait detecter-impacts, la verification d impact doit etre GENERALISEE a tous les audits) ; v0.2.25 : RE-AUDIT COMPLET GENERALISE A 14 PATTERNS (la procedure 4c listait 12 patterns et avait vieilli pendant que 4i/4k/4l s ajoutaient ; la liste des procedures est desormais complete 1-4l et le critere 14 couvre les criteres 1 a 25. Lecon utilisateur 2026-08-09 : la procedure 4c doit etre re-verifiee a chaque ajout de pattern)
**Historique** : v0.1.0 (creation) -> v0.2.0 (documentation des 2 patterns valides en production, 2026-08-07) -> v0.2.1 (documentation de la procedure d'audit des 2 patterns, validee par l'audit des 11 parcours par Themis, 2026-08-08) -> v0.2.2 (regle d'autonomie : chaque parcours est un fichier individuel, convergence uniquement intra-parcours, 2026-08-08) -> v0.2.3 (prototype vulcain : fins independantes documentees comme CAS LEGITIME ASSUME, compatible regle 8, 2026-08-08) -> v0.2.4 (Pattern 3 : une case de parcours peut pointer vers un COMBO - combos-moteur lit definition-combo.json, generateur-commande en mode AUTO, 2026-08-08) -> v0.2.5 (Pattern 4 : case c0 Question Honnete de relecture + c0b RELIRE obligatoire + case_depart = c0, standard de demarrage fige, valide par l'audit Themis 11/11 parcours, 2026-08-08) -> v0.2.6 (Pattern 5 : CHAINE DE DELEGATION ACTIVE - une delegation ne se termine JAMAIS par une fin passive 'X te reactive' : la carte materialise la boucle RELAIS -> RETOUR -> CLOTURE -> FIN. Lecon detecter-impacts v0.2.0 / parcours-vulcain v0.2.1, 2026-08-08) -> v0.2.7 (RE-AUDIT COMPLET DES 5 PATTERNS : a chaque creation/modification/audit, REJOUER les procedures 1, 2, 3, 4 et 4b, jamais seulement la nouvelle procedure. Lecon Themis 2026-08-08 : l audit 4b seul ne testait que Pattern 5, c est la procedure 2 qui a revele 3 ecarts ASCII chez vulcain (c4/c6/c12)) -> v0.2.8 (Pattern 6 : CONTEXTE TEMPS REEL - la question honnete c0 couvre le STATIQUE (fiche + corrections, memorisable) ; l HISTORIQUE est DYNAMIQUE (il change a chaque activation des autres LLM) : sa lecture est OBLIGATOIRE a chaque activation, meme en memoire. Case c0c CONTEXTE entre c0b et c1, traversee par TOUS les chemins. Decision utilisateur 2026-08-08 : chaque agent doit se souvenir des dernieres interventions des autres agents (15 dernieres) et savoir que les autres LLM existent (section Sessions connues), pour eviter les collisions multi-LLM) -> v0.2.9 (MODE AGENT NON-BLOQUANT : les questions sont destinees a l AGENT, jamais a un input() clavier ; sans --reponses l outil affiche QUESTION POUR L AGENT et s arrete proprement code 0 ; option --interactif reservee a l usage humain. Cause : demarrage d un 2e LLM bloque sur une demande de saisie clavier au lieu de repondre a la question, 2026-08-08) -> v0.2.10 (REGLE 10 : AUCUNE BOUCLE D ATTENTE - une branche qui revient sur la MEME case pour attendre est INTERDITE, l attente est une FIN pas une boucle ; les boucles de CONTROLE (re-travail) restent autorisees. Lecon log-externe 2026-08-08 : la boucle c4 -> c4 du parcours-demarrage re-posait la question a l infini) -> v0.2.11 (REPRISE SANS BOUCLE : le message QUESTION POUR L AGENT donne la commande exacte --case <case-courante> --reponses REPONSE pour reprendre la navigation sans rejouer c0. Lecon log-externe 2026-08-08 : sans --case, le LLM relancait depuis le debut et la question honnete c0 etait REPOSEE a chaque relance -> boucle de relecture) -> v0.2.12 (OUTIL DE REFERENCE DES CASES : generateurs-case documente dans la spec comme l outil officiel pour ajouter/editer/supprimer une case avec RECABLAGE AUTO des references + VALIDATION AUTO (json + references + guider-parcours --liste) ; suite de l integration Buffy, 2026-08-08) -> v0.2.13 (Pattern 7 : MODELE DE CASE COMPOSE - une case de decision a AU MINIMUM 2 branches (sauf action directe), des solutions alternatives, des DEVIATIONS vers un workflow secondaire avec RETOUR au workflow principal (case de rejoint). Exemple reel Cerberus/Buffy : erreur hors mission signalee -> decision reparation immediate (reactiver Buffy) ou differee, puis retour au flux. Decision utilisateur 2026-08-08, philosophie agents/philosophie/alleger-decomposer) -> v0.2.14 (OUTIL DE REFERENCE DE LA CARTE COMPLETE : generateurs-carte documente a cote de generateurs-case - creer un squelette conforme aux patterns 4-5-6-7, analyser les chemins BFS, detecter les anomalies (boucles d attente, cases inatteignables, impasses, references cassees, decision a branche unique), dupliquer un chemin avec recablage et prefixe ; action ajouter-bloc de generateurs-case v0.2.0 pour creer d un coup le modele compose decision + deviation + rejoint. Etape OUTILS de la refonte du modele de cases, 2026-08-08) -> v0.2.15 (Pattern 8 : CHAINE DE DELEGATION BOUT-EN-BOUT - la delegation ne repasse PLUS par Cerberus au milieu : Cerberus active Vulcain -> Vulcain finit et ACTIVE Morpheus -> Morpheus finit et ACTIVE Janus -> Janus REACTIVE Cerberus avec le bilan consolide ; chaque maillon passe la boucle RVAV sur son travail AVANT d activer le suivant. L ancien modele boucle (Vulcain -> Morpheus -> Vulcain puis Cerberus) est remplace : la chaine ne retombe jamais sur Cerberus au milieu. Decision utilisateur 2026-08-08 : c est l agent delegue qui active le suivant a SA fin, pas Cerberus (plus fiable)) -> v0.2.16 (Pattern 9 : LIRE LE .MD DE L OUTIL AVANT DE L UTILISER - portee SYSTEMATIQUE : avant d executer tout outil, l agent lit sa documentation (.md du meme dossier) pour savoir ce qu il fait. Ancrage TRIPLE (decision utilisateur) : (a) regle de format ici, (b) guider-parcours v0.3.0 affiche automatiquement LIRE AVANT USAGE : <outil.md> pour chaque indice outil (deduit du chemin, couvre les 193 indices existants SANS les modifier), (c) generateurs-case v0.2.2 ajoute automatiquement l indice fichier .md quand un --indice-outil est ajoute (couvre les futures cases). Constat utilisateur 2026-08-08 : les agents se posaient des questions de fonctionnement avant d utiliser un outil alors que chaque outil a son .md) -> v0.2.17 (GARANT AUTOMATIQUE DU PATTERN 9 : verifier-documents-manquants v0.3.0 branche dans la procedure 4g - l outil controle que chaque script .sh ET .py a son .md et que chaque .md a son script, resultat attendu 0 manquant. Question utilisateur 2026-08-08 : etait-ce evident de creer/avoir un outil qui verifie que les outils ont leur .md ? Oui - l outil existait deja mais ne couvrait pas les .py et n etait pas branche dans 4g (lecon : un outil existe mais n est pas branche = invisible)) -> v0.2.18 (Pattern 10 : UNE CARTE = UN ROLE - la carte d un agent ne contient QUE des actions propres a SON role (activation/verification/decision), jamais d outils d analyse/execution d un autre role ; carte de Cerberus purgee des cases d analyse (lister-outils, lire la fiche de l autre agent) -> 29 a 27 cases, outils restants = coordination pure. Lecon utilisateur 2026-08-08 : Cerberus a lance des analyses lui-meme au lieu d activer Buffy car ses cases lister/lire glissaient de lire pour choisir vers lire pour executer) -> v0.2.19 (Pattern 11 : CONFORMITE D EXECUTION - l'audit Themis ne verifie pas seulement la structure du JSON mais AUSSI si l'execution de la mission a suivi les ordres de la carte : l'agent a-t-il fait ce que sa carte ordonnait ? Lecon constat stabilite des cartes 2026-08-08 : Vulcain a reactive Cerberus au lieu d'activer Morpheus, Cerberus a lance des analyses au lieu d'activer Buffy - les 2 JSON etaient structurellement valides mais l'execution a devie. La conformite d'execution est le SEUL vrai test de stabilite : critere 22 + procedure 4i + case c8b dans le parcours-themis entre le verdict et le rapport, 2026-08-08) -> v0.2.20 (PISTE C : champ catalogue optionnel sur les indices outil - reference a la commande du catalogue generateurs-commande, commande en dur conservee comme fallback ; guider-parcours v0.3.1 affiche catalogue: <nom> + PASSE PAR LE GENERATEUR quand le champ est present, 2026-08-08) -> v0.2.22 (Pattern 12 - CREATION LIMITEE : garde-fou une carte = un role applique aux cases de creation, lecon incident Atlas 2026-08-09 - l explorateur a ecrit un outil dans son dossier au lieu de signaler, 2026-08-09) -> v0.2.23 (Pattern 13 - LA FIN SUIT SA CARTE : generalisation de la regle de retour, lecon utilisateur 2026-08-09 - la regle toujours reactiver Cerberus etait en conflit avec les cartes ; lecon technique double/triple CRLF) -> v0.2.24 (Pattern 14 - VERIFICATION D IMPACT GENERALISEE : detecter-impacts branche comme pas OBLIGATOIRE de toute procedure d audit, lecon utilisateur 2026-08-09) -> v0.2.25 (RE-AUDIT COMPLET GENERALISE A 14 PATTERNS : procedure 4c + critere 14 couvrent desormais 1-4l et les criteres 1 a 25, lecon 2026-08-09)

---

## Objectif

Eliminer les oublis de conventions, regles et protocoles chez les agents en
remplacant la lecture massive des fiches (200+ lignes en memoire) par un
**parcours guide case par case** (jeu de piste). L'agent ne lit plus rien
d'avance : a chaque case, le guide lui donne l'indice exact (outil a lancer,
fichier a lire, regle a appliquer) et une question. Selon sa reponse, il
avance sur une branche precise.

## Pourquoi ce format ?

| Probleme actuel | Solution apportee |
|---|---|
| Fiches de 200+ lignes lues d'un bloc | 1 case a la fois, 20-30 lignes max |
| Regle de relecture la plus violee | Le guide affiche la regle AU MOMENT ou elle s'applique |
| Outil improvise | L'indice-outil donne le nom ET le chemin exact |
| Protocole oublie | L'indice-fichier designe LE fichier a lire a cette etape |
| Branches non prevues (improvistion) | Les branches sont ecrites : chaque reponse mene a une case |

## Vue d'ensemble

```
demarrer.md (case 0 : point d'entree)
    |
    v
parcours-<agent>.json  (source de verite du guidage)
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

## Format du fichier de parcours (JSON)

### Structure generale

```json
{
  "parcours": {
    "nom": "parcours-vulcain",
    "agent": "vulcain",
    "version": "0.1.0",
    "case_depart": "c1",
    "description": "..."
  },
  "cases": {
    "c1": { "...": "..." },
    "c2": { "...": "..." }
  }
}
```

### Structure d'une case

Une case contient une combinaison libre d'elements (0 a N) :

| Cle | Type | Obligatoire | Role |
|---|---|---|---|
| `titre` | texte | oui | Nom de la case (ex: "Verifier le systeme") |
| `type` | texte | oui | `question`, `indice`, `controle` ou `fin` |
| `question` | texte | selon type | Question posee a l'agent (obligatoire si `branches` present) |
| `indices` | tableau | non | Liste d'indices (outil / fichier / regle) a afficher |
| `branches` | tableau | non | Branches reponse -> case suivante |
| `suivant` | texte | si pas de branches | Case suivante automatique |

### Indices (tableau `indices`)

| Type d'indice | Cle | Role |
|---|---|---|
| `outil` | `nom`, `chemin`, `commande`, `catalogue` (optionnel) | L'outil exact a lancer (nom + chemin + exemple de commande). `catalogue` = nom de la commande dans le catalogue de `generateurs-commande` (piste C) : le moteur affiche alors la reference `catalogue: <nom>` + la commande du generateur `--commande <nom>` pour composer la commande via le catalogue au lieu de l'ecrire en dur. La commande en dur est CONSERVEE comme fallback. Absence du champ = comportement historique |
| `fichier` | `chemin`, `raison` | Le fichier/protocole a lire a cette etape (un seul, au bon moment) |
| `regle` | `texte` | LA regle absolue pertinente pour cette case |

### Branches (tableau `branches`)

| Cle | Type | Role |
|---|---|---|
| `reponse` | texte | La reponse attendue (OUI, NON, ou choix exact) |
| `vers` | texte | La case suivante si cette reponse est donnee |

### Types de cases

| Type | Comportement |
|---|---|
| `question` | Affiche la question + les indices, attend une reponse, suit la branche |
| `indice` | Affiche les indices, sans question : passe automatiquement a `suivant` |
| `controle` | Affiche les indices + question de verification (OUI/NON), suit la branche |
| `fin` | Case terminale : le parcours est termine |

### Regles du format

1. Chaque case doit etre atteignable depuis `case_depart` (pas de case orpheline)
2. Toute branche doit pointer vers une case existante
3. Une case `fin` n'a ni branches ni suivant
4. Une case `indice` DOIT avoir `suivant` (pas de branches)
5. Le JSON doit etre valide (json.load) et ASCII strict
6. **RAPPEL ASCII OBLIGATOIRE (v0.2.0)** : toute case qui ECRIT dans un fichier
   (creation, modification, ajout de contenu) DOIT porter, en TETE de sa liste
   `indices`, un indice `regle` rappelant la regle ASCII (100%% ASCII, aucun
   accent/emoji/Unicode, guillemets ASCII, jamais de guillemets francais).
   L'agent voit le rappel JUSTE AVANT d'ecrire.
7. **MULTI-MISSIONS (v0.2.0)** : un parcours peut couvrir PLUSIEURS missions de
   l'agent via une case `Mission` (type question) dont chaque branche mene au
   chemin d'une mission ; les chemins CONVERGENT vers des cases communes
   (verdict, lecons, retour, reactiver) pour eviter la duplication.
8. **AUTONOMIE DES PARCOURS (v0.2.2)** : chaque parcours est un FICHIER
   INDIVIDUEL (`agents/<agent>/parcours/parcours-<agent>.json`), autonome et
   complet pour SON agent. La convergence est uniquement INTRA-parcours
   (factorisation interne des cases communes d'un meme parcours). AUCUN
   partage de cases entre parcours : jamais de fichier commun, jamais de
   reference aux cases d'un autre parcours. Chaque parcours est validable
   independamment (--liste + --reponses + ASCII). Ajouter une case a un
   parcours ne touche JAMAIS les autres.
9. **QUESTION HONNETE EN CASE 0 (v0.2.5)** : TOUT parcours demarre par une case
   `c0` (type `question`) qui pose la question de relecture honnete : "As-tu EN
   MEMOIRE ta fiche et tes corrections, capables de les appliquer SANS relire
   ?". Branches OBLIGATOIRES : `OUI` -> `c1` (mission), `INCERTAIN` -> `c0b`,
   `NON` -> `c0b`. La case `c0b` (RELIRE OBLIGATOIRE, type `indice`) fait relire
   `corrections.md` puis la fiche, puis pointe vers `c1`. `case_depart` vaut
   TOUJOURS `c0`. Seul OUI prouve la memorisation : "je viens de les lire"
   n'est pas une preuve (regles-veracite).
10. **AUCUNE BOUCLE D'ATTENTE (v0.2.10)** : une branche qui revient sur la MEME
    case pour ATTENDRE (ex: `NON` -> meme case "attendre la mission") est
    INTERDITE : l'attente est une FIN, pas une boucle. Le parcours se termine
    par une case `fin` (message : "en attente de mission, le parcours s arrete
    ici, la mission arrive dans la conversation") et l'agent attend dans la
    conversation, pas en bouclant. Les boucles de CONTROLE (NON -> meme case
    = re-travail, refaire l'action puis relancer) sont autorisees : elles ne
    sont pas des attentes passives, l'agent refait l'action et relance avec
    OUI. Lecon log-externe 2026-08-08 : la boucle d'attente c4 -> c4 du
    parcours-demarrage re-posait la question a l'infini a chaque relance.
    DETECTION AUTOMATIQUE (outil v0.2.0) : `valider_parcours` refuse toute
    case dont le titre OU la question contient attendre/attente avec une
    branche vers elle-meme (ERREUR BOUCLE D'ATTENTE). Verification manuelle
    complementaire : `branche vers sa propre case` -> 0 sur les cases
    d'attente.

## CLI de l'outil guider-parcours

```
python3 guider-parcours.py <parcours.json> [options]

Options :
  --case <id>       Demarrer a une case precise (ex: c3) au lieu de case_depart
  --reponses <liste> Fournir les reponses d'un coup (separes par |) : mode agent
  --interactif      Mode interactif (input clavier) reserve a l'usage humain
  --liste           Lister toutes les cases du parcours sans naviguer
  --version         Afficher la version
  --help            Afficher l'aide
```

### Mode agent (par defaut) -- NON-BLOQUANT (v0.2.9)

**Les questions d'un parcours sont destinees a l'AGENT, jamais a une saisie
clavier.** L'outil ne fait JAMAIS `input()` en mode agent :

1. L'outil charge le JSON et valide sa structure (erreur claire si invalide)
2. Il affiche la case courante :
   ```
   === [c1/12] Verifier le systeme ===
   [REGLE]  ...
   [OUTIL]  verifier-systeme  ->  python3 .../verifier-systeme.py
   [FICHIER] protocole-technologies  (raison)

   QUESTION : Quel est le systeme ?
     [1] Windows
     [2] Linux
   ```
3. Si la case est une question/controle SANS reponse predefinie disponible
   (pas de `--reponses`, ou reponses epuisees), il affiche
   `=== QUESTION POUR L'AGENT ===` + les reponses possibles puis **s'arrete
   proprement (code 0)** : **un agent vit dans la console, il n'est pas un
   humain et ne repond jamais a une invite interactive** ; il repond selon
   son etat reel puis fournit sa reponse PAR LA CONSOLE en relancant
   **DEPUIS CETTE CASE** -- le message donne la commande exacte
   `--case <case-courante> --reponses 'REPONSE'` pour REPRENDRE sans rejouer
   les cases deja parcourues (lecon log-externe 2026-08-08 : sans `--case`,
   relancer depuis le debut rejoue c0 et repose la question honnete a chaque
   relance -> boucle de relecture).
4. Une case `indice` passe automatiquement a `suivant`.
5. Une case `fin` met fin au parcours avec le message de fin.

**Le blocage sur `input()` a ete la cause d'un bug de demarrage (2e LLM qui
restait bloque sur une demande de saisie clavier) : le mode agent est
OBLIGATOIRE par defaut, l'outil ne demande jamais rien au clavier sans
`--interactif` explicite.**

### Mode --reponses

L'agent fournit toutes les reponses d'un coup (separees par `|`), l'outil
parcourt les cases sans interaction. Une reponse vide a une case avec branches
est une erreur. Si les reponses fournies sont epuisees avant la fin, l'outil
s'arrete proprement sur la question courante (mode agent).

### Mode --interactif (usage humain uniquement)

`input()` clavier (`--interactif`) reserve au test humain : re-demande en cas
de reponse inconnue, navigation pas a pas au clavier. Les agents n'utilisent
JAMAIS ce mode.

### Mode --liste

Affiche l'inventaire des cases (id, titre, type) pour permettre a l'agent de
localiser une case ou de verifier la couverture d'une mission.

## Exemple minimal

```json
{
  "parcours": {
    "nom": "parcours-vulcain",
    "agent": "vulcain",
    "version": "0.1.0",
    "case_depart": "c1",
    "description": "Parcours de construction d'un outil"
  },
  "cases": {
    "c1": {
      "titre": "Mission",
      "type": "question",
      "question": "Quelle est la mission ?",
      "branches": [
        { "reponse": "construire", "vers": "c2" },
        { "reponse": "modifier", "vers": "c5" }
      ]
    },
    "c2": {
      "titre": "Verifier le systeme",
      "type": "indice",
      "indices": [
        { "type": "regle", "texte": "REGLE ABSOLUE : verifier avant d'agir" },
        { "type": "outil", "nom": "verifier-systeme", "chemin": "agents/tools/verifier/verifier-systeme/verifier-systeme.py", "commande": "python3 agents/tools/verifier/verifier-systeme/verifier-systeme.py" }
      ],
      "suivant": "c3"
    },
    "c9": {
      "titre": "FIN",
      "type": "fin"
    }
  }
}
```

## Outil de reference : generateurs-case (v0.2.12)

Pour AJOUTER, EDITER ou SUPPRIMER une case dans un parcours, l'outil de
reference est `generateurs-case` (categorie generateurs). Il charge la carte
de decision d'un agent (`parcours-<agent>.json`), modifie la case et recable
AUTOMATIQUEMENT les references (`suivant`, `branches[].vers`, `case_depart`).
Chaque operation declenche la VALIDATION AUTO complete : json.load +
references + `guider-parcours --liste`.

**Regle** : toute creation/edition/suppression de case PASSE PAR cet outil
(recablage automatique + validation), jamais par un editeur naif qui casserait
les liens entre cases. L'outil est integre a index-tools et a la carte de
Buffy (c10c) : c'est l'outil officiel de modification des cases.

### Sous-commandes

| Commande | Role |
|---|---|
| `liste` | Lister les cases (id, type, titre) -- la case de depart est marquee (depart) |
| `ajouter` | Ajouter une case a la position voulue (recablage auto du suivant) |
| `editer` | Editer une case existante (titre, question, message, type, indices) |
| `supprimer` | Supprimer une case avec recablage auto des references |

### L'outil de la carte COMPLETE : generateurs-carte (v0.2.14)

`generateurs-case` agit sur UNE case ; `generateurs-carte` agit sur la carte
COMPLETE (les deux dans `agents/tools/generateurs/`) :

| Action | Role |
|---|---|
| `creer` | Creer une carte squelette complete conforme aux patterns 4-5-6-7 (c0 question honnete -> c0b RELIRE -> c0c CONTEXTE -> c1 Mission -> c2 exemple -> c9 FIN) |
| `analyser` | Lister TOUS les chemins de `case_depart` aux fins (BFS anti-boucle), impasses marquees |
| `detecter` | Detecter les anomalies : references cassees, boucles d'attente (regle 10), cases inatteignables, cases sans sortie, decision a branche unique (Pattern 7) |
| `dupliquer-chemin` | Dupliquer un chemin (groupe de cases) avec recablage interne + prefixe des ids |

**Regle** : avant d'ajouter une deviation a la main, utiliser l'action
`ajouter-bloc` de `generateurs-case` (v0.2.0) : elle cree d'un coup la
decision (2 branches) + la deviation + le rejoint du Pattern 7. Puis
verifier la carte avec `generateurs-carte detecter` (0 anomalie attendue).

### Options cles

| Option | Role |
|---|---|
| `--case <id>` | Id de la nouvelle case (defaut : prochain cN libre) |
| `--type <question|indice|controle|fin>` | Type de la case (obligatoire pour ajouter) |
| `--titre <texte>` | Titre de la case |
| `--question <texte>` | Question (types question/controle) |
| `--message <texte>` | Message (type fin) |
| `--suivant <id>` | Case suivante (types indice/question/controle) |
| `--apres <id>` | Inserer APRES cette case (recablage auto du suivant) |
| `--branche <reponse>:<vers>` | Branche (repetable) |
| `--indice-regle <texte>` | Indice regle (repetable -- position 1 = rappel ASCII pour les cases d'ecriture, Pattern 2) |
| `--indice-outil <nom>:<chemin>[:commande]>` | Indice outil (repetable) |
| `--indice-fichier <chemin>:<raison>` | Indice fichier (repetable) |
| `--vers <id>` | Cible de recablage lors d'une suppression (defaut : suivant de la case supprimee) |
| `--dry-run` | Simuler sans rien modifier (convention : TOUJOURS tester avant modification reelle) |

### Exemples

```bash
# Ajouter une case apres c8 (recablage auto : l'ancienne suite de c8 pointe vers la nouvelle)
python3 agents/tools/generateurs/generateurs-case/generateurs-case.py \
  agents/vulcain/parcours/parcours-vulcain.json ajouter \
  --type indice --titre "Verifier le rapport" --suivant c9 --apres c8 \
  --indice-regle "REGLE IMMUABLE ASCII : avant d'ecrire, verifier 100%% ASCII"

# Editer le titre d'une case
python3 agents/tools/generateurs/generateurs-case/generateurs-case.py \
  agents/vulcain/parcours/parcours-vulcain.json editer c6 \
  --titre "Developper l'outil (v2)"

# Supprimer une case (recablage auto vers son suivant, --dry-run d'abord)
python3 agents/tools/generateurs/generateurs-case/generateurs-case.py \
  agents/vulcain/parcours/parcours-vulcain.json supprimer c7 --dry-run
```

### Regles d'utilisation

1. TOUJOURS lancer en `--dry-run` avant une modification reelle (convention).
2. Le recablage est automatique : avec `--apres` (insertion) et a la
   suppression (vers le suivant de la case supprimee, ou `--vers` explicite si
   la case est une fin sans suivant).
3. Une case `fin` sans `suivant` exige `--vers <id>` a la suppression
   (impossible de recabler vers un vide).
4. Garde-fou Pattern 5 : la creation/edition d'une case `fin` avec message
   passif bloquant (`te reactive`, `j attends`) declenche un AVERTISSEMENT
   (jamais de fin passive).
5. Les indices regle s'ajoutent dans l'ordre fourni : placer le rappel ASCII
   en PREMIER pour les cases d'ecriture (Pattern 2).
6. Apres chaque operation, REVALIDER le parcours (regle de RE-AUDIT COMPLET
   v0.2.7) : `guider-parcours --liste` + `--reponses` sur chaque chemin +
   `valider-conformite-ascii`.

## Patterns valides en production (v0.2.0, v0.2.4, v0.2.5, v0.2.6, v0.2.8, v0.2.13, v0.2.15, v0.2.16, v0.2.18, v0.2.19, v0.2.22, v0.2.23, v0.2.24)

Les 14 patterns suivants ont ete valides par les parcours existants et sont
OBLIGATOIRES pour tout nouveau parcours (Pattern 1 et 2 depuis v0.2.0,
Pattern 3 depuis v0.2.4, Pattern 4 depuis v0.2.5, Pattern 5 depuis v0.2.6,
Pattern 6 depuis v0.2.8, Pattern 7 depuis v0.2.13, Pattern 8 depuis v0.2.15,
Pattern 9 depuis v0.2.16, Pattern 10 depuis v0.2.18, Pattern 11 depuis
v0.2.19, Pattern 12 depuis v0.2.22, Pattern 13 depuis v0.2.23).

### Pattern 1 -- Multi-missions (une case Mission + chemins convergents)

Quand un agent a PLUSIEURS missions, le parcours demarre par une case `Mission`
(type question) dont chaque branche mene au chemin d'UNE mission. Les chemins
convergent ensuite vers des cases COMMUNES (verdict, lecons, retour) au lieu de
dupliquer ces cases dans chaque chemin.

```json
"c1": {
  "titre": "Mission",
  "type": "question",
  "question": "Quelle est la mission ?",
  "branches": [
    { "reponse": "outil", "vers": "c2" },
    { "reponse": "statut", "vers": "c11" },
    { "reponse": "modification", "vers": "c18" },
    { "reponse": "autre", "vers": "c27" }
  ]
}
```

Chaque chemin (c2..c10, c11..c17, c18..c26) est specifique a la mission, puis
converge vers les cases communes (verdict -> lecons -> reactiver).

**Exemple reel** : `agents/janus/parcours/parcours-janus.json` (30 cases,
3 chemins : outil / statut / modification).

### Pattern 2 -- Rappel ASCII obligatoire dans les cases d'ecriture

Toute case qui ECRIT dans un fichier (creer-fichier, ecrire-fichier,
editer-fichier, ajouter-contenu-fichier, rapport de controle, lecons) DOIT
porter en TETE de sa liste `indices` un indice `regle` qui rappelle la regle
ASCII. L'agent le voit juste avant d'ecrire.

```json
"c4": {
  "titre": "Ecrire les tests",
  "type": "indice",
  "indices": [
    {
      "type": "regle",
      "texte": "REGLE IMMUABLE ASCII : avant d'ecrire, verifier que le contenu est 100%% ASCII - aucun accent, emoji ou caractere Unicode. Guillemets ASCII uniquement, jamais de guillemets francais."
    },
    {
      "type": "outil",
      "nom": "creer-fichier",
      "chemin": "agents/tools/creer/creer-fichier/",
      "commande": "python3 agents/tools/creer/creer-fichier/creer-fichier.py <chemin>"
    }
  ],
  "suivant": "c5"
}
```

**Regle** : l'indice ASCII est TOUJOURS le premier element de `indices` de la
case d'ecriture. Verifier avec `grep 'REGLE IMMUABLE ASCII' <parcours.json>`
que chaque case d'ecriture est couverte.

### Pattern 3 -- Combo (generateur -> execution)

Une case de parcours peut pointer vers un **COMBO** au lieu d'enchainer une
suite d'outils. Le combo est un orchestrateur declaratif
(`definition-combo.json`) lu par `combos-moteur` (format documente dans
`agents/tools/combos/combos-moteur/spec/spec-combos-moteur.001.01.ebauche.md`).

Le principe du dataflow dans un combo :

```
CASE generateur (mode AUTO)         -> compose la commande (generateurs-commande --reponses)
CASE outil                           -> execute la commande, sortie = variable
CASE controle                         -> si resultat utilisable BRUT -> transmis directement,
                                        sinon une case generateur s'intercale
... jusqu'a la case fin
```

**Benefice** : le parcours est allege (1 case = 1 combo au lieu de 5-6 cases
d'outils), la commande est toujours validee par le generateur (modele du
catalogue), l'agent lance un combo et recupere le resultat final. Le generateur
devient incontournable : c'est lui qui compose chaque commande des cases
generatrices.

```json
"c10": {
  "titre": "Lancer le combo audit-complet",
  "type": "indice",
  "indices": [
    {
      "type": "outil",
      "nom": "combos-moteur",
      "chemin": "agents/tools/combos/combos-moteur/",
      "commande": "python3 agents/tools/combos/combos-moteur/combos-moteur.py <definition-combo.json>"
    },
    {
      "type": "fichier",
      "chemin": "agents/tools/combos/combos-moteur/spec/spec-combos-moteur.001.01.ebauche.md",
      "raison": "Format du combo : cases generateur/outil/controle/fin, variables"
    }
  ],
  "suivant": "c11"
}
```

**Regle** : une case qui pointe vers un combo reference l'outil `combos-moteur`
avec la definition du combo ; la spec du format est un indice `fichier` pour
l'agent. Le combo reste un fichier du cerveau (domaine Buffy), le moteur est un
outil (domaine Vulcain).

### Pattern 4 -- Case Question Honnete en case 0

TOUT parcours demarre par la case `c0` : une question honnete de relecture, au
lieu d'imposer une relecture aveugle. La relecture est desormais DECLENCHEE par
la reponse : seule la reponse OUI prouve la memorisation. C'est le standard de
demarrage fige pour tous les parcours.

```json
"parcours": {
  "nom": "parcours-themis",
  "agent": "themis",
  "version": "0.1.0",
  "case_depart": "c0",
  "description": "..."
},
"cases": {
  "c0": {
    "titre": "Relecture -- Question honnete",
    "type": "question",
    "question": "As-tu EN MEMOIRE ta fiche et tes corrections, capables de les appliquer SANS relire ?",
    "branches": [
      { "reponse": "OUI", "vers": "c1" },
      { "reponse": "INCERTAIN", "vers": "c0b" },
      { "reponse": "NON", "vers": "c0b" }
    ]
  },
  "c0b": {
    "titre": "RELIRE OBLIGATOIRE",
    "type": "indice",
    "indices": [
      {
        "type": "regle",
        "texte": "ACTION OBLIGATOIRE : relire corrections.md puis la fiche avant de continuer. Seul OUI prouve la memorisation."
      },
      {
        "type": "outil",
        "nom": "lire-fichier",
        "chemin": "agents/tools/lire/lire-fichier/",
        "commande": "python3 agents/tools/lire/lire-fichier/lire-fichier.py corrections.md puis la fiche"
      }
    ],
    "suivant": "c1"
  },
  "c1": { "titre": "Mission", "type": "question", "...": "..." }
}
```

**Regle** : `case_depart` vaut TOUJOURS `c0`, les branches de `c0` sont
exactement OUI/INCERTAIN/NON (OUI -> c1, INCERTAIN/NON -> c0b), et `c0b`
(RELIRE OBLIGATOIRE) fait lire corrections.md puis la fiche avant de rejoindre
`c1`. La question contient le mot `memoire` et la formulation "SANS relire".

**Exemple reel** : les 11 parcours (`agents/*/parcours/parcours-*.json`) portent
la case c0 + c0b et demarrent en c0 depuis l'audit Themis du 2026-08-08
(CONFORME 100/100, 6 points verifies par parcours).

### Pattern 5 -- Chaine de delegation ACTIVE (jamais de fin passive)

Une delegation a un autre agent (tests -> Morpheus, controle -> Janus/Themis,
flux spec/todo/pense-bete -> Promethee/Minerve/Athena...) ne se termine
JAMAIS par une case `fin` passive du type "X teste et te reactive". Une fin
passive coupe la chaine : l'agent delegue est active mais personne ne prend le
relais, l'execution s'arrete et l'agent delegue ne fait rien (lecon
utilisateur detecter-impacts v0.2.0, corrigee sur parcours-vulcain v0.2.1).

La carte de l'agent DELEGANT doit MATERIALISER la boucle apres l'activation :

```json
"c8": {
  "titre": "Deleguer les tests a Morpheus",
  "type": "controle",
  "branches": [
    { "reponse": "OUI", "vers": "c9a" },
    { "reponse": "NON", "vers": "c8" }
  ]
},
"c9a": {
  "titre": "RELAIS : prendre le relais de l'agent delegue",
  "type": "indice",
  "indices": [
    { "type": "regle", "texte": "REGLE RELAIS : la delegation ne termine PAS le parcours. Je lance le parcours de l'agent delegue (guider-parcours) et il execute ses cases jusqu'au rapport." },
    { "type": "outil", "nom": "guider-parcours", "chemin": "agents/tools/guider/guider-parcours/", "commande": "python3 agents/tools/guider/guider-parcours/guider-parcours.py agents/<agent-delegue>/parcours/parcours-<agent-delegue>.json" }
  ],
  "suivant": "c9b"
},
"c9b": {
  "titre": "RETOUR : l'agent delegue t'a-t-il reactive avec un rapport VALIDE ?",
  "type": "controle",
  "branches": [
    { "reponse": "OUI", "vers": "c9c" },
    { "reponse": "NON", "vers": "c9a" }
  ]
},
"c9c": {
  "titre": "CLOTURE : verifier le rapport et reactiver Cerberus",
  "type": "indice",
  "suivant": "c9"
},
"c9": {
  "titre": "FIN - Mission terminee",
  "type": "fin",
  "message": "Mission terminee : rapport verifie, Cerberus reactive avec le bilan."
}
```

**Regles** :
1. La case `fin` n'apparait qu'APRES la CLOTURE (le retour a Cerberus est une
   ACTION finale, pas une attente).
2. Le message d'une case `fin` ne contient JAMAIS de formulation passive du type
   "X teste et te reactive", "X fera", "j'attends le retour" : il DECRIT
   l'action finale deja executee ou a executer.
3. Si l'agent delegue doit lui-meme deleguer (chaine), son parcours porte AUSSI
   la boucle (RELAIS -> RETOUR -> CLOTURE -> FIN) : la chaine ne s'arrete
   jamais, chaque maillon se termine par la reactivation de Cerberus.
4. La REGLE ABSOLUE 7 est ajoutee dans le template de fiche agent (v0.2.0) :
   toute nouvelle fiche la reproduit.

**Exemple reel (historique)** : `agents/vulcain/parcours/parcours-vulcain.json` v0.2.1
portait la boucle c8 -> c9a RELAIS -> c9b RETOUR -> c9c CLOTURE -> c9 FIN (et idem
c14 -> c15a/c15b/c15c/c15). DEPUIS v0.2.15, la chaine outil -> tests -> controle est
migree vers le **Pattern 8 (chaine bout-en-bout)** : Vulcain finit et ACTIVE Morpheus
(fins c9/c15), Morpheus finit et ACTIVE Janus, Janus REACTIVE Cerberus avec le bilan
consolide. Le Pattern 5 reste le modele de reference pour les delegations SIMPLES a
un seul niveau (voir exemples JSON ci-dessus).

### Pattern 6 -- CONTEXTE TEMPS REEL (lecture obligatoire de l'historique)

La question honnete c0 couvre le STATIQUE (MA fiche, MES corrections --
contenu memorisable). L'HISTORIQUE (AGENTS-historique.md) est un contenu
DYNAMIQUE : il change a chaque activation des autres agents/LLM. Il est
IMPOSSIBLE de l'avoir en memoire -- sa lecture est donc OBLIGATOIRE a CHAQUE
activation, meme si deja lu (decision utilisateur 2026-08-08 : chaque agent
doit se souvenir des dernieres interventions des autres agents pour eviter
les collisions multi-LLM et comprendre l'activite en temps reel).

Le parcours insere une case `c0c` CONTEXTE entre la relecture et la mission,
traversee par TOUS les chemins :

```json
"c0": {
  "type": "question",
  "branches": [
    { "reponse": "OUI", "vers": "c0c" },
    { "reponse": "INCERTAIN", "vers": "c0b" },
    { "reponse": "NON", "vers": "c0b" }
  ]
},
"c0b": {
  "titre": "RELIRE OBLIGATOIRE",
  "type": "indice",
  "suivant": "c0c"
},
"c0c": {
  "titre": "CONTEXTE OBLIGATOIRE : activite recente des agents",
  "type": "indice",
  "indices": [
    {
      "type": "regle",
      "texte": "REGLE ABSOLUE -- CONTEXTE TEMPS REEL : meme si je viens de lire l historique, je le RELIS TOUJOURS : c est le fil temps reel du cerveau (il change a chaque activation des autres LLM), le dynamique ne se memorise pas. Je lis aussi la section Sessions connues d AGENTS.md pour savoir que les autres LLM existent."
    },
    {
      "type": "outil",
      "nom": "lire-activite-recente",
      "chemin": "agents/tools/lire/lire-activite-recente/",
      "commande": "python3 agents/tools/lire/lire-activite-recente/lire-activite-recente.py"
    },
    {
      "type": "fichier",
      "chemin": "AGENTS.md",
      "raison": "Section ## Sessions connues : la table des sessions existantes (session | id LLM | agent actif | derniere activite)"
    }
  ],
  "suivant": "c1"
}
```

**Regles** :
1. `c0c` existe dans TOUT parcours, entre `c0b` et `c1` : c0 OUI -> c0c,
   c0b -> c0c, c0c -> c1. Aucun chemin ne contourne c0c.
2. La case `c0c` porte l'outil `lire-activite-recente` (les 15 dernieres
   interventions, format date | session | agent | action) et l'indice fichier
   AGENTS.md section `## Sessions connues` (les autres LLM existent).
3. La lecture de l'historique est OBLIGATOIRE meme en memoire : c'est le
   dynamique, il change a chaque activation.
4. La REGLE ABSOLUE 8 est ajoutee dans le template de fiche agent (v0.2.0) :
   toute nouvelle fiche la reproduit.

**Exemple reel** : les 11 parcours (`agents/*/parcours/parcours-*.json`)
portent la case c0c depuis 2026-08-08 (CONTEXTE TEMPS REEL, decision
utilisateur -- avec les outils lire-activite-recente v0.1.0 et
activer-agent-principal v0.4.1 section Sessions connues).

### Pattern 7 -- Modele de case compose (decision + deviations avec retour) (v0.2.13)

Une case de DECISION ne doit plus etre un cul-de-sac a reponse unique : elle
est le debut d'un MODELE COMPOSE. Le principe fondateur vient de la
philosophie "alleger ne veut pas dire supprimer : decomposer pour faciliter"
(agents/philosophie/) : garder la richesse, la decomposer en petites etapes
manipulables.

**Regles du modele compose** :
1. Toute case de decision (`question` ou `controle`) porte AU MINIMUM 2
   branches (sauf action directe : une case `indice` a `suivant` est une
   ACTION, pas une decision). Deux branches = deux solutions alternatives
   pour resoudre le probleme, ou une decision + une deviation.
2. Une DEVIATION est une branche vers un WORKFLOW SECONDAIRE (un groupe de
   cases qui traite un sous-probleme). La derniere case du workflow
   secondaire a un `suivant` qui REJOINT le workflow principal (case de
   rejoint) -- jamais une fin, jamais une boucle d'attente (regle 10).
3. Le retour au flux principal se fait par une case de REJOINT (le plus
   souvent la case qui suit naturellement la decision, ou une case commune
   du flux principal).
4. La deviation n'est PAS une boucle : elle avance dans le workflow
   secondaire puis revient au principal a un point AVANCE (case de rejoint),
   jamais sur la meme case.

```json
"c5": {
  "titre": "Decision : reparation immediate ou differee ?",
  "type": "question",
  "question": "La reparation doit-elle etre faite TOUT DE SUITE ?",
  "branches": [
    { "reponse": "OUI", "vers": "c5a" },
    { "reponse": "NON", "vers": "c6" }
  ]
},
"c5a": {
  "titre": "DEVIATION : workflow secondaire (reactiver Buffy pour reparer)",
  "type": "indice",
  "indices": [ ... ],
  "suivant": "c5b"
},
"c5b": {
  "titre": "REJOINT le flux principal",
  "type": "indice",
  "indices": [ ... ],
  "suivant": "c6"
},
"c6": { "titre": "Suite du flux principal", "type": "indice", "suivant": "c7" }
```

**Exemple reel** : la boucle Cerberus/Buffy (v0.2.13) -- si Buffy trouve des
erreurs HORS MISSION pendant sa mission, elle le signale a Cerberus ; la
carte de Cerberus porte une case de decision "erreur hors mission signalee"
avec 2 branches : OUI (reparation immediate -> deviation : reactiver Buffy,
elle repare, revient au flux) / NON (differer -> le flux principal continue).
Chaque carte porte SA deviation (Buffy : signaler ; Cerberus : decider),
jamais de partage inter-parcours (regle 8).

### Pattern 8 -- Chaine de delegation BOUT-EN-BOUT (v0.2.15)

La delegation ne repasse PLUS par Cerberus au milieu du travail. Quand une
mission en engendre une autre (ex: construire un outil -> le tester -> le
controler), la chaine est LINEAIRE et chaque maillon active le suivant A SA
FIN :

```
Cerberus active Vulcain
  -> Vulcain execute sa mission, passe la boucle RVAV sur son travail,
     puis ACTIVE Morpheus (tests) a sa fin
  -> Morpheus teste, passe la boucle RVAV sur son rapport,
     puis ACTIVE Janus (controle) a sa fin, avec le rapport de tests
  -> Janus controle, passe la boucle RVAV sur son rapport,
     puis REACTIVE Cerberus avec le BILAN CONSOLIDE de la chaine
     (rapport de tests de Morpheus + rapport de controle de Janus)
```

**Pourquoi** (decision utilisateur 2026-08-08) : dans l'ancien modele boucle
(Vulcain -> Morpheus -> Vulcain, puis Vulcain -> Cerberus), demander a
Cerberus de relancer le suivant au milieu de la chaine n'est PAS fiable : la
chaine peut se couper, et chaque retour a l'expediteur ajoute un aller-retour
inutile. Dans la chaine bout-en-bout, C EST L AGENT DELEGUE QUI ACTIVE LE
SUIVANT A SA FIN : personne ne doit demander a Cerberus de le faire.

**Regles** :
1. La fin du parcours d'un maillon de la chaine ORDONNE d'activer le maillon
   suivant (message de fin actif : "J ACTIVE <maillon suivant> ..."), jamais
   une fin passive ni un retour a l'expediteur au milieu.
2. Le dernier maillon (Janus pour la chaine outil -> tests -> controle)
   REACTIVE Cerberus avec le BILAN CONSOLIDE de toute la chaine.
3. RVAV A CHAQUE MAILLON : chaque agent passe la boucle RVAV (Rechercher,
   Verifier, Analyser, Valider) sur SON travail AVANT d'activer le suivant
   (case RVAV avant la fin ou indice RVAV en tete de la fin).
4. Une activation DIRECTE par Cerberus (hors chaine) reste valide : la fin
   revient a Cerberus directement (ex: Morpheus active directement par
   Cerberus -> fin = reactiver Cerberus).
5. Le Pattern 5 (boucle RELAIS -> RETOUR -> CLOTURE) reste valide pour les
   cas simples a un seul niveau ; le Pattern 8 le REMPLACE pour les chaines
   multi-maillons (outil -> tests -> controle).

**Exemple reel** : la chaine outil v0.2.15 -- parcours-vulcain (fins c9/c15 :
"MORPHEUS ACTIVE, la chaine continue"), parcours-morpheus (fin c10 : "J
ACTIVE JANUS avec le rapport de tests"), parcours-janus (fin c10 : "REACTIVE
CERBERUS avec le bilan consolide"), parcours-cerberus (case c7 flux chaine
bout-en-bout).

### Pattern 9 -- LIRE LE .MD DE L OUTIL AVANT DE L UTILISER (v0.2.16)

AVANT d'executer un outil, l'agent lit SA documentation (.md du meme
dossier) pour savoir ce qu'il fait, comment il s'utilise, et ses options.
Portee SYSTEMATIQUE : la regle s'applique a TOUT indice outil, sans
exception (decision utilisateur 2026-08-08).

**Pourquoi** (constat utilisateur) : les agents se posaient souvent des
questions de fonctionnement avant d'utiliser un outil, alors que chaque
outil a un `.md` de documentation. Lire la doc AVANT d'executer elimine les
questions, evite les mauvaises utilisations et reduit les allers-retours.

**Ancrage TRIPLE** (decision utilisateur) :
1. **Regle de format** (ici) : tout indice outil implique la lecture de son
   `.md` avant execution -- documente en tete des indices ou via le rappel
   de l'outil de guidage.
2. **Affichage auto (guider-parcours v0.3.0)** : `afficher_indices` ajoute
   pour CHAQUE indice outil une ligne `LIRE AVANT USAGE : <outil.md>`
   deduite du chemin (dossier de l'outil + nom + .md ; si le chemin pointe
   vers un .py/.sh, remonter au dossier). Le .md est verifie : s'il existe,
   le chemin exact est affiche ; sinon, `LIRE AVANT USAGE (doc a verifier)`.
   Ce mecanisme couvre les 193 indices outil EXISTANTS SANS les modifier.
3. **Generation auto (generateurs-case v0.2.2)** : quand un `--indice-outil`
   est ajoute a une case, l'outil ajoute AUTOMATIQUEMENT l'indice `fichier`
   du `.md` de l'outil (deduit du chemin, si le fichier existe), avec la
   raison `LIRE AVANT USAGE (Pattern 9)`. Ce mecanisme couvre les FUTURES
   cases : chaque nouvel outil reference nait avec son rappel de doc.

```json
"c2": {
  "titre": "Verifier le systeme",
  "type": "indice",
  "indices": [
    {
      "type": "outil",
      "nom": "verifier-systeme",
      "chemin": "agents/tools/verifier/verifier-systeme/verifier-systeme.py",
      "commande": "python3 agents/tools/verifier/verifier-systeme/verifier-systeme.py"
    },
    {
      "type": "fichier",
      "chemin": "agents/tools/verifier/verifier-systeme/verifier-systeme.md",
      "raison": "LIRE AVANT USAGE (Pattern 9) : la doc de l outil explique ce qu il fait et comment l utiliser"
    }
  ],
  "suivant": "c3"
}
```

**Regles** :
1. Le `.md` d'un outil vit dans le MEME dossier que l'outil, avec le meme
   nom (ex: `agents/tools/lire/lire-fichier/lire-fichier.md`).
2. L'indice outil d'une case ne remplace PAS la lecture de la doc : la
   commande donne le QUOI, le `.md` donne le COMMENT (options, pieges,
   exemples). Lire la doc AVANT d'executer.
3. Si le `.md` n'existe pas (ex: motif joker `tester-protection-*`),
   verifier la doc la plus proche (dossier) ou la demander a Vulcain avant
   d'utiliser l'outil.
4. Le rappel reste compatible avec le Pattern 2 (rappel ASCII en position
   1 des cases d'ecriture) : l'indice `.md` s'ajoute APRES le rappel ASCII
   et apres l'indice outil, il ne le remplace pas.

### Pattern 10 -- UNE CARTE = UN ROLE (v0.2.18)

La carte de decision d'un agent ne contient QUE des actions propres a SON
role : des cases d'ACTIVATION, de VERIFICATION et de DECISION. Elle ne
contient JAMAIS d'outils d'ANALYSE ou d'EXECUTION qui appartiennent au role
d'un AUTRE agent (lecon utilisateur 2026-08-08 : Cerberus a lance des
analyses lui-meme au lieu d'activer Buffy, car sa carte portait des cases
lister/lire qui glissent de "lire pour choisir" vers "lire pour executer").

**Le principe** : "une place pour chaque chose & chaque chose a sa place"
(philosophie). Chaque agent fait CE POUR QUOI IL EST HABILITE :

| Agent | Role dans SA carte | Outils autorises |
|---|---|---|
| Cerberus | ROUTEUR PUR : ecouter, identifier, activer, verifier, decider | coordination uniquement (`activer-agent-principal`, `lister-agents` pour choisir, `lire-activite-recente` pour le contexte, `lire-fichier` sur SES fichiers en c0b) |
| Buffy | fichiers du cerveau | outils d'edition/validation du cerveau |
| Vulcain | outils | outils de creation/test developpement |
| Themis | audits | outils d'evaluation |
| ... | ... | ... |

**Regles** :
1. Une carte = LE ROLE de l'agent. Toute case qui porte un outil d'ANALYSE
   ou d'EXECUTION appartenant a un autre role est un ECART.
2. Les outils de COORDINATION (lister pour choisir, lire pour le contexte,
   activer) sont propres au role de coordinateur. Les outils d'ANALYSE du
   cerveau (lister-outils, detecter-impacts, generateurs-carte...) ne
   figurent JAMAIS dans la carte d'un agent qui ne les utilise pas dans SON
   role.
3. PIEGE DU GLISSEMENT : une case de coordination ("lister les agents pour
   choisir") peut devenir une case d'analyse ("lister pour executer") sans
   changer de contenu. La regle est dans l'INTENTION : lire pour DECIDER est
   du role ; lire pour EXECUTER est de la derive. Le generateur et les
   audits verifient la LISTE des outils par carte.
4. Cas Cerberus (exemple reel) : sa carte est purgee des cases d'analyse
   (lister-outils, lire la fiche de l'autre agent) -- il ne reste que des
   cases activer/verifier/decider. Lire la fiche de l'agent active est
   INTERDIT (c'est l'agent qui lit SES fichiers en prenant le relais,
   regle de relecture).
5. La regle est compatible avec le Pattern 8 (chaine) et le Pattern 9
   (lire le .md avant usage) : lire la doc d'un outil de SON role reste
   obligatoire ; les outils des AUTRES roles sont exclus de la carte.

```json
"c2": {
  "titre": "Ecouter la demande",
  "type": "indice",
  "indices": [
    { "type": "regle", "texte": "REGLE ABSOLUE : je n execute JAMAIS une mission moi-meme. Mon role = ecouter, identifier, activer l agent habilite, verifier, decider." },
    { "type": "outil", "nom": "lister-agents", "chemin": "agents/tools/lister/lister-agents/", "commande": "python3 agents/tools/lister/lister-agents/lister-agents.py" }
  ],
  "suivant": "c5"
}
```

### Pattern 11 -- CONFORMITE D EXECUTION (v0.2.19)

La stabilite d'une carte ne se mesure PAS par la structure seule (detecter 0
anomalie, valider-cartes CONFORME) mais par la CONFORMITE D'EXECUTION :
l'agent a-t-il fait ce que sa carte ordonnait pendant l'execution reelle de sa
mission ? (lecon constat stabilite des cartes 2026-08-08).

**Pourquoi** : les violations recentes ont laisse les JSON parfaitement
valides :

| Violation constatee | JSON au moment des faits |
|---|---|
| Vulcain a REACTIVE Cerberus au lieu d'ACTIVER Morpheus | structurellement CONFORME (sa carte disait pourtant MORPHEUS ACTIVE) |
| Cerberus a lance des ANALYSES au lieu d'activer Buffy | structurellement CONFORME (sa carte etait un routeur) |

Dans les 2 cas, aucune validation automatique ne pouvait detecter la derive :
le JSON etait valide, c'est l'EXECUTION qui a devie. La conformite
d'execution est donc le SEUL vrai test de stabilite -- elle exige une
verification CROISEE, pas un outil.

**Comment auditer la conformite d'execution** (croisement, pas outil) :
1. La MISSION recue (la demande initiale, ce que l'agent devait faire).
2. La CARTE de l'agent (les cases ordonnees : activer X, lancer Y, fin = Z).
3. Le DEROULEMENT REEL : le message d'activation/reactivation (qui a ete
   active ?), les FICHIERS MODIFIES (git status, detecter-impacts), les
   RAPPORTS produits.
4. Verdict : si l'agent a execute une action que SA carte ne lui ordonnait
   pas (ou n'a pas execute une action ordonnee), c'est un ECART DE
   CONFORMITE D'EXECUTION -- a signaler dans le rapport d'audit meme si le
   JSON est CONFORME.

**Ou cela vit** : critere 22 + procedure d'audit 4i + case c8b du
parcours-themis (controle entre le verdict c8 et le rapport c9 : "As-tu
verifie que l'execution de la mission a suivi les ordres de la carte ?").

```json
"c8b": {
  "titre": "CONFORMITE D EXECUTION : l agent a-t-il fait ce que sa carte ordonnait ?",
  "type": "controle",
  "question": "As-tu verifie (croisement mission / carte / deroulement reel) que l'EXECUTION de la mission a suivi les ordres de la carte -- et pas seulement la structure du JSON ?",
  "indices": [
    { "type": "regle", "texte": "PATTERN 11 (spec v0.2.19) : la structure valide ne prouve PAS la stabilite. Une carte peut etre CONFORME et l'execution avoir devie (Vulcain -> reactiver au lieu d'activer Morpheus ; Cerberus -> analyser au lieu d'activer Buffy). Verifier par CROISEMENT : mission recue + cases ordonnees par la carte + actions reelles (activation, fichiers modifies, rapports)." }
  ],
  "branches": [
    { "reponse": "OUI", "vers": "c9" },
    { "reponse": "NON", "vers": "c3" }
  ]
}
```

**Regles** :
1. La conformite d'execution est un CRITERE d'audit (critere 22) au meme
   titre que les 11 patterns : chaque audit Themis verifie la conformite
   d'execution AVANT de rendre le verdict.
2. Un ECART d'execution est signale dans le rapport d'audit (section
   Resultats / Synthese) MEME SI le JSON est structurellement CONFORME :
   c'est le seul moyen de detecter la derive comportementale.
3. Le croisement est un raisonnement de l'auditeur (Themis), pas un outil :
   les traces sont la mission recue, le message d'activation/reactivation,
   les fichiers modifies et les rapports.
4. La regle est compatible avec le Pattern 10 (une carte = un role) : le
   Pattern 10 verifie la STRUCTURE de la carte, le Pattern 11 verifie
   l'EXECUTION de la mission -- les deux se completent.

5. La reactivation finale de Cerberus est un POINT DE CONFORMITE
   obligatoire : verifier les 5 points R1-R5 (3e argument
   `agent_precedent` present, pas d aide affichee, sortie `Session ... :
   Cerberus reactive avec succes`, bloc AGENTS.md passe sur Cerberus,
   profil classeur mis a jour). Une reactivation qui affiche l AIDE =
   ECHEC SILENCIEUX (le bloc reste sur l agent) : a signaler comme
   ecart d execution dans le rapport d audit (lecon Themis 2026-08-09).


### Pattern 12 -- CREATION LIMITEE (garde-fou une carte = un role) (v0.2.22)

Le Pattern 10 (une carte = un role) s'applique AUSSI aux CASES DE CREATION :
toute case qui cree, ecrit ou documente porte un indice `regle` CREATION
LIMITEE qui precise le PERIMETRE de creation (ce que l'agent est habilite a
creer) et les ROLES EXCLUS (ce que l'agent ne doit JAMAIS creer lui-meme).
Lecon incident Atlas 2026-08-09 : l'explorateur a ecrit un OUTIL
(scan-catalogue.py) dans son dossier explorations/ au lieu de signaler le
besoin -- sa carte ne portait aucun garde-fou contre la creation d'outils
(defaut connu de sa fiche : "peut creer des structures trop elaborees").

**Pourquoi** : une carte qui autorise "ecrire un fichier" peut glisser vers
"ecrire un outil" sans changer de contenu (meme piege de glissement que le
Pattern 10). Le garde-fou est dans le PERIMETRE EXPLICITE : l'agent sait, a
chaque case de creation, QUOI il peut creer et QUOI il doit signaler.

**Le principe** : chaque agent cree UNIQUEMENT ce que SON role habilite :

| Agent | Habilite a creer | JAMAIS (roles exclus) |
|---|---|---|
| Atlas (explorateur) | rapports de mission (dossier explorations/ ou .tmp-* du workspace) | outil (Vulcain), test (Morpheus), case de parcours (Buffy) |
| Buffy | fichiers du cerveau (parcours, conventions, philosophie) | outils (Vulcain), tests (Morpheus) |
| Vulcain | outils (py/sh/md/spec + catalogue) | parcours (Buffy), tests (Morpheus) |
| Morpheus | tests formels (tester/tests/test-XXX) | outils (Vulcain), parcours (Buffy) |
| Promethee / Minerve / Athena | specs / todos / pense-betes | outils, tests, parcours |
| ... | ... | ... |

**Regles** :
1. Toute case qui cree/ecrit/documente porte un indice `regle` CREATION
   LIMITEE en TETE de ses `indices` : perimetre (rapports de mission dans le
   dossier de l'agent ou .tmp-* du workspace, JAMAIS dans tools/) + roles
   exclus (outil -> Vulcain, test -> Morpheus, case de parcours -> Buffy).
2. Si la mission necessite un outil ou un test MANQUANT, l'agent NE CREE
   RIEN lui-meme : il va a la case `Signaler le besoin` (ou signale a
   Cerberus) qui active l'agent habilite.
3. La case `Signaler le besoin` ne demande JAMAIS a l'agent de "documenter
   une nouvelle case dans le parcours" : la creation de case est le role de
   Buffy.
4. Compatible avec les Patterns 2 (rappel ASCII position 1 des cases
   d'ecriture) et 9 (lire le .md avant usage) : le garde-fou CREATION
   LIMITEE s'ajoute aux autres indices sans les remplacer.

```json
"c9": {
  "titre": "Documenter les decouvertes",
  "type": "indice",
  "indices": [
    {
      "type": "regle",
      "texte": "CREATION LIMITEE A LA DOCUMENTATION : je cree uniquement des rapports de mission (dossier explorations/ ou .tmp-* du workspace, JAMAIS dans tools/). JAMAIS de creation d outil (role Vulcain), JAMAIS de test (role Morpheus), JAMAIS de case de parcours (role Buffy). Si la mission necessite un outil ou un test manquant -> je signale a Cerberus (case Signaler le besoin)."
    },
    {
      "type": "regle",
      "texte": "REGLE IMMUABLE ASCII : avant d'ecrire, verifier que le contenu est 100%% ASCII."
    },
    {
      "type": "outil",
      "nom": "ecrire-fichier",
      "chemin": "agents/tools/ecrire/ecrire-fichier/",
      "commande": "python3 agents/tools/ecrire/ecrire-fichier/ecrire-fichier.py <chemin>"
    }
  ],
  "suivant": "c10"
}
```

**Cas d'application** : toute case de creation/documentation d'un parcours
(ex: cases c9/c18/c19/c25 du parcours-atlas v0.1.3, revision lecon Atlas
2026-08-09). Le garde-fou est place en tete des indices, l'essentiel etant
que l'agent le voie JUSTE AVANT d'ecrire.

### Pattern 13 -- LA FIN SUIT SA CARTE (v0.2.23)

La fin de mission d'un agent suit SA CARTE, jamais une regle generale unique.
L'ancienne regle "toujours reactiver Cerberus" (AGENTS.md, index-agents,
cerberus/corrections, todo-template, 8 cases FIN - Delegation) etait en
CONTRADICTION avec la philosophie "chaque agent active l'agent suivant dans sa
carte" deja materialisee par le Pattern 8 (chaine bout-en-bout) et les
parcours morpheus c17 / janus c30. Buffy a corrige le conflit dans 26
fichiers (2026-08-09) : la regle generale dit desormais la meme chose que les
cartes. Lecon utilisateur : le conflit venait des documents de COORDINATION
(regle generale), pas des parcours -- un pattern doit etre enonce au meme
endroit que les cartes qu'il regit.

**Regles** :
1. Activation DIRECTE par Cerberus (hors chaine) -> fin = reactiver Cerberus.
2. Maillon d'une chaine de delegation -> fin = ACTIVER le maillon suivant
   selon SA carte (message de fin actif : "J ACTIVE <maillon suivant> ...").
3. Le DERNIER maillon de la chaine -> reactiver Cerberus avec le BILAN
   CONSOLIDE de toute la chaine (Pattern 8).
4. La chaine ne retombe JAMAIS sur Cerberus au milieu (retour a l'expediteur
   au milieu = anomalie qui coupe la chaine).

**Lien avec le Pattern 8** : le Pattern 8 (v0.2.15) documente la chaine
bout-en-bout comme CAS PARTICULIER des chaines outil -> tests -> controle
(Vulcain -> Morpheus -> Janus -> Cerberus). Le Pattern 13 GENERALISE la regle
a TOUTES les fins de mission : chaque fiche porte une section "Pour terminer
ma mission (la fin suit SA carte)" + une ligne FLUX adaptee au role (atlas ne
delegue pas ; janus = dernier maillon bilan consolide ; vulcain = apres
delegation des tests a Morpheus ; minerve = Phase 9 flux Promethee -> Minerve).

**Exemple JSON** (fin d'activation directe vs fin de chaine) :

```json
{
  "c9": {
    "titre": "FIN - Activation directe",
    "type": "fin",
    "message": "Reactiver Cerberus avec le bilan (activation directe par Cerberus)."
  },
  "c17": {
    "titre": "FIN - Delegation",
    "type": "fin",
    "message": "L agent active execute sa mission puis active le maillon suivant de la chaine (ou reactive Cerberus si active directement par lui)."
  }
}
```

**Piege technique -- DOUBLE/TRIBLE CRLF (lecon Buffy 2026-08-09)** : ecrire
un fichier CRLF avec `io.open(newline='\r\n')` CONVERTIT chaque `\r\n`
existant en `\r\r\n` (et un second passage en `\r\r\r\n`) : corruption
SILENCIEUSE (py_compile / bash -n cassent ensuite, sans erreur visible au
moment de l'ecriture). REGLE : lire AVEC `newline=''` et ecrire AVEC
`newline=''` (aucune conversion), ou reparer avec `re.sub(r'\r+\n',
'\r\n', txt)`. Preserver le format natif du fichier, jamais laisser Python
### Pattern 14 -- VERIFICATION D IMPACT GENERALISEE (v0.2.24)

Chaque mission d'un agent IMPACTE plusieurs fichiers (outil + spec + catalogue +
index-tools + fiches + parcours + corrections). Un audit Themis ne verifie pas
seulement la conformite de ce qui a ete fait : il verifie AUSSI que TOUS les
fichiers impactes ont ete mis a jour (rien d oublie). Lecon utilisateur
2026-08-09 : seul le rapport-audit-janus utilisait detecter-impacts, la
verification d impact doit etre GENERALISEE a tous les audits (les impacts
oublies - spec pas bump, index pas a jour, catalogue pas regenerer - sont des
defauts silencieux qui corrodent l ecosysteme).

**Regles** :
1. POUR CHAQUE mission auditee, identifier les fichiers modifies : message
   d'activation, message de reactivation (bilan), git status, rapport de
   mission.
2. Lancer detecter-impacts (python3 cerveau-projet/agents/tools/detecter/
   detecter-impacts/detecter-impacts.py <fichier-modifie> --racine
   cerveau-projet) sur UN ECHANTILLON REPRESENTATIF des fichiers modifies
   (outil principal + un fichier transverse type index-tools ou spec).
3. Verifier que TOUS les fichiers impactes listes par l'outil ont ete mis a
   jour : index-tools, catalogue generateurs-commande, spec, fiches,
   parcours, corrections, AGENTS-historique.
4. TOUT impact NON mis a jour = NON CONFORME : documenter le fichier manquant
   dans le rapport avec l'action de correction requise.
5. L'outil detecter-impacts est l'outil de reference (verifier son .md avant
   usage -- Pattern 9) : il detecte les fichiers impactes par reference
   croisee (identite, chemins, commun) et distingue les traces historisees
   [HISTORISE] des fichiers a mettre a jour.

**Lien avec les autres patterns** : le Pattern 11 (conformite d execution)
verifie QUE l'agent a suivi sa carte ; le Pattern 14 verifie QUE les impacts
de ce qui a ete fait sont tous mis a jour. Les deux sont des garanties
d'execution, le premier sur le PROCESSUS, le second sur les LIVRABLES.

**Piege technique -- DOUBLE/TRIBLE CRLF (lecon Buffy 2026-08-09)** : rappel
du Pattern 13 : lire AVEC newline='' et ecrire AVEC newline='' (aucune
conversion), ou reparer avec re.sub(r'\r+\n', '\r\n', txt). Preserver le
format natif du fichier, jamais laisser Python convertir.

## Procedure d'audit des 14 patterns (v0.2.1, v0.2.4, v0.2.5, v0.2.6, v0.2.8, v0.2.13, v0.2.15, v0.2.16, v0.2.18, v0.2.19, v0.2.22, v0.2.23, v0.2.24)

La procedure suivante a ete validee par l'audit de la serie des 11 parcours
realise par Themis (evaluatrice croisee) le 2026-08-08. Elle est a appliquer a
CHAQUE creation, modification ou audit de parcours pour verifier la conformite
aux 11 patterns (le Pattern 3 s'ajoute a la procedure en v0.2.4, le Pattern 4
en v0.2.5, le Pattern 5 en v0.2.6, le Pattern 6 en v0.2.8, le Pattern 7 en
v0.2.13, le Pattern 8 en v0.2.15, le Pattern 9 en v0.2.16, le Pattern 10 en
v0.2.18, le Pattern 11 en v0.2.19).

> **REGLE DE RE-AUDIT COMPLET (v0.2.7, LECON THEMIS)** : a chaque
> creation, modification ou audit d'un parcours, REJOUER les procedures
> 1, 2, 3, 4, 4b, 4d, 4e, 4f, 4g, 4h ET 4i dans leur integralite -- JAMAIS seulement la procedure
> nouvelle ou modifiee. La lecon Themis 2026-08-08 : l'audit lance avec la
> procedure 4b (Pattern 5) seule n'a teste QUE le nouveau pattern ; ce sont
> les procedures precedentes rejouees (surtout la procedure 2, rappel ASCII)
> qui ont revele 3 ecarts chez vulcain (c4 copier-fichier, c6 creer/ecrire,
> c12 editer : rappel ASCII absent ou en position non-1). Un audit partiel
> donne un verdict partiel : la conformite globale n'est prouvee que par le
> re-audit complet des 5 patterns.

### 1. Pattern 1 -- Multi-missions

1. Lancer `guider-parcours.py <parcours.json> --liste` : le parcours se charge
   sans erreur (JSON valide) et inventorie les cases.
2. Verifier que la case `c1` (case_depart) est une case `Mission` de type
   `question` avec au moins 2 branches vers les chemins des missions.
3. Verifier que les chemins CONVERGENT vers des cases communes (lecons,
   fin/reactiver) : les branches des chemins rejoignent les memes cases
   plutot que de dupliquer verdict/lecons/retour dans chaque chemin.

### 2. Pattern 2 -- Rappel ASCII dans les cases d'ecriture

1. Identifier les cases d'ecriture : toute case dont la liste `indices`
   contient un indice `outil` avec un nom d'outil d'ecriture
   (`creer-fichier`, `ecrire-fichier`, `editer-fichier`,
   `ajouter-contenu-fichier`, `inserer-contenu-fichier`, `copier-fichier`)
   ou une action d'ecriture (rapport de controle, lecons).
2. Pour CHAQUE case d'ecriture, verifier que le PREMIER element de la liste
   `indices` est un indice `regle` dont le texte commence par
   `REGLE IMMUABLE ASCII`. Verification structurelle (position 1 = regle
   ASCII) plus fiable qu'une simple recherche de texte : une regle INDEX ou
   une autre regle en position 1 est un ecart.
3. Verifier que la regle INDEX eventuelle reste presente (en position 2 ou
   plus) : la correction ne doit rien supprimer.

### 3. Pattern 3 -- Combo (generateur -> execution)

1. Identifier les cases qui pointent vers un combo (indice outil `combos-moteur`).
2. Verifier que le combo reference existe et que sa spec est documentee.
3. Verifier que la commande de la case reference `combos-moteur.py` avec la
   definition du combo (chemin du fichier definition-combo.json).
4. Verifier la coherence : un combo est un fichier du cerveau (Buffy), le
   moteur est un outil (Vulcain) -- la case ne doit pas invoquer un outil hors
   de son domaine.

### 4. Pattern 4 -- Case Question Honnete en case 0

1. Verifier que `case_depart` vaut `c0` (le parcours demarre par la question
   honnete).
2. Verifier que la case `c0` est une case `question` dont la question porte la
   relecture honnete : contient `memoire` et la formulation "SANS relire".
3. Verifier les branches de `c0` : exactement OUI -> c1, INCERTAIN -> c0b,
   NON -> c0b (pas d'ambiguite de branche).
4. Verifier la case `c0b` (RELIRE OBLIGATOIRE) : type `indice`, titre portant
   `RELIRE`, indices faisant lire `corrections.md` puis la fiche (lire-fichier
   sur corrections.md), `suivant` = c1.
5. Verifier la navigation : OUI -> c1 mission ; NON/INCERTAIN -> c0b -> c1
   (--reponses sur les 3 reponses -> PARCOURS TERMINE).

### 4b. Pattern 5 -- Chaine de delegation ACTIVE

1. Identifier les cases `fin` des parcours dont le message concerne une
   delegation ("activer", "reactiver", "teste", "cree", "spec", "todo").
2. Verifier qu'AUCUNE case `fin` ne porte une formulation passive bloquante :
   grep -i 'te reactive\|j attends\|attend le retour\|x fera\|il me reactive\|tu seras reactive'
   sur les messages des cases `fin` -> 0 resultat attendu (ou formulation
   active de type RELAIS/CLOTURE presente).
3. Verifier que chaque delegation est precedee d'une boucle materialisee dans
   la carte du delegant : apres l'activation, une case RELAIS (lancer le
   parcours de l'agent delegue) puis une case RETOUR (rapport VALIDE ?) puis
   une case CLOTURE (reactiver Cerberus).
4. Verifier que la case `fin` n'apparait qu'apres la CLOTURE : le retour a
   Cerberus est une action, pas une attente.
5. Cas des chaines (ex: athena -> promethee -> minerve) : chaque maillon porte
   la boucle OU son message de fin ordonne explicitement de suivre la chaine
   jusqu'au retour a Cerberus ("RELAIS ACTIF : je ne m'arrete pas en attente").
6. DISTINGUER DELEGATION vs ACTION FINALE : un parcours qui ne delegue pas
   (ex: atlas, clio, janus, themis...) se termine par des fins ACTIVES
   ("Reactiver Cerberus", "Reactiver Vulcain") -- c'est conforme, aucune
   boucle RELAIS/RETOUR/CLOTURE n'est requise. La boucle n'est obligatoire
   QUE pour les parcours qui DELEGUENT (vulcain -> Morpheus, athena ->
   Promethee, promethee -> Minerve). Ne pas declarer un ecart sur un parcours
   sans delegation.

### 4c. RE-AUDIT COMPLET DES 14 PATTERNS (v0.2.25, LECON THEMIS)

1. Apres avoir audite le pattern nouveau ou modifie (4b par exemple),
   REJOUER integralement TOUTES les procedures d'audit dans l'ordre :
   1 (multi-missions), 2 (rappel ASCII position 1), 3 (combos),
   4 (question honnete), 4b (delegation active), 4c (ce re-audit),
   4d (contexte temps reel), 4e (modele compose), 4f (chaine bout-en-bout),
   4g (lire le .md avant usage), 4h (une carte = un role),
   4i (conformite d execution), 4j (creation limitee), 4k (la fin suit SA
   carte) et 4l (verification d impact) sur le MEME parcours.
2. Ne PAS conclure au verdict global tant que les 14 procedures n ont pas ete
   rejouees : un audit qui ne teste que le nouveau pattern ne prouve pas la
   conformite globale (lecon Themis : 3 ecarts ASCII chez vulcain decouverts
   par la procedure 2 rejouee, invisibles a la procedure 4b seule ; lecon
   utilisateur 2026-08-09 : la procedure 4c elle-meme est restee a 12
   patterns pendant que 4i/4k/4l s ajoutaient -- la liste doit etre
   RE-VERIFIEE a chaque ajout de pattern).
3. Verifier en particulier que la procedure 2 (position 1 = `REGLE IMMUABLE
   ASCII`, texte UNIFORME) est rejouee : les cases d'ecriture peuvent porter
   un ancien format ("REGLE IMMUABLE : ASCII strict") qui echappe a une
   simple recherche de texte -- la verification structurelle position 1 est
   obligatoire a CHAQUE audit.
4. Appliquer TOUS les criteres d'acceptation 1 a 25 (criteres 13 fin passive,
   22 conformite d execution, 24 la fin suit SA carte, 25 verification
   d impact) en complement : la conformite d'un parcours = TOUS les
   criteres, pas seulement ceux lies au pattern recent.
5. La procedure 4l (verification d impact) est un pas OBLIGATOIRE du re-audit
   depuis v0.2.24 : lancer detecter-impacts sur un echantillon des fichiers
   modifies (Pattern 14).

### 4d. Pattern 6 -- CONTEXTE TEMPS REEL (v0.2.8)

1. Verifier que la case `c0c` existe dans le parcours (type `indice`, titre
   portant `CONTEXTE`).
2. Verifier le recablage : c0 branche OUI -> c0c (pas c1), c0b `suivant` ->
   c0c, c0c `suivant` -> c1.
3. Verifier que la case `c0c` porte l'outil `lire-activite-recente` (commande
   complete) et un indice fichier AGENTS.md (section `## Sessions connues`).
4. Verifier la navigation : OUI -> c0c -> mission ; NON -> c0b -> c0c ->
   mission (--reponses -> PARCOURS TERMINE).
5. RE-AUDIT COMPLET (regle v0.2.7) : apres l'ajout de c0c, rejouer les
   procedures 1, 2, 3, 4, 4b, 4d, 4e ET 4f dans leur integralite.

### 4e. Pattern 7 -- Modele de case compose (v0.2.13)

1. Identifier les cases `question` et `controle` du parcours (les decisions).
2. Verifier que chaque decision porte AU MINIMUM 2 branches (exception :
   action directe = case `indice` a `suivant`, qui n'est pas une decision).
3. Pour chaque DEVIATION (branche vers un workflow secondaire), verifier que
   le workflow secondaire se termine par un `suivant` de REJOINT vers le
   workflow principal (jamais une case `fin` au milieu, jamais une boucle
   vers la meme case -- regle 10).
4. Verifier la navigation : parcourir chaque chemin avec --reponses ->
   PARCOURS TERMINE (les deviations aboutissent au rejoint, pas a une
   impasse).
5. RE-AUDIT COMPLET (regle v0.2.7) : apres l'ajout de deviations, rejouer
   les procedures 1, 2, 3, 4, 4b, 4d, 4e ET 4f dans leur integralite.

### 4g. Pattern 9 -- LIRE LE .MD AVANT UTILISATION (v0.2.16)

1. Verifier le moteur : `guider-parcours --version` >= v0.3.0 et l'affichage
   d'un indice outil porte la ligne `LIRE AVANT USAGE : <outil.md>`
   (tester sur un parcours reel, ex: vulcain c2 verifier-systeme).
2. Verifier le generateur : `generateurs-case --version` >= v0.2.2 et un
   `--indice-outil` ajoute automatiquement l'indice `fichier` du `.md`
   (LIRE AVANT USAGE, Pattern 9) si la doc existe.
3. Verifier la doc avec L OUTIL (v0.3.0) : lancer
   `verifier-documents-manquants` sur le dossier des outils -- il controle
   que chaque script `.sh` ET `.py` a son `.md` et que chaque `.md` a son
   script. Resultat attendu : **0 document manquant** (les motifs joker
   `tester-protection-*` et les documents de support sont des faux positifs
   ignores par l outil, pas des veritables manquants).
4. RE-AUDIT COMPLET (regle v0.2.7) : apres l'ajout du Pattern 9, rejouer
   les procedures 1, 2, 3, 4, 4b, 4d, 4e, 4f, 4g ET 4h dans leur integralite.

### 4h. Pattern 10 -- UNE CARTE = UN ROLE (v0.2.18)

1. Pour CHAQUE parcours, lister les indices `outil` (guider-parcours
   `--liste` ou lecture du JSON).
2. Verifier que chaque outil appartient au role de l'agent :
   - coordination (activer-agent-principal, lister-agents pour choisir,
     lire-activite-recente pour le contexte) = OK pour un coordinateur ;
   - outils d'ANALYSE du cerveau (lister-outils, detecter-impacts,
     generateurs-carte, generateurs-case hors edition de SES cases) =
     ECART sur une carte qui n'est pas celle de l'agent analyseur.
3. Cas Cerberus : verifier que sa carte est un ROUTEUR PUR -- aucun outil
   d'analyse (lister-outils, generateurs-*), aucun outil de lecture de la
   fiche d'un AUTRE agent (lire-fichier uniquement en c0b sur SES fichiers).
4. Verifier l'INTENTION : une case "lister pour choisir" est de la
   coordination ; une case "lister pour executer" est une derive -- le
   titre et la regle de la case doivent exprimer l'intention de decision.
5. RE-AUDIT COMPLET (regle v0.2.7) : apres la purge d'une carte, rejouer
   les procedures 1, 2, 3, 4, 4b, 4d, 4e, 4f, 4g, 4h ET 4i dans leur integralite.

### 4i. Pattern 11 -- CONFORMITE D EXECUTION (v0.2.19)

1. Pour chaque parcours audite, recueillir les 3 traces : la MISSION recue
   (la demande, ce que l'agent devait faire), la CARTE de l'agent (les
   cases ordonnees : activer X, lancer Y, fin = reactiver/activer Z) et le
   DEROULEMENT REEL (message d'activation/reactivation, fichiers modifies,
   rapports produits).
2. CROISER : comparer les actions reelles aux cases ordonnees -- l'agent
   a-t-il fait ce que sa carte ordonnait ? A-t-il active qui la carte
   designait ? A-t-il lance les outils/cases indiques ? A-t-il termine par
   la fin prevue (reactiver Cerberus, ou activer le maillon suivant de la
   chaine) ?
3. SIGNALER les ECARTS D EXECUTION : une action executee que la carte ne
   ordonnait pas (ex: Vulcain reactive Cerberus au lieu d'activer Morpheus)
   ou une action ordonnee non executee (ex: Cerberus analyse au lieu
   d'activer Buffy) est un ecart MEME SI le JSON est structurellement
   CONFORME -- a inscrire dans le rapport d'audit (Resultats / Synthese).
4. Le critere est compatible avec le Pattern 10 : la procedure 4h verifie
   la STRUCTURE de la carte (les outils autorises), la procedure 4i verifie
   l'EXECUTION de la mission (les actions reelles) -- les deux se
   completent, un audit complet passe les deux.
5. RE-AUDIT COMPLET (regle v0.2.7) : rejouer les procedures 1, 2, 3, 4,
   4b, 4d, 4e, 4f, 4g, 4h ET 4i dans leur integralite.

6. VERIFIER LA REACTIVATION (critere reactiver R1-R5) : l agent audite
   a-t-il reactive Cerberus correctement a la fin de sa mission (3e
   argument `agent_precedent`, sortie `Session ... : Cerberus reactive
   avec succes`, bloc AGENTS.md passe sur Cerberus, profil classeur mis
   a jour) ? Une aide affichee ou un bloc restant sur l agent = ECART
   D EXECUTION a inscrire au rapport (lecon Themis 2026-08-09).


### 4f. Pattern 8 -- Chaine de delegation BOUT-EN-BOUT (v0.2.15)

1. Identifier la chaine : pour chaque parcours qui DELEGUE, verifier la fin
   de chaque maillon : le maillon ACTIVE-t-il le suivant de la chaine (message
   actif "J ACTIVE <suivant>"), ou REACTIVE-t-il Cerberus (dernier maillon) ?
2. Verifier qu'aucun maillon de la chaine ne repasse par Cerberus au milieu :
   pas de "reactiver Cerberus" entre deux maillons d'une meme chaine.
3. Verifier RVAV A CHAQUE MAILLON : chaque fin d'activation est precedee
   d'une case/indice RVAV ("je ne valide JAMAIS sans avoir passe la boucle
   RVAV complete ... AVANT d activer le suivant").
4. Verifier le dernier maillon : REACTIVE Cerberus avec le BILAN CONSOLIDE
   de la chaine (rapports de tous les maillons).
5. Verifier la navigation : chaque chemin de chaque maillon -> PARCOURS
   TERMINE (la fin d'un maillon est bien la derniere case de SON parcours :
   l'activation du suivant se fait par activer-agent-principal, pas par une
   case du parcours courant).
6. RE-AUDIT COMPLET (regle v0.2.7) : apres la migration vers la chaine
   bout-en-bout, rejouer les procedures 1, 2, 3, 4, 4b, 4d, 4e ET 4f dans
   leur integralite.

### 4j. Pattern 12 -- CREATION LIMITEE (v0.2.22)

1. Identifier les cases de creation/documentation : toute case dont la liste
   `indices` contient un outil de creation/ecriture (creer-fichier,
   ecrire-fichier, editer-fichier, ajouter-contenu-fichier) ou dont le titre
   evoque la creation/redaction/documentation.
2. Pour CHAQUE case de creation, verifier qu'elle porte un indice `regle`
   CREATION LIMITEE (en tete des indices) precisant le PERIMETRE (rapports
   de mission dans le dossier de l'agent ou .tmp-* du workspace, JAMAIS
   tools/) et les ROLES EXCLUS (outil -> Vulcain, test -> Morpheus, case de
   parcours -> Buffy).
3. Verifier qu'aucune case ne demande a l'agent de creer un outil, un test
   ou une case de parcours lui-meme ; la case `Signaler le besoin` renvoie
   vers l'agent habilite (Vulcain/Morpheus/Buffy), jamais vers une action de
   creation par l'agent audite.
4. Verifier que la case `Signaler le besoin` ne contient PAS la mention
   "documenter une nouvelle case dans le parcours" (creation de case = role
   de Buffy).

### 4k. Pattern 13 -- LA FIN SUIT SA CARTE (v0.2.23)

1. Pour CHAQUE mission du parcours, identifier la fin attendue par la carte
   (case fin : reactiver Cerberus, ou activer le maillon suivant).
2. Verifier que la fin est COHERENTE avec le type d'activation : activation
   directe par Cerberus -> fin = reactiver Cerberus ; maillon de chaine ->
   fin = activer le suivant selon SA carte ; dernier maillon -> reactiver
   Cerberus avec le bilan consolide.
3. Verifier qu'aucune fin de maillon de chaine ne dit "reactiver Cerberus"
   quand la carte ordonne d'activer le suivant (anomalie qui coupe la chaine
   -- lecon Pattern 11 : Vulcain a reactive Cerberus au lieu d'activer
   Morpheus).
4. Verifier qu'aucun document de coordination (AGENTS.md, index-agents,
   cerberus/corrections, todo-template, protocoles) ne porte l'ancienne regle
   "toujours reactiver Cerberus" (grep : "toujours revenir a Cerberus",
   "derniere action de tout todo est de reactiver Cerberus").

### 4l. Pattern 14 -- VERIFICATION D IMPACT GENERALISEE (v0.2.24)

1. Pour CHAQUE mission auditee, identifier les fichiers modifies (message
   d'activation, bilan de reactivation, git status, rapport de mission).
2. Lancer detecter-impacts sur un ECHANTILLON REPRESENTATIF des fichiers
   modifies (python3 cerveau-projet/agents/tools/detecter/detecter-impacts/
   detecter-impacts.py <fichier-modifie> --racine cerveau-projet).
3. Comparer la liste des fichiers impactes (index-tools, catalogue,
   spec, fiches, parcours, corrections) avec ce qui a ete effectivement
   modifie par l'agent.
4. Tout impact NON mis a jour = NON CONFORME : documenter le fichier
   manquant dans le rapport + l'action de correction requise (lecon
   utilisateur 2026-08-09 : seul le rapport-audit-janus utilisait
   detecter-impacts, la verification doit etre GENERALISEE).
5. Verifier que l'outil a bien ete lu avant usage (.md, Pattern 9).

### 5. Cas particuliers legitimes
| Cas | Pattern | Applicable | Raison |
|---|---|---|---|
| Parcours de ROUTAGE (ex: cerberus) | Pattern 2 | NON | L'agent n'ecrit rien : 0 case d'ecriture, le rappel ASCII ne s'applique pas |
| Prototype historique (ex: vulcain) | Pattern 1 | OUI (fins independantes) | CAS LEGITIME ASSUME : le prototype vulcain garde volontairement des fins INDEPENDANTES par chemin (construire c9, modifier c15, autre c18/c19). Un parcours peut legitimement ne pas converger vers une fin commune : c'est un choix documente, pas un defaut a corriger. Compatible avec la regle 8 AUTONOMIE (chaque parcours est individuel et complet). |

### 6. Autonomie des parcours (regle 8)

1. Verifier que chaque parcours est un fichier INDIVIDUEL dans le dossier de
   SON agent (`agents/<agent>/parcours/parcours-<agent>.json`).
2. Verifier qu'aucun parcours ne reference les cases d'un AUTRE parcours :
   pas de `suivant`/`vers` vers un id de case hors du fichier, pas de fichier
   commun partage.
3. La convergence constatee est uniquement INTRA-parcours (les chemins d'UN
   meme parcours rejoignent SES cases communes).
4. Chaque parcours est complet et validable independamment : `--liste` +
   `--reponses` + ASCII sur SON fichier, sans dependre d'un autre.

### 7. Revalidation complete apres correction

1. `json.load` OK (JSON valide)
2. `--liste` charge sans erreur
3. `--reponses` sur CHAQUE chemin -> PARCOURS TERMINE (navigation inchangee)
4. `valider-conformite-ascii` : 0 caractere non-ASCII sur le parcours
5. Verification structurelle : position 1 des indices des cases d'ecriture
   = regle ASCII (Pattern 2)

## Emplacement des fichiers

| Fichier | Chemin |
|---|---|
| Outil python | `agents/tools/guider/guider-parcours/guider-parcours.py` |
| Outil bash | `agents/tools/guider/guider-parcours/guider-parcours.sh` (parite) |
| Documentation | `agents/tools/guider/guider-parcours/guider-parcours.md` |
| Spec | `agents/tools/guider/guider-parcours/spec/spec-guider-parcours.001.01.ebauche.md` |
| Generateur de cases (reference) | `agents/tools/generateurs/generateurs-case/generateurs-case.py` (py + sh + md) |
| Parcours prototype | `agents/vulcain/parcours/parcours-vulcain.json` |

## Critere d'acceptation

1. Le guide affiche les cases une a une avec indices et branches
2. Une reponse mene a la bonne case (branches testees)
3. Une reponse inconnue affiche une erreur claire (en --reponses : sortie code 1 ; en --interactif : re-demande)
4. Le mode --reponses parcourt le parcours sans interaction
5. Le mode --liste inventorie les cases
6. Un JSON invalide est refuse avec message d'erreur clair
7. Parite py/sh : memes resultats sur le meme parcours
8. ASCII strict : 0 caractere non-ASCII dans les fichiers de l'outil et du parcours
9. Chaque case d'ecriture porte un indice regle ASCII en TETE de ses indices
   (Pattern 2 -- verifier avec `grep 'REGLE IMMUABLE ASCII' <parcours.json>`)
10. Tout parcours multi-missions demarre par une case Mission avec branches et
    chemins convergents vers les cases communes (Pattern 1 -- ex: parcours-janus)
11. Toute case qui pointe vers un combo reference `combos-moteur` + la definition
    du combo (Pattern 3 -- spec-combos-moteur documentee)
12. Tout parcours demarre par la case `c0` (question honnete de relecture) avec
    `c0b` (RELIRE OBLIGATOIRE) et `case_depart` = c0 (Pattern 4)
13. Aucune case `fin` de delegation ne porte de formulation passive bloquante
    ("te reactive", "j'attends", "attend le retour") ; toute delegation est
    materialisee par une boucle RELAIS -> RETOUR -> CLOTURE -> FIN (Pattern 5 --
    verifier avec grep 'te reactive\|j attends' sur les messages des cases fin)
14. RE-AUDIT COMPLET DES 14 PATTERNS : a chaque creation/modification/audit,
    les procedures 1, 2, 3, 4, 4b, 4c, 4d, 4e, 4f, 4g, 4h, 4i, 4j, 4k et 4l
    sont REJOUES integralement (jamais la procedure nouvelle seule) ; le
    verdict global n'est prononce qu'apres le re-audit complet (v0.2.7,
    generalise a 14 patterns en v0.2.25 -- lecon Themis : 3 ecarts ASCII
    vulcain decouverts par la procedure 2 rejouee, invisibles a la 4b seule ;
    lecon 2026-08-09 : la liste des procedures doit etre re-verifiee a
    chaque ajout de pattern)
15. CONTEXTE TEMPS REEL : tout parcours porte la case `c0c` (CONTEXTE
    OBLIGATOIRE) entre c0b et c1 -- c0 OUI -> c0c, c0b -> c0c, c0c -> c1 --
    avec l'outil `lire-activite-recente` et l'indice fichier AGENTS.md
    section `## Sessions connues` ; la lecture de l'historique est obligatoire
    meme en memoire (Pattern 6, v0.2.8 -- decision utilisateur multi-LLM)
16. MODE AGENT NON-BLOQUANT (v0.2.9) : sans --reponses (ou reponses epuisees),
    l'outil affiche `=== QUESTION POUR L'AGENT ===` + les reponses possibles puis
    sort proprement (code 0) -- JAMAIS de `input()` bloquant en mode agent ;
    `--interactif` reserve a l'usage humain
17. OUTIL DE REFERENCE (v0.2.12) : toute creation/edition/suppression de case
    passe par `generateurs-case` (recablage auto des references + validation
    auto json/references/guider-parcours --liste) -- jamais par un editeur naif
18. MODELE DE CASE COMPOSE (v0.2.13) : toute case de decision (`question`/
    `controle`) porte AU MINIMUM 2 branches (sauf action directe `indice` a
    `suivant`) ; chaque deviation (workflow secondaire) se termine par un
    `suivant` de REJOINT vers le workflow principal -- jamais une fin au
    milieu, jamais une boucle d'attente (Pattern 7)
19. CHAINE BOUT-EN-BOUT (v0.2.15) : dans une chaine de delegation multi-
    maillons (outil -> tests -> controle), chaque maillon ACTIVE le suivant A
    SA FIN (message actif, pas de retour a l'expediteur au milieu) ; le
    dernier maillon REACTIVE Cerberus avec le BILAN CONSOLIDE ; chaque maillon
    passe la boucle RVAV sur son travail AVANT d'activer le suivant (Pattern
    8 -- verifier avec grep 'J ACTIVE\|bilan consolide\|RVAV avant activation')
    ; une activation directe par Cerberus reste valide (fin = reactiver
    Cerberus)
20. LIRE LE .MD AVANT UTILISATION (v0.2.16) : guider-parcours >= v0.3.0
    affiche `LIRE AVANT USAGE : <outil.md>` pour chaque indice outil et
    generateurs-case >= v0.2.2 ajoute l'indice fichier .md auto quand un
    --indice-outil est ajoute ; le .md deduit (dossier + nom) existe pour
    chaque outil reference (excepter motifs joker tester-protection-*) ;
    l'agent lit la doc AVANT d'executer (Pattern 9 -- portee systematique)
21. UNE CARTE = UN ROLE (v0.2.18) : les indices outil d'une carte ne
    contiennent QUE des outils du role de l'agent (activation/verification/
    decision propres a SON role), JAMAIS d'outils d'analyse/execution d'un
    autre role (Pattern 10 -- ex: la carte de Cerberus est un routeur pur :
    uniquement activer-agent-principal, lister-agents pour choisir,
    lire-activite-recente pour le contexte, lire-fichier sur SES fichiers en
    c0b ; aucun outil d'analyse comme lister-outils, detecter-impacts,
    generateurs-carte...)
22. CONFORMITE D EXECUTION (v0.2.19) : l'audit Themis ne verifie pas
    seulement la STRUCTURE du JSON (detecter 0 anomalie, valider-cartes
    CONFORME) mais AUSSI si l'EXECUTION de la mission a suivi les ordres de
    la carte : l'agent a-t-il fait ce que sa carte ordonnait ? (Pattern 11
    -- ex: Vulcain a reactive Cerberus au lieu d'activer Morpheus ;
    Cerberus a lance des analyses au lieu d'activer Buffy : dans les 2 cas
    la carte etait structurellement valide mais l'execution a devie --
    constat stabilite des cartes 2026-08-08) -> v0.2.20 (PISTE C : champ catalogue optionnel sur les indices outil - reference a la commande du catalogue generateurs-commande, commande en dur conservee comme fallback ; guider-parcours v0.3.1 affiche catalogue: <nom> + PASSE PAR LE GENERATEUR quand le champ est present, 2026-08-08). La conformite d'execution est
    le SEUL vrai test de stabilite : elle est verifiee par la case c8b du
    parcours-themis (entre le verdict c8 et le rapport c9), le critere est
    croise avec la mission recue, les fichiers modifies et les rapports de
    l'agent audite.
23. CREATION LIMITEE (v0.2.22) : chaque case de creation/documentation
    porte un indice regle CREATION LIMITEE en tete de ses indices
    (perimetre : rapports de mission dans le dossier de l'agent ou
    .tmp-* du workspace, JAMAIS tools/ ; roles exclus : outil ->
    Vulcain, test -> Morpheus, case de parcours -> Buffy ; besoin
    manquant -> Signaler le besoin) (Pattern 12 -- ex: parcours-atlas
    v0.1.3, cases c9/c18/c19/c25)
24. LA FIN SUIT SA CARTE (v0.2.23) : la fin de mission d'un agent suit SA
    carte (Pattern 13) : activation directe par Cerberus -> reactiver
    Cerberus ; maillon de chaine -> activer le suivant selon SA carte ; seul
    le DERNIER maillon reactiver Cerberus avec le bilan consolide. Aucun
    document de coordination ne porte l'ancienne regle "toujours reactiver
    Cerberus" (lecon conflit 2026-08-09 corrige dans 26 fichiers par Buffy).
25. VERIFICATION D IMPACT GENERALISEE (v0.2.24) : pour chaque mission auditee,
    l'agent a-t-il mis a jour TOUS les fichiers impactes par sa mission
    (verifie par detecter-impacts sur un echantillon representatif des fichiers
    modifies) ? Tout impact NON mis a jour (index-tools, catalogue, spec,
    fiches, parcours, corrections) = NON CONFORME (Pattern 14, lecon
    utilisateur 2026-08-09).
