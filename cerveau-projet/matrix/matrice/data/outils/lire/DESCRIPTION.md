---
identite:
  type: outil
  appartient_a: matrice-data-outils
  commun: true
---

# OUTIL -- lire -- porte unique de lecture, annoncee et verifiee

> Porte unique de lecture (M-132 / MO-001). Remplace `read_files` natif (troncature silencieuse 2000 lignes) par une lecture annoncee, verifiee, 2e canal.
> Lecture seule, jamais d'ecriture. Tout fichier lu est dans `matrix/` (perimetre), sauf `AGENTS.md` et `demarrer-*.md` a la racine (allowlist).

## Verbes

```
python3 cerveau-projet/matrix/lancer.py lire lire --fichier <chemin> [--lignes <debut:fin>] [--hash] [--tete auto|<N>]
python3 cerveau-projet/matrix/lancer.py lire lire --fichiers <chemin1,chemin2> [--lignes <debut:fin>] [--hash]
python3 cerveau-projet/matrix/lancer.py lire lire --dossier <chemin> [--filtre <glob>] [--recursif] [--hash]
```

- `--fichier` : 1 fichier (relatif a la racine du workspace, detectee par `data/commun/racine.py`).
- `--fichiers` : N fichiers separes par virgules (ordre preserve, 1 passe).
- `--dossier` : dossier a lister+lire (mode batch, tri mtime).
- `--lignes` : tranche `debut:fin` (1-indexe, inclusif, ex `1:200`, `2001:4000`). Sans cette option : tout le fichier.
- `--tete` : demande la TETE du fichier, pas un nombre de lignes. `auto` la MESURE
  (front matter + premier chapitre, docstring de module, ou declarations d ouverture) ;
  `<N>` garde la forme historique. Elle PRIME sur `--lignes`. Une valeur qui n est ni
  `auto` ni un entier positif est REFUSEE (code 2). Voir `Tete de lecture` plus bas.
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

## Tete de lecture (`--tete`)

Trois formes sont reconnues, et chacune est une MESURE, pas une devine :

| Forme | Ce qu elle rend | Mesure sur le corpus |
|---|---|---|
| `front-matter` | le bloc `---`, le titre et son chapeau | canal : 15/271 lignes |
| `chapitre` | titre + chapeau d un `.md` sans carte | `DESCRIPTION.md` : 12/59 |
| `docstring` | le docstring de tete d un module | `commun.py` : 16/270 |
| `declarations` | commentaires et imports d ouverture (module sans docstring) | `passerelle_user.py` : 53/264 |

Une tete rendue ENTIERE s annonce `TETE COMPLETE (--tete auto)`, jamais `TRONQUE` :
annoncer une troncature renverrait l appelant chercher la suite d une tete qui est finie.

Une FORME INCONNUE (un `.json`, un fichier sans marqueur) ne rend pas le fichier entier
en silence : elle rend `TETE_INCONNUE` lignes (constante de `constants.py`) et le DIT --
mesure du 2026-09-30 : `--tete auto` sur `conventions-matrice.json` rendait 205/205 lignes
et l annonce ne disait rien. Un appel qui croit avoir lu une tete avait lu le complet.

## Benchmark (critere GO MO-001)

- Fichier 5000 lignes : lu complet `5000/5000` (<50ms), vs natif qui tronque a 2000 sans alerte.
- Fichier 1000 lignes, tranche `1:50` : annonce `1000 total, 50 lus (1:50)`.
