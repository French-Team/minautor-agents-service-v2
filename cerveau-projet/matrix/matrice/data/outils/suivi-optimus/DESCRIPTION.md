# OUTIL -- suivi-optimus

> Outil Python dedie a la trace `data/suivi-optimus.jsonl` (M-084, GO createur).
> La trace note L'AGENT (optimus-prime), jamais les outils : decisions, portes,
> missions -- le POURQUOI. Le sac-a-dos note les OUTILS (invocations, codes,
> durees) : les deux ne se recouvrent pas.

## Options

```
python main.py noter --mission M-XXX --theme SUIVI --action <action> --detail "..."
                     [--fichiers "a,b"] [--portes "a,b"] [--duree-s N]
python main.py lire [--mission M] [--action <action>] [--n N]
python main.py verifier
python main.py vue   (genere la vue markdown dediee matrice/suivi-optimus.md)
```

- `--action` : action fermee (enum, voir constants.py) -- obligatoire.
- `--detail` : le contenu de l'evenement (obligatoire).
- `--mission` / `--theme` : contexte de la mission (facultatif).
- `--fichiers` / `--portes` : listes separees par des virgules (facultatif).
- `--duree-s` : duree en secondes (facultatif).
- `lire --n N` : les N derniers evenements (tous si absent).

## Actions fermees (declencheurs d'entree)

| Action | Declencheur |
|---|---|
| `debut` | debut de mission |
| `fin` | fin de mission avec bilan |
| `porte` | porte officielle utilisee (pilote, lot, tresse, defcon, pause/reprise) |
| `depot` | mission deposee au vrac de l'entonnoir (E-XXX) |
| `decision` | GO / arbitrage du createur |
| `decouverte` | constat d'audit interne (ex : angle mort detecte) |
| `bilan` | bilan-periode demande et rendu |

PAS d'entree par fichier edite : bdd-modifications couvre ce niveau (doublon interdit).

## Format de la BDD

Une ligne JSON par evenement (journal en AJOUT SEUL, jamais reecrit) :
`{"date", "mission", "theme", "action", "detail", "fichiers[]", "portes[]", "duree_s"}`
Plus un etalon `suivi-optimus.jsonl.sha256` (empreinte recalculee a chaque ajout).

## Architecture (convention-architecture-outils)

| Piece | Role |
|---|---|
| DESCRIPTION.md | la facade (ce fichier) |
| main.py | point d'entree global : DIRIGE |
| constants.py | chemins, enum fermee des actions |
| commun.py | fonctions communes : lire, ajouter (atomique, LF), empreinte, options |
| noter/ | noter un evenement (action fermee) |
| lire/ | lister (tout ou par mission/action, n derniers) |
| vue/ | generer la vue markdown dediee (matrice/suivi-optimus.md) |
| verifier/ | integrite SHA-256 (etalon-or) |

## Protections

- Journal append-only : ajout atomique (tmp + remplacement), LF forcees.
- Empreinte SHA-256 recalculee A CHAQUE ajout, etalon surveille par l'espion.
- Action fermee : toute action hors enum refusee (code 2).
- Etancheite : le cameleon n'accede JAMAIS a cette trace (zone exclue de son perimetre).