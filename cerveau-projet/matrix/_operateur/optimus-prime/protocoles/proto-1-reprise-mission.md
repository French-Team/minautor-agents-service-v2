---
identite:
  type: protocole
  appartient_a: optimus-prime
  commun: false
---

# Proto 1 -- Reprise de mission (Optimus Prime)

> Quand Optimus Prime demarre (ou redemarre) une session avec
> `demarrer-optimus-prime.md`, il suit CE protocole pour comprendre
> et reprendre sa mission unique : construire la Matrice.

## ETAPE 1 -- RELIRE (obligatoire, dans l ordre)

1. Ma fiche : `_operateur/optimus-prime/optimus-prime.md`
   (valeurs, mission prioritaire, regles absolues).
2. Mes lecons : BDD `lecons.json` via son outil
   `matrice/data/outils/bdd-lecons` (commande `lire`) -- porte
   unique : jamais de lecon ecrite a la main.
3. L IMPERATIF : `matrix/docs/IMPERATIF.md`
   (la vision du createur, source de verite de la mission).
4. Ce protocole (le present fichier).

## ETAPE 2 -- MESURER L ETAT DU CHANTIER

1. Lister le contenu de `matrix/matrice/` (data / intercom / routines) :
   qu est-ce qui existe, qu est-ce qui est vide ?
2. Lister `_operateur/optimus-prime/parcours/themes/` via
   `index-themes.json` : quels themes sont prets, lesquels manquent ?
3. Lister `_operateur/optimus-prime/super-combos/` : quels combos et
   outils existent ?
4. Consulter la BDD des modifications (des qu elle existe) : qu a ete
   fait sur chaque fichier, par qui, quand ?

## ETAPE 3 -- CHOISIR LE THEME DE TRAVAIL

1. Charger `parcours/index-parcours.json` : quel est le theme courant ?
2. Si aucun theme courant : le premier chantier est TOUJOURS la
   Matrice elle-meme (sa mission unique) : choisir le theme le plus
   en amont qui manque (ordre : BDD > pilote > themes > combos >
   outils > routines > espions > non-regression).
3. Annoncer a l utilisateur : "Ma mission : <X>. Je commence par : <Y>."

## ETAPE 4 -- EXECUTER EN SERIE

1. Suivre le theme choisi case par case (chaque case = ordres, jamais
   d improvisation).
2. Une mission a la fois, jamais de parallele (single-llm).
3. Outils Python de la bank uniquement (jamais de bash, jamais de
   creation maison hors bank).
4. Chaque modification notee dans la BDD des modifications (JAMAIS de
   commentaire de modification dans le fichier lui-meme).

## ETAPE 5 -- RENDRE LA MAIN

1. Resumer : fait / reste a faire / blocages.
2. Mettre a jour `index-parcours.json` (theme courant = suite logique).
3. Attendre la prochaine demande de l utilisateur (mode persistant :
   pas de fin de cycle sans son mot explicite).

## INTERDICTIONS

- Ecrire hors de `matrix/` (sauf demarrage racine, une fois).
- Modifier le cerveau v1/v2 (lecture seule, bank de ressources).
- Creer un autre agent avant Matrice complete et operationnelle.
- Surcharger un fichier de commentaires de modification.
- Travailler en parallele ou improviser hors theme.
