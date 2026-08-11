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

## [LECON] 2026-08-09 -- AUDIT CONFORMITE D EXECUTION mission Vulcain : VERDICT NON CONFORME (c14 non execute)

**Objet** : auditer la conformite d execution de la mission Vulcain (correction divergence version generateurs-commande.sh) : l agent a-t-il fait ce que sa carte ordonnait ?

**Verdict** : NON CONFORME (1 ecart majeur). La carte de Vulcain (chemin modifier, v0.2.2) ordonne c14 DELEGUER LES TESTS A MORPHEUS apres toute modification d outil. Deroulement reel : Vulcain a fait SES PROPRES validations (parite --version, --liste, generation reelle, bash -n, ASCII, scan choix) puis a reactive Cerberus directement (08:18) sans activer Morpheus. AUCUNE activation Morpheus pour cette mission. Circonstance attenuante : correction mineure (1 ligne VERSION) + Morpheus avait deja teste l outil juste avant (08:12-08:14) ; mais c14 est une case CONTROLE obligatoire, pas une option.

**Lecons** :
1. La conformite d execution verifie le CROISEMENT mission/carte/deroulement reel, pas seulement le resultat. Un livrable de bonne qualite peut cacher un ecart de processus (ici c14 non execute).
2. Une case CONTROLE de la carte est OBLIGATOIRE : l agent ne peut pas la remplacer par ses propres validations, meme legitimes. Deleguer = activer l agent habilite.
3. Le testeur dedie (Morpheus) doit retester apres TOUTE correction d outil, meme mineure, pour que le cycle soit clos par le bon agent.
4. Distinguer dans les cartes : validations LEGERES (controle de qualite par l agent) vs validations FORMELES (deleguees au testeur) - eviter les zones grises.

**Recommandations** : 1) lancer une mission Morpheus pour retester generateurs-commande (cloture du cycle) ; 2) renforcer c14 dans le parcours Vulcain ; 3) reflechir a la distinction validations legeres/formelles dans les cartes.

**Rapport** : themis/rapports/rapport-audit-conformite-execution-vulcain-2026-08-09.md

---

## [RAPPORT] 2026-08-09 -- AUDIT CONFORMITE EXECUTION : mission 6 divergences spec/py (Vulcain)

**Question auditee** : Vulcain a-t-il aligne EXACTEMENT les 6 divergences demandees SANS toucher guider-parcours ?
**Verdict** : **CONFORME** (6/6 points verifies)

### Preuves point par point

| # | Point verifie | Preuve | Resultat |
|---|---|---|---|
| 1 | generateurs-regenerer-catalogue spec = py (1.0.0) | rescan outil : ALIGNE 1.0.0 = 1.0.0 ; dossier non suivi git = outil recent (creation mission outil durable) | OK |
| 2 | lister-agents spec = py (0.4.0-py) | git diff : `v0.2.0 -> v0.4.0-py` + ligne historique `2026-08-09 | 0.4.0-py | Vulcain | Alignement...` ; rescan ALIGNE | OK |
| 3 | lister-outils spec = py (0.3.0-py) | git diff : `v0.2.0 -> v0.3.0-py` + ligne historique datee ; rescan ALIGNE | OK |
| 4 | verifier-systeme spec = py (0.2.1-py) | git diff : `v0.2.0 -> v0.2.1-py` + ligne historique datee ; rescan ALIGNE | OK |
| 5 | combos-moteur spec = py (0.2.0-beta) | git diff : `**Version :** 0.2.0-ebauche -> 0.2.0-beta` ; rescan ALIGNE | OK |
| 6 | guider-parcours NON TOUCHEE (cas legitime) | git diff spec-guider-parcours : modifs ANTERIEURES (0.2.19 -> 0.2.20, colonne catalogue = missions precedentes Pattern 9/piste C) ; **AUCUNE ligne d alignement** ; version spec reste 0.2.20 (non alignee sur 0.3.1) ; rescan : DIVERGENT (base) = attendu | OK |

### Points complementaires verifies

| Point | Preuve | Resultat |
|---|---|---|
| Documentation cas legitime dans detecter-divergences-version.md | bloc `CAS LEGITIME ASSUME (decision Cerberus 2026-08-09)` present, explique spec patterns v0.2.x vs outil 0.3.1, NE PAS aligner | OK |
| Contenu des 5 spec intact (seules les versions changees) | git diff = uniquement lignes de version + lignes d'historique ajoutees, aucune suppression de contenu | OK |
| Aucune spec hors perimetre touchee dans CETTE mission | git status : spec-guider-parcours M = modifs anterieures (pre-existantes a la mission) ; activer-agent-principal = MISSION SEPAREE ulterieure (lignes historique) - pas celle des 6 divergences | OK |
| ASCII | 5 spec + md outil + corrections vulcain = 0 non-ASCII | OK |
| Lecons documentees (vulcain/corrections.md) | lecon `CORRECTION 6 DIVERGENCES` presente, 5 lecons detaillees (spec porte sa version a plusieurs endroits, en-tete prime, base vs suffixe, cas legitimes assumes, ASCII par fichier) | OK |

### Lecons Themis
1. Le git diff est la preuve la plus fiable de la conformite d'execution : il montre exactement QUELLES lignes ont change et lesquelles n'ont pas ete touchees (guider-parcours = modifs anterieures, pas d'alignement)
2. Distinguer les modifs PRE-EXISTANTES (missions anterieures non commitees) des modifs de LA mission auditee : un fichier M dans git status n'implique pas qu'il a ete touche dans la mission courante
3. Le rescan detecter-divergences-version + git diff se completent : l'outil valide l'etat final, le diff valide le perimetre de modification

**Verification finale** : 6/6 points CONFORMES. La mission Vulcain a aligne exactement les 5 spec + documente le cas legitime guider-parcours SANS toucher la spec-guider-parcours.

---

## [LECON] 2026-08-09 -- CRITERE REACTIVER STANDARD dans les audits de conformite d'execution

**Mission** : completer le rapport d'audit de conformite d'execution (rapport-audit-conformite-execution-vulcain-2026-08-09.md) avec le point reactiver comme critere.

**Actions realisees** :
1. Ligne c15 du tableau detaillee : `Reactivation Cerberus (08:18)` avec commande complete a 3 arguments + sortie de succes + bloc + profil classeur -> OK
2. Verdict section 4 : paragraphe `Point REACTIVER` precisant que pour CETTE mission la reactivation etait CONFORME, donc le verdict global reste NON CONFORME (1 ecart majeur c14)
3. Nouvelle section 7 `Critere REACTIVER` : definition du critere (5 points R1-R5) + verification des faits pour cette mission (5/5 CONFORME) + mise en garde (mission posterieure des 6 divergences a montre l'echec silencieux)

**Lecons** :
1. Le critere reactiver doit devenir STANDARD dans tous les audits de conformite d'execution : 5 points - R1 3e argument agent_precedent present, R2 pas d'aide affichee, R3 sortie `Session ... : Cerberus reactive avec succes`, R4 bloc AGENTS.md passe sur Cerberus, R5 profil classeur mis a jour
2. Une reactivation qui affiche l'AIDE = ECHEC SILENCIEUX (le bloc reste sur l'agent) : un agent peut croire qu'il a reactive alors que le cycle est bloque - le critere rattrape ce type d'echec
3. Distinguer la mission auditee (reactivation conforme ici) des missions posterieures (6 divergences : echec initial puis correction) - croiser AGENTS-historique pour les preuves de chaque reactivation
4. Un nouveau critere d'audit doit etre ajoute aux rapports existants pour enrichir la grille sans changer les verdicts deja etablis (verifier l'impact avant de modifier)

**Validation finale** : rapport 93 lignes, ASCII 0, section 7 complete, verdict global inchange (NON CONFORME c14) avec mention du point reactiver conforme.

---

## [LECON] 2026-08-09 -- PROCEDURE 4i OPERANTE (test reel sur mission Buffy)

**Mission** : auditer la mission Buffy de documentation du protocole (syntaxe reactiver) pour verifier que la procedure 4i enrichie (point 6 critere reactiver, spec v0.2.21) fonctionne sur un cas reel.

**Actions realisees** :
1. Procedure 4i appliquee points 1-6 sur la mission Buffy (08:54-08:55) : croisement mission/carte/deroulement reel
2. Point 6 (critere reactiver R1-R5) applique : 5/5 CONFORME (trace 08:55, sortie de succes, bloc, profil)
3. Verdict global : CONFORME
4. Rapport : themis/rapports/rapport-audit-procedure-4i-2026-08-09.md

**Lecons** :
1. La procedure 4i est OPERANTE : le point 6 s'applique sur un cas reel, les preuves sont disponibles (trace AGENTS-historique, bloc AGENTS.md, profil classeur)
2. LIMITE : la sortie reelle de la commande reactiver n'est PAS conservee dans un fichier (verifiee en direct seulement) - pour un audit A POSTERIORI, R1/R4/R5 directement verifiables (trace historique, bloc, profil), R2/R3 deduits (pas d'entree bloque + bloc passe sur Cerberus)
3. Le croisement mission/carte reste la base : la carte de Buffy (chemin modifier c9-c11-c37-c13b-c8) a ete croisee avec le deroulement reel - les cases combos (c37/c13b) non citees dans la lecon = zone grise a surveiller (meme theme que le rapport Vulcain c14)
4. Un cas de test reel est la meilleure validation d'une procedure d'audit : appliquer la procedure enrichie sur une mission reelle confirme son applicabilite AVANT de la generaliser

**Validation finale** : rapport redige (rapport-audit-procedure-4i-2026-08-09.md), verdict CONFORME, point 6 5/5, procedure 4i operante.

---

## [LECON] 2026-08-09 -- AUDIT COMPLET 11 PARCOURS : CONFORME (procedure 4i point 6 generalisee)

**Mission** : generaliser la procedure 4i (point 6 critere reactiver) a tous les parcours - re-audit integral des 11.

**Actions realisees** :
1. Validation structurelle : valider-cartes-decision --tous = 11/11 CONFORME (JSON valide, c0 question relecture, references valides)
2. Scan des patterns : P1 (11/11), P2 ASCII (10/11 - cerberus coordinateur), P4 c0 (11/11), P6 contexte (11/11), P3 combo (10/11 - cerberus), reactiver (11/11)
3. Point 6 reactiver : 6 agents actifs CONFORMES (buffy, cerberus, janus, morpheus, themis, vulcain) - 1 cas corrige (vulcain 08:44-08:48 echec silencieux documente puis corrige) ; 5 agents en attente N/A (athena, atlas, clio, minerve, promethee)
4. Verdict global : CONFORME

**Lecons** :
1. Le RE-AUDIT COMPLET (regle v0.2.7) fonctionne a l'echelle : les procedures 1-4i appliquees sur les 11 parcours donnent un etat fiable
2. Le point 6 reactiver est GENERALISABLE : preuves dans AGENTS-historique (entrees MISSION/MISSION TERMINEE) - les agents sans mission = N/A (pas un ecart, etat ATTENTE)
3. L'exception cerberus est LEGITIME et confirme le Pattern 10 (une carte = un role) : le coordinateur n'ecrit pas (P2) et ne lance pas de combos (P3)
4. Le cercle lecon -> carte -> procedure -> audit est COMPLET : l'echec reactiver vulcain a genere documentation + critere 4i point 6 + verification generalisee
5. Verifier la structure des lignes AGENTS-historique avant parsing (format : | date | session | agent | raison) - mon premier script utilisait le mauvais index

**Validation finale** : rapport themis/rapports/rapport-audit-complet-4i-11-parcours-2026-08-09.md, verdict CONFORME, ASCII 0.
## [LECON] 2026-08-09 -- AUDIT CIBLE JANUS (utilise quand il faut)

**Audit** : conformite d'execution ciblee sur Janus (controleur des statuts), meme perimetre que l'audit complet 4i des 11 parcours (procedure 4i, point 6 reactiver) + exigence utilisateur : Janus utilise QUAND IL FAUT.
**Verdict** : CONFORME.
**Lecons** :
1. Janus est branche dans le circuit de controle : carte de Cerberus c14 (Activer Janus - second controle) + c15 (Traiter le verdict de Janus) + les 3 combos de controle (controle-outil, controle-modification, controle-impacts) branches dans le parcours janus (c5/c22)
2. Janus est un CONTROLEUR qui signale sans corriger : verdict clair (VALIDE / NON VALIDE) remonte a Cerberus qui active l agent habilite pour corriger - conforme a son role
3. Les 3 controles majeurs recents (08:26 controle detecter-impacts avec verdict NON VALIDE + impact spec detecte, 08:35 scan regle des 5 fichiers avec 6 divergences, 21:46 controle generateurs-carte bout en bout) suivent SA carte avec verdicts clairs documentes dans ses corrections
4. Point 6 reactiver : chaque mission janus (08:26, 08:35, 21:46) est suivie d une entree MISSION TERMINEE sous Cerberus (R1-R5 conformes, aucun echec silencieux)
5. Le risque auto-validation (lecon Vulcain c14 : un agent qui fait ses propres validations au lieu d activer le controleur) est COUVERT par le circuit : quand un agent a valide seul, Cerberus active Janus en second controle - la procedure est en place, c est une question de declenchement par Cerberus
6. Les agents de controle (janus, themis, morpheus) doivent rester des REFERENTS INDEPENDANTS : leur activation ne doit jamais etre contournee par l agent audite - a verifier lors des prochains audits comme critere de conformite

**Validation finale** : rapport themis/rapports/rapport-audit-janus-2026-08-09.md, verdict CONFORME, ASCII 0.
## [LECON] 2026-08-09 -- AUDIT CIBLE MORPHEUS (utilise quand des tests sont necessaires)

**Audit** : conformite d'execution ciblee sur Morpheus (testeur dedie), meme perimetre que l'audit cible Janus (procedure 4i, point 6 reactiver) + exigence utilisateur : Morpheus utilise QUAND DES TESTS SONT NECESSAIRES.
**Verdict** : CONFORME.
**Lecons** :
1. Le parcours morpheus v0.1.1 (20 cases) impose un chemin tester complet : lire la doc de l outil, lire le protocole-tests, ecrire les tests avec template-test (PASSE PAR LE GENERATEUR), AJOUTER LES PROTECTIONS (c5 REGLE ABSOLUE : jamais de test sans protections - tester-protection-boucles-infinies/erreurs-silencieuses/blocage), executer, verifier et donner le verdict, documenter les lecons - retour c9 (qui m a delegue ? VULCAIN -> Activer Janus / CERBERUS -> c14)
2. La decision utilisateur du 2026-08-08 17:01 (constat 3) a acte que LES TESTS SONT LE DOMAINE DE MORPHEUS - depuis, tout test formel est delegue a Morpheus (11 missions reelles tracees)
3. Modele boucle : les agents constructeurs (Vulcain) creent/modifient, Morpheus teste formellement (valider-nommage v0.3.1, nettoyer-sessions v0.1.1, valider-cartes-decision v0.3.0, 3 combos creer-* 89/89) - chaque boucle se termine par une reactivation conforme
4. Cas historique assume : des tests ECRITS par Vulcain ont ete GARDES mais VALIDES par Morpheus (decision utilisateur) - le referent independant est preserve meme quand l ecriture est faite par le constructeur
5. Chaine bout-en-bout (21:45) : Vulcain a directement active Morpheus (Pattern 8) pour tester generateurs-carte - le canal constructeur -> testeur fonctionne sans Cerberus quand le pattern l exige
6. Point 6 reactiver : les 11 missions morpheus sont chacune suivies d une entree MISSION TERMINEE sous Cerberus (R1-R5 conformes, aucun echec silencieux)
7. Observation non bloquante : aucun combo tester-* n existe (les 15 combos sont activation/audit/controle/corriger/creer/sante/valider) - quand les suites de test deviendront repetitives, un combo tester-* (Pattern 3) encapsulera ecrire + proteger + executer
8. Les agents de controle/test (janus, themis, morpheus) restent des REFERENTS INDEPENDANTS : la validation formelle ne doit jamais etre contournee par l agent constructeur - a verifier aux prochains audits

**Validation finale** : rapport themis/rapports/rapport-audit-morpheus-2026-08-09.md, verdict CONFORME, ASCII 0.
## [LECON] 2026-08-09 -- Audit Pattern 12 CREATION LIMITEE sur les 11 parcours (procedure 4j)

**Mission** : verifier que le Pattern 12 (CREATION LIMITEE) est applique dans les 11 parcours -- toutes les cases de creation portent-elles l'indice regle ?

**Verdict** : NON CONFORME (1/11). Seul atlas v0.1.3 est conforme (pilote corrige apres l'incident du jour). 10 parcours en ecart : 21 cases de creation sans garde-fou complet (REGLE WORKSPACE en tete mais SANS les roles exclus) + 10 cases Signaler avec la mention fautive "documenter une nouvelle case dans le parcours".

**Lecons** :
1. Un nouveau pattern s'applique d'abord en PILOTE puis se generalise : l'audit d'un pattern juste documente revele TOUJOURS des ecarts sur les parcours non migres -- c'est attendu, le rapport sert de liste de travail pour la generalisation (Buffy)
2. La REGLE WORKSPACE (deja presente dans 9 parcours) est une BASE du Pattern 12 mais PAS le pattern complet : il manque les ROLES EXCLUS (outil -> Vulcain, test -> Morpheus, case -> Buffy) et le renvoi vers la case Signaler -- l'audit doit distinguer garde-fou partiel et complet
3. Le scan des cases de creation repose sur 2 criteres (outil de creation dans les indices OU titre evocateur) : certaines cases avec titre evocateur (ex: c3 Verifier la structure) n'utilisent AUCUN outil de creation -- il faut verifier les INDICES pas seulement les titres pour eviter les faux positifs
4. La mention fautive "documenter une nouvelle case dans le parcours" est un marqueur fiable : presente dans 10/11 cases Signaler (seule atlas c29 corrigee) -- un grep cible suffit pour l'audit du point 4
5. Le cas vulcain c12 (Modifier l'outil) est un CAS PARTICULIER : modifier l'outil EST son role -- le garde-fou doit l'AUTORISER (perimetre outils = Vulcain) tout en interdisant tests et cases -- le pattern n'interdit pas la creation, il la borne au role
6. Verification croisee obligatoire : un echantillon manuel (buffy c25, athena c20) confirme que le scan JSON dit la verite avant de figer le verdict
## [LECON] 2026-08-09 -- AUDIT PATTERN 13 (LA FIN SUIT SA CARTE) : VERDICT CONFORME

**Controle** : conformite de la nouvelle regle la fin suit SA carte (Pattern 13, spec v0.2.23) dans les 11 parcours - les fins actives sont-elles conformes au Pattern 8 (chaine bout-en-bout) ?

**Verdict** : CONFORME (36 fins analysees, 5 fins actives, 0 anomalie).

**Lecons** :
1. Le Pattern 13 se verifie par la procedure 4k en 4 points : fin attendue par la carte, coherence fin/type d'activation, aucune fin de maillon qui reactive Cerberus au milieu, absence de l'ancienne regle dans les documents de coordination (grep cible)
2. La typologie des fins est maintenant stable : FIN - Reactiver Cerberus (activation directe), FIN - Activer <maillon> (chaine, message actif), FIN - Delegation (modele generique morpheus c17/janus c30), Signaler le besoin (Pattern 12, signalement). Les 11 parcours utilisent tous cette typologie - un greppage de la structure suffit a cartographier l'ecosysteme
3. Les fins actives de la chaine Vulcain->Morpheus->Janus->Cerberus sont conformes : c9/c15 (Vulcain active Morpheus), c10 (Morpheus active Janus), c10 (Janus reactive Cerberus avec bilan consolide). La chaine Athena->Promethee->Minerve (athena c10, promethee c10) et le FLUX Promethee->Minerve sont aussi actives
4. Les fins Reactiver Cerberus restantes correspondent toutes a des activations directes ou au dernier maillon avec bilan consolide (janus c10) : aucune incoherence
5. Point de vigilance cosmetique : les titres des fins actives portent des suffixes heterogenes (CHAIN/FLUX pour athena/promethee, sans suffixe pour morpheus/vulcain) - non bloquant, a uniformiser eventuellement
6. Verification croisee : naviguer les fins actives (athena c10, promethee c10, morpheus c10 via c9->VULCAIN) confirme le PARCOURS TERMINE avec le message actif - le scan JSON dit la verite
7. Le rapport doit etre ASCII 0 : verifier avec valider-conformite-ascii apres ecriture (3 accents 'e' ont ete corriges - coherence/Cosmetique)
## [LECON] 2026-08-09 -- DIAGNOSTIC COUVERTURE CRITERES 1-21 DANS LE PARCOURS THEMIS

**Contexte** : la carte d'audit themis v0.2.5 (23 cases) a 3 cases dediees aux criteres d'execution : c8b (critere 22, Pattern 11), c8c (critere 25, Pattern 14), c8d (critere 24, Pattern 13). Question : quels criteres 1-21 n'ont PAS de case dediee ?

**Verdict** : AUCUN critere 1-21 n'a de case dediee dans le parcours themis. Ce n'est PAS une anomalie : ces criteres sont STRUCTURELS (qualite de l'outil guider-parcours et des cartes), verifies par les tests formels Morpheus et les outils du combo audit-themis (c3) -- ils ne jugent pas le comportement de l'agent. Seuls les criteres d'EXECUTION (juger ce que l'agent a fait) meritent des cases dediees.

**Tableau de couverture (25 criteres)** :
| Critere | Nature | Case dediee | Couverture reelle |
|---|---|---|---|
| 1 (affiche cases) | structurel outil | NON | tests Morpheus (tester-guider-parcours) |
| 2 (branches) | structurel outil | NON | tests Morpheus |
| 3 (reponse inconnue) | structurel outil | NON | tests Morpheus |
| 4 (mode --reponses) | structurel outil | NON | tests Morpheus |
| 5 (mode --liste) | structurel outil | NON | tests Morpheus |
| 6 (JSON invalide) | structurel outil | NON | tests Morpheus |
| 7 (parite py/sh) | structurel outil | NON | tests Morpheus + detecter-divergences-version |
| 8 (ASCII strict) | structurel | NON | combo audit-themis (valider-conformite-ascii) |
| 9 (indice regle en tete) | structurel (Pattern 2) | NON | audit (procedure 2 rejouee) |
| 10 (case Mission) | structurel (Pattern 1) | NON | valider-cartes-decision |
| 11 (combo reference) | structurel (Pattern 3) | NON | audit (verification combos) |
| 12 (c0 + c0b) | structurel (Pattern 4) | NON | valider-cartes-decision |
| 13 (fin passive) | structurel (Pattern 5) | NON | combo audit-themis (detecteur fin passive) |
| 14 (re-audit 14 patterns) | structurel | NON | procedure 4c relue en debut d'audit |
| 15 (c0c contexte) | structurel (Pattern 6) | NON | valider-cartes-decision |
| 16 (mode non-bloquant) | structurel (v0.2.9) | NON | tests Morpheus |
| 17 (generateurs-case) | structurel (v0.2.12) | NON | audit (verification outil de reference) |
| 18 (case compose 2 branches) | structurel (Pattern 7) | NON | valider-cartes-decision |
| 19 (chaine bout-en-bout) | structurel (Pattern 8) | NON | audit (procedure 4i) |
| 20 (lire .md avant usage) | structurel (Pattern 9) | NON | audit (procedure 4g) |
| 21 (une carte = un role) | structurel (Pattern 10) | NON | audit (procedure 4j) |
| 22 (conformite d execution) | EXECUTION (Pattern 11) | OUI c8b | case dediee |
| 23 (creation limitee) | structurel (Pattern 12) | NON | audit (verification des cases de creation) |
| 24 (la fin suit SA carte) | EXECUTION (Pattern 13) | OUI c8d | case dediee |
| 25 (verification d impact) | EXECUTION (Pattern 14) | OUI c8c | case dediee |

**Lecons** :
1. La distinction STRUCTUREL vs EXECUTION est le critere de decision : seuls les criteres qui jugent le COMPORTEMENT de l'agent pendant SA mission (22, 24, 25) ont besoin d'une case dediee dans la carte de Themis. Les criteres 1-21 jugent la QUALITE des livrables (outil, cartes) -- ils sont verifies par les outils/tests, pas par une case.
2. Le critere 23 (CREATION LIMITEE, Pattern 12) n'a pas de case dediee mais est structurel : il est verifie par l'audit des cases de creation (indice regle en tete) -- pas besoin de case dediee.
3. La couverture reelle des criteres 1-21 repose sur 3 piliers : (a) tests formels Morpheus (criteres 1-7, 16), (b) combo audit-themis en c3 (criteres 8, 13, et structure globale), (c) procedures d'audit 1-4l rejouees integralement (criteres 9-21, 23 via procedure 4c RE-AUDIT COMPLET).
4. Risque residuel : si Morpheus ne teste pas guider-parcours ou si le combo audit-themis n'est pas lance, les criteres 1-7 et 16 ne sont couverts par RIEN. Le re-audit complet (procedure 4c) reste le filet de securite.
## [LECON] 2026-08-09 -- RE-AUDIT COMPLET DES 14 PATTERNS (11 parcours) : 65 ECARTS P2/P12

**Contexte** : mission Cerberus (decision utilisateur) : re-audit integral de la procedure 4c (spec-guider-parcours v0.2.25) sur les 11 parcours. La spec contient desormais 14 patterns (le Pattern 14 verification d impact a ete ajoute apres les 13).

**Verdict** : NON CONFORME a 100 % -- 10 parcours sur 11 portent des ecarts sur 2 patterns :
- P2 (rappel ASCII position 1) : 28 ecarts -- la procedure 2 exige que le PREMIER indice des cases d'ecriture soit REGLE IMMUABLE ASCII. Les ajouts recents (piste B PASSE PAR LE GENERATEUR, REGLE WORKSPACE, CREATION LIMITEE) ont ete inseres en position 1, repoussant l ASCII en position 2+. Seul cerberus est conforme.
- P12 (CREATION LIMITEE) : 37 ecarts -- les cases de creation/documentation ne portent pas l indice regle CREATION LIMITEE (perimetre + roles exclus). Les cases Lecons et retour comptent comme cases de documentation (procedure 4j). Atlas est partiellement conforme (c9/c18/c19/c25 ont le garde-fou).
- P14 (verification d impact) : 1 ecart -- vulcain.md plus ancien que parcours-vulcain.json (identification non mise a jour).

**Conformes 11/11** : P1 multi-missions, P3 combos, P4 question honnete, P5 fins actives (0 passive), P6 contexte temps reel, P7 modele compose, P8 chaine bout-en-bout, P9 lire le .md (guider v0.3.1, 0 vrai manquant), P10 une carte = un role (valider-cartes-decision 11/11), P11 conformite d execution (c8b), P13 la fin suit SA carte (c8d). ASCII 0, CRLF 0.

**Lecons** :
1. LA PROCEDURE 2 EST STRUCTURELLE, PAS TEXTUELLE : une regle ASCII PRESENTE en position 2+ ne suffit pas -- la position 1 (premier indice) doit ETRE REGLE IMMUABLE ASCII. Les ajouts recents (piste B, workspace) ont silencieusement viole cette regle en inserant leurs regles en tete.
2. VERIFIER LES AJOUTS RECENTS : chaque fois qu une piste insere un indice (PASSE PAR LE GENERATEUR, REGLE WORKSPACE, CREATION LIMITEE), il faut verifier qu elle ne deplace pas une regle structurelle de position 1.
3. NE PAS LAISSER DE POLLUTION D AUDIT : mes scripts .tmp-* d audit ont fait remonter 185 documents manquants dans verifier-documents-manquants (faux positifs) -- nettoyer les .tmp AVANT de relancer les outils de verification.
4. LES FINS ACTIVES : la navigation --reponses 'OUI' s arrete a la question Mission (MODE AGENT NON-BLOQUANT, comportement attendu) -- la preuve de navigation bout-en-bout vient des tests formels (test-005) et de valider-cartes-decision, pas d un chemin OUI simple.
5. LE PATTERN 12 COMPTE LES CASES LECONS : les cases Lecons et retour (retour dans corrections.md) sont des cases de documentation au sens de la procedure 4j -- elles doivent porter le garde-fou.
6. ACTIONS RECOMMANDEES : deplacement de l ASCII en position 1 (via generateurs-case, critere 17), ajout du garde-fou CREATION LIMITEE (modele = atlas c9/c18/c19/c25), maj identification vulcain.md, puis re-audit 4c.
## [LECON] 2026-08-09 -- RE-AUDIT 4c v2 : CONFORME 11/11 apres corrections P2/P12/P14

**Mission** : re-audit complet 4c de confirmation (spec-guider-parcours v0.2.25) apres les corrections Buffy (P2 : 28 cases position ASCII, P12 : 37 garde-fous CREATION LIMITEE) et Vulcain (P14 : identification vulcain.md).

**Verdict** : CONFORME 11/11 parcours, 0 ecart structurel restant. Les 65 ecarts du precedent re-audit sont tous corriges (P2 28->0, P12 37->0, P14 1->0).

**Methodes** :
1. Diagnostic code avant audit : quand l utilisateur signale un probleme de blocage, VERIFIER d abord par execution reelle (JSON valide, guider-parcours --liste, navigation --reponses, valider-cartes-decision, ASCII/EOL) avant de conclure a un bug. Ici le code n etait PAS casse : 11/11 JSON valides, 11/11 CONFORME, navigation propre. La cause des arrets etait un comportement d execution (arret de tour apres activation), pas une regression des cartes.
2. Audit structurel par script Python : P2/P12 scanne les cases d ecriture (position 1 ASCII + garde-fou CREATION LIMITEE), P5 compte les fins passives, P8 verifie les references suivant/branches, P4 verifie la question honnete c0.
3. Les combos (P3) sont references via des indices fichier/outil avec mention combo dans le texte, pas un type combo dedie : le scan type=='combo' sous-compte, il faut chercher dans nom+texte.
4. P10 : valider-cartes-decision est l outil de reference (11/11 CONFORME), le controle structurel cerberus-outils=14 n est pas un ecart (outils de coordination : activer-agent-principal, guider-parcours).
5. Les rapports Themis dans themis/rapports/ ont leur propre convention de nommage (pas de prefixe themis-) : valider-nommage les signale en faux positif, coherent avec le rapport v1 existant.

**Livrables** : rapport-audit-complet-14-patterns-11-parcours-2026-08-09-v2.md (ASCII 0, LF pur).
## [LECON] 2026-08-09 -- AUDIT CONFORMITE D'EXECUTION P14 : 5/6 points conformes, lacune de carte

**Mission** : auditer (Pattern 11, procedure 4i) si l'execution reelle de la mission P14 (mise a jour identification vulcain.md) a suivi la carte de Vulcain.

**Verdict** : 5/6 points conformes (relecture, Pattern 9 lire le .md, Pattern 14 verification d'impact, RVAV, POINT 6 REACTIVER conforme). 1 ecart : lacune de carte -- le parcours-vulcain v0.2.8 n'a AUCUNE case pour les missions de mise a jour de documentation/fiche (les 3 chemins sont construire/modifier/hors-parcours->signaler). L'agent a du devier de sa carte pour accomplir une mission legitime que la carte ne couvre pas.

**Lecons** :
1. LA CONFORMITE D'EXECUTION PEUT REVELER DES LACUNES DE CARTE : quand l'execution reelle est correcte mais qu'aucune case ne correspond au type de mission, l'ecart est STRUCTUREL (la carte), pas une faute de l'agent. Le Pattern 11 ne doit pas conclure 'conforme' pour une mission que la carte ne couvre pas -- il doit signaler la lacune.
2. VERIFIER PAR NAVIGATION REELLE : pour savoir ce que la carte ordonne, lancer guider-parcours --case c1 --reponses pour tracer le chemin complet (ici 'autre' -> c16 -> NON -> c18 'Signaler le besoin' qui ordonne de ne rien faire). Ne jamais supposer le contenu d'une case.
3. LE POINT 6 REACTIVER SE PROUVE PAR REUSSITE : la commande reactiver exige le 3e argument agent_precedent -- son echec produit 'ERREUR: Parametres manquants'. Une reussite dans la trace AGENTS-historique est la preuve que la syntaxe etait bonne.
4. VERIFIER LES ACCENTS AVANT DE CONCLURE : les guillemets francais << >> (0xAB/0xBB) ne sont PAS couverts par corriger-accents-zones-sensibles (dictionnaire d'accents seulement) -- les remplacer par des guillemets simples et revalider (lecon : corriger par l'outil, puis si l'outil ne couvre pas le caractere, reecrire en ASCII strict).
5. Les missions de documentation (mise a jour de fiche/corrections) sont un type de mission commun a tous les agents : la lacune de carte est probablement partagee (vulcain, buffy, atlas) -- a verifier au prochain audit 4c.

**Livrables** : rapport-audit-conformite-execution-p14-2026-08-09.md (ASCII 0, LF pur).
## [LECON] 2026-08-09 -- AUDIT PISTES MIROIRS THEMIS (verdict CONFORME)

**Audit** : conformite des pistes miroirs audit generalisees par Buffy (9 demandeurs + themis, Pattern 10 + livrable avec retour, 11 parcours).

**Verdict** : CONFORME -- 0 ecart bloquant, 0 fichier suspect lie a la mission. Rapport : rapport-audit-pistes-miroirs-themis-2026-08-09.md.

**Lecons** :
1. LE PATTERN 10 SE VERIFIE DANS LE CONTENU DES INDICES : la simple presence d'une branche `audit` ne suffit pas - il faut verifier que la case Activer porte bien la regle << ROLE DE THEMIS - je n audite JAMAIS moi-meme >> et la CREATION LIMITEE. Ici 9/9 demandeurs conformes + themis c25 (executant) avec ASCII + CREATION LIMITEE doc + RVAV + combo.
2. LE LIVRABLE AVEC RETOUR SE PROUVE PAR LE MESSAGE DE LA FIN : la fin doit dire REACTIVE + fournir le rapport (pas une fin passive). Ici 10/10 fins conformes (9 retours demandeur + c25b reactiver agent precedent).
3. detecter-usage-outils-externes ne prend QU UNE SEULE cible : en multi-cibles il echoue avec << unrecognized arguments >> - utiliser --recursive sur le dossier pour scanner plusieurs fichiers, puis verifier les fichiers suspects un par un.
4. LES DICTIONNAIRES DE CARACTERES SPECIAUX (corriger-dictionnaire-accents.txt, dictionnaire-emojis.txt) SONT DES SUSPECTS LEGITIMES : ils contiennent des caracteres non-ASCII PAR CONCEPTION (c'est leur fonction de les corriger). Toujours verifier l identite du fichier suspect avant de conclure - hors perimetre de la mission auditee.
5. CONFIRMATION de la lecon precedente : les guillemets francais << >> (0xAB/0xBB) ne sont PAS couverts par corriger-accents-zones-sensibles - remplacer par des guillemets ASCII et revalider (outil d'abord, puis reecriture ASCII stricte).
## [LECON] 2026-08-09 -- AUDIT CONFORMITE EXECUTION : GARDE-FOU REGENERATEUR (VULCAIN)

**Audit** : mission Vulcain 'garde-fou cles dupliquees au regenerateur du catalogue'.
**Verdict** : CONFORME (1 point mineur non fonctionnel : commentaire stale ligne 318).
**Lecons** :
1. VERIFIER LE CODE ET LE FONCTIONNEL, PAS LES LECONS : l'audit doit refaire les tests
   (positif/negatif) de facon independante, pas se fier au bilan de l'agent audite.
2. UN COMMENTAIRE STALE EST UN ECART D'EXECUTION : la ligne 318 ('puis reecrire CRLF')
   contredit l'ecriture LF nouvelle - quand on change un comportement, balayer les
   commentaires inline qui le decrivent (pas seulement le docstring).
3. LE MOT CRLF DANS UN COMMENTAIRE N'EST PAS UNE ECRITURE CRLF : ne pas flagger le mot
   - verifier l'ABSENCE d'ecriture (variable resultat_crlf, replace \r\n en ecriture).
4. POINT 6 REACTIVER : verifier dans AGENTS-historique l'entree de reactivation + le
   retour effectif de la session a l'agent precedent (avant l'activation de l'auditrice).
5. LA FIN SUIT SA CARTE : l'auditrice reactive l'agent precedent AVEC son rapport (c25b).
## [LECON] 2026-08-09 -- AUDIT SPEC-REFONTE : VERDICT CONFORME (1 point mineur)

**Mission** : etape 1 du plan de refonte - auditer la spec-refonte-cartes-decision
(v0.1.0, Promethee) pour valider le concept AVANT de lancer l implementation.

**Verdict** : CONFORME avec 1 point mineur (concept valide pour l'implementation).

**Rapport** : `themis/rapports/rapport-audit-spec-refonte-cartes-decision-2026-08-09.md`

**Points verifies (independamment)** :
1. Faits cites tous verifies (buffy 49 cases/45 Ko, atlas 40, vulcain 32,
   cerberus 28 ; spec-guider-parcours v0.2.23 a 15 patterns ; generateurs-case
   v0.2.2 ; generateurs-carte v0.2.0)
2. Vision utilisateur citee verbatim + traduite fidelement
3. Contrat validateur-case complet (structure, modele, surcharge > 3 indices /
   160 car., references, verdict CONFORME / A ALLEGER / NON CONFORME)
4. Plan 7 etapes coherent + chaine obligatoire Vulcain -> Morpheus -> Janus
5. Criteres d'acceptation verifiables (6)
6. Normes : ASCII 0, LF pur, frontmatter, index-spec a jour
7. Conformite d'execution : Promethee a reactive Cerberus (trace historique)

**Point mineur (non bloquant)** : le type `action` (tableau 4.1) presente comme
"inchange" n existe pas dans le modele actuel - guider-parcours ne gere que
fin/indice/question-controle et aucun des 11 parcours ne contient de case
action. A clarifier dans la spec (retirer OU declarer type nouveau a
implementer a l etape 5).

**Lecons** :
1. Un audit de spec RE-VERIFIE chaque fait cite (tailles, versions, nombres)
   - aucun ne s est revele faux ici (fiabilite de la spec prouvee).
2. Croiser TOUJOURS le modele propose avec l outil d execution (guider-parcours)
   ET les donnees reelles (les 11 parcours) : un type lister sans verification
   d existence cree un ecart silencieux.
3. Faux positif de mon propre script (apostrophe) : ne jamais conclure sur un
   KO sans verifier le contexte exact.

## [LECON] 2026-08-09 -- AUDIT CONFORMITE DELEGATION DES TESTS (parcours-vulcain v0.2.12)

**Contexte** : audit demande par l'utilisateur (via Cerberus) : verifier que le
renforcement v0.2.12 applique bien le pattern *interdiction au point d'action +
verification en 2 points au controle*.

**VERDICT : CONFORME avec 1 point mineur non bloquant** (rapport dans
themis/rapports/rapport-audit-conformite-delegation-tests-vulcain-2026-08-09.md).

**Points verifies (7/7 conformes)** :
1. c6 + c12 : regle ABSOLUE DELEGATION DES TESTS en position 1 (test-XXX,
   creation OU mise a jour, meme adaptation mineure).
2. c6 + c12 : ambiguite "5 fichiers (dont test)" supprimee -> "4 fichiers de
   l outil (py sh md spec) + test-XXX ECRIT PAR MORPHEUS".
3. c8 + c14 : question en 2 points (Morpheus ECRIT et EXECUTE + aucun fichier
   de test touche par Vulcain) + regle VERIFICATION EN 2 POINTS.
4. vulcain.md : Pattern 14 v0.2.12 + regle fiche renforcee.
5. Lecon Buffy documentee (point d'action vs controle tardif).
6. Integrite : JSON, valider-case, navigation 2 chemins, ASCII 0, LF pur.

**Point mineur (non bloquant)** : les regles ajoutees en c8/c14 font 341
caracteres (> 160) -> A ALLEGER. Proposition : deplacer vers une reference
(protocole-tests) ou raccourcir.

**Lecons** :
1. Le pattern *interdiction au point d'action + verification en 2 points au
   controle* est bien materialise : la correction structurelle de la recidive
   est effective.
2. Supprimer l'ambiguite est aussi important que la regle elle-meme : une
   contradiction residuelle autorise toujours la derive.
3. Regles ABSOLUE > 160 caracteres = A ALLEGER : privilegier la reference vers
   un fichier de regles commun.
4. Faux positif de mon script (apostrophe) : toujours verifier le contexte
   avant de conclure un KO.

## [LECON] 2026-08-10 -- AUDIT CONFORMITE GLOBALE : VERDICT CONFORME 23/23 (migration + vcd v0.3.1 + mentions stale)

**Mission** : auditer 3 perimetres : (1) migration des 11 parcours au format action, (2) valider-cartes-decision v0.3.1 (type action ajoute), (3) mentions stale de versions corrigees (generateurs-case.md, generateurs-carte.md).

**Resultats** : 23/23 controles OK - VERDICT CONFORME. Audit independant (script dedie 23 points + combo audit-themis + suite d outils) : 11 parcours format action + versions exactes + ASCII/LF, vcd 11/11 + test 24/24, mentions stale corrigees + refs d introduction conservees, conformite d execution (chaine Vulcain->Morpheus->Janus->Cerberus tracee), verification d impact Pattern 14 (aucun impact oublie reel).

**Lecons** :
1. detecter-impacts signale des fichiers NON MIS A JOUR qui ne sont PAS des impacts : les lecons historiques, les rapports dates et les fiches qui CITENT un outil sans version sont des citations, pas des impacts - il faut verifier le contenu avant de conclure
2. evaluer-coherence a repere 15 liens casses dans conventions/index-conventions.md (liens relatifs inexacts) - PRE-EXISTANT depuis le commit initial, hors perimetre de la migration mais a traiter (Buffy, responsable du cerveau-projet)
3. Un audit global croise 3 sources : script dedie (structure), combo audit-themis (suite croisee), detecter-impacts (impact) - la triangulation confirme le verdict
4. Le type action est maintenant pleinement integre : code (generateurs-case.py), validateur (valider-cartes-decision v0.3.1), documentation (2 .md a v0.5.0) - plus aucune liste de types sans action dans le cerveau

## [LECON] 2026-08-10 -- AUDIT CHAINE COMPLETE BUFFY -> JANUS -> THEMIS : VERDICT CONFORME 21/21

**Mission** : auditer le travail de Buffy (creation des 2 protocoles dedies +
branchement protocole-controle-buffy dans parcours-janus v0.3.1) en
appliquant le protocole-audit-buffy (E1-E9) - cas reel de la chaine complete
et du critere reactiver (branche audit-agent c25/c25b).

**Resultats** : 21/21 CONFORME (apres correction du critere E7c). Toutes les
etapes E1-E9 conformes : carte Buffy respectee, lecons au format, impact
verifie, fin suit SA carte, reactiver R1-R5 valide, qualite documentaire
(ASCII 0, LF, tableaux), parcours v0.3.1 + cartes 11/11, aucun motif parasite.

**Lecons** :
1. LE PROTOCOLE-AUDIT-BUFFY EST OPERATIONNEL : applique en reel sur un cas
   de chaine, avec le critere reactiver teste (Janus m a activee, je le
   reactive avec mon rapport). La chaine Buffy -> Janus -> Themis -> retour
   fonctionne bout en bout
2. PIEGE E7c : detecter-divergences-version affiche 1 DIVERGENTE + 2 SANS
   VERSION - compter les occurrences du mot divergence (2) est un faux
   negatif. Le bon critere : utiliser la SYNTHESE de l outil (21 spec : 18
   alignees, 1 divergente, 2 sans version) et verifier si la divergence est
   preexistante (git status vide sur l outil = hors perimetre)
3. OBSERVATION HORS PERIMETRE : divergence preexistante guider-parcours
   (spec 0.5.0 vs py 0.4.0) a signaler a Cerberus pour correction par Vulcain
4. La separation des responsabilites est confirmee : Janus controle (15/15),
   Themis audite (21/21) - les 2 protocoles dedies fonctionnent et se
   completent

## [LECON] 2026-08-10 -- AUDIT REACTIVER/ACTIVER : 2 CASES FAUSSES IDENTIFIEES (atlas c31b, themis c25b)

**Mission** : auditer pourquoi des cases et mentions induisent encore les
agents en erreur sur la reactivation, alors que la philosophie a change
(l agent active l agent suivant dans SA carte, Pattern 13, sans repasser par
Cerberus entre les maillons).

**Resultats** : cause racine identifiee. L outil reactiver ramene TOUJOURS a
Cerberus (fonction reactiver_cerberus - c est sa conception). Les 2 cases qui
disent "REACTIVER L AGENT PRECEDENT" (atlas c31b, themis c25b) donnent la
commande reactiver - incoherence directe entre le texte et la commande : elles
ramenent a Cerberus au lieu de l agent precedent. La bonne commande est
`activer <session> <agent_precedent> <raison>` (l action activer accepte n
importe quel agent). Sur 37 fins mentionnant Cerberus, seules 2 sont fausses.

**Lecons** :
1. LA COMMANDE REACTIVER NE RAMENE QU A CERBERUS : c est une conception de
   l outil (fonction reactiver_cerberus). Pour revenir a un agent precedent
   (maillon de chaine), utiliser ACTIVER avec le nom de l agent - jamais
   reactiver
2. UNE CASE PEUT DONNER UNE COMMANDE FAUSSE : le texte ("reactiver l agent
   precedent") et la commande (reactiver -> Cerberus) peuvent se contredire.
   L audit doit verifier le COUPLE texte+commande, pas seulement le texte
3. LE PATTERN 13 N EST PAS PROPAGE : il est dans la spec-guider-parcours mais
   le protocole-activation decrit encore le cycle simple CERBERUS -> AGENT ->
   CERBERUS. La regle de decision (qui m a active ?) manque dans les cartes
4. SEULEMENT 2 CASES FAUSSES SUR 37 : l audit a ete chirurgical - pas besoin
   de tout reecrire, juste corriger les 2 cas + propager la regle dans le
   protocole-activation
## [LECON] 2026-08-10 -- AUDIT CONFORMITE NON-REGRESSION : VERDICT CONFORME 29/29 (Themis)

**Mission** : audit de conformite globale (tests reverdis test-013/test-016, garde-fou test-018, protocole-tests v0.2.2).

**Verdict** : CONFORME (29/29).

**Lecons** :
1. **La REGLE IMMUABLE de delegation a ete respectee** : seul Morpheus a touche aux fichiers de test (adaptation de version incluse) -- l'audit confirme qu'aucun autre agent n'est passe par-dessus le protocole-tests v0.2.2.
2. **Les versions attendues des tests doivent etre verifiees apres chaque evolution de parcours** : la divergence etait purement cosmetique (compteurs de types deja alignes, seule la version n'avait pas ete bumpee) -- un scan des versions attendues de tous les tests (test-009 a test-018) apres chaque refonte de parcours eviterait ces KO preexistants.
3. **Le couple test-018 + protocole-tests v0.2.2 est un verrou complet** : le test verifie les fins (Pattern 13, anti-regression reactiver), le protocole impose de le re-executer apres toute modification de fin -- les deux se renforcent.
4. **Distinguer version historique et version courante dans les tests** : les mentions historiques (docstring) doivent etre conservees, seule la verification courante change -- l'adaptation chirurgicale de Morpheus est le bon modele.
## [LECON] 2026-08-10 -- AUDIT SANTE E5 FICHE JANUS vs CARTE v0.3.3 (Themis, VERDICT A REVOIR)

**Mission** : etape 3 - audit documentaire du protocole sante E5b sur la fiche janus apres l'allegement (carte v0.3.3, Pattern 16).

**Verdict** : A REVOIR (2 points).

**Lecons** :
1. Pattern 14 viole : la fiche janus dit `PARCOURS (v0.3.2)` (ligne 76) alors que la carte est v0.3.3. Apres toute mise a jour de version de parcours, la fiche doit etre synchronisee (le protocole sante E5 detecte automatiquement cette divergence).
2. E5b viole : la fiche formule le sens des fins (reactiver Cerberus, dernier maillon) mais ne cite AUCUN identifiant cX reel des fins de la carte v0.3.3 (c10, c29, c29d, c30, c32). La lecon du re-audit est explicite : "Une mention textuelle sans identifiant reel est INSUFFISANTE".
3. PIEGE PERSONNEL : dans mon script d'audit, j'ai cherche les mauvaises fins (c14/c16d/c17/c19 de la version precedente) - la carte v0.3.3 a evolue (fins reelles : c10 Reactiver Cerberus, c29 Signaler, c29d Outil temporaire, c30 Delegation, c32 Retour de Themis). TOUJOURS lire les fins reelles du parcours AVANT de croiser.
4. Moi-meme j'ai ecrit 12 non-ASCII (guillemets francais " " + accents) dans mon rapport - corriges via reecriture ASCII strict. Lecon : rediger directement en ASCII (le corriger-accents-zones-sensibles conserve les accents francais par conception "zones sensibles", il ne remplace pas " ").
5. Correction confiee a Buffy (responsable des fichiers du cerveau) : mise a jour v0.3.3 + citation des fins cX.
## [LECON] 2026-08-10 -- RE-AUDIT E5b FICHE JANUS CORRIGEE (Themis, VERDICT VALIDE 10/10)

**Mission** : re-audit du protocole sante E5 sur la fiche janus corrigee (apres correction Buffy + controle Janus).

**Verdict** : VALIDE 10/10 - les 2 points de l'audit precedent (Pattern 14 + E5b) sont resorbes.

**Lecons** :
1. Le cycle complet detecter -> corriger -> controler -> RE-AUDITER fonctionne : l'audit initial A REVOIR (2 KO), correction par Buffy, controle croise Janus 14/14, puis re-audit Themis 10/10 VALIDE.
2. E5b est maintenant conforme : les 5 fins reelles de la carte v0.3.3 (c10, c29, c29d, c30, c32) sont citees par identifiant dans la fiche - le croisement fiche/parcours passe KO -> OK.
3. Pattern 14 conforme : fiche PARCOURS (v0.3.3) == carte v0.3.3.
4. Bonus applique pendant la correction : Pattern 8 -> Pattern 13 aligne dans la fiche (ma recommandation precedente).
5. Le rapport d'audit a ete mis a jour avec le verdict final (A REVOIR -> VALIDE, date de correction) - un rapport d'audit n'est jamais fige, il documente l'evolution.
## [LECON] 2026-08-10 -- AUDIT POST-MIGRATION (Themis, VERDICT A REVOIR : 5 points doc + 1 test)

**Mission** : audit complet post-migration des 8 parcours du groupe cerveau-projet (v0.3.x).

**Verdict** : A REVOIR - 5 points documentaires (Pattern 14 + E5b) + 1 test a adapter (test-014).

**Lecons** :
1. PATTERN 14 VULCAIN STALE : la fiche vulcain ligne 60 dit PARCOURS (v0.5.0) mais la carte est v0.3.0 - la version 0.5.0 vient de l'HISTORIQUE DE LA FICHE (version de fiche confondue avec version de parcours). Piege : verifier la REGLE ABSOLUE PARCOURS, pas seulement la ligne "Parcours" du haut de fiche.
2. E5b non uniforme : seules atlas, clio, janus, morpheus citent leurs fins cX. buffy, cerberus, themis, vulcain (migres PLUS TOT) n'ont pas ete enrichis - la lecon E5b a ete appliquee seulement aux fiches touchees apres sa creation. Il faut une PASSE GLOBALE E5b sur les fiches du cerveau-projet.
3. TEST-014 OBSOLETE : le test attend v0.5.0 de la spec-guider-parcours et 15 patterns, mais la spec est en v0.6.0 avec 16 patterns (Pattern 16 ALLEGEMENT ajoute par Buffy). Les tests doivent etre rescanne apres CHAQUE bump de version de spec (regle RE-SCAN COMPLET).
4. NON-REGRESSION : 10/11 tests verts, seule l'adaptation de versions attendues est necessaire (pas de regression fonctionnelle). La suite test-009 a test-019 est fiable et reproductible.
5. Correction confiee a Buffy (5 points doc) + Morpheus (test-014) - roles distincts.

## [LECON] 2026-08-10 -- RE-AUDIT POST-MIGRATION : A REVOIR -> VALIDE (Themis)

**Mission** : re-audit de confirmation du rapport d'audit post-migration (5 points doc + test-014).
**Verdict** : 13/13 OK, passage A REVOIR -> VALIDE.

**Verifications** :
1. P1 vulcain Pattern 14 : fiche PARCOURS (v0.3.0) == carte 0.3.0, 0 reste v0.5.0
2. P2 E5b : bloc FINS REELLES cX present et conforme sur buffy (9), cerberus (2), themis (5), vulcain (7)
3. P3 test-014 : 12 OK / 0 KO (versions v0.6.0 + 16 patterns)
4. P4 spec : titre v0.6.0 + Version 0.6.0 + 16 patterns coherents
5. P5 refs documentaires v0.6.0 (guider-parcours.md + vulcain.md Spec du format)
6. P6 normes : ASCII 0 + LF pur sur les 5 fichiers modifies

**Lecons** :
1. Le format de sortie du test-014 est `=== RESULTAT : X OK / Y KO (sur N points) ===` - extraire avec cette regex, pas `X/Y`
2. La version JSON de parcours est sans prefixe v (0.3.3) vs fiche avec v (v0.3.3) - normaliser pour comparer
3. Mettre a jour le rapport d'audit avec la mention explicite du re-audit et de l'evolution (un rapport documente l'evolution, il n'est jamais fige) - garder le verdict initial dans le titre (A REVOIR -> VALIDE)
4. Verifier les normes (ASCII strict + LF pur) apres mise a jour du rapport

## [LECON] 2026-08-10 -- AUDIT COHERENCE README POST-MAJ (Themis, VERDICT A REVOIR : 1 ecart reel + 2 mineurs)
1. Le --maj de mettre-a-jour-readme corrige la table et le titre mais PAS l'arborescence commentee : le total 83 residuel (ligne 54) a survecu a la grosse MAJ (119). TOUJOURS scanner les anciens totaux dans TOUT le fichier, pas seulement les compteurs de table.
2. Les badges shields sont TOUS sur une ligne unique (ligne 9 = 6 badges) : un grep par ligne les manque - compter les occurrences de "img.shields.io/badge/" dans la ligne, pas les lignes.
3. Categorie VIRTUELLE templates=1 : pas de dossier physique (outil-template.md a la racine tools/) - le comptage manuel doit l'ajouter pour concordance (118 + 1 = 119).
4. Une ligne d'arborescence avec un ancien total (83) est la preuve la plus rapide d'une MAJ incomplette - ajouter au protocole de relecture README.
5. Outils utilises : combos-analyse-projet, mettre-a-jour-readme --verifier, valider-liens, valider-conformite-ascii, comptage manuel independant.

## [LECON] 2026-08-10 -- RE-AUDIT COHERENCE README : A REVOIR -> VALIDE (Themis)
1. Les 3 points resorbes par Clio (P6 83->119, P7 protections Tester, P8 Activer en tete + reordonnancement) sont confirmes par re-audit.
2. PIEGE de re-audit : les separateurs de table '|---|---|---|' sont MULTIPLES dans le README (table des piliers, des agents, des outils) - un script qui cherche le premier separateur attrape celui d'une AUTRE table. TOUJOURS localiser l'en-tete '| Categorie |' PUIS le separateur juste apres.
3. Le reordonnancement automatique d'une table peut ECRASER l'en-tete + separateur si le script remplace le bloc a partir de la ligne d'en-tete : la verification P8 (en-tete present + Activer en tete) l'a detecte et l'en-tete a ete restaure - la verification croisee de structure (pas seulement du contenu) est indispensable apres un tri.
4. Sources de verite : combos-analyse-projet + mettre-a-jour-readme --verifier = 0 KO (hors __pycache__) confirment la coherence finale.

## [LECON] 2026-08-10 -- AUDIT CONFORMITE GLOBALE PATTERN 17 (Themis, VERDICT CONFORME)

**Contexte** : audit de conformite apres la generalisation du Pattern 17 aux 11 parcours + corrections Buffy + validation Morpheus.
**Verdict** : CONFORME (7 points, 1 KO preexistant test-007 hors perimetre).
**Lecons** :
1. Verifier un pattern generalise case par case : les 12 flux P17 (11 parcours + vulcain x2) doivent porter Xb/Xc/Xd/Xe avec les 3 corrections (regles <= 160, sans commande en dur, Xb sans suivant)
2. Le Pattern 13 (la fin suit SA carte) se verifie par la branche NON de Xb : elle doit pointer vers la fin qui EXISTAIT avant l insertion, jamais reactiver Cerberus par defaut
3. Le Pattern 14 se verifie par croisement fiche vs carte : PARCOURS (vX) dans la fiche == version dans parcours-*.json
4. Attention aux faux negatifs de valider-case : clio (c6b/c6c) et themis (c3) ont des elements a alleger PREE XISTANTS - verifier que les cases P17 elles-memes sont conformes (0 a alleger)
5. Le test-007-figer-lf est un KO preexistant (catalogue 109 attendu, 118 actuel) - a traiter par une mission RE-SCAN ulterieure, hors perimetre P17
## [LECON] 2026-08-10 -- CARTE THEMIS CASSEE : SUIVANT MORT REDONDANT (Themis)

**Constat** : la carte themis a des champs suivant MORTS qui explosent la structure :
1. Questions avec suivant redondant (deja dans leurs branches) : c21, c8, c8b, c8c - le suivant n est jamais lu (les branches priment dans guider-parcours) mais le cartographe le compte -> 210 chemins pour 32 cases (atlas sain : 44 cases / 45 chemins)
2. Fin avec suivant : c23 (Signaler le besoin -> c23c) - la navigation s arrete a la fin, le suivant est un residu trompeur
**Ampleur** : defaut GENERALISE sur 10 parcours (cerberus seul sain) : 14 cases a corriger (10 questions + 4 fins) - athena c18/c20, atlas c26/c29, buffy c10b/c33/c35/c35d, clio c13/c15, janus c27/c29, minerve c18/c20, morpheus c13/c16, promethee c18/c20, themis c21/c23/c8/c8b/c8c, vulcain c16/c18.
**Lecons** :
1. Le champ suivant sur une case qui A des branches est un DEFECT (suivant mort) - il doit etre retire, pas conserve
2. Une fin ne doit JAMAIS avoir de suivant (residu trompeur)
3. Le cartographe (nb chemins) est un excellent detecteur : 210 chemins pour 32 cases = anomalie flagrante (ratio ~1:1 attendu, ex atlas 44/45)
4. valider-cartes-decision ne detecte PAS ce defaut (references valides mais logique morte) - renforcer le validateur pour detecter suivant redondant avec branches + fin avec suivant
**Correction recommandee** : retirer le champ suivant des 14 cases concernees (la navigation reelle utilise deja les branches), verifier avec valider-cartes-decision --tous + cartographe (ratio chemins/cases normal) + non-regression.
