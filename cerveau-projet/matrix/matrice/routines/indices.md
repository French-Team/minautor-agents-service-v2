# INDICES -- routines/ (vie de la Matrice)

> Tete de lecture : lire CECI avant les fichiers. L'indice pointe, le contrat fait foi.

| Besoin | Lire (fichier, section) |
|---|---|
| Routines existantes, etat | `routines-readme.md` (contrat) |
| Surveillance des 7 BDD | outil `espion-integrite` : `tour` (une passe) |
| Boucle de surveillance continue | `espion-integrite` : `boucle` / `boucle arret` |
| Registre des BDD surveillees | `espion-integrite/constants.py` |

## Conventions de la zone

- Une routine = outil Python conforme (entree -> categories -> fonctions simples).
- Arret cooperatif par drapeau : jamais de processus tue, jamais de fantome.
- Journal en ajout seul ; refus de double lancement via fichier PID.
- Une routine SIGNALE, elle ne repare pas en douce.
