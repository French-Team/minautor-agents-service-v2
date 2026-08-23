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
- Pour aller vers un agent specifique → `activer`
- Pour retourner a Cerberus → `reactiver`
- `reactiver` ne va JAMAIS vers un agent autre que Cerberus

---

## PROTOCOLE 3 : Fin de mission (Pattern 8)

Chaque carte a SA fin. La fin dit QUI activer.

| Type de fin | Action |
|---|---|
| **Fin de chaine** | Dernier maillon → `reactiver` Cerberus avec bilan consolide |
| **Fin de branche** | Maillon intermediaire → `activer` le maillon suivant |
| **Fin freelance** | Agent → `activer` Stark (pas reactiver) |
| **Fin Stark** | Stark → `reactiver` Cerberus |

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

## PROTOCOLE 8 : JARVIS — centre nevralgique

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
| **1** | BLOQUANT — l'agent ne demarre pas tant que non lu |
| **2** | Urgent — a traiter en priorite |
| **3** | Normal — traitement standard |
| **4** | Basse — quand possible |
| **5** | Info — simple notification |

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
- PAS de modification des outils v1.

**REGLE** : le template est la SOURCE DE VERITE. Aucune deviation.

---

## PROTOCOLE 10 : Creation d'un outil v2

> Seul un agent grade **gold+** peut creer un outil.
> Forge est le constructeur d'outils (grade silver, medaille constructeur-outils).

| Etape | Action | Qui |
|---|---|
| 1 | Determiner dedie ou commun | Forge |
| 2 | Creer le dossier `<outil>/` avec `entry.py` + `fonctions/` (P1/P2) | Forge |
| 3 | Initialiser RACINE via os_path : `from racine import trouver_racine` (P10) — INTERDIT de compter les niveaux (`../..`) | Forge |
| 4 | Creer `<outil>.md` (template v2, contrat D7) | Forge |
| 5 | Creer `fonctions/` + `<outil>-data.json` (donnees editables, D15) | Forge |
| 6 | Tester l'outil | Forge |
| 7 | Acquitter dans JARVIS | Forge |

**REGLE** : le template est la SOURCE DE VERITE. Aucune deviation.
**REGLE P10** : la detection de racine passe TOUJOURS par
`tools-commun/os_path/` (`trouver_racine(__file__)`).

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

## PROTOCOLE 12 : JARVIS — cycle de vie

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
  → Stark lance JARVIS (jarvis-server.py --transport stdio)
  → Stark utilise JARVIS (messages, activation, status...)
  → Stark dit FIN DE CYCLE
  → Stark arrete JARVIS
  → Stark reactive Cerberus
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
| ALERTE | le serveur, mecaniquement | seuils franchis (manifest.json D15) -> rapport forensique (qui/quoi/comment/quand) -> message P1 [EDITH-RÉVEIL] dans l inbox de stark + demande d activation via JARVIS | a l'evenement ou au delai ecoule |
| ANALYSE | agent EDITH incarnée | lire les observations accumulees, conclure, rapporter a l utilisateur via JARVIS | sur reveil ou a la demande |

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
deposer le message P1 [EDITH-RÉVEIL], et EDITH incarnée doit rapporter
les 4 W a l'utilisateur. Verdict Fury : PASSE si les 4 W sont exacts.
