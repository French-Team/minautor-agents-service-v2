---
identite:
  type: chaine
  appartient_a: optimus-prime
  commun: false
  titre: Reparation de masse des 32 refus muets
  statut: todo
  pense-bete: PB-002
  spec: SP-002
  nemesis: contre-analyse du 2026-09-19 (3 axes : portee, masquage, preuve)
  todo: TD-002
---

# Reparation de masse des 32 refus muets

## Pense-bete -- la demande clarifiee

CONSTAT MESURE (MO-202/MO-239) : 32 des 35 outils de la Matrice rendent un refus MUET -- code 2 et usage SEUL, l option fautive n est jamais NOMMEE ; l appel doit alors deviner parmi toutes les options, et le refus coute trois essais (friction 77). Le motif vit DEJA au domicile partage matrice/data/commun/options.py (signaler_inconnues, EO-179 -- le parseur RETIENT l inconnue) mais c est l APPELANT qui doit la DIRE : mesure, 110 fichiers appellent extraire_options et 3 lieux seulement la disent. PISTE A EXAMINER : que le domicile rende le refus IMPOSSIBLE A OUBLIER (signaler par DEFAUT au lieu d une fonction a appeler), puis generaliser par FAMILLE d outils au lieu de 32 rounds separes. PORTEE A MESURER AVANT TOUTE ECRITURE : 83 a 110 appelants, dont des appels qui acceptent des arguments LIBRES (refuser=False) et qui casseraient sur un refus global. INTERDIT : recopier le motif outil par outil (M-076, un seul domicile).

## Ce qui est deja mesure

- SONDE sc-004-auto-diagnostic (MO-202), sur les 35 outils de matrice/data/outils : 2 conformes, 32 refus-MUETS (code 2 + usage SEUL, l option fautive n est pas nommee) et 1 qui AVALAIT. MO-239 a repare le dernier : 3 conformes / 32 ecarts.
- LE MOTIF EXISTE DEJA, au DOMICILE PARTAGE : matrice/data/commun/options.py, fonction signaler_inconnues (EO-179). Le parseur RETIENT l inconnue sous CLE_INCONNUES ; c est l APPELANT qui doit la DIRE.
- PORTEE : 110 fichiers .py appellent extraire_options (matrice + _operateur) ; 83 cote matrice (mesure MO-215). Seuls 3 lieux DISENT l inconnue : rechercher, benchmark, chaine-pense-bete (+ maintenir depuis MO-239).
- CE QUE LE REFUS MUET FAIT : les 32 rendent bien code 2 ET un usage -- l appel ne part donc PAS ; mais ils ne NOMMENT pas l option fautive, et l appel doit deviner parmi la liste. Mesure du 2026-09-19 : bdd-activites et lire rendent le meme code 2, usage seul, sans le mot de l option.
- COUT MESURE D UNE REPARATION UNITAIRE : MO-239 = 2 fichiers, 4 editions par la porte (un relais local dans commun.py + l appel dans entry.py). A 32 outils, la voie unitaire coute environ 128 editions : c est ce que la demande veut eviter.

## NEMESIS -- avis contradictoire AVANT d ecrire

Trois attaques, et ce qu elles imposent.

1. AXE PORTEE (le plus dangereux). Un refus par DEFAUT au domicile casse tout appel qui accepte des arguments LIBRES (refuser=False) : la portee sur les 110 appelants n est PAS mesuree, donc la voie (1) est aujourd hui une PROMESSE, pas une preuve. Elle ne peut pas etre ecrite avant cette mesure.
2. AXE MASQUAGE. Reparer outil par outil en autant de rounds est justement ce que la demande veut eviter -- mais un regroupement mal mesure produit 32 missions qui se ressemblent et environ 128 editions. La mesure du RELAIS PARTAGE (combien d outils partagent un commun.py, donc combien d editions un seul geste couvre) doit passer AVANT le decoupage.
3. AXE PREUVE. Le seul verdict qui compte est le nombre de CONFORMES sur la MEME sonde, avant et apres, avec le contre-temoin du refus muet. Un outil qui passerait au vert par un autre chemin serait un FAUX VERT : la preuve exigee est la sonde sc-004 rejouee, jamais une declaration.

CE QUE LE NEMESIS IMPOSE, dans l ordre : (a) MESURER les relais partages et la portee sur les appelants ; (b) ne PAS modifier le contrat du domicile avant que la mesure autorise la voie (1) ; (c) dans tous les cas, prouver par la sonde rejouee.

## MESURE DES DEUX VERDICTS (2026-09-19) -- la voie de masse est AUTORISEE

1. PORTEE = RISQUE NUL. Le NEMESIS redoutait des appelants a arguments LIBRES (refuser=False) qui casseraient sur un refus par defaut : MESURE, 0 appelant sur tout le depot (le seul fichier qui nomme ce parametre est le domicile lui-meme, dans sa signature). La voie (1) n est plus une promesse : elle est autorisee.
2. FAMILLES, PAS 32 OUTILS. 57 fichiers entry.py appellent extraire_options ; 3 seulement disent l inconnue. Les fautifs sont 24 dossiers distincts -- les doublons de la liste viennent des sous-verbes bdd-*, qui partagent le MEME commun.py : un seul geste par FAMILLE les couvre tous.
3. LE DOMICILE SAIT DEJA REFUSER. options.py ligne 98 : signaler_inconnues(..., refuser=True) est le DEFAUT. Le refus n est muet que parce que extraire_options n APPELLE PAS cette fonction. Le trou est donc UNE ligne dans UN domicile -- pas 32 editions dispersees.

DECOUPAGE DU GROUPE propose : (A) 1 mission -- la porte du domicile : extraire_options relaie lui-meme l inconnue (refus par defaut, nom de l outil deduit de sys.argv, usage si fourni) ; (B) 1 mission de preuve -- sonde sc-004 rejouee, comptage des conformes AVANT/APRES, contre-temoin du refus muet ; (C) les rounds unitaires restants deviennent INUTILES, sauf pour les familles qui portent leur propre commun.py. INTERDIT rappele : aucune copie du motif hors du domicile (M-076).

## FAMILLES ET HORS-COUVERTURE (mesure 2026-09-19, question du createur)

QUESTION : combien des 24 muets ont leur propre commun.py et ne seraient PAS couverts par le domicile unique ?

REPONSE : 24 sur 24 ont un commun.py -- et AUCUN des 24 n echappe au domicile. Les 26 jumeaux sont des PASSE-PLATS PURS (tous retournent le dictionnaire du domicile tel quel), donc CLE_INCONNUES SURVIT jusqu a l appelant : le refus est MUET parce qu il n est pas LU, pas parce qu il est PERDU. Graver le refus au domicile couvre les 24 d un seul geste.

26 jumeaux, 10 formes seulement (mesure) : 16 repartir(arguments, noms_connus) ; 2 sans_tirets=True ; 2 drapeaux=("json",) ; 1 drapeaux=NOMS_OPTIONS_DRAPEAU ; 1 ("recursif","json","prive") ; 1 ("recursif","hash","prive") ; 1 ("json","verbose") ; 1 ("json","recursif","integration") ; 1 ("json","etat") = maintenir (MO-239).

LE VRAI HORS-COUVERTURE EST AILLEURS : 6 outils n appellent JAMAIS le domicile (parsing maison), mesures a l instant par une option inconnue --
  - bilan-periode, corriger-ascii, journal-multi-encarts : CODE 2, l option n est PAS nommee (chacun declare 1 option) -> 3 fautifs reels, non couverts par le domicile, a traiter a part ;
  - verifier-conventions, verifier-protocoles, verifier-regles : AUCUNE option -- (0 mesuree) ; le code 2 vient du verbe manquant -> ils refusent en DISANT leur usage, rien a reparer ;
  - selecteur-flux : argparse (autre domicile, stdlib) -- avec une sous-commande VALIDE il NOMME l option (unrecognized arguments: --option-inconnue-test 1) -> CONFORME par un autre chemin, hors du domicile de la Matrice.

CE QUE CELA DIT DU DECOUPAGE : la reparation de masse tient en UNE mission au domicile (couvre 24 muets) + 3 missions unitaires hors domicile (bilan-periode, corriger-ascii, journal-multi-encarts), soit 4 rounds au lieu de 32. Les 16 jumeaux purs n ont AUCUNE ligne a changer.

## Ce qui reste a mesurer

- COMBIEN DE CES 32 OUTILS PARTAGENT UN RELAIS LOCAL (commun.py) : si une seule edition de relais couvre plusieurs outils, le groupe se reduit fortement. A mesurer AVANT de decouper.
- COMBIEN DES 110 APPELANTS ACCEPTENT DES ARGUMENTS LIBRES (refuser=False) : un refus global au domicile les casserait. C est la mesure qui decide entre les deux voies.
- LES DEUX VOIES POSSIBLES, a trancher sur mesure : (1) le DOMICILE rend le refus impossible a oublier -- le parseur signale par DEFAUT, l appelant ne peut plus avaler ; (2) une REPARATION PAR FAMILLE, outil par outil dans le lot courant. La voie (1) est plus forte mais elle change un contrat partage : portee a mesurer et NEMESIS obligatoire.
- LE GAIN REEL, chiffre : nombre d outils devenus conformes par voie, nombre d editions evitees, et contre-temoin avant/apres sur la MEME sonde.

