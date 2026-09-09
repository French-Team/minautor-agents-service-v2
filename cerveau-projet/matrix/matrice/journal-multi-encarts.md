# Journal multi-encarts de la Matrice (v3)

> VISUEL GENERE depuis les BDD -- jamais edite a la main (E-049).
> Regenerer : python main.py construire

## Encart : matrice

Flux : classeur-variables.json + fichiers PID des boucles -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| defcon : 2 | 07:33:10 | 09/09/2026 |
| veille-flux : ACTIVE (PID 17656) | 09:18:59 | 09/09/2026 |
| espion-integrite : ACTIVE (PID 10436) | 07:51:27 | 09/09/2026 |

## Encart : missions

Flux : pilote/file-missions.json + pilote/entonnoir-files.json -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| EN COURS M-084 -- SUIVI-OPTIMUS | 09:59:26 | 09/09/2026 |
| vrac : 1 mission(s) (E-057) | 09:57:08 | 09/09/2026 |

## Encart : routines

Flux : routines/veille-flux/journal-veille.txt -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| passe relax terminee : 0 detection(s), 0 alerte(s) | 19:25:17 | 09/09/2026 |
| passe relax demarree | 19:30:17 | 09/09/2026 |
| passe relax terminee : 0 detection(s), 0 alerte(s) | 19:30:18 | 09/09/2026 |
| passe relax demarree | 19:35:18 | 09/09/2026 |
| passe relax terminee : 0 detection(s), 0 alerte(s) | 19:35:18 | 09/09/2026 |

## Encart : alertes

Flux : veille-flux/alertes-emises.json + intercom/matrice/inbox.jsonl -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| intercom : fin-mission | 09:54:19 | 08/09/2026 |
| intercom : fin-mission | 08:27:41 | 09/09/2026 |
| intercom : fin-mission | 09:23:16 | 09/09/2026 |
| intercom : fin-mission | 09:42:29 | 09/09/2026 |
| intercom : fin-mission | 09:59:26 | 09/09/2026 |

## Encart : cameleon

Flux : intercom/cameleon/inbox.jsonl (ecrit par pause-session) -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| pause -- mission M-080 | 07:31:42 | 09/09/2026 |
| reprise -- mission M-080 | 07:32:07 | 09/09/2026 |
| pause -- mission M-080 | 07:32:53 | 09/09/2026 |
| reprise -- mission M-080 | 07:33:09 | 09/09/2026 |

## Encart : optimus

Flux : suivi-optimus.jsonl (ecrit par optimus via l'outil suivi-optimus, jamais le cameleon) -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| decision \| M-084 \| GO createur : construire suivi-optimus | 19:35:29 | 09/09/2026 |

## Encart : usages

Flux : sac-a-dos (chaque outil) -> bdd-usages -> usages-outils-combos.jsonl -> VUE

| Entree | Heure | Date |
|---|---|---|
| suivi-optimus/noter code 2 0ms | 19:35:29 | 09/09/2026 |
| suivi-optimus/lire code 0 0ms | 19:35:29 | 09/09/2026 |
| suivi-optimus/lire code 0 0ms | 19:35:29 | 09/09/2026 |
| suivi-optimus/verifier code 0 0ms | 19:35:30 | 09/09/2026 |
| pause-session/perimetre code 0 2ms | 19:35:58 | 09/09/2026 |
| pause-session/etat code 0 0ms | 19:35:58 | 09/09/2026 |
| journal-multi-encarts/construire code 0 10ms | 19:35:59 | 09/09/2026 |
| journal-multi-encarts/lire code 0 0ms | 19:35:59 | 09/09/2026 |

## Encart : modifications

Flux : notes de mission -> bdd-modifications -> modifications-par-fichier.json -> VUE

| Entree | Heure | Date |
|---|---|---|
| routines/vie/fonctions.py + activer.py | 09:21:34 | 09/09/2026 |
| routines/vie/server_matrice.py + server/entry.py | 09:21:34 | 09/09/2026 |
| data/outils/bdd-regles-matrice/ + bdd-conventions-matrice/ + bdd-protocoles-matrice/ | 09:34:26 | 09/09/2026 |
| matrice-readme.md + agents/cameleon/cameleon.md | 09:34:26 | 09/09/2026 |
| data/bdd-theme-vivier.json | 09:57:43 | 09/09/2026 |

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
| perimetre-cameleon = suivi-optimus | 19:35:58 | 09/09/2026 |
