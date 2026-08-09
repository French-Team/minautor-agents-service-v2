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