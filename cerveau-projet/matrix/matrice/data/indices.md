# INDICES -- data/ (BDD de la Matrice)

> Tete de lecture : lire CECI avant les fichiers. L'indice pointe, le contrat fait foi.

| Besoin | Lire (fichier, section) |
|---|---|
| Regles des BDD, statut des 7 | `data-readme.md` (contrat + tableau statut) |
| Flux d'ecriture vers une BDD | `data-readme.md` (diagramme du flux) |
| Noter une modification de fichier | outil `outils/bdd-modifications` (commande `noter`) |
| Ajouter une lecon | outil `outils/bdd-lecons` (commande `ajouter`) |
| Commandes detaillees d'un outil | `manuel-outils.md` (ce dossier) |
| Motif racine AGENTS.md / sac a dos des outils | `commun/racine.py` + `commun/sac_a_dos.py` (fiches dans `manuel-outils.md` section 21) |
| Verifier l'integrite d'une BDD | outil dedie (commande `verifier`) ou espion-integrite |
| Faire un bilan sur une periode | outil `outils/bilan-periode` (commande `bilan --periode <1h|heures|24h|3j|semaine|mois>`) |

## Conventions de la zone

- PORTE UNIQUE : toute ecriture passe par l'outil dedie, jamais a la main.
- Motif unique : la detection de racine vit dans `commun/racine.py` -- JAMAIS recopiee dans un outil (M-076).
- Sac a dos : chaque outil note son usage (code + duree) via `commun/sac_a_dos.py` -- bdd-usages exclu (recursion interdite).
- Ecriture atomique (tmp + remplacement), fins de ligne LF forcees (determinisme).
- Empreinte SHA-256 cote a cote de chaque BDD (etalon-or).
- L'espion ne repare pas : il signale, la reparation repasse par la porte unique.
