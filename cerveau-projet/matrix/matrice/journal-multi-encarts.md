# Journal multi-encarts de la Matrice (v3)

> VISUEL GENERE depuis les BDD -- jamais edite a la main (E-049).
> Regenerer : python main.py construire

## Encart : matrice

Flux : classeur-variables.json + fichiers PID des boucles -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| defcon : 2 | 07:33:10 | 09/09/2026 |
| veille-flux : ACTIVE (PID 14032) | 19:26:57 | 15/09/2026 |
| espion-integrite : ACTIVE (PID 11600) | 19:26:57 | 15/09/2026 |

## Encart : missions

Flux : pilote/file-missions.json + pilote/entonnoir-files.json -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
(aucune entree)

## Encart : routines

Flux : routines/veille-flux/journal-veille.txt -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| passe relax terminee : 0 detection(s), 0 alerte(s) | 08:35:41 | 16/09/2026 |
| passe relax demarree | 08:40:42 | 16/09/2026 |
| passe relax terminee : 0 detection(s), 0 alerte(s) | 08:40:43 | 16/09/2026 |
| passe relax demarree | 08:45:43 | 16/09/2026 |
| passe relax terminee : 0 detection(s), 0 alerte(s) | 08:45:44 | 16/09/2026 |

## Encart : alertes

Flux : veille-flux/alertes-emises.json + intercom/matrice/inbox.jsonl -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| intercom : signaler | 14:37:20 | 13/09/2026 |
| intercom : signaler | 17:55:02 | 13/09/2026 |
| intercom : signaler | 18:25:57 | 13/09/2026 |
| intercom : signaler | 07:06:47 | 16/09/2026 |
| intercom : signaler | 07:21:58 | 16/09/2026 |

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
| ecrire/editer code 0 10ms | 08:47:30 | 16/09/2026 |
| ecrire/editer code 0 11ms | 08:47:30 | 16/09/2026 |
| ecrire/editer code 0 4ms | 08:47:31 | 16/09/2026 |
| ecrire/editer code 0 6ms | 08:47:31 | 16/09/2026 |
| ecrire/editer code 2 0ms | 08:47:31 | 16/09/2026 |
| ecrire/editer code 0 6ms | 08:47:31 | 16/09/2026 |
| ecrire/editer code 1 6ms | 08:47:41 | 16/09/2026 |
| ecrire/editer code 0 6ms | 08:48:05 | 16/09/2026 |

## Encart : modifications

Flux : notes de mission -> bdd-modifications -> modifications-par-fichier.json -> VUE

| Entree | Heure | Date |
|---|---|---|
| _operateur/optimus-prime/super-combos/combos/outils/bdd-frictions/entry.py | 07:44:03 | 16/09/2026 |
| _operateur/optimus-prime/super-combos/combos/outils/bdd-frictions/fonctions/bdd_frictions.py | 07:49:26 | 16/09/2026 |
| _operateur/optimus-prime/super-combos/sc-002-auto-evolution/main.py | 07:49:27 | 16/09/2026 |
| matrice/data/frictions.db | 07:49:27 | 16/09/2026 |
| _operateur/optimus-prime/espions/registre/registre.json | 07:49:28 | 16/09/2026 |

## Encart : lecons

Flux : lecons gravees -> bdd-lecons -> lecons.json -> VUE (relues a chaque injection)

| Entree | Heure | Date |
|---|---|---|
| L-104 Un balayage ne doit JAMAIS porter le filtre qui cache son perimetre : en MO-126 j'avais exclu 'bdd-f | 07:41:58 | 16/09/2026 |
| L-105 Un test qui peut ECRIRE finira par ecrire : dans mes cobayes MO-124/126/127/130 j'avais remplace le  | 07:47:45 | 16/09/2026 |
| L-106 Une forme produite par une porte se declare a la porte qui la PRODUIT, et tout consommateur la CONSO | 08:31:07 | 16/09/2026 |
| L-107 Une CLASSE de defaut se ferme par un OUTIL qui la MESURE, jamais par le cas qu'on vient de reparer : | 08:37:56 | 16/09/2026 |
| L-108 Une BDD SCELLEE par une empreinte a UN SEUL ECRIVAIN : la porte qui la possede. Un consommateur qui  | 08:38:41 | 16/09/2026 |

## Encart : variables

Flux : machine-defcon / pause-session / bdd-variables -> classeur-variables.json -> VUE

| Entree | Heure | Date |
|---|---|---|
| veille-intervalle = 600 | 16:19:00 | 06/09/2026 |
| defcon = 2 | 07:33:10 | 09/09/2026 |
| perimetre-cameleon = maintenance,_operateur,pilote/file-missions.json,data/historiques-missions.jsonl,data/modifications-par-fichier.json,data/usages-outils-combos.jsonl,data/activites-recentes.json,data/defcon-historique.jsonl,data/classeur-variables.json,data/manuel-outils.md,journal-multi-encarts.md,matrice-readme.md,routines/routines-readme.md,routines/vie/DESCRIPTION.md,routines/espion-integrite,intercom/pilote/outbox.jsonl,intercom/matrice/inbox.jsonl,docs/IMPERATIF.md,templates/theme-bdd/README.md,data/outils/pause-session,data/outils/machine-defcon,data/outils/verifier-regles,data/outils/verifier-protocoles,data/outils/verifier-conventions | 07:43:10 | 15/09/2026 |
