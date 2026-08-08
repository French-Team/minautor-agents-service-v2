---
identite:
  type: spec
  appartient_a: commun
  commun: true
---
# Spec -- Guide-Parcours (jeu de piste) v0.2.8

**Version** : 0.2.8
**Statut** : ebauche
**Date creation** : 2026-08-07
**Agent** : Vulcain (creation + evolutions v0.2.0 : patterns multi-missions + rappel ASCII ; v0.2.1 : procedure d'audit des 2 patterns ; v0.2.2 : regle d'autonomie des parcours ; v0.2.3 : prototype vulcain documente comme cas legitime assume ; v0.2.4 : Pattern 3 - combo generateur -> execution, lien avec spec-combos-moteur ; v0.2.5 : Pattern 4 - case Question Honnete en case 0, standard de demarrage ; v0.2.6 : Pattern 5 - chaine de delegation ACTIVE, JAMAIS de fin passive ; v0.2.7 : regle de RE-AUDIT COMPLET des 5 patterns (lecon Themis : la procedure 4b seule ne teste que Pattern 5, c est la procedure 2 qui a revele les ecarts ASCII de vulcain) ; v0.2.8 : Pattern 6 - CONTEXTE TEMPS REEL : lecture OBLIGATOIRE de l historique a chaque activation, meme en memoire (le dynamique ne se memorise pas))
**Historique** : v0.1.0 (creation) -> v0.2.0 (documentation des 2 patterns valides en production, 2026-08-07) -> v0.2.1 (documentation de la procedure d'audit des 2 patterns, validee par l'audit des 11 parcours par Themis, 2026-08-08) -> v0.2.2 (regle d'autonomie : chaque parcours est un fichier individuel, convergence uniquement intra-parcours, 2026-08-08) -> v0.2.3 (prototype vulcain : fins independantes documentees comme CAS LEGITIME ASSUME, compatible regle 8, 2026-08-08) -> v0.2.4 (Pattern 3 : une case de parcours peut pointer vers un COMBO - combos-moteur lit definition-combo.json, generateur-commande en mode AUTO, 2026-08-08) -> v0.2.5 (Pattern 4 : case c0 Question Honnete de relecture + c0b RELIRE obligatoire + case_depart = c0, standard de demarrage fige, valide par l'audit Themis 11/11 parcours, 2026-08-08) -> v0.2.6 (Pattern 5 : CHAINE DE DELEGATION ACTIVE - une delegation ne se termine JAMAIS par une fin passive 'X te reactive' : la carte materialise la boucle RELAIS -> RETOUR -> CLOTURE -> FIN. Lecon detecter-impacts v0.2.0 / parcours-vulcain v0.2.1, 2026-08-08) -> v0.2.7 (RE-AUDIT COMPLET DES 5 PATTERNS : a chaque creation/modification/audit, REJOUER les procedures 1, 2, 3, 4 et 4b, jamais seulement la nouvelle procedure. Lecon Themis 2026-08-08 : l audit 4b seul ne testait que Pattern 5, c est la procedure 2 qui a revele 3 ecarts ASCII chez vulcain (c4/c6/c12)) -> v0.2.8 (Pattern 6 : CONTEXTE TEMPS REEL - la question honnete c0 couvre le STATIQUE (fiche + corrections, memorisable) ; l HISTORIQUE est DYNAMIQUE (il change a chaque activation des autres LLM) : sa lecture est OBLIGATOIRE a chaque activation, meme en memoire. Case c0c CONTEXTE entre c0b et c1, traversee par TOUS les chemins. Decision utilisateur 2026-08-08 : chaque agent doit se souvenir des dernieres interventions des autres agents (15 dernieres) et savoir que les autres LLM existent (section Sessions connues), pour eviter les collisions multi-LLM)

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
| `outil` | `nom`, `chemin`, `commande` | L'outil exact a lancer (nom + chemin + exemple de commande) |
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

## CLI de l'outil guider-parcours

```
python3 guider-parcours.py <parcours.json> [options]

Options :
  --case <id>       Demarrer a une case precise (ex: c3) au lieu de case_depart
  --reponses <liste> Fournir les reponses d'un coup (separes par |) : mode non-interactif
  --liste           Lister toutes les cases du parcours sans naviguer
  --version         Afficher la version
  --help            Afficher l'aide
```

### Mode interactif

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
3. Il attend la reponse (choix numerique ou texte exact)
4. Il suit la branche correspondante et affiche la case suivante
5. Cas d'erreur : reponse inconnue -> message clair + re-demande
6. Une case `fin` met fin au parcours avec le message de fin

### Mode --reponses

L'agent fournit toutes les reponses d'un coup (separees par `|`), l'outil
parcourt les cases sans interaction. Une reponse vide a une case avec branches
est une erreur.

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

## Patterns valides en production (v0.2.0, v0.2.4, v0.2.5, v0.2.6, v0.2.8)

Les 6 patterns suivants ont ete valides par les parcours existants et sont
OBLIGATOIRES pour tout nouveau parcours (Pattern 1 et 2 depuis v0.2.0,
Pattern 3 depuis v0.2.4, Pattern 4 depuis v0.2.5, Pattern 5 depuis v0.2.6,
Pattern 6 depuis v0.2.8).

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

**Exemple reel** : `agents/vulcain/parcours/parcours-vulcain.json` v0.2.1
(c8 -> c9a RELAIS -> c9b RETOUR -> c9c CLOTURE -> c9 FIN, et idem c14 -> c15a/c15b/c15c/c15).

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

## Procedure d'audit des 6 patterns (v0.2.1, v0.2.4, v0.2.5, v0.2.6, v0.2.8)

La procedure suivante a ete validee par l'audit de la serie des 11 parcours
realise par Themis (evaluatrice croisee) le 2026-08-08. Elle est a appliquer a
CHAQUE creation, modification ou audit de parcours pour verifier la conformite
aux 6 patterns (le Pattern 3 s'ajoute a la procedure en v0.2.4, le Pattern 4
en v0.2.5, le Pattern 5 en v0.2.6, le Pattern 6 en v0.2.8).

> **REGLE DE RE-AUDIT COMPLET (v0.2.7, LECON THEMIS)** : a chaque
> creation, modification ou audit d'un parcours, REJOUER les procedures
> 1, 2, 3, 4, 4b ET 4d dans leur integralite -- JAMAIS seulement la procedure
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

### 4c. RE-AUDIT COMPLET DES 6 PATTERNS (v0.2.7, LECON THEMIS)

1. Apres avoir audite le pattern nouveau ou modifie (4b par exemple),
   REJOUER integralement les procedures 1 (multi-missions), 2 (rappel ASCII
   position 1), 3 (combos), 4 (question honnete) et 4b (delegation active)
   sur le MEME parcours.
2. Ne PAS conclure au verdict global tant que les 5 procedures n ont pas ete
   rejouees : un audit qui ne teste que le nouveau pattern ne prouve pas la
   conformite globale (lecon Themis : 3 ecarts ASCII chez vulcain decouverts
   par la procedure 2 rejouee, invisibles a la procedure 4b seule).
3. Verifier en particulier que la procedure 2 (position 1 = `REGLE IMMUABLE
   ASCII`, texte UNIFORME) est rejouee : les cases d'ecriture peuvent porter
   un ancien format ("REGLE IMMUABLE : ASCII strict") qui echappe a une
   simple recherche de texte -- la verification structurelle position 1 est
   obligatoire a CHAQUE audit.
4. Appliquer le critere d'acceptation 13 (aucune fin passive) en complement
   des criteres 1 a 12 : la conformite d'un parcours = TOUS les criteres,
   pas seulement ceux lies au pattern recent.

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
   procedures 1, 2, 3, 4, 4b ET 4d dans leur integralite.

### 5. Cas particuliers legitimes

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
| Parcours prototype | `agents/vulcain/parcours/parcours-vulcain.json` |

## Critere d'acceptation

1. Le guide affiche les cases une a une avec indices et branches
2. Une reponse mene a la bonne case (branches testees)
3. Une reponse inconnue affiche une erreur claire et re-demande
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
14. RE-AUDIT COMPLET DES 5 PATTERNS : a chaque creation/modification/audit,
    les procedures 1, 2, 3, 4 et 4b sont REJOUES integralement (jamais la
    procedure nouvelle seule) ; le verdict global n'est prononce qu'apres le
    re-audit complet (v0.2.7 -- lecon Themis : 3 ecarts ASCII vulcain
    decouverts par la procedure 2 rejouee, invisibles a la 4b seule)
15. CONTEXTE TEMPS REEL : tout parcours porte la case `c0c` (CONTEXTE
    OBLIGATOIRE) entre c0b et c1 -- c0 OUI -> c0c, c0b -> c0c, c0c -> c1 --
    avec l'outil `lire-activite-recente` et l'indice fichier AGENTS.md
    section `## Sessions connues` ; la lecture de l'historique est obligatoire
    meme en memoire (Pattern 6, v0.2.8 -- decision utilisateur multi-LLM)
