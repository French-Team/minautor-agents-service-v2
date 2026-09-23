# OUTIL -- lister

> Porte unique de listage (MO-003). Remplace `glob` + `list_directory` natifs (pas de perimetre, pas de tri, expose _operateur) par 1 porte filtree, triee, deterministe.

## Verbes

```
python3 cerveau-projet/matrix/lancer.py lister lister --dossier <chemin> [--filtre <glob>] [--recursif] [--json]
```

- `--dossier` : dossier a lister (relatif a la racine, detectee par `data/commun/racine.py`).
- `--filtre` : filtre glob (ex `*.py`, `*.json`, `*.md`). Sans filtre : tout.
- `--recursif` : descend dans les sous-dossiers (rglob tri mtime).
- `--json` : sortie machine JSON (chemins + mtime + taille).

## Garanties (pourquoi meilleur que le natif)

| Natif | lister (ameliore) |
|---|---|
| `glob` sans perimetre (peut lister `_operateur`) | **Perimetre `matrix/` seul** (allowlist `AGENTS.md`/`demarrer-*.md`), hors = code 2 |
| `list_directory` expose structure privee | **Filtre L-016** : zones `_operateur/tmp-optimus/suivi-optimus` exclues (0 fuite) |
| Pas de tri deterministe | **Tri mtime** (puis nom) deterministe |
| Pas de filtre hors glob | **1 porte** couvre `glob+list_directory` (`--filtre` + `--recursif`) |
| Pas de JSON | **`--json` machine** |
| Expose `__pycache__/.git` | **Exclus `__pycache__/.git`** |

## Architecture

| Piece | Role |
|---|---|
| `main.py` | DIRIGE (parser, router) |
| `constants.py` | chemins, allowlist, zones invisibles L-016 |
| `commun.py` | fonctions communes : perimetre, listage, tri, L-016 |
| `lister/` | categorie lister : `entry.py` orchestre, `fonctions.py` fait |

## Protections

- Perimetre `matrix/` seul -- hors = code 2.
- Dossier absent = code 1, pas un dossier = code 1.
- `__pycache__/.git` toujours exclus.
- Zones L-016 exclues si presentes sur le chemin.

## Benchmark (critere GO MO-003)

- `matrix/` complet recursif : <100ms pour 400 fichiers (tri mtime).
- `audit-invisibilite` 0 fuite.
