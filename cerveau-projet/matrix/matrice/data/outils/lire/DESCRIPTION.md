# OUTIL -- lire

> Porte unique de lecture (M-132 / MO-001). Remplace `read_files` natif (troncature silencieuse 2000 lignes) par une lecture annoncee, verifiee, 2e canal.
> Lecture seule, jamais d'ecriture. Tout fichier lu est dans `matrix/` (perimetre), sauf `AGENTS.md` et `demarrer-*.md` a la racine (allowlist).

## Verbes

```
python main.py lire --fichier <chemin> [--lignes <debut:fin>] [--hash]
python main.py lire --fichiers <chemin1,chemin2> [--lignes <debut:fin>] [--hash]
python main.py lire --dossier <chemin> [--filtre <glob>] [--recursif] [--hash]
```

- `--fichier` : 1 fichier (relatif a la racine du workspace, detectee par `data/commun/racine.py`).
- `--fichiers` : N fichiers separes par virgules (ordre preserve, 1 passe).
- `--dossier` : dossier a lister+lire (mode batch, tri mtime).
- `--lignes` : tranche `debut:fin` (1-indexe, inclusif, ex `1:200`, `2001:4000`). Sans cette option : tout le fichier.
- `--hash` : affiche le SHA-256 (hex, 64 chars) du fichier complet (pas de la tranche).
- `--filtre` : filtre glob pour `--dossier` (ex `*.py`, `*.json`).
- `--recursif` : avec `--dossier`, descend dans les sous-dossiers.

## Garanties (pourquoi meilleur que le natif)

| Natif | lire (ameliore) |
|---|---|
| Troncature 2000 lignes silencieuse | **Annonce** `total/lu` a chaque lecture (`L-001` style) ; jamais silencieux |
| Pas de SHA | `--hash` : SHA-256 du fichier complet (preuve disque) |
| Pas de verif encodage | Detecte BOM, line-ends (`LF/CRLF`), non-UTF8 signale (pas de crash) |
| Divergence 2 canaux (L-009) | **2e canal** : relecture systeme `read_bytes` + `read_text` croisee si doute |
| Pas de perimetre | Refuse hors `matrix/` (sauf allowlist racine) ; code 2 + message explicite |
| Divergent (N fichiers, ordre aleatoire) | Ordre preserve, tri mtime si `--dossier`, sortie deterministe |

## Architecture

| Piece | Role |
|---|---|
| `main.py` | DIRIGE (parser, router) |
| `constants.py` | chemins, limites, allowlist |
| `commun.py` | fonctions communes : perimetre, lecture, SHA, tranche |
| `lire/` | categorie lire : `entry.py` orchestre, `fonctions.py` fait |

## Protections

- Lecture seule : jamais d'ecriture, jamais de tmp, jamais d'empreinte.
- Perimetre `matrix/` seul (allowlist : `AGENTS.md`, `demarrer-*.md`) -- hors perimetre = code 2.
- Fichier absent = code 1 + message, pas de crash.
- Tranche hors-bornes = Tronquee a `total`, annoncee.

## Benchmark (critere GO MO-001)

- Fichier 5000 lignes : lu complet `5000/5000` (<50ms), vs natif qui tronque a 2000 sans alerte.
- Fichier 1000 lignes, tranche `1:50` : annonce `1000 total, 50 lus (1:50)`.
