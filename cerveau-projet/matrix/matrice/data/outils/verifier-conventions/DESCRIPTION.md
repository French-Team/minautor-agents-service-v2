# OUTIL verifier-conventions

> Outil de la Matrice (proto-5 auto-amelioration) : remplace la verification
> manuelle des conventions de l'operateur (friction prouvee : un accent
> attrape a la main dans routines/indices.md, le 2026-09-06).
> LECTURE SEULE : il signale les ecarts, il ne repare JAMAIS le marbre.

## Ce qu'il verifie (dossier `_operateur/optimus-prime/conventions/`)

1. ASCII strict : tout caractere non-ASCII est signale (ligne:colonne).
2. Front-matter : bloc `identite` present, avec `type: convention` et
   `appartient_a: optimus-prime`.
3. Index synchronise : `conventions-readme.md` liste chaque fichier de
   convention (aucun absent, aucune ligne morte). L'index = les lignes
   de TABLEAU (commencant par '|') : les mentions en prose (ligne
   Sources, avertissements) ne comptent pas.

## Commande

    python main.py verifier

## Sortie

- `OK` / `ECART` par groupe de controle, detail fichier:ligne:colonne.
- Code 0 si conforme, code 1 si au moins un ecart.

## Regle d'usage

L'outil SIGNALE ; la reparation passe par l'edition (notee en BDD,
porte unique `bdd-modifications`), jamais par une reparation en douce.
