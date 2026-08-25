---
identite:
  type: rapport
  appartient_a: atlas
  date: 2026-08-24
  statut: definitif
  categorie: exploration
---

# DOSSIER COMPLET -- cerveau-projet/freelance/

> Document d'exploration factuel a destination des CONCEPTEURS v1.
> NON NORMATIF : il n'autorise et n'interdit rien aux agents.
> Les regles applicables restent les cartes, fiches, corrections et
> regles-immuables de chaque agent.
>
> Agent : Atlas (exploration) -- Date : 2026-08-24
> Perimetre explore : cerveau-projet/freelance/ (163 fichiers, 42 dossiers)
>
> METHODE RIGOUREUSE (decision utilisateur 2026-08-24) : UN DOSSIER A LA
> FOIS, UN .md PAR DOSSIER. Ce rapport complet est le DOUBLON DE LA
> STRUCTURE : il reproduit l'arborescence de freelance/ et CHAQUE dossier
> pointe vers SON .md dedie dans ce dossier (le detail de chaque
> fichier vit dans le .md du dossier).

---

## SOMMAIRE

1. Vue d'ensemble (ce qu'est ce dossier)
2. DOUBLON DE LA STRUCTURE : arborescence complete avec liens vers les .md par dossier
3. Synthese : cartographie lisible
4. Etat actuel : fonctionnel / en construction / residus

---

## 1. VUE D'ENSEMBLE

`cerveau-projet/freelance/` est le dossier de la **v2** du cerveau-projet :
l'equipe d'agents "freelance" (theme MARVEL, decision D14) qui developpe la
v2 dans un perimetre isole de la v1 (`cerveau-projet/agents/`).

Principes fondateurs du dossier (issus de proposition-v2.md) :
- **D1** : arbre des decisions (remplace la carte lineaire v1)
- **D4** : standard UTF-8 + CRLF + emojis (UNIQUEMENT dans ce dossier ; la v1 garde ASCII + LF)
- **D16** : JARVIS, hub de communication obligatoire -- "RIEN NE PASSE SANS JARVIS"
- **D15** : separation code/donnees (zero valeur en dur, fichiers -data.json)
- **D14** : nommage MARVEL des agents
- **Autonomie v2** : AUCUN outil v1 utilise par les agents freelance

Les 9 agents : Stark, Shuri, Forge, Rogers, Parker, JARVIS, Vision, EDITH, Fury.
Redacteur-v2 (agent v1) n'a PAS de dossier dans freelance/ (il ecrit des docs
freelance mais reste un agent du cerveau v1).

---

## 2. DOUBLON DE LA STRUCTURE -- arborescence avec .md par dossier

```
cerveau-projet/freelance/
|
|--- (RACINE)                                          -> dossier-racine-freelance-2026-08-24.md
|   |--- proposition-v2.md          <- CONCEPTION CENTRALE : decisions D1-D18, principes P1-P9
|   |--- bilan-v1-pour-v2-2026-08-22.md <- Bilan v1 (Themis) : ce qu on garde / laisse
|   |--- mode-demploi-declencheurs-2026-08-23.md <- Les 6 declencheurs [attente]...[stop]
|   +--- freelance-historique.md    <- VIDE (emplacement prevu, D9)
|
|--- conventions/
|   +--- conventions.md             -> dossier-conventions-2026-08-24.md
|                                  (formats, nommage, templates, interdictions v2)
|
|--- docs/
|   +--- mcp-reference.md           -> dossier-docs-2026-08-24.md
|                                  (documentation MCP, base de l architecture)
|
|--- protocoles/
|   |--- protocoles.md              -> dossier-protocoles-2026-08-24.md
|   +--- protocoles-mcp.md          (20 protocoles + architecture MCP de JARVIS)
|
|--- regles/
|   |--- regles-immuables.md        -> dossier-regles-2026-08-24.md
|   +--- philosophie/               (M1-M7, V1-V4, P1-P10, D1-D18, grades, medailles
|                                  + philosophie-regles/missions/creation)
|
|--- routines/
|   |--- README.md                  -> dossier-routines-2026-08-24.md
|   |--- manifest.json              (systeme de surveillance d EDITH, D15)
|   |--- etat-executions.json
|   +--- surveillance/              (detection, evaluer-agents, surveiller-flux-jarvis,
|                                   surveiller-modifications)
|
|--- templates/
|   |--- README.md                  -> dossier-templates-2026-08-24.md
|   +--- template-*.md/.json/.py    (agent, corrections, arbre, theme, fins, outil)
|
|--- tools-commun/                  -> dossier-tools-commun-2026-08-24.md
|   |--- README.md                  (outils partages, Forge responsable)
|   |--- os_path/                   (racine detectee, P10)
|   |--- encodage/ exec/ horloge/ jsonl-store/  (bibliotheque commune, proto 18)
|   |--- rappel/                    (anti-dispersion, proto 20)
|   |--- rating-agents/             (notation des agents, proto 17)
|   |--- defcon/                    (serveur DEFCON, proto 15)
|   |--- securite/                  (lecteur-de-carte + verrou-outils)
|   |--- jarvis/                    (LE HUB : jarvis.py + server MCP + inbox/outbox
|   |                                + files + fonctions/ + serveur/ + combos/)
|   |--- routines-server/           (serveur EDITH H24 + observations/)
|   +--- routines-server.bak-20260823-1700/  (ARCHIVE, a nettoyer)
|
|--- stark/                         -> dossier-stark-2026-08-24.md
|   +--- (fiche, corrections, parcours : JARVIS/LIRE/EXPLORER + fins)
|
|--- shuri/                         -> dossier-shuri-2026-08-24.md
|   +--- (fiche, corrections, parcours : CREER/COORDONNER/EXPLORER/LIRE/VALIDER)
|
|--- forge/                         -> dossier-forge-2026-08-24.md
|   +--- (fiche, corrections, parcours : CREER/COORDONNER/EXPLORER/LIRE/VALIDER)
|
|--- rogers/                        -> dossier-rogers-2026-08-24.md
|   +--- (fiche, corrections, parcours : COORDONNER/EXPLORER/LIRE/MODIFIER/VALIDER)
|
|--- parker/                        -> dossier-parker-2026-08-24.md
|   +--- (fiche, corrections, parcours : COORDONNER/DIAGNOSTIQUER/EXPLORER/LIRE)
|
|--- jarvis/ (agent)                -> dossier-jarvis-agent-2026-08-24.md
|   +--- (fiche, corrections, parcours : COORDONNER/DISTRIBUER/REPONDRE/SUIVRE/TRAITER)
|
|--- vision/                        -> dossier-vision-2026-08-24.md
|   +--- (fiche, corrections, parcours : EXPLORER/MODIFIER/TRAITER)
|
|--- edith/                         -> dossier-edith-2026-08-24.md
|   |--- (fiche dormante, corrections, parcours : LIRE/OBSERVER/RAPPORTER)
|   +--- rapports/ (suivi-stark, suivi-vision : scores EDITH)
|
+--- fury/                          -> dossier-fury-2026-08-24.md
    |--- (fiche hors-round, corrections, parcours : LIRE/RAPPORTER/TESTER)
    |--- rapports/ (5 tests reels PASSE + scenario-parallel-reel.json)
    +--- tools/ (lanceur-scenario + scenarios)
```

**Les 16 .md par dossier** (tous dans ce dossier dedie atlas/rapports/freelance-2026-08-24/) :

| Dossier | .md dedie |
|---|---|
| racine freelance | `dossier-racine-freelance-2026-08-24.md` |
| conventions/ | `dossier-conventions-2026-08-24.md` |
| docs/ | `dossier-docs-2026-08-24.md` |
| protocoles/ | `dossier-protocoles-2026-08-24.md` |
| regles/ | `dossier-regles-2026-08-24.md` |
| routines/ | `dossier-routines-2026-08-24.md` |
| templates/ | `dossier-templates-2026-08-24.md` |
| tools-commun/ | `dossier-tools-commun-2026-08-24.md` |
| stark/ | `dossier-stark-2026-08-24.md` |
| shuri/ | `dossier-shuri-2026-08-24.md` |
| forge/ | `dossier-forge-2026-08-24.md` |
| rogers/ | `dossier-rogers-2026-08-24.md` |
| parker/ | `dossier-parker-2026-08-24.md` |
| jarvis/ (agent) | `dossier-jarvis-agent-2026-08-24.md` |
| vision/ | `dossier-vision-2026-08-24.md` |
| edith/ | `dossier-edith-2026-08-24.md` |
| fury/ | `dossier-fury-2026-08-24.md` |

---

## 3. SYNTHESE : CARTOGRAPHIE LISIBLE

```
freelance/ = la V2 du cerveau-projet, isolee de la v1
|
|--- CONCEPTION (racine)              -> .md racine
|   |--- proposition-v2.md      <- D1-D18 + P1-P9 (la source des decisions)
|   |--- bilan-v1-pour-v2        <- pourquoi on change (Themis)
|   +--- mode-demploi-declencheurs <- comment l'utilisateur pilote
|
|--- NORMATIF (ce qui regit les agents) -> .md regles + conventions + protocoles
|   |--- regles/regles-immuables.md   <- M1-M7, V1-V4, P1-P10, D1-D18, grades
|   |--- regles/philosophie/          <- le POURQUOI des regles
|   |--- conventions/conventions.md   <- le COMMENT (format, nommage)
|   |--- protocoles/protocoles.md     <- les 20 protocoles (cycle, JARVIS, DEFCON...)
|   +--- protocoles/protocoles-mcp.md <- l'architecture MCP
|
|--- AGENTS (9, theme MARVEL, session-freelance) -> .md par agent
|   |--- Stark (gold)  <- coordinateur, responsable JARVIS
|   |--- JARVIS (gold) <- hub de communication (distribue les missions)
|   |--- Shuri (silver) <- construit les agents (proto 9)
|   |--- Forge (silver) <- construit les outils (proto 10)
|   |--- Rogers (silver) <- gardien des regles
|   |--- Vision (silver) <- gardien EXCLUSIF de JARVIS
|   |--- Parker (copper) <- explorateur/diagnostiqueur
|   |--- EDITH (silver, dormante) <- observatrice H24 (serveur sans LLM)
|   +--- Fury (silver, hors-round) <- testeur reel
|   Chacun : fiche D17 + corrections + arbre (racine + themes + fins)
|
|--- MECANIQUE (tools-commun/, forge + vision) -> .md tools-commun
|   |--- jarvis/          <- LE HUB (jarvis.py + server MCP + inbox/outbox + files)
|   |--- os_path/         <- racine detectee (P10)
|   |--- encodage/ exec/ horloge/ jsonl-store/  <- bibliotheque commune (proto 18)
|   |--- rating-agents/   <- notation (proto 17)
|   |--- rappel/          <- anti-dispersion (proto 20)
|   |--- defcon/          <- serveur DEFCON (proto 15)
|   |--- securite/        <- lecteur-de-carte (decide) + verrou-outils (applique)
|   +--- routines-server/ <- serveur EDITH (collecte + alertes)
|
|--- ROUTINES (routines/, D15) -> .md routines
|   +--- manifest.json + surveillance/ (flux jarvis, modifications, evaluation)
|
|--- TEMPLATES (templates/, shuri) -> .md templates
|   +--- agent + corrections + arbre + theme + fins + outil (md/py/data)
|
+--- RAPPORTS ET TRACES
    |--- fury/rapports/   <- 5 tests reels PASSE
    |--- edith/rapports/  <- suivis de scores
    +--- jarvis/historique/ + inbox/ + outbox/ + files/  <- la vie de l'equipe
```

---

## 4. ETAT ACTUEL

### Fonctionnel (verifie sur disque)
- 9 agents freelance avec fiches D17 + arbres des decisions + fins
- JARVIS : jarvis.py v0.9.0 + jarvis-server.py v0.9.0 (refactoring proto 14),
  inbox/outbox actifs (~600 messages), historique, files d'attente
- tools-commun : os_path, encodage, exec, horloge, jsonl-store, rappel,
  rating-agents, defcon, securite (lecteur + verrou), routines-server
- regles-immuables M1-M7 + veracite V1-V4 + P1-P10
- protocoles 1-20 documentes
- routines EDITH : serveur actif (log 23/08), 3 routines en boucle
- Tests reels Fury : inter-round, parallel, protocole 13, rating -- PASSE
- Templates v2 complets

### En construction / points d'attention
- `freelance-historique.md` : VIDE (historique freelance a ecrire)
- `routines/demarrage/` et `routines/arret/` : dossiers vides (scripts
  verifier-integrite.py et detecter-orphelins.py attendus)
- `tools-commun/README.md` : liste des categories theoriques (activer/,
  lire/, consulter/, enregistrer/, valider/) non presentes physiquement
  -- README en retard sur la structure reelle
- `proposition-v2.md` : mentionne des outils cibles v2 (tools-commun/activer/,
  tools-commun/lire/, tools-commun/guider/, tools-commun/valider/) qui
  n'existent pas encore -- l'autonomie v2 repose actuellement sur jarvis.py
  et les outils deja construits
- Outils D18 (markers), D10 (bible des lecons), D9 (tokens-historique.md) :
  prevus par les decisions mais non encore construits dans freelance/
- Le dossier `tools-commun/encodage/` contient un BOM UTF-8 en tete de son
  .md (octet 0xEF 0xBB 0xBF avant "# encodage") -- a noter pour la v2
- Les fichiers du dossier utilisent majoritairement CRLF + accents
  (conforme D4) mais certains scripts python portent "# -*- coding: ascii -*-"
  (jarvis.py, defcon-server.py) -- heritage v1, a harmoniser avec D4

### Residus a nettoyer (domaine Hygie / Vision)
- __pycache__ nombreux (jarvis, routines-server, fonctions des outils)
- .bak de jarvis.py/jarvis-server.py (2-3 par fichier, conserves par regle proto 14)
- routines-server.bak-20260823-1700/ (archive entiere de l'ancien serveur)
- routines-server.pid (fichier PID potentiellement orphelin)
- `dossier-complet-freelance-2026-08-24.md.bak` (28 Ko, cree par
  corriger-accents lors de la premiere version du rapport, dans ce dossier)

---

## EN UNE PHRASE

Le dossier freelance est une v2 DEJA EN MARCHE : les decisions (D1-D18),
les regles gravees (M1-M7), les 9 agents MARVEL, le hub JARVIS et les
protocoles (1-20) existent et ont ete testes reellement par Fury
(inter-round, parallel, declencheurs, rating -- PASSE). Le detail de
chaque dossier vit dans son .md dedie (16 .md dans ce dossier dedie) ;
ce rapport complet est la structure qui les organise. Les chantiers
restants sont documentaires (freelance-historique vide, README
tools-commun en retard, demarrage/arret des routines vides) et les
outils prevus par D9/D10/D18 (tokens, bible des lecons, markers) ne
sont pas encore construits.
