# detecter-evaluations-incompletes

Scan ANTI-RECURRENCE apres correction d'une convention ou d'un pattern :
trouve les mentions residuelles d'un MOTIF dans les 4 sources documentaires
du cerveau-projet, pour garantir qu'une correction declaree est COMPLETE.

## Contexte

Lecon Themis du 2026-08-11 (re-audit convention cT*) : un re-audit qui ne
scanne que les fichiers modifies RATE les mentions residuelles dans les
sources voisines. Themis a du croiser a la main validateur, spec,
generateurs (.md/spec/code) et tests avec une fenetre de contexte. Cet
outil automatise exactement cette methode.

## Les 4 sources scannees

| Source | Chemin | Extensions |
|---|---|---|
| VALIDATEUR | cerveau-projet/agents/tools/valider/ | .py .md |
| SPEC | cerveau-projet/agents/tools/*/spec/ + docs-dev-cerveau-projet/ | .md |
| GENERATEURS | cerveau-projet/agents/tools/generateurs/ | .py .sh .md |
| TESTS | cerveau-projet/agents/tools/tester/tests/ | .py |

## Usage

    python3 cerveau-projet/agents/tools/detecter/detecter-evaluations-incompletes/detecter-evaluations-incompletes.py --motif <motif>
    python3 ... --motif cT1 --filtre cT --contexte 2
    python3 ... --motif <motif> --rapport rapport.md

## Options

| Option | Description |
|---|---|
| `--motif <regex>` | Motif a rechercher (obligatoire) |
| `--filtre <regex>` | Ne garder que les lignes contenant aussi ce filtre |
| `--contexte <n>` | Fenetre de lignes avant la mention (extrait du rapport) |
| `--rapport <fichier>` | Ecrire le rapport markdown (avec extraits de contexte) |
| `--verbose` | Detail des fichiers scannes |
| `--version` | Afficher la version |

## Exemples reels

- Versions figees : `--motif '0.2.9'` trouve les 9 mentions residuelles de
  la version du catalogue dans spec, tests, generateurs et validateur.
- Convention etendue : `--motif 'cT1([^0-9*]|$)'` trouve les mentions de
  l'ancienne convention SANS l'extension (residuelles), en distinguant les
  mentions conformes (`cT1`..`cT10`).

## Sortie

Par source : liste des mentions (chemin:ligne + extrait) + compteur.
Synthese : 0 mention = correction COMPLETE, sinon nombre.
Code de retour : 0 si aucune mention, 1 sinon.

## Version

- v0.1.0 : creation (2026-08-13). 4 sources, motif/filtre/contexte,
  rapport markdown.
