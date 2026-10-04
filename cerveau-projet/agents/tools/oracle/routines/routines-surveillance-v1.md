# Routines de surveillance v1

**Dossier :** `agents/tools/oracle/routines/`
**Declenchement :** routines-server v1 (manifest.json, boucle 30 s)
**Origine :** transposees des routines v2 (decision utilisateur 2026-08-29 :
creer les routines v1 inspirees des v2, sans recuperer leur code - 2 univers
distincts).

## Liste

**Decision utilisateur 2026-08-30 : les routines previennent ORACLE (le
coordinateur), pas Cerberus.** Chaque routine depose son alerte dans
`inbox/oracle.jsonl`, c est Oracle qui decide d aviser Cerberus (modele
aero). Ajoutee par Buffy lors de la reduction du bruit ETAT URGENT : la
alerte directe a Cerberus creait une boucle recursive (le P1 pose dans
inbox/cerberus etait re-compte par flux -> nouveau URGENT -> nouvelle
alerte).

| Routine | Intervalle | Role | Historise |
|---|---|---|---|
| `flux` | 480 s | Surveille les P1 non-acquittes dans l inbox Oracle ; alerte Oracle quand le nombre change | changement uniquement |
| `sante` | 600 s | Etat global v1 : daemons vivants, DEFCON 5 gele, encart coherent, BDD recente | anomalie uniquement |
| `live` | 720 s | Activations/desactivations des agents v1 : agent actif, debordement inbox, derniere activite | anomalie uniquement |
| `encart` | 840 s | Integrite de l encart v1 (AGENTS-activite-recente.md, colonnes) - etats valides charges depuis etats-actions.json (v0.2.0) + depuis v0.3.1 : detection des valeurs 'Inconnu' en colonnes Grade/Agent (acteur non declare dans grades-v1.json) | anomalie uniquement |
| `notation` | 960 s | Depose une demande periodique d evaluation croisee des agents dans l inbox d Oracle (Themis evalue, Janus controle, Oracle coordonne) | au depot uniquement |
| `compter-entree` | 1080 s | Mesure des tokens ENTREE -> data/journal-entree.jsonl + tokens-historique-v1.md | chaque tick |
| `compter-sortie` | 1200 s | Mesure des tokens SORTIE -> data/journal-sortie.jsonl + tokens-historique-v1.md | chaque tick |
| `vigie-perimetre` | 1320 s | Guetteuse du perimetre Oracle (empreintes SHA-256, section `perimetre_surveille` du manifest) - alerte Oracle format 4W quand un fichier surveille change | changement uniquement |
| `verifier-agent-perimetre` | **TIMER DESACTIVE** (decision 2026-08-29 : pas un timer) | **GATE PRE-VOL** : l agent la lance au moment ou il decide de commencer (case c0g de SON parcours) : verifie qu il est LE BON AGENT (agent actif de la session + zone de la mission v1/v2/jarvis) AVANT de faire quoi que ce soit | jamais (porte, pas alerte) |
| `verifier-statuts` | 1440 s | Lit la colonne Etat de l encart v1 et informe ORACLE qui avise en fonction de l etat : **URGENT -> escalade DEFCON 4** (degradation ; normal = DEFCON 2) + **mission-ajouter --file asap** (prioritaire). Si un **ROUND EST EN COURS** : met la mission courante en attente (file attente v1) + instruction **INTER-ROUND** a l agent actif (SIGNALER le besoin a ORACLE via `mission-ajouter`, MA FIN vers ORACLE `--cible oracle`, le **PILOTE largue** l habilite puis renvoie l appelant -- modele aero R2/R3). Anti-inondation (une fois par URGENT), filtre les faux URGENT (Demarrage oracle) | 1 fois par nouvelle URGENT |

## escalade DEFCON (degration URGENT -> 4)

DEFCON **2 = niveau NORMAL** (REPRISE TOTALE, protocole 15 v2). La
routine `verifier-statuts` monte vers **DEFCON 4** (VALIDATION DES
REPARATIONS) quand un etat URGENT reel apparait :
- `oracle.py defcon-escaler 4 "<raison>"` : escalation vers le haut
  (2->4, no-op si deja au niveau cible ou superieur).
- Niveau 4 = on ne reprend que pour verifier/tester/valider les
  reparations ; une fois validees, descente normale par
  `oracle.py defcon-changer 4 3` puis `3 2`.
- DEFCON 5 (arret total) reste reserve a `defcon-declarer`.

## Principes

- **Lecture seule + alerte** : les routines de surveillance ne modifient
  jamais le fonctionnement, elles detectent et signalent (format 4W via
  inbox Oracle, comme vigie-round).
- **Evenementiel** : `sante`, `live`, `encart` historisent UNIQUEMENT en cas
  d anomalie pour ne pas noyer l encart. `flux` historise seulement quand le
  nombre de P1 change.
- **Grades** : ces routines sont graduees dans grades-v1.json (la plupart
  G3 Utilitaire ; `verifier-agent-perimetre` G2 Important - elle protege
  les perimetres). La colonne Grade de l encart le reflete.

## Verifier-agent-perimetre (le bon agent) -- GATE PRE-VOL, PAS UN TIMER

> Decision utilisateur 2026-08-29 : il est inutile de laisser un mauvais
> agent travailler puis tout detruire. La verification a lieu AU MOMENT ou
> l agent decide de lancer son analyse - AVANT qu il commence. Le timer est
> desactive (actif=false dans le manifest) ; la detection a posteriori
> (git) reste disponible a la demande.

- **Porte (case c0g de CHAQUE parcours v1)** : `verifier-agent-perimetre.py
  --gate --moi <mon-agent>` - l agent la lance apres la relecture (c0b),
  avant de commencer. Verifie :
  1. L agent actif de la session-admin (AGENTS.md) == moi. Sinon KO : un
     autre agent est actif, STOP immediat, reactiver Cerberus SANS RIEN
     TOUCHER.
  2. La Raison de la session (ma mission) ne vise pas une zone hors de mes
     habilitations : v2 (freelance) -> seul ferrari (v1) ou un agent v2 ;
     jarvis -> Vision seul ; agent v2 avec mission sans marqueur v2 -> KO.
  3. Cerberus et Oracle (coordination) sont exempts de la verif de zone
     (leur Raison est le bilan FIN de l agent precedent).
- **Zones** : `v1` (cerveau-projet hors freelance), `v2`
  (cerveau-projet/freelance), `jarvis` (tools-commun/jarvis).
- **Agents habilitES** : v2 = agents freelance + ferrari (agent v1
  specialise v2) ; jarvis = Vision seul ; Hygie/Hades = tout le workspace.
- **En mode gate** : PAS d alerte inbox, PAS d historisation, PAS
  d anti-spam - controle pur, retour 0 (OK, commencer) / 1 (KO, STOP).

## Etats dynamiques (colonne Etat)

La liste des etats + leurs regles de detection vivent dans
`agents/tools/oracle/etats-actions.json` (decision utilisateur
2026-08-29, 2e round : rendre les etats dynamiques pour ne plus editer le
code). Etats actuels : **DEBUT, FIN, URGENT, BUG, DEV** (citations -
presente pour le dev, hors flux reel), **ATTENTE** (demande deposee),
**AUTO** (routine sans intervention), **ACTION** (utilitaire avec
intervention a faire), **ACTIF** (defaut). Les regles sont appliquees dans
l ordre du fichier. La section `inbox_outbox` prepare les etats du futur
tableau inbox-outbox-messages.md (A LIRE, A TRAITER, ACQUITTE, REPONDU,
CLOS).

## Tests sur demande

Chaque routine accepte `--dry-run` pour verifier son execution sans
historiser ni alerter (sauf compter-entree / compter-sortie, journaliers).