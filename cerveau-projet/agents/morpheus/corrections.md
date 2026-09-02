


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
