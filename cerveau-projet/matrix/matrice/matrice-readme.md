# LA MATRICE -- CENTRE DE CONTROLE TOTAL

> La Matrice gere TOUT pour les agents : communication, organisation, themes,
> pilote, BDD, espions. Point de convergence de tout ce qui sera construit en v3.

## Deux flux distincts (jamais melanges, jamais brises)

> Decrete createur 2026-09-12 : dual flux. La Matrice opere DEUX flux
> separes, chacun en serie stricte, chacun avec sa surveillance.
> La Matrice est le seul point commun : un flux n'ecrit jamais dans
> les zones de l'autre sans porte officielle.

### Flux 1 : LE CAMELEON (Matrice guide l'agent)

```
user -> Matrice (choisit le theme) -> pilote (+ mission) -> cameleon (execute)
     -> fin au pilote -> pilote -> Matrice (reprend le controle)
```

- Lancement : `demarrer-cameleon.md` (racine, `id=cameleon`, Flux 1) ->
  Matrice ACTIVE (`routines/vie/main.py activer` si besoin) ->
  `COMMUNICATION` (TH-026) injecte -> cameleon se presente une fois
  puis dialogue sans conscience pilote.
- Matrice GUIDE le cameleon : themes du vivier (COMMUNICATION TH-026),
  injections ordonnees (filtre L-016 : 0 fuite invisible), checklists,
  profils de personnalite. Le cameleon ignore qu'il est guide.
- Perimetre cameleon : lecture + ecriture `matrix/` seuls (hors `_operateur/`).
- Surveillance Flux 1 : `veille-flux` (py_compile, ASCII, marbres),
  `espion-integrite` (BDD matrice), `suivi-sync`, non-regression.
  Surveille le FLUX (pilote qui ne fonctionne plus, Matrice qui ne
  demarre plus, processus fantomes), pas les fichiers un par un.
- Agent unique cameleon, devient n'importe qui selon le theme.

### Flux 2 : MAINTENANCE OPTIMUS (Matrice surveille Optimus)

```
user <-> Optimus en direct
ou Matrice reveille Optimus (pause, defcon 5, maintenance, decision)
     -> Optimus execute -> rend la main -> declare debut/fin dans suivi-optimus
     -> Matrice reprend le controle (pilote verrouille pendant maintenance)
```

- Lancement : `demarrer-optimus-prime.md` (racine, `id=optimus-prime`, Flux 2) ->
  hors pilote, reserve et verrouille.
- Optimus GERE la Matrice : construit outils, themes, protocoles, BDD,
  reparations, auto-evolution. Hors flux formel v1/v2, hors pilote.
- Perimetre Optimus : lecture workspace complet, ecriture `matrix/`
  exclusivement (plus `demarrer-optimus-prime.md` + `demarrer-cameleon.md`
  en racine, une fois chacun -- allowlist perimetre).
- Surveillance Flux 2 : `espions-optimus/` (integrite 71 fichiers
  `_operateur/` + activite : file, frictions, verrous) + `remorque`
  (45 equipements) + `suivi-optimus` (trace append-only, vue regeneree,
  etancheite cameleon) + `BDD modifications` (hashes, raisons, friction).
  La Matrice SURVEILLE Optimus dans ce flux reserve et verrouille.
- Flux verrouille : session-matrix en pause, cameleon stoppe, perimetre
  reductible, notifications etanches (jamais la raison).
- Cockpit prive : `_operateur/optimus-prime/cockpit/cockpit-matrice.py` --
  Optimus y consulte la Matrice comme **serveur distant** via routes privees
  verrouillees `/etat /sante /flux1 /flux2 /metriques /complet` (lecture
  seule, jamais d'ecriture, invisible cameleon -- domicile `_operateur/` +
  zone `maintenance`). Au reveil et avant `reprendre`, passage par le cockpit.

## Sections

| Section | Role | Contrat |
|---|---|---|
| `data/` | BDD de la Matrice (lecons, variables, historiques, modifications, usages) | data/data-readme.md |
| `intercom/` | Communication organisee (Matrice, pilote, agent) | intercom/intercom-readme.md |
| `routines/` | Vie de la Matrice (securite, orchestration, demarrage, espions) | routines/routines-readme.md |
| `pilote/` | File de missions, serie stricte, lot, entonnoir + tresse | pilote/DESCRIPTION.md + data/manuel-outils.md |

## Marbre de la Matrice : 3 BDD separees (M-082, decision createur)

Le marbre de la Matrice (regles / conventions / protocoles QUI LA REGISSENT)
vit chez ELLE, en BDD, jamais dans un domicile d'agent (optimus est invisible
de la Matrice) :

| BDD | Outil (porte unique) | Lecture |
|---|---|---|
| `data/regles-matrice.json` | bdd-regles-matrice (ajouter/lire/verifier) | Matrice + cameleon |
| `data/conventions-matrice.json` | bdd-conventions-matrice (ajouter/lire/verifier) | Matrice + cameleon |
| `data/protocoles-matrice.json` | bdd-protocoles-matrice (ajouter/lire/verifier) | Matrice + cameleon (SES routes) |

**ECRITURE = OPTIMUS SEUL** (avec le createur, via ces 3 portes ; empreinte
SHA-256, espion au registre). Le cameleon ne modifie JAMAIS le marbre ni le
contenu de la Matrice : il ne fait que LIRE (routes au chargement) et n'ecrit
que les DONNEES de mission via les portes officielles.

## Regles structurelles (graves dans la BDD regles-matrice, rappelees ici)

- Ecriture : `matrix/` exclusivement.
- Serie stricte : une mission a la fois.
- Outils Python seul.
- Anti-surcharge : modifications notees en BDD, JAMAIS en commentaire dans les fichiers.
- ASCII strict hors base acceptee.
- Architecture des outils : entree -> categorie -> fonctions simples (BDD conventions-matrice CV-001).
- Zero valeur en dur.
- Integrite par SHA-256 (BDD conventions-matrice CV-003).

## Etat de construction (2026-09-06)

| Etape | Statut |
|---|---|
| Squelette dossiers (data / intercom / routines) | fait |
| Contrats des 3 sections | fait (ce depot) |
| BDD modifications-par-fichier + outil bdd-modifications | FAITE (2026-09-06, 1/7) |
| BDD historiques-missions (journalisee par le pilote) | FAITE (2026-09-06, 2/7) |
| BDD lecons + outil bdd-lecons (injection taguee) | FAITE (2026-09-06, 3/7) |
| BDD usages-outils-combos + outil bdd-usages (journal des usages) | FAITE (2026-09-06, 4/7) |
| BDD classeur-variables + outil bdd-variables (une cle = une valeur courante) | FAITE (2026-09-06, 5/7) |
| BDD activites-recentes + outil bdd-activites (sections pre-declarees, rotation 50) | FAITE (2026-09-06, 6/7) |
| BDD historique-bdd + outil bdd-historique (journal filtrable, obsolete sur ajout) | FAITE (2026-09-06, 7/7) |
| Pilote multi-missions (file, injection, fin, lot multi-rounds, checklists auto, tresse, puisage auto) | VIVANT (2026-09-06, M-001 a M-028) |
| Canaux intercom : pilote/outbox + matrice/inbox reels | FAITS (2026-09-06) |
| Plan des 7 BDD | COMPLETE (2026-09-06, 7/7) |
| Routine espion-integrite (surveillance des 7 BDD) | POSEE (2026-09-06) |
| Indices par zone (7 indices.md, entonnoir compris) + manuel-outils central + convention-indices | FAITS (2026-09-06, M-006 + M-025) -- se lisent AVANT les fichiers |
| Trois marbres verifiables (verifier-conventions / regles / protocoles) + corriger-ascii (auto-correction, base acceptee) | FAITS (2026-09-06, M-008 a M-011) |
| Routine veille-flux (surveillance des fichiers modifies, combos, alertes, mission au vrac) | FAITE (2026-09-06, M-012 + M-020 : boucle detection -> mission fermee) |
| Vie de la Matrice : activateur routines/vie/ (lancement DETACHE des boucles veille-flux + espion-integrite, etat, garde double, PID fantome nettoye) + VEILLE PERMANENTE ACTIVEE | FAIT (2026-09-06, M-046) -- raccord demarrage : `routines/vie/main.py activer` |
| Entonnoir en echelon (0 vrac, 1 type -- dev/reparation/doc/audit/**revision** --, 2 categorie, 3 urgence, 4 tresse) + puisage auto par l'injection | FAIT (2026-09-06, M-018 a M-023, M-026/M-027 ; revision ajoutee 2026-09-07, M-055, decision createur) |
| Moules templates/ (outil-bdd + theme-bdd) + outil dupliquer-template (--moule, clones conformes verifies avant ecriture) | POSES (2026-09-06, M-030 + M-031) |
| Machine defcon (echelle fermee 5-4-3-2, descente stricte, valider clot def3) + garde defcon 5 dans le pilote (seul DEFCON injectable) + journal defcon-historique | FAIT (2026-09-07, M-059/M-060, decision createur) -- convention des demandes a crochets (graves en BDD conventions-matrice + domicile optimus pour la forme longue) |
| Outil bilan-periode (periodes fermees 1h/heures/24h/3j/semaine/mois, lecture seule, 4 sources horodatees) -- porte de la demande [bilan] | FAIT (2026-09-07, M-061) |
| Journal multi-encarts (visuel des metriques genere depuis les BDD, 9 encarts a ordre ferme : matrice, missions, routines, alertes, cameleon, usages, modifications, lecons, variables ; tableaux Entree/Heure/Date + ligne de FLUX par encart -- PAS d'encart optimus : optimus reste INVISIBLE, decision createur 2026-09-09) -- nouveau fichier propre a la v3, jamais les fichiers v1/v2 | FAIT (2026-09-08, M-079 ; enrichi M-080, M-084) |
| Protocole de pause session-matrix (outil pause-session : pause/reprendre/etat/perimetre/journal ; defcon 5 -> pause automatique, crochets [alerte]/[pause], gardes pilote, perimetre cameleon reductible, notifications etanchees) | FAIT (2026-09-09, M-080) |
| Agent unique cameleon (fiche matrix/agents/cameleon, personnalites au vivier TH-017..021, perimetre matrix/ seul) + outil editer-agents-md (encart session-matrix dans AGENTS.md, garde structurelle) -- **flux v3** : la Matrice accueille au demarrage, l'operateur fait sa demande, la Matrice lance le cameleon | FAIT (2026-09-07, M-072 a M-074) ; branchement : `demarrer-cameleon.md` + TH-026 COMMUNICATION (M-127) + pilote filtre L-016 `filtrer_pour_cameleon` + M-089 injectee/finie (M-128, Flux 1 GUIDE prouve) |
| Marbre Matrice domicilie : 3 BDD separees (regles / conventions / protocoles) + 3 outils portes (ecriture optimus seul, lecture Matrice + cameleon) | FAIT (2026-09-09, M-082, decision createur) |
| Suivi d'optimus (trace data/suivi-optimus.jsonl append-only + etalon, outil suivi-optimus noter/lire/vue/verifier, vue dediee _operateur/optimus-prime/suivi-optimus.md a tableaux par action (MO-235 : deplacee HORS matrice/, donc invisible au cameleon PAR CONSTRUCTION), etancheite cameleon : zones suivi-optimus + suivi-optimus.jsonl exclues, philosophie d'invisibilite CV-006/L-016) | FAIT (2026-09-09, M-084, GO createur) |
| Autres routines de vie / securite / orchestration | a construire (avec le createur) |
