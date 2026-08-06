# evaluer-conventions

Evalue le respect des conventions : nommage, ASCII, format.

## Usage

```bash
bash evaluer-conventions.sh [DOSSIER]
```

## Ce qu'il verifie

- Nommage des statuts (pas d'accents dans les statuts de fichiers)
- Conformite ASCII (hors exceptions declarees)
- Bandeaux EXCEPTION VOLONTAIRE sur les dictionnaires
- Exclusion du dossier exemples par les outils
- Format des fichiers agents (chaque agent a sa fiche)

## Sortie

Rapport markdown sur stdout avec score /100.
