---
identite:
  nom: protocoles
  version: 0.2.0
  cree: 2026-08-22
  type: reference
  appartient_a: rogers
  commun: false
  tags: protocoles, cycle, activation, fin-de-mission, freelance, v2
  mot-cles: ["protocoles", "cycle", "activation", "fin-de-mission", "jarvis", "v2"]
  session: freelance
# Protocoles -- Equipe Freelance (v2)
# Source : proposition-v2.md + D3 + D11 + D12 + cycle fondamental

> Rogers veille au respect de ces protocoles.

---

## PROTOCOLE 1 : Cycle fondamental

```
CERBERUS -> AGENT -> CERBERUS
    1         2         3
```

| Etape | Action |
|---|---|
| 1 | Cerberus accueille l'utilisateur |
| 2 | Cerberus analyse et choisit l'agent |
| 3 | Cerberus active l'agent |
| 4 | L'agent execute sa mission |
| 5 | L'agent reactive Cerberus avec le bilan |

**Variante freelance** :
```
Cerberus -> Stark -> [Shuri / Forge / Rogers] -> Stark -> Cerberus
```
- Stark est le coordinateur (pas Cerberus directement)
- Shuri/Forge/Rogers retournent a Stark (activer, pas reactiver)
- Stark reactive Cerberus en dernier (reactiver)

---

## PROTOCOLE 2 : Activation vs Reactivation

| Commande | Usage | Destination |
|---|---|---|
| `activer <session> <agent> <raison>` | Activer un agent specifique | L'agent choisi |
| `reactiver <session> '<bilan>' <agent>` | Retourner au principal de session | Cerberus (toujours) |

**REGLE ABSOLUE** :
- Pour aller vers un agent specifique -> `activer`
- Pour retourner a Cerberus -> `reactiver`
- `reactiver` ne va JAMAIS vers un agent autre que Cerberus

---

## PROTOCOLE 3 : Fin de mission (Pattern 8)

Chaque carte a SA fin. La fin dit QUI activer.

| Type de fin | Action |
|---|---|
| **Fin de chaine** | Dernier maillon -> `reactiver` Cerberus avec bilan consolide |
| **Fin de branche** | Maillon intermediaire -> `activer` le maillon suivant |
| **Fin freelance** | Agent -> `activer` Stark (pas reactiver) |
| **Fin Stark** | Stark -> `reactiver` Cerberus |

---

## PROTOCOLE 4 : Inter-round (D11)

Erreur hors-perimetre detectee pendant un round :

| Etape | Action |
|---|---|
| 1 | L'agent detecte l'erreur |
| 2 | Il active L'AGENT HABILITE avec le rapport |
| 3 | L'habilite corrige |
| 4 | L'habilite reactive l'appelant |
| 5 | L'appelant reprend son round |

**REGLE** : une erreur n'est JAMAIS "seulement detectee". Reparation exclusive par l'habilite.

---

## PROTOCOLE 5 : Mode conversation

Agents en mode conversation (Stark, Shuri, Forge, Rogers) :

| Regle | Detail |
|---|---|
| **Activation** | Cerberus (ou Stark) active l'agent |
| **Execution** | L'agent reste actif, discute, execute |
| **Fin de cycle** | L'utilisateur dit "FIN DE CYCLE" |
| **Retour** | L'agent active Stark (activer, pas reactiver) |
| **Stark** | Stark reactive Cerberus (reactiver) |

---

## PROTOCOLE 6 : Tracabilite R/IR (D12)

| Type | Signification |
|---|---|
| **R** | Round (mission normale) |
| **IR** | Inter-round (erreur hors-perimetre) |

Chaque agent n'edite que les fichiers de SON perimetre.

---

## PROTOCOLE 7 : Separation des sessions

| Session | Agents | Domaine |
|---|---|---|
| **session-admin** | Cerberus, Buffy, Vulcain, Themis... | cerveau-projet v1 |
| **session-freelance** | Stark, Shuri, Forge, Rogers... | freelance v2 |

**REGLE** : les deux sessions ne se croisent JAMAIS.

---

## PROTOCOLE 8 : JARVIS -- centre nevralgique

> JARVIS est le SEUL canal de communication inter-agents.
> Aucun agent ne communique directement vers un autre.
> **RIEN NE PASSE SANS JARVIS.**
> Stark ne fait RIEN sans JARVIS. Chaque demande passe par JARVIS.

| Action | Comment |
|---|---|
| **Envoyer un message** | `jarvis.py envoyer --de <moi> --vers <agent> --priorite <1-5> --objet "..." --corps "..."` |
| **Lire mes messages** | `jarvis.py lire --agent <moi>` |
| **Acquitter un message** | `jarvis.py acquitter --agent <moi> --id <id>` |
| **Voir les bloques** | `jarvis.py bloques` |

| Priorite | Effet |
|---|---|
| **1** | BLOQUANT -- l'agent ne demarre pas tant que non lu |
| **2** | Urgent -- a traiter en priorite |
| **3** | Normal -- traitement standard |
| **4** | Basse -- quand possible |
| **5** | Info -- simple notification |

**REGLE** : un message expire apres avoir ete lu et accuse.

---

## PROTOCOLE 9 : Creation d'un agent v2

> Seul un agent grade **gold+** peut creer un agent.
> Shuri est le constructeur d'agents (grade silver, medaille pionnier-marvel).

| Etape | Action | Qui |
|---|---|---|
| 1 | Verifier le nom (MARVEL, D14) | Shuri |
| 2 | Creer le dossier `freelance/<agent>/` + `parcours/` + `tools/` | Shuri |
| 3 | Creer la fiche `<agent>.md` (template v2, D17) | Shuri |
| 4 | Creer `corrections.md` (template v2) | Shuri |
| 5 | Creer `arbre-<agent>.json` (racine) + `theme-*.json` + `fins.json` | Shuri |
| 6 | Mettre a jour AGENTS.md + proposition-v2.md | Shuri |
| 7 | Valider l'agent (VALIDER de l'arbre) | Shuri |
| 8 | Acquitter dans JARVIS | Shuri |

**INTERDICTION ABSOLUE** :
- PAS d'enregistrement dans activer-agent-principal (seul Stark y est)
- PAS de parcours lineaire (parcours-*.json). Uniquement ARBRE DES DECISIONS.
- PERIMETRE WRITE : n'ecrire QUE dans `cerveau-projet/freelance/`. Tout outil - v1 OU v2 - qui ecrirait hors de ce perimetre est interdit.

**REGLE** : le template est la SOURCE DE VERITE. Aucune deviation.

---

## PROTOCOLE 10 : Creation d'un outil v2

> Seul un agent grade **gold+** peut creer un outil.
> Forge est le constructeur d'outils (grade silver, medaille constructeur-outils).

| Etape | Action | Qui |
|---|---|
| 1 | Determiner dedie ou commun | Forge |
| 2 | Creer le dossier `<outil>/` avec `entry.py` + `fonctions/` (P1/P2) | Forge |
| 3 | Initialiser RACINE via os_path : `from racine import trouver_racine` (P10) -- INTERDIT de compter les niveaux (`../..`) | Forge |
| 4 | Creer `<outil>.md` (template v2, contrat D7) | Forge |
| 5 | Creer `fonctions/` + `<outil>-data.json` (donnees editables, D15) | Forge |
| 6 | **Harnacher l'outil** (PROTOCOLE 21) : importer `verifier_outil` et l'appeler en debut de main() | Forge |
| 7 | Tester l'outil (le harnais le verifie a chaque appel) | Forge |
| 8 | Acquitter dans JARVIS | Forge |

**REGLE** : le template est la SOURCE DE VERITE. Aucune deviation.
**REGLE P10** : la detection de racine passe TOUJOURS par
`tools-commun/os_path/` (`trouver_racine(__file__)`).
**REGLE P21 (2026-08-25)** : AUCUN outil v2 n est livre sans son harnais.
Le mini-test de conformite (import `verifier_outil`) est OBLIGATOIRE a
l etape 6 -- un outil non harnache est refuse (SIG ERR du harnais).

---

## PROTOCOLE 11 : Grades et habilitations

| Action | Grade minimum | Medaille requise |
|---|---|
| Lire/crire dans son perimetre | iron | - |
| Modifier les regles de son domaine | silver | - |
| Creer un outil | gold | constructeur-outils |
| Creer un agent | gold | pionnier-marvel |
| Modifier les protocoles | platinum | zero-defaut |
| Modifier les conventions | platinum | - |
| Acces total | diamond | - (Cerberus seul) |

**REGLE** : le grade est VERIFIE avant chaque action critique. Un agent sans le grade requis est BLOQUE.

---

## PROTOCOLE 12 : JARVIS -- cycle de vie

> JARVIS ne tourne QUE pendant le round de Stark.
> Il demarre a l'activation de Stark et s'eteint a la fin du cycle.

| Moment | Action | Qui |
|---|---|---|
| **Stark active par Cerberus** | Stark lance `jarvis-server.py` (Stdio) | Stark |
| **Pendant le round** | Stark utilise JARVIS pour tout : messages, activation, status | Stark |
| **FIN DE CYCLE** | Stark arrete JARVIS puis reactive Cerberus | Stark |

**REGLE** : JARVIS est un processus FIFO (First In, First Out).
- Demarre en premier dans le round de Stark
- S'eteint en dernier avant le retour a Cerberus

**Lifecycle** :
```
Cerberus active Stark
  -> Stark lance JARVIS (jarvis-server.py --transport stdio)
  -> Stark utilise JARVIS (messages, activation, status...)
  -> Stark dit FIN DE CYCLE
  -> Stark arrete JARVIS
  -> Stark reactive Cerberus
```

## PROTOCOLE 13 v2 : Les 6 declencheurs (2026-08-23)

> Declenchement : l'utilisateur place le prefixe EN TETE de sa demande.
> Stark reconnait, transmet a JARVIS qui applique.

## Table des 6 declencheurs

| Prefixe | Effet sur la mission en cours | La demande |
|---|---|---|
| [attente] | placee en file-attente (statut EN_ATTENTE, ordre normal) - NE PAS LA PERDRE | traitee apres la file |
| [attention] | placee DIRECTEMENT APRES la mission en cours (file-asap, statut SUIVANTE) | executee juste apres |
| [urgent] | PREND LE DESSUS : mission courante placee EN PRIORITE dans la file (statut PRIORITAIRE) | executee immediatement |
| [creer] | - | route vers les protocoles de creation PAR TYPE (agent -> proto 9, outil -> proto 10) |
| [probleme] | - | route vers la resolution de problemes RANGEe PAR TYPE DE FICHIER |
| [question] | - | ouvre une PHASE QUESTION/REPONSE dediee entre l'utilisateur et stark : si stark a besoin d'informations, il envoie a JARVIS qui active les agents concernes pour obtenir la reponse et la lui retourne ; stark repond alors a l'utilisateur. Aucune autre tache pendant la phase |
| [stop] | ROUND BRISE - arret complet du dev : TOUTES les missions gelees (DEFCON5), gravite MAXIMALE. Reprendre exige une decision explicite de l'utilisateur. | protocoles d'urgence absolue |

## Files et priorites

| File | Statuts possibles |
|---|---|
| file-asap.jsonl | SUIVANTE (attention), PREPAREE |
| file-attente.jsonl | PRIORITAIRE (urgent), EN_ATTENTE (attente), DEFCON5 (stop) |

reprendre privilegie l'ordre : PRIORITAIRE > SUIVANTE > EN_ATTENTE.

## Routage [creer]

| Type de creation | Protocole |
|---|---|
| Agent v2 | PROTOCOLE 9 |
| Outil v2 | PROTOCOLE 10 |
| Autre (combo, file, protocole...) | arbitrage Stark via JARVIS |

## Routage [probleme] (par type de fichier)

| Type en cause | Premier habilite |
|---|---|
| jarvis.py / jarvis-server.py / files/ | Vision (exclusif) |
| *.json de donnees d'outils | Forge puis Rogers si regle touchee |
| regles / conventions / protocoles | Rogers |
| fiches / arbres d'agents | Shuri |
| historique / git | Hades (v1) - arbitrage Stark |



> L'utilisateur declare l'etat d'urgence EN TETE de sa demande avec un
> prefixe. Stark reconnait le prefixe et le transmet a JARVIS qui applique
> le protocole. Les prefixes s'appliquent a TOUTE tache, pas seulement JARVIS.

### UR-1 -- [urgent] : interruption + plan d'urgence

| Etape | Action |
|---|---|
| 1 | L'utilisateur ecrit : [urgent] <demande>\ |
| 2 | Stark reconnait le prefixe -> envoie a JARVIS (objet prefixe [urgent]) |
| 3 | JARVIS place la mission EN COURS dans files/file-attente.jsonl : {mission, contexte_avant (etat du systeme, messages utiles), date_mise_en_attente, statut=EN_ATTENTE} |
| 4 | La demande urgente devient PRIORITAIRE : traitee immediatement |
| 5 | Apres l'urgence : reprise de la mission mise de cote (commande reprendre) |

### AT-1 -- [attention] : preparation + file ASAP

| Etape | Action |
|---|---|
| 1 | L'utilisateur ecrit : [attention] <demande>\ |
| 2 | Stark transmet a JARVIS avec le prefixe |
| 3 | JARVIS PREPARE la demande (analyse, decoupage) et la place dans files/file-asap.jsonl (statut=PREPAREE) |
| 4 | Execution DES QUE POSSIBLE : des que aucun P1/P2 n'est en cours |

### Files d'attente (D15)

| File | Role |
|---|---|
| files/file-attente.jsonl | missions mises de cote par UR-1 (contexte de reprise) |
| files/file-asap.jsonl | demandes AT-1 preparees, en attente de creneau |

Chaque entree capture l'etat AVANT mission (reprise) et sert d'historique
APRES (statut, resultat).

## PROTOCOLE 14 : Architecture JARVIS -- anti-indigestion (2026-08-23)

> Constat : jarvis.py concentre communication + activations + historique +
> files d'attente + urgence. Sans regle de structure, il devient impossible
> a maintenir.

### Regle 1 -- .bak AVANT tout refactoring

Avant TOUTE modification structurelle de jarvis.py ou jarvis-server.py,
Vision cree une copie horodatee :
    jarvis.py.bak-AAAAMMJJ-HHmm
La sauvegarde n'est supprimee qu'apres validation des tests du nouveau code.

### Regle 2 -- structure obligatoire (meme P1/P2 que les outils)

| Composant | Contenu |
|---|---|
| jarvis.py | point d'entree : parsing CLI + dispatch UNIQUEMENT |
| fonctions/ | une tache par module : messages.py, activations.py, files.py, historique.py, urgence.py |
| jarvis-server.py | serveur MCP : outils declaratifs qui appellent les MEMES fonctions/ |
| jarvis-data.json | donnees D15 |

### Regle 3 -- decoupage progressif

Le refactoring se fait PAR MODULE, un a la fois : chaque module extrait
est teste (comportement inchange) avant d'extraire le suivant.
Ordre propose : files -> historique -> messages -> activations -> urgence.

### Regle 4 -- taille maximale

Un fichier de plus de ~400 lignes doit justifier sa taille ou etre
decoupe. Un module fonctions/ ne fait qu'UNE tache.

## PROTOCOLE 15 : L'echelle DEFCON et le serveur dedie (2026-08-23)

### L'echelle de reprise apres [stop]

| Niveau | Signification | Ce qui est permis |
|---|---|---|
| DEFCON 5 | ARRET TOTAL (declenche par [stop]) | RIEN - tout est gele |
| DEFCON 4 | reparations faites | reprise UNIQUEMENT pour verifier, tester, valider les reparations |
| DEFCON 3 | reparations validees | reprise possible, SOUS SURVEILLANCE du probleme qui a provoque le DEFCON 5 |
| DEFCON 2 | delai de surveillance passe | TOUT peut reprendre normalement |

Transitions : 5 -> 4 quand les reparations sont faites ; 4 -> 3 quand
elles sont validees par un test reel (Fury) ; 3 -> 2 apres le delai de
surveillance. Chaque transition est journalisee et decidee par Stark
avec accord utilisateur.

### Le serveur DEFCON dedie

Un server MCP SEPARATE (tools-commun/defcon/) gere l'etat DEFCON :
- demarre par jarvis (server) a l'entree en DEFCON 5
- stoppe par jarvis (server) a la fin du cycle DEFCON (retour DEFCON 2)
- objectif : ne pas surcharger jarvis-server, isoler la gestion d'urgence

## PROTOCOLE 16 : EDITH -- la cellule dormante (2026-08-23)

> EDITH = agent observateur qui DORT. Son serveur de routines vit H24
> sans LLM : il collecte, surveille et - seul - decide de TIRER L'ALARME.
> Stark ouvre la porte de la cellule : l'incarnation passe toujours par
> la chaine stark -> jarvis -> edith (M1/M2).

### Les 3 couches

| Couche | Qui | Role | Cycle |
|---|---|---|---|
| COLLECTE | mini serveur routines (H24, lecture seule) | executer les routines du manifest.json : demarrage/arret jarvis, observation des flux, detection de modifications | continu, sans LLM |
| ALERTE | le serveur, mecaniquement | seuils franchis (manifest.json D15) -> rapport forensique (qui/quoi/comment/quand) -> message P1 [EDITH-REVEIL] dans l inbox de stark + demande d activation via JARVIS | a l'evenement ou au delai ecoule |
| ANALYSE | agent EDITH incarnee | lire les observations accumulees, conclure, rapporter a l utilisateur via JARVIS | sur reveil ou a la demande |

### Regles

1. LE SERVEUR NE MODIFIE RIEN : lecture seule sur le projet, ecriture
   uniquement de ses observations et rapports.
2. LE SERVEUR N'ACTIVE JAMAIS UN AGENT LUI-MEME : il sonne (message),
   Stark ouvre la cellule (M1/M2 preserves).
3. PERIMETRES DISTINCTS : Fury teste les rounds ; Argus detecte les
   contradictions (v1) ; EDITH observe les flux vivants et les processus.
4. MANIFEST D15 : quelles routines tournent quand, quels seuils d'alerte -
   editable sans toucher au code.

### Cas de validation obligatoire

Modifier un fichier du perimetre EDITH en reel -> le serveur doit
detecter, constituer le rapport forensique (qui/quoi/comment/quand),
deposer le message P1 [EDITH-REVEIL], et EDITH incarnee doit rapporter
les 4 W a l'utilisateur. Verdict Fury : PASSE si les 4 W sont exacts.

## PROTOCOLE 17 : Evaluation periodique des agents (2026-08-23)

> Une routine (toutes les 10 min, ajustable dans routines/manifest.json)
> reveille EDITH pour lancer un cycle d'evaluation des agents.

### Le cycle

| Etape | Qui | Action |
|---|---|---|
| 1 | routine (serveur) | reveil periodique d'EDITH |
| 2 | EDITH | pose le QUESTIONNAIRE STANDARD pour chaque agent actif |
| 3 | EDITH | attribue +/- selon les reponses et les observations collectees |
| 4 | EDITH -> JARVIS | rapport final : liste des changements proposes |
| 5 | JARVIS -> Forge | application via rating-agents v0.2.0 (penalite/felicite) |

### Questionnaire standard (par agent evalue)

| Question | Points si oui |
|---|---|
| A-t-il livre ce qui etait attendu depuis la derniere evaluation ? | +1 |
| Ses bilans etaient-ils traces (ID d'activation reference) ? | +1 |
| Une violation de perimetre ou de regle lui est-elle imputable ? | -1 par violation |
| Un test reel a-t-il echoue sur son travail ? | -1 |

### Tableau des scores

Commande : python3 tools-commun/rating-agents/entry.py lister
Affiche tous les scores /100 en un coup.

### Seuil de revision

Un agent sous **40/100** declenche une REVISION obligatoire :
education (Chiron) ou mission de reparation selon la gravite.

### Fichier de suivi par agent

fiche <agent>.md section SUIVI DE SCORE (ou notes-agents.jsonl filtre) :
chaque evenement avec date, motif, delta. Si revision requise, on sait
POURQUOI : la liste complete des penalites est l'ordre du jour de la
revision.

## PROTOCOLE 18 : Bibliotheque commune + detection post-modification (2026-08-23)

> Le pattern os_path se generalise : chaque douleur subie DEUX FOIS devient
> (1) un outil commun (P1/P10/D15) et (2) une routine de detection qui
> signale sa reaparition apres chaque modification de fichier.

### La bibliotheque commune (tools-commun/)

| Module | Douleur payee | Ce qu'il normalise |
|---|---|---|
| os_path | 5 bugs de niveaux comptes | detection de racine, resolution, localisation |
| encodage | mojibake console, coding ascii vs utf-8 | D4 mecanique : lire/ecrire/detecter |
| exec | quoting PowerShell rate, timeouts oublies | subprocess standardise : rc + captures + timeout |
| jsonl-store | lire/ecrire/append dupliques x4 | UNE implementation JSONL testee |
| horloge | horodatages heterogenes | formats uniques tracables |

### La routine valider-apres-modification

Declenchee par le serveur de routines JUSTE APRES chaque modification
detectee. Heuristiques PRUDENTES : signaler, ne jamais bloquer.

| Verification | Regle violee si positif |
|---|---|
| | Niveaux comptes ("../.." repetes) hors bootstrap P10 | M7/P10 | |
| Header coding absent/incoherent avec le contenu | D4 |
| Caracteres interdits dans les JSON de parcours (accents) | ASCII strict |
| Valeurs en dur suspectes (session-llm-N litteral, listes figees) | P4/M5 |

### Le traitement des alertes

Detection -> message [EDITH] a stark -> JARVIS prepare un INTER-ROUND
PARALLEL pour l'agent habilite : la reparation se fait SANS casser le
round principal en cours. Les collisions de fichiers restent regies par
la regle serie/parallel.

## PROTOCOLE 19 : Canal utilisateur -> jarvis (2026-08-23)

> Un fichier USER-DEMANDES.md (a cote de AGENTS.md) permet a
> l'utilisateur de s'adresser DIRECTEMENT a jarvis, sans passer par stark.

### Le fichier

Pre-rempli avec UNE SECTION par declencheur. L'utilisateur ecrit sous la
section choisie. Detection : empreinte SHA-256 PAR SECTION par le serveur
de routines (intervalle court), changement -> message prioritaire dans
inbox/jarvis.jsonl : objet [USER][<prefixe>].

### L'autonomie de jarvis (sans stark)

| Section | jarvis fait seul |
|---|---|
| [question] | repond avec SES combos |
| [attente] / [attention] / [urgent] | gere les files et distribue aux agents (seul habilite a activer - M2 preserve) |
| [creer] / [probleme] | route vers protocoles/agents habilites |
| [stop] | DEFCON 5 immediat |

**MARBLE PRESERVE** : jarvis EXECUTE les demandes ; il ne modifie jamais
les regles du marbre sans accord utilisateur ou accord exclusif de stark.

### Limite honnete (V1-V4)

Le serveur depose le message ; le traitement se fait quand la session
incarne jarvis (pas un daemon temps reel).

## PROTOCOLE 20 : Le rappel anti-dispersion (2026-08-23)

> Quand un agent applique une correction quelque part, le meme probleme
> existe probablement AILLEURS. L'oubli de ces soeurs est recurrent et
> devient systematique s il n est pas contre mecaniquement.

### La regle

TOUT agent qui applique une correction consulte :
    python3 tools-commun/rappel/entry.py pour --contexte <contexte>
et SIGNALE dans sa reponse les pistes verifiees ou a verifier.

### Contextes de rappel (D15 : tools-commun/rappel/rappels.json)

| Contexte | Rappel type |
|---|---|
| correction-regle | autres corrections.md, regles-immuables, conventions, protocoles, templates |
| correction-outil | parite .sh/.py, serveur MCP equivalent, tests, index |
| correction-fiche | arbre/themes, corrections.md, AGENTS.md, jarvis-data.json |
| correction-jarvis | serveur miroir, routines liees, contrat .md |
| nouveau-fichier | nommage date + declaration dans les index |
| correction-template | protocole de creation + agents construits avec l ancienne version |

Ajouter un rappel = editer rappels.json (D15), jamais le code.

### Obligation dans la reponse

L agent mentionne EXPLICITEMENT dans sa reponse finale les pistes
verifiees ou restantes. Un bilan qui ne mentionne pas la dispersion
verifiee est incomplet.

---

## PROTOCOLE 21 : Harnais generalise aux outils v2 (2026-08-25)

> Decision utilisateur 2026-08-25 : plus rien n est fait par un agent v2
> SANS le harnais correspondant. Chaque outil v2 contient l import d un
> MINI-TEST DE CONFORMITE avec plusieurs messages selon la situation
> (erreur detectee, etc.). Les scripts temporaires sont proteges par
> leur harnais.

### La regle absolue

TOUT outil v2 importe et appelle le harnais en debut de traitement :

```python
from harnais import verifier_outil   # outils
from harnais import verifier_script  # scripts temporaires
```

| Situation | Signal | Action de l agent |
|---|---|---|
| Tout est conforme | `SIG OK` | Continuer |
| Anomalie mineure | `SIG WARN` | Continuer + signaler |
| Erreur detectee | `SIG ERR` | STOPPER + corriger avant de continuer |
| Probleme critique | `SIG CRIT` | Arret immediat + restauration |

### Ce que le mini-test verifie (conformite d un outil v2)

1. Structure obligatoire : `entry.py` + `fonctions/` + `<outil>.md`.
2. Syntaxe Python valide (compile de tous les .py).
3. Detection racine P10 (`trouver_racine`) presente dans entry.py.
4. L outil est harnache (appel verifier_outil present).

### Scripts temporaires (REGLE D ORIGINE v1)

> Comme dans la v1 (decision utilisateur 2026-08-25) : chaque agent cree
> SON dossier temporaire a la RACINE du workspace, `tmp-<agent>/`
> (ex: tmp-stark/, tmp-vision/). Jamais le /tmp systeme.

| Regle | Detail |
|---|---|
| **Dossier dedie a l agent** | Script temporaire dans `tmp-<agent>/` a la RACINE du workspace |
| **Jamais ailleurs** | /tmp systeme, racine, ou dossier d outil = SIG ERR (bloque) |
| **Isolation** | Aucun chemin absolu suspect : le script ne touche QUE son dossier |
| **Lifecycle** | Creer -> executer -> verifier -> SUPPRIMER (`rm -rf tmp-<agent>` en fin de mission) |
| **Sans harnais** | Un script hors harnais = SIG ERR (bloque) |

### Implementation

- Module : `tools-commun/harnais/` (fonctions/harnais.py + entry.py + harnais.md).
- Exemple : `freelance/classeur/entry.py` appelle `verifier_outil()` en debut de main().
- Le harnais est INTUITIF : chaque message dit quoi faire ensuite. L agent
  n a jamais a reflechir pour savoir comment reagir a un signal.

### Transparence (l agent n a PAS a reflechir)

| Capacite | Detail |
|---|---|
| **PYTHONPATH injecte** | `harnais exec` injecte les chemins v2 (os_path, bdd-lecons, harnais) avant de lancer : le script temporaire ecrit `from racine import trouver_racine` SANS sys.path manuel |
| **Lecons diffusees** | avant chaque execution, le harnais affiche les lecons recentes de l agent depuis la BDD v2 (D10) : `=== LECONS APPRISES (BDD v2) ===` |
| **Compensation** | le harnais DETECTE et guide les erreurs de l agent (ex: tmp-<agent> oublie) au lieu de le laisser echouer seul |

### BDD des lecons v2 (D10, construite 2026-08-25)

> La bible des lecons v2 : `tools-commun/bdd-lecons/` (SQLite, modele du
> classeur v2 : rapide). Les agents n ecrivent PLUS leurs lecons dans
> corrections.md : ils les ENREGISTRENT via l outil, le harnais les
> DIFFUSE au moment du besoin (rappel des lecons apprises).

```
bdd-lecons enregistrer "<ce que j ai appris>" --agent <moi> [--categorie C] [--mots-cles a,b]
bdd-lecons lister [--n 20]         # apercu recent (bible)
bdd-lecons chercher [--mot-cle M] [--categorie C] [--agent A]
```

Format d une lecon : `{id, date, agent, categorie(outil|protocole|processus|carte|correction|technique|autre), titre(auto), resume, mots_cles[], source}`.

### Architecture DYNAMIQUE (v0.2.0, decision utilisateur 2026-08-25)

> " On importe le harnais, le harnais fait le reste. " Le harnais des
> scripts temporaires est pilote par la CONFIGURATION (`harnais-data.json`,
> D15 : separation code/donnees), jamais par des editions de code.
> Ajouter une regle = editer UN fichier de donnees, rien d autre.

Le harnais lit la config a CHAQUE appel et applique 4 categories :

| Categorie | Contenu (config) | Exemple |
|---|---|---|
| **Securites** | `securites[]` : fonctionnement du script | zone tmp-<agent>/ dediee, isolation (pas de chemins absolus) |
| **Verifications** | `verifications[]` : agent, raison, ... | agent obligatoire, raison obligatoire (bloquantes) |
| **Imports obligatoires** | `imports_obligatoires[]` | trouver_racine (P10) present dans le script |
| **Rappels** | `rappels[]` : utilisation, commande | lifecycle, promotion vers outil durable, entonnoir |

**REGLE (anti-edition) :** pour ajouter un import obligatoire, une
verification, un rappel ou une securite, on EDITE `harnais-data.json`
-- JAMAIS le code du harnais, JAMAIS les scripts. Le harnais fait le
reste automatiquement (preuve : un import ajoute a la config est verifie
des l appel suivant, sans toucher au code).

**Niveaux (reponse a la question " regle, convention ou protocole ? ") :**

| Niveau | Ou ca vit | Role |
|---|---|---|
| Protocole | PROTOCOLE 21 (ce fichier) | La REGLE d usage : chaque script/outil passe par le harnais |
| Convention | D15 (separation code/donnees) | L ARCHITECTURE : config, jamais de valeurs en dur dans le code |
| Donnees | `harnais-data.json` | Le CONTENU dynamique : imports, verifications, rappels, securites |
| Code | `fonctions/harnais.py` | Le MOTEUR : lit la config, applique tout (stable, ne change presque jamais) |

### Execution protegee d un script temporaire (AVANT -> PENDANT -> APRES)

L agent appelle UNE commande (`harnais exec tmp-<agent>/script.py --agent X
--raison "..."`) ; le harnais fait tout le reste, transparent pour l agent :

| Phase | Ce que le harnais fait |
|---|---|
| **AVANT** | verifications (agent, raison) ; securites (zone tmp-<agent>/, isolation) ; imports obligatoires (trouver_racine...) ; syntaxe Python (compile) ; backup empreinte + etat de la zone ; journalisation |
| **PENDANT** | execution via subprocess ; timeout ; capture stdout/stderr (rien n est perdu) |
| **APRES** | verdict rc ; detection d effets (fichiers crees hors zone, script modifie) ; rappels (lifecycle, promotion, entonnoir) ; journalisation finale |

**REGLE :** tout ce qui peut etre verifie/decide automatiquement est fait
par le harnais. L agent ne reflechit pas (PROTOCOLE 22) : il execute la
commande, le harnais valide et rend un verdict clair.

---

## PROTOCOLE 22 : Anti-reflexion -- commande + pourquoi (2026-08-25)

> Decision utilisateur 2026-08-25 : " l intelligence ne rend pas docile ".
> Quand un agent ne comprend pas le POURQUOI, il reflechit et cherche a
> savoir avant d agir -> ce sont des TROUS DANS LA RAQUETTE. La v2 doit
> les eviter : chaque parcours/arbre donne la commande a executer ET le
> pourquoi, pour que l agent execute quand il comprend ce qu il fait.

### La regle d or des parcours v2

Chaque case/etape d un arbre ou parcours v2 suit le format :

```
SI tu dois faire <ceci>
  -> EXECUTE <commande exacte>
  // POURQUOI : <une phrase qui explique le but>
```

| Element | Obligation |
|---|---|
| **Commande exacte** | La commande a copier-coller est donnee, jamais devinee |
| **Pourquoi** | Une phrase courte explique le BUT (l agent n a pas a chercher) |
| **Pas de choix ouvert** | Si plusieurs options, le parcours DECIDE (jamais " choisis toi-meme ") |
| **Pas de recherche** | L agent n a JAMAIS a chercher le pourquoi du comment : il est dans le parcours |

### Le flux ideal (JARVIS + arbre)

```
JARVIS donne la mission a un agent
    |
    v
L ARBRE DE DECISION prend le relais (theme-*.json / fins.json)
    |
    v
L agent EXECUTE quand il comprend ce qu il fait (commande + pourquoi)
    |
    v
Des qu il ne comprend PAS -> il cherche a savoir (TROU DANS LA RAQUETTE)
    -> le parcours doit l avoir PREVENU (le pourquoi est deja la)
```

### Ce qui est INTERDIT dans un parcours v2

| Interdit | Pourquoi |
|---|---|
| " Choisis la bonne commande " | Oblige l agent a reflechir au lieu d executer |
| " Utilise l outil X " sans commande | L agent doit deviner les arguments |
| Une regle sans raison | L agent cherche le pourquoi et s arrete |
| Renvoyer vers un doc " a lire " | L agent lit au lieu d agir (sauf si necessaire, le parcours le dit) |

### Obligation a la creation d un arbre/parcours

TOUT agent qui cree ou modifie un arbre/parcours v2 verifie que chaque
case action a : (1) une commande EXACTE copiable, (2) un " pourquoi "
clair. Un arbre avec une case " fais ce qu il faut " est NON CONFORME.

### Role de JARVIS

JARVIS est un element essentiel : il donne la mission (le QUOI), puis
l arbre prend le relais (le COMMENT + le POURQUOI). JARVIS ne donne
jamais une mission sans que l arbre du destinataire ait la commande et
le pourquoi correspondants.
