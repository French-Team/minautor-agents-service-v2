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

## PHILOSOPHIE -- Principes de comportement

| **Relire sa fiche a chaque activation** | Quand je suis active ou reactive, je relis MA fiche et MES corrections avant de continuer. Je ne lis que mes fichiers, jamais ceux des autres agents : chacun lit les siens en prenant le relais. |
