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

## [LECON] 2026-09-02 -- CONSOMMATEUR [NOTATION] : oracle.py v0.5.9 (mission eaa954a0)

**Contexte** : les demandes d evaluation croisee de la routine notation
(deposees dans l inbox d Oracle toutes les 960s) n etaient JAMAIS prises en
compte - Oracle acquittait par habitude et la rotation purgeait. Fix :
`_consommer_notation()` convertit chaque demande [NOTATION] en mission Themis
(hooks cmd_lire + cmd_acquitter) avec anti-inondation (mission EN_ATTENTE +
delai 60 min).

**Lecons** :
1. Un hook dans cmd_acquitter doit s executer AVANT la suppression du message
   (le message acquitte est RETIRE du fichier - le consommateur ne le verrait
   plus apres).
2. Les routines peuvent deposer a l infini : l anti-inondation est
   indispensable (mission EN_ATTENTE + delai temporel) pour eviter la
   surcharge de la file.
3. Test reel indispensable : injecter un message dans l inbox, declencher la
   lecture, verifier la mission dans la file + les marqueurs sur le message.

## [LECON] 2026-09-02 -- ETATS DE VOL DU PILOTE DANS LA COLONNE ETAT : etats-actions.json v0.1.2

**Contexte** : l utilisateur a vu dans AGENTS-activite-recente.md la ligne
pilote `RETOUR AEROPORT: oracle` classee DEBUT dans la colonne Etat -
incoherent. Cause : etats-actions.json reglait DEBUT avec les prefixes
[DEBUT, RETOUR] : toute raison commencant par RETOUR (y compris les
phases de vol du pilote) etait classee DEBUT a tort ; RECUPERE,
DECOLLAGE et LARGUE ne matchaient aucune regle -> defaut ACTIF.

**Correction (etats-actions.json v0.1.1 -> v0.1.2, decision utilisateur
2026-09-02 : etats calques sur l action)** : 4 nouveaux etats de vol
places AVANT DEBUT (l ordre du fichier compte, la premiere regle qui
matche gagne) : DECOLLAGE (prefixe DECOLLAGE), RECUPERE (prefixe
RECUPERE), RETOUR (prefixe RETOUR AEROPORT), LARGUE (prefixe LARGUE).
DEBUT ne matche plus RETOUR seul - remplace par RETOUR ORACLE (les
agents reellement reactives via Oracle restent DEBUT). Docstring de
_etat_action (activer-agent-principal.py) aligne - seules les data ont
change, pas le code (pas de bump d activer-agent-principal).

**Preuves** : 1) json valide, 2) _etat_action 8/8 OK (4 vols pilote
-> leurs etats ; RETOUR ORACLE : ... -> DEBUT ; DEBUT -> DEBUT ; FIN ->
FIN ; oracle -> ACTION), 3) traces reelles AGENTS-historique (pilote)
classent RETOUR/RECUPERE correctement, 4) encart charge dynamiquement
les etats connus depuis le fichier (pas de pin), 5) syntaxe / ASCII 0/0
/ CRLF 0/0.

**Lecons** : 1) un prefixe commun (RETOUR) dans une regle de detection
devore toutes les raisons qui le portent - une etiquette de vol de
l aeroport (RETOUR AEROPORT) n est pas un DEBUT de mission ; 2) quand
les regles vivent dans un fichier data, la PRIORITE est l ordre des
regles dans le fichier : les plus specifiques passent avant les plus
generales.

## [LECON] 2026-09-02 -- ORDRE TRACE PILOTE RETOUR AEROPORT vs ATTERRISSAGE CERBERUS : pilote.py v0.2.3

**Contexte** : l utilisateur a detecte dans AGENTS-historique que la
fin-coordination d ORACLE affichait l activation de CERBERUS (RETOUR
ORACLE 18:44:27.882) AVANT la trace pilote RETOUR AEROPORT (18:44:28.000)
- ordre semantiquement inverse : on lisait l atterrissage avant le retour
a l aeroport. Verification : dans _reactiver_maillon (fonctions/pilote.py),
l ordre reel des operations etait : 1) _fin_auto pose FIN oracle ;
2) aap.activer_cerberus ACTIVE Cerberus et ecrit RETOUR ORACLE ; 3) PUIS
_historiser_pilote(RETOUR AEROPORT) dans le bloc rc==0. L activation
precedait donc la trace du retour. Defaut secondaire : _historiser/
_activer_maillon tronquaient a la seconde (%H:%M:%S.000 fixe) alors
qu activer-agent-principal et les routines ecrivent de vrais ms (%f) :
l ordre inter-ecrivains etait illisible (le round 18:22 semblait correct
par artefact de troncature, pas par ordre reel).

**Corrections (pilote.py v0.2.2 -> 0.2.3)** :
1. Branche cible=cerberus de _reactiver_maillon : quand c est
   l aeroport (oracle/pilote) qui termine (fin de round -> atterrissage
   sur Cerberus), _historiser_pilote(RETOUR AEROPORT) est appele AVANT
aap.activer_cerberus (modele aero : FIN -> RETOUR AEROPORT ->
atterrissage Cerberus). Anti-doublon dans le bloc rc==0 (deja_trace).
2. _historiser et _activer_maillon : vrais millisecondes
   (%H:%M:%S.%f tronque a 3) au lieu de .000 fixe - aligne sur
   activer-agent-principal et les routines (encart/flux/notation).

**Preuves** : 1) ordre code verifie (RETOUR AEROPORT pos 1060 <
activer_cerberus pos 1119 dans la branche) ; 2) anti-doublon present ;
3) plus aucun %H:%M:%S.000 dans pilote.py ; 4) test-115 (flux R7)
9/9 OK, test-102 (ms) 6/6 OK, test-098 6/7 (1 KO PRE-EXISTANT bloc
Inconnu Hygie 14:49, hors perimetre - deja documente mission 9e00c945),
verifier-flux-securite reel : seul R1 vulcain actif (moi, normal) ;
5) ASCII 0/0, CRLF 0/0, syntaxe OK.

**Lecons** : 1) L ORDRE D ECRITURE DANS L HISTORIQUE EST L ORDRE DU
CODE, pas l ordre semantique : si une trace de vol est posee dans un bloc
rc==0 APRES l action qu elle decrit, l historique raconte l inverse du
modele. Tracer la phase AVANT l action qu elle introduit (retour aeroport
avant atterrissage). 2) PRECISION DES HORODATAGES : melanger .000 fixe
et ms reels rend l ordre inter-ecrivains illisible - un .000 fixe peut
faire paraitre correct un ordre faux (artefact de troncature). Tout
producteur d historique doit ecrire de vrais ms.

## [LECON] 2026-09-02 -- VERIFIER-FLUX-SECURITE R7 FAUX POSITIF LARGAGE : v0.2.2 (mission 31fe865e)

**Contexte** : inter-round apres la fin Morpheus (ca722bea). Le pilote
signalait FLUX KO R7 a chaque reactiver-fin : 'FIN de vulcain -> prochain
agent morpheus' alors que la sequence respectait le modele aero (fin ->
aeroport -> largage).

**Cause racine** : le scan R7 cherchait le prochain agent en SAUTANT
_est_coordination (oracle/pilote/cerberus). Or le flux reel apres une fin
est : FIN agent -> pilote 'RECUPERE: X' -> oracle 'DEBUT: RETOUR X' ->
pilote active le suivant. En sautant les lignes RECUPERE/RETOUR, le scan
trouvait l agent LARGUE (morpheus ACTIF 15:05:51 apres FIN vulcain
15:03:35) et criait au KO a tort.

**Fix v0.2.2** : le scan s arrete au premier evenement non-routine /
non-citation. Aeroport (oracle/pilote) = OK (la fin a bien ete recue, la
preuve 'DEBUT: RETOUR X' agent=oracle est presente). Cerberus = OK
seulement en atterrissage terminal (rien ne redecoule au-dessus). Un agent
METIER direct apres une fin (sans passage par l aeroport) reste une
violation R7.

**Preuves** : 4 scenarios synthetiques - (S1) fin -> agent metier direct
= KO capture ; (S2) fin -> RECUPERE+RETOUR -> largage = OK ; (S3) fin en
tete = OK ; (S4) fin -> RECUPERE seul -> largage = OK. Tableau reel :
FLUX OK (etait 2 KO). Version py 0.2.2, doc .md alignee (frontmatter
0.1.0 perime -> 0.2.2, regle R7 + changelog). ASCII 0/0, CRLF 0/0,
syntaxe OK. Tests delegues a Morpheus (regle immuable).

**Lecon** : un controleur de flux qui SAUTE la coordination pour chercher
le prochain evenement perd LA PREUVE que la fin est bien passee par
l aeroport - le largage du pilote est le SUIVI normal d une fin, pas une
violation. Un scan de flux doit respecter l ordre reel des evenements
(ne jamais sauter les maillons qui portent la preuve).

## [LECON] 2026-09-02 -- SECTEURS FONCTIONNELS : grades-v1.json v0.2.0 (mission 30d8322e)

**Contexte** : l utilisateur a signale [urgent] que la colonne Secteur de
AGENTS-activite-recente.md affichait encore des dieux grecs (Olympe,
Athena, Hephaistos, Areopage...) alors que le passage v2 avait rendu ces
mots sans signification fonctionnelle. La mission 30d8322e (prise a
11:16:57) n avait JAMAIS ete executee - elle etait restee bloquee en
PRISE : l encart etait regenere par le daemon depuis grades-v1.json, donc
les nouvelles lignes gardaient les anciens labels tant que le fichier de
mapping n etait pas modifie.

**Cause racine** : le mapping des secteurs vivait dans grades-v1.json
(cle secteurs.mapping) avec des valeurs grecques (Olympe = coordination,
Athena = developpement, Areopage = controle/tests/evaluation, etc.).
Deux consommateurs : _secteur_label d activer-agent-principal (nouvelle
entree) et la lecture du daemon encart (relecture du tableau). Aucun
test ne pinnait les valeurs grecques - le changement etait donc sans
risque de regression cote tests.

**Fix** : remplacement par 18 categories fonctionnelles ASCII minuscules
(coordination, developpement, tests, controle, evaluation, strategie,
communication, exploration, securite, surveillance, traces,
documentation, specification, planification, formation, nettoyage,
systeme, general) avec mapping par nom d agent ou mot-cle de role (93
cles). Nouvelle entrees : pilote/retour-aeroport/decollage ->
coordination, nemesis/hades -> evaluation/traces, routines de
surveillance (flux, sante, live, encart, vigie, top3, verifier-statuts)
-> surveillance/sante. Defaut 'General' -> 'general'. Description du
fichier alignee (les dieux grecs restent dans l IDENTITE des agents -
citations.py - pas dans les secteurs d activite).

**Regressions evitees** : (1) a la reecriture de la colonne Secteur du
tableau (50 lignes), attention aux INDICES - dans une ligne du tableau
decoupee par '|', Agent = colonne 2 et Secteur = colonne 6 (pas 3 et 7)
; (2) la restauration du bloc routines ne doit PAS revenir a l etat
HEAD : le pilote (grade SP) etait declare dans l arbre de travail par la
mission urgente 801f952d - le reverter a fait reapparaitre 'Inconnu' en
colonne Grade (detecte par l encart a 15:54:36, corrige en remettant
"pilote": "SP").

**Preuves** : grades-v1.json v0.2.0 - JSON valide, ASCII 0/0, CRLF 0/0,
94 cles de mapping, 18 valeurs fonctionnelles uniques, aucun dieu grec
residuel dans le tableau (grep = 0), encart --dry-run = OK, pilote ->
Special/coordination. Invariants vs HEAD : version/echelle/agents/defaut
inchanges, seulement description + routines (pilote SP) + secteurs
modifies.

**Lecon** : une mission restee PRISE sans etre executee laisse la
REALITE (les mots affiches) inchangee - le mapping vit dans un fichier
data consomme par les daemons ; verifier AVANT de conclure qu une tache
est faite, et toujours verifier l alignement fichier-data <-> fichier-
affichage. Ne jamais restaurer un bloc JSON depuis HEAD sans verifier
les declarations ajoutees par les missions en cours (le pilote SP etait
un ajout non-commit de la mission urgente Inconnu).

## [LECON] 2026-09-02 -- FIN D ORACLE -> CERBERUS (fin de round) : decision utilisateur

**Contexte** : l utilisateur a observe que chaque fin de mission aboutissait
en boucle 'pilote -> oracle -> pilote -> oracle...'. Il a precise : le
pilote n est PAS en cause ; seul la fin d ORACLE (l aeroport) etait a
verifier. Modele attendu : oracle avertit puis active cerberus ->
cerberus finit la mission avec le bilan (cerberus = point de
Depart/arrivee des demandes utilisateur).

**Cause racine** : la carte d oracle (oracle/parcours/fins.json) portait
TOUTES ses fins (fin-coordination, fin-signal, fin-inter-round) en
cible=oracle + '--cible oracle' : oracle se reactivait lui-meme a chaque
fin. Le pilote avait deja la branche cible=cerberus (activer_cerberus +
mission_type=RETOUR + theme-de-oracle cote cerberus) mais elle n etait
JAMAIS atteinte car la carte forqait --cible oracle. Boucle infinie,
la chaine ne retombait jamais sur cerberus avec le bilan consolide.

**Fix (decision utilisateur : seule fin-coordination atterrit sur
cerberus)** :
  1. oracle/parcours/fins.json : fin-coordination -> cible=cerberus +
     commande --cible cerberus (bilan consolide de coordination).
     fin-signal et fin-inter-round RESTENT cible=oracle (le pilote
     decide du suivant).
  2. pilote.py (_executer_fin_oracle) : le message 'cible=cerberus =
     VESTIGE v1' exemPE desormais l agent oracle (fin de round
     legitime, exception decision 2026-09-02).
  3. auditer-conformite-arbre : _f4(fins, agent) + besoins-v2.json F4
     documentes - exception oracle/fin-coordination -> cerberus.
  4. detecter-fins-passives : CIBLE_NON_ORACLE exemPE le couple
     (agent=oracle, nom_fin=fin-coordination, cible=cerberus).

**Regle _reactiver_maillon verifiee** : la ligne 'oracle atterrit
TOUJOURS sur l aeroport' ne s applique que si cible_forcee est VIDE.
Avec '--cible cerberus' (cible_forcee=cerberus), la branche
elif cible==cerberus s execute -> Cerberus est active avec le bilan.

**Preuves** : test bout-en-bout reactiver-fin oracle --cible cerberus ->
'Cerberus reactive avec succes', raison 'RETOUR ORACLE : COORDINATION
TERMINEE', etat de carte mission_type=RETOUR ; auditer-conformite-arbre
--agent oracle -> F4 OK (exception) 18 OK / 0 bloquant ;
detecter-fins-passives -> 30 agents, 0 probleme ; syntaxe/ASCII/CRLF
0/0 sur les 6 fichiers touches.

**Lecon** : (1) ne jamais confondre 'la carte d un agent fixe la cible'
et 'le pilote decide' - si la carte force --cible oracle, la branche
cerberus du pilote est morte ; (2) une modification de carte doit
verifier TOUS les garde-fous qui scrutent la structure (test-114,
auditer-conformite-arbre F4, detecter-fins-passives) - deleguE a
Morpheus via mission fe00998c pour test-114 ; (3) toujours confirmer
au pres de l utilisateur quelle fin precise doit changer (ici : seule
fin-coordination, pas fin-signal/fin-inter-round).

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

## [LECON] 2026-09-02 -- AGENT CREE MAIS INACTIVABLE : NEMESIS BRANCHE A L ACTIVATION (Vulcain)

**Contexte** : la creation de l agent v1 nemesis (Buffy, theme AGENT) a reproduit le pattern connu : agent cree (fiche, corrections, arbre, AGENTS.md) mais ABSENT du dictionnaire AGENTS de activer-agent-principal -> inactivable. 4e occurrence (Argus v0.5.8, Chiron v0.5.12, ferrari v0.7.4, maintenant nemesis 0.8.9).

**Realise** : (1) dictionnaire AGENTS du .py : entree nemesis (role + fiche agents/nemesis/nemesis.md + corrections) ; (2) 3 case statements du .sh (role, fiche, corrections) ; (3) couleur nemesis (#6d28d9) ; (4) bump 0.8.8 -> 0.8.9 (py, md, spec) ; (5) enseignement : le verrou-habilitation attend --agent <nom> pour autoriser les edits sous agents/tools/ - sans --agent, le verrou dit agent appelant: ? et BLOQUE meme si la session est activee sur vulcain.

**Lecons** :
1. LE PATTERN AGENT CREE MAIS INACTIVABLE RECIDIVE (4e fois) : le theme AGENT de Buffy cree l agent mais AUCUNE etape ne branche l outil activer-agent-principal - soit le theme AGENT gagne une etape de verification, soit le controle Janus/Themis doit le detecter avant de declarer l agent disponible.
2. LE VERROU CIBLE TOOLS LIT --agent PASSE EN ARGUMENT, PAS LA SESSION : editer-fichier sous agents/tools/ exige --agent vulcain explicite ; l activation de la session (profil session) ne suffit pas - le verrou affiche agent appelant: ? et bloque.
3. LES APOSTROPHES DANS UNE COMMANDE BASH CASSENT LA LIGNE : un echo avec 'Oui, mais...' passe dans une commande editer-fichier sans heredoc tronque la ligne au premier apostrophe - utiliser des variables bash single-quote ou heredoc pour les contenus avec apostrophes.

**Verdict** : VALIDE - get_agent_info(nemesis) OK, syntaxe py + bash OK, ASCII 0/0 sur py/sh/md/spec, test-092 et bump de version transmis a Morpheus.


## [LECON] 2026-09-02 -- OUTIL DETECTEUR : CIBLE = DOSSIER DES AGENTS, PAS DOSSIER D'UN AGENT
Lors du test formel test-112 de detecter-fins-passives, les preuves factices
etaient K.O car le test passait le DOSSIER DE L'AGENT (tmp/zz-passif) comme
CIBLE, alors que l'outil attend le DOSSIER DES AGENTS (dossier contenant les
sous-dossiers d'agents, par defaut cerveau-projet/agents/). Le scan listait
alors 'parcours' comme un pseudo-agent sans fins.json -> 0 probleme, RC=0.
CORRECTION : passer la racine des agents + filtrer avec --agents <factice>.
LE VERDICT D'UN DETECTEUR SE PREUVE SUR UNE FIXTURE AU BON NIVEAU DE LA
HIERARCHIE : le niveau CIBLE et le niveau des sous-dossiers analyses doivent
respecter le contrat de l'outil.


## [LECON] 2026-09-02 -- D6/D7 APPLIQUE : ANTI-HEREDOC + EXECUTER-FORMULAIRE + INJECTION P2

**Contexte** : propositions Socrate (via utilisateur) relayees en 2026-09-02 :
(1) l agent ne compose plus les commandes (decision D6/D7 2026-08-21, jamais
implementee) et les outils simples doivent accepter de LONGUES instructions
sans heredoc bash (contenus tronques vecus dans les rounds) ; (2) le pilote
injecte la mini-description + la liste des flags avec la mission.

**Realise** :
1. Anti-heredoc : creer-fichier v0.3.3 et ecrire-fichier v0.3.3 gagnent
   --contenu-chemin <fichier> ; editer-fichier v0.5.1 gagne
   --remplacements-chemin <fichier.json> ([{ancien, nouveau, premier?}]).
   Le contenu est TOUJOURS lu depuis un fichier, jamais d argument bash
   geant. Pattern deja present chez ajouter/inserer (--fichier SOURCE).
2. executer-formulaire v0.1.0 (categorie executer, triplet py/sh/md) :
   --schema affiche description + champs (cle/type/requis/flag/defaut) et
   un exemple de fichier de reponses ; --reponses <json> VALIDE (refus
   AVANT execution si requis manquant, RC=1) puis COMPOSE depuis le modele
   du catalogue et EXECUTE a la place de l agent (D6).
3. Injection P2 : files.py (oracle v0.5.7) injecte un bloc [OUTIL]
   (description + flags) par outil du catalogue mentionne (max 3), a
   l ajout de mission. Catalogue maj (creer/ecrire: parametre
   contenu-chemin).

**Lecons** :
1. DECISION EXISTANTE != IMPLEMENTATION : D6/D7 datait du 21/08, aucune
   mise en oeuvre 12 jours apres - quand une decision utilisateur reste
   lettre morte, la relancer explicitement (ici c est Socrate qui l a fait).
2. FLAG TEXTE DANS LE MODELE DE CATALOGUE : un parametre texte avec champ
   flag (--contenu-chemin) doit etre compose en DEUX argv (flag + valeur),
   pas en un seul - bug attrape au test (commande b.md src.txt au lieu de
   b.md --contenu-chemin src.txt).
3. LE NEWLINE FINAL EST UN CONTRAT : creer/ecrire-fichier ajoutent un 

   final (historique) - les tests comparent apres rstrip, pas a l identique.
4. TEST FORMEL AVANT FIN : test-113 (11 points) couvre les 3 modes
   anti-heredoc, le formulaire (schema/refus/execution/dry-run) et
   l injection P2 - non-regression test-003 89/89 + test-092 9/9.

**Preuves** : test-113 11/11, creer 15 Ko sans troncature, refus RC=1
(requis manquant), injection P2 OK, ASCII 0/0, catalogue/fichiers
synchronises.
## [LECON] 2026-09-02 -- FILE DE RELAIS ORDONNEE + CLASSIFIEE : oracle v0.5.8 (Vulcain)

**Contexte** : decision utilisateur [attention] - le relais (oracle.py mission-relais / files.py) consommait la file asap en FIFO strict : une mission EN_ATTENTE vieille partait avant un message plus recent potentiellement PLUS IMPORTANT. Demande : ordonner la file par importance (priorite puis anciennete, P1 avant P2, recent avant ancien a importance egale) et la classifier (type de mission).

**Realise** (outils : lire-fichier, editer-fichier, mettre-a-jour-versions, valider-conformite-ascii, detecter-decalages-catalogue, oracle) :
1. fonctions/files.py : nouvelle fonction classifier(mission) -> (priorite 1/2, type urgent/purge/revision/test/creation/coordination) par mots-cles ([urgent]/[attention]/etat urgent/purge p1/P1 non-acquitte/anomalie/defcon -> P1 ; sinon P2). ajouter() stocke priorite+type a l ajout. prendre() ne prend PLUS la 1ere ligne : il selectionne la mission EN_ATTENTE la PLUS IMPORTANTE (priorite basse puis DATE RECENTE d abord - tri stable, entrees sans date en fin). lister() affiche Px/type et trie par importance. relais() porte la classification.
2. oracle.py VERSION 0.5.7 -> 0.5.8 ; oracle.md 0.5.3 -> 0.5.8 avec entree versionning.
3. Preuves : test reel sur FILES_DIR temporaire - ordre de prise = [P1/urgent, P1/purge, P2/test(recent), P2/revision(ancien)] VALIDE ; syntaxe ast OK x2 ; ASCII 0/0 x3 ; catalogue 188 conformes/0 decalage. Bump manuel (le bumper de dossier oracle bloque : 6 versions independantes dans le dossier - sous-outils separement versionnes).

**Lecons** :
1. UNE FILE N EST PAS UNE FIFO PAR DEFAUT : l ordre de consommation d une file de travail doit reflete l IMPORTANCE (priorite explicite ou deduite), pas l anciennete brute - le FIFO strict fait patienter un message URGENT derriere une chaine de vieilles missions.
2. LA PRIORITE SE DEDUIT AU DEPOT (classifier a l ajout) ET SE RE-DEDUIT AU TRI pour les anciennes entrees sans champ : le tri est retro-compatible sans migration des jsonl existants.
3. LE TRI PAR DATE DESC PREND 1 LIGNE AVEC DES TUPLES : (priorite, tuple(-ord(c) pour c in date)) - comparer des dates ISO par inversion de chaque octet donne l ordre inverse lexicographique sans parser les dates.
4. LE BUMPER DE DOSSIER REFUSE UN DOSSIER MULTI-VERSIONS : oracle/ contient oracle.py 0.5.7, oracle-demarrage 0.1.1/0.1.3, oracle-server 0.2.0, routines-server 0.2.0/0.2.1, oracle.md 0.5.3 - passer le bump a l outil individualise (--parcours/<fichier>) ou manuel quand le dossier est multi-outils.

**Verdict** : VALIDE (sous test Morpheus 52ceaea1) - ordre de prise prouve P1 avant P2 puis recent avant ancien, ASCII 0/0, catalogue 0 decalage.
2026-09-02 | CORRECTION DOC oracle.md (retour Morpheus) : une mission ne doit PAS contenir le mot-cle 'inter-round' dans sa raison si elle est en realite une modification - le pilote deduit le theme par mots-cles et se trompe de branche (theme-inter-round au lieu de theme-modifier). Reclasser la mission au depot (raison commencant par le verbe Modifier...) pour que le pilote serve le bon theme. Les corrections doc mineures dans une version deja bumpee (0.5.8) ne necessitent PAS de re-bump : la doc est corrigee dans la meme version.
2026-09-02 | REFS PARCOURS V1 DANS LES OUTILS (mission 622127e3, suite cb6eb3ec) : demarrer-llm.py gardait un repli v1 (branche elif parcours-<agent>.json affichant guider-parcours) obsolete depuis que TOUS les agents ont un arbre v2 - retire (v0.1.1 -> v0.1.2) ; editer-parcours.md clarifie qu il ne sert qu a la MAINTENANCE des archives v1 (marbre) et jamais a creer/guider du v1. Lecons : (1) verifier l etat reel avant de garder un repli v1 - scan : 0 agent sans arbre v2, donc tout repli guider-parcours est du code mort actif ; (2) les outils qui chargent parcours-*.json sont LEGITIMES s ils maintiennent/auditent l archive v1 (editer-parcours = compagnon du cartes-lock, detecter-contradictions audite des copies) - c est le POINTEUR de guidage actif (fallback demarrage) qui doit disparaitre ; (3) les .md d outils v1 peuvent porter une note ARCHIVE sans bump de code (doc seule).
2026-09-02 | URGENT ENCART DETECTION INCONNU (mission 801f952d) : la routine encart verifiait Etat/Executeur mais PAS Grade/Agent - des acteurs systeme non declares (pilote) affichaient grade 'Inconnu' SANS alerte. Fix : (1) grades-v1.json declare 'pilote' (routines, grade SP) - un acteur systeme legitime doit etre DECLARE au mapping sinon il pollue la colonne Grade ; (2) encart.py v0.3.1 detecte grade 'Inconnu' + agent hors mapping (helper _agents_connus). Lecon : quand une routine surveille un tableau genere, chaque COLONNE denombrant des acteurs doit croiser le mapping de reference - une colonne sans controle laisse les acteurs non declares s afficher en 'Inconnu' indefiniment ; le test synthetique (fichier temp + GRADES_V1 pointe sur le vrai fichier) valide la detection sans toucher le fichier reel.
2026-09-02 | ORDRE DES DEFINITIONS AU MODULE (inter-round Hygie, mission cd5bc94c) : super-pilote v0.2.1 etait INDEMARRABLE - NameError a l import car PID_FILE = SUPER_COMBOS_DIR / ... etait evalue AVANT la definition de SUPER_COMBOS_DIR (lignes 47/51). Personne ne l a vu car les 9 daemons tournaient depuis AVANT le fix (ancien code en memoire) : la relance de la purge Hygie a revele le bug. Fix v0.2.2 : PID_FILE deplace APRES les definitions de chemins (ORACLE_DIR, SUPER_COMBOS_DIR). Lecon : une constante composee d une autre constante du module doit etre declaree APRES elle ; apres un fix de daemon, TOUJOURS tester le demarrage reel (--boucle) et pas seulement la compilation - un test-085 vert ne prouve pas qu un daemon demarre, il prouve qu il est whiteliste. Preuve : python3 super-pilote.py --boucle -> daemon lance, super-pilote.pid ecrit (PID vivant), detecteur 0 residuel, test-085 8/8.
2026-09-02 | ADAPTATION PURIFIER-RVAV v0.1.1 -> v0.1.2 FORMAT V2 AGENTS-HISTORIQUE (demande utilisateur) : l outil decoupait encore le format v1 '| <span' (0 occurrence depuis la migration v2) et supposait ancien-en-haut. Le format reel v2 (## date + ### agent + entrees '- hh:mm...') est RECENT-EN-HAUT avec des sections non triees entre elles : archiver les blocs du haut aurait deplace les RECHTS au lieu des anciens - bombe a retardement des le depassement du quota. Fix : decoupage v2 par entree individuelle (date+agent+heure portes), tri par (date, heure) pour archiver les PLUS ANCIENNES, suppression des sections agents et dates devenues vides. Corrections.md inchange (blocs ## [LECON] ancien-en-haut). Preuves sur copie reelle : 513 -> 197 lignes, 0 perdu / 0 doublon, accumulation anti-ecrasement (374 = 299+75), ASCII/LF 0/0, structure v2 conservee (16 sections). Lecon : un outil qui parse un format de fichier DOIT etre re-teste contre le format reel apres une migration de structure - le format vivant a change et l outil ne le voyait pas (test-065 ne couvre que corrections.md, pas l historique v2).
