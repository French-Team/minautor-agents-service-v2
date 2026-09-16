# Journal multi-encarts de la Matrice (v3)

> VISUEL GENERE depuis les BDD -- jamais edite a la main (E-049).
> Regenerer : python main.py construire

## Encart : matrice

Flux : classeur-variables.json + fichiers PID des boucles -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| defcon : 2 | 07:33:10 | 09/09/2026 |
| veille-flux : ACTIVE (PID 8264) | 19:18:08 | 15/09/2026 |
| espion-integrite : ACTIVE (PID 7780) | 19:18:08 | 15/09/2026 |

## Encart : missions

Flux : pilote/file-missions.json + pilote/entonnoir-files.json -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
(aucune entree)

## Encart : routines

Flux : routines/veille-flux/journal-veille.txt -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| passe relax terminee : 0 detection(s), 0 alerte(s) | 19:15:11 | 15/09/2026 |
| passe relax demarree | 19:18:08 | 15/09/2026 |
| passe relax terminee : 0 detection(s), 0 alerte(s) | 19:18:09 | 15/09/2026 |
| passe relax demarree | 19:23:09 | 15/09/2026 |
| passe relax terminee : 0 detection(s), 0 alerte(s) | 19:23:10 | 15/09/2026 |

## Encart : alertes

Flux : veille-flux/alertes-emises.json + intercom/matrice/inbox.jsonl -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| intercom : signaler | 13:52:43 | 13/09/2026 |
| intercom : alerte-grave | 14:32:04 | 13/09/2026 |
| intercom : signaler | 14:37:20 | 13/09/2026 |
| intercom : signaler | 17:55:02 | 13/09/2026 |
| intercom : signaler | 18:25:57 | 13/09/2026 |

## Encart : cameleon

Flux : intercom/cameleon/inbox.jsonl (ecrit par pause-session) -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| pause -- mission M-080 | 07:31:42 | 09/09/2026 |
| reprise -- mission M-080 | 07:32:07 | 09/09/2026 |
| pause -- mission M-080 | 07:32:53 | 09/09/2026 |
| reprise -- mission M-080 | 07:33:09 | 09/09/2026 |
| pause -- mission DIALOGUE-COMMUNICATION | 11:07:23 | 12/09/2026 |

## Encart : usages

Flux : sac-a-dos (chaque outil) -> bdd-usages -> usages-outils-combos.jsonl -> VUE

| Entree | Heure | Date |
|---|---|---|
| suivi-optimus/coherence code 0 24ms | 19:23:05 | 15/09/2026 |
| corriger-ascii/corriger code 1 239ms | 19:23:09 | 15/09/2026 |
| veille-flux/passe-relax code 0 1152ms | 19:23:10 | 15/09/2026 |
| bdd-activites/noter code 0 2ms | 19:23:10 | 15/09/2026 |
| bdd-sessions/resume code 0 3ms | 19:24:04 | 15/09/2026 |
| suivi-optimus/vue code 0 2ms | 19:24:04 | 15/09/2026 |
| suivi-optimus/noter code 0 1ms | 19:24:04 | 15/09/2026 |
| suivi-optimus/noter code 0 1ms | 19:24:22 | 15/09/2026 |

## Encart : modifications

Flux : notes de mission -> bdd-modifications -> modifications-par-fichier.json -> VUE

| Entree | Heure | Date |
|---|---|---|
| matrice/routines/veille-flux/commun.py | 19:18:18 | 15/09/2026 |
| matrice/routines/veille-flux/constants.py | 19:18:18 | 15/09/2026 |
| tmp-optimus/mesure-mo097-veille.py | 19:18:19 | 15/09/2026 |
| _operateur/optimus-prime/super-combos/combos/outils/verifier-observations-non-redondantes.py | 19:19:20 | 15/09/2026 |
| _operateur/optimus-prime/cockpit/revue-seuils-cockpit.md | 19:22:38 | 15/09/2026 |

## Encart : lecons

Flux : lecons gravees -> bdd-lecons -> lecons.json -> VUE (relues a chaque injection)

| Entree | Heure | Date |
|---|---|---|
| L-081 UN DOCUMENT SANS CARTE D'IDENTITE NE PEUT PAS ETRE INJECTE AU BON MOMENT. Sur 65 documents de la zon | 08:31:35 | 14/09/2026 |
| L-082 UN ROLE DONNE N'EST PAS UN ROLE INJECTE. Le cameleon recoit UNE personnalite par mission (categorie  | 08:38:27 | 14/09/2026 |
| L-083 Le verbe enregistrer du pilote note DEJA debut+fin au journal suivi-optimus (mission menee hors file | 09:41:23 | 14/09/2026 |
| L-084 UN CONTROLE QUE PERSONNE NE BRANCHE N'EXISTE PAS : le croisement file du pilote <-> journal suivi-op | 19:12:41 | 15/09/2026 |
| L-085 UN SEUIL COMPARE DOIT APPARTENIR A L'OBJET MESURE : le cockpit comparait la duree de la veille-flux  | 19:19:35 | 15/09/2026 |

## Encart : variables

Flux : machine-defcon / pause-session / bdd-variables -> classeur-variables.json -> VUE

| Entree | Heure | Date |
|---|---|---|
| veille-intervalle = 600 | 16:19:00 | 06/09/2026 |
| defcon = 2 | 07:33:10 | 09/09/2026 |
| perimetre-cameleon = maintenance,_operateur,pilote/file-missions.json,data/historiques-missions.jsonl,data/modifications-par-fichier.json,data/usages-outils-combos.jsonl,data/activites-recentes.json,data/defcon-historique.jsonl,data/classeur-variables.json,data/manuel-outils.md,journal-multi-encarts.md,matrice-readme.md,routines/routines-readme.md,routines/vie/DESCRIPTION.md,routines/espion-integrite,intercom/pilote/outbox.jsonl,intercom/matrice/inbox.jsonl,docs/IMPERATIF.md,templates/theme-bdd/README.md,data/outils/pause-session,data/outils/machine-defcon,data/outils/verifier-regles,data/outils/verifier-protocoles,data/outils/verifier-conventions | 07:43:10 | 15/09/2026 |
