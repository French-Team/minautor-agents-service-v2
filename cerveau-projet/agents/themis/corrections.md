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
## [LECON] 2026-08-11 -- AUDIT PATTERN 14 COMPLET : TRIO SANS BLOC FINS (Themis, VERDICT A REVOIR)

**Mission** : auditer la conformite globale du Pattern 14 (volets principal REGLE ABSOLUE PARCOURS vX + secondaire bloc FINS REELLES + lien Parcours vX) sur les 11 fiches, apres la correction Buffy du 2026-08-11.

**Verdict** : A REVOIR -- 1 ecart reel.

**Constat** :
- P1 (REGLE ABSOLUE vX) : CONFORME 11/11 -- la correction Buffy est efficace.
- P2 (bloc FINS REELLES version + fins) : CONFORME sur les 8 fiches qui l'ont (y compris cT6..cT10 de janus et les cXe du Pattern 17).
- **P2b (ECART) : le TRIO (athena, minerve, promethee) n'a AUCUN bloc FINS REELLES** -- aucune fin reelle cX citee dans leurs fiches, alors que le protocole-sante E5b exige le croisement fiche/parcours (lecon du re-audit 2026-08-10). Leurs 6 fins reelles (c9e, c10, c20, c20d, c21, c23, v0.2.4) ne sont nulle part.
- P3 (lien Parcours vX) : CONFORME 11/11. P4 (mentions stale) : CONFORME. P5 (normes) : CONFORME 0/0. P6 (valider-cartes 11/11 + test-018 13/13 + test-021 9/9) : CONFORME.

**Lecons** :
1. Le bloc FINS REELLES etait absent du trio depuis la migration v0.2.4 -- le protocole-sante E5b doit etre RENFORCE pour exiger le bloc sur TOUTES les fiches (pas seulement celles qui en ont deja un).
2. Les IDs cT* (ligne trio) : les regex de scan doivent etre `[a-zA-Z]*\d+[a-z]*` (lettre MAJUSCULE au milieu) -- les regex `[a-z]?` creent des faux negatifs.
3. Recommandation : Buffy ajoute le bloc FINS REELLES sur les 3 fiches du trio (format des 8 autres).
## [LECON] 2026-08-11 -- AUDIT CONVENTION cT* : VERDICT A REVOIR (ecarts documentaires generateurs-ligne) (Themis)

**Contexte** : audit de conformite globale de la convention de nommage etendue cT* (valider-case v1.0.2, spec-guider-parcours v0.6.2 regle 11, generateurs-ligne v0.3.1, generateurs-case v0.4.1, tests 009/014/015 reverdis).

**Lecon** :
1. La chaine FONCTIONNELLE est conforme (validation, documentation principale, generation, garde-fous positifs, non-regression 21/21, 0 NOMMAGE sur janus) mais le SCAN ANTI-RECURRENCE revele 3 ecarts DOCUMENTAIRES mineurs, tous dans la famille generateurs-ligne : .md ligne 197, spec (4 lignes : 93/126/153/169), commentaires .py (3 endroits : 275/419-422/460) citent encore l'ancienne convention c<numero>[a-z]? sans l'extension cT*. Un audit qui ne scanne que les fichiers modifies rate les mentions restantes dans les specs/commentaires voisins.
2. Faux positifs a connaitre : les mentions c<numero>[a-z]? dans test-017 sont LEGITIMES (le test verifie les ids GENERES par l'outil, qui ne produit que des cas normaux -- c'est une verification de comportement, pas une documentation de convention). Un scan P4 doit exclure les tests qui verifient la generation.
3. L'historique de spec-guider-parcours est une ligne unique de ~100 000 caracteres : une recherche dans les 2000 premiers caracteres apres **Historique** donne un FAUX NEGATIF -- toujours chercher dans TOUTE la ligne (str.find sur toute la chaine).
4. L'audit structurel doit croiser 4 sources (validateur, spec, generateurs, tests) : la documentation etait alignee sur les fichiers principaux mais pas sur les 3 fichiers satellites de generateurs-ligne.
## [LECON] 2026-08-11 -- RE-AUDIT cT* : A REVOIR -> VALIDE (E1/E2/E3 resorbes, 14/14 OK) (Themis)

**Contexte** : re-audit cible de la convention cT* apres la correction Vulcain des 3 ecarts documentaires (E1 generateurs-ligne.md:197, E2 spec-generateurs-ligne 4 lignes, E3 generateurs-ligne.py 3 commentaires -- 8 mentions de l'ancienne convention sans l'extension cT*).

**Lecon** :
1. Le re-audit cible (R1-R5) sur les seuls ecarts precedents est suffisant quand la correction est documentee et verifiee par l'agent : 14/14 OK, verdict final VALIDE ajoute au rapport existant (mise a jour, pas de nouveau rapport).
2. Le scan anti-recurrence par CONTEXTE (fenetre +/- 2 lignes contenant c[<prefixe-alpha-maj>] ou cT1..cT10) distingue proprement les mentions du cas normal COMME PARTIE de la convention etendue (conformes) des mentions isolees (ecarts) : c'est la bonne methode pour verifier une convention etendue.
3. Le code n'a pas change (commentaires uniquement) : la non-regression (test-010, test-017, compile py) est la preuve que la correction est sans impact fonctionnel.
4. Verdict final : la convention cT* est desormais documentee de facon coherente sur TOUTE la chaine (validateur -> spec -> generateurs .md/spec/code -> tests).
## [LECON] 2026-08-11 -- SECOND CONTROLE DE MA PROPRE CARTE v0.3.7 : PISTE c12f/c12g CONFORME (Themis, VERDICT VALIDE)

**Contexte** : apres l'ajout par Buffy de la piste 'defaut signale -> activer l'agent habilite' (c12f question + c12g action, modele Janus c9f/c9g + boucle KO ligne trio cT8-cT10, fin c12e reutilisee), controle croise de ma propre carte.

**Points controles** :
1. FORMAT : c12 (suivant c12f), c12f (question + branches OUI->c12g / NON->c12b), c12g (action, indices regle + outil, suivant c12e), c12e (fin reutilisee sans duplication). 34 refs resolues, 0 reference morte, 0 suivant mort.
2. NAVIGATION : 3 flux OK (defaut signale, pas de defaut, auto-amelioration).
3. PATTERN 12 : c12g ne cree AUCUN fichier (regle + outil uniquement) -- l'agent habilite cree son propre rapport.
4. PATTERN 14 : fiche v0.3.7, plus de v0.3.6, 6 fins reelles toutes citees dans le bloc FINS REELLES (c12e, c13, c23, c23d, c24, c25b).
5. NORMES : 0 non-ASCII, 0 CRLF sur parcours + fiche + rapport.
6. NON-REGRESSION : 21/21 OK.

**Lecons** :
1. Le modele de piste 'defaut signale' est desormais present chez les DEUX agents de controle (Janus c9f/c9g et Themis c12f/c12g) -- meme structure, identifiants adaptes, fin de reprise reutilisee.
2. Controleur sa propre carte est legitime quand la modification a ete faite par un autre agent (Buffy) -- le controle croise reste independant (regle de relecture + protocole de controle).
3. Un rapport qui designe un coupable declenche maintenant l'activation immediate de l'agent habilite chez Themis comme chez Janus.

## [LECON] 2026-08-13 -- AUDIT REGISTRE vs CARTES : 15 LACUNES + 1 REFERENCE MORTE (Themis)

**Mission** : auditer le registre des usages (courant 21 lignes + historique 75) pour verifier que tous les outils reellement utilises sont assignes aux cartes (demande utilisateur).

**Resultat** : rapport themis/rapports/audit-registre-cartes-2026-08-13.md - 1 reference morte (verifier-cartes-decision, typo janus), 15 usages legitimes hors carte (janus 4, morpheus 4, vulcain 6), Cerberus 0 correction (derives corrigees par test-034).

**Lecons** :
1. L AUDIT MANUEL COMPLET REVELE PLUS QUE LE SCAN AUTO : evaluer-processus (registre courant seul) donne 0 probleme mais l historique (75 lignes, archive par la non-regression) contient les usages anciens - lire les DEUX sources pour un audit complet.
2. QUALIFIER AVANT DE CORRIGER : les ecarts de Cerberus (tester-lancer-non-regression, generateurs-*) sont des DERIVES CORRIGEES - les re-assigner annulerait test-034. Un ecart n est pas toujours une lacune : il faut lire le contexte de la declaration.
3. UNE REFERENCE MORTE DANS LE REGISTRE EST UNE DETTE SILENCIEUSE : verifier-cartes-decision (typo de valider-cartes-decision) pointe vers un outil inexistant - le registre doit pointer vers des outils reels, sinon les audits croises sont fausses.
4. LE WILDCARD NE MATCHE PAS LE NOM REEL : la carte morpheus reference tester-protection-* mais l outil s appelle tester-protections - un nom d outil doit etre EXACT dans les indices, pas un pattern approximatif.


## [LECON] 2026-08-13 -- AUDIT MISSION MORPHEUS AXE D THEMIS (Themis, VERDICT VALIDE)

**Controle** (mission Morpheus, maillon automatique axe D) : verification T1-T4
de l adaptation des 5 tests de version. RESULTAT : VALIDE - versions exactes
(test-004 morpheus 0.4.4, test-016 buffy 0.4.2 action 40 controle 5, test-005
atlas 0.4.2 residus c30+c11a, test-006 48 cases, test-017 contrat outil 7x),
compteurs egaux au parcours reel, normes 0/0, non-regression 36/36 OK.
LE CON INFIRMEE : le KO test-024 lors de l audit etait un artefact (script
.tmp-audit lance depuis la racine) - relance propre = 36/36.
FIN : rapport themis/rapports/audit-morpheus-tests-axe-d-2026-08-13.md + reactiver
JANUS pour le controle croise final.


## [LECON] 2026-08-13 -- AUDIT TEST-037 SEUL JANUS NON-REGRESSION (Themis, VERDICT VALIDE)

**Controle** (mission Morpheus, maillon automatique) : T1-T5 verts - test-037
couvre les invariants (seul janus, regle fiche, identite contenu, 10 cartes,
normes), cartes corrigees coherentes (seul janus garde l outil), integration
serie d OK, normes 0/0. LE CON : distinguer construction (ids partages par le
trio = meme structure voulue) et identite (contenu toujours distinct) lors des
verifications d unicite des parcours. Rapport : themis/rapports/audit-test-037-
2026-08-13.md. FIN : activer JANUS pour le controle croise final.


## [LECON] 2026-08-13 -- AUDIT ANTI-ARTEFACT TEST-024 (Themis, VERDICT VALIDE)

**Controle** (mission Morpheus, maillon automatique) : T1-T4 verts - code
portable (os.getppid + /proc + powershell fallback, fallback = aucune
exclusion), protection intacte (un vrai residu non exclu reste KO), normes
0/0, integration reelle OK (parent unique exclu -> serie d 15/15 OK).
LE CON : le scan d un garde-fou doit distinguer le script temporaire EN COURS
D EXECUTION (parent direct, orchestrateur legitime) d un RESIDU (plus utilise
par aucun processus) - le parent est la signature fiable, tout le reste est
detecte. Rapport : themis/rapports/audit-anti-artefact-test024-2026-08-13.md.
FIN : activer JANUS pour le controle croise final.
## [LECON] 2026-08-13 -- AUDIT BADGE README AUTO (Themis, VERDICT VALIDE)

**Audit** de la mission badge header : combo massive v0.1.1 (aligner_badge_header
via importlib, source de verite compter_outils) + garde-fou test-038
(synchronisation affichage + href du badge). T1-T5 verts : aucun ecart.

**Verification cle** : aligner_badge_header sur README sain retourne False
(aucune fausse correction - important pour le mode conservatif) et la preuve
negative du test-038 (href desynchronise) detecte bien le KO.

**Lecon** : un correctif automatique doit etre verifie dans les 2 sens :
rien a faire (idempotence) ET correction effective (desynchronisation).
## [LECON] 2026-08-13 -- AUDIT BADGES HEADER GENERALISES (Themis, VERDICT VALIDE)

**Audit** de la mission badges : combo massive v0.1.2 (aligner_badges_header :
Outils via compter_outils, Version via clio/version-readme.txt, Statut via
clio/statut-projet.txt, badges statiques href-alignes) + garde-fous
test-038 etendu (7 points) et test-039 (residus de version a la racine).
T1-T5 verts : aucun ecart.

**Verification cle** : les sources de verite de version/statut vivent dans
cerveau-projet/agents/clio/ (jamais a la racine - les fichiers 0.2.1/v0.2.6
etaient des residus accidentels de redirections).

**Lecon** : une synchronisation de badges est complete quand chaque badge
dynamique a UNE source de verite nommee et que les garde-fous verifient
affichage ET href (2 occurrences par badge).
## [LECON] 2026-08-13 -- AUDIT CATALOGUE-INDEX (Themis, VERDICT VALIDE)

**Audit** de la mission catalogue-index : Buffy a indexe les 137 outils du
catalogue (4 outils reels + section Tests 39) avec stats recalculees
(total 118 -> 166, le total etait faux depuis longtemps) ; Morpheus a cree
test-040 (script + doc + index). T1-T5 verts : aucun ecart.

**Verification cle** : le badge README (128) compte les dossiers reels
(compter_outils) et non les lignes d index - il reste inchange quand l index
gagne des lignes. Deux compteurs differents a ne pas confondre.

**Lecon** : le total de l index-tools etait obselete (outils ajoutes sans
mise a jour des stats) - le garde-fou test-040 detecte les manques de
script/doc/index, et test-007 verifie le total des stats.

## [LECON] 2026-08-13 -- CONTROLE CROISE NON-REGRESSION 5 SERIES (Themis, VERDICT VALIDE)

**Audit** (mission Morpheus, apres Buffy) : passage de 4 a 5 series dans
tester-lancer-non-regression.py. Verification T1-T5 : 5/5 verts.
- T1 : les 2 copies du lanceur modifiees a l identique (5 cles SERIES,
  SERIES_ORDRE a-e, choices 6 valeurs) - la copie 2 (avec __main__ final)
  est celle executee, la coherence des 2 est indispensable
- T2 : doc md a jour (tableau 5 series + option --series <a,b,c,d,e,tous>)
- T3 : test-027 11/11 sans modification (couverture + doublons + test-027
  en serie D) - l invariant du decoupage reste vert
- T5 : aucune reference residuelle a|b|c|d ou "4 series" dans l ecosysteme
  (index-tools, README, catalogue)

**Lecon durable** : un changement de structure (decoupage en series) doit
etre verifie dans les 2 sens : le code (2 copies identiques) ET la doc
associee (tableau + options), avec le garde-fou qui protege la structure
(test-027) passe sans modification.

## [LECON] 2026-08-13 -- CONTROLE CROISE PATTERN VERSION README CLIO (Themis, VERDICT VALIDE)

**Audit** (mission Morpheus, apres Buffy) : documentation de la convention de
bump de version dans clio.md v0.2.1. T1-T5 : 5/5 verts.
- T1 : section PATTERN VERSION README complete (sources de verite exactes,
  regle de bump MINEUR/MAJEUR, lien aligner_badges_header, garde-fous
  test-038/039, anti-residus fichiers de version a la racine)
- T2 : version fiche 0.2.1 (frontmatter + tableau) - plus de 0.2.0
- T3 : verifier-conformite-fiche CONFORME - la section specifique est
  TOLEREE (non bloquante)
- T5 : parcours clio intact + sources version/statut intactes (0.2.0 / stable)

**Lecon durable** : documenter une convention de maintenance dans la fiche
de l'agent responsable (section specifique toleree) ne touche NI au parcours
NI aux sources - la verification cible (conformite + garde-fous badges)
suffit a valider. La convention transforme une source de verite technique
en comportement reel de l'agent.

## [LECON] 2026-08-13 -- CONTROLE CROISE BUMP VERSION COMBO MASSIVE (Themis, VERDICT VALIDE)

**Audit** (mission Morpheus, apres Buffy) : combos-maj-readme-massive v0.1.3
bumpe la version du README quand le contenu change. T1-T5 : 5/5 verts.
- T1 : bumper_version (increment MINEUR X.Y.Z -> X.(Y+1).0) + lire_version +
  snapshot du README + bump AVANT aligner_badges_header (le badge Version
  s aligne sur la nouvelle version)
- T2 : rapport complet (etape 3b + synthese console + Contexte fichier)
- T4 : version-readme.txt reel intact (0.2.0) - le bump est CONDITIONNEL
  (README modifie), pas d inflation de version sur un projet a jour

**Lecon durable** : la source de verite de version doit etre bumpee par
L OUTIL qui modifie le contenu (pas seulement par l agent) - et le bump doit
preceder l alignement des badges pour eviter un badge obsolette. Le rapport
est la preuve visible : il montre ancienne -> nouvelle quand le README change,
et "inchangee" quand rien n a bouge.

## [LECON] 2026-08-13 -- AUDIT GARDE-FOU ANTI-RESIDUS v0.5.2 (Themis, VERDICT VALIDE)

**Audit** : garde-fou anti-residus de activer-agent-principal (v0.5.2, Buffy +
verifications Morpheus). 24/24 OK : presence py+sh + declenchement actions reelles,
preuve positive/negative sandbox, section doc, versions 0.5.2 partout, normes 0/0,
test-007 22/22, test-039 4/4, registre a jour.

**Lecon** : la double protection (garde-fou proactif dans l outil au point d entree +
garde-fou reactif test-039 dans la suite) est la bonne reponse a une classe d accident
dont la cause est dans la COMMANDE D APPEL (impossible a corriger dans le code de
l outil). Quand la cause racine est externe, on protege le point d entree.

## [LECON] 2026-08-13 -- AUDIT GARDE-FOU ETENDU 3 OUTILS (Themis, VERDICT VALIDE)

**Audit** : extension du garde-fou anti-residus a guider-parcours (v0.5.1),
valider-cartes-decision (v0.4.1), editer-parcours (v0.1.1). 25/25 OK : garde-fou
present + preuve sandbox, versions partout (py/sh/doc/spec), tests 012/024/028
verts, normes 0/0, catalogue et parcours intacts.

**Lecon** : l ARTEFACT D AUTO-INCRIMINATION de test-024 s est reproduit une 3e
fois : lancer test-024 depuis un script .tmp-*.py a la racine = KO (le garde-fou
detecte le script qui le lance). C est devenu un reflexe : TOUJOURS lancer test-024
en commande directe, jamais depuis un script temporaire. Un audit qui lance les
garde-fous depuis son propre script temporaire s auto-incrimine.

## [LECON] 2026-08-13 -- AUDIT TEST-041 + LANCEUR DEDOUBLE (Themis, VERDICT VALIDE)

**Audit** (mission Morpheus, demande utilisateur) : test-041 garde-fou outils critiques anti-residus + reparation du lanceur dedouble. 13/13 VALIDE.

**Observation** : la reparation du lanceur (669 lignes, 1 bloc SERIES) est saine. Le garde-fou test-041 verifie bien la presence de verifier_residus_racine dans les 4 outils critiques (activer, guider, valider, editer).

**Lecon recurrente confirmee** : l artefact d auto-incrimination de test-024 (lancer le garde-fou depuis un script temporaire .tmp-*.py a la racine -> KO auto-inflige) s est reproduit. Reflexe documente : TOUJOURS lancer test-024 en commande directe depuis un bash sans residu.

## [LECON] 2026-08-13 -- AUDIT REGLE ANTI-ECHAPPEMENT JSON (Themis, VERDICT VALIDE)

**Audit** (mission Buffy, demande utilisateur) : regle anti-echappement JSON documentee dans protocole-creation-scripts-temporaires v0.2.0. 9/9 VALIDE.

**Observation** : la regle d or (TOUTE commande complexe = script temporaire via write_file, jamais inline) et le piege test-024 auto-incrimination sont maintenant formels. Les dizaines d erreurs JSON passees ne devraient plus se reproduire.

## [LECON] 2026-08-13 -- AUDIT REGLE ANTI-ECHAPPEMENT COMBOS (Themis, VERDICT VALIDE)

**Audit** (mission Buffy, demande utilisateur) : regle anti-echappement etendue aux commandes bash des combos. 12/12 VALIDE.

**Observation** : le piege (interpolation brute {var} + shlex.split -> apostrophe casse la commande) est maintenant documente dans la doc du moteur ET le protocole. Les 52 commandes actuelles sont propres, la regle protege le futur.

## [LECON] 2026-08-13 -- AUDIT TEST-042 COMBOS-VARIABLES-QUOTEES (Themis, VERDICT VALIDE)

**Audit** (mission Morpheus, demande utilisateur) : garde-fou test-042 + correction 8 commandes. 9/9 VALIDE.

**Observation** : la distinction cle (commande = exactement {var} -> ne pas quoter, vs argument {var} -> quoter) est formalisee dans le test. Les 22 commandes entieres generees restent intactes, les 8 arguments sont corriges.

## [LECON] 2026-08-13 -- AUDIT PREUVES APOSTROPHE COMBOS (Themis, VERDICT VALIDE)

**Audit** (mission Morpheus, demande utilisateur) : preuves reelles du quoting des combos avec raison a apostrophe. 8/8 VALIDE.

**Observations** :
- Le quoting fonctionne : la raison 'reprise d activation de la mission' traverse generateur + shlex.split + execution intacte.
- Sans quoting, la commande echoue en 'No closing quotation' AVANT execution - preuve que le garde-fou test-042 est necessaire.
- La sortie d une case outil est capturee silencieusement par combos-moteur : utiliser --verbose pour la verifier.

## [LECON] 2026-08-13 -- AUDIT TEST-043 GENERATEURS-QUOTER (Themis, VERDICT VALIDE)

**Audit** (mission Morpheus, demande utilisateur) : garde-fou test-043 generateurs-quoter. 12/12 VALIDE.

**Observation** : la chaine d echappement est maintenant surveillee sur ses DEUX maillons : test-042 cote combos (definitions-combo.json) et test-043 cote catalogue (parametres quoter:true de generateurs-commande). Un retrait du champ quoter ou une regression de composer_valeur serait signale a la non-regression.
## [LECON] 2026-08-13 -- AUDIT MISSION TRIPLE CHRONO/REGLE/SCRIPTS (Themis, VERDICT VALIDE)

**Controle croise** (mission Buffy, demande utilisateur) : 20/20 points OK.
V1) versions/sections presentes (template v0.3.0, protocole-tests v0.3.1,
Regle 9, outil-template-python v0.1.1-beta, protocole scripts v0.2.2) ;
V2) canevas complet (point_actif/chrono_etape/bilan_chrono) + outil-template.py
compile avec --chrono ; V3) normes 0/0 sur les 7 fichiers + lecon ;
V4) 0 residu racine (commande directe - l artefact d auto-incrimination est
recurrent quand un audit lance lui-meme le scan) ; V5) references coherentes.

**Lecons** :
- Le triplet protections + options on/off + chrono est desormais la REGLE
  IMMUABLE de creation de tout fichier (fonctions/tests/workflows) : il se
  propage par les templates (test v0.3.0 + outil v0.1.1-beta) et les
  protocoles (tests v0.3.1 + outils Regle 9). Les futures mesures de duree
  alimenteront les outils de suivi.
- La contradiction scripts temporaires est levee : jetable ephemere racine
  (rm -f immediat) vs outil temporaire de mission (generateur + registre).
- Chaque audit Themis qui scanne la racine DOIT confirmer T4 en commande
  directe (artefact d auto-incrimination recurrent).
## [LECON] 2026-08-13 -- AUDIT TEST-044 TRIPLET TEMPLATE (Themis, VERDICT VALIDE)

**Controle croise** (mission Morpheus, demande utilisateur) : 15/15 points OK.
test-044-triplet-template : 14/14 (positif), preuve negative rejouee (perte
de bilan_chrono detectee, restauration identique), serie e + DUREES, 1 bloc
SERIES, conformite 029 (44 tests) + 030, normes 0/0, correction du template
(global NB en tete de main du canevas) verifiee.

**Lecons** :
- Le triplet du template est desormais SURVEILLE en permanence : un futur
  template appauvri serait signale a la non-regression. Le garde-fou a
  prouve sa valeur des la creation en revelant le bug latent du canevas
  (UnboundLocalError NB_KO).
- La regle de creation de fichier (protections + options on/off + chrono)
  s applique aussi aux GARDE-FOUS eux-memes : test-044 est le premier test
  qui affiche un bilan CHRONO.
## [LECON] 2026-08-13 -- AUDIT REGLE STRICTE SCRIPTS DEDIES (Themis, VERDICT VALIDE)

**Controle croise** (mission Buffy, demande utilisateur) : 15/15 points OK.
Protocole v0.2.3 : regle stricte (JAMAIS de script temporaire a la racine),
aucune tolerance residuelle, dossier dedie .agents-tmp/ partout (deux usages +
spawn_agents + procedure + pieges + RVAV) ; .gitignore a jour ; test-024
13/13 (dossier invisible pour le scan racine) ; test-039/041 verts ; normes 0/0.

**Lecons** :
- La nouvelle pratique est EN PLACE et SURVEILLABLE : racine 0 .tmp en
  permanence (test-024), .agents-tmp/ vide en fin de mission. Tous les
  agents (moi comprise) utilisent .agents-tmp/ desormais.
- L artefact d audit s est deplace dans .agents-tmp/ : un audit qui scanne
  .agents-tmp/ doit se verifier en commande directe apres suppression de son
  propre script (meme lecon que pour la racine).
## [LECON] 2026-08-13 -- AUDIT RETOUR REGLE D ORIGINE + RESIDUS EN CASCADE (Themis, VERDICT VALIDE)

**Controle croise** (mission Buffy -> Morpheus, demande utilisateur) : 15/15
points OK apres re-audit. Protocole v0.2.4 (regle d origine : dossier
tmp-<agent>/ cree a la racine, rm -rf en fin de mission), 0 mention
.agents-tmp, test-024 point 2b (0 dossier tmp-* residuel hors agent courant),
gitignore tmp-*/, .agents-tmp/ supprime, conformite 029/030, normes 0/0.

**Decouverte majeure** : le garde-fou 2b a detecte DEUX residus reels en
cascade : tmp-buffy (Buffy a active Morpheus sans supprimer son dossier) puis
tmp-morpheus (Morpheus a active Themis sans supprimer son dossier). LA
DISCIPLINE n est pas encore automatique chez les agents : la regle exige
rm -rf tmp-<agent> AVANT de reactiver l agent suivant. Le garde-fou protege
la regle, mais chaque agent doit l appliquer - y compris Themis (qui a du
supprimer tmp-morpheus pendant son propre audit).

**Lecons** :
- Un garde-fou qui protege une regle d usage DOIT exclure l usage courant
  legitime (agent courant via le profil classeur) sinon il s auto-incrimine
  pendant les missions.
- La verification des residus se fait en commande directe, apres suppression
  du dossier de l agent courant : l audit Themis a du re-auditer apres
  suppression de tmp-morpheus.
- Passer la main (activer l agent suivant) SANS supprimer son dossier
  temporaire = anomalie detectee par test-024. La chaine entiere applique
  desormais la regle.

## [LECON] 2026-08-13 -- AUDIT DE LA CHAINE HYGIE (Themis, VERDICT VALIDE)

**Contexte** : audit croise de la creation de l agent de nettoyage Hygie
(fiche + parcours + chariot + test-045).

**Points cles** :
- 18/18 au premier passage + T6 confirme apres suppression du dossier
  tmp-themis (artefact d auto-incrimination classique : mon propre dossier
  de mission present pendant le scan).
- RESIDUS REELS DECOUVERTS : les dossiers tmp-buffy/tmp-cerberus/tmp-clio/
  tmp-morpheus n avaient pas ete supprimes en fin de mission - la discipline
  v0.2.4 impose a CHAQUE agent de supprimer SON dossier avant de passer la
  main. Themis a applique la discipline.
- Le registre courant est vide a chaque non-regression (garde-fous globaux) :
  les usages sont lus dans registre-usages-outils.historique.jsonl.

**Lecon** : un audit doit verifier la REALITE (fichiers presents, registre
archive) et pas seulement les declarations - et l auditeur s applique la
discipline a lui-meme en premier (supprimer son dossier de mission).


## [LECON] 2026-08-14 -- RESPONSABILITE README + CORRECTION INCOHERENCES (Themis)

**Contexte** : decision utilisateur - Themis devient responsable de la VERACITE
des README (public + dev). L utilisateur a signale que readme-dev racontait
n importe quoi (Janus active "par Cerberus" alors qu il est le dernier maillon
de la chaine ; 44 tests au lieu de 46). Investigation : la fausse phrase venait
du commit beta, recopiee sans verification ; personne n avait la responsabilite
explicite du contenu factuel des README.

**Fait** :
1. Corrige readme-dev.md : ligne 139 (Janus active par les agents en fin de
   mission) + ligne 309 (44 -> 46 tests, verifie par comptage reel).
2. Corrige la cause racine janus.md (limites 239-240 : regles contradictoires
   avec la pratique reelle - 35 occurrences 'activer janus' dans l historique).
3. Ajoute ma responsabilite README : fiche v0.3.0 (role + section
   RESPONSABILITE README avec sources de verite et grille) + parcours v0.4.3
   (case c30 branchee sur c1, branche 'readme').
4. Validations : valider-cartes CONFORME, valider-case CONFORME,
   verifier-conformite-fiche CONFORME, test-038 7/7, normes 0/0.

**Lecon** : la veracite d un README ne se verifie pas avec des compteurs
structuraux - il faut CROISER le contenu avec les sources de verite (fiches,
AGENTS-historique, git log). C est maintenant ma grille obligatoire.
## [LECON] 2026-08-14 -- SUPPRESSION REGISTRE HISTORIQUE + FUSION 12 ENTREES (Themis, en relais)

**Contexte** : decision utilisateur -- supprimer le registre-usages-outils.
historique.jsonl (percu comme residu : ne recoit plus d ecritures depuis 08:52)
et ne garder qu UN SEUL registre. Verite etablie avant d agir : l historique
n etait PAS un residu inerte -- le lanceur non-regression l ecrivait a chaque
lancement via archiver_registre (round 8, 395 lignes). Mais la decision
utilisateur est claire : un seul registre. Simplification executee.

**Actions realisees** :
1. FUSION : les 12 entrees mode script-temporaire de l historique (vulcain 2,
   hygie 6, morpheus 3, buffy 1) ont ete ajoutees au registre actif
   registre-usages-outils.jsonl (dedoublonnage par agent+outil+mode, 0 doublon)
2. SUPPRESSION : registre-usages-outils.historique.jsonl supprime
3. detecter-usage-scripts-temporaires.py : scanner_registre ne lit plus que le
   registre actif (registre_historique supprime)
4. tester-lancer-non-regression.py : archiver_registre supprime, remplace par
   purger_registre qui PRESERVE les entrees script-temporaire (memoire des
   declarations conservee dans le registre actif) + message sans avertissement
5. test-024 : point 13 remplace -- verifie que le registre actif contient les
   12 entrees script-temporaire + que le fichier historique n existe pas
6. Docs detecter-usage-scripts-temporaires.md + tester-lancer-non-regression.md
   mises a jour (plus d historique)

**Lecons** :
1. VERITE AVANT SUPPRESSION : un fichier qui ne recoit plus d ecritures n est
   pas forcement un residu -- verifier qui le LIT (grep) avant de conclure.
   Ici l historique etait ecrit par le lanceur a chaque non-regression.
2. PURGE QUI PRESERVE : quand le lanceur vide le registre avant les tests, il
   doit PRESERVER les entrees mode script-temporaire sinon la memoire des
   declarations est perdue a chaque non-regression (et le detecteur devient
   aveugle). purger_registre = garde les script-temporaire, purge le reste.
3. UN SEUL FICHIER : la decision utilisateur simplifie -- un seul registre
   actif, la memoire script-temporaire y vit, plus de double fichier.
4. NON-REGRESSION : 46/47, seul test-028 preexistant KO (spec activer-agent-
   principal 0.5.3 vs outil 0.5.4, bump Vulcain a traiter).
5. Les 15 scripts non declares du detecteur sont des mentions HISTORIQUES
   (lecons/git) preexistantes, pas liees a la fusion.


## [LECON] 2026-08-15 -- AUDIT CHRONO + DIAGNOSTIC NON-ACTIVATION THEMIS (Themis)

**Contexte** : 3 demandes utilisateur - (1) verifier la generalisation du
triplet chrono, (2) comprendre pourquoi Themis ne s active plus, (3) reclasser
les series par frequence de KO.

**Resultats de l audit** :
1. CHRONO : le triplet est PRESENT dans 12/56 tests (21%) et 1/119 outils .py
   (1%) - il n est PAS generalise. Decision connue : le template v0.3.0
   l impose aux NOUVEAUX tests, les existants ne sont pas migres. Le vrai trou
   est dans les OUTILS (1% seulement).
2. THEMIS : cause racine = l axe D (declencheur automatique avant Janus) est
   documente dans la FICHE mais PAS branche dans les CARTES. Toutes les fins
   principales vont directement a Janus (FIN - Activer Janus). Themis est hors
   de la route de fin de mission.
3. SERIES : ordre fixe a,b,c,d,e ; donnees KO disponibles dans le registre-tests
   pour un reclassement dynamique par taux de KO.

**Lecon** : une regle documentee dans une FICHE sans etre branchee dans les
CARTES (ou les outils) est INEFFECTIVE - c est exactement le bug de
non-activation de Themis. Verifier que toute regle "automatique" est meca-
nisee dans les parcours/outils, pas seulement ecrite.


## [LECON] 2026-08-16 -- AUDIT REGLE RELEVE MEME ROUND CONFORME (Themis)

**Contexte** : test reel de la regle immuable RELEVE MEME ROUND gravee par Buffy dans regles-groupes-agents.md (zone marbre, porte UTILISATEUR). Mission Themis : auditer la regle + prouver que la chaine se deroule dans le meme round.

**Verdict : CONFORME (5/5)** :
1. Section presente (ligne 197) + cycle exact `cerberus -> agents <-> agents <-> themis + janus -> cerberus` (ligne 202).
2. Marbre intact : test-057 24/24 CONFORME.
3. 4 imperatifs presents : JAMAIS d arret apres activation, JAMAIS retour Cerberus en milieu de chaine, Seul le DERNIER maillon reactive Cerberus, utilisateur n a PAS a relancer.
4. Coherence cartes : themis a FIN - Activer Janus (c13), janus a Activer Themis pour auditer + FIN - Retour de Themis - les deux agents sont DANS le cycle.
5. Normes 0/0 ASCII + LF, valider-cartes themis CONFORME.

**Preuve du test reel** : l activation de Themis a declenche IMMEDIATEMENT l execution de l audit dans le meme round, sans relance utilisateur - la regle fonctionne.

**Lecon** : le cycle de releve est une CHAINE agents <-> agents avec themis (audit) et janus (controle) integres ; chaque fin de mission active le maillon suivant, seul le dernier reactive Cerberus.

## [LECON] 2026-08-16 -- AUDIT CARTE CERBERUS : HABILITATIONS LIMITEES (Themis)

**Contexte** : derive utilisateur - Cerberus a fait un diagnostic/audit
(convention des scripts temporaires) alors que c est le travail de
Themis. Demande : verifier la carte de Cerberus pour limiter ses
habilitations a la coordination et a la lecture.

**Verdict d audit** : la carte v0.4.9 est globalement CONFORME - les
garde-fous c1/c5/c18/c22 (VERIF/AUDIT/ANALYSE -> Themis c22, jamais
Cerberus) sont presents et bien branches. MAIS 1 correction majeure :
la case c10 contient combos-analyse-projet (outil d ANALYSE avec
ecriture de rapport, proprietaire Clio) - c est le trou par lequel la
derive est passee. Retirer cet outil de la carte de Cerberus.

**Lecon** : les garde-fous de comportement ne suffisent pas si la
carte contient encore l OUTIL de la tentation. Une habilitation se
verifie par l inventaire des indices outils : coordination
(activer-agent-principal), lecture (lister-agents, lire-fichier,
lire-activite-recente), declaration (enregistrer-usage-outil) - et
RIEN d autre. Tout outil d analyse/audit dans une carte autre que
Themis est un ecart.

**Rapport** : themis/rapports/rapport-audit-carte-cerberus-
habilitations-2026-08-16.md
## [LECON] 2026-08-18 -- AUDIT CHAINE LIRE-HEAD : VERDICT CONFORME (Themis)

**Mission** : auditer la chaine Vulcain -> Morpheus (outil lire-head v0.1.1 +
garde-fou test-091 + pins catalogue), activee par Morpheus (c25b, audit de
fin de mission).

**Verdict** : CONFORME (96/100). 0 critique, 0 majeur, 2 mineurs (residus).

**Resultats cles** :
1. Outil lire-head : nommage lire- OK, ASCII 0, LF 3/3, doc complete,
   catalogue 182 (version 0.2.13), index 203, versions alignees 0.1.1.
2. Test-091 : 13 points couvrant les invariants (front-matter, bloc de
   commentaires, premiere ligne vide, --lignes, --info-commune PRESENT,
   PREUVE NEGATIVE ABSENT, fichier introuvable, --dry-run, parite .sh,
   normes) + protections/options/chrono/rating (template v0.4.0). Execution
   reelle relancee par Themis : 13 OK / 0 KO.
3. Pins : test-007/024/060/079 (182 + 203 + lire-head), test-005 (0.2.13),
   test-040 (5/5), test-027 (couverture OK).
4. Conformite d'execution : les 3 maillons ont suivi leur carte (Vulcain ->
   Morpheus -> Themis), la chaine ne retombe pas sur Cerberus au milieu.
5. Etat git : perimetre respecte, aucun fichier hors mission.

**Lecons** :
1. LA CHAINE BOUT-EN-BOUT A PRODUIT UNE CHAINE COMPLETE SANS RACCROC :
   Vulcain (construction) -> Morpheus (tests) -> Themis (audit) -> retour.
   La delegation fonctionne sans repasser par Cerberus quand chaque maillon
   suit SA carte (Pattern 8/13).
2. LES ARTEFACTS DE VERROU D'HABILITATION SONT PREVISIBLES : quand un
   maillon de chaine execute des outils reserves a un autre agent (ex:
   test-005 point 21 execute valider-cartes-decision en tant que Morpheus,
   non habilite), le verrou bloque avec un message clair. Le message BLOQUE
   + la liste des agents habilites distinguent un artefact d'une vraie
   regression : un audit ne doit PAS les compter comme KO.
3. LES DETECTEURS QUI ECRIVENT LEUR RAPPORT DANS LE DOSSIER COURANT CREENT
   DES RESIDUS RECURRENTS : detecter-decalages-catalogue a laisse
   rapport-detecter-decalages-catalogue-<date>.md a la racine. Chaque agent
   doit verifier la sortie des detecteurs qu'il lance et la nettoyer (ou
   demander a Hygie), et les outils devraient ecrire par defaut dans
   traces/ ou tmp-.
4. RE-VERIFICATION INDEPENDANTE : l'audit a relance le test-091 et re-verifie
   chaque pin au lieu de faire confiance aux rapports (regles-veracite :
   je ne fais JAMAIS confiance a un rapport sans l'avoir verifie moi-meme).

**Verdict** : CONFORME. Rapport : themis/rapports/rapport-audit-chaine-lire-head-2026-08-18.md.
## [LECON] 2026-08-18 -- FAUTE DE CHAINE : REACTIVER AU LIEU D'ACTIVER (Themis)

**Contexte** : pendant l'audit chaine lire-head, a la fin de ma mission
(c25b), j'ai lance `reactiver session-llm-1 <raison> themis` au lieu de la
commande exacte ordonnee par ma carte : `activer session-llm-1 morpheus
<raison>` (Activer l'agent precedent avec son rapport). Le reactiver a
ramene Cerberus au milieu de la chaine (violation Pattern 8/13), court-
circuitant Morpheus (qui devait ensuite activer Janus).

**Reparation** : la chaine a ete relancee au maillon manquant (activer
morpheus) avec une raison expliquant la correction. Aucune perte de travail
(rapport Themis ecrit, lecon enregistree).

**Lecons** :
1. c25b (Activer l'agent precedent) utilise la commande `activer`, PAS
   `reactiver`. `reactiver` ramene TOUJOURS Cerberus : c'est reserve au
   DERNIER maillon (Janus) ou a l'activation directe.
2. Le 3e argument de `activer <session> <agent> <raison>` est l'agent a
   ACTIVER (le maillon suivant), pas l'agent precedent a ramener. J'ai
   confondu la semantique des 2 commandes.
3. Meme faute que la lecon Cerberus du 2026-08-08 : reactiver Cerberus au
   milieu d'une chaine = double faute (accepter la violation + court-
   circuiter les maillons suivants). La reparation = reactiver la chaine
   au maillon manquant et documenter l'ecart.
4. GARDE-FOU A GRAVER : a la fin d'une mission en CHAINE (activee par un
   maillon), TOUJOURS utiliser `activer <session> <maillon-suivant> <raison>`.
   Seule l'activation DIRECTE par Cerberus (ou le dernier maillon Janus)
   utilise `reactiver`.

**Verdict** : CONFORME (la chaine a ete reprise au bon maillon, sans perte).
## [CORRECTION] 2026-08-18 -- RE-EDUCATION CARTE v0.4.9 -> v0.4.10 (Themis)

**Contexte** : session-llm-2 (kilo-llm) a donne a Themis une mission hors
perimetre ("inventaire et audit des outils de performance") : Themis a
improvise (tentative editer-parcours 2x, BLOQUE) puis s'est arretee sans
repondre. Diagnostic Chiron : la carte v0.4.9 etait pedagogiquement en
retard sur les cartes recentes.

**Erreurs detectees** :
1. Case c1 (Mission) : AUCUN indice de classification -> un LLM peu
   discipline ne sait pas qu'une mission hors branches doit repondre
   "autre" -> c21.
2. Aucune gestion "outil non autorise / bloque" : quand le verrou
   d'habilitation bloque un outil (ex. editer-parcours reserve a Buffy),
   la carte ne redirigeait pas vers c21 -> c22 (activer l'agent habilite).

**Corrections appliquees** (par Buffy, seule habilitee editer-parcours) :
1. c1 : ajout de l'indice "GARDE-FOU C1" -> demande hors des 6 branches
   -> reponse autre -> c21 (modele : Cerberus GARDE-FOU C1).
2. c21 : ajout de l'indice "REDIRECTION OUTIL BLOQUE" -> verrou bloque
   un outil tente -> reponse OUI -> c22.
3. c22 : ajout de l'indice "AGENTS HABILITES" -> Buffy cartes, Vulcain
   outils, Morpheus tests, Hygie suppression, Janus controle.
4. Bump 0.4.9 -> 0.4.10 + synchronisation fiche themis.md (Pattern 14).

**Lecon** : une carte a jour doit TOUJOURS avoir (a) un indice de
classification dans c1 (garde-fou anti-improvisation), (b) une
redirection quand un outil est bloque par le verrou d'habilitation.
Apres une modification de carte, re-valider le poids des indices
(valider-case --surcharge) pour rester sous le budget.
## [LECON] 2026-08-18 -- AUDIT RESYNC CARTES-LOCK : VERDICT CONFORME (Themis)

**Mission** : audit-fin-mission demande par Vulcain (c15f) sur sa
modification de mettre-a-jour-versions v0.1.5 (ajout de
resynchroniser_cartes_lock apres bump --parcours --wet).

**Actions** :
1. Carte v0.4.10 (re-education) : branche audit-fin-mission -> c25 -> combo
   audit-themis -> c25b (FIN - activer l agent precedent avec son rapport).
2. Combo audit-themis lance (chemin corrige : agents/tools/combos/).
3. Verifications ciblees : code (normalisation LF+rstrip identique a
   editer-parcours), versions (0.1.5 py+md, --version, bumper --tous 0/0),
   normes (ASCII 0, LF 0, py_compile OK), preuve reelle (empreinte lock
   MATCH + test de perturbation), perimetre (aucun fichier de test touche).

**Verdict** : CONFORME -- 0 defaut.

**Lecon** : le GARDE-FOU C1 (ajoute a ma carte en v0.4.10) fonctionne en
conditions reelles : la mission correspondait a une branche exacte
(audit-fin-mission) et le chemin c25 -> c25b s est execute de bout en bout.
Tout outil qui ecrit une carte hors editer-parcours doit resynchroniser
cartes-lock.json (modele : la correction de Vulcain dans mettre-a-jour-
versions v0.1.5).
## [LECON] 2026-08-18 -- AUDIT GARDE-FOU PARITE AGENTS (test-092) : VERDICT CONFORME (Themis)

**Mission** : audit-fin-mission declenche par Morpheus (c31) sur la chaine :
test-092 cree par Morpheus (garde-fou parite agents <-> dictionnaire AGENTS de
activer-agent-principal), defaut detecte (argus + gardien absents du .sh),
signale a Vulcain qui a corrige (bump 0.5.12 -> 0.5.13).

**Actions** :
1. Carte v0.4.10 : branche audit-fin-mission -> c25 -> combo audit-themis ->
   c25b (FIN - activer l agent precedent avec son rapport).
2. Combo audit-themis lance (chemin corrige : agents/tools/combos/).
3. Verifications ciblees : parite .sh (argus/gardien dans les 3 fonctions),
   test-092 9/9 OK, versions 0.5.13 coherentes (py/sh/md/spec), bumper --tous
   0/0, normes ASCII/LF, perimetre git propre, non-regression 10 tests verts.

**Verdict** : CONFORME -- 0 defaut.

**Lecon** : le cycle "garde-fou -> detection d un vrai defaut -> signalement a
l agent d origine -> correction -> verdissement" est la preuve que le systeme
de protection fonctionne : le test-092 a detecte exactement le signalement
Janus jamais corrige (argus/gardien absents du .sh depuis la mission
branchement-chiron), et apres correction il reverdit (9/9). Un garde-fou de
parite doit comparer dans les DEUX sens (agent declare absent de l outil =
oubli ; agent de l outil absent d AGENTS.md = agent mort) + verifier la parite
py/sh (le .sh etait en retard meme quand le .py etait a jour).
## [LECON] 2026-08-18 -- AUDIT CARTE JANUS : VERDICT A REVOIR (Themis)

**Mission** : audit a la demande de Cerberus (l utilisateur se demande si Janus
a ete eduque et si sa carte est conforme).

**Actions** :
1. Combo audit-themis (chemin corrige : agents/tools/combos/).
2. Verifications ciblees : version carte (0.4.20 = fiche PARCOURS), structure
   (51 cases, 11 fins, boucle KO, Pattern 17), garde-fous pedagogiques
   (GARDE-FOU C1, redirection outil bloque, AGENTS HABILITES), historique
   d education (corrections.md + BDD lecons).

**Constat** : carte structurellement SAINE mais pedagogiquement EN RETARD :
c1 sans indice GARDE-FOU C1, aucune redirection "outil bloque", c28 sans
l indice AGENTS HABILITES. Janus n a JAMAIS ete re-eduque par Chiron (seule
lecon Chiron #23 = Themis). Le comportement observe par l utilisateur (Janus
enumere puis active le maillon suivant) est CONFORME a sa carte - ce n est
pas un defaut de comportement, c est la carte qui manque de garde-fous pour
les cas limites (outil bloque).

**Lecon** : la re-education de Themis (v0.4.10) a cree un MODELE de conformite
pedagogique pour toutes les cartes : (a) indice de classification en c1,
(b) redirection quand le verrou bloque un outil, (c) indice AGENTS HABILITES
dans la case d activation. Toute carte d un agent principal doit etre
verifiee contre ce modele. Preuve concrete pendant l audit : le verrou a
bloque Themis sur valider-cartes-decision et MA carte re-education a
correctement redirige (c21/c22) vers l agent habilite.

**Verdict** : A REVOIR - signalement a Chiron (education) pour re-education
de Janus sur le modele Themis v0.4.10.
## [LECON] 2026-08-18 -- AUDIT RE-EDUCATION CARTE JANUS : VERDICT CONFORME (Themis)

**Mission** : audit-fin-mission declenche par Buffy (c8a) sur la re-education
de la carte Janus v0.4.20 -> v0.5.0 (signalement Themis + Chiron, modele
Themis v0.4.10).

**Verifications** : 3 indices en place (c1 GARDE-FOU C1, c27 REDIRECTION OUTIL
BLOQUE + DOMAINES, c28 AGENTS HABILITES), version 0.5.0 sync fiche, lock
MATCH (resync bumper v0.1.5), valider-cartes-decision CONFORME (sous session
habilitee), test-021 9/9 sous buffy (KO point 7 sous themis = artefact de
verrou), test-037 6/6, normes OK, perimetre propre.

**Lecons** :
1. Le cycle est boucle : mon audit A REVOIR (carte janus en retard
   pedagogique) a declenche la re-education (Chiron -> Buffy -> re-audit
   CONFORME). Le modele de conformite pedagogique est desormais applique a
   cerberus, themis ET janus : (a) GARDE-FOU C1 en c1, (b) redirection outil
   bloque, (c) AGENTS HABILITES.
2. Le KO point 7 de test-021 sous ma session est un artefact de verrou
   (valider-cartes-decision bloque pour themis) : verifier les tests KO sous
   la session de l agent habilite (buffy l a lance 9/9) avant de conclure a
   une regression - meme lecon que test-005 sous morpheus.
3. Toujours verifier ASCII apres ecriture du rapport : j ai introduit 2
   'habilitee' accentues (U+00E9) par erreur - corriger avant le verdict.

**Verdict** : CONFORME - 0 defaut.
## [LECON] 2026-08-18 -- AUDIT CARTES VULCAIN/MORPHEUS/BUFFY : VERDICT A REVOIR (Themis)

**Mission** : audit a la demande de Cerberus - verifier si les cartes de
Vulcain, Morpheus et Buffy sont conformes au modele pedagogique (re-education
Themis v0.4.10, Janus v0.5.0).

**Constat** : les 3 cartes sont structurellement SAINES (version sync
carte/fiche, cases et fins completes, cases Activer l agent habilite presentes
pour Pattern 17) mais PEDAGOGIQUEMENT EN RETARD : c1 sans AUCUN indice (0),
pas de redirection outil bloque, pas d indice AGENTS HABILITES. Aucun des 3
n a JAMAIS ete eduque par Chiron (seules educations : Themis #23, Janus #34).

**Lecon** : le modele de conformite pedagogique est la NORME pour TOUTES les
cartes d agents principaux. Les cartes de cerberus (0.5.4), themis (0.4.10)
et janus (0.5.0) sont conformes ; celles de vulcain (0.4.28), morpheus
(0.4.15) et buffy (0.4.14) sont en retard. Une carte structurellement valide
peut manquer de guidage : verifier le CONTENU des indices (classification,
verrou bloque, agents habilites), pas seulement la forme. L audit doit couvrir
TOUTES les cartes principales, pas seulement celles signalees - le retard
pedagogique est silencieux tant qu aucun cas limite (verrou, hors branches)
ne le revele.

**Verdict** : A REVOIR - 3 cartes a re-eduquer (vulcain, morpheus, buffy),
modele : Themis v0.4.10 / Janus v0.5.0.
## [LECON] 2026-08-18 -- AUDIT RE-EDUCATION 3 CARTES : VERDICT CONFORME (Themis)

**Mission** : audit-fin-mission declenche par Buffy sur la re-education des
cartes de Vulcain, Morpheus et Buffy (0.4.x -> 0.5.0, modele Themis v0.4.10 /
Janus v0.5.0).

**Verifications** : 3 garde-fous en place sur les 3 cartes (GARDE-FOU C1 en
c1, REDIRECTION OUTIL BLOQUE + DOMAINES AUTRES AGENTS, AGENTS HABILITES),
textes < 160 caracteres, versions 0.5.0 sync fiches, 3 locks MATCH, normes
OK, perimetre propre.

**Lecons** :
1. Le cycle est boucle : mon audit A REVOIR (3 cartes en retard) a declenche
   la re-education complete (Chiron -> Buffy -> re-audit CONFORME). Les 6
   cartes principales (cerberus, themis, janus, vulcain, morpheus, buffy)
   sont desormais toutes conformes au modele pedagogique.
2. Les KO attendus sont documentables : test-016 pin version (domaine
   Morpheus) et test-057 verrou SEUL BUFFY (artefact de session quand la
   session active EST buffy - reverdit sous janus). Verifier les tests KO
   sous la session appropriee avant de conclure.
3. Le verrou a bloque Themis sur valider-cartes-decision pendant cet audit :
   ma carte re-eduquee (c21/c22) a correctement redirige - la verification
   structurelle a ete faite par Buffy (session habilitee), preuve transmise
   dans sa mission.

**Verdict** : CONFORME - 0 defaut.
## [LECON] 2026-08-18 -- AUDIT CARTES SECONDAIRES : VERDICT A REVOIR (Themis)

**Mission** : audit a la demande de Cerberus - verifier la conformite des
cartes des agents secondaires (Atlas, Argus, Hygie, Clio, Hermes, Gardien,
Chiron, Athena, Promethee, Minerve) au modele pedagogique.

**Constat** : les 10 cartes secondaires sont structurellement SAINES
(versions sync carte/fiche, cases Mission hors parcours + activation
presentes) mais PEDAGOGIQUEMENT EN RETARD : 9 sur 10 sans AUCUN indice en c1,
aucune redirection outil bloque, aucun indice AGENTS HABILITES. Chiron est un
cas particulier (c1 de type ACTION a mission unique, redirections c10/c11
signalent a Buffy/Vulcain) mais sans liste AGENTS HABILITES. Aucun des agents
secondaires n a jamais ete eduque par Chiron.

**Lecon** : le retard pedagogique est GENERALISE - il touche TOUTES les
cartes non eduquees (principales ET secondaires). Le modele de conformite
pedagogique doit etre applique a l ensemble des 16 cartes, avec adaptation
pour les cas particuliers : les agents a mission unique (chiron) n ont pas
besoin du GARDE-FOU C1 classique (c1 action) mais doivent avoir une
redirection vers les agents habilites (c10/c11) et la liste AGENTS HABILITES.
L audit de conformite pedagogique est desormais un controle recurrent : il
reste 10 cartes en retard apres la re-education des 6 principales.

**Verdict** : A REVOIR - 10 cartes a re-eduquer (avec adaptation chiron).
## [LECON] 2026-08-18 -- AUDIT RE-EDUCATION 10 CARTES SECONDAIRES : CONFORME (Themis)

**Mission** : audit de fin de mission (Buffy c8a) de la re-education des 10
cartes secondaires au modele pedagogique (GARDE-FOU C1, redirection outil
bloque, AGENTS HABILITES).

**Actions** : combo audit-themis + verifications ciblees : garde-fous en
place (9/10 avec les 3, chiron cas particulier avec AGENTS HABILITES en c10),
versions bumpees (atlas 0.5.0, argus/hygie/hermes/gardien/chiron 0.2.0, clio
0.6.0, athena/promethee/minerve 0.4.0), locks 10/10 MATCH, fiches 10/10
CONFORME, bumper 0/0, ASCII 0, test-006 19/19, test-020 46/46, test-021 9/9.

**Lecons** :
1. Le modele pedagogique s'applique AUSSI aux cartes secondaires (16 cartes
   au total desormais conformes) avec ADAPTATION pour les agents a mission
   unique : Chiron (c1 action) n'a pas de GARDE-FOU C1 classique, mais la
   redirection (c10/c11) + AGENTS HABILITES. Le test pedagogique reste :
   "que fait la carte si le verrou bloque un outil ? si la mission est hors
   perimetre ?"
2. valider-cartes-decision est BLOQUE pour MA session (habilites :
   argus/buffy/janus/vulcain) : je verifie sous la session habilitee (Buffy
   l'a fait 10x CONFORME) et je documente l'artefact dans le rapport.
3. Le pin de version atlas (test-005 point 17) est l'adaptation Morpheus --
   meme pattern que test-016/test-004 des missions precedentes : chaque bump
   de carte casse les pins, la boucle KO de Janus active Morpheus.

**Verdict** : CONFORME - 0 defaut restant (hors pin Morpheus documente).

## [LECON] 2026-08-18 -- AUDIT PARCOURS AUTO-CORRECTION CHIRON (Themis)

**Mission** : auditer le parcours d'auto-correction de Chiron (v0.3.0, construit par Buffy) : cycle complet, budgets, navigation, verrou pilote, test-058, lock, fiche.

**Verdict** : CONFORME. Cycle c11b->c15->c16->c17->c18 complet, referents 0 manquant, budgets <= 3.0, textes nouveaux < 160, navigation guider OK, verrou bloque chiron sur toute cible != SA carte, test-058 6/6, lock MATCH, fiche sync, bumper 0/0.

**Lecons** :
1. UN PILOTE D AUTO-CORRECTION EST UN CYCLE, PAS UNE BRANCHE : detecter (question d aiguillage) -> se re-eduquer (lecon) -> corriger (editer-parcours avec verrou par cible) -> verifier (Themis) -> reprendre (question d attente, pattern Buffy c8b). La reprise en QUESTION rend le cycle pilotable par le retour de l auditeur.
2. L EXCEPTION PILOTE DOIT ETRE COHERENTE DANS LE GARDE-FOU : test-058 scannait la carte chiron a 2 niveaux (indices OUTIL + texte brut). L exception au niveau 1 sans le niveau 2 = faux positif. Morpheus a adapte la boucle texte : exception ciblee, pas d exclusion globale.
3. LE VERROU EST LA VRAIE GARANTIE, LE TEST LE REFLETE : le verrou bloque chiron sur les autres cartes (teste : atlas -> BLOQUE). Le pilote est sur que le verrou le limite, meme si le test etait en retard.
4. LES TEXTES > 160 PREEXISTANTS SONT HORS PERIMETRE : la carte chiron a des textes > 160 dans c1-c14 (preexistants). Ne pas les confondre avec les nouvelles cases (toutes < 160).

## [LECON] 2026-08-18 -- MON EDUCATION AUX COMBOS ASCII (Themis)

**Mission** : auditer les modifications appliquees a MA carte et MA fiche pour l'education aux combos ASCII (demande utilisateur, diagnostic Chiron, application Buffy).

**Verdict** : CONFORME. c9 = regle ASCII en tete (pattern 2) + indice OUTIL combos-corriger-non-ascii (--full --dry-run) ; fiche themis.md + combo-corriger-ascii + combos-corriger-non-ascii ; PARCOURS v0.5.0 sync ; lock MATCH ; test-058 6/6 ; bumper 0/0 ; evaluateur 15 liens preexistants.

**Lecons** :
1. J AVAIS LA REGLE MAIS PAS L OUTIL : ma regle ABSOLUE 4/5 imposait les outils du cerveau assignes dans ma carte, mais AUCUN outil ASCII n y etait assigne -> je ne pouvais pas l appliquer, d ou mes 8 scripts temporaires. L education = l outil assigne dans la case, pas une regle de plus.
2. APRES CHAQUE RAPPORT : combos-corriger-non-ascii --full --dry-run PUIS --full. Le dry est OBLIGATOIRE avant le wet (preuve datee verifiee par l outil, wet refuse sans elle). Le rapport dry est concis mais complet (tous fichiers, codes U+XXXX).
3. LE COMBO --full EST RAPIDE ET SUR : dry ~1 s, wet ~3 s (correction ciblee uniquement des fichiers detectes). Plus besoin de scripts temporaires pour l ASCII.
4. L EXCEPTION PILOTE CHIRON NE ME CONCERNE PAS : Chiron peut auto-corriger SA carte uniquement ; pour la mienne, c est Buffy qui applique (SEUL BUFFY). Le cycle education : Chiron diagnostique -> Buffy corrige -> moi j audite.

## [LECON] 2026-08-18 -- AUDIT FICHE CHIRON CAPACITE PILOTE (Themis)

**Mission** : auditer la mise a jour de la fiche chiron.md (capacite pilote d auto-correction, carte v0.3.0) par Buffy.

**Verdict** : CONFORME. Vue ensemble v0.3.0 (23 cases) = JSON, cases 23/23, EXCEPTION PILOTE 3 occurrences (regles absolues 1/2 + limites), 0 formulation absolue non nuancee, cycle CHIRON -> THEMIS -> CHIRON documente, lock MATCH, test-058 6/6, test-006 19/19, bumper 0/0, evaluateur 15 preexistants (0 chiron).

**Lecons** :
1. UNE EXCEPTION DE CARTE DOIT ETRE DOCUMENTEE PARTOUT DANS LA FICHE, PAS SEULEMENT DANS LA CARTE : l agent relit SA fiche au demarrage (c0) -- si la fiche contredit la carte, il est desoriente. L audit verifie l ABSENCE de formulation absolue non nuancee, pas seulement la presence de l exception.
2. LE COMPTAGE DES CASES SE FAIT SUR LE JSON : la fiche affichait 15 cases alors que le JSON en avait 18 (c0c/c0e absents de la liste). Le reflet exact = compter les cles du dict cases et aligner la liste 1:1.
3. L AUDIT DE FICHE CROISE 3 SOURCES : carte JSON (version + cases), fiche (reflet), tests (test-058 pour l exception, test-006 pour la navigation). Les 3 doivent etre coherents entre eux.

## [LECON] 2026-08-18 -- AUDIT RE-EDUCATION CHIRON CYCLE PILOTE REEL (Themis)

**Mission** : verifier la re-education de Chiron (c17 du cycle pilote) apres sa correction reelle de c18 (cas A REVOIR sans branche, texte 168 car).

**Verdict** : CONFORME. c18 a 3 branches (OUI CONFORME -> c12, A REVOIR -> c15, NON -> c18), texte aligne 151 car, navigation complete (A REVOIR -> c15, OUI -> c14 FIN, NON -> c18), lock MATCH, 0 branche cassee, fiche sync v0.3.0 (23 cases), lecon BDD 58.

**Point d attention** : test-058 point 2b KO -- la boucle registre n a pas l exception chiron (contrairement aux boucles indices OUTIL et texte). Les declarations legitimes chiron/editer-parcours du cycle pilote reel sont faussement signalees. Adaptation a faire par Morpheus.

**Lecons** :
1. LA VERIFICATION D UN PILOTE SE FAIT PAR SON ACTION REELLE, PAS PAR UN TEST : la meilleure preuve que le cycle d auto-correction fonctionne est de le laisser tourner sur une incoherence reelle (c18 : cas A REVOIR sans branche). Le pilote a detecte, corrige, verifie - tout le cycle a fonctionne sans intervention externe.
2. UN TEXTE DE REGLE QUI PROMET UNE BRANCHE INEXISTANTE EST UN VRAI DEFAUT DETECTABLE : la regle c18 annoncait 'A REVOIR -> c15' mais aucune branche ne menait a c15. L audit verifie que chaque cible annoncee dans un texte de question existe dans les branches.
3. L EXCEPTION PILOTE DOIT COUVRIR TOUTES LES BOUCLES DES GARDE-FOUS : test-058 a l exception chiron dans les boucles indices et texte mais PAS dans la boucle registre (2b). Chaque nouvelle boucle de verification du garde-fou doit porter l exception, sinon le pilote est faussement signale.

## [LECON] 2026-08-18 -- AUDIT FICHE CHIRON BRANCHE A REVOIR c18 (Themis)

**Mission** : auditer la mise a jour de la fiche chiron.md (documentation de la branche A REVOIR de c18, issue de la verification reelle du cycle pilote).

**Verdict** : CONFORME. Fiche reflete les 3 branches de c18 (OUI CONFORME -> c12, A REVOIR -> c15, NON pas revenue -> c18) dans les Branches de decision ET le tableau du cycle pilote. verifier-conformite-fiche CONFORME, valider-cartes CONFORME (point 10), lock MATCH, test-058 6/6, bumper 0/0, evaluateur 0 lien chiron, ASCII 0.

**Lecons** :
1. LA FICHE SUIT LE PARCOURS : une evolution de case (c18 : A REVOIR -> c15) doit etre refletee dans TOUTES les sections de la fiche qui decrivent cette case. L audit verifie la correspondance branches JSON <-> mentions fiche, section par section.
2. LE CYCLE PILOTE EVOLUE LA CARTE, BUFFY EVOLUE LA FICHE : Chiron a corrige c18 (verrou pilote SA carte), Themis a verifie la re-education (CONFORME), puis Buffy a documente la fiche (SEUL BUFFY sur les fichiers agents) et Themis audite de nouveau. La separation des pouvoirs est respectee a chaque etape.
3. L AUDIT DE FICHE APRES UNE EVOLUTION DE CARTE = verifier que les 3 branches du JSON apparaissent dans la fiche, pas seulement la branche nouvelle.

## [LECON] 2026-08-18 -- AUDIT TABLEAU AGENTS DISPONIBLES CERBERUS (Themis)

**Mission** : auditer la completion du tableau "Agents disponibles" de cerberus.md (5 agents secondaires ajoutes : Argus, Chiron, Gardien, Hermes, Hygie).

**Verdict** : CONFORME. Tableau 15/15 agents (vs dossiers agents/), roles conformes AGENTS.md, conditions d activation operationnelles (fiches), verifier-conformite-fiche CONFORME, bumper 0/0, evaluateur 15 preexistants, ASCII 0, perimetre propre.

**Lecons** :
1. LE TABLEAU AGENTS DISPONIBLES EST LA CARTE D ENTREE DU ROUTEUR : un agent oublie ne sera jamais active par Cerberus. L audit de completude (valider-tableaux) compare le tableau aux dossiers agents/ -- 15/15 apres correction.
2. UN FAUX POSITIF D OUTIL N EST PAS UN DEFAUT DE MISSION : "classeur-variables" (dossier de donnees, pas un agent) est signale par valider-tableaux de facon preexistante. Il ne faut PAS l ajouter au tableau (ce serait un agent fantome) -- c est l outil qui devrait distinguer `type: fiche-agent` de `type: classeur`.
3. LES ROLES ET CONDITIONS D ACTIVATION VIENNENT DE 2 SOURCES : AGENTS.md (roles) + fiches (conditions operationnelles). L audit verifie les 2, pas seulement la presence du nom.

- **2026-08-19 (audit test-055)** : audit CONFORME du correctif Buffy (10 indices editer-parcours ajoutes). Verification : cases exactes signalees -> indice present (10/10), pattern identique buffy/chiron, test-055 12/12, test-006 19/19, 10 cartes CONFORMES, ASCII/LF 0.

## [LECON] 2026-08-19 -- AUDIT INTEGRATION TOKENS VULCAIN (Themis)

**Mission** : auditer la mission Vulcain (integration tokens dans le cycle d'activation : analyser-tokens --snapshot, chronometrer-duree --tokens, activer-agent-principal v0.5.17, evaluer-processus v0.1.11).

**Verdict** : CONFORME. Execution conforme a la carte Vulcain (c9f -> active Themis), parite py/sh validee, bumper PROPRE, ASCII/LF 11/11, tests 098/060/092/040/028/067 verts, preuve reelle au repere (vulcain 13min 27s + chrono themis avec tokens_debut).

**Lecons** :
1. MON COMBO D'AUDIT ETAIT CLOUE : combo-audit-themis c1 genere `combos-audit-general.py cerveau-projet` (l'outil attend le WORKSPACE, pas le projet -> chemin cerveau-projet/cerveau-projet INEXISTANT -> 57 erreurs factices, score 46/100 au lieu de structure 100/100) et c4 passe un argument que combos-valider-cerveau REFUSE. `echec_ok: true` masque les echecs -> "COMBO TERMINE" avec resultats faux. Lecon : VERIFIER CHAQUE GENERATEUR DU COMBO SUR UN LANCER REEL, ne pas faire confiance a echec_ok.
2. UNE ERREUR DE LANCEUR PRECEDE TOUTE CONCLUSION D'AUDIT : quand audit-general donnait CRITIQUE, c'etait le parametrage du combo, pas le projet. Avec le bon dossier (.), evaluer-structure = 100/100. Toujours relancer l'outil directement avec le bon parametre avant de conclure.
3. MA CARTE PORTE UNE REFERENCE PERIMEE : c3/c25 indiquent `cerveau-projet/combos/combo-audit-themis/` (inexistant) au lieu de `agents/tools/combos/combo-audit-themis/`. Les indices fichier des cartes doivent pointer vers des chemins REELS - a corriger par Buffy (SEUL BUFFY sur les cartes).
4. LES SCORES D'EVALUATEURS CONTIENNENT DES FAUX POSITIFS STRUCTURELS CONNUS : evaluer-agents prend les dossiers de donnees (conventions, lecons, philosophie, regles-immuables, traces) pour des agents, evaluer-coherence prend `protocole-X/` et les options CLI pour des liens casses. Les citer sans les attribuer a la mission auditee.

## [LECON] 2026-08-20 -- AUDIT MISSION VULCAIN ENCART ID : VERDICT CONFORME (Themis)

**Mission** : auditer la mission Vulcain (remplacement session -> id LLM dans l encart Activites recentes et le corps d AGENTS-historique.md, demande utilisateur).

**Verdict** : CONFORME -- 0 defaut dans le perimetre.

**Verifications cles** (20 points, re-executes par l auditrice) :
1. Outil activer-agent-principal v0.5.20 : composer_bloc_historique ecrit '- HH:MM | id | raison' avec identifiant = id_lie_a_session(session) or session (repli si aucun id lie) ; maj_encart_activites header '| Heure | Agent | id | Raison |'.
2. Migration : 170 entrees avec id, 0 session-llm en colonne, mappage historique exact (bord 20/08 20:51 : avant -> llm-1, apres -> freebuff ; session-llm-3 -> kilo-test2 ; session-llm-4 -> opencode), mentions dans les raisons conservees.
3. Coherence encart <-> corps : 10/10 (heure/agent/id identiques).
4. Normes : ASCII 0 (fichier + outils + rapport), LF pur, py_compile OK.
5. test-091 : 13/13 ; lire-activite-recente v0.1.2 affiche l id.
6. Preuve reelle sur copie : resolution session-llm-1 -> freebuff, session inconnue -> None (repli).
7. Conformite d execution : carte Vulcain suivie, Pattern 13 respecte (retour Cerberus avec bilan, garde-fou v0.5.19).
8. Aucun parseur casse : evaluer-processus parse l ancien format v0.5.15 (deja obsolete), aucun outil ne lit plus la colonne session.

**Lecons** :
1. UNE MIGRATION DE FORMAT DE JOURNAL PARTAGE = MAPPAGE HISTORIQUE, PAS REMPLACEMENT GLOBAL : l id d une session change dans le temps (session-llm-1 = llm-1 puis freebuff). La migration doit etre temporelle (bord de date/heure), pas un simple sed. Verifier le bord exact (l identification a 20:51 est la seule entree freebuff a cette heure, legitime).
2. LE REPLI EST LE BON COMPORTEMENT POUR LES SESSIONS INCONNUES : id_lie_a_session retourne None pour les sessions purgees -> l outil replie sur la session. Un audit doit verifier le repli (preuve sur copie avec session inexistante) ET la resolution reelle (session connue -> id).
3. LA COHERENCE ENCART <-> CORPS EST LE TEST CLE D UNE MIGRATION : l encart extrait les 10 dernieres entrees du corps. Apres migration, comparer les 10 entrees (heure/agent/id) des 2 sources : toute divergence = migration incomplete.
4. LES KO DE LA NON-REGRESSION NE SONT PAS TOUS LIES A LA MISSION : test-035 (nettoyer-sessions au demarrage cerberus, avant la mission), test-098 (ancien format v0.5.15), test-001..008 (anciens formats) sont preexistants. Les identifier par leur date/heure dans le registre, pas par leur nom.
5. MA CARTE PORTE TOUJOURS LE CHEMIN PERIME DU COMBO (cerveau-projet/combos/ -> agents/tools/combos/), signale le 19/08 et non corrige : l amelioration de carte a ete demandee a Buffy pendant cet audit (Pattern 17).

**Rapport** : themis/rapports/rapport-audit-encart-id-2026-08-20.md (ASCII 0).

[LECON 2026-08-20] Audit reparation immediate erreurs hors mission (Buffy) : VERDICT CONFORME 0 defaut. Verifie : registre (vulcain tester-lancer mode direct -> verrou-dev liste blanche DEV_NON_REGRESSION ; janus proteger-verrou-marbre DECLARATION_FAUTIVE retiree), carte janus c9 + indice ajouter-contenu-fichier (bump 0.5.3, fiche sync, lock sync), evaluer-processus global/janus/cerberus/vulcain 0 probleme, marbre 8/8, ASCII 0, detecter-impacts 0 non-a-jour, lecon BDD #177 avant retour. Lecon : la reparation immediate des erreurs hors mission (regle utilisateur) passe par la correction ciblee du registre (mode verrou-dev pour les usages legitimes de la liste blanche, retrait des declarations fautives) + l ajout des indices manquants aux cartes. valider-cartes-decision reste verrouille pour Themis (artefact de verrou connu) - s appuyer sur la verification de Buffy + la verification structurelle independante.
[LECON 2026-08-20] Audit reparation carte themis (Buffy) : VERDICT CONFORME 0 defaut. Verifie : carte themis v0.5.3 + case c16 contient l indice evaluer-processus + description a jour, fiche themis PARCOURS (v0.5.3) sync (Pattern 14), lock OK, evaluer-processus global + themis 0 probleme, marbre 8/8, ASCII 0 CRLF 0, detecter-impacts 0 non-a-jour reel (2 faux positifs de mtime : reecriture binaire du JSON apres la fiche), conformite execution (trace Buffy : editer-parcours -> valider-cartes-decision -> lecon BDD #180 avant retour), Pattern 13 respecte. Lecon : apres une reecriture binaire d un JSON (correction CRLF), le mtime change et detecter-impacts signale la fiche 'non a jour' alors que le contenu est correct - verifier le CONTENU (version) pas le mtime. Le defaut OUTIL_HORS_CARTE themis -> evaluer-processus est corrige : la carte themis couvre maintenant l outil d audit evalue-processus.
[LECON 2026-08-20] Verification agent Socrate (demande utilisateur) : VERDICT CONFORME - Socrate fonctionne. Verifie : fiche complete (v0.2.0, role conversation revision), carte parcours-socrate.json valide (16 cases, c0 RELIRE -> c0b -> c0e -> c0c -> c1 -> questions -> c7 missions-revision.md -> c8 FIN reactiver Cerberus, commande exacte), valider-case CONFORME, branche AGENTS.md, activer-agent-principal connait socrate, verrou habilitation OK, cartes-lock OK, evaluer-processus 0 probleme, dossier coherent (missions-revision.md cree 20:16 = preuve d execution), ASCII 0. 2 ecarts mineurs non bloquants signales : 1) champ parcours du JSON incomplet (pas de nom/agent/description -> guider affiche Agent : ?) ; 2) Pattern 14 absent de la fiche (pas de mention PARCOURS (vX.Y.Z)). Agent habilite pour reparer : Buffy. Lecon : verifier un agent = croiser toutes les sources (fiche, carte, lock, AGENTS.md, verrou habilitation, activer-agent-principal, preuve d execution reelle) - ne jamais se limiter a la structure JSON.
[LECON 2026-08-20] Re-verification boucle KO socrate (Buffy) : VERDICT CONFORME - les 2 ecarts sont CORRIGES. Verifie : 1) champ parcours du JSON complete (nom: parcours-socrate, agent: socrate, version 0.1.0, description) + preuve fonctionnelle guider --liste affiche 'Agent : socrate' (avant 'Agent : ?') ; 2) Pattern 14 present (REGLE ABSOLUE -- PARCOURS (v0.1.0) ligne 86, coherence fiche/carte P10) ; 3) registre : plus AUCUNE entree valider-case janus/themis, les 3 restantes sont toutes de buffy (outil exclusif) ; 4) evaluer-processus global 0 probleme (avant : 2 DECLARATION_FAUTIVE) ; 5) marbre 8/8, lock socrate present, ASCII 0 CRLF 0, detecter-impacts 8 faux positifs de mtime (dossier socrate cree 20:16, carte modifiee 23:05 - modification additive). Lecon : une boucle KO doit re-verifier le defaut ORIGINEL (les 2 ecarts) ET son contexte (les declarations fautives retirees du registre) - croiser contenu JSON, preuve fonctionnelle, registre (absences + usages restants) et scan global. Point d attention hors perimetre : missions-revision.md (cree 20:16 par Socrate) porte 28 CRLF - fichier de travail de Socrate, non modifie par la reparation, a signaler pour correction eventuelle.
[LECON 2026-08-20] Verification cases FIN vulcain/buffy/clio (demande utilisateur : activer agent suivant, pas reactiver Cerberus) : VERDICT A REVOIR - 3 ecarts + 1 incoherence. CONFORME : fins principales (buffy c8/c22/c27, clio c12 'Activer Janus', vulcain c9/c15 chaine Morpheus) - commandes 'activer <session> janus/morpheus', messages 'commandes activer, PAS reactiver'. ECARTS : E1 buffy c15e message reference 'ma fin normale c13 (FIN - Reactiver Cerberus)' mais c13 INEXISTANTE dans la carte ; E2 clio c10e meme message mais c13 = 'Mission hors parcours' (question) ; E3 vulcain c9e/c15e meme message mais c13 = 'Lancer le combo corriger-ascii' (action) ; E4 vulcain c16d 'Je REACTIVE Cerberus' (branche documentation, a trancher activation directe vs maillon) ; E5 vulcain fiche v0.6.0 vs JSON 0.5.2 (Pattern 14, HEAD coherent 0.5.2/0.5.2 - fiche bumpee sans JSON). Lecon : verifier les references de cases dans les messages de REPRISE - les c15e/c10e/c9e ont ete copies d'un parcours a l'autre et referencent des c13 'FIN - Reactiver Cerberus' qui n'existent pas dans les cartes cibles ; verifier aussi la synchronisation version fiche/carte (Pattern 14 P10). Agent habilite : Buffy.
[LECON 2026-08-20] Verification AGENTS-historique.md position interventions Themis (demande utilisateur) : VERDICT A REVOIR - DEF A UT CONFIRME. Les 3 interventions Themis du 21/08 (06:59, 06:47, 06:38) sont dans la section ## 21/08/2026 placee AU-DESSUS de l encart '## Activites recentes (10)' (ligne 17), alors que les autres jours (20/08, 19/08, 18/08) sont SOUS l encart. CAUSE : dans ajouter_historique() de activer-agent-principal.py (lignes ~570-585), la branche else (nouvelle date) insere la nouvelle section jour apres le PREMIER \n---\n (fin du FRONTMATTER) au lieu d apres la fin de l ENCART - le fichier a 3 zones (en-tete, encart, historique) et le premier \n---\n est la fin de l en-tete. Verifie aussi : coherence chronologique entrees themis OK, encart = 10 dernieres entrees du corps OK, ASCII 0 CRLF 0. Lecon : un fichier en-tete + encart + historique a 3 zones - pour inserer dans l historique, cibler la fin de l encart (--- apres le tableau) ou la premiere section ## <date>, jamais le frontmatter. Agent habilite : Vulcain (outil activer-agent-principal).

[LECON 2026-08-21] Audit fins de Buffy et boucle de chaine (demande utilisateur) : VERDICT A REVOIR - 5 constats. E1 : les fins de buffy (c8/c22/c27) activent TOUJOURS Janus, jamais Vulcain (modif outil) ni Morpheus (tests) - le flux c16->c31 (Vulcain)/c17 (Athena)->c8a (Themis)->c8 (Janus) aboutit toujours a Janus, Morpheus n est jamais active par Buffy. E2 : 3 chaines CONTRADICTOIRES pour le cas modif outil (buffy c31 indice : Vulcain->Janus->Clio->Cerberus SANS Morpheus ; vulcain c9/c15 : Vulcain->Morpheus->Janus->Cerberus ; buffy c35 : Vulcain reactive l agent precedent) - la chaine ne converge pas. E3 CAUSE RACINE : le garde-fou v0.5.19 de activer-agent-principal BLOQUE toute activation directe (agent actif != cerberus, cible != cerberus, cible != actif -> BLOQUE sauf --forcer) donc meme les chaines bout-en-bout prevues par les cartes (Vulcain->Morpheus, Morpheus->Janus, Buffy->Janus) ne peuvent PAS s executer - la boucle reelle passe par Cerberus (chaque agent reactive Cerberus qui route le suivant) et les messages 'J ACTIVE X' des fins sont en decalage avec l outil. E4 : les 20 fins 'FIN - Activer X' n ont PAS de message de relais explicite ('commence ET finis ton travail puis active l agent suivant') - le message generique n existe qu une fois (buffy c36). E5 : buffy c15e reference 'c13 (FIN - Reactiver Cerberus)' INEXISTANTE (defaut E1 du 20/08 jamais repare). DECISION UTILISATEUR A TRANCHER : Option A (retour Pattern 8 : adapter le garde-fou pour autoriser l activation de chaine legitime + fins avec routage + harmoniser les chaines) vs Option B (tout par Cerberus : remplacer les fins 'Activer X' par 'Reactiver Cerberus'). Lecon : croiser CARTE et OUTIL - une fin de carte peut promettre une activation que l outil bloque (garde-fou) : verifier TOUJOURS la faisabilite reelle de l activation directe avant de conclure sur une chaine.
[LECON 2026-08-21] Audit reparation Buffy (boucle KO Janus, activee par relais) : VERDICT A REVOIR - 1 defaut D1. CONFORME : carte cerberus v0.5.9 c45/c45b/c46/c46b au format conforme (branches[] + suivant, plus aucun branche_vraie) ; integration socrate 4 parcours v0.1.2 fins 'FIN - Activer Janus' + c1b recablee (c1->c1b, OUI->c2/NON->c1) ; cerberus.md ligne 221 socrate (valider-tableaux 24/24) ; outil convertir-carte-mermaid v0.2.1 correctif multi-parcours (nom_fichier_parcours par fichier source, 20 cartes synchronisees, 8 fichiers socrate sans collision) ; pins tests (test-013 22/22, test-072 10/10, test-070 13/13, test-094 7/7, test-096 11/11) ; 52 fichiers ASCII/LF purs ; marbre 8/8 ; Pattern 14 cerberus 0.5.9 + socrate 0.1.2 ; conformite execution verifiee au registre (editer-parcours, valider-cartes-decision, valider-case, valider-tableaux, convertir-carte-mermaid, mettre-a-jour-versions - outils de la carte Buffy). D1 : cartes-lock.json DESYNCHRONISE pour parcours-cerberus.json (empreinte lock 35c8... != fichier actuel 49b2... selon empreinte_fichier d'editer-parcours : LF + rstrip par ligne) - la description a ete modifiee en write_bytes direct APRES le bump editer-parcours (carte 18:33 > lock 18:11) - prochaine edition via editer-parcours BLOQUEE (anti-contournement barrage n3). Agent habilite : Buffy (resync lock via editer-parcours ou resynchroniser_cartes_lock de mettre-a-jour-versions). LECONS : 1) une ecriture directe write_bytes sur une carte verrouillee desynchronise le lock SANS signalement - apres TOUTE modification directe, recalculer l'empreinte (LF + rstrip par ligne) ; 2) les garde-fous existants (test-057, valider-cartes-decision) verifient l'EXISTENCE du manifeste et la conformite structurelle, PAS la correspondance lock <-> fichier - un audit croise doit recalculer les empreintes ; 3) les outils exclusifs (proteger-verrou-marbre gardien, tester-lancer-non-regression janus) ne se DECLARENT pas au registre par un agent non habilite - les verifications se font par lecture directe.
[LECON 2026-08-21] Audit alignement indices cartes (Buffy) : VERDICT CONFORME 0 defaut. 34 indices de 16 cartes alignes alias corriger-symboles -> canonique corriger-accents-zones-sensibles. Verifie : 0 alias restant, Pattern 14 16/16, lock 0 divergence, regle texte vulcain c7 corrigee, test-055 12/12, test-035 10/10, test-096 11/11, test-071 7/7, test-005 28/28 (atlas 0.5.4), test-013 22/22 (cerberus 0.5.10), test-016 20/20 (buffy 0.5.4), marbre 8/8, valider-cartes-decision 17/17, ASCII/LF 0, conformite execution registre OK. Rapport : themis/rapports/rapport-audit-alignement-cartes-buffy-2026-08-21.md. LECON : auditer un alignement = verifier (1) l alias a disparu des indices, (2) la regle texte associee corrigee AUSSI (test-055), (3) les pins de versions adaptes, (4) les vues mermaid/SVG regenerees (test-096). LECON TECHNIQUE : quand j ecris un rapport, eviter les tirets cadratins (U+2014) et emojis - les remplacer par - et [OK] des la creation (Pattern 2 ASCII).
[LECON 2026-08-21] Audit correction sessions proposition-v2 (Buffy) : VERDICT CONFORME 0 defaut. Clarification utilisateur : session-admin = agents DEJA EXISTANTS (Cerberus, Buffy, Themis, etc. qui gerent le cerveau-projet v1), session-freelance = NOUVEAUX agents v2 dans freelance/. Verifie : 10 occurrences coherentes (decision 38-39, arborescence 81, activation 153, section 8 tableau complet, etapes 222), 0 reference session-llm restante, contenu des 10 sections preserve, ASCII 0 CRLF 0, conformite execution (buffy : guider-parcours + enregistrer-lecon x4). Lecon : la distinction session-admin / session-freelance est la reference pour toute mention future des sessions dans la v2 (source : proposition-v2.md section 8).



## [LECON] 2026-08-22 -- AUDIT CREATION REDACTEUR-V2 PAR BUFFY (Themis)

**Mission** : verifier le travail deja fait par Buffy - creation de l agent Redacteur-v2.
**Resultats** : creation COMPLETE ET BRANCHEE (fiche, corrections, parcours, activation
py/sh parite, AGENTS.md, readme-dev, ASCII 0).
**Ecarts** : E1 MAJEUR README public obsolete (16 agents annonces vs 18 reels, Socrate et
Redacteur-v2 absents - domaine exclusif Clio) ; E2 regle RELECTURE absente de la fiche
(valider-relecture KO) ; E3 parcours c0b sans branche INCERTAIN ; E4 faux positifs
valider-relecture (6 dossiers non-agents comptes comme agents - a signaler a Vulcain).
**Verdict** : CONFORME AVEC RESERVES - creation valide, documentation publique a mettre
a jour via Clio.
**Rapport** : themis/rapports/rapport-audit-creation-redacteur-v2-2026-08-22.md
**Lecon** : une creation d agent n est terminee que si TOUTES les surfaces de reference
sont synchronisees (readme-dev OUI mais README public NON). Le garde-fou valider-relecture
a attrape l ecart E2 des la premiere passe - la mecanisation fonctionne.
## [LECON] 2026-08-23 -- AUDIT CORRECTIONS DE FORMATION DE CLIO POUR README-V2 (Themis)

**Contexte** : audit de fin de mission de la mission Buffy 'corrections de formation de Clio pour readme-v2' (E1-E5 Chiron, verdict Janus VALIDE sur le diagnostic). Activee par Buffy (maillon de chaine c8a).

**Verdict** : CONFORME -- 0 defaut dans le perimetre.

**Verifications** : navigation reelle c1 readme-v2 -> c22 -> c23 (guider --reponses PARCOURS atteint), Pattern 14 fiche clio.md v0.6.5 == parcours 0.6.5, E1-E4 corriges (branche readme-v2 + cases c22/c23, EXCEPTION REDACTION V2, SOURCES DE VERITE V2 en Connexions, ton v2 badges agents v2), lecon Buffy dans corrections.md + BDD id 287, registre usages complet (12 outils declares), ASCII 0/0 sur clio.md + parcours-clio.json + buffy/corrections.md, conformite execution (carte Buffy suivie, Themis activee AVANT Janus = c8a -> c8).

**Points hors perimetre signales** : P1 clio/corrections.md 383 CRLF PRE-EXISTANTS (fichier non modifie par la mission, git status initial confirme) -> Hygie ; P2 3 divergences d'outils (editer-fichier, valider-cartes-decision, activer-agent-principal) -> Vulcain (mission separee, deja identifiee par Chiron + Janus).

**Lecon** : un audit de fin de mission se prouve par le CROISEMENT mission/carte/deroulement reel. La navigation reelle du nouveau chemin (guider --reponses) + la lecture structurelle du JSON compensent un outil verrouille (valider-cartes-decision ferme pour Themis - artefact de verrou connu) : ne pas conclure 'non verifiable' quand un outil est bloque, verifier par une voie independante.
## [LECON] 2026-08-23 -- AUDIT MISSION CLIO (VERIFIER) : README DOIT-IL REFLETER LA REPARATION (Themis)

**Contexte** : audit de fin de mission de la mission Clio "verifier" activee par Cerberus (c16 OUI) -- la reparation a modifie des fichiers, le README doit-il etre mis a jour ? Activee par Clio (maillon de chaine c12a).

**Verdict** : CONFORME -- 0 defaut dans le perimetre.

**Verifications** : verdict Clio NON correct (reparation documentaire : CRLF, 9 residus, 3 alignements de versions -- aucun outil/agent cree/supprime ; badges Agents-19/Outils-165 = realite 19/165 confirmee par le verifier), comportement conforme a la carte c11 (verifier sans modifier, signaler sans corriger), registre usage clio -> mettre-a-jour-readme (22:00:39), ecarts signalis PRE-EXISTANTS prouves (README.md + readme-dev.md absents du git status de session).

**Points hors perimetre** : P1 readme-dev incoherence interne (entete "164 outils" vs section 6 "165 outils" vs reel 165 -- categorie Git manquante du tableau) -> Clio ; P2 mismatch structurel outil/README (le verifier attend la section 'La boite a outils' absente du README 1ere personne du 20/08 -> MANQUANT massifs a chaque verification, bruit permanent) -> Vulcain et/ou Clio.

**Lecon** : une reparation documentaire ne change pas les compteurs du README (verifier creations/suppressions d'outils avant de decider) ; le verifier README peut produire un bruit structurel permanent quand le README change de format (signaler le mismatch) ; un ecart SOMME du tableau readme-dev se prouve par la categorie manquante (164 vs 165 = Git absente).

**Rapport** : themis/rapports/rapport-audit-clio-verifier-readme-reparation-2026-08-23.md (ASCII 0).
[LECON 2026-08-24] Audit P-A editer-fichier pour Clio : CONFORME (P-B fiche a aligner). La reparation (decision utilisateur) est correcte : indice editer-fichier en c20 carte clio, bump 0.6.6, Pattern 14 OK, verrou (source=cartes) reconnait clio, ASCII 0/0. P-B : la fiche Clio garde 3 occurrences de 'UNIQUE outil mettre-a-jour-readme' (l.48/124/282) contradictoires avec la nouvelle habilitation - la fiche doit etre alignee sur la decision utilisateur. LECON : quand une habilitation est elargie (decision utilisateur), TOUTES les mentions de la fiche de l agent doivent etre alignees sur la carte. Rapport : themis/rapports/rapport-audit-pa-clio-editer-fichier-2026-08-24.md.

[LECON 2026-08-24] Audit validation flux editer-fichier Clio : VERDICT CONFORME. Mission Clio de validation du nouveau flux (decision utilisateur : editer-fichier habilite). Verifie : indice editer-fichier en c20 carte clio (source verrou), Pattern 14 v0.6.6, regle fiche assouplie (3 occurrences), registre complet, ASCII 0/0, dry-run sans modification. Lecon : une mission de VALIDATION prouve une habilitation par un test reel du verrou en dry-run (zero blocage, zero redirection) - plus probant qu'une relecture de carte. Flux Clio -> editer-fichier direct fonctionne.

[LECON 2026-08-24] BILAN STRATEGIQUE v1 redige : rapport complet (126 lignes, ASCII 0/0) dans themis/rapports/bilan-strategique-v1-2026-08-22.md. Methode : 212 lecons BDD + AGENTS-historique + audit croise. Verdicts : benefique = lecons.db, cartes, cycle+controles, outils validation, classeur. Nefaste = sur-ingenierie gouvernance, habilitations decouvertes tard, 3 memoires non synchronisees, chaines disproportionnees, outils jetables. Regles a garder : relecture, registre, dry-run, ASCII, RVAV, verifier juge, Pattern 13, anti-usurpation, double verification. Versionning = utile signal / fardeau discipline. Lecon : un bilan strategique = relecture croisee + synthese (pas un audit de mission) - les cases c8c/c8d (impacts/fins) ne s appliquent pas a un rapport, reponse honnete OUI avec constat d absence d impact.

[LECON 2026-08-24] Comparatif v1 vs v2 super-detail redige (263 lignes, ASCII 0/0) dans themis/rapports/comparatif-v1-v2-2026-08-24.md. Bandeau NON NORMATIF en tete + 16 piliers (v1/v2/DECISION/RISQUE/PREUVE) + synthese (5 vitaux + 5 pieges). Verdicts : 7 a garder, 7 a adapter, 2 a creer. Lecon : la neutralisation du risque documentaire est STRUCTURELLE (rapport dans themis/rapports/, jamais reference dans une carte/fiche, bandeau NON NORMATIF) - pas une promesse.

[LECON 2026-08-24] Audit test-100 frontmatter : VERDICT CONFORME. Test Morpheus valide (2/2 OK, 806 .md, critere CLOTURE pertinent, aucun outil modifie). Lecon : le bon critere pour un garde-fou de frontmatter est la CLOTURE du bloc, pas la validite YAML complete - le projet utilise volontairement des frontmatters non-strict (block scalars, commentaires seuls, exemples avec accents) = faux positifs si parse strict exige.

## [LECON] 2026-08-24 -- AUDIT MISSION ATLAS EXPLORATION FREELANCE : CONFORME

**Contexte** : audit de fin de mission (chaine Cerberus -> Atlas -> Themis).
Atlas a explore le dossier freelance et produit un dossier complet.

**Verdict** : CONFORME, 0 defaut. Rapport : rapports/rapport-audit-atlas-exploration-freelance-2026-08-24.md.
Livrable audite : atlas/rapports/dossier-complet-freelance-2026-08-24.md
(536 lignes, 14 sections, bandeau NON NORMATIF, ASCII 0/0).

**Verifications** : grades des 9 agents (fiches, exacts), 20 protocoles,
M1-M7, 598 messages JARVIS, registre atlas 12 usages, 1 lecon BDD + bloc
corrections.md. Point de vigilance : corriger-accents a cree un .bak (28 Ko)
dans atlas/rapports/ -> residu domaine Hygie (a supprimer).

**Lecon** : pour auditer un rapport d'exploration, verifier les DONNEES
(chiffres, grades, volumes) contre les sources reelles, pas seulement la
forme -- c'est la que se cachent les erreurs.

## [LECON] 2026-08-24 -- AUDIT MISSION BUFFY : METHODE RIGOUREUSE ATLAS (CONFORME)

**Contexte** : audit de la modification d'Atlas (carte + fiche + livrables) pour
l'exploration rigoureuse decidee par l'utilisateur (un dossier a la fois, un .md
par dossier, rapport complet = doublon de structure).

**Verdict** : CONFORME, 0 defaut.

**Lecons** :
1. La boucle c2a-c2b-c2c (un dossier a la fois, .md par dossier, boucle jusqu a
   couverture totale) est le pattern a garder pour les explorations exhaustives.
2. Le doublon de structure (arborescence + liens vers les .md dedies) rend le
   rapport complet navigable et comparable v1 vs v2.
3. Le verrou d habilitation bloque valider-cartes-decision pour les agents non
   habilites (themis) - c'est le verrou qui fonctionne, pas un defaut.

**Preuves** : rapport-audit-buffy-atlas-methode-rigoureuse-2026-08-24.md ; carte
v0.5.5 nav validee c2c OUI->c8 / NON->c2a ; 17 .md dedies + 35 liens ;
fiche PARCOURS v0.5.5 + REGLE ABSOLUE METHODE RIGOUREUSE ; ASCII 0/0.

## [LECON] 2026-08-24 -- AUDIT MISSION CLIO : README APRES MISSION BUFFY ATLAS (CONFORME)

**Contexte** : audit de la mission Clio (verification README apres la mission
Buffy methode rigoureuse Atlas).

**Verdict** : CONFORME, 0 defaut.

**Lecons** :
1. Une modification INTERNE d'agent (carte/fiche/rapports) ne change ni le
   nombre d'agents ni le nombre d'outils : Clio doit verifier (--verifier) et
   NE RIEN modifier si 0 ecart. Ne pas forcer une mise a jour inutile.
2. Le --verifier est la source de verite : 0 ecart + git status vide =
   decision correcte de ne rien faire.
3. Le perimetre Clio est respecte quand elle n'utilise QUE mettre-a-jour-readme.

**Preuves** : rapport-audit-clio-readme-atlas-2026-08-24.md ; --verifier 0
ecart (19 agents, Outils-165, readme-dev 40 categories = 165) ; git status
README vide ; ASCII 0/0 ; registre clio 25.

## [LECON] 2026-08-24 -- AUDIT MISSION BUFFY : CORRECTION ATLAS DOSSIER DEDIE (CONFORME)

**Contexte** : audit de la correction de la methode Atlas (probleme utilisateur :
rapports a la racine de atlas/rapports/ au lieu d'un dossier dedie par
exploration).

**Verdict** : CONFORME, 0 defaut.

**Lecons** :
1. Le DOUBLON DE STRUCTURE doit vivre dans UN DOSSIER DEDIE PAR EXPLORATION
   (atlas/rapports/<cible>-<AAAAMMJJ>/) qui est LE DOSSIER COMPLET : c'est la
   bonne organisation pour des explorations multiples comparables v1 vs v2.
2. Des LIENS RELATIFS SIMPLES (noms de fichiers) dans le dossier-complet
   rendent le deplacement du dossier entier sans casse - c'est le pattern a
   recommander.
3. Apres une reorganisation, verifier : la racine ne contient plus que le
   dossier dedie, les liens resolvent, les mentions textuelles de chemins
   sont mises a jour.

**Preuves** : rapport-audit-buffy-atlas-dossier-dedie-2026-08-24.md ; carte
v0.5.6 (c2/c2b/c9 dossier dedie, 0 orpheline) ; atlas/rapports/ = [dossier
dedie] avec 19 fichiers ; liens 18/18 ; ASCII 0/0 ; registre buffy 229.

## [LECON] 2026-08-24 -- AUDIT MISSION CLIO : README APRES CORRECTION ATLAS DOSSIER DEDIE (CONFORME)

**Contexte** : audit de la mission Clio (verification README apres la
correction de la methode Atlas : dossier dedie par exploration).

**Verdict** : CONFORME, 0 defaut.

**Lecons** :
1. Une reorganisation de LIVRABLES (deplacement de rapports dans un dossier
   dedie) ne change ni le nombre d'agents ni d'outils : Clio doit verifier
   (--verifier) et NE RIEN modifier si 0 ecart.
2. Le --verifier est la source de verite : 0 ecart + git status vide =
   decision correcte de ne rien faire.
3. Le perimetre Clio est respecte quand elle n'utilise QUE mettre-a-jour-readme.

**Preuves** : rapport-audit-clio-readme-atlas-dossier-dedie-2026-08-24.md ;
--verifier 0 ecart (19 agents, Outils-165, readme-dev 40 categories = 165) ;
git status README vide ; ASCII 0/0 ; registre clio 27.

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
