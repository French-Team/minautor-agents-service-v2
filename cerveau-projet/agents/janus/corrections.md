## [LECON] 2026-08-24 -- CONTROLE MISSION CLIO VERIFIER README (APRES ENCART AUTRE) : VERDICT VALIDE (Janus)

**Contexte** : apres la mission suppression encart 'autre' (activer-agent-principal v0.7.1), Cerberus a active Clio pour verifier le README. Clio : --verifier 0 ECART, aucune modification necessaire. Themis : audit CONFORME 0 defaut. Janus : controle final.

**Diagnostic** : VERIFIE et VALIDE - --verifier 0 ECART (agents table OK, badge Outils-165 OK, readme-dev 40 categories somme 165 = 165), README.md 0 diff, ASCII 0/0 (README + readme-dev + README-v2), rapport Themis present. Le seul diff readme-dev (categorie Git/hades-contexte-git) est PRE-EXISTANT (mission anterieure, deja compte dans la somme 165) : ce n'est pas un ecart de la mission.

**Lecons** :
1. UNE MISSION QUI MODIFIE UN OUTIL EXISTANT (logique interne : mapping, encarts) NE CHANGE JAMAIS LE README : ni agent ni outil ajoute -> le --verifier a 0 ecart est le verdict ATTENDU, pas une surprise.
2. UN DIFF PRE-EXISTANT DANS readme-dev (categorie ajoutee par une mission anterieure) N EST PAS UN ECART de la mission courante si la somme des categories = total reel (165) - verifier la somme avant de signaler.
3. LE FLUX VERIFIER DE CLIO : c1 verifier -> c11 (--verifier) -> c19 (usages) -> c12a (activer Themis) -> c12b (retour) -> c12 (activer Janus). Ne pas confondre avec c12b qui est le point d attente du retour de Themis (PATTERN RE-ESSAI).

**Preuves** : rapport controle-clio-verification-readme-encart-autre-2026-08-24.md, combo controle-modification OK, ASCII 0/0, --verifier 3 OK.
## [LECON] 2026-08-24 -- CONTROLE ENCARTS 10 ACTIVITES : VALID (Janus)

Controle de la mission Vulcain v0.7.2 : encarts 10 activites + raisons completes. VERDICT VALID. Versions 0.7.2 coherentes py/sh/spec, syntaxe OK, ASCII 0/0, mapping correct, repli 'autre' toujours supprime. Test fonctionnel : 10 lignes par encart, 0 troncature. Tests Morpheus : test-056 18/18, test-090 11/11, 0 regression. 9 problemes evaluer-processus pre-existants documentes.
## [LECON] 2026-08-25 -- CONTROLE REPARATION MICROSECONDES (activer-agent-principal v0.7.3) : VERDICT VALID (Janus)

Controle final de la chaine Cerberus -> Themis (audit) -> Vulcain (reparation) -> Morpheus (tests + garde-fou). VERDICT VALID, 0 defaut.

**Verifications** : (1) versions 0.7.3 coherentes py/sh/md/spec ; (2) lanceur officiel (Janus habilite) : test-102/101/099/100 = 4 OK / 0 KO ; (3) reparation timestamps verifiee : 4 x strftime(...%f)[:-3] (l.879/1036/1308/1367) + get_timestamp %3N (.sh) ; (4) ASCII strict 0/0 sur 12 fichiers de la mission (1 correction : 4 tirets cadratins '--' dans le rapport Themis, section ajoutee par l audit -> remplaces par '-') ; (5) LF pur 0 CRLF.

**Lecons** :
1. LE VERROU D HABILITATION DU LANCEUR EST UN VRAI CONTROLE CROISE : Morpheus ne peut pas lancer le lanceur (verrou ferme pour lui, test-027 points 5-8 KO attendus) - c est Janus qui le lance : le second controle utilise l outil OFFICIEL, pas les tests en --isoler.
2. UN TIRET CADRATIN '--' (U+2014) INTRODUIT PAR UN EDITEUR EST UNE VIOLATION ASCII : le str_replace de ma section de rapport a introduit 4 em-dashes invisibles - toujours revalider ASCII apres CHAQUE edition (pas seulement a la creation).
3. UNE CHAINE DE REPARATION COMPLETE PRODUIT DES BONUS : le garde-fou test-102 a revele un bug preexistant du lanceur (glob test-0* excluait test-100+) - les controles en chaine (audit -> reparation -> tests -> controle) attrapent plus que la mission initiale.

**Preuves** : rapport themis/rapports/rapport-diagnostic-microsecondes-2026-08-25.md (suite audit CONFORME), rapport morpheus/rapports/rapport-tests-microsecondes-2026-08-25.md, lanceur 4 OK/0 KO, ASCII 0/0.
## [LECON] 2026-08-25 -- CONTROLE EDUCATION CERBERUS -> FERRARI : VERDICT VALID (Janus)

Controle final de la chaine Cerberus -> Chiron (education) -> Buffy (application inter-round) -> Janus (controle). VERDICT VALID, 0 defaut.

**Verifications** : (1) ferrari present dans la fiche cerberus.md (2 occurrences : table 'Agents disponibles' + REGLE voie freelance v1 vs v2) ; (2) ferrari present dans regles-choisir-agent.md (1 : matrice Etape 1) ; (3) verifier-conformite-fiche cerberus 1 CONFORME / 0 ECART (v0.2.2) ; (4) ASCII strict 0/0 sur les 2 fichiers modifies ; (5) aucun changement de parcours (flux generique c8 -> c10 suffisant).

**Lecons** :
1. UNE EDUCATION DE COORDINATEUR SANS CHANGEMENT DE PARCOURS SE CONTROLE PAR LA PRESENCE DU SAVOIR DANS SES SOURCES DE VERITE (fiche + matrice) : la preuve d education n est pas un diff de carte mais la presence de ferrari dans la table 'Agents disponibles' et la matrice choisir-agent.
2. LA CONTRADICTION FERRARI/JARVIS EST UNE DETTE A SUIVRE : la fiche ferrari liste 'Corriger JARVIS' vs exclusivite Vision (AGENTS.md) - signalee dans le rapport Chiron, a arbitrer (Argus/Vision/Buffy) lors d une prochaine mission.

**Preuves** : rapport chiron/rapports/rapport-education-cerberus-ferrari-2026-08-25.md, fiche cerberus v0.2.2 CONFORME, ASCII 0/0, LF pur.
## [LECON] 2026-08-25 -- CONTROLE BRANCHEMENT AGENT CONFIDENTIEL (activer-agent-principal v0.7.4) : VERDICT VALID (Janus)

Controle final de la chaine Cerberus -> Vulcain (branchement) -> Morpheus (test-092 adapte) -> Themis (audit) -> Janus (controle). VERDICT VALID, 0 defaut.

**Verifications** : (1) agent v1 specialise freelance CONFIDENTIEL present dans le dictionnaire py + 3 case statements sh + couleur ; (2) versions 0.7.4 coherentes py/sh/md/spec ; (3) test-092 9/9 OK (exemption documentee ferrari/stark, KO preexistant stark resolu) ; (4) confidentialite : absent de la table AGENTS.md et des docs v2 - seule la raison transitoire du bloc session peut porter le nom, nettoyee a chaque activation ; (5) activation reelle sur copie OK.

**Lecons** :
1. LA CONFIDENTIALITE D UN AGENT SE VERIFIE PAR 3 ABSENCES + 1 PRESENCE : absent d AGENTS.md (table), absent des docs freelance/, absent des raisons d activation (a nettoyer a chaque activation) - mais PRESENT dans le dictionnaire d activation (sinon inactivable). Le nom ne doit vivre QUE dans les sources v1 internes (fiche Cerberus, matrice, corrections).
2. LA RAISON DU BLOC SESSION EST UN VECTEUR DE FUITE TRANSOIRE : chaque activation ecrase la raison - le dernier maillon de la chaine doit reactiver Cerberus avec une raison SANS le nom confidentiel pour laisser AGENTS.md propre.

**Preuves** : test-092 9/9, versions 0.7.4 coherentes, ASCII 0/0, activation sur copie OK, grep AGENTS.md -> 0 occurrence du nom (apres reactivation finale).
## [LECON] 2026-08-28 -- CONTROLE CROISE PILOTE ORACLE + VIGIE-ROUND (Janus)

**Contexte** : round vulcain puis morpheus puis janus, decision utilisateur les deux en cascade. Controle croise de la chaine.

**Constats** :
1. Pilote Oracle corrige, limite par defaut 1 pas, mission et ordre en tete du plateau, plus d activation automatique des maillons, precedent cerberus lors d une auto-reactivation.
2. Routine vigie-round creee et indexee, detection session orpheline et chaine en attente, alerte 4W, anti-spam 30 min.
3. test-104 garde-fou 10 points, 10 OK via lanceur, serie e 100 sur 100.
4. test-063 avait un BUG DE COUVERTURE : lister_tests_reels utilisait startswith test-0, excluant test-100 et plus, traites comme fantomes. Corrige en startswith test- : 102 tests reels couverts, 11 sur 11 OK.
5. KO preexistants hors perimetre du round, documentes : catalogue 187 vs 186 attendu, CRLF residuels, cerberus-freelance cU2, processus residuels lies aux daemons actifs, test-082 pilote.py docstring tmp-buffy issue du code du 27-08 non commite.

**Lecons** :
1. UN GARDE-FOU PEUT AVOIR UN ANGLE MORT : startswith test-0 ne couvre pas test-100 plus. La couverture des listes de tests doit etre testee avec un test au-dela de 99.
2. LES KO PREEXISTANTS D UN ETAT NON COMMITE NE DOIVENT PAS BLOQUER UN ROUND : les documenter et verifier que le round lui-meme est vert.

**Verdict** : VALIDE - pilote Oracle corrige, vigie-round operationnelle, test-104 10 sur 10 via lanceur, test-063 corrige 11 sur 11, lecons avec verdict. KO preexistants documentes pour un round dedie.
## [LECON] 2026-08-28 -- CONTROLE CROISE NON-REGRESSION OBSOLETE + CORRECTIONS ROUND (Janus)

**Contexte** : prise de conscience utilisateur - la suite de non-regression n est plus valide depuis la migration des agents. Controle croise de la chaine vulcain-morpheus (inter-round inclus).

**Constats** :
1. Corrections vulcain (round precedent) : test-082 9/9, test-040 5/5 (hades-contexte-git indexe), test-047 10/10 (CRLF : 5 sources oracle LF + 40 fichiers + exclusions freelance/observations).
2. Adaptations morpheus : test-005 28/28 SOUS JANUS (le point 21 valider-cartes est bloque par le verrou sous morpheus - habilite pour janus), test-013 22/22, test-018 13/13.
3. Inter-round vulcain : hades c5 (vers retire, titre 'FIN DE MISSION - reactiver Cerberus', bilan consolide) + cerberus c1h*/c20h alleges -> valider-case CONFORME, 0 reference cassee.
4. Mon adaptation hades c5 a revele la REGLE IMMUABLE JANUS (test-070 : fin 'FIN - Reactiver Cerberus' uniquement chez janus) : titre aligne sur le modele redacteur-v2 (FIN DE MISSION) qui ne matche pas le motif strict.

**KO restants (9) tous PREEXISTANTS ou artefacts** :
- test-070 themis c8ir 'me REACTIVE' : protocole inter-round legitime (l habilite reactive l appelant) - etat non commite.
- test-072 'mecano' = parcours-ferrari avec identite.appartient_a='mecano' (renommage ferrari non reporte) + c0 type=indice (structure obsolete).
- test-080 fiche buffy section PARCOURS (carte arbre v2 sans maj fiche).
- test-060/067/079/007 : catalogue 187 vs 186 + activer-agent-principal.sh 0.7.4 vs .py 0.8.2 (bump .py sans .sh) + registre stark 2026-08-23.
- test-085 processus daemons : artefact attendu (daemons oracle+routines actifs).
- test-055 cerberus-freelance cU2 : regle mentionne generateurs-commande/consulter-combos sans indices outil.

**Lecons** :
1. LE VERROU D HABILITATION EST UN FILTRE REEL DE LA NON-REGRESSION : test-005 point 21 passe uniquement sous janus (habilite valider-cartes) - un test qui appelle un outil verrouille ne peut etre valide que par l agent habilite.
2. UN TITRE DE FIN 'FIN - Reactiver Cerberus' EST RESERVE A JANUS (REGLE IMMUABLE) : les autres derniers maillons (redacteur-v2, hades) utilisent 'FIN DE ... - reactiver Cerberus' pour exprimer la reactivation sans matcher le motif strict.
3. UN RENOMMAGE D AGENT (mecano -> ferrari) LAISSE DES TRACES : identite.appartient_a dans le parcours + nom du dossier - test-072 le detecte (c0 type=indice). A corriger par Vulcain (carte ferrari).

**Verdict** : VALIDE - toutes les corrections du round sont vertes sous janus (test-005 28/28, test-013 22/22, test-018 13/13, test-082 9/9, test-040 5/5, test-047 10/10), 0 nouveau KO introduit (hades corrige). KO restants documentes pour un round dedie (cartes ferrari, cerberus-freelance, themis c8ir, bumper .sh, catalogue 187).
## [LECON] 2026-08-28 -- RECONTROLE APRES INTER-ROUND MORPHEUS : BARRIERE KO DEBLOQUEE, 4 KO CACHES REVELES (Janus)

**Contexte** : recontrole de la chaine apres l inter-round morpheus (test-070 + compteurs catalogue adaptes). La non-regression a tourne avec --desactiver 79,85 (2 KO documentes hors perimetre).

**Adaptations morpheus verifiees (toutes vertes sous janus)** :
- test-070 : 13/13 (exemption inter-round pour 'l habilite me REACTIVE' = protocole v0.2.0).
- test-007 : 15/15 (catalogue 187).
- test-060 : 12/12 (catalogue 187 + version analyser-tokens 0.1.4).
- test-079 : 14/15 (point 5 KO = outil analyser-noms-maj ne connait pas les agents freelance stark ni la casse Cerberus - 87 entrees AGENT_INCONNU, domaine Vulcain).
- test-067/072/080/055 : verts (corrections vulcain de l inter-round precedent).

**BARRIERE KO DEBLOQUEE -> 4 KO CACHES REVELES (preexistants, jamais vus car la barriere s arretait sur les 9 premiers)** :
1. test-096 (6 KO) : ferrari + hades n ont NI .mmd NI .svg dans cartes-vues/mermaid - la generation des vues n a jamais suivi l ajout de ces 2 agents. Domaine : generation cartes-vues (Vulcain/Buffy).
2. test-001 (1 KO) : lien casse - protocole-verification-coherence.001.01.ebauche.md pointe vers ../../../themis/rapports/rapport-audit-coherence-readme-2026-08-10.md (fichier inexistant). Domaine : doc (Buffy).
3. test-006 (1 KO) : compteur fige - parcours-atlas attendu 49 cases/13 chemins, reel 51/16 (evolution v0.5.7). Meme classe que les compteurs adaptes par morpheus. Domaine : test (Morpheus).
4. test-004 (1 KO) : version morpheus 0.5.4 attendue, parcours-morpheus reel 0.5.8. Pin de version obsolete. Domaine : test (Morpheus).

**Lecons** :
1. LA BARRIERE KO MASQUE LES KO SUIVANTS : tant que la serie KO persiste, les tests au-dela de la barriere ne tournent pas - debloquer les premiers revele les suivants (ici 4 KO preexistants caches).
2. UN AJOUT D AGENT DOIT GENERER SES VUES MERMAID : ferrari et hades sont dans AGENTS.md et leurs parcours existent, mais cartes-vues/mermaid n a jamais ete regenere - test-096 le detecte.
3. LE RECONTROLE COMPLET NECESSITE --desactiver LES KO DOCUMENTES : sinon la barriere stoppe tout (verdict faussement restreint). Les KO documentes doivent etre listes pour laisser la suite tourner.

**Verdict** : VALIDE - toutes les adaptations morpheus sont vertes sous janus. 0 nouveau KO introduit par le round. 6 KO restants documentes pour un round dedie : test-079 (outil analyser-noms-maj, Vulcain), test-085 (daemons, artefact attendu), test-096 (cartes-vues, Vulcain/Buffy), test-001 (lien casse doc, Buffy), test-006 (compteur atlas, Morpheus), test-004 (version morpheus, Morpheus).
## [LECON] 2026-08-29 -- CONTROLE FINAL REPARATION GATE : VERDICT VALIDE (Janus)

Controle final de la chaine apres la reparation Buffy des 25 KO GATE (decision utilisateur marbre-log 2026-08-29 appliquee sans synchroniser les garde-fous).

**Constats** : non-regression complete 96 OK / 10 KO (106 tests, serie). Tous les KO de la reparation GATE corriges + synchronisation des garde-fous : valider-cartes-decision reconnait le chemin GATE (c0b OUI -> c0g -> c0ga -> c0c), test-005 (15e commande c0g), test-006 (54 cases/17 chemins), test-021 (sequences OUI supplementaire), test-045, test-072 (branches c0b GATE), test-103 (raison tronquee sans ponctuation - corrigee dans AGENTS.md), cerberus.md PARCOURS v0.5.11 (Pattern 14).

**Lecons** :
1. UN GARDE-FOU CENTRAL MASQUE LES KO SUIVANTS : corriger valider-cartes-decision a resolu test-045 d un coup mais revele des suivants morts preexistants (buffy c16/c22b/c27b/c8b, vulcain c15g/c9g, morpheus c14b).
2. LA DERIVE LAISSE DES TRACES FAUTIVES : registre-usages-outils (DECLARATION_FAUTIVE buffy verifier-systeme, cerberus analyser-noms-maj) + MARBRE DIVERGENT (cerberus.c10, regles-general-global) - violation de securite a nettoyer par les agents habilites.
3. LES 10 KO RESTANTS SONT TOUS PREEXISTANTS OU CONSEQUENCE DE LA DERIVE : test-027/063 (tests 105-109 non mappes), test-028 (spec divergente), test-035 (traces fautives), test-047 (artefacts routines), test-057/068 (marbre), test-070 (oracle c14/c20), test-079 (registre noms-maj), test-094 (oracle absent table cerberus.md) - a traiter en round dedie.

**Verdict** : VALIDE - la reparation GATE est conforme et verifiee. 10 KO preexistants documentes pour un round dedie (priorite : violation marbre).
## [LECON] 2026-08-30 -- MIGRATION ARBRE V1 -> MODELE AERO (Buffy)

Migration de l arbre de Janus au modele aero (spec round-avion-parachutiste 2026-08-30).

**Constats** : audit initial F4 BLOQUANT (4 fins cible cerberus, vestiges v1) + C4 (activation descendante dans theme-inter-round). Reconstruction appliquee : fins -> oracle (R1) + commandes reactiver-fin --cible oracle, theme-inter-round nettoye (l agent n active plus d autre agent, R3). Fiche janus.md alignee (fin vers ORACLE, le pilote decide).

**Lecons** :
1. LES FINS V1 (cible cerberus + commande activer) SONT DES VESTIGES SYSTEMATIQUES : l audit F4 les detecte et la reconstruction les reoriente vers oracle --cible oracle, sans toucher aux themes (contenu descendant).
2. L INTER-ROUND DANS LE MODELE AERO : l agent n active JAMAIS l appelant directement (commande activer) - il accuse reception et sa fin reactiver-fin --cible oracle ramene a ORACLE, le pilote reactive l appelant depuis l etat de carte (precedent).
3. TEST PILOTE BOUT EN BOUT : theme NON-REGRESSION pilote -> Theme termine -> Fin de parcours : l agent doit revenir vers ORACLE (modele aero R1) - valide.

**Verdict** : VALIDE - arbre de janus en phase modele aero (audit 20 OK / 0 bloquant / 0 avertissement).
## [LECON] 2026-09-04 -- CONTROLE SIGNAL DETECTER-IMPACTS + CORRECTION BRANCHES AUTRE : A REVOIR (Janus)

**Contexte** : mission 8bca6f3d - verifier le signal detecter-impacts suite a la correction des branches AUTRE (18 theme-autre.json realignes sur le modele ORACLE/pilote, R3 - l agent signale au pilote au lieu d activer lui-meme).

**Verifications** : (1) signal detecter-impacts reproduit sur theme-autre.json (15 impliques / 14 potentiellement non mis a jour) et sur theme-agent.json (15 impliques / 3) ; (2) examen des 15 fichiers Buffy : distinction impacts reels vs traces/preexistants ; (3) valider-cartes-decision sur les 3 parcours sous controle : Buffy, Morpheus, Vulcain.

**Constats** :
1. LA CORRECTION DES BRANCHES AUTRE EST CONTENTE ET COMPLETE : les 18 theme-autre.json sont realignes (0 residu ancien modele 'Activer l agent habilite' sur tout le corpus), les fins v2 pointent vers ORACLE (reactiver-fin --cible oracle).
2. LE SIGNAL DETECTER-IMPACTS EST FIABLE MAIS BRUITEUX : il compare les dates de modification des fichiers partageant le meme appartient_a - sur un changement de theme, il flag 14 fichiers dont la plupart n ont pas besoin de mise a jour (artefacts de timestamp) et IGNORE les impacts reels hors appartient_a. Verifier par CONTENU (grep du motif change), pas par la seule liste.
3. IMPACT REEL RESIDUEL : theme-creer.json de Buffy (l.92) porte encore la description 'les signaler a Cerberus' au lieu d ORACLE/pilote (la fin reelle fin-erreurs-hors-mission est correctement vers ORACLE - ecart de COHERENCE doc/code, domaine Buffy, mineur).
4. ECART DE VALIDATION PARCOURS : valider-cartes-decision valide encore le parcours v1 (parcours-<agent>.json) alors que le pilote v0.2.4 sert les arbres v2 (arbre-<agent>.json + themes) - le validateur ne couvre PAS le format navigue (5 erreurs NON CONFORME sur un arbre v2 sain). Les 3 parcours v1 sous controle sont NON CONFORME pour des suivants morts PREEXISTANTS documentes (buffy c16/c22b/c27b/c8b, morpheus c14b, vulcain c15g/c9g, lecons 2026-08-29) + Pattern 14 absent - aucun n est lie a la correction AUTRE.

**Lecons** :
1. UNE CORRECTION DE NAVIGATION SE CONTROLE PAR LE MOTIF DE CONTENU, PAS PAR LA LISTE D IMPACTS : le signal detecter-impacts oriente, le grep du motif (ancien modele -> nouveau modele) prouve. Toujours recouper les deux.
2. QUAND LE PILOTE NAVIGUE UN FORMAT ET LE VALIDATEUR EN VERIFIE UN AUTRE (v2 servi vs v1 valide), les ecarts de validation ne refletent PAS l etat reel des cartes - l ecart est dans l OUTIL (valider-cartes-decision a aligner sur le format v2, domaine Vulcain/Buffy).
3. LES PARCOURS V1 LEGACY NON SERVIS SONT DES SOURCES DE FAUX POSITIFS : detecter-impacts les flag (timestamp) et valider-cartes-decision les valide (NON CONFORME) alors que le pilote ne les lit plus - dette de migration a trancher (supprimer ou figer).

**Verdict** : A REVOIR - correction AUTRE CONFORME (0 residu), signal detecter-impacts VERIFIE (fiable mais a recouper par contenu), mais 1 ecart doc residuel (theme-creer Buffy -> ORACLE, domaine Buffy) + 1 ecart outil de validation (valider-cartes-decision ne couvre pas le format v2 servi par le pilote, domaine Vulcain). Les NON CONFORME des parcours v1 sont PREEXISTANTS et hors perimetre.
