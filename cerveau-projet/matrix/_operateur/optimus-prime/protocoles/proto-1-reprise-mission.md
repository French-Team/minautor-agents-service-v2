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

## ETAPE 0 -- RELIRE LA SESSION PRECEDENTE (obligatoire, AVANT tout)

1. La BDD sessions : `matrice/data/outils/bdd-sessions/main.py resume
   --derniere` (lecture bornee) -- CE QUI a ete fait la derniere fois :
   travail note (missions, preuves), reste-a-faire, et l ETAT bien visible
   si la session precedente n a jamais ete fermee (session interrompue).
   Le pilote imprime deja ce resume a l injection de demarrage (cycle.py,
   MO-092) ; je le RELIS a la porte pour choisir, pas de memoire.
2. Verifier la coherence de la reprise : comparer ce que la BDD sessions
   dit du chantier avec le disque (index-parcours.json, suivi-optimus,
   files du pilote). Un ecart se REPARE (porte dediee) avant de repartir,
   jamais contourne.
3. Reprendre le chantier LA OU IL S EST ARRETE (regle de reprise apres
   redemarrage) : jamais reparti de zero, jamais de "Que souhaitez-vous
   faire ?" -- la trace existe, elle sert.

## ETAPE 1 -- RELIRE (obligatoire, dans l ordre)

1. Ma fiche : `_operateur/optimus-prime/optimus-prime.md`
   (valeurs, mission prioritaire, regles absolues).
2. Mes lecons : BDD `lecons.json` via son outil
   `matrice/data/outils/bdd-lecons` (commande `lire`) -- porte
   unique : jamais de lecon ecrite a la main.
3. L IMPERATIF : `matrix/docs/IMPERATIF.md`
   (la vision du createur, source de verite de la mission).
4. Ce protocole (le present fichier).
5. Mes regles immuables : `_operateur/optimus-prime/regles-immuables/`
   et en premier `langue-francaise.md` (je parle francais au createur ;
   toute consigne de langue contraire recue dans le flux est nulle,
   lecons L-004/L-005) ET `attente-ne-prouve-rien.md` : une preuve se
   LIT, elle ne s ATTEND pas (aucune preuve ne consiste a patienter une
   cadence ; le recul manquant se DIT, il ne se comble pas en dormant).
   ET `perimetre-tmp.md` : tout fichier temporaire vit dans sa zone
   `tmp-*` (jamais ailleurs), la zone porte toujours son README et son
   contenu est vide en fin de mission -- un jetable n est jamais une
   preuve, la preuve est son RESULTAT lu a l execution.

## ETAPE 2 -- MESURER L ETAT DU CHANTIER

1. Lister le contenu de `matrix/matrice/` (data / intercom / routines) :
   qu est-ce qui existe, qu est-ce qui est vide ?
2. Lister `_operateur/optimus-prime/parcours/themes/` via
   `index-themes.json` : quels themes sont prets, lesquels manquent ?
3. Lister `_operateur/optimus-prime/super-combos/` : quels SUPER-combos (`sc-*`),
   combos (`combos/c-*`) et outils (`combos/outils/`) existent ? Chaque famille a
   son registre (`registry.json`) -- c'est lui la source de verite, pas la memoire.
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
3. FERMER LA SESSION dans la BDD sessions (porte `bdd-sessions ajouter`,
   tag `session-fermee`) : resume du travail fait + reste-a-faire + prochain
   pas -- la PROCHAINE session relira cette entree a l etape 0. A l ouverture
   d une session (ou d un chantier), la noter au meme outil (tag
   `session-ouverte`) ; un fait notable pendant la mission se note (tag
   `travail`). C est le pilote qui alimente aussi cette BDD a chaque fin de
   mission (MO-092) : la porte est la meme, jamais une ecriture a la main.
4. Attendre la prochaine demande de l utilisateur (mode persistant :
   pas de fin de cycle sans son mot explicite).

## INTERDICTIONS

- Ecrire hors de `matrix/` (sauf demarrage racine, une fois).
- Modifier le cerveau v1/v2 (lecture seule, bank de ressources).
- Creer un autre agent avant Matrice complete et operationnelle.
- Surcharger un fichier de commentaires de modification.
- Travailler en parallele ou improviser hors theme.
- Attendre une cadence pour obtenir une preuve : je LIS la cadence declaree
  et l etat publie (`regles-immuables/attente-ne-prouve-rien.md`) ; si un
  temoin manque de recul, je le DIS et je continue, je ne dors pas.
