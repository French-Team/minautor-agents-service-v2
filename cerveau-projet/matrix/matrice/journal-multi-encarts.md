# Journal multi-encarts de la Matrice (v3)

> VISUEL GENERE depuis les BDD -- jamais edite a la main (E-049).
> Regenerer : python main.py construire

## Encart : matrice

Flux : classeur-variables.json + fichiers PID des boucles -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| defcon : 2 | 07:33:10 | 09/09/2026 |
| veille-flux : ACTIVE (PID 13376) | 07:14:49 | 08/09/2026 |
| espion-integrite : ACTIVE (PID 10436) | 07:51:27 | 09/09/2026 |

## Encart : missions

Flux : pilote/file-missions.json + pilote/entonnoir-files.json -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| vrac : 4 mission(s) (E-051, E-054, E-055, E-056) | 08:21:45 | 09/09/2026 |

## Encart : routines

Flux : routines/veille-flux/journal-veille.txt -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| passe relax terminee : 0 detection(s), 0 alerte(s) | 08:20:22 | 09/09/2026 |
| passe relax demarree | 08:23:37 | 09/09/2026 |
| passe relax terminee : 0 detection(s), 0 alerte(s) | 08:23:38 | 09/09/2026 |
| passe relax demarree | 08:25:24 | 09/09/2026 |
| passe relax terminee : 0 detection(s), 0 alerte(s) | 08:25:27 | 09/09/2026 |

## Encart : alertes

Flux : veille-flux/alertes-emises.json + intercom/matrice/inbox.jsonl -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| intercom : fin-mission | 22:48:20 | 07/09/2026 |
| intercom : fin-mission | 23:03:18 | 07/09/2026 |
| intercom : fin-mission | 07:25:26 | 08/09/2026 |
| intercom : fin-mission | 09:54:19 | 08/09/2026 |
| intercom : fin-mission | 08:27:41 | 09/09/2026 |

## Encart : cameleon

Flux : intercom/cameleon/inbox.jsonl (ecrit par pause-session) -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| pause -- mission M-080 | 07:31:42 | 09/09/2026 |
| reprise -- mission M-080 | 07:32:07 | 09/09/2026 |
| pause -- mission M-080 | 07:32:53 | 09/09/2026 |
| reprise -- mission M-080 | 07:33:09 | 09/09/2026 |

## Encart : usages

Flux : sac-a-dos (chaque outil) -> bdd-usages -> usages-outils-combos.jsonl -> VUE

| Entree | Heure | Date |
|---|---|---|
| corriger-ascii/corriger code 1 70ms | 08:25:25 | 09/09/2026 |
| veille-flux/passe-relax code 0 2279ms | 08:25:28 | 09/09/2026 |
| bdd-activites/noter code 0 1ms | 08:25:29 | 09/09/2026 |
| journal-multi-encarts/construire code 0 10ms | 08:26:09 | 09/09/2026 |
| bdd-modifications/noter code 0 3ms | 08:27:04 | 09/09/2026 |
| bdd-modifications/noter code 0 3ms | 08:27:04 | 09/09/2026 |
| bdd-modifications/noter code 0 3ms | 08:27:04 | 09/09/2026 |
| bdd-modifications/noter code 0 3ms | 08:27:05 | 09/09/2026 |

## Encart : modifications

Flux : notes de mission -> bdd-modifications -> modifications-par-fichier.json -> VUE

| Entree | Heure | Date |
|---|---|---|
| matrice/matrice-readme.md | 09:53:55 | 08/09/2026 |
| data/outils/journal-multi-encarts/ | 08:27:04 | 09/09/2026 |
| data/outils/pause-session/ | 08:27:04 | 09/09/2026 |
| pilote/commun.py + injection + fin | 08:27:04 | 09/09/2026 |
| data/outils/machine-defcon/monter/entry.py | 08:27:05 | 09/09/2026 |

## Encart : lecons

Flux : lecons gravees -> bdd-lecons -> lecons.json -> VUE (relues a chaque injection)

| Entree | Heure | Date |
|---|---|---|
| L-011 Un bilan ne peut affirmer qu'une preuve qui a COURU : les 2 tentatives 'file consommer' de M-019 ont | 17:59:14 | 06/09/2026 |
| L-012 Un processus vivant garde le code de son lancement : toute boucle (veille, espion) dont le code a et | 08:47:33 | 07/09/2026 |
| L-013 Ne JAMAIS compter les chemins a la main (cd ../../x) : utiliser la racine DETECTEE par remontee jusq | 19:54:17 | 07/09/2026 |
| L-014 La Matrice gere ENTIEREMENT l'agent unique cameleon : il vit dans matrix/agents/cameleon (session-ma | 21:02:48 | 07/09/2026 |
| L-015 Tester une branche d'incident (TimeoutExpired) sur le VRAI journal append-only = violation du contra | 07:17:25 | 08/09/2026 |

## Encart : variables

Flux : machine-defcon / pause-session / bdd-variables -> classeur-variables.json -> VUE

| Entree | Heure | Date |
|---|---|---|
| veille-intervalle = 600 | 16:19:00 | 06/09/2026 |
| defcon = 2 | 07:33:10 | 09/09/2026 |
| perimetre-cameleon = (perimetre complet : aucune zone exclue) | 07:32:33 | 09/09/2026 |
