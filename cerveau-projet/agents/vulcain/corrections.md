---
identite:
  type: corrections
  appartient_a: vulcain
  commun: false
# Corrections et Surcharges -- Vulcain
# Constructeur d'outils reels

agent:
  nom-agent: "vulcain"
  version_corrections: "0.1.0"
  derniere_mise_a_jour: "2026-08-05"

# Types de corrections
types:
  - regle: "Ajout d'une nouvelle regle specifique a Vulcain"
  - surcharge: "Modification d'une section existante de la fiche"
  - correction: "Correction d'une erreur recurrente"
  - configuration: "Parametre de travail specifique"
---

# Corrections et Surcharges
---



## [LECON] 2026-08-25 -- REPARATION ARBRES v2 : vues stark regenerees (inter-round Morpheus)

**Contexte** : inter-round de Morpheus (mission tests microsecondes). Le correctif glob du lanceur (test-0* -> test-*) a rendu test-101 actif : il n avait JAMAIS tourne et a revele une desynchronisation preexistante - arbre-stark.json (25/08 07:25) plus recent que ses vues (24/08 18:47), edith egalement signale au premier run.

**Realise** : verifier_arbres -> seul stark desynchronise (edith resynchronise entre-temps, probablement par le serveur EDITH H24). Regeneration : convertir-carte-mermaid --arbres --agent stark (stark.mmd 4 lignes + stark.svg 1170 octets). Resultat : 9 arbres v2 synchronises OK, test-101 11/11 OK.

**Lecons** :
1. UN ARBRE MODIFIE SANS REGENERER SES VUES = DESYNCHRONISATION INVISIBLE tant que test-101 ne tourne pas : toute modification d un arbre-<agent>.json doit s accompagner de convertir-carte-mermaid --arbres (le garde-fou verifie octet a octet).
2. LE GLOB DU LANCEUR PEUT EXCLURE DES TESTS SANS AUCUN SIGNE : test-100/101/102 commencent par test-1 et le glob test-0* ne les matchait pas - verifier la couverture (test-027 point 1) apres chaque ajout de test.

**Validations** : --arbres --verifier section arbres OK (rc v1 cartes = preexistant socrate/themis/vulcain hors perimetre), test-101 11/11 OK, normes ASCII/LF couvertes par test-101 points 5/5b.
## [LECON] 2026-08-25 -- MICROSECONDES -> MILLISECONDES : activer-agent-principal v0.7.2 -> v0.7.3 (Vulcain)

**Contexte** : l utilisateur constate que l outil ecrit toujours les timestamps d historique a 6 chiffres (microsecondes) au lieu de 3 (millisecondes) comme demande plus tot. Le commit 4fbd28f (18:41) n avait corrige que les FICHIERS DE DONNEES (AGENTS-historique.md, variables-actuelles.md), pas l OUTIL qui les ecrit : 4 occurrences %f (l.876, 1033, 1305, 1364) dans activer-agent-principal.py + get_timestamp() en %N (9 chiffres) dans le .sh.

**Realise** : (1) .py : %f -> troncature [:-3] sur les 4 occurrences (strftime puis troncature des 3 derniers chiffres) ; (2) .sh : %N -> %3N (GNU date supporte la precision) ; (3) versions : en-tete .py aligne 0.7.1 -> 0.7.2 puis bump 0.7.2 -> 0.7.3 (.py, .sh, spec, doc) ; la doc .md etait en dette massive (0.5.30 jamais bumpee) - alignee sur 0.7.3 avec entree au tableau versionning ; (4) tests Morpheus : test-102 (garde-fou millisecondes, 6/6 OK) + preuve baseline (KO test-001/002/003/008 preexistants).

**Lecons** :
1. %3f EST INVALIDE EN PYTHON (ValueError: Invalid format string) : la correction proposee dans le rapport Themis (%3f) ne fonctionne PAS - le bon pattern est la TRONCATURE [:-3] (deja utilise par horloge.py avec [:12]).
2. UN CORRECTIF DE DONNEES SANS CORRECTIF DE L OUTIL = RECURRENCE : 4fbd28f avait corrige les fichiers de donnees mais l outil a re-ecrit les 6 chiffres a la prochaine activation - toujours corriger l OUTIL (source) en plus des donnees.
3. LA DOC .md PEUT S'ENDETTER SANS LIMITE : la doc etait a 0.5.30 alors que l outil etait a 0.7.x (jamais bumpee depuis des versions) - le bumper en mode dossier la revele, la bumpee individuellement pour l aligner.
4. LE .sh N EST PAS TOUJOURS UN WRAPPER PUR : activer-agent-principal.sh a sa PROPRE logique get_timestamp() (%N) - verifier la parite .py/.sh a chaque correction de format (pas seulement les appels).

**Validations** : execution reelle sur copie (AGENTS_FILE surcharge) : .py et .sh ecrivent HH:MM:SS.mmm a 3 chiffres ; test-102 6/6 OK ; test-099 6/6 OK ; test-101 11/11 OK (apres reparation arbres) ; syntaxe python/bash OK ; ASCII 0/0 ; LF pur.
## [LECON] 2026-08-25 -- FERRARI BRANCHE A L ACTIVATION : activer-agent-principal v0.7.3 -> v0.7.4 (Vulcain)

**Contexte** : demande utilisateur - activer ferrari (agent v1 specialise freelance, double identite v1/v2, CONFIDENTIEL : seul Cerberus le connait, invisible des agents v2). L outil repondait 'Agent inconnu ferrari' : ferrari etait cree (fiche, parcours, protocoles) mais ABSENT du dictionnaire AGENTS - inactivable (meme oubli qu Argus v0.5.8 / Chiron v0.5.12).

**Realise** : (1) dictionnaire AGENTS du .py : entree ferrari (role + fiche agents/ferrari/ferrari.md + corrections) ; (2) 3 case statements du .sh (role, fiche, corrections) ; (3) couleur ferrari (#dc2626) ; (4) bump 0.7.3 -> 0.7.4 (py, sh, md + entree versionning, spec) ; (5) tests Morpheus : test-092 adapte avec EXEMPTIONS_MORTS={stark, ferrari} (9/9 OK, stark KO preexistant resolu), activation reelle sur copie OK.

**Lecons** :
1. UN AGENT CONFIDENTIEL NE PEUT PAS APPARAITRE DANS AGENTS.md MAIS DOIT ETRE DANS LE DICTIONNAIRE D ACTIVATION : la confidentialite (invisible des agents v2) impose de ne pas le lister dans AGENTS.md, mais sans dictionnaire il est inactivable - l ajout py/sh est la seule voie, et test-092 doit porter une EXEMPTION DOCUMENTEE (pas un contournement).
2. LE PATTERN 'AGENT CREE MAIS INACTIVABLE' RECIDIVE (Argus, Chiron, maintenant ferrari) : a chaque creation d agent v1, verifier que le dictionnaire AGENTS du .py + les 3 case statements du .sh le couvrent AVANT de le declarer disponible.
3. UNE EXEMPTION DE TEST PEUT RESOUDRE DES KO PREEXISTANTS : stark (v2, fiche freelance/) etait deja 'mort' pour test-092 - la liste d exemptions l a couvert, test-092 passe de 7/9 a 9/9.

**Validations** : syntaxe py + bash OK, get_agent_info('ferrari') + get_agent_role/fiche/corrections ferrari OK, activer session-admin ferrari sur copie OK, test-092 9/9, ASCII 0/0, LF pur.
## [LECON] 2026-08-27 -- SERVEUR DE DEMARRAGE V1 (oracle-demarrage) : l impasse v1 etait identique a la v2 (Vulcain)

**Contexte** : demande utilisateur - les agents ne demarraient plus apres activation depuis l ajout d oracle (hub de coordination v1, ne de JARVIS v2). L utilisateur a recadre : oracle doit reproduire la communication v1 (ancetre de la v2) mais NE PAS copier le code v2 - 2 univers distincts. Diagnostic : (1) oracle-server.py lance en mode stdio avec stdin DEVNULL = EOF immediat -> le serveur ne tournait JAMAIS (prouve : returncode 0 en 2s) ; (2) pas de DETACHED_PROCESS -> mort avec la console ; (3) sonde os.kill(pid,0) sur Windows TERMINE le processus au lieu de tester (lecon v2 hooks.py) ; (4) JSON double-encode dans inbox/cerberus.jsonl faisait crasher relais et agents_bloques ('str' object has no attribute get).

**Corrections** : (1) oracle-server.py v0.2.0 : nouveau mode --boucle (daemon resident : harnais + relais toutes les N secondes, log visible dans observations/oracle-log.txt, PID file, tolerance JSON double-encode dans relais) ; (2) NOUVEL OUTIL oracle-demarrage.py v0.1.1 : serveur de demarrage v1 (demarrage/arret/etat) - lance oracle-server --boucle + futur routines-server v1 s il existe, affiche DEFCON/files/agents bloques, declare ORACLE OPERATIONNEL, sonde PID Windows via OpenProcess, dry-run qui ne lance PAS les serveurs ; (3) relais.py : tolerance ligne string (double-encode).

**Lecons** :
1. UN SERVEUR LANCE AVEC stdin=DEVNULL MEURT AU PREMIER EOF : le mode stdio d un serveur qui lit des commandes JSON sur stdin est inutilisable en daemon - il faut un mode --boucle dedie (comme routines-server v2) qui tourne sans stdin.
2. os.kill(pid, 0) SUR WINDOWS NE TESTE PAS, IL TUE (TerminateProcess) : toute sonde PID doit passer par OpenProcess (lecon deja documentee v2 hooks.py, reproduite par oracle v1 - verifier TOUJOURS la sonde quand on cree un serveur).
3. UN FICHIER JSONL HISTORIQUE PEUT CONTENIR DU JSON DOUBLE-ENCODE (une string JSON dans une ligne) : tout lecteur de jsonl doit tolerer isinstance(msg, str) avant msg.get() - le fichier cerberus.jsonl contenait exactement ce cas et crashait le daemon.
4. LE DRY-RUN D UN LANCEUR DE SERVEUR DOIT NE RIEN LANCER : la premiere version de oracle-demarrage --dry-run lancait reellement le serveur (test prouve : pid cree) - un dry-run qui a des effets de bord est un mensonge.
5. LA V1 ET LA V2 SONT 2 UNIVERS : s inspirer du PATTERN v2 (chaine de demarrage, daemon detache, log visible, PID file) est legitime, copier le CODE v2 ne l est pas - chaque univers a son code, ses chemins, ses fichiers.
## [LECON] 2026-08-27 -- SERVEUR DE ROUTINES V1 (routines-server + citations) : les chemins relatifs cassent tout sous un cwd different (Vulcain)

**Contexte** : demande utilisateur - construire le serveur de routines v1 (equivalent v2, mais code 100% v1, univers dieux grecs) avec la routine citations (repere visuel toutes les 5 min, temporaire, desactivee en production) + ajouter la colonne Debut/Fin au tableau activites v1 (grades/secteurs grecs ASCII, inspire v2 sans copier). Le daemon (routines-server.py) lance les scripts via subprocess avec cwd=routines/ - ce qui a revele 4 bugs lies aux chemins relatifs.

**Corrections** : (1) routines-server.py v0.2.0 : daemon resident (boucle sur le manifest, etat persistant dans etat-executions.json, pid, tolerant aux erreurs) ; (2) routine citations.py v0.2.0 : citation d un dieu grec historisee dans le tableau activites v1 ; (3) manifest.json (citations 300s, actif=true dev / actif=false prod) ; (4) grades-v1.json (grades G0-SP + secteurs grecs ASCII) ; (5) activer-agent-principal.py v0.8.1 : colonnes Grade | Agent | Debut/Fin | Secteur + _construire_encart_v1 (migration qui reconstruit l encart SEUL, pas corps+encart).

**Lecons** :
1. UN DAEMON QUI LANCE DES SCRIPTS ENFANTS DOIT FORCER LES CHEMINS EN ABSOLU : le script citations.py etait lance avec cwd=routines/ donc les AGENTS_HISTORIQUE/AGENTS_ACTIVITE_RECENTE/GRADES_V1/CLASSEUR_STOCKAGE relatifs pointaient au mauvais endroit -> id=session-admin au lieu de glm5, grade [G?] au lieu de [G5]. Forcer _racine_projet() (_DOSSIER remonte jusqu a AGENTS-historique.md) ET injecter les variables d env + sys.path en ABSOLU.
2. UNE FONCTION DE MIGRATION DOIT RECONSTRUIRE L ENCART SEUL, JAMAIS corps+encart : la premiere version appelait maj_encart_activites (qui retourne corps complet + encarts, format de l ancien fichier unique) et l ecrivait dans AGENTS-activite-recente.md -> le corps du journal ecrasait le tableau. _construire_encart_v1(corps) reconstruit frontmatter+tableau UNIQUEMENT.
3. VERIFIER LE CODE RETOUR DES FONCTIONS CHARGEES DYNAMIQUEMENT : _historiser_agent retournait False quand le chemin etait introuvable mais main() l ignorait (print + exit 1) -> le daemon croyait la routine OK alors que rien n etait ecrit. Toujours brancher le retour sur le veritable succes.
4. LA COLONNE GRADE/SECTEUR EST ALIMENTEE PAR MAPPING DIRECT AGENT (pas mots-cles) : le mapping par mots-cles du role retombait sur [GEN] pour des agents non listes - ajouter les entrees directes par nom d agent dans grades-v1.json (plus robuste que lire les tags des fiches).

**Validations** : daemon routines + oracle-server tournent en parallele (oracle-demarrage demarrage/etat), routine citations ecrit grade [G5] secteur [TRS] id glm5 dans le tableau v1, migration du header ancien->nouveau sans incoherence (0 ligne a 9+ barres fausses), ASCII 0/0, JSON valides, syntaxe py + bump versions OK.
## [LECON] 2026-08-28 -- PILOTE ORACLE : LE MAITRE D HOTEL N EXECUTE PAS LE TRAVAIL (Vulcain)

**Contexte** : demande utilisateur - le round est brise depuis qu on a cree oracle. Diagnostic reel : oracle.py pilote deroulait TOUT l arbre de l agent en un seul appel, activait les maillons de controle automatiquement et posait FIN sans aucun travail fait.

**Diagnostic** :
1. _piloter_theme boucle sur tous les redirects avec limite 60 par defaut, tout l arbre servi d un coup.
2. _executer_commande_oracle et _activer_maillon activaient morpheus, janus et themis automatiquement aux cases delegation, maillons actives sans aucun travail.
3. _executer_fin_oracle reactive Cerberus automatiquement.
4. cmd_activer posait precedent egal a l agent lui-meme lors d une auto-reactivation.

**Corrections** pilote.py et oracle.py :
a. TA MISSION plus ORDRE de demarrer en tete du plateau.
b. limite par defaut 1 pas, a 3 endroits, cmd_pilote, main argparse de pilote.py et parser de oracle.py.
c. delegations transformees en arrets decision-libre, plus d activation automatique des maillons.
d. precedent egal a cerberus quand l activation vient de cerberus, auto-reactivation.

**Puis** : routine vigie-round, partie detection de la decision utilisateur les deux en cascade, session orpheline plus chaine en attente, alerte 4W a Cerberus, anti-spam 30 min, lecture seule.

**Lecons** :
1. UN PILOTE NE DOIT JAMAIS EXECUTER LE TRAVAIL NI ACTIVER LES MAILLONS A LA PLACE DE L AGENT : le maitre d hotel sert le plateau, l invite mange. L activation des maillons de controle n a de sens qu apres le travail reel.
2. UNE LIMITE PAR PAS EST LA GARANTIE DU RYTHME : sans borne, un pilote automatique deroule tout ; avec limite 1, l agent execute puis rappelle.
3. LA MISSION ET L ORDRE DE DEMARRER SONT LE PREMIER MESSAGE : un plateau qui commence par le besoin 1 sans rappeler la mission ne demarre pas l agent.
4. LE PRECEDENT D UNE AUTO-REACTIVATION EST CERBERUS, PAS L AGENT LUI-MEME.

**Verdict** : VALIDE - pilote corrige et teste manuellement, 1 pas a la fois, plus d activation fantome, vigie-round operationnelle, manifest recharge a chaque tic, ASCII 0, compilation OK. Tests delegues a Morpheus.
## [LECON] 2026-08-28 -- KO PREEXISTANTS CORRIGES + NON-REGRESSION OBSOLETE (Vulcain)

**Contexte** : retour de la chaine Vulcain-Morpheus-Janus (round pilote Oracle + vigie-round). Janus a documente 5 KO preexistants : catalogue 187 vs 186, CRLF residuels, cerberus-freelance cU2, processus daemons, test-082 docstring pilote.py.

**Corrections** :
1. test-082 : faux positif - la docstring '<racine>/tmp-buffy' matchait le motif '>\s?/tmp' (le > de <racine> colle a /tmp). Reformule en '[racine]'. 9/9 OK.
2. test-040 : hades-contexte-git jamais indexe dans index-tools.md (au catalogue depuis sa creation). Section Git creee. 5/5 OK.
3. test-047 CRLF : CAUSE RACINE = write_text/open('w') sur Windows traduisent \n en \r\n. Corrige dans 5 sources oracle (pilote.py, vigie-round.py, routines-server.py, oracle-server.py, oracle-demarrage.py) avec io.open(newline='\n'). Corrige 40+ fichiers existants (parcours, etat-cartes, grades-v1) + 7 fichiers non-ASCII (emoji U+1F7E0, ideogrammes U+51B3, accents). Exclusions par defaut : freelance/ (CRLF volontaire D4) + observations/ (logs daemons generes). 10/10 OK.

**Prise de conscience utilisateur** : LA NON-REGRESSION N EST PLUS VALIDE DEPUIS LA MIGRATION DES AGENTS. Les tests portent des compteurs FIGES : test-005 (parcours-atlas 0.5.4 vs 0.5.7, 13 vs 14 commandes c35), test-013 (27 vs 33 cases action c1h/c20h), test-018 (21 vs 24 parcours : cerberus-freelance/ferrari/redacteur-v2/socrate), valider-cartes hades c5.vers->cerberus (format fin obsolete). Adaptation = domaine MORPHEUS (regle immuable : seul Morpheus ecrit les tests).

**Verdict** : VALIDE - les 3 vrais KO corriges (test-082 9/9, test-040 5/5, test-047 10/10), ASCII 0/0, compilation OK. Tests obsoletes transmis a Morpheus.
## [LECON] 2026-08-28 -- INTER-ROUND DETTES DE CARTES : HADES C5 + CERBERUS C1H* ALLEGES (Vulcain)

**Contexte** : inter-round depuis morpheus (non-regression obsolete depuis migration des agents - tests adaptes par morpheus, dettes de cartes detectees transmises).

**Corrections** :
1. HADES parcours-hades.json case c5 : fin avec champ vers='cerberus' INVALIDE (spec regle 3 : une fin n a ni branches ni suivant). Le champ vers pointait vers un AGENT au lieu d une case - reference cassee valider-cartes --tous. Corrige : champ vers RETIRE (la fin REACTIVER se materialise par la COMMANDE dans le message, comme janus c10). valider-cartes hades CONFORME.
2. PARCOURS-CERBERUS cases c1h/c1hb/c1hc/c1he/c1hf (texte 205 car) + c20h (203 car) : indices regle >160 (commande oracle d historisation). Alleges : suppression du preambule 'apres analyse et comprehension de ma mission' et compaction du texte -> <160 car. valider-case parcours-cerberus CONFORME (0 erreur, 0 a alleger).

**Lecons** :
1. UNE FIN NE PORTE JAMAIS DE CHAMP vers : spec regle 3 - la fin REACTIVER se materialise par la COMMANDE dans le message (comme janus c10, redacteur-v2 c8). Un vers sur une fin = reference cassee silencieuse.
2. LES INDICES REGLE >160 SONT UNE DETTE QUI S ACCUMULE : chaque ajout de case avec une regle longue (ex: commande oracle) fait passer le verdict de CONFORME a A ALLEGER - alleger immediatement en compacant, pas plus tard.

**Verdict** : VALIDE - hades CONFORME, cerberus CONFORME, 0 reference cassee dans valider-cartes --tous, ASCII 0/0, LF pur.

## LECON (inter-round Cerberus 2026-08-28, apres controle Janus)

VERDICT OBLIGATOIRE a chaque correction : relancer le test concerne pour PROUVER le vert (test-055 12/12, test-067 8/8, test-072 10/10, test-080 11/11).

1. LE .sh PARTIEL N EST PAS UN BUG DE VERSION : activer-agent-principal.sh (0.7.4) est l equivalent bash PARTIEL du .py (0.8.2) - les fonctions 0.7.5+ (encart, BDD, grades) sont cote .py uniquement (changelog v0.7.5 'Parite .sh : non concerne'). Bumper le .sh serait un mensonge. Solution : EXEMPTIONS_AUDIT dans mettre-a-jour-versions.py (chemin, version pinnee, raison) - le fichier est compte EXEMPT au lieu d INCOHERENT, et redevient INCOHERENT si bumpe sans retirer l exemption.

2. NE JAMAIS REWRITER UN JSON PARCours EN ENTIER (json.dump) : ca detruit le format compact des branches ({"reponse": ..., "vers": ...}) et cree un diff de 988 lignes pour 3 changements. Toujours faire des replacements CHIRURGICAUX (str_replace sur le texte exact) : diff minimal (5-12 lignes) et format preserve.

3. LES CHEMINS D OUTIL DOIVENT ETRE VERIFIES AU CATALOGUE : consulter-combos est sous consulter/consulter-combos/ (pas combos/consulter-combos/). J ai mis un chemin fantome dans cU2 de cerberus-freelance - corrige apres verification. Toujours verifier le chemin reel avant d ecrire un indice outil.

4. LA FICHE BUFFY DEVIAIT DU TEMPLATE : section '## PARCOURS / ARBRE (SOURCE DE VERITE DU GUIDAGE)' au lieu de '## PARCOURS (SOURCE DE VERITE DU GUIDAGE)'. verifier-conformite-fiche --tous : buffy ECARTS -> CONFORME apres renommage (test-080 11/11).
## LECON (chaine Cerberus 2026-08-28, apres recontrole Janus : 2 problemes OUTIL)

1. ANALYSER-NOMS-MAJ IGNORAIT LES AGENTS FREELANCE ET LA CASSE : lister_agents_reels ne scannait que cerveau-projet/agents/ (pas freelance/) et comparait en casse stricte - 87 entrees AGENT_INCONNU (55 stark + 32 'Cerberus'). Correctif : 2 bases (agents/ + freelance/), comparaison en minuscule (agent.lower() vs nom.lower()).

2. LES OUTILS PLATS SONT INVISIBLES DE lister_outils_reels : la fonction n attendait que tools/<categorie>/<outil>/ (2 niveaux) - oracle.py, routines-server.py, oracle-demarrage.py (scripts directs dans tools/oracle/) etaient OUTIL_ORPHELIN. Correctif : detecter aussi les scripts .py/.sh directs dans un dossier categorie (base_script = nom sans extension, RE_NOMMAGE_OK).

3. LE REGISTRE EST UN ARTEFACT D EXECUTION, PAS UNE SOURCE DE VERITE : mes propres enregistrements --outil tester ont cree des OUTIL_ORPHELIN (le nom canonique est tester-lancer-non-regression). Normalisation du registre : tester->tester-lancer-non-regression, citations->oracle (routine interne oracle), tester-outil->tester-lancer-non-regression (outil supprime). Le registre doit rester PROPRE (test-079).

4. LA GENERATION MERMAID DOIT SUIVRE LES AJOUTS D AGENTS : ferrari et hades avaient des parcours mais AUCUNE vue .mmd/.svg (test-096 6 KO). Regeneration : convertir-carte-mermaid --tous + --tous --svg + --arbres (les arbres v2 stark/vision et les 24 cartes sont maintenant synchronises).

VERDICT OBLIGATOIRE : test-079 15/15, test-096 11/11, registre PROPRE (0 probleme), compile OK, ASCII 0/0.
## [LECON] 2026-08-29 -- COLONNE EXECUTEUR ROUTINES : RT(INTERVALLE) (Vulcain)

**Mission** : la colonne Executeur du tableau AGENTS-activite-recente.md affichait
VIDE pour les entrees historisees par les routines v1 (citations, flux, sante,
live, encart, vigie-round...) : elles appellent ajouter_historique SANS passeur
executeur, donc _ecrire_encart_v1 ecrivait exec_aff = "".

**Diagnostic** : le point d ecriture de la colonne Executeur est _ecrire_encart_v1
(exec_aff = executeur or ""). Les routines passent par ajouter_historique sans
executeur -> colonne vide. Le manifest des routines (oracle/routines/manifest.json)
porte l intervalle (intervalles_secondes) de chaque routine.

**Correction** (activer-agent-principal v0.8.6 -> 0.8.7) :
1. Constante MANIFEST_ROUTINES (chemin ABSOLU comme ETATS_ACTIONS - les routines
   tournent avec cwd=routines/, un relatif serait introuvable).
2. Helper _executeur_routine(agent) : retourne "RT(<intervalle>s)" (ex: RT(300s))
   si l agent est une routine ACTIVE du manifest avec intervalle > 0, sinon "".
3. _ecrire_encart_v1 : exec_aff = executeur or _executeur_routine(agent) or "".
4. _construire_encart_v1 (reconstruction/migration) : meme helper sur la colonne
   Executeur (elle etait codee en dur a vide).

**Verification** : test reel sur copie (env AGENTS_ACTIVITE_RECENTE) -> la ligne
test citations affiche "| Temporaire | citations | 4 | RT(300s) | ...". Test de
reconstruction _construire_encart_v1 -> RT(300s) present. ASCII 0, 0 CRLF,
detecter-decalages-catalogue 0 decalage, bump 0.8.7 (py + md + historique).

**Lecons** :
1. LE POINT D ECRITURE D UNE COLONNE PEUT ETRE DOUBLE : _ecrire_encart_v1 (ajout
   d entree) ET _construire_encart_v1 (regeneration complete depuis le corps) -
   modifier l un sans l autre cree une incoherence a la prochaine migration.
2. L INTERVALLE D UNE ROUTINE VIT DANS LE MANIFEST, PAS DANS LE CODE : lire
   manifest.json (chemin ABSOLU - les daemons lances avec cwd=routines/ ne
   resolvent pas les relatifs) au lieu de dupliquer les durees en dur.
3. TOUJOURS TESTER SUR COPIE : les env AGENTS_* permettent de simuler un
   enregistrement reel sans polluer l encart/le corps (verif de la colonne
   produite, pas seulement de la compilation).

**Verdict** : VALIDE (test reel sur copie OK, ASCII 0, CRLF 0, catalogue 0 decalage).

**Outils utilises** : lire-fichier, editer-fichier, mettre-a-jour-versions,
valider-conformite-ascii, detecter-decalages-catalogue, valider-conventions,
oracle (pilote), enregistrer-usage-outil.
## [LECON] 2026-08-30 -- VERROU BLEU : CROISEMENT ORACLE ADDITIF SANS CASSER (Vulcain)

**Contexte** : mission URGENT (super-combo, chaine socrate -> buffy -> vulcain) - deplacer la source de verite de l habilitation vers l etat du round oracle pour arreter l usurpation d identite (le LLM reecrit AGENTS.md puis deverrouille les outils dedies).

**Diagnostic** : proteger-verrou-habilitation croyait agent_actif_session() (colonne 'Agent actif' d AGENTS.md), un fichier que la session edite directement -> verrou grille a la source. Le DEFCON log du 29/08 le prouve : 'le flux etait casse et le LLM a repris la main'.

**Corrections** :
1. oracle.py 0.5.3 -> 0.5.4 + files.py : mission-lister accepte desormais --statut et --agent (filtres optionnels, la sortie par defaut est INCHANGEE). Permet d interroger 'y a-t-il une mission EN_ATTENTE/PRISE pour tel agent ?'.
2. proteger-verrou-habilitation 0.4.2 -> 0.5.0 : nouvelle option ADDITIVE --verrou-interne. Quand activee, croise oracle (mission-lister --statut EN_ATTENTE --agent X) et BLOQUE si aucune mission relayee prouve l incarnation. Sans l option, comportement INCHANGE (test-056 intact).

**Lecons** :
1. ADDITIF D ABORD : un outil teste (verrou, 100+ tests) se modifie par AJOUT d option, jamais en changeant le defaut - sinon toute la serie KO. Le comportement par defaut reste l ancien ; la nouvelle exigence s active explicitement.
2. BUMBER COMPOSITE = FICHIER CIBLE : le dossier oracle contient plusieurs outils ; je bumpe FICHIER par FICHIER (oracle.py, files.py n a pas de VERSION propre), jamais le dossier (KO incoherence) - lecon deja note.
3. UN BUMP DE VERSION CASSE LE TEST QUI FIGE L ANCIENNE : test-056 fige v0.4.2 en dur ; passer a 0.5.0 rend test-056 KO ATTENDU. Le deleguer a Morpheus pour qu il repointe la version + ajoute le test d usurpation (blueprint critere 2).
4. LES FICHIERS 'FICHIERS' SONT TOUS ECRITS PAR LA SESSION : aucune garde purement extensionelle n arrete un LLM avec acces shell. La vraie autorite = le serveur oracle demarre (processus/PID) + croisement historique coherent (blueprint option c hybride).

**Rappel** : on a ecrit du code AVANT de bumper les versions : implementation puis bump, dans cet ordre.
