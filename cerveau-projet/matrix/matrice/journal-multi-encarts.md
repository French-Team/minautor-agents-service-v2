---
identite:
  type: journal
  appartient_a: matrice
  commun: true
  liens: matrice/data/outils/journal-multi-encarts/main.py, matrice/data/outils/journal-multi-encarts/construire/entry.py
---

# Journal multi-encarts de la Matrice (v3)

> VISUEL GENERE depuis les BDD -- jamais edite a la main (E-049).
> Regenerer : python main.py construire

## Encart : matrice

Flux : classeur-variables.json + fichiers PID des boucles -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| defcon : 2 | 07:33:10 | 09/09/2026 |
| veille-flux : ARRET |  |  |
| espion-integrite : ARRET |  |  |

## Encart : missions

Flux : pilote/file-missions.json + pilote/entonnoir-files.json -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
(aucune entree)

## Encart : routines

Flux : routines/veille-flux/journal-veille.txt -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| passe relax demarree | 18:48:55 | 04/10/2026 |
| passe relax terminee : 0 detection(s), 0 alerte(s) | 18:49:05 | 04/10/2026 |
| passe relax demarree | 18:54:08 | 04/10/2026 |
| passe relax terminee : 0 detection(s), 0 alerte(s) | 18:54:19 | 04/10/2026 |
| passe relax demarree | 18:59:23 | 04/10/2026 |

## Encart : alertes

Flux : veille-flux/alertes-emises.json + intercom/matrice/inbox.jsonl -> VUE lecture seule

| Entree | Heure | Date |
|---|---|---|
| intercom : signaler | 17:52:37 | 04/10/2026 |
| intercom : signaler | 18:08:18 | 04/10/2026 |
| intercom : signaler | 18:23:59 | 04/10/2026 |
| intercom : signaler | 18:39:40 | 04/10/2026 |
| intercom : signaler | 18:55:21 | 04/10/2026 |

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
| rendre-graphe/svg code 0 2ms | 18:58:36 | 04/10/2026 |
| rendre-graphe/mermaid code 0 8ms | 18:58:36 | 04/10/2026 |
| rendre-graphe/svg code 0 9ms | 18:58:36 | 04/10/2026 |
| rendre-graphe/verifier code 0 1ms | 18:58:36 | 04/10/2026 |
| suivi-optimus/coherence code 1 24ms | 18:58:38 | 04/10/2026 |
| suivi-optimus/coherence code 1 24ms | 18:58:38 | 04/10/2026 |
| suivi-optimus/vue code 0 50ms | 18:59:23 | 04/10/2026 |
| corriger-ascii/corriger code 0 1001ms | 18:59:24 | 04/10/2026 |

## Encart : modifications

Flux : notes de mission -> bdd-modifications -> modifications-par-fichier.json -> VUE

| Entree | Heure | Date |
|---|---|---|
| _operateur/optimus-prime/preparation/mo-583-cadrage-cartes-liens.md | 18:41:36 | 04/10/2026 |
| _operateur/optimus-prime/preparation/mo-584-cadrage-depot-git.md | 18:53:20 | 04/10/2026 |
| _operateur/optimus-prime/preparation/mo-585-doublon-naissance.md | 18:56:36 | 04/10/2026 |
| .gitignore |  |  |
| x |  |  |

## Encart : lecons

Flux : lecons gravees -> bdd-lecons -> lecons.json -> VUE (relues a chaque injection)

| Entree | Heure | Date |
|---|---|---|
| L-237 UN TEMOIN QUI NE CONNAIT PAS LE NOUVEAU TIRVOIR CRIE A TORT, ET IL A RAISON DE CRIER. Le solder des  | 11:19:34 | 04/10/2026 |
| L-238 LE CONTROLE QU ON ECRIT POUR UN AUTRE SE RETOURNE CONTRE SOI. Le nouveau controle d ancrage a accuse | 11:19:34 | 04/10/2026 |
| L-239 UN GARDE QUI ACCUSE UN ETAT REELLEMENT INTERDIT N EST PAS UNE PANNE DU GARDE : C EST UN ETAT A RAMEN | 14:19:00 | 04/10/2026 |
| L-240 Reconstruire un depot git : le remote est une donnee, pas une page blanche. Avant tout rm -rf .git,  | 17:45:21 | 04/10/2026 |
| L-241 Un blocage de la veille n'est pas forcement un defaut du code : REPRODUIRE par le CHEMIN DU PRODUCTE | 18:01:38 | 04/10/2026 |

## Encart : variables

Flux : machine-defcon / pause-session / bdd-variables -> classeur-variables.json -> VUE

| Entree | Heure | Date |
|---|---|---|
| veille-intervalle = 600 | 16:19:00 | 06/09/2026 |
| defcon = 2 | 07:33:10 | 09/09/2026 |
| perimetre-cameleon = maintenance,_operateur,pilote/file-missions.json,data/historiques-missions.jsonl,data/modifications-par-fichier.json,data/usages-outils-combos.jsonl,data/activites-recentes.json,data/defcon-historique.jsonl,data/classeur-variables.json,data/manuel-outils.md,journal-multi-encarts.md,matrice-readme.md,routines/routines-readme.md,routines/vie/DESCRIPTION.md,routines/espion-integrite,intercom/pilote/outbox.jsonl,intercom/matrice/inbox.jsonl,docs/IMPERATIF.md,templates/theme-bdd/README.md,data/outils/pause-session,data/outils/machine-defcon,data/outils/verifier-regles,data/outils/verifier-protocoles,data/outils/verifier-conventions,data/lecons.json,data/sessions.json | 07:39:10 | 17/09/2026 |
| interpreteur-python = runtime/python.exe | 11:43:09 | 04/10/2026 |
