# Porte `injection/` -- injections du pilote cameleon

> **Un seul dossier d'injection.** Le dossier `injections/` (moteur de catalogue
> parallelle, ne le 2026-09-12, jamais committe) a ete **fusionne ici** le
> 2026-09-13 : deux dossiers dont le nom ne differait que d'un `s` etaient un
> piege (deux *namespace packages* voisins, aucun `__init__.py`). Le nom qui fait
> foi est celui de l'architecture officielle (`DESCRIPTION.md`) : `injection/`.

## Les 6 pieces de la porte

| Piece | Role |
|---|---|
| `entry.py` | la porte : verbes `statut`, `injecter`, `enchainer` (et `mission --action`) |
| `cycle.py` | le **cycle** : orchestre les injections par phase (`demarrer`, `mission_debut/pendant/fin`) |
| `fonctions.py` | l'injection de **mission** : ordonnee, filtree L-016, pesee en tokens, deposee dans l'outbox intercom |
| `injecter.py` | le **moteur du catalogue** : sert les injections de DEMARRAGE et de PHASE |
| `config.json` | le **catalogue** : quelles sources, pour quelle phase, obligatoires ou non |
| `README.md` | ce fichier |

## Qui appelle quoi (le vrai cablage)

```
python main.py injecter                     <- ORDRE 2 de demarrer-cameleon.md
  -> injection/entry.py  (verbe injecter)
     -> injection/cycle.py (CycleCameleon.demarrer)
        -> injection/injecter.py demarrage  <- le CATALOGUE (fiche + doc matrice)
     -> injection/fonctions.py (preparer_injection)
        -> l'injection de MISSION dans l'outbox intercom
```

## Lancer le catalogue directement

```bash
python injection/injecter.py --categories            # la liste vient du CATALOGUE
python injection/injecter.py demarrage               # fiche d'identite + doc de la Matrice
python injection/injecter.py demarrage --format json
python injection/injecter.py mission                 # les 3 phases d'un coup
```

## Doctrine : aucune degradation silencieuse (2026-09-13)

| Cas | Comportement |
|---|---|
| source absente, `"obligatoire": true` | **REFUS nomme**, code 2 |
| source absente, `"obligatoire": false` | **ALERTE nommee**, code 0 (on continue) |
| `"obligatoire"` non declare | traite comme **obligatoire** (prudence) + alerte |
| `type` inconnu du moteur | **REFUS nomme**, code 2 |
| `section` demandee et introuvable | **REFUS nomme**, code 2 |
| categorie absente du catalogue | **REFUS nomme**, code 2 |
| filtre `categorie` qui vide le contenu | **ALERTE nommee** (contenu vide signale, jamais muet) |

Types servis : `fichier`, `json`, `bdd`, `dossier`, `outil` (fichier lu, dossier liste).
Les **categories viennent du catalogue** : aucune liste en dur dans le moteur.

> Regle gravee : `ORDRE 2` dit "RIEN ne commence avant cette relecture complete".
> Une source obligatoire absente doit donc **crier**, jamais imprimer un contenu vide.
> (Avant le 2026-09-13, elle imprimait `[FICHIER INTRUVABLE: ...]` et rendait code 0.)

## Ce que ce catalogue ne fait PAS

Il ne touche ni la file des missions, ni les statuts, ni les tokens : c'est
`fonctions.py` qui s'en charge (serie stricte, pause, tresse, poids). Le
catalogue **sert du contexte**, il ne decide rien.
