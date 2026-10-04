---
identite:
  type: outil
  appartient_a: matrice
  commun: true
  version: 1
  date: 2026-09-23
  liens: matrice/templates/routine/README.md, matrice/data/outils/ecrire/DESCRIPTION.md, matrice/data/manuel-outils.md
---

# OUTIL -- dupliquer-template -- genere un outil ou une routine depuis un moule

> Outil Python dedie : genere un OUTIL ou une ROUTINE conforme depuis un moule
> `templates/outil-bdd/` (modele-mere : bdd-lecons). Proto-5 : la galere
> native (recopier un outil a la main = derive) devient un outil.

## Options

```
python3 cerveau-projet/matrix/lancer.py dupliquer-template generer --nom bdd-xxx --bdd xxx.json --prefixe X \
       --liste xxx --champ xxx [--humain xxx]
```

- `--nom` : nom du dossier outil sous `data/outils/` (forme fermee `bdd-[a-z][a-z0-9-]*`).
- `--bdd` : nom du fichier BDD dans `data/` (`xxx.json`).
- `--prefixe` : prefixe des identifiants (`X-001`).
- `--liste` : cle de la liste des entrees dans la BDD.
- `--champ` : nom de l'option CLI et du champ de contenu.
- `--humain` : libelle humain dans les messages (defaut : le champ).
- `--role` (moule routine) : ce que la routine fait, en une phrase.
- `--cadence` (moule routine) : cadence declaree en secondes (defaut 300, plancher 5).

## Le pipeline (verifier AVANT d'ecrire)

1. lecture du MOULE (`templates/<moule>/`, jamais un outil vivant) ;
2. traduction des jetons en MEMOIRE ;
3. verification de chaque source : py_compile + ASCII strict + aucun jeton residuel ;
4. refus si l'outil cible existe deja (jamais d'ecrasement) ;
5. ecriture, puis verification du clone executable (docstring + code 2 sans argument pour un OUTIL ; UNE PASSE `--once` pour une ROUTINE, jamais son demon).

Un seul ecart = aucune ecriture : jamais d'outil a moitie livre.

## Suites attendues (apres generation)

Fiche dans `data/manuel-outils.md`, BDD ajoutee au registre de
l'espion-integrite, premiere entree creee par la porte du clone.

## Architecture (convention-architecture-outils)

| Piece | Role |
|---|---|
| DESCRIPTION.md | la facade (ce fichier) |
| main.py | point d'entree global : DIRIGE |
| constants.py | chemins moule/outils, motif du nom, jetons |
| commun.py | options |
| generer/ | valider, traduire, verifier, ecrire |
