


## [LECON] 2026-08-12 -- ROUND 10b : PARALLELE PAR DEFAUT TESTE (Morpheus)

**Mission** : adapter les tests apres le passage du lanceur en parallele par defaut (v0.1.3, Vulcain round 10b).

**Resultat** : test-024 13/13 (v0.1.3), test-027 11/11 (v0.1.3 + 2 nouveaux points), non-regression 27/27 identique en mode defaut (parallele) et en --serial.

**Lecons** :
1. UN CHANGEMENT DE MODE PAR DEFAUT DOIT ETRE TESTE DES DEUX COTES : test-027 verifie desormais (a) que sans option le lanceur passe par la structure Serie A (defaut = parallele) ET (b) que --serial redonne la structure serie (echelon de secours fonctionnel). Le defaut n est pas un detail - il se verifie.
2. L HERITAGE DU FILTRE EST UNE REGRESSION SILENCIEUSE SI NON TESTE : --tests test-003 sans option doit lancer UN SEUL test (1 OK / 0 KO sur 1 tests) - si le filtre n etait pas herite par les sous-processus, toute la serie A partirait.
3. STRUCTURE DE SORTIE = SIGNATURE DU MODE : RESULTAT Serie X = parallele ; RESULTAT : (sans libelle) = serie. La structure de sortie est le moyen fiable de distinguer les 2 modes dans un test.

## [LECON] 2026-08-12 -- ROUND 11 : GARDE-FOU COHERENCE DOCUMENTAIRE (Morpheus)

**Mission** : creer le garde-fou test-028 (specs vs outils + catalogue vs interfaces) apres les corrections Vulcain du round 11.

**Resultat** : test-028 8/8 OK, serie D 6 tests, non-regression 28/28, normes 0/0.

**Lecons** :
1. UN NOUVEAU TEST DOIT ETRE AFFECTE A UNE SERIE : test-028 etait hors-serie a sa creation (test-027 KO : couverture 100% exigee). Ajout a la serie D du lanceur (constantes SERIES) - test-027 lit les constantes par import, donc il est reste vert sans modification.
2. UN TEST DE GARDE-FOU NE REIMPLEMENTE PAS LA DETECTION : mon premier point 4 cherchait 'Version' dans les 2000 premiers caracteres - faux KO sur 3 specs qui mettent leur version dans le tableau historique en fin de fichier. Correction : croiser la SORTIE de l outil avec la presence d un .py associe (se fier a l outil, pas re-inventer sa logique).
3. LE CHAMP **Version outil** EST LE CONTRAT DES SPECS DE CONVENTIONS : une spec qui versionne des patterns (guider-parcours 0.6.2) au-dela de l outil (0.5.0) doit le declarer explicitement - le garde-fou le verifie.

## [LECON] 2026-08-12 -- ROUND 10c : SERIE D ALLEGEE 29s -> 5s (Morpheus)

**Mission** : reduire le temps de la serie D de la non-regression (demande utilisateur).

**Diagnostic** : serie D = 29s dont test-027 = 26s (les 4 autres tests <= 1s). Cause : test-027 lancait 3 fois le lanceur avec --tests test-003-combos-creer (89 points, ~6s par execution).

**Correction** : remplacement de test-003-combos-creer par test-001-evaluer-agents-coherence (0s, lecteur pur, dans la serie A) dans les points 6a/6b/7/8 + libelles + docstring. Logique inchangee : isolation, defaut=parallele, --serial prouves avec un test leger.

**Resultat mesure** : test-027 26s -> 2s (11/11), serie D 29s -> 5s, non-regression complete 47s -> 23s (27/27).

**Lecons** :
1. UN TEST DE GARDE-FOU QUI LANCE UN TEST LOURD EST UN PIEGE DE PERFORMANCE : test-027 executait test-003 (89 points de combos) a travers le lanceur - le garde-fou devenait plus cher que ce qu il verifiait. Le test de preuve doit utiliser le test LE PLUS LEGER de la serie (test-001 : lecteur pur 0s).
2. LA PREUVE DE FILTRAGE N A PAS BESOIN D UN GROS TEST : l isolation (--series a vs c), le defaut parallele et --serial se prouvent avec n importe quel test de la serie - la valeur du test est la STRUCTURE de sortie, pas la taille du test lance.
3. MESURER AVANT D OPTIMISER : le chrono par test a montre que test-027 (26s) etait le vrai coupable, pas test-024 comme suppose - toujours mesurer chaque composant avant de choisir la cible.

## [LECON] 2026-08-12 -- ROUND 10 : TEST-027 SERIES + TEST-024 ADAPTE (Morpheus)

**Mission** : tester le nouveau --series/--parallele du lanceur de non-regression v0.1.2 (Vulcain round 10).

**Resultat** : test-024 adapte (13/13), test-027 cree (9/9), non-regression 27/27 OK en mode serie ET en mode --parallele (A=6, B=10, C=6, D=5) - parite complete, registre 0 ligne.

**Lecons** :
1. VERSION FIGEE DANS UN TEST : test-024 verifiait la version du lanceur en dur (v0.1.1) -> le bump v0.1.2 l a fait KO. Adaptation : libelle + assertion en v0.1.2. Un bump d outil doit toujours etre croise avec les tests qui figent sa version (grep des versions avant validation).
2. PIEGE STDERR ARGPARSE : quand argparse rejette une option (--series z), le message usage part sur STDERR, pas stdout. Un test qui verifie le message sur stdout est KO a tort (rc=2 etait bon, le message etait sur stderr). Toujours concatener stdout + stderr pour verifier un message d erreur.
3. GARDE-FOU COUVERTURE DES SERIES : le test-027 verifie que CHAQUE test-0XX du disque appartient a une serie du lanceur (par import de la constante SERIES) - un futur test-028 non affecte fera KO + avertissement hors-serie a l execution : anti-recurrence de l oubli d affectation.
4. PIEGE RECURSION : un test de garde-fou du lanceur ne doit JAMAIS lancer le lanceur sans filtre --tests qui l inclurait lui-meme (test-027 est dans la serie D). Toute invocation combine --series <X> + --tests <test hors D>.
5. PARITE SERIE/PARALLELE : la non-regression complete donne 27/27 dans les 2 modes avec des bilans par serie identiques - la preuve que le decoupage ne perd aucun test et que le parallelisme ne casse rien.

## [LECON] 2026-08-11 -- TEST-007 ADAPTE 120 -> 138 COMMANDES (Morpheus, VERDICT VALIDE)

**Mission** : adapter le point 13 du test-007-figer-lf apres l ajout des 18 commandes de test au catalogue generateurs-commande (Vulcain).

**Lecons** :
1. Le point 13 du test-007 exigeait exactement 120 commandes ; le catalogue passe a 138 apres l ajout de test-004 a test-021. Adaptation : 120 -> 138 + verification supplementaire de la presence de test-021-ligne-trio (garde-fou positif : le nouveau test est bien au catalogue).
2. Le point 14 (index-tools total 110) est independant du catalogue : il compte les OUTILS, pas les commandes de test. Aucun impact.
3. Le catalogue reference desormais TOUS les tests (test-001 a test-021) : generation de commandes complete pour la suite de tests.
4. Resultat : test-007 reverdi (15/15), non-regression complete 21/21 OK, normes 0/0.
5. Chaine conforme : Vulcain (catalogue) -> Morpheus (test-007) -> prochaine etape Janus (controle croise) avant le retour a Cerberus.

## [LECON] 2026-08-11 -- TEST-021 LIGNE TRIO CREE (Morpheus, VERDICT VALIDE)

**Mission** : creer le test-021 dedie a la ligne trio de Janus + boucle de correction, comme garde-fou non-regression.

**Lecons** :
1. Le test-021 couvre : structure statique (branche trio c1->cT1, types cT1..cT10), commandes exactes cT6..cT10 (garde-fou P8 insensible a la casse), navigation reelle OUI (athena->cT6, promethee->cT7, minerve->c10 Reactiver Cerberus), navigation KO (athena->cT8, promethee->cT9, minerve->cT10), boucle de correction (branche corriger + c9f -> c10 sur le trio), valider-cartes CONFORME, ASCII + LF.
2. Le point ASCII a detecte 2 non-ASCII dans le PROTOCOLE-CONTROLE-TRIO (residu de la mission Buffy : 'recoit' et 'structure' accentues dans la REGLE D EXCELLENCE). Le test sert aussi de filet sur les autres fichiers du perimetre : il a rattrape un ecart laisse par la mission precedente.
3. La non-regression passe de 20 a 21 tests : le script de detection par glob (test-0*/test-0*.py) inclut automatiquement le nouveau test.
4. Convention respectee : seul Morpheus ecrit et execute les tests (REGLE IMMUABLE DELEGATION du protocole-tests).
5. Resultat : test-021 9/9 OK, non-regression 21/21 OK, normes 0/0. La ligne trio est desormais verrouillee par un garde-fou automatique : toute modification des cartes (fin cT sans commande, branche trio perdue, boucle corriger cassee) cassera la non-regression.

## [LECON] 2026-08-11 -- TEST-018 ADAPTE APRES MIGRATION DU TRIO VERS JANUS (Morpheus)

**Mission** : adapter test-018 (fins reactivation) apres la correction du trio (etape 2) : minerve n'est plus une fin REACTIVER mais 'FIN - Activer Janus'.

**Lecons** :
1. Le trio (athena c10, promethee c10, minerve c10) a migre vers 'FIN - Activer Janus' : FINS_PRECISEES est desormais vide (janus est la seule fin REACTIVER restante, dernier maillon legitime).
2. Le bloc FINS_ACTIVER_JANUS passe de 3 a 6 agents (atlas/themis/morpheus + athena/promethee/minerve) : garde-fou positif elargi.
3. Point 1b adapte : 'La seule fin REACTIVER restante est janus (dernier maillon)' au lieu de 'Les 2 fins (janus, minerve)'.
4. Point 4 adapte : nav_ok == 0 (aucune fin precisee restante) au lieu de 1.
5. Faux positif de detection : mon script de non-regression comptait KO un test affichant '19/19 OK' car il cherchait '0 KO'. Le motif fiable est '[KO]' ou un compteur 'N KO' avec N > 0 (regex [1-9][0-9]* KO).
6. Resultat : test-018 13/13 OK, non-regression 20/20 OK, normes 0/0.

## [LECON] 2026-08-09 -- GENERATEURS-LIGNE v0.2.0 TESTE (configs externalisees + ajouter-config)

**Mission** : tester formellement l'evolution de generateurs-ligne v0.1.0 -> v0.2.0 (decision utilisateur + Cerberus) : gabarits EXTERNALISES dans gabarits-ligne.json (pattern themes-amelioration.json, une place pour chaque chose) + sous-commande ajouter-config (validation + dry/wet) pour que Buffy cree une nouvelle config reutilisable sans toucher au code de l'outil (Pattern 12 : creation limitee).
**Livrables testes** : generateurs-ligne.py v0.2.0 + .sh + .md + spec/ + gabarits-ligne.json (nouveau) + entree catalogue (action ajouter-config + parametres description/gabarit) + test-017 mis a jour (v0.1.0 -> v0.2.0, 32 points).

**Lecons** :
1. Le test-017 passe de 24 a 32 points : version v0.2.0, --aide 5 sous-commandes (2c : ajouter-config --help affiche --description/--gabarit), lister-configs lit le JSON (6), nouveaux points 16a-16g (ajouter-config dry/wet, JSON trie, ajout reel CONFORME avec la nouvelle config, gabarit invalide rejete "au moins 2 branches", conflit de nom rejete sans --force, nettoyage restaure a 4 configs), ASCII sur 5 fichiers + test (19).
2. LE PIEGE DU SUFFIXE VIDE : un gabarit externe a une 1re case avec "suffixe": "" (point d'entree) - la validation "if not suf" rejetait cette case legitime comme "suffixe manquant" (not "" est True). Corrige : verifier uniquement isinstance(suf, str). Le vide est UNE VALEUR VALIDE de suffixe.
3. PIEGE IDENTITE (detecter-impacts) : le bloc identite: doit tenir dans les 12 PREMIERES lignes du .py/.sh (contrainte du detecteur) - un en-tete documentaire trop long repousse commun: hors limite -> detecter-impacts lit "commun=false" (defaut) et considere l'outil non migre. Compactage de l'en-tete requis (retirer la ligne Sous-commandes, inutile car dans --aide).
4. detecter-decalages-catalogue signale un faux positif de limitation : il ne lit que l'aide RACINE, pas les sous-parsers -> les flags du sous-parser ajouter-config (--description/--gabarit) sont signales absents de l'aide alors qu'ils existent dans ajouter-config --help. Verifier avec --help du sous-parser avant de conclure.
5. Non-regression confirmee : test-005 (catalogue) 26/26, test-006 (cartographier) aucun nouveau KO (p2b preexistant connu), test-017 32/32.
6. Les configs externalisees sont un exemple de "une place pour chaque chose" : l'agent peut enrichir le catalogue de gabarits SANS modifier le code -> plus besoin de demander a Vulcain pour chaque nouvelle config.

**Validation** : protections 10/10 (nommage, ASCII 0, LF pur, py_compile, bash -n, parite --version v0.2.0, gabarits-ligne.json valide + trie, catalogue a jour, test-006 non-regression, detecter-impacts identite commun=true), test-017 32/32, test-005 26/26.
**Fin de mission** : Janus active pour le second controle croise de generateurs-ligne v0.2.0 et du test-017 mis a jour.
## [LECON] 2026-08-09 -- GENERATEURS-LIGNE v0.3.0 TESTE (sous-commande copier)

**Mission** : tester formellement l'evolution generateurs-ligne v0.2.0 -> v0.3.0 (demande utilisateur validee par le questionnaire ameliorer-outil de Cerberus) : sous-commande copier pour dupliquer une LIGNE existante d'une carte (2 sources : --source case avec 3 modes, ou --config gabarit) afin de faciliter la composition de nouvelles lignes ; generateurs-case assure ensuite l'edition fine du clone.
**Livrables testes** : generateurs-ligne.py v0.3.0 + .sh + .md + spec/ + gabarits-ligne.json + entree catalogue (copier dans les choix + parametres source/mode/branche) + test-017 etendu (41 points).

**Lecons** :
1. CONCEPT VALIDE PAR L'UTILISATEUR (via Cerberus + generateurs-amelioration) : copier doit accepter DEUX sources -- une case de la carte (--source) OU un gabarit (--config) -- et PLUSIEURS modes de detection : complet (remonter a la decision d'entree puis tout le sous-chemin), branche (copier UNIQUEMENT la branche choisie d'une decision), suite (copier le chemin qui part de la source jusqu'au REJOINT).
2. MODE COMPLET : si la source est une decision (question/controle), elle EST le point d'entree de la ligne -> copier sa suite complete SANS remonter. Mon premier jet remontait les predesseurs jusqu'au flux principal (c10b du parcours buffy) -> groupe enorme -> IndexError sur _LETTRES. Regle corrigee : decision -> racine = source ; action -> remonter jusqu'a la 1re decision rencontree.
3. PIEGE _LETTRES : le generateur d'ids cXa/cXb... n'avait que 10 lettres ("abcdefghij") alors que le mode suite peut copier des groupes > 10 cases -> IndexError. Corrige : _LETTRES etendu a 26 lettres + bascule sur numeros sequentiels c<base+i> pour les groupes > 27 cases (convention c<numero> toujours conforme).
4. Les cases REJOINT du groupe copie sont EXCLUES et remplacees par la cible de rejoint externe (--rejoint ou ancien suivant) : le clone ne duplique pas les "retours au flux" (sinon boucles).
5. Catalogue : --mode doit avoir defaut "" (pas "complet") sinon le generateur de commandes le compose aussi pour ajouter (qui n'a pas cette option) -> commande cassee. Defaut vide = flag retire.
6. Non-regression : test-005 (catalogue) 26/26, test-006 aucun nouveau KO (p2b preexistant), test-017 41/41 (dont 17a-17h : copier dry/wet, clone 4 cases, ids sans doublon, --config, modes branche/suite, blocage carte + --force).
7. Le cycle complet de l'utilisateur : copier une ligne existante (ou un gabarit) -> generateurs-case pour editer les cases du clone finement -> la carte reste conforme (valider-case CONFORME a chaque wet).

**Validation** : protections 9/9 (nommage, ASCII 0, LF pur, py_compile, bash -n, parite v0.3.0, catalogue a jour, detecter-impacts commun=true, detecter-divergences-version ALIGNE), test-017 41/41.
**Fin de mission** : Janus active pour le second controle croise de generateurs-ligne v0.3.0 et du test-017 etendu.
## [LECON] 2026-08-09 -- GENERATEURS-AMELIORATION v2.0.0 TESTE (theme ameliorer-outil reformule, 14 questions)

**Mission** : tester formellement l'evolution generateurs-amelioration v1.0.0 -> v2.0.0 (demande utilisateur orientee pendant le questionnaire lui-meme) : le theme ameliorer-outil passe de 10 a 14 questions avec 5 RAPPELS STRATEGIQUES en tete (q1 diagnostic de l existant, q2 horloge = anticiper les extensions naturelles, q3 formats = couvrir la famille de cas, q4 ameliorer vs evoluer = eviter patch puis refonte, q5 perimetre) + 9 questions techniques renumerees (q6-q14).
**Livrables testes** : themes-amelioration.json v2.0.0 (14 questions) + generateurs-amelioration.py/.sh v2.0.0 + .md + spec/ + test-008 mis a jour (10 -> 14 questions, 19 points).

**Lecons** :
1. L'utilisateur a donne l'orientation PENDANT le questionnaire (q1 du theme ameliorer-outil) : les questions doivent etre des RAPPELS qui poussent l'agent a reflechir a CE qui doit etre ameliore et a anticiper l'EVOLUTION (principes : horloge = heure+minute d'abord mais penser secondes/chronometre ; formats = ne pas creer mp3 seule si d'autres formats sont previsibles). Ce sont maintenant les 5 premieres questions de tout questionnaire d'amelioration.
2. REGLE DES 5 FICHIERS APPLIQUEE AU CONTENU : quand la version d'un outil change (1.0.0 -> 2.0.0), verifier TOUTES les mentions : .py (VERSION=), .sh (commentaire), .md (historique), spec (version + historique), ET le fichier de contenu (themes-amelioration.json). J'avais oublie le .py/.sh -> KO parite au test-008 -> corrige.
3. Le test-008 a 3 zones a adapter quand le nombre de questions change : l'en-tete docstring (10 -> 14), les verifications --liste ("10 questions" -> "14 questions"), la structure JSON (len(questions) == 10 -> 14), et la generation des reponses (range(1, 11) -> range(1, 15)).
4. Le questionnaire non-interactif (--reponses) est le mode de test parfait : il valide que les 14 questions sont posees, que les 14 reponses sont recapitulatives, et que la parite py/sh est identique.
5. Non-regression confirmee : test-008 19/19, test-017 (generateurs-ligne) 41/41, test-005 (catalogue) 26/26.
6. La philosophie derriere les rappels : "ameliorer ce qui existe d'abord, MAIS anticiper l'evolution pour ne pas patcher aujourd hui ce qu'on refondra demain" - le double travail (patch puis refonte) est ce que la checklist doit eviter.

**Validation** : protections 9/9 (nommage, ASCII 0, LF pur, py_compile, bash -n, parite v2.0.0, themes-amelioration.json 2.0.0 + 14 questions + 5 rappels, detecter-impacts commun=true, detecter-divergences-version ALIGNE), test-008 19/19.
**Fin de mission** : Janus active pour le second controle croise de generateurs-amelioration v2.0.0 et du test-008 mis a jour.
## [LECON] 2026-08-09 -- TEST GENERATEURS-CASE CORRIGE (28/28) + COMMANDE CONVERTIR TESTEE

**Mission** : corriger les 4 echecs preexistants de tester-generateurs-case.sh (le test
attendait 21 cases, le parcours vulcain en a 32 depuis plusieurs versions) et tester
formellement la nouvelle commande `convertir` de generateurs-case v0.4.0 (creee par
Vulcain, mode batch de migration).

**Resultat** : VERDICT VALIDE -- 28 tests reussis / 0 echec (17 d'origine corriges +
PT16 a PT20 pour convertir).

**Les 4 echecs preexistants corriges** (preuve : les memes 4 echecs avec le parcours
original HEAD, 17/4 identique -- independants de la commande convertir) :
- PT5 : 21 cases figees -> NB0 dynamique (nombre reel de cases du parcours source)
- PT6b : 22 figees -> NB0+1 apres ajout
- PT7/PT7b : la case ajoutee apres c8 est le PROCHAIN ID LIBRE (c22), plus c20 -- 
  extraction via python (c8.suivant) au lieu d un grep fragile
- PT8b : le pointant reel de c8 est c7b (structure c7->c7b->c8), plus c7 -- recablage
  verifie sur c7b -> nouvelle case

**Nouveaux tests (PT16-PT20)** :
- PT16 : convertir --dry-run ne modifie pas la version (fichier inchange)
- PT17 : convertir wet -> 0 indice restant + version bumpee via --version-parcours
- PT18 : mapping --refs remplace les regles longues par des refs (14 refs obtenues)
- PT19 : parite py/sh sur convertir --dry-run (sorties identiques)
- PT20 : sans --version-parcours, la version est conservee

**Lecons** :
1. PIEge WINDOWS/MSYS : un python3 -c avec un chemin /tmp/... dans le CODE echoue
   (le chemin n est pas converti en chemin Windows, contrairement aux arguments de
   ligne de commande). Solution : BASE_WIN=$(cygpath -m "$BASE") et utiliser $BASE_WIN
   dans les python3 -c. Les appels a l OUTIL gardent $BASE (bash convertit pour les
   programmes natifs).
2. Valeurs figees dans les tests = tests fragiles : le parcours vulcain evolue
   (21 -> 32 cases). Capturer dynamiquement (NB0, NOUVELLE via c8.suivant) au lieu
   de figer des ids.
3. grep -A20 est trop court pour atteindre une cle dans une case riche en indices :
   preferer l extraction via python json (plus robuste).
4. Le fichier tester-generateurs-case.sh porte un nom de runner (tester-*) : valider-
   nommage le rejette (rc=1) mais c est un BRUIT PREEXISTANT (la ligne 87-88 de
   valider-nommage exclut tests/ de la validation -- convention propre test-NNN-*).
## [NOTE] 2026-08-09 -- ARRET TECHNIQUE AVANT ACTIVATION JANUS (lecon Cerberus)
Morpheus s est arrete avant d activer Janus : cause = 3 appels d outils echoues
(JSON Parse error) sur des commandes bash trop complexes (guillemets imbriques +
chemins MSYS dans python -c). L activation de Janus a ete rejouee au tour suivant
(22:53) sans perte : la chaine est completee. Regle operationnelle documentee dans
les corrections de Cerberus : preferer un script .py temporaire aux commandes bash
inlined avec echappements multiples.

## [LECON] 2026-08-09 -- TEST-005 GENERATEURS-COMMANDE MIS A JOUR (26/26 OK) (Morpheus)

**Mission** (DELEGATION DES TESTS, depuis Buffy) : mettre a jour les 3 valeurs de version figees du test-005 apres le fix du generateur v0.2.1 -> v0.2.2 et le catalogue v0.2.3 -> v0.2.4.

**Livrables** :
1. Valeurs mises a jour dans test-005-generateurs-commande.py : KO1 py --version v0.2.1 -> v0.2.2, KO2 sh --version v0.2.1 -> v0.2.2, KO14 catalogue 0.2.3 -> 0.2.4, + en-tetes/doc (GENERATEUR v0.2.2, titre du test).
2. Lecons : 2 references v0.2.1 conserves = historique (ligne 11 : "Corrige py v0.2.1 + sh v0.2.1" decrit le fix passe, PAS une valeur attendue). Toujours verifier chaque occurrence : valeur attendue (a corriger) vs reference historique (a conserver).
3. Execution complete : 26 OK / 0 KO. ASCII 0, LF pur, py_compile OK. Test uniquement (aucun changement generateur/catalogue).

**Lecon** : quand un test verifie des versions, distinguer (a) les valeurs attendues (assertions, doc du plan) a mettre a jour, (b) les references historiques dans les commentaires a conserver. La regle des 5 fichiers ne s'applique pas ici : le test n'a pas de spec (c'est un fichier de test, convention propre).

**Verification impact** : detecter-impacts sur le test modifie -> le seul fichier impacte est le test lui-meme (aucun outil ne reference le test-005).
## [LECON] 2026-08-09 -- TEST-005 MIS A JOUR APRES MIGRATION (atlas v0.2.0, 26/26 OK)

**Mission** : mettre a jour test-005 apres migration des 4 parcours (delegation Buffy).
**Resultat** : test-005 26/26 OK, ASCII 0, LF pur.

**Lecons** :
1. LA REALITE AVANT LA MISSION : la mission annoncait "plus de commande en dur apres migration" mais le scan reel montre que c30 a TOUJOURS sa commande template (cartographier-parcours.py {parcours}) - le residu est conserve et documente, pas supprime. Le test point 18 (1 seul residu c30) reste valide.
2. La mise a jour d'un test porte sur les VALEURS ATTENDUES (version 0.2.0) et les libelles, pas sur les faits de l'existant (residu c30).
3. L'historique du docstring (v0.1.1 -> v0.1.2 -> v0.1.10 -> v0.2.0) documente la chronologie - ne pas l'effacer, seulement ajouter l'etape migration.
4. 7 remplacements chirurgicaux (docstring, historique, cas couverts, header, commentaire section, 2 verifications version) - jamais de reecriture complete du test.
5. Les 2 occurrences restantes de 0.1.10 sont dans l'historique documentaire (lignes 18/20) : conservees volontairement.
6. Verification complete : execution reelle 26/26 OK (navigation atlas, valider-cartes-decision CONFORME, ASCII 0 sur 4 fichiers) + valider-conformite-ascii + LF pur.
7. Un KO futur sur le point 18 signalera une REGRESSION reelle (commande en dur supplementaire), pas un faux positif.

**Fichier modifie** : test-005-generateurs-commande.py (version atlas 0.1.10 -> 0.2.0, historique + cas couverts).

## [LECON] 2026-08-10 -- valider-cartes-decision v0.3.1 TESTE (Morpheus, VERDICT VALIDE)

**Mission** : tester formellement valider-cartes-decision v0.3.1 apres l'ajout du type action
(impact oublie de la migration des 11 parcours).

**Resultats** :
1. tester-valider-cartes-decision.sh : 24/24 VALIDE (2 KO initiaux corriges : les tests 1-2
   comparaient --version a 0.3.0 au lieu de 0.3.1 - le comparateur attendu n'avait pas ete
   mis a jour, seul le grep l'avait ete)
2. Non-regression --tous : 11 agents verifies / 11 conformes / 0 non conforme
3. test-005 generateurs-commande : 26 OK / 0 KO
4. ASCII 0 + LF pur sur les 4 fichiers de l'outil

**Lecons** :
1. Quand on met a jour une version d'outil, verifier DANS LE TEST les 2 cotes de chaque
   comparaison : l'extraction (grep -o) ET le comparateur attendu (= '0.3.x') - un script
   de mise a jour qui ne touche que le grep laisse des tests KO silencieux
2. Le test formel (tester-*.sh) est le juge final : la verification manuelle (11/11 conformes)
   ne suffit pas, il faut AUSSI executer le test formel apres chaque correction
3. Detection d'un piege d'outil : valider-cartes-decision etait obsolete pour le type action
   mais la migration semblait terminee - toujours verifier les VALIDATEURS du modele apres
   une migration de format

## [LECON] 2026-08-10 -- GUIDER-PARCOURS v0.5.0 TESTE (Morpheus, VERDICT VALIDE 9/9)

**Mission** : tester formellement la correction de la divergence guider-parcours
(bump de version 0.4.0 -> 0.5.0 sur py/sh/md par Vulcain).

**Resultats** : 9/9 OK. Parite --version py/sh = v0.5.0/v0.5.0, navigation
--liste parcours-vulcain OK, navigation janus avec refs resolues, valider-
cartes-decision --tous 11/11, ASCII 0 + LF pur (3 fichiers), evaluer-coherence
0 lien casse, detecter-divergences-version : guider-parcours ALIGNE.

**Lecons** :
1. La parite --version py/sh est la premiere preuve d un bump de version
   reussi - les 2 affichent 0.5.0, la divergence est resorbee (0 DIVERGENTE)
2. La navigation reelle (--liste + --reponses) confirme que le bump n a rien
   casse : les refs sont resolues, le type action s execute sans question
3. La chaine Vulcain -> Morpheus fonctionne sans repasser par Cerberus :
   Vulcain m a active, je le reactive avec mon rapport de tests
## [LECON] 2026-08-10 -- TEST-018-FINS-REACTIVATION CREE (Morpheus, VERDICT VALIDE 9/9)

**Mission** : creer le test formel test-018-fins-reactivation verifiant les fins REACTIVER-CERBERUS precisees (condition activation directe) dans les 11 parcours.

**Test cree** : `cerveau-projet/agents/tools/tester/tests/test-018-fins-reactivation/test-018-fins-reactivation.py` (9 points, 9/9 OK).

**Ce que le test verifie** :
1. Aucun parcours n'a plus d'une fin REACTIVER-CERBERUS (controleur de chaine unique)
2. Les 6 fins REACTIVER identifiees (atlas, clio, janus, minerve, morpheus, themis)
3. Regle Pattern 13 : toute fin REACTIVER porte la condition (activation directe) OU est le dernier maillon (janus c10 : bilan consolide)
4. Les 4 fins precisees (atlas c11, clio c12, minerve c10, themis c13) portent EXACTEMENT 'activation directe par Cerberus'
5. Navigation reelle vers les 4 fins : PARCOURS TERMINE + condition affichee
6. Anti-regression : aucune fin 'Activer X' ne contient la commande reactiver (le piege corrige reste elimine)
7. ASCII strict 0 + LF pur 0 sur le test + les 11 parcours

**Lecons** :
1. **Tous les parcours n'ont pas de fin REACTIVER-CERBERUS** : athena, buffy, cerberus, promethee et vulcain finissent par ACTIVER un autre agent (maillon de chaine) -- la regle est 'au plus une par parcours', pas 'une dans chaque parcours' (mon premier jet comptait 11, corrige a 6).
2. **Le titre des fins varie en casse** ('FIN - Reactiver Cerberus' vs 'REACTIVER CERBERUS') : normaliser avec .lower() pour la detection.
3. **La navigation --case vers une fin affiche 'PARCOURS TERMINE'** : c'est la signature fiable pour verifier une fin depuis guider-parcours.
4. **Le test-018 protege contre la regression du piege reactiver** : toute nouvelle fin 'Activer X' avec la commande reactiver sera detectee au prochain passage.
## [LECON] 2026-08-10 -- GARDE-FOU TEST-018 AJOUTE AU PROTOCOLE-TESTS (Morpheus)

**Mission** : ajouter dans le protocole-tests la regle : apres toute modification d'une fin de parcours, le test-018 doit rester vert (garde-fou automatique).

**Action realisee** : protocole-tests.001.01.ebauche.md v0.2.1 -> v0.2.2, sous-section  Garde-fous de non-regression  ajoutee dans la section  Delegation des tests  (REGLE IMMUABLE -- GARDE-FOU FIN DE PARCOURS) : definition d'une fin de parcours (type fin, titres FIN - Reactiver Cerberus / FIN - Activer X), commande d'execution du test-018, rappel de ce qu'il verifie (Pattern 13, 4 fins precisees, anti-regression piege reactiver), verdict attendu 0 KO, correction avant validation.

**Lecons** :
1. **Le garde-fou protege contre la regression du piege reactiver** : toute future modification d'une fin de parcours (titre, message, commande) sera verifiee par le test-018 -- l'anti-regression est maintenant exigee par le protocole, pas seulement par la diligence de l'agent.
2. **La regle s'integre dans la section Delegation** : c'est le bon endroit car elle renforce la REGLE IMMUABLE existante (Morpheus execute les tests) -- le garde-fou est un cas particulier de la delegation.
3. **Versionnage du protocole** : 0.2.1 -> 0.2.2 (bump mineur pour l'ajout d'une regle) -- la version est la source de verite pour detecter les divergences.
4. **Verification finale** : ASCII 0, LF pur, test-018 reste 9/9 apres la modification du protocole (la regle n'affecte pas les parcours, elle les protege).
## [LECON] 2026-08-10 -- VERSIONS OBSOLETES TEST-013/TEST-016 CORRIGEES (Morpheus, VERDICT VALIDE)

**Mission** : corriger les versions attendues obsoletes des tests (test-013 cerberus v0.3.1, test-016 buffy v0.3.3) pour reverdir la non-regression.

**Actions realisees** :
1. **test-013-cerberus-migration.py** : version attendue 0.3.0 -> 0.3.1 (docstring en-tete, titre du test, cas couverts, verification). 22/22 OK (avant 21/22).
2. **test-016-migration-buffy.py** : version attendue 0.3.1 -> 0.3.3 (cas couverts + verification). 20/20 OK (avant 19/20). Attention : les mentions 0.3.1 HISTORIQUES (fiche buffy Pattern 14, branchement generateurs-ligne v0.3.1) ont ete CONSERVEES -- seule la version courante attendue change.
3. Non-regression : test-018-fins-reactivation 9/9 OK, py_compile OK, ASCII 0, LF pur.

**Lecons** :
1. **Distinguer version HISTORIQUE et version COURANTE attendue dans un test** : le docstring d'un test documente l'historique des evolutions (ne pas toucher), seul le champ de verification courant doit etre mis a jour. Le remplacement global serait destructeur.
2. **La divergence de version etait purement cosmetique** : les compteurs de types (18/4/4/2 et 32/7/2/9) correspondaient deja aux parcours reels -- seule la version attendue n'avait pas ete bumpee apres l'evolution des parcours.
3. **REGLE IMMUABLE respectee** : seul Morpheus a touche aux fichiers de test (conformement au protocole-tests v0.2.2 et au choix utilisateur) -- la modification de version dans un test reste une adaptation de test, donc du domaine de Morpheus.
## [LECON] 2026-08-10 -- 3 TESTS CORRIGES APRES SCAN (Morpheus, VERDICT VALIDE)

**Mission** : corriger les 3 tests a problemes detectes par le scan (test-009, test-010, test-012) suite a la recommandation de la lecon Themis.

**Actions realisees** :
1. **test-010-generateurs-case** : version attendue v0.3.1 -> v0.4.0 (l outil generateurs-case est passe a v0.4.0). 25/25 OK (avant 24/25). Mention historique  etape 5 v0.3.1  conservee.
2. **test-012-guider-parcours** : version attendue v0.4.0 -> v0.5.0 (guider-parcours est a v0.5.0). 18/18 OK (avant 17/18). Mention historique  Consolidation v0.4.0 (2026-08-09)  conservee.
3. **test-009-valider-case** : TEMOIN REBASE -- le parcours-morpheus (temoins  non migre avec >= 10 surcharges ) est desormais CONFORME (parcours migre). Nouveau temoin : parcours-janus (seul A ALLEGER, 3 surcharges), seuils adaptes de >= 10 a >= 3 dans les points 3e, 6, 8 + docstring. 20/20 OK (avant 17/20).

**Lecons** :
1. **La migration des parcours a change la donne pour les temoins de test** : plus aucun parcours reel avec >= 10 surcharges -- le temoin A ALLEGER est passe de morpheus a janus (3 surcharges). Les temoins de test doivent etre revus apres chaque grande migration (meme classe que la lecon des versions attendues).
2. **Distinguer version HISTORIQUE et version COURANTE** : les mentions  etape 5 v0.3.1  et  Consolidation v0.4.0 (2026-08-09)  documentent l historique et sont conservees ; seules les verifications courantes changent.
3. **Le scan complet (test-009 a test-018) est l outil de non-regression fiable** : il a revele 3 KO reels (2 versions + 1 temoin) -- apres chaque refonte d outil ou de parcours, re-scanner toute la suite.
4. **Non-regression finale** : test-009 20/20, test-010 25/25, test-012 18/18, test-013 22/22, test-016 20/20, test-018 9/9 -- toute la suite est verte.
## [LECON] 2026-08-10 -- REGLE RE-SCAN COMPLET AJOUTEE AU PROTOCOLE-TESTS (Morpheus)

**Mission** : ajouter dans le protocole-tests la regle : re-scanner toute la suite (test-009 a test-018) apres chaque refonte d'outil ou de parcours.

**Action realisee** : protocole-tests.001.01.ebauche.md v0.2.2 -> v0.2.3, REGLE IMMUABLE -- RE-SCAN COMPLET ajoutee dans la section  Garde-fous de non-regression  (apres le garde-fou FIN DE PARCOURS) : definition des refontes (outil : bump de version, interface ; parcours : migration, cases/fins), commande de scan en boucle sur test-009 a test-018, verdict 0 KO, les 2 lecons associees (versions attendues apres bump, temoins apres migration), rappel que seul Morpheus adapte les tests obsoletes avant validation.

**Lecons** :
1. **Le protocole-tests devient un vrai verrou de non-regression en 2 volets** : GARDE-FOU FIN DE PARCOURS (test-018 apres modification de fin) + RE-SCAN COMPLET (toute la suite apres refonte d'outil ou de parcours) -- les deux sont des REGLES IMMUABLES documentees.
2. **La regle RE-SCAN COMPLET generalise la lecon du scan du jour** : les 3 KO detectes (test-010 version, test-012 version, test-009 temoin rebase) sont devenus les 2 cas types documentes (versions attendues + temoins) -- la prochaine refonte saura quoi chercher.
3. **La commande de scan est simple et executable** : boucle bash sur les dossiers test-0*/ avec execution du .py -- 10 tests executes, 0 KO partout a la verification.
4. **Verification finale** : protocole v0.2.3, ASCII 0, LF pur, scan complet 10/10 vert (test-009 a test-018).
## [LECON] 2026-08-10 -- TEST-019 COMBO-CONTROLE-BUFFY CREE (Morpheus, VERDICT 11/11 VALIDE)

**Mission** : tester formellement le combo-controle-buffy v0.1.0 (cree par Vulcain pour alleger c11/c18 du parcours janus, Pattern 16 ALLEGEMENT).

**Livrables** : cerveau-projet/agents/tools/tester/tests/test-019-combos-controle-buffy/ (py + md), 11/11 points passes, ASCII 0 + LF pur.

**Lecons** :
1. Le format special de nommage des tests est reconnu automatiquement par valider-nommage (regex test-XXX-nom + dossier parent test-*) : pas besoin de --type test (type inconnu), le scan --recursive sur le dossier ne compte rien (Total 0) car le dossier test-XXX n'est pas une structure d'outil standard -- le nommage est valide par le format special.
2. Le combo-controle-buffy couvre le rappel des regles (pattern-2 ASCII, pattern-12 creation limitee) + lecture du protocole-controle-buffy + creation du fichier de controle : c'est le gabarit type d'un combo d'allegement de cases de controle (Pattern 16, levier B).
3. Navigation de secours a tester ABSOLUMENT : c1=NON et c1=OUI;c2=NON -> c5 FIN REGLES NON RESPECTEES (les garde-fous des 2 patterns sont preserves).
4. Variable manquante {fichier_controle} -> erreur claire avec mention de la case c4 (teste).
5. Piege Windows : chemin en FORWARD SLASHES pour --var (protocole-creation-combos).
6. La suite de tests s'etend : test-019 ajoute (regle RE-SCAN COMPLET couvre maintenant test-009 a test-019).
## [LECON] 2026-08-10 -- NON-REGRESSION POST-ALLEGEMENT JANUS (Morpheus, test-019 reverdi + test-009 corrige)

**Mission** : etape 3 - relancer la suite apres l'allegement du parcours janus (c8/c11/c18, v0.3.3, Pattern 16).

**Resultat** : test-019-combos-controle-buffy 11/11 VALIDE (reverdi sans changement), test-009-valider-case 20/20 VALIDE (CORRIGE : temoin artificiel).

**Lecons** :
1. Le test-019 ne depend PAS du parcours janus (il teste le combo directement) : reverdi sans modification. AUCUN autre test ne reference parcours-janus sauf test-009.
2. DECOUVERTE IMPORTANTE : le test-009-valider-case utilisait le parcours janus comme TEMOIN REEL du verdict A ALLEGER (attendu >= 3 surcharges). Apres l'allegement (janus CONFORME), le test tombait a 17/20 avec 3 KO (3e, 6, 8b). C'est la preuve que l'allegement a bien resorbe les 3 surcharges reelles.
3. SOLUTION DURABLE : fabriquer un TEMOIN ARTIFICIEL dans le dossier temp (copie de parcours-cerberus + 3 indices regle de 200 car. ajoutes a 3 cases) via la fonction fabriquer_temoin_surcharge() - le test ne depend plus de l'etat des parcours reels (aucun parcours n'est plus en surcharge dans le projet).
4. Regle : un test qui depend d'un etat reel (ici un parcours en surcharge) casse des que cet etat change - toujours preferer un temoin artificiel genere dans tmp.
5. valider-cartes-decision : 11/11 CONFORMES (janus inclus), re-confirme apres allegement.

**Statut** : suite reverdie (test-009 + test-019), 0 regression. Prochaine etape : audit Themis (protocole sante E5b sur la fiche janus vs carte v0.3.3).
## [LECON] 2026-08-10 -- TEST-014 CORRIGE + NON-REGRESSION 11/11 REVERDIE (Morpheus)

**Mission** : adapter le test-014-spec-guider-parcours aux versions reelles (spec v0.6.0 + 16 patterns) puis reverdir la non-regression.

**Resultat** : test-014 12/12 (corrige), non-regression test-009 a test-019 = 11/11 VALIDE, 0 KO.

**Lecons** :
1. Le test-014 attendait des versions OBSOLETES : spec v0.5.0 + 15 patterns. La spec est en v0.6.0 avec 16 patterns (Pattern 16 ALLEGEMENT ajoute par Buffy lors de sa reecriture).
2. DECOUVERTE : la spec elle-meme avait une INCOHERENCE interne (titre ligne 7 = v0.5.0, Version ligne 9 = 0.6.0) - le titre n'avait pas ete bumpe lors de la reecriture du Pattern 16. Le test-014 (1a) l'a detectee : corrigee en v0.6.0.
3. DECOUVERTE : les refs documentaires guider-parcours.md et vulcain.md (Spec du format) pointaient v0.5.0 - mises a jour en v0.6.0 (points 6a/6b du test). ATTENTION : vulcain.md ligne 60 (PARCOURS (v0.5.0)) est le point 1 de l'audit Themis RESERVE a Buffy (version de fiche vs version de parcours) - ne pas confondre avec la ligne 71 (Spec du format).
4. Processus : corriger le test ET les fichiers qu'il verifie (spec, docs) ensemble - un test qui attend une version impose que les refs documentaires soient synchronisees.
5. La non-regression complete (test-009 a test-019) est reverdie : 11/11 verts.

## [LECON] 2026-08-10 -- TEST-020 COMBOS CLIO CREE (Morpheus, VERDICT 46/46 VALIDE)

**Mission** : ecrire le test formel des 3 combos Clio v0.1.0 (Vulcain a cree, delegation des tests).
**Resultat** : test-020-combos-clio : 46 OK / 0 KO. Non-regression test-009 a test-020 : 12/12 verts.

**Combos testes** :
1. combos-analyse-projet (orchestre py/sh/md) : etat reel + ecarts README vs realite
2. combo-maj-readme (encapsule definition-combo.json, 5 cases) : petite MAJ
3. combos-maj-readme-massive (orchestre py/sh/md) : grosse MAJ conservative

**Cas couverts** : nommage (7 fichiers), versions 0.1.0, JSON valide (5 cases),
execution reelle des 2 orchestres sans --rapport, combos-moteur --liste,
dry-run c2=OUI (verifier->maj->ascii) et c2=NON (verifier->ascii), parite .sh,
ASCII + LF sur les 7 fichiers.

**Lecons** :
1. Piege de test : la DESCRIPTION du combo encapsule mentionne --maj dans son
   texte mais la navigation c2=NON ne l'EXECUTE pas - verifier l'absence dans
   la partie apres [DRY-RUN] (out.split("DRY-RUN]")[1]) et non dans tout le
   flux de sortie
2. Les tests de combos doivent executer SANS --rapport (aucune creation de
   fichier pendant les tests)
3. Le dossier du test-019 s'appelle test-019-combos-controle-buffy (avec 's' a
   combos) - le nouveau test est test-020 (dernier numero)
4. Chaque combo orchestre est teste en execution reelle complete (les 5 etapes
   de la grosse MAJ) - pas seulement --version
5. Outils utilises : lire-fichier, activer-agent-principal ; execution via
   subprocess dans le test (jamais de commande directe)

## [LECON] 2026-08-10 -- Test reel pilote Pattern 17 (themis v0.3.2)

**Contexte** : test reel du pilote Pattern 17 (rapport de fin -> detection d ameliorations -> ligne d auto-amelioration) dans le parcours themis v0.3.2 (cases c12b/c12c/c12d/c12e).
**Verdict** : VALIDE 8/8.
**Lecons** :
1. Navigation branche OUI complete et visible : [29/32] Ameliorations possibles -> [30/32] generateur (commande reelle --theme ameliorer-agent generee + indice PASSE PAR LE GENERATEUR) -> [31/32] Activer l agent habilite -> [32/32] FIN Reprise
2. Navigation branche NON directe : [29/32] -> FIN Reactiver Cerberus (pas de passage par le generateur)
3. Generation reelle du theme ameliorer-agent : rc=0, 1460 caracteres, 5 questions
4. Les 6 protocoles-autoameliorer (agents, cerveau, conventions, outils, protocoles, regles) existent tous dans regles-immuables/general
5. Normes : ASCII 0 + LF pur sur spec v0.6.1, parcours v0.3.2, themes-amelioration.json
6. Le pilote est pret pour la generalisation aux 10 autres parcours

## [LECON] 2026-08-10 -- Test complet 11 themes generateur amelioration (Morpheus, VALIDE 6/6)

**Contexte** : garde-fou non-regression sur themes-amelioration.json v2.2.0 (11 themes, 64 questions) - generation reelle de chacun, --liste, theme inconnu, normes, coherence carte themis c12d.
**Verdict** : VALIDE 6/6.
**Lecons** :
1. Generation reelle confirmee pour les 11 themes : ameliorer-outil (14 questions) + 10 themes de 5 questions = 64 au total
2. --liste rc=0 affiche exactement les 11 themes (affiches=11, correspondance avec le JSON)
3. Theme inconnu -> rc=1 avec message (gestion d erreur correcte)
4. Coherence transverse : la regle c12d de la carte themis reference bien les 11 themes et la couverture des 6 protocoles-autoameliorer est complete (singulier/pluriel : agent/outil/protocole)
5. JSON v2.2.0 valide, tri alphabetique, ids uniques, ASCII 0 + LF pur
6. Garde-fou non-regression : ce test de repere (VALIDE 6/6) sert de base pour les futures evolutions du generateur

## [LECON] 2026-08-10 -- NON-REGRESSION APRES GENERALISATION PATTERN 17 (Morpheus)

**Contexte** : mise a jour des versions attendues (test-013 cerberus 0.3.1->0.3.2, test-016 buffy 0.3.3->0.3.4, test-005 atlas 0.2.0->0.3.1) + comptages de cases (2a/2b) apres insertion P17, puis non-regression ciblee.
**Verdict** : TESTS CORRIGES (versions + comptages) MAIS 1 PROBLEME DE FOND NON-TEST detecte : les regles P17 des cases Xc/Xd (copiees depuis themis c12c/c12d) font 172 et 492 caracteres - elles violent le garde-fou REEL "regle <= 160 caracteres" de valider-case (points 3b/3c/9 KO sur test-013 et test-016).
**Lecons** :
1. Le garde-fou valider-case impose regle <= 160 caracteres - les regles longues P17 doivent etre raccourcies dans les 11 parcours (themis inclus, c12c=172 et c12d=492) par Buffy (domaine cartes)
2. Le modele themis P17 copie tel quel propage le defaut - la generalisation a duplique les regles trop longues
3. test-013 : apres correction comptages, il reste 1 KO (3b) ; test-016 : 3 KO (3b/3c/9) - tous lies aux regles longues
4. L avertissement cerberus c5 (pattern de re-essai NON->soi-meme) est un faux positif preexistant, voulu
5. La sequence correcte : Buffy corrige les regles (<= 160 car) -> Morpheus relance la non-regression pour reverdir

## [LECON] 2026-08-10 -- VALIDATION FINALE GENERALISATION PATTERN 17 (Morpheus, 18/20 OK)

**Contexte** : validation finale de la non-regression complete (test-001 a test-020) apres la generalisation du Pattern 17 aux 11 parcours + corrections Buffy (regles <= 160 car, commandes en dur retirees, suivant retire des Xb).
**Verdict** : CONFORME - 18/20 tests OK, 2 KO PREE XISTANTS hors perimetre P17.
**Lecons** :
1. Non-regression complete : 18 tests verts (dont test-005 26/26, test-006 19/19, test-013 22/22, test-014 12/12, test-016 20/20 - tous reverdis apres adaptation)
2. Les 2 KO restants sont PREE XISTANTS et documentes : test-004 (parcours morpheus attend v0.1.3, actuel v0.3.1 - version obsolete depuis la migration morpheus) et test-007 (catalogue attend 109 commandes, actuel 118 - obsolete depuis l ajout des 3 combos Clio). Aucun lie a la mission P17
3. valider-cartes-decision --tous : 11/11 CONFORME - toutes les cartes restent valides apres insertion P17
4. La chaine complete est stable : 11 parcours avec Pattern 17 (case alternative Ameliorations possibles + ligne d auto-amelioration), chaque fin suivant SA carte (Pattern 13)
## [LECON] 2026-08-10 -- CORRECTION KO PREEXISTANT test-007 (Morpheus)

**Mission** : corriger les valeurs attendues obsoletes du test-007 (test-figer-lf) pour reverdir la non-regression complete.
**Verdict** : VALIDE 15/15 - non-regression 19/20 OK (seul test-004 reste KO, preexistant documente).
**Lecons** :
1. Les valeurs attendues obsoletes etaient dans le test : catalogue 109 -> 118 commandes, index-tools total 108 -> 110 (le "| Corriger | 6 |" ligne 411 etait deja correct, seul le Total avait change)
2. La correction doit couvrir TOUTES les occurrences (8 points : 4 x libelles + 4 x code/verifications) - ne pas seulement corriger le code, les libelles des verifier() doivent etre synchronises
3. Avant de modifier un test, verifier les valeurs reelles dans les sources (catalogue-commandes.json version 0.2.5, index-tools.md Total ligne 436) - ne jamais deviner
4. Normes respectees : ASCII 0, CRLF 0 sur le test modifie
5. Le KO test-004 (parcours morpheus v0.1.3) est PREEXISTANT et hors perimetre : il necessite une mission dediee (mise a jour de la version attendue du parcours-morpheus, actuellement v0.3.1)
## [LECON] 2026-08-10 -- CORRECTION DERNIER KO PREEXISTANT test-004 (Morpheus)

**Mission** : corriger la version attendue obsoletes du test-004 (test-combos-tester-outil) pour atteindre 20/20 de non-regression complete.
**Verdict** : VALIDE - NON-REGRESSION COMPLETE 20/20 OK (0 KO).
**Lecons** :
1. La version attendue du parcours morpheus etait obsolete : v0.1.3 -> v0.3.1 (verifiee dans parcours-morpheus.json)
2. 3 occurrences synchronisees (libelle en-tete ligne 19, commentaire ligne 134, verification code ligne 137) - ne jamais corriger seulement le code, les libelles doivent suivre
3. Normes respectees : ASCII 0, CRLF 0 sur le test modifie
4. La non-regression complete est maintenant 20/20 : aucun KO preexistant ne subsiste dans la suite formelle (test-001 a test-020)
5. Lecon transverse : la mise a jour des versions attendues doit etre faite par Morpheus (protocole-tests), jamais par un autre agent, meme pour une simple valeur
## [LECON] 2026-08-10 -- TEST-006 ADAPTE APRES RETRAIT SUIVANTS MORTS (Morpheus)

**Mission** : adapter test-006-cartographier-parcours au nouveau nombre de chemins atlas (45 -> 39) apres le retrait des suivant morts (6 chemins fantomes en moins).
**Verdict** : VALIDE - NON-REGRESSION COMPLETE 20/20 OK.
**Lecons** :
1. Les suivant morts des cartes creaient des chemins FANTOMES comptes par le cartographe : le retrait les elimine (atlas 45 -> 39, themis 210 -> 48)
2. Toute correction structurelle de cartes impacte le nb de chemins -> verifier test-006 et adapter la valeur attendue (2 occurrences : libelle ligne 15 + verification ligne 117)
3. Les fichiers cartographie-*.md generes pendant un audit sont des RESIDUS a nettoyer (test-017 les detecte) - le cartographe les cree a chaque execution
4. Normes respectees : ASCII 0, CRLF 0
5. La non-regression complete est 20/20 : suite formelle entierement verte apres la correction
## [LECON] 2026-08-10 -- GARDE-FOU SUIVANT MORT TESTE (Morpheus, VERDICT VALIDE)

**Mission** : tester formellement valider-cartes-decision v0.3.2 apres l'ajout
du garde-fou suivant mort (controle 7).

**Ce qui a ete fait** :
1. tester-valider-cartes-decision.sh mis a jour : versions 0.3.1 -> 0.3.2
   (points 1-2, qui etaient les 2 KO) + 4 nouveaux points (25-28) testant le
   controleur 7 sur un parcours infeste : NON CONFORME, erreur 'Suivants
   morts' presente, 'fin avec suivant' detectee, 'branches priment' detectee.
2. Test local : 28/28 VALIDE.
3. Verification des references 0.3.1 dans les tests formels : les mentions
   dans test-004 (parcours morpheus v0.3.1), test-005 (parcours atlas v0.3.1),
   test-016 (parcours buffy v0.3.1) et test-010/012 (generateurs-case v0.3.1)
   concernent D'AUTRES versions de parcours/outils, PAS valider-cartes-decision
   -> AUCUNE modification requise (les appels a valider-cartes se font par
   chemin sans verification de version).
4. Non-regression complete : 19/20 OK.

**KO restant : test-003-combos-creer (PREEXISTANT, hors perimetre)** :
- Point 7a : 'dry-run retourne 0: attendu=0, obtenu=1'
- Concerne combo-creer-protocole (createur-fichier en --dry-run), AUCUN lien
  avec valider-cartes-decision (prouve : test-003 ne reference aucun des
  fichiers modifies par cette mission)
- A traiter dans une mission dediee (createur-fichier / combo-creer dry-run)

**Lecons** :
1. Quand un test affiche 'X KO' dans son resume, ne pas confondre le compteur
   interne ('0 KO') avec un echec reel : le critere fiable est la presence de
   'NON VALIDE' ou le code de sortie, pas la sous-chaine 'KO' (piege de
   parsing)
2. Toute nouvelle version d'outil cree un KO sur le test local si la version
   attendue n'est pas synchronisee : la mise a jour des versions fait partie
   du travail de test (Morpheus), pas du travail de construction (Vulcain)
3. Les references de versions dans les tests formels peuvent concerner
   d'autres composants : verifier le CONTEXTE avant de modifier (ex: 'v0.3.1'
   = parcours morpheus/atlas/buffy, pas valider-cartes-decision)
4. Verifier les fichiers .pyc dans git status : un __pycache__ modifie est un
   artefact a nettoyer, jamais a committer
## [LECON] 2026-08-11 -- TESTS ADAPTES APRES CORRECTION COMBO-CREER-* (Morpheus)

**Mission** : adapter les tests apres la correction des combos creer-* et du
catalogue (Vulcain, catalogue v0.2.6).

**Ce qui a ete fait** :
1. test-003-combos-creer : ajout de la variable 'contenu=contenu' aux vars de
   combo-creer-agent (ligne 56) car la case c8 (creer-fichier) exige desormais
   la variable contenu (la definition du combo passe {contenu}). Resultat :
   89/89.
2. test-005-generateurs-commande : point 14 catalogue version 0.2.5 -> 0.2.6
   (label + verification). Resultat : 26/26.
3. Non-regression complete : 20/20 OK, 0 KO.

**Lecons** :
1. Quand un combo evolue (ajout d'un parametre obligatoire comme contenu),
   le test formel qui fournit les vars doit etre mis a jour EN MEME TEMPS que
   la definition du combo - sinon le test echoue en 'Variable non trouvee'
   (erreur de test, pas de l outil)
2. La version du catalogue est testee par test-005 : toute modification du
   catalogue (modele/parametres/version) entraine une adaptation du point 14
3. La chaine complete Vulcain (correction) -> Morpheus (tests) a elimine le
   KO preexistant test-003 qui durait depuis plusieurs missions : les 20
   echecs initiaux (cles obsoletes fichier/source/destination vs catalogue)
   sont resorbes
4. La non-regression 20/20 est la base de confiance : toute future
   modification de catalogue ou de combo doit re-verifier test-003 et test-005

**Resultat** : NON-REGRESSION COMPLETE 20/20 OK, 0 KO.
## [LECON] 2026-08-11 -- GARDE-FOU CLES COMBOS TESTE (Morpheus, VERDICT VALIDE)

**Mission** : tester le garde-fou des cles des definitions-combo vs catalogue
(combos-moteur v0.3.0 + detecter-decalages-catalogue v0.1.1).

**Ce qui a ete fait** :
1. test-002-combos-moteur : nouveau Test 13 (5 points) ajoute :
   - 13a : combo avec cle hors catalogue (fichier au lieu de chemin pour
     valider-conventions) -> REJETE code 1
   - 13b : erreur claire 'hors catalogue' presente
   - 13c : erreur cite la cle fautive ET la commande ciblee
   - 13d : combo avec cle exacte (chemin) -> ACCEPTE code 0
   - 13e : parite sh (le .sh embarque le garde-fou, rejette aussi)
   Resultat : 36/36 REUSSI.
2. test-003-combos-creer : 89/89 (les cles dry_run/recursive retirees par
   Vulcain ne changent pas les commandes generees).
3. Non-regression complete : 20/20 OK, 0 KO.

**Lecons** :
1. Un garde-fou de validation au chargement doit etre teste des deux cotes :
   (a) le rejet (cle fautive -> code 1 + erreur claire) et (b) l acceptation
   (cle conforme -> code 0) - sinon on ne prouve que la moitie du comportement
2. La parite py/sh d un outil embarque (heredoc) doit etre testee pour le
   NOUVEAU comportement aussi (13e : le .sh rejette comme le .py) - pas
   seulement pour --liste/navigation
3. Les definitions de test existantes de test-002 n utilisent pas de cases
   generateur avec catalogue : le nouveau garde-fou ne les a pas cassees
   (aucune adaptation necessaire, seul un ajout de points de test)
4. Le detecteur-decalages-catalogue (v0.1.1) confirme 14 combos scannes / 0
   probleme : la correction des 8 cles par Vulcain a assaini toutes les
   definitions

**Resultat** : NON-REGRESSION COMPLETE 20/20 OK, 0 KO.

## [LECON] 2026-08-11 -- NON-REGRESSION PARCOURS VULCAIN v0.3.3 (Morpheus, VERDICT VALIDE)

**Contexte** : Buffy a branche le scan COMBOS (detecter-decalages-catalogue section COMBOS) dans le parcours vulcain v0.3.3 (4 cases : c6b/c6c construction, c12b/c12c modification). Mission : confirmer que rien n'est casse.

**Lecons** :
1. Aucun test formel n'attend la version d'un parcours d'agent en dur : la non-regression (20/20 OK) passe sans adaptation meme apres un bump de version de carte (v0.3.2 -> v0.3.3).
2. test-014 reference 'vulcain' mais uniquement pour les patterns de la spec-guider-parcours (Pattern 12/14 cites comme exemples) : ce n'est pas une reference a la version du parcours.
3. La modification d'une carte de decision (ajout de cases alternatives) est sans impact sur les tests tant que la structure (valider-cartes CONFORME, navigation reelle OK) est respectee.
4. Le verdict de non-regression se fait avec les 20 tests de la suite formelle (test-001 a test-020), en executant chaque test et en verifiant l'absence de [KO].

## [LECON] 2026-08-11 -- TESTS ADAPTES APRES CORRECTION MASSIVE P12 (Morpheus, VERDICT VALIDE)

**Contexte** : Buffy a corrige 16 ecarts P12 (CREATION LIMITEE) sur 7 parcours, avec bump de version (atlas 0.3.2, buffy 0.3.5, clio v0.4.2, janus 0.3.5, themis 0.3.4, vulcain 0.3.5). Impact tests : test-005 verifiait atlas v0.3.1 et test-016 verifiait buffy 0.3.4.

**Lecons** :
1. test-005 (generateurs-commande) : 8 occurrences de la version atlas (lignes 6, 41-42, 115, 176-183) - tout remplacer 0.3.1 -> 0.3.2.
2. test-016 (migration-buffy) : 3 occurrences de la version buffy (lignes 21, 100-102) - remplacer 0.3.4 -> 0.3.5.
3. PIEGE : ajouter un indice CREATION LIMITEE a une case deja a 3 indices la fait passer a 4 -> valider-case signale une SURCHARGE (SEUIL_INDICES=3) et le test-016 point 10 casse. Solution : fusionner les indices outil qui pointent vers le MEME script (generateurs-case + generateurs-case-convertir -> 1 seul indice avec sous-commande). Toujours verifier apres ajout : aucune case > 3 indices.
4. test-009 et test-013 utilisent des TEMOINS ARTIFICIELS (fabriques dans le test) : ils ne verifient pas les vrais parcours, donc les surcharges des 6 parcours modifies ne les impactent pas.
5. La non-regression complete (20/20 OK) est le verdict final : adapter les versions attendues + verifier le seuil d'indices sur les parcours modifies + relancer la suite.

**Verdict** : VALIDE - 20/20 OK, 0 KO.

## [LECON] 2026-08-11 -- TESTS ADAPTES APRES OUTIL EDITER-FICHIER-AGENTS (Morpheus, VERDICT VALIDE)

**Contexte** : Vulcain a cree l outil editer-fichier-agents et l a ajoute au catalogue de commandes (version 0.2.6 -> 0.2.7, 118 -> 119 commandes).

**Lecons** :
1. Ajouter un outil au catalogue impacte 2 tests : test-005 (version catalogue 0.2.6, lignes 38 + 164) et test-007 (nombre de commandes 118, lignes 30 + 219-225).
2. La valeur 118 apparait dans test-007 en 4 endroits (commentaire + condition + 2 messages de verifier) : tout remplacer.
3. Apres adaptation, verifier qu'il ne reste AUCUNE occurrence des anciennes valeurs (grep 0.2.6 / 118) dans les tests (hors pyc).
4. La non-regression complete (20/20 OK) est le verdict final apres toute modification du catalogue.
5. Le detecteur detecter-decalages-catalogue peut etre long (timeout > 30s) : lancer avec --sortie et un timeout adapte.

**Verdict** : VALIDE - 20/20 OK, 0 KO.

## [LECON] 2026-08-11 -- TESTS ADAPTES APRES BRANCHEMENT EDITER-FICHIER-AGENTS (Morpheus, VERDICT VALIDE)

**Contexte** : branchement de editer-fichier-agents dans le parcours buffy v0.3.6 (nouvelle case c11b, branche 'fiche' dans c10b).

**Points adaptes dans test-016-migration-buffy** :
1. Version attendue 0.3.5 -> 0.3.6 (docstring + verification)
2. Nombre de cases action 34 -> 35 (message descriptif mis a jour avec c11b)
3. Historique docstring : ligne v0.3.6 ajoutee

**Lecons** :
1. Toute nouvelle case dans un parcours peut casser le compteur de types (action/question/fin) d'un test formel -- verifier les tests qui comptent les cases
2. La version du parcours est verifiee en dur dans test-016 : chaque bump de version exige l'adaptation du test (DELEGATION : Morpheus)
3. Le message descriptif du point 2a doit lister les cases speciales (c10d, c11b, c15c/c15d) pour rester lisible
4. NON-REGRESSION COMPLETE 20/20 OK apres adaptation -- la suite reste verte

**Outils utilises** : lire-fichier, str_replace, .zz-nonreg (script temporaire de non-regression), valider-conformite-ascii

## [LECON] 2026-08-11 -- TESTS ADAPTES APRES OUTIL VERIFIER-CONFORMITE-FICHE (Morpheus, VERDICT VALIDE)

**Contexte** : ajout de verifier-conformite-fiche au catalogue generateurs-commande (v0.2.8, 120 commandes).

**Points adaptes** :
1. test-005-generateurs-commande : version catalogue 0.2.7 -> 0.2.8 (2 occurrences : docstring + verification)
2. test-007-figer-lf : nombre de commandes 119 -> 120 (3 occurrences : docstring, ok_cat, messages -- dont 1 dans le bloc d'exception)

**Lecons** :
1. Le bloc d'exception d'un test peut contenir la meme valeur que la verification (message avec 119) -- verifier TOUTES les occurrences, pas seulement la condition
2. Le format de sortie des tests differe (certains affichent 'RESULTAT', d'autres 'BILAN') -- ne pas grepper un motif unique pour verifier le succes, utiliser le code de retour
3. Apres adaptation : NON-REGRESSION COMPLETE 20/20 OK -- la suite reste verte
4. Aucun autre test ne reference 119 ou 0.2.7 (grep global confirme)

**Outils utilises** : lire-fichier, str_replace, .zz-nonreg (script temporaire de non-regression), valider-conformite-ascii

## [LECON] 2026-08-11 -- NON-REGRESSION APRES REFONTE PAR ROLE (Morpheus, VERDICT VALIDE)

**Contexte** : refonte du template de fiche par role (noyau + variantes), outil verifier-conformite-fiche v0.2.1, 11 fiches corrigees, catalogue v0.2.9.

**KO detecte et corrige** : test-005-generateurs-commande attendait la version catalogue 0.2.8 mais le bump a 0.2.9 (ajout parametre variante) avait ete fait par Vulcain sans adapter le test. Adapte : 0.2.8 -> 0.2.9 (2 occurrences : docstring + verification).

**Validations finales** :
1. test-005 : 26/26 OK
2. NON-REGRESSION COMPLETE : 20/20 OK, 0 KO
3. verifier-conformite-fiche --tous : 11/11 CONFORME (0 ecart)
4. Normes : ASCII 0 + LF pur (test modifie)
5. 0 occurrence restante de 0.2.8 dans la suite

**Lecons** :
1. Apres une refonte du catalogue (bump de version), RE-SCANNER la suite (test-005 verifie la version) -- c'est la regle RE-SCAN COMPLET du protocole-tests
2. La verification finale croisee : non-regression + conformite des fiches -- deux angles complementaires (tests vs modele)
3. Le modele par role est operationnel : 11/11 fiches conformes au noyau + variante, avec les sections specifiques legitimes en avertissement non bloquant

**Outils utilises** : .zz-nonreg (script temporaire), valider-conformite-ascii, verifier-conformite-fiche (v0.2.1), str_replace
## [LECON] 2026-08-11 -- TEST-018 ADAPTE : FIN CLIO C12 DEVENUE 'ACTIVER JANUS' (Morpheus, VERDICT VALIDE)

**Mission** : adapter le test-018-fins-reactivation apres la transformation de la fin de clio (c12 : 'Reactiver Cerberus' -> 'Activer Janus', mission Buffy).

**Actions** :
1. Constat KO : 3 points cassaient (1b, 3, 4) car clio n'avait plus de fin REACTIVER-CERBERUS
2. Adaptation du test :
   - FINS_PRECISEES : clio retiree -> 3 agents (atlas c11, minerve c10, themis c13)
   - Point 1b : 6 -> 5 fins REACTIVER (atlas, janus, minerve, morpheus, themis)
   - Points 3 et 4 : '4 fins' -> '3 fins' (texte + compteurs)
   - NOUVEAUX points 4b/4c : garde-fou que clio c12 est bien 'FIN - Activer Janus' (REGLE IMMUABLE JANUS) + navigation reelle PARCOURS TERMINE
3. Verification : test-018 reverdi 11 OK / 0 KO + non-regression complete 20/20 + normes ASCII 0 / LF 0

**Lecons** :
1. Quand une fin change de nature (Reactiver -> Activer X), le test-018 exige une adaptation en 2 endroits : la liste des fins REACTIVER (1b) ET les fins precisees (3/4) - ne pas oublier le docstring de contexte
2. Ajouter un garde-fou POSITIF (4b/4c) pour la nouvelle fin : le test verifie desormais la presence de la fin Activer Janus de clio et sa navigabilite - il couvre ainsi les 2 natures de fins
3. guider-parcours --case c12 sur une fin Activer Janus retourne bien PARCOURS TERMINE sans 'activation directe' - c'est le comportement attendu pour une fin de chaine
4. La non-regression complete (20 tests) reste le filet final avant de rendre le verdict
## [LECON] 2026-08-11 -- TEST-018 GENERALISATION JANUS + NORMALISATION VERSIONS (Morpheus, VERDICT VALIDE)

**Mission** : adapter le test-018-fins-reactivation apres la generalisation de la REGLE IMMUABLE JANUS (atlas c11, themis c13, morpheus c14 transformees en FIN - Activer Janus par Buffy).

**Actions** :
1. Constat KO : 3 points (1b, 3, 4) - les fins REACTIVER n'etaient plus que 2 (janus c10, minerve c10)
2. Adaptation du test :
   - fins REACTIVER attendues : 2 (janus + minerve) au lieu de 5
   - FINS_PRECISEES : ne reste que minerve c10 (condition 'activation directe par Cerberus' conservee)
   - navigation : 1 fin precisee (minerve)
   - NOUVEAU garde-fou positif 4d : atlas c11 + themis c13 + morpheus c14 = fins 'FIN - Activer Janus' navigables (REGLE IMMUABLE JANUS)
3. Normalisation des versions : les 4 parcours touches (atlas, clio, morpheus, themis) stockaient 'v0.3.3' (avec prefixe v) alors que la convention est SANS prefixe (buffy, cerberus, vulcain...) - corrige vers '0.3.3' etc. Les FICHES gardent le prefixe v dans Pattern 14 (convention : parcours sans v, fiches avec v)
4. Tests de versions adaptes : test-004 (morpheus 0.3.1 -> 0.3.2), test-005 (atlas 0.3.2 -> 0.3.3)
5. Verification : test-018 12/12 OK + non-regression complete 20/20 + normes 0/0

**Lecons** :
1. La normalisation de version est une lecon transversale : 4 parcours sur 11 stockaient leur version avec un prefixe 'v' (incoherent) - verifier le format (parcours sans v / fiches avec v) a chaque bump
2. Le garde-fou 4d du test-018 verifie desormais la presence de TOUTES les fins Activer Janus (clio + atlas + themis + morpheus) : toute regression sur ces fins cassera le test
3. Ne reste que 2 fins REACTIVER dans le cerveau : janus c10 (legitime, dernier maillon) et minerve c10 (trio, hors perimetre) - si on etend la regle au trio un jour, le test-018 devra etre re-adapte
4. Chaque transformation de fin impose la verification en cascade : carte + fiche + test-018 + tests de version (test-004/test-005)
## [LECON] 2026-08-11 -- GARDE-FOU POSITIF COMMANDE ACTIVER DANS TEST-018 (Morpheus, VERDICT VALIDE)

**Mission** : renforcer le test-018 avec un garde-fou positif : toute fin 'FIN - Activer X' doit contenir la COMMANDE EXACTE d'activation (activer-agent-principal.py activer session-llm-1 <agent> '<raison>').

**Contexte** : probleme detecte par l'utilisateur - l'execution reelle ne suivait pas la carte (cloture Morpheus ecrite 'je reactive Cerberus' alors que sa carte dit 'FIN - Activer Janus'). Cause racine : les 8 fins 'Activer Janus' ne contenaient pas la commande exacte, l'executant retombait sur reactiver (qui ramene toujours a Cerberus). Buffy a enrichi les 8 messages avec la commande exacte.

**Action** : ajoute le point 5b dans la Passe 3 du test-018 : pour chaque fin 'FIN - Activer X' de tous les parcours, verification POSITIVE que le message contient 'activer-agent-principal.py activer' ET 'activer session-llm-1'. Le point 5 existant (anti-reactiver) est conserve.

**Verifications** : test-018 13/13 OK (point 5b vert), non-regression complete 20/20, normes 0 non-ASCII / 0 CRLF.

**Lecons** :
1. Le test-018 verifie desormais les 2 faces de la regle : NEGATIVE (pas de reactiver dans une fin Activer X - point 5) et POSITIVE (la commande activer exacte doit etre presente - point 5b). C'est la bonne forme de garde-fou.
2. Le point 5b aurait detecte le probleme avant qu'il n'arrive : toute fin 'Activer X' sans commande activer exacte fera echouer la non-regression
3. Le reflexe reactiver (qui ramene toujours a Cerberus) est le piege principal des chaines Agent -> Agent -> Cerberus : la commande exacte dans la fin est la seule protection fiable
## [LECON] 2026-08-11 -- TEST-005 AMELIORE + CONTRAT DOCUMENTATION .md (Morpheus)

**Mission** : ameliorer test-005 (verification .md present pour chaque commande du catalogue + commandes de test composables) et reverdir la non-regression apres le volet 1 Buffy (case c0d lecture doc dans les 11 parcours).

**Actions** :
1. Test-005 passe de 22 a 28 points : ajout du point 23 (chaque commande du catalogue 138 a son .md a cote du script - contrat LECTURE DOC) et point 24 (les commandes de test test-004 a test-021 sont composables via generateurs-commande).
2. Creation des 14 .md de test manquants (test-006 a test-021) au format standard : titre, testeur, date, objet extrait de la docstring, contexte, execution.
3. Corrections de versions liees au bump c0d : test-004 (morpheus 0.3.3), test-013 (cerberus 0.3.3 + 21 cases action), test-016 (buffy 0.3.7 + 36 cases action), test-006 (atlas 45 cases).

**Lecons** :
1. La REGLE ABSOLUE LECTURE DOC impose que chaque commande du catalogue pointe vers un outil avec un .md a cote - le test-005 la verifie desormais en permanence.
2. L'ajout d'une case action dans les parcours (c0d) fait monter les compteurs de types dans test-013 (20->21) et test-016 (35->36) : il faut mettre a jour les tests en meme temps que les parcours.
3. Les .md de test sont le contrat d'utilisation : tout nouveau test doit avoir son .md cree au meme moment.
## [LECON] 2026-08-11 -- TESTS 009/015 ADAPTES A VALIDER-CASE v1.0.2 (Morpheus)

**Mission** : adapter les tests de valider-case a la nouvelle version v1.0.2 (convention de nommage etendue : prefixes thematiques majuscules cT* pour la ligne trio Janus) puis reverdir la non-regression.

**Actions** :
1. test-009-valider-case : version v1.0.1 -> v1.0.2 (docstring, libelles, --version) - 20/20 OK.
2. test-015-valider-case-garde-fou : version v1.0.1 -> v1.0.2 (docstring, libelles, --version) - 9/9 OK.
3. spec-valider-case.001.01.ebauche.md : version 1.0.1 -> 1.0.2 + convention de nommage documentee (c[<prefixe-alpha-maj>]<numero>[a-z]? avec exemple cT1..cT10).
4. Non-regression complete : 33/33 OK. Normes 0/0.

**Lecons** :
1. Un bump de version d'un outil touche TOUJOURS ses tests (--version verifie) : adapter les tests dans la meme chaine (Morpheus), pas en retard.
2. La spec de l'outil mentionne la convention de nommage : elle doit suivre le bump (2 fichiers outil : .md ET spec/).
3. Aucun test de rejet cT* n'existait dans test-009/015 : le bug nommage etait invisible cote tests - penser a ajouter un point qui verifie l'ACCEPTATION d'un id cT* (garde-fou positif) lors d'une prochaine evolution.
## [LECON] 2026-08-11 -- Garde-fou positif cT* dans test-009/015 (valider-case v1.0.2)

**Contexte** : apres l'extension de la convention de nommage v1.0.2 (prefixe thematique majuscule cT* pour la ligne Trio de Janus, regex `^c[A-Z]?\d+[a-z]*$`), aucun test ne verifiait l'ACCEPTATION des ids cT* par valider-case -- seulement le rejet des ids invalides. Un futur retour en arriere de la regex (c\d+[a-z]*$) aurait passe la non-regression sans etre detecte.

**Lecon** :
1. Toute modification de convention (extension de regex, nouveau format) doit etre couverte par un GARDE-FOU POSITIF en plus des garde-fous negatifs : verifier que le nouveau format est ACCEPTE, pas seulement que l'ancien est rejete.
2. Un parcours artificiel minimal (depart c0 question 2 branches -> fin cT*, sans indices ni refs) suffit pour isoler le controle de nommage : verdict CONFORME + 0 erreur NOMMAGE + retour 0.
3. test-009 a gagne le point 11c (cT6 accepte), test-015 le point 10 (cT10 accepte) -- un id par test pour couvrir la plage sans dupliquer.
4. Les parcours artificiels temporaires doivent etre ecrits en ASCII + LF dans tmp/ (newline="\n") pour ne pas polluer les normes.
5. Non-regression complete reverdie : 21/21 tests OK (test-009 21/21, test-015 10/10).
## [LECON] 2026-08-11 -- TEST-014 ADAPTE A LA SPEC v0.6.2 + GARDE-FOU POSITIF REGLE 11 (Morpheus)

**Contexte** : Vulcain a documente la convention de nommage etendue cT* dans la spec-guider-parcours (bump v0.6.1 -> v0.6.2, regle 11 NOMMAGE DES IDS DE CASES, refs doc guider-parcours.md et vulcain.md passees a v0.6.2). Le test-014 etait KO sur 4 points (1a, 1b, 6a, 6b : versions 0.6.1/0.6.0).

**Lecon** :
1. REGLE IMMUABLE DELEGATION respectee : Vulcain a signale l'impact test sans y toucher, Cerberus a active Morpheus pour l'adaptation.
2. L'adaptation couvre 5 endroits du test-014 : docstring (contexte + cas couverts), en-tete du print, point 1a (titre ligne 7), point 1b (Version ligne 9), points 6a/6b (refs doc) -- les versions sont verifiees en dur dans le test, pas lues depuis la spec (choix du test : figer la version attendue).
3. GARDE-FOU POSITIF ajoute (point 11) : la regle 11 NOMMAGE DES IDS doit etre presente avec cT1/cT10 et la reference valider-case v1.0.2 -- un futur retrait de la convention passerait en KO (anti-recurrence, meme logique que le garde-fou positif cT* du test-009/015).
4. Resultats : test-014 13/13 OK, non-regression complete 21/21 OK, normes 0 non-ASCII / 0 CRLF.
## [LECON] 2026-08-11 -- TEST-007 ADAPTE A 139 COMMANDES + DECOUVERTE D'UN DEFAUT DE TRI DU CATALOGUE (Morpheus)

**Contexte** : ajout de l'outil detecter-convention-nommage au catalogue generateurs-commande (138 -> 139 commandes).

**Adaptation du test-007** (point 13) : 138 -> 139 (docstring, condition len(noms) == 139, messages). Point 14 (index-tools 110 + Corriger 6) deja conforme, inchange.

**Lecons** :
1. Apres adaptation du compte, le test-007 restait KO (nb=139) : la cause n'etait PAS le test mais le CATALOGUE lui-meme -- detecter-convention-nommage a ete insere en FIN de liste (position 138, apres verifier-systeme) au lieu de sa position alphabetique dans la famille detecter-*. Le test verifie noms == sorted(noms) : garde-fou legitime qui a fonctionne.
2. REGLE DELEGATION inverse : Morpheus ne touche qu'aux tests. La reparation du tri du catalogue (deplacer detecter-convention-nommage entre detecter-decalages-catalogue et les autres detecter-*) releve de VULCAIN. Signale a Cerberus pour activation.
3. Confirme la lecon RE-SCAN COMPLET : toute insertion dans le catalogue doit respecter le tri alphabetique (le test-007 le verifie) -- l'ordre d'insertion JSON n'est pas libre.
4. Normes test-007 : 0 non-ASCII, 0 CRLF, 0 mention 138 restante (4 occurrences 139).

## [LECON] 2026-08-11 -- BUDGET PONDERE DES INDICES TESTE EN REEL (valider-case v1.1.0, generateurs-case v0.4.2) (Morpheus)

**Mission** : tester la non-regression apres l'implementation du budget pondere des indices par Vulcain (decision utilisateur : 2 indices courts = 1 indice long).

**Tests independants realises (mes propres parcours temoins, pas ceux de Vulcain)** :
1. 6 courts (50 car.) = poids 3,0 -> CONFORME
2. 4 longs (120 car.) = poids 4,0 -> A ALLEGER
3. 2 longs + 2 courts = poids 3,0 -> CONFORME
4. 1 long + 4 courts = poids 3,0 -> CONFORME
5. 1 texte > 160 car. = TOUJOURS signale (plafond absolu inchange)
6. 5 courts + 1 long = poids 3,5 -> A ALLEGER (depassement mixte)
7. 6 indices sans texte (ref) = poids 3,0 -> CONFORME
=> 7/7 OK

**Autres verifications** :
- test-009 (23 points dont 3f/3g budget), test-010 (25), test-015 (10) : tous verts
- Parite py/sh : valider-case v1.1.0 identique des 2 cotes ; generateurs-case exige ses arguments (comportement normal)
- Non-regression complete : 21/21 OK
- Normes : 0 non-ASCII, 0 CRLF

**Lecons** :
1. Le modele pondere est robuste : la frontiere 3,0 fonctionne pour tous les melanges (pur courts, pur longs, mixte)
2. Les indices SANS texte (ref/outil) comptent comme courts (0,5) : 6 refs = 3,0 accepte - c'est coherent avec leur faible charge cognitive
3. Le plafond absolu 160 car. reste le veritable garde-fou de la taille d'un indice : le budget pondere ne concerne que le NOMBRE

## [LECON] 2026-08-11 -- test-022 budget pondere (Morpheus)

**Mission** : creer un test formel dedie au budget pondere des indices (frontiere exacte 3,0).
**Resultat** : test-022-budget-pondere cree (py + md), 14/14 OK.
**Lecons** :
1. La frontiere exacte du budget (3,0 OK / 3,5 KO) doit etre testee avec des cas aux limites : 3,0 exact (6 courts OU 3 longs OU 2 longs + 2 courts) passe, 3,5 (1 long + 5 courts) KO, 4,0 (4 longs) KO.
2. Une case de test minimale sans indices existants evite les fausses surcharges lors de l'ajout d'indices temoins.
3. Le plafond absolu de 160 caracteres reste independant du budget pondere : un indice > 160 est toujours signale.
4. Les refs (indices de type reference) comptent comme indices courts (0,5) : a verifier dans les cas limites.
5. Toute creation de test doit etre referencee dans le catalogue generateurs-commande (insertion triee, LF pur) et le compteur de test-007 (139 -> 140) doit etre mis a jour pour reverdir la non-regression.
6. La plage documentaire des tests (test-001 a test-021 -> test-001 a test-022) doit etre mise a jour dans test-021.md.
7. Le diff du catalogue vs HEAD peut etre large (changements non commites anterieurs) : verifier uniquement que l'insertion est minimale et triee.

## [LECON] 2026-08-11 -- TEST-014 ADAPTE A valider-case v1.1.0 (Morpheus)

**Mission** : adapter le test-014 apres la correction des versions stale dans les specs (valider-case v1.0.2 -> v1.1.0 par Promethee).
**Resultat** : test-014 reverdi 13/13, non-regression complete 22/22.
**Lecons** :
1. Quand une spec corrige une version d'outil referencee (ex: valider-case v1.0.2 -> v1.1.0), les tests formels qui verifient le TEXTE EXACT de la spec cassent : test-014 verifie litteralement "valider-case v1.0.2" in spec (garde-fou positif regle 11). Le test doit suivre la version.
2. La chaine correcte : Promethee (specs) -> Morpheus (tests) -> Janus (controle croise). Chaque maillon verifie sa partie AVANT d'activer le suivant.
3. Le test-014 verifie aussi la version dans son en-tete documentaire (ligne 18 : "v1.0.2) ; refs doc passees a v0.6.2") : les 2 occurrences (en-tete + garde-fou) doivent etre mises a jour ensemble.
4. La non-regression complete (22 tests) confirme qu'aucune autre spec corrigee (combos-moteur, detecter-decalages, generateurs-case, generateurs-ligne, detecter-convention-nommage, spec-refonte) ne casse de test.

## [LECON] 2026-08-11 -- TEST-023 GREP CROISE BUDGET PONDERE CREE (Morpheus)

Creation du test-023-grep-budget-pondere : garde-fou non-regression
automatique materialisant l etape E7 du protocole-verification-coherence
v0.2.0 (grep croise des seuils budget pondere sur les 6 fichiers).

Perimetre (26 points) :
- P1-P16 : les 4 valeurs textuelles ('100 car' / '0,5' / '3,0' / '160')
  presentes dans CHACUN des 4 fichiers textes (spec-refonte,
  spec-valider-case, spec-guider-parcours, valider-case.md)
- P17-P19 : valider-case.py contient SEUIL_COURT = 100, BUDGET_INDICES = 3.0,
  SEUIL_TEXTE = 160
- P20-P22 : generateurs-case.py contient SEUIL_COURT = 100,
  BUDGET_INDICES = 3.0, SEUIL_REGLE_DEFAUT = 160
- P23-P24 : anti-recurrence : '> 3 indices' / 'plus de 3 indices' ABSENTS
  des 6 fichiers
- P25-P26 : normes du test (ASCII strict, LF pur)

Autres travaux :
- test-023 reference au catalogue generateurs-commande (140 -> 141 commandes,
  trie, LF pur, 0 non-ASCII)
- test-007-figer-lf mis a jour (point 13 : 140 -> 141 + entree test-023) :
  15/15 VALIDE
- Non-regression complete : 23/23 OK

Lecons :
1. Le grep croise E7 est desormais un test AUTOMATIQUE de la suite : toute
   divergence de seuil ou retour de l ancienne regle fera KO au test-023.
2. Toute commande ajoutee au catalogue impacte test-007 (compteur) : mettre a
   jour le point 13 dans la MEME mission que l ajout au catalogue.

## [LECON] 2026-08-11 -- TEST-005 ADAPTE A GENERATEURS-COMMANDE v0.2.3 (Morpheus)

Adaptation du test-005-generateurs-commande apres le bump du generateur en
v0.2.3 (journalisation d usage ajoutee par Vulcain) : 10 occurrences v0.2.2
-> v0.2.3 (docstring, bloc GENERATEUR, points --version py/sh, ligne RESULTAT).

Lecons :
1. KO DE PARITE PY/SH DECOUVERT : le .sh de generateurs-commande est une
   implementation bash PARALLELE (pas un simple wrapper) avec VERSION codee
   en dur : Vulcain avait bump le .py sans le .sh -> --version .sh restait
   v0.2.2. Corrige (2 occurrences) -> parite v0.2.3 py/sh. A retenir : tout
   bump de version d un outil avec .sh parallele doit toucher LES DEUX.
2. La modification preexistante du docstring test-005 (REGLE ABSOLUE LECTURE
   DOC, Buffy 2026-08-09) a ete conservee intacte.
3. test-005 reverdi : 28/28 OK. Non-regression complete : 23/23 OK.
4. Le registre d usage (enregistrer-usage-outil v0.1.0 + registre JSONL)
   est operationnel : la journalisation auto du generateur fonctionne
   (mode generateur) et l outil dedie couvre les usages directs/combos.
## [LECON] 2026-08-11 -- --no-journal AJOUTE AUX 4 TESTS QUI PASSENT PAR LE GENERATEUR (Morpheus)

**Contexte** : le registre d usage des outils (source de verite) etait pollue par la
non-regression (88 lignes de test). generateurs-commande v0.2.3 + combos-moteur v0.3.1
supportent --no-journal. Restait a l ajouter aux tests.

**Tests modifies** :
1. test-005-generateurs-commande : composer() -> --no-journal sur l appel PY uniquement
   (le .sh du generateur ne journalise pas et ne supporte pas l option).
2. test-002-combos-moteur : run_py() centralise + 2 appels sh (--liste / --reponses).
3. test-003-combos-creer : run_py() centralise + 2 appels sh (--liste / --dry-run args_sh).
4. test-004-combos-tester-outil : 5 appels executer([PYTHON, MOTEUR_PY, ...]).

**Methodes** : injection dans les fonctions centrales (run_py) quand elles existent,
sinon sur chaque appel. Verif par test individuel (pollution 0) puis non-regression complete.

**Resultats reels** : pollution test-003 = 0, test-004 = 0, non-regression 23/23 OK,
registre a 0 ligne apres la non-regression (source de verite propre).

**Lecon** : apres ajout d une option d outil, SCANNER tous les tests qui passent par
l outil (direct ou via combos) et verifier la pollution par test un a un
(identifier test par test) - la non-regression globale seule ne dit pas QUI pollue.
## [LECON] 2026-08-11 -- 6 TESTS ADAPTES APRES BUMP DES 11 PARCOURS (Morpheus)

**Contexte** : Buffy a branche le registre d usage dans les 11 cartes (nouvelle case dediee
"Enregistrer mes usages d outils" avant chaque fin) + bump des versions (0.3.x/0.4.x -> 0.4.0/0.5.0,
trio -> 0.3.0). Les tests qui verifiaient les versions ou les compteurs de cases sont devenus KO.

**Tests adaptes** (6) :
1. test-004 : morpheus v0.3.3 -> v0.4.0 (3 occ. texte + 1 condition).
2. test-005 : atlas v0.3.4 -> v0.4.0 (4 occ. texte + 3 occ. description + 1 condition).
3. test-013 : cerberus v0.3.3 -> v0.4.0 + compteur action 21 -> 22 (+ c24 registre usage).
4. test-016 : buffy v0.3.7 -> v0.4.0 + compteur action 36 -> 37 (+ c42 registre usage).
5. test-006 : parcours-atlas 45 -> 46 cases (la nouvelle case c34) - nb chemins inchange (39).
6. test-021 : c9f.suivant c10 -> c24 (nouvelle case registre) puis c10 - la verification
   structurelle doit suivre le nouveau chemin c9f -> c24 -> c10.

**Resultats** : non-regression complete 23/23 OK, registre d usage a 0 ligne apres
(source de verite propre, --no-journal deja en place).

**Lecons** :
1. Apres bump de versions de parcours, SCANNER tous les tests qui referencent ces versions
   (grep 0.X.Y) ET les compteurs (nb cases, nb chemins, types) - la non-regression seule
   revele les KO mais il faut anticiper les compteurs dans les tests formels.
2. La navigation peut rester identique (la fin est toujours atteinte) mais la verification
   STRUCTURELLE (c9f.suivant) doit suivre le nouveau chemin (insertion d une case intermediaire).
3. Le nb de CHEMINS (depart -> fins) ne change pas quand la nouvelle case mene a une fin
   existante : seul le nb de CASES augmente.

## [LECON] 2026-08-11 -- TEST-013 ADAPTE APRES BUMP CERBERUS 0.4.1 (Morpheus)

**Contexte** : mission anti-regression historique (19 fins PASSE PAR LE GENERATEUR + maillon manquant Cerberus c15b/c15c) -> bump cerberus 0.4.0 -> 0.4.1.

**Actions** : test-013 adapte (9 remplacements) : version 0.4.0 -> 0.4.1, compteur cases action 22 -> 23 (c15c ajoutee), controles 4 -> 5 (c15b ajoutee), descriptions mises a jour. 22/22 OK. Non-regression complete 23/23 OK, registre 0 ligne.

**LE CONS** :
1. Quand une nouvelle case controle/action est ajoutee a un parcours, verifier le test de migration du parcours concerne (test-013 pour cerberus) : il verifie les compteurs de types (action/question/controle/fin) qui changent a chaque ajout.
2. Les 3 chemins de navigation du test-013 ne passent pas par c15b -> ils restent verts ; seul le comptage de types est sensible.
3. Ecrire le script de non-regression avec un comptage robuste des [KO] (regex) : un parsing fragile de la ligne RESULTAT produit des faux KO.

## [LECON] 2026-08-11 -- TEST-007 ADAPTE + GARDE-FOU TEST-024 ANTI-SCRIPTS-TEMPORAIRES (Morpheus)

**Contexte** : mission anti-scripts-temporaires (Vulcain a cree lancer-non-regression, editer-parcours, detecter-usage-scripts-temporaires + registre v0.2.0 mode script-temporaire + catalogue 142->145 + index 108->111).

**Actions** :
1. test-007 adapte : catalogue 142 -> 145, index-tools 110 -> 111 (6 remplacements). 15/15 VALIDE.
2. test-024-scripts-temporaires cree : garde-fou anti-recurrence qui verifie (12 points) : aucun .zz-*/.tmp-* a la racine, les 3 outils + registre v0.2.0 operationnels, catalogue 145, index 4 lignes (incluant editer-fichier-agents qui manquait), ASCII/LF. 12/12 OK.
3. Non-regression complete lancee avec le NOUVEL OUTIL lancer-non-regression (au lieu d'un script maison) : 24/24 OK, registre 0 ligne.

**LE CONS** :
1. La premiere utilisation d'un nouvel outil doit se faire dans la mission qui le cree (ex : lancer-non-regression pour la non-regression) - c'est la preuve reelle de son fonctionnement.
2. Tout ajout de commande au catalogue casse test-007 (compteur) : l'adapter dans la meme chaine.
3. Le garde-fou test-024 verifie l'absence de scripts temporaires a la racine : c'est le filet qui empechera la regression (un agent qui laisse un .zz-*.py cassera la non-regression).

## [LECON] 2026-08-11 -- 3 TESTS DE VERSION ADAPTES + REGLE DECLARATION RACCOURCIE (Morpheus, 2e passage)

**Contexte** : 2e passage de la chaine anti-scripts-temporaires. Buffy a renforce les cartes (10 fins outil-temporaire + editer-parcours branche + bumps versions) ce qui a casse test-004/005/016.

**Actions** :
1. test-004 (morpheus 0.4.0 -> 0.4.1, 4 occurrences), test-005 (atlas 0.4.0 -> 0.4.1, 8 occurrences), test-016 (buffy 0.4.0 -> 0.4.1, 4 occurrences) : 16/16, 28/28, 20/20 OK.
2. **BUG DECOUVERT** : la regle DECLARATION ajoutee par Buffy dans les 10 fins outil-temporaire faisait 200 caracteres (> 160) -> valider-case A ALLEGER + test-016 3 KO. Racourcie a 93 caracteres dans les 10 parcours : "REGLE ANTI-SCRIPTS : DECLARER au registre (enregistrer-usage-outil --mode script-temporaire)." -> buffy CONFORME, test-016 20/20.
3. Non-regression complete : 24/24 OK avec l OUTIL lancer-non-regression, registre 0 ligne.

**LE CONS** :
1. TOUTE regle ajoutee dans une case doit rester <= 160 caracteres (valider-case A ALLEGER au-dessus) - verifier la longueur a l ajout, pas seulement a la validation.
2. Le diagnostic test par test (3b/3c/9 du test-016) a revele le probleme de surcharge : toujours lancer le test de migration du parcours concerne apres une modif de carte.
3. L'outil lancer-non-regression est stable : 24/24 en 2e utilisation, registre toujours 0.

## [LECON] 2026-08-12 -- TEST-001 v0.1.2 ADAPTE + GARDE-FOU TEST-025 NETTOYER-SESSIONS (Morpheus)

**Contexte** : chaine Vulcain -> Morpheus -> Janus. Vulcain a corrige nettoyer-sessions v0.1.2 (bug : l en-tete ## Sessions LLM etait supprime a tort, ce qui cassait sidentifier apres un nettoyage).

**Actions** :
1. test-001-nettoyer-sessions.sh v0.1.0 -> v0.1.2 : version attendue 0.1.1 -> 0.1.2, ASSERTION 4b INVERSEE (l en-tete ## Sessions LLM doit etre PRESERVE = 1, plus supprime = 0), + 3 tests d INTEGRATION 7c/7d/7e (apres le nettoyage reel, sidentifier sur la copie AGENTS_FILE/AGENTS_HISTORIQUE/CLASSEUR_STOCKAGE doit recreer le bloc session). Resultat : 35/35 VALIDE.
2. test-025-nettoyer-sessions-garde-fou cree (py + md, 11 points) : garde-fou anti-recurrence de la boucle COMPLETE sur copies (nettoyage -> en-tete conserve -> sidentifier recreer le bloc) + parite py/sh + normes. Resultat : 11/11 OK.
3. Non-regression complete : 25/25 OK avec l OUTIL lancer-non-regression, registre 0 ligne.

**Lecons** :
1. Les tests figent l ANCIEN comportement : le test-001 verifiait '## Sessions LLM supprimee = 0' (le bug). Quand le comportement documente change, le test doit etre INVERSE en meme temps que l outil, sinon il protege l erreur.
2. TEST D INTEGRATION = la boucle complete : le bug sidentifier n etait visible qu en enchainant nettoyage PUIS sidentifier sur copies. Les tests 7c/7d/7e + le garde-fou test-025 verrouillent cette boucle.
3. PIEGE SYNTAXE BASH : une ligne de continuation de verifier a perdu son guillemet fermant lors de l insertion -> 'syntax error near unexpected token'. Relire la zone inseree (bash -n) AVANT d executer.
4. Le test-024 (garde-fou precedent) n est PAS au catalogue : meme convention pour test-025 (pas d entree catalogue) -> test-007 (145) et test-024 point 8 restent verts sans adaptation.
5. Le glob de lancer-non-regression inclut automatiquement le nouveau test-025 : la non-regression passe de 24 a 25 tests sans modifier l outil.

## [LECON] 2026-08-12 -- TEST-001 DETECTER-CABLAGES-MANQUANTS + GARDE-FOU TEST-026 (Morpheus)

**Contexte** : chaine Vulcain -> Morpheus -> Janus (reprise de mission par decision utilisateur). Vulcain a finalise detecter-cablages-manquants v0.1.1 (cases orphelines, boucles bloquantes, references mortes) + corrige les orphelines clio (c6/c6a/c7/c8 vestiges retires, parcours-clio 0.5.2 -> 0.5.3).

**Actions** :
1. test-001-detecter-cablages-manquants.sh cree (8 points) : version v0.1.1, parcours sain (cerberus) PROPRE sans CAS_ORPHELINE/REF_MORTE/BOUCLE_BLOQUANTE, bug simule (1 orpheline + 1 boucle indirecte z1->z2 SANS sortie dans le graphe atteignable + 1 ref morte) = detection 100%, --tous PROPRE sur 11 parcours, --rapport ecrit. Resultat : 8/8 VALIDE.
2. test-026-detecter-cablages-manquants-garde-fou cree (py + md, 10 points) : garde-fou anti-recurrence du bug des questions orphelines -- les 11 parcours doivent avoir 0 CAS_ORPHELINE, 0 BOUCLE_BLOQUANTE, 0 REF_MORTE, 0 CASE_DEPART, 0 FIN_NON_JOIGNABLE + --tous PROPRE + normes. Resultat : 10/10 OK.
3. test-007 adapte (catalogue 145 -> 146 + index-tools Total 111 -> 115, entree detecter-cablages-manquants) + test-024 point 8 adapte (145 -> 146 + nouvelle entree).
4. Non-regression complete : 26/26 OK avec l OUTIL lancer-non-regression, registre 0 ligne.

**Lecons** :
1. UN GARDE-FOU NE DOIT PAS CASSER QUAND LE PARCOURS S AMELIORE : le test-001 utilise une copie du vrai parcours cerberus (source de verite) -> il reste vert tant que le cablage est sain, et detecte toute regression.
2. LA BOUCLE INDIRECTE DOIT ETRE INJECTEE DANS LE GRAPHE ATTEIGNABLE : une boucle z1->z2 hors graphe est classee CAS_ORPHELINE, pas BOUCLE_BLOQUANTE -- brancher la boucle depuis une case atteignable (c15c.suivant=z1) pour tester la detection de cycle.
3. TOUT AJOUT DE COMMANDE AU CATALOGUE CASSE 2 TESTS (test-007 point 13/14 ET test-024 point 8) : les adapter dans la meme chaine, pas au coup par coup.
4. Le glob de lancer-non-regression inclut automatiquement le nouveau test-026 : la non-regression passe de 25 a 26 tests sans modifier l outil.

## [LECON] 2026-08-12 -- NON-REGRESSION 26/26 APRES CORRECTION CATALOGUE (generateurs-ligne) : AUCUNE ADAPTATION NECESSAIRE (Morpheus)

**Contexte** : chaine Cerberus -> Vulcain -> Morpheus (-> Janus). Vulcain a corrige le doublon de parametres de l entree generateurs-ligne du catalogue (cles dupliquees branche/mode/source) qui bloquait regenerer-catalogue, + README (badge Shields Outils-121 -> 126 + categorie enregistrer ajoutee).

**Actions** : non-regression complete 26/26 OK (aucun test casse : test-005 generateurs-commande, test-007 13/14, test-017 generateurs-ligne, test-024 point 8 tous verts - le catalogue reste a 146 commandes triees, le doublon n affectait pas les compteurs), regenerer-catalogue --dry-run = 0 cle dupliquee (OK), garde-fous test-025 11/11 et test-026 10/10 verts, normes ASCII 0 sur catalogue/README.

**Lecons** :
1. UN DOUBLON DE PARAMETRES DANS LE CATALOGUE NE CASSE PAS LES TESTS DE COMPTAGE : test-007/024 verifient le NOMBRE de commandes et le tri, pas l integrite interne des parametres - seul regenerer-catalogue (garde-fou) le detectait. Le garde-fou est indispensable : sans lui, la corruption serait passee inapercue.
2. QUAND AUCUN TEST NE CASSE, NE RIEN ADAPTER : la tentation d une adaptation prophylactique est une regression silencieuse - verifier d abord que le KO existe reellement (ici 0 KO, donc 0 adaptation).
3. Les garde-fous specifiques (test-025, test-026) sont relances individuellement en plus de la non-regression : ils verrouillent des comportements que les tests de comptage ne couvrent pas.
## [LECON] 2026-08-12 -- APRES AMELIORATION 5 OUTILS D EDITION (Morpheus)

**Contexte** : Vulcain a ameliore la qualite pro des outils d edition texte (editer-fichier, inserer-contenu-fichier, ajouter-contenu-fichier, remplacer-texte, supprimer-ligne) : echec explicite (code 1 quand rien n est fait), --apres <motif> + --indent, --backup. Parcours cerberus bumped v0.4.3 (garde-fou c1) + themes-amelioration.json agent_habilite vulcain.

**Actions** : non-regression complete 26/26 OK (test-013 adapte 0.4.2->0.4.3 vert, les 5 outils ne cassent aucun test de comptage), regenerer-catalogue --dry-run = 0 cle dupliquee + 0 a ajouter, normes ASCII/LF 0/0 sur les 21 fichiers modifies.

**Lecons** :
1. AMELIORER UN OUTIL SANS CHANGER SON INTERFACE NE CASSE RIEN : les 5 bumps de version n ont affecte aucun test (parcours, combos, catalogue utilisent les memes commandes). La retrocompatibilite argparse est la regle d or.
2. LA NON-REGRESSION PROUVE LA SECURITE DES BUMPS : 26/26 verts apres 5 bumps = les interfaces sont stables. Un KO aurait signale une interface cassee.
3. Les garde-fous (test-025, test-026) restent verts : les modifications n ont pas touche aux mecanismes de protection.
## [LECON] 2026-08-12 -- APRES EXTENSION QUALITE PRO 5 OUTILS FICHIERS (Morpheus)

**Contexte** : Vulcain a homogeneise la qualite pro des 5 outils fichiers de base (creer/supprimer/deplacer/lire/ecrire-fichier) tous en 0.3.0 : echec explicite (fichier inexistant/destination existante -> code 1), protection nommage, --backup, promotion prepare.

**Actions** : non-regression complete 26/26 OK (aucun test casse - les 5 bumps ne changent aucun compteur), regenerer-catalogue --dry-run = 0 cle dupliquee + 0 a ajouter, normes ASCII/LF 0/0.

**Lecons** :
1. DEUXIEME VAGUE D OUTILS AMELIORES, ZERO TEST CASSE : la regle retrocompat (interfaces conservees) tient - la qualite pro est desormais un standard applique a 10 outils (5 edition + 5 fichiers).
2. LA NON-REGRESSION EST LE THERMOMETRE DE LA STABILITE : 26/26 verts apres 10 bumps cumules = les interfaces sont eprouvees. Le systeme absorbe les ameliorations sans regression.
3. Un KO serait un signal d interface cassee ; 0 KO = les garde-fous (test-025/026) et les compteurs sont intacts.
## [LECON] 2026-08-12 -- APRES ROUND 2 PERFORMANCE (Morpheus)

**Contexte** : Vulcain a corrige 3 goulots de performance mesures (remplacer-texte.sh 8.5s->0.55s par delegation a un seul process python3, lire-fichier lecture paresseuse, editer-fichier une seule passe).

**Actions** : non-regression complete 26/26 OK (aucun test casse - les versions 0.3.0/0.4.0 ne sont verifiees par aucun test, les interfaces argparse sont inchangees), regenerer-catalogue --dry-run = 0 cle dupliquee + 0 a ajouter, normes ASCII/LF 0/0.

**Lecons** :
1. LES OPTIMISATIONS DE PERFORMANCE NE CASSENT RIEN QUAND L INTERFACE NE CHANGE PAS : 3 outils modifies en profondeur (boucle, lecture, scan) et 26/26 tests verts - la non-regression prouve que le comportement externe est identique.
2. LA MESURE AVANT/APRES EST LA SEULE PREUVE : 8.5s -> 0.55s (15x) est un chiffre, pas une opinion. Le theme performance doit toujours fournir des mesures.
3. Un benchmark temporaire propre (fichiers crees puis supprimes) est le bon outil pour prouver un gain - aucun residu, aucune modification des vrais fichiers.

## [LECON] 2026-08-12 -- APRES ROUND 3 SECURITE (Morpheus)

**Contexte** : Vulcain a renforce la securite de 9 outils fichiers/edition (encodages robustes, refus octet nul, refus symlink, backup binaire) avec bumps 0.3.1/0.4.1.

**Actions** : non-regression complete 26/26 OK (les bumps 0.3.1/0.4.1 ne sont verifies par aucun test), regenerer-catalogue --dry-run = 0 a ajouter + 0 doublon, normes ASCII/LF 0/0 sur les 9 .py.

**Lecons** :
1. TROISIEME VAGUE D OUTILS AMELIORES, ZERO TEST CASSE : la regle retrocompat tient encore - 15 outils a qualite pro (10 qualite + 3 performance + 9 securite, certains cumules) sans aucun changement d interface.
2. LA SECURITE SERT AUSSI LA NON-REGRESSION : des outils qui ne crashent plus sur des fichiers exotiques (BOM, latin-1) protegent les tests futurs eux-memes.

## [LECON] 2026-08-12 -- APRES ROUND 4 ROBUSTESSE (Morpheus)

**Contexte** : Vulcain a corrige 3 echecs silencieux (ecrire-fichier v0.3.2 troncature contenu vide, lire-fichier v0.4.2 validation plage, supprimer-ligne v0.3.2 pluriel).

**Actions** : non-regression complete 26/26 OK (aucun test ne verifiait --lignes 0 ni le comportement contenu vide - les changements de comportement sont compatibles), regenerer-catalogue --dry-run = 0 a ajouter + 0 doublon, normes ASCII/LF 0/0 sur 10 fichiers.

**Lecons** :
1. QUATRIEME VAGUE, ZERO TEST CASSE : la regle retrocompat tient - les 3 corrections changent des comportements SILENCIEUX vers des comportements EXPLICITES, et aucun test ne dependait du comportement silencieux.
2. LE PASSAGE SILENCIEUX -> EXPLICITE EST TOUJOURS SANS RISQUE POUR LES TESTS : transformer un no-op muet en erreur ou message documente ne peut pas casser un test qui verifie le comportement utile.
3. LE GARDE-FOU TEST-024 N A RIEN DETECTE CETTE FOIS : Vulcain a range ses scripts de test dans .robustesse/ (pas a la racine) - le protocole creation-scripts-temporaires est applique.
## [LECON] 2026-08-12 -- APRES ROUND 6 GENERATEURS (Morpheus)

**Contexte** : Vulcain a corrige 3 faiblesses sur les generateurs : generateurs-commande v0.2.4 (flag du MODELE sans champ flag declare laisse orphelin quand valeur vide - 95 entrees du catalogue concernees), generateurs-regenerer-catalogue v1.1.1 (catalogue introuvable/JSON invalide -> message ERREUR propre + rc 1, plus de traceback), generateurs-amelioration v2.1.0 (--version/--liste affichent la version des themes v2.2.0).

**Actions** : non-regression complete : 24 OK / 2 KO attendus au premier passage (test-005 version generateurs-commande v0.2.3 en dur, test-008 version generateurs-amelioration v2.0.0 en dur + sortie --version). Adaptation : test-005 v0.2.3 -> v0.2.4 (docstring + 2 asserts + en-tete), test-008 v2.0.0 -> v2.1.0 + assert 'themes v2.2.0' dans --version. Apres adaptation : 26/26 OK. regenerer-catalogue --dry-run : 0 a ajouter + garde-fou 0 cle dupliquee. Normes ASCII/LF 0/0 sur 11 fichiers.

**Lecons** :
1. IMPACT PREVU vs IMPACT IMPREVU : la mission annoncait l impact exact (test-005 KO sur la version en dur) - le premier passage 24/2 a confirme la prediction, aucun KO surprise. Quand l impact est predit, l adapter fait partie de la mission, pas une surprise.
2. LES TESTS DE VERSION EN DUR SONT FRAGILES PAR NATURE : test-005 et test-008 verifient des versions en dur - chaque bump de version d un outil les casse. C est un signal, pas un bug : la version du test DOIT suivre la version de l outil.
3. LA PARITE PY/SH RESTE GARANTIE PAR LE WRAPPER : test-008 verifie py/sh identiques sur --version/--liste - le wrapper pur exec python3 a transmis la nouvelle sortie themes sans divergence.
4. LE CATALOGUE N A PAS BOUGE : 146 entrees intactes apres le round (0 ajout, 0 modification) - la correction du flag orphelin se fait dans le generateur, pas dans les donnees.

## [LECON] 2026-08-12 -- APRES ROUND 5 COMBOS (Morpheus)

**Contexte** : Vulcain a corrige le combos-moteur v0.3.2 (py + sh, parite) : arret immediat si une case outil echoue (exit != 0), champ optionnel echec_ok:true pour les cases dont le code non-nul est un resultat legitime, + echec_ok ajoute aux 30 cases outil de controle des 10 combos declaratifs.

**Actions** : non-regression complete 26/26 OK (test-002 navigation + test-020 dry-run restent verts - l arret sur echec ne les affecte pas), regenerer-catalogue --dry-run = 0 a ajouter + 0 doublon, normes ASCII/LF 0/0 sur 16 fichiers.

**Lecons** :
1. CINQUIEME VAGUE, ZERO TEST CASSE : la regle retrocompat tient - l arret sur echec est un changement de comportement par defaut, mais les tests ne lancent que des combos qui reussissent (ou des dry-run).
2. LE MOTEUR DE COMBOS EST MAINTENANT FIABLE : un combo qui echoue une etape ne se termine plus en faux succes (rc=0) - le resultat est remonte a l agent qui l a lance.


## [LECON] 2026-08-12 -- ROUND 7 VALIDER : NON-REGRESSION (Morpheus)

**Contexte** : non-regression complete apres les corrections Vulcain du round 7
valider (refs mortes valider-case v1.1.1, versions alignees, valider-nommage
v0.3.3 categorie + formats speciaux, renommage lancer-non-regression ->
tester-lancer-non-regression).

**KO constates (3, tous des impacts attends annonces par Vulcain)** :
1. test-007 : catalogue 146 mais NON TRIE (le renommage en place de
   lancer-non-regression -> tester-lancer-non-regression avait deplace la ligne
   hors de l ordre alphabetique : tester- vient apres valider-). Correction :
   re-tri du catalogue par nom (146, trie, normes 0/0).
2. test-009 : verifiait valider-case v1.1.0 en dur (4 endroits docstring +
   assert) -> bump 1.1.1 attendu, adapte.
3. test-015 : idem (v1.1.0 dans docstring + assert) -> adapte 1.1.1.

**Lecons** :
1. UN RENOMMAGE DANS UN FICHIER TRIE (catalogue JSON, index, listes) CREE UN
   DESORDRE SILENCIEUX : remplacer le nom sans re-trier laisse le fichier
   invalide aux yeux des tests de tri, sans erreur visible a l oeil. Apres tout
   renommage, verifier tri + compteurs + presence.
2. LES TESTS QUI VERIFIENT UNE VERSION EN DUR SONT DES SISMOMETRES : ils ont
   detecte instantanement le bump 1.1.1. Les adapter est l impact ATTENDU,
   jamais une surprise - mais verifier qu il n y a PAS d autres occurences de
   l ancienne version dans le test (grep complet avant de relancer).
3. test-024 (garde-fou anti-scripts-temporaires) verifie deja le NOUVEAU chemin
   de l outil renomme (adapte par Vulcain) : 12/12. La mise a jour des garde-fous
   doit accompagner le renommage, sinon la non-regression casse a la chaine.

**Validations** : non-regression 26/26, catalogue 146 trie + dry-run 0 a
ajouter + garde-fou 0 cle dupliquee, valider-nommage --recursive tools/
335/335 (0 erreur), test-007 15/15, test-009 23/23, test-015 10/10, normes 0/0
sur 18 fichiers.


## [LECON] 2026-08-12 -- ROUND 8 REGISTRE/TRACES : NON-REGRESSION (Morpheus)

**Contexte** : non-regression complete apres les corrections Vulcain du round 8
(archivage du registre au lieu de purge, filtre detecteur, garde-fous
enregistrer, versions alignees).

**Verifications** :
1. NON-REGRESSION : 26/26 OK (aucun KO - test-024 avait deja ete adapte par
   Vulcain : versions v0.1.1/v0.2.1 + nouveau point 13 garde-fou memoire).
2. IDEMPOTENCE DE L ARCHIVAGE : lancements successifs de la non-regression ->
   l historique passe de 7 a 10 lignes (3 usages Vulcain archives) puis reste
   stable a 10 (pas de doublon). Le dedoublonnage par ligne exacte fonctionne.
3. DETECTEUR : plus de .tmp-eol-test/.tmp-gc-test/.tmp-morpheus-test (faux
   positifs elimines par le filtre .py/.sh). Les 8 scripts restants non
   declares sont de VRAIS scripts historiques (ecart honnete, ils n ont
   jamais ete declares au registre).
4. CATALOGUE : dry-run 0 a ajouter, 0 cle dupliquee.
5. NORMES : 0/0 sur 10 fichiers.

**Lecons** :

1. L IDEMPOTENCE SE TESTE PAR LA REPETITION : une fonction d archivage qui
   dedoublonne doit etre verifiee sur DEUX lancements consecutifs (7 -> 10 ->
   10), pas sur un seul. Le premier lancement ajoute, le second ne doit rien
   ajouter.

2. UN GARDE-FOU DE LA MEMOIRE SE VERIFIE PAR LA PRESENCE DE L HISTORIQUE :
   le point 13 de test-024 (l historique du registre existe) protege contre
   le retour de la purge pure : si quelqu un retablit fh.write('') sans
   archiver, le test KO. La non-regression ne teste pas seulement le code,
   elle teste la POLITIQUE de retention des donnees.

3. UNE NON-REGRESSION QUI PASSE 26/26 SANS AUCUN KO APRES UNE MISSION QUI
   CHANGE LA POLITIQUE DE DONNEES (purge -> archivage) EST UN BON SIGNE :
   les tests avaient ete mis a jour par Vulcain AVANT (test-024 13/13
   verifie en amont), donc pas de surprise au lancement. La chaine
   correction -> adaptation des tests -> non-regression fonctionne.

**Validations** : non-regression 26/26, test-024 13/13, catalogue dry-run 0 a
ajouter, detecteur sans faux positifs de dossiers, historique idempotent
(7 -> 10 -> 10), normes 0/0 sur 10 fichiers.

## [LECON] 2026-08-12 -- VALIDATION FIX SIDENTIFIER v0.5.1 (Morpheus)

**Contexte** : Vulcain a corrige le bug de demarrage (sidentifier ecrasait le profil classeur avec Cerberus en dur). Mission : reverdir la non-regression + verifier que l identite de la session est coherente.

**Lecons** :

1. LA PREUVE D UN FIX DE DEMARRAGE, C EST LE DEMARRAGE LUI-MEME : le test decisif n est pas le code mais sidentifier llm-1 qui doit afficher l agent reel du bloc (morpheus apres activation, pas Cerberus). Verification faite en conditions reelles : 'agent principal : morpheus' + classeur coherent.

2. UN PARCOURS PROPRE N IMPLIQUE PAS UN DEMARRAGE PROPRE : detecter-cablages-manquants donnait 30/30 atteignables et la navigation fonctionnait, pourtant l agent s arretait. Le cycle d identification (sidentifier -> classeur) est une 3e source de verite a part entiere, hors du parcours.

3. LA NON-REGRESSION NE COUVRE PAS LA COHERENCE CROISEE DES SOURCES : aucun test ne comparait AGENTS.md vs classeur sur l agent actif. Un garde-fou possible : un test qui verifie que sidentifier rend l agent du bloc.

**Validations** : non-regression 26/26, catalogue dry-run 0 a ajouter, parcours morpheus PROPRE (30/30), sidentifier -> morpheus, classeur coherent, normes 0/0 sur 7 fichiers.

## [LECON] 2026-08-12 -- AUDIT MORPHEUS : LE TEMPLATE EST LA REFERENCE (Morpheus)

**Mission** : audit de mes pratiques de creation de tests (demande utilisateur). Constat : je ne suivais pas le template-test.md (obsolete v0.1.0 bash/protections) mais les tests precedents - derive prouvee : test-001/002 en coding utf-8 + marqueur [ECHEC] invisible pour le lanceur qui compte les [KO].

**Resultat** : template-test.md v0.2.0 (format Python canonique), migration de test-001/002/003 (utf-8 + [ECHEC] -> ascii + [OK]/[KO] + NB_POINTS/verifier/main/RESULTAT), fiche + carte morpheus v0.4.2 (case c3 : indice obligatoire LIRE template-test.md), garde-fou test-029 (14 points : invariants vitaux de CHAQUE test-0XX) affecte a la serie D, test-004 adapte (morpheus 0.4.2), non-regression 29/29, normes 0/0.

**Lecons** :
1. LE TEMPLATE EST LA REFERENCE, PAS LES TESTS PRECEDENTS : un test ancien peut porter des derives (utf-8, [ECHEC], bash). Copier un test precedent = reproduire ses derives. Chaque nouveau test part du template.
2. UN MARQUEUR INVISIBLE EST PIRE QU AUCUN : [ECHEC] n etait pas compte par le lanceur de non-regression (regex [KO]) - un echec pouvait passer inapercu si le returncode etait mal gere. Les marqueurs [OK]/[KO] sont le contrat avec le lanceur.
3. UN GARDE-FOU NE DOIT PAS S AUTO-INCRIMINER : test-029 verifie l absence de [ECHEC] - son propre code en mentionnait le motif (concatenation + retrait docstring/commentaires requis).
4. UN NOUVEAU TEST DOIT ETRE AFFECTE A UNE SERIE (lecon round 11) : test-029 affecte a la serie D.
5. UN BUMP DE PARCOURS CASCADE SUR LES TESTS : morpheus 0.4.1->0.4.2 a casse test-004 (verifiait 0.4.1) - adapte.
