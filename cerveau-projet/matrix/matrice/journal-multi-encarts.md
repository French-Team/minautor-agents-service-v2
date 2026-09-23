# Journal multi-encarts de la Matrice (v3)

> VISUEL GENERE depuis les BDD -- jamais edite a la main (E-049).
> Regenerer : python main.py construire

## Encart : matrice

Flux : classeur-variables.json + fichiers PID des boucles -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| defcon : 2 | 07:33:10 | 09/09/2026 |
| veille-flux : ACTIVE (PID 316) | 07:20:33 | 23/09/2026 |
| espion-integrite : ACTIVE (PID 5560) | 07:20:33 | 23/09/2026 |

## Encart : missions

Flux : pilote/file-missions.json + pilote/entonnoir-files.json -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
(aucune entree)

## Encart : routines

Flux : routines/veille-flux/journal-veille.txt -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| passe relax demarree | 07:40:41 | 23/09/2026 |
| passe relax terminee : 0 detection(s), 0 alerte(s) | 07:40:43 | 23/09/2026 |
| passe relax demarree | 07:45:43 | 23/09/2026 |
| passe relax terminee : 0 detection(s), 0 alerte(s) | 07:45:45 | 23/09/2026 |
| passe relax demarree | 07:47:21 | 23/09/2026 |

## Encart : alertes

Flux : veille-flux/alertes-emises.json + intercom/matrice/inbox.jsonl -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| intercom : signaler | 20:58:56 | 20/09/2026 |
| intercom : signaler | 07:44:31 | 21/09/2026 |
| intercom : signaler | 09:01:00 | 22/09/2026 |
| intercom : signaler | 09:31:02 | 22/09/2026 |
| intercom : signaler | 10:01:04 | 22/09/2026 |

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
| ecrire/editer code 0 4ms | 07:46:37 | 23/09/2026 |
| ecrire/ecrire code 0 2ms | 07:46:37 | 23/09/2026 |
| ecrire/ecrire code 0 2ms | 07:46:37 | 23/09/2026 |
| ecrire/editer code 0 3ms | 07:46:38 | 23/09/2026 |
| ecrire/ecrire code 0 5ms | 07:47:01 | 23/09/2026 |
| journal-multi-encarts/construire code 0 126ms | 07:47:01 | 23/09/2026 |
| suivi-optimus/construire code 2 0ms | 07:47:01 | 23/09/2026 |
| corriger-ascii/corriger code 0 573ms | 07:47:21 | 23/09/2026 |

## Encart : modifications

Flux : notes de mission -> bdd-modifications -> modifications-par-fichier.json -> VUE

| Entree | Heure | Date |
|---|---|---|
| _operateur/optimus-prime/tmp-optimus/cobaye-mo363-cadence.py | 07:24:28 | 23/09/2026 |
| _operateur/optimus-prime/tmp-optimus/bilan-mo363.txt | 07:27:04 | 23/09/2026 |
| _operateur/optimus-prime/pilote/commun.py | 07:33:23 | 23/09/2026 |
| demarrer-optimus-prime.md | 07:33:23 | 23/09/2026 |
| _operateur/optimus-prime/audits/audit-voie-injection.md | 07:39:49 | 23/09/2026 |

## Encart : lecons

Flux : lecons gravees -> bdd-lecons -> lecons.json -> VUE (relues a chaque injection)

| Entree | Heure | Date |
|---|---|---|
| L-162 Le cockpit N AFFICHE RIEN lui-meme : il appelle le verbe du DOMICILE (ici lot etat, chez le pilote). | 10:06:34 | 21/09/2026 |
| L-163 UN ROUGE MUET : QUAND LA CAUSE EST ECRITE PAR LE GARDE MAIS PAS EXTRAITE PAR LE LANCEUR, LE VERDICT  | 07:33:32 | 22/09/2026 |
| L-164 UN AGENT QUI EDITE AU NATIF NE PEUT PAS PRETENDRE AVOIR PROUVE SA PUBLICATION -- ET SON < PRISTINE > | 07:40:19 | 22/09/2026 |
| L-165 Un process qui depend de la memoire d'un agent n'est pas un process : c'est une discipline. DEMANDE  | 08:48:06 | 22/09/2026 |
| L-166 UNE PROSE QUI CITE DES NOMS VOYAGE PAR FICHIER, JAMAIS DANS UN ARGUMENT SHELL : LES ACCENTS GRAVES S | 09:48:45 | 22/09/2026 |

## Encart : variables

Flux : machine-defcon / pause-session / bdd-variables -> classeur-variables.json -> VUE

| Entree | Heure | Date |
|---|---|---|
| veille-intervalle = 600 | 16:19:00 | 06/09/2026 |
| defcon = 2 | 07:33:10 | 09/09/2026 |
| perimetre-cameleon = maintenance,_operateur,pilote/file-missions.json,data/historiques-missions.jsonl,data/modifications-par-fichier.json,data/usages-outils-combos.jsonl,data/activites-recentes.json,data/defcon-historique.jsonl,data/classeur-variables.json,data/manuel-outils.md,journal-multi-encarts.md,matrice-readme.md,routines/routines-readme.md,routines/vie/DESCRIPTION.md,routines/espion-integrite,intercom/pilote/outbox.jsonl,intercom/matrice/inbox.jsonl,docs/IMPERATIF.md,templates/theme-bdd/README.md,data/outils/pause-session,data/outils/machine-defcon,data/outils/verifier-regles,data/outils/verifier-protocoles,data/outils/verifier-conventions,data/lecons.json,data/sessions.json | 07:39:10 | 17/09/2026 |
| interpreteur-python = auto | 08:48:36 | 19/09/2026 |
