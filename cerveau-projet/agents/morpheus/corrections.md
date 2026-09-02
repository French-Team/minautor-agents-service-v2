


## [LECON] 2026-09-02 -- TEST-120 CONSOMMATEUR [NOTATION] (mission f141af1d) : 8/8 OK

**Contexte** : oracle.py v0.5.9 a branche un consommateur qui convertit les
messages [NOTATION] de la routine notation en mission Themis (evaluation
croisee). Ce test verrouille : conversion, marqueurs accuse/consomme/
consomme_date, anti-inondation (mission EN_ATTENTE + delai 60 min), preuve
negative (NON-[NOTATION] -> rien), hook cmd_lire.

**Lecons** :
1. Chaque point d un test de file/inbox doit avoir SON sous-repertoire isole
   (lecon test-118 re-appliquee) : sinon la mission d un point precedent reste
   EN_ATTENTE et fausse les tests d anti-inondation des points suivants
   (premiers essais 5 OK / 3 KO, corrige en isolant p1..p6).
2. Charger oracle.py en module et rediriger INBOX_DIR + FILES_DIR +
   _FICHIER_CONSOM_NOTATION + _files.FILES_DIR vers des repertoires
   temporaires : test fiable sans jamais toucher les vrais messages/missions.
3. Le hook cmd_lire affiche le message ET declenche le consommateur : verifier
   les deux effets (mission deposee + message lu).

## [LECON] 2026-09-02 -- TEST-119 FLUX [mot] (mission 119cfe78) : 7/7 OK

**Contexte** : l utilisateur a constate que sa demande [question] avait ete
traitee sans servir le theme dedie ni faire la fin vers Oracle. Ce test
verrouille le flux complet : detection des prefixes [mot] (pilote.py
_type_mission_auto), routage vers le theme dedie (_resoudre_racine), theme-
question.json sans 'Repondre directement', et les 9 themes [mot] pointent vers
une fin reactiver cible=oracle.

**Lecons** :
1. VERIFIER L INDENT DU JSON AVANT REECRITURE : profils-tests.json utilise
   json.dump indent=1, pas indent=2. Un mauvais indent reformate tout le
   fichier (diff 454 lignes pour un ajout de 1 ligne). Toujours verifier le
   diff apres ecriture JSON.
2. Charger pilote.py en module (importlib) pour tester _type_mission_auto et
   _resoudre_racine directement - plus fiable qu une simulation CLI.
3. Preuve negative sur les fins : cloner fins.json en memoire, corrompre la
   cible (oracle -> cerberus), verifier que le garde-fou la detecte.

## [LECON] 2026-09-02 -- TEST-118 FILE DE RELAIS (mission 52ceaea1) : 8/8 OK

**Contexte** : garde-fou dedie sur la file de relais ordonnee/classifiee
(oracle v0.5.8, decision utilisateur [attention] 2026-09-02 : priorite
basse d abord puis date recente, classifier par mots-cles).

**Travail** : creation de test-118 (8 points, v0.1.0) sur FILES_DIR
TEMPORAIRE (jamais les vraies files) : classifier 8 cas, ajouter/lister,
tri importance (P1 recentes puis P2 recentes), prendre atomique,
retro-compat, relais, ASCII/LF. Enregistrement dans les DEUX registres
(serie E + profils) - test-027 point 1 vert.

**Lecons** :
1. DANS UN TEST DE FILE, ISOLER CHAQUE POINT DANS SON PROPRE
   SOUS-REPERTOIRE : les points se partageaient le meme FILES_DIR et la
   mission du point 2 restait EN_ATTENTE quand le point 3 ajoutait les
   siennes -> l ordre attendu etait fausse (une mission fantome en fin de
   classement). Sous-dossier par point (sous_tmp) = files vierges a
   chaque point.
2. RELAIS() RETOURNE (entree, erreur) COMME PRENDRE() : un tuple, pas
   une entree directe - depaqueter avant de tester les champs. Lire la
   signature de la fonction sous test AVANT d ecrire l assertion (lecon
   test-118 : 'tuple' object has no attribute 'get').
3. PIEGE DES DOSSIERS TEMPORAIRES : _file_path ne cree pas le dossier
   parent - le test doit os.makedirs sur le FILES_DIR temporaire AVANT
   le premier ajouter().

## [LECON] 2026-09-02 -- CARTE CERBERUS THEME DE-USER (mission bbdf735b) : VALIDE

**Contexte** : la carte Cerberus a ete modifiee (suppression de l etape
[2] 'Identifier l agent habilite' du theme DE-USER - il ne reste que
'Ecouter' + 'Envoyer a Oracle', c est Oracle qui identifie l agent).

**Verifications** : 1) verifier-conformite-fiche cerberus CONFORME ;
2) navigation reelle guider-arbre --reponses DE-USER : 2 besoins
seulement, plus aucune trace 'Identifier l agent' ni 'matrice' dans
theme-de-user.json ; 3) aucun test ne pinne arbre-cerberus. VALIDE.

**Lecons** :
1. VERIFIER LA NAVIGATION REELLE EN PLUS DES VALIDATIONS STATIQUES :
   guider-arbre affiche la vraie experience - un theme peut etre un JSON
   valide (guider-arbre --valider OK) mais afficher une etape oubliee a
   la navigation. Lancer --reponses DE-USER prouve le flux reel.
2. PIEGE GUEDILLEMETS : ne JAMAIS mettre de guillemets francais (ou
   accents) dans un rapport - meme une citation d un libelle (comme
   'Identifier l agent') doit etre ecrite avec des apostrophes ASCII.
   Re-valider l ASCII du rapport APRES redaction (piege recurrent).

## [LECON] 2026-09-02 -- TEST-117 ETATS PILOTE (mission 05a239b9) : 7/7 OK

**Contexte** : suite au fix etats-actions.json v0.1.2 (mission 8d3fbc34),
la colonne Etat des lignes pilote doit reflecter les phases de vol
reelles. DECISION UTILISATEUR : etats calques sur l action - DECOLLAGE,
RECUPERE, RETOUR, LARGUE, et DEBUT ne matche plus RETOUR seul mais
RETOUR ORACLE (agents reactives).

**Travail** : creation de test-117 (7 points, v0.1.0) : 1) JSON valide
v0.1.2 ; 2) les 4 etats pilote presents AVANT DEBUT dans le fichier
(l ordre = priorite) ; 3) _etat_action 8 cas reels + non-regression ;
4) encart etats connus ; 5) PREUVE NEGATIVE (retirer la regle RETOUR ->
la trace RETOUR AEROPORT retombe a tort) ; 6-7) ASCII/LF. Enregistrement
dans les DEUX registres (serie E du lanceur + profils-tests.json) -
test-027 point 1 couverture vert.

**Lecons** :
1. PREUVE NEGATIVE SUR FICHIER DATA : la priorite des regles
   (etats-actions.json) se teste en la RETIRANT - copier le fichier dans
   tmp, supprimer une regle, recharger _etat_action avec env
   ETATS_ACTIONS pointe sur la copie, verifier que la trace retombe a
   tort. C est la preuve que la regle servait a quelque chose.
2. EXIGER LE VRAI FICHIER (etats-actions.json) DANS LE TEST : pinner la
   version 0.1.2 et l ordre des cles dans le fichier - pas seulement le
   comportement de _etat_action, parce que c est le fichier data qui est
   editable sans toucher au code (la lecon de etats-action v0.8.4).

## [LECON] 2026-09-02 -- TEST-116 RETOUR AEROPORT AVANT CERBERUS (mission 787de42a) : 7/7 OK

**Contexte** : suite au fix pilote.py v0.2.3 (mission a7a14712), aucun
garde-fou ne pinnat l ORDRE chronologique exact de la fin-coordination
d Oracle : la trace pilote RETOUR AEROPORT doit etre ecrite AVANT
l activation Cerberus (retour aeroport puis atterrissage). C etait
invisible car la troncature .000 masquait l inversion.

**Travail** : creation de test-116 (7 points, v0.1.0) : 1) ordre dans le
code pilote.py (RETOUR AEROPORT ligne 581 < activer_cerberus ligne 582) ;
2) flux reel AGENTS-historique (cycle le plus recent conforme) ; 3) vrais
ms sur la trace pilote recente ; 4) preuve negative (inversion simulee
detectee) ; 5) modele conforme ; 6-7) ASCII/LF. Enregistrement dans les
DEUX registres : SERIES e du lanceur + profils-tests.json serie outils.
test-027 point 1 couverture OK.

**Lecons** :
1. UN GARDE-FOU D ORDRE CHRONOLOGIQUE DOIT VERIFIER LE CYCLE RECENT,
   PAS L HISTOIRE : AGENTS-historique conserve les anciennes traces du
   bug (avant v0.2.3 elles etaient inversees) - si le test exigeait
   l ordre sur TOUTES les entrees, il serait KO en permanence sur le
   passe. Le test prend le DERNIER retour pilote et verifie qu une
   activation le suit bien apres (et qu aucune activation ne le precede).
   Les traces historiques du bug restent comme archive.
2. UN NOUVEAU TEST DOIT ETRE ENREGISTRE DANS LES SERIES DU LANCEUR ET
   LES PROFILS : test-116 a d abord rate test-027 point 1 (hors-serie)
   car il manquait dans la constante SERIES de tester-lancer-non-
   regression.py ET dans profils-tests.json. Les deux registres sont
   requis - la couverture du garde-fou depend de l un comme de l autre.

## [LECON] 2026-09-02 -- REVERSE NON-REGRESSION 047cb88b : MISSION RESTEE PRISE SANS FIN (Morpheus)

**Contexte** : la mission 047cb88b (reverse de la non-regression - classer
les tests v1 obsolete/a-refaire/a-conserver, produire le rapport) a ete
PRISE a 11:16:57 et un premier passage a 11:35 a produit le rapport +
cree test-114, MAIS la mission n a JAMAIS ete TERMINEE : elle est restee
PRISE des heures, decalee par les missions suivantes (fe00998c, f6963ebd...),
jusqu a ce que l utilisateur la reclame. Reprise en flux formel : Oracle a
re-active Morpheus (etat de carte re-initialise) et la mission a ete
re-executee proprement.

**Travail de reprise** : 1) re-verification du classement sur la suite
reelle (113 tests, scan code a code) : obsolete = 013/016/018/072 (role
actif transfere a test-114), a-conserver = outils v1 maintenus
(006/009/010/011/012/014/015/017/022/023/096) + gouvernance corpus global
(024/046/055/057/070/071), a-refaire = fait via test-114 ; 2) mise a jour
du rapport avec la realite actuelle (test-114 v0.1.1 exception
fin-coordination oracle->cerberus, vestige 1 buffy CORRIGE f6963ebd, .bak
toujours presents = domaine Hygie signale) ; 3) verdict VALIDE.

**Lecons** :
1. UNE MISSION PRISE SANS FIN RESTE UNE MISSION NON FAITE : produire le
   livrable (rapport + test) ne TERMINE pas la mission - il faut
   mission-terminer + lecon + fin selon SA carte. Le statut PRISE sans fin
   fausse l etat de la file (l agent semble occupe, la mission n est pas
   livree au pilote).
2. A LA REPRISE, RE-VERIFIER LA REALITE : entre 11:35 et la reprise, la
   realite avait change (test-114 v0.1.1, vestige buffy corrige) - le
   rapport devait etre mis a jour, pas recopie tel quel.

**Verdict** : VALIDE - rapport mis a jour, classement verifie, mission
047cb88b TERMINEE, lecon posee, fin selon carte. ASCII 0/0, CRLF 0/0.

## [LECON] 2026-09-02 -- TEST-114 EXCEPTION FIN DE ROUND ORACLE (mission fe00998c) : 8/8 OK

**Contexte** : inter-round apres la decision utilisateur 2026-09-02 - la
fin-coordination d ORACLE (l aeroport) atterrit sur CERBERUS avec le bilan
consolide (fin de round) au lieu de se reactiver lui-meme en boucle. Vulcain
a modifie oracle/parcours/fins.json (fin-coordination -> cible=cerberus) +
les garde-fous outils (auditer-conformite-arbre F4, detecter-fins-passives,
pilote.py). Le point 3 de test-114 (reverse vestiges v1) exigeait TOUTE fin
reactiver -> cible=oracle : il cassait.

**Adaptation (v0.1.0 -> 0.1.1)** : erreurs_fins accepte l exception etroite
(oracle, fin-coordination, cible=cerberus) ; fin-signal et fin-inter-round
d oracle restent cible=oracle ; docstring point 3 documente la decision ;
point 8 (preuve negative) inchange.

**Verdict** : VALIDE - 8/8 OK x3 deterministe. Point 3 vert avec
l exception, point 8 vert (zz-vestige != oracle avec fin cerberus TOUJOURS
detecte : l exception ne desactive rien pour les autres agents). ASCII 0/0,
CRLF 0/0, 0 residu. Rapport :
rapport-test114-fin-oracle-cerberus-2026-09-02.md.

**Lecons** :
1. UNE DECISION UTILISATEUR QUI CHANGE LA CIBLE D UNE FIN CREE UNE
   EXCEPTION DOCUMENTEE DANS LE GARDE-FOU DE REVERSE, PAS UNE
   DESACTIVATION : le test-114 (jamais cerberus) et la nouvelle regle
   (seulement oracle/fin-coordination -> cerberus) coexistent si
   l exception est la PLUS ETROITE possible - triplet (agent, fid, cible)
   verifie, jamais une liste d agents a la volee.
2. LA PREUVE NEGATIVE PROUVE L ETROITESSE DE L EXCEPTION : l agent
   factice du point 8 porte un nom != oracle -> il reste detecte. Si la
   preuve negative passait, l exception serait trop large.
3. UNE MODIFICATION DE CARTE D AGENT (fins.json) A DEUX EFFETS : le
   comportement reel (pilote) ET les garde-fous structurels (test-114,
   auditer-conformite-arbre, detecter-fins-passives). Verifier les TROIS
   avant de conclure - c est le pilote (oracle) qui largue le bon
   maillon pour chaque garde-fou (outils -> vulcain, tests -> morpheus).

**Outils utilises** : lire-fichier, editer-fichier, valider-conformite-ascii,
oracle (mission-prendre/lister/terminer), tester-protections (executions
protegees).

## [LECON] 2026-09-02 -- TEST-115 R7 VERIFIER-FLUX-SECURITE (mission bdc8b291) : 9/9 OK

**Contexte** : inter-round apres le fix Vulcain 31fe865e (faux positif
R7 v0.2.2 : le scan sautait la coordination et trouvait l agent LARGUE
apres une fin). Mission : figer le comportement dans test-115.

**Verifications** :
1. 4 scenarios cles couverts : violation (fin -> agent metier direct =
   KO R7), largage normal (fin -> RECUPERE + RETOUR oracle -> largage =
   OK), fin en tete (OK), cerberus terminal vs non terminal (OK vs KO).
2. Example de scenario positif ET negatif pour chaque comportement
   (regression 0.2.1 ne peut plus revenir silencieusement).
3. Enregistrement serie E + profil 'outils' valide (test-027 point 1
   'chaque test-0XX appartient a une serie' passe).

**Verdict** : VALIDE - 9/9 OK x3 (deterministe), purge anti-residu OK.
Rapport rapport-test115-r7-verifier-flux-2026-09-02.md.

**Lecons** :
1. UN TEST DE ROUTINE QUI LIT UNE CONSTANTE MODULE A L IMPORT :
   AGENTS_ACTIVITE_RECENTE est resolue au chargement du module. Pointer
   une fixture VIA os.environ apres l import ne sert a rien (le test lit
   la vraie table et les scenarios negatifs passent A TORT). Il faut
   positionner la variable AVANT exec_module et la restaurer ensuite.
2. SCENARIO POSITIF + NEGATIF POUR CHAQUE BRANCHE : un fix de roule a
   deux effets contradictoires (accepter le largage MAIS garder la
   detection de la violation). Tester uniquement le largage OK laisserait
   une regression de la detection possible ; tester uniquement la
   violation bloquerait le fix. Les deux cotes sont obligatoires.
3. ENREGISTRER IMMEDIATEMENT LE NOUVEAU TEST : serie E du lanceur +
   profil 'outils' de profils-tests.json - sinon test-027 point 1 KO
   (test non couvert) et le test ne tourne jamais dans la serie.

**Outils utilises** : lire-fichier, creer-fichier, editer-fichier,
valider-conformite-ascii, oracle (mission-prendre/lister/terminer).


## [LECON] 2026-09-02 -- TEST-065 ADAPTATION FORMAT V2 (mission ca722bea) : 12/12 OK

**Contexte** : inter-round apres l adaptation purifier-rvav v0.1.1 -> v0.1.2
par Vulcain (decoupage v2 d AGENTS-historique : ## date + ### agent +
entrees '- hh:mm...', tri date/heure pour archiver les PLUS ANCIENNES,
sections vides supprimees). Mission : adapter test-065 -- pin de version
0.1.1 -> 0.1.2 + AJOUTER un point de non-regression format v2.

**Verifications** :
1. Pin 0.1.2 valide (l outil affiche bien 'purifier-rvav 0.1.2').
2. Nouveau point 7 format v2 (4 sous-verifications) sur fixture recent-en-haut :
   (a) les ANCIENNES (tri date/heure) sont archivees et les recentes conservees
   -- preuve que le bug v1 (archiver les blocs du haut) ne peut pas revenir ;
   (b) sections ### et ## vides supprimees, structure v2 conservee ;
   (c) non-perte 0 perdue + 0 doublon ; (d) aucun vestige '| <span'.
3. Regle anti-residu respectee : fixture et archive purgees, tmp-test065
   absent apres chaque execution (3 passages, 12/12 OK a chaque fois).
4. Aucun pin 0.1.1 purifier-rvav residuel ailleurs (les 0.1.1 restants dans
test-005/test-007 concernent d autres outils).

**Verdict** : VALIDE - 12/12 OK, les 8 invariants existants (points 1-6+
8/9 normes) restent VERTs, aucune regression induite. Rapport :
rapport-test065-format-v2-2026-09-02.md.

**Lecons** :
1. UN PIN DE VERSION PERIME SANS ERREUR CACHE UNE REGRESSION : test-065
   figurait 0.1.1 en dur; si l outil etait reste en 0.1.2 sans mise a jour
   du test, la verite se serait degradee silencieusement. Toujours aligner
   test et outil au meme round.
2. TESTER L ORDRE CHRONOLOGIQUE, PAS SEULEMENT LA NON-PERTE : le piege v1
   etait d archiver les blocs du haut (recent-en-haut = les PLUS RECENTES).
   La fixture recent-en-haut avec date recente en HAUT et ancienne en BAS
   prouve le sens du tri -- c est le point qui aurait manque sinon.
3. LES NUMEROS DE POINTS SONT LOCAUX AU TEST : verifie avant renumeration
   qu aucun autre fichier (profils-tests.json, lanceur) ne les reference --
   uniquement le NOM du test est reference.

**Outils utilises** : lire-fichier, oracle (mission-prendre/lister/terminer),
purifier-rvav (via le test sur fixture), activer-agent-principal.


## [LECON] 2026-08-24 -- TESTS OUTIL METTRE-A-JOUR-README (DEVIATION P2) : VALIDE

**Contexte** : inter-round Vulcain (delegue par Buffy, deviation P2) - Vulcain a adapte verifier()/dry_run() de mettre-a-jour-readme pour la nouvelle norme README public (1ere personne 20/08, sans section 'La boite a outils'). Bump 0.4.4 -> 0.4.5.

**Verifications** : test-064 (exclusivite mettre-a-jour-readme = clio) 7/7 OK - la carte clio n'a pas ete touchee. detecter-decalages-catalogue : 187 conformes / 0 decalages. --verifier py + sh : [OK] Badge Outils-165 + [INFO] nouvelle norme, seul l ecart SOMME readme-dev 164 vs 165 reste (P1, domaine Clio). --dry-run py + sh : [AUCUN CHANGEMENT] (le README public est deja a jour). ASCII 0/0 py/md/sh.

**Lecons** :
1. UNE MODIFICATION DOCUMENTAIRE D OUTIL (verifier tolere un nouveau format README) N IMPACTE PAS LES TESTS D EXCLUSIVITE (test-064 verifie la carte, pas le code).
2. LA COHERENCE PY/SH EST OBLIGATOIRE : toute adaptation du verifier .py doit etre repercutee dans le .sh (wrapper porte la meme logique) + verifier la syntaxe (bash -n) et la sortie identique.
3. LE DRY-RUN [AUCUN CHANGEMENT] EST LA PREUVE QUE L OUTIL ACCEPTE LE NOUVEAU FORMAT SANS ECRIRE - c'est le verdict attendu pour une reparation de mismatch structurel.

**Preuves** : test-064 7/7 OK, catalogue 0 decalage, verifier/dry-run py=sh, rapport detecter-decalages-catalogue-2026-08-24.md.

[LECON 2026-08-24] Test-100-frontmatter-yaml-ferme cree : VALIDE (2 OK/0 KO, 807 .md, 437 avec frontmatter). Incident preview : rapports Themis frontmatter NON FERME invisible pour la non-regression. Lecon : (a) un defaut qui ne se manifeste que dans un outil externe (preview) exige un test dedie ; (b) le parse YAML strict rejette des frontmatters volontaires (block scalars, commentaires seuls) - le critere pertinent est la CLOTURE ; (c) test-ascii*.md ont un frontmatter ferme sans cle : volontaire.
## [LECON] 2026-08-24 -- TEST-101 ARBRES V2 MERMAID : VALIDE (inter-round Vulcain)

**Contexte** : inter-round de Vulcain (mission: etendre convertir-carte-mermaid au mode --arbres pour les ARBRES de decision v2 - freelances avec arbre-<agent>.json, racine/branches/fins, PAS des cartes v1). Delegue a Morpheus : creer le test dedie du mode --arbres.

**Verifications** : test-101-arbres-mermaid-garde-fou cree (11 points : 9 .mmd + 9 .svg + index, verifier_arbres rc=0, syntaxe 0 erreur, index 9 agents, ASCII 0/0 + LF pur 0 CRLF, XML 9/9 bien formes, determinisme 9/9 octet a octet, 2 preuves negatives .mmd/.svg detectees rc=1). 11 OK / 0 KO. 0 residu (fichiers sources restaures apres preuves). Les 6 KO de test-096 sont PRE-EXISTANTS (hades manquant + svg v1 desynchronises - identifies a la baseline via stash).

**Lecons** :
1. LES ARBRES V2 SONT UNE STRUCTURE DIFFERENTE DES CARTES V1 : arbre-<agent>.json (racine -> branches vers theme-*.json -> fins.json centralise) vs parcours-<agent>.json (cases). Un test dedie etait NECESSAIRE - le test-096 (cartes v1) ne couvre pas le mode --arbres meme s il affiche la ligne arbres via l outil.
2. verifier_arbres(racine, dossier_sortie) attend la RACINE DU PROJET (contenant cerveau-projet/), PAS cerveau-projet/ lui-meme - sinon lister_arbres trouve 0 arbre et les preuves negatives passent a tort (faux positif). Premier essai du test : 9 OK/2 KO, les 2 preuves ne detectaient rien car 0 arbre compare. Correction : passer PROJECT_ROOT.
3. LE --verifier COMBINE cartes v1 ET arbres v2 (rc = rc_v1 or rc_v2) : la preuve negative doit appeler verifier_arbres DIRECTEMENT (module) pour isoler les arbres, pas la CLI --verifier (deja rc=1 a cause des cartes v1 pre-existantes desynchronisees).

**Preuves** : test-101 11/11 OK, --arbres --verifier "9 arbres v2 synchronises : OK", baseline stash test-096 6 KO pre-existants, ASCII 0/0 test-101.
## [LECON] 2026-08-24 -- TESTS SUPPRESSION ENCART AUTRE (activer-agent-principal v0.7.1) : VALIDE (inter-round Vulcain)

**Contexte** : inter-round de Vulcain : supprimer le concept d encart 'Activites recentes -- autre' dans AGENTS-historique.md (demande utilisateur : ne garder que session-admin et session-freelance). Modifie : mapper_id_vers_session (mapping sessions historiques session-1 -> session-admin, session-llm-1 -> session-freelance, session-llm-2 -> session-admin) + maj_encart_activites (repli 'autre' supprime : les entrees non mappees sont ignorees des encarts, pas de nouvel encart).

**Verifications** : test-001 11/12 (KO Test 7 pre-existant baseline), test-002 7/8 (pre-existant baseline), test-018 10/13 (3 KO pre-existants : compte parcours 21 vs 23, redacteur-v2), test-021 8/9 (KO-7 pre-existant), test-056 18/18 OK, test-090 11/11 OK. Aucun NOUVEAU KO (comparaison stash). Fonction maj_encart_activites testee sur copie : encarts = [session-admin, session-freelance], plus d 'autre', entrees session-1/themis absorbees.

**Lecons** :
1. UNE SUPPRESSION DE CONCEPT (encart 'autre') SE VERIFIE PAR LA REGENERATION : lancer maj_encart_activites sur une copie et verifier que les encarts produits ne contiennent que admin/freelance - la preuve est dans la SORTIE, pas dans le code.
2. LES ENTREES HISTORIQUES NON MAPPEES (session-1) DOIVENT ETRE IGNOREES DES ENCARTS, PAS CREEES DANS 'autre' : le repli par defaut d un mapping.get() est une source de concepts parasites - un repli qui cree une categorie inattendue est un bug de conception.
3. LA COMPARAISON STASH EST LA SEULE PREUVE DE NON-REGRESSION : chaque KO constate doit etre rejoue a la baseline pour distinguer pre-existant vs nouveau.

**Preuves** : test-056 18/18, test-090 11/11, baselines test-001/002/018/021 identiques, sortie maj_encart_activites sans 'autre', ASCII 0/0.
LECON 2026-08-25 (mission tests microsecondes) : 1) Le glob test-0* du lanceur ne matchait PAS les tests 100+ (test-100/101/102 jamais executes par la non-regression) - corrige en test-* (lanceur + test-027). Toujours verifier que la detection par glob couvre les nouveaux numeros. 2) %3f est INVALIDE en Python (ValueError) : la troncature [:-3] est le bon pattern (horloge.py). 3) test-101 (arbres mermaid) n ayant jamais tourne, la desynchronisation edith/stark etait invisible - verifier que chaque nouveau test est reellement execute (test-027 point 1). 4) Un correctif de donnees sans correctif de l outil qui les ecrit = recurrence (deja arrive avec 4fbd28f).
## [LECON] 2026-08-25 -- TEST-092 : EXEMPTION AGENTS CONFIDENTIELS (ferrari/stark)

Contexte : Vulcain a branche ferrari a l activation (activer-agent-principal v0.7.4). ferrari est CONFIDENTIEL (seul Cerberus le connait, absent volontairement d AGENTS.md - decision utilisateur) : test-092 (parite py/sh/AGENTS.md) le signalait comme 'agent mort' (KO points 4/5, avec stark en KO preexistant).

Realise : EXEMPTIONS_MORTS = {stark, ferrari} soustraite des morts aux points 4/5 + docstring documente les 2 raisons. Resultat : test-092 9/9 OK (le KO preexistant stark est resolu au passage). Activation reelle sur copie : ferrari ACTIVABLE.

Lecons :
1. UN AGENT CONFIDENTIEL (absent volontairement d AGENTS.md) CONFLIT AVEC LA PARITE py/sh/AGENTS.md : la confidentialite et le garde-fou de parite sont incompatibles par conception - il faut une EXEMPTION EXPLICITE ET DOCUMENTEE dans le test, pas un contournement silencieux.
2. UNE EXEMPTION DOCUMENTEE PEUT RESOUDRE UN KO PREEXISTANT AU PASSAGE : stark (v2, fiche freelance/) etait deja 'mort' - la liste d exemptions l a couvert aussi, test-092 passe de 7/9 a 9/9.
3. TOUT AGENT CONFIDENTIEL DOIT AVOIR SA RAISON DANS LE TEST : la liste d exemptions doit porter la decision utilisateur (qui connait l agent, pourquoi il est absent) pour que le garde-fou reste lisible.

**Preuves** : rapport test092-ferrari-2026-08-25.md, test-092 9 OK / 0 KO, activation sur copie OK, ASCII 0/0, LF pur.
## [LECON] 2026-08-28 -- TEST-104 VIGIE-ROUND + PILOTE ORACLE : GARDE-FOU 10/10 (Morpheus)

**Contexte** : mission vulcain, correction du pilote Oracle et creation de la routine vigie-round, decision utilisateur les deux en cascade. Garde-fou de non-regression demande.

**Actions** : creation de test-104-vigie-round-garde-fou avec 10 points, triplet, protections importees, serie e, profils-tests mis a jour. Verifie le triplet de la vigie, la detection 4W session-orpheline, la detection chaine-en-attente, l anti-spam 30 min, le manifest, l execution reelle --dry-run, le pilote limite par defaut 1 pas, la mission et l ordre en tete du plateau, l absence d activation automatique des maillons, le parser oracle --limite 1.

**Lecons** :
1. LA LIMITE VIVAIT DANS LE PARSER, PAS DANS LA FONCTION : la limite 60 par defaut etait portee par argparse, default 60 de oracle.py, qui ecrase le defaut python de cmd_pilote. Un garde-fou doit verifier les DEUX endroits, argparse et fonction.
2. UN GARDE-FOU DE ROUTINE SE TESTE AUSSI PAR EXECUTION REELLE --dry-run, rc egal 0 et sortie conforme : le code structurel seul ne suffit pas.
3. L ANTI-SPAM D UNE VIGIE EST ESSENTIEL : sans lui, l alerte spammerait l inbox de Cerberus toutes les 60 secondes.
4. LES MOTIFS DE TEST DOIVENT MATCHER LE TEXTE REEL : un retour a la ligne casse la chaine, un commentaire sur 2 lignes doit etre teste par motifs par ligne.

**Verdict** : VALIDE - test-104 10 OK sur 10, serie e, profils-tests a jour, non-regression complete deleguee a Janus.
## [LECON] 2026-08-28 -- NON-REGRESSION OBSOLETE DEPUIS LA MIGRATION : COMPTEURS FIGES ADAPTES (Morpheus)

**Contexte** : prise de conscience utilisateur - la suite de non-regression n est plus valide depuis la migration des agents. Les tests portaient des compteurs figes qui n avaient pas suivi les ajouts de parcours/cases. Mission : adapter les tests obsoletes (test-005, test-013, test-018) + transmettre les dettes de cartes a Vulcain.

**Adaptations (domaine Morpheus)** :
1. test-018 : 21 -> 24 parcours (cerberus-freelance, ferrari, socrate revision-*), DERNIER_MAILLON etendu a redacteur-v2 c8 (fin REACTIVER legitime, bilan consolide, MODE CONVERSATION), point 1b adapte (set(fins) == set(DERNIER_MAILLON)). 13/13 OK.
2. test-005 : parcours-atlas 0.5.4 -> 0.5.7, 13 -> 14 commandes (ajout c35), chemins de navigation etendus (questions c10b/c11b ajoutees), case c3 disparue -> c16 (Lister les fichiers existants) avec --case direct. 27/28 (point 21 valider-cartes bloque par le verrou d habilitation sous morpheus - passera sous Janus, habilite).
3. test-013 : parcours-cerberus 27 -> 33 cases action (6 ajoutees c1h*/c20h, branche historisation Oracle), verdict 3b adapte : 0 erreur + dette allegement LIMITEE a la liste documentee c1h*/c20h (au lieu de CONFORME strict). 22/22 OK.

**Dettes de cartes detectees (transmises a Vulcain)** :
1. hades c5.vers->cerberus : fin avec champ vers invalide (spec regle 3 : une fin n a ni branches ni suivant) - reference cassee valider-cartes --tous.
2. parcours-cerberus c1h*/c20h : 6 indices >160 car (commande oracle d historisation) - a alleger vers reference.

**Lecons** :
1. UN COMPTEUR FIGE DANS UN TEST DEVIENT UN MENSONGE APRES UNE MIGRATION : chaque ajout d agent/parcours/case doit etre accompagne de la mise a jour des compteurs des tests qui les comptent - la non-regression doit rester la photo de la realite.
2. UN VERDICT STRICT (CONFORME) PEUT ETRE REMPLACE PAR UNE DETTE DOCUMENTEE LIMITEE : au lieu d accepter n importe quel A ALLEGER, verifier que la dette est EXACTEMENT la liste documentee - le garde-fou reste serre tout en reflechissant la realite.
3. UNE FIN AVEC CHAMP vers EST INVALIDE (spec regle 3) : les fins REACTIVER se materialisent par la COMMANDE dans le message, jamais par un champ vers pointant vers un agent.

**Verdict** : VALIDE - test-018 13/13, test-013 22/22, test-005 27/28 (point 21 = verrou habilitation, passera sous Janus), ASCII 0/0, compilation OK. Dettes de cartes transmises a Vulcain (inter-round).
## [LECON] 2026-08-28 -- SUITE INTER-ROUND : VERDICTS STABILISES APRES CORRECTION DES CARTES (Morpheus)

**Contexte** : reprise du round principal apres l inter-round vulcain (dettes de cartes hades c5 + cerberus c1h*/c20h corrigees).

**Adaptations finales** :
1. test-013 point 3b : restaure CONFORME strict (la dette c1h*/c20h a ete allegee par vulcain - la carte est redevenue CONFORME, le verdict strict redevient la bonne attente). 22/22 OK.
2. test-018 : la correction de hades (titre 'FIN - Reactiver Cerberus' + message 'BILAN CONSOLIDE') l a rendu detecte par le test - c est une fin dernier maillon LEGITIME : DERNIER_MAILLON etendu a hades c5. 13/13 OK.

**Lecons** :
1. UNE CORRECTION DE CARTE PEUT REVELER UNE FIN LEGITIME AU TEST : retirer le champ vers de hades c5 a expose sa fin REACTIVER au garde-fou - le test doit alors l accepter comme dernier maillon (pas le corriger pour le masquer).
2. UNE DETTE DOCUMENTEE DANS UN TEST PEUT ETRE RESORBEE : le test-013 a d abord documente la dette (A ALLEGER limite), puis l inter-round vulcain l a corrigee - le test doit REVENIR au verdict strict des que la realite le permet (sinon le garde-fou reste affaibli pour rien).

**Verdict** : VALIDE - test-005 27/28 (point 21 verrou habilitation, passera sous Janus), test-013 22/22, test-018 13/13, ASCII 0/0, compilation OK. Non-regression complete deleguee a Janus (controle croise).
## [LECON] 2026-08-28 -- DERNIERS TESTS OBSOLETES ADAPTES (Morpheus, inter-round Cerberus)

**Contexte** : apres l inter-round vulcain (cartes corrigees), Cerberus m a active pour les 2 derniers tests obsoletes : test-070 (themis c8ir) et les compteurs catalogue 186 figes.

**Adaptations** :
1. test-070 point 3 : ajout de l exemption INTER-ROUND pour la forme presente 'me/le/la REACTIVE'. Quand le contexte immediat mentionne l inter-round (protocole-fin-mission v0.2.0), 'l habilite me REACTIVE' designe l HABILITE qui reactive l APPELANT - ce n est PAS une cible non-Cerberus fautive. Le message themis c8ir est la formulation officielle du protocole. 13/13 OK. La preuve negative 6b (injection sans mot-cle inter-round) reste detectee : l exemption ne l affaiblit pas.
2. test-007 point 13, test-060 point 7, test-079 point 10 : compteurs catalogue 186 -> 187 (hades-contexte-git est un outil reel ajoute commit 8a85f52, catalogue correct verifie par test-040 5/5). test-007 15/15, test-060 12/12.
3. test-060 : version analyser-tokens 0.1.2 -> 0.1.4 (le .py et le .md ont ete bumpe a 0.1.4, le test pinnait l ancienne version). 12/12 OK.

**KO restant documente (hors mission)** : test-079 point 5 - le registre reel contient 87 entrees AGENT_INCONNU (55 stark + 32 Cerberus) : analyser-noms-maj ne connait pas les agents freelance (stark sous freelance/, pas agents/) ni l ancienne casse 'Cerberus'. C est un probleme d OUTIL (analyser-noms-maj doit inclure les agents freelance + normaliser la casse), domaine Vulcain - pas un probleme de test.

**Lecons** :
1. UNE EXEMPTION DE TEST DOIT GARDER SA PREUVE NEGATIVE : l exemption inter-round de test-070 reste etroite (mot-cle 'inter-round' dans le contexte immediat) - la preuve negative 6b injecte une forme SANS ce mot-cle et reste detectee. Exempter = cibler le contexte exact, pas desactiver la detection.
2. UN COMPTEUR DE TEST DOIT SUIVRE LE CATALOGUE REEL : 187 est la realite (hades-contexte-git est indexe, test-040 le verifie) - le pin 186 etait un mensonge post-migration.
3. UN PIN DE VERSION DANS UN TEST PEUT DEVENIR OBSOLETE SANS BUMP : analyser-tokens a ete bumpe 0.1.2 -> 0.1.4 sans que test-060 ne suive. Verifier la version reelle avant de corriger un compteur.

**Verdict** : VALIDE - test-070 13/13, test-007 15/15, test-060 12/12, test-079 14/15 (point 5 = outil analyser-noms-maj, transmis a Vulcain), ASCII 0/0, compilation OK. Recontrole delegue a Janus.
## [LECON] 2026-08-28 -- DERNIERS COMPTEURS FIGES ADAPTES (Morpheus, chaine Cerberus)

**Contexte** : suite de la chaine (vulcain a corrige test-079/096), Cerberus m a active pour les 2 derniers tests obsoletes restants.

**Adaptations** :
1. test-006 point 2b : compteurs fige - parcours-atlas attendu 52 cases/14 chemins, reel 51 cases/16 chemins (evolution v0.5.7). Adapte vers les valeurs reelles verifiees par generation reelle (cartographier-parcours sort 51/16). 19/19 OK.
2. test-004 point 7a : version parcours-morpheus 0.5.4 attendue, reel 0.5.8. Pin adapte. 7a OK.

**KO restant (contrainte d execution, pas un bug de test)** : test-004 point 8 - valider-cartes-decision --agent morpheus est BLOQUE par le verrou d habilitation (morpheus n est pas habilite : seuls argus/buffy/janus/vulcain). Passera sous Janus (habilite) lors de la non-regression. Meme cas que test-005 point 21.

**Lecons** :
1. UN EN-TETE DE CARTOGRAPHIE EST UN MIROIR DU PARCOURS : les compteurs (cases/chemins) changent avec chaque evolution de carte - le test doit refleter la generation reelle, pas une version passee.
2. LE VERROU D HABILITATION S APPLIQUE AUSSI AUX TESTS MORPHEUS : valider-cartes-decision est exclusif a argus/buffy/janus/vulcain - un test morpheus qui l appelle ne peut etre vert que lance par l agent habilite (Janus). Documenter la contrainte, pas la contourner.

**Verdict** : VALIDE - test-006 19/19, test-004 7a OK (point 8 verrou habilitation, passera sous Janus), ASCII 0/0, compilation OK.
## [LECON] 2026-08-29 -- TEST COLONNE EXECUTEUR ROUTINES RT(INTERVALLE) (Morpheus)

**Mission** : tester la modification activer-agent-principal v0.8.7 (colonne
Executeur de l encart v1 : les routines v1 affichent desormais RT(<intervalle>s)
via le helper _executeur_routine qui lit manifest.json).

**Tests executes** :
1. Comportement _executeur_routine : 7/7 OK (citations RT(300s), flux RT(600s),
   vigie-round RT(60s), sante RT(300s), agents normaux cerberus/vulcain/oracle =
   chaine vide).
2. Test reel sur copie (env AGENTS_* vers /tmp/aap-test2) : l encart produit
   bien les lignes "| citations | 4 | RT(300s) | ...", "| flux | 4 | RT(600s) |",
   "| vigie-round | 4 | RT(60s) |" et les agents normaux restent a colonne vide.
   Les colonnes Defcon/Etat/Secteur restent intactes.
3. Tests existants lies : test-092 9/9 OK, test-102 6/6 OK, test-098 5 OK / 2 KO
   (les 2 KO sont PREEXISTANTS et HORS PERIMETRE : point 2 - les routines flux/
   notation/verifier-statuts/vigie-perimetre historisent des blocs agents dans
   AGENTS-historique.md sans etre dans la liste des agents connus du test
   (exemption uniquement citations) ; point 3 - jour vide 28/08/2026 residu du
   nettoyage de session). Aucun KO lie a la colonne Executeur.
4. Le point 5 de test-098 (lire-activite-recente) depend du cwd : lance depuis
   le dossier du test il echoue (chemin relatif AGENTS-historique.md introuvable),
   lance depuis la racine il passe. Piege cwd : toujours lancer les tests depuis
   la racine du projet comme la non-regression.

**Verdict** : VALIDE - la modification fonctionne (preuve reelle sur copie),
aucun test lie ne casse a cause d elle. 2 KO preexistants a traiter separement
(routines dans test-098 + jour vide du nettoyage).

**Lecons** :
1. TESTER LE COMPORTEMENT SUR COPIE, PAS SEULEMENT LA FONCTION : l appel direct
   de _executeur_routine prouve la logique, mais c est l ecriture reelle dans
   l encart (env AGENTS_ACTIVITE_RECENTE vers copie) qui prouve la colonne
   produite - les deux sont necessaires.
2. UN TEST QUI ECHOUE N EST PAS FORCEMENT CAUSE PAR LA MODIFICATION : les 2 KO
   de test-098 existaient avant (routines non listees, jour vide du nettoyage).
   Toujours distinguer KO preexistant vs KO introduit (tester l etat avant ou
   analyser la cause racine : la colonne Executeur n affecte pas les blocs du
   corps historique).
3. PIEge CWD DES TESTS : lire-activite-recente utilise un chemin relatif par
   defaut - lance depuis le dossier du test il echoue, depuis la racine il passe.
   La non-regression lance depuis la racine : reproduire SES conditions.

**Outils utilises** : lire-fichier, lire-activite-recente, oracle (pilote/lire/
acquitter/mission-lister), verifier-systeme, enregistrer-usage-outil,
tester-protections (lancer_protege via tests individuels).

## [LECON] 2026-09-02 -- TEST-092 PARITE COUVRANT NEMESIS (apres branchement activer-agent-principal v0.8.9)

**Contexte** : inter-round apres la creation de l agent v1 nemesis (Buffy) et son branchement a l activation (Vulcain v0.8.8 -> 0.8.9 : dictionnaire AGENTS py + 3 case statements sh + couleur). Mission : verifier/adapter le garde-fou de parite py/sh/AGENTS.md et les tests qui pinent la version.

**Verifications** :
1. test-092 : ajout de nemesis au pin minimal AGENTS_ATTENDUS (point 1), l extraction dynamique couvre automatiquement le reste (AGENTS.md -> py -> sh dans les deux sens). 9/9 OK.
2. Aucun test ne pinne la version 0.8.8 d activer-agent-principal : test-056 pinne proteger-verrou-habilitation (v0.5.0, outil distinct), test-106 ne mentionne 0.8.8 qu en docstring descriptive (le test charge le module a la volee, pas de pin).
3. Preuve de bout en bout : activation reelle de nemesis sur copie isolee (env AGENTS_FILE + AGENTS_HISTORIQUE vers temp) -> 'nemesis active avec succes' OK. L agent est desormais ACTIVABLE.
4. Coherence 3 sources : AGENTS.md lien [Nemesis](...), py dictionnaire, sh 3 case statements. Version 0.8.9 py/md/spec.
5. 0 residu (tmp-test092-* supprime), ASCII/LF du test modifies OK (point 8 du test verifie).

**Lecons** :
1. LE PIN MINIMAL D UN GARDE-FOU DE PARITE DOIT SUIVRE LES NOUVEAUX AGENTS : AGENTS_ATTENDUS est un anti-corruption (AGENTS.md vide ne doit pas rendre le test vert) - ajouter chaque nouveau agent au pin en meme temps que le branchement (Buffy cree, Vulcain branche, Morpheus pinne).
2. LE BESOIN 'TESTS QUI PINENT LA VERSION' SE VERIFIE PAR RECHERCHE, PAS PAR SOUPcon : aucun test ne pinne 0.8.8 - la mission etait plus large que la realite. Verifier avec grep cible AVANT d adapter des tests (ne rien casser pour rien).
3. UNE DOCSTRING QUI MENTIONNE UNE VERSION N EST PAS UN PIN : test-106 date la tracabilite R/IR 'activation v0.8.8' dans un commentaire - pas de bump necessaire tant que le test charge le module a la volee.
4. PIEGE WINDOWS : subprocess.run avec cwd='Z:/...' (slash POSIX) echoue NotADirectoryError sur CreateProcess - utiliser os.path.abspath('.') natif pour le cwd des sous-processus (deja note lecon cwd des tests, confirme ici).

**Verdict** : VALIDE - test-092 9/9 OK, activation reelle sur copie OK, 0 pin 0.8.8 residuel, 0 residu, ASCII/LF OK. Non-regression complete et recontrole delegues a Janus (pilote).
## [LECON] 2026-09-02 -- TEST MODIFICATION CARTE CERBERUS (ETAPE 2 THEME DE-USER SUPPRIMEE) : VALIDE (Morpheus)

**Contexte** : inter-round Buffy - suppression de l etape [2] 'Identifier l agent habilite (matrice, NE PAS executer soi-meme)' du theme DE-USER de la carte cerberus (decision utilisateur : c est ORACLE qui identifie/largue l agent habilite, pas Cerberus). Verification demandee : coherence carte/fiche, navigation theme DE-USER, pins eventuels.

**Verifications** :
1. verifier-conformite-fiche --agent cerberus : 1 CONFORME / 0 ECART.
2. Navigation guider-arbre : theme DE-USER ne propose plus que 2 besoins ('Ecouter la demande completement' + 'Envoyer la mission a Oracle et lui rendre la main') - l etape 2 a bien disparu.
3. 0 residu du texte supprime ('matrice, NE PAS executer soi-meme' introuvable dans cerveau-projet/agents/cerberus/).
4. theme-de-user.json : redirects = [Ecouter, Envoyer a Oracle] ; arbre-cerberus.json version 0.2.2 ; JSON OK.
5. test-034 (cerberus sans outils de test) NON IMPACTE : il epingle les cases c5/c6 du PARCOURS V1 (parcours-cerberus.json), pas le theme v2 - parcours v1 intact (c5 'Identifier l agent habilite', c6 'Activer l agent habilite' presentes).

**Lecons** :
1. CARTE V2 vs PARCOURS V1 : les tests qui pinnent des cases (test-034 c5/c6) ciblent le PARCOURS v1 archive ; une modification du THEME v2 ne les casse pas tant que le parcours v1 reste intact. Verifier la CIBLE du test avant de conclure a un impact.
2. LA NAVIGATION REELLE EST LA PREUVE : guider-arbre --reponses 'DE-USER' montre les besoins effectifs du theme - plus fiable qu un grep du fichier seul.
3. RESIDU NUMERIQUE : un grep retournant 'residu: 0' est ambigu (code de sortie grep) ; verifier l ABSENCE de sortie (aucune ligne affichee) plutot que le code retour.

**Verdict** : VALIDE - modification conforme, 0 regression detectee, test-034 non impacte.
2026-09-02 | TEST FILE RELAIS ORDONNEE (oracle v0.5.8) : les tests files.py doivent comparer les VALEURS int de priorite (1/2), pas les chaines ('P1') ; prendre() renvoie un TUPLE (entree, erreur) et FILES_DIR est un pathlib.Path (pas str) - le harnais de test doit unpacker et passer un Path. Tri valide a egale priorite = DATE RECENTE d abord (decision utilisateur) : un fixture avec purge plus recente qu urgent donne purge en premier - c est le comportement attendu, pas un bug. L10n ecart doc : oracle.md ligne 122 dit encore '(marque PRISE, FIFO)' - reference FIFO obsoleted a signaler a Vulcain pour mise a jour.
2026-09-02 | TEST REFS PARCOURS V1 x2 (missions 8093a011 + 7353bea9) : VALIDE. Verification de la migration v1->v2 complete : 0 theme/arbre/fins v2 contient guider-parcours ou parcours-<agent> (grep global), 7 arbres guider-arbre --valider VALIDES, reprise v2 cible le bon arbre-<agent>.json (les 6 fichiers existent), outils : demarrer-llm.py v0.1.2 sans repli v1 (--version OK, runtime glm5 admin affiche l arbre v2 cerberus sans mention guider-parcours), editer-parcours.md porte la note ARCHIVE V1. Non-regression : test-034 6/6 + test-109 11/11 (les pins parcours v1 c5/c6 du PARCOURS archive sont intacts - la migration corrige les pointeurs v2, jamais les archives v1). Lecon : un test de migration v1->v2 doit verifier la DOUBLE direction - (1) aucun pointeur actif v2 ne redirige vers v1 (grep themes/arbres), (2) les outils de demarrage ne tombent plus sur le repli v1 (runtime reel), et la non-regression sur les tests qui pinent l ARCHIVE v1 (test-034) prouve qu on n a pas casse les fichiers proteges.
2026-09-02 | TEST URGENT ENCART DETECTION INCONNU (mission 3c2970e6) : VALIDE. 3 zones testees : 1) run reel encart --dry-run = OK (fichier propre, pilote declare SP ne pollue plus) ; 2) detection synthetique : agent-fantome avec grade Inconnu detecte (2 anomalies : grade + agent absent mapping), pilote Special NON signale ; 3) non-regression : les controles Etat inconnu + Executeur vide existants fonctionnent toujours (2 anomalies sur fichier synthetique, pilote propre). Lecon : le test de detection sur un fichier TEMP (shim remplacant le chemin encart + GRADES_V1 pointe sur le vrai fichier) valide la logique sans toucher le fichier reel - pattern a reutiliser pour les routines de surveillance (le cwd reel ne se cale pas depuis /tmp, il faut pointer GRADES_V1 explicitement).
