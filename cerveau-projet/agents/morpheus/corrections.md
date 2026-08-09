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
