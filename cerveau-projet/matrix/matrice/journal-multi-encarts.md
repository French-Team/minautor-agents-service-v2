# Journal multi-encarts de la Matrice (v3)

> VISUEL GENERE depuis les BDD -- jamais edite a la main (E-049).
> Regenerer : python main.py construire

## Encart : matrice

Flux : classeur-variables.json + fichiers PID des boucles -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| defcon : 2 | 07:33:10 | 09/09/2026 |
| veille-flux : ACTIVE (PID 17656) | 09:18:59 | 09/09/2026 |
| espion-integrite : ACTIVE (PID 8940) | 19:42:44 | 09/09/2026 |

## Encart : missions

Flux : pilote/file-missions.json + pilote/entonnoir-files.json -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
(aucune entree)

## Encart : routines

Flux : routines/veille-flux/journal-veille.txt -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| passe relax terminee : 0 detection(s), 0 alerte(s) | 21:20:32 | 09/09/2026 |
| passe relax demarree | 21:25:32 | 09/09/2026 |
| passe relax terminee : 0 detection(s), 0 alerte(s) | 21:25:33 | 09/09/2026 |
| passe relax demarree | 21:30:33 | 09/09/2026 |
| passe relax terminee : 0 detection(s), 0 alerte(s) | 21:30:34 | 09/09/2026 |

## Encart : alertes

Flux : veille-flux/alertes-emises.json + intercom/matrice/inbox.jsonl -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| intercom : fin-mission | 09:23:16 | 09/09/2026 |
| intercom : fin-mission | 09:42:29 | 09/09/2026 |
| intercom : fin-mission | 09:59:26 | 09/09/2026 |
| intercom : fin-mission | 19:44:04 | 09/09/2026 |
| intercom : retour-lot | 19:44:04 | 09/09/2026 |

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
| machine-defcon/- code 2 0ms | 21:30:27 | 09/09/2026 |
| pause-session/etat code 0 0ms | 21:30:27 | 09/09/2026 |
| corriger-ascii/corriger code 1 83ms | 21:30:33 | 09/09/2026 |
| veille-flux/passe-relax code 0 493ms | 21:30:34 | 09/09/2026 |
| bdd-activites/noter code 0 1ms | 21:30:34 | 09/09/2026 |
| verifier-regles/verifier code 0 2ms | 21:30:42 | 09/09/2026 |
| verifier-protocoles/verifier code 0 2ms | 21:30:47 | 09/09/2026 |
| verifier-conventions/verifier code 0 2ms | 21:30:47 | 09/09/2026 |

## Encart : modifications

Flux : notes de mission -> bdd-modifications -> modifications-par-fichier.json -> VUE

| Entree | Heure | Date |
|---|---|---|
| matrice/data/conventions-matrice.json | 20:33:40 | 09/09/2026 |
| matrice/data/outils/journal-multi-encarts | 20:33:40 | 09/09/2026 |
| matrice/data/outils/suivi-optimus | 20:33:40 | 09/09/2026 |
| matrice/data/outils/{bdd-regles-matrice,theme-vivier,bdd-lecons} | 20:33:40 | 09/09/2026 |
| matrice/suivi-optimus.md | 20:33:40 | 09/09/2026 |

## Encart : lecons

Flux : lecons gravees -> bdd-lecons -> lecons.json -> VUE (relues a chaque injection)

| Entree | Heure | Date |
|---|---|---|
| L-012 Un processus vivant garde le code de son lancement : toute boucle (veille, espion) dont le code a et | 08:47:33 | 07/09/2026 |
| L-013 Ne JAMAIS compter les chemins a la main (cd ../../x) : utiliser la racine DETECTEE par remontee jusq | 19:54:17 | 07/09/2026 |
| L-014 La Matrice gere ENTIEREMENT l'agent unique cameleon : il vit dans matrix/agents/cameleon (session-ma | 21:02:48 | 07/09/2026 |
| L-015 Tester une branche d'incident (TimeoutExpired) sur le VRAI journal append-only = violation du contra | 07:17:25 | 08/09/2026 |
| L-016 Philosophie d'invisibilite : si un acteur est invisible aux yeux d'un autre, il ne doit JAMAIS etre  | 20:15:38 | 09/09/2026 |

## Encart : variables

Flux : machine-defcon / pause-session / bdd-variables -> classeur-variables.json -> VUE

| Entree | Heure | Date |
|---|---|---|
| veille-intervalle = 600 | 16:19:00 | 06/09/2026 |
| defcon = 2 | 07:33:10 | 09/09/2026 |
| perimetre-cameleon = maintenance,_operateur,pilote/file-missions.json,data/historiques-missions.jsonl,data/modifications-par-fichier.json,data/usages-outils-combos.jsonl,data/activites-recentes.json,data/defcon-historique.jsonl,data/classeur-variables.json,data/manuel-outils.md,journal-multi-encarts.md,matrice-readme.md,routines/routines-readme.md,routines/vie/DESCRIPTION.md,routines/espion-integrite,intercom/pilote/outbox.jsonl,intercom/matrice/inbox.jsonl,docs/IMPERATIF.md,templates/theme-bdd/README.md,data/outils/pause-session,data/outils/machine-defcon,data/outils/verifier-regles,data/outils/verifier-protocoles,data/outils/verifier-conventions | 21:30:07 | 09/09/2026 |
