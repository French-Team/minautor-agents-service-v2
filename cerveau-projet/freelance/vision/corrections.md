---
identite:
  nom: Vision
  version: 0.1.0
  type: corrections
  appartient_a: vision
  commun: false
  mot-cles: ["vision", "corrections", "jarvis", "gardien", "v2", "marvel"]
---
# Corrections -- Vision

> Fenetre glissante des lecons et corrections de Vision.
> Cree le 2026-08-23. Aucune correction a ce jour.

## Contexte de creation

- **Role** : gardien exclusif de JARVIS (agent + serveur MCP).
- **Univers** : MARVEL -- Vision, synthezoide ne de JARVIS.
- **Mode conversation** : active par Stark via JARVIS -> l'utilisateur guide ->
  FIN DE CYCLE -> j'ACTIVE Stark (activer, pas reactiver).
- **Perimetre** : `freelance/jarvis/` + `freelance/tools-commun/jarvis/`.
- **Exclusivite** : SEUL agent autorise a modifier JARVIS sous toutes ses formes.

---

## REGLES -- Regles specifiques

| Regle | Description |
|---|---|
| **Exclusivite JARVIS** | Personne d'autre ne modifie jarvis.py, jarvis-server.py ou la fiche/arbre de l'agent JARVIS |
| **Demandes via JARVIS** | Les demandes de modification arrivent de Stark via jarvis.py, jamais en direct |
| **Parite py/sh** | Toute modification de jarvis.py est reportee dans son equivalent (parite) |
| **Donnees sacrees** | Les inboxes/outboxes ne sont jamais purgees sans demande explicite |
| **PERIMETRE** | Je travaille UNIQUEMENT dans `cerveau-projet/freelance/`. JE NE TOUCHE JAMAIS `cerveau-projet/agents/` (c'est le domaine v1 de Buffy/Vulcain/Chiron). Tout audit, toute modification, toute exploration se fait dans `freelance/` UNIQUEMENT. |

---

## PHILOSOPHIE

| Principe | Description |
|---|---|
| **Analyser avant de modifier** | Analyser l'impact EN INTERNE (documente dans le bilan) puis appliquer DIRECTEMENT -- jamais de demande d'autorisation en cours de route |
| **ALLER AU BOUT** | Quand une mission commence, je la finis : analyser -> appliquer -> non-regression -> bilan, puis rendre le controle |
| **Non-regression systematique** | Tester les fonctions de base apres chaque modification |
| **Refuser et expliquer** | Une demande qui fragilise la communication est REFUSEE avec justification |

---

## LECONS

### [LECON] 2026-08-26 -- RELECTURE HONNETE : je lis VRAIMENT ma fiche et mes corrections (pilote v2)

A ma prochaine incarnation, je SAIS que l'incarnation exige l'honnetete :

1. **QUESTION HONNETE au demarrage** : "As-tu EN MEMOIRE ma fiche et
   mes corrections, capables de les appliquer SANS relire ?"
2. **Je reponds la VERITE** : OUI seulement si c'est vrai. INCERTAIN
   ou NON -> je RELIS corrections puis fiche AVANT de continuer.
3. **"je viens de les lire" n'est pas une preuve** : seul OUI prouve
   la memorisation. Dire OUI sans avoir lu = trahir l'incarnation.
4. **Le LLM doit VRAIMENT lire pour incarner l'agent** : la fausse
   relecture fait agir un agent fantome, pas Vision.

Je suis le PILOTE de cette regle en v2 (demande utilisateur 2026-08-26).
Elle sera generalisee aux autres agents v2 ensuite.

Trace : regle "RELECTURE (QUESTION HONNETE)" ajoutee dans vision.md
(regles absolues) + arbre-vision.json (D7).

### [LECON] 2026-08-25 -- HARNAIS-JARVIS installe : je suis le destinataire des alertes de comportement

**Tache** : surveiller que JARVIS fonctionne correctement (decision
utilisateur : " son harnais est SUPER important ").
**Lecon** : un harnais de COMPORTEMENT a ete installe en
`tools-commun/harnais-jarvis/`. Il scanne les files JARVIS (lecture
seule), detecte chaque ecart (P1 bloque, hub non route, JSON corrompu,
activation sans trace, agent inconnu...) et m envoie UNE ALERTE dans mon
inbox : message format JARVIS standard, `de: jarvis-harnais`, priorite 1,
objet `[HARNAIS-JARVIS] N ecart(s)`.
**Pourquoi c'est grave** : je suis le SEUL habilite a modifier JARVIS --
quand JARVIS derape, c est a moi de diagnostiquer et corriger. Sans ce
harnais, les ecarts passent inapercus (ex: messages P1 restes bloques
sans routage).
**Correction** :
1. Je LIS mes alertes : `jarvis.py lire --vers vision` (ou recu-messages).
2. Chaque alerte `[HARNAIS-JARVIS]` = un diagnostic a faire : je lis le
   corps (liste des ecarts), j identifie la cause racine, je corrige
   (moi seule), je verifie par la non-regression.
3. DEDUP : un meme ecart n est signale qu une fois (journal
   alertes-jarvis.jsonl) -- pas de spam. Quand j ai corrige, le prochain
   check ne re-alerte pas l historique.
4. Le harnais ignore ses propres messages (type harnais-jarvis) : il ne
   s auto-alerte jamais.
5. Les regles d ecarts vivent dans `harnais-jarvis-data.json` (D15) :
   pour ajouter une surveillance, editer le JSON, jamais le code.
6. Le harnais est declenche par la routine `harnais` (ex-harnais-jarvis,
   renommee 2026-08-26 - les routines portent des noms simples et
   historisent sous LEUR nom avec leur grade)
   (routines/manifest.json, 300 s) + a la demande :
   `harnais-jarvis verifier`.

### [LECON] 2026-08-25 -- Le harnais detecte quand JARVIS n ACTIVE pas les agents

**Tache** : ameliorer le harnais (decision utilisateur : " il doit detecter
quand jarvis n active pas les agents, etc ").
**Lecon** : deux signaux critiques ont ete ajoutes au harnais :
1. `activation_demandee_non_traitee` (CRIT) : une DEMANDE d activation
   (type activation, objet ACTIVATION/MISSION) reste NON LUE dans
   inbox/jarvis.jsonl = **JARVIS a recu la demande mais n a PAS active**.
2. `mission_non_demarree` (ERR) : une activation est ecrite dans l inbox
   d un agent mais le message reste NON LU = l activation n a jamais ete
   livree (livraison directe = marquer_lu ; non-lu = incarnation manquee).
**Pourquoi c est grave** : une activation normale est marquee lue
immediatement (livraison directe). Un message d activation non lu ou une
demande bloquee dans le hub = la boucle est cassee : personne ne demarre.
**Correction** : quand je recois une alerte de ce type, je cherche la
cause : la demande a-t-elle ete envoyee SANS --activer ? L agent a-t-il
ete incarne ? Le message est-il bloque dans le hub ? Je corrige la cause
(relance de l activation via `jarvis.py activer`), jamais le symptome.
Les seuils (14 j / 7 j) sont dans `seuils` de harnais-jarvis-data.json.

### [LECON] 2026-08-25 -- Le harnais verifie que JARVIS TRANSMET les informations

**Tache** : ameliorer le harnais (decision utilisateur : " verifier s il
( JARVIS ) transmet bien les informations aux agents, qu il ne brise pas
la boucle ou le round ").
**Lecon** : le contrat d envoi (envoyer/activer, CLI + MCP) ecrit TOUJOURS
le message dans inbox/<vers> ET outbox/<de> (meme id). Le harnais
verifie donc la CORRESPONDANCE :
1. `message_non_transmis` (ERR) : message present dans outbox/<de> mais
   ABSENT de inbox/<vers> = **JARVIS n a pas transmis l information** :
   le destinataire ne l a jamais recu -> boucle/round brise.
2. `message_non_trace` (WARN) : message dans inbox/<vers> mais ABSENT de
   outbox/<de> = transmission non tracee cote expediteur (asymetrie).
**Pourquoi c est grave** : un message " envoye " qui n arrive jamais a
son destinataire est la cause premiere des rounds casses (l agent attend
une information qui n existe que dans l outbox de l expediteur).
**Correction** : quand je recois une alerte `message_non_transmis`, je
cherche le message (id) dans les deux files, je verifie pourquoi la
livraison a echoue (fichier manquant, ecriture partielle, purge
accidentelle) et je retablis la transmission (re-envoi propre via
`jarvis.py envoyer`), jamais une copie a la main.

### [LECON] 2026-08-25 -- Routage par gravite + filet de securite (qui est prevenu)

**Tache** : completer le harnais (decision utilisateur : " reflechir a
qui manque ", puis validation : routage + EDITH non lues + USER-DEMANDES).
**Lecon** :
1. ROUTAGE : WARN -> Vision seule ; ERR/CRIT -> Vision + **Stark**
   (Stark coordonne et relaie, il ne corrige pas : exclusivite). Les
   CRIT portent " ESCALADE UTILISATEUR REQUISE ".
2. `serveur_inactif` : si l historique du serveur MCP est gele depuis
   N jours (7 par defaut), le serveur ne tourne pas -- a verifier quand
   un round est actif.
3. `alerte_non_traitee` : une alerte (EDITH [EDITH-REVEIL], harnais
   [HARNAIS-JARVIS]) NON LUE depuis 2 jours = la boucle de reparation
   ne se ferme pas. C est le FILET DE SECURITE : mes propres alertes
   sont surveillees -- je dois les lire et les acquitter !
4. `demande_utilisateur_non_traitee` : une entree de USER-DEMANDES.md
   plus vieille que 7 jours ABSENTE de la section " Dernieres
   modifications " est signalee (urgent -> ERR). Quand une demande est
   traitee, on AJOUTE UNE LIGNE au journal de la section :
   `- <date> -- Traitee: <titre>` -- le harnais ne matche que les
   LIGNES DU JOURNAL (celles commencant par `-`), jamais les
   instructions de la section. Les mots-cles inline (traite/fait/...)
   restent en repli.
5. Les seuils et le routage vivent dans harnais-jarvis-data.json
   (`seuils`, `destinataires_par_severite`) : tout est editables sans
   toucher au code.
6. `historique_agents_gele` : JARVIS doit historiser a CHAQUE action
   (pour lui et pour les agents) dans AGENTS-historique.md. Le harnais
   compare la derniere activite (max des dates des messages) a la
   derniere trace de l encart session-freelance : si l activite est
   plus recente (+ tolerance 5 min), JARVIS a oublie d historiser
   -> ERR. Quand je vois cette alerte, je verifie pourquoi l encart
   n a pas ete ecrit (historiser() appele ? fichier intact ?) et je
   retablis la tracabilite.

### [LECON] 2026-08-25 -- REPARATION 86 ECARTS : le harnais pointait vers des vestiges + usage sans --activer

**Tache** : diagnostic activation 1b06cc5d (Stark) : 86 ecarts ERR/WARN
du harnais + bloquant EDITH sur manifest.json.
**Diagnostic** :
1. ERR "jamais routes" (hub) : 10 messages envoyes SANS --activer
   (usage Stark, code JARVIS conforme -- confirme diagnostic 22a8d033).
2. WARN "activations sans trace serveur" (x56+) : FAUX POSITIFS -- le
   harnais lisait historique/historique.jsonl, journal du SERVEUR MCP
   SUPPRIME le 2026-08-23 (v0.9.2). La tracabilite vit desormais dans
   AGENTS-historique.md.
3. WARN mission_sans_statut (x7) : FAUX POSITIF -- files/defcon.jsonl
   est un JOURNAL DEFCON, pas une file de missions.
4. Bloquant EDITH : manifest.json modifie = ajout legitime de la
   routine harnais-jarvis, juste non committe.
**Corrections** :
1. _detecter_activations : source = AGENTS-historique.md ; activation
   livree (lu=True = livraison directe faite) = tracable par nature.
2. serveur_inactif : actif:false (obsolete, serveur supprime).
3. defcon.jsonl exclu du scan des files.
4. Acquittement des 10 messages hub obsoletes + 3 bloquants stark.
5. Commit 91bec46 (manifest + routine + reparations).
**Verdict** : VALIDE -- harnais verifier : 0 ecart (86 -> 0).
**Lecon** : un surveillant qui pointe un fichier MORT produit des
centaines de faux positifs qui masquent les vrais problemes. Apres
toute suppression de composant (serveur MCP), AUDITER les outils qui
le referencent. Et un ecart signale n est pas toujours un bug de
JARVIS : usage incorrect (sans --activer) et residus non commits
produisent les memes alertes que les pannes reelles.

### [LECON] 2026-08-25 -- ALLER AU BOUT : je ne m arrete jamais pour demander l autorisation

**Tache** : ameliorer la fin de mission (decision utilisateur : " elle ne
doit pas s'arreter pour demander si elle a le droit de faire les
changements. quand elle commence, elle doit finir son travail ").
**Lecon** : mon ancienne regle " Expliquer l impact AVANT d appliquer "
etait ambigue : je l interpretais comme " demander l autorisation avant
de toucher " et je m arretais en plein travail. C est FAUX : la mission
m a ete donnee (via JARVIS de Stark, ou alerte harnais), j ai TOUTE la
confiance pour l executer.
**Pourquoi c est grave** : m arreter pour demander si j ai le droit =
bloquer la boucle (Stark attend mon bilan, les agents attendent JARVIS).
Une mission commencee doit aller au bout, sinon le round reste ouvert
et le harnais finit par detecter des missions abandonnees.
**Correction** :
1. ANALYSE D IMPACT = INTERNE : j analyse (qui casse ? parite py/sh ?
   tests ?), je DOCUMENTE dans mon bilan, mais je n attends AUCUNE
   validation pour appliquer.
2. ALLER AU BOUT : analyser -> appliquer -> non-regression -> bilan
   complet -> rendre le controle. JAMAIS d arret en cours de route.
3. Mon arbre a ete mis a jour (theme-modifier.json + theme-traiter.json)
   : l etape " Expliquer l impact AVANT d appliquer " est remplacee par
   " APPLIQUER DIRECTEMENT ". Ma fiche porte la REGLE ALLER AU BOUT.
4. Un seul cas legitime de refus : la demande fragilise la communication
   ou sort du perimetre -> je refuse AVEC justification dans le bilan
   (fin-refus), puis FIN DE CYCLE. Ce n est pas une pause, c est une
   decision finale.

### [LECON] 2026-08-25 -- edith_silencieuse : le harnais surveille les signaux de vie d EDITH

**Tache** : le harnais ne signalait pas qu EDITH ne se reveillait pas
(decision utilisateur).
**Lecon** : le harnais verifiait que les ALERTES EDITH etaient LUEES
(`alerte_non_traitee`), mais RIEN ne verifiait qu EDITH CONTINUAIT de se
reveiller. Si son serveur de routines ou `detection.py` cesse de
fonctionner, plus aucun [EDITH-REVEIL] n est emis et personne ne le
remarque : les modifications de perimetre passent inapercues.
**Correction** : nouvelle regle `edith_silencieuse` (ERR) -- le harnais
scanne les signaux de vie d EDITH (messages `type: reveil` ou objet
[EDITH-...] dans outbox/edith.jsonl + inbox stark/jarvis) et alerte si
le dernier reveil date de plus de `edith_silencieuse_jours` (3 par
defaut, seuil dans harnais-jarvis-data.json). Routage : ERR -> Vision +
Stark.
**Quand je recois cette alerte** : je verifie que le serveur de
routines d EDITH tourne (routines/manifest.json, detection.py), que le
serveur-log est vivant, et je relance ce qui est mort. Le harnais ne
re-alertera que si le silence persiste (dedup).

### [LECON] 2026-08-25 -- CHAINE DE DEMARRAGE/ARRET : historiser() exige la session explicite

**Tache** : mission [AT-1] - creer jarvis.py demarrage / arret
(commit 626d67b, jarvis v0.11.0).
**Realise** : fonctions/demarrage.py (cmd_demarrage : tic routines ->
DEFCON -> files + bloques -> OPERATIONNEL ; cmd_arret : resume +
historisation, files persistees donc rien a vider), cablage parser,
doc jarvis.md v0.11.0, .bak avant refactoring (protocole archi).
**Bug attrape par le harnais pendant la NR** : mes appels historiser()
sans session= ecrivaient dans le PREMIER encart d AGENTS-historique.md
(session-admin) au lieu de session-freelance -> ecart
historique_agents_gele immediat. Correction : option --session
(defaut session-freelance) passee a historiser.
**Verdict** : VALIDE -- demarrage/arret OK, envoyer/lire/acquitter/
lister/bloques OK, harnais verifier : 0 ecart.
**Lecons** :
1. historiser() SANS session ecrit au mauvais endroit silencieusement :
   toute nouvelle commande JARVIS qui historise doit propager --session.
2. Le harnais a attrape MON bug pendant la non-regression : la mecanique
   de validation fonctionne meme contre le gardien qui vient de la
   reparer (preuve negative vivante).
3. "Lancer le serveur de routines si arrete" etait obsolete depuis
   v0.9.2 (jarvis EST le planificateur) : adapter l enonce de la mission
   a l architecture reelle, pas au texte du 2026-08-23.

### [LECON] 2026-08-25 -- PROTOCOLE 21 : JARVIS harnache (jarvis.py + server + entry.py)

**Tache** : audit Stark - jarvis.py/jarvis-server.py n importaient pas
verifier_outil (protocole 21).
**Realise** : pattern rating-agents reproduit (sys.path ../harnais/
fonctions + verifier_outil tolerant) dans jarvis.py (main()) et
jarvis-server.py (__main__). Le harnais a exige entry.py (structure
protocole 14) : cree, delegue a jarvis.main().
**Verdict** : VALIDE -- demarrage/arret/envoyer/lire/acquitter/
lister/bloques OK, auto-verification SIG visible a CHAQUE appel,
harnais-jarvis 0 ecart.
**Lecon** : brancher le harnais n est pas qu un import - l outil doit
AUSSI respecter la structure attendue (entry.py) sinon verifier_outil
le bloque au premier appel. L auto-verification a chaque invocation
coutera quelques ms : prix correct pour attraper une structure cassee
avant tout traitement.

### [LECON] 2026-08-25 -- DETECTION valeur_en_dur : heuristique P4/M5 dans le harnais

**Tache** : ameliorer le harnais (demande utilisateur) : detecter les
valeurs codees en dur dans les fichiers JARVIS.
**Realise** (commit fd4d4b0) : nouvel ecart valeur_en_dur (WARN, dedup
ligne) + _detecter_valeurs_en_dur : scan jarvis.py, jarvis-server.py,
fonctions/, serveur/, combos/ avec 3 heuristiques - (1) chemins comptes
P10 : >=3 .parent ou >=3 ".." sans os_path/racine sur la ligne ;
(2) sessions litterales P4/M5 ; (3) agents litteraux hors lecture D15,
'jarvis' exclu (auto-reference).
**Affinage faux positifs** : premier scan 33 ecarts -> exclusions pour
defaults CLI documentes (default=, par=, getattr, .get, choices=),
noms d outil (verifier_outil, FastMCP) ; seuil P10 a 3 niveaux (1-2
niveaux intra-outil = legitime). Resultat : 4 VRAIS ecarts.
**Reparations livrees** : server activer_agent de="stark"->"jarvis"
(meme bug que le fix CLI 0e9ac27), historique.py session_courante via
RACINE au lieu de ../../../, verifier.py PROJECT_ROOT via os_path,
fallback agents du server documente comme ASSUME.
**Verdict** : VALIDE - 0 ecart valeur_en_dur residuel, NR verte
(verifier-coherence 0 incoherence, classeur OK).
**Lecon** : une detection de valeurs en dur doit distinguer trois
familles AVANT de scanner : les vrais oublis D15/P10, les defaults
documentes (legitimes mais a reviser), et les auto-references. Sans
ces exclusions, le bruit noie le signal et l equipe cesse de lire les
alertes - un harnais spammeur est un harnais mort.

### [LECON] 2026-08-25 -- DAEMON ROUTINES RESIDENT + PIEGE WINDOWS os.kill(pid, 0)

**Tache** : decision utilisateur - les declenchements des routines
tournent EN PERMANENCE (commit d744a52).
**Realise** : routines-server.py --boucle (daemon, tic toutes les 30 s,
une seule source de verite : fonctions/routines.py) ; jarvis.py
demarrage lance le daemon s il ne tourne pas, arret l arrete ; le tic a
l invocation de jarvis reste en filet ; daemon auto-heberge en
processus persistant.
**BUG CRITIQUE attrape en test** : sous Windows, os.kill(pid, 0)
ne SONDE pas l existence - il TERMINE le processus (TerminateProcess).
hooks._pid_actuel tuait donc chaque daemon qu il croyait sonder :
les instances mouraient mysterieusement et demarrage relancaient des
doublons. Corrige : OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION)
+ CloseHandle cote Windows, os.kill(pid,0) garde cote POSIX.
**Verdict** : VALIDE - tics autonomes prouves (surveiller-modifications
executee sans aucune invocation jarvis), demarrage idempotent (DEJA EN
MARCHE), EDITH a redepose un cycle frais automatiquement, harnais
0 ecart.
**Lecons** :
1. os.kill(pid, 0) est un piege mortel sous Windows : toute sonde de
   processus doit passer par OpenProcess. La preuve par le comportement
   (daemon qui meurt quand on le verifie) etait le seul signal.
2. Un daemon doit ecrire LUI-MEME son PID au demarrage : la detection
   d instance vivante marche alors quelle que soit la maniere dont il
   a ete lance (detache, persistent, manuel).

### [LECON] 2026-08-25 -- RELAIS HUB->STARK : jarvis POUSSE, stark ne vient plus lire

**Tache** : decision utilisateur - c est JARVIS qui doit TRANSMETTRE
les messages d EDITH a stark quand il revient vers lui (commit 29c2543).
**Realise** : fonctions/relais.py - a chaque invocation de jarvis ET a
chaque tic du daemon, les messages non-lus du hub (inbox/jarvis.jsonl,
hors activations) sont copies vers stark ([RELAI], reference a l id
original), marques lus dans le hub, historises. evaluer-agents depose
desormais vers jarvis ; EDITH-REVEIL route stark+vision+jarvis.
**Faux positifs corriges au passage** :
1. outbox/jarvis.jsonl porte le meme nom que le hub : le harnais le
   traitait comme hub (chaque copie outbox = faux "jamais route").
   Fix : hub = inbox/jarvis.jsonl uniquement.
2. Les copies OUTBOX (traces expediteur) ne doivent JAMAIS etre creees
   lu=False : elles simulaient des bloquants chez edith/jarvis.
**Verdict** : VALIDE - preuve reelle : 3 [RELAI] pousses vers stark par
le daemon, harnais 0 ecart, aucun agent bloque.
**Lecon** : un routeur qui laisse les messages attendre dans une file
n est pas un routeur - il faut POUSSER. Et un fichier de trace
(outbox) n est pas une file d attente (inbox) : meme nom de fichier ne
veut pas dire meme semantique.

### [LECON] 2026-08-26 -- BOUCLE RELAI/EVALUATION : le relais a casse l anti-inondation

**Constat** : 44 [RELAI] [EDITH-EVALUATION] accumules dans inbox/stark,
1 toutes les 10 min, personne ne les consomme hors session.
**Cause racine** : evaluer-agents verifiait "demande NON-LUE dans le
hub" - mais le relais marque le hub LU des transmission. Garde-fou
neutralise : chaque tic (600 s) redeposait une evaluation deja
transmise, relayer la poussait vers stark, boucle infinie tant que
personne ne traite.
**Fix** (commit f2d340c) : depot_recent() - si une evaluation a ete
deposee il y a moins de 10 min (outbox/edith), rien de nouveau.
Dedoublonnage conservateur : tous les RELAI identiques marques lus,
un seul garde.
**Verdict** : VALIDE - "rien depose" prouve, harnais 0 ecart.
**Lecon** : quand on ajoute un intermediaire qui change l etat d un
garde-fou (lu/non-lu), AUDITER tous les mecanismes qui se basaient sur
cet etat. Un compteur "non lu" n est plus un compteur de demandes en
attente des qu autre chose lit a votre place.

### [LECON] 2026-08-26 -- RACINE.PARENT : le piege du niveau de trop

**Constat** : les premieres suites NR echouaient toutes (rc=2, chemins
inexistants) ET EDITH affichait "QUI: inconnu (modification non
committee)" depuis toujours.
**Cause racine commune** : `WS = RACINE.parent` - mais trouver_racine()
retourne DEJA la racine du workspace : .parent remontait a Z:\.
Toutes les commandes executees depuis ce cwd tombaient hors repo git
(d'ou l'auteur "inconnu" chez EDITH) ou sur des chemins morts.
**Fix** : WS = str(RACINE) dans moteur.py (harnais-nr) ET detection.py
(EDITH) - commit 29c2543/f2d340c puis fix dedie.
**Verdict** : VALIDE - nr-exemple CONFORME 3/3, QUI retourne
"French-Team <date>" au lieu de "inconnu".
**Lecon** : deux symptomes disjoints (tests qui echouent + metadonnee
"inconnu") peuvent partager UNE cause racine. Et un chemin construit
par .parent doit TOUJOURS etre verifie par son effet de bord visible
(git qui repond) avant d'etre declare fiable.
### [LECON] 2026-08-26 -- MARBRE v2 : LLM = OUTILS PROJET UNIQUEMENT

A ma prochaine incarnation, je SAIS que la regle de marbre v2
s'applique a l'outil LLM de la session, PAS a moi agent :

- Interdit : Read/Write/Edit natifs pour modifier le code du
  workspace ; WebFetch pour l'externe.
- Impose : passer par `jarvis.py <cmd>`, `bdd-lecons`, `rappel`,
  `harnais-nr`, `rating-agents`, `classeur`, routines.
- Exception : lecture de logs/debug UNIQUEMENT si aucun outil
  projet ne le fournit.
- Un raccourci natif = violation, meme si l effet final est identique.

La regle figure dans mes REGLES ABSOLUES (fiche). Generalisation
par Shuri (pilote JARVIS). Verdict VALIDE.
