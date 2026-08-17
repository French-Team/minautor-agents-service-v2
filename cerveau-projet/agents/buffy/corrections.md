---
identite:
  type: corrections
  appartient_a: buffy
  commun: false
# Corrections et Surcharges -- Buffy
# Agent principal -- Developpeur du cerveau-projet

agent:
  nom-agent: "buffy"
  version_corrections: "0.5.0"
  derniere_mise_a_jour: "2026-08-05"

# Types de corrections
types:
  - regle: "Ajout d'une nouvelle regle specifique a Buffy"
  - surcharge: "Modification d'une section existante de la fiche"
  - correction: "Correction d'une erreur recurrente"
  - configuration: "Parametre de travail specifique"
---

# Corrections et Surcharges



## [LECON] 2026-08-11 -- REGLE ABSOLUE LECTURE DOC + CASE c0d DANS 11 PARCOURS (Buffy)

**Mission** : renforcer la regle 'lire le .md avant utilisation' (REGLE ABSOLUE protocole-outils + case c0d dans les 11 parcours).

**Lecons** :
1. Le protocole-outils avait une etape 2 faible ('Lire la documentation') dans une liste : transformee en REGLE ABSOLUE explicite (lecture du .md = contrat d utilisation, usage sans doc = erreur).
2. Case c0d inseree entre c0c et c1 dans les 11 parcours : point d entree universel (toute mission passe par c1). C est une action (ne consomme pas de reponse) : la navigation des tests n est pas cassee.
3. PIEGE SURCHARGE : mes indices REGLE initiaux faisaient 262/175 caracteres - au-dessus du seuil de valider-case (SEUIL_TEXTE = 160) -> 3 tests KO (test-009/013/015). Raccourcis a 137/114 : resorbe.
4. Impacts versions : l ajout de la case a bump 11 versions de parcours -> test-004 (morpheus), test-005 (atlas), test-013 (cerberus), test-016 (buffy) attendent les anciennes versions : a adapter par Morpheus (REGLE IMMUABLE DELEGATION).
5. test-006 (cartographie) attend un en-tete avec nb cases : le nombre de cases change (c0d) -> a adapter aussi.
6. Resultat intermediaire : 11/11 CONFORME, navigation c0d OK, normes 0/0, non-regression 16/21 (5 KO = adaptations de tests prevues).

## [LECON] 2026-08-11 -- LIGNE TRIO DE JANUS + BOUCLE DE CORRECTION (Buffy)

**Mission** : construire la ligne trio dans la carte de Janus (poste de controle de la chaine athena -> promethee -> minerve) + cases correction dans le trio + protocole enrichi.

**Lecons** :
1. Janus est desormais le POSTE DE CONTROLE DE LA CHAINE : branche 'trio' dans c1 -> cT1 (lire protocole) -> cT2 (quel agent) -> cT3/cT4/cT5 (controles) -> OK : cT6/cT7 (transmettre au suivant) ou c10 (reactiver Cerberus apres minerve) / KO : cT8/cT9/cT10 (renvoyer le rapport a l agent concerne).
2. Boucle KO cote trio : chaque agent du trio a une branche 'corriger' dans c1 -> c9f (CORRIGER selon le rapport de Janus, CREATION LIMITEE Pattern 12) -> c10 (FIN - Activer Janus). L'agent corrige puis reactive Janus qui revalide.
3. Le validateur v0.4.0 (P10) a DETECTE l'incoherence fiche/parcours apres le bump des versions : preuve en conditions reelles que le garde-fou semantique fonctionne. Les 4 fiches ont ete mises a jour (janus v0.3.6, trio v0.2.3).
4. Navigation reelle validee : athena OUI -> cT6 Activer promethee ; athena NON -> cT8 Renvoyer a athena ; minerve OUI -> c10 Reactiver Cerberus ; c1->corriger -> c9f -> c10 sur les 3 agents.
5. Protocole-controle-trio v0.2.0 : nouvelle section 'Chaine de transmission et boucle de correction' + pieges (transmission non conforme, retour a Cerberus en milieu de chaine) + REGLE D EXCELLENCE (livrable passe en aval uniquement s il est excellent).
6. Resultat : 4/4 CONFORME, non-regression 20/20, normes 0/0.

## Regles specifiques

| Regle | Description |
|---|---|
| **Les index ne sont PAS des fichiers de suivi** | Un index contient UNIQUEMENT la navigation et le point d'entree |
| **Outils.md -> Cerberus -> Vulcain** | Quand je cree un outil.md, je demande a Cerberus d'activer Vulcain |
| **Tester avant d'appliquer** | TOUJOURS tester les outils en mode --dry-run d'abord |

---

## Philosophie

| Philosophie | Description |
|---|---|
| **Respect du Cycle** | Avant de terminer, verifier que Cerberus peut reprendre |
| **Comprehension Avant l'Action** | Comprendre POURQUOI avant de modifier |
| **Integrite des Noms** | Donner un NOM PROPRE aux agents, jamais fonctionnel |
| **Hierarchie Sacree** | Respecter l'ordre des fichiers |
| **Verification Obligatoire** | Verifier CHAQUE point avant de valider |

---

## Lecons apprises

| Date | Lecon | Philosophie |
|---|---|---|
| 2026-08-08 | CONFORMITE D EXECUTION (Pattern 11, spec-guider-parcours v0.2.19, decision utilisateur recommandation 4 du constat stabilite) : la stabilite d une carte ne se mesure PAS par la structure seule (detecter 0 anomalie, valider-cartes CONFORME) mais par la CONFORMITE D EXECUTION : l agent a-t-il fait ce que sa carte ordonnait ? Lecons : (1) LES VIOLATIONS RECENTES LAISSENT LES JSON VALIDES : Vulcain a reactive Cerberus au lieu d activer Morpheus, Cerberus a lance des analyses au lieu d activer Buffy -- dans les 2 cas la carte etait structurellement CONFORME, seule l EXECUTION a devie ; aucune validation automatique ne pouvait le detecter ; (2) LE CROISEMENT EST UN RAISONNEMENT, PAS UN OUTIL : mission recue + cases ordonnees par la carte + deroulement reel (message d activation/reactivation, fichiers modifies, rapports) -- Themis croise ces 3 traces AVANT de rendre le verdict ; (3) SPEC v0.2.19 : Pattern 11 documente (tableau des 2 violations + exemple JSON c8b) + procedure d audit 4i (croiser mission/carte/deroulement, signaler les ecarts meme si JSON CONFORME) + critere 22 + re-audit complet passe de 10 a 11 patterns ; (4) PARCOURS THEMIS : case c8b CONFORMITE D EXECUTION ajoutee via generateurs-case entre le verdict c8 et le rapport c9 (branches OUI->c9 / NON->c3 re-audit), chemin doute c17 reoriente vers c8b pour que TOUT audit passe par le controle -- 21 cases ; (5) PIEGE RECABLAGE : ajouter --apres ne recable QUE le champ suivant, PAS les branches -- c8 pointait encore OUI->c9 en contournant c8b, corrige par editer --branche OUI:c8b (verifier suivant ET vers apres chaque ajout/suppression) ; (6) PIEGE STR_REPLACE : un oldString present a 2 endroits (fin de la ligne Historique ET fin du critere 21) est remplace par la PREMIERE occurrence sans allowMultiple -- le bloc v0.2.19 s est colle par erreur dans le critere, reparation par 2 remplacements cibles ; (7) VALIDATION : navigation 5/5 PARCOURS TERMINE (audit/doute/rvav/autre x2), valider-cartes --tous 11/11 CONFORME, detecter 0 anomalie, ASCII 0 sur spec + parcours | La structure valide ne prouve PAS la stabilite : la conformite d execution (l agent a-t-il fait ce que sa carte ordonnait ?) est le SEUL vrai test |
| 2026-08-04 | Comprendre avant d'agir | Comprehension Avant l'Action |
| 2026-08-04 | Respecter la hierarchie | Hierarchie Sacree |
| 2026-08-05 | Les noms ont une ame | Integrite des Noms |
| 2026-08-05 | Le cycle est sacre | Respect du Cycle |
| 2026-08-05 | Un index n'est pas un suivi | Regle des index |
| 2026-08-05 | Le workflow est automatique | Buffy->Cerberus->Vulcain |
| 2026-08-07 | ETAPE SYSTEME (choix .py/.sh) ajoutee dans la section Outils de base (P0) des 11 fiches + template : consulter le profil systeme stocke avant d'executer un outil | Choix .py/.sh systematique |
| 2026-08-07 | Quand une mission renomme une mission dans la table d'une fiche, renommer AUSSI le titre de section detaille (### Mission : X) pour que valider-tableaux trouve la correspondance | Coherence table/section |
| 2026-08-07 | Delegation des tests : Vulcain active Morpheus au moment des tests de ses outils (modele boucle : Morpheus reactive Vulcain, qui termine puis reactive Cerberus). Les fiches vulcain.md et morpheus.md ont ete restructurees en consequence | Delegation aux agents dedies |
| 2026-08-07 | Corrections mineures morpheus.md (rapport Themis) : lien frontmatter 'tools/tests/' -> 'tools/tester/' (dossier renomme) + motif 'protection-*' -> 'tester-protection-*' (6 occurrences) | Suivre les rapports Themis jusqu a la correction |
| 2026-08-08 | Vague 1 migration schema identite (33 fichiers) : bloc identite: ajoute aux 11 fiches + 11 corrections (frontmatter YAML) + 11 parcours (cle JSON top-level). Lecons : (1) themis/corrections.md n avait PAS de frontmatter --- (cas particulier traite a la main), (2) guider-parcours tolere les cles inconnues mais valider-cartes-decision cherche la section Carte de Decision dans les fiches allegees -> NON CONFORME PRE-EXISTANT (hors perimetre, a signaler), (3) detecter-impacts BUG DECOUVERT en usage reel : le fichier modifie apparait lui-meme dans les impliques (comparaison chemin relatif vs absolu : args.fichier relatif vs scanner absolu) -> a corriger par Vulcain, (4) valider-nommage sur agents/ = faux positifs (concu pour outils/ uniquement) | Migration par vagues + verifier chaque outil en usage reel |
| 2026-08-08 | CHASSE AUX INTENTIONS PASSIVES (Pattern 5, spec v0.2.6) : apres la decouverte utilisateur (carte vulcain se terminait par une FIN passive 'Morpheus teste et te reactive' -> chaine coupee), chasse systematique dans tout le cerveau. Lecons : (1) SCAN : les 11 parcours ont ete scannes pour les formulations passives dans les messages des cases fin (te reactive / j attends / attend le retour / il me reactive) -> seuls vulcain et morpheus portaient des formulations a corriger (les autres fins etaient deja actives) ; (2) CORRECTIONS : vulcain.md (J attends son retour -> LA CHAINE NE S ARRETE PAS : boucle RELAIS -> RETOUR -> CLOTURE materialisee dans la carte v0.2.1), morpheus.md (3 occurrences modele boucle precisees avec la case RETOUR c9b/c15b de Vulcain), fins CHAIN/FLUX athena c10 + promethee c10 (ajout RELAIS ACTIF : je ne m arrete pas en attente, la chaine continue jusqu au retour a Cerberus) ; (3) PREVENTION : REGLE ABSOLUE 7 ajoutee au template fiche-agent (chaine de delegation active) + Pattern 5 documente dans la spec-guider-parcours v0.2.6 (structure RELAIS -> RETOUR -> CLOTURE -> FIN + procedure d audit 4b) + GARDE-FOU generateurs-case v0.1.1 py/sh (detection des formulations passives a la creation/edition d une case fin, avertissement jaune non bloquant) + doc generateurs 0.1.1 ; (4) VALIDATION : scan final 11 parcours = 0 passif, json.load, --liste, --reponses chemins athena/promethee -> PARCOURS TERMINE, py_compile + bash -n, parite py/sh garde-fou (ATTENTION detectee 1/1), ASCII 0 sur 9 fichiers ; (5) REGLE GENERALE : une delegation ne se termine JAMAIS par une fin passive -- la carte du delegant materialise la boucle (RELAIS lancer le parcours du delegue -> RETOUR verifier son rapport -> CLOTURE reactiver Cerberus) | Toute fin passive coupe la chaine : materialiser la boucle RELAIS -> RETOUR -> CLOTURE |
| 2026-08-08 | Spec-guider-parcours v0.2.7 : RE-AUDIT COMPLET DES 5 PATTERNS (lecon Themis : l audit 4b seul ne testait que Pattern 5, c est la procedure 2 qui a revele 3 ecarts ASCII chez vulcain c4/c6/c12). Lecons : (1) REGLE : a chaque creation/modification/audit de parcours, REJOUER les procedures 1, 2, 3, 4 et 4b en integralite -- JAMAIS seulement la procedure nouvelle ou modifiee ; un audit partiel donne un verdict partiel ; (2) AJOUTS : preamble REGLE DE RE-AUDIT COMPLET en tete de la procedure + section 4b enrichie (point 6 : distinguer DELEGATION vs ACTION FINALE -- les parcours sans delegation se terminent par des fins actives Reactiver Cerberus, pas de boucle requise) + section 4c RE-AUDIT COMPLET (rejouer les 5 procedures, verifier en particulier la procedure 2 position 1 texte UNIFORME REGLE IMMUABLE ASCII) + critere d acceptation 14 ; (3) PIEGE ASCII REPETITIF : 2 accents introduits malgre la regle (REJOUES puis Apres) -> les detecter avec valider-conformite-ascii AVANT de declarer termine (l outil signale les lignes non-ASCII, corriger puis revalider a 0) | Un audit partiel donne un verdict partiel : toujours re-auditer les 5 patterns |
| 2026-08-08 | CONTEXTE TEMPS REEL (Pattern 6, spec-guider-parcours v0.2.8) : decision utilisateur -- chaque agent doit se souvenir des dernieres interventions des autres agents (meme si deja en memoire) et savoir que les autres LLM existent. Lecons : (1) DISTINCTION STATIQUE/DYNAMIQUE : la question honnete c0 couvre le STATIQUE (fiche + corrections, memorisable) ; l HISTORIQUE (AGENTS-historique.md) est DYNAMIQUE (il change a chaque activation des autres LLM) -- le dynamique ne se memorise pas, sa lecture est OBLIGATOIRE meme en memoire ; (2) 2 OUTILS LIVRES PAR VULCAIN (VERDICT Morpheus VALIDE, test-006 26/26) : lire-activite-recente v0.1.0 (les 15 dernieres interventions au format date | session | agent | action, env AGENTS_HISTORIQUE) + activer-agent-principal v0.4.1 (section ## Sessions connues dans AGENTS.md reconstruite a chaque action depuis le classeur, table session | id LLM | agent actif | derniere activite) ; (3) ANCRAGE 5 NIVEAUX : case c0c CONTEXTE inseree dans les 11 parcours (c0 OUI -> c0c, c0b -> c0c, c0c -> c1 -- traversee par TOUS les chemins, meme OUI) + demarrer.md (section 2) + protocole-activation (Etape 3 + regle d or + piege) + spec v0.2.8 (Pattern 6 + procedure 4d + critere 15) + template (REGLE ABSOLUE 8) ; (4) PIEGE MODIFICATION JSON EN MASSE : un heredoc complexe dans spawn_agents casse le JSON (Unterminated string) -- ecrire le script de transformation dans un fichier (write_file) puis l executer ; (5) RECABLAGE : la case c0c doit etre atteignable par OUI ET par c0b (sinon le chemin OUI contourne le contexte) -- verifier les 2 branches apres transformation | Le dynamique ne se memorise pas : relire l historique a chaque activation, meme en memoire |
| 2026-08-08 | VAGUE 2 -- migration agents/tools/ vers le schema hybride v0.2.0 (281 fichiers migres + 5 deja + 1 IGNORE + 0 erreur, outil migrer-identite v0.1.3 Vulcain + 3 verdicts Morpheus VALIDES). Lecons : (1) APPLIQUER AVEC L OUTIL PUIS VERIFIER PAR UN RE-SCAN : apres la migration reelle, relancer l outil en dry-run -- les fichiers restes a migrer revelent les cas non couverts (le re-scan a revele 17 blocs hors fenetre 12 puis 2 cas .sh) ; (2) BUG 1 (v0.1.1) : _a_identite_md retournait DEJA sur la simple fermeture --- meme sans identite: -> 4 fichiers de test/template ignores a tort ; corrige par detection stricte + protection frontmatter-sans-identite (ignore, jamais de double frontmatter) ; (3) BUG 2 (v0.1.2) : _migrer_py_sh traversait la 1re ligne vide + le long en-tete documentaire -> bloc a la ligne 13 pour 17 fichiers (illisible par detecter-impacts, re-migration = doublon) ; corrige par insertion apres l en-tete court + mode REPARER (deplace sans doublon) ; (4) BUG 3 (v0.1.3) : 2 fichiers .sh avec en-tete court suivi de commentaires SANS ligne vide (ligne # seul) -> la boucle traversait tout jusqu a l indice 12 ; corrige par insertion APRES la ligne # Statut (ou # Version) ; (5) PIEGE DE TEST : le chemin /tmp du shell Windows (AppData) differe du Z:/tmp de write_file -> pour tester detecter-impacts sur un fichier cree par script, utiliser le chemin absolu Z:/tmp (sinon fichier introuvable = faux negatif) ; (6) REGLE : une migration massive se valide par (a) re-scan idempotence a 0 migre, (b) py_compile/bash -n/json sur TOUT, (c) detecter-impacts qui lit l identite sur un echantillon de chaque format, (d) ASCII 0 -- les 4 valides pour la vague 2 ; (7) les .pyc regeneres par py_compile apparaissent en git status (artefacts conserves par le projet, 86 suivis) : ne pas les confondre avec des fichiers de la migration | Une migration massive se valide par re-scan a 0 migre + compilation globale + detecter-impacts qui lit chaque format |
| 2026-08-08 | AUDIT OUTILS FANTOMES + CORRECTION (decision utilisateur) : audit croise des 88 outils reels contre index-tools + 11 fiches + 11 parcours + demarrage + combos. Lecons : (1) METHODE D AUDIT : comparer 5 sources (dossiers reels, index-tools, fiches P0, parcours agents, parcours-demarrage + definitions-combo + catalogue) -- le parcours-demarrage et les combos citent des outils absents des parcours agents (nettoyer-sessions, detecter-usage-outils-externes...) : ne jamais conclure sans ces sources supplementaires ; (2) RESULTAT : 0 outil fantome total (generateurs-case etait le seul, deja corrige), MAIS 2 anomalies : 5 combos BRANCHES dans les parcours mais absents de index-tools.md (combo-audit-themis, combo-controle-outil, combo-controle-modification, combo-corriger-ascii, combo-sante-tableaux -> decouverte cassee pour un humain qui consulte l index) + 2 combos TOTALEMENT INVISIBLES (combo-activation, combo-controle-impacts : crees, testes, jamais branches) ; (3) FAUX POSITIFS A EXCLURE : sous-dossiers composants (tests/spec/protections), documents de reference (outils-base.md), motifs textuels de fiches (creer-fichier / ecrire-fichier, template-test, tester-protection-*) ; (4) CORRECTION : index-tools.md section Combos 4->11 (Total 92->99, note 84+11+3+1), carte buffy v0.2.1 (case c13b combo-controle-impacts apres c13 avant RVAV c14, case c34b combo-activation apres c34 avant c36, ajoutees AVEC generateurs-case --apres --suivant) ; (5) PIEGE ECRITURE PARCOURS : un heredoc complexe dans spawn_agents casse le JSON (Unterminated string) et un python -c multiligne casse aussi -- ecrire le script dans un fichier (.tmp-buffy-lire/) puis l executer ; (6) navigation des 2 nouveaux chemins confirmee PARCOURS TERMINE (c9->...->c13b->c14 et c33->c34->c34b->c36), ASCII 0 sur parcours + index | Un outil cree et teste mais jamais branche est invisible ; l audit d un ecosysteme compare toutes les sources, pas seulement les parcours agents |
| 2026-08-08 | INTEGRATION generateurs-case (decision utilisateur : l outil existait (v0.1.0, teste 21/21 Morpheus) mais n etait branche NULLE PART -> l agent qui corrige les cases ne peut pas utiliser un outil que sa carte ne connait pas, REGLE ABSOLUE 5). Lecons : (1) DIAGNOSTIC : outil cree et teste ne veut PAS dire branche -- verifier index-tools.md (absent), fiche P0 (absent), 11 parcours (0 reference), spec (absente) ; un outil fantome est invisible pour les agents ; (2) CORRECTION Buffy : index-tools.md (section Generateurs + stats 4->5, Total 91->92, note 83->84 outils d action), fiche buffy.md (P0 ajoute), carte buffy (case c10b question 'fichier a modifier = carte de decision ?' inseree APRES c10 avec recablage auto, branches OUI->c10c / non->c11 ; case c10c indice generateurs-case -> c12) ; (3) J AI MODIFIE MON PROPRE PARCOURS AVEC L OUTIL generateurs-case (ajouter --case --apres --branche --suivant --indice-regle --indice-outil) : test en conditions reelles reussi, recablage c10->c10b automatique, validation auto des references a chaque ajout (ajouter d abord la cible c10c PUIS la branche c10b pour que les references existent au moment de la validation) ; (4) PIEGE : une question ajoutee avec --apres herite d un champ suivant residuel (recablage) -- les branches priment dans la navigation mais le suivant parasite peut etre retire pour la proprete ; (5) PREEXISTANT (hors perimetre, a signaler) : valider-cartes-decision --tous = 5/5 NON CONFORME car il cherche l ancienne section Carte de Decision que les fiches allegees n ont plus (parcours = source de verite) -- outil a mettre a jour par Vulcain ; (6) la navigation de mon parcours reste PARCOURS TERMINE sur les 2 branches (c9->c10b->c10c->c12 et c9->c10b->c11->c12), ASCII 0 sur les 3 fichiers modifies | Un outil cree et teste mais non branche est un outil fantome : verifier index + fiche + parcours + spec avant de le considerer utilisable |
| 2026-08-08 | PISTE NETTOYAGE dans le demarrage (decision utilisateur) : le parcours de demarrage a desormais plusieurs pistes (le demarrage est un jeu de piste comme tout le reste). (1) CASE DE CHOIX EN PREMIERE POSITION : c0 = l utilisateur a-t-il commence par 'nettoyer la session existante' ? OUI -> c0n (nettoyage) / NON -> c0r (relecture honnete) - la relecture reste obligatoire meme apres nettoyage (on nettoie d abord, puis on relit le contexte et on s identifie) ; (2) CASE NETTOYAGE c0n : lancer l outil nettoyer-sessions (Vulcain v0.1.0, perimetre etats actifs uniquement : blocs session-llm + Sessions connues dans AGENTS.md, lignes profil-session-* dans le classeur ; le frontmatter et le journal historique sont PRESERVES) puis DEMANDER a l utilisateur SON id et s identifier a neuf (sidentifier <id>) ; (3) demarrer.md reste LA PORTE : une seule ligne ajoutee (phrase 'nettoyer la session existante' + ce que ca fait), tout le reste vit dans le parcours JSON ; (4) la carte de decision decompose le demarrage en petites cases directives et informationnelles : chaque case donne UN indice (outil) au bon moment, l agent n a pas a cogiter ; (5) VALIDATION : JSON 11 cases version 0.2.0, --liste OK, navigation des 2 chemins (OUI|OUI|OUI|NON nettoyage + NON|OUI|OUI|NON normal) PARCOURS TERMINE, ASCII 0 sur parcours + demarrer.md, liens 0 invalide | Une carte de decision se construit en petites cases directives : chaque case = UN indice, jamais de long texte |
| 2026-08-08 | BUG ajouter_historique CORRIGE (v0.5.0, mission utilisateur V3) : l insertion d une entree dans AGENTS-historique.md se faisait apres le PREMIER --- rencontre -- or depuis la migration schema hybride, le fichier commence par un frontmatter (--- identite ---) -> les entrees s accumulaient APRES la ligne 1, poussant identite: + entete # Historique des Agents au milieu du fichier. Lecons : (1) CAUSE RACINE .sh : regex awk /^|---/ = ALTERNATION (^ OU ---) -> matche TOUTE ligne, insertion apres la ligne 1 ; .py : re.match(^\s*\|?---) matche l ouverture du frontmatter -> meme effet ; CORRECTION (parite) : inserer la nouvelle entree AVANT la premiere ligne | 20XX- (index($0,"| 20")==1 en awk / ^\| 20 en regex), le frontmatter et l entete restent en tete ; (2) TOUT FICHIER AVEC FRONTMATTER risque le meme bug pour toute logique inserer apres le premier --- : verifier les regex qui matchent --- en position 1 ; (3) REPARATION : trier les 150 entrees par timestamp DESC (stable) + reconstruire frontmatter/entete/intro/--- + preserver la fin legacy preexistante (## Historique + ligne coupee, presente dans HEAD) ; (4) PIEGE TEST POLLUTION : quand on teste activer-agent-principal sur COPIE, rediriger LES 3 variables (AGENTS_FILE + AGENTS_HISTORIQUE + CLASSEUR_STOCKAGE) -- oublier une seule = l outil ecrit sur les VRAIS fichiers (le test sidentifier test-id a pollue AGENTS.md session-llm-4 + classeur, restaure a llm-2/16:03) ; (5) CONSTAT TEST-003 A REVOIR (PREEXISTANT, hors perimetre) : nom_session du test lit encore **Nom** au lieu de **Nom Agent** (migration v0.5.0 non propagee au test, git diff vide) -> a signaler a Morpheus | Toute insertion apres le premier --- casse un fichier a frontmatter : inserer au debut du tableau, jamais apres un delimiteur |
| 2026-08-08 | REFONTE CONCEPTUELLE DU MODELE DE CASES (etape concept, decision utilisateur) : Pattern 7 MODELE COMPOSE dans la spec-guider-parcours v0.2.13 + philosophie + 2 pilotes. Lecons : (1) CONCEPT : une case de DECISION doit avoir AU MINIMUM 2 branches (sauf action directe `indice` a `suivant`) -- 2 branches = 2 solutions alternatives, ou une decision + une DEVIATION vers un workflow secondaire avec RETOUR au flux principal (case de rejoint) ; l agent reflechit tout en restant guide, plus de cul-de-sac a reponse unique ; (2) PHILOSOPHIE : nouveau dossier agents/philosophie/ (index + fiche PLACE 'une place pour chaque chose et chaque chose a sa place' + fiche ALLEGER 'alleger ne veut pas dire supprimer : decomposer pour faciliter' -- metaphore palette de briques) : les philosophies sont le POURQUOI, les regles/conventions le COMMENT ; (3) SPEC v0.2.13 : Pattern 7 documente (regles 1-4 + schema JSON c5/c5a DEVIATION/c5b REJOINT/c6) + procedure d audit 4e + critere 18 + RE-AUDIT COMPLET passe de 6 a 7 patterns ; protocole-carte-decision : section modele compose ajoutee apres les 5 modeles de cases ; (4) PILOTES avec generateurs-case : buffy v0.2.2 (c13c question erreurs hors mission apres c13b combo : OUI -> c13d fin signalement a Cerberus / NON -> c14 flux principal) + cerberus v0.2.0 (c12a question apres c12 : OUI -> c12b DEVIATION reactiver Buffy -> c12c REJOINT -> c13 / NON -> c13) -- la boucle complete des 2 cotes (Buffy signale, Cerberus decide) ; (5) PIEGE CONFIRME : une question ajoutee avec --apres herite d un champ suivant residuel -- les branches priment mais je le RETIRE pour la proprete (editer-fichier sur le JSON) ; (6) RVAV : --tous 11/11 conformes, ASCII 0 sur 8 fichiers, navigation des 2 deviations PARCOURS TERMINE (OUI et NON), liens 4/4 valides ; (7) nommage philosophie-* = meme pattern que convention-* (fichiers fondateurs, pas des outils -- valider-nommage --type outil les rejette comme il rejette convention-structures.md, pas un ecart) ; (8) convention-structures : dossier philosophie/ ajoute a l arbre L2 de agents/ | Une case de decision = un modele compose (2+ branches, deviations avec retour) : la philosophie 'alleger = decomposer' guide le format des cartes |

---

## Configuration

| Element | Valeur |
|---|---|
| **Outils** | Utiliser nos outils partages, pas des outils generiques |
| **Workflow** | Buffy -> Cerberus -> Vulcain -> Cerberus |

---

## Connexions

| Fichier | Role |
|---|---|
| `buffy.md` | Ma fiche principale |
| `AGENTS.md` | Fichier dynamique (je suis l'agent principal) |
| `index-cerveau.md` | Point d'entree du cerveau |
| `demarrer.md` | Protocole de demarrage |

### Lecon : Ne pas utiliser les emojis

**Ce qui sest passe** : >> cerveau-projet/agents/buffy/corrections.md && echo Jai cree un fichier avec des emojis ([OK], [ERREUR], [ATTENTION]).

**Ce que jai compris** : >> cerveau-projet/agents/buffy/corrections.md && echo La regle interdit les emojis. >> cerveau-projet/agents/buffy/corrections.md && echo Les emojis doivent etre remplaces par des symboles ASCII. >> cerveau-projet/agents/buffy/corrections.md && echo  >> cerveau-projet/agents/buffy/corrections.md && echo **Ce que je fais maintenant** : >> cerveau-projet/agents/buffy/corrections.md && echo Avant de creer un fichier, je verifie quil ny a pas demojis.
Si je vois des emojis, je les remplace immediatement.

## [NOTES] 2026-08-07 -- Parcours Morpheus et Clio (jeu de piste)

**Tache** : creer les parcours (jeu de piste) de Morpheus et Clio + allegement de leurs fiches (parcours = source de verite).
**Lecon** :
1. Les FICHIERS DU CERVEAU (fiches, parcours JSON, documents) sont MON domaine (Buffy, developpeur principal). Les OUTILS dans agents/tools/ sont le domaine de Vulcain. Un parcours JSON pour un agent est un fichier du cerveau -> Buffy, pas Vulcain. Distinction cle : outil (Vulcain) vs contenu/fiche (Buffy).
2. Pattern du parcours : 5 modeles de cases (question, indice-outil, indice-fichier, regle, controle) + branches. Chaque case donne UN indice au bon moment.
3. parcours-morpheus.json (17 cases) : missions tester (lire doc -> protocole-tests -> template-test -> 3 protections OBLIGATOIRES -> executer -> verdict -> lecons -> retour VULCAIN ou CERBERUS selon delegation). Le controle de la delegation est une QUESTION avec branches (VULCAIN/CERBERUS) - cas du modele boucle.
4. parcours-clio.json (16 cases) : missions corriger (journal -> verifier -> maj -> controle nouvelle categorie manquante -> insertion manuelle editer-fichier -> ASCII -> lecons) et verifier (sans modifier). Integre la lecon Clio : --maj ne cree pas une categorie absente.
5. La navigation est validee par guider-parcours --liste (charge + valide la structure) et --reponses (parcourt les branches). Les parcours JSON sont valides si --liste affiche toutes les cases sans ERREUR.
6. Fiches allegees : morpheus.md et clio.md passent en v0.2.0, section PARCOURS (SOURCE DE VERITE DU GUIDAGE) avec la commande guider-parcours, regles absolues conservees, connexions + historique. Le guidage des missions vit dans le JSON, pas dans la fiche.

## [NOTES] 2026-08-07 -- Generalisation du jeu de piste (demarrer.md + protocole-carte-decision)

**Tache** : generaliser le concept PARCOURS (jeu de piste) dans demarrer.md et protocole-carte-decision.
**Lecon** :
1. demarrer.md est la CASE 0 du jeu : apres l'identification, chaque agent lance SON parcours (guider-parcours + agents/<agent>/parcours/parcours-<agent>.json) au lieu de lire la fiche d'avance
2. Le protocole-carte-decision a evolue en v0.2.0 : la carte statique (tableaux) est SUPERSEDEE par le parcours JSON guide -- le protocole documente les deux (historique + actuel), le parcours est la methode officielle
3. Quand un protocole IMMUABLE evolue : conserver le contenu historique sous une section dediee et ajouter la section d'evolution EN TETE (le lecteur voit d'abord la methode actuelle)
4. Les lecons operationnelles des agents (ex: --maj ne cree pas une categorie absente) peuvent devenir des CASES du parcours -- le parcours est vivant, il absorbe les corrections
5. Les 5 modeles de cases (question, indice-outil, indice-fichier, regle, controle) + branches sont maintenant le standard documente pour TOUS les agents
6. ASCII strict valide sur demarrer.md + protocole (0 non-conforme)

## [NOTES] Correction ASCII 2026-08-07 -- demarrer.md (retour Janus)

**Correction** : 2 guillemets francais doubles non-ASCII a la ligne 13 de demarrer.md (detectes par le second controle Janus, VERDICT 9/10 NON CONFORME).
**Lecon** : quand j'ecris une citation entre guillemets dans un fichier du cerveau, utiliser TOUJOURS des guillemets ASCII ("...") et jamais les guillemets francais -- la regle ASCII est stricte et le controleur croise valider-conformite-ascii + detecter-usage-outils-externes.

## [NOTES] Rappel ASCII dans les parcours 2026-08-07 (demande utilisateur)

**Mission** : ajouter un indice regle ASCII dans CHAQUE case d'ecriture des parcours (jeu de piste) pour que l'agent voie la regle juste avant d'ecrire.
**Lecons** :
1. Les cases de type indice acceptent plusieurs indices dont regle : le rappel ASCII s'ajoute en TETE de la liste indices, avant l'outil d'ecriture, pour etre vu juste avant d'ecrire
2. Audit complet : passer en revue TOUTES les cases de type indice des 3 parcours (vulcain, morpheus, clio) -- 7 cases d'ecriture identifiees (vulcain c6/c12 deja couverts, morpheus c4/c8 et clio c6/c8/c10 a completer)
3. La modification d'un parcours JSON doit etre validee par --liste (structure) + --reponses (navigation inchangee) + valider-conformite-ascii (le JSON lui-meme doit rester ASCII)

## [NOTES] Parcours Janus 2026-08-07 (serie jeu de piste)

**Mission** : construire parcours-janus.json (3 chemins de controle) + fiche janus.md allegee v0.2.0.
**Lecons** :
1. Le parcours Janus couvre 3 missions distinctes (outil, statut, modification) via 3 branches de la case Mission -- un parcours peut porter PLUSIEURS missions, chaque chemin convergeant vers les cases communes (verdict, lecons, retour)
2. Les regles specifiques de l'agent deviennent des INDICES de case (Regle 1 : ecrire la mission avant de controler ; Regle 4 : signaler sans corriger) -- pas une section de la fiche
3. La fiche allegee garde : identite, regles absolues (y compris celles de l'agent), outils de base, RVAV, verdicts, connexions -- 0 mission detaillee (le guidage vit dans le JSON)
4. Validation : --liste (structure) + --reponses sur CHAQUE chemin (outil c1->c10, statut c11->c17, modification c18->c26) + ASCII 0 non-conforme

## [NOTES] Template fiche-agent v0.2.0 2026-08-07

**Mission** : mettre a jour fiche-agent-template.md selon le standard v0.2.0 (parcours = source de verite).
**Lecons** :
1. Le template a ete reecrit sur le modele des fiches allegees (morpheus.md) : frontmatter allege (SUPPRESSION carte_decision), section PARCOURS (SOURCE DE VERITE) a la place de CARTE DE DECISION, 0 mission detaillee (le guidage vit dans le JSON a construire)
2. Les regles absolues 1-6 restent (REGLE PARCOURS ajoutee + REGLE IMMUABLE ASCII avec rappel guillemets ASCII) -- le template integre maintenant le Pattern 2 de la spec v0.2.0 (rappel ASCII) directement
3. Un template obsolete fait naitre des fiches obsoletes : toute evolution de format (ici parcours v0.2.0) doit etre REPERCUTEE dans le template pour que les nouveaux agents naissent conformes
4. Validation : ASCII 0 non-conforme, 0 mission detaillee, PARCOURS present, version 0.2.0 coherente

## [NOTES] Parcours Cerberus 2026-08-07 (serie jeu de piste -- 5e parcours)

**Mission** : construire parcours-cerberus.json (23 cases, 4 chemins) + fiche cerberus.md allegee v0.2.0.
**Lecons** :
1. Le parcours du COORDINATEUR est un parcours de ROUTAGE : case Mission avec 4 branches (accueil, activation, retour, autre) menant aux chemins de coordination -- Cerberus ne execute pas, il active (les cases pointent vers activer-agent-principal)
2. Le chemin RETOUR est le plus riche : relire fiche/corrections -> lire raison -> liste definie (Janus ?) -> verdict -> fichiers changes (Clio ? avec anti-boucle) -> reprendre -- c'est le cycle fondamental entier transcrit en cases
3. Les regles de Cerberus deviennent des indices : NON-EXECUTION (jamais de commande d'analyse), ANTI-BOUCLE Clio (exclure fichiers Clio + rapports Janus), liste definie du second controle
4. La fiche allegee garde le cycle fondamental + la table des agents (sa valeur unique de coordinateur) -- le reste vit dans le JSON

## [NOTES] Parcours Buffy 2026-08-07 (serie jeu de piste -- 6e parcours, le mien)

**Mission** : construire parcours-buffy.json (36 cases, 6 chemins) + fiche buffy.md allegee v0.2.0.
**Lecons** :
1. MON parcours couvre 6 branches de la case Mission (creer, modifier, agent, protocole, controler, autre) -- le plus riche des parcours, car Buffy est l'agent qui ecrit le plus de fichiers du cerveau
2. Le Pattern 2 (rappel ASCII) s'applique FORTEMENT ici : 6 indices REGLE IMMUABLE ASCII dans les cases d'ecriture (creer c5, lecons c7, modifier c11, lecons c15, agent c20, protocole c25) -- Buffy est la principale productrice de fichiers, donc la principale cible de l'erreur ASCII
3. Les delegations sont des branches : pense-bete -> Athena (c17), outil -> Vulcain (c31) -- je n'ecris JAMAIS un outil ou un pense-bete moi-meme (REGLE DELEGATION)
4. La sous-mission est une case dediee (c32) avec le FLUX ORIENTE (sauvegarder -> sortir -> revenir) -- une sous-mission n'est jamais une fin

## [NOTES] Allegement demarrer.md + enrichissement destinations 2026-08-08

**Mission** : alleger demarrer.md (~180 -> ~45 lignes, porte d'entree uniquement) + enrichir protocole-identification (MODE ID v0.4.0) + index-cerveau.md (v0.3.0, protocoles cles + fichiers cles) + aligner convention-sous-protocoles.
**Lecons** :
1. demarrer.md ne doit servir QU A lancer le LLM, l identifier et devenir Cerberus : identification condensee + commande du parcours + pointeur vers index-cerveau.md -- tout le reste vit dans les protocoles et l index (le LLM se noie avec trop d information au demarrage)
2. AVANT de retirer une section de demarrer.md, verifier que sa destination absorbe reellement le contenu : protocole-identification couvrait les etapes 1-7 mais PAS le MODE ID multi-session (v0.4.0) -- la section a ete ajoutee EN TETE du protocole (pattern evolution, comme protocole-carte-decision)
3. Les references externes determinent ce qu on peut retirer : parcours-cerberus c11 cite la regle Reactiver Cerberus SANS lire = inutile en la rattachant a demarrer.md -- cette regle a ete CONSERVEE dans la version allegee
4. Un exemple pedagogique (convention-sous-protocoles section Dans demarrer.md) peut decrire une structure devenue fausse : verifier les fichiers qui citent demarrer.md par son nom lors d un allegement
5. L index-cerveau.md absorbe l inventaire (protocoles cles + fichiers cles) : l index = point d entree de la maison, demarrer.md = la porte
6. Validation : ASCII 0 sur les 4 fichiers + liens cites existants + regle c11 conservee + CASE 0 toujours presente

## [NOTES] Combo pilote combo-activation 2026-08-08 (etape 3 plan combo-orchestrateur)

**Mission** : creer le combo pilote combo-activation (sidentifier -> activer -> reactiver) au format definition-combo.json + le tester avec combos-moteur.
**Lecons** :
1. Une DEFINITION de combo est un FICHIER DU CERVEAU -> domaine Buffy (spec-combos-moteur ligne 184 : cerveau-projet/combos/), contrairement au MOTEUR (combos-moteur) qui est un OUTIL -> domaine Vulcain. Meme distinction que parcours (Buffy) vs guider-parcours (Vulcain)
2. Le cycle d'activation complet se decline en 8 cases : 3 generateurs (sidentifier/activer/reactiver) + 3 outils d'execution ({cmd1}/{cmd2}/{cmd3}) + 1 controle (OUI/NON, --reponses c3=OUI) + 1 fin -- le generateur AUTO compose les commandes exactes (quoter pour les raisons a espaces) et le moteur les execute
3. TEST SUR COPIES : ne JAMAIS executer le combo sur les vrais fichiers (il active/reactiverait la session reelle) -- copier AGENTS.md + AGENTS-historique.md + variables-actuelles.md dans /tmp/ et lancer avec AGENTS_FILE / AGENTS_HISTORIQUE / CLASSEUR_STOCKAGE (pattern des tests activer-agent-principal) ; verifier ensuite que la copie AGENTS.md passe de Cerberus -> agent -> Cerberus
4. PIEGE GREP : le champ Nom d'un bloc session est 4 lignes apres le marqueur ### Session -- grep -A 3 est trop court, utiliser -A 6 (deja documente par Morpheus : grep -A2 trop court)
5. Validation en 3 etapes : --liste (8 cases, structure), --dry-run (commandes affichees sans effet, navigation jusqu'a fin), execution reelle sur copies (cycle complet Cerberus -> Buffy -> Cerberus, historique + classeur mis a jour dans les copies)
6. Nettoyage : supprimer /tmp/combo-test apres le test pour ne laisser aucune trace

## [NOTES] Generalisation du Pattern 3 2026-08-08 (etape 6 plan combo-orchestrateur)

**Mission** : generaliser le Pattern 3 a tous les parcours (perimetre utilisateur : toutes les suites combinables) -- creer 4 combos et remplacer les suites d'outils repetees dans 3 parcours (janus, vulcain, buffy).
**Lecons** :
1. 4 combos crees (9 fichiers JSON au total dans cerveau-projet/combos/) : combo-controle-outil (4 cases, janus chemin outil), combo-controle-modification (10 cases, janus chemin modification : nommage-recursif -> liens -> separation -> sante -> tableaux -> surcharge -> traces), combo-corriger-ascii (4 cases, vulcain c7/c13), combo-sante-tableaux (6 cases, buffy chemin controler)
2. PARCOURS MODIFIES : janus 30->24 cases (c6-c7 et c23-c26 supprimes, recables vers c5/c22 combos), vulcain 19 (c7/c13 -> combo en place), buffy 36->34 (c29-c30 supprimes, c28 -> combo) -- chaque parcours passe en v0.2.0 avec mention Pattern 3 dans la description
3. PATTERN 3 CASE : une case combo garde la regle Pattern 3 en tete + l'outil combos-moteur (commande combos-moteur.py <definition>) + le fichier definition-combo.json -- les outils CONTEXTUELS (fichier precis de la mission) restent des indices de la case (valider-ebauche spec pour janus outil, verifier-role-fichier pour janus modification)
4. Les combos utilisent les DEFANTS DU CERVEAU (cerveau-projet, cerveau-projet/agents) comme cibles stables -- les commandes sont composees par le generateur AUTO pour les 4 commandes du catalogue utilisees (valider-nommage-recursif, combos-valider-cerveau, corriger-accents, audit-general deja utilise)
5. PIEGE RECABLAGE (deja note etape 5) : verifier suivant ET vers quand on supprime des cases -- c26->c8 et c7->c8 etaient les refs a conserver, les autres supprimees (grep refs mortes vide)
6. Validation complete : json.load 7 fichiers, combos-moteur --liste + --dry-run 4 combos (navigation jusqu a fin), guider-parcours --reponses sur 14 chemins (janus 4, vulcain 2, buffy 5, themis 3 deja) PARCOURS TERMINE, ASCII 0 sur 7 fichiers, parite py/sh 4/4
7. Les parcours NON transformables restent : cerberus (chemin retour = arbre de decision, pas une suite), morpheus (tester = protections chargees dans le test, pas des CLI), atlas/clio/athena/minerve/promethee (suites specifiques non repetees) -- le Pattern 3 s'applique aux SUITES LINEAIRES d'outils, pas aux decisions

## [NOTES] Pattern 3 dans parcours themis 2026-08-08 (etape 5 plan combo-orchestrateur)

**Mission** : integrer le Pattern 3 (spec v0.2.4) dans un parcours pilote -- remplacer la suite d'outils du chemin audit du parcours themis par Lancer le combo X.
**Lecons** :
1. PATTERN 3 VALIDE EN PRODUCTION : une case de parcours peut pointer vers un COMBO -- la case c3 reference combos-moteur (outil) + la definition du combo (fichier), avec un indice regle qui annonce le Pattern 3
2. COMBO THEMIS : combo-audit-themis (cerveau-projet/combos/) enchaine la suite d'outils du chemin audit (c3-c7) : 2 generateurs AUTO (audit-general, combos-valider-cerveau via le catalogue) + 4 outils directs (valider-relecture, valider-tableaux, detecter-local-hors-fonction, detecter-usage-outils-externes) + 1 fin = 9 cases
3. PIEGE RECABLAGE : en supprimant les cases c4-c7, TOUTES les references doivent etre recablees -- c19 (RVAV) pointait vers c4, recable vers c3 (le combo) ; verifier suivant ET vers (grep des refs avant/apres)
4. REDUCTION DU PARCOURS : themis passe de 24 cases a 17 (le chemin audit de 7 etapes devient c2 -> c3 combo -> c8 verdict) -- le combo rend le parcours plus digeste, exactement l'objectif
5. valider-nommage --type outil NE S'APPLIQUE PAS aux definitions-combo.json (fichiers JSON de definition, pas des outils .sh/.py/.md) -- valider une definition par json.load + valider-conformite-ascii + combos-moteur --liste + --dry-run
6. Le generateur AUTO compose les commandes exactes avec les defauts du catalogue (audit-general -> cerveau-projet, combos-valider-cerveau -> cerveau-projet/agents) ; la parite py/sh du moteur est conservee (PARITE OK)
7. Le combo est un FICHIER DU CERVEAU (domaine Buffy) qui consomme des outils du cerveau (domaine Vulcain) -- la distinction outil/contenu reste : le moteur et le catalogue sont restes INCHANGES

## [NOTES] Fiche vulcain v0.4.0 -- spec v0.2.3 + cas assume 2026-08-08

**Mission** : mettre a jour la fiche vulcain.md (reference spec v0.2.3 dans la section PARCOURS + ligne d'historique pour la decision du cas assume).
**Lecons** :
1. Quand une decision (cas assume) est documentee dans la spec et le rapport Themis, la FICHE de l'agent concerne (vulcain.md) doit aussi la porter : reference spec a jour + entree d'historique -- les 4 documents (spec, doc, rapport, fiche) racontent la meme histoire
2. La version de fiche propre de Vulcain (0.4.0) reste inchangee : on ajoute une entree d'historique, on ne rebumpe pas la version
3. Validation : ASCII 0 sur la fiche + presence ref (v0.2.3) + historique 2026-08-08 Decision utilisateur + CAS LEGITIME ASSUME

## [NOTES] Correction Pattern 2 -- minerve c8 + promethee c8 2026-08-08 (retour Themis)

**Mission** : corriger les 2 ecarts Pattern 2 detectes par l audit Themis de la serie des 11 parcours (rappel ASCII absent des cases de mise a jour d index).
**Lecons** :
1. L audit Themis a detecte ce que mes controles successifs avaient laisse passer : les cases minerve c8 (index-todo.md) et promethee c8 (index-spec.md) utilisent editer-fichier (ecriture) mais n avaient pas le rappel ASCII en tete de leurs indices -- la REGLE INDEX etait en position 1
2. Le Pattern 2 s applique a TOUTE case avec outil d ecriture (creer/ecrire/editer/ajouter-contenu-fichier), y compris les mises a jour d index -- pas seulement les cases de creation/remplissage
3. La correction est minimale : insertion de l indice regle ASCII en position 1 (texte uniforme identique aux autres cases), la REGLE INDEX passe en position 2
4. Revalidation complete : json.load OK, --liste 22, --reponses des 4 chemins (minerve/promethee x creer/completer) -> PARCOURS TERMINE, ASCII 0, verif structurelle premier indice = regle ASCII
5. Lecon processus : apres l audit Themis, TOUJOURS re-scanner la tete des indices des cases d ecriture de tous les parcours (script structurel) avant de declarer la serie conforme

## [NOTES] Parcours Atlas 2026-08-07 (serie jeu de piste -- 11e parcours)

**Mission** : construire parcours-atlas.json (29 cases, 5 branches de mission) + fiche atlas.md allegee v0.2.0.
**Lecons** :
1. Le parcours de l EXPLORATEUR est le PLUS COMPLET de la serie : la case Mission a 5 branches (explorer, web, documenter, analyser, autre) car la fiche Atlas porte 4 missions -- le Pattern 1 (multi-missions) pousse a son maximum
2. La signature d Atlas est la REGLE VALIDER AVANT DE MODIFIER (je ne modifie pas de fichiers sans validation explicite) : elle est en indice des 4 cases d ecriture (c9 documenter decouvertes, c14 documenter source, c18 creer structure, c19 rediger contenu, c25 cartographie) x5
3. Atlas ne delegue pas : la case FIN c11 REACTIVE CERBERUS (il rend le resultat de son exploration) -- contrairement a Athena (CHAIN Promethee) ou Promethee (FLUX Minerve)
4. Rappel ASCII x6 (Pattern 2) : les 5 cases d ecriture + la case lecons c10 -- l agent qui documente le plus apres Buffy
5. La mission web utilise un indice FICHIER (protocole-recherches-web) et non un outil : les missions a protocole s incarnent par des indices fichier
6. Validation : --liste (32 lignes) + --reponses sur les 5 chemins (explorer/web/documenter/analyser/autre OUI+NON) -> PARCOURS TERMINE, ASCII 0 non-conforme sur parcours + fiche
7. 11e parcours : la serie est COMPLETE - les 11 agents ont leur jeu de piste

## [NOTES] Parcours Athena 2026-08-07 (serie jeu de piste -- 10e parcours)

**Mission** : construire parcours-athena.json (21 cases, 3 chemins) + fiche athena.md allegee v0.2.0.
**Lecons** :
1. Le parcours de la REDACTRICE de pense-betes suit le meme patron que promethee/minerve (2 missions creer/completer, anti-doublon en premiere case) avec la signature CHAIN PROMETHEE : la case FIN active Promethee pour la spec (chain Athena -> Promethee -> Minerve) au lieu de reactiver Cerberus
2. Les regles propres d Athena sont des indices : STATUT EBAUCHE (je m arrete au statut ebauche, pas prepare) + SOUS-FICHIERS SUR DEMANDE (pas de spec/todo/liens sauf demande explicite) dans les cases RVAV (c8, c15) x4
3. Rappel ASCII x4 (Pattern 2) : squelette c4, remplissage c5, completer c14, lecons c9
4. Validation : --liste (22 lignes) + --reponses sur les 3 chemins -> PARCOURS TERMINE, ASCII 0 non-conforme sur parcours + fiche
5. 10e parcours : la serie est presque complete - il ne reste que Atlas

## [NOTES] Parcours Promethee 2026-08-07 (serie jeu de piste -- 9e parcours)

**Mission** : construire parcours-promethee.json (21 cases, 3 chemins) + fiche promethee.md allegee v0.2.0.
**Lecons** :
1. Le parcours du REDACTEUR de specs est structurellement identique a celui de Minerve (2 missions creer/completer, anti-doublon en premiere case) mais avec UNE DIFFERENCE CLE : la case FIN active MINERVE (FLUX Promethee -> Minerve pour le todo) au lieu de reactiver Cerberus -- le flux de delegation est incarne dans la structure
2. REGLE PENSE-BETE SOURCE : je ne cree pas de spec sans pense-bete source -- en indice de la case c3
3. Rappel ASCII x4 (Pattern 2) : squelette c4, remplissage c5, completer c14, lecons c9 -- meme volume d ecriture que Minerve
4. Validation : --liste (22 lignes) + --reponses sur les 3 chemins -> PARCOURS TERMINE, ASCII 0 non-conforme sur parcours + fiche

## [NOTES] Parcours Minerve 2026-08-07 (serie jeu de piste -- 8e parcours)

**Mission** : construire parcours-minerve.json (21 cases, 3 chemins) + fiche minerve.md allegee v0.2.0.
**Lecons** :
1. Le parcours de la REDACTRICE de todos couvre 2 missions (creer, completer) via les branches de la case Mission, convergeant vers les cases communes (lecons c9, retour c10) -- Pattern 1 applique
2. Les regles propres de Minerve sont des indices : PHASE 0 (activation agent adapte OBLIGATOIRE) + PHASE 9 (reactiver Cerberus OBLIGATOIRE) dans les cases de remplissage (c5, c14) + la case FIN c10 porte PHASE 9
3. ANTI-DOUBLON : rechercher-todos est l OUTIL de la premiere case de chaque chemin (c2, c11) -- la regle est incarnee dans la structure
4. Rappel ASCII x4 (Pattern 2) : squelette c4, remplissage c5, completer c14, lecons c9 -- Minerve ecrit des fichiers todo donc le rappel est proportionnel
5. Validation : --liste (22 lignes) + --reponses sur les 3 chemins -> PARCOURS TERMINE, ASCII 0 non-conforme sur parcours + fiche

## [NOTES] Parcours Themis 2026-08-07 (serie jeu de piste -- 7e parcours)

**Mission** : construire parcours-themis.json (24 cases, 4 chemins) + fiche themis.md allegee v0.2.0.
**Lecons** :
1. Le parcours de l EVALUATRICE croisee est un parcours de NON-EXECUTION : la REGLE ABSOLUE NON-EXECUTION (elle ne modifie JAMAIS rien, elle evalue et rapporte) est en indice des cases d evaluation et la case Verdict (c8) rappelle que le rapport est sa seule ecriture -- sauf rapport et lecons, aucun outil d ecriture dans le parcours
2. Les 4 branches de la case Mission (audit, doute, rvav, autre) convergent vers les cases communes : rapport c9, lecons c12, retour c13 -- le Pattern 1 (multi-missions + chemins convergents) est applique
3. Le doute d un agent est route vers le choix de l evaluateur adapte (c15 : structure/conventions/coherence/agents -> c16 qui liste les 4 evaluateurs) -- la specialite croisement de Themis est incarnee dans la structure
4. Le rappel ASCII (Pattern 2) est present x2 dans les cases d ecriture (rapport c9, lecons c12) -- Themis ecrit peu, contrairement a Buffy (x6)
5. Validation : --liste (24 cases) + --reponses sur les 4 chemins -> PARCOURS TERMINE, ASCII 0 non-conforme sur parcours + fiche

## [NOTES] Correction ASCII janus/corrections.md 2026-08-07 (pre-existant)

**Mission** : corriger les 3 caracteres non-ASCII pre-existants dans janus/corrections.md (cosmetiques + guillemets francais), signales par Janus lors du controle liste-parcours.
**Lecons** :
1. Quand on corrige des caracteres non-ASCII cites dans une MISSION d activation, ne jamais recopier les caracteres incrimines dans la raison : l outil activer-agent-principal REFUSE l activation si la raison contient un caractere non-ASCII (2 tentatives refusees pour cette raison exactement) -- decrire le caractere par son code (U+00AB/U+00BB) ou sans accent (cosmetiques)
2. Corriger un caractere non-ASCII = preserver le sens : cosmetiques -> cosmetiques (accent retire), guillemets francais -> formulation ASCII (caracteres U+00AB/U+00BB)
3. Validation : valider-conformite-ascii doit passer de 3 caracteres/2 lignes a 0 non-conforme

## [NOTES] Liste des parcours dans demarrer.md 2026-08-07 (synchronisation)

**Mission** : ajouter la liste des 6 parcours dans demarrer.md (case 0) + completer la doc guider-parcours.md.
**Lecons** :
1. demarrer.md (case 0) doit lister TOUS les parcours disponibles (vulcain, morpheus, clio, janus, cerberus, buffy) avec leurs chemins -- un LLM qui demarre voit immediatement si SON parcours existe
2. SOURCE DE VERITE PARTAGEE : toute creation de parcours (agents/<agent>/parcours/) doit mettre a jour 2 endroits : demarrer.md (case 0) ET guider-parcours.md (Emplacement des parcours) -- cerberus (5e) et buffy (6e) manquaient dans la doc, la liste a ete completee
3. La doc guider-parcours.md a ete bumpee en v0.2.1 (mise a jour de liste seulement, CLI inchangees) -- distinguer version doc vs version outil
4. ASCII strict valide (0 non-conforme) sur demarrer.md et guider-parcours.md

## [NOTES] Protocole-creation-combos 2026-08-08 (conventions de creation des combos)

**Mission** : creer le protocole + les conventions de creation des combos (decisions utilisateur : protocole dedie pense-bete+spec+todo + conventions dans la doc/spec du moteur, redacteur Buffy).
**Lecons** :
1. Deux niveaux documentaires : le protocole-creation-combos (cycle complet pense-bete + spec + todo dans regles-immuables/general/) porte le PROCESSUS (quand/ou/comment/valider), la spec-combos-moteur porte le FORMAT (le QUOI) -- complement, pas doublon
2. La distinction OUTIL vs DEFINITION est la cle : agents/tools/combos/ = OUTILS (moteur + combos executables .py/.sh, domaine Vulcain) ; cerveau-projet/combos/<nom>/definition-combo.json = DEFINITIONS (fichiers du cerveau, domaine Buffy) -- la doc moteur citait 2 emplacements ambigus, corrigee vers l'emplacement canonique unique
3. Les conventions de facto des 6 combos sont figees : nommage combo-<action> (dossier = champ nom), cases c1..cn, titres Generer la commande X / Executer X / FIN - resume, sorties cmd1.. / resultat_<action>, cibles par defaut cerveau-projet/agents (validation) ou cerveau-projet (audit), version 0.1.0, outils contextuels EXCLUS (indices de la case du parcours)
4. Les regles de decision (quand creer) : suite LINEAIRE repetee (>=2) ou longue (>=3) -> OUI ; arbre de decision (cerberus retour) -> NON ; protections embarquees dans un test (morpheus) -> NON ; suite specifique non repetee (redacteurs) -> NON
5. PIEGE CHEMINS RELATIFS : le niveau de remontee depend du dossier du fichier -- protocole dans protocole-creation-combos/ (3 x ../ vers pense-betes), spec dans spec/ (1 niveau de plus), spec-combos-moteur dans agents/tools/combos/combos-moteur/spec/ (5 x ../ vers la racine) -- valider TOUJOURS avec valider-liens --racine . apres creation (6 liens protocole, 7 liens spec : 5 etaient faux)
6. PIEGE ASCII REPETITIF : ecrire en ASCII des le depart ; j ai introduit 3 accents (enchaine x2, coherent, traceable, Eleve) malgre la regle -- verifier avec valider-conformite-ascii avant de declarer termine

## [NOTES] Regle CITER le combo avant de le lancer 2026-08-08 (tracabilite)

**Mission** : regle de tracabilite -- l'agent qui lance un combo doit le CITER avant de l'executer (decision utilisateur : source de verite dans protocole + spec/doc moteur, rappel dans les 6 cases combo des parcours).
**Lecons** :
1. DOUBLE ANCRAGE d'une regle de comportement : la source de verite (protocole-creation-combos 9.5 + spec-combos-moteur + doc 0.1.2) documente la regle ET le rappel est en TETE des indices des cases combo (themis c3, janus c5/c22, vulcain c7/c13, buffy c28) -- l'agent voit la regle juste avant de lancer, meme principe que le rappel ASCII (Pattern 2)
2. La formulation de citation est uniforme : Je lance le combo <nom> : <chemin> - il enchaine <outils>. -- la commande combos-moteur seule ne revele pas le nom du combo, la citation cree la tracabilite pour l'utilisateur, Cerberus et Janus
3. L'indice CITER est insere en POSITION 1 des indices (avant PATTERN 3) -- comme le rappel ASCII, la regle critique est vue en premier
4. La spec du protocole porte la regle en EX-09 (citation obligatoire avant lancement) et le flux 5.4 mentionne l'indice CITER en tete -- spec et protocole racontent la meme histoire
5. Validation : json.load 4 parcours, ASCII 0 sur 8 fichiers, 6/6 chemins PARCOURS TERMINE (navigation inchangee), liens 0 invalide

## [NOTES] Relecture en QUESTION HONNETE 2026-08-08 (decision utilisateur)

**Mission** : transformer la REGLE DE RELECTURE (exiger une lecture) en QUESTION HONNETE que l agent se pose (verifier la memorisation) avec reponses + actions obligatoires.
**Lecons** :
1. Le probleme de la regle ancienne : exiger une LECTURE ne prouve PAS la MEMORISATION -- un LLM peut avoir lu un fichier et ne plus rien en restituer. La regle nouvelle pose la question : As-tu EN MEMOIRE ta fiche et tes corrections, capables de les appliquer SANS relire ? -- seul OUI (veracite) continue
2. DESIGN DE LA CASE : c0 (question, branches OUI -> c1 mission / INCERTAIN -> c0b / NON -> c0b) + c0b (indice RELIRE OBLIGATOIRE : corrections puis fiche, puis -> c1) -- inseree en TETE des 11 parcours avec case_depart c1 -> c0
3. LA NAVIGATION PROUVE LA LOGIQUE : OUI -> mission directement ; NON -> passe par c0b (relire) puis mission ; INCERTAIN idem -- la relecture est DECLENCHEE PAR LA REPONSE, plus jamais imposee aveuglement
4. PIEGE TEST CHEMIN : les chemins avec etapes supplementaires (clio corriger : question ecarts, morpheus tester : question delegation VULCAIN/CERBERUS) s arretent en attente de reponses -- ce n est pas une erreur, c est le comportement normal du guide ; compter les questions reelles avant de conclure a un echec
5. DOUBLE ANCRAGE conserve : question dans les parcours (c0, operationnel) + regle dans demarrer.md (section 2), protocole-activation (etape 3), les 11 fiches et le template -- meme formulation partout
6. Validation : json.load 11 parcours, navigation OUI/NON/INCERTAIN sur les chemins cles, ASCII 0 sur 25 fichiers, liens 0 invalide

## [NOTES] Cerberus = ORCHESTRATION UNIQUEMENT 2026-08-08 (decision utilisateur)

**Mission** : figer dans protocole-activation la regle Cerberus = orchestration uniquement -- la todolist de Cerberus ne contient que la coordination, les etapes internes de l agent vivent dans SA carte de decision (son parcours JSON).
**Lecons** :
1. LE PROBLEME DETECTE PAR L UTILISATEUR : quand Cerberus detaille dans sa todolist les etapes internes de l agent (relire fiche, lire spec, editer, valider...), la carte de decision de l agent devient DECORATIVE -- il n a plus qu a suivre la liste de Cerberus au lieu de suivre SON parcours
2. LA REGLE : Cerberus donne la MISSION (le quoi + le pourquoi + les criteres de validation), jamais le comment. Quand l agent est active, il REPREND LE CONTROLE en lancant SON parcours (guider-parcours.py parcours-<agent>.json) -- SA carte de decision le guide case par case (indices outil/fichier/regle + branches)
3. ANCRAGE DANS protocole-activation : etape 5 du cycle precissee (Agent execute sa mission en lancant SON parcours) + nouvelle section Etape 5 dediee (la reponse a la question comment l agent reprend le controle + tableau todolist Cerberus = orchestration uniquement) + Regle d Or (Cerberus = orchestration) + Piege (todolist qui detaille les etapes internes rend la carte inutile)
4. LA TODO LIST DE CERBERUS = 4 etapes max : analyser/choisir l agent, activer, second controle Janus si liste definie, bilan/cloture -- les etapes internes ne s y trouvent JAMAIS
5. Validation : ASCII 0 sur le protocole, presence Etape 5 + regle d or + piege verifiee

## [LECON] 2026-08-08 -- GARDE-FOU RESTAURATION : interdiction de git checkout/restore/reset --hard sur fichiers NON COMMITES

**Mission** : inscrire dans les protocoles le garde-fou issu de l incident piste B (un git checkout de restauration avait ecrase les modifs non commitees de la piste B).
**Resultat** : 2 emplacements complementaires (regle courte + procedure) : (1) regles-general-global.md -> ligne Restauration securisee ajoutee au tableau des regles globales (apres Perimetre workspace) ; (2) protocole-gestion-defaillances.001.01.ebauche.md -> bloc Regle de restauration (IMMUABLE -- lecon incident piste B) dans Etape 3 -- Corriger la defaillance : INTERDIT checkout/restore/reset --hard si modifs non commitees, OBLIGATOIRE git status avant, METHODE SURE = sauvegarde (cp) ou git stash, restauration depuis sauvegarde du workspace.
**Lecons** :
1. LE GARDE-FOU A DEUX NIVEAUX : une regle courte dans le tableau global (visible, memoire immediate) + une procedure detaillee dans le protocole (action en contexte de defaillance) - coherant avec l approche multi-couches du cerveau (regle globale > protocole).
2. EMPLACEMENT DU PROTOCOLE : protocole-gestion-defaillances Etape 3 (Corriger la defaillance) est le bon endroit car la restauration EST une correction de defaillance - pas protocole-auto-correction (qui couvre le cycle agent, pas la restauration de fichiers).
3. VALIDATION : ASCII 0 sur les 2 fichiers, rendu des tableaux coherent, index-regles-general reference deja les 2 fichiers (aucun index a mettre a jour).
4. La regle est redigee en ASCII strict, sans guillemets francais, avec les commandes git entre backticks pour la lisibilite.

## [LECON] 2026-08-08 -- REPARATION PISTE B : indices PASSE PAR LE GENERATEUR restaures dans les 11 parcours (apres perte par git checkout)

**Incident** : lors de la piste C volet 2, un git checkout de restauration (apres erreur JSON d insertion) a ecrase les modifications NON COMMITEES de la piste B - 0 regle, 0 indice generateurs-commande dans les 11 parcours (verifie avant reparation).
**Reparation** : script d edition chirurgicale ligne par ligne (jamais json.dump de reformatage) : pour chaque parcours, insertion en TETE des indices de la case cible (celle qui lance une suite d outils) d une paire (1) regle PASSE PAR LE GENERATEUR : compose la commande de l outil via le catalogue (--commande NOM --reponses ...) + (2) outil generateurs-commande avec nom, catalogue: generateurs-commande, chemin, commande d exemple CIBLEE sur l outil de la case. Versions patch +1 par parcours (athena 0.1.0->0.1.1, vulcain 0.2.1->0.2.2, etc.).
**Lecons** :
1. INCIDENT GIT : NE JAMAIS restaurer par git checkout des fichiers NON COMMITES - verifier git status AVANT toute restauration ; si des modifs non commitees existent, les sauvegarder d abord (cp dans un dossier temp) ou utiliser git stash. La piste C a ete sauvegardee (cp) avant reparation pour ce meme risque.
2. CIBLES CONFIRMEES par la lecon d origine : athena c4 (generer le squelette), vulcain c2 (verifier le systeme), themis c16 (lancer l evaluateur adapte). Pour les 8 autres, critere documente applique : la case qui lance une suite d outils, avec ajustements verifies par le catalogue (morpheus c4 creer-fichier car c6 tester-protection-* est un pseudo-outil ABSENT du catalogue).
3. FORMAT v0.2.20 : l indice outil porte maintenant le champ catalogue: generateurs-commande en plus de nom/chemin/commande - le moteur affiche la ligne catalogue + PASSE PAR LE GENERATEUR automatiquement.
4. VALIDATION COMPLETE : json.load 11/11, navigation --reponses 11/11 PARCOURS TERMINE, affichage [REGLE] PASSE PAR LE GENERATEUR verifie sur athena + vulcain, ASCII 0/11, valider-cartes --tous 11/11 CONFORME, diff minimal 12+ par fichier (11 lignes indices + 1 version).
5. LE COMPTAGE VALIDE : exactement 11 regles + 11 indices generateurs-commande (un par parcours) - la trace AGENTS-historique (lignes 21-22) a permis une reparation a l identique.

## [LECON] 2026-08-08 -- VAGUE 3 : migration du reste du cerveau (schema hybride complet)

**Tache** : appliquer la migration vers le schema hybride sur tout le cerveau hors agents/tools/ (decision utilisateur, outil migrer-identite v0.2.1 valide par Morpheus).
**Lecons** :
1. La verification Cerberus prealable a revele 2 limites de la cartographie avant l'application : (L1) BRUIT des traces historisees (controles/rapports/retro-actions jamais a jour) faussant le verdict -> detecter-impacts v0.2.1 les marque [HISTORISE] et les exclut du verdict ; (L2) fichiers racine non migres (AGENTS.md etait REFUSE par detecter-impacts) -> migrer-identite v0.2.0/v0.2.1 les couvre (types racine, historique, classeur, pense-bete, template, note)
2. Le dry-run reel AVANT application a revele 4 cas que le mini-cerveau ne couvrait pas : definition-combo.json du dossier combos/ (type combo par dossier, pas seulement prefixe), exemples/ et recherches-web/ (test pollue + recherches jamais a migrer), sauvegardes/ (artefacts), AGENTS-historique.md (journal -> type historique)
3. APPLICATION RELLE : 21 fichiers migres dans cerveau-projet/ (5 notes vulcain appartient_a=vulcain, 5 classeur, 7 combos, 3 templates, 1 pense-bete) + AGENTS.md (racine) + AGENTS-historique.md (historique) -> 0 erreur, idempotence 0 migre au re-scan
4. VERIFICATION BOUT EN BOUT : detecter-impacts lit l identite sur tous les nouveaux formats (note, combo, racine), ASCII 0 sur le perimetre migre, et le cas reel final montre 20 traces [HISTORISE] exclues du verdict
5. La cartographie des impacts est desormais COMPLETE : chaque fichier du cerveau porte son identite, detecter-impacts peut cartographier de bout en bout (modifier un outil -> famille + references vivantes, sans bruit des traces datees)

## [NOTES] Convention identification v0.5.0 -- migration des fiches (2026-08-08)

**Mission** : appliquer la convention 'aucun mot seul' aux fichiers du cerveau (outils valides Morpheus).
**Migration reelle** :
1. 11 fiches agents (agents/<a>/<a>.md) : agent.nom -> agent.nom-agent, agent.statut -> agent.statut-<a>
(ex: statut-cerberus), profil.role -> profil.role-agent -- role_principal et role_specifique INCHANGES
2. 2 templates (fiche-agent-template, corrections-template) : memes renommages, statut-[nom-agent]
3. 11 corrections.md : agent.nom -> agent.nom-agent (morpheus/themis sans champ -> inchange)
4. parcours-demarrage.json : references champ Id LLM -> Nom LLM (case c2)
5. protocole-identification (regle immuable) : references Id LLM -> Nom LLM (lecture retrocompat notee)
**Validation** : lister-agents v0.3.0 lit les nouveaux champs, statut-<agent> present dans les 11 fiches,
nom-agent dans 20 fichiers, ASCII 0 sur le perimetre, detecter-impacts lit l identite des fiches
**Lecons** :
1. La migration ciblee au frontmatter (script) preserve le corps markdown des fiches -- ne jamais
sed global sur un fichier markdown (risque de casser le texte)
2. Les corrections morpheus/themis utilisent agent: "x" (deja qualifie) ou pas de champ -- verifier
le format reel avant de migrer, ne pas supposer que toutes les corrections ont nom:
3. Les traces historiques (corrections.md, notes mission) documentent l ANCIEN format -- on ne les
modifie pas (temoignage de l evolution), seuls les fichiers ACTIFS sont migres
4. PILOTE TAGS (2026-08-08) : la cle `tags:` se place dans le frontmatter `identite:` APRES `commun:`
(avant les commentaires de la fiche). Les tags viennent du VOCABULAIRE CONTROLE de convention-tags.md
(kebab-case ASCII, singulier, 2-5 par fichier). 17 fichiers pilotes : 6 outils de validation
(validation + theme propre + communs) et 11 fiches agents (categorie agent + transverses).
Verifier avec `lister-outils --tag <tag>` / `lister-agents --tag <tag>` que le filtre fonctionne.
5. REGLE WORKSPACE (2026-08-08, IMMUABLE) : l'ecriture se fait UNIQUEMENT dans le workspace
(Z:/analyste-in-console). JAMAIS de fichier temporaire hors workspace (Z:/tmp, /tmp systeme).
Les scripts temporaires se creent DANS le workspace (ex: .tmp-test/) puis se suppriment.
La sortie du workspace n'est autorisee qu'en LECTURE. Faute grave commise et corrigee
(nettoyage de Z:/tmp) - regle inscrite dans regles-perimetre-workspace.md.
6. ASCII 2 ALTERNATIVES (2026-08-08) : a la verification, [OK] aucun non-ASCII -> continuer /
[NON] non-ASCII detecte -> LANCER LE COMBO combo-corriger-ascii (jamais corriger soi-meme).
Le combo enchaine corriger-accents --all --recursive + valider-conformite-ascii.
Rappel insere en tete des cases d'ecriture des 10 parcours (32 cases).

## [NOTES] CHAINE BOUT-EN-BOUT + REGLES IMMUABLES 2026-08-08 (Pattern 8, decision utilisateur)

**Mission** : corriger le constat utilisateur (RVAV absent des generateurs 0 occurrence -> nouvelles cartes/cases sans regles immuables ; delegation court-cuitee : tests faits par l agent au lieu de Morpheus, Janus jamais active) par (1) la CHAINE DE DELEGATION BOUT-EN-BOUT et (2) les REGLES IMMUABLES dans les generateurs, puis re-audit Themis.
**Lecons** :
1. CHAINE BOUT-EN-BOUT (Pattern 8, spec-guider-parcours v0.2.15) : la delegation ne repasse PLUS par Cerberus au milieu -- Cerberus active Vulcain -> Vulcain finit et ACTIVE Morpheus -> Morpheus finit et ACTIVE Janus -> Janus REACTIVE Cerberus avec le BILAN CONSOLIDE. Decision utilisateur : c est l agent delegue qui active le suivant a SA fin, pas Cerberus (plus fiable que la boucle Vulcain -> Morpheus -> Vulcain puis Cerberus).
2. RVAV A CHAQUE MAILLON : chaque agent passe la boucle RVAV (Rechercher, Verifier, Analyser, Valider) sur SON travail AVANT d activer le suivant -- case c7b/c13b ajoutee dans parcours-vulcain (RVAV avant activation), indice RVAV en tete de c9 janus.
3. PARCOURS MODIFIES : vulcain 30->24 cases (c9a/c9b/c9c + c15a/c15b/c15c RELAIS/RETOUR/CLOTURE supprimes, branches c8/c14 OUI -> fin directe, fins c9/c15 = MORPHEUS ACTIVE) ; morpheus (c10 FIN Activer Vulcain -> FIN Activer Janus avec le rapport, c9 regle chaine) ; janus (c9 RVAV avant reactivation + c10 bilan consolide) ; cerberus (c7 flux chaine bout-en-bout).
4. GENERATEURS PORTEURS DE REGLES : generateurs-case v0.2.1 (garde-fou non bloquant RVAV + delegation + ASCII : cases d ecriture sans rappel ASCII position 1 -> RAPPEL ASCII + RVAV ; fins de delegation -> RAPPEL DELEGATION chaine bout-en-bout) + generateurs-carte v0.1.1 (squelette c2b RVAV avant fin + rappel ASCII dans c2 + fin c9 chaine bout-en-bout).
5. PIEGE ASCII RECURRENT (encore !) : j ai introduit nait/naitront (i circonflexe) dans les lecons vulcain et themis -- corrige avec l OUTIL corriger-dictionnaire-accents (jamais a la main, regle utilisateur) qui cree un .bak (a supprimer). La regle utilisateur : au moment de la verification ASCII, 2 alternatives (OK continuer / NON lancer l outil de correction), jamais de correction manuelle.
6. AUDIT STRUCTUREL vs CROISE : le premier script d audit (detecteur trop strict exigeant le prefixe exact REGLE IMMUABLE ASCII et 'memoire' en minuscules) a produit 29 faux ecarts -- les parcours portent REGLE WORKSPACE ... ASCII 2 ALTERNATIVES en position 1 (rappel ASCII present) et MEMOIRE en majuscules. Toujours verifier un echantillon manuel avant de declarer des ecarts : re-audit final = 11/11 OK, 0 ecart.
7. Le rapport Themis (corrections.md Themis) documente le verdict CONFORME : 8 procedures rejouees (1, 2, 3, 4, 4b, 4d, 4e, 4f), chaine bout-en-bout verifiee sur vulcain/morpheus/janus/cerberus.

## [NOTES] LIRE LE .MD AVANT UTILISATION 2026-08-08 (Pattern 9, decision utilisateur)

**Mission** : corriger le constat utilisateur (les agents se posent souvent des questions de fonctionnement avant d'utiliser un outil alors que chaque outil a son .md) par le Pattern 9 LIRE LE .MD AVANT DE L UTILISER, portee SYSTEMATIQUE, ancrage TRIPLE.
**Lecons** :
1. CONSTAT VERIFIE : 193 indices outil dans les 11 parcours, tous les .md existent (sauf motifs joker tester-protection-*), mais AUCUN parcours ne demandait de lire la doc avant execution -- guider-parcours affichait OUTIL/chemin/commande sans invitation a lire le .md. L'agent voyait le QUOI (commande) mais pas le COMMENT (options, pieges, exemples du .md).
2. ANCRAGE TRIPLE (decision utilisateur) : (a) regle de format dans la spec (Pattern 9, v0.2.16) ; (b) AFFICHAGE AUTO guider-parcours v0.3.0 -- afficher_indices ajoute la ligne LIRE AVANT USAGE : <outil.md> deduite du chemin (dossier + nom + .md, ou remontee au dossier si chemin .py/.sh) pour CHAQUE indice outil, couvre les 193 existants SANS les modifier ; (c) GENERATION AUTO generateurs-case v0.2.2 -- un --indice-outil ajoute automatiquement l'indice fichier .md (si la doc existe) avec la raison LIRE AVANT USAGE (Pattern 9), couvre les futures cases.
3. CONVERSION .sh EN WRAPPER PUR : guider-parcours.sh etait un heredoc complet (ancien pattern) avec le code python duplique -- le .sh affichait encore v0.2.0 pendant que le .py passait en v0.3.0 (divergence de version). Converti en wrapper pur (exec python3 guider-parcours.py "$@") : parite garantie PAR CONSTRUCTION, plus jamais de doublon de logique ni de divergence de version.
4. PIEGE DEDUCTION DU .md : le chemin d'un indice outil peut pointer vers un DOSSIER (se termine par /) ou vers un FICHIER (.py/.sh) -- la deduction doit gerer les 2 cas (dossier -> dossier + nom + .md ; fichier -> remonter au dossier + nom + .md). Le .md est VERIFIE (Path.is_file()) : s'il existe, chemin exact ; sinon mention 'doc a verifier'.
5. PIEGE ASCII REPETITIF (encore) : la spec v0.2.16 a recu 1 caractere non-ASCII (detecte par valider-conformite-ascii) -- corrige par l OUTIL corriger-dictionnaire-accents (jamais a la main, regle utilisateur 2 alternatives) ; .bak cree puis supprime.
6. RE-AUDIT COMPLET (regle v0.2.7) : le Pattern 9 passe la procedure d'audit de 8 a 9 patterns (procedure 4g ajoutee : moteur >= v0.3.0 affiche LIRE, generateur >= v0.2.2 ajoute l'indice .md, chaque .md deduit existe sauf jokers) + critere d'acceptation 20.
7. La navigation est INCHANGEE (les 4 parcours de la chaine + cerberus accueil/retour PARCOURS TERMINE) : l'affichage ajoute une ligne informative, ne change aucune branche.

## [NOTES] 2026-08-08 -- Constat stabilite des cartes de decision (mission Buffy)

**Mission** : analyser la stabilite des 11 cartes de decision (constat utilisateur : plus on avance, plus elles deviennent instables, contenu qui se deteriorerait).
**Constats (preuves, outils du cerveau uniquement) :
1. STRUCTURELLEMENT VALIDES : valider-cartes-decision --tous = 11/11 CONFORME ; generateurs-carte detecter = 0 anomalie sur les 11 (references, boucles, impasses, cases inatteignables). La deterioration n est PAS visible par les outils de validation : les JSON sont sains.
2. LA DERIVE EST COMPORTEMENTALE, pas structurelle : les cas recents de violation (Vulcain reactive Cerberus au lieu d activer Morpheus, Cerberus analyse lui-meme au lieu d activer Buffy) viennent de l EXECUTION de la carte, pas du contenu du JSON. La carte dit une chose, l agent en fait une autre.
3. COMPLEXITE CROISSANTE : taille moyenne 25 cases (19 a 43) ; buffy 43 cases / 21 outils references, atlas 32/15 -- les cartes GROSSISSENT avec les patterns accumules (9 patterns) et les cas particuliers (deviations c12a/b/c, c13b/c/d, c10b, c34b). Plus une carte est grosse, plus la surface de derive est grande : plus de cases = plus de chances qu un agent saute une etape ou se perde.
4. CARTE DE CERBERUS = ROUTEUR : ses 5 outils sont tous des outils de COORDINATION (lister-agents, lister-outils, lire-fichier, lire-activite-recente, activer-agent-principal) -- la carte est structurellement un routeur, MAIS les cases c3/c4/c8/c9 (lister/lire pour choisir) sont celles qui ont glisse vers l analyse : lire pour choisir devient lire pour executer. Le risque est dans ce glissement, pas dans la carte.
**Recommandations structurelles (a valider avec l utilisateur) :
1. FIGER la regle : une carte = ROLE, pas de la technique. Cerberus ne devrait contenir QUE des cases activer/verifier/decider (jamais d outil d analyse). Buffy/agents = les outils d execution.
2. ALLEGER les cartes : sous 25 cases idealement (les combos Pattern 3 servent a ca : une suite d outils devient UNE case Lancer le combo X). Buffy a 43 cases = la premiere candidate a la decomposition.
3. RENFORCER le garde-fou d execution : chaque carte (ou le generateur) rappelle la regle TU ACTIVES L AGENT, TU N EXECUTES PAS - sauf pour les outils de SON role.
4. La stabilite d une carte ne se mesure PAS par detecter (0 anomalie) mais par la CONFORMITE D EXECUTION (l agent a-t-il fait ce que la carte ordonnait ?) -- ajouter ce critere aux audits Themis.

## [NOTES] 2026-08-08 -- Pattern 10 UNE CARTE = UN ROLE (purge carte Cerberus + spec v0.2.18)

**Mission** : figer la regle une carte = un role (decision utilisateur) : purger la carte de Cerberus de toute case d analyse/execution, garder uniquement activer/verifier/decider.
**Lecons** :
1. LA DERIVE N EST PAS DANS LE JSON MAIS DANS L INTENTION : les cases lister/lire de la carte de Cerberus (c3 lister-agents, c4 lister-outils, c8 verifier, c9 lire la fiche de l autre, c12 lire la raison) etaient structurellement de la coordination, MAIS elles glissent de lire pour choisir vers lire pour executer. La purge retire les vraies cases d analyse : c4 lister-outils (analyse du cerveau, role Vulcain/Buffy) et c9 lire la fiche de l AUTRE agent (contredit la regle de relecture : chacun lit SES fichiers en prenant le relais). c12 transformee : l outil lire-fichier retire, remplace par une regle de role (lire pour DECIDER, pas pour executer).
2. OUTIL DE REFERENCE : les suppressions/editions passent par generateurs-case (recablage auto + validation auto json/references/guider-parcours --liste) -- c4 supprimee (c3 -> c5 auto), c9 supprimee (c8 -> c10 auto), c12/c16 editees via --indice-regle (remplace les indices, y compris les outils). RESULTAT : 29 -> 27 cases, outils restants = coordination pure (activer-agent-principal, lister-agents, lire-activite-recente, lire-fichier uniquement en c0b RELIRE = SES fichiers).
3. SPEC v0.2.18 : Pattern 10 documente (une carte = le role de l agent, tableau des roles, 5 regles dont le PIEGE DU GLISSEMENT lire pour decider vs lire pour executer, exemple JSON c2 routeur) + procedure d audit 4h (lister les outils par carte, verifier l appartenance au role, cas Cerberus routeur pur) + critere d acceptation 21 + re-audit complet passe de 9 a 10 patterns (4c et regle de re-audit mises a jour).
4. PIEGE TEST : la navigation apres purge doit couvrir TOUS les chemins restants (accueil 4 reponses, activation 4, retour 5, autre 3) -> 4/4 PARCOURS TERMINE ; valider-cartes-decision --agent cerberus CONFORME ; generateurs-carte detecter 0 anomalie ; ASCII 0 sur spec + carte.
5. LA REGLE A UNE DOUBLE PORTEE : (a) les cartes EXISTANTES (purge au cas par cas), (b) les FUTURES cartes (le generateur generateurs-carte creer doit integrer la regle dans le squelette -- prochaine evolution).

## [NOTES] 2026-08-08 -- Alleger la carte de Buffy (combo-corriger-fichier, Pattern 3)

**Mission** : alleger la carte de Buffy (43 cases, la plus grosse) en remplacant les suites d outils par des cases Lancer le combo X (Pattern 3, decision utilisateur suite au constat stabilite des cartes).
**Lecons** :
1. IDENTIFIER LA VRAIE SUITE MECANIQUE : dans la carte de Buffy, la seule suite d outils PUREMENT sequentielle et reutilisable est c12+c13 (corriger-nommage -> corriger-liens -> corriger-emojis -> corriger-accents-zones-sensibles -> condenser-fichier -> nettoyer-fichier) : 6 outils sur le MEME fichier, sans decision entre eux. Les autres chemins (creer/agent/protocole) ont des DECISIONS et des etapes manuelles (index, AGENTS.md) : les encapsuler perdrait la guidance -- ne PAS toucher (la guidance est la valeur d un chemin de creation).
2. COMBO CREE : combo-corriger-fichier v0.1.0 (definition-combo.json 7 cases : 6 outils + fin, variable {fichier} --var fichier=<chemin>, format identique a combo-controle-impacts) + doc .md. Verifie : combos-moteur navigation COMBO TERMINE.
3. RECABLAGE VIA GENERATEURS-CASE : supprimer c13 (c12 -> c13b auto), supprimer c12 (c10c ET c11 -> c13b auto), ajouter c37 Lancer le combo corriger-fichier apres c10c (c10c -> c37 -> c13b), PUIS REORIENTER c11 -> c37 (sinon le chemin editer-fichier contourne le combo). PIEGE : apres une suppression double, les 2 references (c10c, c11) sont recablees vers la MEME case (c13b) -- verifier et reorienter chaque branche.
4. RESULTAT : 43 -> 42 cases (6 outils -> 1 case). Gain modeste mais la reduction de SURFACE est reelle : le chemin modifier passe de 2 cases d outils a 1 case de combo. L objectif sous 30 cases exigerait d encapsuler les chemins de creation (a faire avec soin, guidance a preserver) ou de fusionner des missions.
5. CONFORMITE PATTERN 3 + 9 + 10 : la case c37 porte la regle de TRACABILITE (citer le combo avant de le lancer) + PATTERN 3 (spec v0.2.18) + outil combos-moteur + indice fichier definition-combo.json (Pattern 3) ; LIRE AVANT USAGE affiche la doc du moteur (Pattern 9) ; les outils du combo sont du DOMAINE de Buffy (corriger/condenser/nettoyer = fichiers du cerveau, Pattern 10).
6. VALIDATIONS : navigation 8/8 PARCOURS TERMINE (dont les 2 branches du chemin modifier), valider-cartes-decision --tous 11/11, detecter 0 anomalie, ASCII 0 (carte + combo json/md + index), index-tools mis a jour (section Combos + compteur 11 -> 12 + note 100 -> 101).

## [LECON] 2026-08-08 -- Encapsulation des chemins de creation (combo-creer-*, Pattern 3 + guidance)

**Tache** : encapsuler les 3 chemins de creation de MA carte (creer, agent, protocole) dans des combos EN PRESERVANT la guidance par des cases controles (decision utilisateur : la premiere vague d allegement avait conserve ces chemins pour leur guidance, maintenant on encapsule SANS perdre la guidance).
**Lecons** :
1. LA GUIDANCE RESTE DANS LA CARTE, LE MECANIQUE VA DANS LE COMBO : les etapes PUREMENT MECANIQUES (valider-nommage, valider-conventions, rechercher-fichier, creer-fichier, copier-fichier, copier-dossier) sont encapsulees dans les combos ; les POINTS DE CONTROLE (index manuel, AGENTS.md manuel, RVAV controle) restent des cases de la carte -- la carte reste un parcours GUIDE, le combo fait le travail repetitif. Resultat : creer (c1->c2c combo->c6 index->c7 lecons->c8), agent (c1->c18c combo->c21 AGENTS.md->c22), protocole (c1->c23c combo->c26 RVAV->c27) -- 42 a 35 cases.
2. LES COMBOS PEUVENT PORTER LEURS PROPRES CASES CONTROLE : chaque combo-creer-* a une case controle interne (OUI/NON) qui verifie une etape avant de continuer (c4 nommage+structure OK ? / c2 nom valide ? / c2 convention respectee ?) -- la guidance peut vivre DANS le combo pour les verifications mecanisables, et dans la carte pour les etapes manuelles.
3. FORMAT definition-combo.json : bloc combo DOIT porter `case_depart` (sinon ERREUR case_depart manquant), cases type outil (commande avec interpolation {var}, sortie, suivant), controle (question + branches), fin (message). Les commandes d outils directs s ecrivent en dur avec {var} (valider-nommage {chemin}) sans passer par le generateur si la commande n est pas au catalogue.
4. PIEGE RECABLAGE (deja note) : ajouter --apres recable QUE le champ suivant -- apres ajout de c2c, c3/c4/c5 sont orphelins (plus personne ne pointe vers eux), il faut les supprimer en CASCADE (c5, c4, c3, c2) pour que le recablage enchaine proprement vers la cible de guidance (c6).
5. PIEGE BOUCLE RVAV : apres suppression de c25, la branche NON de c26 (RVAV) a ete recablee vers c26 LUI-MEME (boucle d attente, regle 10) -- corrige par editer --branche NON:c23c (relancer le combo = boucle de CONTROLE/re-travail autorisee, pas une attente). TOUJOURS verifier les branches des controles apres une suppression en cascade.
6. PIEGE CLI generateurs-case : `editer` NE supporte PAS --indice-outil (seulement --indice-regle) -- pour ajouter une case combo avec l outil combos-moteur, utiliser `ajouter --indice-outil nom:chemin:commande` puis supprimer les anciennes cases en cascade.
7. VALIDATION : 3 combos json.load OK + combos-moteur --liste + navigation dry-run COMBO TERMINE (OUI et NON) ; carte v0.3.0 navigation 9/9 PARCOURS TERMINE (creer, agent, protocole OUI + NON->OUI sortie de boucle, modifier, controler, autre x2) ; valider-cartes --tous 11/11 CONFORME ; detecter 0 anomalie ; ASCII 0 sur 8 fichiers (3 defs + 3 docs + parcours + index).

## [LECON] 2026-08-08 -- AUDIT generateurs-commande (outil fantome ?)

**Mission** : verifier pourquoi generateurs-commande n'est jamais utilise directement par personne.
**Audit complet (Buffy, domaine analyse du cerveau)** :
1. **0 reference directe** dans les 11 parcours, la carte buffy, demarrer.md, protocole-activation -- les agents ne le voient JAMAIS dans leurs cases
2. **Usage indirect reel** : combos-moteur l'appelle en mode AUTO dans 5 combos (combo-activation 3, combo-audit-themis 2, combo-controle-modification 2, combo-corriger-ascii 1, combo-sante-tableaux 1) -- l'outil n'est PAS mort, il vit derriere le moteur
3. **Catalogue trop pauvre (13 commandes vs 100+ outils reels)** : les commandes du quotidien (valider-nommage, valider-conventions, rechercher-fichier, creer-fichier, copier-dossier, copier-fichier) n'ont AUCUNE entree au catalogue
4. **Contresens personnel (Buffy)**: mes 3 combos creer-* (creer-fichier-cerveau, creer-agent, creer-protocole) utilisent des commandes python3 en DUR au lieu de cases generateur -- precisement parce que les commandes requises manquaient au catalogue. J'ai donc contribue au probleme au lieu de le resoudre (Pattern 3 mal applique : la case combos-moteur aurait du etre composee par le generateur)
5. **Chronologie** : generateur cree le 2026-08-07 16:07, les parcours construits avant/independamment -- l'outil est ne sans etre branche dans la guidance

**Diagnostic** : le generateur n'est pas un outil fantome au sens strict (usage indirect reel via combos-moteur), mais il est DECONNECTE de la guidance directe : aucune case de parcours ne dit a l'agent de l'utiliser, et le catalogue ne couvre pas les outils quotidiens. Un agent qui suit sa carte ne rencontre jamais generateurs-commande -> il ecrit les commandes en dur.

**Pistes de correction (a decider par Cerberus/utilisateur)** :
- A. Enrichir le catalogue avec les commandes manquantes (les 100+ outils) -> puis convertir les cases outil en dur des combos en cases generateur (Pattern 3 complet)
- B. Ajouter une case/indice dans les parcours demandant de passer par le generateur pour composer les commandes
- C. Procede d'audit anti-fantome : chaque nouvel outil doit etre branche (parcours OU combo OU protocole) au moment de sa creation, pas juste liste dans index-tools

**Lecon** : un outil qui n'est ni branche dans une guidance ni couvert par le catalogue est invisible pour les agents -- la liste dans index-tools ne suffit pas.

## [LECON] 2026-08-08 -- ENRICHISSEMENT du catalogue generateurs-commande (13 -> 98 commandes)

**Mission** : piste A du diagnostic valide (enrichir le catalogue avec les 89 outils reels).
**Realise** :
1. **Catalogue 13 -> 98 commandes** (v0.2.0) : les 89 outils reels (hors testers/spec) couverts, chacun avec script + modele + parametres (texte, choix, flag) et questions
2. **Generation automatique** : script temporaire qui parse la ligne `usage:` de chaque outil (argparse `--aide`/`--help` ET custom) pour extraire positionnels + flags avec leurs arguments
3. **Corrections manuelles** : 8 entrees speciales (valider-nommage, valider-relecture, verifier-systeme, valider-cartes-decision, rechercher-pense-betes/specs/todos, nettoyer-sessions) avec flags en dur dans le modele
4. **Amelioration du generateur** (generateurs-commande.py) : les flags a valeur en dur dans le modele (--cle {cle}) sont RETIRES quand la valeur est vide (evite les flags orphelins type `--appartient-a` sans valeur)
5. **Descriptions** recuperees depuis le help (ligne apres usage:) ou le .md, 71 corrigees

**Lecons** :
1. **Les outils utilisent --aide, pas --help** (convention du projet) : un parseur qui ne teste que --help rate les 2/3 des outils ; toujours tester --aide d abord
2. **La ligne `usage:` est la source la plus fiable** : elle contient positionnels + flags (avec arguments) en une ligne, meme quand argparse affiche une erreur (unrecognized arguments: --aide)
3. **Flags a valeur vs flags booleens** : la convention du catalogue est flag booleen = param type flag (rendu par le generateur), flag a valeur = flag en DUR dans le modele (--theme {theme}) + param texte ; un flag a valeur dans le champ flag du param n est jamais rendu
4. **Les descriptions du .md sont piegees** (ligne `**Version :**` matche le pattern) : la description reelle est la ligne apres usage: dans le help
5. **Penser a la non-regression combos** : les 13 commandes originales (utilisees par combos-moteur en AUTO) doivent rester intactes apres fusion -- verifie a la fin
6. **Les tests de validation doivent utiliser les BONNES cles** : un test avec mauvaise cle produit un faux KO (detecter-surcharge-fichier avec seuil_seuil, lister-fichiers avec extension_extension)

## [LECON] 2026-08-08 -- CONVERSION des combos creer-* en cases generateur (Pattern 3 complet)

**Mission** : convertir les commandes python3 en dur des 3 combos creer-* (combo-creer-fichier-cerveau, combo-creer-agent, combo-creer-protocole) en cases generateur utilisant le catalogue.
**Realise** :
1. **3 combos v0.1.0 -> v0.2.0** : chaque case outil avec commande en dur devient une PAIRE (case generateur + case outil d execution) selon le pattern combo-activation (catalogue + entrees + sortie cmdN -> commande {cmdN})
2. **Commandes composees par le generateur** : valider-nommage --type outil {chemin}, valider-conventions {fichier}, rechercher-fichier {fichier}, copier-dossier {source} {destination}, copier-fichier {source} {destination}, creer-fichier {fichier} {contenu}
3. **Controles preserves** : chaque controle (c4/c2/c2) reste en place, renumerote (combo-fichier: c7, combo-agent: c3, combo-protocole: c3) avec branches vers generateur+outil ou fin
4. **Doc .md des 3 combos mise a jour** (structure generateur -> outil, --reponses c7/c3/c3)
5. **Correction du catalogue** : creer-fichier contenu passe OBLIGATOIRE -> OPTIONNEL (le help dit fichier [contenu]) - c etait un bug du parseur de la mission precedente (tous les positionnels etaient obligatoires)

**Lecons** :
1. **Les commandes en dur des combos crees precedemment etaient incompletes** : copier-dossier exige 2 arguments (source + destination) mais les commandes en dur n en avaient qu un -- le combo n avait jamais ete reellement execute (seulement dry-run de navigation)
2. **creer-fichier cree les dossiers parents automatiquement** (fichier.parent.mkdir(parents=True)) : pas besoin d un outil mkdir separe
3. **Le pattern generateur -> outil double le nombre de cases** mais rend le combo AUTONOME : l agent n a plus a connaitre la syntaxe exacte des outils, le generateur compose via le catalogue
4. **Faux positif nommage** : valider-nommage --type outil sur les definition-combo.json signale 'doit commencer par combos-' MAIS c est le cas pour TOUS les combos existants (combo-activation etc.) : les definitions suivent la convention combo-* et non combos-* -- ne pas corriger
5. **Un parametre obligatoire dans le catalogue bloque le combo** : verifier la realite du help (fichier [contenu] = optionnel) avant de tester un combo qui ne fournit pas ce parametre

## [LECON] 2026-08-08 -- PISTE B : indice PASSE PAR LE GENERATEUR dans les 11 parcours

**Mission** : brancher generateurs-commande dans la guidance directe des parcours (le generateur etait DECONNECTE : 0 occurrence dans les 11 parcours, les agents ecrivaient les commandes en dur).
**Resultat** : un indice (regle PASSE PAR LE GENERATEUR + outil generateurs-commande avec commande d exemple ciblee sur l outil de la case) ajoute en tete de la case la plus pertinente de chaque parcours (celle qui lance une suite d outils), 11/11, versions bumper (patch +1).
**Lecons** :
1. Le choix de la case cible est un RAISONNEMENT par parcours : la case qui lance une suite d outils (ex: athena c4 squelette, vulcain c2 verifier-systeme, themis c16 evaluer) -- pas la case 0, pas la case mission ; l outil de la case determine le nom catalogue a citer dans la commande d exemple.
2. FORMAT DE L INDICE OUTIL (verifie dans guider-parcours afficher_indices) : {"type": "outil", "nom": ..., "chemin": ..., "commande": ...} -- le moteur affiche nom + chemin + commande et deduit AUTOMATIQUEMENT la ligne LIRE AVANT USAGE (Pattern 9) depuis le chemin ; PAS de champ raison pour les indices outil (seul fichier en a un) -- le message passe par un indice regle adjacent.
3. PIEGE JSON.DUMP SUR LES PARCOURS : reecrire un parcours avec json.dump(indent=2) reformate TOUT le fichier (218+/210- pour un ajout de 12 lignes) -- les parcours doivent etre edites CHIRURGICALEMENT (insertion de lignes au format exact du fichier), jamais reformates en entier.
4. PIEGE GUILLEMETS DANS TEXTE JSON : un texte d indice avec des guillemets internes non echappes casse le JSON (Expecting ',' delimiter) -- ne JAMAIS mettre de guillemets dans les textes d indices, ou les echapper proprement.
5. Le bump de version (patch +1) se fait sur la ligne version du bloc parcours -- verifier avec git diff --stat que le diff est minimal (121+/11- = 11 fichiers x 11 lignes ajoutees + 11 versions).
6. VALIDATION : json.load immediat dans le script, ASCII 0/11, valider-cartes --tous 11/11 CONFORME, navigation --reponses PARCOURS TERMINE 11/11 avec affichage de l indice verifie.
| VERITE | Un outil cree et teste mais jamais branche est invisible : l indice PASSE PAR LE GENERATEUR fait rencontrer generateurs-commande a chaque agent qui suit sa carte |

## [LECON] 2026-08-08 -- PISTE C VOLET 2 : champ catalogue ajoute aux 177 indices outil des 11 parcours

**Mission** : appliquer le champ optionnel catalogue (format v0.2.20, volet 1 Vulcain) aux indices outil des parcours - la commande en dur est CONSERVEE comme fallback.
**Resultat** : 184 indices outil au total, 177 champ catalogue ajoutes (les 7 restants = les 6 outils exclus sans entree catalogue exploitable : template-test, 3 protections tester, tester-protection-* x2, creer-fichier / ecrire-fichier), diff minimal 177+ / 0-, JSON ASCII strict.
**Lecons** :
1. POINT D INSERTION : inserer le champ catalogue APRES la ligne nom (toujours suivie d une virgule), PAS apres la ligne commande (souvent la derniere cle sans virgule -> Expecting , delimiter). Lecon de la piste B confirmee : edition chirurgicale ligne par ligne, jamais json.dump de reformatage.
2. EXCLUSIONS : 6 noms d outils sans entree catalogue exploitable - template-test et les tester-protection-* (pseudo-outils de protocole, commande descriptive non executoire) et creer-fichier / ecrire-fichier (nom compose) - ils restent sans champ catalogue par conception.
3. L AFFICHAGE (guider-parcours v0.3.1) montre desormais pour chaque indice outil : catalogue: <nom> + PASSE PAR LE GENERATEUR (commande generateurs-commande --commande <nom>) + LIRE AVANT USAGE (Pattern 9) - l agent sait composer la commande via le catalogue ET lire la doc avant usage.
4. VALIDATION : json.load 11/11, ASCII 0/11, valider-cartes --tous 11/11 CONFORME, navigation 11/11 PARCOURS TERMINE, diff 177+ / 0- (aucune ligne supprimee).
| VERITE | Chaque commande des parcours est desormais retracable au catalogue (champ catalogue) tout en gardant son fallback en dur : zero derive, zero casse |

## PHILOSOPHIE -- Principes de comportement

| **Relire sa fiche a chaque activation** | Quand je suis active ou reactive, je relis MA fiche et MES corrections avant de continuer. Je ne lis que mes fichiers, jamais ceux des autres agents : chacun lit les siens en prenant le relais. |
## [CONTROLE] 2026-08-08 -- Verif impacts creation verifier-restauration-sure (VERDICT CONFORME)

**Objet** : verifier avec detecter-impacts (v0.2.1) que la creation de l outil verifier-restauration-sure par Vulcain a mis a jour tous les fichiers impliques.
**Resultat** : VERDICT CONFORME. detecter-impacts sur le .py -> 6 fichiers impliques, tous [A JOUR] : catalogue-commandes.json (reference), index-tools.md (reference), spec (reference), .md (reference), .sh (reference), corrections vulcain (reference). 0 potentiellement non mis a jour.
**Verifications croisees** : catalogue contient la commande (modele --fichier {fichier}, generation reelle OK : python3 .../verifier-restauration-sure.py --fichier test.md) ; index-tools ligne 268 ; spec presente ; ASCII 0 sur les 4 fichiers + catalogue ; parite py/sh OK ; JSON valide 105 commandes ; diff minimal (1961 insertions 0 suppression - consequence de la regeneration, pas de reformatage).
**Lecons** :
1. detecter-impacts prend UN FICHIER, pas un dossier (ERREUR fichier introuvable sur le dossier) - lancer sur le .py de reference.
2. Le regenerateur du catalogue met le NOM DU SCRIPT comme description (ex: verifier-restauration-sure.py) - les entrees regenerees ont des descriptions cosmetiques a corriger (verifier-systeme a aussi Options:). Correction chirurgicale texte (jamais json.dumps).
3. verifier la generation reelle de la commande via le generateur (--reponses) en plus de la presence de l entree.
## [CORRECTION] 2026-08-08 -- Descriptions cosmetiques du catalogue (63 corrigees + 8 completees = 0 restante)

**Objet** : corriger les descriptions cosmetiques du catalogue generateurs-commande (fragments d aide captures par le regenerateur : Options :, Arguments :, [--aide], source destination, etc).
**Resultat** : 63 descriptions corrigees (extraction depuis l en-tete du .py) + 8 descriptions partielles completees (celles finissant par :) = 0 description cosmetique restante sur 105. JSON valide, ASCII 0, CRLF uniforme (2352/2352/2352), non-regression generateur OK, generation reelle verifiee (valider-nommage, verifier-systeme, ajouter-contenu-fichier).
**Methodes (script .tmp, puis supprime)** :
1. SOURCE FIABLE : la description est dans l EN-TETE du .py, sous 2 formats : (A) docstring triple-quote ("""
 nom.py

 Description...), (B) commentaires (# nom.py puis # Description) pour les outils convertis. Le regex de docstring capture le 1er triple-quote du fichier, qui peut etre un docstring de FONCTION INTERNE (ex: _COULEURS) - gerer les 2 formats explicitement.
2. PIEGE CRLF PARASITE : le fichier avait 2 CRLF parasites parmi 2350 LF. La detection naive (si '
' in txt) choisissait CRLF -> split en 3 lignes (fichier entier) -> aucun remplacement silencieux. SOLUTION : normaliser en LF en memoire (txt.replace(CRLF, LF)), split, reecrire en CRLF uniforme.
3. Le nom du script peut finir par .sh (tests) meme si le .py existe : accepter .py OU .sh pour detecter la ligne du nom.
4. La translitteration ASCII (NFKD) est obligatoire sur les descriptions extraites (les docstrings contiennent des accents).
5. Limiter a ~90 caracteres en coupant a la derniere phrase pour les descriptions longues.


## [LECON] 2026-08-09 -- PARITE --version py/sh OBLIGATOIRE integree dans le parcours Vulcain (v0.2.3)

**Objet** : rendre la verification de parite --version py/sh OBLIGATOIRE apres toute creation/modification d outil, suite a la divergence generateurs-commande.sh (v0.1.0-beta vs .py v0.2.0) detectee par Morpheus (T5) et corrigee par Vulcain.

**Modification** : parcours-vulcain.json v0.2.2 -> v0.2.3. Indice outil 'verifier-parite-version' ajoute dans c6 (Developper l'outil) et c12 (Modifier l'outil) : diff <(python3 <outil>.py --version | tr -d '\r') <(bash <outil>.sh --version | tr -d '\r') -> si divergence, aligner le .sh (VERSION/STATUT) avant de continuer. Description mise a jour (mention v0.2.3).

**Validations** :
1. Navigation chemin CREATION (OUI|construire|OUI|OUI) : c6 -> c7 -> c7b -> c8 -> c9 OK, l'indice parite s'affiche.
2. Navigation chemin MODIFICATION (OUI|modifier|OUI) : c12 -> c13 -> c13b -> c14 -> c15 OK.
3. valider-cartes-decision --agent vulcain : CONFORME.
4. json.tool OK, ASCII 0 non-ASCII, CRLF preserve (509/509), workspace propre.

**Lecons** :
1. INSERTION JSON DANS UN TABLEAU : un indice insere en FIN de tableau d'indices ne doit PAS avoir de virgule de queue - ma 1re insertion a produit une virgule illegale (trailing comma) corrigee par un script de reparation cible. Verifier le JSON avec json.tool APRES chaque insertion (pas seulement a la fin).
2. PRESERVATION CRLF : edition chirurgicale (normalisation LF en memoire + restauration CRLF a l'ecriture) - jamais json.dumps sur tout le fichier (detruit le formatage et peut changer le style de fin de ligne).
3. NAVIGATION : le format --reponses doit matcher les branches reelles des cases questions (c0=OUI, c1=construire/modifier, c3=OUI) - consulter les branches AVANT de construire le chemin de test.
4. Quand on rend une verification obligatoire, l'ajouter aux 2 chemins paralleles (creation ET modification) pour eviter une asymetrie.

## [LECON] 2026-08-09 -- REGLE DES 5 FICHIERS integree dans le parcours Vulcain (v0.2.4)

**Objet** : ajouter la regle des 5 fichiers comme indice dans la case c12 (Modifier l outil) du parcours Vulcain, suite a la lecon Vulcain (controle Janus : impact spec oublie).

**Modification** : parcours-vulcain.json v0.2.3 -> v0.2.4. Indice de type regle "REGLE DES 5 FICHIERS" ajoute dans c12 apres verifier-parite-version : apres TOUTE modification de version d un outil, verifier l alignement VERSION/STATUT dans les 5 fichiers du dossier outil (py, sh, md, spec + catalogue/index associe si present) ; distinguer les versions propres (catalogue-commandes.json a SA version top-level, index-tools.md a la version de l index - pas celle de l outil). Description mise a jour (mention v0.2.4).

**Validations** :
1. json.tool OK (aucune virgule de queue cette fois - lecon Buffy precedente appliquee : indice insere en FIN de tableau SANS virgule de queue).
2. ASCII 0 non-ASCII.
3. CRLF preserve (513/513).
4. Navigation chemin modification (OUI|modifier|OUI) : c12 -> c13 -> c13b -> c14 -> c15 OK, l indice REGLE DES 5 FICHIERS s affiche dans le detail de c12.
5. valider-cartes-decision --agent vulcain : CONFORME.
6. Workspace propre (0 .tmp restant).

**Lecons** :
1. La lecon du piege de virgule de queue (Buffy 2026-08-09, insertion JSON en fin de tableau) est appliquee avec succes : l insertion de la regle des 5 fichiers dans c12 n a produit AUCUNE erreur JSON - la methode (script d edition chirurgicale + verification json.tool immediate) est fiable.
2. L insertion d un indice de type regle dans une case existante est chirurgicale : on cible la fin du dernier indice + "suivant" pour inserer SANS perturber la navigation (le chemin reste identique).
3. La mise a jour de version (0.2.3 -> 0.2.4) et de la description doit accompagner CHAQUE modification de parcours - la description porte l historique des versions (convention des parcours).
4. Une regle issue d une lecon documentee (ici : regle des 5 fichiers de Vulcain) devient un indice de carte : le cercle vertueux lecon -> carte -> application est confirme.

---

## [LECON] 2026-08-09 -- SYNTAXE reactiver : 3e argument agent_precedent OBLIGATOIRE (documente)

**Mission** : documenter la bonne syntaxe de `reactiver` (3e argument obligatoire) dans le parcours de Cerberus + le protocole-activation, suite a la regression vecue (2 commandes reactiver sans 3e argument -> aide affichee, bloc reste sur vulcain).

**Actions realisees** :
1. **parcours-cerberus.json** (version 0.2.1 -> 0.2.2) : case c7 = indice regle `SYNTAXE RETOUR OBLIGATOIRE` avec la commande complete a 3 arguments + mention du 3e argument obligatoire + symptome d'echec (aide affichee, bloc non mis a jour) + ligne de confirmation attendue ; case c20 (FIN) = indice regle court de rappel. Les cases c21/c12b laissees telles quelles (reactiver un AGENT = activer, syntaxe correcte).
2. **protocole-activation.001.02.prepare.md** : Etape 6 = note `3e argument OBLIGATOIRE` ajoutee APRES la fermeture du bloc bash (premiere tentative inseree DANS le bloc = corrigee) ; table Pieges Courants = entree `Oublier le 3e argument de reactiver (agent_precedent)` avec la solution (verifier `Session ... : Cerberus reactive avec succes`).

**Lecons** :
1. `reactiver` exige 3 arguments : `<session> <raison> <agent_precedent>` - sans le 3e, la commande affiche l'AIDE au lieu de reussir et le bloc session reste sur l'agent (echec SILENCIEUX, fausse impression de succes)
2. Verifier la sortie : la ligne `Session session-llm-1 : Cerberus reactive avec succes` confirme le succes
3. Ne jamais inserer une note > dans un bloc ```bash``` (elle devient du code) - l'inserer APRES la fermeture
4. Toujours verifier le contexte visuel apres une insertion (j'ai du corriger le placement de la note)
5. Verifier ASCII sur chaque fichier modifie (0 non-ASCII)

**Validation finale** : JSON parcours valide (version 0.2.2), navigation guider-parcours OK (chemin jusqu a [27/27]), ASCII 0 (parcours + protocole), note et piege en place.

---

## [LECON] 2026-08-09 -- CRITERE REACTIVER integre dans la spec-guider-parcours (v0.2.21)

**Mission** : integrer le critere reactiver dans la procedure d'audit de la spec-guider-parcours (Pattern 11 + procedure 4i) pour application automatique.

**Actions realisees** :
1. **Pattern 11 -- CONFORMITE D'EXECUTION** : regle 5 ajoutee dans la section Regles (apres la regle 4) : la reactivation finale de Cerberus est un POINT DE CONFORMITE obligatoire - verifier les 5 points R1-R5 (3e argument agent_precedent, pas d'aide, sortie Session ... : Cerberus reactive avec succes, bloc AGENTS.md sur Cerberus, profil classeur a jour) - une aide affichee = ECHEC SILENCIEUX a signaler comme ecart d'execution (lecon Themis 2026-08-09)
2. **Procedure 4i** : point 6 ajoute (apres le point 5 RE-AUDIT COMPLET) : VERIFIER LA REACTIVATION (critere reactiver R1-R5) - l'agent audite a-t-il reactive Cerberus correctement ? Une aide affichee ou un bloc restant sur l'agent = ECART D'EXECUTION a inscrire au rapport
3. **Version** : 0.2.20 -> 0.2.21 (en-tete)

**Lecons** :
1. La chaine `5. RE-AUDIT COMPLET` et `4. La regle est compatible avec le Pattern 10` apparaissent dans PLUSIEURS procedures/sections : un remplacement global sur ces chaines insere au MAUVAIS endroit (j'ai insere le point 6 dans la 4d au lieu de la 4i, puis la regle 5 au milieu de la regle 4) - TOUJOURS cibler avec le marqueur de section (### 4i, ### Pattern 11) + verifier le contexte apres insertion
2. Une insertion entre une ligne et sa CONTINUATION (phrase sur 2 lignes) coupe la phrase : verifier la fin reelle du bloc avant d'inserer (la continuation peut etre a la ligne suivante)
3. Apres toute insertion dans une spec, relancer detecter-divergences-version pour confirmer que la version est bien lue (0.2.21 lu, cas legitime conserve)
4. Verifier ASCII + style de fin de ligne apres chaque correction (LF preserve 1308/1308)

**Validation finale** : Pattern 11 regle 5 (lignes 951-957) correctement placee apres la regle 4 complete, procedure 4i point 6 (lignes 1163-1168) apres le point 5 complet, version 0.2.21 lue par l'outil, ASCII 0, LF 1308.
## [LECON] 2026-08-09 -- COMBO tester-outil CREE (Pattern 3, chemin de test Morpheus encapsule)

**Mission** : creer combo-tester-outil (ecrire tests + protections + executer) et le brancher dans le parcours morpheus.
**Lecons** :
1. Le combo tester-outil encapsule les anciennes cases c4-c6 du parcours morpheus : c1 generateur (catalogue creer-fichier, entrees fichier/contenu/forcer -> cmd1) -> c2 outil ({cmd1} cree le fichier) -> c3 controle (protections ajoutees ? OUI->c4 / NON->c5) -> c4 outil ({commande_test}) -> c5 fin PROTECTIONS MANQUANTES / c6 fin SYNTHESE. La REGLE ABSOLUE (jamais de test sans protections) est PRESERVEE par le controle c3.
2. Le combo recoit ses donnees via --var (fichier_test, contenu_test, commande_test) - l interpolation {var} est faite par combos-moteur (variable inconnue = erreur : toujours fournir les 3).
3. Format des reponses de controles pour combos-moteur : --reponses 'c3=OUI' (case=reponse), PAS 'OUI' seul.
4. Navigation testee : OUI -> c6 FIN (fichier cree + test execute), NON -> c5 FIN protections manquantes. Parcours morpheus v0.1.1 -> v0.1.2 : c4 remplacee par Lancer le combo tester-outil (outil combos-moteur, suivant c7), c5/c6 supprimees (encapsulees), JSON valide, CRLF preserve, ASCII 0.
5. valider-nommage signale 2 ERREUR sur definition-combo.json : BRUIT PREEXISTANT identique sur les 15 combos (format combos-*/definition-combo.json hors perimetre de l outil) - ne pas corriger, documenter.
6. Apres creation d un combo : index-tools.md (table Combos) + lecon corrections.md + navigation reelle (--liste + --reponses OUI/NON) + valider-cartes-decision --agent (parcours) + detecter-impacts (impacts identite traites).
7. detecter-impacts signale des fichiers identification NON MIS A JOUR (corrections.md, fiche, test-003) : verifier s ils referencent une VERSION du parcours - ici AUCUNE (la fiche reference la spec, pas la version du parcours) -> bruit de date, pas un impact reel a traiter.

**Validation finale** : combo-tester-outil v0.1.0, parcours morpheus v0.1.2, index-tools a jour, ASCII 0 sur 3 fichiers.
## [LECON] 2026-08-09 -- PIEGE WINDOWS documente dans protocole-creation-combos v0.1.2

**Mission** : documenter le piege Windows (backslashes vs forward slashes dans les variables de combos) pour les prochaines creations.
**Lecons** :
1. Le piege : une variable de chemin passee via --var (ex: fichier_test=<chemin>) avec des backslashes Windows (Z:\...\x.sh) passe dans la commande generee, puis shlex.split de la case outil ECLATE le backslash (interprete comme echappement) -> commande invalide, fichier non cree. Solution : FORWARD SLASHES (Z:/.../x.sh) acceptes par Python et shlex
2. Decouverte par le test formel Morpheus du combo tester-outil (2 KO -> forward slashes -> 16/16 VALIDE) - le piege etait dans la lecon Morpheus, il est maintenant FIGE dans le protocole (section 6.3b) pour toutes les prochaines creations
3. Impact en cascade (detecter-impacts) : la spec du protocole doit suivre le protocole -> EX-10 ajoutee (v0.1.2-ebauche) avec priorite Haute et critere d'acceptation (navigation reelle testee avec forward slashes). Les 2 references combos-moteur (md + spec) sont de simples liens sans version -> bruit de date, pas de mise a jour necessaire
4. Rituel de verification : ASCII 0 (protocole + spec), valider-liens 0 invalide (protocole + spec), style LF preserve, workspace propre
5. Le cycle protocole -> spec -> todo : quand on ajoute une regle au protocole, la spec porte l'exigence (EX-N) et l'historique des 2 fichiers est bumpe - detecter-impacts guide la mise a jour en cascade

**Validation finale** : protocole v0.1.2 (section 6.3b), spec v0.1.2-ebauche (EX-10), ASCII 0 x2, liens OK, workspace propre.
## [LECON] 2026-08-09 -- DIAGNOSTIC GENERALISATION GENERATEUR (187 commandes en dur)

**Contexte** : diagnostic demande par l utilisateur (mode diagnostic, aucune modification).
**Resultat** : 187 commandes python3 en dur dans les 11 parcours + demarrage, 53 outils distincts, 53/53 couverts par le catalogue (106 commandes).
**Lecons** :
1. Le catalogue est PRET (91/92 outils) mais les parcours fournissent les commandes exactes en dur -> l agent n a aucune raison d utiliser le generateur
2. Cause racine : ni regle immuable (obligation), ni indices systematiques (~2/parcours, morpheus 0, demarrage 0) -> le generateur est un outil orphelin malgre sa qualite
3. Solution recommandee : S1 (convertir 185 commandes en references catalogue) + S2 (regle immuable passage obligatoire par le generateur), S3 optionnelle (indices enrichis)
4. EXCEPTION identifiee : 2 commandes composites (parite py/sh --version avec diff) ne peuvent pas etre generees -> restent en dur, a documenter
5. Methode : scan Python sur les 12 JSON (glob agents/*/parcours + demarrage) - regex outils tools/.../nom.py - fiable et reproductible
6. Rapport depose dans mission-diagnostic.md (conforme au sous-protocole-diagnostic, ASCII OK)
7. La decision de conversion appartient a l utilisateur (diagnostic d abord, decision ensuite)
## [LECON] 2026-08-09 -- PILOTE ATLAS GENERALISATION GENERATEUR (fiabiliser + strict)

**Contexte** : pilote complet demande par l utilisateur sur le parcours Atlas avant generalisation aux 11 autres (diagnostic 187 commandes en dur).
**PHASE 1 - FIABILISATION (BUG MAJEUR TROUVE ET CORRIGE)** : generateurs-commande composait les flags optionnels non renseignes en VIDE (ex: lire-fichier -> --debut --fin --lignes sans valeur) -> argparse code 2 (usage).
1. CAUSE RACINE .py (ligne 216) : condition INVERSEE - if valeur=="" and parametre.get("flag") is None : le flag n etait retire que quand il n existait PAS ; il fallait le retirer quand il EXISTAIT. Corrige v0.2.0 -> v0.2.1 (py + sh) : retirer --flag {placeholder} quand valeur vide.
2. .sh : la logique de retrait n existait PAS (simple replace) - portee la meme correction (parite stricte, --version v0.2.1/v0.2.1).
3. CATALOGUE : 9 flags booleens en dur dans les modeles (--inverse, --forcer, --backup, --unique, --liste, --lister/--resume/--compter/--json) n avaient pas de placeholder -> reponse non laissait le flag. Corrige : flag en dur -> placeholder {cle} (reponse oui = flag, non = absent). Version catalogue 0.1.0-beta -> 0.2.0.
4. DOC .md : chiffre 98 commandes obsolete -> 106 (verifie par comptage JSON).
5. REGENERATEUR : mode SYNCHRONISATION preserve les entrees existantes ENTIERES (modele inclus) - dry-run confirme 83 preserves / 0 ajoute - mes corrections de modeles survivront aux futures regenerations.
**PHASE 2 - PILOTE STRICT (parcours-atlas v0.1.1 -> v0.1.2)** : 24 champs commande retires des indices outil avec catalogue (ne restent que type/nom/catalogue/chemin). guider-parcours affiche alors catalogue: X + PASSE PAR LE GENERATEUR SANS commande en dur (ligne 183 : if ind.get(commande) -> optionnel).
6. Navigation 6/6 chemins PARCOURS TERMINE (explorer, web, documenter, analyser, autre+OUI delegation, autre+NON signaler) + valider-cartes-decision --agent atlas CONFORME.
7. PIEGE : json.dump reecrit le fichier en LF - le parcours atlas etait en CRLF (608 lignes) -> RESTAURER CRLF apres json.dump (remplacer 
 par 
) - verifier style avant/apres.
8. MODELE POUR GENERALISATION : (a) verifier que le catalogue compose chaque outil du parcours SANS flag vide, (b) corriger py/sh/catalogue si besoin, (c) retirer les commandes en dur des indices avec catalogue, (d) naviguer TOUS les chemins + valider-cartes.
9. Les 2 commandes composites (parite py/sh --version avec diff) restent en dur - exception documentee, hors catalogue.
10. DECISION UTILISATEUR ATTENDUE : valider le pilote Atlas puis generaliser aux 10 autres parcours (187 -> 24 commandes restantes si tous traites comme Atlas).
## [LECON] 2026-08-09 -- REVISION PARCOURS ATLAS v0.1.2 -> v0.1.3 (une carte = un role)

**Contexte** : constat utilisateur - Atlas n est pas habilite a creer des outils ni etablir des tests. L incident du jour le prouve (Atlas a ecrit un outil scan-catalogue.py dans explorations/ au lieu de signaler). La carte d Atlas devait le recentrer sur l exploration et le SIGNALEMENT.

**Actions** : ajout d un indice REGLE CREATION LIMITEE A LA DOCUMENTATION en tete des indices des 4 cases de creation/documentation (c9 Documenter les decouvertes, c18 Creer la structure de documentation, c19 Rediger le contenu, c25 Creer la cartographie) : rapports de mission uniquement (explorations/ ou .tmp-* du workspace, JAMAIS tools/), JAMAIS d outil (Vulcain), JAMAIS de test (Morpheus), JAMAIS de case de parcours (Buffy) ; correction de la case c29 Signaler le besoin (message : signaler a Cerberus - outil -> Vulcain, test -> Morpheus, nouvelle case -> Buffy - je ne cree rien moi-meme ; suppression de la mention documenter une nouvelle case) ; version bump 0.1.2 -> 0.1.3.

**Validations** : JSON valide 32 cases, navigation 6/6 chemins PARCOURS TERMINE (explorer, web, documenter, analyser, autre+OUI, autre+NON), valider-cartes-decision CONFORME, ASCII 0, CRLF preserve (624 pur), detecter-impacts = faux positifs identification (la fiche atlas.md reference le parcours par chemin, pas par version).

**Lecons** :
1. UNE CARTE = UN ROLE s applique aussi aux CASES de creation : quand un agent a un defaut connu (ex: Atlas peut creer des structures trop elaborees - deja note dans sa fiche), la carte doit porter un GARDE-FOU EXPLICITE dans les cases concernees, pas seulement une mention dans la fiche
2. Le SIGNALEMENT est le canal : un agent qui decouvre un besoin (outil, test, case) SIGNALE a Cerberus qui active l agent habilite - la case c29 doit dire exactement QUI fait QUOI (Vulcain/Morpheus/Buffy), jamais inviter l agent a faire lui-meme
3. Edition chirurgicale d un parcours CRLF : lire en newline='', remplacer avec \r\n, reecrire en newline='' - jamais json.dumps global (recrirait en LF) ; verifier le compte de remplacements (1 par ancre)
4. detecter-impacts sur un parcours signale la fiche en identification : faux positif si la fiche ne porte pas la version du parcours (verifier le contenu avant de conclure)
## [LECON] 2026-08-09 -- Correction case c23 Signaler le besoin du parcours cerberus (Pattern 12, Ecart B)

**Mission** : corriger la case c23 du parcours cerberus (mention fautive "documenter une nouvelle case dans le parcours") -- premiere correction de la generalisation du Pattern 12 (audit Themis 1/11 conforme).

**Lecons** :
1. Le modele atlas c29 n'est pas copiable tel quel pour cerberus : Atlas SIGNALE a Cerberus (il est le demandeur), Cerberus DECIDE et ACTIVE (il recoit le besoin de l utilisateur) -- chaque carte adapte la formulation du garde-fou a SON role (signaler a l utilisateur + activer l agent habilite)
2. Le message corrige supprime la creation de case (role Buffy) mais conserve le perimetre : "Situation non couverte : signaler le besoin a l utilisateur et activer l agent habilite (besoin d outil -> Vulcain, besoin de test -> Morpheus, besoin de nouvelle case -> Buffy). Je ne cree rien moi-meme : je signale et j active."
3. La navigation de guider-parcours exige de repondre a TOUTES les questions du chemin, y compris c0 (relecture honnete OUI) : le chemin vers c23 est OUI|autre|NON (c1 branche autre -> c18 -> NON) -- sans le OUI initial, l outil refuse la reponse suivante
4. Edition chirurgicale CRLF : remplacement du message seul + bump version 0.2.2 -> 0.2.3, jamais json.dumps -- 510 CRLF preserves, ASCII 0
5. valider-cartes CONFORME + detecter-impacts = faux positifs (la fiche cerberus reference le parcours par chemin, jamais par version)
6. Cette correction est la plus simple de la generalisation (parcours cerberus sans case de creation) : elle sert de modele pour les 9 autres cases Signaler fautives (athena c20, buffy c35, clio c15, janus c29, minerve c20, morpheus c16, promethee c20, themis c23, vulcain c18) -- chacune adaptee au role de l agent
## [LECON] 2026-08-09 -- Correction des 9 cases Signaler fautives (generalisation Pattern 12, Ecart B)

**Mission** : corriger les 9 cases Signaler restantes (athena c20, buffy c35, clio c15, janus c29, minerve c20, morpheus c16, promethee c20, themis c23, vulcain c18) en adaptant chaque message au role de l agent.

**Lecons** :
1. UN AGENT NE SE RENVOIE JAMAIS A LUI-MEME : la regle des roles exclus est adaptative - vulcain (constructeur d outils) ne renvoie pas les besoins d outil a Vulcain, morpheus (testeur) ne renvoie pas les tests a Morpheus, buffy (conceptrice de parcours) ne renvoie pas les nouvelles cases a Buffy ; les 6 agents a roles non-createurs (athena, clio, janus, minerve, promethee, themis) gardent les 3 renvois complets
2. Le message corrige conserve la structure du modele atlas : "Mission hors perimetre : signaler le besoin a Cerberus (besoin d outil -> Vulcain, besoin de test -> Morpheus, besoin de nouvelle case -> Buffy). Je ne cree rien moi-meme : je signale et j attends la mission." - avec suppression de la mention fautive "documenter une nouvelle case dans le parcours"
3. Edition en LOT : un seul script Python a traite les 9 fichiers avec verification du comptage (message 1 fois, version 1 fois) avant remplacement - jamais de remplacement aveugle ; chaque fichier preserve son format (9/9 CRLF pur, 0 LF)
4. Versioning : bump +1 mineur pour chaque parcours (v0.1.1->v0.1.2, v0.2.3->v0.2.4, v0.2.1->v0.2.2, v0.1.2->v0.1.3, v0.2.1->v0.2.2, v0.2.4->v0.2.5) - 9 fichiers modifies
5. VALIDATIONS : valider-cartes-decision 9/9 CONFORME, ASCII 0/9, navigation echantillon (morpheus c16 via OUI|autre|NON, vulcain c18 via OUI|autre|NON) PARCOURS TERMINE avec le nouveau message adapte, mention fautive disparue dans les 9
6. Cette mission complete le point 4 de la procedure 4j : les 11 parcours ont desormais une case Signaler conforme (atlas c29, cerberus c23, + 9 corriges) - reste le point 2 (21 cases de creation sans garde-fou complet) pour la conformite totale du Pattern 12
## [LECON] 2026-08-09 -- Regle retour de mission corrigee : la fin suit SA carte (Pattern 8 generalise)

**Mission** : corriger le conflit entre l'ancienne regle "toujours reactiver Cerberus" et la nouvelle philosophie "chaque agent active l agent suivant dans sa carte" (decision utilisateur : option "La fin suit SA carte" + perimetre "Tout + parcours").

**Nouvelle regle (source de verite, spec Pattern 8 v0.2.15 deja conforme)** :
1. Activation DIRECTE par Cerberus (hors chaine) -> fin = reactiver Cerberus
2. Maillon d'une chaine de delegation -> fin = ACTIVER le maillon suivant selon SA carte
3. Le DERNIER maillon de la chaine -> reactiver Cerberus avec le BILAN CONSOLIDE
4. La chaine ne retombe JAMAIS sur Cerberus au milieu

**Lecons** :
1. **PIEGE MAJEUR : double/triple CRLF avec io.open(newline='\\r\\n')** : ecrire un fichier CRLF avec `newline='\\r\\n'` CONVERTIT chaque `\\r\\n` existant en `\\r\\r\\n` (et un 2e passage en `\\r\\r\\r\\n`) - le fichier est corrompu sans erreur visible (py_compile/bash -n cassent ensuite). CORRECTION : toujours lire AVEC `newline=''` et ecrire AVEC `newline=''` (aucune conversion), ou normaliser avec `re.sub(r'\\r+\\n', '\\r\\n', txt)` pour reparer. REGLE : preserver le format natif, jamais laisser Python convertir.
2. La regle generale (AGENTS.md, index-agents, cerberus corrections, todo-template) portait l'ancienne regle EN PARALLELE de la spec Pattern 8 deja conforme - le conflit venait des documents de coordination, pas des parcours (morpheus c17 / janus c30 avaient deja la bonne formulation)
3. Perimetre touche : 8 cases FIN - Delegation (athena c21, atlas c28, buffy c36, clio c16, minerve c21, promethee c21, themis c24, vulcain c19) + AGENTS.md (cycle etape 5 + section Fin de mission + regle finale) + index-agents.md + cerberus/corrections.md (2 lignes) + todo-template.md + 8 fiches (atlas, buffy, clio, janus, minerve, themis, vulcain + template) + 2 protocoles (activation, controle-statuts) + minerve (parcours c5/c14, fiche, corrections) + generateurs-squelette-todo (py+sh) + spec todo-protocole-composition = 26 fichiers
4. L'adaptation au role : chaque fiche porte la regle commune + une ligne FLUX specifique a son profil (atlas ne delegue pas ; janus dernier maillon avec bilan consolide ; vulcain apres delegation tests a Morpheus ; minerve Phase 9 flux Promethee -> Minerve)
5. Validations : valider-cartes 11/11 CONFORME, ASCII 0 sur 26 fichiers, navigation vulcain c19 (OUI|autre|OUI) et minerve PARCOURS TERMINE avec nouvelle regle, py_compile + bash -n OK, parite py/sh generateurs-squelette-todo (le --version n'existe pas dans ces interfaces - comportement preexistant, tester avec --dry-run)
6. detecter-usage-outils-externes signale le CRLF natif des parcours JSON et .py comme suspect : FAUX POSITIF (le CRLF est le format natif du projet, 465/281 lignes) - verifier si le CRLF etait PREEXISTANT (git) avant de considerer une infraction
## [LECON] 2026-08-09 -- VERIFICATION D IMPACT BRANCHEE DANS LE PARCOURS THEMIS (v0.2.4)

**Mission** : brancher detecter-impacts comme etape OBLIGATOIRE de l audit dans le parcours-themis (volet 2 de la generalisation decidee par l utilisateur), reference a la procedure 4l / Pattern 14 de la spec v0.2.24 (volet 1 documente par Promethee).

**Livrables** :
1. Case c8c VERIFICATION D IMPACT (Pattern 14) inseree entre c8b (Conformite d execution) et c9 (Ecrire le rapport) : type controle, question (as-tu lance detecter-impacts sur un echantillon des fichiers modifies et verifie que TOUS les fichiers impactes sont a jour ?), indice regle (Pattern 14 + procedure 4l : tout impact NON mis a jour = NON CONFORME), indice outil detecter-impacts (commande exacte avec --racine), indice fichier LIRE AVANT USAGE (auto), branches OUI->c9 / NON->c3
2. Recablage de c8b : OUI -> c8c (au lieu de c9) pour que le chemin d audit passe par la verification d impact
3. Bump version parcours themis v0.2.3 -> v0.2.4
4. Format CRLF natif restaure (le fichier etait CRLF pur, generateurs-case l avait reecrit en LF)

**Validations** : JSON valide (22 cases), valider-cartes-decision --agent themis CONFORME, ASCII 0, CRLF pur (510 lignes, 0 LF), navigation chemin complet OUI|audit|OUI|OUI|OUI|OUI|OUI = c8c affichee avec outil + LIRE AVANT USAGE puis PARCOURS TERMINE c13.

**Lecons** :
1. generateurs-case ajoute la case MAIS ne recable PAS les branches des cases existantes qui pointaient vers l ancienne cible : apres ajout de c8c apres c8b, c8b pointait encore OUI->c9 -> c8c etait INACCESSIBLE. TOUJOURS verifier le recablage des cases POINTEUSES apres une insertion (editer c8b --branche 'OUI:c8c')
2. generateurs-case reecrit le fichier en LF quel que soit le format natif : restaurer le CRLF apres usage (remplacer \n par \r\n) pour preserver le format natif du parcours (piege CRLF connu, nouvelle manifestation via l outil de cases)
3. Les cases de controle avec branche NON doivent pointer vers une case de re-travail (c3 = combo audit-themis) et OUI vers la suite (c9 = rapport) : le modele c8b/c8c est coherent
4. La verification croisee par navigation est indispensable : 5 reponses OUI ne suffisaient pas (le chemin passe par c1=audit), il fallait le chemin exact OUI|audit|OUI|... -- verifier le chemin dans la structure avant de naviguer
5. L indice fichier LIRE AVANT USAGE (Pattern 9) est ajoute automatiquement par generateurs-case v0.2.2 quand un --indice-outil est fourni : verifie le Pattern 9 sans action manuelle
## [LECON] 2026-08-09 -- TITRES DES FINS ACTIVES UNIFORMISES (athena v0.1.4, promethee v0.1.4)

**Mission** : retirer les suffixes (CHAIN) de athena c10 et (FLUX) de promethee c10 pour aligner sur le modele sans suffixe (morpheus c10, vulcain c9/c15) - point de vigilance n 1 de l audit Pattern 13 (verdict CONFORME).

**Livrables** :
1. athena c10 : FIN - Activer Promethee (CHAIN) -> FIN - Activer Promethee
2. promethee c10 : FIN - Activer Minerve (FLUX) -> FIN - Activer Minerve
3. Bump versions : athena v0.1.3 -> v0.1.4, promethee v0.1.3 -> v0.1.4

**Validations** : JSON valide (2/2), ASCII 0, CRLF natif preserve (athena 442, promethee 454 - 0 LF), valider-cartes-decision CONFORME (2/2), navigation PARCOURS TERMINE avec les nouveaux titres (2/2), scan des 11 parcours : plus AUCUN suffixe CHAIN/FLUX dans les titres.

**Lecons** :
1. Un point de vigilance cosmetique d un audit (verdict CONFORME) peut etre traite en mission dediee : c est le bon usage du rapport Themis (les points de vigilance sont des actions, pas des defauts)
2. Le suffixe (CHAIN)/(FLUX) etait dans le TITRE seul : les occurrences CHAIN/FLUX dans les MESSAGES et INDICES (ex: CHAIN Athena -> Promethee -> Minerve) sont LEGITIMES et a PRESERVER - un remplacement global aurait casse les messages. TOUJOURS cibler le champ exact (titre) dans une edition chirurgicale
3. La convention des titres de fins actives est desormais uniforme : FIN - Activer <maillon> sans suffixe (morpheus c10, vulcain c9/c15, athena c10, promethee c10)
4. Edition chirurgicale avec newline='' (piege CRLF) : les 2 fichiers en CRLF pur sont restes en CRLF pur (442/454 lignes)
5. Le scan de verification doit cibler les TITRES (champ titre), pas le fichier entier (grep CHAIN/FLUX sur le fichier entier touche 7 parcours a cause des messages - seul le scan des titres est pertinent)
## [LECON] 2026-08-09 -- CRITERE 24 (PATTERN 13) BRANCHE DANS LE PARCOURS THEMIS (v0.2.5)

**Mission** : ajouter la verification du critere 24 (LA FIN SUIT SA CARTE, Pattern 13) dans le parcours-themis - suite de la generalisation des criteres dans la carte d audit (c8b = critere 22, c8c = critere 25, c8d = critere 24).

**Livrables** :
1. Case c8d LA FIN SUIT SA CARTE (Pattern 13) inseree entre c8c (VERIFICATION D IMPACT) et c9 (Ecrire le rapport) : type controle, question (fin coherente avec le type d activation + aucune fin de maillon qui reactive Cerberus au milieu), indice regle (Pattern 13 + procedure 4k spec v0.2.23 : activation directe -> reactiver, maillon -> activer le suivant, dernier maillon -> reactiver avec bilan, chaine jamais sur Cerberus au milieu), branches OUI->c9 / NON->c3
2. Recablage de c8c : OUI -> c8d (au lieu de c9)
3. Bump version parcours themis v0.2.4 -> v0.2.5 (23 cases)
4. Format CRLF natif restaure (fichier en CRLF pur, generateurs-case avait reecrit en LF)

**Validations** : JSON valide (23 cases), valider-cartes-decision --agent themis CONFORME, ASCII 0, CRLF pur (532 lignes, 0 LF), navigation chemin complet OUI|audit|OUI|OUI|OUI|OUI|OUI|OUI = c8b -> c8c -> c8d affichees puis PARCOURS TERMINE.

**Lecons** :
1. La sequence d audit du parcours themis est desormais complete pour les 3 criteres d execution majeurs : c8b CONFORMITE D EXECUTION (critere 22, Pattern 11) -> c8c VERIFICATION D IMPACT (critere 25, Pattern 14) -> c8d LA FIN SUIT SA CARTE (critere 24, Pattern 13) : les 3 verifications sont OBLIGATOIRES dans le deroulement de la carte, plus aucune ne peut etre sautee
2. Confirme encore : generateurs-case ajoute la case mais NE RECABLE PAS les branches des cases pointeuses - c8c pointait encore OUI->c9, il fallait editer c8c --branche OUI:c8d (lecon deja apprise avec c8b/c8c, appliquee sans surprise)
3. Confirme encore : generateurs-case reecrit le fichier en LF quel que soit le format natif - restaurer le CRLF apres usage (532 lignes)
4. L'ordre d'insertion dans la sequence (apres c8c) est naturel : d abord la conformite d execution, puis les livrables (impact), puis la regle de retour (fin) - la carte d audit verifie le processus de haut en bas
5. Navigation de verification : 8 reponses necessaires (OUI|audit|OUI x6) car le chemin passe par c1=audit puis les 3 cases de controle - toujours compter les cases question du chemin avant de naviguer
## [LECON] 2026-08-09 -- FICHE THEMIS MISE A JOUR (VERIFICATIONS D AUDIT + CRITERE 24)

**Mission** : ajouter la verification du critere 24 (Pattern 13) dans la fiche themis (section outils/verifications de l audit) - suite du branchement c8d dans le parcours themis v0.2.5.

**Livrables** :
1. Ligne `detecter-impacts` ajoutee au tableau Outils de base (P0) apres detecter-usage-outils-externes
2. Bloc `VERIFICATIONS D AUDIT OBLIGATOIRES (criteres d execution)` insere entre le tableau et la REGLE : c8b CONFORMITE D EXECUTION (critere 22, Pattern 11), c8c VERIFICATION D IMPACT (critere 25, Pattern 14, detecter-impacts), c8d LA FIN SUIT SA CARTE (critere 24, Pattern 13 : activation directe -> reactiver, maillon -> activer le suivant, dernier maillon -> bilan consolide, chaine jamais sur Cerberus au milieu)
3. Entree Historique 2026-08-09 v0.2.1 ajoutee a la table de la fiche

**Validations** : ASCII 0, LF pur preserve (258 lignes, 0 CRLF), detecter-impacts present (2 occurrences), bloc VERIFICATIONS present (1), structure coherente (tableau intact, bloc insere entre tableau et REGLE), historique ajoute.

**Lecons** :
1. La fiche themis (source statique relue en c0) et le parcours themis (source de verite du guidage) doivent rester ALIGNES : le parcours v0.2.5 a les 3 cases c8b/c8c/c8d, la fiche documente maintenant les 3 verifications correspondantes - la fiche est le REFLET statique du parcours, pas une source independante
2. La sequence c8b -> c8c -> c8d couvre les 3 criteres d execution majeurs : conformite d execution (22), verification d impact (25), la fin suit SA carte (24) - un audit Themis passe OBLIGATOIREMENT par les 3
3. Piege des apostrophes dans les ancrages : les lignes existantes de la fiche contiennent des apostrophes (d'outils, j'utilise) - un ancrage sans apostrophe echoue silencieusement (ECHEC R1/R2) - toujours copier la ligne EXACTE (repr) avant de construire le remplacement
4. La section Historique de la fiche est une table | Date | Evenement | Details | : les mises a jour de fiche s y ajoutent avec bump de version de la fiche (v0.2.1)
5. Edition chirurgicale LF avec newline='' : la fiche est restee en LF pur (258 lignes) - piege CRLF confirme
## [LECON] 2026-08-09 -- CARTOGRAPHIER-PARCOURS BRANCHE DANS LE PARCOURS ATLAS (v0.1.4 -> v0.1.5)

**Mission** : brancher l outil cartographier-parcours v0.1.0 (cree par Vulcain, teste 19/19 Morpheus, controle Janus) dans le parcours atlas - decision utilisateur option 3 (case dediee).
**Livrables** :
1. Case c30 CARTOGRAPHIER UN PARCOURS (type indice, 33e case) : indice regle Pattern 9 LIRE AVANT USAGE en tete + indice regle Pattern 12 CREATION LIMITEE (sortie = rapport de mission dans le dossier du parcours audite, JAMAIS tools/, outil en lecture seule) + indice outil cartographier-parcours AVEC champ catalogue (PASSE PAR LE GENERATEUR) + indice fichier LIRE AVANT USAGE auto + suivant c10 (convergence Lecons et retour -> c11 FIN).
2. Branche cartographier:c30 ajoutee dans c1 (6 branches : explorer, web, documenter, analyser, autre, cartographier).
3. Version 0.1.4 -> 0.1.5, CRLF natif restaure (655 lignes, 0 LF), ASCII 0, valider-cartes CONFORME.
4. Navigation : chemin cartographier c30 -> c10 -> c11 PARCOURS TERMINE ; regression explorer c2 -> c11 toujours OK.
5. Bout en bout : generation reelle (33 cases, 21 chemins) puis fichier supprime (0 residu).
**Lecons** :
1. PIEGE generateurs-case editer --branche (grave) : `editer c1 --branche cartographier:c30` a REMPLACE les 5 branches existantes par une seule au lieu d AJOUTER - il a fallu re-ecrire les 6 branches (les 5 originales + la nouvelle). TOUJOURS re-lister les branches de la case avant un editer --branche et re-ecrire la liste COMPLETE.
2. Confirme encore : generateurs-case ne recable PAS les branches des cases pointeuses (ici c1) - mais ici c est la case elle-meme qui porte les branches, donc editer c1 avec la liste complete etait necessaire.
3. Confirme encore : generateurs-case reecrit en LF quel que soit le format natif - restaurer le CRLF apres chaque operation (655 lignes).
4. Le champ catalogue d un indice outil n est PAS ajoute par generateurs-case --indice-outil (il ajoute nom/chemin/commande) - l ajouter manuellement (edition chirurgicale JSON, indentation 10 espaces dans le fichier reel, jamais copier-coller d une indentation supposee) pour que guider-parcours affiche catalogue: + PASSE PAR LE GENERATEUR.
5. Le champ catalogue fait le lien avec le catalogue generateurs-commande (v0.2.20 PISTE C) : la commande en dur reste le fallback, mais l affichage PASSE PAR LE GENERATEUR pousse l agent a composer via generateurs-commande.
6. La case c30 respecte le Pattern 12 (CREATION LIMITEE) : l outil produit un rapport de mission dans le dossier du parcours audite, il ne cree PAS d outil - c est le bon usage d un outil de cartographie pour l explorateur.
## [LECON] 2026-08-09 -- REGLE FIGER LF DOCUMENTEE DANS LE PROTOCOLE-OUTILS

**Mission** : formaliser la decision FIGER LF (diagnostic CRLF/LF 2026-08-09) dans le protocole-outils, apres la mission 1 (outil corriger-fins-de-ligne + 11 outils d'ecriture corriges).
**Livrable** : section "Regle FIGER LF (decision 2026-08-09)" inseree dans cerveau-projet/agents/regles-immuables/general/protocole-outils/protocole-outils.001.01.ebauche.md entre le cycle A+B+C et le Processus de creation (ligne 208). Contenu : pourquoi (write_text / open sans newline='' -> CRLF Windows, detecter-usage sanctionnait nos propres outils, autocrlf=true amplifiait), pattern obligatoire (open(..., newline='') CORRECT vs write_text INTERDIT), outil de reference corriger-fins-de-ligne (--dry-run obligatoire), migration + figement git (.gitattributes + autocrlf false -> 0 suspect).
**Validations** : ASCII 0, LF pur preserve (264 -> 314 lignes, 0 CRLF), section bien placee (Regle FIGER LF ligne 208 juste avant Processus de creation ligne 258), contenu coherent avec le cycle A+B+C existant (le tableau deja citait "Fins de ligne LF | CRLF (Windows)").

**Lecons** :
1. LA REGLE EXISTAIT DEJA, IL FALLAIT LA FORMALISER : le protocole citait deja LF comme signature (cycle A+B+C) mais sans donner le PATTERN CONCRET ni l OUTIL - la decision l a rendue operationnelle (comment ecrire, avec quel outil corriger, comment figer git)
2. DOCUMENTER = DONNER LE MOYEN D'EXECUTER : une regle sans pattern concret (newline='') et sans outil (corriger-fins-de-ligne) reste inapplicable - c'est le couple regle + outil + exemple qui la rend exigeable
3. Le protocole-outils est en LF pur : toute edition doit preserver le LF (newline='' en ecriture, jamais CRLF) - piege CRLF confirme encore une fois
4. La section s'insere logiquement apres le cycle A+B+C (qui cite deja LF comme signature) et avant le Processus de creation - l'ordre du protocole suit le flux : pourquoi (detection) -> comment (pattern) -> outil -> migration
5. ASCII strict : aucun accent introduit dans la section (meme dans les exemples de code)
## [LECON] 2026-08-09 -- MISSION 2 FIGER LF TERMINEE : MIGRATION MASSIVE 286 FICHIERS CRLF -> LF

**Mission** : executer le wet par lots (du plus petit au plus grand) de la migration CRLF -> LF + .gitattributes + autocrlf false (decision utilisateur, sequence de securite : dry-run global -> rapport -> validation -> wet).
**Resultat** : 0 fichier texte CRLF restant (585 fichiers en LF), .gitattributes cree ('* text=auto eol=lf', LF), git config core.autocrlf false (local), test-007 15/15 VALIDE, ASCII 0.

**Execution par lots** :
- LOT 1 racine (log-externe.md) : 1 converti
- LOT 2 pense-betes/ : 4 convertis
- LOT 3 agents/ (qui CONTIENT tools/) : 283 convertis -> couvre en fait les lots 3+4 (261 tools + 20 agents + 2)
- Total : 286 fichiers convertis en LF

**BUG DECOUVERT ET CORRIGE (robustesse de l outil)** : buffy/corrections.md contenait des sequences multi-CR (\\r\\r\\r\\n, 713 occurrences) - resultat d'editions successives corrompues. L outil corriger-fins-de-ligne v0.1.0 ne convertissait qu UN \\r\\n a la fois (une passe = 11 lignes au lieu de tout). CORRECTION : remplacement binaire par regex rb'\\r+\\n' -> b'\\n' (convertis TOUS les CR avant un LF). Bump v0.1.0 -> v0.1.1 (py/sh/md/spec + test-007 point 1 aligne) - regle des 5 fichiers respectee.

**Validations** : 0 CRLF hors exemples (le seul reste = assets/images/logo.jpg, binaire image - faux positif), detecter-usage-outils-externes : 20 suspects = 2 dictionnaires + 17 exemples + log-externe.md (TOUS des exceptions legitimes declarees), test-007 15/15 v0.1.1, ASCII 0 sur 5 fichiers outils, .gitattributes LF pur, autocrlf false.

**Lecons** :
1. LE FICHIER MIXTE EST PIEGE : un fichier qui melange CRLF et LF (editions successives avec newline differents) peut contenir des multi-CR (\\r\\r\\r\\n) - l outil doit convertir TOUS les \\r avant \\n, pas seulement \\r\\n. Le regex rb'\\r+\\n' est la solution robuste.
2. UNE PASSE QUI NE CONVERTIT PAS TOUT = ALARME : si l outil convertit 11 lignes au lieu de tout le fichier, verifier les octets bruts (d.find(b'\\r\\n')) - le symptome multi-CR se voit immediatement.
3. agents/ CONTIENT tools/ : quand on convertit agents/ --recursive, tools/ est inclus (283 fichiers = 261 tools + 20 agents + 2). Decouper par domaine est redondant - verifier la hierarchie reelle avant de decouper les lots.
4. detecter-usage-outils-externes : les seuls suspects restants apres migration sont les exceptions declarees (dictionnaires fonctionnels, exemples/, log-externe.md) - un resultat 0 absolu est IMPOSSIBLE par conception, le controle est : 0 suspect HORS exceptions.
5. Le .bak suivi par git (buffy/corrections.md.bak) est converti en LF comme les autres fichiers - c est un fichier commite, le commit de migration l inclura naturellement.
6. Verifier l'idempotence apres correction de l outil : 2e passe = 0 converti prouve que le fichier est stable.
## [LECON] 2026-08-09 -- ECARTS P2 CORRIGES : REGLE IMMUABLE ASCII EN POSITION 1 (28 cases, 9 parcours)

**Contexte** : le re-audit Themis des 14 patterns a revele 28 ecarts P2 (procedure 2 : le premier indice de chaque case d ecriture doit etre REGLE IMMUABLE ASCII). Les ajouts recents (piste B PASSE PAR LE GENERATEUR, REGLE WORKSPACE, CREATION LIMITEE) avaient insere leurs regles en position 1, repoussant l ASCII en position 2+.

**Correction** : edition chirurgicale des JSON (json.load / reordonnancement / json.dump avec newline vide pour LF pur), version bump a chaque parcours modifie.

**Resultat** : 28 cases corrigees sur 9 parcours (athena 2, atlas 4, buffy 9, janus 4, minerve 3, morpheus 1, promethee 3, themis 1, vulcain 1) + 3 cases SANS regle ASCII (buffy c19, c24, janus c9) ont recu la regle ajoutee en position 1. RE-AUDIT P2 : 0 ecart restant sur les 11 parcours (36 cases d ecriture toutes conformes).

**Validations** : JSON valide (9/9), valider-cartes-decision CONFORME (9/9), navigation --liste OK (athena 23, buffy 43, vulcain 25 cases), ASCII 0, LF pur, versions bump : athena 0.1.5, atlas 0.1.6, buffy 0.2.7, janus 0.2.4, minerve 0.1.5, morpheus 0.1.4, promethee 0.1.5, themis 0.2.6, vulcain 0.2.7. Aucune fiche d agent a mettre a jour (les mentions de version sont des notes historiques ou references a la spec, pas au parcours).

**Lecons** :
1. LA CORRECTION P2 EST UN REORDONNANCEMENT, PAS UNE CREATION : la regle ASCII existait dans 25/28 cases en position 2+ - il suffit de la deplacer en position 1. Mais 3 cases (buffy c19/c24, janus c9) n avaient AUCUNE regle ASCII : la procedure exige qu elle soit AJOUTEE.
2. GENERATEURS-CASE ne gere pas le reordonnancement fin des indices - l edition chirurgicale du JSON (json.load/dump) avec newline vide est la methode fiable pour reordonner sans casser le format (indent 2, LF pur).
3. UNIFORMITE DU TEXTE : le texte de la regle ASCII doit etre IDENTIQUE aux autres cases (y compris le double pourcent 100%% present dans les JSON) - la procedure 2 exige un texte UNIFORME.
4. BUMP DE VERSION A CHAQUE PARCOURS MODIFIE : ne pas oublier de bumper 0.x.y -> 0.x.y+1 dans le JSON (les fiches ne mentionnent pas la version du parcours sauf en notes historiques - ne pas les modifier).
5. VERIFICATION AVANT CONCLUSION : toujours relancer le script de verification position 1 apres correction (0 ecart restant = preuve).
## [LECON] 2026-08-09 -- PATTERN 12 APPLIQUE : 37 GARDE-FOUS CREATION LIMITEE INSERES (10 parcours)

**Contexte** : le re-audit Themis des 14 patterns a revele 37 ecarts P12 : les cases de creation/documentation ne portaient pas l indice regle CREATION LIMITEE (perimetre + roles exclus) exige par la procedure 4j.

**Correction** : insertion d un indice regle CREATION LIMITEE dans les 37 cases, texte ADAPTE AU ROLE DE CHAQUE AGENT (athena pense-betes, minerve todos, promethee specs, themis rapports d audit, clio README+lecons, janus missions de controle, morpheus lecons, buffy fichiers du cerveau, atlas documentation, vulcain EXCEPTION outils - il est habilite a creer des outils avec les 5 fichiers). Toutes les cases portent le suffixe commun des roles exclus (JAMAIS outil hors role, JAMAIS test Morpheus, JAMAIS case de parcours Buffy, signaler a Cerberus si manquant).

**Position d insertion** : apres la regle ASCII en position 1 (preservation de la correction P2) ; si PASSE PAR LE GENERATEUR est en position 1, inserer en position 2 (athena c4 : [0] ASCII, [1] GENERATEUR, [2] CREATION LIMITEE).

**Resultat** : 37/37 garde-fous inseres (0 manque), versions bump : athena 0.1.6, atlas 0.1.7, buffy 0.2.8, clio 0.1.4, janus 0.2.5, minerve 0.1.6, morpheus 0.1.5, promethee 0.1.6, themis 0.2.7, vulcain 0.2.8.

**Validations** : re-audit P12 0 manque, NON-REGRESSION P2 0 ecart (position 1 ASCII preservee), JSON valide 10/10, valider-cartes-decision CONFORME 10/10, navigation --liste OK, ASCII 0, LF pur, 0 residu.

**Lecons** :
1. LE GARDE-FOU P12 EST ADAPTE AU ROLE, PAS UN COPIER-COLLER : athena ne cree pas de rapports d audit (themis) ni d outils (vulcain) - le texte doit refleter le perimetre reel de l agent. Seule l EXCEPTION vulcain (habilite a creer des outils) differe du modele JAMAIS outil.
2. INSERTION SANS ECRASER LA CORRECTION P2 : le garde-fou s insere APRES la regle ASCII en position 1 (position 2 si PASSE PAR LE GENERATEUR est en position 1) - les 2 patterns P2 et P12 coexistent sans conflit.
3. LES CASES LECONS COMPTENT : les cases Lecons et retour (retour dans corrections.md) sont des cases de documentation au sens de la procedure 4j - elles ont recu le garde-fou comme les autres.
4. VULCAIN = EXCEPTION ASSUMEE : sa carte porte le garde-fou adapte (outils avec 5 fichiers, mais JAMAIS test Morpheus, JAMAIS case Buffy) - documenter cette exception pour eviter que l audit la signale comme anomalie.
5. VERIFICATION EN DEUX PASSES : re-audit P12 (0 manque) + re-audit P2 (0 regression) - chaque correction de pattern doit prouver qu elle n a pas casse le pattern precedent.
## [LECON] 2026-08-09 -- CASE DOCUMENTATION AJOUTEE AU PARCOURS-VULCAIN (v0.2.9)

**Mission** : corriger la lacune de carte revelee par l audit de conformite d execution P14 (Themis) -- le parcours-vulcain n avait AUCUNE case pour les missions de mise a jour de documentation/fiche.

**Modifications parcours-vulcain (v0.2.8 -> v0.2.9)** :
1. Branche 'documentation' ajoutee dans c16 (Mission hors parcours) -> c16b.
2. Case c16b (indice) 'Documentation / Mise a jour de ma fiche' : REGLE IMMUABLE ASCII (position 1, Pattern 2) + CREATION LIMITEE A LA DOCUMENTATION (Pattern 12, adaptee au role : rapport de mission + mises a jour fiche/corrections/lecons, JAMAIS tools/) + REGLE WORKSPACE + indice outil detecter-impacts (Pattern 14) + indice fichier .md auto (Pattern 9).
3. Case c16c (indice) 'RVAV avant reactiver Cerberus' : REGLE RVAV + fichier rvav-workflow.md.
4. Case c16d (fin) 'FIN - Documentation' : reactiver Cerberus avec bilan (rappel du 3e argument agent_precedent obligatoire, lecon reactiver).
5. Version bump 0.2.8 -> 0.2.9 + vulcain.md aligne.

**Validations** : navigation chemin documentation (c16 -> c16b -> c16c -> c16d FIN) OK, valider-cartes-decision CONFORME, references validees 27 cases, ASCII 0, LF pur, detecter-impacts (vulcain.md + corrections.md a jour apres lecon).

**Lecons** :
1. GENERATEURS-CASE EST L OUTIL DE REFERENCE : ajouter/editer/supprimer des cases avec recablage auto + validation auto (references + guider-parcours --liste) -- ne jamais editer le JSON a la main pour les cases.
2. UNE CASE DE DOCUMENTATION N EST PAS UNE CASE D OUTIL : le chemin se termine par RVAV -> reactiver Cerberus (Pattern 13 : activation directe = reactiver), PAS par la delegation a Morpheus (les tests ne s appliquent qu aux outils). Ne pas recopier le chemin c13b-c14-c15 (modification d outil).
3. L'ERREUR REFERENCES INVALIDES pendant l ajout est NORMALE si la case cible n existe pas encore : ajouter dans l ordre (c16b -> c16c -> c16d) et la validation finale confirme les 27 cases.
4. TOUJOURS verifier la structure de la nouvelle case apres creation : P2 position 1 ASCII, P12 CREATION LIMITEE, P14 detecter-impacts -- les patterns s appliquent aux cases ajoutees comme aux existantes.
5. La version du parcours doit etre alignee dans la fiche (vulcain.md ligne Parcours) : detecter-impacts le signale sinon (Pattern 14).
## [LECON] 2026-08-09 -- ETAPE 2 OUTIL TEMPORAIRE : CASES ALTERNATIVES BESOIN D OUTIL ? DANS LES 10 PARCOURS

**Mission** : ajouter la decision Besoin d'outil ? (TEMPORAIRE vs DURABLE) dans les 10 parcours des agents operationnels (athena, atlas, buffy, clio, janus, minerve, morpheus, promethee, themis, vulcain) + ajuster les garde-fous Pattern 12. Cerberus EXCLU (routeur pur, Pattern 10 : une carte = un role).

**Structure ajoutee par parcours** : entre la case Mission hors parcours/perimetre et la case Signaler le besoin, une decision Besoin d'outil ? (question 2 branches) : TEMPORAIRE -> case Creer l outil temporaire (indices : REGLE IMMUABLE ASCII position 1 + CREATION LIMITEE adaptee au role avec EXCEPTION OUTIL TEMPORAIRE + REGLE WORKSPACE + indice outil generateurs-outil-temporaire avec champ catalogue + indice .md auto Pattern 9) -> FIN - Outil temporaire (message : suppression 0 residu + PROMOTION : 2e utilisation -> ACTIVER VULCAIN directement, Vulcain reactive l agent precedent) ; DURABLE -> case Signaler le besoin (message mis a jour : besoin d outil DURABLE -> activer Vulcain directement - maillon de chaine).

**Lecons** :
1. LE MODELE EST REUTILISABLE PAR SCRIPT : pour une operation repetitive sur 10 parcours, ecrire un script Python parametre (config par agent : ids, texte creation limitee adapte au role, message signaler, version cible) qui appelle generateurs-case en sous-processus (outil de reference : recablage auto + validation) au lieu de 45 commandes manuelles. Le pilote (athena) a valide le modele avant generalisation.
2. LES IDS SUFFIXES PEUVENT ENTRER EN COLLISION : verifier avant d'utiliser sign+b/c/d (ex: vulcain c16b existe deja pour documentation) -- calculer les ids libres dynamiquement.
3. LA BRANCHE VERS SIGNALER N'EST PAS TOUJOURS NON : buffy utilise des reponses nommees (sous-mission/autre-agent/non), vulcain a 3 branches (OUI/NON/documentation). Le recablage doit reutiliser la reponse EXISTANTE de la branche (ne jamais supposer la valeur).
4. LE TEXTE CREATION LIMITEE EST ADAPTE AU ROLE DE CHAQUE AGENT : athena pense-betes, atlas documentation, buffy fichiers du cerveau, clio README+lecons, janus missions de controle, minerve todos, morpheus lecons, promethee specs, themis rapports d audit, vulcain EXCEPTION (il cree des outils durables lui-meme). La clause commune : outil temporaire autorise via generateurs-outil-temporaire (jetable .tmp-*.py, JAMAIS tools/), outil DURABLE -> Vulcain.
5. LES AVERTISSEMENTS generateurs-case (Pattern 5 fin passive, rappel delegation) sont PRE-EXISTANTS sur les messages Signaler le besoin -- ne pas les traiter dans cette mission (hors perimetre).
6. IMPACT : seule la fiche vulcain.md reference la version du parcours (v0.2.9 -> v0.2.10) ; les autres fiches ne mentionnent que le lien sans version -- ne pas modifier inutilement.
7. VALIDATIONS : JSON valide + ASCII 0 + CRLF 0 sur les 10 parcours, valider-cartes-decision --tous 11/11 CONFORME, navigation reelle des 2 chemins (TEMPORAIRE et DURABLE) sur un echantillon, branche documentation de vulcain PRESERVEE (non regression).
## [LECON] 2026-08-09 -- PISTES MIROIRS BUFFY -> ATLAS POUR LA CARTOGRAPHIE (maillon de chaine avec retour)

**Mission** : Buffy a besoin de cartographier un parcours -> elle doit avoir une piste qui l emmene vers Atlas (l agent qui cartographie) ; et Atlas doit avoir la piste miroir (quand un agent a besoin de moi, je fais et je REACTIVE l agent precedent en lui fournissant ma carte).

**Structure creee** :
- BUFFY (v0.2.10) : case c33 Mission hors parcours + branche cartographier -> c38 Activer Atlas pour cartographier (indices : REGLE UNE CARTE = UN ROLE Pattern 10 - la cartographie est le ROLE D ATLAS, je ne cartographie JAMAIS moi-meme + CREATION LIMITEE - Atlas cree le rapport + outil activer-agent-principal) -> c39 FIN - Retour d Atlas avec sa carte (Atlas me REACTIVE en me fournissant sa carte, je reprends ma mission).
- ATLAS (v0.1.9) : case c1 Mission + branche cartographier-agent -> c31 Cartographier pour un agent (indices : ASCII + CREATION LIMITEE A LA DOCUMENTATION - sortie cartographie-<parcours>.md dans le dossier du parcours audite + RVAV + outil cartographier-parcours) -> c31b FIN - Reactiver l agent precedent avec sa carte (reactiver-agent-principal reactiver session-llm-1 <raison> <agent_precedent> en fournissant la carte).

**Lecons** :
1. PISTES MIROIRS : quand l agent A a besoin du role de l agent B, ajouter la piste d activation dans LE PARCOURS DE A (activer B en maillon de chaine) ET la piste de reception dans LE PARCOURS DE B (faire + reactiver A en lui fournissant le livrable). C est la materialisation de la boucle RELAIS -> RETOUR -> CLOTURE (Pattern 5) sans fin passive.
2. ORDRE D AJOUT DES CASES : ajouter la FIN d abord (elle n a pas de suivant), puis l INDICE qui pointe vers elle (--suivant), puis recabler la case decision (--branche). Ne jamais --apres une case qui n existe pas encore (erreur : la case a inserer apres n existe pas).
3. LE LIVRABLE EST FOURNI A L AGENT : la fin d Atlas ne dit pas seulement reactiver -- elle dit reactiver L AGENT PRECEDENT EN LUI FOURNISSANT MA CARTE (le livrable circule avec le retour). Le retour n est pas vide : il transporte le rapport.
4. Pattern 10 respecte : Buffy ne cartographie PAS elle-meme (elle active Atlas), Atlas ne cree pas de case de parcours (role Buffy). Chaque piste pointe vers l agent habilite.
5. VALIDATIONS : navigation reelle des 2 chemins (buffy c33 cartographier -> c38 -> c39 FIN ; atlas c1 cartographier-agent -> c31 -> c31b FIN), valider-cartes-decision CONFORME sur les 2 parcours, ASCII 0, LF pur, references validees (buffy 47 cases, atlas 38 cases).
## [LECON] 2026-08-09 -- PISTES MIROIRS THEMIS GENERALISEES (audit sur demande d un agent)

**Mission** : generaliser le modele de pistes miroirs (active l agent habilite + l agent reactive le demandeur avec son livrable) au besoin inter-agents THEMIS AUDITE SUR DEMANDE D UN AGENT.

**Modifications** (10 parcours) :
1. COTE DEMANDEUR (9 agents operationnels - athena v0.1.8, atlas v0.1.10, buffy v0.2.11, clio v0.1.6, janus v0.2.7, minerve v0.1.8, morpheus v0.1.7, promethee v0.1.8, vulcain v0.2.11) : branche `audit` sur la case decision Mission hors parcours -> case indice Activer Themis pour auditer (Pattern 10 : l audit est le ROLE DE THEMIS, je n audite JAMAIS moi-meme + CREATION LIMITEE + outil activer-agent-principal + LIRE AVANT USAGE) -> FIN - Retour de Themis avec son rapport (Themis me REACTIVE avec son rapport, je reprends ma mission).
2. COTE THEMIS (v0.2.9) : branche `audit-agent` sur c1 (Mission) -> case indice Auditer pour un agent (ASCII pos 1 + CREATION LIMITEE A LA DOCUMENTATION - le rapport d audit est le livrable, JAMAIS toucher aux fichiers de la mission auditee + RVAV + combo audit-themis via combos-moteur) -> FIN - Reactiver l agent precedent avec son rapport (reactiver-agent-principal.py reactiver session-llm-1 <raison> <agent_precedent>).
3. Cerberus EXCLU (routeur pur Pattern 10).

**Lecons** :
1. Le modele de pistes miroirs est GENERALISABLE : demandeur (branche sur la decision + Activer + FIN retour) / executeur (branche sur sa Mission + case d execution + FIN reactiver l agent precedent avec le livrable). Le livrable circule TOUJOURS avec le retour.
2. Ajout chirurgical des branches en Python (liste de dicts {reponse, vers}) pour PRESERVER les branches existantes - generateurs-case `editer --branche` remplace TOUTES les branches, dangereux.
3. Choix des ids : toujours verifier la liste complete des cases (numeriques ET suffixes c20b/c20c/c20d) avant d utiliser cN+1 - les suffixes sont deja pris sur beaucoup de parcours.
4. Pattern 10 respecte partout : aucun agent n audite lui-meme, aucun agent ne cree le rapport de l autre. Chaque piste pointe vers l agent habilite (Themis pour l audit, Atlas pour la cartographie, Vulcain pour les outils durables).
5. VALIDATIONS : navigation reelle des 2 chemins (athena c18 audit -> c22 -> c23 FIN ; themis c1 audit-agent -> c25 -> c25b FIN), valider-cartes-decision --tous = 11/11 CONFORME, ASCII 0, LF pur, references validees, impact vulcain.md aligne v0.2.11.
## [LECON] 2026-08-09 -- SCAN ET CORRECTION GUILLEMETS FRANCAIS (projet 100% propre)

**Mission** : scanner tout le projet pour detecter les fichiers contenant encore des guillemets francais U+00AB/U+00BB et les corriger avec l outil ameliore (v0.2.2).

**Resultat** : le projet actif etait deja 100% propre (hors exemples/ et hors dictionnaires) - le SEUL fichier concerne etait un .bak suivi par git : rapport-audit-conformite-execution-p14-2026-08-09.md.bak (30 guillemets francais, ancienne version du rapport Themis avant sa correction).

**Actions** :
1. Dry-run puis application reelle de corriger-accents-zones-sensibles --all sur le .bak : 39 corrections (30 guillemets + 9 autres non-ASCII), ASCII 0, LF pur, 0 guillemet restant.
2. Suppression du .bak.bak (sauvegarde de sauvegarde creee par l outil, non suivie par git, 0 residu).
3. Scan global final : seuls restent le dictionnaire (exception volontaire, contient " " par fonction) et logo.jpg (binaire JPEG, hors perimetre texte).

**Lecons** :
1. L OUTIL CREE UN .bak.bak QUAND ON CORRIGE UN .bak : avant de corriger un fichier .bak, prevoir la suppression du .bak.bak resultant (artefact non suivi par git, 0 residu obligatoire).
2. LES FAUX POSITIFS DU SCAN : les octets 0xC2/0xAB peuvent apparaitre par hasard dans les fichiers BINAIRES (logo.jpg) - verifier l identite du fichier (binaire vs texte) avant de conclure ; le dictionnaire corriger-dictionnaire-accents.txt ne commence PAS par dictionnaire- (nom corriger-dictionnaire-accents.txt) - l exclusion par prefixe ne le capture pas dans un scan maison (les outils l excluent par sous-chaine du chemin).
3. L OUTIL AMELIORE (v0.2.2) FONCTIONNE : dry-run 39 corrections, application reelle identique, parite py/sh deja confirmee en v0.2.2 - la correction est chirurgicale et fiable.
4. LE PROJET EST VRAIMENT PROPRE : scan decode UTF-8 avec chemins normalises (piege backslash Windows) confirme 0 fichier texte avec guillemets francais hors exceptions - la maintenance reguliere (missions guillemets v0.2.1 + symboles v0.2.2 + ce scan) porte ses fruits.
## [LECON] 2026-08-09 -- AJOUT corriger-symboles AU CATALOGUE (Buffy)

**Mission** : ajouter la commande `corriger-symboles` au catalogue generateurs-commande (le dictionnaire couvre maintenant plus de familles : fleches, box drawing, NBSP, guillemets francais).
**Verdict** : REUSSIE.
**Actions** :
1. Entree `corriger-symboles` ajoutee au catalogue (111 commandes) : alias oriente symboles du script `corriger-accents-zones-sensibles.py` (meme modele que l'alias existant `corriger-accents`, description dediee aux symboles)
2. **BUG DECOUVERT ET CORRIGE** : le modele `--all {recursif} {cible}` faisait perdre `--all` (partie fixe, purge totale regle immuable) quand `recursif` est vide (cas par defaut) : la regex de nettoyage du generateur retire `--flag {placeholder}` ensemble quand la valeur du placeholder est vide. Correction : placer le flag fixe EN FIN de modele, jamais suivi d'un placeholder -> `{recursif} {cible} --all`. Applique aux 2 alias (corriger-accents + corriger-symboles) pour la coherence.
**Lecons** :
1. Un flag EN DUR dans un modele NE DOIT JAMAIS etre suivi d'un placeholder : `--all {recursif}` -> la regex du generateur mange les deux quand recursif est vide. Pattern correct : `{recursif} {cible} --all`
2. La position d'un flag fixe (fin de modele) est la garantie qu'il reste toujours present dans la commande generee
3. detecter-decalages-catalogue : 0 decalage (110 conformes, 1 non testable preexistant = test-001-evaluer-agents-coherence)
4. test-005-generateurs-commande : 24/26 OK, 2 KO PREEXISTANTS hors perimetre (parcours-atlas : version 0.1.10 reelle vs 0.1.5 attendue par le test + 1 commande en dur restante dans la case c30 atlas) - a signaler pour une future mise a jour du test
5. Piege des fichiers de test : ne pas nommer les fichiers de test avec la sous-chaine `test-` (exclue par le filtre par defaut de l'outil -> "Aucun fichier trouve")
6. L'outil corriger-accents-zones-sensibles corrige les symboles MEME sans --all (mode intelligent zones sensibles) mais le mode --all est la purge totale (regle immuable) - les 2 alias le garantissent desormais
## [LECON] 2026-08-09 -- INDICE PASSE PAR LE GENERATEUR CORRIGER-SYMBOLES (10 PARCOURS)

**Mission** : ajouter l'indice PASSE PAR LE GENERATEUR pour corriger-symboles dans le 1er
cas de correction ASCII de 10 parcours (perimetre valide par l utilisateur : 1 cas principal
par parcours ; Cerberus exclu, 0 cas de correction). Insertion apres la regle mentionnant
combo-corriger-ascii (buffy c37 : apres la regle PATTERN 3, cas sans regle combo).

**Lecons** :
1. GARDE-FOU ROUND-TRIP AVANT TOUTE REWRITE JSON : verifier que load + dump(indent=2) + '\n'
   reproduit le fichier a l'identique AVANT de modifier - le saut de ligne final manquant dans
   json.dumps a ete attrape par le garde-fou (le diff contenu = 0 ligne, seule l EOL finale
   differait). Sans ce controle, une rewrite aurait reformate tout le fichier (diff geant).
2. PATTERN INDICE OUTIL STRICT : {type: outil, nom, catalogue, chemin} SANS champ commande
   (pilote strict) - guider-parcours affiche alors catalogue: + PASSE PAR LE GENERATEUR.
   Toujours verifier 3 occurrences par parcours (texte regle + nom + catalogue) = pas de doublon.
3. NE PAS BUMP DE VERSION SANS BESOIN : l ajout d indices est purement additif - bump de
   version entrainerait la cascade fiches (Pattern 14) + tests (test-005 atlas 0.1.10,
   test-004 morpheus) - garder les versions stables, documenter la decision.
4. PILOTE STRICT : corriger-symboles est un ALIAS du script corriger-accents-zones-sensibles
   (catalogue v0.2.3) - l indice outil pointe vers le dossier du script reel, jamais un chemin
   imaginaire.
5. NON-REGRESSION : test-005-generateurs-commande 26/26 OK apres modification des 10 parcours
   (atlas c3/c18 modifies sans casser la navigation testee).
6. OBSERVATION DIVERGENCE PREEXISTANTE : test-004 p7a attend morpheus v0.1.3, parcours reel
   v0.1.7 - a signaler (hors perimetre de cette mission, ne pas corriger ici).
## [LECON] 2026-08-09 -- DEFAILLANCE CLE DUPLIQUEE DANS LE CATALOGUE (inserer-contenu-fichier)

**Mission** : corriger l entree inserer-contenu-fichier du catalogue generateurs-commande -
cle fichier dupliquee (positionnelle obligatoire = cible + optionnelle flag --fichier = source)
et modele {fichier} {position} {contenu} --fichier {fichier} qui generait la cible comme SA
propre source. Correction : cle source dediee + modele {fichier} {position} {contenu} --fichier {source}.

**Lecons** :
1. CLE DUPLIQUEE = COLLISION DE PLACEHOLDER : deux parametres avec la meme cle produisent la
   meme valeur 2 fois dans la commande generee (inserer generait cible.md debut hello
   --fichier cible.md) - TOUJOURS verifier l unicite des cles (scan cibles : 1 seul doublon
   dans les 111 entrees).
2. LIRE L INTERFACE RELLE DE L OUTIL AVANT DE MODELISER : dans inserer-contenu-fichier,
   --fichier (dest=source) = FICHIER SOURCE a inserer, pas la cible - le modele confondait
   cible et source. Le flag du parametre source doit porter une cle distincte ({source}).
3. GARDE-FOU ROUND-TRIP REUTILISABLE : load + dump(indent=2)+LF identique verifie avant rewrite
   (meme methode que pour les parcours) - diff minimal garanti (3 lignes modifiees ici).
4. VERIFICATION PAR GENERATION REELLE : optionnel vide -> flag ABSENT (cible.md debut hello),
   optionnel renseigne -> --fichier src.txt, parite py/sh identique - la generation est la
   preuve de la correction.
5. NE PAS BUMP LA VERSION SANS BESOIN : test-005 p14 verifie catalogue 0.2.3 - correction de
   contenu sans changement de contrat = pas de bump (evite la regression test).
6. IMPACT LIMITE VERIFIE : seul test-007 mentionne l outil (docstring LF) - aucun parcours/
   combo ne depend de la cle fichier-source.
## [LECON] 2026-08-09 -- PISTE AMELIORER INTEGREE AU PARCOURS CERBERUS

**Mission** : brancher la piste Ameliorer dans parcours-cerberus.json (phase 2
du design generateur d amelioration valide : integration Cerberus seul).

**Livrables** (1 fichier, parcours-cerberus.json v0.2.3 -> 28 cases) :
- Branche `{reponse: ameliorer, vers: c1b}` ajoutee dans c1 (Mission), avant
  la branche `autre`
- Case `c1b` (indice) : regle AMELIORATION + regle PASSE PAR LE GENERATEUR +
  outil generateurs-amelioration (chemin/catalogue, sans commande) + regle
  PATTERN 12 (Cerberus DECLENCHE puis ACTIVE, n execute pas) -> suivant c5
- PAS de bump de version (ajout additif, precedent corriger-symboles)

**Validations** : navigation reelle guider-parcours (chemin c0 -> c1 ->
ameliorer -> c1b : regles + outil + LIRE AVANT USAGE affiches) OK * ASCII 0 *
CRLF 0 * diff minimal 29 insertions / 0 suppression * test-005 26/26 OK.

**Lecons** :
1. Le format de parcours-cerberus.json est **indent=1 SANS saut de ligne
   final** (contrairement aux autres parcours en indent=2) : le garde-fou
   round-trip doit DETECTER l'indentation reelle et la presence du saut final
   avant toute reecriture (2 tentatives KO avant detection correcte).
2. Le generateur d amelioration est maintenant DECLENCHE depuis la carte de
   Cerberus (piste ameliorer) : la checklist est posee AVANT l activation de
   l agent habilite -- philosophie : refflechir avant d agir.
3. PATTERN 12 : la case d indice rappelle que Cerberus ne fait que declencher
   la checklist (guidance) puis active l agent habilite -- il n execute pas.
4. L'outil generateurs-amelioration est reference dans le catalogue : la
   navigation affiche automatiquement PASSE PAR LE GENERATEUR + LIRE AVANT
   USAGE (le branchement catalogue fonctionne bout en bout).
## [LECON] 2026-08-09 -- BOUCLE SIGNALEMENT ERREURS HORS MISSION FERMEE (c13d)

**Mission** : fermer la boucle du signalement des erreurs hors mission (perimetre
A seul, decision utilisateur). Diagnostic : la piste c13c/c13d existait dans
parcours-buffy.json mais c13d etait une FIN VIDE d indices - elle ne disait pas
COMMENT signaler les erreurs a Cerberus (la decision Cerberus c12a depend de la
RAISON de la reactivation).

**Livrables** (1 fichier, parcours-buffy.json, c13d enrichie) :
- 3 indices ajoutes a la fin c13d (message existant preserve) :
  1. regle SIGNALEMENT OBLIGATOIRE : erreurs transmises a Cerberus DANS LA
     RAISON de la reactivation (ce que Cerberus lit en c12a -> c12b reparation
     immediate)
  2. regle PASSE PAR LE GENERATEUR : commande de reactivation composee via le
     catalogue + syntaxe reactiver <session> "<raison>" buffy (3e argument
     agent_precedent OBLIGATOIRE)
  3. outil activer-agent-principal (chemin/catalogue, sans commande - raison
     dynamique)
- PAS de bump de version (ajout additif)

**Validations** : round-trip indent=2/LF/saut final OK * structure c13d (message
+ 3 indices) OK * ASCII 0 * CRLF 0 * diff 100% chirurgical (+17/-1, la seule
suppression est la virgule du message car indices suit) * test-005 26/26 OK.

**Lecons** :
1. Une FIN de parcours n est pas un simple stop : elle doit porter les indices
   de CLOTURE (comment reagir a la fin) sinon le flux s arrete sans effet -
   exactement le trou de c13d (signalement non transmis).
2. La RAISON de la reactivation est le CANAL de communication inter-agents :
   c est elle que l agent precedent lit a son retour pour decider (c12a).
   Un signalement qui ne passe pas par la raison est perdu.
3. Etat du circuit apres correction : Buffy c13c OUI -> c13d (raison avec les
   erreurs) -> Cerberus c12a OUI -> c12b reactiver Buffy (reparation) -> c12c
   rejoint -> c13. Boucle complete.
4. Reste hors perimetre (decision utilisateur, perimetre A seul) : les 10
   autres agents n ont pas de piste "Erreurs hors mission" - a traiter en
   mission B ulterieure si decide.
## [LECON] 2026-08-09 -- MIGRATION PILOTE etape 6 : parcours-cerberus v0.3.0 (nouveau format)

**Mission** : migrer le parcours cerberus (pilote) au nouveau format : indices REFERENCES + cases ACTION, avec valider-case comme juge, puis generalisation.
**Resultat** : cerberus passe de v0.2.3 (0 erreur / 15 a alleger) a v0.3.0 (0 erreur / 0 a alleger / CONFORME).
**Lecons** :
1. La migration = 2 gestes : (a) remplacer les indices regle >160 car. par des refs resolvables (pattern-N, protocole-activation) ou des textes courts, (b) convertir les cases de pilotage 'indice' en 'action' (naviguent identiquement dans guider-parcours v0.4.0 : passage automatique)
2. Piege refs : la resolution de valider-case cherche les refs 'regle-*' par prefixe de NOM de fichier -- 'regles-choisir-agent' NE MATCHE PAS (le nom du fichier est 'regles-choisir-agent.md' mais le prefixe attendu est 'regle-'; utiliser le chemin relatif complet a la place)
3. 13 indices longs migres : 6 refs (pattern-6, pattern-8, pattern-10, pattern-12, protocole-activation x2, regles-choisir-agent via chemin) + 7 textes courts <160
4. Surcharge de nombre d indices : c1b (4 indices) et c6 (4 indices) depassaient SEUIL_INDICES=3 -- supprime un indice redondant (PASSE PAR LE GENERATEUR, deja affiche par l'indice outil) dans chaque
5. Le test-009 (valider-case) attendait 'A ALLEGER >= 10' sur cerberus -- a du etre adapte : cerberus = CONFORME maintenant, le temoin A ALLEGER devient buffy (60 a alleger). MAJ du test = partie integrante de la migration
6. Non-regression complete : test-005 26/26, test-009 19/19, test-010 25/25, test-011 19/19, test-012 18/18, test-001-gp VALIDE
7. Navigation guider-parcours intacte : chemins accueil/activation/retour aboutissent tous a PARCOURS TERMINE, refs resolues (pattern-8, protocole-activation affiches)
8. Pattern 14 respecte : fiche cerberus mise a jour (PARCOURS v0.2.0 -> v0.3.0)
9. Normes : ASCII strict + LF pur sur parcours + fiche + test-009
10. La boucle mesure -> produit -> navigue est maintenant complete et prouvee sur UN parcours reel : valider-case (0 a alleger) + guider-parcours (refs resolues, action enchaine) + generateurs-case/carte (produisent des cases/cartes allegees)

**Preuve** : valider-case : CONFORME 0 erreur / 0 a alleger ; detecter-decalages : 112 conformes / 0 decalage.

## [LECON] 2026-08-09 -- MIGRATION DE MON PARCOURS (v0.2.11 -> v0.3.0)

**Mission** : migrer le parcours-buffy vers le nouveau format (indices references + cases action), modele cerberus v0.3.0.
**Resultat** : CONFORME (lecons surcharges) - avant : 0 erreur, 15 surcharges ; apres : 0 erreur, 0 surcharge.

**Lecons** :
1. Les dict d'indices OUTIL/FICHIER (meme avec champ commande long) ne declenchent PAS la regle des 160 caracteres : seule la longueur du TEXTE d'un indice regle compte. Les cases de cerberus CONFORME ont des commandes outil de 200+ caracteres.
2. Le seuil de surcharge est le NOMBRE d'indices (3 max) ET la longueur du texte regle (160 max). Reduire les cases a 3 indices en priorisant : ref de garde-fou (pattern-2 ASCII, pattern-12 creation limitee) + l'outil/fichier actionnable.
3. Les refs valides dans le parcours : pattern-N (resolu depuis spec-guider-parcours), protocole-X (dossier), chemin relatif complet d'un fichier (resolu par os.path.isfile). J'ai utilise pattern-2, pattern-3, pattern-6, pattern-12 + regles-perimetre-workspace.md.
4. Les textes regle recurrents se remplacent par des refs (une place pour chaque chose) : "REGLE IMMUABLE ASCII" -> pattern-2, "CREATION LIMITEE" -> pattern-12, "CONTEXTE TEMPS REEL" -> pattern-6, "UNE CARTE = UN ROLE" -> pattern-10, "PATTERN 3 (spec...)" -> pattern-3.
5. Les cases de type indice avec suivant se convertissent SANS RISQUE en action : guider-parcours navigue identiquement (enchainement sans question). 31 cases converties.
6. Le format des questions est "branches" (liste de {reponse, vers}) et non "choix" : verifier le bon format avant d'ecrire un script de navigation.
7. Apres la migration, le test-009 utilisait mon parcours comme temoin A ALLEGER : bascule sur morpheus (17 surcharges, non migre) - a verifier systematiquement apres chaque migration de parcours.
8. La fiche de l'agent (Pattern 14) doit etre mise a jour avec la nouvelle version du parcours (v0.2.0 -> v0.3.0) en meme temps que la migration.

## [LECON] 2026-08-09 -- GENERATEURS-LIGNE BRANCHE DANS MON PARCOURS (v0.3.0 -> v0.3.1)

**Mission** : brancher generateurs-ligne v0.1.0 (cree par Vulcain, suite des generateurs : carte -> ligne -> case) dans mon parcours (je suis responsable du cerveau-projet).
**Livrables** :
1. Case c10d GERER UNE LIGNE DE PARCOURS AVEC GENERATEURS-LIGNE (type action) : indices ref pattern-2 (ASCII) + ref pattern-12 (CREATION LIMITEE) + outil generateurs-ligne AVEC champ catalogue (PASSE PAR LE GENERATEUR, commande ajouter --config <defaut|config-1|config-2|config-3> [--point-attache] [--reponse] [--rejoint] [--force] [--dry-run]) + suivant c37 (combo corriger-fichier, convergence comme c10c).
2. Branche 'ligne' -> c10d ajoutee dans c10b (3 branches : OUI -> c10c, non -> c11, ligne -> c10d).
3. Version 0.3.0 -> 0.3.1, fiche buffy a jour (Pattern 14 v0.3.1).
4. test-016-migration-buffy adapte : version 0.3.1 + compteur action 31 -> 32 (la nouvelle case c10d est une action) -> 20/20 OK.

**Validations** : valider-case CONFORME (0 erreur, 0 surcharge), navigation chemin ligne -> PARCOURS TERMINE, c10d affichee avec l indice generateurs-ligne, chemin creer -> PARCOURS TERMINE (regression OK), ASCII 0, LF pur, nommage OK, test-017 (generateurs-ligne) 24/24 non-regression.

**Lecons** :
1. Le branchement d un nouvel outil dans MON parcours suit le modele cartographier-parcours (atlas) : case dediee (action) + branche dans la question du flux concerne (c10b) + convergence sur le combo corriger (c37).
2. IMPACT CACHE : toute nouvelle case action change le compteur de types du test-016-migration-buffy (31 -> 32 action) -- verifier systematiquement apres chaque ajout de case.
3. L indice outil avec champ catalogue materialise le PASSE PAR LE GENERATEUR : la commande est composee via le catalogue (--commande generateurs-ligne --reponses ...) au lieu de l ecrire en dur.
4. Le bloc est CONFORME d entree : refs pattern-2/pattern-12 + 1 outil = 3 indices max, texte court, ids conformes.

## [LECON] 2026-08-09 -- RENFORCEMENT DELEGATION DES TESTS (parcours-vulcain v0.2.12)

**Contexte** : l'utilisateur a constate une recidive : Vulcain a ecrit/adapte le test-008 lui-meme
(mission generateurs-amelioration v2.0.0) au lieu d'activer Morpheus pour l'ecrire, puis la chaine
est passee directement a Janus. Sa carte avait deja c8/c14 "Deleguer les tests a Morpheus" mais la
regle n'empechait pas l'ecriture de tests pendant c6 (Developper) et c12 (Modifier).

**Cause racine** :
1. c6/c12 ne contenaient aucune regle explicite "ne jamais ecrire/modifier un fichier de test" ;
   pire, la regle CREATION LIMITEE listait les "5 fichiers (py sh md spec test)" -- ambiguite qui
   laissait croire que le test fait partie des fichiers que Vulcain cree.
2. c8/c14 etaient des auto-controles tardifs qui ne verifiaient QUE l'activation de Morpheus, pas
   l'absence d'ecriture de fichiers test-XXX par Vulcain lui-meme.

**Corrections apportees (parcours-vulcain v0.2.12)** :
1. c6 + c12 : nouvel indice regle position 1 "REGLE ABSOLUE -- DELEGATION DES TESTS (IMMUABLE)" :
   ne JAMAIS ecrire ni modifier un fichier de test (test-XXX, creation OU mise a jour, meme
   adaptation mineure) - role Morpheus ; transmettre le besoin dans la mission de Morpheus.
2. c6 + c12 : regle CREATION LIMITEE corrigee : "4 fichiers de l outil (py, sh, md, spec)" +
   "le fichier de test test-XXX est ECRIT PAR MORPHEUS, jamais par moi".
3. c8 + c14 : question renforcee en 2 points (as-tu active Morpheus pour ECRIRE et EXECUTER ?
   ET n as-tu toi-meme touche a AUCUN fichier de test ?) + regle VERIFICATION EN 2 POINTS.
4. vulcain.md : version parcours v0.2.12 (Pattern 14) + regle delegation de la fiche renforcee
   (mise a jour test-XXX incluse).

**Lecons** :
1. Une regle de delegation doit etre placee la ou l'action se produit (c6/c12), pas seulement au
   point de controle final (c8/c14) -- le controle tardif n'empeche pas la faute.
2. Une regle ambigu (5 fichiers dont test) annule la regle explicite qui la suit ("JAMAIS de
   test") : il faut retirer la contradiction, pas seulement ajouter une nouvelle regle.
3. Pattern valide : "interdiction au point d'action + verification en 2 points au controle final".

## [LECON] 2026-08-09 -- ALLEGEMENT c6/c8/c12/c14 (parcours-vulcain v0.2.13)

**Contexte** : point mineur de l'audit Themis du 2026-08-09 (regles de 341
caracteres > 160 -> A ALLEGER dans c8/c14). L'utilisateur a pose la question
cle : "si on allege c8/c14, on ne risque pas de casser la chaine ?"

**Reponse demontree (preuves, pas intuition)** :
1. La chaine est portee par : type controle + branches (OUI -> c9/c15,
   NON -> c8/c14) + indice outil activer-agent-principal (c8) + question
   (147 car.). PAS par le texte explicatif de l'indice regle.
2. Guider-parcours ne lit jamais les indices regle pour naviguer : il lit
   question + branches (verifie dans guider-parcours.py).
3. Le format ref est deja le standard : 33 indices ref dans les 11 parcours,
   resolus nativement (lignes 178/240).

**Corrections apportees (v0.2.13)** :
1. protocole-tests v0.2.1 : nouvelle section "Delegation des tests" (seul
   Morpheus ECRIT et EXECUTE les test-XXX, creation OU mise a jour, meme
   adaptation mineure - aucun autre agent n'y touche). C'est LE fichier de
   regles que Morpheus lit (case c3 de sa carte) : la ref est utile.
2. c8 + c14 : regle VERIFICATION EN 2 POINTS (341 car.) remplacee par une
   reference vers protocole-tests. Chaine inchangee (assertions type +
   branches + question 147).
3. c6 + c12 : regle DELEGATION DES TESTS (465 car., ajoutee en v0.2.12)
   remplacee par la meme reference - coherence totale (la regle reste au
   point d'action via la ref affichee).
4. Version parcours 0.2.13 + fiche vulcain.md Pattern 14.

**Validations (TOUT VERT)** :
- valider-case returncode 0 : 0 A ALLEGER sur c8/c14 (avant : 2) ;
- navigation construire (c0..c9) ET modifier (c0..c15) : PARCOURS TERMINE
  (PREUVE que la chaine n'a pas bouge) ;
- protocole-tests : section presente, v0.2.1, ASCII 0, LF pur ;
- parcours : JSON valide, ASCII 0, LF pur.

**Lecons** :
1. Alleger une case sans casser la chaine = ne toucher QU'AU TEXTE explicatif
   (indices regle), JAMAIS aux branches / question / indice outil / type.
2. La validation de navigation (guider-parcours PARCOURS TERMINE avant/apres)
   est la PREUVE objective qu'une case controle n'a pas change de comportement.
3. Documenter la regle longue dans un fichier de reference commun (protocole-
   tests) puis la remplacer par une ref : la regle reste visible a l'agent
   (resolution native) sans surcharger la case - pattern "texte -> reference".
4. Un A ALLEGER preexistant (c12 : 6 indices en HEAD, regles longues) n'est
   PAS introduit par l'allegement : distinguer preexistant vs introduit avant
   de conclure (lecon deja apprise a l'audit).

## [LECON] 2026-08-09 -- MIGRATION PARCOURS-MORPHEUS v0.2.0 (pilote 2, spec-refonte etape 6)

**Contexte** : generalisation de la migration des cartes (spec-refonte etape 6).
Apres le pilote cerberus, migration de morpheus (le testeur) au nouveau format
avant de poursuivre sur les autres agents. Nouvelle regle utilisateur appliquee :
Buffy passe par le second controle Janus MEME sans modifier du code.

**Travail realise (parcours-morpheus v0.1.7 -> v0.2.0)** :
1. 10 cases indice -> action (c0b, c0c, c2, c3, c4, c8, c11, c15, c16c, c18) :
   elles avaient toutes un suivant et pas de question (modele cible cerberus).
2. Regles > 160 car. -> refs :
   - c0c : CONTEXTE TEMPS REEL (376) -> ref pattern-6 ;
   - c4 : COMBO ENCAPSULE (332) -> ref pattern-3 + ref protocole-tests ;
   - c8 : CREATION LIMITEE (338) -> ref pattern-2 + regle courte ;
   - c9 : CHAINE BOUT-EN-BOUT (192) -> ref pattern-8 ;
   - c16c : CREATION LIMITEE temporaire (400) -> ref pattern-2 + pattern-12 ;
   - c18 : UNE CARTE = UN ROLE (193) -> ref pattern-10 + pattern-12 ;
   - c0 : veracite (170) -> regle courte ; c2 : 2 regles fusionnees (4 -> 3 indices).
3. Max 3 indices par case (critere d'acceptation 2 de la spec-refonte).
4. Fiche morpheus.md : Pattern 14 (version parcours v0.2.0).

**Validations TOUT VERT** :
- valider-case CONFORME, 0 A ALLEGER, 0 regle > 160, 0 case > 3 indices ;
- navigation des 7 chemins morpheus PARCOURS TERMINE (test direct, test chaine,
  verifier, delegation, temporaire, durable, audit) ;
- JSON valide, ASCII 0, LF pur.

**Lecons** :
1. Migration carte = 3 transformations : type (indice->action), texte long -> ref,
   nb d'indices (<= 3). Le modele cerberus est la reference exacte.
2. La navigation valide CHAQUE chemin (question/controle/fin), pas seulement le
   chemin principal : chaque fin (c10 Activer Janus, c14 Reactiver Cerberus) doit
   etre atteignable (Pattern 13 - la fin suit SA carte).
3. Les refs pattern-N sont resolues nativement par guider-parcours (titre + corps
   depuis la spec-guider-parcours) : une regle longue devenue ref reste visible.
4. Attention aux reponses de navigation apres migration : les cases action ne
   demandent PLUS de reponse -> adapter le nombre de reponses fournies.

## [LECON] 2026-08-09 -- MIGRATION PARCOURS-ATHENA v0.2.0 (4e parcours, spec-refonte etape 6)

**Contexte** : poursuite de la migration des cartes (apres cerberus et
morpheus). Athena (redactrice de pense-betes) migree au nouveau format avec la
chaine obligatoire Buffy -> Janus (regle utilisateur).

**Travail realise (parcours-athena v0.1.8 -> v0.2.0)** :
1. 16 cases indice -> action (dont c0b/c0c oublies au 1er passage - corrige) :
   au final 18 action / 4 question / 5 fin / 0 indice.
2. Regles > 160 car. -> refs :
   - c0c : CONTEXTE TEMPS REEL (376) -> ref pattern-6 ;
   - c4/c5/c9/c14/c20c : ASCII (181-188) + CREATION LIMITEE (350-407) ->
     refs pattern-2 + pattern-12 (2 refs + outil = 3 indices) ;
   - c22 : UNE CARTE = UN ROLE (193) -> ref pattern-10 + pattern-12 ;
   - c0/c0b : relecture/action obligatoire (170/183) -> raccourcies ;
   - c4 : 9 indices -> 3 (la plus chargee du parcours).
3. Max 3 indices par case ; 13 refs au total, toutes resolvables.
4. Fiche athena.md : Pattern 14 (version parcours v0.2.0).

**Validations TOUT VERT** :
- valider-case CONFORME : 0 erreur, 0 a alleger, 0 avertissement ;
- navigation des 6 chemins athena PARCOURS TERMINE (creer, completer,
  delegation, temporaire, durable, audit) ;
- 0 regle > 160, 0 case > 3 indices, refs resolvables contre la spec ;
- JSON valide, ASCII 0, LF pur.

**Lecons** :
1. Verifier la liste des cases indice AVANT de declarer la migration finie :
   c0b/c0c ont ete traites (regles raccourcies/ref) mais leur TYPE n'a pas
   change - reverifier {indice} apres chaque passe.
2. Le mapping des refs est recursif et reutilisable d'un parcours a l'autre :
   ASCII -> pattern-2, CREATION LIMITEE -> pattern-12, CONTEXTE -> pattern-6,
   UNE CARTE = UN ROLE -> pattern-10, WORKSPACE -> regle-perimetre-workspace.
3. Une case a 9 indices (c4) se reduit proprement a 3 avec 2 refs + l'outil
   principal : les regles devenue refs restent visibles via la resolution.

## [LECON] 2026-08-09 -- REGLE JANUS MATERIALISEE DANS MA CARTE (parcours-buffy v0.3.2)

**Contexte** : la regle utilisateur "Buffy passe par Janus meme sans modifier
du code" etait actee et appliquee en pratique (controles sur allegement v0.2.13,
migrations morpheus + athena) mais MA carte ne la contenait pas : mes fins de
creation c8/c22/c27 reactivaient Cerberus directement.

**Corrections (v0.3.2)** :
1. c8 (creation fichier), c22 (creation agent), c27 (creation protocole) :
   "FIN - Reactiver Cerberus" -> "FIN - Activer Janus" avec message de chaine
   bout-en-bout (modele morpheus c10) : j active JANUS (second controle), il
   reactive Cerberus avec son verdict.
2. Regle IMMUABLE JANUS ajoutee dans les 3 fins (145 car.) : "apres TOUTE
   mission (meme sans modifier du code), j active JANUS (second controle) qui
   reactive Cerberus avec son verdict".
3. Description du parcours + fiche buffy.md Pattern 14 (v0.3.2).

**Validations TOUT VERT** :
- valider-case CONFORME 0 A ALLEGER ;
- navigation des 3 chemins de creation (-> c8, -> c22, -> c27) PARCOURS TERMINE
  avec les fins "Activer Janus" atteintes ;
- JSON valide, ASCII 0, LF pur.

**Lecons** :
1. Materieliser une regle = la mettre dans la carte (fins + description), pas
   seulement l'appliquer en pratique : une regle non ecrite est une regle
   oubliee.
2. Le modele morpheus c10 (FIN - Activer Janus) est le pattern standard de fin
   de chaine : "j active le maillon controle qui reactive Cerberus".
3. Regle longue > 160 car. dans une fin -> A ALLEGER : raccourcir (le message
   detaille reste dans le message de la fin et la description du parcours).
4. La regle s'applique a la mission qui la materialise : ce changement de carte
   passe lui-meme par Janus (controle croise de ce fichier).

## [LECON] 2026-08-09 -- ENTREE CATALOGUE generateurs-case-convertir + FIX BUG REGEX FLAGS (Buffy)

**Mission** : ajouter l'entree catalogue generateurs-case-convertir (rendre la sous-commande convertir generable).

**Livrables** :
1. Entree generateurs-case-convertir ajoutee (catalogue v0.2.3 -> 0.2.4, 115 entrees, tri OK, ASCII 0, LF pur) : modele "{chemin} convertir --refs {refs} --seuil {seuil} --version-parcours {version_parcours} {dry_run} {verbose}", 6 parametres (chemin obligatoire, refs/seuil/version_parcours avec flag, dry_run/verbose en flags booleens).
2. BUG REEL DECOUVERT et corrige dans le generateur (py + sh v0.2.1 -> 0.2.2) : le regex de retrait des flags vides "--[a-z0-9-]+\s+{cle}" etait TROP LARGE. Quand un placeholder voisin etait deja remplace par son flag (ex: {dry_run} -> --dry-run), le regex capturait le flag genere du placeholder adjacent et le retirait (commande T1 perdait --dry-run quand verbose vide). Fix : utiliser le flag DECLARE du parametre (re.escape(flag_param) + \s+ {cle}) au lieu d'un motif generique.
3. PIEGE DOUBLE TIRET : mon premier fix ecrivait r"--%s..." % flag_param qui contient deja "--" -> pattern "----refs" qui ne matche jamais (T2/T4/T5 gardaient --refs sans valeur = commandes invalides). CORRIGE : r"%s..." directement (le flag declare contient ses tirets).

**Tests reels** : T1 dry-run OUI/verbose NON -> --dry-run present; T2 minimal -> tout retire sauf --seuil 160 (defaut); T4/T5 combinaisons OK; non-regression activer-activer, valider-nommage, detecter-impacts, guider-parcours inchangees; parite py/sh v0.2.2 + generation identique; ASCII 0 + LF pur sur les 5 fichiers.

**3 KO test-005** : valeurs de version figees (v0.2.1 attendu vs v0.2.2 reel, catalogue 0.2.3 vs 0.2.4) -> tests a mettre a jour par Morpheus (DELEGATION DES TESTS, je ne corrige pas les tests).

**Lecons** :
1. Les sous-commandes = entrees catalogue SEPAREES (activer-activer/reactiver) ; generateurs-case avait une entree generique {chemin} qui ne couvrait pas convertir -> creer l'entree dediee.
2. Toujours tester la generation REELLE avec plusieurs combinaisons de reponses (vides + remplis + flags) : le bug n'apparait qu'avec un flag adjacent vide.
3. Ne jamais ecrire "--%s" quand la valeur contient deja les tirets (double tiret silencieux).
4. PIEGE ECRITURE ASCII : ne JAMAIS ouvrir un fichier existant en mode 'w' avec encoding ascii si le contenu source contient du non-ASCII (plantage -> fichier TRONQUE a 0 octet). Construire tout le contenu en memoire PUIS ecrire en utf-8, ou filtrer avant. Le fichier corrections.md contenait 9 points medians U+00B7 preexistants (HEAD) : corriges en '*' (dette ASCII preexistante corrigee au passage).

## [LECON] 2026-08-09 -- CARTE BUFFY : c10c UTILISE generateurs-case-convertir (parcours v0.3.3) (Buffy)

**Mission** : corriger ma carte pour que la conversion des parcours passe par la commande catalogue generateurs-case-convertir (creee dans la chaine precedente).

**Livrables** :
1. c10c (Gerer les cases) : indice outil generateurs-case -> format PASSE PAR LE GENERATEUR (commande en dur RETIREE, juste nom + catalogue + chemin), + NOUVEL indice outil generateurs-case-convertir (nom + catalogue + chemin) pour couvrir la conversion en masse.
2. c10d (Gerer une ligne) : commande en dur generateurs-ligne retiree (coherence PASSE PAR LE GENERATEUR).
3. ALLEGEMENT c10c : 4 indices (2 refs + 2 outils) depassaient le max 3 -> ref pattern-12 retiree (justification : c10c MODIFIE des cases d'un parcours existant, ce n'est PAS une case de creation d'outil - le Pattern 2 ecriture ASCII est conserve). valider-case CONFORME (0 erreur, 0 a alleger).
4. Version parcours 0.3.2 -> 0.3.3 + fiche buffy.md mise a jour (Pattern 14).

**Validations** : valider-case CONFORME, transitions c10b (OUI->c10c, ligne->c10d, non->c11) intactes, c10c/c10d->c37, JSON valide, ASCII 0, LF pur.

**Lecons** :
1. La commande generateurs-case-convertir est desormais generable : quand une carte modifie des parcours, elle doit la referencer (nom + catalogue + chemin) au lieu d'ecrire la ligne en dur.
2. Ajouter un outil a une case existante peut depasser le max 3 indices -> verifier valider-case et alleger (retirer la ref la moins pertinente selon la nature de la case : creation vs modification).
3. Toujours verifier les transitions apres modification d'une zone de branches (c10b) : le flux doit rester intact.
## [LECON] 2026-08-09 -- MIGRATION 4 PARCOURS TERMINEE (atlas, clio, janus, themis)

**Mission** : finir la migration des cartes au nouveau format (100% actions, 0 indices).
**Resultat** : 4 parcours migres via generateurs-case convertir + mapping generique.

**Lecons** :
1. La migration utilise generateurs-case convertir avec un mapping generique {motifs: [{contient, ref}], cases: {}} - les motifs communs (RELECTURE, CONTEXTE, ASCII, CREATION LIMITEE, WORKSPACE, VALIDER) sont partages par tous les parcours
2. Les refs resolvables sont soit pattern-N (verifie dans la spec-guider-parcours), soit chemins relatifs existants (protocoles/regles)
3. valider-case en mode auto du wet est trop optimiste : la validation independante apres affinage est LA reference (atlas: 11 a alleger apres wet)
4. Modele d'allegement standard pour les cases d'ecriture/creation : pattern-2 + pattern-12 + outil = 3 indices (modele athena/buffy c10c). Retirer pattern-12 quand la case ne cree pas d'outil durable
5. Cas speciaux : c16 themis (5 evaluateurs) reduit a 3 outils cles + titre explicite ; regles specifiques > 160 car (ex: lecon Clio 180 car) a raccourcir en gardant le sens
6. Apres migration : verifier valider-cartes-decision --agent <nom> = CONFORME + navigation PARCOURS TERMINE pour chaque parcours
7. Les fiches peuvent deja etre a jour (atlas/clio v0.2.0 en fiche avant la migration du parcours) - la version du parcours rattrape la fiche, ne pas la casser
8. Observations hors perimetre notees : valider-cartes-decision.py ligne 22 mentionne "spec v0.2.9" alors que la spec est en v0.5.0 (mention stale preexistante, docstring) - a corriger plus tard
9. DELEGATION DES TESTS respectee : test-005 (versions atlas fige en v0.1.10) mis a jour par Morpheus, pas par Buffy

**Fichiers modifies** : parcours-atlas v0.2.0, parcours-clio v0.2.0, parcours-janus v0.3.0, parcours-themis v0.3.0 (valider-case CONFORME + navigation OK), fiches janus.md/themis.md alignees.

## [LECON] 2026-08-10 -- 15 LIENS CASSES CORRIGES (observation Themis, score coherence 50 -> 75)

**Contexte** : evaluer-coherence (audit Themis 2026-08-10) signalait 15 liens internes casses
preexistants (fichiers jamais modifies depuis le commit initial). Les cibles existaient TOUTES,
seuls les chemins relatifs etaient inexacts.

**Correction** (10 fichiers, 15 liens) :
1. fiche-agent-template.md : lien placeholder parcours-<agent>.json mis en backticks (texte,
   pas un lien markdown resolvable) + 2 liens ../tools/ -> tools/ (le ../ etait en trop depuis agents/)
2. conventions/index-conventions.md + regles-immuables/index-regles-immuables.md : ../index-pense-bete.md
   -> ../../pense-betes/index-pense-bete.md, ../specs/index-spec.md -> ../../pense-betes/specs/index-spec.md
3. themis/themis.md : 2 liens rvav-workflow/ (dossier) -> rvav-workflow.md (fichier) + correction
   du chemin relatif (../../agents/ -> ../ depuis agents/themis/)
4. pense-betes/index-pense-bete.md : conventions/ -> ../agents/conventions/, regles-immuables/ -> ../agents/regles-immuables/
5. pense-betes/specs/index-spec.md : ../conventions/... -> ../../agents/conventions/..., ../regles-immuables/... -> ../../agents/regles-immuables/...
6. pense-betes/specs/todo/index-todo.md : ../../regles-immuables/ -> ../../../agents/regles-immuables/
7. recherches-web/badges-github-shields/badges-README-github.md : ../agents/ -> ../../agents/
8. janus/controles/controle-protocole-creation-combos-2026-08-08.md : protocole-creation-combos/
   -> ../../regles-immuables/general/protocole-creation-combos/

**Verifications** : evaluer-coherence : 15 liens casses -> 0 (score 50/100 -> 75/100), valider-liens
0 invalide sur les fichiers modifies, ASCII 0 + LF pur sur les 10 fichiers.

**Lecons** :
1. evaluer-coherence a une liste MOTIFS_GENERIQUES (texte, chemin, ancien.md, fichier.md, index.md,
   frere-a, ...) qui filtre les exemples de documentation : un lien vers une cible fictive
   d'exemple n'est PAS compte - il faut reproduire cette logique pour savoir quels liens sont
   reellement casses
2. Un meme lien peut apparaitre a PLUSIEURS endroits d'un meme fichier (themis.md : rvav-workflow
   en 2 occurrences) - scanner TOUTES les occurrences, pas seulement la premiere
3. Les chemins relatifs depuis un dossier profond demandent de compter les ../ correctement :
   depuis agents/ vers pense-betes/ il faut ../../ (agents/.. = cerveau-projet/, puis pense-betes/)
4. Un lien vers un DOSSIER (rvav-workflow/) est casse si la cible est un FICHIER (.md) - verifier
   l'existence reelle de la cible (fichier vs dossier)
5. La correction de liens preexistants ne touche JAMAIS aux exemples volontaires de documentation
   (convention-liens.md, valider-liens.md utilisent des cibles fictives legitimes)

## [LECON] 2026-08-10 -- GARDE-FOU FORMAT DES LECONS AJOUTE (piege markdown, 2 fichiers)

**Contexte** : lors de la correction des 15 liens casses, la lecon Janus dans corrections.md
contenait un exemple litteral de syntaxe de lien (texte entre crochets suivi d'une cible entre
parentheses) -> evaluer-coherence l'a interprete comme un VRAI lien casse (score 75 -> 50/100).
Le format '## [LECON]' n'etait documente nulle part comme convention.

**Ajout** (garde-fou du piege) dans 2 fichiers :
1. protocole-auto-correction.001.01.ebauche.md : nouvelle section "Format d'ecriture des lecons
   (garde-fou)" inseree avant "Types de corrections" (Etape 5) - regle de format + piege a eviter
   + methode pour proteger un exemple de syntaxe
2. corrections-template.md : bloc "FORMAT DES LECONS (garde-fou)" ajoute apres le PRINCIPE de la
   section LECONS

**Verifications** : ASCII 0 + LF pur sur les 2 fichiers, evaluer-coherence reste 0 lien casse
(score 75/100) - le garde-fou est redige en DECRIVANT la syntaxe sans produire le motif
interpretable (lecon du piege appliquee a la documentation elle-meme).

**Lecons** :
1. Documenter une regle de format demande d'appliquer la regle AU TEXTE DE LA REGLE : decrire la
   syntaxe en toutes lettres, jamais l'ecrire en litteral
2. Le format '## [LECON] <date> -- <titre>' est maintenant la convention documentee (protocole
   + template) - il etait utilise en pratique sans etre ecrit
3. Un piege decouvert en production doit devenir un garde-fou DOCUMENTE (pas seulement une lecon
   chez un agent) : le protocole est le bon endroit pour les regles durables

## [LECON] 2026-08-10 -- 2 PROTOCOLES DEDIES A LA VERIFICATION DU TRAVAIL DE BUFFY CREES

**Mission** : creer 2 protocoles separes pour la verification du travail de
Buffy (documents du cerveau-projet) : protocole-controle-buffy (Janus, second
controle croise) et protocole-audit-buffy (Themis, audit de conformite).

**Resultats** :
- protocole-controle-buffy.001.01.ebauche.md cree (10 etapes E1-E10 : fichiers
  modifies, preuve d integrite git status, doc complete, toutes les formes de
  liens, piege markdown, lecons, conventions, separation, parcours/fiches,
  verdict) + fichier d exemples (2 cas reels) + pieges courants
- protocole-audit-buffy.001.01.ebauche.md cree (9 etapes E1-E9 : croisement
  mission/carte/deroulement, conformite d execution, impact Pattern 14, fin
  suit SA carte, reactiver R1-R5, qualite documentaire, parcours/fiches,
  piege lecons, rapport) + exemples + pieges
- index-regles-general.md : 2 entrees ajoutees (table Protocoles)
- janus.md + themis.md : liens ajoutes dans Protocoles applicables
- Verification : ASCII 0 + LF pur + valider-tableaux CONFORME (2/2) +
  evaluer-coherence 0 lien casse (75/100) + 7 sections standard presentes
  dans les 2 protocoles

**Lecons** :
1. LES CHEMINS RELATIFS D UN PROTOCOLE : depuis regles-immuables/general/
   protocole-XXX/, le bon pattern est : 2 points + 2 points + 2 points pour
   conventions/ et tools/ (protocole-creation-combos sert de reference), et
   2 points + 2 points pour les protocoles voisins du meme dossier general/.
   J avais d abord ecrit des chemins trop courts (2 niveaux au lieu de 3) :
   evaluer-coherence a detecte 16 liens casses - corriger TOUJOURS en
   resolvant les cibles reelles, pas a vue
2. La verification croisee outil (evaluer-coherence) + resolution manuelle
   (os.path) est la methode fiable pour les liens relatifs : l outil compte,
   la resolution identifie
3. Le piege markdown s applique aussi aux PROTOCOLES : decrire une syntaxe
   de lien en toutes lettres sans produire le motif (texte entre crochets
   suivi d une cible entre parentheses) - mes 2 protocoles en donnent
   l exemple sans le produire (evaluer-coherence 0 lien casse)
4. Les fiches janus.md et themis.md referencent maintenant leurs protocoles
   dedies : la section Protocoles applicables est le point d entree naturel
   pour les agents qui doivent appliquer un protocole

## [LECON] 2026-08-10 -- PROTOCOLE-CONTROLE-BUFFY BRANCHE DANS LE PARCOURS-JANUS v0.3.1

**Mission** : brancher le protocole-controle-buffy dans le parcours-janus pour
que Janus l applique quand il controle le travail de Buffy (documents du
cerveau), puis tester la chaine complete en reel (Buffy -> Janus -> Themis).

**Resultats** :
- parcours-janus.json : version 0.3.0 -> 0.3.1
- case c11 (Ecrire la mission de controle AVANT) : indice fichier ajoute ->
  protocole-controle-buffy (etapes E1-E10 si le controle porte sur le travail
  de Buffy)
- case c18 (Ecrire la mission de controle AVANT) : indice fichier identique
- case c8 (Verdict du controle) : regle ajoutee -> les points de controle du
  travail de Buffy sont ceux du protocole-controle-buffy
- Verification : JSON valide (32 cases intactes, 0 echappement, ASCII strict,
  LF pur), valider-cartes-decision --tous 11/11 CONFORME, navigation
  guider-parcours 33 cases OK, evaluer-coherence 0 lien casse (75/100)

**Lecons** :
1. LE BRANCHEMENT D UN PROTOCOLE DANS UNE CARTE : les cases "Ecrire la mission
   de controle AVANT" (c11/c18) sont le point d entree naturel : c est la
   que l agent decide QUEL protocole appliquer selon la nature du travail
   controle (outil Vulcain vs documents Buffy). La case de verdict (c8) porte
   la regle de rappel
2. json.dump REECRIT le fichier entier : le diff git peut etre large meme pour
   une petite modification (56+120 lignes) si le working tree contenait deja
   des changements non commites (ici la migration 0.2.7 -> 0.3.0). VERIFIER
   l integrite par la structure (nb cases, type de chaque case, branches) et
   non par la taille du diff
3. La verification d un parcours modifie = 3 outils complementaires :
   valider-cartes-decision --tous (structure + types), guider-parcours --liste
   (navigation), evaluer-coherence (liens). Les 3 doivent etre verts avant
   de conclure
4. La chaine complete Buffy -> Janus -> Themis est maintenant operationnelle :
   Buffy branche (protocole-controle-buffy), Janus controle en l appliquant,
   Janus active Themis (case c31) qui audite avec le protocole-audit-buffy et
   reactive Janus avec son rapport

## [LECON] 2026-08-10 -- 2 CASES FAUSSES REACTIVER/ACTIVER CORRIGEES + PROTOCOLE-ACTIVATION PATTERN 13

**Mission** : corriger les cases qui induisaient les agents en erreur sur la
reactivation (recommandations HAUTE de l audit Themis) : atlas c31b et themis
c25b donnaient la commande reactiver pour revenir a l agent precedent, mais
reactiver ramene TOUJOURS a Cerberus (conception de l outil).

**Resultats** :
- atlas c31b : titre + message corriges - "FIN - Activer l agent precedent
  avec sa carte" + commande activer-agent-principal.py activer session-llm-1
  <agent_precedent> <raison>
- themis c25b : idem - "FIN - Activer l agent precedent avec son rapport"
- protocole-activation : ligne Fin de mission enrichie avec le Pattern 13 et
  le tableau de decision a 3 modes : MODE DIRECT (active par Cerberus ->
  reactiver), MODE CHAINE (active par un agent -> activer le suivant ou
  l agent precedent), DERNIER MAILLON (reactiver avec bilan consolide)
- Verification : 0 case fausse restante (scan des 11 parcours), cartes 11/11,
  evaluer-coherence 0 lien casse, navigation OK, ASCII 0 + LF pur

**Lecons** :
1. UNE CASE DE FIN DOIT DONNER LA BONNE COMMANDE : le texte et la commande
   doivent etre coherents. "REACTIVER l agent precedent" avec la commande
   reactiver ramene a Cerberus - la bonne formulation est "ACTIVER l agent
   precedent" avec la commande activer <agent> (accepte n importe quel agent)
2. LE PATTERN 13 EST MAINTENANT PROPAGE : il ne suffit pas qu il soit dans la
   spec-guider-parcours - le protocole-activation (source de verite de
   l activation) doit porter la regle de decision (QUI m a active ?) et les
   3 modes
3. LA REGLE DE DECISION DANS UNE LIGNE : le critere unique est "qui m a
   active ?" : Cerberus -> reactiver ; agent -> activer (suivant ou
   precedent) ; dernier maillon -> reactiver avec bilan
4. L audit Themis a ete chirurgical : sur 37 fins mentionnant Cerberus,
   seulement 2 etaient fausses - le scan apres correction confirme 0 reste
## [LECON] 2026-08-10 -- RECOMMANDATIONS MOYENNES AUDIT REACTIVER APPLIQUEES (Buffy)

**Mission** : appliquer les recommandations MOYENNE de l'audit Themis reactiver/activer (regle de decision dans les fins de parcours + verifier les 11 fiches agents).

**Actions realisees** :
1. **4 fins de parcours** precisees  (activation directe par Cerberus)  : atlas c11, clio c12, minerve c10, themis c13 -- la condition de la fin REACTIVER-CERBERUS est desormais explicite (morpheus c14 et janus c10 l'avaient deja).
2. **Fiche morpheus.md** : 2 corrections -- titre de section  Pour revenir a Vulcain  + commande du bloc code corrigee `reactiver` -> `activer <session> vulcain` (ligne 165). C'etait le MEME piege que les cases (reactiver ramene toujours a Cerberus) : c'etait la source reelle de l'erreur de Morpheus dans la chaine precedente.
3. **Fiche atlas.md** : ligne 172  TOUJOURS reactiver Cerberus  corrigee en reference au Pattern 13 (fin = SA carte) -- la ligne 171 (Pattern 8) etait deja correcte.

**Lecons** :
1. **La regle des 5 fichiers s'applique aussi aux FICHES agents** : l'audit Themis ne scannait que les parcours JSON -- la fiche morpheus.md portait le piege reactiver sans etre detectee. Toujours scanner fiches + parcours + protocoles pour les classes de bugs transverses.
2. **Le piege reactiver se propageait a 3 endroits distincts** (2 cases + 1 fiche) : apres correction d'une classe de bug, refaire un scan GLOBAL (pas seulement la cible initiale) pour trouver tous les porteurs.
3. **Modification chirurgicale de JSON via json.dumps risque de reformater** : pour les parcours, passer par des remplacements de texte precis (str_replace sur les blocs JSON) ou verifier l'integrite apres (0 echappement \uXXXX, meme nombre de cases).
4. **Verification finale** : cartes 11/11, evaluer-coherence 0 lien casse, ASCII 0 + LF pur sur les 6 fichiers modifies.
## [LECON] 2026-08-10 -- PROTOCOLE-SANTE-FICHIERS-AGENTS CREE + BRANCHE PARCOURS-JANUS v0.3.2 (Buffy)

**Mission** : creer le protocole sante-fichiers-agents pour Janus (verification periodique de l etat des fichiers agents) + le brancher dans le parcours-janus.

**Actions realisees** :
1. **Protocole cree** : `regles-immuables/general/protocole-sante-fichiers-agents/protocole-sante-fichiers-agents.001.01.ebauche.md` (modele protocole-controle-buffy, 7 etapes E1-E7 : inventaire, coherence fiche/parcours, format, normes, regles a jour, rapport, verdict). ASCII 0, LF pur.
2. **Reference** : index-regles-general.md (entree) + fiche janus.md (section Protocoles applicables).
3. **Parcours-janus v0.3.1 -> v0.3.2** : nouvelle case c33  Verifier l etat des fichiers agents  (action, 3 indices : ref pattern-2, fichier protocole-sante, outil creer-fichier pour le rapport) + branche  sante  dans c1 (Mission). Suivant : c8 (Verdict) pour rejoindre la boucle existante.

**Lecons** :
1. **valider-case impose 3 indices max** : ma premiere version de c33 avait 4 indices (ref pattern-2 + ref pattern-12 + fichier + outil) -> A ALLEGER. Retrait de la ref pattern-12 (redondante avec le fichier protocole qui porte deja la regle) -> 3 indices conformes.
2. **Ne pas aggraver les surcharges preexistantes** : janus etait deja A ALLEGER 3 (c8 indice 201 chars, c11/c18 4 indices) avant ma mission -- ma case c33 est conforme, le verdict reste a 3 (preexistant), je n ajoute aucune surcharge.
3. **Lien casse preexistant signale, pas corrige** : `spec-refonte-cartes-decision.001.01.ebauche.md` est supprime (D) dans le working tree -- le lien dans index-spec.md est casse. Hors perimetre de ma mission, a signaler dans le rapport (lien casse = lecon : verifier evaluer-coherence avant/apres).
4. **La navigation c33 -> c8 -> c9 -> c10 (fin) fonctionne** : la nouvelle branche sante rejoint proprement la boucle de verdict existante.

## [LECON] 2026-08-10 -- CORRECTION 4 ECARTS PROTOCOLE SANTE (Buffy)

**Mission** : corriger les 4 ecarts legers detectes par Janus lors du premier
etat des lieux sante-fichiers-agents.

**Corrections appliquees** :
1. janus.md : REGLE ABSOLUE -- PARCOURS (v0.3.0) -> (v0.3.2) -- seule mention
   de version du parcours dans la fiche (la ligne Parcours n'a pas de version).
2. promethee/corrections.md : 8 caracteres U+00B7 (point milieu) remplaces par
   "-" (lecons historiques lignes 177, 178, 209) -- ASCII 0.
3. athena.md : ajout de la section "Pour terminer ma mission (la fin suit SA
   carte)" sur le modele des fiches migrees (clio.md), adaptee a sa fin reelle
   : elle active Promethee (maillon de chaine), elle ne reactive pas Cerberus.
4. cerberus.md : relecture alignee sur le Pattern 13 -- remplacement du
   "cycle fondamental" (CERBERUS -> AGENT -> CERBERUS -> JANUS -> CERBERUS ->
   CLIO, philosophie reactiver Cerberus systematique) par le nouveau schema
   (CERBERUS -> AGENT_1 -> AGENT_2 -> ... -> CERBERUS, seul le dernier maillon
   reactive Cerberus), ligne Clio "Agents disponibles" corrigee (activer Clio
   quand la mise a jour du README est necessaire, plus "apres chaque mission"),
   frontmatter cycle.sortie et specialites alignes, version fiche 0.2.1 +
   entree Historique.

**Lecons** :
- La derive silencieuse des fiches agents se corrige avec des remplacements
  chirurgiques : verifier TOUTES les mentions de version (ici une seule).
- La section "Pour terminer ma mission (la fin suit SA carte)" est le modele
  standard des fiches migrees : a copier-adapter a la fin reelle de chaque
  agent (maillon de chaine vs activation directe).
- La relecture d'une fiche = aligner le cycle, les connexions et l'historique
  sur le paradigme actuel, pas seulement corriger une ligne.

**Outils utilises** : lire-fichier, editer-fichier, valider-conformite-ascii,
valider-cartes-decision, activer-agent-principal.

## [LECON] 2026-08-10 -- PATTERN 13 FORMULE DANS FICHE MORPHEUS (Buffy)

**Mission** : formuler explicitement le Pattern 13 (la fin suit SA carte) dans
la fiche morpheus (point mineur du re-audit sante), en conservant sa REGLE
DELEGATION et en alignant avec sa fin reelle de carte.

**Modification** : ajout dans la section "UTILISATION DE
activer-agent-principal" (apres le bloc "Pour revenir a Vulcain") de la
sous-section "### Pour terminer ma mission (la fin suit SA carte)", adaptee
aux fins reelles du parcours morpheus : c10 FIN - Activer Janus (second
controle), c14 FIN - Reactiver Cerberus (activation directe), retour VULCAIN
apres delegation (MODE CHAINE).

**Lecons** :
- La formulation Pattern 13 doit reflete les fins REELLES de la carte de
  l'agent (verifiees dans parcours-<agent>.json), pas un modele generique :
  chaque agent a ses maillons de chaine et ses fins propres.
- La REGLE DELEGATION existante (VULCAIN -> MORPHEUS -> VULCAIN) et la regle
  "Pour revenir a Vulcain" (MODE CHAINE, jamais reactiver) sont conservees
  integralement : la nouvelle section les reference sans les dupliquer.
- Verifications : ASCII 0 + LF pur + valider-cartes-decision 11/11.

**Outils utilises** : lire-fichier, editer-fichier, valider-conformite-ascii,
valider-cartes-decision, activer-agent-principal.

## [LECON] 2026-08-10 -- PROTOCOLE SANTE E5 RENFORCE (CROISEMENT FICHE/PARCOURS) (Buffy)

**Mission** : integrer la lecon du re-audit sante dans le protocole-sante :
verifier le Pattern 13 en CROISANT la fiche avec les fins reelles de la carte
(identifiants cX), pas seulement par une mention textuelle.

**Modification** (protocole-sante-fichiers-agents v0.1.0 -> v0.1.1) :
- E5 du tableau : Pattern 13 verifie par croisement fiche/parcours
  (sous-criteres E5a/E5b/E5c) + outil parcours-<agent>.json ajoute.
- Nouvelle section "### Detail E5 : verifier le Pattern 13 par croisement
  fiche/parcours" apres le tableau des etapes :
  - E5a : mention textuelle ("la fin suit SA carte" formulee explicitement) ;
  - E5b : croisement fiche/parcours -- chaque fin citee (cX) doit correspondre
    a une case de type fin dans parcours-<agent>.json avec le bon titre ;
  - E5c : conformite du sens (fin declaree = fin reelle : direct -> reactiver
    Cerberus ; maillon -> activer le suivant ; dernier maillon -> Cerberus).

**Lecons** :
- Piege d'insertion : NE JAMAIS inserer des blocs de citation (>) ou des
  sous-sections (###) entre les lignes d'un tableau markdown -- cela casse le
  tableau. Toujours inserer le detail APRES la derniere ligne du tableau.
- Le veritable critere du Pattern 13 est le CROISEMENT fiche/carte : la fiche
  doit citer des identifiants cX qui existent reellement dans le parcours avec
  le bon type (fin) et le bon sens. Une simple phrase generique ne suffit pas.
- La version du protocole doit etre bumpee a chaque evolution du contenu.

**Outils utilises** : lire-fichier, editer-fichier, valider-conformite-ascii,
valider-cartes-decision, activer-agent-principal.

## [LECON] 2026-08-10 -- REGLES-GROUPES-AGENTS + PATTERN 16 REECRIT (CORRECTION D ASSIGNATION) (Buffy)

**Contexte** : l utilisateur a clarifie l organisation du cerveau en 3 groupes
et a signale une faute d assignation : Promethee (trio projets futurs) avait
documente le Pattern 16 dans la spec-guider-parcours (outil du cerveau-projet).

**Tache 1 -- Regle-immuable regles-groupes-agents** : cree
cerveau-projet/agents/regles-immuables/general/regles-groupes-agents.md :
1) Coordination : Cerberus ; 2) Cerveau-projet (gestion du dossier
cerveau-projet lui-meme : outils, parcours, fiches, protocoles, spec des
outils, README) : Buffy (RESPONSABLE), Vulcain, Morpheus, Janus, Atlas,
Themis, Clio ; 3) Trio projets futurs (pense-betes/specs/todos pour le dev
des apps futures) : Athena, Promethee, Minerve. REGLE ABSOLUE : le trio n est
JAMAIS utilise pour developper le cerveau-projet. Referencee dans
index-regles-general.md + section "Groupes d agents" dans AGENTS.md.

**Tache 2 -- Pattern 16 reecrit** : suppression complete du bloc Pattern 16
ecrit par Promethee (revert v0.5.0 : version, en-tetes patterns v0.2.28
retires, procedure 15 patterns) puis re-ecriture ENTIERE du Pattern 16 par
Buffy (responsable) : v0.6.0, 6 etapes (DETECTER / TRIER reference-combo /
ANTI-DOUBLON obligatoire via rechercher-texte present-partiel-absent /
DEPLACER jamais supprimer / PRISE EN COMPTE obligatoire par resolution
affichee / VERIFIER), exemple janus c8-c11-c18, lien patterns 3-7 et
spec-refonte 4.2.

**Lecons** :
- REGLE DE ROLE (lecon utilisateur) : ne JAMAIS assigner le trio (athena,
  promethee, minerve) au developpement du cerveau-projet. Tout fichier de
  cerveau-projet (y compris les spec des outils comme spec-guider-parcours)
  est du domaine de Buffy (responsable) ou du groupe cerveau-projet.
- La matrice regles-choisir-agent disait deja "Creer une spec -> Promethee",
  mais cela concerne les SPECS DE PROJETS (pense-betes/specs/todos), PAS les
  spec des outils du cerveau : distinguer spec de projet futur et spec d outil.
- Correction d une erreur d assignation : supprimer completement le livrable
  de l agent non habilite (revert), puis re-ecrire par l agent responsable.
- Piege ASCII : la section ajoutee dans AGENTS.md contenait des accents
  (gerent, lui-meme, utilise, developper, em-dash) -- corriger en ASCII strict.

**Outils utilises** : lire-fichier, editer-fichier, creer-fichier,
valider-conformite-ascii, valider-liens, activer-agent-principal.
## [LECON] 2026-08-10 -- ALLEGEMENT PARCOURS JANUS (c8/c11/c18, Pattern 16) (Buffy)

**Mission** : etape 2b du Pattern 16 - alleger les 3 cases surchargees du parcours janus avec anti-doublon.

**Livrables** : parcours-janus v0.3.2 -> v0.3.3. c8 : indice regle 201 car. remplace par {ref: protocole-controle-buffy}. c11/c18 : 4 indices -> 3 indices (ref pattern-3 + outil combos-moteur avec --var fichier_controle differencie + fichier definition-combo). valider-case CONFORME, navigations reelles OK (c8 ref resolue, c11/c18 combo affiche), JSON valide, ASCII 0, LF pur.

**Lecons** :
1. ANTI-DOUBLON : avant de deplacer un contenu vers une source, verifier qu'il y existe DEJA (rechercher-texte / grep). Pour c8 : le contenu E1-E10 vit deja dans protocole-controle-buffy (10 etapes verifiees) -> rien a copier, juste une ref. Pour c11/c18 : le combo encapsule deja pattern-2 + pattern-12 + protocole + creer-fichier -> les 2 cases POINTENT vers le MEME combo, seule la variable fichier_controle differe.
2. c11 et c18 ne sont PAS identiques (controle-statut vs controle-modification) : il faut garder la distinction par la variable --var fichier_controle dans la commande de l'indice outil, pas par un contenu duplique.
3. Modele d'une case combo (vu dans les parcours existants) : indice ref pattern-3 + indice outil combos-moteur (commande complete avec --var) + indice fichier definition-combo.json (raison). PAS de type d'indice "combo" : c'est l'outil combos-moteur qui lance le combo.
4. guider-parcours resout {ref: protocole-<x>} automatiquement (affiche [REFERENCE] + chemin) : une ref est plus leger et TOUJOURS a jour que le texte inline.
5. La navigation de controle : trouver le chemin via BFS sur les branches (reponses reelles 'statut'/'modification'/'sante' pas OUI). c8 = OUI|sante, c11 = OUI|statut, c18 = OUI|modification.
## [LECON] 2026-08-10 -- CORRECTION FICHE JANUS (Pattern 14 + E5b) APRES AUDIT THEMIS (Buffy)

**Mission** : corriger les 2 points de l'audit Themis sur la fiche janus apres l'allegement (carte v0.3.3).

**Corrections** :
1. Pattern 14 : ligne 76 `PARCOURS (v0.3.2)` -> `PARCOURS (v0.3.3)`.
2. E5b : ajout d'un bloc "FINS REELLES DE MA CARTE v0.3.3" citant les 5 fins avec leurs identifiants cX (c10 Reactiver Cerberus, c29 Signaler le besoin, c29d Outil temporaire, c30 Delegation, c32 Retour de Themis).
3. Bonus (recommandation Themis) : alignement de la numerotation "Pattern 8" -> "Pattern 13" dans la regle fin-suit-SA-carte.

**Verifications** : v0.3.2 residuel absent, 5 fins cX citees, Pattern 13 present / Pattern 8 absent, ASCII 0, LF pur.

**Lecons** :
1. Apres TOUTE mise a jour de version de parcours, la fiche agent doit etre synchronisee (Pattern 14) - le protocole sante E5 detecte la divergence automatiquement.
2. E5b exige les identifiants cX REELS des fins : il faut lire le parcours JSON (fins de type 'fin') et les citer, pas seulement formuler le sens.
3. L'audit Themis a aussi revele un Pattern 8 stale dans la fiche (numerotation ancienne de la spec) : quand on touche la regle fin-suit-SA-carte, en profiter pour aligner la numerotation sur la spec actuelle (Pattern 13).
## [LECON] 2026-08-10 -- MIGRATION TERMINEE : ATLAS/CLIO/MORPHEUS v0.3.0 (Buffy)

**Mission** : finir la migration des cartes de decision (demande utilisateur).

**Resultat** : les 11 parcours sont maintenant migres au format v0.3.x. Les 3 derniers (atlas, clio, morpheus) passes de v0.2.0 a v0.3.0.

**Lecons** :
1. ETAT REEL : les 3 parcours etaient DEJA au format migre (0 case type=indice, 0 regle >160, refs pattern/protocole presentes, CONFORME). La migration restante etait surtout : bump version + synchronisation des fiches (Pattern 14 + E5b).
2. Le trio (athena, minerve, promethee) reste en v0.2.0 VOLONTAIREMENT : reserve aux futurs projets (regle groupes-agents) - ne PAS migrer.
3. Les refs avec chemin brut (ex : clio c11 regles-perimetre-workspace.md) sont un format VALIDE : vulcain c15 fait pareil, guider-parcours les resout ([REFERENCE] + chemin). Pas besoin de les convertir en protocole-<x>.
4. Fin de migration = 3 actions : bump version parcours, Pattern 14 dans la fiche (PARCOURS (vX)), E5b (citer les fins reelles cX dans la fiche - modele janus).
5. Navigation de controle : toujours lire les branches RELLES de c1 (clio : corriger/verifier/autre, PAS mettre-a-jour) avant de naviguer - une mauvaise reponse donne un code 1 trompeur.
6. valider-cartes-decision --tous : 11/11 CONFORMES apres migration complete.

## [LECON] 2026-08-10 -- CORRECTION 5 POINTS DOCUMENTAIRES POST-MIGRATION (Buffy)

**Mission** : corriger les 5 points documentaires de l'audit Themis post-migration.
**Resultat** : 9/9 VALIDE.

**Corrections appliquees** :
1. vulcain.md ligne 60 : PARCOURS (v0.5.0) -> PARCOURS (v0.3.0) (Pattern 14 : le v0.5.0 etait une version de fiche confondue avec la version de parcours)
2. buffy.md : bloc FINS REELLES DE MA CARTE v0.3.3 (9 fins citees : c8, c13d, c22, c27, c35, c35d, c36, c39, c41)
3. cerberus.md : bloc FINS REELLES DE MA CARTE v0.3.1 (2 fins : c20, c23) insere dans la section Le cycle fondamental apres le bloc Chaine complete
4. themis.md : bloc FINS REELLES DE MA CARTE v0.3.0 (5 fins : c13, c23, c23d, c24, c25b)
5. vulcain.md : bloc FINS REELLES DE MA CARTE v0.3.0 (7 fins : c9, c15, c16d, c18, c18d, c19, c21)

**Lecons** :
1. Le bloc FINS REELLES se place dans la section fin de mission (apres le bloc Pattern 13 / la ligne "Ne JAMAIS utiliser str_replace") ; pour cerberus (pas de section fin), se placer apres le bloc Chaine complete du cycle fondamental
2. Chaque cX cite doit correspondre a une case de type fin reelle de la carte (croisement fiche/parcours E5b) - verifier titres ET exhaustivite (aucune fin oubliee)
3. Piege regex : pour extraire un bloc de lignes blockquote, utiliser (?:> [^\n]*\n)+ et non un lookahead (?=\n\n|\n>) qui s'arrete au premier \n> 
4. Toujours verifier les normes (ASCII strict + LF pur) apres insertion dans les fiches
5. Outils utilises : lire-fichier, activer-agent-principal, valider-conformite-ascii ; insertion via script Python (jamais str_replace sur AGENTS.md)

## [LECON] 2026-08-10 -- CORRECTION NUMEROTATION PATTERN 8 -> 13 DANS 8 FICHES (Buffy)

**Mission** : corriger le decalage de numerotation dans le bloc fin de mission des fiches agents.
**Resultat** : 17/17 VALIDE (9 remplacements sur 8 fiches).

**Corrections appliquees** :
1. 7 fiches : 'La fin de mission suit SA carte (Pattern 8)' -> '(Pattern 13)' : athena, atlas, buffy, clio, morpheus, themis, vulcain
2. minerve : 2 occurrences 'Pattern 8/13' -> 'Pattern 13' (lignes 95 et 156)

**Lecons** :
1. Le pattern LA FIN SUIT SA CARTE est le Pattern 13 (v0.2.23) ; le Pattern 8 existe TOUJOURS dans la spec (Chaine de delegation BOUT-EN-BOUT) - la correction doit etre chirurgicale sur la phrase exacte, pas un remplacement global de 'Pattern 8'
2. Preserver les references legitimes au Pattern 8 : vulcain ligne 190 'bilan consolide de la chaine (Pattern 8)' est une reference au Pattern 8 (bout-en-bout), NE PAS la toucher
3. minerve utilisait le format composite 'Pattern 8/13' - simplifier en 'Pattern 13'
4. Toujours verifier les normes (ASCII strict + LF pur) et l'absence de regressions apres modification des fiches
5. Outils utilises : lire-fichier, activer-agent-principal ; insertion via script Python (jamais str_replace sur AGENTS.md)

## [LECON] 2026-08-10 -- CARTE CLIO v0.4.0 ENRICHIE (branche ampleur + combos) (Buffy)

**Mission** : donner plusieurs possibilites a Clio selon l'AMPLEUR de la mise a jour du README.
**Resultat** : 21/21 + preuve navigation (cases c6b/c6c atteintes), valider-cartes-decision CONFORME.

**Modifications** (parcours-clio.json v0.3.0 -> v0.4.0, 24 -> 27 cases) :
1. c5 recablee : OUI -> c5a (au lieu de c6)
2. Nouvelle c5a (question) : Ampleur de la correction ? PETITE -> c6b, GROSSE -> c6c
3. Nouvelle c6b (action) : Executer combo-maj-readme (PETITE MAJ) - ref pattern-3 + outil combos-moteur + fichier definition-combo.json -> suivant c9
4. Nouvelle c6c (action) : Executer combos-maj-readme-massive (GROSSE MAJ) - ref pattern-3 + outil combos-maj-readme-massive.py + fichier .md (LIRE AVANT USAGE) -> suivant c9

**Lecons** :
1. La navigation guider-parcours affiche les TITRES de cases, pas les identifiants cX - pour verifier qu'une case est atteinte, chercher le TITRE dans la sortie, pas l'id
2. Le nombre de reponses de guider-parcours doit couvrir TOUTES les questions du chemin : 'OUI|corriger|OUI|PETITE' (4 reponses : c0, c1, c5, c5a) - un nombre insuffisant donne rc=1
3. Les refs de type chemin de fichier (qui commencent par c comme 'cerveau-projet/...') ne doivent pas etre comptees comme references de cases dans la verification de refs mortes - exclure celles qui contiennent / ou backslash
4. Anti-doublon : verifier qu'aucune case ne reference deja le combo avant d'ajouter (json.dumps + recherche du nom)
5. generateurs-case v0.4.0 a les commandes ajouter/editer/supprimer/convertir/ajouter-bloc - l'ajout via script JSON direct est acceptable pour les parcours (pas AGENTS.md)
6. Outils utilises : lire-fichier, guider-parcours, valider-cartes-decision, activer-agent-principal

## [LECON] 2026-08-10 -- PATTERN 17 RAPPORT DE FIN AVEC AMELIORATIONS (Buffy, spec v0.6.1 + pilote themis v0.3.2)
1. Pattern 17 ecrit dans spec-guider-parcours (v0.6.0 -> v0.6.1, 17 patterns) : la case apres 'Lecons et retour' est ALTERNATIVE - si le rapport contient des ameliorations possibles de l'agent, direction SA ligne d'auto-amelioration, sinon fin normale.
2. La ligne d'auto-amelioration = GENERATEUR D'ABORD (generateurs-amelioration --theme) -> ACTIVATION de l'agent habilite (Vulcain/Buffy/Themis selon nature) -> REPRISE par l'agent precedent (Pattern 13).
3. Pilote themis : c12b (question alternative, OUI->c12c NON->c13), c12c (generateur), c12d (activation agent habilite), c12e (FIN - Reprise du parcours). 32 cases, v0.3.2.
4. Navigation verifiee : branche OUI affiche generateur + activation + c12e, branche NON -> c13 direct. valider-cartes-decision CONFORME.
5. Le generateur d'amelioration n'avait qu'UN theme (ameliorer-outil) - le theme ameliorer-agent est reference par l'indice outil mais doit exister dans themes-amelioration.json (a verifier lors de la generalisation).
6. Constat catalogue : seuls 5/11 parcours referencent generateurs-commande (atlas, buffy, clio, janus, themis) - la generalisation du catalogue et du Pattern 17 reste a faire.

## [LECON] 2026-08-10 -- CARTE THEMIS c12d: REPERTOIRE 11 THEMES (Buffy, parcours v0.3.3)

**Contexte** : themes-amelioration.json passe a v2.2.0 (11 themes, 64 questions, couverture 6/6 des protocoles-autoameliorer + spec trio). La regle de c12d (Activer l agent habilite) listait seulement 3 natures - mise a jour avec le repertoire complet et le mapping des agents habiles.
**Verdict** : CONFORME (valider-cartes-decision) + navigation reelle OK + fiche synchronisee.
**Lecons** :
1. La regle de delegation c12d doit refleter le repertoire REEL du generateur (11 themes) sinon l agent ignore les natures disponibles
2. Mapping des agents habiles par nature : Vulcain (outil/combo/protocole), Buffy (carte/case/parcours/cerveau/conventions), Janus (regles), trio athena/promethee/minerve (spec/pense-bete/todo)
3. Toujours verifier la navigation reelle de la case modifiee + valider-cartes-decision + synchroniser la fiche (Pattern 14)

## [LECON] 2026-08-10 -- PATTERN 17 GENERALISE AUX 10 PARCOURS (Buffy)

**Contexte** : generalisation du Pattern 17 (rapport de fin -> ameliorations possibles -> ligne d auto-amelioration) sur les 10 parcours restants (themis etait le pilote v0.3.3). Modele themis : case lecons -> Xb (question alternative) -> OUI: Xc (generateur) -> Xd (activation agent habilite) -> Xe (FIN Reprise) ; NON -> la fin reelle de SA carte.
**Verdict** : valider-cartes-decision 11/11 CONFORME + navigation reelle OUI/NON OK sur les 11 flux.
**Lecons** :
1. La mecanique des cases action : champ "suivant" explicite (pas de branches) - la case lecons pointe vers Xb, Xc -> Xd -> Xe, et Xb.suivant = la fin normale (branche NON)
2. Chaque agent garde SA fin reelle (Pattern 13 : la fin suit SA carte) - jamais reactiver Cerberus par defaut : athena->Promethee, atlas->Cerberus, buffy->c16->Janus, cerberus->c20, clio->Cerberus, janus->Cerberus, minerve->Cerberus, morpheus->c9(Retour)->Janus/Cerberus, promethee->Minerve, vulcain c8->c9 et c14->c15
3. Cas particulier morpheus : la case lecons c8 mene a c9 (question Retour qui m a delegue) qui est PRESERVEE - le Pattern 17 s insere avant elle (c8 -> c8b -> NON -> c9)
4. Cas particulier vulcain : 2 flux (construire c8->c9 et modifier c14->c15) - 2 insertions P17 (c9b-e et c15b-e)
5. Cas particulier cerberus : point d insertion c19 (Reprendre la coordination) -> c19b (il n a pas de case lecons classique mais termine sa coordination)
6. Collision d identifiants verifiee sur les 10 parcours avant insertion (0 collision)
7. Apres refonte de parcours : RE-SCAN des tests formels (protocole-tests) - test-013 cerberus 0.3.1->0.3.2, test-016 buffy 0.3.3->0.3.4, test-005 atlas 0.2.0->0.3.1 - delegation a Morpheus
8. Pattern 14 : fiche agent synchronisee pour les 10 parcours (dont clio 0.3.0->0.4.1, rattrapage d un retard preexistant)

## [LECON] 2026-08-10 -- CORRECTIONS P17 (regles longues + commandes + suivant) (Buffy)

**Contexte** : la non-regression apres generalisation P17 (Morpheus) a revele 3 defauts introduits par la copie du pilote themis : 1) regles P17 de 172/492 caracteres > garde-fou valider-case (<= 160), 2) commandes en dur dans les indices outil (conflit avec le standard PASSE PAR LE GENERATEUR teste par test-005), 3) champ suivant sur les questions alternatives Xb (doublon c11 x2 dans le cartographe, car les questions standard n ont PAS de suivant).
**Verdict** : corrige - valider-case CONFORME 11/11, valider-cartes-decision 11/11, non-regression 18/20 (2 KO preexistants).
**Lecons** :
1. REGLE <= 160 CARACTERES : toute regle inseree doit respecter le garde-fou valider-case - verifier avec valider-case --dry-run apres insertion
2. FORMAT PASSE PAR LE GENERATEUR : les indices outil ne portent PAS de commande en dur (le guider la genere depuis le catalogue) - le pilote themis avait ce defaut latent, la generalisation l a propage
3. QUESTIONS SANS SUIVANT : une case question a des branches mais PAS de champ suivant (c0/c1 n en ont pas) - le champ suivant sur Xb creait un doublon dans le cartographe (c11 x2)
4. La copie d un pilote propage ses defauts - toujours valider le MODELE avant de le generaliser
5. Tests adaptes en consequence : test-005 (catalogue 0.2.5 + chemins OUI|explorer|NON), test-006 (44 cases/45 chemins), test-013/016 (comptages), test-014 (spec v0.6.1 + 17 patterns)
## [LECON] 2026-08-10 -- SUIVANTS MORTS RETIRES DES CARTES (Buffy, 10 parcours)

**Mission** : retirer les champs suivant MORTS des cartes (questions avec suivant redondant deja dans leurs branches + fins avec suivant). Constat Themis : themis faisait 210 chemins pour 32 cases (ratio anormal).
**Resultat** : 25/25 suivant retires sur 10 parcours (athena 2, atlas 2, buffy 4, clio 2, janus 2, minerve 2, morpheus 2, promethee 2, themis 5, vulcain 2). 0 anomalie residuelle.
**Lecons** :
1. Le champ suivant sur une question qui A des branches est un DEFECT (suivant mort : jamais lu, les branches priment) - il doit etre retire
2. Une fin ne doit JAMAIS avoir de suivant
3. Le cartographe (nb chemins) est le detecteur ideal : ratio chemins/cases ~1:1 attendu (atlas 44/45 avant -> 44/39 apres retrait des fantomes ; themis 210 -> 48)
4. valider-cartes-decision ne detecte pas ce defaut (references valides mais logique morte) - renforcer le validateur : detecter suivant redondant avec branches + fin avec suivant
5. Les cartographies generees par cartographier-parcours pendant un audit sont des RESIDUS a nettoyer (test-017 KO)
6. La navigation reelle est INTACTE apres correction (les branches gerent deja tout) : PARCOURS TERMINE atteint, valider-cartes 11/11 CONFORME
7. test-006 attendait 45 chemins atlas -> 39 apres correction (mise a jour Morpheus necessaire)

## [LECON] 2026-08-11 -- Scan COMBOS branche dans parcours vulcain v0.3.3

**Contexte** : brancher le scan detecter-decalages-catalogue (section COMBOS) dans le parcours de Vulcain pour un lancement regulier quand il cree/modifie un combo ou le catalogue.

**Lecons** :
1. Le scan COMBOS est un outil de CONTROLE pour Vulcain (proprietaire des combos et du catalogue) : il doit etre lance dans les 2 flux de construction ET de modification, PAS dans un combo de controle externe.
2. Les branches des questions du parcours utilisent la cle `reponse` (pas `si`) : pour tester la navigation avec guider-parcours --reponses, il faut construire la sequence des reponses exactes case par case (ex: 'OUI|construire|OUI|OUI|OUI' pour atteindre c6b en construction).
3. Les branches d'une question qui mene au meme endroit (OUI/NON -> meme case) sont legales mais il faut verifier que le flux NON saute bien la case d'action (test des 2 branches).
4. Apres toute modification de parcours : valider-cartes-decision --agent <agent> (CONFORME) + navigation reelle des 3 branches (OUI/NON) + synchronisation de la fiche (Pattern 14 : PARCOURS vX) + verifier qu'aucun test formel ne reference l'ancienne version.
5. Les regles des nouvelles cases ne doivent pas depasser 160 caracteres (garde-fou valider-case) : formuler les regles courtes et actionnables.
6. normes : ASCII 0 + LF pur partout, pas de residu .tmp/.zz.

## [LECON] 2026-08-11 -- CORRECTION ECART JANUS P12 (Buffy, parcours vulcain v0.3.4)

**Contexte** : le second controle Janus a revele que les cases action c6c/c12c (Lancer le scan detecter-decalages-catalogue section COMBOS) ECRIVENT un rapport par defaut (rapport-detecter-decalages-catalogue-<date>.md sans --sortie) mais ne portaient pas d'indice regle CREATION LIMITEE (Pattern 12).

**Lecons** :
1. Toute case action qui lance un outil ecrivant un fichier PAR DEFAUT (rapport, sortie sans --sortie) DOIT porter un indice regle CREATION LIMITEE (Pattern 12) qui precise le perimetre de creation et le role exclu.
2. Le modele est c20 : 'CREATION LIMITEE : ... je ne cree AUCUN autre fichier dans le cerveau' -- adapte au contexte de la case.
3. L'indice CREATION LIMITEE se place EN TETE de la liste des indices de la case (comme le rappel ASCII du Pattern 2).
4. La conformite de structure (valider-cartes CONFORME) ne suffit pas : croiser avec ce que fait RELLEMENT l'outil appele (ecrit-il un fichier par defaut ?) avant de valider une case.
5. Toute modification de carte implique : bump de version (v0.3.3 -> v0.3.4) + synchronisation fiche (Pattern 14 PARCOURS) + re-audit (valider-cartes CONFORME + navigation 2 flux + normes ASCII/LF).

## [LECON] 2026-08-11 -- CORRECTION MASSIVE P12 (Buffy, 16 ecarts / 7 parcours)

**Contexte** : le scan des 11 parcours a revele 16 cases d'ecriture (outil qui ecrit un fichier par defaut) sans indice CREATION LIMITEE (Pattern 12) ni regle EXCEPTION OUTIL TEMPORAIRE. Meme classe que l'ecart c6c/c12c vulcain.

**Lecons** :
1. Les 16 ecarts se repartissent en 3 groupes : A) outil ecrit par defaut -> indice regle CREATION LIMITEE adapte (9 cases), B) outil temporaire sans regle -> EXCEPTION OUTIL TEMPORAIRE modele buffy c35c (4 cases), C) role dedie README -> CREATION LIMITEE AU README (3 cases clio).
2. PIEGE SCRIPT : modifier les indices EN MEMOIRE puis reecrire dans une boucle SEPAREE qui recharge le fichier depuis le disque = les modifications en memoire sont PERDUES. Toujours charger une fois, modifier, et ecrire dans la MEME logique (parcours_data en memoire puis une seule passe d'ecriture).
3. Tout bump de version de parcours (6 parcours : atlas 0.3.2, buffy 0.3.5, clio v0.4.2, janus 0.3.5, themis 0.3.4, vulcain 0.3.5) exige la synchronisation de la fiche (Pattern 14 PARCOURS) dans les 6 .md.
4. Impact tests : test-005 verifie atlas v0.3.1 et test-016 verifie buffy 0.3.4 - les versions ayant change, ces tests cassent. DELEGATION DES TESTS : SEUL Morpheus adapte les tests (protocole-tests v0.2.2).
5. Apres correction massive : re-scan 16/16 + valider-cartes 6/6 CONFORME + normes ASCII 0 + LF pur sur les 6 parcours et les 6 fiches.
6. Le format de version de clio est 'v0.4.x' (prefixe v) : le bump doit conserver le prefixe.

## [LECON] 2026-08-11 -- EDITER-FICHIER-AGENTS BRANCHE DANS PARCOURS BUFFY v0.3.6

**Contexte** : brancher le nouvel outil editer-fichier-agents dans le parcours de Buffy pour editer les fiches agents (.md) par bloc/ligne avec correcteur ASCII.

**Lecons** :
1. Le flux d'edition de Buffy : c10b (Question : parcours a modifier ?) avec branches OUI->c10c (generateurs-case), non->c11 (editer-fichier), ligne->c10d (generateurs-ligne). J'ai ajoute la branche 'fiche'->c11b (Modifier une fiche agent .md) avec l'outil editer-fichier-agents.
2. SEUIL_INDICES=3 : la nouvelle case c11b doit rester a 3 indices max (pattern-2 + pattern-12 + outil) - PAS de regle PASSE PAR LE GENERATEUR separee, elle est materialisee DANS la commande de l'indice outil (--commande editer-fichier-agents --reponses ...).
3. Le branchement est coherent : c11b.suivant = c37 (comme c11) - le flux rejoint le combo corriger-fichier pour la suite.
4. Navigation reelle : la sequence de reponses est 'OUI|modifier|fiche' (3 questions : c0, c1, c10b) - compter les QUESTIONS, pas les cases, pour construire --reponses.
5. IMPACT TESTS : test-016 verifie la version buffy (0.3.5), le nombre de cases action (34) et le nombre de questions/fins - l'ajout d'une case fait passer 34->35 action et 54->55 total. DELEGATION DES TESTS : Morpheus adapte.
6. Apres modif de carte : valider-cartes CONFORME + valider-case CONFORME + navigation des 4 branches (fiche/OUI/non/ligne) + fiche synchronisee (Pattern 14 PARCOURS v0.3.6).

## [LECON] 2026-08-11 -- SUPPRESSION REELLE DES 11 BLOCS HISTORIQUE (Buffy, editer-fichier-agents)

**Mission** : supprimer en reel les blocs '## Historique' obsoletes des 11 fiches agents (l'information vit dans AGENTS-historique.md + corrections.md).

**Deroulement** (sequence de securite Cerberus puis Buffy) :
1. CERBERUS : dry-run global 11/11 detectes (0 modification) + rapport (vulcain 222-236 le plus gros, 15 lignes)
2. CERBERUS : validation de contenu sur 3 echantillons -- blocs uniquement redondants (creation, versions passees)
3. BUFFY : WET avec --backup sur les 11 fiches -- 11/11 [OK] Supprime
4. BUFFY : verification 0 occurrence restante, blocs PARCOURS/REGLES ABSOLUES/Connexions intacts, ASCII 0 + LF pur
5. Nettoyage : suppression des 11 .bak non suivis (les 6 .bak preexistants suivis par git sont conserves)

**Lecons** :
1. La sequence de securite dry-run -> rapport -> validation contenu -> wet est indispensable pour une operation massive : elle a confirme avant le wet que les blocs etaient 100% redondants
2. editer-fichier-agents --bloc X --supprimer --backup fonctionne parfaitement en reel : le bloc est remplace par la ligne suivante du fichier (separateur '---' conserve), 0 ligne vide parasite
3. Les 11 fiches n'ont PAS de bloc '## Identite' -- l'identite vit dans l'en-tete YAML/tableau du haut (ne pas s'alarmer si IDENTITE=0 a la verification)
4. Les .bak generes par --backup ne sont PAS suivis par git (untracked) : les supprimer apres verification pour ne pas polluer le depot -- verifier aussi qu'ils ne sont pas deja suivis (git ls-files) avant suppression
5. Les blocs Historique des fiches sont maintenant tous supprimes : 11/11 fiches allegees, structure PARCOURS intacte

**Outils utilises** : editer-fichier-agents (--bloc/--supprimer/--backup/--dry-run), valider-conformite-ascii, git status, scripts .zz- temporaires

## [LECON] 2026-08-11 -- REFONTE TEMPLATE PAR ROLE ETAPES 1-2 (Buffy, v0.3.0)

**Mission** : refondre fiche-agent-template.md selon le modele noyau + variantes (decision utilisateur TEMPLATE PAR ROLE), puis creer les 2 variantes de famille.

**Produits** :
1. fiche-agent-template.md v0.3.0 : NOYAU OBLIGATOIRE dans l'ordre (Vue d'ensemble, PARCOURS, REGLES ABSOLUES, Outils de base P0, WORKFLOW RVAV, UTILISATION de activer-agent-principal, Limites, Connexions). Section Historique AGENT retiree. Forces/Faiblesses + Style de travail retirees du noyau (-> variantes). Documentation du modele par role dans le frontmatter (commentaires #). Cle 'famille: [cerveau-projet | trio]' ajoutee.
2. fiche-template-variante-cerveau.md : Forces et Faiblesses + Style de travail (8 agents cerveau-projet).
3. fiche-template-variante-trio.md : Vue d'ensemble complement + Forces + Style + Limites (trio athena/promethee/minerve).

**Preuves du succes** :
- L'outil verifier-conformite-fiche avec le NOUVEAU noyau : buffy n'a plus '## Historique manquant' (retire du template) -- il ne reste que ses sections specifiques (Forces/Style) tolerees = exactement le comportement par role attendu
- Normes : ASCII 0 + LF pur sur les 3 fichiers

**Lecons** :
1. PIEGE : toute section '## X' du template est exigee des fiches par l'outil. L'historique DU TEMPLATE doit vivre dans le frontmatter (commentaires #), PAS en section '## ' -- sinon toutes les fiches devraient l'avoir
2. Les fichiers templates (racine agents/) ne sont PAS soumis a la regle de prefixe de valider-nommage (regle des outils dans tools/) -- un NOK la-dessus est attendu et non bloquant
3. Le modele par role se materialise par la cle 'famille' dans le frontmatter des fiches : l'outil (etape 3) verifiera noyau + variante selon cette cle
4. Les sections specifiques par agent (cerberus cycle, janus Verdicts, themis rapport...) restent tolerees et signalees -- elles seront documentees dans les variantes

**Outils utilises** : lire-fichier, ecrire-fichier, valider-conformite-ascii, verifier-conformite-fiche (validation du nouveau noyau), .zz- scripts temporaires

## [LECON] 2026-08-11 -- ETAPE 4 : 11/11 FICHES CONFORMES AU MODELE PAR ROLE (Buffy)

**Mission** : corriger les 9 fiches agents en ecart (rapport v020 : 2 CONFORME / 9 ECARTS) pour atteindre 11/11 CONFORME selon le modele noyau + variante.

**Corrections appliquees** (via editer-fichier-agents --ajouter multi-lignes, case c11b) :
1. cerberus : + WORKFLOW RVAV + UTILISATION + Forces et Faiblesses (gardee Le cycle fondamental + Agents disponibles)
2. atlas : + Forces et Faiblesses
3. janus : + Forces et Faiblesses + Style de travail (garde Verdicts)
4. morpheus : + Style de travail (garde Structure des tests + Checklist)
5. themis : + Forces et Faiblesses + Style de travail (garde PROTOCOLE DE RAPPORT + 5 sous-sections)
6. vulcain : + Vue d'ensemble + Limites + Forces et Faiblesses + Style de travail (garde Technologies + Processus + BOUCLES)
7. athena (trio) : + Vue d'ensemble complement + Forces + Limites complement
8. minerve (trio) : + Vue d'ensemble + Limites + complements trio + Forces + Style
9. promethee (trio) : idem minerve
+ cle 'famille: cerveau-projet|trio' ajoutee dans le frontmatter des 9 fiches.

**Lecons** :
1. PIEGE : appliquer un script de correction sur TOUTES les fiches apres avoir teste sur UNE deja corrigee cree des DOUBLONS -- isoler les fiches deja traitees ou re-executer proprement
2. editer-fichier-agents --ajouter accepte le multi-lignes (split sur \n) : on peut inserer des blocs complets, mais il faut RECALCULER le numero de ligne apres chaque insertion (les ancres bougent)
3. La correction de l outil verifier-conformite-fiche v0.2.0 -> v0.2.1 etait necessaire : les sections SPECIFIQUES etaient TOLE REES mais BLOQUANTES (KO) -- le verdict CONFORME doit ignorer les specifiques (avertissement ~ non bloquant)
4. Le modele par role fonctionne : 11/11 CONFORME avec les sections specifiques legitimes signalees en avertissement (cerberus cycle, janus Verdicts, morpheus tests, themis rapport, vulcain techno)
5. normes : 0 ecart ASCII/LF sur les 11 fiches + l outil

**Outils utilises** : editer-fichier-agents (--ajouter multi-lignes), verifier-conformite-fiche (v0.2.1), valider-conformite-ascii, .zz- scripts temporaires
## [LECON] 2026-08-11 -- FIN ACTIVER JANUS AJOUTEE DANS LA CARTE DE CLIO (Buffy, v0.4.3)

**Mission** : ajouter la fin 'Activer Janus' (second controle) dans la carte de clio, sur le modele buffy/morpheus.

**Actions** :
1. Diagnostique : parcours-clio v0.4.2 - fin principale c12 = 'FIN - Reactiver Cerberus', aucune mention Janus (themis seule branchee via c17/c18)
2. Transforme la case c12 en 'FIN - Activer Janus' (type fin conserve) avec :
   - message adapte au role de Clio (mise a jour du README : actif JANUS pour le second controle, Janus reactive Cerberus avec le verdict consolide)
   - indice regle REGLE IMMUABLE JANUS (meme texte que buffy/morpheus)
3. Bump version : v0.4.2 -> v0.4.3
4. Fiche clio.md : Pattern 14 (v0.4.3) + bloc FINS REELLES mis a jour (etait stale v0.3.0, c12 redecrite + c10e ajoutee)

**Verifications** :
- valider-cartes-decision --agent clio : CONFORME (0 suivant mort)
- Navigation flux principal (corriger|OUI|PETITE|NON) : fin de parcours c12 'FIN - Activer Janus'
- Navigation flux audit (autre|audit) : c18 'FIN - Retour de Themis avec son rapport'
- Normes : 0 non-ASCII, 0 CRLF (carte + fiche)

**Lecons** :
1. Le test-018 verifie encore clio c12 comme fin REACTIVER-CERBERUS : il DOIT etre adapte par Morpheus (clio n'a plus de fin Reactiver - c12 est devenue Activer Janus)
2. Le bloc FINS REELLES de la fiche clio etait stale (v0.3.0 alors que le parcours etait v0.4.2) - verifier ce bloc a chaque modification de carte (lecon deja connue mais recurrence)
3. Les reponses de navigation se lisent dans les branches (champ 'reponse') - pour c1: corriger/verifier/autre, c13: OUI/NON/audit
## [LECON] 2026-08-11 -- FINS REACTIVER -> ACTIVER JANUS POUR ATLAS/THEMIS/MORPHEUS (Buffy)

**Mission** : transformer les fins 'FIN - Reactiver Cerberus' restantes en 'FIN - Activer Janus' (second controle) pour atlas c11, themis c13, morpheus c14 (perimetre valide par Cerberus/utilisateur : Minerve/trio hors perimetre).

**Actions** :
1. Atlas : c11 'FIN - Reactiver Cerberus' -> 'FIN - Activer Janus' (message cartographie + indice REGLE IMMUABLE JANUS), v0.3.2 -> v0.3.3
2. Themis : c13 -> 'FIN - Activer Janus' (message evaluation + REGLE IMMUABLE JANUS), v0.3.4 -> v0.3.5
3. Morpheus : c14 (cas CERBERUS direct) -> 'FIN - Activer Janus' (message tests + REGLE IMMUABLE JANUS), v0.3.1 -> v0.3.2. Morpheus n'a plus AUCUNE fin Reactiver (c10 et c14 sont tous deux Activer Janus)
4. Fiches : Pattern 14 (nouvelles versions) + blocs FINS REELLES reecrits + bloc FLUX de morpheus.md corrige (mention obsolete 'reactivation de Cerberus' retiree)

**Verifications** :
- valider-cartes-decision : atlas CONFORME, themis CONFORME, morpheus CONFORME
- Navigations reelles : --case c11/c13/c14 -> PARCOURS TERMINE 'FIN - Activer Janus' (3/3)
- Normes : 0 non-ASCII, 0 CRLF (6 fichiers)

**Lecons** :
1. Apres transformation, il ne reste que 2 fins REACTIVER dans tout le cerveau : janus c10 (dernier maillon, legitime) et minerve c10 (trio, hors perimetre) - le test-018 doit etre adapte par Morpheus (5 -> 2 fins REACTIVER)
2. Le bloc FLUX des fiches peut contenir des mentions obsoletes meme quand le bloc FINS REELLES est mis a jour - verifier les 2
3. La REGLE IMMUABLE JANUS s'applique 'apres TOUTE mission (meme sans modifier du code)' - y compris quand l'agent est active directement par Cerberus (cas morpheus c14)
## [LECON] 2026-08-11 -- COMMANDE EXACTE AJOUTEE AUX 8 FINS ACTIVER JANUS (Buffy)

**Mission** : corriger le probleme ou l'execution reelle ne suit pas la carte (cloture Morpheus ecrite 'je reactive Cerberus' alors que sa carte dit 'FIN - Activer Janus').

**Cause racine** : aucune des 8 fins 'FIN - Activer Janus' ne contenait la commande exacte d'activation (activer-agent-principal.py activer session-llm-1 janus '<raison>') - elles disaient 'J ACTIVE JANUS' sans la commande precise, donc l'executant retombait sur le reflexe reactiver (qui ramene toujours a Cerberus). Recurrence de la lecon Themis.

**Actions** : enrichi les messages des 8 fins avec la COMMANDE EXACTE + mention 'PAS reactiver (reactiver ramene toujours a Cerberus)' :
- atlas c11, clio c12, themis c13, morpheus c10/c14, buffy c8/c22/c27
- Message adapte au role de chaque agent (cartographie, readme, evaluation, tests, chaines de creation)
- Pas de bump de version (correction de contenu de message uniquement)

**Verifications** : valider-cartes 5/5 CONFORME, 8/8 commandes exactes presentes, navigations reelles OK (4/4), normes 0 non-ASCII / 0 CRLF.

**Lecons** :
1. Toute fin qui ACTIVE un autre agent doit contenir la COMMANDE EXACTE (pas seulement l'intention 'J active X') - c'est le seul moyen de garantir que l'execution suit la carte
2. La mention 'PAS reactiver' est cruciale : la commande reactiver ramene TOUJOURS a Cerberus, ce qui casse les chaines Agent -> Janus -> Cerberus
3. Une lecon Themis avait deja etabli ce principe (la reactivation directe a Cerberus) - l'audit des fins Activer X doit verifier la presence de la commande, pas seulement le titre
4. Le test-018 verifie les fins mais pas le contenu des messages : un garde-fou futur pourrait verifier que toute fin 'FIN - Activer X' contient 'activer-agent-principal.py activer' et pas 'reactiver' (a proposer a Vulcain/Janus)
## [LECON] 2026-08-11 -- PROTOCOLE-CONTROLE-TRIO CREE (Buffy, v0.1.0)

**Mission** : creer le protocole-controle-trio (protocole dedie de Janus pour controler le travail du trio athena/promethee/minerve) - avant la correction du trio.

**Actions** :
1. Modele : protocole-controle-buffy (en-tete + 7 sections + frontmatter identite)
2. Cree cerveau-projet/agents/regles-immuables/general/protocole-controle-trio/protocole-controle-trio.001.01.ebauche.md
3. Sections : Objectif (trio = chaine de production pense-bete -> spec -> todo, travail DETERMINANT), Prerequis, Etapes E1-E10 (E4 = coherence de la CHAINE, E5 = format/templates, E6 = index, E9 = cartes + fin c10 Activer Janus commande exacte), RVAV, Exemples, Pieges, Liens

**Verifications** : 0 non-ASCII, 0 CRLF, 7 sections exactement (convention-protocoles).

**Lecons** :
1. Le trio est une CHAINE DE PRODUCTION : la coherence du maillon amont (pense-bete -> spec -> todo) est LE point de controle central (E4) - c'est ce qui distingue le controle du trio du controle documentaire de Buffy
2. Le protocole doit etre cree AVANT la correction du trio : c'est le standard qui guidera la correction (fin c10 Activer Janus + commande exacte)
3. Le travail du trio est DETERMINANT : en cas de doute, le verdict Janus penche vers A REVOIR plutot que VALIDE (regle absolue du protocole)
4. Pas d'index global des protocoles : les protocoles vivent dans regles-immuables/general/ sans index central (convention existante)
## [LECON] 2026-08-11 -- TRIO CORRIGE : CHAQUE AGENT ACTIVE JANUS (Buffy, v0.2.2)

**Mission** : corriger le trio (athena, promethee, minerve) - chaque agent doit ACTIVER JANUS a sa fin (decision utilisateur), apres la creation du protocole-controle-trio.

**Actions** :
1. athena c10 : 'FIN - Activer Promethee' -> 'FIN - Activer Janus' (message pense-bete + commande exacte activer janus + REGLE IMMUABLE JANUS)
2. promethee c10 : 'FIN - Activer Minerve' -> 'FIN - Activer Janus' (message spec + commande exacte + REGLE IMMUABLE JANUS)
3. minerve c10 : 'FIN - Reactiver Cerberus (PHASE 9)' -> 'FIN - Activer Janus' (message todo + DERNIER MAILLON du trio + commande exacte + REGLE IMMUABLE JANUS)
4. Versions : 0.2.1 -> 0.2.2 (3 agents)
5. Fiches : Pattern 14 (v0.2.2) + blocs FLUX corriges (athena : activer Promethee -> Janus ; promethee : activer Minerve -> Janus + section 'Pour activer Minerve' -> 'Pour activer Janus')

**Verifications** : valider-cartes 3/3 CONFORME, 3/3 commandes exactes, navigations c10 OK, normes 0 non-ASCII / 0 CRLF.

**Lecons** :
1. La chaine du trio est desormais : athena -> Janus -> Cerberus, promethee -> Janus -> Cerberus, minerve -> Janus -> Cerberus (chaque maillon passe par le second controle)
2. minerve etait le seul agent avec 'Reactiver Cerberus (PHASE 9)' - c'etait le DERNIER maillon du trio, sa transformation ferme la generalisation : il ne reste plus QU'UNE fin Reactiver dans tout le cerveau (janus c10)
3. Le test-018 devra etre adapte par Morpheus : 1 fin REACTIVER restante (janus c10) au lieu de 2
4. Les fiches du trio portaient des blocs FLUX avec des commandes d'activation (activer Promethee/Minerve) - verifier ces blocs a chaque changement de chaine
5. Le protocole-controle-trio (etape 1) est le standard qui a guide cette correction : E9 exige la fin c10 Activer Janus avec commande exacte
## [LECON] 2026-08-11 -- MENTIONS SECOND AIRES P14 CORRIGEES (Buffy)

**Mission** : corriger les mentions secondaires de versions de parcours obsoletes dans les fiches agents (le Pattern 14 principal REGLE ABSOLUE PARCOURS vX etait deja a jour partout).

**Constats** :
1. Les blocs FINS REELLES DE MA CARTE vX n avaient pas suivi les ajouts de fins (Pattern 17, ligne trio Janus) ni les bumps c0d : 8 fiches concernees (atlas, buffy, cerberus, clio, janus, morpheus, themis, vulcain).
2. Les liens Parcours (vX) affichaient d anciennes versions : 6 fiches (athena, cerberus, minerve, morpheus, promethee, vulcain - apres correction des 8 premieres, athena/minerve/promethee restaient).

**Actions** :
1. Reconstruit les 8 blocs FINS REELLES : version reelle du parcours + liste complete des fins (type fin) avec les libelles enrichis conserves et les nouvelles fins ajoutees (libelle du parcours).
2. Corrige les 6 liens Parcours (vX) a la version reelle.
3. Verifie : valider-cartes 11/11 CONFORME (P10 fiche/parcours), non-regression 33/33 OK, normes 0/0.

**Lecons** :
1. Le Pattern 14 a DEUX volets : la REGLE ABSOLUE (suivie) ET les mentions secondaires (bloc FINS REELLES + lien Parcours vX) qui se periment silencieusement quand on ajoute des fins (Pattern 17) ou des cases (c0d).
2. Le bloc FINS REELLES doit etre gere comme un artefact derive du parcours : a chaque ajout de fin (cXe, cT*), le mettre a jour dans la fiche - idealement verifie par le protocole-sante-fichiers-agents.
3. Les IDs de fins cT6-cT10 (ligne trio) ont une lettre majuscule au milieu : les regex de scan [a-z] les ratent - utiliser [a-zA-Z] dans les outils de verification.
## [LECON] 2026-08-11 -- PROTOCOLE-SANTE v0.1.2 : BLOC FINS REELLES OBLIGATOIRE (Buffy)

**Mission** : renforcer le protocole-sante-fichiers-agents pour verifier le croisement du bloc FINS REELLES de la fiche avec les fins reelles du parcours (anti-recurrence de l'ecart detecte par l'audit Themis du Pattern 14 : le trio n'avait aucun bloc).

**Action** :
1. Sous-critere E5d ajoute : le bloc FINS REELLES DE MA CARTE vX devient OBLIGATOIRE sur CHAQUE fiche (les 11), avec croisement BIDIRECTIONNEL fiche/parcours : (1) version du bloc == version du parcours, (2) chaque fin reelle citee (aucune absente), (3) chaque fin citee existe et est de type fin (aucune fantome), (4) titre declare == titre reel de la case.
2. Version bump v0.1.1 -> v0.1.2 + historique + ligne E5 du tableau des etapes maj.

**Verification reelle** : le garde-fou detecte exactement l'etat actuel - trio (athena, minerve, promethee) A REVOIR (pas de bloc), 8 autres A JOUR (blocs conformes v0.3.x/v0.4.x). Normes 0/0.

**Lecons** :
1. Une verification de croisement doit etre BIDIRECTIONNELLE et OBLIGATOIRE sur tous les fichiers du perimetre, pas seulement ceux qui ont deja l'artefact : le bloc FINS REELLES etait present sur 8 fiches mais absent du trio depuis la migration v0.2.4 - c'est le trou que E5d ferme.
2. Le renforcement du protocole (garde-fou) est la bonne reponse a un ecart detecte : le protocole-sante verifie desormais automatiquement le Pattern 14 secondaire a chaque execution de Janus.
3. Prochaine mission recommandee : Buffy ajoute les blocs FINS REELLES sur le trio pour passer le garde-fou E5d en A JOUR 11/11.
## [LECON] 2026-08-11 -- BLOCS FINS REELLES DU TRIO AJOUTES : E5d 11/11 A JOUR (Buffy)

**Contexte** : l'audit Themis du Pattern 14 (2026-08-11) avait revele que les 3 fiches du trio (athena, minerve, promethee) ne citaient AUCUNE fin reelle cX, en ecart avec le protocole-sante E5d (renforce la veille : bloc FINS REELLES obligatoire sur CHAQUE fiche avec croisement bidirectionnel). Mission : ajouter les blocs sur les 3 fiches.

**Lecon** :
1. Les 3 parcours du trio (v0.2.4) ont les MEMES 6 fins reelles (c9e, c10, c20, c20d, c21, c23) -- le bloc est donc identique sur les 3 fiches, seuls les titres exacts viennent du parcours JSON (a verifier en reel, jamais recopies d'une autre fiche).
2. Le titre reel de c20 est "Signaler le besoin" SANS prefixe "FIN -" (contrairement aux 5 autres fins) -- le croisement E5d exige le titre EXACT du parcours, pas un titre normalise.
3. Point d'insertion standard : fin de la section PARCOURS (apres le bloc Case 0 commune), avant le separateur `---` qui precede ## REGLES ABSOLUES -- identique aux 8 fiches deja conformes.
4. Le verificateur E5d (croisement bidirectionnel) confirme : 11 A JOUR / 0 A REVOIR ; valider-cartes-decision --tous CONFORME ; non-regression 21/21 OK ; normes 0/0.
5. Anti-recurrence : le protocole-sante E5d v0.1.2 detecte maintenant automatiquement toute fiche sans bloc ou avec un bloc incomplet/incoherent (version, fin absente, fin fantome, titre inexact).
## [LECON] 2026-08-11 -- PISTE 'DEFaut SIGNALE -> ACTIVER L AGENT HABILITE' AJOUTEE DANS LA CARTE DE JANUS v0.3.8 (Buffy)

**Contexte** : constat utilisateur sur la chaine reelle -- Morpheus a decouvert un defaut cause par Vulcain (tri du catalogue) et l a rapporte dans son rapport de fin, mais la carte de Janus n avait AUCUNE piste pour lire ce rapport et activer l'agent habilite (Vulcain). Le flux c8 -> c9 -> c9b -> c10 renvoyait TOUJOURS a Cerberus ; seule la ligne TRIO (cT8-cT10) avait la boucle KO.

**Modification (parcours-janus v0.3.7 -> v0.3.8)** :
1. c9 (Lecons et retour) : suivant c9b -> c9f
2. c9f (question) 'Un rapport ou une lecon signale un defaut a corriger chez un autre agent ?' : OUI -> c9g, NON -> c9b
3. c9g (action) 'Activer l agent habilite pour reparer le defaut' : REGLE 4 (je signale, je ne corrige pas) + boucle KO (modele ligne trio cT8-cT10), suivant c9e (fin existante REUTILISEE, pas de duplication)
4. Fiche janus.md : PARCOURS v0.3.8 + FINS REELLES v0.3.8 (les fins listees restent valides, c9e reutilisee)

**Lecons** :
1. Le flux de verdict d un agent de controle doit TOUJOURS avoir une piste de retour vers l'agent concerne (boucle KO) -- pas seulement dans la ligne trio mais dans TOUT le parcours.
2. Reutiliser les fins existantes (c9e) evite la duplication et garde le test-018 (fins) vert.
3. Apres bump de version d un parcours, verifier la fiche (Pattern 14) : valider-cartes-decision detecte l incoherence fiche/parcours (NON CONFORME) et le test-021 la propage -- tout reverdi apres correction de la fiche.
4. Les 3 flux de navigation valides : defaut signale (c9f OUI), pas de defaut (c9f NON -> c9b -> c10), auto-amelioration (c9b OUI -> c9c -> c9d -> c9e).
## [LECON] 2026-08-11 -- PISTE 'DEFaut SIGNALE -> ACTIVER L AGENT HABILITE' AJOUTEE DANS LA CARTE DE THEMIS v0.3.7 (Buffy)

**Contexte** : extension a Themis de la piste ajoutee a Janus (c9f/c9g v0.3.8, validee par second controle) : un rapport/lecon qui signale un defaut chez un autre agent doit declencher l'activation immediate de l'agent habilite (boucle KO).

**Modification (parcours-themis v0.3.6 -> v0.3.7)** :
1. c12 (Lecons et retour) : suivant c12b -> c12f
2. c12f (question) 'Un rapport ou une lecon signale un defaut a corriger chez un autre agent ?' : OUI -> c12g, NON -> c12b
3. c12g (action) 'Activer l agent habilite pour reparer le defaut' : REGLE 4 (je signale, je ne corrige pas) + boucle KO (modele cT8-cT10), suivant c12e (fin existante REUTILISEE)
4. Fiche themis.md : PARCOURS v0.3.7 + FINS REELLES v0.3.7 (les 6 fins citees restent valides : c12e, c13, c23, c23d, c24, c25b)

**Verifications reelles** :
- valider-cartes-decision --agent themis : CONFORME
- 3 flux de navigation OK (defaut signale, pas de defaut, auto-amelioration) + 0 reference morte
- Pattern 12 : c12g ne cree aucun fichier (regle + outil)
- Non-regression complete : 21/21 OK
- Normes : 0 non-ASCII, 0 CRLF (parcours + fiche)

**Lecons** :
1. Le modele de piste 'defaut signale' est REPRODUCTIBLE d une carte a l autre : adapter uniquement les identifiants (c9f/c9g chez Janus -> c12f/c12g chez Themis) et reutiliser la fin de reprise existante.
2. Apres bump de version, verifier la fiche (Pattern 14) : valider-cartes-decision detecte l incoherence fiche/parcours.
3. Themis et Janus (agents de controle) ont desormais la boucle complete : defaut signale -> activation immediate de l agent habilite.
## [LECON] 2026-08-11 -- 18 FINS 'ACTIVER JANUS' / 'RETOUR DE THEMIS' CORRIGEES POUR LA BOUCLE KO (Buffy)

**Contexte** : apres l'ajout de la piste 'defaut signale -> activer l'agent habilite' dans les cartes de Janus (c9f/c9g v0.3.8) et Themis (c12f/c12g v0.3.7), les fins des 8 agents qui activent ces controleurs contenaient des messages inexacts affirmant que Janus/Themis 'REACTIVE Cerberus' ou 'me REACTIVE' sans mentionner la boucle KO.

**Corrections (18 fins, 8 parcours)** :
1. 10 fins 'Activer Janus' (athena c10, atlas c11, buffy c8/c22/c27, clio c12, minerve c10, morpheus c10/c14, promethee c10) : derniere phrase remplacee par 'Janus controle ; s il signale un defaut (boucle KO, carte Janus v0.3.8 c9f/c9g), il m activera pour corriger et je le reactiverai avec mon bilan ; sinon il REACTIVE Cerberus avec <verdict>' (variante adaptee par fin).
2. 8 fins 'Retour de Themis' (athena c23, atlas c33, buffy c41, clio c18, minerve c23, morpheus c19, promethee c23, vulcain c21) : message remplace pour distinguer 'si aucun defaut -> Themis me REACTIVE avec son rapport' / 'si defaut signale (boucle KO, carte Themis v0.3.7 c12f/c12g) -> Themis m active pour corriger et je la reactiverai avec mon bilan'.

**Decision versionning** : PAS de bump de version -- correction purement documentaire des messages (aucun changement structurel ni de navigation). Les tests test-004 (morpheus 0.3.3), test-005 (atlas 0.3.4) et test-016 (buffy 0.3.7) verifient les versions : un bump aurait casse ces tests sans apporter de valeur.

**Verifications reelles** :
- 18/18 fins avec boucle KO presente
- valider-cartes-decision --tous : 11/11 CONFORME
- Non-regression complete : 21/21 OK
- Normes : 0 non-ASCII, 0 CRLF sur les 8 parcours

**Lecons** :
1. Toute fin qui active Janus/Themis doit mentionner la boucle KO pour ne pas induire l'agent en erreur (le controleur peut renvoyer le rapport pour correction avant de clore vers Cerberus).
2. Une correction de messages n'exige pas de bump de version si aucun test ne verifie le contenu -- verifier les tests qui referencent les versions avant de bumper.
3. Attention aux indices dans les scans de fichiers (split('/')[2] = agent, pas [3]).
## [LECON] 2026-08-11 -- REGLE PATTERN 13 MATERIELISEE DANS LA CARTE ET LA FICHE DE CERBERUS (Buffy)

**Contexte** : constat utilisateur -- Buffy (et d'autres agents) ne suivent pas leur carte de fin 'Activer Janus' car les missions redigees par Cerberus imposent systematiquement 'A LA FIN : reactiver Cerberus'. Le Pattern 13 (la fin suit SA carte) etait viole par la redaction des missions, pas par les cartes des agents.

**Modifications** :
1. parcours-cerberus.json (v0.3.3 INCHANGEE) : regle courte (< 160 car) ajoutee dans c7 'Annoncer la mission et suivre le cycle' (3 indices, max 3) : 'PATTERN 13 : ne JAMAIS demander reactiver Cerberus dans une mission - l agent suit SA carte (ex. Buffy/Morpheus : active Janus, qui reactive Cerberus).'
2. cerberus.md : regle complete ajoutee dans la section 'Pour terminer ma mission (la fin suit SA carte)' : 'REGLE REDACTION DE MISSION (Pattern 13) : quand je redige une mission, je ne demande JAMAIS reactiver Cerberus a la fin. Je demande a l agent de suivre SA carte (ex. BUFFY/MORPHEUS : active JANUS pour le second controle, qui reactive Cerberus avec son verdict). Formule : A LA FIN : suis TA carte pour ta fin (Pattern 13).'

**Point d'attention (surcharge)** : la regle complete (349 car) placee dans c6 a fait passer la case a 4 indices (max 3) + indice de 349 car (> 160) -> valider-case A ALLEGER, tests 009/013/015 KO. Resolution : retirer la regle de c6 (retour 3 indices) et la placer en version courte dans c7 (3 indices, 153 car) + version complete dans la fiche.

**Verifications reelles** :
- valider-case cerberus : CONFORME (0 surcharge)
- valider-cartes-decision --agent cerberus : CONFORME
- Non-regression complete : 21/21 OK (test-009, test-013, test-015 reverdis)
- Normes : 0 non-ASCII, 0 CRLF (parcours + fiche)

**Lecons** :
1. Une case a max 3 indices et max 160 car par indice : toute regle longue doit aller dans la FICHE ou etre raccourcie (le Pattern 13 est maintenant dans c7 + fiche).
2. La racine du defaut 'agent ne suit pas sa carte' etait la REDACTION des missions par Cerberus : desormais la regle est OBLIGATOIRE dans sa carte (c7) et sa fiche (Pattern 13 : ne JAMAIS demander reactiver Cerberus).

## [LECON] 2026-08-11 -- GENERALISATION PATTERN 13 CONTROLEURS + INCIDENT RESTAURATION GIT (Buffy)

**Mission** : ajouter la regle 'ne JAMAIS demander reactiver Cerberus' (Pattern 13) aux cases d'activation des cartes de controle (cerberus c12b/c17/c21/c22/c14, janus c28, themis c22), selon le choix utilisateur 'Controleurs + Cerberus'.

**Modifications appliquees** :
1. cerberus c12b/c17/c21/c22 : ajout regle courte P13 (3 indices, <=144 car)
2. cerberus c14 : fusion des 2 regles (REGLE + ANTI-BOUCLE) en 1 texte (158 car) pour liberer une place, puis ajout P13
3. janus c28 et themis c22 : ajout regle courte P13
4. cerberus c6/c10 : PAS de modification (cases pleines 3/3) - leurs flux passent par c7 qui porte deja la regle

**INCIDENT CRITIQUE (lecon majeure)** : le git checkout de restauration du format a EFFACE les changements non commites des missions precedentes (janus v0.3.8 piste c9f/c9g + ligne trio cT1-cT10 ; themis v0.3.7 piste c12f/c12g + c13 Activer Janus ; cerberus c0d). Reconstruction complete depuis les rapports de controle et les tests (test-021, test-013, test-018).

**Lecons** :
1. FORMAT DES PARCOURS = indent=2 (pas indent=1) - verifier le round-trip avant d'ecrire
2. NE JAMAIS utiliser git checkout sur des fichiers avec changements non commites - verifier git status AVANT
3. Un script qui recharge le fichier a chaque iteration ecrase les modifications precedentes (charger UNE fois par agent)
4. Les rapports de controle (janus/controles/, themis/rapports/) sont des sources de verite fiables pour la reconstruction
5. Les tests (test-013/018/021) sont les juges de la conformite - les laisser guider la reconstruction

**Verifications finales** : valider-cartes-decision 3/3 CONFORME, non-regression 21/21 OK, 0 non-ASCII, 0 CRLF, 0 residu.

## [LECON] 2026-08-11 -- TEST-023 BRANCHE DANS LE PARCOURS VULCAIN v0.3.7 (Buffy)

Branchement du test-023-grep-budget-pondere (garde-fou coherence budget
pondere E7 du protocole-verification-coherence v0.2.0) dans le parcours
vulcain, dans les 2 flux de refonte d outils/specs :
- c6d (flux CONSTRUIRE, entre c6c et c7) : Lancer le test-023-grep-budget-pondere
- c12d (flux MODIFIER, entre c12c et c13) : idem
Chaque case : 3 regles courtes (<= 100 car., poids 0,5) + 1 indice outil
(PASSE PAR LE GENERATEUR) = poids 2,0 (budget 3,0 OK).

Lecons :
1. Le pattern c6c/c12c est le modele des cases scan/controle : indices
   CREATION LIMITEE + PASSE PAR LE GENERATEUR + indice outil + condition.
2. ATTENTION BUDGET PONDERE : 3 regles LONGUES (> 100 car.) + 1 outil =
   3,5 > 3,0 -> A ALLEGER. Raccourcir les textes a <= 100 car. donne
   3 x 0,5 + 0,5 = 2,0 OK. Verifier le poids a chaque ajout d indices.
3. valider-cartes-decision croise la fiche (Pattern 14) : bump du parcours
   = mise a jour des mentions PARCOURS (vX.Y.Z) dans la fiche dans la MEME
   mission (regle E5b/croisement).
4. OBSERVATION PREEXISTANTE (hors perimetre) : les cases c6c/c12c ont un
   indice regle de 198 car. (> 160) -> A ALLEGER preexistant (git HEAD deja
   NON CONFORME). A traiter dans une mission ulterieure (alleger ces textes
   vers des references).
## [LECON] 2026-08-11 -- REGISTRE D USAGE BRANCHE DANS LES 11 CARTES (Buffy)

**Objet** : nouvelle case dediee "Enregistrer mes usages d outils" (outil PASSE PAR LE
GENERATEUR -> enregistrer-usage-outil) avant chaque fin de mission des 11 parcours,
suite a la demande utilisateur (11 agents, nouvelle case).

**Modifications** :
1. 11 parcours : 13 nouvelles cases action (vulcain c22/c23 et morpheus c20/c21 ont 2 fins
   principales) avec indice outil enregistrer-usage-outil (catalogue, sans commande en dur
   = PASSE PAR LE GENERATEUR) + 1 regle courte. Poids 1.0 (budget 3.0 OK).
2. Re-pointage des precurseurs (suivant + branches) vers la nouvelle case.
3. Bumps de version : cerberus/buffy/vulcain/morpheus/janus/atlas/themis 0.4.0,
   clio 0.5.0, trio athena/promethee/minerve 0.3.0.
4. 11 fiches : REGLE ABSOLUE PARCOURS mise a jour (Pattern 14).

**Verifications reelles** : valider-cartes-decision 11/11 CONFORME, valider-case OK
(seuls ecarts = preexistants confirmes via git HEAD : vulcain c9e/c15e/c6c/c12c,
clio c6c), navigation reelle buffy [57/57] et athena [34/34] passant par la nouvelle case
puis la fin.

**Pieges evites** :
1. Le re-pointage automatique (suivant=fin -> suivant=nouvelle case) a aussi transforme le
   suivant de la NOUVELLE case (auto-reference !) -> correction : la nouvelle case doit
   pointer vers la fin cible. Verifier le JSON resultat (suivant != id de la case).
2. Les versions dans le JSON n ont pas de prefixe 'v' (0.4.0, pas v0.4.0) -> le bump doit
   gerer les deux formats (le test-022/valider-cartes P9 exige sans prefixe).
3. Les ecarts valider-case (c9e/c15e non joignables vulcain, c6c A ALLEGER) etaient
   PREEXISTANTS : comparer avec git HEAD avant de corriger quoi que ce soit.

## [LECON] 2026-08-11 -- ANTI-REGRESSION HISTORIQUE + MAILLON MANQUANT CERBERUS (Buffy)

**Contexte** : l'utilisateur a constate que AGENTS-historique.md n'etait plus mis a jour (regression) et que le maillon "rapport de Janus avec problemes a resoudre -> Cerberus active l'agent habilite" manquait.

**Cause racine de la regression** : les activations/reactivations passaient par des scripts temporaires maison au lieu de l'outil central activer-agent-principal (qui journalise AGENTS-historique + classeur). Dans les cartes : 19 fins d'activation (sur 10 parcours) n'avaient PAS l'indice outil activer-agent-principal PASSE PAR LE GENERATEUR -> la commande etait en dur dans le message ou absente (janus c10 n'avait rien du tout).

**Actions realisees** :
1. AGENTS.md : bloc session-llm-1 reconstruit (un seul tableau Cerberus, sans separateur parasite). Cause de la corruption : mes scripts de cloture utilisaient txt.find('---') qui attrapait le separateur du tableau markdown |---|---| au lieu du separateur de bloc.
2. AGENTS-historique.md : bloc ## Historique duplique supprime + 9 entrees du tour restaurees.
3. 19 fins des 10 parcours : indice outil activer-agent-principal PASSE PAR LE GENERATEUR ajoute (athena c10, atlas c11+c31b, buffy c22+c27+c8, clio c12, janus cT6-cT10+c10 avec commande reactiver, minerve c10, morpheus c10+c14, promethee c10, themis c13+c25b). Poids budget <= 3.0 verifie partout.
4. Cerberus 0.4.0 -> 0.4.1 : nouvelle case c15b "Rapport de Janus : problemes a resoudre ?" (controle, OUI->c15c / NON->c16) + c15c "Activer l agent habilite (problemes a resoudre)" (action, suivant->c15b, boucle de verification) + c15 branche OUI -> c15b. Fiche cerberus Pattern 14 v0.4.1.

**Verifications reelles** : valider-cartes-decision 11/11 CONFORME, valider-case cerberus CONFORME (0 erreur, 0 a alleger), navigation reelle des 2 flux (OUI -> c15c -> retour c15b ; NON -> c16), poids budget 21/21 OK. Ecarts vulcain/clio = preexistants (confirme via git HEAD). Test-013 : 3 KO attendus (version 0.4.1 + compteurs) -> mission Morpheus.

**LE CON (regle absolue)** : pour TOUTE activation/reactivation d'agent, utiliser l'OUTIL CENTRAL activer-agent-principal (commande exacte, PASSE PAR LE GENERATEUR). JAMAIS de script temporaire maison qui modifie AGENTS.md/AGENTS-historique directement. C'est l'outil central qui garantit la trace dans AGENTS-historique et le classeur. Un script de cloture temporaire = regression silencieuse (historique non journalise + corruption de structure).

## [LECON] 2026-08-11 -- CARTES RENFORCEES ANTI-SCRIPTS-TEMPORAIRES (Buffy)

**Contexte** : mission anti-scripts-temporaires (3 outils crees par Vulcain, garde-fou test-024 par Morpheus). Renforcement des cartes pour que le Pattern outil-temporaire soit reellement suivi.

**Actions** :
1. 10 fins "FIN - Outil temporaire" (athena c20d, atlas c29d, buffy c35d, clio c15d, janus c29d, minerve c20d, morpheus c16d, promethee c20d, themis c23d, vulcain c18d) : ajout de l'indice outil enregistrer-usage-outil PASSE PAR LE GENERATEUR + regle DECLARATION (tout outil temporaire cree est declare au registre en mode script-temporaire). Poids 1.5 <= 3.0 partout.
2. buffy c10b : outil editer-parcours branche (modification de parcours via l outil au lieu d un script maison).
3. Bumps : athena/minerve/promethee 0.3.1, atlas/buffy/janus/morpheus/themis/vulcain 0.4.1, clio 0.5.1. Fiches Pattern 14 alignees (10/10).

**Verifications** : valider-cartes-decision 11/11 CONFORME, normes 10 fiches + 11 JSON OK.

**LE CONS** :
1. Le maillon manquant etait la DECLARATION : les cases creaient l'outil temporaire mais ne journalisaient pas sa creation. Maintenant la fin exige enregistrer-usage-outil --mode script-temporaire AVANT suppression.
2. Le circuit est complet : creer (generateurs-outil-temporaire) -> declarer (enregistrer-usage-outil) -> supprimer (0 residu) -> detecter (detecter-usage-scripts-temporaires croise le registre).
3. Les bumps de versions cassent les tests de version (test-004/005/016) : a adapter par Morpheus dans la meme chaine.

## [LECON] 2026-08-12 -- FIN DU CYCLE VICIEUX DES ECARTS PRE-EXISTANTS (Buffy)

**Mission** : corriger MAINTENANT les 5 ecarts pre-existants signales depuis plusieurs missions Janus sans jamais etre corriges.

**Causes identifiees** :
1. vulcain c9e/c15e non joignables : les questions c9b/c15b (Ameliorations possibles) etaient ORPHELINES - c22.suivant pointait la fin c9 directement, et c9b.NON pointait c22 (boucle). Recablage correct (modele morpheus c8->c8b->c9) : c22.suivant=c9b, c9b.NON=c9 ; c23.suivant=c15b, c15b.NON=c15.
2. vulcain c6c/c12c : indice regle CREATION LIMITEE de 198 car (> 160) - raccourci a 125 car.
3. clio c6c : indice regle PATTERN 3 de 175 car (> 160) - raccourci a 130 car.

**Verifications reelles** : valider-case vulcain CONFORME + clio CONFORME (0 erreur, 0 a alleger), valider-cartes-decision 11/11 CONFORME, navigation reelle c9b->c9 (NON), c9b->c9e (OUI), c15b->c15 (NON), non-regression 24/24 OK (outil lancer-non-regression), registre 0 ligne apres tests.

**Lecons** :
1. Un Pattern 17 mal cable (question orpheline + boucle NON) rend des fins injoignables SANS erreur visible de navigation quotidienne - seul valider-case le detecte. Toujours verifier la joignabilite de TOUTES les fins apres insertion de cases.
2. Les ecarts pre-existants signales dans les rapports doivent etre corriges a la mission suivante, pas accumules : chaque rapport doit transmettre la liste des ecarts ouverts a Cerberus.
3. La regle des 160 caracteres est un plafond dur : les indices regle doivent etre concis, l'info detaillee va dans le protocole reference, pas dans la case.



## [LECON] 2026-08-13 -- AXE D : THEMIS MAILLON AUTOMATIQUE DE LA CHAINE (Buffy)

**Contexte** : demande utilisateur (axe D de la mission Themis) - Themis avait une
faiblesse declaree 'Depend de Cerberus pour etre activee' : les agents avaient une
case 'Activer Themis pour auditer' mais AUCUNE fin de mission ne l activait
systematiquement (seulement la branche 'audit' de la mission hors parcours).

**Decisions** :
1. POINT D INSERTION : Themis AVANT Janus (evaluation puis controle croise). La
   REGLE IMMUABLE JANUS exige que Janus soit le dernier maillon qui reactive
   Cerberus (test-018 : seule fin REACTIVER-CERBERUS = janus c10) -> Themis ne peut
   PAS passer apres. Nouvelle chaine : Cerberus -> Agent -> Themis -> Agent -> Janus
   -> Cerberus. Themis reactive l'agent precedent avec son rapport (c25b deja prevu)
   et l'agent reprend vers sa fin Janus.
2. MECANIQUE DE CASE : impossible de mettre un 'suivant' sur une fin (garde-fou
   suivant mort de valider-cartes : 0 fin avec suivant dans les 11 parcours).
   Solution : 2 nouvelles cases avant CHAQUE fin de mission - action 'Activer Themis
   pour auditer ma mission' (commande exacte activer session-llm-1 themis) -> controle
   'Retour de Themis recu ?' (OUI -> fin existante / NON -> soi-meme = pattern de
   re-essai natif, la boucle d attente est legitime).
3. PERIMETRE : buffy (c8/c22/c27), vulcain (c9/c15), morpheus (c10/c14), atlas (c11),
   clio (c12). janus N EST PAS modifie (sa fin c10 est REACTIVER Cerberus, il est le
   dernier maillon - la mission la listait par erreur). La carte themis v0.4.2 est
   elargie : branche 'audit-fin-mission' dans c1 -> c25 (Auditer pour un agent) +
   message c25 enrichi.
4. FICHE THEMIS : faiblesse 'Depend de Cerberus' remplacee par une FORCE (activee
   automatiquement en fin de mission) + declenchement enrichi + Pattern 14 v0.4.2.

**Lecons** :
1. Une fin avec un 'suivant' est IMPOSSIBLE (garde-fou suivant mort) : la reprise
   apres une delegation se modele par un CONTROLE de re-essai (NON -> soi-meme),
   pattern natif deja autorise par valider-case et detecter-cablages.
2. Les fins 'FIN - Activer Janus' ne changent PAS : on insere l'etape Themis AVANT,
   ce qui preserve test-018 (fins Activer Janus en place) et test-033 (morpheus
   c10/c14 inchanges). Seuls les compteurs de version/cases des tests changent
   (test-004 morpheus 0.4.3->0.4.4, test-016 buffy 0.4.1->0.4.2 + 3 actions/3
   controles en plus) : a adapter par Morpheus.
3. La commande activer themis exacte (PAS reactiver) doit etre dans le message de
   l'action, comme pour les fins Activer Janus - le piege reactiver reste elimine.
4. Verification : 6/6 valider-case CONFORME + valider-cartes CONFORME + detecter
   PROPRE, navigation reelle c22a -> c22b (OUI) -> c22 FIN, normes 0/0, 0 residu
   temporaire. Themis n'est plus une option : c'est un maillon automatique.

## [LECON] 2026-08-13 -- CONTEXTE RECOLTE AVANT MODIFICATION DE CARTES (Buffy)

**Lecons** :
1. AVANT de modifier des cartes, recolter : les ids de cases existants (choisir des
   ids libres : c8a/c8b libres chez buffy mais c9b/c15b pris chez vulcain -> c9f/c9g),
   les predecesseurs exacts de chaque fin (suivant ET branches), les regles des
   validateurs (garde-fou suivant mort, seuil 160 car sur les indices regle).
2. Le seuil de 160 caracteres s'applique AUSSI aux nouvelles cases : mon premier
   indice REGLE THEMIS faisait 176 caracteres -> raccourci a 151.
3. Les messages de fin des agents ne sont pas tous 'FIN - Activer Janus' : vulcain
   c9/c15 sont 'FIN - Construire/Modifier un outil' qui activent MORPHEUS (pas
   Janus) - la mission Cerberus les avait identifies par erreur ; l'insertion
   Themis reste pertinente (evaluation avant la chaine Morpheus -> Janus).


## [LECON] 2026-08-13 -- SEUL JANUS LANCE LA NON-REGRESSION (Buffy)

**Contexte** : demande utilisateur - verifier que SEUL Janus a le droit de lancer
la non-regression (tester-lancer-non-regression) : sur une ligne de travail
multi-agents, c est Janus a la fin qui la lance (dernier maillon avant
Cerberus). Philosophie enoncee : les agents sont construits de la meme facon
(meme template) mais chacun a SON identite et SON role - aucun interet a avoir
des parcours identiques.

**Actions** : 1) AUDIT Cerberus : signatures d ids des 11 cartes TOUTES
distinctes (principe identite deja respecte). 2) parcours-morpheus v0.4.5 :
case c12 completement adaptee - titre Completer et executer les tests de l
outil, indice tester-lancer-non-regression RETIRE, regle sous 160 car (152) :
Morpheus execute les tests INDIVIDUELS (python3 test-XXX.py + protections),
la non-regression COMPLETE appartient a JANUS. 3) parcours-vulcain v0.4.6 :
case c8 - indice residuel tester-lancer-non-regression RETIRE (la case delegue
via activer-agent-principal). 4) fiche morpheus.md : REGLE ABSOLUE --
NON-REGRESSION JANUS ajoutee (seul Janus lance la complete). 5) test-004 adapte
(morpheus 0.4.4 -> 0.4.5).

**Verifications** : valider-case 2/2 CONFORME, valider-cartes 2/2 CONFORME,
detecter-cablages PROPRE, test-004 16/16, test-033/test-018 verts, seul janus
(3) reference la non-regression dans les cartes, normes 0/0.

**Lecon** : la separation des roles est un garde-fou de gouvernance : chaque
agent execute SES outils de role (Morpheus = tests individuels, Janus =
non-regression complete finale). Un indice outil residuel dans une carte
(vulcain c8) est une derive a detecter par audit, pas seulement par les tests.
## [LECON] 2026-08-13 -- BADGE HEADER AUTO DANS combos-maj-readme-massive v0.1.1 (Buffy)

**Contexte** : lecon Clio/Janus - le combo maj-readme-massive reconstruisait
les tables mais pas le badge Outils-N en dur du header, et le lien href
pouvait rester obsolete (ex : affichage 128, lien 121).

**Correction** : nouvelle fonction aligner_badge_header(racine) qui importe
compter_outils (source de verite de combos-analyse-projet) via importlib
(le nom du module source contient des tirets : import direct impossible) et
remplace l affichage ET le href du badge Outils-N (regex badge/Outils-([0-9]+)-).
Appel dans l Etape 4. Bump 0.1.0 -> 0.1.1 + doc a jour + test-020 adapte.

**Tests** : README deja aligne -> aucune correction (False) ; README
desynchronise (display 120 / href 99) -> realise sur 128 affichage + href
(True) ; test-020 46/46 OK (execution reelle du combo incluse).

**Lecon** : tout import inter-fichiers doit passer par importlib quand le nom
du module source contient des tirets (convention de nommage des outils).
## [LECON] 2026-08-13 -- BADGES HEADER GENERALISES v0.1.2 (Buffy)

**Contexte** : demande utilisateur d etendre la synchronisation des badges
du header au-dela d Outils. Decisions : version = fichier dedie
clio/version-readme.txt (semver sans v, maintenu par Clio), statut =
clio/statut-projet.txt, suppression des residus accidentels 0.2.1/v0.2.6
a la racine (sorties de activer-agent-principal).

**Correction** : aligner_badge_header -> aligner_badges_header generalisee :
regex generique badge/Nom-(valeur)-(couleur) (re.sub global affichage + href)
pour Outils (compter_outils), Version (v+contenu), Statut (contenu), et
alignement du href sur l affichage pour les badges statiques (Plateforme,
Fait_avec, Langages) en cas de divergence. Bump 0.1.2 + doc + test-020.

**Tests** : idempotence (README sain -> aucune correction), desynchronisation
(version 0.2.9 + statut dev + href 121 -> realignes affichage+href), test-020
46/46 OK.

**Lecon** : les fichiers de version accidentels a la racine (noms de type
"0.2.1" / "v0.2.6") provenaient de redirections de sortie - les sources de
verite de version doivent vivre dans le cerveau-projet (clio/), jamais a la
racine.
## [LECON] 2026-08-13 -- TOUS LES OUTILS DU CATALOGUE INDEXES (Buffy)

**Contexte** : demande utilisateur - chaque outil ajoute au catalogue doit
avoir sa doc et son entree index-tools. Etat initial : 137 scripts uniques
(0 script manquant, 0 doc manquante) mais 27 entrees index-tools absentes
(4 outils reels + 23 tests). Decision utilisateur : tout indexer.

**Actions** : ajoute combos-analyse-projet + combos-maj-readme-massive
(section Combos), enregistrer-usage-outil (section Enregistrer creee),
verifier-conformite-fiche (section Verifier), et nouvelle section Tests
(tester/tests/) avec les 39 tests (descriptions depuis les docstrings, 2e
ligne du docstring = vraie description). Stats recalculees : total 118 -> 166.
Test-007 adapte (15/15). Badge README inchange (128, compte les dossiers).

**Lecon** : le total de l index-tools etait faux depuis longtemps (les
compteurs ne couvraient pas tous les outils) - le garde-fou a venir
(test-040 Morpheus) verifiera en permanence catalogue -> doc + index.
Les descriptions du catalogue pour les tests contenaient des chemins de
scripts (mauvaise qualite) - les docstrings des tests sont la source fiable.

## [LECON] 2026-08-13 -- NON-REGRESSION PASSEE A 5 SERIES (Buffy)

**Contexte** : demande utilisateur - la serie d de la non-regression grossissait
(18 tests, 26 unites) vs 13-14 pour a/b/c. Objectif : equilibrer en 5 series.

**Changement** : tester-lancer-non-regression.py passe de 4 a 5 series.
- nouvelle serie e = [test-028, 029, 032..040] (11 tests, 13 unites) :
  coherence documentaire + anti-recurrence (test-028 le plus lourd en tete)
- serie d reduite a [test-023..027, 030, 031] (7 tests, 13 unites) :
  registre + garde-fous globaux conserves (invariant test-027)
- equilibre final : a=14, b=13, c=14, d=13, e=13 (67 unites, 0 manquant,
  0 doublon)
- les 2 copies du lanceur (copie 2 executee via __main__ final) modifiees
  a l'identique : SERIES, SERIES_NOMS, SERIES_ORDRE, choices argparse,
  commentaires d'en-tete ; doc .md (tableau + option --series)

**Verifications** : py_compile OK, --series d = 7/7 OK (13.9s),
--series e = 11/11 OK (44.3s), test-027 11/11 (invariants intacts sans
modification du test), test-031 10/10, test-032 10/10, normes 0/0.

**Lecon durable** : un decoupage en series doit rester EQUILIBRE en durees
unitaires (DUREES_CONNUES) : une serie qui concentre les tests lourds devient
le goulet d'etranglement du mode mono-serie. Le test-027 (couverture + absence
de doublons + affectation de test-027 en d) est l'invariant qui protege le
decoupage : tout nouvel ajout de test doit etre affecte a une serie.

## [LECON] 2026-08-13 -- PATTERN VERSION README DOCUMENTE DANS LA FICHE CLIO (Buffy)

**Contexte** : demande utilisateur - les sources de verite de la version du
README existaient (clio/version-readme.txt = 0.2.0, clio/statut-projet.txt =
stable) et le combo combos-maj-readme-massive les lisait, mais la fiche clio
ne documentait PAS la convention de bump : Clio n'avait aucun moyen de savoir
qu'elle doit maintenir version-readme.txt a chaque grosse MAJ (case c6c).

**Changement** : ajout dans clio.md (v0.2.0 -> v0.2.1) d'une section dediee
"## PATTERN VERSION README (convention de maintenance)" - section SPECIFIQUE
toleree par verifier-conformite-fiche (non bloquante) - qui documente :
- les 2 fichiers sources de verite (version semver sans v, statut
  stable/prepare/dev)
- la REGLE DE BUMP : a chaque GROSSE MAJ (case c6c, combo massive),
  increment MINEUR pour une MAJ de contenu, MAJEUR pour une refonte,
  JAMAIS de patch pour une grosse MAJ
- le lien avec aligner_badges_header (le badge s'aligne automatiquement)
- les garde-fous test-038 (badge == source) + test-039 (sources + anti-residus)
- l'anti-residus : JAMAIS de fichier de version semver a la racine

**Verifications** : verifier-conformite-fiche --agent clio = CONFORME
(section specifique toleree), normes ASCII/LF 0/0, test-028 8/8 OK,
aucun test ne fige la version de la fiche clio.

**Lecon durable** : une source de verite n'est utile que si le gardien de la
source sait QU'IL doit la maintenir ET COMMENT (quand bumper, quel increment).
Documenter la convention dans la fiche de l'agent responsable est le maillon
qui transforme une source technique en comportement reel. Les sections
specifiques des fiches (tolerees) sont le bon endroit pour ces conventions
de maintenance propres a un agent.

## [LECON] 2026-08-13 -- COMBO MASSIVE BUMPE LA VERSION DU README (Buffy)

**Contexte** : demande utilisateur - le combo combos-maj-readme-massive lisait
la version (clio/version-readme.txt) pour aligner le badge Version du header,
mais ne BUMPAIT jamais la source quand le README changeait, et le rapport ne
mentionnait ni la version ni le bump (contraire a la convention Pattern
version README documentee dans la fiche clio).

**Changement** (v0.1.2 -> v0.1.3) :
- fonction bumper_version(racine) : incremente la version MINEURE
  (semver X.Y.Z -> X.(Y+1).0, jamais de patch pour une grosse MAJ) dans
  clio/version-readme.txt ; retourne (ancienne, nouvelle) ou None
- fonction lire_version(racine) : lit la version courante
- dans main() : SNAPSHOT du README au debut ; apres l etape --maj, si le
  README a change, bump AVANT aligner_badges_header (le badge Version
  s aligne sur la NOUVELLE version)
- rapport : etape 3b (bump), synthese console + Contexte du fichier --rapport
  mentionnent ancienne -> nouvelle ou "inchangee"
- doc .md + .sh mis a jour (version + mention bump) ; test-020 adapte
  (0.1.2 -> 0.1.3)

**Verifications** : py_compile, bumper_version testee en sandbox (bump,
absent, illisible, lecture), preuve fonctionnelle README modifie -> 0.2.0 ->
0.3.0, test-020 46/46, version-readme.txt reel intact (0.2.0, pas de bump car
README a jour), normes 0/0.

**Lecon durable** : une source de verite de version doit etre bumpee par
l OUTIL qui modifie le contenu (pas seulement par l agent) : le combo detecte
le changement (snapshot) et incremente AVANT d aligner les badges, sinon le
badge afficherait l ancienne version. Le bump est conditionnel (README change)
pour eviter une inflation de version a chaque lancement idempotent.

## [LECON] 2026-08-13 -- GARDE-FOU ANTI-RESIDUS ACTIVER-AGENT-PRINCIPAL v0.5.2 (Buffy)

**Contexte** : demande utilisateur - corriger la cause racine des residus 0.2.1/v0.2.6
(supprimes, surveilles par test-039). Diagnostic : le code de l outil (.sh + .py) etait
PROPRE (aucune redirection, verifie sur tout l historique git) - les residus venaient de
la COMMANDE D APPEL (redirection > / tee de la sortie de reactiver vers des fichiers
nommes comme des versions du contexte). Decision utilisateur : garde-fou PROACTIF dans
l outil + regle documentee (pas de capture auto, pas de suppression auto).

**Correction** : v0.5.1 -> v0.5.2 (py + sh + doc + spec).
- verifier_residus_racine() (py) / verifier_residus_racine (sh, parite ls -p) : scanne le
  repertoire courant, detecte les fichiers nommes comme des versions semver pures
  (regex ^v?X.Y.Z$), affiche un WARNING encadre (===) listant les residus + la regle
  anti-residu (supprimer, sources de verite de version dans clio/, JAMAIS a la racine).
- Declenche au debut de chaque action reelle (sidentifier/activer/reactiver/sessions),
  pas pour aide/--version (sorties propres conservees).
- Doc .md : nouvelle section "Ne jamais rediriger la sortie" (interdiction > et tee,
  la preuve d une activation est dans AGENTS-historique.md) + bump table versionning.
- Spec : bump parite (detecter-divergences-version).

**Tests** : preuves fonctionnelles sandbox 6/6 (positif py/sh : WARNING + action executee,
negatif : silence, --version/aide non contamines), test-007 22/22 VALIDE, evaluer-coherence
"Tous les outils references exist" (pas de faux positif backticks - lecon clio respectee),
normes ASCII/LF 0/0 sur 4 fichiers.

**Lecon durable** : un garde-fou REACTIF (test-039 detecte le residu a la non-regression)
n empeche pas l accident - un garde-fou PROACTIF au point d entree (l outil qui s execute
a chaque debut/fin de session) rend l accident VISIBLE immediatement, avant qu il ne soit
committe. Un outil ne peut pas empecher son appelant de rediriger sa sortie, mais il peut
rendre le resultat de l accident impossible a ignorer.

## [LECON] 2026-08-13 -- GARDE-FOU ANTI-RESIDUS ETENDU AUX 3 OUTILS CRITIQUES (Buffy)

**Contexte** : extension du garde-fou anti-residus (verifier_residus_racine, cree dans
activer-agent-principal v0.5.2) aux outils qui s executent souvent : guider-parcours
(v0.5.0 -> 0.5.1), valider-cartes-decision (v0.4.0 -> 0.4.1), editer-parcours
(v0.1.0 -> 0.1.1). Convention : auto-contenu (duplication du helper, comme
verifier_ascii) - pas de module partage entre outils.

**Correction** : verifier_residus_racine() + REGEX ^v?X.Y.Z$ + appel apres parse_args
(guider, editer) ou apres le bloc --version (valider) - les actions reelles declenchent
la detection, --version/aide restent propres. Les .sh de guider et valider sont des
WRAPPERS PURS (exec python3) : le garde-fou du .py les couvre, seul le bump de version
du .sh est necessaire. Docs : bump header + ligne versionning + mention du garde-fou
(editer.md n avait pas de table -> section Versionning creee). Spec guider : bump du
champ **Version outil** (la version de la SPEC v0.6.2 ne change pas).

**Tests** : preuves sandbox 6/6 (positif : WARNING + action executee pour les 3 outils ;
negatif : silence), --version des 3 propres, compile + bash -n OK, normes 0/0 sur 9
fichiers, evaluer-coherence "Tous les outils references existent".

**IMPACTS TESTS (a adapter par Morpheus)** : test-028 point 6 fige "Version outil :
0.5.0" -> 0.5.1 ; test-024 point 5 fige "editer-parcours --version v0.1.0" -> 0.1.1.

**Lecon durable** : le pattern "wrapper pur" (exec python3 dans le .sh) rend la parite
de sortie garantie PAR CONSTRUCTION et permet de n ajouter le garde-fou qu au point
d entree .py - verifier si le .sh est wrapper avant d y dupliquer du code.

## [LECON] 2026-08-13 -- REGLE ANTI-ECHAPPEMENT JSON DOCUMENTEE (Buffy)

**Mission** (Cerberus, demande utilisateur) : documenter la regle anti-echappement JSON des spawn_agents. Le piege (guillemets imbriques, backslashes, apostrophes, chevrons, pipes, heredocs dans les commandes inline) etait RECURRENT - lecons dans 5 corrections.md mais aucune regle formelle.

**Action** : enrichi protocole-creation-scripts-temporaires v0.2.0 avec la section 'Commandes spawn_agents : eviter les erreurs d echappement JSON' : regle d or (TOUTE commande complexe = script temporaire via write_file, jamais inline), cas a risque, procedure valide (1. write_file .tmp-*.py coding ascii, 2. basher cd + python3 + rm -f, 3. verifier 0 residu), pieges connus (test-024 auto-incrimination = commande directe toujours, residu en cas de timeout, ne pas lancer de test depuis un script temp). Index-regles-general mis a jour.

**Lecon** : la methode fiable eprouvee sur des dizaines de missions (write_file puis basher simple avec rm -f dans la commande) est maintenant la regle officielle. Les erreurs JSON ont coute des dizaines de spawn echoues - elles ne devraient plus se reproduire. Normes 0/0.

## [LECON] 2026-08-13 -- REGLE ANTI-ECHAPPEMENT ETENDUE AUX COMBOS (Buffy)

**Mission** (Cerberus, demande utilisateur) : etendre la regle anti-echappement aux commandes bash des combos. Mecanisme identifie : combos-moteur.py fait un remplacement BRUT de {var} (interpoler L249) puis shlex.split (L408) - une valeur avec apostrophe non echappee casse la commande en ValueError.

**Action** : combos-moteur.md v0.3.3 + section 'ECHAPPEMENT DES VALEURS' (regle d or : quoter {var} dans les commandes des cases outil, exemples MAUVAIS/BON, cas des valeurs avec apostrophes, application aux commandes bash des combos et du catalogue). Protocole-creation-scripts-temporaires v0.2.1 + section 'Commandes bash des combos (meme regle)' dans les pieges.

**Lecon** : le catalogue (149) et les 52 commandes des combos sont propres aujourd hui mais la regle protege le futur - un futur combo avec une raison contenant une apostrophe aurait casse en pleine chaine. Documenter le piege AVANT l'accident est la lecon de cette serie de missions anti-echappement. Normes 0/0.
## [LECON] 2026-08-13 -- TRIPLET PROTECTIONS + OPTIONS + CHRONO + CLARIFICATION SCRIPTS TEMPORAIRES (Buffy)

**Contexte** : demande utilisateur en 3 points : (1) generaliser le chrono dans
le template des tests (sans migrer les tests existants), (2) introduire une
REGLE IMMUABLE pour tout fichier contenant fonctions/tests/workflows : doit
toujours contenir protections + options on/off + chrono (pour les futurs
outils de suivi : isoler un test, desactiver une fonction ou un workflow),
(3) comprendre pourquoi les agents creent leurs scripts temporaires a la racine.

**Reponse question 1 (factuelle)** : c etait NOTRE protocole qui le prescrivait !
La section Commandes spawn_agents (v0.2.0) encourageait l ecriture a la racine
alors que la section originelle l interdisait : contradiction interne. Clarifie
en v0.2.2 par la section DEUX USAGES DISTINCTS : script jetable ephemere
(write_file racine + rm -f immediat dans la meme commande, 0 residu, jamais
declare) vs outil temporaire de mission (generateur + dossier dedie +
declaration registre). La racine ne doit JAMAIS contenir de .tmp-* residuel
(test-024), mais le jetable ephemere n existe plus au moment des controles.

**Changements** :
1. template-test.md v0.2.1 -> v0.3.0 : options on/off (--no-chrono, --isoler N,
   --desactiver 1,3,5) + chrono par etape (chrono_etape, bilan_chrono,
   point_actif) dans la structure et le canevas. Tests EXISTANTS non migres.
   Correction OUTIL_MD manquant dans le canevas (bug latent).
2. protocole-tests v0.3.0 -> v0.3.1 : REGLE IMMUABLE triplet (table protections
   / options on/off / chrono) + reference template v0.3.0+.
3. protocole-outils : Regle 9 (IMMUABLE) -- protections + options on/off + chrono
   pour tout outil.
4. outil-template-python.md v0.1.0-beta -> v0.1.1-beta : option standard
   --chrono + REGLE IMMUABLE triplet.
5. outil-template.py : bloc REGLE IMMUABLE triplet + option --chrono dans
   construire_parser (compile OK).
6. protocole-creation-scripts-temporaires v0.2.1 -> v0.2.2 : section DEUX
   USAGES DISTINCTS (levement de la contradiction racine) + formulations
   nuancees (Objectif, etape 3, piege 1).
7. index-regles-general : description protocole-tests enrichie.

**Lecons** :
- Un protocole qui se contredit est pire qu un protocole muet : les agents
  suivent la section la plus facile (la racine). La clarification doit etre
  explicite, pas implicite.
- Le triplet protections/options/chrono se propage par les TEMPLATES (test +
  outil) : modifier la reference amont suffit, les fichiers existants restent
  valides (decision utilisateur : pas de migration).
- Le chrono dans le template cree la matiere premiere des futurs outils de
  suivi : sans mesure, pas d amelioration ciblee (lecon du round performance).

**Fichiers modifies (7)** : template-test.md, protocole-tests v0.3.1,
protocole-outils (Regle 9), outil-template-python.md, outil-template.py,
protocole-creation-scripts-temporaires v0.2.2, index-regles-general.md.
Normes ASCII/LF : 0/0. Test-029 a ADAPTER par Morpheus (template 0.2.1 -> 0.3.0).
## [LECON] 2026-08-13 -- REGLE STRICTE SCRIPTS DEDIES + POINT DE BASCULE IDENTIFIE (Buffy)

**Contexte** : demande utilisateur - les .tmp continuaient d etre crees a la
racine. Question : pourquoi la regle du dossier temporaire dedie (creer le
dossier, les fichiers dedans, supprimer a la fin) a change, et ou ?

**Reponse factuelle (point de bascule)** :
- v0.1.0 (2026-08-11, Promethee) : regle d origine - JAMAIS de script jetable
  a la racine, toujours generateurs-outil-temporaire (dossier dedie) +
  suppression en fin de mission.
- v0.2.0 (2026-08-13 20:44, mission anti-echappement JSON spawn_agents) :
  la methode documentee fut write_file -> .tmp-xxx.py puis python3 + rm -f
  dans la meme commande. Or write_file ecrit a la RACINE : la methode a
  naturalise les .tmp-*.py a la racine, en contradiction silencieuse avec
  v0.1.0. C EST LE POINT DE BASCULE.
- v0.2.2 (2026-08-13 21:18, mission triple) : la section DEUX USAGES
  DISTINCTS a officialise la tolerance (racine autorisee si rm -f immediat) -
  aveu : c est moi (Buffy) qui ai ecrit cette tolerance.
- v0.2.3 (2026-08-13 21:34, cette mission) : REGLE STRICTE RESTAUREE.

**Changements v0.2.3** : 11 zones corrigees (intro, Objectif, etape 3,
section Deux usages distincts, section spawn_agents ECRIRE/EXECUTER/VERIFIER,
procedure valide, piege test-024, piege script a la racine, piege residu,
RVAV) + .gitignore (.agents-tmp/). Dossier dedie .agents-tmp/ cree : invisible
pour test-024 (13/13 OK, scan racine uniquement), tous les scripts temporaires
y vivent (jetables ephemeres compris), vide en fin de mission.

**Lecons** :
- UNE TOLERANCE DOCUMENTEE DEVIENT UNE NORME : ecrire une exception dans un
  protocole (v0.2.2) garantit qu elle sera utilisee systematiquement. La
  regle stricte est le seul encadrement fiable.
- La methode anti-echappement (write_file + rm -f dans la meme commande)
  n imposait pas la racine : write_file accepte un chemin relatif. Le vrai
  oubli est de ne pas avoir ecrit .agents-tmp/ devant le nom du script des
  la v0.2.0.
- Revoir l historique AVANT de repondre : la question utilisateur a permis
  de dater le bascule a la minute pres (20:44 v0.2.0, 21:18 v0.2.2).
## [LECON] 2026-08-13 -- RETOUR A LA REGLE D ORIGINE DES SCRIPTS TEMPORAIRES (Buffy)

**Contexte** : l utilisateur a fait remarquer que les .tmp continuaient d etre
crees a la racine, puis a exige le RETOUR A LA REGLE D ORIGINE : l agent cree
SON dossier temporaire a la racine et le SUPPRIME en fin de mission. J avais
complique inutilement : v0.2.2 (tolerance ecrite du script jetable a la
racine) puis v0.2.3 (dossier permanent .agents-tmp/). La regle d origine etait
parfaite et je l avais remplacee par deux mecanismes plus complexes.

**Changements v0.2.4** : protocole reecrit en entier (0 mention .agents-tmp) :
dossier tmp-<agent>/ cree a la racine (mkdir), scripts jetables dedans
(write_file -> tmp-<agent>/<script>.py), SUPPRESSION COMPLETE en fin de
mission (rm -rf tmp-<agent>) : 0 dossier residuel, 0 script eparpille. Le nom
sans point (tmp-<agent>) est invisible pour test-024 (startswith .tmp-/.zz-).
.gitignore : tmp-*/ (retrait de .agents-tmp/). Dossier .agents-tmp/ supprime.
Residu tmp-cerberus (de ma propre recon) supprime - la regle s applique a moi
aussi.

**Lecons** :
- NE PAS REMPLACER UNE REGLE QUI FONCTIONNE : la regle d origine (dossier
  cree + supprime) etait simple, verifiable et comprise. Mes v0.2.2/v0.2.3
  ont resolu un probleme theorique (l auto-incrimination test-024) en creant
  un probleme reel (dossiers permanents, tolerances). Le retour a l origine
  est aussi un retour a la simplicite.
- Le garde-fou des dossiers residuels (adapte par Morpheus dans test-024 :
  aucun dossier tmp-* hors dossier de l agent courant) protegera la regle
  sans empecher la mission en cours.
- La pratique : mkdir tmp-<agent> des le premier script, rm -rf tmp-<agent>
  AVANT de reactiver l agent suivant.

## [LECON] 2026-08-13 -- AGENT HYGIE CREE DE BOUT EN BOUT (Buffy)

**Contexte** : demande utilisateur - creer un agent de nettoyage complet pour
tester en reel toute notre mise en place (regles, conventions, protocoles,
outils/combos). Decisions utilisateur : nom HYGIE, perimetre = TOUT le
workspace (seul habilite a supprimer sans demande, avec snapshot + tracabilite),
snapshots dans le dossier dedie de l agent avec rotation 7 jours.

**Livrables** :
- Dossier cerveau-projet/agents/hygie/ : fiche CONFORME (noyau v0.3.0 +
  variante cerveau-projet), corrections.md, parcours v0.1.0 CONFORME
  (valider-case 0 erreur apres allegement de 4 indices > 160 car,
  valider-cartes-decision CONFORME, detecter-cablages-manquants PROPRE),
  snapshots/ avec README de rotation 7 jours.
- Chariot de nettoyage (3 outils au protocole 5 fichiers, catalogue 149->152) :
  detecter-residus (scan par zone cerveau-projet/workspace, --sans-cache),
  snapshot-nettoyage (creer/consulter/rotation/liste),
  combo-nettoyage-hygie (Pattern 3, combos-moteur).
- References : index-agents, regles-groupes-agents (groupe 2), variante
  famille, AGENTS.md table des agents, index-tools (166->170).
- Test reel : detecter-residus a DETECTE 2 vrais residus a la racine
  (rapport-detecter-decalages-catalogue-2026-08-12/13.md egare) - preuve
  vivante que Hygie a du travail reel.

**Lecon** : creer un agent de bout en bout, c est creer 3 choses qui doivent
etre CONFORMES des la naissance : la fiche (template), le parcours (spec
v0.6.2, patterns 4-5-6-7-8-12-13) et les outils (protocole 5 fichiers +
catalogue + index-tools). La validation se fait IMMEDIATEMENT apres chaque
creation (valider-case + valider-cartes + cablages + conformite fiche),
jamais en fin de mission. Un nouvel agent = nouvelles references partout
(index-agents, groupes, variante famille, AGENTS.md, catalogue choix agents,
README)."


## [LECON] 2026-08-13 -- WORKSPACE/ CREE + DETECTER-RESIDUS v0.1.2 (Buffy)

**Contexte** : demande utilisateur - creer le dossier workspace/ (futur) et
tester la compartimentation reelle du scan detecter-residus (mission activee
par Cerberus apres la creation de l agent Hygie).

**Ce qui a ete fait** :
1. Dossier `workspace/` cree (README.md) - futur espace separe du cerveau
2. Compartimentation stricte v0.1.1 : la zone workspace ne penetre JAMAIS
   dans cerveau-projet/ (prune du walk) - les deux zones sont etanches
3. TEST REEL (residus factices poses dans les deux zones) : chaque zone ne
   voit que SES residus, --tous voit les deux sans chevauchement

**2 bugs decouverts par le test reel et corriges (v0.1.2)** :
- CLASSIFICATION : est_rapport_egare testait le PREMIER segment du chemin
  (toujours "cerveau-projet") au lieu du DOSSIER PARENT IMMEDIAT -> les 171
  rapports legitimes des agents (agents/*/rapports/, agents/*/controles/)
  etaient classes a tort en RAPPORT_EGARE. Corrige : parent immediat
  (rapports/controles/rapport/controle) = legitime.
- DOUBLE COMPTAGE : les fichiers de la racine (zone workspace) etaient
  traites 2 fois (niveau racine + os.walk) -> deduplication par chemin.

**Lecons** :
- Un test reel vaut mieux que 100 lectures : le test de compartimentation a
  revele 2 bugs invisibles a la lecture du code.
- Un outil de detection doit etre valide par des RESIDUS FACTICES poses et
  retires, pas seulement par le scan de l etat courant.

**Residus reels restants pour Hygie** (non supprimes, Hygie est le seul
habilite) : 2 rapports-detecter-decalages egare a la racine, 3 rapport-impact
dans verifier-conformite-fiche/, 8 fichiers .bak dans le cerveau.


## [LECON] 2026-08-13 -- WORKSPACE/ AJOUTE AU .GITIGNORE (Buffy)

**Contexte** : demande utilisateur - ajouter workspace/ au .gitignore pour
que les futurs travaux temporaires du dossier workspace (futur espace de
travail separe) ne polluent pas git.

**Ce qui a ete fait** : ajout du pattern au .gitignore racine :
- `workspace/*` : ignore TOUT le contenu du dossier (fichiers + sous-dossiers)
- `!workspace/README.md` : le README du dossier reste VERSIONNE (documentation)

**Preuves reelles** (git check-ignore) :
- workspace/.tmp-test.md -> IGNORE
- workspace/dossier/x.txt -> IGNORE
- workspace/README.md -> NON ignore
- git add --dry-run workspace/README.md -> add 'workspace/README.md'
- tmp-*/ inchange (toujours ignore), temps-reference.json inchange

**Lecons** :
1. Le pattern `dir/*` + `!dir/README.md` est le standard pour "dossier de
   travail ignore sauf sa documentation" : la regle d exception doit venir
   APRES la regle d exclusion (l ordre compte dans .gitignore).
2. Verifier TOUJOURS par git check-ignore apres une modification du
   .gitignore : c est la preuve que le pattern fait ce qu on attend.
3. Aucun test de non-regression ne couvre le .gitignore : si on veut une
   protection durable, un garde-fou pourrait verifier que workspace/ est
   ignore et que README.md ne l est pas.


## [LECON] 2026-08-14 -- TEST-035 REVERDI : CARTE JANUS v0.4.3 + RETRAITS REGISTRE (Buffy)

**Contexte** : reverdir test-035-evaluer-processus (serie e 16/17). Vulcain a corrige les 2 bugs de l outil (v0.1.1). Restaient 4 ecarts : retrait d entree registre erronee morpheus + ajout de 3 outils a la carte de janus.

**T1 - Retrait registre** : entree erronee 'morpheus/tester-lancer-non-regression' retiree (seul Janus lance la non-regression, regle utilisateur). J ai aussi retire l usage 'vulcain/tester-lancer-non-regression' (meme regle - Vulcain n a pas a lancer la non-regression). Lecons : un agent ne doit JAMAIS enregistrer un usage de tester-lancer-non-regression sauf Janus.

**T2 - Carte janus v0.4.2 -> v0.4.3** : ajout de 3 indices outil a la case c21 (Verifier les impacts) : detecter-residus, detecter-divergences-version, evaluer-processus (outils que Janus utilise reellement dans ses controles - prouve par le registre). Bump fiche (PARCOURS v0.4.3) + FINS REELLES mise a jour (bloc stale v0.3.8 -> v0.4.3, 11 fins).

**Verifications** : valider-cartes-decision --agent janus CONFORME, evaluer-processus --tous 0 probleme, test-035 8/8, serie e complete 17/17 (0 KO). Normes 0/0 partout.

**Lecon** : quand un agent utilise reellement un outil (prouve au registre), la carte DOIT etre mise a jour pour le legitimer - sinon chaque usage ressort OUTIL_HORS_CARTE et pollue les garde-fous. Et une entree registre erronee (outil utilise hors regle) doit etre RETIREE, pas contournee.

## [LECON] 2026-08-14 -- REVERDIR TEST-035 : OUTIL REEL UTILISE = OUTIL DANS LA CARTE (Buffy)

**Contexte** : mission Cerberus (reverdir test-035) - apres correction carte janus + retrait
registre, mon propre usage de 'valider-cartes-decision' au registre ressortait en
OUTIL_HORS_CARTE (absent de MA carte).

**Lecon** : quand un outil est reellement utilise, la bonne correction est de l AJOUTER a
la carte (pas de retirer l usage du registre). Ajout de valider-cartes-decision a la case
c14 (controle RVAV) de ma carte + bump 0.4.2 -> 0.4.3 (Pattern 14 : fiche synchronisee,
FINS REELLES v0.3.8) + adaptation test-016 (version 0.4.3, serie b) car il verifiait la
version en dur. De plus : le chemin du dossier test-035 est 'test-035-evaluer-processus'
(pas test-035-processus-cartes-registre) - bien verifier le nom reel du dossier test.

**Verifications** : evaluer-processus 0 probleme, test-035 8/8, test-016 20/20,
valider-cartes buffy CONFORME, normes 0/0, registre 20 lignes (seuls les usages janus
de tester-lancer-non-regression restent - legitimes).

## [LECON] 2026-08-14 -- COMPLEMENT : VALIDER-CARTES-DECISION DANS LA CARTE JANUS (Buffy)

**Contexte** : le controle croise de Janus (reverdissement test-035) a declare son usage
de valider-cartes-decision au registre, mais cet outil etait ABSENT de la carte janus -
ce qui aurait cree un OUTIL_HORS_CARTE au test suivant.

**Lecon** : Janus est LE controleur croise : il valide les cartes des autres agents a
CHAQUE mission. valider-cartes-decision est un outil CENTRAL de son role et doit etre
dans sa carte (case c21, avec detecter-residus, detecter-divergences-version,
evaluer-processus). Bump carte janus 0.4.3 -> 0.4.4 + fiche synchronisee (Pattern 14).

**Verifications** : valider-cartes janus CONFORME (fiche == parcours 0.4.4),
evaluer-processus 0 probleme (usages janus couverts), test-035 8/8, normes 0/0.

## [LECON] 2026-08-14 -- OUTILLAGE DOUBLE README (PUBLIC + DEV) (Buffy)

**Contexte** : demande utilisateur - scinder le README en 2 : README.md (racine) =
GRAND PUBLIC (titres revus, SANS structure ni detail technique) et
cerveau-projet/readme-dev.md = DEVELOPPEURS (detaile, base uniquement sur les
sources de verite). Le brouillon readme-dev.md (consignes utilisateur) est remplace
par un vrai README dev. Ajout d une section AMELIORATION visible dans le README
public, reliee a la branche ameliorer de la carte Cerberus.

**Outillage realise (Buffy - le contenu sera rempli par Clio)** :
1. TEMPLATE : creation de cerveau-projet/agents/readme-dev-template.md (structure
   developpeur : demarrage session, identification LLM, multi-session, agents,
   outils, combos, cartes/parcours/indices, RVAV, tests + protections,
   auto-amelioration, sources de verite). ASCII strict + LF.
2. PARCOURS CLIO 0.5.4 -> 0.5.5 : branche 'readme-dev' dans c1 -> nouvelle case
   c20 (remplir readme-dev.md depuis le template, sources de verite uniquement,
   ASCII) qui rejoint c10 (flux lecons/retour). Fiche clio mise a jour (Pattern 14).
3. CARTE CERBERUS 0.4.3 -> 0.4.4 : indice regle ajoute dans c1b (branche
   ameliorer) qui reference la SECTION AMELIORATION du README public et le flux
   de mise a jour par Clio. Fiche cerberus mise a jour (Pattern 14).

**IMPACTS TESTS (documentes pour Morpheus, non modifies par moi)** :
- test-013-cerberus-migration : version carte cerberus en dur 0.4.3 -> 0.4.4
  (KO version seule ; compteurs 23/5/5/3 inchanges -> pas d autre impact)
- test-020-combos-clio : NON impacte (combos non touches)
- test-038-badge-readme : NON impacte (badges inchanges tant que Clio ne refond
  pas le README public - attention aux badges Outils-N/Version/Statut a la refonte)
- test-039-residus-version-racine : NON impacte

**SUITE** : Clio remplira les 2 README (branche readme-dev + combo massif pour le
public), puis Morpheus adaptera test-013, puis Janus controlera.

## [LECON] 2026-08-14 -- REGLE POIDS DES CASES (valider-case v1.1.1) (Buffy)

**Contexte** : mes ajouts d indices dans les cartes (cerberus c1b, clio c20) ont fait
echouer valider-case : verdict A ALLEGER.

**REGLE APPRISE (budget par CASE, pas par indice)** :
- Budget : 3.0 unites par case
- Ponderation : indice court (texte <= 100 car) = 0,5 unite ; long (> 100 car) = 1,0 ;
  outil/fichier/ref sans texte = 0,5
- Un indice ne doit JAMAIS depasser 160 caracteres
- Corriger = court-circuiter : 1 regle courte (<= 100 car) + references, jamais 2
  indices longs ajoutes a une case deja fournie (ex c1b avait 2.0 -> 2.5 OK, c20
  a ete reduite de 4.0 a 3.0)

**Application** : a chaque modification de carte, verifier valider-case (--dry-run)
et le poids des cases modifiees AVANT de considerer la carte valide.

**Etat final** : cerberus c1b (2.5) et clio c20 (3.0) CONFORMES, version cerberus
0.4.4 conservee (indice toujours present, plus court), clio 0.5.5 conservee.


## [LECON] 2026-08-14 -- CAUSE RACINE CLASSEUR ABSENT DU README (Buffy)

**Contexte** : l utilisateur a remarque que la section Classeur a ete oubliee dans le README public. Diagnostic Cerberus : le README public n avait aucune section Classeur, et le combo massif (lance par test-020) reinjectait 5 lignes CASSEES dans la table des agents (format 3 colonnes dans un tableau 2 colonnes) pour les pseudo-agents Classeur-variables, Conventions, Philosophie, Regles-immuables, Traces avec 'Selon sa carte de decision'.

**Cause racine (2 outils)** :
1. mettre-a-jour-readme.py : les fonctions lister_agents_reels() ET compter_agents() listent TOUS les dossiers de agents/ sauf tools -> 17 dossiers au lieu des 12 vrais agents. La ligne 274 ecrivait la ligne 'Selon sa carte de decision' pour chaque pseudo-agent.
2. combos-analyse-projet.py : comptage agents avec le meme critere (tous les dossiers sauf tools) -> 17.

**Correction** : critere fiable = un agent d action a un parcours JSON agents/<nom>/parcours/parcours-<nom>.json. Les 5 dossiers concepts (classeur-variables, conventions, philosophie, regles-immuables, traces) n ont pas de parcours -> exclus. Applique dans les 2 outils, versions py + sh + md. Resultat : les 2 outils affichent Agents reels : 12. Preuve : test-020 a relance le combo massif et AUCUNE nouvelle ligne n a ete reinjectee (le README est passe de 5 a 5 lignes, pas plus).

**Lecon** : quand un outil liste ou compte des 'agents', il doit utiliser le critere du PARCOURS JSON (source de verite structurelle), pas la simple presence d un dossier. Les dossiers de concepts ne sont pas des agents d action.

**Impacts documentes** : test-020 verifie 'combos-analyse-projet 0.1.0' en dur -> KO attendu (version 0.1.1) -> Morpheus adaptera. Clio retirera les 5 lignes cassees du README public et ajoutera la vraie section Classeur.
## [LECON] 2026-08-14 -- CREATION DE L AGENT HERMES (Buffy)

**Contexte** : decision utilisateur -- creer un agent dedie au vocabulaire et
aux fautes d orthographe (dieu grec de l eloquence : Hermes), suite a la faute
`enchannements` trouvee dans readme-dev:264.

**Livrables** :
- Agent Hermes complet : fiche (template noyau v0.3.0 + variante cerveau-projet,
  role_specifique langue), corrections.md, parcours 24 cases (v0.1.0, fin
  Activer Janus), registration activer-agent-principal (.py + .sh)
- Outil `detecter-fautes-orthographe` v0.1.0 : dictionnaire de fautes
  francaises courantes en ASCII + --tous/--fichier/--rapport/--verbose/--tout
- Catalogue 152 -> 153 (trie), index-tools (Detecter 12 -> 13, Total 170 -> 171)
- Premiere mission reelle : readme-dev:264 `enchannements` -> `enchainements`
- Mission UTF-8 : 19 headers .py + 2 headers .sh `coding: utf-8` ->
  `coding: ascii` (contenu verifie pur ASCII avant correction)

**Lecons** :
1. PATRON DE CREATION D AGENT : suivre Hygie exactement -- fiche (frontmatter
   identite/agent/profil/config/surcharges) + parcours JSON avec cle
   `parcours` + `identite` (les oublier casse valider-cartes) + fin Activer
   Janus + registration dans activer-agent-principal (.py AGENTS dict + .sh 3
   blocs case).
2. PIEGE ECRITURE PYTHON SUR WINDOWS : `io.open(f, 'w')` convertit les LF en
   CRLF. Apres TOUTE ecriture Python, repasser corriger-fins-de-ligne sur les
   fichiers ecrits (verifier avec count(b'\r\n')).
3. LE DICTIONNAIRE DE FAUTES ne doit contenir QUE des vraies fautes : une
   entree avec fautif == correct cree des faux positifs. Le francais ASCII
   correct (probleme, etre, deja, parallele) ne doit jamais etre signale.
4. MOT ANGLAIS LEGITIME : verifier le contexte (ex: `success` dans les badges
   GitHub n est pas une faute francaise).
5. SCAN --tous : parcourir la racine UNE fois (pas `.` + `cerveau-projet` en
   double), exclure tmp-*/workspace/.
6. IMPACTS TESTS ATTENDUS pour Morpheus : test-007 (catalogue 152 -> 153),
   test-018 (12 parcours -> 13), test-004/005/016 (si versions touchees).
7. Le fichier des agents dans AGENTS.md doit etre mis a jour (liste des agents)
   par le mecanisme habituel (Clio/README + index).


## [LECON] 2026-08-14 -- GARDE-FOU ANTI-DERIVE CERBERUS (Buffy)

**Contexte** : derive constatee le 2026-08-14 - Cerberus a execute SEUL 19
taches (verifications, corrections, garde-fous, outils) au lieu d activer
l agent habilite, alors que 7 jours de chaines Cerberus->Agent->Cerberus
avaient bien fonctionne. Cause racine : les demandes de type verification
semblent petites -> traitees seul -> personne ne controle (boucle de controle
externe disparue).

**Correction (mission Cerberus -> Buffy)** :
1. parcours-cerberus.json v0.4.4 -> v0.4.5 : indice GARDE-FOU C1 ajoute dans
   la case c1 (Mission) : 'TOUTE tache d execution (verifier, corriger, creer,
   modifier, tester) -> activer l agent habilite. Jamais executer seul.'
   (135 car, sous la limite 160). Les 5 branches existantes de c1 intactes.
2. fiche cerberus.md synchronisee (Pattern 14) : REGLE ABSOLUE PARCOURS
   v0.4.5 + bloc FINS REELLES v0.4.5 (fins reelles c19e/c20/c23 verifiees
   conformes a la carte).

**Validations** : valider-case CONFORME (indice 135 car), valider-cartes
CONFORME (fiche == parcours 0.4.5), verifier-conformite-fiche CONFORME,
evaluer-processus cerberus 0 probleme, normes 0 non-ascii / 0 CRLF.

**Impact tests (a adapter par Morpheus)** : test-013-cerberus-migration
(version 0.4.4 en dur -> 0.4.5). NE PAS toucher aux tests (domaine Morpheus).

**Regle durable** : toute demande de verification/correction/audit declenche
l activation de l agent dont c est le role - jamais une tache de Cerberus.

## [LECON] 2026-08-15 -- ECART CARTE VULCAIN CORRIGE : INDICE OUTIL outil-template EN c4 (Buffy)

**Contexte** : la chaine doc-obligatoire (Vulcain -> Morpheus -> Janus) a signale un ecart
de carte : la carte vulcain contient la REGLE c4 (ETAPE 3 OBLIGATOIRE : j utilise TOUJOURS
outil-template) mais PAS d indice outil outil-template -> evaluer-processus signalait
OUTIL_HORS_CARTE chaque fois que vulcain declaraient un usage de outil-template.

**Correction** : ajout de l indice outil outil-template dans les indices de la case c4 du
parcours-vulcain (format identique aux autres indices outil), bump 0.4.7 -> 0.4.8, fiche
vulcain.md mise a jour (Pattern 14 : version parcours 0.4.8).

**Verifications** : valider-cartes-decision --agent vulcain CONFORME (fiche 0.4.8 ==
parcours 0.4.8), evaluer-processus --agent vulcain 0 probleme, preuve positive reelle
(declaration d usage vulcain outil-template acceptee : plus d OUTIL_HORS_CARTE),
valider-cartes --tous 13/13 CONFORMES.

**Lecons** :
1. Toute REGLE de carte qui mentionne un outil doit avoir l indice outil correspondant,
   sinon evaluer-processus signale OUTIL_HORS_CARTE a chaque usage declare. Une regle
   sans indice outil est une carte incomplete (verifier la coherence regle/indices a la
   creation d une regle).
2. LA FIN SUIT SA CARTE : la mission recue disait "reactiver Cerberus" mais MA carte
   Buffy (c8/c22/c27) impose ACTIVER JANUS en fin de mission. La carte est la source de
   verite : j ai corrige la raison d activation dans AGENTS.md et AGENTS-historique.md
   pour la rendre conforme, puis j ai active JANUS pour le second controle.

## [LECON] 2026-08-15 -- 6 ECARTS REGLE/INDICE OUTIL CORRIGES SUR 4 CARTES (Buffy)

**Contexte** : le garde-fou test-055 (Morpheus) a detecte 6 incoherences regle/indice
outil (outil mentionne dans une regle sans indice outil dans la meme case) sur 4 cartes.

**Corrections** (edition JSON sure avec backup, format identique aux autres indices) :
- buffy c10c : + indice outil generateurs-case (parcours 0.4.3 -> 0.4.4)
- clio c20 : + indice outil valider-conformite-ascii (parcours 0.5.5 -> 0.5.6)
- janus c16 : + indice outil changer-statut (parcours 0.4.4 -> 0.4.5)
- vulcain c2 : + indice outil verifier-systeme ; c7 : + corriger-symboles (script reel
  corriger-accents-zones-sensibles) + combos-moteur (parcours 0.4.8 -> 0.4.9)
Fiches mises a jour (Pattern 14) : buffy/clio/janus/vulcain.

**Verifications** : valider-cartes-decision CONFORME x4 + --tous 13/13 CONFORMES,
evaluer-processus global 0 probleme, test-055 9/9 (garde-fou reverdi), normes ASCII/LF
0/0 sur parcours + fiches, 0 .bak residuel.

**Lecon** : la decouverte corriger-symboles (commande du catalogue dont le script reel
est corriger-accents-zones-sensibles) montre que le CHEMIN d un indice outil doit
pointer vers le script REEL de la commande, pas vers un nom suppose : quand le nom de
commande differe du dossier, verifier le champ "script" du catalogue. A NOTER POUR
CERBERUS : le test-016 (migration buffy) fige la version 0.4.3 du parcours buffy ->
mon bump 0.4.4 le rend KO attendu, adaptation par Morpheus.


## [LECON] 2026-08-15 -- BRANCHER LE BUMPER DANS LA CARTE VULCAIN (Buffy)

**Contexte** : demande utilisateur - brancher le bumper (mettre-a-jour-versions) dans les cartes des agents : case de bump systematique apres chaque modification d outil.

**Analyse Cerberus** : seul VULCAIN modifie des outils (construction c6->c9 et modification c12->c15). Buffy delegue les outils via c31, Morpheus ne fait que les tests, Themis audite. Donc la carte cible est vulcain (2 chemins).

**Actions realisees** :
1. Inserer dans parcours-vulcain.json (v0.4.9 -> v0.4.10) via editer-parcours :
   - c6a 'Bumper l outil (mettre-a-jour-versions)' entre c6 et c6b (c6.suivant=c6a, c6a.suivant=c6b) - chemin construction
   - c12a idem entre c12 et c12b (c12.suivant=c12a, c12a.suivant=c12b) - chemin modification
   Chaque case porte l indice outil mettre-a-jour-versions (catalogue + chemin + nom + type) + indice regle BUMP SYSTEMATIQUE.
2. Fiche vulcain.md : PARCOURS (v0.4.10) - bloc FINS REELLES inchange (aucune fin ajoutee).

**Validations** : valider-cartes-decision vulcain CONFORME, detecter-cablages 0 probleme (57 cases, 57 atteignables), test-055 12/12 (coherence regle/indice outil), test-026 10/10, navigation reelle c6 -> c6a (case Bumper affichee), normes 0/0 ASCII + LF.

**Lecon** : editer-parcours n accepte qu UN SEUL --inserer-case par appel (le dernier ecrase le premier si on en met 2 dans la meme commande) - il faut 2 appels separes (insertion + re-pointage). Le titre d une case qui contient un nom d outil du catalogue DOIT avoir l indice outil correspondant (garde-fou test-055) - verifie avant de nommer une case.


## [LECON] 2026-08-15 -- ECART CARTES DETECTER-CABLAGES-MANQUANTS CORRIGE (Buffy)

**Contexte** : KO preexistant test-035 - buffy et janus avaient declare 'detecter-cablages-manquants' au registre (usages legitimes de controle pendant la mission bumper cartes) mais l outil etait ABSENT des indices outil de leurs cartes.

**Actions** :
1. Carte buffy : indice outil detecter-cablages-manquants ajoute a c10 'Verifier les dependances' (le bon endroit : apres modification d un parcours on verifie les dependances/cablages). PAS a c14 (RVAV) : c14 avait deja 3 indices et la case verifie surtout ASCII/cartes - le deplacer a c10 evite de depasser le budget d indices.
2. Carte janus : indice ajoute a c33 'Verifier l etat des fichiers agents' (controle des parcours).
3. Bump des versions avec l OUTIL bumper (mettre-a-jour-versions --parcours <agent> --wet) : buffy 0.4.4 -> 0.4.5, janus 0.4.5 -> 0.4.6 (parcours + fiche en un seul passage, verification post-bump OK).

**Validations** : valider-cartes buffy + janus CONFORMES, cablages 2 parcours PROPRE, test-035 8/8 (0 probleme de processus), test-055 12/12, normes 0/0 ASCII + LF, test-016 : 1 seul KO restant = VERSION (0.4.4 -> 0.4.5) a adapter par Morpheus (le point 10 'plus de 3 indices' passe car c14 est revenu a 3).

**Lecon** : (1) quand on ajoute un outil de controle a une carte, choisir la case de VERIFICATION DES DEPENDANCES (c10) plutot que la case RVAV finale (c14) qui a deja son budget d indices ; (2) le bumper fait parcours + fiche d un coup (aucune spec oubliee) ; (3) verifier test-016 apres bump d une carte (il fige la version).


## [LECON] 2026-08-15 -- ASSIGNATION BUMPER + EVALUER-PROCESSUS A MA CARTE (Buffy)

**Contexte** : test-035 KO - j avais declare au registre 2 usages REELS (mettre-a-jour-versions pour bumper, evaluer-processus pour le scan global) sans que ces outils soient dans MA carte -> OUTIL_HORS_CARTE.

**Actions** : indice outil mettre-a-jour-versions ajoute a c10b (parcours a modifier : apres editer-parcours, bumper le parcours) + indice evaluer-processus ajoute a c26 (Passer par RVAV). Version 0.4.5 -> 0.4.6 avec le bumper (parcours + fiche d un coup).

**Validations** : valider-cartes buffy CONFORME, test-035 8/8 (0 probleme de processus), test-055 12/12, normes 0/0. test-016 : 1 seul KO = version (0.4.4 -> 0.4.6) a adapter par Morpheus.

**Lecon** : quand un nouvel outil est branche dans le systeme (le bumper), il faut l assigner a TOUTES les cartes des agents qui l utilisent reellement (vulcain pour construire, MAIS AUSSI buffy qui modifie des parcours/fiches). La carte doit refleter les usages reels avant qu ils soient declares au registre, sinon evaluer-processus signale OUTIL_HORS_CARTE.


## [LECON] 2026-08-15 -- DETECTER-DIVERGENCES-VERSION ASSIGNE A LA CARTE VULCAIN (Buffy)

**Contexte** : test-035 KO - vulcain a declare detecter-divergences-version au registre (usage REEL de verification des versions apres la correction des 30 en-tetes par --tous) mais l outil etait ABSENT des indices outil de sa carte -> OUTIL_HORS_CARTE.

**Actions** : indice outil detecter-divergences-version ajoute a c7b 'RVAV avant activation' (carte vulcain, 2 -> 3 indices), bump 0.4.10 -> 0.4.11 avec le bumper (parcours + fiche d un coup).

**Validations** : valider-cartes vulcain CONFORME, test-035 8/8 (0 probleme de processus), test-055 12/12, test-013 22/22, test-016 20/20, normes 0/0.

**Lecon** : la verification des versions (detecter-divergences-version) est un outil naturel de la carte de VULCAIN (constructeur d outils qui bump des versions) - il doit etre assigne AVANT son premier usage declare au registre. Meme piege que le bumper : un outil utilise par un agent doit etre dans SA carte.


## [LECON] 2026-08-15 -- BUMPER JANUS + GENERATEURS-COMMANDE CARTE CERBERUS (Buffy)

**Contexte** : mission Cerberus - ajouter l outil mettre-a-jour-versions (bumper) a la carte janus
(usage reel Janus rescan --tous pendant son controle, KO test-035 OUTIL_HORS_CARTE).

**Travail effectue** :
1. Carte janus c33 (Verifier l etat des fichiers agents) : + indice outil mettre-a-jour-versions
   (commande --tous). Parcours janus 0.4.6 -> 0.4.7, fiche a jour (Pattern 14). CONFORME, cablages 50/50.
2. DECOUVERTE en route : mon activation via generateurs-commande a revele un 2e KO test-035 -
   Cerberus utilise generateurs-commande (Pattern 17 PASSE PAR LE GENERATEUR) mais l outil etait
   ABSENT de sa carte, et le generateur journalise le NOM DE COMMANDE (activer-activer) au lieu de
   son propre nom dans le registre. Corrections : + indice outil generateurs-commande a la carte
   cerberus c10 (Activer l agent), parcours cerberus 0.4.5 -> 0.4.6, fiche a jour. Entree registre
   cerberus corrigee (activer-activer -> generateurs-commande, veracite).
3. Garde-fous : test-035 reverdi 8/8, test-055 12/12, cablages PROPRE 13 parcours, normes 0/0.

**Lecon** : (a) quand un agent utilise un GENERATEUR (Pattern 17), l outil du generateur doit etre
dans SA carte (le generateur journalise le nom de COMMANDE du catalogue, pas le nom de l outil -
ecart de journalisation a transmettre a Vulcain pour ameliorer generateurs-commande) ; (b) chaque
activation par generateur peut creer une entree registre OUTIL_HORS_CARTE - verifier test-035 apres
toute activation.

**KO attendu transmis** : test-013 fige cerberus 0.4.5 -> a adapter par Morpheus (0.4.6).


## [LECON] 2026-08-15 -- CARTE MORPHEUS TESTER-PROTECTIONS + CARTE BUFFY GUIDER-PARCOURS (Buffy)

**Contexte** : mission Cerberus (bilan Janus) - KO test-035 restant : morpheus 'tester-protections'
absent de la carte (matcher exact d evaluer-processus vs pattern 'tester-protection-*').

**Travail effectue** :
1. Carte morpheus c12 (Completer et executer les tests de l outil) : + indice outil tester-protections
   (chemin tester/tester-protections/, catalogue tester-protections). Parcours morpheus 0.4.5 -> 0.4.6,
   fiche a jour (Pattern 14). CONFORME.
2. DECOUVERTE en route : mes propres usages Buffy de guider-parcours (P0 de MA fiche, ligne 167 :
   'Suivre MON parcours case par case') etaient absents de MA carte -> indice ajoute a ma case c0.
   Parcours buffy 0.4.6 -> 0.4.7, fiche a jour. CONFORME.
3. Le generateur a journalise UNE 3e entree cerberus 'activer-activer' lors de MON activation
   (bug de journalisation generateurs-commande : il journalise le NOM DE COMMANDE au lieu de son
   propre nom) -> entree corrigee vers generateurs-commande (veracite).

**Lecon** : (a) un outil utilise par un agent DOIT etre dans SA carte - verifier test-035 apres
chaque mission (les usages declares au registre creent des OUTIL_HORS_CARTE) ; (b) le bug de
journalisation de generateurs-commande se reproduit a CHAQUE activation (3 occurrences aujourd hui) -
correction a la racine necessaire par Vulcain : journaliser 'generateurs-commande' au lieu du nom
de commande du catalogue.

**KO attendus transmis a Morpheus** : test-016 fige buffy 0.4.6 (bump -> 0.4.7) ; test-004 fige
morpheus 0.4.5 (bump -> 0.4.6).


## [LECON] 2026-08-15 -- CARTE VULCAIN : 2 INDICES RVAV AJOUTES (Buffy)

**Contexte** : mission Cerberus (bilan Janus) - KO test-035 : Vulcain declare un usage REEL de
detecter-cablages-manquants et valider-cartes-decision (son RVAV) mais absents de sa carte.

**Travail effectue** : case c7b (RVAV avant activation) de la carte vulcain : + indices outil
detecter-cablages-manquants et valider-cartes-decision. Parcours vulcain 0.4.12 -> 0.4.13, fiche
a jour (Pattern 14). Verifications : test-035 8/8, test-055 12/12, carte CONFORME, cablages
PROPRE 13 parcours, normes 0/0.

**Lecon** : le RVAV d un agent utilise des outils de validation (valider-cartes-decision,
detecter-cablages-manquants) qui doivent etre dans SA carte des que declares au registre - le
garde-fou test-035 verifie le croisement registre/carte a chaque mission.


## [LECON] 2026-08-15 -- CARTE JANUS : TESTER-PROTECTIONS AJOUTE (Buffy)

**Contexte** : mission Cerberus (bilan Janus) - KO test-035 : Janus declare un usage REEL de
tester-protections (importe dans ses tests de controle) mais absent de sa carte.

**Travail effectue** : case c4 (Verifier les tests) de la carte janus : + indice outil
tester-protections. Parcours janus 0.4.7 -> 0.4.8, fiche a jour (Pattern 14). Verifications :
test-035 8/8, test-055 12/12, carte CONFORME, cablages 50/50, normes 0/0, aucun test ne fige janus.

**Lecon** : les protections importees (tester-protections) sont un outil comme les autres - tout
agent qui les importe dans ses tests de controle doit les avoir dans SA carte (garde-fou test-035).

## [LECON] 2026-08-15 -- CARTE VULCAIN c10 + DETECTER-RESIDUS (Buffy)

**Contexte** : mission .tmpignore - Vulcain a declare un usage reel de detecter-residus au registre (preuve derogation ciblee) mais l outil manquait a sa carte. Ajoute a c10 (Verifier le systeme - modification) + bump vulcain 0.4.14.

## [LECON] 2026-08-15 -- CARTE VULCAIN c7 + CORRIGER-FINS-DE-LIGNE (Buffy)

**Contexte** : mission protection LF - Vulcain a corrige des CRLF reintroduits avec corriger-fins-de-ligne (usage reel) mais l outil manquait a sa carte. Ajoute a c7 (Lancer le combo corriger-ascii) + bump vulcain 0.4.15.

## [LECON] 2026-08-15 -- CARTE VULCAIN +2 INDICES LF (Buffy)

**Contexte** : mission garantie LF - Vulcain a utilise combos-audit-general (preuve rapport LF) et executer-script-temporaire (preuve entonnoir) sans les avoir dans sa carte. Ajoutes : c13 + combos-audit-general, c18c + executer-script-temporaire. Bump vulcain 0.4.16.


## [LECON] 2026-08-15 -- INDICE ANTI-ARRET C0 MORPHEUS (Buffy)

**Contexte** : demande utilisateur - corriger le bug "Morpheus casse le round"
(diagnostic Janus : la mission confiee dans AGENTS.md n est pas relue au
demarrage du parcours, case c1 ouverte). Decision utilisateur : corriger
SEULEMENT la carte de Morpheus.

**Fait** :
1. Ajout d un indice 'regle' dans la case c0 de parcours-morpheus.json :
   "REGLE ANTI-ARRET : je lis MA Raison (mission confiee) dans AGENTS.md avant
   la case Mission." (91 car, COURT <= 100 -> budget pondere c0 = 1,0/3,0 OK)
2. Bump parcours 0.4.7 -> 0.4.8 + fiche morpheus.md synchronisee (Pattern 14,
   1 occurrence).
3. Validations : valider-cartes morpheus CONFORME, --tous 13/13, valider-case
   OK (seuls avertissements legitimes de boucles voulues c10b/c14b), cablages
   PROPRE 34/34, normes 0/0.

**Incident (transparence)** : la chaine s est encore brisee - Buffy activee
mais mission non executee (0 trace). Reprise par l agent actif (pattern des
rounds precedents) : c est le MEME bug d arret qui touche Morpheus, cette fois
applique a Buffy. Le garde-fou anti-arret ajoute a c0 de Morpheus devrait
reduire ce pattern pour Morpheus ; il faudra l etendre aux autres agents si le
bug persiste.

**Impact test (mission Morpheus, seul habilite)** : test-004-combos-tester-outil
point 7a fige la version parcours morpheus 0.4.7 -> KO constate (1 KO sur 10).
A adapter : 0.4.7 -> 0.4.8 (ligne 155 + docstring ligne 19). Les references
0.4.7 dans corrections.md sont de l historique (a conserver).

**Lecon** :
1. Bumper un parcours peut casser les tests qui figent sa version - toujours
   verifier les references dans les tests et documenter l impact pour Morpheus.
2. Le bug d arret (mission non relue au demarrage) touche TOUS les agents
   reactives, pas seulement Morpheus - le garde-fou c0 est le bon remede.

## [LECON] 2026-08-16 -- CORRECTION KO2 TEST-035 : INDICES MANQUANTS CARTE VULCAIN (Buffy)

**Contexte** : la non-regression (Janus) a bloque la barriere E : test-035 (evaluer-processus) signalait 2 OUTIL_HORS_CARTE pour vulcain : 'evaluer-rating' et 'tester-lancer-non-regression' declares au registre (2026-08-15 20:09 et 20:25) mais absents des indices de la carte vulcain (v0.4.17).

**Correction** (Buffy, seule habilitee a corriger les cartes) :
1. Ajout des 2 indices outil a la case c10 "Verifier le systeme (modification)" de parcours-vulcain.json (format modele : type/nom/catalogue/chemin), en plus de verifier-systeme/evaluer-processus/detecter-* existants.
2. Bump parcours 0.4.17 -> 0.4.18.
3. Fiche vulcain.md synchronisee (Pattern 14 : REGLE ABSOLUE PARCOURS + lien Parcours v0.4.18).

**Verifications** : JSON valide, evaluer-processus 0 probleme, valider-cartes --agent vulcain CONFORME, valider-cartes --tous 14/14, test-035 8/8, test-013 22/22, test-055 12/12, normes 0/0 ASCII + LF.

**Lecons** :
- Un usage registre sans indice carte = ecart detecte par evaluer-processus : quand un agent utilise un nouvel outil, la carte doit etre mise a jour (par Buffy) au meme round.
- La case "Verifier le systeme" (c10 vulcain) est le bon endroit pour les outils de verification/rating.
- valider-cartes --agent detecte l incoherence fiche/parcours (fiche v0.4.17 != parcours 0.4.18) : toujours synchroniser la fiche (Pattern 14) apres un bump de parcours.

## [LECON] 2026-08-16 -- CORRECTION CONFLIT TEST-037 : RETRAIT DECLARATION FALCATIVE + INDICE (Buffy)

**Contexte** : la relance 2 de non-regression (Janus) a franchi 4 barrieres (E, D, C, A) mais bloque sur la barriere B : test-037 KO sur 2 points - la carte vulcain contenait tester-lancer-non-regression ET le registre contenait la declaration fautive vulcain (2026-08-15 20:25:54).

**Cause racine** : MA correction KO2 (round precedent) etait TROP LARGE - j ai ajoute tester-lancer-non-regression a la carte vulcain pour satisfaire test-035 (usage registre dans la carte), mais cet outil est EXCLUSIF janus (verrou d habilitation) : vulcain ne l a JAMAIS reellement lance (l usage registre etait une declaration a tort pendant le developpement du mode profil).

**Correction** :
1. Registre : suppression de la ligne exacte vulcain/tester-lancer-non-regression (2026-08-15 20:25:54) - 116 -> 115 lignes.
2. Carte vulcain c10 : retrait de l indice tester-lancer-non-regression (10 -> 9 indices) - evaluer-rating conserve (legitime).

**Verifications** : test-037 6/6, test-035 8/8, evaluer-processus 0 probleme, valider-cartes --agent vulcain CONFORME, test-058 6/6, normes 0/0 ASCII + LF, 0 residu.

**Lecons** :
- Ne JAMAIS ajouter un outil EXCLUSIF a une carte pour satisfaire un test de coherence : l exclusivite (seul janus lance la non-regression) PRIME.
- Une declaration registre fautive (usage jamais reel) se RETIRE du registre - c est la regle 2b de test-037.
- La boucle d auto-correction doit verifier les GARDE-FOUS D EXCLUSIVITE (test-037, 058, 059...) avant de valider une correction de carte : satisfaire test-035 peut casser test-037.


## [LECON] 2026-08-16 -- RENFORCEMENT REGLES CERBERUS C1/C5/C18 (Buffy)

**Contexte** : l'enquete (derive Cerberus qui analyse lui-meme au lieu d'activer) a abouti a la decision utilisateur : GARDER combos-analyse-projet dans c10 mais RENFORCER les regles. Le blocage cartes-lock (divergent) avait ete corrige par Vulcain (proteger-modifier-marbre v0.1.1 + resync des 2 cartes).

**Correction (Buffy, via editer-parcours --modifier-case uniquement)** :
1. c1 : GARDE-FOU C1 renforce - VERIFICATION/AUDIT/ANALYSE -> branche AUTRE -> c18 -> c22 (Themis) ; Execution -> ACCUEIL -> c5 -> c6 ; JAMAIS analyser avant activer.
2. c5 : GARDE-FOU C5 - VERIF/AUDIT/ANALYSE -> Themis (c22) ; Execution -> activer la matrice ; aucune analyse avant activation.
3. c18 : question elargie aux VERIFICATIONS (croiser/verifier/comparer) + GARDE-FOU C18 - OUI -> c22 (Themis audite), NON -> c23, jamais d analyse par Cerberus.
4. Bump parcours 0.4.7 -> 0.4.8 + fiche cerberus Pattern 14 synchronisee.

**Verifications** : valider-case CONFORME (0 erreur, 0 a alleger - indices raccourcis sous 160 car apres 2e passe), valider-cartes --agent cerberus CONFORME, valider-cartes --tous 14/14, test-034 6/6, test-013 20/22 (KO version 0.4.7 en dur + verdict -> a adapter par Morpheus).

**Lecons** :
- Les indices regle des cartes doivent rester sous 160 caracteres (valider-case ALLEGER) : formuler concis des la 1re passe.
- Renforcer une carte = editer-parcours --modifier-case (jamais JSON direct), le lock se met a jour automatiquement depuis la correction Vulcain v0.1.1.
- Un bump de carte casse les tests qui pincent la version en dur : anticiper l adaptation Morpheus.


## [LECON] 2026-08-16 -- REGLE IMMUABLE RELEVE MEME ROUND GRAVEE (Buffy)

**Contexte** : demande utilisateur - les agents actives ne se declenchent plus dans le meme round (il faut relancer manuellement). L utilisateur veut une regle immuable : toute activation declenche l execution immediate dans le MEME ROUND.

**Proposition validee par l utilisateur (2 iterations)** :
- v1 rejetee : le cycle 'cerberus -> agent -> cerberus' est trompeur (les agents communiquent aussi entre eux).
- v2 validee : le cycle reel est `cerberus -> agents <-> agents <-> themis + janus -> cerberus` - Themis (audit) et Janus (controle) sont DANS le cycle, pas seulement Cerberus en bout de chaine.

**Gravure (porte du marbre)** :
1. Insertion de la section '### RELEVE MEME ROUND (IMMUABLE)' dans regles-groupes-agents.md apres LE MODELE DE CONFIANCE (via inserer-contenu-fichier + supprimer-ligne pour corriger un premier placement erronne).
2. Porte du marbre : proteger-modifier-marbre --zone regles-groupes-agents --autorisation UTILISATEUR -> empreinte bd98... -> 08c9... journalisee (21:59:09).
3. test-057 marbre 24/24 CONFORME (la zone gravee est verifiee par le garde-fou).

**Lecons** :
- Le cycle de releve n est PAS un aller-retour binaire : c est une CHAINE agents <-> agents avec Themis et Janus dans le cycle, seul le dernier maillon reactive Cerberus.
- Toute regle immuable gravee dans regles-groupes-agents.md passe par la porte du marbre (autorisation UTILISATEUR obligatoire) + test-057 verifie l integrite.
- Bien verifier l emplacement avant insertion : inserer-contenu-fichier --apres cible le motif, pas la fin d un bloc (corrige par supprimer-ligne + reinsertion).


## [NOTE] 2026-08-16 -- BRISURE DE CHAINE : DIAGNOSTIC + MISSION INTERROMPUE (Buffy)

**Situation** : mission Buffy 'eduquer Janus a la non-regression' activee par Cerberus, execution commencee (lecture fiche janus + options lanceur), puis INTERROMPUE par l utilisateur : 'le plus important, c est de revenir a cerberus et de reparer la chaine'.

**Diagnostic de la brisure (constat reel des rounds precedents)** :
- Chaque activation d agent (activer-agent-principal) est un appel d outil : apres l appel, le tour se termine et l agent active ne continue PAS automatiquement dans le meme round - l utilisateur doit relancer.
- La regle RELEVE MEME ROUND est gravee (marbre), mais le MECANISME d execution ne la suit pas encore : il manque le comportement 'apres avoir active, ENCHAINER immediatement en tant qu agent active' (activation + execution dans le MEME message).
- Dans les rounds reussis, le pattern etait : Cerberus active -> puis CONTINUATION dans le meme tour (l agent devient actif et execute). Ici, apres l activation de Buffy, le tour s est arrete avec un bilan au lieu d enchainer l execution.

**Cause racine** : la discipline de releve n est pas mecanisee dans le geste d activation lui-meme - l agent qui active doit SAVOIR qu il ne termine pas son tour : il devient l agent active et execute immediatement.

**Etat de la mission Buffy (a reprendre apres reparation)** : fiche janus lue (sections trouvees, insertion prevue apres ligne 185 'Pour terminer ma mission'), options du lanceur recoltees (--series, --profil, --fichiers, --desactiver, --activer, --etat-tests, barrieres, chrono, rating). Section 'UTILISATION DE tester-lancer-non-regression' A INSERER dans janus.md + verification carte janus (case c4 non-regression).


## [LECON] 2026-08-15 -- MECANISER LA RELEVE DANS LE PROTOCOLE-ACTIVATION (Buffy)

**Contexte** : derive recurrente - apres une activation, l agent active s arrete et l utilisateur doit relancer. Cerberus a decide (demande utilisateur) de mecaniser la releve dans le protocole-activation.

**Modifications** (protocole-activation.001.02.prepare.md) :
1. Regles d Or : ajout de la regle RELEVE MEME ROUND (IMMUABLE) - apres activation, l agent actif EXECUTE IMMEDIATEMENT dans le meme round.
2. Etape 5 : le point 4 precise que l activation EST l ordre d execution (jamais d arret, jamais de bilan intermediaire pour attendre l utilisateur).
3. Pieges Courants : ajout du piege 'S arreter apres une activation (brisure de chaine)' - l activation EST l ordre d execution.
4. Derniere mise a jour : 2026-08-15.

**Lecon** : la chaine se brise quand l agent produit un bilan intermediaire au lieu d executer. Le protocole grave maintenant le comportement : activation = ordre d execution, dans le meme round. Reference : regles-groupes-agents.md (RELEVE MEME ROUND, marbre).



## [LECON] 2026-08-15 -- EDUQUER JANUS A LA NON-REGRESSION (Buffy)

**Contexte** : la fiche janus.md ne contenait AUCUNE mention de tester-lancer-non-regression alors que Janus est le SEUL habilite a lancer la suite (regle immuable + verrou). Un outil ameliore ne sert a rien si son utilisateur exclusif ne sait pas l utiliser.

**Modification** : section 'UTILISATION DE tester-lancer-non-regression (MON OUTIL EXCLUSIF)' inseree dans janus.md apres la section activer-agent-principal : usage de base (--agent janus), mode BARRIERES (5 series par importance, 100% vert pour franchir), options essentielles (--series, --profil, --fichiers, --desactiver/--activer, --etat-tests, --parallele, --serial, --rapport, --timeout-test, --rebase-reference), reference de temps (chrono + seuil 25% + rating + tests lents), lecture du rapport en cas de KO (relancer la serie concernee avant la suite complete), journalisation registre-tests.jsonl. Correction mineure : ligne vide entre '## Forces et Faiblesses' et '## Style de travail'.

**Verifications** : verifier-conformite-fiche --agent janus = 1 CONFORME / 0 ECARTS, normes ASCII 0 + LF 0, 0 residu.



## [LECON] 2026-08-15 -- CREATION DE L AGENT ARGUS (Buffy, etape 1/3)

**Contexte** : demande utilisateur - creer l agent ARGUS (detecteur de contradictions dans les cases, les regles, les protocoles et l historique git). Decision utilisateur : nom Argus + suspendre le catalogue.

**Ce qui a ete fait** :
1. Fiche argus.md creee DEPUIS LE TEMPLATE fiche-agent-template.md (noyau v0.3.0 + variante cerveau-projet) - PAS depuis un autre agent (regle : le template est la reference, pas les fiches existantes). verifier-conformite-fiche --agent argus : 1 CONFORME / 0 ECARTS.
2. Parcours argus.json cree (22 cases) : c0/c0b/c0c communes, c1 Mission (auditer/git/autre), c2 AUDIT CONTRADICTIONS, c3 LECTURE GIT (lecture seule), c5 croisement double source, c6 classement gravite, c7 rapport, c8 controle (quel agent habilite corrige), cD1/cD2/cD3 RELAIS (Buffy/Vulcain/Morpheus), cR1 RETOUR, c13 FIN - Activer Janus, c29 hors parcours. valider-cartes --agent argus : CONFORME.
3. Roster regles-groupes-agents.md (groupe 2) + AGENTS.md (liste agents secondaires) : Argus ajoute.
4. Navigation reelle guider-parcours : c0 OUI -> c0c -> c1 -> c2 OK.

**A faire par la suite** :
- VULCAIN (etape 2) : creer l outil detecter-contradictions (reference dans le parcours c2/c3, INTROUVABLE actuellement) + lecture git en lecture seule + catalogue + index-tools.
- MORPHEUS (etape 3) : adapter les tests qui pincent le nombre d agents (test-037 11 agents, test-026 11 parcours, test-018 12 agents) + garde-fou.
- Le role Argus : DETECTE et SIGNALE, ne corrige JAMAIS (l agent habilite corrige).


## [LECON] 2026-08-15 -- REVITALISATION PURIFICATION RVAV (Buffy)

**Contexte** : decision utilisateur - le protocole rvav-workflow.md etait ABANDONNE et PERIME (etape 5 [purifier] orientee fichiers de contenu, jamais appliquee aux fichiers du cerveau). Constat : 40 fichiers en surcharge (janus/corrections.md 4736 lignes !).

**Audit des besoins reels** :
- corrections.md des agents : 14 a 275 lecons, ~17-21 lignes/lecon. Critiques : janus 4736, buffy 3421, vulcain 3328, morpheus 2826.
- AGENTS-historique.md : 150 entrees, 1565 lignes.
- Fiches agents (255-314) et protocoles (262-384) : structure template/documentaire, signaler seulement.

**Principe adopte (anti-perte)** : on ne supprime JAMAIS d information - les lecons sont la memoire des erreurs (anti-repetition). La purification DEPLACE les lecons/entrees les plus anciennes vers un fichier d archive cote a cote (<agent>-historique.md, AGENTS-historique-archive.md). Quotas : corrections.md 1000 lignes, AGENTS-historique.md 800.

**Livre** : protocole rvav-workflow.md etape 5 reecrite (quotas par type + procedure dry-run -> rapport -> validation -> execution + lien outil purifier-rvav) ; spec complete de l outil dans tmp-buffy/audit-purification-rvav.md (transmise a Vulcain).

**Lecon** : condenser-fichier (l outil existant) est un faux outil : lignes_apres == lignes_avant, il ne condense RIEN (copie + backup sans transformation). A remplacer/supprimer au profit de purifier-rvav.
## [LECON] 2026-08-16 -- ASSIGNATION PURIFIER-RVAV A HYGIE (Buffy)

**Contexte** : decision utilisateur - purifier-rvav est assigne a HYGIE SEULEMENT (c est son chariot de nettoyage). Clio mettra le README a jour ensuite.
**VERDICT** : VALIDE (carte hygie v0.1.1 CONFORME, valider-case 0 erreur, cablages PROPRE)

**Actions** : via editer-parcours (barrage n3) - insertion case c9b "Purifier les fichiers surcharges (RVAV)" (indice outil purifier-rvav + regle anti-perte), re-pointage c9.suivant -> c9b, bump 0.1.0 -> 0.1.1. Fiche hygie.md Pattern 14 synchronisee.

**Lecons** :
1. Le marbre ne verrouille que les cases de cerberus + constitution + regles-groupes - les autres cartes se modifient via editer-parcours sans porte.
2. editer-parcours re-empreinte cartes-lock.json automatiquement apres chaque ecriture legitime (verifie : lock mis a jour sans action manuelle).
3. L aide de editer-parcours (docstring) dit --vers mais le parser attend --cible pour --suivant - documenter l ecart.
4. Indice regle limite a 160 caracteres (valider-case A ALLEGER) : mon texte initial de 165 car a du etre raccourci.
## [LECON] 2026-08-16 -- INDICE COMBOS-ANALYSE-PROJET AJOUTE A LA CARTE CLIO (Buffy)

**Contexte** : KO test-035 (evaluer-processus) pendant la non-regression Janus - la declaration registre clio->combos-analyse-projet etait signalee OUTIL_HORS_CARTE : le combo de verification README n etait PAS dans les indices de la carte clio (seuls combos-moteur et combos-maj-readme-massive y etaient).
**VERDICT** : VALIDE (carte clio v0.5.7 CONFORME, evaluer-processus 0 probleme)

**Correction** : ajout de l indice outil combos-analyse-projet a la case c4 "Verifier l etat reel" (son role exact) via editer-parcours --modifier-case + bump clio 0.5.6 -> 0.5.7 + fiche Pattern 14.

**Lecons** :
1. Les 2 autres declarations fautives (buffy->valider-case, vulcain->combos-analyse-projet) ont ete retirees du registre : usages ponctuels de verification/modification, PAS des outils de role - ne pas les declarer.
2. Quand un agent utilise un outil de ROLE (recurrent), l outil DOIT etre dans sa carte (indice outil) - sinon test-035 KO. Le retrait de declaration masque l ecart ; l ajout d indice corrige la cause.

## [LECON] 2026-08-16 -- PROTOCOLE + PARCOURS ARGUS (Buffy)

**Contexte** : le re-test d Argus (v0.1.1) recommande de formaliser son fonctionnement : protocole de signalement en 4 elements + parcours type par cas.

**Livraisons** :
1. PROTOCOLE : protocole-argus-contradictions/001.01.ebauche.md (v0.1.0) : R1 les 4 elements OBLIGATOIRES d un signalement (type, gravite, fichier+ligne, 2 sources croisees), R2 JE DETECTE JE NE CORRIGE PAS + table des agents habilites (Buffy/Vulcain/Morpheus/Hygie), R3 cas types (--cases/--fichier/--regles/--git/--tous), R4 PREUVE NEGATIVE (copie + injection + --fichier quand soupcon malgre 0 contradiction), R5 cycle signalement -> activation agent habilite -> controle au retour -> Cerberus. Reference dans index-regles-general.md (apres protocole-fin-mission).
2. PARCOURS argus v0.1.0 -> v0.1.1 (via editer-parcours, barrage n 3 respecte) : case c30 enrichie (preuve negative --fichier avant de conclure "rien a signaler" : copie + injection + detection), case c7 enrichie (indice protocole-argus-contradictions R1 4 elements).
3. FICHE argus.md : version 0.1.1 (frontmatter + tableau + PARCOURS v0.1.1), protocole ajoute dans Protocoles applicables.

**Validations** : valider-cartes argus CONFORME, --tous 15/15, test-028 8/8, test-029 14/14, normes 0/0.

**Lecon** : un outil fonctionnel ne suffit pas - il faut son protocole d utilisation (quand/signaler comment) et son parcours a jour. Le rapport de comportement d un agent est la matiere premiere de ses protocoles.

## [LECON] 2026-08-16 -- OUBLI DE NETTOYAGE CORRIGE : PARCOURS ARGUS v0.1.3 (Buffy)

**Contexte** : verification Cerberus (demande utilisateur "argus va-t-il nettoyer ses tmp ?") : le parcours argus v0.1.1 que j avais livre avait UNE case qui CREE tmp-argus (c30 preuve negative) mais AUCUNE case de nettoyage en fin de mission. Morpheus/Vulcain/Buffy ont tous une case "FIN - Outil temporaire" (c16d/c18d/c35d) - Argus etait le seul sans.

**Correction** : via editer-parcours : insertion de la case c31 "NETTOYER tmp-argus (0 residu)" (indices : regle protocole-creation-scripts-temporaires + enregistrer-usage-outil --mode script-temporaire), re-pointage c30.suivant -> c31, cR1 OUI -> c31, c8 controle final -> c31, c31 -> c13, bump 0.1.1 -> 0.1.3. Fiche mise a jour (PARCOURS v0.1.3, Pattern 14). Verifie : valider-cartes argus CONFORME, --tous 15/15, 0 reference morte, normes 0/0.

**Incident technique** : le premier --inserer-case a echoue (JSON sans champ "id") MAIS les re-pointages vers c31 ont reussi -> 3 references mortes temporaires. Corrige en re-inserant c31 avec "id":"c31" (les re-pointages sont devenus valides). Lecon : TOUJOURS verifier l etat du parcours (refs mortes) APRES chaque operation editer-parcours, et verifier le format attendu (champ id) avant d inserer.

**Lecon principale** : quand une carte d agent a une case qui CREE des fichiers/dossiers temporaires, elle DOIT avoir la case de nettoyage correspondante avant la fin (regle anti-scripts 0 residu + test-024). A verifier pour chaque agent qui manipule des fichiers temp.

## [LECON] 2026-08-16 -- REGLE DE NETTOYAGE GRAVEE DANS LES TEMPLATES (Buffy)

**Contexte** : apres la correction de la carte argus (case c31 de nettoyage), verification Cerberus (demande utilisateur) : la regle de nettoyage existait dans protocole-creation-scripts-temporaires mais AUCUN template ne l imposait -> c est pourquoi l oubli a pu arriver.

**Corrections** :
1. fiche-agent-template.md : REGLE ABSOLUE 9 NETTOYAGE DES TEMPORAIRES (IMMUABLE) : toute case qui cree des fichiers/dossiers temporaires doit etre suivie d une case de nettoyage avant la fin (0 residu + declaration registre mode script-temporaire). Reference a la lecon argus.
2. template-test.md : point 12 NETTOYAGE DES PREUVES TEMPORAIRES (IMMUABLE) : toute preuve creee par un test (tmp-testNNN-) est SUPPRIMEE en fin de test (bloc finally), 0 residu (lecon test-051).
3. protocole-carte-decision : regle 7 CASE DE NETTOYAGE OBLIGATOIRE pour toute carte qui cree des fichiers temp.

**Validations** : test-029 14/14, test-044 15/15 (triplet intact), normes 0/0.

**Lecon** : une regle qui vit uniquement dans un protocole (qu on ne relit pas) ne protege pas : c est le TEMPLATE (relu a chaque creation) qui doit porter la regle. Regle de conception : toute contrainte de structure doit etre dans le template, pas seulement dans le protocole.
## [LECON] 2026-08-16 -- CORRECTION C29E ARGUS (AUTO-REACTIVATION) + SYNCHRO FICHE (Buffy)

**Contexte** : demande utilisateur de revoir les cases de fin d Argus qui stoppent le round. Le scan Cerberus de TOUTES les fins de TOUTES les cartes a trouve UN SEUL bug : argus c29e (FIN - Signaler le besoin) executait reactiver session-llm-1 '<raison>' argus = AUTO-REACTIVATION (boucle infinie qui stoppe le round) au lieu de reactiver cerberus. Cause : faute de frappe lors de la creation du parcours (le message disait 'signaler a Cerberus' mais la commande reactivait argus).

**Corrections** : 1) carte argus via editer-parcours (barrage n3) : c29e reactiver -> cerberus, bump v0.1.3 -> v0.1.4, 2) fiche argus.md : PARCOURS (v0.1.3) -> (v0.1.4) (Pattern 14).

**Validations** : valider-cartes argus CONFORME, normes 0/0, test-037 non impacte (liste d agents seulement), scan complet : aucune autre auto-reactivation dans les 15 cartes (les FIN - Delegation descriptives sont le modele standard - l agent active continue la chaine).

**Lecons** : 1) le message d une fin et sa commande doivent TOUJOURS viser le meme agent (le message disait Cerberus, la commande reactivait argus - incoherence interne), 2) apres correction de carte, verifier immediatement le Pattern 14 (valider-cartes signale fiche != parcours), 3) le scan des fins doit verifier la CIBLE de reactiver (pas seulement la presence du mot) - c est la que se cache l auto-reactivation.
## [LECON] 2026-08-16 -- LACUNES PARCOURS ARGUS CORRIGEES : DELEGATION AVEC RETOUR + INDICES OUTILS (Buffy)

**Contexte** : demande utilisateur - trouver les lacunes qui font qu Argus n est pas optimal vs les agents principaux (Buffy/Vulcain). Diagnostic Cerberus : 1) CRITIQUE - c29a (FIN - Delegation) etait une fin SANS CASE DE RETOUR : quand l agent delegue reactivait Argus avec son bilan, aucune case ne disait comment reprendre ; 2) carte courte (23 cases vs 57-63) ; 3) outils de validation presents en P0 mais absents des cases.

**Corrections** (parcours argus v0.1.4 -> v0.1.6, via editer-parcours barrage n3) :
1) c29a transformee de FIN en ACTION 'DELEGATION - Activer l agent habilite' avec suivant -> cR1 (la case RETOUR existante joue la reprise : verifier le rapport de l agent a la reactivation) - la boucle est bouclee : c29a -> cR1 -> c31 -> c13
2) indices ajoutes : c0 -> guider-parcours, c4 (controle RVAV) -> valider-cartes-decision + valider-conformite-ascii, c5 (croisement) -> valider-nommage
3) fiche argus.md synchronisee (Pattern 14 : v0.1.6)

**Validations** : valider-cartes argus CONFORME + --tous 15/15, test-055 12/12, test-069 8/8, normes 0/0, 11 outils uniques tous au catalogue (vs 7 avant).

**Lecons** : 1) une fin de delegation DOIT etre suivie d une case de reprise (soit une fin dediee c15e/c9e, soit une case RETOUR existante comme cR1) - sinon l agent delegue qui revient retombe au debut et le round derive ; 2) les outils de validation (valider-cartes-decision, valider-conformite-ascii, valider-nommage) doivent etre branches dans les CASES du parcours, pas seulement listes en P0 de la fiche - le parcours est la source de verite du guidage ; 3) verifier apres chaque modification : validateur + test-055 (coherence regle/indice) + test-069 (garde-fou outil).
## [LECON] 2026-08-16 -- GRAVER LA REGLE RELIRE SA FICHE AVANT MISSION (Buffy)

**Contexte** : demande utilisateur - la regle de relecture existait en 3 couches (AGENTS.md REGLE DE RELECTURE, protocole-activation GARDE-FOU RELECTURE, cerberus.c0/c0b dans le marbre) mais PAS au niveau regle immuable du fichier grave.

**Action** : ajout de la section "RELIRE SA FICHE AVANT MISSION (IMMUABLE)" dans regles-groupes-agents.md (apres RELEVE MEME ROUND) : chaque agent relit SA fiche + SES corrections juste avant SA mission ; coherence fiche + corrections + mission = demarrage a la lettre sans derive ; mecanisme c0/c0b + GARDE-FOU RELECTURE du protocole-activation. Porte du marbre ouverte avec proteger-modifier-marbre (zone regles-groupes-agents, autorisation UTILISATEUR explicite) - empreinte mise a jour + journalisee.

**Lecon** : une regle de comportement n est IMMUABLE que si elle est gravee dans le marbre (regles-groupes-agents.md + empreinte + verrou test-057). Les couches protocole/AGENTS.md ne suffisent pas : un agent peut les contourner. La gravure + la porte + le verrou forment le triptyque complet.
## [LECON] 2026-08-16 -- CORRECTION c0b ARGUS/GARDIEN (Buffy)

**Contexte** : demande utilisateur - creer un garde-fou verifiant c0/c0b sur les 15 parcours. Scan prealable : 13/15 conformes mais argus c0b avait des indices type "fichier" au lieu du modele outil lire-fichier, et gardien c0b n avait QUE la regle (aucun outil).

**Action** : correction des 2 cases c0b au modele exact (regle ACTION OBLIGATOIRE + outil lire-fichier vers corrections.md + outil lire-fichier vers fiche.md, suivant c0c) via editer-parcours + bump argus v0.1.8->v0.1.9 et gardien v0.1.1->v0.1.2 + fiches synchronisees (Pattern 14). Validation : valider-cartes 15/15, test-055 12/12, normes 0/0.

**Lecon** : le scan structurel des cartes avant un garde-fou revele les ecarts au modele (2 cartes avaient c0b sans outil de lecture). Le garde-fou seul aurait KO - il faut CORRIGER les cartes AVANT de creer le test, sinon le test verrouille un etat defectueux. Toujours scanner la cible avant d ecrire le garde-fou.
## [LECON] 2026-08-16 -- CORRECTION c0b ATLAS/MINERVE/PROMETHEE (Buffy)

**Contexte** : le garde-fou test-072 (Morpheus) a detecte des ecarts c0b : promethee (2e lire-fichier vers corrections.md au lieu de la fiche), minerve (idem), atlas (2 outils lire-fichier SANS commande du tout).

**Action** : correction des 3 c0b au modele exact (commande lire-fichier corrections.md + lire-fichier <agent>.md) + bumps atlas v0.4.3->v0.4.4, minerve v0.3.2->v0.3.3, promethee v0.3.2->v0.3.3 + fiches synchronisees. Validation : 15/15 cartes conformes, scan c0b 15/15 OK, test-072 10/10, normes 0/0.

**Lecon** : un garde-fou bien ecrit DECOUVRE des ecarts reels que le scan humain avait manques (atlas sans commande, minerve/promethee doublon corrections). Le scan complet systematique (toutes les cartes d un coup) est plus efficace que la correction au cas par cas - scanner TOUT, corriger TOUT, puis reverifier.
## [LECON] 2026-08-16 -- 3 REFERENCES PROTOCOLE AJOUTEES (Buffy, zone marbre)

**Contexte** : l audit --coherence de detecter-contradictions v0.1.2 signalait 3 REGLE_SANS_REFERENCE (mineur) dans regles-groupes-agents.md : RELEVE MEME ROUND (sans protocole-activation), SEUL JANUS (sans protocole-tests), SEUL BUFFY (sans protocole-controle-buffy).

**Action** : ajout des 3 references au format du modele existant ([protocole-X/](protocole-X/)) SANS toucher au texte des regles + porte du marbre ouverte (proteger-modifier-marbre zone regles-groupes-agents, autorisation UTILISATEUR explicite, empreinte 0f8b3d68 journalisee). Verification : verrou marbre rc=0, audit --coherence ne signale plus QUE le MAJEUR c0c connu, test-073 7/7, test-069 9/9, test-057 24/24, normes 0/0.

**Lecon** : une regle IMMUABLE doit CITER son protocole associe - c est la reference croisee qui rend l ensemble navigable et auditable. L audit --coherence detecte automatiquement ces oublis (mineur) et la porte du marbre permet de les corriger sans casser le verrou. Les 3 references ajoutees suivent exactement le modele des 2 deja presentes (HYGIE -> nettoyage, MORPHEUS -> tests) : format [protocole-X/](protocole-X/).
## [LECON] 2026-08-16 -- CORRECTION BRANCHE OUI -> c0c (Buffy, zone marbre + protocole)

**Contexte** : l audit --coherence signalait en MAJEUR que la regle gravee RELIRE disait OUI -> mission au lieu de OUI -> c0c -> mission (le protocole et les 15 cartes passent par c0c).

**Action** : correction de la regle gravee (ligne 243 : OUI -> c0c contexte obligatoire -> mission) + porte du marbre (autorisation UTILISATEUR, empreinte 0e4f25c2). MAIS l audit a alors revele une 2e incoherence : le protocole-activation lui-meme disait OUI -> mission (ligne 75) alors que ligne 92-93 il dit c0 -> c0c -> mission - le protocole etait incoherent EN INTERNE. Correction de la ligne 75 du protocole (OUI -> c0c contexte -> mission). Resultat : audit --coherence PROPRE (0 contradiction).

**Lecon** : corriger la regle gravee a revele que le PROTOCOLE avait la meme erreur de flux - l audit compare la regle au premier match de flux du protocole, donc un protocole incoherent en interne produit des faux conflits. La correction en chaine (regle PUIS protocole) a rendu les 2 sources coherentes entre elles ET avec les 15 cartes. L audit --coherence est l outil qui verifie la coherence COMPLETE du triptyque regle + protocole + cartes.
## [LECON] 2026-08-16 -- 2 REFERENCES MARBRE AJOUTEES : AUDIT --COHERENCE PROPRE (Buffy)

**Contexte** : demande utilisateur - les regles SEUL CLIO et LE MODELE DE CONFIANCE ne citaient pas leur protocole (2 MINEUR REGLE_SANS_REFERENCE signales par l audit --coherence apres la table 8/8 de Vulcain).

**Action** : ajout des 2 references dans regles-groupes-agents.md au format modele [protocole-X/](protocole-X/) : SEUL CLIO -> protocole-verification-coherence (ligne 154, mecanique de verification de coherence documentaire), LE MODELE DE CONFIANCE -> protocole-controle-statuts (ligne 207, mecanique du second controle Janus). Porte du marbre ouverte (autorisation UTILISATEUR, empreinte c782ba8c journalisee). Verifications : audit --coherence PROPRE (0 contradiction), verrou rc=0, normes 0/0.

**Lecon** : la table REGLE_PROTOCOLE de detecter-contradictions est un contrat bidirectionnel : ajouter une association cote outil revele les references manquantes cote marbre, et corriger le marbre fait disparaitre les mineurs automatiquement - l audit sert de preuve de correction. Le format de reference est uniforme ([protocole-X/](protocole-X/)) et l insertion se fait en fin de section (apres Garde-fou ou apres la derniere puce) avant la section suivante.
## [LECON] 2026-08-16 -- WORKFLOW KO OBLIGATOIRE GRAVE DANS LA FICHE DE JANUS (Buffy)

**Contexte** : l option --relancer-ko v0.5.2 (mecanisation des KO) existait dans l outil mais la fiche de Janus ne la mentionnait pas - la section KO disait seulement "je RELANCE la serie concernee", trop vague, Janus ne l appliquait pas (demande utilisateur : graver le workflow).

**Action** : remplacement de la section par le WORKFLOW KO OBLIGATOIRE en 5 etapes imperatives : (1) KO detecte -> lire le rapport, (2) JAMAIS relancer la suite complete apres un KO - rapporter a Cerberus qui active l agent habilite, (3) REVALIDATION CIBLEE avec --relancer-ko (l outil deduit la liste du dernier run), (4) validation de la serie --series X, (5) suite complete en dernier. + ajout de --relancer-ko a la table des options essentielles. Pas de bump : la fiche reference le parcours v0.4.11, non modifie.

**Lecon** : un outil mecanise ne sert a rien si la fiche de l agent qui doit l utiliser ne documente pas le WORKFLOW d usage : l outil (--relancer-ko) et la fiche (workflow KO en 5 etapes) forment le couple complet - l outil deduit, la fiche ordonne. La formulation imperatives ("JAMAIS", "OBLIGATOIRE", "Interdit") est celle qui contraint vraiment l agent, pas les suggestions.
## [LECON] 2026-08-16 -- COMMANDES CORRIGER-SYMBOLES --all + RESYNC LOCK (Buffy)

**Contexte** : diagnostic Cerberus - Morpheus corrige les accents a la main
car les indices corriger-symboles des cartes n avaient AUCUN champ
commande (l agent ne savait pas comment appeler l outil) et l outil SANS
--all conserve les accents du corps de texte.

**Correction** : ajout du champ commande avec --all aux 32 indices
corriger-symboles des 15 cartes (via editer-parcours --modifier-case,
jamais d ecriture JSON directe - barrage n 3). Chaque commande :
'python3 .../corriger-accents-zones-sensibles.py
cerveau-projet/agents/<agent>/corrections.md --all'.

**Decouverte importante** : 5 cartes (argus, atlas, gardien, minerve,
promethee) avaient une empreinte PERIMEE dans cartes-lock.json - elles
avaient ete modifiees anterieurement sans passage par editer-parcours, le
lock n ayant jamais ete resynchronise. editer-parcours refusait d ecrire
(blocage circulaire : on ne peut pas ecrire car le lock diverge, et le
lock ne se met a jour qu apres une ecriture). Solution : verifier les 5
cartes (valider-cartes 5/5 CONFORME) puis resynchroniser le lock
(maintenance legitime du manifeste, documentee au registre).

**Lecons** :
1. Un indice outil sans champ commande est INUTILE pour l agent : le nom
   et le chemin ne suffisent pas, la commande exacte doit etre dans la
   carte (lecon deja apprise pour d autres indices, reappliquee ici).
2. Le mode standard de corriger-accents-zones-sensibles est --all (la doc
   le dit) - une commande sans --all conserve les accents du corps et
   pousse l agent a corriger a la main.
3. cartes-lock.json peut devenir perime silencieusement : test-057
   verifie la couverture mais PAS la conformite des empreintes - angle
   mort a signaler (un garde-fou de conformite serait utile).

## [LECON] 2026-08-16 -- INDICE DETECTER-TRONCATURES CARTE VULCAIN (Buffy)

**Contexte** : non-regression 76 tests - test-035 evaluer-processus signalait
OUTIL_HORS_CARTE : la declaration registre de creation de detecter-troncatures
par Vulcain etait legitime mais la carte vulcain n avait pas l indice (les
autres detecter-* crees par Vulcain sont en case c10).

**Action** : via editer-parcours --modifier-case (barrage n3 respecte, jamais
d ecriture JSON directe), ajout de l indice detecter-troncatures a la case
c10 de parcours-vulcain (nom/chemin/commande --tous) + bump 0.4.20 -> 0.4.21
+ synchro fiche (Pattern 14).

**Verifications** : valider-cartes vulcain CONFORME, --tous 15/15, evaluer-
processus --agent vulcain 0 probleme, scan global 0 probleme, normes 0/0.

**Lecon** : quand Vulcain cree un outil detecter-*, l indice doit etre ajoute
a SA carte (case c10) des la creation - sinon la declaration registre de
creation devient OUTIL_HORS_CARTE et la barriere test-035 bloque. C est une
modification de carte -> Buffy (via editer-parcours + bump + synchro fiche).


## [LECON] 2026-08-16 -- INDICES ANALYSER-NOMS-MAJ/CORRIGER-NOMS-MAJ CARTE VULCAIN (Buffy)

**Contexte** : la non-regression (barriere E) etait bloquee par test-035
(2 OUTIL_HORS_CARTE) : Vulcain a declare l usage des 2 nouveaux outils au
registre mais sa carte n avait pas encore les indices.

**Correction** : ajout des 2 indices outil (analyser-noms-maj,
corriger-noms-maj) dans la case c10 de parcours-vulcain via
editer-parcours --modifier-case --bump (0.4.21 -> 0.4.22), fiche synchro
(Pattern 14). Resultat : valider-cartes CONFORME, evaluer-processus 0 probleme.

**Lecons** :
1. Tout outil CREE et DECLARE au registre exige son indice dans la carte
   de l agent qui le cree : la declaration registre sans indice carte =
   OUTIL_HORS_CARTE (test-035).
2. editer-parcours --contenu attend le JSON COMPLET de la case (pas un
   diff) : reconstruire la case entiere puis la passer a --modifier-case.
3. Le cwd d un subprocess Python sous Windows doit etre un chemin absolu
   natif (Z:\\...) : un chemin POSIX (/z/...) leve NotADirectoryError.


## [LECON] 2026-08-16 -- SECTION ENVIRONNEMENT DE TRAVAIL DANS LES FICHES (Buffy)

**Contexte** (demande utilisateur) : chaque fiche agent doit contenir les
infos de l environnement reel (OS, shell, langages, racine projet) pour
que les agents sachent toujours sur quel systeme ils travaillent et
n oublient jamais les differences Windows vs Linux.

**Actions** :
1. Template fiche-agent-template.md : section OBLIGATOIRE `## Environnement
   de travail (Systeme)` ajoutee entre UTILISATION et Limites - verifier-
   conformite-fiche la lit DYNAMIQUEMENT, elle devient exigee partout.
2. Les 15 fiches agents : bloc genere par verifier-systeme --bloc-fiche
   <agent> insere avant ## Limites (Windows reel + differences Windows vs
   Linux : chemins POSIX/natifs, bash MSYS, LF jamais CRLF, python3, ASCII
   via entonnoir).
3. Verifications : verifier-conformite-fiche 11/11 CONFORME (cerveau-
   projet) + athena/gardien CONFORMES (trio + nouveaux), test-016 20/20,
   test-045 15/15, test-046 10/10, normes 0/0 sur 16 fichiers.

**Lecons** :
1. verifier-conformite-fiche est DYNAMIQUE (sections lues du template) :
   ajouter une section au template suffit a l exiger partout - aucun
   compteur a adapter.
2. subprocess Python sous Windows : cwd natif (Z:\\...) obligatoire,
   un chemin POSIX (/z/...) leve NotADirectoryError.
3. Le template a ete ecrit par le 1er run AVANT l erreur cwd : verifier
   l etat reEL apres un run partiel avant de conclure.

## [LECON] 2026-08-16 -- JOURNALISATION ET REDIRECTIONS : JAMAIS DE /tmp SYSTEME (Buffy)

**Contexte** : constat utilisateur - les agents redirigeaient leurs .log vers le
/tmp du systeme (ex: > /tmp/nr.log) au lieu du dossier tmp-AGENT/ du workspace.
Le protocole creation-scripts-temporaires ne couvrait que les SCRIPTS jetables,
rien sur les journaux et captures de sortie : c etait le trou.

**Correction (protocole v0.2.11)** : nouvelle section Journalisation et
redirections de sortie - le dossier tmp-AGENT/ est le SEUL endroit ou ecrire
pendant une mission, y compris les journaux. Toute redirection d ecriture
(> fichier.log, tee, captures) va dans tmp-AGENT/fichier.log, JAMAIS vers le
/tmp systeme ni ailleurs hors workspace. Le journal disparait avec le dossier
en fin de mission (rm -rf tmp-AGENT) : 0 residu.

**Dette legacy documentee** : 13 vieux .sh de tests d outils (activer-agent-
principal test-001..008, detecter-impacts, detecter-usage-outils-externes)
utilisent encore /tmp pour leur espace de test - hors suite non-regression,
a migrer ou retirer dans une mission ulterieure (ne pas laisser la regle
nouvelle s appliquer a du code mort).

## [LECON] 2026-08-16 -- CARTE CERBERUS v0.5.0 : HABILITATIONS LIMITEES (Buffy)

**Contexte** : verdict Themis (rapport themis/rapports/rapport-audit-
carte-cerberus-habilitations-2026-08-16.md) - la case c10 de la carte de
Cerberus contenait combos-analyse-projet (outil d ANALYSE avec rapport
ecrit, proprietaire Clio) : le trou par lequel Cerberus a derive (audit
au lieu d activer Themis). Demandes utilisateur : habilitations de
Cerberus limitees a la coordination et a la lecture.

**Correction (porte du marbre, autorisation utilisateur)** :
- c10 : indice combos-analyse-projet RETIRE (reste activer-agent-principal)
- c0b : indice lire-fichier dedoublonne (1 au lieu de 2)
- version 0.4.9 -> 0.5.0 + fiche cerberus.md (Pattern 14)
- valider-cartes CONFORME, valider-case OK, lock cartes resynchronise

**Lecon protocole marbre pour une CASE protegee** : editer-parcours
refuse de modifier une case protegee (hash nouveau != empreinte). La
sequence correcte : (1) l UTILISATEUR autorise la porte ; (2) ecrire la
case modifiee directement (cadre protocole marbre, backup avant) ;
(3) proteger-modifier-marbre --zone --autorisation re-empreinte le
manifeste ET resynchronise cartes-lock.json (FIX v0.1.1) ; (4) les
verrous passent ensuite. Ne pas contourner : toujours la porte d abord.

## [LECON] 2026-08-16 -- CARTE JANUS v0.4.12 : RETRAIT EDITER-FICHIER DE C4 (Buffy)

**Contexte** : Janus a corrige des fichiers de tests au lieu de les renvoyer a
Morpheus. Cause racine : la case c4 'Verifier les tests' de parcours-janus.json
contenait un indice outil editer-fichier - Janus avait donc l habilitation de
modifier les fichiers qu il devait seulement VERIFIER.

**Correction** (via editer-parcours uniquement) : retrait de l indice
editer-fichier de c4, bump 0.4.11 -> 0.4.12, fiche janus.md synchronisee,
valider-cartes CONFORME, normes 0/0.

**Verification bumper** : l outil bumper = mettre-a-jour-versions (nom de
catalogue), il etait DEJA present en c33 de la carte de Janus - l audit initial
cherchait le mot 'bumper' au lieu du nom reel.

**Lecon** : une case 'VERIFIER X' ne doit JAMAIS porter un outil de modification
de X - l habilitation suit le principe de separation verification/modification.
Et pour auditer un outil, chercher son NOM DE CATALOGUE reel (mettre-a-jour-versions),
pas son surnom (bumper).

## [LECON] 2026-08-16 -- SYNCHRONISATION REGLES SOURCE/PROTOCOLE (Buffy, test-083)

**Contexte** : le nouveau garde-fou test-083 (regles exclusives IMMUABLE de
regles-groupes-agents.md synchronisees avec leur protocole associe) a detecte
3 ecarts reels : 1) protocole-tests ne citait JAMAIS JANUS (alors que la
section SEUL JANUS LANCE LA NON-REGRESSION le reference) ; 2)
protocole-verification-coherence ne citait JAMAIS CLIO (l Agent du protocole
etait Themis) ; 3) les sections LE MODELE DE CONFIANCE et RELEVE MEME ROUND
n avaient pas de garde-fou test-XXX cite.

**Corrections** :
- protocole-tests : section REGLE IMMUABLE SEUL JANUS LANCE LA NON-REGRESSION
  (janus seul habite, morpheus tests individuels uniquement, garde-fou test-037)
- protocole-verification-coherence : mention CLIO seul habite a mettre a jour
  le README (Themis verifie, Janus controle croise, garde-fou test-020)
- regles-groupes-agents.md : garde-fous ajoutes aux 2 sections (MODELE DE
  CONFIANCE -> test-056 verrou + test-057 marbre ; RELEVE MEME ROUND ->
  test-056 verrou + protocole-activation) - passage de la PORTE DU MARBRE
  (autorisation utilisateur) car le fichier est grave.

**Lecon** : une regle exclusive dupliquee dans un protocole doit nommer
l AGENT exclusif dans le protocole (pas seulement dans la source). La porte
du marbre est OBLIGATOIRE pour regles-groupes-agents.md (zone gravee) : ne
jamais l oublier apres une modification, sinon test-057 casse.

## [LECON] 2026-08-16 -- PROTOCOLE-SECURITE-MARBRE v0.1.1 : RELECTURE AVANT GRAVURE (Buffy)

**Demande utilisateur** : graver la relecture obligatoire avant toute nouvelle
regle immuable - audit Argus (doublons + concordance source/protocole) AVANT
la porte du marbre.

**Correction** : protocole-securite-marbre v0.1.1 - le flux de la porte ajoute
l etape 4 RELECTURE OBLIGATOIRE : toute zone de REGLES (fichier dans
regles-immuables/) exige detecter-contradictions --regles PROPRE avant
l autorisation (non PROPRE = refus meme avec autorisation). Une nouvelle
regle immuable majeure DOIT entrer au marbre via cette porte apres relecture
Argus PROPRE.

**Lecon** : un protocole de securite documente le FLUX, mais seule la
MECANISATION (outil v0.1.3 de Vulcain) rend la relecture ineluctable - le
protocole et l outil doivent rester synchronises (le protocole decrit ce que
l outil applique).


## [LECON] 2026-08-16 -- CARTE HYGIE C4 + DETECTION PROCESSUS (Buffy)

**Contexte** : suite mission Vulcain (combo-nettoyage-hygie v0.1.1) - la case
c4 Detection compartimentee de la carte hygie doit aussi scanner les
processus residuels.

**Modifie** (via editer-parcours, --modifier-case) :
- c4 : ajout de l indice outil detecter-processus-residuels (commande
  --detail) apres detecter-residus, avant combos-analyse-projet.
- Bump parcours hygie 0.1.4 -> 0.1.5 + fiche hygie.md synchronisee (Pattern 14).

**Preuves** : valider-cartes-decision --agent hygie CONFORME, verrou --audit
hygie detecter-processus-residuels OK, normes 0/0.

**Lecon** : la detection complete de Hygie couvre maintenant 3 leviers dans c4
(fichiers detecter-residus, processus detecter-processus-residuels, analyse
combos-analyse-projet) - le combo v0.1.1 fait la meme chose cote execution.

**APRES** : activer MORPHEUS (adapter test-005 0.2.5 -> 0.2.6, verifier
test-045 chariot hygie inclut detecter-processus-residuels) puis JANUS.
## [LECON] 2026-08-16 -- SYNCHRO FICHES APRES MIGRATION RELECTURE (Buffy)

**Contexte** : Vulcain a migre les 15 parcours vers la relecture obligatoire
(c0 action RELIRE + c0b question confirmation) et bumpe les versions. Les
15 fiches portaient encore l ancienne version -> valider-cartes 15 NON
CONFORME (incoherence fiche/parcours, Pattern 14).

**Travail realise** : mise a jour du bloc "REGLE ABSOLUE -- PARCOURS (vX.Y.Z)"
des 15 fiches (argus 0.1.10, athena 0.3.3, atlas 0.4.5, buffy 0.4.10,
cerberus 0.5.1, clio 0.5.10, gardien 0.1.3, hermes 0.1.3, hygie 0.1.6,
janus 0.4.13, minerve 0.3.4, morpheus 0.4.11, promethee 0.3.4, themis 0.4.6,
vulcain 0.4.23). Resultat : valider-cartes --tous = 15 CONFORME.

**Lecon** :
- Toute migration de parcours (bump de version) doit synchroniser les fiches
  dans la MEME chaine, sinon valider-cartes bloque immediatement (Pattern 14).
- La version vit dans le parcours JSON ; la fiche la REFLETE : jamais editer
  la fiche avant d avoir bumpe le parcours.


## [LECON] 2026-08-16 -- BRANCHEMENT OUTILS WEB DANS LA CARTE ATLAS (Buffy)

**Contexte** : suite de la mission Vulcain (rechercher-web + detecter-recherches-obsoletes
creees). Buffy branche les 2 indices outil dans le parcours atlas et synchronise
la fiche.

**Fait** :
- c13 "Executer la recherche" : + indice outil `rechercher-web` (commande avec
  --agent {agent} et requete quotee) - la case n avait AUCUN outil avant.
- c12 "Formuler la requete" : + indice outil `detecter-recherches-obsoletes`
  (verifier la fraicheur des recherches existantes AVANT de re-chercher -
  aligne avec l etape 2 du protocole : chercher dans le cerveau d abord).
- Bump parcours atlas 0.4.5 -> 0.4.6 (via editer-parcours, l outil sanctionne).
- Fiche atlas synchronisee (Pattern 14 : PARCOURS v0.4.6).
- Verifie : valider-cartes --agent atlas CONFORME, verrou ouvert pour atlas
  (les 2 outils), navigation c12 -> c13 -> c14 -> c10, normes ASCII + LF.
- Registre : 4 declarations (editer-parcours, valider-cartes-decision,
  mettre-a-jour-versions) - la declaration guider-parcours a ete RETIREE
  (outil non assigne a une carte : pas d indice outil, usage via fiche).

**Lecons** :
- Le verrou lit les CARTES comme source de verite : un outil non branche
  bloque TOUT agent (meme le proprietaire prevu) tant que l indice n est pas
  dans le parcours. L ordre de la chaine est donc : outil cree (Vulcain) ->
  carte branchee (Buffy) -> mission reelle (Atlas).
- Une fin de mission doit TOUJOURS suivre SA carte : la carte Buffy impose
  "Activer Janus" (c8/c22/c27), jamais "reactiver Cerberus" - evaluer-processus
  detecte les FIN_MISSION_ERRONEE. Verifier la carte avant d ecrire la raison
  d activation (corrige en cours de mission).
- guider-parcours n est un indice outil d AUCUNE carte : ne pas le declarer
  au registre en mode direct (risque OUTIL_HORS_CARTE test-035). Les usages
  via fiche (bloc code) ne se declarent pas.
- Les indices outil ont le format {type, nom, catalogue, chemin, commande} :
  respecter les 5 cles pour le verrou et test-035.


## [LECON] 2026-08-16 -- EDUQUER JANUS SUR LA SUITE DE NON-REGRESSION (Buffy)

**Contexte** : demande utilisateur URGENTE - Janus lance encore la suite de
non-regression comme avant alors que le lanceur a beaucoup evolue (serie KO
persistante, categories/tags, classement dynamique par taux de KO). L outil
s est ameliore mais la fiche et la carte de Janus (ce qu il lit en mission)
n avaient pas suivi.

**Fait** :
- fiche janus.md : ajout des options manquantes au tableau (--ko reprendre/
  nouveau, --etat-ko, --tags, --categorie, --desactiver-categorie/--activer-
  categorie, --etat-categories, --ordre-fixe, --relancer-ko --series X) +
  nouveau paragraphe WORKFLOW SERIE KO PRIORITAIRE (constater --etat-ko ->
  --ko reprendre en premier avec barriere -> series normales -> suite complete)
  + note ciblage par --tags/--profil selon la zone de mission.
- carte parcours-janus.json : case c4 "Verifier les tests" + regle workflow
  serie KO (indice regle), bump 0.4.13 -> 0.4.14, fiche synchronisee
  (Pattern 14), valider-cartes CONFORME, normes ASCII + LF.

**Lecons** :
- Ameliorer un outil SANS mettre a jour la fiche + la carte de son utilisateur
  = amelioration morte : Janus lit SA fiche et SA carte, pas le --aide du
  lanceur. L education fait partie du livrable d une amelioration d outil.
- Verifier l ecart par la VRAIE source de Janus : sa fiche (section UTILISATION)
  et sa carte (indices outil) - pas seulement le code du lanceur.
- L utilisateur a raison : "on ameliore l outil mais Janus ne sait pas l
  utiliser" - a chaque nouvelle option majeure du lanceur, l education de
  Janus doit etre planifiee dans le round (Morpheus ne suffit pas).

## [LECON] 2026-08-16 -- CORRECTION DES CASES REACTIVER FAUTIVES (Buffy)

**Contexte** : demande utilisateur (le garde-fou anti-auto-reactivation ne
fonctionne pas : test-070 ne scanne que les cases de type 'fin', toutes les
cases d'action/regle echappent au scan).

**Constats** :
- La commande `reactiver <session> <raison> <agent>` ramene TOUJOURS a
  Cerberus (le 3e argument est informatif, pas la cible).
- 31 cases fautives sur 11 parcours : titres et messages qui affirmaient
  "reactiver X" avec X != Cerberus (ex: cerberus c12b "reactiver Buffy",
  argus c29a "il me reactivera", les boucles KO Janus/Themis "je le/la
  reactiverai avec mon bilan", "Themis me REACTIVE").

**Corrections** (via editer-parcours, barrage n3, + bump + fiche Pattern 14) :
- "reactiver X (X != cerberus)" -> "activer X" (commande activer).
- "je le/la reactiverai avec mon bilan" -> "je l ACTIVE (commande activer)
  pour re-controle/re-audit avec mon bilan".
- "Themis me REACTIVE" -> "Themis me RE-ACTIVE (commande activer)".
- argus c29a : "il reactivera Cerberus avec le bilan".

**Lecon** : tout message de carte qui mentionne une relance d'agent doit
utiliser la commande `activer` (sauf si la cible est Cerberus, alors
`reactiver`). Le mot "reactive" est surcharge (verbe general vs commande) :
pour lever l'ambiguite, toujours preciser "(commande activer)" ou
"reactiver Cerberus".

**Preuves** : valider-cartes 15/15 CONFORME, bumper 0 incoherent, normes
ASCII/LF 0 ecart, rescan 0 forme fautive restante.

## [LECON] 2026-08-16 -- CASES REACTIVER RESIDUELLES CORRIGEES (Buffy)

**Contexte** : suite de la correction des 31 cases reactiver fautives. Le
garde-fou etendu test-070 v2 (scan de TOUTES les cases, plus seulement les
fins) a detecte 3 cas majeurs que le scan initial avait rates car ils
utilisent le PRESENT 'me REACTIVE' (pas le futur ni la commande) :
  - buffy c39 'Atlas me REACTIVE' -> 'Atlas me RE-ACTIVE (commande activer)'
  - cerberus c15c 'Janus recontrole et me reactive' -> 'Janus recontrole
    puis REACTIVE Cerberus avec son rapport'
  - janus c32 'Themis me REACTIVE' -> 'Themis me RE-ACTIVE (commande activer)'
  + 3 cas mineurs d ambiguite (janus cT8/cT9/cT10 'me reactive (boucle KO)'
    -> 'me RE-ACTIVE (commande activer) pour re-controle (boucle KO)').

**Lecon** : la forme PRESENT 'me REACTIVE' (ou 'reactiver X') est aussi
fautive que la commande : reactiver ramene TOUJOURS a Cerberus. La
formulation sans ambiguite est 'RE-ACTIVE (commande activer)' quand la
cible est un autre agent, ou 'REACTIVE Cerberus' quand la cible est
Cerberus. Les garde-fous doivent scanner TOUTES les cases (action, regle,
controle), pas seulement les fins : c etait la faille de test-070 v1.

**Preuves** : test-070 11 OK / 0 KO, valider-cartes 15/15, bumper 0
incoherent, normes ASCII/LF 0 ecart.


## [LECON] 2026-08-17 -- EDUQUER JANUS A LA COMPOSITION CIBLEE DE LA SUITE (Buffy)

**Contexte** : demande utilisateur - Janus lancait encore la suite complete
par reflexe meme pour un petit controle. La suite avait toutes les briques
(--fichiers, --profil, --tags, --categorie, --desactiver/--activer,
--etat-tests/--etat-categories, --series) mais ni la fiche ni la carte de
Janus n ordonnaient la DECISION de composition.

**Lecons techniques** :
1. editer-parcours --contenu REMPLACE TOUTE la case : il faut fournir le
   JSON COMPLET (type + titre + indices), pas seulement le champ modifie.
   J ai perdu le champ type de c4 (-> c4:None, NON CONFORME) puis restaure
   a la passe suivante (v0.4.17). Toujours verifier valider-cartes apres.
2. Un workflow immuable doit etre dans la FICHE (detail) ET la CARTE
   (resume dans la case outil) pour que l agent le lise pendant la mission.
3. La composition ciblee se resume en 6 pas : identifier fichiers modifies
   -> choisir le mode le plus leger (--fichiers/--profil/--tags/--series)
   -> desactiver les tests inutiles (--desactiver, persistant)
   -> valider les series concernees -> reactiver en fin (--activer)
   -> suite complete UNIQUEMENT en validation finale.

**Preuves** : carte janus v0.4.17 CONFORME, valider-cartes --tous 15/15,
bumper --tous 0 incoherent, normes ASCII/LF 0/0.

## [LECON] 2026-08-17 -- C4 JANUS SUIVANT PERDU + EDITER-PARCOURS CIBLE (Buffy)

**Contexte** : la barriere B a bloque sur test-026 (detecter-cablages) : la
case c5 de la carte janus etait ORPHELINE. Cause racine : MA mission
composition ciblee (carte janus v0.4.17) avait ecrase la case c4 avec
editer-parcours --contenu (incident deja documente : type perdu puis restaure)
MAIS le champ suivant avait aussi ete perdu sans etre restaure - c4 n avait
NI suivant NI branches, c5 devenait orpheline. Les 6 indices etaient presents
(le fix --suivant c4 --cible c5 a suffi, aucun contenu a reconstruire).
Correction : c4.suivant=c5 (via --suivant/--cible, l option CHIRURGICALE),
bump janus 0.4.17 -> 0.4.18, fiche synchronisee. Verdict : carte CONFORME,
detecter-cablages PROPRE, test-026 10/10.

**Lecon 1 - editer-parcours deduit la CIBLE de --agent, pas de la session** :
j ai lance --suivant c4 --cible c5 --wet avec --agent buffy (pour respecter la
regle SEUL BUFFY) et l outil a modifie PARCOURS-BUFFY, pas parcours-janus !
Pour editer la carte d un AUTRE agent, il faut --agent <agent-cible> (janus
ici). Les 2 operations (--suivant + --bump) ont touche la carte buffy : le
--suivant etait IDEMPOTENT (c4.suivant deja c5) mais le --bump a monte la
version 0.4.12 -> 0.4.13 SANS raison. REPARATION : version remise a 0.4.12 +
empreinte SHA-256 recalculee dans cartes-lock.json (meme fonction que
editer-parcours) pour que le barrage n3 reste coherent.

**Lecon 2 - un --bump sans modification reelle = pollution** : le bump ne doit
suivre qu une modification de contenu. Un bump parasite desynchronise la fiche
(Pattern 14) et pollue l historique. TOUJOURS verifier quel fichier l outil a
ecrit dans sa sortie ([OK] Parcours ecrit : <chemin>) AVANT de poursuivre.

**Lecon 3 - le verrou anti-contournement se re-synchronise par le lock** : une
reparation d erreur (retour de version) peut se faire sans casser le barrage
n3 SI on recalcule l empreinte avec la fonction EXACTE de l outil
(SHA-256 du contenu normalise LF + lignes sans espace final).


## [LECON] 2026-08-17 -- CHIRON : JE DETECTE JE NE CORRIGE PAS (Buffy)

**Contexte** : la non-regression de Janus a bloque sur test-058 (barriere D) :
la carte de Chiron (creee precedemment) utilisait editer-fichier-agents, outil
EXCLUSIF a Buffy, dans c10 (corriger les incoherences simples) et c12 (ecrire
les lecons dans les corrections de l agent cible).

**Cause racine** : lors de la creation de Chiron, sa carte a ete ecrite avec un
script Python direct (au lieu d editer-parcours) et a copie le modele d un
agent correcteur, alors que Chiron est un EDUCATEUR qui DETECTE et SIGNALE
(comme Argus : JE DETECTE JE NE CORRIGE PAS).

**Correction** (via editer-parcours --agent chiron --modifier-case, le seul
outil habilite) :
- c9  : OUI -> c10 "documenter les corrections proposees" (plus "corriger")
- c10 : retrait d editer-fichier-agents -> "documenter le rapport puis
        SIGNALER a Buffy" (corrections simples ET complexes vont a Buffy)
- c12 : retrait d editer-fichier-agents -> "ecrire MES lecons dans MES
        corrections uniquement" (jamais les fichiers des autres agents)
- c13 : bumper MA fiche uniquement (jamais celle des autres)
- fiche chiron.md : REGLE ABSOLUE 1 = JE DETECTE JE NE CORRIGE PAS, retrait
  d editer-fichier-agents de la table P0, du workflow Purifier et des Limites

**Verifications** : valider-cartes chiron CONFORME, test-058 6/6, test-055
12/12, test-071 7/7, test-072 10/10, verifier-conformite-fiche CONFORME,
normes ASCII 0 + LF pur sur carte et fiche.

**Lecon Buffy** : un nouvel agent correcteur ne doit JAMAIS heriter des outils
exclusifs d un autre role. L exclusivite (SEUL BUFFY CORRIGE LES FICHIERS DES
AGENTS) est verifiee par test-058 sur le TEXTE des cartes (pas seulement les
indices outil) : toute mention d editer-fichier-agents ou editer-parcours hors
de la carte buffy est un KO. Toujours creer les cartes via editer-parcours
(jamais de script Python direct) pour que le lock cartes-lock.json soit
coherent des la premiere ecriture.


## [LECON] 2026-08-17 -- EDUCATION JANUS : CYCLE KO v0.6.0 (Buffy)

**Contexte** : l utilisateur a constate que --ko-puis-stop (v0.5.9) n etait
pas documente dans la fiche de Janus (0 occurrence) et ne correspondait pas a
son modele de travail. Vulcain a corrige le lanceur (v0.6.0 : --ko nouveau =
balayage complet, --ko-puis-stop = CONTROLE TERMINE), Morpheus a adapte les
tests, je devais eduquer la fiche de Janus.

**Corrections dans janus.md** :
- Tableau Options essentielles : ajout de --ko-puis-stop + reformulation de
  --ko nouveau (MODE BALAYAGE COMPLET).
- Nouvelle section WORKFLOW CYCLE KO (v0.6.0) : passe 1 balayage (--ko
  nouveau, totalite des KO), passe 2 revalidation ciblee (--ko reprendre
  --ko-puis-stop), serie KO verte = CONTROLE TERMINE, suite complete
  conditionnelle (seulement si code partage touche - decision Janus).
- Harmonisation des sections WORKFLOW KO OBLIGATOIRE et COMPOSITION CIBLEE
  (la "suite complete en dernier" devient "suite complete conditionnelle").

**Verifications** : janus.md CONFORME (verifier-conformite-fiche 1/1), normes
ASCII 0 + LF pur.

**Lecon Buffy** : quand un outil evolue (nouvelle option), la fiche de l agent
utilisateur doit etre mise a jour dans la MEME chaine (Vulcain -> Morpheus ->
Buffy -> Janus). Une option sans education = un agent qui continue d utiliser
l ancien comportement, exactement le bug signale par l utilisateur.
