# OUTIL verifier-protocoles

> Outil de la Matrice (lot marbre 3/3) : verification du marbre des
> protocoles de l'operateur. LECTURE SEULE : il signale les ecarts, il ne
> repare JAMAIS le marbre.

## Ce qu'il verifie (dossier `_operateur/optimus-prime/protocoles/`)

1. ASCII strict : tout caractere non-ASCII est signale (ligne:colonne).
2. Front-matter : bloc `identite` present, avec `type: protocole` et
   `appartient_a: optimus-prime` (index exclu).
3. Index synchronise : `protocoles-readme.md` liste chaque protocole
   (lignes de tableau seulement). Un `.md` cite n'est mort que s'il
   n'existe ni dans le dossier ni a son chemin relatif (les liens vers
   docs/ ou la fiche sont legimitimes).

## Racine (pattern v1)

La racine du workspace se DETECTE en remontant jusqu'au dossier contenant
`AGENTS.md` (elle ne se compte jamais) : l'outil tourne depuis n'importe
quel repertoire courant.

## Commande

    python main.py verifier

## Sortie

- `OK` / `ECART` par groupe de controle, detail fichier:ligne:colonne.
- Code 0 si conforme, code 1 si au moins un ecart.
