---
identite:
  type: corrections
  appartient_a: themis
  commun: false
---

# Corrections -- Themis

> Fichier de suivi des corrections et lecons apprises par Themis.
> Chaque entree contient : date, contexte, erreur detectee, correction appliquee, lecon.

---

## Historique des corrections

| Date | Contexte | Erreur | Correction | Lecon |
|---|---|---|---|---|
| 2026-08-07 09:00 | Test Audit general en conditions reelles (9 etapes) | AGENTS-historique.md (racine) contenait U+00E9 corrompu dans 'cosmetique' -- detecte par combos-valider-cerveau (valider-conformite-ascii sans argument = scan racine) | Remplace par 'e' simple -- ASCII OK | Le combo scanne la racine (fichiers hors cerveau-projet/ inclus). Apres toute modification d'AGENTS-historique.md, verifier ASCII.
| 2026-08-07 09:00 | Test Audit general en conditions reelles (9 etapes) | evaluer-coherence a 50/100 : 10 liens 'casses' signales | Les 10 liens sont des exemples de documentation (blocs de code, exemples de resultat, syntaxe expliquee), pas des liens reels | Amelioration a planifier : evaluer-coherence doit ignorer les liens dans les blocs de code et les motifs generiques (ancien.md, texte, chemin, .*)
| 2026-08-07 | Inventaire des 78 outils | valider-tableaux signale 1 probleme : themis.md annonce 'Audit general (dont inventaires)' dans la table mais la section s'appelle encore '### Mission : Audit general' | Incoherence de nommage : suffixe ajoute a la table sans renommer le titre de section | Quand on renomme une mission dans la table, renommer AUSSI le titre de la section detaillee (### Mission : X) pour que valider-tableaux trouve la correspondance
| 2026-08-07 | Verification croisee Morpheus / protocole-tests | 2 incoherences mineures : lien frontmatter 'tools/tests/' casse (renommage en 'tester/' non reporte) + motif generique 'protection-*' vs noms reels 'tester-protection-*' dans les etapes | Rapport : themis/rapports/coherence-morpheus-protocole-tests-2026-08-07.md | Lors d'un renommage de dossier d'outils, verifier les fichiers_lies des fiches (frontmatter) et les motifs generiques des etapes
| 2026-08-07 14:21 | Audit general post-activation | evaluer-agents signale 79 faux erreurs '__pycache__' comme des outils manquants (dossiers d'artefacts Python comptes comme des outils) | Rapport : themis/rapports/audit-general-2026-08-07-14-21.md | CORRIGER evaluer-agents: exclure __pycache__ et les dossiers de categorie (parents des outils) | CORRIGER evaluer-agents pour exclure __pycache__ et les dossiers de categorie
| 2026-08-07 14:21 | Audit general post-activation | evaluer-coherence signale un lien casse faux positif: `../agents/conventions/protocoles/convention-protocoles.md` dans `recherches-web/badges-github-shields/badges-README-github.md` -- le fichier existe mais l'outil calcule cible_racine depuis cerveau-projet/ au lieu de la racine du projet | Rapport : themis/rapports/audit-general-2026-08-07-14-21.md | CORRIGER evaluer-coherence: utiliser le projet root comme racine pour cible_racine
| 2026-08-07 14:21 | Audit general post-activation | evaluer-coherence signale 4 faux outils casses (cat, grep, sed, basher) reference par athena -- commandes systeme listees en exemple dans la regle 'OUTILS EXCLUSIFS', pas des outils reels | Rapport : themis/rapports/audit-general-2026-08-07-14-21.md | CORRIGER evaluer-coherence: exclure les commandes systeme connues du scan des outils casses
| 2026-08-08 | Mise a jour du rapport serie parcours (decision utilisateur) | Le prototype vulcain (fins independantes par chemin) est passe de observation-a-corriger a CAS LEGITIME ASSUME | Rapport : themis/rapports/rapport-evaluation-serie-parcours-2026-08-08.md | Une observation d audit peut devenir un cas assume par decision utilisateur : mettre a jour le rapport (observation + recommandation + synthese) et la spec (v0.2.3) de facon SYNCHRONISEE pour garder la coherence audit/spec
| 2026-08-08 | Audit serie 11 parcours (conformite spec v0.2.0) | 2 ecarts MINEURS Pattern 2 : minerve c8 et promethee c8 (mise a jour d'index via editer-fichier) n'ont pas le rappel ASCII en tete de leurs indices + 1 caractere non-ASCII dans MON rapport (le mot 'anterieur' ecrit avec un accent) | Rapport : themis/rapports/rapport-evaluation-serie-parcours-2026-08-08.md | L'audit des 2 patterns est reproductible : (1) Pattern 1 = case Mission question + branches + convergence (--liste + lecture structurelle), (2) Pattern 2 = pour chaque case avec outil d'ecriture (creer/ecrire/editer/ajouter-contenu-fichier), verifier que le PREMIER indice est la regle ASCII. Les parcours de ROUTAGE (cerberus : 0 case d'ecriture) et le PROTOTYPE (vulcain : fins par chemin) sont des cas legitimes documentes. PIEGE RECURRENT : meme moi, evaluatrice, j'ai introduit un accent (anterieur) dans le rapport -- TOUJOURS re-valider l'ASCII du rapport APRES sa redaction, pas seulement le contenu audite. |

## [NOTES] Audit 2026-08-08 -- relecture QUESTION HONNETE dans les 11 parcours

**Audit** : verification que les lecons de la transformation de la relecture en QUESTION HONNETE (case c0 + c0b) sont appliquees dans les 11 parcours.
**Verdict** : CONFORME (100/100, 6/6 points sur les 11 parcours).
**Lecons** :
1. Le referentiel d'audit decoule des lecons de l'auteur (Buffy corrections.md) : 6 points verifiables mecaniquement (case_depart c0, question memoire, branches OUI/INCERTAIN/NON, c0b RELIRE + corrections + fiche, navigation OUI->c1 et c0b->c1, c1 mission presente)
2. PIEGE CRITERE D'AUDIT : le premier script cherchait le mot RELIRE dans le TEXTE de l'indice regle de c0b, alors qu'il est dans le TITRE de la case -- faux negatif sur les 11 parcours ; toujours verifier OU le motif attendu est stocke (titre vs texte) avant de conclure a un ecart
3. La navigation prouve la logique de la decision utilisateur : OUI passe a la mission, NON et INCERTAIN passent par c0b (relire obligatoire) puis la mission -- l echantillon themis + atlas (6 chemins) confirme PARCOURS TERMINE
4. Le rapport ne recommande AUCUNE correction : les 11 parcours sont conformes au referentiel

## [RAPPORT] Audit 2026-08-08 -- Garde-fou restauration (VERDICT CONFORME 5/5)

**Objet** : audit de coherence et conformite du garde-fou restauration ajoute par Buffy (lecon incident piste B) dans regles-general-global.md (tableau regles globales) et protocole-gestion-defaillances.001.01.ebauche.md (Etape 3).
**Verdict** : CONFORME -- 5/5 criteres (presence, coherence inter-fichiers, format, non-regression, hierarchie/index).
**Lecons** :
1. AUDIT MULTI-NIVEAUX : le garde-fou se verifie a 5 niveaux complementaires (presence, coherence, format, non-regression, hierarchie) - un garde-fou present mais contradictoire ou mal place serait inutile.
2. CASSE DIFFERENTE != CONTRADICTION : NON COMMITES (majuscules d emphase dans le tableau) vs non commites (texte courant du protocole) designent la meme condition - l auditeur doit comparer le SENS, pas la casse.
3. VERIFICATION AUTOMATISEE : comparaison par script des commandes interdites (checkout/restore/reset --hard), de la condition et des alternatives (git status/cp/git stash) entre les 2 fichiers - plus fiable que la lecture seule.
4. DIFF MINIMAL CONFIRME : 9 insertions, 0 suppression sur 2 fichiers - la rege a ete ajoutee sans reformatage global.
5. Rapport ecrit dans themis/rapports/rapport-audit-garde-fou-restauration-2026-08-08.md (ASCII OK).

## [RAPPORT] Audit 2026-08-08 -- Piste B reparse : indices PASSE PAR LE GENERATEUR (VERDICT CONFORME)

**Objet** : audit croise de la piste B reparse par Buffy (indices generateurs-commande dans les 11 parcours), apres perte par git checkout et reparation.
**Verdict** : CONFORME -- 7/7 criteres.
**Lecons** :
1. AUDIT SANS CONFIANCE : toutes les validations Buffy (json.load, navigation, ASCII, valider-cartes) ont ete re-executees independamment - meme verdict (11/11).
2. LE COMPTAGE DES CHAMPS catalogue (C7) a change de facon ATTENDUE : 188 = 177 (piste C intacte) + 11 (piste B reparse, chaque indice generateurs-commande porte catalogue: generateurs-commande). Un compteur global qui ne tient pas compte des ajouts legitimes fausserait le verdict.
3. L ajustement morpheus (c4 creer-fichier au lieu de c6 tester-protection-*) est valide : tester-protection-* est un pseudo-outil de protocole SANS entree catalogue executable - citer un nom executable dans la commande d exemple est plus utile pour l agent.
4. La procedure d audit des patterns (spec v0.2.x) couvre bien la piste B : Pattern 3 (generateur) + Pattern 9 (LIRE AVANT USAGE) verifies sur l affichage reel.
5. Rapport ecrit dans themis/rapports/rapport-audit-piste-b-2026-08-08.md (ASCII OK).

## [RAPPORT] Audit 2026-08-08 -- Conformite 5 patterns (spec v0.2.6), suite chasse aux intentions passives

**Audit** : verifier la conformite globale des 11 parcours aux 5 patterns de la spec-guider-parcours v0.2.6, avec la PROCEDURE D AUDIT 4b (Pattern 5 -- chaine de delegation ACTIVE) fraichement documentee.
**Verdict** : CONFORME (11/11 parcours, 3 ecarts Pattern 2 CORRIGES pendant l'audit).
**Resultats par pattern** :
1. PATTERN 5 -- SCAN PASSIF : 11/11 parcours, 0 case fin avec formulation passive bloquante (te reactive / j attends / attend le retour / il me reactive / tu seras reactive) -- scan des messages de TOUTES les cases fin, 0 resultat
2. PATTERN 5 -- BOUCLE MATERIALISEE : vulcain porte la boucle complete RELAIS c9a/c15a -> RETOUR c9b/c15b -> CLOTURE c9c/c15c -> FIN c9/c15 (navigation --reponses des 2 chemins : PARCOURS TERMINE) ; athena c10 et promethee c10 portent le message RELAIS ACTIF (je ne m arrete pas en attente, la chaine continue jusqu au retour a Cerberus) ; les 8 autres parcours n ont PAS de delegation (leurs fins sont des ACTIONS finales : Reactiver Cerberus / Reactiver Vulcain / coordination terminee / signaler le besoin) -> aucune fin passive, le Pattern 5 est conforme
3. PATTERN 4 -- QUESTION HONNETE : 11/11 parcours, case_depart c0, c0 question honnete (MEMOIRE + SANS relire), branches OUI->c1 / INCERTAIN->c0b / NON->c0b, c0b RELIRE OBLIGATOIRE (lire corrections.md + fiche, suivant c1)
4. PATTERN 1 -- MULTI-MISSIONS : 11/11, case c1 Mission question avec 3 a 6 branches par parcours
5. PATTERN 2 -- RAPPEL ASCII POSITION 1 : 10/11 OK, VULCAIN 3 ECARTS DETECTES ET CORRIGES pendant l audit (c4 copier-fichier, c6 creer/ecrire-fichier, c12 editer-fichier : le rappel ASCII n etait pas en position 1, texte non uniforme REGLE IMMUABLE : ASCII strict au lieu de REGLE IMMUABLE ASCII) -> texte uniforme insere en position 1, re-verification OK
6. PATTERN 3 -- COMBO : 6 cases combo (buffy c28, janus c5/c22, themis c3, vulcain c7/c13) referencent toutes combos-moteur + definition-combo.json
7. VALIDATIONS TECHNIQUES : json.load 11/11 OK, guider-parcours --liste 11/11 charge, ASCII 0 sur les 11
**Lecons** :
1. Le Pattern 5 est la CLE de la non-coupure de chaine : une delegation sans boucle materialisee OU sans message RELAIS ACTIF cree une fin passive qui bloque l execution. La regle de la spec v0.2.6 est confirmee par l audit : sur 11 parcours, seuls les 3 qui deleguent (vulcain boucle, athena/promethee relais actif) en ont besoin -- les 8 autres se terminent par des actions finales de reactivation
2. PIEGE CRITERE D AUDIT (deja note au rapport precedent) : un test trop strict peut produire des faux ecarts -- ici le test cherchait 'memoire' en minuscules alors que la question porte 'EN MEMOIRE' en MAJUSCULES (faux ecart sur les 11) ; toujours verifier la casse et le format reel avant de conclure
3. PATTERN 2 NON UNIFORME CHEZ VULCAIN : les cases d ecriture portaient REGLE IMMUABLE : ASCII strict (ancien format) au lieu du texte uniforme REGLE IMMUABLE ASCII (spec v0.2.0) -- la procedure d audit 4b ne testait que Pattern 5, c est la procedure d audit 2 (position 1) qui a revele les 3 ecarts ; re-auditer les 5 patterns, pas seulement le nouveau
4. L audit croise confirme : la chasse aux intentions passives (Buffy) a atteint son objectif -- 0 formulation passive dans les 11 parcours, la chaine ne peut plus se couper par une fin passive

## [RAPPORT] Re-audit 2026-08-08 -- Conformite 8 patterns (spec v0.2.15) + chaine bout-en-bout

**Objet** : re-audit complet des 11 parcours apres la migration vers la CHAINE BOUT-EN-BOUT (Pattern 8, spec v0.2.15) et l'ajout des regles immuables dans les generateurs (generateurs-case v0.2.1 + generateurs-carte v0.1.1).
**Verdict** : CONFORME -- 11/11 parcours OK, 0 ecart.

**Points verifies (procedure re-audit complet v0.2.7 + 4f)** :
1. PATTERN 4 (question honnete) : 11/11 case_depart = c0, question contenant memoire + SANS relire, c0b RELIRE, c0c CONTEXTE -- OK
2. PATTERN 2 (rappel ASCII position 1) : toutes les cases d ecriture portent un indice regle ASCII en position 1 (formulation REGLE IMMUABLE ASCII ou REGLE WORKSPACE ... ASCII 2 ALTERNATIVES, spec v0.2.0) -- 11/11 OK. ATTENTION AUDIT : un detecteur trop strict exigeant le PREFIXE EXACT 'REGLE IMMUABLE ASCII' produit des faux positifs (les cases portent REGLE WORKSPACE ... ASCII 2 ALTERNATIVES, qui est le rappel ASCII en position 1) -- verifier la PRESENCE du rappel ASCII en position 1, pas le prefixe exact
3. PATTERN 7 (modele compose) : aucune decision a branche unique -- OK
4. PATTERN 5/8 (fins actives + chaine bout-en-bout) : 0 formulation passive (grep te reactive/j attends/attend le retour/il me reactive) ; la chaine outil -> tests -> controle est migree : Vulcain fins c9/c15 (MORPHEUS ACTIVE), cases RVAV c7b/c13b avant activation, Morpheus fin c10 (ACTIVE JANUS avec le rapport), Janus fin c10 (REACTIVE CERBERUS avec BILAN CONSOLIDE + RVAV c9), Cerberus c7 (flux chaine bout-en-bout) -- CONFORME
5. LE DERNIER MAILLON de la chaine (Janus) REACTIVE Cerberus avec le bilan consolide -- CONFORME (Janus c10)
6. REGLES IMMUABLES DANS LES GENERATEURS : generateurs-case v0.2.1 (garde-fou RVAV + delegation + ASCII, non bloquant) + generateurs-carte v0.1.1 (squelette c2b RVAV avant fin + rappel ASCII + fin chaine bout-en-bout) -- les prochaines cartes/cases ne naitront plus sans regles immuables

**Lecons** :
1. Le re-audit complet (regle v0.2.7) reste la seule preuve de conformite globale : 8 procedures rejouees (1, 2, 3, 4, 4b, 4d, 4e, 4f), jamais la nouvelle seule
2. L audit structurel automatique (python) est utile en PREMIERE PASSE, mais un audit croise manuel sur un echantillon (c0, c5 buffy, c12 vulcain) evite de declarer des faux ecarts sur des formulations legitimes
3. La chaine bout-en-bout (Vulcain -> Morpheus -> Janus -> Cerberus) verrouille la delegation : aucun maillon ne repasse par Cerberus au milieu, chaque maillon passe RVAV avant d activer le suivant

## [VERDICT] Audit 2026-08-08 -- Validation du diagnostic Buffy sur generateurs-commande

**Objet** : verifier le diagnostic de Buffy (outil fantome ? deconnecte de la guidance).
**Methode** : re-verification par execution reelle de chaque point (grep, comptage, lecture des definitions, git log) -- aucune confiance.

**Resultats point par point** :
1. **0 reference directe** dans les 11 parcours, demarrer.md, protocole-activation -- CONFORME (verifie par comptage reel)
2. **Usage indirect reel** : 5 combos ont des cases generateur (combo-activation 3, combo-audit-themis 2, combo-controle-modification 2, combo-corriger-ascii 1, combo-sante-tableaux 1) ; combos-moteur contient bien generateurs-commande + --reponses -- CONFORME
3. **Catalogue trop pauvre** : 13 commandes vs **89 outils reels** (comptage par dossier avec .py hors testers/spec), seulement 8/13 commandes couvrent un outil reel existant -- CONFORME dans le fond AVEC 1 CORRECTION : Buffy affirmait que valider-nommage n avait AUCUNE entree au catalogue ; or valider-nommage-recursif EXISTE (le mode simple seul est absent). Correction de precision : 6 outils quotidiens sur 7 sont absents (valider-nommage couvert uniquement en mode recursif)
4. **Contresens Buffy** : les 3 combos creer-* (creer-fichier-cerveau, creer-agent, creer-protocole) ont 0 case generateur et 3-4 commandes python3 en dur chacune -- CONFORME (comptage reel : generateur=0, outil=3-4, en dur=3-4)
5. **Chronologie** : generateurs-commande.py cree le 2026-08-07 16:07 -- CONFORME

**VERDICT GLOBAL** : CONFORME AVEC 1 CORRECTION DE PRECISION (point 3 : valider-nommage-recursif existe au catalogue ; le diagnostic reste juste dans son fond : le catalogue est largement sous-couvert). Les 4 autres points sont confirmes a l identique. Les 3 pistes de correction (enrichir le catalogue, brancher un indice generateur dans les parcours, audit anti-fantome a la creation) restent valides.

**Lecons** : (1) un comptage d outils reels doit scanner la structure reelle tools/categorie/outil/outil.py (mon premier glob tools/*/*.py a donne 0 par erreur de profondeur), (2) la verification par sous-chaine peut induire en erreur (valider-nommage matche valider-nommage-recursif) -- toujours lister le catalogue complet, (3) le diagnostic Buffy est globalement fiable : 4/5 points identiques, 1 nuance de precision.

## PHILOSOPHIE -- Principes de comportement

| **Relire sa fiche a chaque activation** | Quand je suis active ou reactive, je relis MA fiche et MES corrections avant de continuer. Je ne lis que mes fichiers, jamais ceux des autres agents : chacun lit les siens en prenant le relais. |

## [LECON] 2026-08-24 -- COMPARATIF V1 VS V2 RECREE ET MIS A JOUR (perte de livrable)

**Contexte** : mission de recree + mise a jour du comparatif v1 vs v2
(demande utilisateur) apres la perte du rapport initial (263 lignes,
valide Janus a 07:45, jamais commite, disparu du disque).

**Verdict** : rapport recree dans themis/rapports/comparatif-v1-v2-2026-08-24.md
(304 lignes, ASCII 0/0, frontmatter YAML FERME, bandeau NON NORMATIF) :
16 piliers compares (colonnes v1/v2/DECISION/RISQUE/PREUVE) + synthese
(5 piliers vitaux + 5 pieges) + conclusion. Colonne v2 ENRICHIE avec les
donnees reelles du dossier complet freelance reorganise (Atlas 2026-08-24) :
9 agents MARVEL avec grades, JARVIS v0.9.0 (~600 messages), regles M1-M7,
protocoles 1-20, tools-commun, tests Fury PASSE.

**Lecons** :
1. Un livrable JAMAIS COMMITE peut disparaitre sans trace git : les
   rapports d'analyse doivent etre commites rapidement ou re-verifies
   avant toute manipulation ulterieure.
2. Le frontmatter YAML FERME est obligatoire (lecon test-100) : tout
   .md commencant par --- doit avoir sa cloture ---.
3. Le dossier complet Atlas (atlas/rapports/freelance-2026-08-24/) est
   desormais la SOURCE DE VERITE de la v2 pour toute analyse croisee.

**Preuves** : comparatif-v1-v2-2026-08-24.md (304 lignes, ASCII 0/0) ;
frontmatter ferme ligne 9 ; dossier-complet-freelance-2026-08-24.md ;
registre themis.
## [LECON] 2026-08-24 -- DECISIONS README V2 + EDUCATION V2 (recommande)

**Contexte** : mission de trancher les 2 piliers restes A DECIDER du
comparatif v1 vs v2 (demande utilisateur 2026-08-24).

**Verdict** : recommandations produites (validation utilisateur requise) :
1. README v2 = CLIO avec EXCEPTION REDACTION V2 (deja preparee par la
   lecon Chiron 2026-08-23 : fiche EXCEPTIONS V2 + carte c22/c23
   readme-v2) -- il suffit de LANCER la mission.
2. Education v2 = ARBRES + BIBLE DES LECONS (D10 a construire) + ROGERS
   (veille regles/conventions) -- principe Chiron preserve (consulter les
   lecons avant les actions sensibles).

Comparatif mis a jour : piliers 8 et 15 passes de A DECIDER a ADAPTER,
bilan 2 garder / 14 adapter / 0 decider.

**Lecons** :
1. Quand un agent est deja PEDAGOGIQUEMENT PREPARE pour une cible
   (Clio/readme-v2), la decision la plus economique est de LANCER la
   mission preparee plutot que de changer d'agent.
2. La philosophie v2 (moins c'est plus) favorise l'apprentissage INTEGRE
   (arbres + bible) + un gardien existant (Rogers) plutot qu'un nouvel
   agent dedie.
3. Une recommandation de decision doit etre ACTIONNABLE (qui fait quoi,
   quand) pour etre validee facilement.

**Preuves** : recommandations-decisions-readme-education-2026-08-24.md
(114 lignes, ASCII 0/0, frontmatter ferme) ; comparatif mis a jour
(309 lignes) ; lecon BDD.
## [LECON] 2026-08-24 -- AUDIT CLIO README-V2 (CONFORME)

**Contexte** : audit de la mission Clio (redaction README-v2.md, decision
utilisateur 2026-08-24).

**Verdict** : CONFORME, 0 defaut.

**Lecons** :
1. L EXCEPTION REDACTION V2 fonctionne de bout en bout quand la fiche +
   la carte sont preparees (lecon Chiron respectee : la pedagogie
   precede l activation).
2. Les badges dynamiques d un README se verifient contre les sources
   RELLES (agents, modules, protocoles), pas contre le texte.
3. Le frontmatter YAML FERME est verifie a chaque audit (lecon test-100).

**Preuves** : rapport-audit-clio-readme-v2-2026-08-24.md ; README-v2.md
(189 lignes, ASCII 0/0, frontmatter ferme ligne 8) ; registre clio 9
usages ; lecon BDD.
## [LECON] 2026-08-24 -- AUDIT VERIFICATION README APRES README-V2 : CONFORME

**Contexte** : audit de la mission Clio (verification README apres la
mission readme-v2 et l'inter-round Buffy carte clio v0.6.7).

**Verdict** : CONFORME, 0 defaut.

**Points** : mettre-a-jour-readme --verifier 0 ECART (agents table OK,
badge Outils-165, readme-dev 40 categories somme 165) ; ASCII 0/0 sur
README.md et readme-dev.md ; registre clio 4 usages ; aucun fichier
modifie par la mission (verification pure).

**Lecons** :
1. Un bump de carte/fiche d agent (sans ajout ni suppression d agent ou
   d outil) ne necessite AUCUNE mise a jour du README : le --verifier
   le prouve (0 ecart).
2. Une mission de VERIFICATION ne modifie jamais le README : elle
   rapporte son etat (a jour / pas a jour).

**Preuves** : rapport-audit-clio-verification-readme-apres-readme-v2-2026-08-24.md ;
--verifier 0 ecart ; ASCII 0/0 ; registre clio 4 usages (18:00).
## [LECON] 2026-08-24 -- AUDIT SESSIONS NOMMEES (Themis)

Audit de la mission Buffy (sessions nommees admin/freelance + detection IR auto) : VERDICT CONFORME 0 defaut. Migration noyau complete et coherente : outil v0.7.0, demarrage a session explicite, encarts par session, detection IR auto, 11 outils + 6 tests alignes, registre et lecons complets, ASCII 0/0. Les echecs restants (catalogue 186 vs 187, redacteur-v2, marbre) sont pre-existants et hors perimetre.
## [LECON] 2026-08-24 -- AUDIT VERIFICATION README (Clio apres mission Atlas vues-v2) : CONFORME

Audit de la mission Clio verifier (apres education Atlas arbres v2 : carte v0.5.7 branche vues-v2, outil convertir-carte-mermaid v0.3.0 --arbres) : VERDICT CONFORME 0 defaut. mettre-a-jour-readme --verifier 0 ECART (agents table OK, badge Outils-165 OK, readme-dev 40 categories somme 165 = 165 OK). La mission n ajoute NI agent NI outil -> AUCUNE modification du README necessaire (README.md 0 diff). ASCII README 0/0. Registre Clio 5 usages. Lecon : une mission qui modifie une CARTE ou un OUTIL EXISTANT (sans ajouter agent/outil) ne change jamais le README - le --verifier a 0 ecart est le verdict attendu et Clio n a rien a corriger.
## [LECON] 2026-08-24 -- AUDIT VERIFICATION README (Clio apres mission encart 'autre' v0.7.1) : CONFORME

Audit de la mission Clio verifier (apres suppression encart 'autre' : activer-agent-principal v0.7.1, logique interne d encarts) : VERDICT CONFORME 0 defaut. mettre-a-jour-readme --verifier 0 ECART (agents table OK, badge Outils-165 OK, readme-dev 40 categories somme 165 = 165 OK). La mission modifie un OUTIL EXISTANT sans ajouter agent/outil -> AUCUNE modification du README necessaire (README.md 0 diff ; le diff readme-dev categorie Git est pre-existant). ASCII 0/0 (README, readme-dev, README-v2). Lecon : une modification de LOGIQUE INTERNE d un outil (mapping, encarts, comptage) ne change jamais le README - le --verifier a 0 ecart est le verdict attendu. Verification du perimetre : le seul diff readme-dev (categorie Git) est pre-existant et deja compte dans la somme 165.
## [LECON] 2026-08-25 -- DIAGNOSTIC MICROSECONDES 6 CHIFFRES AU LIEU DE 3 (Themis)

**Contexte** : demande utilisateur - verifier pourquoi l outil continue d ecrire les micro-secondes a 6 chiffres au lieu de 3 comme demande plus tot (fichiers v1 supposes corriges).

**VERDICT** : DIAGNOSTIC - cause racine identifiee. Le commit 4fbd28f (2026-08-25 18:41, fix Microsecondes -> millisecondes) n a corrige que les FICHIERS DE DONNEES (AGENTS-historique.md 250 lignes, variables-actuelles.md 3) mais PAS l outil qui ecrit ces timestamps : activer-agent-principal.py utilise %f (6 chiffres) a 4 endroits (lignes 876, 1033, 1305, 1364) pour ecrire AGENTS-historique.md, AGENTS.md (Sessions connues) et le classeur. Preuve chronologique : 30 min apres le commit, les activations 18:43/18:48/18:51 ont REECRIT des timestamps a 6 chiffres (.092801, .638046, .236346, .252571). Aucun %3f dans l historique git de l outil (git log -S %3f = 0).

**Verification freelance** : les fichiers actifs sont DEJA conformes (horloge.py l.23 et historique.py l.52 tronquent %f a [:12] = 3 chiffres ; les autres utilisent isoformat(timespec=seconds)). Seuls les .bak-* (sauvegardes) gardent des formats plus longs - non concernes.

**Correction proposee** : Vulcain remplace les 4 %f par %3f dans activer-agent-principal.py + parite .sh + bump version ; Hygie re-corrige les donnees (8 lignes historique + 1 AGENTS.md + classeur) ; garde-fou optionnel : test de non-regression sur absence de \.[0-9]{6} dans les entrees d historique.

**Lecon** : corriger les DONNEES sans corriger la SOURCE qui les genere = correction instantanement re-ecrasee. Le diagnostic d une regression se prouve par la CHRONOLOGIE (entrees post-commit avec le mauvais format). %f = 6 chiffres (microsecondes), %3f = 3 chiffres (millisecondes).

**Rapport** : themis/rapports/rapport-diagnostic-microsecondes-2026-08-25.md
## [LECON] 2026-08-25 -- AUDIT BRANCHEMENT AGENT CONFIDENTIEL (activer-agent-principal v0.7.4) : CONFORME (Themis)

Audit de la mission Vulcain (branchement a l activation de l agent v1 specialise freelance, CONFIDENTIEL - seul Cerberus le connait, invisible des agents v2). VERDICT CONFORME, 0 defaut.

**Verifications** : (1) ferrari present dans le dictionnaire AGENTS du .py (role + fiche + corrections) + les 3 case statements du .sh + couleur ; (2) versions 0.7.4 coherentes py/sh/md/spec ; (3) test-092 9/9 OK (EXEMPTIONS_MORTS={stark, ferrari}, KO preexistant stark resolu) ; (4) confidentialite respectee : 0 occurrence dans AGENTS.md (table + freelance/) - seule la raison transitoire du bloc session la mentionnait, nettoyee a la prochaine activation ; (5) activation reelle sur copie OK (agent activable) ; (6) ASCII 0/0, LF pur.

**Lecons** :
1. UN AGENT CONFIDENTIEL S ACTIVE MAIS NE S AFFICHE PAS : la confidentialite (invisible des agents v2) impose 3 verifications - absent d AGENTS.md, absent des docs freelance/, mais PRESENT dans le dictionnaire d activation (sinon inactivable). La raison transitoire du bloc session est le dernier endroit ou le nom peut fuiter : la nettoyer a chaque activation suivante.
2. LE GARDE-FOU DE PARITE DOIT PORTER L EXCEPTION EXPLICITEMENT : test-092 a ete adapte avec une liste d exemptions documentee (ferrari confidentiel + stark v2) - une exemption silencieuse serait un contournement, une exemption documentee est une regle.

**Preuves** : rapport morpheus/rapports/rapport-test092-ferrari-2026-08-25.md, test-092 9/9, grep ferrari AGENTS.md -> 1 (raison transitoire), freelance/ -> 0, ASCII 0/0.
## [LECON] 2026-08-29 -- AUDIT COLONNE EXECUTEUR ROUTINES : MODIFICATION CONFORME MAIS TESTS NON DELEGUES (Themis)

**Mission** : auditer la mission Vulcain (activer-agent-principal v0.8.7) - les
routines v1 affichent desormais RT(<intervalle>s) dans la colonne Executeur de
l encart v1.

**Resultats de l audit** :
1. Modification CONFORME : helper _executeur_routine (lit manifest.json),
   branche dans _ecrire_encart_v1 ET _construire_encart_v1. Test reel sur copie
   (env AGENTS_*) prouve RT(300s) dans la colonne. ASCII 0, CRLF 0, versions
   0.8.7 coherentes, 0 decalage catalogue, 0 signe outil externe, lecon+verdict
   presents. Le .sh n ecrit pas l encart (non concerne, lecon 0.7.5).
2. DEFAILLANCE PROCESSUS (1 defaut MAJEUR) : la carte de Vulcain ordonne la
   DELEGATION DES TESTS A MORPHEUS avant la fin (besoin 9 du pilote). Aucune
   mission Morpheus n a ete deposee dans les files Oracle. La chaine prevue
   (Vulcain -> Morpheus -> Janus -> Cerberus) a ete coupee : Vulcain a depose
   directement la mission Themis (audit) sans passer par les tests.

**Verdict** : A REVOIR (modification conforme, processus de fin incomplet).

**Lecons** :
1. UNE MODIFICATION PEUT ETRE PARFAITE ET LE PROCESSUS DEFAILLANT : l audit
   cible (code, ASCII, versions, test reel) est 100% vert, mais la regle
   absolue de delegation des tests (Morpheus) n a pas ete suivie. Un audit qui
   ne verifie QUE le code rate les defauts de processus.
2. VERIFIER LA DELEGATION DES TESTS DANS LES FILES, PAS DANS LE DISCOURS : la
   mission Themis elle-meme annoncait "tests deja prevus par Morpheus" - mais
   aucune mission Morpheus n existait dans les files Oracle. Toujours croiser
   les affirmations avec la realite des files (mission-lister).
3. LA FIN DE CARTE SE VERIFIE PAR LE PARCOURS DE L AGENT AUDITE : le besoin 9
   du pilote Vulcain ("Deleguer les tests a Morpheus") etait la preuve que la
   carte ordonnait cette delegation. Un agent qui passe directement de la
   modification a l audit (Themis) sans les tests viole sa carte.

**Outils utilises** : lire-activite-recente, lire-fichier, detecter-impacts,
detecter-usage-outils-externes, valider-conformite-ascii,
detecter-decalages-catalogue, combos-audit-general, consulter-lecons,
oracle (pilote/lire/acquitter/mission-lister), guider-parcours.
