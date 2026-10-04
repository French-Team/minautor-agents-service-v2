---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
---

# espions-optimus -- Surveillance de la zone Optimus par la Matrice

> La Matrice surveille Optimus comme elle surveille ses BDD : ces espions
> SIGNALENT, ils ne reparent jamais (la reparation passe par Optimus).
> Decide par le createur (M-111) : la zone `_operateur/optimus-prime/`
> est la seule qui n etait couverte par aucun espion.

## Espions

| Espion | Role | Commande |
|---|---|---|
| integrite | Empreintes SHA des fichiers zone Optimus (detection de modification hors BDD) | `python3 cerveau-projet/matrix/_operateur/optimus-prime/espions/espion-integrite-optimus.py enregistrer` / `verifier` |
| activite | File missions Optimus, frictions actives, verrous BDD non liberes | `python3 cerveau-projet/matrix/_operateur/optimus-prime/espions/espion-activite-optimus.py` |
| tracebacks | Tracebacks et exceptions des outils (scan statique + run dynamique) | `python3 cerveau-projet/matrix/_operateur/optimus-prime/espions/espion-tracebacks-optimus.py tour` |
| sondes | Les sondes de l AGENT : commande, code, et si un traceback en est sorti (axe B) | `python3 cerveau-projet/matrix/_operateur/optimus-prime/espions/espion-sondes-optimus.py executer -- <commande...>` / `rapport` / `auto-test` |

## Registre

`registre/registre.json` : empreintes de reference + date de pose.
Mis a jour par `enregistrer` APRES chaque evolution auto-validee.

## Registre des sondes (espion sondes)

`registre/sondes.jsonl` : une ligne par sonde -- date, commande, code, `traceback`
(oui/non), signature, duree, et la PILE quand il y en a une (tronquee, et DITE
tronquee). Deux apps :

1. LA MESURE (axe B) : `rapport` rend le TAUX de sondes qui ont rendu un traceback
   et le detail par famille de commande. Mesure du 2026-09-23 : 10 sondes notees,
   8 tracebacks = 80 % (python3 8/8 ; grep 0/1 ; cat 0/1).
2. LE REMEDE : une sonde qui plante REND UNE LIGNE (`SONDE EN ECHEC ... : <type>`),
   jamais la pile en console -- le createur ne peut plus confondre une sonde et une
   panne. La pile reste lisible au registre, et le code rendu est 3 (distinct d un
   refus), pour qu un plantage ne se lise jamais comme un refus ordinaire.

PORTEE, DITE AUSSI PAR LE RAPPORT : l espion ne voit QUE les sondes qui passent par
lui. Un registre vide ne dit pas < aucune sonde >, il dit < aucune sonde NOTEE >.

## Zones surveillees (dans `_operateur/optimus-prime/`)

parcours/, protocoles/, conventions/, regles-immuables/,
super-combos/combos/outils/*.py, optimus-prime.md
(docs internes exclus : .bak, __pycache__)
