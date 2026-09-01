---
identite:
  type: outil
  nom: Oracle
  version: 0.5.3
  cree: 2026-08-26
  appartient_a: commun
  commun: true
  role: Hub de coordination des agents v1
  session: session-admin
---

# Oracle -- Coordination des agents v1

> Equivalent de JARVIS (v2) pour la session-admin (v1).

## Vue d'ensemble

| Champ | Valeur |
|---|---|
| **Nom** | Oracle |
| **Version** | 0.5.3 |
| **Role** | Hub de communication inter-agents v1 |
| **Session** | session-admin |
| **Responsable** | Buffy (creation), Cerberus (usage) |

## Commandes CLI

```bash
# Envoyer un message
python3 oracle.py envoyer <de> <vers> "<objet>" "<corps>"

# Lire les messages non lus
python3 oracle.py lire <agent>

# Acquitter un message
python3 oracle.py acquitter <agent> <id>

# Lister les messages
python3 oracle.py lister <agent>

# Historiser une action
python3 oracle.py historiser <agent> "<raison>" [--type R|IR]

# Activer un agent
python3 oracle.py activer <agent> "<raison>"

# Afficher les sessions
python3 oracle.py sessions

# Etat d'Oracle
python3 oracle.py status
# Piloter la carte d un agent (maitre d hotel : sert la case + repond aux questions verrouillees)
python3 oracle.py pilote <agent> [--parcours X] [--limite N]

# Piloter la reintegration du maillon precedent (pose FIN:<bilan> puis reactiver)
python3 oracle.py reactiver-fin <agent> <bilan>

# Missions dans les files
python3 oracle.py mission-ajouter <mission> [--file asap, normale, plus-tard]
python3 oracle.py mission-lister [--file X]

# Relais autonome (Oracle agent prend la main : consomme la mission, deduit\
# l'agent, historise son DEBUT a sa place, lui envoie le message, lance le pilote)
python3 oracle.py mission-relais [--file asap, normale, plus-tard, attente]

# Defcon (niveau de menace)
python3 oracle.py defcon
python3 oracle.py defcon-changer <niveau> <commentaire>

# Harnais, relais et dashboard
python3 oracle.py harnais
python3 oracle.py relais
python3 oracle.py dashboard
```

## Architecture

```
cerveau-projet/agents/tools/oracle/
|--- oracle.py          # CLI (commandes)
|--- oracle-server.py   # Serveur MCP (daemon, mode --boucle)
|--- routines-server.py # Daemon resident des routines v1 (manifest + boucle)
|--- routines/          # Manifest + scripts des routines v1
|   |--- manifest.json
|   |--- citations.py
|   +--- data/citations-grecques.json
|--- grades-v1.json     # Grades [GX] + secteurs [XXX] de l encart v1 (ASCII)
|--- oracle-data.json   # Config (liste des agents)
|--- oracle.md          # Ce fichier
|--- inbox/             # Messages recus par agent
|   |--- cerberus.jsonl
|   |--- buffy.jsonl
|   +--- ...
|--- outbox/            # Messages envoyes par agent
|   |--- cerberus.jsonl
|   |--- buffy.jsonl
|   +--- ...
+--- files/             # Files de missions
```

## Integration avec les outils existants

Oracle **delegue** a activer-agent-principal.py pour :
- Les activations/reactivations
- L'ecriture dans AGENTS-historique.md (corps)
- L'ecriture dans AGENTS-activite-recente.md (encart)
- L'ecriture dans historique.db (BDD)

Oracle ajoute :
- Le routing des messages (inbox/outbox)
- La consultation rapide de l'etat des agents
- L'historisation centralisee

## Consommation autonome des missions (mission-relais, decision 2026-08-29)

`mission-relais` permet a ORACLE (l agent, pas seulement le serveur) de
prendre la main avant et apres chaque mission, comme dans le flux
`USER -> Cerberus -> Oracle -> Agent -> Cerberus -> USER` :

1. **Prendre** la premiere mission EN_ATTENTE de la file (defaut `asap`)
   via `files.relais()` (marque PRISE, FIFO).
2. **Determiner l agent cible** : champ `agent` explicite, sinon deduction
   par mots-cles (`files.deduire_agent()` : tests -> morpheus, outil ->
   vulcain, audit -> themis, etc). Depuis 2026-08-30 : un **ETAT URGENT /
   P1 non-acquittes** est deduit vers **oracle** (le coordinateur de la
   coordination) qui declenche le super-combo purge-p1 pour distribuer les
   P1 a chaque destinataire - au lieu du repli vague cerberus.
3. **Historiser le DEBUT de l agent A SA PLACE** (colonne Agent = l agent
   cible, Executeur = Oracle) - Oracle est le SEUL a historiser.
4. **Envoyer le message** a l agent (inbox, priorite 1).
5. **Lancer le pilote** : initialization de l etat de carte (`init_etat`) ->
   le pilote dirige l agent (maitre d hotel).

Cas limites : file vide -> message << Aucune mission >>, code 0. Missing
agent -> repli sur Cerberus si indeducible.

## Role dans le cycle v1

```
Utilisateur -> Oracle -> Agent -> Oracle -> Utilisateur
```

Oracle est le point d'entree unique pour la communication entre agents v1.

## Serveur de demarrage v1 (oracle-demarrage)

> IMPASSE v1 2026-08-27 (meme nature que la v2, mission [AT-1]) : le
> serveur oracle ne tournait jamais (lancement stdio avec stdin DEVNULL =
> EOF immediat) et rien ne demarrait l infrastructure au lancement de
> session. Reponse : `oracle-demarrage` (serveur de demarrage v1,
> equivalent de `jarvis demarrage`/`arret` v2, code 100% v1).

```bash
# Chaine de demarrage v1 (oracle-server --boucle + futur routines v1)
python3 oracle-demarrage.py demarrage --confirme-doc

# Extinction propre
python3 oracle-demarrage.py arret --confirme-doc

# Etat des serveurs v1
python3 oracle-demarrage.py etat --confirme-doc
```

`oracle-server.py` dispose du mode `--boucle` (daemon resident v0.2.0) :
harnais (surveillance) + relais (transmission) toutes les N secondes, log
visible dans `observations/oracle-log.txt`, PID dans `oracle-server.pid`.
La sonde PID Windows passe par OpenProcess (os.kill(pid, 0) TERMINERAIT
le processus - lecon v2 hooks.py).

## Serveur de routines v1 (routines-server)

> Equivalent v1 du routines-server v2 (decision utilisateur 2026-08-27 :
> on s inspire de la v2 mais on ne recupere PAS son code - 2 univers
> distincts). Daemon resident qui tick les routines du manifest en boucle.

```bash
# Lance par oracle-demarrage (demarrage) - detache, survit a la console
python3 routines-server.py --boucle [--intervalle N]   # defaut 30s
```

- Manifest : `routines/manifest.json` (editable sans toucher au code)
- Etat des executions : `routines/etat-executions.json` (persistant)
- PID : `routines-server.pid` ; log : `observations/routines-log.txt`
- Tolerant : une routine en erreur ne tue jamais le daemon (timeout 60s)

### Routine vigie-round (detection des rounds casses)

> Decision utilisateur 2026-08-28 : LES DEUX EN CASCADE - detection
> (routine vigie) + prevention (blocages mecaniques). La vigie est la
> partie DETECTION : elle surveille en continu les rounds casses et
> alerte Cerberus, en LECTURE SEULE.

Toutes les 60 s (manifest.json), `vigie-round.py` verifie :
- SESSION ORPHELINE : agent actif non cerberus sans activite depuis
  X minutes (seuil par defaut 10, reglable `--seuil-minutes`)
- CHAINE EN ATTENTE : etat de carte a `etape=fin` sans reactivation
  de Cerberus (Pattern 13 non execute)

Alerte : inbox Oracle de Cerberus, format 4W (QUI/QUOI/QUAND/OU), avec
anti-spam 30 min. Doc : `routines/vigie-round.md`.

### Routine citations (temporaire)

Repere visuel du fonctionnement des serveurs en arriere-plan : toutes les
5 min, une citation d un dieu grec est historisee dans le tableau
Activites recentes v1 (colonne Grade = `[G5]` = temporaire, Secteur =
`[TRS]`). Univers v1 = dieux grecs (la v2 utilise les heros Marvel).

> TEMPORAIRE (marqueur manifest.json) : `actif: true` en dev,
> **desactivee en production** (`actif: false`) - la routine sera retiree
> en fin de dev (Hygie pourra purger script + entree manifest).

Le script `citations.py` force les chemins AGENTS_* / GRADES_V1 / BDD en
ABSOLU (le daemon le lance avec cwd=routines/, un chemin relatif ecrirait
au mauvais endroit et perdrait l id LLM).

## Pilote Oracle (maitre d hotel de la carte - vision 2026-08-27)

> Vision utilisateur : _Oracle est un maitre d hotel, l agent est un invite
> servi sur un plateau_. Oracle prend le CONTROLE de la carte de l agent
> (parcours.json) : il lit la case courante, repond aux questions
> verrouillees a sa place, sert chaque commande outil a executer, et avance
> seul jusqu a une VRAIE decision libre (verdict, delegation, choix
> d agent). L agent n a plus qu a executer ce qu Oracle lui sert.

```bash
# Activer un agent : Oracle ensemble l etat de carte + pose DEBUT (colonne D/F)
python3 oracle.py activer <agent> "<mission>"

# Servir le plateau suivant de l agent (maitre d hotel)
python3 oracle.py pilote <agent> [--parcours X] [--limite N]

# Pilotage de la reintegration du maillon precedent avec pose du FIN
# (colonne Debut/Fin) : Oracle pose FIN:<bilan> sur l agent qui quitte puis
# re-active le maillon precedent (celui qui l avait active) ou Cerberus
# pour la fin de chaine - le round ne se brise jamais.
python3 oracle.py reactiver-fin <agent> "<bilan>"
```

- **etat-cartes/&lt;agent&gt;.json** : persiste la case courante, le type de
  mission (construire/modifier/tester/audit/...), l etape.
- **repondeur automatique** (`fonctions/pilote.py`) : resout les questions
  verrouillees (confirmation lecture -> OUI, mission -> branche du type,
  probleme outil -> NON, combo -> NON, technologie -> OUI...), laisse les
  vraies decisions libres.
- **serviteur de commande** : extrait les indices [OUTIL]/[FICHIER] de la
  case et les sert a l agent.
- **DEBUT automatique** : `cmd_activer` prefxe l historisation par
  `DEBUT:` (remplit la colonne Debut/Fin du tableau v1) et appelle
  `activer_agent(..., historiser=False)` pour eviter le DOUBLON d entrees.
- **DELEGATIONS pilotees** : quand le parcours atteint une case "AS-TU
  ACTIVE X ?" (delegation de maillon, ex : tests -> Morpheus), Oracle
  active le maillon LUI-MEME via activer-agent-principal et pose son
  `DEBUT:` automatiquement -- le round ne se brise jamais a la main de
  l agent.

## Historique serveur

| Version | Date | Description |
|---|---|---|
| 0.5.6 | 2026-08-30 | CLI `oracle.py historiser` renseigne TOUJOURS la colonne EXECUTEUR de l encart v1 (executeur="Oracle") - mission 4e30f06d suite detection cases EXECUTEUR vides (encart.py v0.3.0). Chaque historique CLI creait auparavant une case EXECUTEUR vide (alimentee uniquement par _historiser_auto / mission-relais). aligne sur le comportement mission-relais (Executeur=Oracle). |
| 0.5.3 | 2026-08-29 | DEFCON-ESCALER (decision utilisateur : URGENT -> DEFCON 4 pour informer Oracle qui avise en fonction de l etat) : nouvelle commande `defcon-escaler <cible 3|4> <commentaire>` + fonction defcon.escaler() - ESCALADE vers le haut (degradation 2->4, no-op si deja au niveau cible ou superieur). Le DEFCON etant une valve a sens unique descendant (5->4->3->2), l etat URGENT devait pouvoir REMONTER vers DEFCON 4 (VALIDATION DES REPARATIONS). Niveau NORMAL corrige : DEFCON 2 = REPRISE TOTALE (protocole 15 v2), et non 3. DEFCON 5 (arret total) reste reserve a defcon-declarer. Consomme par la routine verifier-statuts. |
| 0.5.2 | 2026-08-29 | INCIDENT CORRUPTION HUB RESOLU : le relais (fonctions/relais.py) re-echappait les lignes brutes du hub a chaque tic (_ecrire_jsonl appliquait json.dumps sur un brut deja serialise) -> inbox/cerberus.jsonl a atteint 1 Go de guillemets imbriques en cascade. Fix : un str est ecrit TEL QUEL, un dict serialize une seule fois. Reconstruction du hub (55 messages valides extraits par decodage iteratif, 41 alertes [FANTOMES] spammees purgees, 14 messages legitimes conserves, 1 Go -> 6 Ko). Faux positif SERVEUR MORT corrige (auto-exclusion os.getpid() retirait le daemon lui-meme - 18 alertes [FANTOMES] spammees, fix dans fonctions/controle_processus.py). Garde-fous : test-108 (controle processus), test-109 (relais + audit hub 11 points). Audit complet des inbox/outbox v1 + v2 : aucune autre corruption. |
| 0.5.1 | 2026-08-27 | ROBUSTESSE LECTURE MESSAGES (reparation du round) : tolerance aux lignes inbox/outbox DOUBLE-ENCODEES (string au lieu de dict) dans cmd_status, lecture, acquitter, lister, lire-message, cmd_lire, cmd_nettoyer - isinstance(msg, dict) avant msg.get (bug : AttributeError 'str' object has no attribute 'get' plantait Oracle et arretait le pilotage du round) |
| 0.5.0 | 2026-08-27 | PILOTAGE DE LA REINTEGRATION (maillon precedent + pose FIN) : enregistrement du maillon precedent dans l etat de carte (cmd_activer / _activer_maillon), _fin_auto pose FIN:<bilan> automatiquement (colonne Debut/Fin), commande oracle.py reactiver-fin <agent> <bilan> qui reactive le maillon precedent (activer_agent, reprise) ou Cerberus (reactiver_cerberus, fin de chaine - Pattern 8). Le round ne se brise jamais ni au debut ni a la fin de la chaine. |
| 0.4.0 | 2026-08-27 | PILOTE ORACLE (maitre d hotel, vision utilisateur) : etat de carte par agent (etat-cartes/), repondeur automatique fiable des questions verrouillees, serviteur de commande outil, DEBUT automatique a l activation (colonne Debut/Fin). Modules : fonctions/pilote.py + commande oracle.py pilote + activer_agent(historiser=False) |
| 0.2.1 | 2026-08-27 | Routines v1 : routines-server.py (daemon manifest+boucle) + routine citations (dieu grec, 5 min, temporaire, desactivee en production) + grades-v1.json (grades/secteurs ASCII du tableau v1) |
| 0.2.0 | 2026-08-27 | Mode `--boucle` : daemon resident (harnais + relais), tolerance JSON double-encode inbox, lance par oracle-demarrage |
| 0.1.0 | 2026-08-26 | Creation : serveur MCP stdio/http, routing inbox/outbox, harnais, files, DEFCON |
