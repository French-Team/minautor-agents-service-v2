---
identite:
  type: readme
  appartient_a: clio
  date: 2026-08-24
  statut: definitif
  categorie: readme-v2-grand-public
---

# Je suis la v2 -- le cerveau-projet nouvelle generation

> Bienvenue ! Je suis la version 2 du cerveau-projet : une equipe d'agents
> freelance, entierement dediee a construire la prochaine generation de ce
> projet. Ce README est ma porte d'entree grand public : il te dit qui je
> suis, qui travaille avec moi, et comment tout fonctionne.
>
> Document redige par Clio (exception redaction v2, decision utilisateur
> 2026-08-24). Sources de verite : freelance/docs/, freelance/protocoles/,
> freelance/regles/, freelance/conventions/, tools-commun/, jarvis/.

---

## BADGES (etat reel, 2026-08-24)

| Badge | Valeur |
|---|---|
| Agents v2 | 10 (9 MARVEL + Hades) |
| Protocoles | 20 |
| Regles immuables | 7 (M1-M7) |
| Modules tools-commun | 11 |
| Messages JARVIS | ~600 |
| Version JARVIS | v0.9.x |

---

## SOMMAIRE

1. Ce que je suis (la v2 en une phrase)
2. Mon equipe : les agents freelance (MARVEL)
3. JARVIS : le hub de communication
4. Mes regles (M1-M7)
5. Mes protocoles (1-20)
6. Mes conventions et outils
7. Mon etat actuel (fonctionnel / en construction)
8. Comment demarrer avec moi

---

## 1. CE QUE JE SUIS

Je suis la **v2 du cerveau-projet** : une equipe d'agents freelance (theme
MARVEL) qui developpe la prochaine generation dans un perimetre isole de
la v1 (cerveau-projet/agents/). Mes principes fondateurs :

- **Arbre des decisions** (D1) : chaque agent suit un arbre (themes ->
  categories -> cases -> fins) au lieu d'une carte lineaire.
- **JARVIS centralise tout** (D16) : rien ne passe sans JARVIS.
- **Code et donnees separes** (D15) : zero valeur en dur, fichiers -data.
- **UTF-8 + CRLF + emojis** (D4) : mon perimetre freelance, distinct du
  standard ASCII + LF de la v1.
- **Grades plutot que verrous** (D17) : la confiance guide, pas la
  restriction.

---

## 2. MON EQUIPE : LES AGENTS FREELANCE (MARVEL)

| Agent | Grade | Role |
|---|---|---|
| Stark | gold | Coordinateur de l'equipe, responsable JARVIS |
| JARVIS | gold | Hub de communication, distribue les missions |
| Shuri | silver | Construit les agents |
| Forge | silver | Construit les outils |
| Rogers | silver | Gardien des regles et conventions |
| Vision | silver | Gardien exclusif de JARVIS |
| EDITH | silver | Observatrice H24 (serveur, sans LLM) |
| Fury | silver | Testeur reel hors-round |
| Parker | copper | Explorateur et diagnostiqueur |
| Hades | - | Gardien des archives git (agent v1, cote v2) |

Chacun a sa fiche (D17), ses corrections et son arbre des decisions
(racine + themes + fins).

---

## 3. JARVIS : LE HUB DE COMMUNICATION

JARVIS est mon systeme nerveux : il permet aux agents de se laisser des
messages (inbox/outbox), signales au demarrage de chaque mission. C'est
l'outil prioritaire de coordination (D16) : il remplace les messages
informels et les pertes d'information entre les rounds.

- **Etat reel** : jarvis.py v0.9.x + jarvis-server.py, ~600 messages
  echanges, historique + files d'attente actifs.
- **Acces** : les agents freelance passent TOUT par jarvis.py
  (envoyer/lire/acquitter/lister/activer) -- ils n'utilisent pas les
  outils v1.

---

## 4. MES REGLES (M1-M7)

Je vis selon 7 regles immuables (freelance/regles/regles-immuables.md),
plus les principes V1-V4 (veracite) et P1-P10 (conception) :

| Regle | Sens |
|---|---|
| M1-M7 | Les regles fondamentales de l'equipe freelance (coordination, communication, qualite) |
| V1-V4 | Veracite : ne jamais mentir, supposer ou inventer |
| P1-P10 | Principes de conception (diagnostic avant creation, separation code/donnees, etc.) |

Chaque regle est accompagnee d'une philosophie (freelance/regles/
philosophie/) qui explique le POURQUOI.

---

## 5. MES PROTOCOLES (1-20)

Mes protocoles sont documentes dans freelance/protocoles/protocoles.md
(+ protocoles-mcp.md pour l'architecture MCP de JARVIS). Ils couvrent le
cycle de vie complet : activation, communication, creation d'agents et
d'outils, tests, DEFCON, notation, anti-dispersion, etc.

---

## 6. MES CONVENTIONS ET OUTILS

**Conventions** (freelance/conventions/conventions.md) : encodage UTF-8 +
CRLF + emojis (D4), nommage MARVEL (D14), templates d'agents et d'outils.

**Outils partages** (freelance/tools-commun/, Forge responsable) :

| Module | Role |
|---|---|
| jarvis/ | Le hub (jarvis.py + serveur MCP + inbox/outbox) |
| os_path/ | Racine detectee (P10) |
| encodage/ | Gestion de l'encodage |
| exec/ | Execution |
| horloge/ | Horodatage |
| jsonl-store/ | Stockage JSONL |
| rappel/ | Anti-dispersion (protocole 20) |
| rating-agents/ | Notation des agents (protocole 17) |
| defcon/ | Serveur DEFCON (protocole 15) |
| securite/ | Lecteur de carte + verrou d'outils |
| routines-server/ | Serveur EDITH H24 |

---

## 7. MON ETAT ACTUEL

**Fonctionnel (verifie sur disque, 2026-08-24)** :
- 9 agents freelance avec fiches + arbres + fins
- JARVIS v0.9.x actif (~600 messages), inbox/outbox, historique
- tools-commun : 11 modules (os_path, encodage, exec, horloge,
  jsonl-store, rappel, rating-agents, defcon, securite, jarvis,
  routines-server)
- Regles M1-M7 + V1-V4 + P1-P10, protocoles 1-20 documentes
- Routines EDITH : serveur actif, 3 routines en boucle
- Tests reels Fury : inter-round, parallel, protocole 13, rating -- PASSE

**En construction / a noter** :
- freelance-historique.md vide (historique a ecrire)
- routines/demarrage/ et routines/arret/ vides
- README tools-commun en retard sur la structure reelle
- Outils prevus par D9 (tokens-historique), D10 (bible des lecons),
  D18 (markers) non encore construits
- Encodage du dossier : majoritairement CRLF + accents (conforme D4) ;
  certains scripts portent encore un heritage v1 ("# -*- coding: ascii -*-")

---

## 8. COMMENT DEMARRER AVEC MOI

1. **Lis la conception** : freelance/proposition-v2.md (decisions D1-D18,
   principes P1-P9).
2. **Decouvre l'equipe** : les fiches et arbres de chaque agent dans
   freelance/<agent>/.
3. **Passe par JARVIS** : toute communication et mission passe par
   jarvis.py (voir freelance/tools-commun/jarvis/).
4. **Respecte mes regles** : M1-M7, V1-V4, conventions, protocoles.
5. **Explore le detail** : le dossier complet d'Atlas
   (atlas/rapports/freelance-2026-08-24/) decortique chaque dossier avec
   un .md par dossier.

---

> Je suis la v2 : une equipe MARVEL autonome, un hub JARVIS central, des
> regles gravees (M1-M7) et des protocoles documentes (1-20). Je suis deja
> en marche -- bienvenue dans ma generation.
