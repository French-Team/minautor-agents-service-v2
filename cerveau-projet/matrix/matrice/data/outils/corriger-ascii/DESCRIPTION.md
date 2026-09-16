# OUTIL corriger-ascii

> Outil de la Matrice (M-011, doctrine du createur) : le LLM ecrit avec des
> accents, la Matrice corrige en arriere-plan. Les petites erreurs mecaniques
> sont corrigees SANS interrompre le travail du LLM ; chaque correction est
> notee en BDD (porte unique, par le combo ou l'operateur).

## Ce qu'il fait

- Cible : fichiers `.md`, `.py`, `.json` des zones de la Matrice et de
  l'operateur (liste en constantes). Les `.jsonl` (journaux) et les fichiers
  sous etalon `.sha256` sont HORS CIBLE et RAPPORTES comme tels.
- Les `.json` sous etalon sont des BDD : ils sont hors champ de reecriture
  (jamais corriges, jamais touches) mais desormais COMPTES et NOMMES.
- Convertit les caracteres non-ASCII via la CARTE de conversion (constants.py) :
  e-accents -> e, a-accents -> a, c-cedille -> c, guillemets/apostrophes
  typographiques -> ASCII, tirets cadratins -> `-`, etc.
- Caractere non convertible par la carte : LAISSE TEL QUEL et signale
  (probleme plus grave -> decision humaine, jamais de perte de donnees).

## Protections fondamentales

- UN FICHIER SOUS ETALON `.sha256` N'EST JAMAIS REECRIT (les BDD empreintees
  sont intouchables : lecons, modifications...). Verifie AVANT toute ecriture.
- L'EXEMPTION EST VISIBLE (MO-075) : les fichiers hors du champ de reecriture
  (BDD sous etalon + journaux `.jsonl`) sont NOMMES et RAPPORTES en fin de
  rapport, chacun avec son motif -- aucun fichier n'est exclu en silence. Le
  rapport ne cite aucun point de code pour eux : il dit seulement qu'ils sont
  hors champ (l'angle mort est mesure, pas corrige).
- Ecriture atomique (tmp + remplacement), fins de ligne LF forcees.
- LECTURE SEULE par defaut : `corriger` sans `--appliquer` ne fait que le rapport.

## Racine (pattern v1)

Detectee en remontant jusqu'au dossier contenant `AGENTS.md`.

## Commandes

    python main.py verifier              (scan seul : ecarts + convertibilite)
    python main.py corriger              (rapport : ce qui serait corrige)
    python main.py corriger --appliquer  (applique les corrections convertibles)

## Regle d'usage

Une correction appliquee est TOUJOURS suivie d'une note en BDD via
`matrice/data/outils/bdd-modifications` (le combo de veille ou l'operateur).
