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
