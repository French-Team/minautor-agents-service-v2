# Spec -- Guide-Parcours (jeu de piste) v0.2.4

**Version** : 0.2.4
**Statut** : ebauche
**Date creation** : 2026-08-07
**Agent** : Vulcain (creation + evolutions v0.2.0 : patterns multi-missions + rappel ASCII ; v0.2.1 : procedure d'audit des 2 patterns ; v0.2.2 : regle d'autonomie des parcours ; v0.2.3 : prototype vulcain documente comme cas legitime assume ; v0.2.4 : Pattern 3 - combo generateur -> execution, lien avec spec-combos-moteur)
**Historique** : v0.1.0 (creation) -> v0.2.0 (documentation des 2 patterns valides en production, 2026-08-07) -> v0.2.1 (documentation de la procedure d'audit des 2 patterns, validee par l'audit des 11 parcours par Themis, 2026-08-08) -> v0.2.2 (regle d'autonomie : chaque parcours est un fichier individuel, convergence uniquement intra-parcours, 2026-08-08) -> v0.2.3 (prototype vulcain : fins independantes documentees comme CAS LEGITIME ASSUME, compatible regle 8, 2026-08-08) -> v0.2.4 (Pattern 3 : une case de parcours peut pointer vers un COMBO - combos-moteur lit definition-combo.json, generateur-commande en mode AUTO, 2026-08-08)

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

## Patterns valides en production (v0.2.0, v0.2.4)

Les 3 patterns suivants ont ete valides par les parcours existants et sont
OBLIGATOIRES pour tout nouveau parcours (Pattern 1 et 2 depuis v0.2.0,
Pattern 3 depuis v0.2.4).

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

## Procedure d'audit des 3 patterns (v0.2.1, v0.2.4)

La procedure suivante a ete validee par l'audit de la serie des 11 parcours
realise par Themis (evaluatrice croisee) le 2026-08-08. Elle est a appliquer a
CHAQUE creation, modification ou audit de parcours pour verifier la conformite
aux 3 patterns (le Pattern 3 s'ajoute a la procedure en v0.2.4).

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

### 4. Cas particuliers legitimes

| Cas | Pattern | Applicable | Raison |
|---|---|---|---|
| Parcours de ROUTAGE (ex: cerberus) | Pattern 2 | NON | L'agent n'ecrit rien : 0 case d'ecriture, le rappel ASCII ne s'applique pas |
| Prototype historique (ex: vulcain) | Pattern 1 | OUI (fins independantes) | CAS LEGITIME ASSUME : le prototype vulcain garde volontairement des fins INDEPENDANTES par chemin (construire c9, modifier c15, autre c18/c19). Un parcours peut legitimement ne pas converger vers une fin commune : c'est un choix documente, pas un defaut a corriger. Compatible avec la regle 8 AUTONOMIE (chaque parcours est individuel et complet). |

### 5. Autonomie des parcours (regle 8)

1. Verifier que chaque parcours est un fichier INDIVIDUEL dans le dossier de
   SON agent (`agents/<agent>/parcours/parcours-<agent>.json`).
2. Verifier qu'aucun parcours ne reference les cases d'un AUTRE parcours :
   pas de `suivant`/`vers` vers un id de case hors du fichier, pas de fichier
   commun partage.
3. La convergence constatee est uniquement INTRA-parcours (les chemins d'UN
   meme parcours rejoignent SES cases communes).
4. Chaque parcours est complet et validable independamment : `--liste` +
   `--reponses` + ASCII sur SON fichier, sans dependre d'un autre.

### 6. Revalidation complete apres correction

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
