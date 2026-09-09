# LA MATRICE -- CENTRE DE CONTROLE TOTAL

> La Matrice gere TOUT pour les agents : communication, organisation, themes,
> pilote, BDD, espions. Point de convergence de tout ce qui sera construit en v3.

## Flux unique (jamais brise)

```
user -> Matrice (theme) -> pilote (+ mission) -> agent (execution)
     -> fin au pilote -> pilote -> Matrice (reprend le controle)
```

## Sections

| Section | Role | Contrat |
|---|---|---|
| `data/` | BDD de la Matrice (lecons, variables, historiques, modifications, usages) | data/data-readme.md |
| `intercom/` | Communication organisee (Matrice, pilote, agent) | intercom/intercom-readme.md |
| `routines/` | Vie de la Matrice (securite, orchestration, demarrage, espions) | routines/routines-readme.md |
| `pilote/` | File de missions, serie stricte, lot, entonnoir + tresse | pilote/DESCRIPTION.md + data/manuel-outils.md |

## Regles structurelles (ancrees ailleurs, rappelees ici)

- Ecriture : `matrix/` exclusivement (regles-immuables/perimetre-write.md).
- Serie stricte : une mission a la fois (regles-immuables/serie-stricte.md).
- Outils Python seul, protections ouverture/fermeture (regles-immuables/python-seul.md).
- Anti-surcharge : modifications notees en BDD, JAMAIS en commentaire dans les fichiers
  (regles-immuables/anti-surcharge.md).
- ASCII strict (regles-immuables/ascii-strict.md).
- Architecture des outils : entree -> categorie -> fonctions simples
  (conventions/convention-architecture-outils.md).
- Zero valeur en dur (conventions/convention-zero-valeurs-en-dur.md).
- Integrite par SHA-256 (conventions/convention-integrite-sha256.md).

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
| Machine defcon (echelle fermee 5-4-3-2, descente stricte, valider clot def3) + garde defcon 5 dans le pilote (seul DEFCON injectable) + journal defcon-historique | FAIT (2026-09-07, M-059/M-060, decision createur) -- convention des demandes a crochets `_operateur/optimus-prime/conventions/convention-crochets.md` |
| Outil bilan-periode (periodes fermees 1h/heures/24h/3j/semaine/mois, lecture seule, 4 sources horodatees) -- porte de la demande [bilan] | FAIT (2026-09-07, M-061) |
| Journal multi-encarts (visuel des metriques genere depuis les BDD, 9 encarts a ordre ferme : matrice, missions, routines, alertes, cameleon, usages, modifications, lecons, variables ; tableaux Entree/Heure/Date + ligne de FLUX par encart) -- nouveau fichier propre a la v3, jamais les fichiers v1/v2 | FAIT (2026-09-08, M-079 ; enrichi M-080) |
| Protocole de pause session-matrix (outil pause-session : pause/reprendre/etat/perimetre/journal ; defcon 5 -> pause automatique, crochets [alerte]/[pause], gardes pilote, perimetre cameleon reductible, notifications etanchees) | FAIT (2026-09-09, M-080) |
| Agent unique cameleon (fiche matrix/agents/cameleon, personnalites au vivier TH-017..021, perimetre matrix/ seul) + outil editer-agents-md (encart session-matrix dans AGENTS.md, garde structurelle) -- **flux v3** : la Matrice accueille au demarrage, l'operateur fait sa demande, la Matrice lance le cameleon | FAIT (2026-09-07, M-072 a M-074) ; branchement cameleon au pilote : a venir (GO) |
| Autres routines de vie / securite / orchestration | a construire (avec le createur) |
