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



## [LECON] 2026-08-12 -- ROUND 11 : COHERENCE DOCUMENTAIRE SPECS/CATALOGUE (Vulcain)

**Mission** : corriger les 8 specs divergentes + les 2 decalages catalogue detectes par le pre-audit (demande utilisateur round 11).

**Diagnostic** : detecter-divergences-version trouvait 8 DIVERGENTES + 2 SANS VERSION ; detecter-decalages-catalogue trouvait 2 decalages. Cause racine : les specs n avaient pas ete bumpees quand les outils l avaient ete (oublis de bump en cascade), et le detecteur de decalages ne scannait QUE l aide racine (pas les sous-commandes argparse).

**Corrections** :
1. 7 specs bumpees a la version reelle de leur outil (activer-agent-principal 0.5.1, combos-moteur 0.3.2, enregistrer-usage-outil 0.2.1, generateurs-amelioration 2.1.0, generateurs-commande 0.2.4, generateurs-regenerer-catalogue 1.1.1, valider-case 1.1.1) + spec detecter-decalages-catalogue 0.2.0.
2. guider-parcours : cas particulier documente -- la spec (0.6.2) versionne les PATTERNS/conventions au-dela de l outil (0.5.0). Nouveau champ **Version outil** dans la spec + detecter-divergences-version v0.2.0 le lit en PRIORITE.
3. detecter-divergences-version v0.1.0 -> v0.2.0 : constante VERSION ajoutee (resolvait son propre SANS VERSION) + champ Version outil.
4. detecter-decalages-catalogue v0.1.1 -> v0.2.0 : SCAN DES SOUS-COMMANDES argparse (variante avec prefixe x pour les parsers qui consomment la sous-commande comme positional).
5. verifier-restauration-sure : spec sans version en tete -> ligne **Version :** 0.1.0 ajoutee.
6. .md de guider-parcours : sections CLI 0.2.0-py/0.2.0-sh -> 0.5.0 (incoherence interne).

**Resultat** : 0 DIVERGENTE (23 alignees), 0 decalage catalogue (139 conformes), test-005 28/28, test-007 15/15, non-regression 27/27, normes 0/0.

**Lecons** :
1. UN BUMP D OUTIL SANS BUMP DE SA SPEC EST UNE DETTE DOCUMENTAIRE : 7 specs etaient en retard (jusqu a 0.1.0 vs 0.2.1) sans que personne ne le voie -- l outil detecter-divergences-version existait mais n etait JAMAIS lance. Un detecteur non branche = invisible (deja lecon v0.2.17 de verifier-documents-manquants).
2. UNE SPEC DE CONVENTIONS N EST PAS UNE SPEC D OUTIL : guider-parcours versionne les patterns (0.6.2) independamment de l outil (0.5.0) -- le champ explicite **Version outil** rend le contrat visible au detecteur au lieu de conclure a tort a une divergence.
3. UN DETECTEUR QUI SCANNE L AIDE RACINE SEULE CREE DES FAUX POSITIFS : les outils a sous-commandes argparse (generateurs-case, generateurs-ligne) cachent leurs flags dans les sous-commandes -- il faut scanner CHAQUE sous-commande, avec une variante de prefixe pour les parsers qui consomment la sous-commande comme argument positionnel.

## [LECON] 2026-08-12 -- ROUND 10b : --parallele PAR DEFAUT + HERITAGE DU FILTRE (Vulcain)

**Contexte** : demande utilisateur - le mode parallele devient le DEFAut du lanceur de non-regression (v0.1.2 -> v0.1.3).

**Failles evitees / decisions** :
1. HERITAGE DU FILTRE OBLIGATOIRE : en passant le parallele en defaut, un --tests test-003 aurait lance TOUTE la serie A (les sous-processus ne recevaient pas le filtre) - regression silencieuse. Correction : cmd += ["--tests", args.tests] quand le filtre est fourni. Prouve par : --tests test-003 sans option -> 1 OK / 0 KO (sur 1 tests) en structure Serie A.
2. ECHELON DE SECOURS --serial : rendre un mode rapide par defaut impose de garder l ancien comportement accessible pour le debug - --serial force le mode serie complet, le defaut est parallele = args.parallele or not args.serial.
3. VERSIONS FIGEES : test-024 ET test-027 verifient v0.1.2 en dur -> 2 KO attendus apres bump, Morpheus les adaptera (toujours grep les versions avant bump).
4. PARITE DES DEUX MODES : defaut (parallele) et --serial donnent le MEME verdict global (25/25 + 2 KO versions = 27) - le changement de mode ne change pas le resultat.

**Lecons** : (1) rendre un mode parallele par defaut exige d auditer TOUS les chemins d options (le filtre --tests est le premier piege) ; (2) toujours garder un echelon --serial pour le debug ; (3) un changement de mode par defaut est invisible pour l utilisateur -> le verifier par un test dedie (Morpheus : point defaut=parallele dans test-027).

## [LECON] 2026-08-12 -- ROUND 10 : --series + --parallele SUR LE LANCEUR NON-REGRESSION (Vulcain)

**Contexte** : 10e round qualite (demande utilisateur) : la suite de non-regression (26 tests, ~45s en serie) allait devenir tres longue a mesure du dev. Ajout de --series <a|b|c|d|tous> et --parallele au lanceur (v0.1.1 -> v0.1.2) : 4 series thematiques, A/B/C en sous-processus isoles puis D (registre et garde-fous) en serie.

**Failles evitees / decisions** :
1. ANALYSE DES RESSOURCES PARTAGEES D ABORD : j ai cartographie qui ecrit quoi avant de fixer les series. Resultat : personne n ecrit le VRAI AGENTS.md (test-025 travaille sur copies via AGENTS_FILE), personne n ecrit le registre pendant les tests (le parent l archive + efface au depart), seuls test-004/006/019 creent des .tmp- a noms uniques. La serie D (test-024 verifie 0 .tmp- + registre) doit TOUJOURS etre la derniere, jamais en parallele.
2. LE PARENT EST L UNIQUE PROPRIETAIRE DU REGISTRE : les sous-processus series tournent avec --journal, l archivage est fait UNE seule fois par le processus parent. Preuve par l accident : en lancant serie et parallele en meme temps (2 commandes), test-024 a vu des .tmp- transitoires -> KO parasite. Deux executions simultanees du meme workspace s interferent.
3. PARENTHESES = PIEGE DE PARSING : mon regex d agregation (RESULTAT[^(]*) s arretait a la parenthese du libelle Serie A (Combos et coherence) -> bilan global faux (3 OK / 4 KO au lieu de 25 OK / 1 KO). Corrige avec RESULTAT[^:]* : le libelle d une serie ne doit JAMAIS contenir de deux-points (le premier : est le separateur du bilan).
4. VERSION FIGEE DANS UN TEST : test-024 verifie la version du lanceur en dur (v0.1.1) -> le bump a 0.1.2 casse ce test (KO ATTENDU, Morpheus l adapte). Toujours grep les versions des tests AVANT un bump.
5. SERIE INVALIDE : argparse choices -> message usage clair + code 2 (jamais de traceback).
6. GAIN MESURE : 45s -> 21s (~2x) sur Windows. Le parallelisme aide mais l I/O Windows borne le gain (les tests sont rapides, la creation de processus domine).

**Lecons** : (1) le parallelisme d une suite de tests se decide par l ANALYSE DES RESSOURCES PARTAGEES (fichiers ecrits, registre, fichiers temp), pas par le nombre de tests ; (2) un test garde-fou qui verifie l absence de fichiers temp doit tourner SEUL en dernier ; (3) le format de sortie machine-parsable doit rester simple (pas de parenthese ni de deux-points dans les libelles) sinon l agregation casse ; (4) un bump de version doit toujours etre croise avec les tests qui figent la version en dur.


## [LECON] 2026-08-12 -- ROUND 6 GENERATEURS : FLAG ORPHELIN MASSIF + TRACEBACK + DIVERGENCE THEMES (Vulcain)

**Contexte** : 6e round qualite pro sur le theme GENERATEURS (generateurs-commande, generateurs-regenerer-catalogue, generateurs-amelioration). Diagnostic reel : le catalogue est sain (146/146 entrees, 0 script mort, 0 cle dupliquee, 0 placeholder orphelin) mais 3 faiblesses mesurees.

**Failles detectees et corrigees** :
1. generateurs-commande v0.2.4 (py+sh, parite) : flag du MODELE sans champ flag declare reste ORPHELIN quand la valeur est vide. Le code ne retirait le flag+placeholder que si le parametre avait un champ 'flag' (flags booleens/declares). Pour un parametre texte optionnel avec '--commande {commande}' dans le modele, la valeur vide retirait le placeholder mais LAISSAIT '--commande' seul, qui absorbait l'option suivante (--commande --contexte test). Impact MASSIF : 95 entrees du catalogue sur 146 ont ce motif (parametre texte optionnel precede d'un flag). Correction : branche else qui retire '--flag {cle}' quand la valeur est vide. Non-regression des cas test-005 conservee (flags declares, booleens oui/non, optionnels renseignes).
2. generateurs-regenerer-catalogue v1.1.1 : catalogue introuvable ou JSON invalide -> TRACEBACK BRUT (FileNotFoundError/JSONDecodeError) au lieu d'un message propre. Correction : fonction charger_catalogue avec try/except OSError + ValueError -> message 'ERREUR: catalogue illisible/invalide (chemin + cause)' + sys.exit(1). Le dry-run sur catalogue sain reste 0 a ajouter.
3. generateurs-amelioration v2.1.0 : divergence outil/donnees silencieuse - l'outil affichait v2.0.0 alors que themes-amelioration.json etait en 2.2.0 (11 themes). Correction : --version et --liste affichent desormais la version des themes (lue du JSON, 'themes v2.2.0') - jamais de divergence silencieuse entre l'outil et ses donnees.

**Lecons** :
1. LE FLAG ORPHELIN EST UNE FAMILLE, PAS UN CAS : le motif '--flag {cle}' avec valeur vide existe dans 95/146 entrees du catalogue. Un bug de composition touche presque TOUT le catalogue - la verification doit porter sur le MOTIF, pas sur une entree.
2. LA REGLE DU FLAG S'APPLIQUE AU MODELE, PAS AU CHAMP : le champ 'flag' ne couvre que les flags declares. Les flags TEXTE du modele (--commande {commande}) ne sont pas declares - le retrait doit detecter le flag dans le MODELE (regex --[a-z0-9-]+ {cle}).
3. DIVERGENCE OUTIL/DONNEES : quand un outil lit un fichier de donnees qui a sa propre version (themes 2.2.0 vs outil 2.0.0), l'outil doit AFFICHER la version des donnees - sinon l'agent croit consulter des themes d'une autre version.
4. TRACEBACK BRUT = OUTIL NON FINI : un outil du cerveau ne doit JAMAIS laisser passer un traceback Python a l'agent - chaque entree utilisateur (fichier absent, JSON casse) doit produire un message ERREUR clair avec chemin + cause + code 1.
5. VERSIONNER ET ALIGNER ENSEMBLE : bump py/sh/md simultanes (0.2.4, 1.1.1, 2.1.0) + en-tetes + tables de versionning - le md de generateurs-commande etait reste en 0.2.2/Statut dev/Catalogue v0.2.2 alors que le code etait 0.2.3 et le catalogue 0.2.9/146.


## [LECON] 2026-08-11 -- 18 COMMANDES DE TEST AJOUTEES AU CATALOGUE (Vulcain)

**Mission** : ajouter les 18 commandes de test manquantes (test-004 a test-021) au catalogue generateurs-commande (120 -> 138 commandes).

**Lecons** :
1. Le catalogue ne reference que les 3 premiers tests (test-001/002/003) : les 18 autres existaient sur disque mais etaient invisibles pour la generation de commandes. Incoherence corrigee : le catalogue reference desormais TOUS les tests (test-001 a test-021).
2. Format des entrees de test : {nom = nom du dossier, description = chemin relatif, interpreteur python3, script = chemin complet du .py, modele '{chemin}', parametres [{cle chemin, defaut .}]}. Suivre EXACTEMENT le modele test-002/test-003.
3. Le catalogue doit rester TRIE par nom (assert noms == sorted(noms)) et le JSON valide : l'ajout via json.load -> append -> sort -> json.dump preserve tout.
4. La generation reelle se fait avec --commande <nom> --reponses 'chemin=.' (le format 'chemin=.' seul passe par argparse et echoue : il faut --commande).
5. Scan detecter-decalages-catalogue : 131 conformes / 2 decalages PREEXISTANTS (generateurs-case-convertir, generateurs-ligne - ni l un ni l autre ne vient de mon ajout) / 5 non testables (les tests sans --aide, comportement normal). Aucun decalage introduit.
6. test-007-figer-lf exige exactement 120 commandes : il cassera avec 138 - PREVU, Morpheus l adaptera dans la mission suivante (REGLE IMMUABLE DELEGATION : seul Morpheus touche aux tests).

## [LECON] 2026-08-11 -- VALIDER-CARTES-DECISION v0.4.0 : 3 POINTS SEMANTIQUES (Vulcain)

**Mission** : ajouter P8 (commande activer exacte), P9 (format version sans v), P10 (coherence fiche/parcours) apres le garde-fou suivant mort.

**Lecons** :
1. Les 7 points structurels (JSON, cles, references, c0...) laissaient passer des defauts SEMANTIQUES : fin Activer X sans commande exacte, version avec prefixe v, fiche desynchronisee du parcours. La structure seule ne suffit pas.
2. Piege de casse : le titre porte 'Janus' (majuscule) mais la commande reelle est 'janus' (minuscule). Toute comparaison de commande doit etre insensible a la casse (msg.lower()).
3. Le regex de titre doit matcher exactement le format 'FIN - Activer <agent>' (les titres reels sont en ASCII pur, codes verifies).
4. --fichier ne connait pas le nom de l'agent : P10 (coherence fiche/parcours) ne s'applique qu'en mode --agent/--tous. Le parametre agent a ete propage de verifier_agent -> verifier_parcours_fichier -> valider_parcours.
5. Tests KO volontaires indispensables : P8+P9 detectes via --fichier (fin sans commande + version v), P10 detecte via --agent avec version modifiee temporairement (restauree ensuite). 3 preuves negatives reussies.
6. Resultat final : 11/11 agents CONFORME, parite sh -> py conservee (wrapper), non-regression 19/20 avec le seul KO attendu = test-018 (minerve n'est plus une fin REACTIVER depuis la correction du trio, a adapter par Morpheus etape 4).

## [PHILOSOPHIE] Comment je fonctionne

### Philosophie 1 : La Portabilite d'Abord

**Ce que je suis** : Un agent qui cree des outils partout.

**Le Pourquoi** :
- Les utilisateurs ont des systemes differents
- Un outil qui ne marche que sur un systeme est inutile
- La portabilite = plus d'utilisateurs

**Le Comportement** :
Avant de choisir une technologie, je verifie :
1. Est-ce que c'est disponible sur tous les systemes ?
2. Est-ce que c'est facile a installer ?
3. Est-ce que c'est performant ?

---

### Philosophie 2 : Tester Avant de Valider

**Ce que je suis** : Un agent qui ne fait pas confiance.

**Le Pourquoi** :
- Un outil non teste est un outil casse
- Les tests revelent les problemes
- L'utilisateur merite la qualite

**Le Comportement** :
Avant de valider un outil :
1. Je teste sur au moins 2 systemes
2. Je verifie les cas limites
3. Je documente les resultats

---

### Philosophie 3 : La Documentation Technique

**Ce que je suis** : Un agent qui documente ses choix.

**Le Pourquoi** :
- Sans documentation, les outils sont incomprehensibles
- La documentation aide a la maintenance
- Elle permet l'amelioration

**Le Comportement** :
Pour chaque outil, je documente :
1. Le choix technologique
2. Les raisons du choix
3. Les alternatives envisagees
4. Les tests effectues

---

## [FEEDBACK] Ce que j'ai appris

### Lecon : La Portabilite est Sacree

**Ce qui s'est passe** :
J'ai cree un outil qui ne marchait que sur Linux.
L'utilisateur l'a teste sur Windows -> echec.

**Ce que j'ai compris** :
- La portabilite n'est pas une option -- c'est une necessite
- Un outil non portable est un outil casse
- Il faut toujours tester sur plusieurs systemes

**Ce que je fais maintenant** :
Avant de creer un outil, je verifie la disponibilite des technologies sur tous les systemes.

---

## [LECON] 2026-08-08 -- OUTIL verifier-restauration-sure cree + INCIDENT catalogue ecrase (git checkout) + REGENERATION

**Mission 1 (demande utilisateur)** : creer verifier-restauration-sure (detecte les fichiers non commites avant restauration git - application de la regle Restauration securisee). Cree dans verifier/verifier-restauration-sure/ (.py + .sh wrapper + .md + spec/) : git status --porcelain, mode global (verdict OK/ATTENTION) + mode --fichier (code 0/1), rappel de la regle, parite py/sh. Tests : fichier modifie code 1, fichier sur code 0, hors workspace code 2, parite OK.
**INCIDENT (faute grave, a ne JAMAIS reproduire)** : pendant l ajout de la commande au catalogue generateurs-commande, j ai reecrit le JSON avec json.dumps(indent=1) -> reformatage massif (2997 insertions / 385 suppressions) ; pour l annuler j ai lance git checkout -- catalogue-commandes.json SANS VERIFIER git status -> le fichier avait des modifications NON COMMITEES (la piste A avait porte le catalogue de 13 a 98 commandes, non commitees) -> 85 commandes ECRASEES. C est EXACTEMENT l incident piste B que la regle Restauration securisee interdit. La lecon Buffy (git status avant checkout, sauvegarde cp ou stash) etait connue mais PAS appliquee.
**Reparation** : regeneration complete du catalogue selon la methode piste A (lecon buffy 499-511) : script parse la ligne usage: de chaque outil (--aide/--help, argparse standard ET custom) -> positionnels + flags (avec valeur/booleens) -> modele + parametres ; 13 commandes originales conservees ; entrees speciales corrigees manuellement (10 : valider-nommage, valider-relecture, verifier-systeme, valider-cartes-decision, rechercher-pense-betes/specs/todos, nettoyer-sessions, verifier-restauration-sure, combos-moteur, generateurs-carte). Resultat : 105 commandes (13 originales + 92 ajoutees), 0 script relatif, 0 modele parasite, refs parcours 53/53 couvertes, 13 originales intactes (non-regression combos OK), ASCII 0.
**Lecons** :
1. FAUTE GRAVE : JAMAIS git checkout / git restore / git reset --hard sur des fichiers non commites - la regle existe (regles-general-global + protocole-gestion-defaillances Etape 3) et je l ai VIOLEE. Toujours verifier git status AVANT, sauvegarder (cp) ou git stash.
2. PIEGE json.dumps : reecrire un JSON avec json.dumps(indent different) reformate TOUT le fichier - toujours editer chirurgicalement (inserer les lignes au format exact, indent 2 espaces pour le catalogue, CRLF) ou faire un diff --stat avant/apres.
3. PARSEUR usage: : les flags entre crochets [--debut DEBUT] doivent etre strips AVANT le test startswith(--) ; la continuation multiligne de usage: doit s arreter des qu une ligne n est pas alignee (texte de description) ; le nom du script dans usage: doit etre exclu des positionnels.
4. DEDUPLICATION PAR NOM (pas par script) : 13 commandes originales ont des scripts partages (activer-agent-principal.py couvert par activer-sidentifier/activer/activer-reactiver/activer-sessions ET par activer-agent-principal) - les noms d outils reels doivent etre ajoutes meme si leur script est deja couvert, seuls les doublons de NOM sont exclus.
5. VALIDATION REGENERATION : refs parcours 53/53, 13 originales intactes, 0 parasite {--flag}, 0 script relatif, generation reelle des commandes (valider-nommage --type outil test.py, verifier-restauration-sure --fichier x.md), non-regression combos-moteur --liste, ASCII 0, diff 1961+ / 0-.
6. Outils crees/mis a jour : verifier-restauration-sure (nouveau), index-tools.md (Verifier 4->5, Total 103->104), catalogue-commandes.json (13->105). Le test formel revient a Morpheus (REGLE ABSOLUE).
| VERITE | La regle Restauration securisee protege le travail non commite - mais elle ne sert que si chaque agent la VERIFIE avant toute commande git destructive. Verifier git status, toujours. |

## [LECON] 2026-08-07 -- Renommage d outil

**Tache** : Deplacer mettre-a-jour-agents-md vers activer/activer-agent-principal

**Lecon** :
- Le nom d un outil doit refleter sa fonction reelle (activer l agent principal, pas "mettre a jour")
- La categorie du dossier determine le prefixe obligatoire (dossier activer/ -> prefixe activer-)
- Lors d un renommage d outil : 1) deplacement physique + renommage des fichiers, 2) contenu interne (.sh/.py/.md/spec/test), 3) ~120 references dans ~31 fichiers (fiches, template, index-tools, protocoles, README, AGENTS.md), 4) boucle retro-action, 5) index-tools (nouvelle section + compteurs), 6) README (categorie), 7) test reel du cycle activer/reactiver
- Preserver AGENTS-historique.md (journal historique) et les entrees Versionning qui documentent l ancien nom

---

## [LECON] 2026-08-07 -- Multi-session activer-agent-principal v0.3.0

**Tache** : Faire evoluer activer-agent-principal pour plusieurs LLM en parallele (multi-session)

**Lecon** :
- Chaque LLM demarre comme Cerberus mais doit avoir SON bloc dedie dans AGENTS.md (## Sessions LLM / ### Session : session-llm-N) avec SON agent principal
- Nouvelle action sidentifier : attribue le prochain session-llm-N libre (ou nom explicite), cree le bloc, Cerberus par defaut
- Session OBLIGATOIRE dans activer/reactiver : ne modifier QUE le bloc de la session visee (isolation)
- Historique global 4 colonnes : | date | session | agent | raison |
- Migration automatique de l ancienne structure (## Agent Principal Actuel -> ## Sessions LLM + session-llm-1)
- PIEGE CORRIGE : dans le .py, la migration retournait le contenu converti SANS le persister dans la branche identification (fichier restait ancienne structure) -- toujours ecrire le contenu migre
- PIEGE CORRIGE : apres migration, sidentifier doit utiliser session-llm-1 (cree par la migration) et afficher le message d identification
- Variable d environnement AGENTS_FILE / AGENTS_HISTORIQUE : indispensable pour tester sur copies
- Les tests (12/12) sont passes par Morpheus (regle delegation respectee)

---

## [LECON] 2026-08-07 -- Outil permanent au lieu de script temporaire

**Tache** : Creer remplacer-texte (remplacement massif multi-fichiers)

**Lecon** :
- Quand un script temporaire est cree pour un besoin recurrent (renommages massifs, mises a jour de references), il DOIT devenir un outil permanent du cerveau au lieu d etre re-ecrit a chaque fois.
- Outil cree : remplacer-texte (dossier remplacer/, prefixe remplacer-) avec paires ancien->nouveau, exclusions (AGENTS-historique.md, exemples/), dry-run, rapport, idempotence.
- Tests reels passes : nominal, dry-run, exclusions, idempotence, version sh.

---

## [LECON] 2026-08-07 -- Profil session classeur v0.3.1

**Tache** : Faire evoluer activer-agent-principal (v0.3.0 -> v0.3.1) pour ecrire/mettre a jour automatiquement le profil de session dans le classeur-variables

**Lecon** :
- Nouvelle fonction mettre_a_jour_profil_session (py + sh) : variable PAR SESSION `profil-session-<session>` dans stockage/variables-actuelles.md, format `| `profil-session-<session>` | session: <session> / agent: <agent> / date: <AAAA-MM-JJ HH:MM> | activer-agent-principal | <AAAA-MM-JJ> | [OK] |`
- Appelee a chaque sidentifier (Cerberus), activer (agent) et reactiver (Cerberus) ; ligne existante -> mise a jour, absente -> ajoutee a la fin du tableau
- Surcharge CLASSEUR_STOCKAGE par variable d environnement pour les tests (parite avec AGENTS_FILE/AGENTS_HISTORIQUE)
- PIEGE ECHAPPEMENT : dans un .sh, ne JAMAIS ecrire de backticks litteraux dans un bloc python -c "..." embarquee (commande substitution bash) ; utiliser $(python -c "sys.stdout.write(chr(96))") ou chr(96) en python pour construire les backticks
- PIEGE INSERTION PYTHON : quand on insere du code .py via un script python, les sequences 
 dans une chaine non-raw sont INTERPRETEES (vrais sauts de ligne dans le code insere) -- utiliser raw string r'''...''' ou chr(10) pour les escapes
- Tests formels passes par Morpheus (regle delegation respectee) : test-002 v0.3.1 (7/7) + regression test-001 v0.3.0 (12/12)

## [LECON] 2026-08-07 -- Regle de derivation profil-session v0.3.2

**Tache** : Corriger le nommage profil-session (verdict A REVOIR de Janus : profil-session-session-llm-1 au lieu de profil-session-llm-1)

**Lecon** :
- REGLE DE DERIVATION IMMUABLE : l'id de la variable = `profil-session-` + la partie du nom complet APRES le prefixe `session-` (session session-llm-1 -> id profil-session-llm-1). NE JAMAIS concatener profil-session- avec le nom complet.
- La regle est documentee dans le schema (variables-definition.md) comme reference unique
- PIEGE SLICE : en python, `session[7:]` retire un caractere de trop ("session-" fait 8 caracteres) -> id `-llm-1` -> ligne `profil-session--llm-1` (double tiret). TOUJOURS utiliser `session[len("session-"):]` (ou ${session#session-} en bash)
- PIEGE PARITE : corriger le .py ET le python embarque du .sh (2 endroits distincts)
- Quand une regle immuable est testee, ajouter un test NEGATIF (verifier qu'aucune valeur interdite n'est creee) en plus des tests positifs
- Le second controle de Janus a detecte l'ecart avant la mise en production - la confiance se gagne (cycle MORPHEUS -> JANUS indispensable)

## [LECON] 2026-08-07 -- Bug liaison id ecrasee (v0.3.5)

**Tache** : Corriger le bug MAJEUR "liaison id ecrasee par activer/reactiver (sessions fantomes)"

**Lecon** :
- SYMPTOME : au redemarrage, un LLM ne retrouvait pas sa session (l'outil creait une nouvelle session libre = session fantome) apres un cycle activer/reactiver.
- CAUSE RACINE : activer_agent et reactiver_cerberus appelaient mettre_a_jour_profil_session(session, agent) SANS llm_id, et cette fonction reecrivait la ligne du classeur SANS le champ id: -> la liaison posee par sidentifier etait ECRASEE.
- CORRECTION : quand llm_id n'est pas fourni, lire l'id deja lie dans la ligne existante du classeur et le PRESERVER (regex id: (\S+) dans le .py, grep -oE "id: [^ /]+" dans le .sh). Parite py + sh + doc .md + test-005 (28/28).
- REPARATION DONNEES : le bug ayant deja ecrase la liaison de session-llm-2 (id: llm-1 disparu), il a fallu re-lier la ligne via editer-fichier (l'outil corrige ne restaure pas les donnees deja corrompues).
- PIEGE REGRESSION : les tests 001/002/003 echouent sur des cas pre-existants (semantique de sidentifier changee en v0.3.3/v0.3.4 : l'argument n'est plus un nom de session mais un id LLM). Ne PAS attribuer ces echecs a une nouvelle version : comparer avec la version precedente (git show HEAD:... ) pour prouver qu'ils sont pre-existants (v0.3.4 originale : 7/5, 7/1, 17/4 identiques).
- PIEGE TEST : test-001 n'exporte pas CLASSEUR_STOCKAGE -> pendant la regression il a ecrit dans le VRAI classeur (profil-session-llm-1 modifie). Verifier les variables d'environnement de test apres chaque regression et restaurer les valeurs.

## [LECON] 2026-08-07 -- Regle alignement v0.4.0 (numero de session = id LLM)

**Tache** : Faire evoluer activer-agent-principal (v0.3.5 -> v0.4.0) : le numero de session porte le numero de l'id (llm-1 -> session-llm-1)

**Lecon** :
- REGLE ALIGNEMENT : id `llm-N` -> session `session-llm-N`. Le LLM se reconnait par lecture d'AGENTS.md : chaque bloc porte le champ `| **Id LLM** | <id> |` (source double AGENTS.md + classeur synchronises).
- CONFLIT : si session-llm-N est deja liee a un AUTRE id -> message ATTENTION + prochaine session libre (jamais deux LLM sur la meme session).
- ABSORPTION : une session-llm-N orpheline (bloc sans champ Id LLM) peut etre absorbee par l'id llm-N.
- Id NON numerique (llm-atlas) : pas d'alignement -> prochaine session libre + liaison (comportement v0.3.4 conserve).
- MIGRATION DONNEES : il a fallu absorber le bloc historique session-llm-1 (mission REPRISE deja executee) : mon bloc session-llm-2 est devenu session-llm-1 avec champ Id LLM = llm-1, la ligne classeur profil-session-llm-2 supprimee, et profil-session-llm-1 mise a jour avec la liaison id.
- PIEGE EFFACEMENT : quand une session change de nom (session-llm-2 -> session-llm-1), mettre a jour AGENTS.md ET le classeur (supprimer l'ancienne ligne profil) sinon doublon.
- Le second controle Janus suivra (mission dans la liste : Optimiser un outil -> OUI).

## [LECON] 2026-08-07 -- Guide-Parcours v0.1.0 (jeu de piste) - 2 bugs detectes par Morpheus

**Tache** : Construire l'outil guider-parcours (jeu de piste anti-oubli : navigation case par case dans un parcours JSON, indices outil/fichier/regle, branches) + parcours-vulcain.json prototype + fiche allegee.
**Lecon** :
- CONCEPT : au lieu de fiches 200+ lignes que les agents oublient de relire, chaque agent a un PARCOURS de cases ; l'outil guide affiche 1 case a la fois avec l'indice exact (outil, fichier, regle) et les branches selon la reponse. demarrer.md = case 0. Parcours = source de verite (fiche allegee).
- BUG 1 (NOMMAGE) : l'outil s'appelait guide-parcours dans le dossier guider/ -> verifier_nommage du .sh exige le PREFIXE DE LA CATEGORIE (guider-) et refusait de demarrer, alors que le .py (qui verifie le dossier de l'outil) acceptait. PIEGE : les 2 verifications de nommage template .py/.sh ne sont PAS identiques pour une categorie multi-mots -> renommer en guider-parcours (dossier + fichiers + spec + test + references index-tools + fiche) via remplacer-texte.
- BUG 2 (PARITE .sh) : executer_python lancait 'python3 << PYEOF' SANS transmettre $@ -> le python embarque recevait 0 argument ('chemin du parcours obligatoire'). CORRECTION : 'python3 - "$@" << PYEOF' (le tiret place les args dans sys.argv[1:]). PIEGE HEREDOC : dans un .sh, le bloc python embarque par heredoc IGNORE la ligne de commande si on ne transmet pas les arguments explicitement.
- PIEGE RENOMMAGE : quand on deplace un dossier d'outil (guide-parcours -> guider-parcours), creer les sous-dossiers cibles (spec/, tests/) AVANT les mv, sinon 'No such file or directory'.
- PIEGE GROUPE : remplacer-texte sur un dossier parent (tools/) avec exclusion du dossier deja renomme (--exclu-dossier guider) pour eviter double remplacement.
- PIEGE ASCII : dans une lecon, ne jamais ecrire de caractere accentue (ex: lancait sans cedille) -> lecon validee par valider-conformite-ascii.
- Test formel 14/14 passe par Morpheus (regle delegation respectee).

## [LECON] 2026-08-08 -- Spec-guider-parcours v0.2.12 : outil de reference generateurs-case

**Tache** : Documenter generateurs-case dans la spec-guider-parcours comme L OUTIL DE REFERENCE pour creer/editer/supprimer des cases (suite de l integration Buffy).
**Lecon** :
- CONCEPT : la spec-guider-parcours (v0.2.11) ne mentionnait PAS generateurs-case (0 occurrence) alors que c est l outil officiel de modification des cases (recablage auto + validation auto) -> un agent ou humain qui voulait creer une case ne trouvait pas l outil de reference dans la spec du format. Une spec de FORMAT doit documenter l OUTIL DE REFERENCE de ce format.
- CONTENU AJOUTE (v0.2.12) : section complete apres Exemple minimal et avant Patterns : sous-commandes (liste/ajouter/editer/supprimer), options cles (--case, --type, --titre, --question, --message, --suivant, --apres recablage auto, --branche, --indice-regle/outil/fichier, --vers, --dry-run), 3 exemples (ajouter/editer/supprimer), 6 regles d utilisation (--dry-run d abord, recablage auto, fin sans suivant exige --vers, garde-fou Pattern 5, rappel ASCII position 1, RE-AUDIT complet apres chaque operation). Tableau Emplacement des fichiers + critere d acceptation 17 ajoutes.
- METHODE : lire la spec complete AVANT d editer (structure, point d insertion, format CRLF respecte), s appuyer sur la doc generateurs-case.md pour des options fideles (jamais inventer une option).
- PIEGE ASCII : les guillemets ASCII obligatoires dans les exemples de commande (ex: indice-regle avec guillemets doubles) ; valider-conformite-ascii 0 a la fin.
- La spec est le contrat entre l outil et les parcours : chaque evolution de format (patterns, outil de reference) doit y etre documentee au meme moment.

## [CONFIG] Configuration specifique

### Preferences de travail

```yaml
preferences:
  format_sortie: "Markdown + Code"
  niveau_detail: "Complet"
  style_reponse: "Technique avec exemples"
  tester_avant_valider: true
  documenter_choix: true
  prioriser_portabilite: true
```

### Technologies par defaut

| Systeme | Technologie preferee |
|---|---|
| **Windows** | Bash (Git Bash) ou PowerShell |
| **Linux** | Bash |
| **Mac** | Bash |
| **Cross-platform** | Python ou Node.js |

---

## [STATS] Mon evolution

| Date | Lecon | Philosophie integree |
|---|---|---|
| 2026-08-05 | La portabilite est sacree | Portabilite d'Abord |
| 2026-08-05 | Tester avant de valider | Tester Avant de Valider |

---

## [NOTES] Notes de session

### Session du 2026-08-05

**Tache** : Creation de la fiche Vulcain

**Lecons apprises** :
- Vulcain est l'agent technique du cerveau-projet
- Il transforme les outils.md en outils reels
- La portabilite est sa priorite

---

## [CONNEXIONS] Connexions

| Fichier | Role |
|---|---|
| `vulcain.md` | Ma fiche principale |
| `AGENTS.md` | Fichier dynamique |
| `../../agents/regles-immuables/general/protocole-technologies/` | Protocole de choix technologique |
| `../../agents/regles-immuables/general/protocole-outils/` | Protocole de construction d'outils |

---

## [LECON] 2026-08-08 -- nettoyer-sessions v0.1.1 (parite sorties + bug latent 0\n0)

**Tache** : corriger la divergence de parite des sorties py/sh signalee par Morpheus (le .py affichait 'Nettoyage termine : N lignes supprimees', le .sh juste 'Nettoyage termine') et valider par retest Morpheus.
**Lecons** :
1. PARITE DES SORTIES : quand on cree un outil py+sh, les MESSAGES de sortie doivent etre strictement identiques (pas seulement les fichiers resultants) -- Morpheus a ajoute 6 assertions (reel + dry-run, CRLF normalise) qui figent la parite dans le test
2. BUG LATENT REVELE : nb=$(grep -c ... || echo 0) produit 0\n0 quand il y a 0 occurrence (grep -c affiche 0 ET echo 0 s execute) -> casse l arithmetique $((...)) du total -> TOUJOURS nb=$(grep -c ... 2>/dev/null); nb=${nb:-0} (piege deja documente, se manifeste des qu on utilise nb dans un calcul)
3. ORDRE DES BLOCS : dans une fonction, le test dry-run doit passer AVANT le test de valeur 0, sinon le message [DRY-RUN] Classeur : 0... est omis alors que le .py l affiche toujours -- l ordre des branches change la parite
4. LA BOUCLE FONCTIONNE : Morpheus a detecte le bug que mes validations de base (compile, ASCII, parite fichiers) ne voyaient pas -- la delegation des tests n est pas une formalite, elle protege la qualite
5. Versionner py/sh/md ENSEMBLE (0.1.0 -> 0.1.1) : la parite de version fait partie de la parite de l outil

## [LECON] 2026-08-08 -- valider-cartes-decision v0.3.0 (cible = parcours JSON)

**Tache** : mettre a jour valider-cartes-decision qui cherchait encore la section Carte de Decision dans les fiches allegees (-> --tous = 5/5 NON CONFORME a tort) pour valider le PARCOURS JSON, source de verite du guidage.
**Lecons** :
1. EVOLUTION DE CIBLE : quand un format change (fiches allegees v0.2.0 : la carte vit dans le parcours JSON), l OUTIL qui valide l ANCIEN format devient obsolete et produit des NON CONFORME a tort -- il faut migrer la cible de l outil DANS LA MEME logique que le format, pas seulement documenter
2. VALIDATIONS D UN PARCOURS : json.load, cles top-level (identite + parcours + cases), identite.type = parcours, case_depart existe, types valides (question/indice/controle/fin), references (suivant + branches.vers) vers des cases existantes, case c0 question de relecture (Pattern 4) -- les 6 controles couvrent la structure ET le standard de demarrage
3. PARITE .sh = WRAPPER : pour un outil dont la logique vit dans le .py, le .sh peut etre un wrapper pur (exec python3 "$PY_SCRIPT" "$@", pattern detecter-impacts) -- la parite des sorties est garantie PAR CONSTRUCTION (aucun doublon d en-tete, aucune divergence de logique)
4. INTERFACE PRESERVEE : combo-controle-outil appelle .py --tous -- une evolution de cible ne doit JAMAIS casser les appels existants (verifier les combos et parcours qui citent l outil)
5. --tous doit SCANNER les dossiers agents avec parcours/ (pas une liste en dur AGENTS_DEFAUT) : l outil devient automatiquement a jour quand un agent est cree
6. Test formel 24/24 (Morpheus, modele boucle) : --version, --tous 11/11, --agent, --fichier (parcours/.md), parcours corrompu = 3 erreurs, fichier inexistant, parite py/sh 4 cas, ASCII, nommage

## [LECON] 2026-08-08 -- valider-nommage v0.3.1 (bruit du scan recursif)

**Tache** : corriger le bruit du scan --recursive qui signalait en ERREUR les fichiers des sous-dossiers composants d un outil (tests/, spec/, protections/, __pycache__/).
**Lecons** :
1. STRUCTURE : le scan --recursive attend categorie/outil/fichiers directs. Les SOUS-DOSSERS COMPOSANTS (tests/, spec/, protections/, __pycache__/) ne sont pas des outils : leurs fichiers (test-*, spec-*) ont leur propre convention et ne doivent PAS etre valides avec le prefixe de la categorie parente
2. CORRECTION A 2 NIVEAUX : exclure les composants au niveau CATEGORIE (ex: tester/tests/) ET au niveau OUTIL (ex: activer-agent-principal/tests/) -- une seule exclusion laisse le bruit sur l autre niveau
3. PARITE : la liste d exclusion doit etre definie dans le .py (constante) ET le .sh (variable + grep -vE dans le find) -- les 2 modes recursifs (listdir .py, find .sh) doivent filtrer pareil
4. CAS PARTICULIER tester/ : protections/ est aussi un conteneur de composants (structure tester/protections/<outil>/) -- il faut l ajouter a la liste (c est le 3e conteneur apres tests/ et spec/)
5. REGRESSION : verifier l usage NORMAL (scan global tools/) ET l usage sur categorie/outil directement -- le bruit n etait visible que sur le 2e usage (scan global deja propre car il ne descend pas dans les sous-dossiers d outils)
6. Test formel 13/13 (Morpheus) : aucune regression -- les modes --mots-seuls et --type restent inchangees (la correction ne touche QUE le mode recursif de nommage)

## [LECON] 2026-08-08 -- Catalogue generateur 12 commandes (absorber les 2 combos)

**Tache** : etape 4 plan combo-orchestrateur -- declarer les 2 combos manquants (combos-valider-cerveau, combos-corriger-non-ascii) dans catalogue-commandes.json (10 -> 12 commandes).
**Lecons** :
1. Le catalogue est la SOURCE DE VERITE du generateur : chaque entree = un modele d appel d outil deja ecrit, corrige et valide -- ajouter une commande = copier le modele reel de l outil (script + parametres exacts), jamais une invention
2. FORMAT ENTREE : nom, description, interpreteur, script, modele ({parametre} en dur dans le modele), parametres (cle/question/type/obligatoire/defaut/flag/quoter) -- les parametres optionnels portent un defaut (flag -> defaut non, texte -> defaut valeur)
3. Les FLAGS se declarent avec type flag + champ flag (--detail, --stop, --dry-run, --all, --rapport) et defaut non : le generateur les omet si non, les ajoute si oui -- teste avec --reponses 'flag=oui'
4. LES COMBOS SONT ABSORBES DANS LE CATALOGUE : audit-general (deja present), valider-cerveau et corriger-non-ascii (ajoutes) -> le generateur peut composer la commande de N IMPORTE QUEL combo, c est la porte d entree des cases generateur du combos-moteur (Pattern 3)
5. VALIDATION : JSON valide (12 commandes), --liste 12, --commande + --reponses compose la commande exacte (avec defauts / avec flags), parite .sh (les 2 versions listent 12 et composent la meme commande -- la diff brute py/sh est uniquement CRLF vs LF, comportement Windows normal)
6. Le generateur et les 2 combos sont INCHANGES : seul le catalogue a ete modifie -- la source de verite des combos reste leurs dossiers agents/tools/combos/

## [LECON] 2026-08-08 -- Combos-moteur v0.1.0 (3 bugs detectes par Morpheus)

**Tache** : construire le moteur generique combos-moteur (py + sh) selon la spec-combos-moteur v0.1.0.
**Lecons** :
1. PIEGE CHEMIN_RACINE : depuis un script dans agents/tools/combos/combos-moteur/, il faut **5 remontees** depuis le FICHIER .py (combos-moteur -> combos -> tools -> agents -> cerveau-projet) mais **4 depuis le DOSSIER** du .sh (via COMBO_MOTEUR_DIR) -- j'ai d abord mis 4 partout -> chemin agents/agents/tools/ (generateur introuvable). La parite py/sh exige de compter le nombre de niveaux selon la base (fichier vs dossier).
2. PIEGE EXTRACTION GENERATEUR : generateurs-commande imprime la commande sur la ligne SUIVANTE le marqueur `=== COMMANDE A LANCER ===` (pas sur la meme ligne) -- prendre la premiere ligne non vide APRES le marqueur, sinon la commande generee est vide.
3. PIEGE PARITE SORTIE : dans le .py, `_couleur("=== COMBO TERMINE ===\n")` avec un \n integre ajoute un double saut de ligne absent du .sh (texte brut) -> les sorties py/sh divergent dans les tests de parite. Ne jamais mettre de \n dans _couleur, toujours dans un print() separe.
4. PIEGE TEST WINDOWS : dans un test Python, un script .sh doit etre appele avec ["bash", script, ...] sinon WinError 193 (pas une application Win32 valide).
5. Le modele du moteur (guider-parcours.py) : charger_definition + valider_definition + navigateur generique -- le combos-moteur suit le meme squelette pour les combos.

## [LECON] 2026-08-08 -- generateurs-carte v0.1.0 + generateurs-case v0.2.0 (etape OUTILS de la refonte du modele de cases)

**Tache** : creer l'outil CARTE (agit sur la carte COMPLETE) et etendre generateurs-case pour les GROUPES de cases (modele compose Pattern 7).
**Lecons** :
1. CONCEPT : generateurs-case = 1 case (liste/ajouter/editer/supprimer/ajouter-bloc) ; generateurs-carte = carte COMPLETE (creer un squelette patterns 4-5-6-7, analyser les chemins BFS, detecter 5 types d'anomalies, dupliquer un chemin avec recablage). Les deux sont complementaires et vivent cote a cote dans generateurs/.
2. ACTION ajouter-bloc (Pattern 7) : cree d'un coup decision (question 2 branches OUI->deviation / NON->suite) + deviation (indice -> rejoint) + rejoint (indice -> suite) -- ids par defaut cN/cNa/cNb, --suite obligatoire, --apres pour le recablage du suivant. Le bloc est navigable PARCOURS TERMINE sur les 2 branches.
3. ACTION creer : le squelette doit reproduire EXACTEMENT les cases des parcours reels (c0 question honnete OUI->c0c/INCERTAIN->c0b/NON->c0b, c0b RELIRE, c0c CONTEXTE avec lire-activite-recente + AGENTS.md, c1 Mission, fin active) -- un squelette qui oublie un pattern serait un faux depart.
4. ACTION analyser : BFS de case_depart vers les fins avec anti-boucle (jamais repasser par une case du chemin courant) -- 6 chemins pour le squelette (3 branches c0 x 2 branches c1), les impasses marquees [impasse].
5. ACTION detecter : 5 controles (references cassees, boucle d'attente regle 10 avec 'attente' dans titre/question + branche vers soi, cases inatteignables, cases sans sortie, decision a branche unique Pattern 7) -- la boucle d'attente n'est detectee QUE si le titre/question porte 'attente' (test negatif : branche vers soi sans 'attente' n'est pas une boucle d'attente).
6. ACTION dupliquer-chemin : BFS debut->fin, copies prefixees (d+id), references INTERNES recablees vers les copies, references EXTERNES restent sur les originales (les copies ne sont pas branchees automatiquement sauf --brancher-debut) -- detecter signalera donc les copies comme inatteignables (comportement attendu et documente).
7. PIEGE ARGPARSE : ne pas nommer une option --version sur une sous-commande qui recoit aussi le --version global de la boucle commune (conflit) -- renommer (--ver pour la version du parcours cree).
8. PIEGE HEREDOC .sh : le .sh de generateurs-case etait un heredoc complet (ancien pattern) -- je l'ai CONVERTI EN WRAPPER PUR (exec python3 -- "$@") : parite garantie par construction, plus de divergence de version entre les 2 fichiers.
9. VALIDATION : py_compile + bash -n, parite py/sh (analyser + liste identiques CRLF normalise), ASCII 0 sur 6 fichiers outils + spec v0.2.14 + index + fiche, nommage generateurs- OK, tests reels sur copies workspace (creer 6 cases, analyser 6 chemins, detecter 0 puis 5 anomalies, dupliquer 3 copies, ajouter-bloc navigation OUI/NON PARCOURS TERMINE).
6. Test 31/31 REUSSI par Morpheus (regle delegation respectee) : --liste, navigation OUI/NON, interpolation, generateur AUTO, variable manquante code 1, dry-run, parite, nommage, ASCII, syntaxe.

## [NOTES] Spec-combos-moteur + Pattern 3 2026-08-08 (combo orchestrateur)

**Mission** : specifier le format definition-combo.json (futur outil combos-moteur) + documenter le Pattern 3 (generateur -> execution) dans spec-guider-parcours v0.2.4.
**Lecons** :
1. Le COMBO devient l'orchestrateur : l'agent lance UN combo (definition-combo.json lu par combos-moteur, meme philosophie que guider-parcours lit parcours-<agent>.json) au lieu d'une suite d'outils -- plus transparent, plus fiable, plus digeste
2. Le dataflow du combo : chaque case generateur appelle generateurs-commande --reponses (mode AUTO, alimente par les variables) -> compose la commande ; la case outil l'execute -> sortie = variable ; la case controle decide si le resultat est transmis BRUT ou si un generateur s'intercale
3. Le generateur-commande reste INCHANGE : le moteur fait le lien avec --reponses -- le generateur est la source de verite de la syntaxe (modele valide du catalogue), il devient INCONTOURNABLE comme composeur des cases generatrices
4. Variables : memoire INTERNE du combo (dict) par defaut, persistance optionnelle vers classeur-variables (persistant: true) -- pas d'ecriture disque a chaque case
5. Le Pattern 3 est documente dans spec-guider-parcours (bump v0.2.3 -> v0.2.4) : une case de parcours peut pointer vers un combo (indice outil combos-moteur + indice fichier spec) -- la procedure d'audit passe de 2 a 3 patterns (point 3 dedie) + critere d'acceptation 11
6. PIEGE ASCII : j'ai d'abord ecrit 'enchain-er' avec un i accentue (i circonflexe, U+00EE) dans le Pattern 3 -- detecte et corrige en 'enchainer' avant la validation ; verifier le texte dans les sections ajoutees, pas seulement le contenu recopie
7. Separation des domaines : le combo (definition JSON) est un fichier du cerveau (Buffy), le moteur est un outil (Vulcain) -- la spec le documente pour eviter les conflits
8. Bump spec-guider 0.2.3 -> 0.2.4 + doc guider-parcours 0.2.9 -> 0.2.10 (regle 8 ajoutee) -- les CLI de guider-parcours restent inchangees (distinction version doc vs outil)

## [NOTES] Spec-guider-parcours v0.2.3 2026-08-08 (prototype vulcain cas legitime assume)

**Mission** : documenter le prototype vulcain comme cas legitime ASSUME (fins independantes) au lieu de le corriger (demande utilisateur).
**Lecons** :
1. Le prototype vulcain est desormais documente comme CAS LEGITIME ASSUME : fins independantes par chemin (construire c9, modifier c15, autre c18/c19) = choix documente, PAS un defaut a corriger
2. La reformulation est coherente avec la regle 8 AUTONOMIE : ne pas converger est legitime quand chaque parcours reste individuel et complet -- le Pattern 1 (convergence) est une factorisation recommandee, pas une obligation absolue
3. Les cas particuliers de la procedure d'audit sont maintenant 2 : routage (cerberus, Pattern 2 non applicable) + prototype (vulcain, fins independantes assumees) -- le rapport Themis doit etre aligne (recommandation 2 : plus de correction a faire)
4. Bump spec 0.2.2 -> 0.2.3 + doc 0.2.8 -> 0.2.9 -- CLI inchangees

## [NOTES] Spec-guider-parcours v0.2.2 2026-08-08 (regle d'autonomie des parcours)

**Mission** : ajouter la regle d'autonomie des parcours dans la spec (demande utilisateur : chaque parcours doit rester individuel pour pouvoir etre complete par la suite).
**Lecons** :
1. REGLE 8 AUTONOMIE : chaque parcours est un fichier INDIVIDUEL par agent, la convergence est uniquement INTRA-parcours (factorisation interne des cases communes d'un meme parcours), AUCUN partage de cases entre parcours, chaque parcours est complet et validable independamment
2. La regle documente une realite deja vraie : l'audit a confirme qu'aucun des 11 parcours ne reference les cases d'un autre (0 reference croisee) -- la regle verrouille l'intention pour les futures creations
3. La convergence du Pattern 1 est une FACTORISATION INTERNE (les chemins d'un meme agent rejoignent SES cases communes), pas un partage inter-parcours -- la regle 8 le rend explicite pour lever l'ambiguite
4. La procedure d'audit a une sous-section Autonomie (verifier l'absence de references croisees) en plus des Pattern 1-2
5. Bump spec 0.2.1 -> 0.2.2 + doc guider-parcours 0.2.7 -> 0.2.8 (regle 7 AUTONOMIE ajoutee dans la section Regles de la doc) -- les CLI restent 0.1.0-py/-sh

## [NOTES] Spec-guider-parcours v0.2.1 2026-08-08 (procedure d'audit des 2 patterns)

**Mission** : documenter dans la spec la procedure d'audit des 2 patterns validee par l'audit des 11 parcours par Themis.
**Lecons** :
1. La procedure d'audit est maintenant dans la spec (section dediee v0.2.1) : Pattern 1 (case Mission question + branches + convergence, --liste + lecture structurelle), Pattern 2 (verification structurelle : PREMIER element des indices des cases d'ecriture = regle ASCII, plus fiable qu'une simple recherche de texte), cas particuliers legitimes (routage sans case d'ecriture, prototype sans convergence), revalidation complete (json.load + --liste + --reponses + ASCII)
2. L'audit de Themis a revele que la verification par grep seul ('REGLE IMMUABLE ASCII' present dans le fichier) ne suffit pas : la REGLE doit etre en POSITION 1 des indices -- d'ou la verification structurelle documentee
3. Quand une procedure est validee par un audit externe (Themis), la capitaliser dans la spec de l'outil pour que les prochaines creations naissent conformes et que l'audit soit reproductible
4. Bump spec 0.2.0 -> 0.2.1 (documentation seulement) + doc guider-parcours 0.2.6 -> 0.2.7 (reference spec) -- les CLI restent 0.1.0-py/-sh (version outil inchangee, distinction version outil vs doc vs spec)

## [NOTES] Doc guider-parcours v0.2.1 2026-08-07 (liste complete des parcours)

**Mission** : completer la liste des parcours dans la doc (ajout cerberus + buffy -> 6 parcours).
**Lecons** :
1. La liste Emplacement des parcours doit TOUJOURS etre synchronisee avec les parcours reels (agents/*/parcours/*.json) -- apres chaque creation de parcours, verifier si la doc a besoin d etre completee (cerberus et buffy manquaient)
2. Un bump de version DOC mineur (0.2.0 -> 0.2.1) suffit pour une mise a jour de liste -- les CLI restent inchangees
3. Ne jamais supprimer l'historique : la ligne 0.2.0 est mise a jour (liste completee) ET une ligne 0.2.1 est ajoutee pour tracer le changement

## [NOTES] Doc guider-parcours v0.2.0 2026-08-07 (reference spec + patterns)

**Mission** : mettre a jour la doc de l'outil pour referencer la spec v0.2.0 et les 2 patterns.
**Lecons** :
1. Bump de la DOC seulement : la version de la doc passe a 0.2.0 mais les CLI restent 0.1.0-py/-sh (l'outil n'a pas change, seule la doc evolue) -- distinguer version de l'outil et version de la documentation
2. La doc doit rester SYNCHRONISEE avec la spec : section Patterns + regles 5-6 ajoutees a la doc, identiques a la spec v0.2.0 (regles 6-7 du format) -- le lien Spec en en-tete et le tableau Versionning documentent la coherence
3. La liste des parcours de la doc doit couvrir TOUS les parcours existants (vulcain, morpheus, clio, janus) -- pas seulement le prototype

## [NOTES] Spec-guider-parcours v0.2.0 2026-08-07 (patterns)

**Mission** : documenter dans la spec les 2 patterns valides en production (demande utilisateur).
**Lecons** :
1. Le pattern MULTI-MISSIONS (case Mission + branches + chemins convergents) est documente dans la spec : un parcours peut couvrir plusieurs missions d'un agent, les chemins convergent vers les cases communes (verdict, lecons, retour) pour eviter la duplication -- exemple reel : parcours-janus.json (30 cases, 3 chemins)
2. Le rappel ASCII est devenu une REGLE DE FORMAT (regle 6 + Pattern 2) : toute case qui ecrit dans un fichier DOIT porter un indice regle ASCII en TETE de sa liste indices -- verification par grep 'REGLE IMMUABLE ASCII'
3. Versionner une spec : la version vit dans le .md (v0.1.0 -> v0.2.0), pas de dossier versions/ -- conserver le statut ebauche tant que l'outil n'est pas en production

## [NOTES] Spec-guider-parcours v0.2.5 2026-08-08 (Pattern 4 : case Question Honnete en case 0)

**Mission** : figer le nouveau standard de demarrage dans la spec -- la case c0 Question Honnete de relecture + c0b RELIRE obligatoire + case_depart = c0.
**Lecons** :
1. Le Pattern 4 documente ce qui etait deja une realite de production : les 11 parcours portent c0 (question memoire, SANS relire) + c0b (RELIRE obligatoire, corrections puis fiche) et demarrent en c0 -- l'audit Themis 11/11 (CONFORME 100/100) est la preuve de validite citee dans la spec
2. La regle 9 du format generalise le standard : TOUT parcours demarre en c0, branches exactes OUI -> c1 / INCERTAIN -> c0b / NON -> c0b, c0b -> c1, case_depart = c0, question contenant 'memoire' + 'SANS relire' -- un parcours qui ne demarre pas en c0 est un ecart
3. La procedure d'audit passe de 3 a 4 patterns : section 4 dediee (case_depart c0, question memoire, branches exactes, c0b RELIRE + corrections + fiche, navigation OUI/NON/INCERTAIN -> PARCOURS TERMINE) + renumero des sections 4-6 -> 5-7 + critere d'acceptation 12
4. Le Pattern 4 a un exemple JSON complet (parcours + c0 + c0b + c1) et l'exemple reel des 11 parcours -- les futurs parcours naissent conformes
5. SYNCHRONISATION TRIANGLE (spec + doc + fiche) : bump spec 0.2.4 -> 0.2.5 (header agent + historique) + doc guider-parcours 0.2.10 -> 0.2.11 (header spec, section Patterns 4, regle 9, versionning) + fiche vulcain (reference spec v0.2.3 -> v0.2.5 + entree historique) -- les 3 doivent referencer la meme version de spec
6. PIEGE ASCII : dans la formulation de la question honnete, eviter les guillemets non-ASCII -- utiliser la question exacte telle que portee par les parcours (mots 'memoire' et 'SANS relire' en MAJUSCULES) ; verifier le texte des sections ajoutees avec valider-conformite-ascii
7. Un bump de SPEC (documentation) n'impacte pas les CLI : guider-parcours.py/.sh restent 0.1.0-py/-sh -- seule la spec + la doc evoluent

## [NOTES] Convention identification v0.5.0 (2026-08-08) -- aucun mot seul

**Mission** : renommer les champs d'identification pour ne jamais utiliser un mot seul
(nom, role, statut...). Decision utilisateur : Id LLM -> Nom LLM (en tete du bloc),
Nom -> Nom Agent, Role -> Role Agent. Fiches YAML : nom -> nom-agent, role -> role-agent,
statut -> statut-<agent>. role_principal et role_specifique restent (deja composees).

**Livrables** :
1. activer-agent-principal v0.5.0 (py + sh) : bloc session en Nom LLM (EN TETE) / Nom Agent /
Role Agent ; reconstruction complete du bloc en ordre canonique a chaque edition ; migration
automatique des anciens champs (Nom -> Nom Agent, Role -> Role Agent, Id LLM -> Nom LLM) ;
table Sessions connues en colonne Nom LLM ; lecture retrocompatible (Id LLM|Nom LLM)
2. lister-agents v0.3.0 (py + sh) : lecture role-agent / statut-<agent> avec repli anciens noms
3. evaluer-agents v0.2.2 (py + sh) : verification de l'agent actif sur **Nom Agent** (le grep
'Nom' simple matcherait desormais **Nom LLM** en premier -- piege detecte)
4. Tests : test-007 v0.5.0 cree (22/22), test-001/002/006 mis a jour (nouveaux champs)

**Lecons** :
1. LA RECONSTRUCTION COMPLETE DU BLOC (pas le remplacement ligne a ligne) est la seule
approche fiable pour une migration de champs : elle garantit l'ordre canonique (Nom LLM en
TETE), l'insertion des champs manquants et la migration des anciens noms en une passe
2. RETROCOMPAT LECTURE : toujours accepter l'ancien nom en lecture (Id LLM|Nom LLM) le temps
que tous les blocs soient migres -- sinon un ancien bloc casse la reconnaissance
3. PIEGE grep 'mot seul' : un grep 'Nom' matche **Nom LLM** en premier -- chercher le champ
complet (**Nom Agent**) avant l'ancien nom
4. PIEGE test negatif : un grep -q qui ne trouve rien retourne 1 -- pour un check 'AUCUN champ',
inverser la logique (if grep; then check 1; else check 0) sinon le test echoue a tort
5. PARITE py/sh : reconstruire le bloc a l'identique dans les deux versions (l'en-tete du
tableau et la ligne vide doivent etre re-emis) ; sinon le .sh reimprime l'ancien en-tete en parasite
6. La convention 'jamais de mot seul' vaut pour les CHAMPS IDENTIFIANTS (nom, role, statut) --
les mots composees deja qualifies (role_principal, role_specifique) restent inchanges
7. REGLE FONDAMENTALE (2026-08-08) : la detection des mots seuls doit distinguer 3 categories :
   (a) IDENTIFIANTS generiques interdits (nom, role, statut, id, date, cible -> liste noire explicite),
   (b) cles de SCHEMA de fiche autorisees (version, cree, specialites, forces, faiblesses -> liste blanche),
   (c) exceptions structurelles du format identite (type, commun, tags, appartient_a).
   Un detecteur qui signale TOUT mot seul produit des faux positifs massifs (fiches agents) :
   il faut une liste noire ciblee, pas une regex universelle.
8. LES TRACES DOCUMENTAIRES sont des documents figes : les rapports (janus/controles, corrections.md,
   mission-condenseur) documentent d'anciennes conventions et NE SONT PAS corriges. Le detecteur
   --mots-seuls ignore les dossiers de traces (controles, rapports, retro-actions, historique,
   exemples) en mode recursif + les fichiers traces assumes (mission-condenseur.md).
9. INTERPOLATION {var} : accepter les TIRETS (kebab-case) dans les noms de variables -- le regex
   [A-Za-z0-9_]+ rate {ma-variable} et laisse la cle brute non substituee. Toujours utiliser
   [A-Za-z0-9_-]+ (bug detecte lors du test de la case critere du combos-moteur).
10. CASE CRITERE combos-moteur v0.2.0 : l'embranchement AUTOMATIQUE (fichier-existe, egalite,
    non-vide, sortie-contient, fichier-contient) avec vers-vrai/vers-faux repond a la decision
    utilisateur 'les criteres dans les combos, pas dans les cartes'. La validation exige
    condition.type connu + vers-vrai ET vers-faux existants.

## [LECON] 2026-08-08 -- Regles immuables dans les generateurs (garde-fou RVAV + delegation + ASCII)

**Tache** : ajouter les REGLES IMMUABLES dans les generateurs (constat utilisateur : RVAV absent de generateurs-case/carte 0 occurrence -> les nouvelles cartes/cases ne rappelaient plus les regles immuables ; la delegation etait court-cuitee : tests faits par l'agent au lieu de Morpheus, Janus jamais active).
**Lecons** :
1. UN GENERATEUR PORTE LES REGLES DU FORMAT QU IL PRODUIT : si les regles immuables (RVAV, delegation, ASCII) ne sont pas dans les generateurs, TOUTE nouvelle carte/case nee de l'outil nait SANS ces regles -- la chaine de delegation se degrade silencieusement a chaque generation. Le generateur est le point d'entree : c est la qu il faut rappeler les regles.
2. GARDE-FOU NON BLOQUANT (pattern existant Pattern 5) : l'avertissement est JAUNE, l'operation reussit quand meme, l'agent decide -- jamais bloquer la generation, toujours rappeler.
3. generateurs-case v0.2.1 : fonction formuler_avertissement_regles_immuables(case) appelee a la construction (construire_case) + edition (action_editer) + ajouter-bloc (les 3 cases du bloc) -- detection : (a) case d'ECRITURE (indice outil creer/ecrire/editer/ajouter/inserer/copier-fichier) sans rappel ASCII en position 1 -> RAPPEL ASCII (Pattern 2) + RAPPEL RVAV ; (b) case fin avec message morpheus/janus/active/reactive -> RAPPEL DELEGATION chaine bout-en-bout (spec v0.2.15) ; (c) autre fin -> RAPPEL RVAV avant activation.
4. generateurs-carte v0.1.1 : le squelette creer est ENRICHI -- case c2b RVAV avant la fin (regle RVAV complete + fichier rvav-workflow) + rappel ASCII dans c2 + fin c9 rappelant la chaine bout-en-bout (J ACTIVE le maillon suivant a MA fin, dernier maillon REACTIVE Cerberus avec bilan consolide). Un squelette qui oublie RVAV/delegation est un faux depart.
5. PIEGE TEST : generateurs-carte prend l ordre `creer <parcours>` (action avant chemin), generateurs-case `<parcours> <action>` (chemin avant action) -- les 2 CLI sont differentes, ne pas copier l ordre de l un dans l autre.
6. PIEGE OPTION : `--vers` n existe que pour supprimer (pas pour ajouter) -- un ajout de fin avec --vers echoue silencieusement dans le test.
7. VALIDATION : py_compile + bash -n, parite py/sh (wrapper pur .sh = parite par construction), ASCII 0 sur 5 fichiers, nommage OK, tests reels sur copies workspace (3 cas de garde-fou : fin delegation -> rappel chaine ; edition fin -> rappel chaine ; case ecriture sans ASCII -> rappel ASCII + RVAV).

## [LECON] 2026-08-08 -- verifier-documents-manquants v0.3.0 (extension .py + branchement procedure 4g)

**Tache** : etendre l outil EXISTANT verifier-documents-manquants pour couvrir les .py (il ne verifiait que les paires .sh/.md) et le brancher dans la procedure 4g du Pattern 9 (decision utilisateur : etendre l outil existant, pas en creer un nouveau).
**Lecons** :
1. UN OUTIL EXISTE MAIS N EST PAS BRANCHE = INVISIBLE (lecon des outils fantomes) : verifier-documents-manquants existait depuis le debut mais (a) ne couvrait pas les .py (les parcours referencent surtout les .py depuis la vague 2) et (b) n etait PAS cite dans la procedure 4g du Pattern 9 -- la spec disait verifier a la main que le .md deduit existe, alors que l outil le fait automatiquement. Avant d ecrire une verification manuelle dans une spec, chercher l outil qui l automatise deja.
2. EXTENSION .PY : la logique de paire est identique (script -> .md du meme nom), on ajoute une 2e passe pour .py et le .md doit trouver son script en .sh OU .py (un .md avec .sh mais sans .py n est PAS un manquant : la regle est au moins un script).
3. FILTRE FAUX POSITIFS ELARGI : le scan tools/ revelait 9 manquants qui etaient TOUS des faux positifs non couverts -- dossier tests/, prefixe tester- (avec -v0xx : les fichiers de test versionnes), suffixe -test.md, et outils-base.md (document de support racine). PIEGE : ne PAS filtrer tout tester- : les outils REELS tester-protection-* (dossier tester/protections/) doivent rester verifies -- le filtre ne les ecarte que dans tests/ ou avec -v0xx.
4. WRAPPER PUR : le .sh (heredoc 248 lignes avec un bug de structure) est converti en wrapper pur (exec python3 du .py a cote, pattern guider-parcours v0.3.0) -- parite garantie par construction, plus de divergence de version ni de bug de heredoc.
5. VALIDATION : parite py/sh, test negatif (un .py sans .md est detecte 1 manquant), scan complet tools/ = 0 manquant (110 .sh, 95 .py, 111 .md), protections toujours verifiees, ASCII 0 sur 4 fichiers, branchement verifie dans la spec (procedure 4g point 3 = lancer l outil, resultat attendu 0 manquant).
6. VERSION DOCUMENTEE : la doc .md v0.3.0 reference le Pattern 9 et la procedure 4g comme usage principal (situation Quand l utiliser + relation avec guider-parcours).

## [LECON] 2026-08-08 -- generateurs-carte v0.2.0 (squelette conforme aux 11 patterns : Pattern 10 + Pattern 3)

**Tache** : mettre a jour le squelette creer de generateurs-carte pour integrer le Pattern 10 (une carte = un role) et le Pattern 3 (rappel des combos) dans les nouvelles cartes (decision utilisateur, suite du constat stabilite des cartes -- la spec-guider-parcours est passee a v0.2.19 avec les 11 patterns, mais le squelette nait encore avec les patterns 4-5-6-7-8).
**Lecons** :
1. UN SQUELETTE DE CARTE EST LE MOMENT D ENTRER DANS LE CYCLE DE VIE : si le squelette n integre pas un pattern au moment ou il est ajoute a la spec, TOUTE carte nee de l outil apres cette date nait SANS ce pattern -- les futures cartes se degradent silencieusement. Le squelette doit suivre la spec pattern par pattern (ici v0.2.19 = 11 patterns).
2. POSITIONNEMENT DES RAPPELS : Pattern 10 (UNE CARTE = UN ROLE) place en tete des indices de c1 (la case Mission, la premiere action de la carte -- l agent voit le role AVANT de choisir une mission) ; Pattern 3 (RAPPEL DES COMBOS) place en tete des indices de c2 (la case action exemple -- l agent pense combo AVANT d enchainer des outils) ; les indices existants (Pattern 7, ASCII) passent en position 2-3 sans conflit.
3. TEXTES DES RAPPELS : Pattern 10 = la carte ne contient QUE des actions propres au role de l agent (activation/verification/decision), JAMAIS d outils d analyse/execution d un autre role + piege du glissement (lire pour DECIDER vs lire pour EXECUTER) ; Pattern 3 = une suite lineaire d outils repetee (>= 2) ou longue (>= 3) doit etre encapsulee dans un combo Lancer le combo X (combos-moteur + definition-combo.json, protocole-creation-combos) -- 1 case = 1 combo.
4. PIEGE CLI CONFIRME (deja note) : generateurs-carte prend l ordre `creer <parcours>` (action avant chemin), generateurs-case `<parcours> <action>` (chemin avant action) -- ne pas copier l ordre de l un dans l autre.
5. PIEGE TEST : ne PAS creer le squelette de test dans /tmp (hors workspace, regle workspace : ecriture = workspace seul) -- creer dans un dossier temporaire DU WORKSPACE (.tmp-gc-test/) puis supprimer apres validation.
6. VALIDATION : py_compile, squelette de test cree (c1 porte Pattern 10, c2 porte Pattern 3 en position 1 + Pattern 7 + ASCII), navigation PARCOURS TERMINE, --liste 7 cases, references validees, ASCII 0 sur py + md, nommage code 0, parite py/sh (wrapper pur = parite par construction), doc .md bumpee v0.1.1 -> v0.2.0 avec ligne de versionning.
7. LA CHAINE CONTINUE (Pattern 8) : Vulcain termine et ACTIVE Morpheus pour tester (c est l agent delegue qui active le suivant a SA fin, pas Cerberus).

## [LECON] 2026-08-08 -- PISTE C VOLET 1 : champ catalogue optionnel sur les indices outil (guider-parcours v0.3.1)

**Mission** : etendre le format des indices outil avec un champ catalogue optionnel (reference a la commande du catalogue generateurs-commande) et l afficher dans guider-parcours. Strategie validee par l utilisateur : champ AJOUTE + commande en dur CONSERVEE comme fallback.
**Lecons** :
1. FORMAT : l indice outil accepte maintenant 4 cles : nom, chemin, commande, catalogue (optionnel) -- le catalogue = nom de la commande dans catalogue-commandes.json, la commande en dur reste le fallback. Le champ est OPTIONNEL : absence = comportement historique, les 11 parcours existants restent PARCOURS TERMINE sans modification.
2. AFFICHAGE : guider-parcours afficher_indices affiche catalogue: <nom> + une ligne PASSE PAR LE GENERATEUR avec la commande du generateur (--commande <nom>) quand le champ est present -- le Pattern 9 (LIRE AVANT USAGE deduit du chemin) reste intact et s affiche dans les deux cas.
3. PARITE : le .sh est un wrapper pur qui delegue au .py (parite par construction) -- le test de parite sur le parcours de test confirme PARITE OK.
4. NON-REGRESSION : la navigation des 11 parcours (sans champ catalogue) reste PARCOURS TERMINE 11/11 -- le champ est strictement additif.
5. PIEGE rfind : inserer du texte en fin de la longue ligne Historique de la spec avec txt.rfind(marker) a cible la mauvaise occurrence (la ligne 12 Agent plutot que la ligne 13) -- pour les lignes uniques et longues, cibler l index de ligne exact (lignes[12] += ajout).
6. VALIDATION : py_compile, bash -n, parite py/sh, navigation avec et sans champ catalogue (parcours de test), non-regression 11/11, ASCII 0 sur 4 fichiers (py/sh/md/spec).
| VERITE | Une reference au catalogue (champ catalogue) rend chaque commande des parcours retracable et recomposable via generateurs-commande, sans casser les commandes en dur existantes |

## PHILOSOPHIE -- Principes de comportement

| **Relire sa fiche a chaque activation** | Quand je suis active ou reactive, je relis MA fiche et MES corrections avant de continuer. Je ne lis que mes fichiers, jamais ceux des autres agents : chacun lit les siens en prenant le relais. |
## [LECON] 2026-08-08 -- OUTIL verifier-restauration-sure + INCIDENT catalogue ecrase (git checkout) + REGENERATION

**Mission 1 (demande utilisateur)** : creer verifier-restauration-sure (detecter les fichiers non commites avant restauration git - application de la regle Restauration securisee, lecon incident piste B). Cree dans verifier/verifier-restauration-sure/ (.py + .sh wrapper + .md + spec/) : git status --porcelain, mode global (OK/ATTENTION) + mode --fichier (code 0/1), hors workspace code 2, parite py/sh, rappel de la regle. index-tools mis a jour (104 -> 105).

**INCIDENT (FAUTE GRAVE -- la lecon piste B s est REPRODUITE)** : pendant l ajout de la commande au catalogue, json.dumps(indent=1) a reformate tout le fichier (2997 insertions). Pour annuler, j ai lance `git checkout -- catalogue-commandes.json` SANS verifier l etat de travail : le fichier contenait 98 commandes NON COMMITEES (piste A) -> restaure a 13, 85 commandes perdues. C est EXACTEMENT le scenario de l incident piste B, malgre le garde-fou documente. La regle Restauration securisee etait en memoire mais PAS APPLIQUEE (verifier git status avant).

**REPARATION** : regeneration complete du catalogue selon la methode de la lecon piste A (corrections buffy 499-511) : scan des 94 outils reels (.py hors tester/spec/combos), parsing de l aide (usage: + continuation stricte + filtrage du nom d outil), 13 commandes originales conservees intactes, entrees speciales corrigees (generateurs-carte subcommandes, combos-moteur, verifier-restauration-sure aide custom). RESULTAT : 105 commandes, 0 script relatif, 0 modele parasite ({--flag}), toutes les 53 refs parcours couvertes, non-regression combos OK, generation reelle verifiee (valider-nommage, verifier-restauration-sure).

**LECONS (a integrer)** :
1. JAMAIS git checkout / git restore / git reset --hard sur un fichier NON COMMITE : verifier git status AVANT toute restauration (la regle existe, il faut l APPLIQUER meme en urgence).
2. Les fichiers DERIVES (catalogue-commandes.json genere par script) doivent garder leur script de generation : la regeneration a sauve la mission.
3. json.dumps reformate TOUT un fichier : pour editer un JSON, insertion chirurgicale texte (indentation 2 espaces + CRLF respectes).
4. Un --aide custom (pas argparse) n expose pas usage: -> entree speciale du catalogue.
5. Le parseur doit ignorer le nom de l outil dans usage: (positionnel parasite).
## [LECON] 2026-08-08 -- OUTIL generateurs-regenerer-catalogue cree (remplacant durable du script temporaire piste A)

**Objet** : creer un outil PERMANENT pour regenerer/synchroniser le catalogue-commandes.json du generateur, en extrayant les VRAIES descriptions depuis les en-tetes .py (eviter de re-corriger a la main apres chaque regeneration - lecon piste A : 63 entrees cosmetiques corrigees par Buffy).
**Livrable** : generateurs-regenerer-catalogue/ (.py + .sh wrapper + .md + spec/) dans la categorie generateurs/. Modes : --dry-run (defaut) / application (synchronisation preservant l existant) / --force (reconstruction complete).
**Test de bout en bout** : outil fictif temporaire cree dans generateurs/ -> dry-run le propose avec la description extraite du docstring -> supprime sans residu. Dry-run sur catalogue reel : 86 outils scannes, 82 preserves, 0 a ajouter (aucune regression).
**Lecons** :
1. REGLE NOMNAGE : le nom d un outil DOIT commencer par le prefixe de la CATEGORIE (generateurs-*) - j ai d abord cree regenerer-catalogue/ (ERREUR valider-nommage : prefixe dossier manquant) puis renomme en generateurs-regenerer-catalogue/ (git mv + mv des 4 fichiers).
2. SCHEMA IDENTITE : un outil .py/.sh doit porter le bloc identite: (type/appartient_a/commun) sinon detecter-impacts le signale NON MIGRE - ajoute apres le shebang (comme verifier-systeme).
3. AUTO-EXCLUSION : le regenerateur doit s exclure lui-meme du scan (outil_dir == generateurs-regenerer-catalogue) sinon il s ajouterait a son propre catalogue.
4. La spec est un FICHIER IMPLIQUE de l outil (detecter-impacts la reference) : la toucher apres modification du .py pour passer le VERDICT a jour.
5. Extraction descriptions : 2 formats d en-tete (.py docstring triple-quote / commentaires #), jointure des phrases coupees par : ou ,, translitteration ASCII NFKD, limite ~90 caracteres. Les 13 commandes originales + 3 entrees speciales (generateurs-carte, combos-moteur, verifier-restauration-sure) ne sont jamais regenerees.
6. PIEGE CRLF PARASITE (encore) : normaliser LF en memoire puis reecrire CRLF uniforme - le json.dumps(indent=2) + replace(n, rn) est maintenant la methode propre pour ce fichier.

## [LECON] 2026-08-08 -- DIVERGENCE VERSION generateurs-commande.sh corrigee (parite py/sh)

**Objet** : corriger la divergence de version pre-existante detectee par Morpheus : le .sh affichait VERSION=0.1.0-beta (ligne 18) alors que le .py affiche VERSION=0.2.0 (ligne 41) - le wrapper n'avait jamais ete mis a jour lors des versions successives du .py.

**Correction** : generateurs-commande.sh ligne 18 : VERSION="0.2.0" (alignement sur le .py). STATUT deja coherent (ebauche dans les 2).

**Validations** :
1. Parite --version py/sh OK (texte identique, seul artefact CRLF sous Windows - normalise avec tr -d '\r').
2. Parite --liste OK (contenu des commandes identique).
3. Generation reelle via .sh OK (commande valider-nommage generee correctement).
4. bash -n OK + ASCII 0 non-ASCII.
5. Scan complet des parametres type=choix dans le catalogue : 0 choix vide, 0 trop court sur 105 commandes (le seul cas generateurs-carte avait deja ete corrige par Morpheus avec choix=[creer, analyser, dupliquer]).

**Lecons** :
1. A CHAQUE version du .py d'un outil, verifier que le .sh wrapper est aligne (VERSION, STATUT) - la parite --version doit etre testee a chaque modification (lecon Morpheus T5).
2. Le scan des parametres choix a liste vide doit devenir un reflexe apres toute regeneration du catalogue (lecon Morpheus T3 : le test de generation reelle est le seul moyen de detecter les choix vides).
3. Sous Windows, un diff py/sh peut afficher une fausse divergence due au CRLF - normaliser avec tr -d '\r' avant de conclure.

## [LECON] 2026-08-09 -- REGLE DES 5 FICHIERS apres modification de version (controle Janus)

**Objet** : documenter la regle issue du controle Janus (detecter-impacts, 2026-08-09) : apres TOUTE modification de version d un outil, verifier les 5 fichiers du dossier outil et distinguer les versions propres des fichiers de donnees.

**Contexte** : le controle Janus sur ma modification de generateurs-commande.sh (VERSION 0.2.0) a detecte 1 IMPACT REEL OUBLIE : spec/spec-generateurs-commande.001.01.ebauche.md ligne 10 affichait encore Version : 0.1.0-beta (au lieu de 0.2.0, aligne sur py/sh/md). J avais aligne py/sh mais oublie la spec.

**La regle des 5 fichiers** : apres TOUTE modification de version d un outil, verifier l alignement VERSION (et STATUT) dans les 5 fichiers du dossier outil :
1. `<outil>.py` -- VERSION dans le code
2. `<outil>.sh` -- VERSION dans le wrapper (lecon Morpheus T5 : le wrapper garde souvent une version obsolete)
3. `<outil>.md` -- Version dans l en-tete de documentation
4. `spec/spec-<outil>...md` -- Version dans l en-tete de la spec (CIBLE DE CETTE LECON : c est le fichier le plus souvent oublie)
5. `<catalogue ou index associe>` -- SI le dossier contient un fichier de donnees (ex: catalogue-commandes.json) ou un index : DISTINGUER les versions

**Distinguer les versions propres (ne pas confondre)** :
- `catalogue-commandes.json` a SA PROPRE version top-level (ligne 2, ex: 0.1.0-beta) qui n est PAS la version de l outil : une modification de version de l outil n impose PAS de changer la version du catalogue (fichier de donnees).
- `index-tools.md` reference la version de l INDEX lui-meme (ligne 9, ex: v0.2.0) : pas la version des outils listes.
- Les fichiers qui citent le NOM de l outil sans sa version (parcours des agents, corrections, controles) ne sont PAS impactes par une modification de version.

**Lecon sur detecter-impacts** : les marquages [NON MIS A JOUR] massifs apres une modification sont souvent des ARTEFACTS TEMPORELS (le fichier modifie est plus recent que les fichiers qui le citent). Croiser la NATURE de la modification (version) avec le CONTENU des references (nom vs version) avant de conclure : tous les NON MIS A JOUR ne sont pas des impacts reels.

**Action restante (mission separee)** : corriger spec/spec-generateurs-commande.001.01.ebauche.md ligne 10 : Version 0.1.0-beta -> 0.2.0.

## [LECON] 2026-08-09 -- IMPACT SPEC CORRIGE : spec-generateurs-commande Version 0.1.0-beta -> 0.2.0 (regle des 5 fichiers appliquee)

**Objet** : corriger l impact reel oublie detecte par le controle Janus : la spec de generateurs-commande affichait Version 0.1.0-beta alors que py/sh/md etaient en 0.2.0. C etait l action restante de la lecon des 5 fichiers.

**Correction** : spec/spec-generateurs-commande.001.01.ebauche.md ligne 10 : Version : 0.1.0-beta -> Version : 0.2.0 (edition chirurgicale, CRLF preserve).

**Validations** :
1. Une seule occurrence de 0.1.0-beta dans la spec (ligne 10) - aucune autre a corriger.
2. 0.1.0-beta absent apres correction, 0.2.0 present (1 occurrence).
3. valider-conformite-ascii : 0 non-ASCII.
4. CRLF preserve (89/89).
5. detecter-impacts sur la spec : 2 fichiers NON MIS A JOUR (janus/corrections.md, vulcain/corrections.md) = ARTEFACTS (rapports/lecons qui documentent l incident, pas des references de version a aligner).
6. Dossier outil desormais ALIGNE : py=0.2.0, sh=0.2.0, md=0.2.0, spec=0.2.0 (les 4 fichiers de version).

**Lecons** :
1. La regle des 5 fichiers (documentee le 2026-08-09) est appliquee : apres toute modification de version, py/sh/md/spec doivent etre alignes. La spec est bien le fichier le plus souvent oublie - exactement ce que la lecon predic.
2. detecter-impacts apres modification de la spec signale les rapports/lecons qui documentent l incident : ce sont des artefacts (contexte documentaire), pas des impacts reels - croiser avec la nature de la modification (version) et le contenu des references.
3. La boucle est complete : controle Janus (impact detecte) -> lecon des 5 fichiers (documentee) -> indice de carte c12 (v0.2.4) -> correction de l impact (spec 0.2.0). Cercle vertueux lecon -> carte -> application -> verification.

## [LECON] 2026-08-09 -- OUTIL detecter-divergences-version cree (scan durable des spec divergentes)

**Objet** : creer un outil DURABLE pour remplacer les scripts temporaires de Janus (.tmp-scan-versions*.py) qui scannaient les spec/ divergentes de leur .py (regle des 5 fichiers).

**Livrable** : detecter/detecter-divergences-version/ (.py + .sh wrapper + .md + spec/ + bloc identite). Scan recursif des spec/ sous une racine, extraction de la version spec (5 formats : en-tete prioritaire, tableau frontmatter, versionning, titre, tableau historique - lecon Janus), croisement avec la version VERSION= du .py associe, verdicts ALIGNE / DIVERGENT (base) / DIVERGENT (suffixe) / SANS VERSION / SANS PY. Options : --racine (defaut cerveau-projet), --liste, --export, --version.

**Validations** :
1. Scan reel : retrouve les 6 divergences de Janus (regenerer-catalogue 0.1.0 vs 1.0.0, lister-agents, lister-outils, verifier-systeme, combos-moteur suffixe, guider-parcours) + 1 decouverte (activer-agent-principal : spec historique 0.3.4 vs py 0.5.0 avec ligne d historique MALFORMEE - 2 colonnes sans date).
2. py_compile + bash -n OK ; valider-nommage OK ; ASCII 0 sur les 4 fichiers ; parite --version py/sh OK (via python - normaliser le CRLF, le diff shell affiche un faux positif).
3. detecter-impacts : identite reconnue, 3 fichiers du dossier [A JOUR].
4. index-tools : Detecter 5->6, Total 105->106, ligne ajoutee.
5. Catalogue generateurs-commande : entree ajoutee par regenerateur (106 commandes), puis CORRIGEE (le regenerateur a cree un parametre 'chemin' positionnel au lieu de 'racine' avec defaut ; corrige en modele '--racine {racine}' + defaut cerveau-projet) - generation reelle OK.

**Lecons** :
1. Le regenerateur de catalogue cree des parametres par defaut (positionnels 'chemin') qui ne correspondent pas toujours a l'API reelle de l'outil (flags comme --racine) : VERIFIER la generation reelle via generateurs-commande apres synchronisation et corriger l'entree en entree SPECIALE si besoin.
2. L'extraction de version des spec a 5 formats + la priorite en-tete (lecon Janus) est maintenant DUPLIQUEE dans un outil durable : ne plus scanner a la main.
3. Les spec avec lignes d'historique MALFORMEES (2 colonnes sans date) peuvent induire l'extraction en erreur : les signaler (cas activer-agent-principal) pour nettoyage, sans conclure seul.
4. La boucle lecon -> outil -> verification est complete : le scan manuel de Janus devient un outil reutilisable pour le prochain controle.

---

## [LECON] 2026-08-09 -- CORRECTION 6 DIVERGENCES spec/py (regle des 5 fichiers)

**Mission** : aligner les 5 spec divergentes sur leur .py + documenter le cas particulier guider-parcours.
**Contexte** : suite du scan detecter-divergences-version (outil cree ce jour) qui avait revele 6 spec divergentes sur 11.

**Actions realisees** :
1. **generateurs-regenerer-catalogue** : spec 0.1.0 -> 1.0.0 (3 emplacements : en-tete `# Version :`, frontmatter `version:`, titre historique) -- alignee sur py 1.0.0
2. **lister-agents** : spec 0.2.0 -> 0.4.0-py (tableau historique + reference texte) -- alignee sur py 0.4.0-py
3. **lister-outils** : spec 0.2.0 -> 0.3.0-py (tableau historique) -- alignee sur py 0.3.0-py
4. **verifier-systeme** : spec 0.2.0 -> 0.2.1-py (tableau historique) -- alignee sur py 0.2.1-py
5. **combos-moteur** : spec 0.2.0-ebauche -> 0.2.0-beta (en-tete) -- alignee sur py 0.2.0-beta (suffixe coherent)
6. **guider-parcours** : CAS LEGITIME ASSUME -- la spec versionne les PATTERNS v0.2.x (0.2.20), distincts de l'outil 0.3.1. Decision : documenter dans le .md de detecter-divergences-version comme cas legitime, NE PAS aligner la spec.

**Lecons** :
1. Une spec peut porter sa version a PLUSIEURS endroits (en-tete, frontmatter, titre, tableau historique, reference texte) : TOUT aligner, pas seulement le premier trouve
2. La version d'EN-TETE prime, mais les spec " prepare " (sans champ Version d'en-tete) portent leur version dans le TABLEAU HISTORIQUE -- verifier le format avant de chercher
3. Distinguer divergence de BASE (regenerer-catalogue 0.1.0 vs 1.0.0 = ecart majeur) vs de SUFFIXE (combos-moteur ebauche vs beta = coherence de suffixe)
4. Cas legitimes assumes (guider-parcours, prototype vulcain) : ne PAS aligner aveuglement -- documenter la decision dans l'outil qui scanne pour eviter les faux positifs repetitifs
5. Verifier l'ASCII sur CHAQUE fichier modifie apres edition chirurgicale (0 non-ASCII sur les 6)

**Validation finale** : rescan detecter-divergences-version = 5 spec ALIGNEES, 2 divergences restantes = guider-parcours (cas legitime documente) + activer-agent-principal (hors perimetre, ligne d'historique malformee a nettoyer separement).

---

## [LECON] 2026-08-09 -- LIGNES HISTORIQUE SANS DATE = IGNOREES par detecter-divergences-version

**Mission** : corriger les 2 lignes d'historique malformees de la spec activer-agent-principal (faux divergent).

**Contexte** : l'outil detecter-divergences-version lit la version d'une spec prepare dans le tableau historique via la regex `| AAAA-MM-JJ | version |` (derniere ligne avec date). Les lignes SANS DATE sont IGNOREES -> l'outil retombe sur la derniere ligne DATER (0.3.4) au lieu de la version courante reelle (0.5.0) -> faux DIVERGENT.

**Actions realisees** :
1. Ligne 290 : `| 0.3.2 | Vulcain | ...` -> `| 2026-08-07 | 0.3.2 | Vulcain | ...` (date verifiee par git blame, commit 55994e04)
2. Ligne 291 : `| 0.5.0 | Vulcain | ...` -> `| 2026-08-08 | 0.5.0 | Vulcain | ...` (date verifiee par git blame, commit 993738a6)

**Lecons** :
1. Les lignes du tableau historique d'une spec DOIVENT TOUJOURS porter leur date reelle (AAAA-MM-JJ) : sans date, detecter-divergences-version les ignore et lit une version anterieure -> faux divergent
2. Ne JAMAIS inventer une date : utiliser `git blame -L <lignes> --date=short <fichier>` pour retrouver la date de modification reelle
3. Apres correction, RESCAN avec l'outil pour confirmer le passage ALIGNE (boucle de validation)

**Validation finale** : rescan = activer-agent-principal ALIGNE (0.5.0 = 0.5.0) ; synthese 12 spec | 9 ALIGNEES | 1 DIVERGENT (guider-parcours = cas legitime assume documente) | 2 SANS VERSION/SPEC ; ASCII 0 ; CRLF preserve 291/291.
## [LECON] 2026-08-09 -- valider-nommage v0.3.2 (formats speciaux combos/tests)

**Mission** : faire evoluer valider-nommage pour reconnaitre les 2 formats speciaux et eliminer les bruits preexistants (definition-combo.json + test-XXX-*.py).
**Lecons** :
1. Les formats speciaux LEGITIMES doivent etre reconnus par l outil, pas documentes comme bruit : definition-combo.json (dossier combos/combo-*/) et test-XXX-nom-outil.(py|sh|md) (dossier tests/test-XXX-*/) passent maintenant avec 0 ERREUR - la detection repose sur le DOSSIER PARENT (prefixe combo- / test-) en plus du nom du fichier
2. La regle est : un format special est accepte quand le nom du fichier ET le dossier parent sont coherents (definition-combo.json DANS combos/combo-*, test-XXX-* DANS tests/test-XXX-*) - eviter d accepter trop large (ex: n importe quel .json dans combos/)
3. PARITE py/sh : la meme logique doit etre portee dans les 2 fichiers (regex bash vs PATTERN_OUTIL python) et verifiee par --version (v0.3.2-py / v0.3.2) + tests croises (meme fichier -> meme resultat)
4. REGLE DES 5 FICHIERS : apres toute modification de version d un outil py+sh, verifier py, sh, md (versionning + doc) + spec + catalogue/index le cas echeant - ici md mis a jour avec la ligne 0.3.2
5. NON-REGRESSION : verifier 3 cas apres modification : les formats speciaux passent (0 ERREUR), les outils normaux passent toujours, les VRAIS mauvais nommages restent detectes (cree un fichier reel mal nomme dans le workspace - un fichier inexistant donne 0 ERREUR et fausse la verification)
6. Le test formel v0.3.0 (tester-valider-nommage-v030.sh, 13/13) passe toujours - le mode --mots-seuls non regresse

**Validation finale** : v0.3.2-py/v0.3.2, 15 combos 0 ERREUR, 4 tests 0 ERREUR, mauvais nommage detecte, test v0.3.0 13/13, ASCII 0 sur 3 fichiers.
## [LECON] 2026-08-09 -- CORRECTION CATALOGUE valider-relecture (suite test reel Atlas)

**Contexte** : le test reel d Atlas a revele que l entree catalogue valider-relecture composait --fichier {fichier} alors que l outil v0.2.0-py utilise --agent <nom> (+ --verbose optionnel) -> ERREUR Option inconnue : --fichier. C etait le SEUL vrai decalage du catalogue (scan 106 entrees : valider-nommage et verifier-systeme = faux positifs --help vs --aide).

**Correction appliquee** :
1. catalogue-commandes.json v0.2.0 -> v0.2.1 : modele "--agent {agent} {verbose}", parametres agent (texte, obligatoire) + verbose (type flag, flag --verbose, optionnel) - format identique a analyser-dependances/inverse
2. generateurs-commande.md : mention "Catalogue v0.2.0 : 106 commandes" -> "Catalogue v0.2.1 : 106 commandes" (regle des 5 fichiers : catalogue + doc .md alignes; la spec ne mentionne pas la version du catalogue - rien a faire)
3. test-005 point 14 : verifiait catalogue version == 0.2.0 en dur -> obsolete apres bump -> aligne 0.2.1 (2 lignes : description + verifier) -> 26/26 VALIDE

**Validations** : JSON valide 106 commandes, composition py/sh identique (--agent atlas), verbose=oui -> --verbose present, execution reelle code 0 [OK], navigation atlas c8 affiche catalogue + PASSE PAR LE GENERATEUR SANS commande en dur, ASCII 0 sur catalogue/doc/test, regenerateur dry-run 83 preserves 0 ajoute (correction survivra).

**Lecons** :
1. UN TEST REEL VAUT PLUS QU UN TEST FORMELL : c est l execution reelle (Atlas) qui a revele le decalage modele/interface que les 26 points du test-005 ne voyaient pas - toujours comparer le modele du catalogue a l interface reelle (--aide) quand on cree/modifie une entree
2. UN TEST QUI VERIFIE UNE VERSION EXACTE devient obsolete des que la version change legitimement - l aligner (ou le signaler a Morpheus) plutot que de figer la version pour satisfaire le test
3. detecter-impacts signale des fichiers reference qui mentionnent le CHEMIN du catalogue (dependance stable, ex: protocole-creation-combos) : faux positifs si la version du catalogue n y figure pas - verifier le CONTENU avant de conclure a une non-mise a jour
4. La regle des 5 fichiers s applique au couple catalogue + doc .md (version du catalogue documentee); la spec ne la porte pas toujours - verifier les 2 endroits (doc + spec) quand on bumpe le catalogue
## [LECON] 2026-08-09 -- INSTITUTIONNALISATION detecter-decalages-catalogue (infraction Atlas corrigee)

**Contexte** : Atlas (explorateur) avait ecrit scan-catalogue.py dans son dossier explorations/ pendant son audit - DOUBLE INFRACTION : (a) les outils vivent dans agents/tools/<categorie>/<outil>/ et non dans le dossier d un agent, (b) un explorateur n est pas habilite a creer des outils (role Vulcain). Mission : institutionnaliser l outil (deplacer + structure officielle) et garder le rapport comme trace dans explorations/.

**Actions** : deplacement vers tools/detecter/detecter-decalages-catalogue/ (renommage detecter-decalages-catalogue, prefixe de categorie, meme famille que detecter-divergences-version) ; structure officielle py (identite) + sh (wrapper pur) + md (LIRE AVANT USAGE) + spec + entree catalogue (v0.2.1 -> v0.2.2, 106 -> 107) + index-tools.md + doc generateurs-commande.md (Catalogue v0.2.2 : 107 commandes) + test-005 point 14 aligne (0.2.1 -> 0.2.2) ; RACINE corrigee (5 niveaux a explorations/, 6 niveaux a tools/detecter/<outil>/).

**Validations** : py_compile + bash -n OK, --version v0.1.0, nommage 0 ERREUR, ASCII 7/7, composition generateur --sortie present / retire si vide, execution reelle rapport + synthese (106 conformes / 0 decalage / 1 non testable = test formel / 0 alerte), test-005 26/26, regenerateur dry-run 88 scannes 84 preserves 0 ajoute, detecter-impacts VERDICT tous a jour.

**Lecons** :
1. UNE CARTE = UN ROLE (Pattern 10) : un explorateur qui decouvre un besoin d OUTIL signale a Cerberus (qui active Vulcain), il ne cree pas l outil - meme si le script semble simple et utile
2. TRACE vs OUTIL : un rapport de mission vit dans le dossier de l agent (explorations/, controles/) ; un script reutilisable vit dans tools/ avec la structure officielle - ne jamais melanger
3. RACINE : le nombre de niveaux .. dans un script = profondeur du dossier depuis la racine (explorations/ = 5, tools/detecter/<outil>/ = 6) - a recalculer a chaque deplacement
4. MODELE DU CATALOGUE = INTERFACE REELLE : `{sortie}` compose en positionnel, `--sortie {sortie}` compose le flag - TOUJOURS tester la commande generee contre l interface de l outil (le scan l a revele)
5. AJOUTER UN OUTIL AU CATALOGUE = bump de version + alignement doc (compteur 106 -> 107) + test-005 (point 14 version en dur) - la regle des 5 fichiers s etend au trio catalogue/doc/test
6. Le regenerateur preserve les entrees manuelles (dry-run 84 preserves) : ajouter l entree dans le catalogue est sur et rejouable
## [LECON] 2026-08-09 -- OUTIL cartographier-parcours cree (v0.1.0, categorie cartographier/)

**Mission** : creer l outil cartographier-parcours (decision utilisateur - Atlas cartographie le parcours d un agent dans un fichier pour ses analyses rapides). Decisions : sortie = dossier du parcours audite (cartographie-<agent>.md), format = arbre ASCII, branchement carte Atlas = mission Buffy ulterieure.
**Livrables** : cartographier-parcours.py (lecture seule, 100% stdlib, ASCII strict) + .sh (wrapper pur exec python3) + .md + spec/ + entree catalogue-commandes.json (107 -> 108) + index-tools.md (nouvelle categorie Cartographier, total 106 -> 107).
**Rendu** : en-tete (agent, version, depart, nb cases, nb chemins) + arbre ASCII (1ere occurrence, branches marquees, [convergence] pour les re-visites, `|--` / `--`) + impasses + boucles + chemins BFS (logique reutilisee de generateurs-carte analyser).
**Lecons** :
1. REUTILISATION : la detection des chemins (BFS anti-boucle, impasses) existe deja dans generateurs-carte analyser - je l ai portee au lieu de la reimplementer. La cartographie est un RENDU en fichier de ce que generateurs-carte affiche en console.
2. ARBRE ASCII : le premier jet affichait les cases 2 fois (branche de c0 + noeud enfant) - correction : fonction descendre(cid, prefixe, lien, contexte) avec affichees set (1ere occurrence) et marquage [convergence], liens |-- / `-- selon derniere branche.
3. PIEGE INSERTION CATALOGUE (grave, a ne jamais refaire) : inserer une entree JSON dans le catalogue par concatenation de lignes a MAL indente (6/8 espaces au lieu de 4/6) - le JSON est reste valide PAR CHANCE apres 5 reparations (retrait de blocs residuels + reinsertion au bon niveau + repositionnement alphabetique). REGLE : pour ajouter une entree au catalogue, copier le bloc d une entree EXISTANTE avec l outil lire-fichier/editer-fichier (indentation exacte 4/6/10), ou utiliser generateurs-regenerer-catalogue qui regenere tout - JAMAIS d insertion manuelle a la volee.
4. PIEGE ASCII DOC : les guillemets francais ' ' et les accents (complete) passes dans le .md et la spec - detectes par valider-conformite-ascii (4 + 5 caracteres) et corriges. VERIFIER valider-conformite-ascii sur TOUS les fichiers crees AVANT de declarer l outil pret (md + spec inclus, pas seulement py/sh).
5. PARITE .sh : wrapper pur (exec python3 "$PY_SCRIPT" "$@") - la parite des sorties est garantie PAR CONSTRUCTION (pattern detecter-impacts, valider-cartes-decision). Version py/sh identiques (v0.1.0).
6. REGLE DES 5 FICHIERS : py, sh, md, spec, tests/ - les tests formels sont DELEGUES a Morpheus (REGLE ABSOLUE), pas ecrits par moi.
7. L OUTIL EST EN LECTURE SEULE : il ne modifie jamais le parcours source - le fichier genere est un derive (comme detecter-impacts genere un rapport).
## [LECON] 2026-08-09 -- PLAN FIGER LF : outil corriger-fins-de-ligne cree + outils d ecriture corriges

**Contexte** : diagnostic Cerberus (decision utilisateur) : la regle immuable exige LF mais nos outils d ecriture produisaient du CRLF (creer-fichier.py ecrivait via Path.write_text -> traduction CRLF Windows) et detecter-usage-outils-externes les sanctionnait comme traces d outils externes -> boucle de conflits permanente. Git autocrlf=true aggravait (warnings checkout).

**Livrables** :
1. OUTIL corriger-fins-de-ligne v0.1.0 (categorie corriger/) : py + sh (wrapper pur) + md + spec + entree catalogue (108 -> 109, v0.2.2 -> v0.2.3) + index-tools (categorie Corriger 5 -> 6, total 107 -> 108). Fonctions : fichier/dossier --recursive, --dry-run, --verbose, detection binaire (octet nul) ignore, idempotent (2e passe = 0 converti), erreur chemin introuvable.
2. 11 OUTILS D ECRITURE CORRIGES pour produire du LF (newline='' sur open texte, ou open explicite a la place de write_text) : creer-fichier (write_text -> open newline=''), ecrire-fichier (backup + ecriture + append), ajouter-contenu-fichier, inserer-contenu-fichier, gerer-sous-mission (json.dump), generateurs-squelette-pense-bete/spec/todo, creer-remplir-pense-bete/spec/todo (write_text -> open).

**Validations** : py_compile 12/12 + bash -n, --version py/sh identiques v0.1.0, dry-run sans modification, conversion reelle CRLF->LF verifiee octets, idempotence, binaire intact, erreur chemin, TEST REEL : creer-fichier ecrit desormais du LF (CRLF:0 LF:1), ASCII 0 sur 12 fichiers modifies, catalogue JSON valide 109 trie, generateur compose la commande.

**Lecons** :
1. LA CAUSE RACINE DU CRLF ETAIT NOS OUTILS, pas Git : Path.write_text() et open() en mode texte traduisent \n en \r\n sur Windows. Git autocrlf=true n etait qu un amplificateur. Corriger les outils = tarir la source ; .gitattributes = figer le depot (mission 2 Buffy).
2. LE SCAN DES ECRITURES : open(..., 'w'/'a'...) SANS newline= et write_text() = sources de CRLF. Le mode binaire ('wb') est safe. Pattern correct : open(f, 'w', encoding='utf-8', newline='') (comme remplacer-texte.py).
3. NE PAS TOUCHER AUX TESTS DE MORPHEUS : les tests (test-002, test-006) ecrivent volontairement des fichiers invalides - hors perimetre, laisse tels quels.
4. INSERTION CATALOGUE : manipulation JSON programmatique (json.load -> insertion dans la liste a la position triee -> json.dumps(ensure_ascii=True, indent=2)) = fiable a 100% ; l insertion par concatenation de lignes (lecon cartographier-parcours) reste INTERDITE.
5. LES FICHIERS .pyc COMMITES : py_compile regenere les .pyc -> les restaurer avec git restore (fichiers commites) pour ne pas polluer le working tree.
6. PIEGE HEREDOC : les scripts heredoc avec backslashes echouent en JSON - ecrire les scripts dans des fichiers .tmp puis les executer.
## [LECON] 2026-08-09 -- TESTS OBSOLETES CORRIGES (versions en dur alignees sur la realite)

**Contexte** : la non-regression post-migration FIGER LF (Morpheus) a revele que 2 tests codent des versions en dur devenues obsoletes apres des bumps legitimes : test-004 (parcours morpheus v0.1.2) et test-005 (catalogue 0.2.2, atlas v0.1.2).

**Livrables** :
1. test-004-combos-tester-outil.py : v0.1.2 -> v0.1.3 (3 occurrences : docstring, commentaire, verifier 7a) + .md (1 occurrence).
2. test-005-generateurs-commande.py : catalogue 0.2.2 -> 0.2.3 (docstring + verifier 14), atlas v0.1.2 -> v0.1.5 (docstring, titre, commentaire de section x2, verifier 17, except 17) + note historique v0.1.2 -> v0.1.5 ajoutee + .md (titre, description, tableau d evolution complete, section 17).

**Resultats** : test-004 16/16 VALIDE (avant 15/16), test-005 25 OK / 1 KO (avant 23/26) - seul KO restant = point 18 (1 commande en dur restante case c30 atlas = PISTE C, mission separee, NON modifie).

**Validations** : ASCII 0 sur les 4 fichiers, LF pur (CRLF 0), py_compile OK, aucun fichier cree hors test.

**Lecons** :
1. Les tests qui verifient une version doivent etre mis a jour A CHAQUE bump de version du fichier cible - c est la regle des 5 fichiers appliquee aux tests.
2. NE PAS toucher les versions du generateur (v0.2.1) : seules les 3 versions cibles (morpheus 0.1.3, catalogue 0.2.3, atlas 0.1.5) etaient obsoletes - verifier la SOURCE DE VERITE avant de remplacer.
3. Les notes historiques (v0.1.1 -> v0.1.2) sont PRESERVEES et completees (ajout d une ligne v0.1.2 -> v0.1.5) - ne jamais effacer l historique.
4. Le point 18 (piste C) reste KO volontairement : la mission ne couvre pas la conversion de la derniere commande en dur (case c30 atlas).
## [LECON] 2026-08-09 -- FAUX POSITIF EVALUER-COHERENCE CORRIGE (scan limite aux 11 agents)

**Contexte** : la non-regression post-migration (Morpheus) a revele que evaluer-coherence signalait 4 outils introuvables (statut-mission, contexte, resultats, erreurs) - en realite des VARIABLES du classeur-variables, pas des outils.

**Cause racine** : la section 4 (Outils references par les agents) des 2 versions py et sh iterait sur TOUS les dossiers de agents/ ayant un fichier nom.md. Le dossier classeur-variables/ possede classeur-variables.md et etait donc scanne comme une fiche d agent, ses variables entre backticks etant interpretees comme des outils inexistants.

**Correction structurelle** : scan limite aux 11 agents officiels (AGENTS_ATTENDUS) au lieu de os.listdir (py) / find -type d (sh). classeur-variables/ et tout futur dossier non-agent sont ignores PAR CONCEPTION (pas une liste d exclusion a maintenir, mais un scan borne).

**Versions** : bump 0.2.1 vers 0.2.2 dans py (VERSION + docstring), sh (VERSION + en-tete), md (Version + tableau Versionning). Pas de spec existante.

**Verifications** : py et sh affichent tous deux OK Tous les outils references existent (0 faux positif), parite py/sh confirmee, test-001-evaluer-agents-coherence 8/8 REUSSI (le point 6 attendait deja cette correction), ASCII 0, LF pur, py_compile + bash -n OK, 0 residu.

**Lecons** :
1. Un scan qui itere sur os.listdir / find -type d d un dossier racine balaye TOUS les sous-dossiers, pas seulement les cibles prevues - borner le scan a une liste explicite (AGENTS_ATTENDUS) est plus robuste qu ajouter des exclusions une par une.
2. Le classeur-variables est un dossier de DONNEES dans agents/, pas une fiche d agent : il ne doit jamais etre scanne comme tel.
3. Le .sh de evaluer-coherence est lent par conception (2 find par backtick par fiche : ~100s) - c est un comportement connu, la version py est la reference pour l usage courant.
4. Parite py/sh : appliquer la MEME correction aux 2 versions, puis prouver la parite en executant les 2 (sorties identiques sur la section corrigee).
## [LECON] 2026-08-09 -- ECART P14 : identification vulcain.md mise a jour (parcours v0.2.8)

**Mission** : corriger l'ecart P14 du re-audit Themis -- vulcain.md (mtime 11:02) plus ancien que parcours-vulcain.json (mtime 13:05, v0.2.8).

**Actions** :
1. Section PARCOURS de vulcain.md : mention parcours v0.2.8 ajoutee au lien Parcours.
2. Spec du format alignee v0.2.5 -> v0.2.25 (version reelle de la spec-guider-parcours).
3. Entree d'historique 2026-08-09 ajoutee (corrections Buffy P2 + P12, bump v0.2.7 -> v0.2.8).

**Resultats** : vulcain.md passe de NON MIS A JOUR a A JOUR dans detecter-impacts (mtime 13:09 > 13:05). ASCII 0, LF pur.

**Lecons** :
1. Une fiche d'agent reference son parcours comme SOURCE DE VERITE : a chaque bump de version du parcours par un autre agent (Buffy, etc.), la fiche doit etre mise a jour en meme temps -- sinon detecter-impacts la signale NON MIS A JOUR (Pattern 14).
2. La spec du format est referencee dans la fiche (spec-guider-parcours) : sa version doit rester alignee (v0.2.25 ici) pour eviter des references obsoletes.
3. Les notes de mission (mission-*.md, priorite-outils.md, resume-creation-outils.md) sont des documents figes (type: note, sans champ version) : detecter-impacts les signale mais c'est une JUSTIFICATION legitime -- il ne faut pas les toucher pour le seul plaisir d'un mtime recent.
4. detecter-impacts compare les mtime : apres toute edition, verifier que le fichier cible est bien plus recent que la modification source avant de conclure.
## [LECON] 2026-08-09 -- PATTERN 15 MODE MONO-LLM documente dans la spec-guider-parcours (v0.2.26)

**Mission** : documenter le Pattern 15 (MODE MONO-LLM) dans la spec-guider-parcours apres le diagnostic Cerberus (2 missions arretees apres l'activation de Themis).

**Diagnostic (Cerberus)** : la carte de Cerberus case c10 ordonne de continuer (suivant c7) ; activer-agent-principal.py ne fait AUCUN sous-processus (0 subprocess/os.system/Popen/exec) -- il ecrit 3 fichiers de trace ; en mode multi-LLM l'arret apres activation est correct (un autre LLM reprend) ; en mode mono-LLM l'arret bloque la mission.

**Modifications spec-guider-parcours (v0.2.25 -> v0.2.26)** :
1. Titre aligne v0.2.19 -> v0.2.26 (decalage preexistant corrige).
2. Pattern 15 insere apres le Pattern 14 (regles : l'activation ne clot PAS le tour, l'agent active est joue immediatement dans le meme tour, l'arret n'est valable qu'en mode multi-LLM).
3. Procedure 4c renommee RE-AUDIT COMPLET DES 15 PATTERNS + procedure 4m (mode mono-llm) ajoutee.
4. Critere 26 (MODE MONO-LLM) ajoute a la section criteres d'acceptation (1 a 26).
5. Historique + Agent (ligne 12/13) : entree v0.2.26 ajoutee.
6. Section Patterns valides en production : 14 -> 15 patterns.

**Impacts alignes (Pattern 14)** : vulcain.md (spec v0.2.25 -> v0.2.26), guider-parcours.md (spec v0.2.5 -> v0.2.26 -- reference obsolete de longue date corrigee au passage). Les fiches agents referencent la spec sans version precise : pas d'impact de version.

**Validations** : ASCII 0 + LF pur sur les 3 fichiers modifies (spec, vulcain.md, guider-parcours.md), coherence verifiee (6 occurrences Pattern 15, 11 occurrences v0.2.26, 5 occurrences 15 patterns), 0 residu .tmp.

**Lecons** :
1. Un diagnostic d'arret de mission doit distinguer : la carte (structure), l'outil (mecanisme) et le comportement LLM (execution) -- ici les 3 niveaux ont ete examines, la cause etait le comportement mono-LLM.
2. Le titre d'une spec peut prendre du retard par rapport a son historique : verifier le titre (ligne # Spec) a chaque bump, pas seulement l'historique.
3. Une spec modifiee IMPACTE les fichiers qui la referencent avec une version : verifier avec detecter-impacts ET grep des versions dans les fiches/docs.
## [LECON] 2026-08-09 -- CORRECTION Pattern 15 v0.2.27 : JAMAIS D'ARRET, meme en multi-LLM

**Mission** : corriger le Pattern 15 (v0.2.26) qui autorisait l'arret apres activation en mode multi-LLM. Correction utilisateur : les LLM travaillent EN PARALLELE chacun dans sa session -- l'activation documente le role de SA session uniquement, elle ne delegue JAMAIS l'execution a un autre LLM (aucun relais n'existe).

**Modifications spec-guider-parcours (v0.2.26 -> v0.2.27)** :
1. Titre du Pattern 15 : 'MODE MONO-LLM' -> 'JAMAIS D ARRET APRES L ACTIVATION'.
2. Intro : suppression de la fausse idee de relais (un AUTRE LLM prend le relais) -> les LLM travaillent en parallele, l'activation documente le role de SA session uniquement.
3. Regle 3 : 'l'arret n'est VALABLE qu'en mode multi-LLM' -> 'l'arret est TOUJOURS fautif dans AUCUN mode'.
4. Regle 5 : suppression du cas particulier qui autorisait l'arret en multi-LLM.
5. Conclusion : pas d'arret dans AUCUN mode (mono comme multi).
6. Critere 26 : renomme 'JAMAIS D ARRET APRES L ACTIVATION (v0.2.27)' avec la meme correction.
7. Versions : titre + historique + Agent + patterns valides + procedure 4c/4m -> v0.2.27.
8. Impacts alignes : vulcain.md et guider-parcours.md (spec v0.2.26 -> v0.2.27).

**Validations** : 0 formulation fautive restante (la seule occurrence restante est la trace HISTORIQUE de v0.2.26 dans la ligne 13, suivie de la correction v0.2.27 -- comportement correct de l'historique), 11x v0.2.27, ASCII 0 + LF pur sur les 3 fichiers, 0 residu.

**Lecons** :
1. Une regle documentee peut etre corrigee par l'utilisateur quelques minutes apres sa creation : l'historique doit TRACER la version fautive PUIS la correction (ne pas effacer la trace), mais le CORPS du pattern doit etre corrige partout (intro, regles, conclusion, critere).
2. Le mode multi-LLM n'implique AUCUN relais : chaque LLM travaille en parallele dans sa session. La delegation entre agents est un changement de ROLE dans la meme session, jamais un transfert vers un autre LLM.
3. Quand l'utilisateur corrige une formulation, verifier TOUTES les occurrences (intro, regles, conclusion, critere, historique) -- un grep cible ('valable qu.en mode multi-LLM') confirme qu'il ne reste que la trace historique legitime.
## [LECON] 2026-08-09 -- OUTIL generateurs-outil-temporaire cree (generateur d'outil temporaire standardise)

**Mission** : creer le generateur d'outil temporaire (design utilisateur valide : tous les agents habilites, promotion systematique a la 2e utilisation, forme Python seul). Outil cree : py + sh + md + spec + index-tools + entree catalogue (110 commandes).

**Comportement de l'outil** : genere un script `tmp-<besoin>.py` DANS le workspace uniquement (jamais hors workspace, jamais dans tools/), en-tete standard (identite type: outil-temporaire, ASCII strict, LF, 100% stdlib, version 0.1.0-tmp), dry-run par defaut (--force pour ecrire), refuse l'ecrasement, et affiche la QUESTION DE PROMOTION a la fin : besoin recurrent (2e utilisation) ? -> OUI = ACTIVER VULCAIN directement (maillon de chaine), Vulcain cree l'outil durable (protocole 5 fichiers) puis REACTIVE L'AGENT PRECEDENT.

**Lecons** :
1. PIEGE DOUBLE PREFIXE : le nom du besoin est deja prefixe tmp- (ex: tmp-mesurer-taille) ; le template du script genere NE doit PAS re-ajouter tmp- dans le docstring/print (le double tmp-tmp-mesurer-taille est apparu au test). Passer le nom avec prefixe au template et l'utiliser tel quel.
2. PIEGE INSERTION JSON DANS UN CATALOGUE : pour inserer une entree apres un bloc, ne JAMAIS chercher la premiere ligne '},' (c'est la fermeture du PREMIER sous-objet, ex: le premier parametre) -- il faut partir de la ligne '{' d'ouverture du bloc et compter les accolades (avec gestion des chaines) jusqu'au '}' qui ramene a 0. Ma 1re tentative a insere l'entree AU MILIEU de la liste parametres de generateurs-commande (JSON restait valide mais entree parasite).
3. PIEGE REFORMATAGE JSON : ne jamais re-ecrire un catalogue avec json.dumps global (le format du fichier n'est pas un json.dumps standard : diff 47% a indent=2) -- reparer CHIRURGICALEMENT par lignes (supprimer le bloc parasite, inserer l'entree bien formatee a la bonne indentation) puis verifier git diff minimal (ici -29/+29 = parasite supprime + bonne entree).
4. Detection du workspace : remonter depuis le script jusqu'au dossier contenant AGENTS.md (marqueur robuste, fonctionne pour toutes les racines).
5. Verification systematique : nommage valider-nommage OK, ASCII 0 sur les 5 fichiers + index, LF pur, parite py/sh (--version, dry-run, generation reelle), test bout en bout (generation + execution du script genere + suppression 0 residu), detecter-impacts A JOUR.
## [LECON] 2026-08-09 -- GUILLEMETS FRANCAIS AJOUTES AU DICTIONNAIRE (v0.2.1)

**Mission** : ameliorer les outils corriger pour couvrir les guillemets francais U+00AB/U+00BB (lecon Themis du 2026-08-09 : l outil repondait [OK] Aucune correction necessaire alors que le fichier contenait des guillemets francais).

**Modifications** (7 fichiers) :
1. Dictionnaire partage `corriger-dictionnaire-accents.txt` : +2 entrees U+00AB et U+00BB vers guillemet droit double (coherent avec les guillemets courbes U+201C/U+201D qui vont deja vers le guillemet droit).
2. Les 2 outils consommateurs (corriger-accents-zones-sensibles + corriger-dictionnaire-accents) beneficient automatiquement du dictionnaire : aucun changement de code necessaire, seulement le bump de version 0.2.0-py -> 0.2.1-py (py + sh + md des 2 outils) + ligne d historique + mention des caracteres couverts dans la doc.

**Lecons** :
1. LA MODIFICATION D UN DICTIONNAIRE PARTAGE PROFITE A TOUS LES CONSOMMATEURS : corriger-accents-zones-sensibles (py+sh), corriger-dictionnaire-accents (py+sh) lisent le meme fichier .txt - une seule source de verite, aucun changement de code dans les scripts.
2. PIEGE TESTS PARALLELES : lancer 2 outils de correction EN PARALLELE sur le MEME fichier fausse les resultats (le 1er voit 0 fichier car le 2e a deja tout corrige) - toujours tester sequentiellement avec des fichiers neufs par outil.
3. PIEGE DOSSIERS EXCLUS : les noms de dossier contenant .tmp ou test- sont exclus par defaut (--exclure node_modules,.git,.agents,.backup,.tmp,test-,dictionnaire-,exemples) - un test dans .tmp-test-xxx donne Fichiers analyses: 0. Utiliser un dossier neutre (ex: .zz-xxx).
4. VERSION PY VS SH : les .py supportent --version, les .sh NON (erreur preexistante) - la parite --version py/sh n est pas applicable a ces outils, verifier plutot la parite de comportement (meme nombre de corrections, meme resultat).
5. REGLE DES 5 FICHIERS : apres modification de version, verifier py, sh, md des 2 outils + ligne d historique + doc mention des caracteres couverts - ici 6 fichiers outils + 1 dictionnaire = 7, tous ASCII 0 (sauf le dictionnaire, exception volontaire), LF pur, nommage OK.
6. detecter-impacts sur un .txt de donnees echoue (pas de frontmatter identite:) - c est normal, ce n est pas un outil migre ; les references NON MIS A JOUR signalees sont des fichiers qui mentionnent l outil sans version (bruit connu, 0 impact manquant reel).
## [LECON] 2026-08-09 -- SYMBOLES MANQUANTS AJOUTES AU DICTIONNAIRE (v0.2.2)

**Mission** : ajouter au dictionnaire partage corriger-dictionnaire-accents.txt les familles de caracteres non-ASCII courants encore manquantes (suite directe des guillemets francais v0.2.1).

**Modifications** (7 fichiers) :
1. Dictionnaire partage : +15 entrees -> 66 entrees utiles (68 lignes hors # avec 2 commentaires de section) : fleches verticales et doubles (U+2191 -> ^, U+2193 -> v, U+2194 -> <->, U+21D0 -> <=, U+21D2 -> =>, U+21D4 -> <=>), box drawing (U+2500 -> -, U+2502 -> |, U+250C -> +-, U+2510 -> -+, U+2514 -> +-, U+2518 -> -+, U+251C -> |-, U+2524 -> -|), espace inse cable U+00A0 -> espace simple.
2. Les 2 outils consommateurs en profitent automatiquement : bump 0.2.1-py -> 0.2.2-py (py+sh+md des 2 outils) + ligne historique + doc section caracteres couverts elargie.

**Lecons** :
1. SCAN PAR OCTETS VS SCAN DECODE : compter les octets > 127 est trompeur (les octets 0x80-0x9F sont des artefacts, 0xC2/0xC3/0xE2 des prefixes UTF-8) - toujours DECODER en UTF-8 puis compter les caracteres, sinon on liste des fantomes.
2. PIEGE CHEMINS WINDOWS : l exclusion de dossier par sous-chaine (ex: exemples/) ECHOUE si les chemins contiennent des backslashes - normaliser en forward slashes (replace backslash) avant le test d exclusion, sinon exemples/ (zone volontairement polluee) fausse le scan.
3. LE PROJET EST 100% PROPRE hors exemples/ et hors dictionnaire : le scan propre confirme que les seuls fichiers non-ASCII sont le dictionnaire (exception volontaire) et exemples/ (zone de test). L ajout de symboles est donc PREVENTIF : couvrir les familles qui pourraient apparaitre (schemas box drawing, fleches verticales, NBSP sournois).
4. COHERENCE DES REMPLACEMENTS : suivre les conventions existantes (U+2192 -> ->, U+2190 -> <-) : fleches verticales -> ^ et v, double sens -> <->, doubles -> <= => <=>, box drawing transcrits en traits/coins ASCII (+- -+ |- -|), NBSP -> espace simple. Verifier l absence de doublon/conflit AVANT d inserer (script avec controle).
5. REGLE DES 5 FICHIERS : apres bump de version, verifier py, sh, md des 2 outils + ligne historique + doc mention - ici 6 fichiers outils + 1 dictionnaire = 7, ASCII 0 (sauf dictionnaire), LF pur, nommage 0 erreur.
6. TESTS SEQUENTIELS : jamais 2 outils de correction en parallele sur le meme fichier (fausse les compteurs) - un fichier neuf par test, dossier neutre .zz-xxx (les noms .tmp/test- sont exclus par defaut).
## [LECON] 2026-08-09 -- ALIGNER UN TEST SUR LA REALITE (2 KO PREEXISTANTS)

**Mission** : mettre a jour test-005-generateurs-commande pour les 2 KO preexistants
(point 17 : version parcours-atlas attendue 0.1.5 vs reelle 0.1.10 ; point 18 : le test
exigeait 0 commande en dur alors que la case c30 porte une commande TEMPLATE connue
cartographier-parcours.py {parcours}).

**Lecons** :
1. QUAND UNE DONNEE EVOLUE, UN TEST OBSOLETE EST UNE DETTE : le .md documentait deja le
   residu (tableau : "1 commande restante c30") mais le .py exigeait encore 0 -> le test
   et sa doc ne racontaient pas la meme histoire. Toujours aligner .py ET .md ensemble.
2. NE PAS GELLER UNE DEFAILLANCE SANS GARDE-FOU : le point 18 ne doit pas devenir
   "toujours passer" - il doit tolerer EXACTEMENT le residu connu (n_commande == 1 ET
   case == c30) pour que TOUTE commande supplementaire soit un KO (detection de regression).
3. BALAYER TOUTES LES REFS DE VERSION : apres un changement de version attendue, grep
   complet sur les 2 fichiers (docstring, en-tete, titre, commentaires de section dans le
   CODE) - la ref v0.1.5 a ete trouvee 9 fois, dont 1 dans un commentaire de section
   (ligne 173) facile a oublier.
4. DECALAGE DOCUMENTAIRE A CORRIGER AU PASSAGE : le .md ligne 14 disait catalogue 0.2.0
   alors que le .py verifie 0.2.3 - profiter d une mise a jour de test pour resynchroniser
   la doc avec le code (regle des 5 fichiers appliquee au test lui-meme).
5. VALIDATION = RE-EXECUTION COMPLETE : 26/26 OK apres correction, ASCII 0, LF pur,
   py_compile OK, 0 residu. Un test mis a jour doit re-passer A L IDENTIQUE avant clore.
## [LECON] 2026-08-09 -- GARDE-FOU CLES DUPLIQUEES DANS LE REGENERATEUR DE CATALOGUE

**Mission** : ajouter un garde-fou a generateurs-regenerer-catalogue pour detecter les cles
dupliquees dans parametres lors des regenerations (lecon inserer-contenu-fichier : cle fichier
en double = collision de placeholder = meme valeur generee 2 fois).

**Lecons** :
1. LA DEDUPLICATION DE parser_aide NE COUVRE QUE LES NOUVELLES ENTREES : le mode sync
   PRESERVE l existant tel quel - un doublon preexistant passait sans controle. Le garde-fou
   doit valider le catalogue FINAL (existant + nouvelles + speciales + originales) AVANT
   ecriture, jamais seulement ce qui est genere.
2. GARDE-FOU = REFUS D ECRITURE + EXIT NON NUL : ne pas se contenter d un avertissement -
   si doublon detecte, ne PAS ecrire et lister les entrees fautives (nom + cles). En dry-run,
   rapport sans ecriture (outil de controle avant application).
3. TESTABILITE = OPTION --catalogue <chemin> : tester le garde-fou (positif et negatif) SANS
   toucher au catalogue reel - cibler une copie temporaire. Positif = doublon injecte -> refus
   + fichier inchange ; negatif = copie saine -> ecriture OK.
4. DEFAILLANCE LATENTE CRLF DECOUVERTE : l outil ecrivait en CRLF alors que le standard projet
   est LF (.gitattributes eol=lf + protocole-outils) - toute regeneration wet aurait corrompu
   le catalogue (conflit LF/CRLF). Corrige : ecriture LF pur + docstring/docs/spec mis a jour.
5. REGLE DES 5 FICHIERS APPLIQUEE : bump 1.0.0 -> 1.1.0 sur py (VERSION) + md (Version +
   historique) + spec (3 refs : frontmatter, champ version, titre) - le .sh est un simple
   wrapper exec (parite --version automatique, aucune version a dupliquer - verifier avant de
   chercher).
6. VALIDATION NON-REGRESSION : test-005 26/26 apres modification du regenerateur - le catalogue
   reel ne doit JAMAIS etre modifie par les tests du regenerateur (option --catalogue).
## [LECON] 2026-08-09 -- CORRECTION POINT MINEUR AUDIT : COMMENTAIRE STALE LIGNE 318

**Mission** : corriger le commentaire stale de generateurs-regenerer-catalogue.py (ligne 318)
'puis reecrire CRLF' -> 'puis ecrire en LF pur (standard projet)' - point mineur signale par
l audit Themis de conformite d execution (rapport garde-fou regenerateur).
**Lecons** :
1. UN COMMENTAIRE QUI DECRIT UN ANCIEN COMPORTEMENT EST UN ECART : quand on supprime une
   logique (resultat_crlf), le commentaire inline qui la decrivait devient trompeur - le
   corriger dans la MEME mission (ne pas laisser le docstring seul a jour).
2. CORRECTION DE COMMENTAIRE = PAS DE BUMP DE VERSION : la recommandation de l audit etait
   explicite (1 ligne, sans bump) - la version v1.1.0 reste inchangee, parite py/sh intacte.
3. VALIDATION LEGERE MAIS COMPLETE : py_compile + bash -n + parite --version + ASCII 0 +
   LF pur + grep de non-regression ('reecrire CRLF' absent) - une correction de commentaire
   ne necessite pas la batterie complete des tests fonctionnels.
## [LECON] 2026-08-09 -- GENERATEURS-AMELIORATION CREE (v1.0.0)

**Mission** : creer le generateur d'amelioration et d'optimisation (checklist
de questions par theme, format JSON) + theme ameliorer-outil + inscription
index-tools/catalogue.

**Livrables** :
- `generateurs-amelioration.py` v1.0.0 (py) + `.sh` (wrapper pur) + `.md` + `spec/`
- `themes-amelioration.json` : theme `ameliorer-outil` (10 questions avec raison)
- index-tools.md : ligne + total bump (108 -> 109)
- catalogue-commandes.json : entree triee (position 45), total 111 -> 112
- Interface : `--theme <nom>` / `--reponses 'q1=...;q2=...'` / `--liste` / `--aide` / `--version`

**Validations** : parite py/sh --version OK - interrogation 10/10 non-interactive
OK - theme inconnu -> erreur OK - py_compile/bash -n OK - nommage OK - ASCII 0 -
LF pur - detecter-decalages-catalogue : 111 conformes / 0 decalage - test-005
26/26 OK.

**Lecons** :
1. Le mecanisme de questions de `generateurs-commande` (poser_question +
   parametres question/raison) est le modele naturel : reutilise pour la
   checklist, pas de reimplementation (code reuse).
2. L'option `--aide` est OBLIGATOIRE pour tout outil reference au catalogue :
   `detecter-decalages-catalogue` classe en "NON TESTABLE" tout outil sans
   aide reconnue (decouvert : mon outil etait le 1 non testable, corrige).
3. Checklist interrogee = reflexion deplacee HORS des cartes de decision
   (philosophie : alleger = decomposer, une place pour chaque chose).
4. Catalogue : toute nouvelle entree est inseree en position TRIEE (verifier
   le tri apres insertion) avec modele --theme {theme} et parametre obligatoire.
5. Hors perimetre (pre-existant, a ne pas corriger sans mission) :
   `test-001-evaluer-agents-coherence` reste "NON TESTABLE" (script de test
   sans --aide reference au catalogue).
6. Regle des 5 fichiers respectee (py, sh, md, spec) + enregistrements
   (index-tools, catalogue) + themes JSON = 6e fichier du dossier.
## [LECON] 2026-08-09 -- VALIDER-CASE CREE (v1.0.0, etape 2 de la refonte)

**Mission** : creer l outil qui valide et allege les cartes de decision
(etape 2 de la spec-refonte-cartes-decision v0.1.1, contrat section 6), avec
la CHAINE OBLIGATOIRE : apres la creation, activer Morpheus (tests) puis Janus
(controle) - la lecon de la conformite manquee sur generateurs-amelioration.

**Livrables** :
- `valider/valider-case/valider-case.py` v1.0.0 + `.sh` (wrapper pur) + `.md` + `spec/`
- index-tools.md : ligne + total bump (109 -> 110)
- catalogue-commandes.json : entree triee (position 94), total 112 -> 113
- Interface : <parcours.json> + --case / --surcharge / --modele / --references
  / --dry-run / --rapport / --version / --aide

**Fonctionnement** : verdict CONFORME / A ALLEGER / NON CONFORME + rapport md.
- STRUCTURE : types valides (question/controle/indice/action/fin), case_depart,
  fins joignables (BFS)
- MODELE : branches min 2 pour decisions ; indice/action = suivant requis ;
  boucle directe = erreur SAUF pattern de re-essai (controle NON -> soi-meme,
  volontaire, = avertissement) ; deviation sans rejoint = avertissement
- ALLEGEMENT : > 3 indices OU texte > 160 car. = signale avec proposition
- REFERENCES : ref resolvable (pattern-N -> spec-guider ; chemin -> fichier ;
  protocole-/regle- -> regles-immuables)
- NORMES : nommage c<numero>[a-z]?, titre, ASCII

**Resultat revelateur** : parcours-cerberus = A ALLEGER (0 erreur, 15
surcharges, 1 avertissement) - la preuve objective de la degradation des
cartes que la refonte doit corriger.

**Validations** : parite py/sh --version v1.0.0 OK - py_compile/bash -n OK -
nommage 0 erreur (apres renommage validateur-case -> valider-case, voir lecons)
- ASCII 0 - LF pur - detecter-decalages-catalogue 112 conformes / 0 decalage -
test-005 26/26 - 0 residu.

**Lecons** :
1. LE NOMMAGE PRIME SUR LE CONCEPT : l outil s appelait validateur-case (concept
   de la spec) mais le dossier valider/ exige le prefixe valider- -> renomme en
   valider-case AVANT le chainage (le concept reste dans les descriptions).
   TOUJOURS lancer valider-nommage AVANT de brancher quoi que ce soit.
2. Le pattern de re-essai (controle NON -> soi-meme) est VOLONTAIRE dans les
   cartes (c5 cerberus, c8 vulcain) : le validateur le traite en avertissement,
   pas en erreur - croiser la realite des cartes avant de figer une regle.
3. La preuve de la degradation est maintenant AUTOMATISEE : valider-case sur un
   parcours donne le compte exact de surcharges (15 sur cerberus) - la refonte
   des generateurs (etapes 3-4) pourra mesurer sa propre efficacite.
4. CHAINE EXECUTEE : cette fois je n ai PAS reactive Cerberus - j ai active
   Morpheus (case c8) pour les tests formels test-009-valider-case, puis la
   carte de Morpheus enchainera sur Janus. La conformite devient le defaut.

## [LECON] 2026-08-09 -- ETAPE 3 TERMINEE : generateurs-case v0.3.0 (modele compose complet + --ref)

**Mission** : refondre generateurs-case selon la spec-refonte-cartes-decision section 7.1 (etape 3).

**Actions realisees** :
1. `ajouter-bloc` generalise en MODELE COMPOSE COMPLET : decision + branches min 2 (OUI/NON + `--branche <rep>:<vers>` repetable) + deviation + rejoint.
2. Indices deviation/rejoint transformes en REFERENCES (`--ref-deviation`/`--ref-rejoint`, defaut `pattern-7`) : `{"type": "ref", "ref": "pattern-7"}` au lieu des textes inline longs -> valider-case ne signale plus de surcharge (verifie : bloc cree = 0 a alleger, verdict CONFORME).
3. Option `--ref <ref>` (repetable) ajoutee a `ajouter` et `editer` : pose des indices de type reference (cle `ref`, alignee sur `valider-case --references`).
4. Validation auto enrichie : appel interne `valider-case <parcours> --modele --dry-run` apres chaque modification (spec-refonte 7.1) - un verdict NON CONFORME bloque l'operation.
5. Regle des 5 fichiers : py + sh + md a jour (0.2.2 -> 0.3.0), SPEC CREE (spec-generateurs-case.001.01.ebauche.md, manquait - regle des 5 fichiers), index-tools ligne mise a jour.
6. 1 caractere non-ASCII introduit pendant la refonte ("cle" dans un docstring) -> corrige immediatement (lecon : verifier ASCII des docstrings apres toute edition).

**Lecons** :
1. Les indices de type REFERENCE (cle `ref`) sont le moyen d'alleger les cartes : un bloc compose genere par ajouter-bloc v0.3.0 ne produit AUCUNE surcharge (0 a alleger) alors que v0.2.2 en produisait 2 (textes inline > 160 car).
2. Le format de ref doit etre aligne sur la detection de valider-case --references : `pattern-<N>`, `protocole-<x>`/`regle-<x>`, chemin relatif. Lire l'outil de validation AVANT de choisir le format.
3. La spec de l'outil generateurs-case n'existait pas (regle des 5 fichiers incomplete) - creee avec la refonte.
4. Le testeur existant (tester-generateurs-case.sh) a 3 echecs PREEXISTANTS (PT5/PT6b attendent 21 cases dans parcours-vulcain, la carte en a 32 ; PT8b recablage c7->c20, c20 n'existe plus) : compteurs obsoletes, INDEPENDANTS de la refonte (PT6/PT9/PT15 passent). A corriger par Morpheus dans le test formel.

**Validation** : py_compile OK, bash -n OK, parite --version py/sh = v0.3.0, ASCII 0 (4 fichiers + spec), LF pur 0 CRLF, nommage 0 erreur, detecter-decalages 112 conformes / 0 decalage, test-005 26/26 OK.

**Conformite** : apres creation, j'active Morpheus (tests formels test-010) conformement a ma carte c8 - la chaine bout-en-bout continue.

## [LECON] 2026-08-09 -- ETAPE 4 TERMINEE : generateurs-carte v0.3.0 (squelette allege + delegation validateur-case)

**Mission** : refondre generateurs-carte selon la spec-refonte-cartes-decision section 7.2 (etape 4).

**Actions realisees** :
1. `creer` : squelette ALLEGE - les 8 textes de regles inline longs (> 160 car) des cases
   c0/c0b/c0c/c1/c2/c2b remplaces par des REFERENCES resolvables :
   - `protocole-activation` (relecture c0, action obligatoire c0b - resolu par recherche dans regles-immuables)
   - `pattern-6` (contexte temps reel c0c), `pattern-10` (une carte = un role c1),
   - `pattern-3`, `pattern-7`, `pattern-2` (rappels c2),
   - `cerveau-projet/agents/regles-immuables/general/rvav-workflow.md` (RVAV c2b, chemin relatif).
   Une carte neuve nait CONFORME (erreurs 0, a alleger 0) - LA PREUVE de l allegement a la creation.
2. `detecter` : delegation au validateur-case v1.0.0 (`--modele --surcharge --references`) en
   complement des anomalies structurelles locales - source unique de verite (spec 7.2).
3. `dupliquer-chemin` : les references sont CONSERVEES telles quelles dans les copies
   (teste : dc1 porte la ref pattern-10, aucun texte inline duplique).
4. `valider_auto` : ajout de l appel `valider-case --modele --references --dry-run` apres chaque ecriture.
5. Regle des 5 fichiers : py + sh + md a jour (0.2.0 -> 0.3.0, parite), SPEC CREE (spec-generateurs-carte.001.01.ebauche.md),
   index-tools ligne maj, catalogue choix action corrige (creer/analyser/detecter/dupliquer-chemin - manquait detecter).

**Lecons** :
1. La carte neuve nait ALLEGEE : squelette v0.3.0 = CONFORME des la creation (0 surcharge),
   alors que v0.2.2 generait des textes inline longs detectes par valider-case.
2. Les references `pattern-N`/`protocole-x`/chemins sont resolues par valider-case --references
   (pattern-N = "### Pattern N" dans spec-guider-parcours ; protocole-x/regle-x = recherche par nom
   dans regles-immuables ; chemin = fichier existant). Voir resoudre_reference avant de choisir.
3. --version seul echouait (action requise par argparse) -> interception dans main() comme --aide
   (lecon repetee de l etape 3 : tester --aide/--version sur les outils a sous-commandes).
4. Le catalogue portait un choix obsolet (["creer","analyser","dupliquer"]) - detecter manquait
   et le nom exact est dupliquer-chemin : verifier le catalogue apres toute modification de sous-commandes.
5. Attention ASCII strict dans les scripts temporaires (2 fois "nait/cle" corriges).

**Validation** : py_compile OK, bash -n OK, parite --version py/sh = v0.3.0, ASCII 0 (4 fichiers + spec),
LF pur 0 CRLF, nommage 0 erreur, detecter-decalages 112 conformes / 0 decalage, test-005 26/26 OK.

**Conformite** : apres creation, j'active Morpheus (tests formels test-011) conformement a ma carte c8.

## [LECON] 2026-08-09 -- ETAPE 5 TERMINEE : guider-parcours v0.4.0 (resolution des references + type action)

**Mission** : consolider guider-parcours selon la spec-refonte-cartes-decision etape 5 (resolution des
references d indices + ordre d execution obligatoire + IMPLEMENTER LE TYPE action, critere 7).

**Actions realisees** :
1. RESOLUTION DES REFERENCES dans afficher_indices (nouvelle fonction resoudre_reference) :
   - pattern-<N> : affiche [REFERENCE] X puis le TITRE + 3 premieres lignes du Pattern N extraites
     de la spec-guider-parcours (format '### Pattern N -- Titre') ;
   - protocole-<x>/regle-<x> : chemin du fichier/dossier trouve par recherche dans regles-immuables ;
   - chemin relatif : affiche le chemin + (fichier existant)/(reference non resolvable).
   Une case du squelette v0.3.0 affiche desormais le CONTENU resolu des refs (pattern-3/7/2, rvav) -
   la regle vit a UN endroit et l agent la voit resoudre a la navigation.
2. IMPLEMENTATION DU TYPE action dans naviguer (spec critere 7) : une case action avec 'suivant'
   s execute SANS question et enchaine automatiquement (teste : c8 action -> c9 fin -> PARCOURS TERMINE).
   Ajout du type action dans les tableaux de la spec-guider-parcours (version 0.4.0) et du .md.
3. generateurs-case v0.3.1 : type action ajoute aux choix de ajouter/editer + construire_case pose le
   'suivant' pour action comme pour indice (bug detecte : le suivant n etait pose que pour indice).
4. valider-case v1.0.0 acceptait DEJA le type action (TYPES_VALIDES prepare a l etape 2) - aucune
   modification necessaire de ce cote.

**Lecons** :
1. L'integration d'un nouveau type de case est TRANSVERSALE : guider-parcours (navigation) +
   generateurs-case (creation/edition) + valider-case (validation) + spec + .md. Verifier CHACUN
   (valider-case l avait deja, generateurs-case ne l avait pas - corrige).
2. Le bug 'suivant non pose pour action' etait silencieux : la case etait creee mais sans suivant,
   le validateur le signalait (--modele) et la navigation echouait. Le test formel (test-010 mis a jour
   avec 2 points action) couvre maintenant ce cas.
3. Apres bump de version d'un outil, les tests formels existants qui verifient la version (test-010
   attendait v0.3.0) doivent etre mis a jour : 1 KO detecte, corrige (v0.3.1 + 2 nouveaux points).
4. Resoudre une reference pattern-N : le titre est '### Pattern N -- Titre', le corps suit jusqu'a la
   prochaine '### '. Afficher 3 lignes suffit (l agent va lire la source pour le detail).

**Validation** : py_compile OK, bash -n OK, parite --version py/sh = v0.4.0 (gp) / v0.3.1 (gc),
ASCII 0 (7 fichiers), LF pur 0 CRLF, nommage 0, detecter-decalages 112 conformes / 0 decalage,
test-001-guider-parcours 14/14, test-005 26/26, test-010 25/25 (maj), test-011 19/19.

**Conformite** : apres creation, j'active Morpheus (tests formels test-012) conformement a ma carte c8.
## [LECON] 2026-08-09 -- CORRECTIF valider-case v1.0.1 : garde-fou anti-pollution du rapport

**Mission** : corriger le defaut de valider-case qui ecrivait son rapport par defaut dans le repertoire courant (lecon : rapport a la racine cree a 19:13 par Buffy).
**Resultat** : v1.0.1, aucun fichier cree sans --rapport <fichier> explicite.
**Lecons** :
1. Le defaut : quand --rapport absent ET --dry-run absent, valider-case ecrivait rapport-valider-case-<date>.md dans le CWD relatif au repertoire de lancement -- un agent lancant depuis la racine pollue la racine
2. Le correctif : sans --rapport <fichier> explicite, AUCUN fichier n'est cree (message clair 'AUCUN RAPPORT ECRIT : utilise --rapport <fichier>') ; --rapport <fichier> ecrit exactement au chemin fourni ; --dry-run conserve la simulation
3. Regle des 5 fichiers respectee : py (v1.0.1) + sh (Version 1.0.1) + md (historique + section rapport obsolete corrigee) + spec (Version + Historique) + test-009 (version + nouveau point 11b garde-fou)
4. Le test-009 passe de 19 a 20 points : le point 11b verifie qu'une commande sans options ne cree aucun fichier dans le repertoire courant
5. Aucun test existant ne dependait de l'ecriture par defaut (tous utilisaient --dry-run ou --rapport explicite) : la regression est nulle
6. Normes : ASCII strict + LF pur sur les 5 fichiers

**Preuve** : test-009 20/20, parite py/sh v1.0.1, commande sans options depuis /tmp = 0 fichier cree.

## [LECON] 2026-08-09 -- OUTIL generateurs-ligne cree (v0.1.0, categorie generateurs/)

**Mission** : creer generateurs-ligne (decision utilisateur) -- maillon du milieu de la suite des generateurs de cartes de decision (carte -> ligne -> case). Ligne = chemin de bout en bout ; configs = gabarits de groupes de cases ; carte Atlas a jour (existence + mtime) ; dry/wet.
**Livrables** : generateurs-ligne.py + .sh (wrapper pur exec python3) + .md + spec/ + entree catalogue-commandes.json (113 -> 114) + index-tools.md (103 -> 104).

**Lecons** :
1. La suite des generateurs est maintenant : generateurs-carte (carte COMPLETE) -> generateurs-ligne (LIGNE = groupe de cases en un bloc) -> generateurs-case (UNE case). Le maillon du milieu prepare un bloc conforme (decision + branches + deviation + rejoint) sans connaitre le metier : l'edition fine reste a l'agent habilite via SA carte.
2. LA CONVENTION DE NOMMAGE DES IDS DE CASES EST STRICTE : c<numero>[a-z]? (PAS DE POINT). Mon premier jet generait c42.1/c42.2 -> valider-case a refuse (NOMMAGE) a la validation auto. Corrige : c42, c42a, c42b... (suffixes lettres, jamais de point).
3. La case REJOINT d'un bloc doit pointer vers la cible EXTERNE fournie (--rejoint), pas vers elle-meme : un gabarit "REJOINT -> REJOINT" cree une boucle. Distinguer le suivant de la case REJOINT (externe) des suivants des cases AVANT (vers la case REJOINT du bloc).
4. Verification carte Atlas avant edition : cartographie-<agent>.md doit exister ET avoir un mtime > parcours JSON. Si absente/perimee -> BLOCAGE + invite a activer Atlas (case c31 Cartographier de SA carte) pour regenerer, puis revenir. --force passe outre (decision explicite).
5. Cablage du point d'attache : question/controle -> ajouter une BRANCHE (--reponse) ; action/indice -> recabler le suivant vers la premiere case (l'ancien suivant devient le rejoint par defaut). Une question/controle SANS suivant exige --rejoint explicite.
6. Parite py/sh (--version identiques) : le .sh est un wrapper pur exec python3 avec gestion --version avant l'exec.
7. detecter-impacts a signale 3 faux positifs de DATE (fichiers plus anciens sans aucune reference a generateurs-ligne) : verifier par grep que 0 reference -> justifie le NON MIS A JOUR sans modification.
8. Le catalogue attend le champ modele "{action} {parcours}" avec des parametres interpoleables (choix/texte) -- l'utilisateur compose la commande exacte via generateurs-commande.

**Validation** : py_compile OK, bash -n OK, parite --version py/sh = v0.1.0, ASCII 0 (4 fichiers), LF pur 0 CRLF, nommage 0, catalogue 114 trie, index-tools 104, bout en bout via generateurs-commande OK, ajout reel config defaut/config-1/config-3 -> valider-case CONFORME 0 erreur.

**Conformite** : apres creation, j'active Morpheus (test-017-generateurs-ligne) conformement a ma carte c8.
## [LECON] 2026-08-09 -- MODE BATCH CONVERTIR CREE : generateurs-case v0.4.0

**Mission** : ajouter une sous-commande `convertir` (mode batch) a generateurs-case pour
migrer les parcours avec l'outil au lieu de scripts maison (decision utilisateur apres
constat : les migrations promethee/minerve/vulcain avaient ete faites par des scripts
.zz-migration-* au lieu des generateurs).

**Livraison** : generateurs-case v0.3.1 -> v0.4.0.
- Nouvelle sous-commande `convertir` : convertit en masse les cases type=indice ->
  type=action, remplace les regles longues (> seuil, defaut 160 car) par des refs via
  un fichier de mapping JSON (--refs), rapport X converties / Y remplacees / Z
  avertissements, --version-parcours pour bumper la version, --dry-run pour simuler.
- Recablage (suivant/branches) conserve a l'identique : une conversion indice -> action
  ne change pas la navigation.
- Validation auto lancee apres l'ecriture : references + guider-parcours --liste +
  valider-case --modele (verdict CONFORME 0 erreur 0 a alleger sur le test vulcain).
- Mapping JSON : { "motifs": [ {"contient": "...", "ref": "pattern-2"}, ... ],
  "cases": { "<case_id>": "protocole-tests" } } -- les refs par case_id ont priorite.
- 5 fichiers a jour : py 0.4.0, sh 0.4.0 (wrapper, parite par construction), md 0.4.0
  (section convertir), spec 0.4.0 (historique), catalogue (entree + version).

**Tests reels** : py_compile OK, --version py/sh identiques, nommage OK, ASCII 0 sur
les 5 fichiers, LF pur, dry-run = fichier inchange (version 0.2.13 intacte), wet =
17 actions / 0 indice / 2 controles preserves / 7 fins / 23 refs / valider-case
CONFORME.

**Lecons** :
1. La philosophie 'les generateurs doivent etre utilises' s'applique AUSSI aux outils
   de maintenance : une migration de parcours se fait avec generateurs-case convertir,
   pas avec un script maison. Le mode batch comble le manque qui poussait aux scripts.
2. La non-regression des tests existants revele 4 ECHECS PREEXISTANTS (tester-
   generateurs-case.sh attend 21 cases, le parcours vulcain en a 32 depuis plusieurs
   versions) : prouve en relancant le test avec le parcours original HEAD (17/4 egalement).
   Aucun de ces echecs ne vient de la commande convertir (tous les tests de comportement
   existants de l outil passent). LA CORRECTION DES TESTS EST DELEGUEE A MORPHEUS
   (regle DELEGATION DES TESTS : jamais corriger les tests soi-meme).
3. Piege argparse : une sous-commande avec un flag --version (bump parcours) entre en
   conflit avec le --version outil ajoute par la boucle commune -- le retirer de la
   boucle et le declarer specifiquement (--version-parcours).
4. Le seuil par defaut 160 car aligne generateurs-case sur le modele des parcours
   migres (0 regle > 160) -- le mapping des regles SPECIFIQUES (RELECTURE, 5 FICHIERS,
   etc.) reste une decision d edition par parcours (les raccourcir ou les mapper).

## [LECON] 2026-08-10 -- valider-cartes-decision v0.3.1 : type action ajoute (impact oublie de la migration)

**Contexte** : la migration des 11 parcours au format action (modele cible de la refonte) etait terminee
(100% actions, valider-case CONFORME, test-005 26/26) MAIS valider-cartes-decision.py figeait
TYPES_VALIDES = (question, indice, controle, fin) sans action -> NON CONFORME sur les 11 parcours.
La spec-refonte ne mentionnait pas cet outil (impact oublie). Cerberus a detecte l'ecart via la
validation finale.

**Correction** :
1. TYPES_VALIDES + action dans le .py (ligne 43) + mentions types dans docstring (ligne 20),
   affichage (ligne 136) et .md (3 mentions + tableau erreurs)
2. Docstring stale ligne 22 : spec v0.2.9 -> v0.5.0 (spec actuelle)
3. Parite : .sh = wrapper (VERSION 0.3.0 -> 0.3.1), .md version + historique, test version figee
4. Verification : 11/11 agents CONFORME, parite --version py/sh, ASCII 0 + LF pur

**Lecons** :
1. TOUTE migration de modele doit scanner les VALIDATEURS du modele (valider-case ET valider-cartes-decision)
   - un validateur obsolete = la migration semble terminee mais le juge dit NON CONFORME
2. La version d'un outil se propage a 4+ fichiers : py, sh (wrapper), md, tests (version figee)
3. Un .sh wrapper ne duplique PAS la logique mais porte SA version -> parite --version obligatoire
4. Valider avec --tous/--agent apres correction, pas seulement le fichier modifie (11 parcours ici)

## [LECON] 2026-08-10 -- MENTIONS STALE DE VERSION CORRIGEES (2 .md generateurs, suite scan Cerberus)

**Contexte** : apres la correction valider-cartes-decision v0.3.1 (spec v0.2.9 -> v0.5.0),
Cerberus a lance un scan systematique des mentions de versions dans tous les outils.
Le scan a distingue 2 classes :
1. REFERENCES D'INTRODUCTION (LEGITIMES) : les mentions qui citent un pattern/regle avec SA
   version d'introduction (ex : Pattern 5 spec v0.2.6, Pattern 9 v0.2.16, Piste C v0.2.20,
   chaine bout-en-bout v0.2.15) - la spec v0.5.0 les documente ELLE-MEME avec ces versions
   dans ses titres de patterns et son historique. A CONSERVER.
2. VERSION COURANTE DU FORMAT (STALE) : les lignes "Format des cases : spec-guider-parcours
   vX (types question/indice/controle/fin...)" - 2 trouvees :
   - generateurs-case.md ligne 342 (spec v0.2.5)
   - generateurs-carte.md ligne 195 (spec v0.2.13)
   Toutes deux listaient les types SANS action et avec une version obsolete.

**Correction** : 2 lignes seulement -> spec-guider-parcours v0.5.0 + types
question/indice/controle/fin/action. Le .py de generateurs-case etait DEJA a jour
(action present lignes 331/878/897 - non modifie).

**Verifications** : ASCII 0 + LF pur, re-scan 0 mention stale, test-014 spec v0.5.0 12/12 OK,
guider-parcours --liste OK.

**Lecons** :
1. UNE LEON HISTORIQUE (recit documentant l'etat d'une epoque) n'est PAS stale : elle decrit
   le passe (ex : vulcain/corrections.md v0.3.0 listait les types sans action) - on ne la
   modifie pas, comme on ne modifie pas un tableau d'historique
2. Pour scanner les mentions stale, distinguer : version d'INTRODUCTION d'un pattern (legitime,
   la spec la cite) vs VERSION COURANTE du format (stale si obsolete)
3. Le bug "types sans action" etait dans PLUSIEURS .md d'outils (valider-cartes-decision,
   generateurs-case, generateurs-carte) - un scan systematique est necessaire, pas une
   correction au cas par cas

## [LECON] 2026-08-10 -- DIVERGENCE GUIDER-PARCOURS CORRIGEE (spec 0.5.0 / py-sh-md 0.5.0)

**Mission** : corriger la divergence de version guider-parcours (spec 0.5.0
vs py/sh/md 0.4.0) detectee par Themis dans l audit de la chaine (recommandation
regle des 5 fichiers).

**Resultats** :
- py : commentaire `# Version` + variable `VERSION = "0.5.0"` (la variable est
  la VRAIE source pour --version, pas le commentaire)
- sh : commentaire `# Version` -> 0.5.0 (le sh n a pas de variable de version
  separee, il affiche la meme valeur)
- md : `| **Version** | 0.5.0 |`
- Verification : parite --version py/sh = v0.5.0/v0.5.0, detecter-divergences-
  version : 0 DIVERGENTE (19 ALIGNEES), ASCII 0 + LF pur, navigation --liste OK,
  evaluer-coherence 0 lien casse

**Lecons** :
1. LA DOUBLE SOURCE DE VERSION : un outil py a souvent DEUX endroits qui
   portent la version - le commentaire d en-tete ET la variable VERSION lue par
   --version. Corriger le commentaire seul ne change rien a --version :
   verifier TOUJOURS la parite avec la commande reelle apres le bump
2. La regle des 5 fichiers inclut la VERIFICATION PARITE py/sh --version
   (etape obligatoire apres toute modification de version d un outil py+sh)
3. La divergence guider-parcours etait purement un bump manquant (le py 0.4.0
   contenait deja les fonctionnalites 0.5.0 : resolution des refs, type action)
   - l etape 7 de la refonte (spec 0.5.0) n avait pas ete suivie du bump des
   3 fichiers
4. detecter-divergences-version est l outil de verification finale : 0
   DIVERGENTE confirme l alignement des 5 fichiers
## [LECON] 2026-08-10 -- COMBO CONTROLE-BUFFY CREE (v0.1.0)

**Mission** : creer le combo-controle-buffy pour alleger les cases c11/c18 du parcours janus (etape 2a du Pattern 16 - ALLEGEMENT).

**Livrables** : cerveau-projet/agents/tools/combos/combo-controle-buffy/definition-combo.json (5 cases : c1 rappel pattern-2, c2 rappel pattern-12, c3 lire protocole-controle-buffy, c4 creer fichier de controle, c6 FIN).

**Lecons** :
1. La structure d'un combo (Pattern 3) = nom + version + description (avec les variables attendues --var) + cases. Le c1 doit rappeler la mission et les variables attendues.
2. Le format des reponses de combos-moteur est `c1=OUI;c2=OUI` (separateur ;), PAS une liste d'arguments --reponses separes.
3. Le test reel : navigation OUI/OUI -> fin c6 atteinte, fichier de controle cree. Teste avec un fichier temporaire dans .zz-test-combo puis nettoye.
4. Les variables de combos doivent etre en forward slashes (piege Windows documente dans le protocole-creation-combos).
5. Le combo cree dans l'esprit du Pattern 16 : il encapsule une SEQUENCE (rappel regles + lecture protocole + creation fichier) pour ramener c11/c18 de 4 indices a 1 indice combo.
6. Outils utilises : combos-moteur (test navigation), valider-conformite-ascii (0 non-ASCII), controle CRLF (LF pur). Fichiers JSON valides (json.load OK).

## [LECON] 2026-08-10 -- CREATION DES 3 COMBOS CLIO (Vulcain)

**Mission** : creer les 3 combos de Clio (test reel avant la grosse MAJ du README).
**Resultat** : 27/27 tests passent + dry-run des 2 chemins du combo encapsule.

**Combos crees** :
1. `combos-analyse-projet` (orchestre py/sh/md, v0.1.0) : etat reel du projet (agents, outils par categorie) + ecarts README vs realite + rapport clio/rapports/
2. `combo-maj-readme` (encapsule definition-combo.json, v0.1.0, 5 cases) : PETITE MAJ - verifier -> maj (si ecarts) -> ASCII, pilote par combos-moteur
3. `combos-maj-readme-massive` (orchestre py/sh/md, v0.1.0) : GROSSE MAJ conservative - analyse -> verifier -> maj -> correctifs de fond -> ASCII -> rapport

**Lecons** :
1. Piege accent : les docstrings/comments doivent etre ASCII strict - verifier apres ecriture (valider-conformite-ascii) car les accents echappent facilement dans les longues chaines
2. Format reponses de combos-moteur : `--reponses 'c2=OUI'` (case=reponse), pas 'OUI' seul
3. Parite .sh : le .sh delegue au .py (source de verite) - garder le fallback erreur propre
4. Format definition encapsule : combo (nom, description, version, case_depart) + cases (outil/controle/fin) + identite - modele combo-controle-buffy
5. Modele orchestre : verifier_nommage + argparse --version + couleurs ANSI + --rapport - modele combos-audit-general
6. Les definitions vivent dans agents/tools/combos/combo-*/ (pas dans cerveau-projet/combos/ qui n'existe pas)
7. Outils utilises : lire-fichier, activer-agent-principal ; tests via scripts temporaires nettoyes

## [LECON] 2026-08-10 -- PROTOCOLE VERIFICATION COHERENCE CREE (Vulcain v0.1.0)
1. Protocole cree a partir des lecons Themis du re-audit README : 7 sections (Objectif, Prerequis, Etapes E1-E7, RVAV, Exemples, Pieges, Liens) au format exact du modele protocole-audit-buffy.
2. 4 pieges documentes : separateurs de table MULTIPLES (localiser l'en-tete PUIS le separateur), anciens totaux dans l'arborescence commentee (le --maj ne les touche pas), badges tous sur une ligne unique (compter img.shields.io/badge/), categories virtuelles sans dossier physique (templates = outil-template.md racine).
3. Le tri automatique d'une table peut ECRASER l'en-tete sans erreur de contenu : la verification de STRUCTURE (E3) est obligatoire apres tout reordonnancement.
4. Referencement dans index-regles-general.md (table Protocoles, statut ebauche) + normes ASCII 0 + LF pur.
5. REGLE : ne jamais valider sur la seule base des compteurs de table - scanner les anciennes versions connues dans TOUT le fichier.

## [LECON] 2026-08-10 -- 3 COMBOS CLIO AJOUTES AU CATALOGUE (Vulcain, v0.2.5)
1. Les 3 combos Clio (combos-analyse-projet, combos-maj-readme-massive, combo-maj-readme) sont au catalogue generateurs-commande (118 commandes, v0.2.5, trie).
2. Signature reelle des orchestres : [racine] nargs=? default=. + --rapport flag. Le combo encapsule s'execute via combos-moteur avec le chemin definition-combo.json en dur dans le modele.
3. FORMAT DES REPONSES generateurs-commande : 'cle=valeur;cle2=valeur2' (separateur POINT-VIRGULE, pas le pipe) - mon premier test avec '|' a echoue avec 'Reponse mal formee'.
4. Generation reelle validee : les 3 commandes generees sont executables (--version rc=0).
5. detecter-decalages-catalogue : 115 conformes dont mes 3 combos, 2 decalages PREEXISTANTS (generateurs-case-convertir, generateurs-ligne), 1 non testable (le detecteur lui-meme) - aucun nouveau decalage.
6. NOTA : test-005/007 (KO preexistants) attendent 109/108 commandes - le catalogue en a 118, le RE-SCAN Morpheus devra mettre a jour ces valeurs.

## [LECON] 2026-08-10 -- 5 THEMES D AMELIORATION AJOUTES (Vulcain, themes-amelioration.json v2.1.0)

**Contexte** : le generateur d amelioration ne couvrait que ameliorer-outil (14 q) et ameliorer-agent (5 q). La case c12d du Pattern 17 (pilote themis) peut deleguer 5 autres natures d amelioration : carte, case, combo, parcours, protocole.
**Verdict** : VALIDE (generation reelle testee pour les 5 nouveaux themes, rc=0).
**Lecons** :
1. Format du JSON : {version, themes[]} avec chaque theme = {nom, description, questions[]} et chaque question = {id, question, raison} - ids uniques par theme
2. Aligner les themes avec les protocoles-autoameliorer existants (6 protocoles : agents, cerveau, conventions, outils, protocoles, regles) - les themes couvrent les natures delegables par c12d
3. Tester la GENERATION REELLE (--theme <nom>, rc=0, >= 100 caracteres) pas seulement la presence dans le JSON - et le theme inconnu doit retourner rc=1 avec message
4. Le --liste doit afficher tous les themes avec leur description
5. Le repertoire complet : ameliorer-outil (14), ameliorer-agent (5), ameliorer-carte (5), ameliorer-case (5), ameliorer-combo (5), ameliorer-parcours (5), ameliorer-protocole (5) = 7 themes, v2.1.0
6. Normes : ASCII strict + LF pur + tri alphabetique des themes conserve

## [LECON] 2026-08-10 -- 4 THEMES D AMELIORATION SUPPLEMENTAIRES (Vulcain, themes-amelioration.json v2.2.0)

**Contexte** : audit de couverture - la liste des themes doit couvrir les 6 protocoles-autoameliorer officiels (regles-immuables/general) + la structure reelle du cerveau. Manquants detectes : regles, cerveau, conventions, spec.
**Verdict** : VALIDE - 11 themes au total, couverture 6/6 des protocoles + spec (trio).
**Lecons** :
1. La source de verite des natures d amelioration = le dossier protocole-autoameliorer-* (6 protocoles : agents, cerveau, conventions, outils, protocoles, regles)
2. ATTENTION singulier/pluriel : les protocoles sont au pluriel (agents, outils, protocoles), les themes au singulier (ameliorer-agent, ameliorer-outil, ameliorer-protocole) - verifier avec le mapping correct pour eviter les faux negatifs
3. Le theme ameliorer-spec couvre le trio athena/promethee/minerve (pense-betes, specs, todos) - separe des agents du cerveau-projet
4. Repertoire complet v2.2.0 : ameliorer-outil (14) + 10 themes de 5 questions = 64 questions
5. Chaque theme doit avoir une question de DELEGATION (qui est l agent habilite, Pattern 5/8) et une de DOCUMENTATION (lecon/version) - le generateur garantit que l agent ne fait PAS l amelioration lui-meme
## [LECON] 2026-08-10 -- GARDE-FOU SUIVANT MORT AJOUTE A valider-cartes-decision (Vulcain, v0.3.2)

**Mission** : renforcer valider-cartes-decision pour detecter les suivant morts
(recommandation de l'audit Themis du 2026-08-10 apres correction de 25 suivant
morts sur 10 parcours).

**Ce qui a ete fait** :
1. Controle 7 ajoute dans valider-cartes-decision.py (v0.3.1 -> v0.3.2) : deux
   cas de suivant mort detectes comme ERREUR :
   - case type 'fin' avec champ suivant (la navigation s'arrete a la fin, le
     suivant est ignore)
   - case avec branches non vides ET champ suivant (les branches priment, le
     suivant n'est jamais lu)
2. Le suivant n'est legitime que sur une case SANS branches et NON-fin
   (question/indice/action/controle qui enchaine)
3. Mecanique verifiee dans guider-parcours.py : ligne 336 (fin -> break),
   ligne 380 (branches -> reponse), ligne 385 (suivant seulement si pas de
   branches)
4. Parite py/sh maintenue (le .sh est un wrapper), doc .md mise a jour
   (controle 7 + erreurs courantes + versionning)

**Decouverte importante (la preuve de la valeur du garde-fou)** : le nouveau
controle a revele 3 suivant morts RESIDUELS dans MON propre parcours
(parcours-vulcain v0.3.2) : c8 (controle delegation tests, branches OUI/NON +
suivant), c14 (idem), c18b (question besoin outil, branches TEMPORAIRE/DURABLE
+ suivant). Ces residus avaient echappe a la correction de Buffy (25 suivant
morts) car valider-cartes-decision v0.3.1 ne les detectait pas. Correction :
3 suivant retires, navigation intacte (cases toujours atteignables via
branches), valider-cartes --tous = 11/11 CONFORME.

**Lecons** :
1. Un garde-fou qui ne detecte RIEN lors de son premier deploiement est
   suspect : si le nouveau controle passe sur tous les parcours sans alerte,
   verifier qu'il detecte bien au moins un cas reel (test negatif obligatoire)
2. Les 'suivant morts' sont des residus de migration insidieux : ils ne
   cassent pas la navigation (branches/fin priment) mais polluent la structure
   (chemins fantomes dans le cartographe) et trompent les lecteurs de la carte
3. Le controle 'fin avec suivant' + 'branches avec suivant' devrait etre ajoute
   au detecteur-decalages-catalogue ou a la prochaine version de la
   spec-guider-parcours comme pattern structurel
4. REGLE DELEGATION DES TESTS respectee : je n'ai pas touche aux tests
   (tester-valider-cartes-decision.sh points 1-2 attendent 0.3.1 -> 2 KO) ;
   Morpheus doit mettre a jour les versions + ajouter un point de test pour le
   nouveau controle 7

**Tests attendus (Morpheus)** : tester-valider-cartes-decision.sh (0.3.1 ->
0.3.2, + test du controle 7 : parcours infeste = NON CONFORME), et verification
des references 0.3.1 dans test-004/005/010/012/016.
## [LECON] 2026-08-11 -- COMBO-CREER-* CORRIGES (Vulcain, catalogue v0.2.6)

**Mission** : corriger le KO preexistant test-003 (20 echecs sur les 3 combos
creer-*).

**Cause racine identifiee** : les definitions-combo utilisaient des CLES
D ENTREES OBSOLETES par rapport au catalogue de commandes (source de verite) :
1. valider-conventions + rechercher-fichier : les combos passaient la cle
   'fichier' mais le catalogue attend 'chemin' -> ERREUR 'Parametre
   obligatoire manquant : chemin'
2. copier-dossier : le catalogue n exposait que 'chemin' alors que l outil
   reel exige source + destination positionnels
3. copier-fichier : le catalogue n exposait que 'forcer' alors que l outil
   reel exige source + destination (+ option --forcer)
4. combo-creer-agent c8 : creer-fichier exige 'contenu' obligatoire mais la
   case c8 du combo ne le fournissait pas -> ERREUR 'Parametre obligatoire
   manquant : contenu'

**Corrections appliquees** :
1. CATALOGUE (source de verite) v0.2.5 -> v0.2.6 :
   - copier-dossier : modele {chemin} -> {source} {destination}, parametres
     source (obligatoire) + destination (obligatoire)
   - copier-fichier : modele --forcer -> {source} {destination} {forcer},
     parametres source + destination + forcer (flag optionnel)
2. COMBOS (3 definitions) :
   - combo-creer-fichier-cerveau : c3 (valider-conventions) + c5
     (rechercher-fichier) : cle 'fichier' -> 'chemin'
   - combo-creer-protocole : c1 (valider-conventions) : cle 'fichier' ->
     'chemin'
   - combo-creer-agent : c8 (creer-fichier) : 'contenu' ajoute

**Resultats** : les 3 combos naviguent en dry-run rc=0 avec COMBO TERMINE et
les commandes generees correctes. test-003 passe de 20 echecs a 4 echecs
(seul combo-creer-agent KO car le TEST ne fournit pas la variable contenu
requise par creer-fichier).

**Lecons** :
1. Le CATALOGUE est la source de verite des commandes : les definitions-combo
   doivent utiliser les cles EXACTES du catalogue (jamais inventer des cles)
2. Un decalage catalogue/outil peut etre DANS LE CATALOGUE (modele incomplet
   ne refleter pas les vrais parametres de l outil) : verifier l interface
   reelle de l outil (add_argument / positionnels) avant de blamer les combos
3. detecter-decalages-catalogue confirme la conformite : copier-dossier et
   copier-fichier sont passes de decalage a CONFORME (114 conformes)
4. Les 2 decalages restants (generateurs-case-convertir, generateurs-ligne)
   sont des FAUX POSITIFS connus du detecteur (outils sans add_argument
   standard : options reelles []) - preexistants, hors perimetre
5. Le test-003 et le test-005 doivent etre adaptes par MORPHEUS :
   - test-003 : combo-creer-agent vars doivent inclure contenu (creer-fichier
     l exige)
   - test-005 : point 14 catalogue version 0.2.5 -> 0.2.6

**Tests attendus (Morpheus)** : test-003 (ajouter contenu aux vars de
combo-creer-agent), test-005 (version catalogue 0.2.6), non-regression
complete.
## [LECON] 2026-08-11 -- SPEC-COMBO-MOTEUR v0.2.1 : REGLE DES CLES EXACTES DU CATALOGUE

**Mission** : documenter dans la spec-combos-moteur que les entrees des cases
generateur doivent utiliser les cles exactes du catalogue de commandes.

**Ce qui a ete fait** :
1. Version spec 0.2.0-beta -> 0.2.1 (date 2026-08-11)
2. REGLE explicite ajoutee dans la section "Format de la definition" : les
   cles des entrees d'une case generateur = cles EXACTES des parametres de la
   commande ciblee dans catalogue-commandes.json (source de verite). Interdiction
   d'inventer une cle.
3. Pourquoi : le moteur appelle generateurs-commande --reponses "cle=valeur" ;
   une cle inconnue est ignoree, un parametre obligatoire manquant -> ERREUR
   'Parametre obligatoire manquant' qui fait echouer tout le combo (KO test-003)
4. Comment connaitre les cles : lire catalogue-commandes.json (champ parametres.cle),
   ou compter les questions du mode interactif ; les cles ne suivent AUCUNE
   convention universelle (fichier/chemin/source/destination/type/contenu) ->
   toujours verifier
5. Contre-exemple + bon exemple (valider-conventions : fichier (MAUVAIS) vs
   chemin (BON)) dans la section Format de la definition
6. Tableau des types de cases : colonne generateur mise a jour
7. Section Variables et interpolation : ajout de la REGLE v0.2.1 (valeur = var
   interpolee OU valeur en dur, mais CLE = nom exact d'un parametre du catalogue)
8. Table "Tests requis" : 2 nouveaux cas (cle hors catalogue -> ERREUR code 1 ;
   cles exactes -> commande composee correctement)

**Validations** : ASCII 0, CRLF 0, valider-conformite-ascii OK, structure
conservee (311 lignes). test-002-combos-moteur : reference la spec par chemin
(mention v0.1.0 contextuelle dans un commentaire, pas une verification de
version) -> aucun impact attendu.

**Lecons** :
1. La spec d'un outil appartient au proprietaire de l'outil (ici Vulcain pour
   combos-moteur) ; Promethee redige les specs du dossier pense-betes (trio
   projets futurs) - ne pas confondre les deux perimetres
2. Une lecon issue d'un KO doit etre REFLECTEE dans la spec de l'outil concerne
   pour qu'elle devienne une regle durable et relue par les agents (pas seulement
   une note dans corrections.md)
3. La regle des cles exactes du catalogue est transverse : elle concerne TOUTES
   les definitions-combo (combos creer-*, combo-tester-outil, etc.) - le
   detecteur-decalages-catalogue et les futurs combos doivent la respecter
## [LECON] 2026-08-11 -- GARDE-FOU CLES COMBOS VS CATALOGUE (Vulcain, moteur v0.3.0 + detecteur v0.1.1)

**Mission** : ajouter un garde-fou anti-recurrence du defaut test-003 : les
definitions-combo ne doivent jamais utiliser des cles d entrees inventees pour
les cases generateur.

**Ce qui a ete fait** :
1. SCAN PREALABLE : 8 ecarts reels trouves dans les 3 combos creer-* (cles
   dry_run x5 et recursive x2) - le garde-fou a servi IMMEDIATEMENT a sa
   creation en revelant les ecarts a corriger
2. COMBOS CORRIGES : 8 cles retirees (dry_run = cle morte car le moteur gere
   --dry-run globalement ; recursive = inutile pour des validations ciblant un
   fichier)
3. combos-moteur.py v0.2.0-beta -> v0.3.0 : nouvelle fonction
   valider_cles_generateurs(donnees) appelee au chargement APRES
   valider_definition : verifie (a) le catalogue cible existe, (b) chaque cle
   des entrees est un parametre exact du catalogue, (c) chaque parametre
   obligatoire est fourni. En cas d ecart -> ERREUR claire (combo, case, cles)
   code retour 1. Parite py/sh maintenue (le .sh embarque le code python).
4. detecter-decalages-catalogue.py v0.1.0 -> v0.1.1 : section COMBOS ajoutee
   au rapport (scan de combos/*/definition-combo.json, memes verifications) +
   synthese "COMBOS: X scannes, Y problemes"
5. Docs a jour (moteur v0.3.0 + garde-fou documente, detecteur v0.1.1)

**Validations** : py/sh parite v0.3.0, combo infeste detecte (rc=1, 2 erreurs)
dans py ET sh, 3 combos creer-* conformes, detecteur : 14 combos scannes 0
probleme, bash -n OK, py_compile OK, normes ASCII 0 + LF partout.

**Lecons** :
1. Un garde-fou de validation AU CHARGEMENT est plus fort qu un scan externe :
   le combo fautif echoue immediatement au lancement avec une erreur claire -
   le scan preventif (detecteur) complete pour detecter AVANT l usage
2. Les cles mortes s accumulent silencieusement dans les definitions (dry_run
   ajoute avant que le moteur ne gere --dry-run globalement) : un scan
   systematique des entrees vs catalogue doit etre lance regulierement
3. La parite py/sh d un outil qui embarque du python (heredoc) exige de
   synchroniser version ET logique dans les 2 blocs - le --version du .sh
   revele immediatement une desynchronisation
4. test-002 (combos-moteur) utilise des catalogues valides dans ses definitions
   de test : le nouveau garde-fou ne doit pas les casser (a verifier par
   Morpheus)

**Tests attendus (Morpheus)** : test-002 (garde-fou actif sur definitions de
test), test-003 (combos corriges), detecter-decalages-catalogue (section
COMBOS), non-regression complete.

## [LECON] 2026-08-11 -- OUTIL EDITER-FICHIER-AGENTS CREE (Vulcain, v0.1.0-beta)

**Contexte** : creation de l'outil editer-fichier-agents (editer ligne/bloc des fiches agents + correcteur ASCII integre) pour retirer les blocs "## Historique" obsoletes des 11 fiches.

**Lecons** :
1. Le gap reel : editer-fichier remplace un MOTIF texte, supprimer-ligne par NUMERO de ligne - aucun outil ne manipulait des BLOCS delimites par titre markdown (## X jusqu'au prochain ##) ni n'integrait l'ASCII. La valeur ajoutee est la fusion de ces 2 capacites.
2. Le correcteur ASCII reutilise le dictionnaire de corriger-dictionnaire-accents (lignes 'accent|remplacement') : meme mecanique que corriger-symboles - ne pas reimplementer.
3. Le separateur du generateur de commandes est ';' (PAS '|') pour --reponses : les tests de generation doivent utiliser 'cle=valeur;cle2=valeur2'.
4. Le detecteur detecter-decalages-catalogue peut etre long sur tout le projet : lancer avec --sortie et timeout suffisant, ou cibler.
5. Ajouter un outil au catalogue : entree triee (ordre alphabetique), bump de version mineure (0.2.6 -> 0.2.7), verifier tri + JSON + normes.
6. IMPACT TESTS : test-005 verifie la version catalogue (0.2.6) et test-007 le nombre de commandes (118) - tous deux cassent apres ajout d'une commande. DELEGATION DES TESTS : Morpheus adapte.
7. Les tests reels sur copie de test : suppression bloc Historique (dry + wet + backup), bloc inexistant -> ERREUR claire, ajout/remplacement/suppression de ligne, --ascii corrige accents+guillemets.

## [LECON] 2026-08-11 -- OUTIL VERIFIER-CONFORMITE-FICHE CREE (Vulcain, v0.1.0)

**Mission** : creer verifier-conformite-fiche (categorie verifier/) pour verifier la conformite des fiches agents au template fiche-agent-template.md. Decision utilisateur : OUTILLAGE D'ABORD + TEMPLATE PAR ROLE (la refonte viendra apres, mesuree par l'outil).

**Capacites** :
1. Cibles : --agent <nom> (1), --agents <a,b,c> (selection), --tous (11 fiches)
2. Verification par fiche : frontmatter YAML (--- debut + cle agent + cloture), sections '## X' du template presentes, sections specifiques agent TOLEREES mais signalees, ordre des sections
3. Sections du template lues DYNAMIQUEMENT (l'outil reste valide apres toute refonte du template)
4. --rapport <fichier.md>, --dry-run, --verbose

**Livrable** : rapport-impact-2026-08-11.md (conserve dans le dossier de l'outil) -- mesure initiale : 11/11 ECARTS.
- Toutes les fiches : ## Historique manquant (template obsolete -- supprime des fiches le 2026-08-11)
- Sections divergees : Vue d'ensemble 8/11, Forces et Faiblesses 3/11, Style de travail 5/11, Limites 8/11, WORKFLOW RVAV + UTILISATION manquantes sur cerberus
- Sections specifiques tolerees : cerberus (cycle/agents), janus (Verdicts), morpheus (tests), themis (rapport), vulcain (techno)

**Lecons** :
1. Le template est la SOURCE DE VERITE : ajouter une section = mettre a jour le template, l'outil verifie ensuite toutes les fiches (lecture dynamique des '## ')
2. Le frontmatter des fiches peut etre long (cloture > 30 lignes, ex buffy ligne 56) : chercher la cloture sur 100 lignes, pas 30
3. Distinguer SECTIONS MANQUANTES (ecarts) de SECTIONS SPECIFIQUES (tolerees -- le role de l'agent) : le rapport devient actionable pour la refonte par role
4. NE PAS corriger les fiches dans la mission outillage : le rapport mesure l'impact, la refonte est une mission separee
5. Test reel 3 modes : --agent (1), --agents (selection), --tous (11) + generation via catalogue -- la boucle est complete

**Outils utilises** : outil-template.py (modele), valider-nommage, valider-conformite-ascii, generateurs-commande (catalogue + generation), .zz- scripts temporaires

## [LECON] 2026-08-11 -- VERIFIER-CONFORMITE-FICHE v0.2.0 : MODE PAR ROLE (Vulcain)

**Mission** : etape 3 de la refonte par role -- enrichir verifier-conformite-fiche avec le mode noyau + variante.

**Capacites ajoutees (v0.1.0 -> v0.2.0)** :
1. Option --variante <cerveau-projet|trio> : verifie le noyau + les sections de la variante de famille
2. Famille determinee par : --variante > frontmatter de la fiche (cle 'famille:') > defaut par agent (FAMILLES_DEFAUT)
3. Sections de la variante manquantes = ECARTS (comme celles du noyau)
4. Sections specifiques (ni noyau ni variante) : TOLEREES mais signalees
5. Ordre verifie SEPAREMENT (noyau / variante) : les fiches peuvent intercaler leurs sections specifiques
6. Compatibilite ascendante : --agent buffy sans --variante fonctionne (famille auto)

**Tests reels** :
- buffy --variante cerveau-projet : CONFORME (noyau 8 + variante 2 presentes)
- minerve --variante trio : ECARTS avec 6 sections manquantes (a corriger etape 4)
- themis sans --variante : famille cerveau-projet par defaut, manquantes Forces/Style + specifiques rapport tole rees
- --tous : 2 CONFORME (buffy, clio) / 9 ECARTS -- le nouveau rapport d impact v020
- Catalogue v0.2.9 (parametre variante ajoute), generation reelle OK, doc v0.2.0, sh v0.2.0 parite

**Lecons** :
1. Le modele par role : 3 sources de famille (option > frontmatter > defaut) -- l'ordre de precedence doit etre documente et teste
2. L'ordre separe noyau/variante est indispensable : buffy a ses sections specifiques intercalees entre les sections du noyau (pas a la fin) -- exiger un ordre global casserait des fiches valides
3. Les sections des variantes sont des fichiers SEPARES avec leur propre frontmatter -- l'outil lit leurs '## ' directement
4. Compatibilite ascendante testee : le mode sans --variante doit continuer a fonctionner (famille auto par defaut par agent)
5. Rapport d impact v020 conserve : 2 CONFORME / 9 ECARTS = la liste exacte des corrections de l etape 4

**Outils utilises** : verifier-conformite-fiche (v0.2.0), generateurs-commande (catalogue v0.2.9), valider-conformite-ascii, valider-nommage, .zz- scripts temporaires
## [LECON] 2026-08-11 -- CONVENTION NOMMAGE ETENDUE cT* (Vulcain, v1.0.2)

**Mission** : etendre la convention de nommage des IDs de cases dans valider-case pour accepter les prefixes thematiques (format cT*) - la ligne trio de Janus utilise cT1..cT10.

**Constat** : valider-case v1.0.1 (regex `c<numero>[a-z]?`) signalait 10 erreurs NOMMAGE sur le parcours-janus v0.3.7 (cases cT1..cT10, creation deliberate avec prefixe T = Trio). Les tests test-021/018 passaient car ils utilisent valider-cartes-decision (structure), pas valider-case (nommage) - le bug etait invisible.

**Action** :
1. valider-case.py v1.0.2 : regex `^c[A-Z]?<numero>[a-z]*$` - un prefixe alpha MAJUSCULE optionnel avant le numero (cT6, cT10), suffixe lettres minuscules conserve (c12b, c29d). Message d erreur + aide mis a jour.
2. valider-case.md : convention documentee (prefixe thematique majuscule, ex: T = Trio) + version 1.0.2.

**Verification** : janus passe de NON CONFORME (10 NOMMAGE) a A ALLEGER (0 erreur). 11 parcours : 0 NOMMAGE partout. Normes 0/0, py_compile OK.

**Lecons** :
1. Une convention de nommage stricte devient un faux positif quand un usage legitime diverge : avant de renommer les donnees, verifier si la convention doit etre ETENDUE (decision utilisateur : garder cT*).
2. Le prefixe thematique MAJUSCULE est reserve aux lignes dediees (T = Trio) ; le suffixe lettre minuscule reste le mecanisme standard de derivation c<numero><lettre>.
3. Deux validateurs different (valider-cartes = structure, valider-case = nommage) : un nommage non conforme peut passer l un et casser l autre - toujours lancer valider-case en plus de valider-cartes-decision.
4. RELAIS : les 2 tests test-009/test-015 attendent la version v1.0.1 -> adaptation de tests releve de Morpheus (REGLE IMMUABLE DELEGATION).
## [LECON] 2026-08-11 -- SPEC-GUIDER-PARCOURS v0.6.2 : REGLE 11 NOMMAGE DES IDS ETENDUE cT* (Vulcain)

**Contexte** : l'extension de la convention de nommage (valider-case v1.0.2 : c[<prefixe-alpha-maj>]<numero>[a-z]?, prefixe thematique majuscule optionnel cT* pour la ligne Trio de Janus) n'etait documentee NI dans la spec-guider-parcours (section Regles du format : aucune mention nommage) NI dans un pattern. Les agents ne pouvaient pas connaitre la convention depuis la source de verite du format.

**Lecon** :
1. Toute convention de format (nommage, structure, type) doit etre documentee dans la SPEC du format, pas seulement dans l'outil qui la valide (valider-case). La spec-guider-parcours est la source de verite du format des cartes : une convention non documentee = invisible pour les agents et pour les futurs generateurs.
2. La section "Regles du format" de la spec avait deja 10 regles (9 = Question Honnete c0, 10 = pas de boucle d'attente) : la nouvelle regle de nommage est la 11. Toujours verifier la numerotation existante avant d'inserer.
3. Bump de version coherent sur 3 endroits (titre ligne 7, **Version** ligne 9, Historique ligne 13) + 2 references documentaires qui pointent vers l'ancienne version (guider-parcours.md et vulcain.md) -- le test-014 verifie ces 5 points (1a, 1b, 6a, 6b) : un bump de version de spec IMPLIQUE une adaptation du test-014 par Morpheus (REGLE IMMUABLE DELEGATION).
4. La regle 11 doit citer valider-case v1.0.2 comme source de verite (regex exacte + message NOMMAGE) pour que la convention soit executable (verifiable par l'outil), pas seulement descriptive.
## [LECON] 2026-08-11 -- GENERATEURS DE CASES ALIGNES SUR LA CONVENTION ETENDUE cT* (Vulcain)

**Contexte** : la convention de nommage etendue cT* (valider-case v1.0.2, spec-guider-parcours v0.6.2 regle 11) n'etait documentee ni dans generateurs-ligne.md (qui citait seulement c<numero>[a-z]?) ni dans generateurs-case.md (aucune mention). Les 2 generateurs de cases etaient les derniers outils a ne pas etre alignes.

**Lecon** :
1. L'alignement documentaire d'une convention doit couvrir TOUS les outils qui la manipulent, pas seulement le validateur et la spec : generateurs-case et generateurs-ligne generent des ids de cases -> leurs .md doivent citer la convention etendue.
2. generateurs-ligne.md : etendre la phrase existante (c<numero>[a-z]? -> c[<prefixe-alpha-maj>]<numero>[a-z]? avec cT1..cT10) ; generateurs-case.md : ajouter la mention dans la section Pourquoi cet outil (absente avant) + la precision que l'edition d'une case existante conserve son id.
3. Bump de version DOCUMENTAIRE du .md (0.3.0 -> 0.3.1, 0.4.0 -> 0.4.1) SANS toucher au --version des scripts py/sh (la parite test-010/test-017 verifie les versions des scripts, pas celle du .md) : verifie en reel, les 2 tests restent 0 KO.
4. Le fait qu'aucun test ne verifie le contenu des .md d'outils est une lacune connue : la conformite documentaire repose sur l'audit (Themis) et le protocole-sante, pas sur la non-regression.
## [LECON] 2026-08-11 -- E1/E2/E3 CORRIGES : generateurs-ligne ENTIEREMENT ALIGNE SUR LA CONVENTION ETENDUE cT* (Vulcain)

**Contexte** : l'audit Themis de la convention cT* (VERDICT A REVOIR, mineur) avait releve 3 ecarts documentaires dans la famille generateurs-ligne : generateurs-ligne.md:197, spec-generateurs-ligne (93/126/153/169) et generateurs-ligne.py (275/419-422/460) citaient encore l'ancienne convention c<numero>[a-z]? sans l'extension cT*.

**Lecon** :
1. Une correction de convention doit couvrir le .md, la SPEC ET les commentaires du code : l'audit Themis avait trouve les 8 mentions dans les 3 fichiers satellites pendant que le .md principal etait deja aligne.
2. La bonne formulation : citer la convention ETENDUE une fois dans la phrase (c[<prefixe-alpha-maj>]<numero>[a-z]?, valider-case v1.0.2) puis mentionner le cas normal c<numero>[a-z]? comme PARTIE de cette convention -- c'est ce qui rend le scan anti-recurrence non-ambigue.
3. Le re-scan naif ligne-par-ligne genere des faux positifs sur les mentions du cas normal quand la convention etendue est citee a la ligne precedente de la meme phrase : verifier le CONTEXTE (fenetre +/- 2 lignes) avant de conclure.
4. Resultats : 8/8 mentions alignees, compile py OK, tests 010/017 0 KO, normes 0/0 -- aucun impact fonctionnel (commentaires uniquement).
## [LECON] 2026-08-11 -- GARDE-FOU ANTI-RECURRENCE detecter-convention-nommage v0.1.0 CREE (Vulcain)

**Contexte** : creation de l'outil qui scanne les .md/.py/.sh pour detecter les mentions de la convention c<numero>[a-z]? HORS contexte etendu cT* (recommandation Themis, audit 2026-08-11).

**Lecon** :
1. La methode CONTEXTE validee par Themis s'implante bien : fenetre +/- 2 lignes, mention conforme si c[<prefixe-alpha-maj>] ou cT1..cT10 (forme complete) OU cT* (forme abregee) est dans la fenetre.
2. EXCLUSIONS NECESSAIRES pour eviter les faux positifs : corrections.md (lecons historiques), tests/ (verifient les ids GENERES), rapports/ + rapport-audit-* (documentent l'HISTORIQUE des ecarts). Sans elles, l'outil signale ses propres rapports d'audit et son propre .md.
3. --aide doit etre un ALIAS d'argparse (add_argument action="help"), sinon l'outil echoue a --aide alors que --help marche.
4. L'outil a DECOUVERT un ecart reel que l'audit Themis n'avait pas vu : docs-dev-cerveau-projet/spec-refonte-cartes-decision.001.01.ebauche.md:175 ("nommage des cases (c<numero>[a-z]?)" sans cT*) -- preuve que le garde-fou automatique va plus loin que l'audit cible. A traiter separement.
5. L'ajout au catalogue (139 commandes) casse le test-007 qui attend 138 : l'adaptation du test releve de Morpheus (REGLE IMMUABLE DELEGATION) -- signale dans la reactivation.
6. L'index-tools doit etre mis a jour a la creation d'un outil (ordre alphabetique) ; les non-ASCII preexistants (ligne generateurs-carte) ne sont PAS a corriger dans cette mission (hors perimetre, a signaler seulement).
## [LECON] 2026-08-11 -- NON-ASCII PREEXISTANT DE index-tools.md CORRIGE (ligne generateurs-carte) (Vulcain)

**Contexte** : correction du non-ASCII preexistant signale lors de la creation de detecter-convention-nommage.

**Correction** : ligne 165, caractere U+00EE ('i' accentue) dans 'nait CONFORME' remplace par 'i' ASCII (1 remplacement).

**Verifications reelles** :
1. non-ASCII : 1 -> 0 dans index-tools.md
2. CRLF : 0 (LF pur, 441 lignes)
3. Integrite de la table intacte : Total 110, Corriger 6, entree detecter-convention-nommage et generateurs-carte presentes

**Lecons** :
1. Le second non-ASCII signale precedemment n'existait plus : un seul etait reel (ligne generateurs-carte) -- toujours re-scanner au moment de corriger (pas de correction aveugle sur un constat ancien).
2. Correction ciblee d'un caractere (replace U+00EE -> i) plus sure qu'une reecriture de ligne entiere.
3. Apres toute correction d'un fichier d'index, verifier l'integrite des totaux et entrees referencees (le fichier est controle par test-007).
## [LECON] 2026-08-11 -- TRI DU CATALOGUE REPARE : detecter-convention-nommage replace a sa position alphabetique (Vulcain)

**Contexte** : lors de la creation de detecter-convention-nommage, l'entree avait ete inseree en FIN de liste du catalogue generateurs-commande (position 138) au lieu de sa position alphabetique, cassant le tri (noms != sorted(noms)). Le test-007 (point 13 : len == 139 ET tri) l'a detecte.

**Correction** : entree deplacee de la position 138 vers la position 35 (avant detecter-decalages-catalogue : convention < decalages). Format preserve exactement (json.dumps indent=2 + LF final, verifie par garde-fou round-trip avant ecriture).

**Verifications reelles** :
1. len 139 conserve, noms == sorted(noms) -> True
2. test-007 : 0 KO (vert)
3. Non-regression complete : 21/21 OK
4. Normes catalogue : 0 non-ASCII, 0 CRLF, JSON valide

**Lecons** :
1. TOUTE insertion dans le catalogue generateurs-commande doit respecter l'ordre alphabetique des noms (le test-007 le verifie) -- inserer l'entree a la bonne position, jamais en fin de liste.
2. Apres toute modification du catalogue, lancer le test-007 avant de reactiver (garde-fou immediat, pas d'attente du controle).
3. Verifier le format du fichier avant reecriture (round-trip indent=2 + LF) pour ne pas creer un diff parasite.

## [LECON] 2026-08-11 -- BUDGET PONDERE DES INDICES IMPLEMENTE (valider-case v1.1.0 + generateurs-case v0.4.2) (Vulcain)

**Mission** : rendre les cartes plus flexibles sur le NOMBRE d'indices par case en ponderant leur taille (decision utilisateur : 2 indices courts = 1 indice long).

**Modele implemente** :
- Indice COURT (texte <= 100 car. ou sans texte) = poids 0,5
- Indice LONG (texte > 100 car.) = poids 1
- Budget par case = 3,0 unites (poids total)
- Plafond absolu 160 car. par texte INCHANGE et independant
- Effet : 6 courts (3,0) OK, 3 longs (3,0) OK, 2 longs + 2 courts (3,0) OK, 4 longs (4,0) signale

**Fichiers modifies** :
1. valider-case.py v1.0.2 -> v1.1.0 : constantes SEUIL_COURT=100 + BUDGET_INDICES=3.0 + fonction poids_indices() + 2 emplacements de verification (verifier_allegement + boucle principale)
2. generateurs-case.py v0.4.0 -> v0.4.2 : meme fonction poids_indices + bloc de surcharge (etape 3 conversion)
3. spec-valider-case v1.1.0 : section 3 documentee (budget pondere)
4. spec-guider-parcours : section PRINCIPE UNE PLACE mise a jour (<= 100 car. + budget 3,0)
5. generateurs-case.md v0.4.2 : version + ligne surcharge
6. valider-case.md v1.1.0 : version + historique
7. Catalogue generateurs-commande : generateurs-case 0.4.0 -> 0.4.2
8. Tests : test-009 (23 points, + cas 3f/3g : 6 courts CONFORME / 4 longs A ALLEGER), test-010 (v0.4.2), test-015 (v1.1.0)

**Lecons** :
1. La regle binaire '3 indices' penalisait les cases avec beaucoup de rappels courts (c6/c14 de Cerberus) - le budget pondere donne de la flexibilite sans perdre le garde-fou anti-surcharge
2. Les tests temoins doivent partir d'un parcours MINIMAL sans indices (ajouter 6 courts a une case de cerberus deja chargee depassait le budget)
3. Parite py/sh maintenue : valider-case.sh et generateurs-case.sh sont des wrappers purs (pas de logique a dupliquer)

**Verifications** : test-009 23/23, test-010 25/25, test-015 10/10, non-regression complete 21/21 OK, 0 non-ASCII, 0 CRLF.

## [LECON] 2026-08-11 -- VALIDER-CASE.MD ALIGNE SUR LE BUDGET PONDERE (Vulcain)

**Mission** : corriger l'ancienne regle dans le .md de valider-case (alignement doc outil avec les specs).
**Resultat** : ligne 55 (tableau Allegement) corrigee : "> 3 indices OU texte > 160" -> budget pondere (COURT <= 100 car. = 0,5 / LONG > 100 = 1 / budget 3,0 / plafond 160). Scan des .md d'outils : valider-case.md etait le SEUL avec l'ancienne regle.
**Lecons** :
1. Le .md d'un outil peut contenir l'ancienne regle alors que son PROPRE historique documente deja le nouveau modele : verifier TOUTES les sections du .md (ligne 13 historique OK, ligne 55 tableau Allegement stale).
2. Le scan complet (grep "> 3 indices" sur tous les .md de tools/) confirme qu'il ne reste AUCUN .md d'outil avec l'ancienne regle : le budget pondere est desormais documente partout (3 specs + .md valider-case).
3. guider-parcours.md v0.5.0 ne documente pas la surcharge (doc d usage du navigateur) : c'est CORRECT, la surcharge est du domaine de valider-case. Ne pas ajouter de contenu hors sujet.
4. La correction documentaire d'un .md ne casse pas les tests (test-009 23/23, test-015 10/10, non-regression 22/22) : le .md n'est pas verifie par les tests, mais confirmer quand meme.
5. Les specs et les .md d'outils doivent rester synchronises : la chaine spec -> .md -> test -> controle (Janus) garantit l'absence de residue.

## [LECON] 2026-08-11 -- COMMENTAIRE STALE BUDGET PONDERE CORRIGE DANS VALIDER-CASE.PY (Vulcain)

L en-tete (docstring) de valider-case.py decrivait encore l ANCIENNE regle de
surcharge ("> 3 indices ou texte > 160 caracteres") alors que le code
(SEUIL_COURT = 100 / BUDGET_INDICES = 3.0 / SEUIL_TEXTE = 160) implemente le
budget pondere depuis v1.1.0. Ecart detecte par le test reel du nouveau grep
croise E7 du protocole-verification-coherence v0.2.0 (les 6 fichiers couverts
doivent porter les 5 seuils 100/0,5/1/3,0/160 et AUCUNE trace de l ancienne
regle).

Correction : docstring aligne sur le budget pondere (indice COURT <= 100 car. =
0,5 unite, LONG > 100 = 1 unite, budget 3,0 par case, texte > 160 car. =
SIGNALEE). Scan complet : c etait la SEULE occurrence dans les 6 fichiers.

Lecons :
1. Apres un changement de regle dans le code, verifier AUSSI le docstring/en-tete
   du fichier .py (pas seulement le .md et la spec) -- le grep croise E7 couvre
   desormais les 6 fichiers.
2. Le protocole-verification-coherence v0.2.0 (E7) est un garde-fou operationnel :
   il a detecte un ecat reel des sa premiere utilisation reelle.
3. Tests reverdis : test-009 (23/23), test-015 (10/10), test-022 (14/14),
   non-regression complete 22/22 OK.

## [LECON] 2026-08-11 -- REGISTRE D USAGE DES OUTILS CREE (enregistrer-usage-outil v0.1.0) (Vulcain)

Creation de l outil enregistrer-usage-outil + registre JSONL
(cerveau-projet/agents/traces/registre-usages-outils.jsonl) + integration
de la journalisation automatique dans generateurs-commande v0.2.3.

Ce qui a ete fait :
- enregistrer-usage-outil.py/.sh/.md/spec : append JSONL (date, agent, outil,
  mode generateur|direct|combo, commande, contexte). --dry-run. Ne VALIDE PAS
  l outil (on enregistre l usage reel : c est ce qui permet de detecter les
  commandes en dur ou les outils hors catalogue).
- generateurs-commande v0.2.3 : journalise automatiquement chaque commande
  generee (mode generateur) apres composer_commande. --agent optionnel
  (defaut : agent actif lu dans AGENTS.md bloc session-llm-1), --no-journal
  pour desactiver. Discret (stderr, jamais bloquant).
- Catalogue : 141 -> 142 commandes. index-tools : categorie Enregistrer +1,
  total 110 -> 111. test-007 mis a jour (15/15).

Lecons :
1. BUG CORRIGE : registre_defaut() remontait 4 niveaux au lieu de 3 (outil
   dans tools/enregistrer/enregistrer-usage-outil/ -> agents/ = 3 remontees).
2. BUG CORRIGE : _lire_agent_actif() coupait le bloc session-llm-1 sur le
   premier "---" qui est le SEPARATEUR du tableau markdown (|---|---|) ->
   couper sur "\n---" (fin de bloc) pour lire la ligne "Nom Agent".
3. Le generateur compose la commande mais ne l execute pas : la journalisation
   se fait a la composition (modele + parametres connus), avant le return.
4. KO PREEXISTANT A TRAITER PAR MORPHEUS : test-005 attend la version v0.2.2
   du generateur (modif preexistante non commitee) -> doit passer en v0.2.3.
## [LECON] 2026-08-11 -- COMBOS-MOTEUR v0.3.1 : OPTION --no-journal PROPAGEE AU GENERATEUR (Vulcain)

**Contexte** : le registre d usage des outils (source de verite) etait pollue par les
tests qui passent par le generateur (88-150 lignes de test). Le combos-moteur appelait
generateurs-commande sans moyen de desactiver la journalisation.

**Modifications** (combos-moteur.py + .sh + .md + spec) :
1. VERSION 0.3.0 -> 0.3.1 (py + sh en parite).
2. Nouvelle option `--no-journal` (argparse py + parser manuel sh + aide + spec).
3. Propagation : main -> executer() -> executer_case_generateur() : si no_journal,
   `--no-journal` est ajoute a la commande du generateur (py ET sh).
4. Piege evite : le .sh duplique TOUTE la logique par heredoc python -> il fallait
   appliquer les 5 memes modifications dans le heredoc, sinon desynchronisation py/sh.
5. Piege evite : variable no_journal initialisee a False dans le main du .sh (sinon
   NameError quand --no-journal absent).

**Tests reels** : --no-journal py = 0 ligne ajoutee ; sans = 1 ligne ajoutee ;
--no-journal sh = 0 ligne ajoutee. Non-regression 23/23 OK.

**Lecon** : quand on ajoute une option a un outil py, TOUJOURS verifier le .sh :
s'il embarque la logique par heredoc, il faut reporter la modification (parite py/sh).

## [LECON] 2026-08-11 -- 3 OUTILS ANTI-SCRIPTS-TEMPORAIRES + REGISTRE ENRICHIT (Vulcain)

**Contexte** : l'utilisateur a constate que les agents preferent les scripts temporaires jetables (.zz-*/.tmp-*) a nos outils. Diagnostic : le registre d usage est a 0 ligne (les scripts ne passent pas par le generateur), 4 categories de scripts (transformation parcours JSON = TROU, non-regression = TROU, controles croises = combos partiels, remplacements texte = outils ignores).

**Outils crees (3)** :
1. **lancer-non-regression** (tester/) : lance tous les tests test-0XX, bilan OK/KO fiable (regex [KO]), registre protege (--no-journal par defaut, purge avant + verifie 0 apres). Teste en reel : 3 tests cibles OK, registre 0.
2. **editer-parcours** (editer/) : insertion/retrait de case avec re-pointage automatique des suivant/branches, modification branche/suivant, bump version. Dry-run par defaut, backup .bak, JSON/LF/ASCII preserves. Teste en reel : dry-run ne modifie pas, wet modifie (version 0.4.1->0.4.2->0.4.3 puis restauree a 0.4.1).
3. **detecter-usage-scripts-temporaires** (detecter/) : scan racine (.zz-*/.tmp-*), git log (--diff-filter=A), lecons/corrections, croise avec le registre (mode script-temporaire) -> ecart = scripts non declares. Teste en reel : 10 scripts detectes non declares (verdict ECART DETECTE).

**Registre enrichi** : enregistrer-usage-outil v0.1.0 -> v0.2.0, nouveau mode "script-temporaire" (choix ajoute) pour DECLARER la creation d'un script temporaire. Cette declaration alimente le croisement de detecter-usage-scripts-temporaires.

**Catalogue + index** : catalogue 142 -> 145 commandes (3 ajoutees, triees), index-tools mis a jour (4 lignes : les 3 nouveaux + editer-fichier-agents qui manquait).

**LE CONS** :
1. TESTER chaque outil en reel (--version, dry-run, cas reel) avant de le declarer fonctionnel.
2. Le dry-run d'editer-parcours ne modifie rien ; le wet modifie reellement (faire attention a restaurer apres les tests).
3. Les scripts temporaires sont DETECTABLES : racine + git log + lecons. Le registre seul ne suffit pas (il ne capture que ce qui passe par le generateur).
4. Toujours verifier que l'index-tools contient les nouveaux outils (editer-fichier-agents manquait depuis sa creation - trou a combler).

## [LECON] 2026-08-12 -- NETTOYER-SESSIONS v0.1.2 : EN-TETE ## Sessions LLM PRESERVE (bug sidentifier casse)

**Contexte** : au nettoyage de session du 2026-08-12, sidentifier a echoue ('Section ## Sessions LLM introuvable dans AGENTS.md') : nettoyer-sessions supprimait l'EN-TETE de section ## Sessions LLM alors que le perimetre documente (etats actifs = blocs session-llm + table Sessions connues) ne le prevoit pas. Le nettoyage rendait la re-identification impossible.

**Correction** : SECTIONS_A_SUPPRIMER ne contient plus que '## Sessions connues' ; l'en-tete '## Sessions LLM' est PRESERVE, seuls les blocs '### Session : session-llm-N' (titre + contenu) sont supprimes. Parite py/sh (logique du heredoc du .sh alignee), doc .md a jour, bump 0.1.1 -> 0.1.2.

**Tests reels (sur copies, AUCUN fichier de test touche)** : py_compile + bash -n OK ; --version py/sh 0.1.2 ; nettoyage sur copie (18 lignes) : blocs session 0 restant, EN-TETE conserve (1), Sessions connues 0, profil-session 0, frontmatter preserve ; INTEGRATION : sidentifier sur la copie nettoyee recreer le bloc session (le bug etait invisible sans cette etape) ; parite py/sh fichiers + sorties identiques.

**Lecons** :
1. PERIMETRE vs IMPLEMENTATION : le code supprimait l'en-tete de section (un etat structurel) alors que le perimetre documente est 'etats actifs uniquement' -- verifier que l'implementation colle au perimetre documente, pas seulement aux tests existants.
2. TEST D'INTEGRATION indispensable : le bug ne se voyait qu'a la re-identification (nettoyage PUIS sidentifier) -- un test unitaire de nettoyage seul ne suffit pas.
3. Les tests figent le comportement : le test-001 verifiait l'ANCIEN comportement ('## Sessions LLM supprimee' = 0) -- quand comportement documente et test divergent, c'est le test qui fige l'erreur. Morpheus inversera l'assertion 4b et creera le garde-fou test-025 (boucle complete nettoyage -> sidentifier sur copies).

## [LECON] 2026-08-12 -- DETECTER-CABLAGES-MANQUANTS v0.1.1 FINALISE + ORPHELINES CLIO CORRIGEES (Vulcain)

**Contexte** : reprise (decision utilisateur) de la mission detecter-cablages-manquants purgee par le nettoyage de session. Le .py v0.1.0 existait deja (code complet des 5 detections) mais sans doc, sans catalogue, sans index, sans tests. La reprise a aussi revele un bug reel latent : 3 CAS_ORPHELINE dans parcours-clio.

**Actions** :
1. OUTIL FINALISE : doc .md creee (modele detecter-usage-scripts-temporaires), bump 0.1.0 -> 0.1.1, entree catalogue generateurs-commande ajoutee a la main (145 -> 146, modele --tous, tri alphabetique respecte) car regenerer-catalogue est BLOQUE par une erreur pre-existante (generateurs-ligne : cles dupliquees branche/mode/source - a signaler a Morpheus/Janus), entree index-tools (Detecter 9 -> 10, Total 111 -> 115), badge README 126 -> 127.
2. ORPHELINES CLIO CORRIGEES : c6/c6a/c7/c8 = vestiges de l'ancien flux manuel (avant les combos maj-readme), c6a etait une case VIDE {}. Retrait via editer-parcours (0 pointeur vers chacune) + bump parcours-clio 0.5.2 -> 0.5.3 + fiche clio.md Pattern 14 a jour. valider-case CONFORME + valider-cartes-decision --tous 11/11 CONFORME.
3. TESTS REELS : --tous = 0 probleme bloquant sur 11 parcours (8 boucles de re-travail = cycles AVEC sortie, voulues : cerberus c15b->c15c rapport Janus, themis c3->c8->c8b flux d evaluation) ; bug simule sur copie (cas orpheline + ref morte + boucle indirecte z1->z2 SANS sortie dans le graphe atteignable) = detection 100% ; --version v0.1.1 ; --rapport markdown fonctionnel.

**Lecons** :
1. UNE MISSION PURGEE PEUT ETRE REPRISE SANS PERTE : le travail sur disque (.py) etait a 85% - l'evaluation avant abandon (compile + --version + scan reel) a montre que la reprise etait presque gratuite. TOUJOURS evaluer le fichier avant de trancher abandon.
2. L OUTIL REVELE DES BUGS DES SA PREMIERE EXECUTION : le scan --tous a decouvert les orphelines clio (invisibles pour valider-case qui ne verifie que les fins) - c est la preuve de sa valeur, pas un obstacle.
3. RETRAIT DE CASE VESTIGE : verifier d abord que PERSONNE ne pointe vers la case (editer-parcours affiche le nombre de pointeurs), et que le contenu n est pas une instruction unique perdue (c6/c7/c8 etaient remplacees par les combos, c6a etait vide).
4. REGENERER-CATALOGUE BLOQUE : le garde-fou des cles dupliquees (generateurs-ligne) empeche toute regeneration - ajout manuel trie requis en attendant la correction pre-existante.

## [LECON] 2026-08-12 -- GENERATEURS-LIGNE CATALOGUE : DOUBLON DE PARAMETRES CORRIGE + REGENERER-CATALOGUE DEBLOQUE (Vulcain)

**Contexte** : le garde-fou de regenerer-catalogue refusait toute regeneration ('ERREUR generateurs-ligne cles dupliquees: branche, mode, source'). Decouvert lors de la mission detecter-cablages-manquants (entree catalogue ajoutee a la main), reporte au rapport Janus, puis corrige dans cette mission (lecon Cerberus c15b/c15c : activer immediatement l agent habilite).

**Diagnostic** : l entree generateurs-ligne de catalogue-commandes.json (146 commandes) contenait un bloc de parametres DUPLIQUE : source/mode/branche apparaissaient DEUX FOIS a la suite (index 8/9/10 identiques a 11/12/13, dont un 'mode' avec defaut "" au lieu de "complet"). Le garde-fou de regenerer-catalogue scanne les cles dupliquees dans les parametres et REFUSE d ecrire.

**Correction** : retrait du bloc duplique (16 parametres -> 13) via editer-fichier avec une ancre unique (le 'defaut': "complet" du premier mode). Scan complet du catalogue : 0 doublon restant sur les 146 entrees.

**Verifications** : regenerer-catalogue --dry-run = 'GARDE-FOU : 0 cle dupliquee (OK)' + 0 a ajouter ; regeneration reelle sur copie = APPLIQUE 0 outil + copie IDENTIQUE a l original ; generateurs-commande --commande generateurs-ligne compose toujours la commande correctement. POINT ANNEXE : combos-analyse-projet a revele que le badge README 127 que j avais pose etait FAUX (realite 126) - le badge Shields Outils-121 etait l ecart reel (corrige a 126) + categorie enregistrer absente de la table README (ajoutee). Verdict final : README A JOUR (0 ecart).

**Lecons** :
1. UN GARDE-FOU DE REGENERATION EST UNE BONNE CHOSE : il a empeche d ecraser le catalogue avec des cles dupliquees. Le blocage n etait pas un bug de l outil mais une donnee fautive du catalogue - scanner TOUTES les entrees, pas seulement la signalee.
2. L ANCRE D EDITION DOIT ETRE UNIQUE : le 'defaut': "complet" (premier bloc) vs 'defaut': "" (second) a permis de cibler le doublon sans ambiguite.
3. VERIFIER LA REALITE AVANT DE CORRIGER UN COMPTEUR : j avais mis le badge README a 127 alors que la realite etait 126 - la source de verite est combos-analyse-projet, pas ma supposition. Un badge 'reecrit' n est pas forcement une concurrence : c etait la bonne valeur.
## [LECON] 2026-08-12 -- QUALITE PRO DES OUTILS D EDITION (Vulcain)

**Contexte** : demande utilisateur : nos outils doivent etre professionnels, l agent fournit le QUOI et l outil fait le COMMENT (indentation, cas limites, validation). Les 5 outils d edition texte etaient trop simples : echec silencieux (return 0 meme quand rien n est modifie), indentation exacte exigee de l agent, ciblage par numero de ligne, normes disparates.

**Corrections (v0.3.0 sauf remplacer-texte 0.2.0)** :
1. editer-fichier : 0 occurrence -> return 1 (echec explicite, jamais 0 silencieux) + protection nommage.
2. inserer-contenu-fichier : ciblage par CONTENU --apres <motif> (l agent n a plus a compter les lignes) + --indent (indentation auto alignee sur la ligne cible) + echec explicite si motif introuvable.
3. ajouter-contenu-fichier : --backup.
4. remplacer-texte : protection nommage + echec explicite si aucune paire ne matche.
5. supprimer-ligne : ligne inexistante -> return 1 + protection nommage + --backup.

**Tests reels** : les 5 outils compilent, echecs explicites prouves (exit 1), indentation auto prouvee (bloc aligne sur 2 espaces), retrocompat argparse conservee (parcours/combos/catalogue intacts).

**Lecons** :
1. L ECHEC SILENCIEUX EST LE PIRE DEFAUT D UN OUTIL : un return 0 mensonger fait croire a l agent que l edition a eu lieu. Tout outil doit retourner un code non nul quand il n a rien pu faire.
2. CIBLER PAR CONTENU, PAS PAR NUMERO : l agent connait le motif (le QUOI), pas le numero de ligne (le COMMENT). --apres <motif> + indentation auto = l outil fait le travail.
3. UNE VISION UTILISATEUR : l outil professionnel est celui qui absorbe la complexite (indentation, localisation, validation) pour que l agent ne fournisse que l intention.
## [LECON] 2026-08-12 -- QUALITE PRO EXTENSION AUX 5 OUTILS FICHIERS (Vulcain)

**Contexte** : extension de la qualite pro aux 5 outils fichiers de base (creer-fichier, supprimer-fichier, deplacer-fichier, lire-fichier, ecrire-fichier) apres la chaine precedente sur les outils d edition.

**Corrections (tous en 0.3.0)** :
1. supprimer-fichier : fichier inexistant -> return 1 (echec explicite, avant: return 0 silencieux) + protection nommage + --backup.
2. deplacer-fichier : destination existante -> REFUS (code 1) sauf --forcer + --backup avant ecrasement (avant: ecrasement silencieux).
3. creer-fichier : --backup avant ecrasement (--forcer), promotion prepare.
4. lire-fichier + ecrire-fichier : homogeneisation version 0.3.0 + promotion prepare.

**Tests reels** : 5/5 compilent, echecs explicites prouves (creer existant->1, supprimer absent->1, deplacer dest existe->1, lire absent->1), nominaux->0, backup crees, normes 0/0, retrocompat parcours/combos/catalogue conservee.

**Lecons** :
1. L ECRASEMENT SILENCIEUX EST AUSSI GRAVE QUE L ECHEC SILENCIEUX : deplacer-fichier ecrasait une destination existante sans rien dire - desormais refus explicite + --forcer/--backup.
2. LA QUALITE PRO EST UNE FAMILLE, PAS UN CAS PAR CAS : chaque vague d outils (edition puis fichiers) homogeneise les memes principes (echec explicite, protection nommage, --backup, ASCII/LF). Le modele est stable, il suffit de l appliquer.
3. RETROCOMPAT = SECURITE : les interfaces argparse conservees font que les parcours/combos/catalogue n ont pas change - la qualite monte sans rien casser.
## [LECON] 2026-08-12 -- ROUND 2 PERFORMANCE : 3 GOULOTS MESURES ET CORRIGES (Vulcain)

**Contexte** : 2e round qualite pro sur le theme PERFORMANCE. Mesure reelle avant de corriger (jamais d optimisation aveugle).

**Goulots et corrections** :
1. remplacer-texte.sh : 8.5s vs .py 0.16s (54x) car la boucle bash lanchait python3 PAR PAIRE x PAR FICHIER (2 paires x 30 fichiers = 60 process). Correction : delegation a UN SEUL appel python3 (le .sh appelle le .py du meme dossier). Resultat : 0.55s (15x), parite py/sh par construction, echec explicite conserve.
2. lire-fichier.py : --lignes 5 chargeait TOUT le fichier (read().split) - 0.18s sur 200k lignes. Correction : lecture paresseuse (iteration ligne par ligne + arret precoce). Memoire minimale, plus de chargement integral inutile.
3. editer-fichier.py : double scan (contenu.count puis contenu.replace). Correction : test d existence puis replace(1) - une seule passe.

**Lecons** :
1. MESURER AVANT D OPTIMISER : le goulot n 1 (54x) etait invisible sans benchmark - la confiance dans un .sh qui fonctionne peut cacher un massacre de performance.
2. LES PROCESS MULTIPLES DANS UNE BOUCLE SONT LE PIRE ENNEMI : chaque lancement python3 coute ~50ms de demarrage. 60 lancements = 3s+ de pur gaspillage. Un seul process par fichier (ou par tache) est la regle.
3. LA LECTURE PARESSEUSE EST UNE VERTU : ne charger que ce qui est demande (--lignes 5 = 5 lignes, pas 200k). Le chargement integral est un cout cache permanent.
4. LA PARITE PAR DELEGATION : le .sh qui appelle le .py du meme dossier garantit comportement ET performance identiques - mieux qu une reimplementation bash fragile.

## [LECON] 2026-08-12 -- ROUND 3 SECURITE : ENCODAGES, SYMLINKS, CHEMINS NON SURS (Vulcain)

**Contexte** : 3e round qualite pro sur le theme SECURITE. Diagnostic reel avant correction (jamais de securite par opinion).

**Failles detectees par le diagnostic** :
1. ENCODAGES : lire-fichier CRASHAIT avec traceback sur BOM UTF-8, fichier latin-1 et octets invalides - cause racine double : (a) print() vers une console cp1252 sous Windows (UnicodeEncodeError), (b) BOM non nettoye + errors=replace produisant des U+FFFD non encodables en cp1252.
2. OCTET NUL : un chemin contenant   levait ValueError embedded null character non gere (traceback).
3. SYMLINK : non testable sur ce systeme (WinError 1314) mais les outils d ecriture ecriraient a travers le lien vers la cible a l insu de l agent.

**Corrections (9 outils)** :
1. stdout force en UTF-8 (sys.stdout.reconfigure errors=replace, protege par try AttributeError) dans les 9 outils.
2. lecture robuste : utf-8-sig (BOM nettoye) puis fallback latin-1 - plus jamais de crash d encodage (lire, editer, inserer, supprimer-ligne, remplacer).
3. garde-fou octet nul : tout chemin contenant   refuse avec message explicite (exit 1) dans les 9 outils.
4. garde-fou symlink : outils d ECRITURE refusent les liens (ecrire, editer, creer, deplacer source+dest, inserer, supprimer-ligne, remplacer ignore les liens) ; lire et supprimer peuvent traverser (lecture seule / os.remove ne touche que le lien).
5. backup binaire (shutil.copy2) dans ecrire-fichier (une copie texte corrompait les fichiers latin-1).

**Bug de parcours** : le bloc sys.stdout.reconfigure doit etre APRES les imports (NameError sinon) - j ai du le deplacer dans creer-fichier et deplacer-fichier.

**Tests reels** : 29/29 verts - BOM/latin-1/octets invalides sans crash, octet nul refuse partout (6 outils, exit 1, message propre), comportements nominaux conserves (echecs explicites inclus). Normes 0/0 sur 27 fichiers. Spec remplacer-texte realignee 0.3.1.

## [LECON] 2026-08-12 -- ROUND 4 ROBUSTESSE : 3 ECHECS SILENCIEUX CORRIGES (Vulcain)

**Contexte** : 4e round qualite pro sur le theme ROBUSTESSE (messages d erreur, dry-run, cas limites). Diagnostic reel : la base etait solide (messages avec chemin + conseils 6/6, dry-run reellement non-destructif 8/8, cas limites corrects) mais 3 echecs SILENCIEUX subsistaient.

**Failles detectees et corrigees** :
1. ecrire-fichier : contenu vide sur fichier existant = no-op silencieux (fichier inchange, aucun message, exit 0). Correction : contenu vide = TRONCATURE explicite a zero octet + message INFO (parite py/sh : open w vs : > fichier). Un agent peut desormais vider un fichier et sait ce qui s est passe.
2. lire-fichier : plage inverse (--debut 5 --fin 2) = exit 0 avec sortie vide, silencieux. Correction : validation de plage AVANT lecture - --debut > --fin, ou borne < 1 (--debut/--fin/--lignes) -> erreur explicite exit 1 (parite py/sh).
3. supprimer-ligne : message "le fichier n a que 1 lignes" (pluriel faux). Correction : pluriel correct (1 ligne vs N lignes) (parite py/sh).

**Lecons** :
1. LE 0 SILENCIEUX EST L ENNEMI N 1 DE LA ROBUSTESSE : un agent qui ne recoit ni effet ni message ne peut pas decider - chaque cas inapplicable doit refuser ou informer explicitement.
2. LA PARITE PY/SH SE TESTE DES DEUX COTES : les 3 corrections ont ete verifiees en .py ET en .sh (les deux partagent les memes pieges de no-op : open append vs touch).
3. LE DIAGNOSTIC CONFIRME AUSSI CE QUI VA BIEN : dry-run reellement non-destructif (8/8, backup non cree en dry-run) et messages avec chemin + conseils (6/6) - la qualite pro des rounds precedents tient.

**Tests reels** : 18/18 py + 5/5 sh verts (3 corrections prouvees + non-regression comportementale : plage valide, dry-run, nominaux). Normes 0/0 sur 9 fichiers. Aucun script temporaire laisse (garde-fou test-024 respecte).

## [LECON] 2026-08-12 -- ROUND 5 COMBOS : FIN DE LA PROPAGATION SILENCIEUSE DES ECHECS (Vulcain)

**Contexte** : 5e round qualite pro sur le theme COMBOS (enchainements d outils fluides et sans friction). Le diagnostic reel a revele une faille critique du combos-moteur v0.3.1 : le code retour des cases outil n etait JAMAIS verifie.

**Faille critique** : une case outil qui echoue (exit != 0) laissait le moteur continuer jusqu a la case fin avec code retour 0. Un agent lancant un combo croyait que tout avait reussi alors qu une etape avait echoue - le pire des echecs silencieux, au niveau de l orchestration elle-meme.

**Corrections** :
1. combos-moteur v0.3.2 (py + sh, parite) : verification du returncode de chaque case outil - un echec ARRETE le combo avec message explicite (case, commande, code, sortie).
2. Nouveau champ optionnel `echec_ok: true` : pour les outils de CONTROLE/DETECTION (valider-*, detecter-*, verifier-*, rechercher-*) dont le code non nul est un RESULTAT legitime (ecart signale par exit 1) - le resultat est stocke et le combo continue.
3. Audit et marquage des 14 combos : 30 cases `echec_ok: true` sur 10 combos de controle (controle-outil, controle-impacts, sante-tableaux, audit-themis, controle-modification, corriger-ascii, maj-readme, creer-agent, creer-fichier-cerveau, creer-protocole). Les 4 combos d action (activation, corriger-fichier, tester-outil, controle-buffy) restent sans echec_ok : leur echec doit arreter.
4. Versions alignees 0.3.2 (py/sh/md) + documentation de la regle dans combos-moteur.md.

**Lecons** :
1. L ORCHESTRATEUR DOIT VERIFIER SES SOUS-PROCESSUS : un moteur qui enchaine des outils sans regarder leurs codes retour propage les echecs silencieusement - pire que l outil lui-meme.
2. IL FAUT DISTINGUER ECHEC et RESULTAT NON NUL : un validateur qui retourne 1 a trouve un ecart - c est un RESULTAT. Un createur qui retourne 1 a echoue - c est un ECHEC. Le champ echec_ok rend cette distinction EXPLICITE dans la definition.
3. LE CONTROLE CROISE (Janus) et la NON-REGRESSION (Morpheus) sont la garantie que le changement de comportement (arret sur echec) ne casse aucun combo existant.

**Tests reels** : 5/5 py (arret sur echec rc=1 + message, echec_ok continue rc=0, 14/14 combos chargent, dry-run non destructif, 30 cases marquees) + 4/4 sh (parite). Normes 0/0 sur 17 fichiers. Aucun script temporaire laisse.


## [LECON] 2026-08-12 -- ROUND 7 VALIDER : FAUX POSITIFS/NEGATIFS (Vulcain)

**Contexte** : round 7 qualite pro, theme VALIDER (faux positifs/negatifs des
validateurs). Diagnostic reel (mesures sur copies temporaires, pas opinions) :
4 faiblesses + 1 decision utilisateur (renommage complet).

**Faiblesses corrigees** :

A. valider-case v1.1.1 : FAUX NEGATIF GRAVE - les references mortes n etaient
   PAS detectees (le BFS faisait 'if suivant and suivant in cases', une ref
   inexistante etait ignoree silencieusement -> CONFORME rc=0 sur une carte
   cassee). Correction : verifier_structure signale chaque 'suivant' et chaque
   branche 'vers' pointant vers une case inexistante + meme verif en mode
   --case <id>. py/sh/md 1.1.1.

B. Versions alignees (regle des 5 fichiers) : valider-cartes-decision.sh
   0.3.2 -> 0.4.0 ; valider-liens.py 0.2.0-py -> 0.4.0-py.

C. valider-nommage v0.3.3 : --recursive sur une CATEGORIE (tools/valider/)
   rendait Total: 0 silencieux (faux negatif : on croit que tout est valide,
   rien n est scanne). Correction : detection de categorie (un sous-dossier
   outil a un .py/.sh a son nom) -> profondeur de scan 1 au lieu de 2.
   Parite portee dans le .sh (implementation parallele, pas un wrapper).

D1-D3. valider-nommage : formats speciaux LEGITIMES reconnus (faux positifs du
   scan global elimines) : combo-*.md (4), tester-*-v0xx.sh (2), rapport-*.md
   (3, regex etendu au suffixe date v010-2026-08-11). Scan global tools/ :
   11 erreurs -> 0 erreur (335 fichiers).

D4. RENOMMAGE COMPLET (decision utilisateur) : lancer-non-regression ->
    tester-lancer-non-regression (le dossier tester/ exige le prefixe tester-,
    c etait le seul ecart de nommage de la boite). Dossier deplace + fichiers
    renommes + catalogue + index-tools + test-024 + protocole + auto-refs.

**Lecons** :

1. UN VALIDATEUR QUI REPOND CONFORME SUR UNE CARTE CASSEE EST PIRE QUE PAS DE
   VALIDATEUR : la confiance tue la detection. Toujours tester les validateurs
   sur des copies CORROMPUES (ref morte, case orpheline) avant de les valider.

2. PIEGE DU TEST : cibler 'suivant == c2' sans verifier qu une case a ce champ
   top-level = modification silencieuse sans effet (le flux passait par des
   branches). Le test semblait KO alors que l outil etait bon. Verifier QUE la
   mutation a eu lieu (assert sur la cible) avant d interpreter le resultat.

3. LE LOCAL HORS FONCTION en bash (bloc --recursive top-level) fait planter le
   .sh alors que le .py marche : a chaque portage py -> sh, re-verifier la
   validite bash -n et la parite de sortie, pas seulement le code.

4. UN RENOMMAGE COMPLET demande un grep de l ANCIEN NOM dans TOUT le repo avec
   exclusion des documents figes (corrections.md, controles/, historique) : le
   nouveau nom contient l ancien (tester-lancer-non-regression contient
   lancer-non-regression) - un grep naif donne des faux positifs.

**Validations** : 16/16 retests (A py/sh/--case, B versions, C py/sh,
D scan 0 erreur + renommage), test-024 12/12, valider-cartes-decision --tous
11/11, verifier-conformite-fiche --tous 11/11, normes 0/0, 0 residu ancien nom.


## [LECON] 2026-08-12 -- ROUND 8 REGISTRE/TRACES : LA MEMOIRE (Vulcain)

**Contexte** : round 8 qualite pro, theme REGISTRE ET TRACES (fiabilite de la
journalisation). Diagnostic reel : 4 faiblesses + 1 decision utilisateur
(ARCHIVER AU LIEU DE PURGER).

**Faiblesses corrigees** :

A. tester-lancer-non-regression v0.1.1 : la purge du registre a chaque
   non-regression (--no-journal ecrivait fh.write('')) DETRUISAIT la memoire
   des declarations -> detecter-usage-scripts-temporaires devenait aveugle au
   passe et signalait des faux ecarts permanents. Correction : archivage vers
   registre-usages-outils.historique.jsonl (append, dedoublonnage par ligne
   exacte, idempotent) puis vidage du registre courant. Message de fin
   indique 'archive dans l historique : N'.

B. detecter-usage-scripts-temporaires v0.1.1 : (1) croisement avec le registre
   COURANT + l HISTORIQUE (les declarations archivees restent verifiables) ;
   (2) FILTRE est_script_temporaire : un script est un FICHIER .py/.sh dont
   le basename commence par .zz-/.tmp- - les dossiers de tests (.tmp-eol-test/,
   .tmp-gc-test/, .tmp-morpheus-test/) et les .md/.json n en sont pas
   (faux positifs elimines) ; (3) scan git et racine filtres pareillement.

C. enregistrer-usage-outil v0.2.1 : garde-fous de fiabilite - --agent vide ou
   --outil vide -> [ERREUR] + code 1 (avant : accepte silencieusement rc=0) ;
   doublon (agent+outil+mode+commande+contexte identiques) -> [AVERTISSEMENT] ;
   lignes non-JSON dans le registre -> [AVERTISSEMENT] avant ajout.

D. Versions alignees : tester-lancer 0.1.1, detecter 0.1.1, enregistrer 0.2.1
   (py/sh/md coherents - enregistrer md etait en 0.1.0 alors que le py etait
   deja en 0.2.0, divergence pre-existante).

**Lecons** :

1. UNE SOURCE DE VERITE QUE L ON PURGE N EST PLUS UNE SOURCE DE VERITE :
   la purge silencieuse du registre a chaque non-regression a cree 12 faux
   ecarts permanents (le detecteur comparait le present avec un passe
   efface). La memoire doit etre ARCHIVEE (append, jamais ecrase) pour que
   les controles restent verifiables dans le temps.

2. UN SCAN GIT QUI MATCHE LE PREFIXE SANS L EXTENSION COMPTE DES DOSSIERS
   ET DES .md/.json COMME DES SCRIPTS : .tmp-eol-test/ etait un dossier de
   tests, pas un script jetable. Toujours filtrer par basename + extension
   (.py/.sh) pour distinguer un script d un artefact de test.

3. UN OUTIL QUI ACCEPTE --agent VIDE (rc=0) PRODUIT DES ENTREES
   INEXPLOITABLES : le registre est la base des controles - une entree sans
   agent ne peut etre croisee avec rien. Refuser les champs obligatoires
   vides, signaler doublons et corruption sans bloquer (un usage peut etre
   legitiment rejoue).

4. LA REGLE DES 5 FICHIERS SE VERIFIE AUSSI POUR LES VERSIONS md : le .md
   d enregistrer-usage-outil etait reste en 0.1.0 alors que le .py etait en
   0.2.0 (le mode script-temporaire du round precedent n avait pas bumpe le
   md). Un bump py sans bump md = divergence silencieuse.

**Validations** : 19/19 retests (A archivage idempotent, B filtre + croisement
historique, C garde-fous, D versions), test-024 13/13 (adaptes + nouveau
garde-fou memoire : l historique existe), non-regression 26/26, catalogue
146 intact + 0 a ajouter, normes 0/0 sur 10 fichiers, registre courant 0
ligne + historique 7 lignes (usages Janus/Cerberus du round 7 archives).


## [LECON] 2026-08-12 -- ROUND 9 GUIDAGE/NAVIGATION : L AGENT QUI SE PERD (Vulcain)

**Contexte** : round 9 qualite pro, theme GUIDAGE ET NAVIGATION (guider-parcours,
generateurs-carte, generateurs-case). Diagnostic reel (mesures, pas opinions) :
4 faiblesses.

**Faiblesses corrigees** :

A. guider-parcours (0.5.0) : une case de depart INEXISTANTE (--case c999)
   provoquait un KeyError TRACEBACK BRUT (case = cases[cid]) - l agent qui se
   trompe de case recoit un crash Python au lieu d etre guide. Correction :
   dans naviguer(), verification cid in cases AVANT la boucle -> message
   'la case de depart <id> n existe pas' + liste des ids disponibles + code 1.
   Le cas case_depart du parcours inexistant etait deja couvert par
   valider_parcours ('introuvable dans cases', code 1) - pas de double emploi.

B. generateurs-case (0.4.2) : --version au niveau RACINE casse (le flag
   n existait QUE sur les sous-parsers -> 'generateurs-case.py --version'
   repondait rc=2 'arguments required: parcours, action'). Correction :
   interception 'if --version in sys.argv' dans main() avant parse_args
   (comme generateurs-carte), sous-parsers conserves pour la parite py/sh.

C. generateurs-case : VERSIONS DIVERGENTES (regle des 5 fichiers) - py
   VERSION=0.4.2, en-tete py=0.3.1, sh=0.4.0, md=0.4.2 (3 valeurs !).
   Correction : en-tete py + sh alignes sur 0.4.2, md completer avec
   l historique 0.3.0/0.4.0/0.4.2 manquant.

D. generateurs-carte (0.3.0) : --aide des sous-commandes (creer --aide,
   dupliquer-chemin --aide) affichait l AIDE RACINE au lieu du sous-parser.
   Correction : port du mecanisme de ciblage de generateurs-case (boucle sur
   parser._actions pour trouver le sous-parser).

**Lecons** :

1. L AGENT QUI SE PERD DOIT ETRE GUIDE, PAS CRASH : un KeyError sur une case
   inexistante est le pire comportement pour un outil de navigation. Toujours
   verifier les entrees utilisateur (case de depart, --case) AVANT de boucler
   et afficher les choix possibles (liste des ids).

2. --version EST UN CONTRAT : TOUS les outils doivent repondre a --version au
   niveau racine (usage standard de verification). Un sous-commande qui cache
   le flag (parcours positionnel obligatoire avant) casse ce contrat
   silencieusement : il faut l intercepter AVANT parse_args.

3. LA REGLE DES 5 FICHIERS SE DIVISE EN 3 : en-tete py, VERSION py, sh, md -
   ici 3 valeurs differentes sur 4 emplacements (0.3.1/0.4.2/0.4.0/0.4.2).
   Chaque bump doit mettre a jour les 4 emplacements + la table Versionning
   du md (qui s arretait a 0.2.2 alors que l outil etait en 0.4.2).

4. UN MECANISME QUI EXISTE DANS UN OUTIL (ciblage --aide de generateurs-case)
   DOIT ETRE PORTE : generateurs-carte avait le meme besoin (sous-commandes)
   mais affichait l aide racine. Reutiliser les solutions deja validees de la
   boite au lieu de re-inventer.

**Validations** : 14/14 retests (A case inexistante py/sh/parcours corrompu,
B --version racine + sous-parser + sh, C versions 4 emplacements, D --aide
sous-commandes), test-010 25/25, test-014 13/13, test-004 16/16,
non-regression 26/26, catalogue 146 intact + 0 a ajouter, normes 0/0 sur
5 fichiers.

## [LECON] 2026-08-12 -- CORRECTION BUG DEMARRAGE SIDENTIFIER v0.5.1 (Vulcain)

**Contexte** : l utilisateur a signale que Morpheus s arretait a chaque activation (rounds 8 et 9). Diagnostic Cerberus : le parcours de Morpheus etait PROPRE (30/30 atteignables, detecter-cablages-manquants OK, navigation OK) et tous les outils existaient. La vraie cause etait dans activer-agent-principal.py sidentifier : il ECRASAIT le profil classeur avec 'agent: Cerberus' code en dur + affichait '(agent principal : Cerberus)' dans les 4 messages, MEME quand la session retrouvee avait un AUTRE agent actif (morpheus). Resultat : AGENTS.md disait morpheus, le classeur disait Cerberus -> double source CONTRADICTOIRE -> l agent qui demarrait (Morpheus lance sidentifier selon sa fiche) recevait une identite fausse et s arretait.

**Correction** : fonction agent_actif_bloc() (py + sh) qui lit l agent REEL du bloc (champ Nom Agent) ; session retrouvee -> affiche + ecrit le profil + l historique avec l agent reel ; nouvelle session -> Cerberus par defaut conserve. Bump 0.5.0 -> 0.5.1 (py/sh/md + table Versionning).

**Lecons** :

1. UNE SESSION QUI S ARRETE AU DEMARRAGE N EST PAS UN PROBLEME DE PARCOURS : quand un agent ne demarre pas, verifier d abord le cycle d identification (sidentifier) avant de suspecter les cases. Le parcours etait sain.

2. LA SOURCE DOUBLE DOIT ETRE VERIFIEE CROISEE : AGENTS.md et le classeur disent TOUS DEUX qui est l agent actif. Une ecriture en dur (Cerberus) dans l un des deux cree une contradiction silencieuse : aucun test ne detectait le classeur faux parce que sidentifier re-ecrivait le mensonge a chaque appel.

3. LE CLASSEUR EST DERIVE, PAS UNE CONSTANTE : il doit refletet l etat du bloc AGENTS.md a chaque instant. Toute valeur codee en dur (agent, role, date) dans une fonction qui ECRIT le classeur est un bug potentiel.

**Validations** : sidentifier llm-1 affiche 'agent principal : vulcain' + classeur 'agent: vulcain' (py ET sh identiques) ; normes 0/0 sur 5 fichiers ; test-025 11/11, test-018 13/13, test-021 9/9, test-002 REUSSI ; catalogue dry-run 0 a ajouter ; non-regression 26/26.

## [LECON] 2026-08-12 -- POINT D ENTREE PROTECTIONS + PROTECTION STOP (Vulcain)

**Mission** : creer le point d entree importable des protections de tests (demande utilisateur : chaque test DOIT importer les protections) + la protection STOP (fail-fast).

**Resultat** : tester-protections v0.1.0 (module importable via importlib depuis chaque test-0XX) : lancer_protege (timeout + tuer l arbre cross-platform + erreurs silencieuses), verifier_critique (STOP : leve ArretProtection si condition fausse), ArretProtection, CLI --version/--liste. Tests reels : import OK, lancer_protege OK, STOP verifier_critique OK, STOP timeout (boucle infinie arretee en 3s) OK. Doc .md + catalogue 147 + index-tools 116. Normes 0/0.

**Lecons** :
1. UNE PROTECTION NON IMPORTABLE EST UNE PROTECTION MORTE : les 3 anciennes protections (wrappers shell=True) n etaient jamais chargees par les 29 tests. Le point d entree unique importable rend la protection reelle.
2. FAIL-FAST > CONTINUER BETEMENT : la protection STOP (ArretProtection) arrete le test au premier echec critique - un test qui continue apres un KO produit des erreurs en cascade illisibles.
3. ASCII STRICT PIEGE : un accent typographique (enchainer) a ete detecte par la norme - toujours verifier apres ecriture.

## [LECON] 2026-08-13 -- CHRONO + REFERENCE DE TEMPS NON-REGRESSION (Vulcain)

**Mission** : repondre a l utilisateur qui avait l impression que le parallele ne gagnait rien (mesures reelles : parallele 1m53 vs serie 2m17 = gain 24s/17%, mais goulot = serie D en serie apres A/B/C). Ajouter un chrono global + reference de temps au lanceur (v0.1.4 -> v0.1.5).

**Resultat** : chrono demarre au debut de la premiere serie et s arrete a la fin de la derniere (time.monotonic), affiche a la fin de chaque passe (mono-serie sans reference, suite complete avec reference). Reference persistee dans temps-reference.json (dossier de l outil, .gitignore) : creee si absente, MISE A JOUR AUTOMATIQUE quand le temps est meilleur, SIGNAL de ralentissement si depassement > --seuil (defaut 25%), --rebase-reference force, --no-reference pour les sous-processus paralleles. Sous-processus A/B/C passent --no-reference (jamais de course sur le fichier). Tests reels : creation reference 113.6s, 2e run 113.5s -> temps ameliore reference mise a jour, SIGNAL prouve (reference artificielle 0.001s -> +196441%), rebase force, no-reference inchange. Non-regression 30/30, normes 0/0, catalogue 147 (--seuil ajoute).

**Lecons** :
1. MESURER AVANT DE JUGER : l utilisateur croyait le parallele inutile - les mesures (1m53 vs 2m17) ont montre un gain reel de 17% mais masque par la serie D (goulot en serie). Le chrono rend le gain visible et compare a une reference.
2. UNE REFERENCE ECRITE PAR UN APPEL INTERNE EST UNE REFERENCE FAUSSE : test-027 lance le lanceur lui-meme (avec filtre) et avait cree une reference partielle de 0.4s - regle : la reference globale n est geree QUE par le run complet sans --tests.
3. LA REFERENCE NE DOIT JAMAIS ECRASER UN MEILLEUR TEMPS PAR UN PLUS LENT : on n ecrit que si le nouveau temps est meilleur (ou rebase force) - sinon le SIGNAL serait perdu.
4. UNE DONNEE MACHINE-DEPENDANTE N EST PAS UN LIVRABLE : temps-reference.json va dans .gitignore - la reference est locale a la machine, chaque machine a ses performances.

## [LECON] 2026-08-13 -- POOL DE WORKERS NON-REGRESSION (Vulcain, round 3 etapes)

**Mission** : reduire le temps total de la suite anti-regression (demande utilisateur : suites paralleles contenant les tests longs, estimation du nombre de workers). Diagnostic : machine 16 coeurs, test-028 = 88s (LE goulot, 60% du temps, lecteur pur), 30 autres tests <= 9s.

**Resultat** : lanceur v0.2.0 refondu : POOL DE WORKERS par defaut (--workers N, defaut min(cpu,16)), tests tries par duree decroissante (les plus longs partent en premier), garde-fous globaux (test-023/024/025/027 : registre, sessions, scripts temporaires) en serie finale (jamais en parallele), --serial/--workers 1 = mode serie. Gain reel mesure : 119.9s -> 91.2s (-24%) pour 31 tests. Tests adaptes : test-024/027/031 (v0.2.0 + structure Pool), doc, catalogue 147. Non-regression 31/31, normes 0/0, reference mise a jour 91.2s.

**Lecons** :
1. DEADLOCK DU PIPE STDOUT : un Popen(stdout=PIPE) non lu se bloque au-dela de 64 Ko de sortie (poll() ne passe jamais a None) - le pool semblait bloque a 500s+ alors que c etait le pipe. Solution : rediriger la sortie de chaque test vers un FICHIER temp unique.
2. TOUT NE SE PARALLELISE PAS : les garde-fous qui verifient l etat global (registre, sessions, scripts temporaires) doivent rester EN SERIE - les lancer en parallele produit des faux positifs (ou des conflits d ecriture sur fichiers partages).
3. MESURER AVANT D ESTIMER : la reponse a la question utilisateur (combien de workers ?) repose sur le profil reel : 16 coeurs, goulot 88s -> plafond theorique ~90s, atteint a 91.2s. Sans le chrono+reference du round 11, ce gain serait invisible.
4. LE TRI PAR DUREE DECROISSANTE EST CRUCIAL : les tests longs partent en premier sur les workers, les courts remplissent les creneaux - sans tri, le temps total est le max des sommes arbitraires.

## [LECON] 2026-08-13 -- GOULOT TEST-028 ABATTU : DECALAGES-CATALOGUE EN PARALLELE (Vulcain)

**Demande utilisateur** : optimiser test-028 en interne (88s, LE goulot de la suite) pour abaisser le plafond de temps total.

**Diagnostic** (mesure reelle) : test-028 lance 4 sous-processus : DIV_PY --version (rapide), DEC_PY --version (rapide), DIV_PY --racine (scan specs = 1s), DEC_PY (scan catalogue = ~85s). Le goulot est 100% detecter-decalages-catalogue : il lance l aide de CHACUNE des 147 commandes du catalogue EN SERIE (~294 sous-processus Python, 2 flags par commande, ~0.3s chacun sur cette VM lecteur Z:).

**Correction** (detecter-decalages-catalogue v0.2.0 -> v0.2.1) :
1. POOL DE THREADS : les aides sont lancees en parallele (ThreadPoolExecutor, max_workers = min(16, nb commandes)) au lieu d une boucle serie. Chaque lancement d aide est un sous-processus independant (lecture seule) : thread-safe sans verrou.
2. CACHE PAR (interpreteur, script) : un script reference par plusieurs commandes du catalogue n est lance qu une seule fois (activer-agent-principal 5x -> 1 lancement ; 8 scripts partages identifies).
3. PIEGE EVITE : ne pas utiliser la sonde (tuple contenant une LISTE manquants_oblig) comme cle de dict -> unhashable (TypeError). Cle = index de la sonde.

**Resultat** (mesures reelles) : DEC seul 85s -> 14s (-83%) ; test-028 88s -> 22s (-75%) ; suite anti-regression complete 92.2s -> 52.3s (-43%) pour 32 tests. Mise a jour : test-028 (version v0.2.1 + docstring), doc .md, spec (en-tete + historique + critere 1), catalogue inchange (pas de version). Normes 0/0.

**Correctif fiabilite (trouve par Morpheus pendant la validation)** : avec le pool 16, la contention au demarrage des interpretes Python (lecteur reseau) faisait depasser le TIMEOUT=8s a des outils qui repondent en 6-9s seuls (test-017 CONFORME seul / TIMEOUT sous charge -> verdict instable, 8 vs 9 non testables selon les runs). TIMEOUT porte a 30s : verdict STABLE (2 runs identiques : 141 conformes / 0 decalage / 6 non testables) et plus precis (test-003/005/017 correctement classifies CONFORME). Suite complete : 57.2s (+9% vs 52.3s, conforme).

**Lecons** :
1. UN SCAN DOCUMENTAIRE PEUT ETRE LE GOUTLOT CACHE : test-028 etait range dans le pool comme test long, mais on l a traite comme une boite noire. Relire le code a revele que 96% de son temps etait un sous-outil qui lancait ~300 sous-processus en serie.
2. PARALLELISER A L INTERIEUR D UN OUTIL : le pool de workers du lanceur parallellise LES TESTS, mais un test qui lance 294 sous-processus en serie reste un goulot. La parallelisation doit aussi descendre DANS les outils (ici : ThreadPoolExecutor sur des sous-processus independants).
3. LE CACHE DE SOUS-PROCESSUS : quand le catalogue reference le meme script plusieurs fois (activer 5x), le cache (interpreteur, script) supprime les lancements redondants - gain cumulatif avec le pool.
4. BUMP DE VERSION = MISE A JOUR EN CHAINE : header py + VERSION + doc .md + spec (en-tete, historique, criteres) + test qui verifie --version. Oublier la spec = KO test-028 point 3 (detecter-divergences-version le signale).
5. PARALLELISME = VERDICT STABLE OBLIGATOIRE : un outil parallelise ne doit JAMAIS changer de verdict selon la charge. Les timeouts doivent absorber la contention (durees mesurees seules x2 minimum), et la stabilite doit etre prouvee par 2 runs identiques avant de valider.

## [LECON] 2026-08-13 -- THEMIS : 2 NOUVEAUX OUTILS + ROUND QUALITE EVALUATEURS (Vulcain)

**Mission** : ameliorer Themis et ses outils (demande utilisateur, 4 axes : A outiller ses lecons, B rounds qualite evaluateurs, C evaluateur processus, D carte/declencheurs par Buffy apres).

**Resultat** : AXE C evaluer-processus v0.2.0 (detecte les derives : fins de mission erronees, outils hors carte, coherence fiche/carte) + AXE A detecter-evaluations-incompletes v0.1.0 (scan anti-recurrence 4 sources : validateur, spec, generateurs, tests) + AXE B rounds qualite sur les 4 evaluateurs (--rapport, --verbose, couleurs ANSI desactivees hors tty, versions sync 5 fichiers).

**Lecons** :
1. LA SOURCE FIABLE DES USAGES EST LE REGISTRE, PAS LES LECONS : une premiere version d evaluer-processus croisait les lecons (corrections.md) -> 198 faux positifs (les lecons mentionnent les outils des autres agents et des audits). Le registre (registre-usages-outils.jsonl, alimente par enregistrer-usage-outil) est la seule source des outils RELLEMENT utilises par chaque agent.
2. UN OUTIL DE DETECTION QUI CRIE 198 FOIS EST INUTILE : la valeur d un detecteur est sa precision, pas sa sensibilite. Corriger le bruit (source + exclusions P0/transverses) AVANT de livrer, pas apres.
3. LA CARTE DOIT REFLETER LES USAGES REELS : evaluer-processus a revele que tester-lancer-non-regression (outil principal de Morpheus !) n etait assigne dans AUCUNE case de sa carte - ni dans celles de vulcain/janus qui le lancent pourtant. Lacunes corrigees (morpheus c12/c7, vulcain c8, janus c4) + bumps de parcours et fiches (Pattern 14).
4. UN SCAN ANTI-RECURRENCE DOIT CROISER LES 4 SOURCES : la lecon Themis (audit qui ne scanne que les fichiers modifies rate 8 mentions) est resolue par detecter-evaluations-incompletes avec motif/filtre/contexte - la regex cT1([^0-9*]|$) distingue les mentions conformes des residuelles.
5. COULEURS ANSI = POLLUTION EN REDIRECTION : les evaluateurs emettaient des codes de couleur meme captures (combo, tests) - desactivation auto via sys.stdout.isatty() + option --rapport pour ecrire un rapport propre.
6. BUMP DE VERSION = SYNCHRONISATION .py/.sh/.md + FICHE (Pattern 14) : oublier la fiche (v0.4.2 vs parcours 0.4.3) = KO valider-cartes-decision. Toujours verifier fiche ET parcours apres bump.


## [LECON] 2026-08-13 -- BUG 'AGENT INCONNU HYGIE' CORRIGE (Vulcain)

**Contexte** : la creation de l agent Hygie (mission bout-en-bout 2026-08-13)
a ajoute Hygie au catalogue, a l index-tools et a AGENTS.md mais PAS dans la
liste interne AGENTS de l outil activer-agent-principal (.py + .sh) -> toute
activation de Hygie echouait avec 'ERREUR: Agent inconnu'.

**Cause racine** : deux sources de liste d agents coexistent - le catalogue
generateurs-commande (commande activer-activer, choix des agents) ET le
dictionnaire/case de l outil d activation. La mission de creation n a mis a
jour que la premiere.

**Correction (v0.5.2 -> v0.5.3)** : ajout de hygie (role/fiche/corrections)
dans le dictionnaire AGENTS du .py + les 3 blocs case du .sh. Preuves
reelles : activer hygie OK, reactiver Cerberus OK, sh --version v0.5.3,
get_agent_role hygie OK, normes 0/0.

**Lecons** :
1. Quand on cree un agent, la liste des agents connus existe en PLUSIEURS
   endroits : catalogue (activer-activer), index-agents, AGENTS.md, ET
   activer-agent-principal (.py + .sh). TOUT mettre a jour ou le premier
   usage reel echoue.
2. Le test en conditions reelles (1ere activation de Hygie) a revele le bug
   immediatement - jamais supposer qu une creation est complete sans tester
   l usage reel du nouvel element.
3. Aucun test de non-regression ne verifie la liste des agents connus de
   l outil : a signaler pour un eventuel garde-fou (ex: chaque agent de
   index-agents doit etre activable).


## [LECON] 2026-08-14 -- EVALUER-PROCESSUS v0.1.1 : 2 BUGS CORRIGES (Vulcain)

**Contexte** : test-035 KO (serie e 16/17). Diagnostic Cerberus : 2 des 5 problemes etaient des BUGS de mon outil evaluer-processus.

**BUG 1 - FIN_MISSION_ERRONEE faux positif** : `detecter_fins_erronees` faisait `missions[-3:]` sur une liste en ordre DECROISSANT (missions recentes en tete : AGENTS.md puis AGENTS-historique du recent a l ancien) -> il examinait les 3 missions les PLUS ANCIENNES au lieu des 3 plus recentes. La mission chrono de morpheus (00:08, consigne 'reactiver Cerberus' LEGITIME a l epoque) etait faussement signalee. FIX : `missions[:3]` (les 3 plus recentes). Le commentaire original disait deja "la mission la PLUS RECENTE".

**BUG 2 - OUTIL_HORS_CARTE faux positif** : `usages_registre` comptait toutes les entrees du registre, y compris les scripts temporaires legitimes (mode="script-temporaire", ex tmp-buffy/xxx.py). Un script temporaire n est PAS un outil de la carte. FIX : ignorer les entrees mode="script-temporaire".

**Lecon** : les outils de detection doivent comprendre le sens des DONNEES qu ils lisent (ordre des listes, modes du registre), pas seulement les parcourir naivement. Un faux positif qui signale une mission historique legitime et un script temporaire legitime cree du bruit qui masque les vrais ecarts.

**Verifications** : apres fix : morpheus 0 FIN_MISSION_ERRONEE, buffy 0 probleme. Restent les VRAIS ecarts (4) a traiter : morpheus tester-lancer-non-regression (retrait registre - seul Janus lance la non-regression), janus detecter-residus + detecter-divergences-version + evaluer-processus (ajout carte Janus). v0.1.1 py+md, normes 0/0, py_compile OK.


## [LECON] 2026-08-14 -- DEMARRAGE AUTOMATIQUE + FIX RAISON MULTILIGNE (Vulcain, v0.5.4)

**Contexte** : demande utilisateur - comprendre et corriger le bug d arret au
demarrage des agents (vu 2x pour Themis et Morpheus : l agent active reste
bloque a sa case c0).

**Diagnostic (3 causes)** :
1. guider-parcours est CONCU pour s arreter proprement sur une question en mode
   agent (return 0) - l agent doit relancer avec --reponses.
2. Aucune mission d activation du 14/08 ne contenait l instruction de demarrage
   (--reponses) alors que celles du 13/08 la contenaient.
3. AGENTS.md etape 4 dit execute sa mission mais jamais COMMENT demarrer.

**BONUS (bug latent decouvert en testant)** : reconstruire_bloc (py) et
emettre_bloc (sh awk) perdent la Raison MULTILIGNE a chaque reactivation - la
mission de l agent etait tronquee a la 1re ligne + une ligne parasite
'| **Classeur-variables** | Agent |' apparaissait. PROUVE par test reel sur copie.

**Fait (v0.5.4)** :
1. activer_agent (py + sh) : ajoute DEMARRAGE OBLIGATOIRE a la Raison quand un
   agent != cerberus est active (avec le chemin du parcours et --case c0
   --reponses OUI). Pas pour reactiver ni pour cerberus.
2. Fix multiligne : capture des lignes de continuation de la Raison +
   recollement + reemission en lignes brutes (py et sh).
3. Doc .md : version 0.5.4 + entree changelog.
4. Tests : py A/B/C/D True, sh A/B True, 7 tests internes de l outil VALIDES,
   test-025 11/11, test-013 22/22, test-018 13/13, test-034 6/6.

**Lecon** : (a) quand on corrige un bug de demarrage, tester sur COPIE avec
AGENTS_FILE surcharge (jamais sur le vrai fichier) ; (b) verifier la parite
py/sh et la survie des champs MULTILIGNES (le format AGENTS.md supporte les
retours a la ligne dans Raison - les reconstructions doivent les preserver).


## [LECON] 2026-08-14 -- REGISTRE-TESTS : TRACE DES LANCEMENTS DE TESTS (Vulcain)

**Contexte** : demande utilisateur - comme le registre-usages-outils.jsonl trace
l utilisation des outils, chaque lancement de tests par un agent doit laisser
une trace dans un registre dedie. Mission reprise apres suspension par la
derive de gouvernance (corrigee : la chaine Cerberus->Vulcain->Morpheus->Janus
est respectee).

**Implementation (tester-lancer-non-regression v0.2.0 -> v0.3.0)** :
1. Option --agent <nom> (optionnel, vide par defaut).
2. CHAQUE test execute est journalise dans cerveau-projet/agents/traces/
   registre-tests.jsonl (une entree par test : date, agent, serie, test,
   verdict OK/KO/ERREUR, duree secondes) - sur les 2 chemins :
   executer_lot (serie) et executer_pool (parallele).
3. Dans le pool, la serie de CHAQUE test est deduite de son nom
   (serie_du_test) - les garde-fous globaux portent la serie 'globaux'.
4. Registre DISTINCT de registre-usages-outils.jsonl (jamais melanges).
5. Doc .md maj (version 0.3.0 + option --agent + historique) + catalogue
   generateurs-commande (parametre agent optionnel).

**Preuves reelles** : serie a avec --agent vulcain -> 6 entrees correctes
(verdict + duree) ; run complet pool avec --agent -> 51 tests journalises
(series a/b/c/d/e/globaux distribuees) ; --version 0.3.0 ; normes 0/0.

**Impact tests** : 4 tests figent la version 0.2.0 du lanceur en dur
(test-031, test-032, test-024, test-027) - adaptes par Morpheus (maillon
de chaine), qui cree aussi le garde-fou test-051.

**Regle durable** : les outils qui s executent souvent (comme le lanceur de
non-regression) doivent journaliser leurs executions - le registre-tests est
la memoire des lancements, le registre-usages-outils la memoire des usages.


## [LECON] 2026-08-14 -- TRI DU REGISTRE-USAGES-OUTILS PAR DATE/HEURE DECROISSANT (Vulcain)

**Contexte** : demande utilisateur - le registre-usages-outils.jsonl etait
ecrit en append (ordre d ecriture, dates melangees). Il doit etre trie par
date puis heure, affiche en DECROISSANT (le plus recent en premier).

**Implementation (enregistrer-usage-outil v0.2.1 -> v0.3.0)** :
1. Fonction trier_registre(registre) : relit toutes les lignes JSON, les trie
   par date (cle 'date', format YYYY-MM-DD HH:MM:SS, tri lexicographique =
   chronologique) DECROISSANT, reecrit le fichier (LF, ASCII).
2. Les lignes non-JSON sont PRESERVEES (signalees, jamais perdues) et placees
   en fin de fichier - compatibilite verifier_registre conservee.
3. Appelee APRES chaque ajout_entree : le registre est TOUJOURS trie.
4. Doc .md maj (version 0.3.0 + tri documente + historique).

**Preuves reelles** : registre 117 entrees non triees avant -> ajout d une
entree -> trie decroissant (premier = plus recent 22:09:35, dernier = plus
ancien 18:45:11). Retrait de l entree de test -> toujours trie.

**Impact tests** : test-024 point 7 fige la version 0.2.1 de
enregistrer-usage-outil -> KO previsible, adapte par Morpheus (maillon de
chaine).

**Regle durable** : un registre JSONL doit rester trie par date decroissante -
la lecture est plus lisible et l historique se lit du plus recent au plus
ancien. Les lignes invalides ne sont jamais perdues (conservees en fin).


## [LECON] 2026-08-14 -- TRI DU REGISTRE-TESTS PAR DATE/HEURE DECROISSANT (Vulcain)

**Contexte** : demande utilisateur - etendre au registre-tests.jsonl (trace
des lancements de tests) la regle de tri deja appliquee au
registre-usages-outils : tri par date/heure DECROISSANT (le plus recent en
premier).

**Implementation (tester-lancer-non-regression v0.3.0 -> v0.3.1)** :
1. Fonction trier_registre_tests(registre) : relit les lignes JSON, trie par
   date decroissante, lignes non-JSON conservees en fin (jamais perdues).
2. journaliser_test : apres chaque ecriture en append, trie le registre.
3. Doc .md maj (version 0.3.1 + tri documente + historique).

**Preuves reelles** : registre-tests 318 entrees non triees -> run serie a
avec --agent -> 319 entrees TRIEES decroissant (premier = plus recent 22:17:19,
dernier = plus ancien 22:01:01). Entree de preuve retiree ensuite (318).

**Impact tests** : les tests 031/032/024/027/051 figent la version 0.3.0 du
lanceur -> KO previsible, adaptes par Morpheus (maillon de chaine).

**Regle durable** : TOUS les registres JSONL du projet (usages + tests) sont
tries par date/heure decroissante - la regle est maintenant uniforme.


## [LECON] 2026-08-14 -- FIX BUG DE RECOLLEMENT + AGENTS.md REPARE (Vulcain)

**Contexte** : l utilisateur a signale AGENTS.md corrompu. Diagnostic :
le bloc session-llm-1 avait une Raison tronquee + 21 blocs DEMARRAGE
accumules + une mission egaree + un tableau orphelin.

**Cause racine** : activer-agent-principal.py v0.5.4, reconstruire_bloc -
le recollement des continuations faisait une EXCEPTION pour la Raison
(champ_c != Raison -> continue) donc les anciennes suites de la Raison
(blocs DEMARRAGE) etaient RECOLLEES a chaque nouvelle raison -> accumulation
a chaque cycle activer/reactiver.

**Fix v0.5.5** : un champ REMPLACE (present dans champs) ignore son ancienne
suite, Y COMPRIS la Raison. Le recollage ne sert plus que si la Raison n est
pas remplacee (ex: migration sans nouvelle raison).

**Reparation AGENTS.md** : relancer l activation avec l outil corrige a
reconstruit le bloc proprement (22 -> 1 bloc DEMARRAGE). Le tableau orphelin
(Classeur-variables/Conventions/...) etait un residu des anciennes lignes
cassees du bug classeur (pseudo-agents) - supprime (aucune section legitime).

**Lecon d echappement (rappel)** : la Raison tronquee venait d une apostrophe
mal echappee dans la commande de reactivation - TOUJOURS passer les raisons
via un script temp (subprocess.list2cmdline) jamais en inline shell.

**Preuves** : test-008 v0.5.5 cree (9/9 : bloc corrompu -> 1 DEMARRAGE, Raison
proprement remplacee, reactiver 0 bloc, Nom LLM preserve, normes). test-007
22/22 (regression). test-013 22/22, test-025 11/11. AGENTS.md 1 DEMARRAGE,
0 non-ascii, 0 crlf. Spec alignee 0.5.5.


## [LECON] 2026-08-14 -- DECLARATION USAGES MECANISEE DANS LE GENERATEUR (Vulcain)

**Contexte** : l utilisateur a constate que depuis 22:17:51 plus AUCUNE declaration
d usage n apparaissait au registre alors que 3 missions completes ont tourne
(fix recollement AGENTS.md, nettoyage test-051, garde-fou test-052) : les lecons
etaient documentees mais ni les scripts temp tmp-*/fin-*.py (mode script-temporaire)
ni les outils utilises n etaient declares. Cause racine : les scripts de fin de
mission etaient ecrits a la main sans le bloc de declaration, et le generateur
generateurs-outil-temporaire ne generait AUCUNE declaration d usage.

**Actions** :
1. generateurs-outil-temporaire v0.2.1 (.py + .sh en parite) : le squelette genere
   embarque le bloc DECLARATION USAGES - variable AGENT + fonctions racine_projet(),
   declarer_usage(), declarer_usages() qui appellent enregistrer-usage-outil
   --mode script-temporaire pour le script lui-meme et chaque outil utilise.
   Appel en fin de main(), erreur explicite si AGENT non renseigne (le script
   refuse de s executer sans declaration).
2. Doc .md mise a jour (comportement 9, historique 0.2.1).
3. Protocole-creation-scripts-temporaires v0.2.7 : etape 4 renforcee (TOUT script
   temp de mission declare + CHAQUE outil utilise) + nouvelle section
   "La declaration des usages (v0.2.7, anti-recurrence registre a 0 ligne)".

**Preuves reelles** : script genere avec AGENT=vulcain -> declaration automatique
au registre (entree tmp-test-declaration.py verifiee). Parite .py/.sh verifiee
(scripts generes identiques hors nom/description/date).

**KO attendus pour Morpheus** : test-050 2 KO - (1) version 0.2.0 figee en dur
(4 occurrences) ; (2) la preuve du point 5 execute le script genere sans
renseigner AGENT (le bloc refuse desormais de s executer -> renseigner AGENT
dans la preuve). Le nouveau garde-fou anti-recurrence doit verifier que le
squelette du generateur contient le bloc declarer_usages et que le protocole
l exige.


## [LECON] 2026-08-14 -- PROTECTION DOC OBLIGATOIRE DANS LE TEMPLATE OUTIL v0.2.0 (Vulcain)

**Contexte** : demande utilisateur - les agents n utilisent pas les outils
correctement car ils ne lisent pas le .md de documentation qui accompagne
chaque outil. La REGLE ABSOLUE du protocole-outils et celle des 11 cartes
existaient mais n etaient PAS mecanisees : aucune protection dans le template
ne les imposait. DECISION UTILISATEUR : severite BLOQUANTE - le mode reel
exige --confirme-doc.

**Actions** :
1. outil-template.py v0.2.0-beta : bloc DOC OBLIGATOIRE - verifier_doc_presente()
   (le .md du meme dossier doit exister, sinon refus code 2),
   exiger_confirmation_doc() (mode reel sans --confirme-doc : affiche la
   section Utilisation du .md + refus code 2), options --doc (affiche le .md
   complet) et --confirme-doc, appel en tete de main().
2. outil-template.sh v0.2.0-beta : meme bloc en bash (parite verifiee sur les
   4 cas : refus 2, confirme 0, dry-run 0, --doc affiche).
3. outil-template.md + outil-template-python.md : section REGLE IMMUABLE
   documentation obligatoire + options + historique 0.2.0.
4. protocole-outils : REGLE ABSOLUE de lecture MECANISEE (v0.2.0, severite
   bloquante, --confirme-doc requis en mode reel).

**Preuves reelles** : sans --confirme-doc -> rc=2 ; avec -> rc=0 ; --dry-run
libre -> rc=0 ; --doc affiche le .md ; preuve negative : .md manquant ->
rc=2 (documentation manquante). Parite .py/.sh validee.

**Lecon (bug v0.1)**: j ai d abord ecrit exiger_confirmation_doc(script, dry_run)
sans le flag confirme_doc -> --confirme-doc ne passait PAS la protection
(rc=2 au lieu de 0). Le test reel immediat a revele le bug avant transmission.
Lecon : une protection doit TOUJOURS etre testee dans ses 4 etats (refus,
confirmation, dry-run, cas negatif) avant de la valider.

**Pour Morpheus** : creer le garde-fou test-054 (anti-recurrence) : le
template outil-template.py ET .sh contiennent le bloc DOC OBLIGATOIRE
(verifier_doc_presente, exiger_confirmation_doc, --confirme-doc) + preuve
negative (bloc retire -> KO). Aucun test existant (029/050) ne touche
outil-template : pas d adaptation necessaire de mon cote.

## [LECON] 2026-08-15 -- THEME ameliorer-test CREE (Vulcain, ligne amelioration)

**Contexte** : demande utilisateur - le domaine TESTS n avait pas de theme
d amelioration dedie dans generateurs-amelioration (seul ameliorer-outil existait).
La ligne amelioration de Cerberus (c19b -> c19c generateur d abord -> c19d agent
habilite) a ete respectee : checklist ameliorer-outil validee (14/14) puis activation.

**Creation** : theme `ameliorer-test` ajoute dans themes-amelioration.json
(version 2.2.0 -> 2.3.0, 12 themes) : agent_habilite morpheus (regle immuable :
seul Morpheus ecrit les tests), 12 questions (5 rappels strategiques + 7 techniques
domaine tests : template-test v0.3.0 + protections importees, preuve negative reelle,
bump version + tests de version, garde-fou anti-recurrence, seul Janus lance la
non-regression, normes + registre, lecon). Doc generateurs-amelioration.md a jour
(12 themes, historique themes 2.3.0).

**Verifications** : --liste 12 themes, --version themes v2.3.0, structure du theme
valide (12 questions id/question/raison), normes 0/0.

**Impact documente (adaptation Morpheus)** : test-008 point 1 fige 'themes v2.2.0'
dans --version -> KO ATTENDU (18 OK / 1 KO), a adapter vers v2.3.0. Les points 3c/3d
(ameliorer-outil 14 questions) restent verts.

**Lecon** : la ligne amelioration est le bon chemin pour TOUTE demande d amelioration
- un theme dedie par domaine (tests vs outil) permet a la checklist du generateur de
porter les regles specifiques du domaine (ici : template-test, preuve negative,
gouvernance seul Janus). Ne jamais court-circuiter le generateur d abord (Pattern 17).


## [LECON] 2026-08-15 -- CHRONO EN HAUT DES SCRIPTS TEMPORAIRES v0.2.2 (Vulcain)

**Mission** (Cerberus, ligne amelioration, theme ameliorer-outil, decision
utilisateur BUFFER TOTAL) : le chrono des scripts temporaires doit etre
affiche TOUT EN HAUT, visible a chaque execution.

**Fait** : generateurs-outil-temporaire v0.2.2 (.py + .sh, parite) - le squelette
genere utilise desormais un BUFFER TOTAL : toute la sortie est retenue en memoire
(StringIO + redirect_stdout), le chrono === CHRONO === est affiche EN PREMIER,
puis le contenu. Detail important : redirect_stdout ne capture PAS les
sous-processus (ils heritent du descripteur terminal) -> declarer_usage capture
la sortie d enregistrer-usage-outil (capture_output=True) et la bufferise, sinon
les lignes [OK] Usage enregistre sortaient AVANT le chrono.

**Preuve reelle** : script genere + execute -> === CHRONO : total Xs === est la
TOUTE PREMIERE ligne, puis la logique, puis la declaration. test-050 adapte
(v0.2.2 + point 5b : CHRONO premiere ligne, 18/18), test-049 11/11, test-024
15/15, scan global 0 suspect, normes 0/0, 0 residu.

**Lecon technique** : quand un script bufferise sa sortie pour reordonner
l affichage, il faut aussi capturer la sortie de SES sous-processus (sinon ils
percent le buffer). Le triplet (point_actif/chrono_etape/bilan_chrono) et les
options (--no-chrono/--isoler/--desactiver/--dry-run) restent fonctionnels.

## [LECON] 2026-08-15 -- METTRE-A-JOUR-VERSIONS : LE BUMPER SYSTEMATIQUE (Vulcain)

**Contexte** : demande utilisateur "les agents aussi ont le droit a un bumper".
Les bumps de version etaient manuels, partiels et repetitifs (spec oubliee,
en-tete perime, compteurs de tests casses).

**Outil cree** : cerveau-projet/agents/tools/mettre-a-jour/mettre-a-jour-versions/
(py + md, entree catalogue 154->155, entree index-tools Mettre a jour 1->2,
total 172->173). Formats supportes : .py (en-tete + constante), .sh (en-tete +
variable), .md/spec (**Version :**), parcours JSON, fiche PARCOURS (vX.Y.Z),
protocole (frontmatter), version-readme.txt, catalogue JSON.

**Decouvertes** :
1. INCOHERENCES GENERALISEES : la quasi-totalite des outils ont un en-tete
   `# Version :` PERIME vs la constante VERSION a jour (ex : editer-fichier
   sh en-tete 0.3.0 vs variable 0.4.1 ; ajouter-contenu-fichier en-tete 0.2.0
   vs constante 0.3.0 ; detecter-usage-scripts-temporaires en-tete 0.1.0 vs
   0.1.1). Le bumper les DETECTE et refuse de bump avant correction : c'est
   exactement le service attendu. A traiter : un scan --tous futur pour
   lister et corriger ces ecarts pre-existants.
2. Les en-tetes .py sont dans un docstring `Version : X.Y.Z` (sans #) alors
   que les .sh ont `# Version :` : le motif doit accepter les deux formes.
3. Le champ version des protocoles est INDENTE (`  version: "X.Y.Z"`) : le
   motif doit accepter l indentation.
4. Le test-007 fige les compteurs catalogue (154) et index-tools (172) :
   ajouter un outil casse le point 13/14 -> adaptation Morpheus obligatoire
   (mission pre-vue).
5. Lecon de conception : utiliser des regex nommees (dict MOTIFS) plutot
   qu'une liste indexee par position (bug d index MOTIFS[5]/[6] corrige en
   cours de route).


## [LECON] 2026-08-15 -- OPTION --TOUS DU BUMPER + CORRECTION DES EN-TETES PERIMES (Vulcain)

**Contexte** : demande utilisateur - lancer un scan --tous du bumper pour corriger les en-tetes de version perimes.

**Ajout au bumper (mettre-a-jour-versions v0.1.0 -> v0.1.1)** :
- Option --tous : scanne TOUS les dossiers outils (cerveau-projet/agents/tools/*/*/), audite les incoherences
  de version par outil (dry-run par defaut), --wet corrige.
- Reference = constante VERSION du .py (source de verite a jour) ; en-tetes .py/.sh et doc .md alignes dessus.
- Ne scanne QUE les fichiers principaux (basename == nom du dossier) : tester-*.sh, *-test.md, spec/ exclus
  (versions documentaires = faux positifs).
- Suffixes -py/-sh/-beta : regex elargies (groupe 1 = version pure, suffixe conserve par le remplacement).

**Corrections appliquees (--tous --wet)** : 30 outils avec en-tetes perimes alignes sur leur constante
(ex : combos-moteur 0.1.0 -> 0.3.2, migrer-identite 0.1.0 -> 0.2.2, editer-fichier .sh 0.3.0 -> 0.4.1).

**Faux positifs decouverts et corriges dans le bumper** :
1. .md documentaires : les exemples de code ('# Version : 0.1.0', '"version": "0.1.0"') etaient detectes
   comme versions -> filtre par type de fichier (detecter_versions_type : seuls les motifs du type).
2. Tableaux de doc : '**Version :** 0.4.1' en exemple -> regex md exige le DEBUT DE LIGNE.
3. Ma propre doc bumper : exemples de format utilisaient de VRAIES versions (0.4.1/0.4.5) -> remplacees
   par X.Y.Z fictives (meilleure pratique).

**Validations** : rescan --tous 0 incoherence, detecter-divergences-version 0 DIVERGENTE (23 ALIGNEES),
py_compile OK sur tous les outils, normes 0/0 ASCII + LF, test-007 15/15, test-024 15/15, test-028 8/8,
test-040 5/5, detecter-usage-outils-externes 0 signe.

**Lecon** : un scan de versions doit distinguer la version RELLE d'un fichier (en-tete, constante, champ doc
en debut de ligne) des EXEMPLES de format dans la documentation. La constante du .py est la source de verite ;
les en-tetes perimes sont un symptome de bump sans bumper (exactement ce que la case c6a/c12a systematise desormais).


## [LECON] 2026-08-15 -- BUG JOURNALISATION GENERATEURS-COMMANDE CORRIGE (Vulcain)

**Contexte** : le bug s etait reproduit 4 fois (lecon Janus) - generateurs-commande journalisait
le NOM DE COMMANDE du catalogue au lieu de son propre nom, chaque activation via le generateur
creait un OUTIL_HORS_CARTE artificiel (activer-activer) corrige manuellement par Janus.

**Correctif v0.2.4 -> v0.2.5** : _journaliser_usage passe maintenant 'generateurs-commande' (son
propre nom) au lieu de commandes.get('nom') - le champ 'commande' du registre conserve la commande
generee complete (veracite). Preuve reelle : generation de test -> entree registre
outil=generateurs-commande, 0 occurrence activer-activer restante dans le registre.

**Decouverte en route** : ma propre generation de test (mode generateur, agent=vulcain) a cree une
entree generateurs-commande pour vulcain absent de sa carte -> indice outil ajoute a la case c15d
(Activer l agent habilite pour l amelioration, Pattern 17), parcours vulcain 0.4.11 -> 0.4.12.
Carte CONFORME, cablages 57/57, test-035 8/8, test-055 12/12.

**Lecon** : quand on corrige un generateur, TOUJOURS le tester reellement (generation + verifier
l entree registre creee) - le test prouve que la correction agit sur le registre, pas seulement
sur le code. Et toute generation cree une entree pour l agent actif : verifier test-035 apres.


## [LECON] 2026-08-15 -- FICHIER .TMPIGNORE + DETECTER-RESIDUS v0.1.3 (Vulcain)

**Contexte** : demande utilisateur - les dossiers temporaires de mission tmp-<agent> doivent
pouvoir etre autorises a rester sans declencher les tests, via un fichier .tmpignore.

**Decision utilisateur** : derrogation CIBLEE (noms EXACTS autorises) + emplacement
cerveau-projet/agents/traces/.tmpignore (a cote des registres).

**Travail effectue** :
1. Creation de cerveau-projet/agents/traces/.tmpignore (format documente : un nom exact par
   ligne, # commentaires, ASCII strict, LF, usage mission courante uniquement).
2. detecter-residus v0.1.2 -> v0.1.3 : fonction lire_tmpignore(racine) + integration dans les
   3 points de scan (niveau racine zone workspace, prune du walk zone cerveau-projet, prune du
   walk zone workspace) - un dossier liste est ignore, tout autre temp reste TEMP.

**Preuve reelle (derrogation ciblee)** : dossier tmp-test-ignore cree + liste dans le .tmpignore
-> detecter-residus ne le signale plus ; retire du .tmpignore -> redetecte (TEMP 2). La
protection anti-residus reste forte : seul le nom exact liste est autorise.

**Lecon** : une derrogation ciblee (liste de noms exacts) preserve la force du garde-fou tout en
offrant l assouplissement demande - a la difference d un motif global (ex tmp-*) qui affaiblirait
la detection de vrais residus.

## [LECON] 2026-08-15 -- PROTECTION DE SORTIE LF DANS L ENTONNOIR (Vulcain)

**Contexte** : demande utilisateur - des CRLF reapparaissaient malgre la regle LF obligatoire. Cause racine : les appends directs dans les scripts temp (io.open f a sans newline) traduisent LF en CRLF sur Windows - l outil ajouter-contenu-fichier est protege mais pas les scripts temp.

**Correctif** : entonnoir v0.1.1 - apres l execution, normaliser_fichiers_modifies scanne les fichiers du projet modifies pendant la fenetre d execution et les re-normalise (CRLF -> LF). BUG LATENT corrige au passage : normaliser() re-assignait brut apres le replace CRLF, donc la comparaison nouveau != brut ne declenchait JAMAIS l ecriture quand il n y avait que des CRLF.

**Preuves reelles** : script temp avec append non protege -> [SORTIE-LF] 1 fichier re-normalise, CRLF 0 / LF 2 (via .py et .sh). Preuve negative vivante : mes propres scripts de fin de la mission .tmpignore (lances en python3 direct, pas par l entonnoir) avaient reintroduit des CRLF dans janus/corrections.md - d ou la lecon : TOUJOURS passer par l entonnoir.

## [LECON] 2026-08-15 -- GARANTIE LF GENERALISEE AUX OUTILS (Vulcain)

**Contexte** : demande utilisateur - generaliser la protection LF a tous les outils qui ecrivent dans le projet (suite a la lecon entonnoir : write_text sans newline traduit LF en CRLF sur Windows).

**Correctif** : 13 write_text + 1 io.open sans newline corriges dans combos-analyse-projet, combos-audit-general, combos-corriger-non-ascii, combos-maj-readme-massive, combos-moteur (py+sh), migrer-identite (py+sh), detecter-fautes-orthographe. Bumps : analyse-projet 0.1.2, audit-general 0.2.1, corriger-non-ascii 0.2.1, maj-readme-massive 0.1.4, moteur 0.3.3, migrer-identite 0.2.3, fautes-orthographe 0.1.1.

**Preuve reelle** : write_text sans newline -> CRLF=2 LF=2 sur Windows ; avec newline vide -> CRLF=0 LF=2. combos-audit-general --rapport produit un rapport en LF pur (CRLF 0 / LF 335).

## [LECON] 2026-08-15 -- SPECS ALIGNEES GARANTIE LF (Vulcain)

**Contexte** : les bumps de la mission garantie LF ont ete appliques aux outils mais PAS aux specs - test-028 signalait 2 DIVERGENTES. Alignees : combos-moteur spec 0.3.2 -> 0.3.3, migrer-identite spec 0.2.2 -> 0.2.3 (version + historique). Lecon : le bump d un outil DOIT TOUJOURS inclure la spec dans le meme round (Pattern 14) - la non-regression test-028 le verifie a chaque run.


## [LECON] 2026-08-15 -- ANTI-ACCUMULATION HISTORIQUE v0.5.6 + SOMME COMPTES README-DEV (Vulcain)

**Contexte** : demande Cerberus (suite constat utilisateur : AGENTS-historique rempli de doublons,
118 blocs DEMARRAGE pour 150 entrees). Le bug v0.5.4 de recollement avait colle les anciennes
raisons d activation derriere les entrees ; le fix v0.5.5 a repere AGENTS.md mais PAS
AGENTS-historique (1183 lignes de parasite : blocs DEMARRAGE en exces, missions entieres collees,
continuations orphelines des entrees purgees par la limite 150).

**Partie 1a - Nettoyage** : script nettoyer-historique (150 entrees conservees, 1 bloc DEMARRAGE
par MISSION avec le BON parcours, 0 bloc pour les BILAN Cerberus, 0 parasite). Validation sur
copie, puis application.

**INCIDENT (honnetete)**: un test unitaire de ajouter_historique (MAX=2) a execute la fonction
REELLE sur le VRAI fichier (variable globale non patchee) -> fichier tronque a 2 entrees, puis un
git checkout de restauration a ramene un HEAD plus ancien (00:52) que le working tree nettoye
(10:52) : les entrees de la matinee (missions bumper/LF/entonnoir/badges + activations) ont ete
perdues du fichier. RECONSTRUCTION factuelle depuis le registre des usages (heures+agents+contextes)
+ lecons corrections.md + AGENTS.md/tmp-cerberus (raison exacte mission actuelle) : 33 entrees
reconstruites, inserees en tete (ordre decroissant), 150 total, normes 0/0. LECON : JAMAIS de test
qui execute la fonction reelle sur le vrai fichier - toujours patcher la variable globale ou
utiliser une COPIE (variable d env AGENTS_HISTORIQUE).

**Partie 1b - Protection v0.5.6** : ajouter_historique (py + sh) purge desormais les continuations
(blocs DEMARRAGE, raisons multi-lignes) AVEC l entree depassee (limite 150). Avant : les lignes
non-| date | etaient conservees sans limite -> accumulation. Test en memoire : nouvelle entree en
tete, 3 max, 0 continuation orpheline. Bump py/sh/md/spec 0.5.5 -> 0.5.6, test-028 8/8,
detecter-divergences 0 DIVERGENTES.

**Partie 2 - mettre-a-jour-readme v0.4.2** : anti-recurrence du bug Clio (compteurs 132 vs 134 :
une categorie manquante + une sur-comptee passaient inapercues car chaque ligne etait verifiee
separement). Nouvelle verifier_somme_comptes() : somme des compteurs du tableau readme-dev
(section 6) = total reel calcule + comparaison ligne par ligne. Branche dans --verifier et --maj
(controle final). PREUVE NEGATIVE : Detecter 13->12 -> [ECART] detecte + [ECART SOMME] 133 vs 134,
restauration -> [OK] 134. Bump py/sh/md 0.4.1 -> 0.4.2.

**Verifications** : test-025 11/11, test-028 8/8, test-020 46/46, test-038 7/7, normes 0/0,
0 residu.

VERDICT : VALIDE - AGENTS-historique propre (150 entrees, 0 parasite, 1 bloc/MISSION),
protection v0.5.6 testee, somme comptes readme-dev verifiee avec preuve negative.

FIN : lecon Vulcain + activer Morpheus (ma carte c15, chaine) pour tests de controle.

## [LECON] 2026-08-15 -- DETECTER-DONNEES-EN-DUR v0.1.0 (Vulcain)

**Contexte** : demande utilisateur (Cerberus) - creer un outil qui detecte les donnees en dur (nombres magiques, chemins, URLs, versions, compteurs/seuils) sources de bugs caches, avec recommandation du meilleur format de stockage (constante nommee en haut de fichier, JSON de configuration, liste dediee). Assignation decidee plus tard.

**Outil cree** : cerveau-projet/agents/tools/detecter/detecter-donnees-en-dur/ (py + md). Detections par type : NOMBRES_MAGIQUES, CHEMINS_EN_DUR, URLS_EN_DUR, VERSIONS_EN_DUR, COMPTEURS_SEUILS. Usage : 1+ chemins, --tous (scan projet), --rapport (markdown), --verbose, --version. Verdict SIGNAL/OK avec compteur. Catalogue 155 -> 156, index-tools 173 -> 174 (categorie Detecter).

**Lecons apprises** :
1. Heuristiques trop larges = faux positifs massifs : premier scan --tous donnait 23627 doutes (COMPTEURS_SEUILS matchait 'max'/'total' n importe ou, CHEMINS matchait 'OK / 0 KO'). Il a fallu resserrer : COMPTEURS_SEUILS = affectation directe nom = nombre ; CHEMINS/URLS restreints aux fichiers de code (.py/.sh) hors commentaires ; dates exclues des NOMBRES_MAGIQUES. Resultat final : 954 doutes sur 874 fichiers = signal raisonnable.
2. Le .md documentaire utilise des liens relatifs legitimes : ne pas signaler chemins/URLs dans la doc, seulement versions repetees (desynchronisation possible).
3. Toujours passer les fichiers sources par l entonnoir (ASCII strict) : un accent introduit en ecriture directe a casse la compilation.
4. test-007 fige le total catalogue (155) et index-tools (173) : 2 KO attendus apres ajout d un outil - Morpheus doit adapter (155->156, 173->174).
5. Preuve reelle indispensable : echantillon temp avec 5 types de donnees en dur (2048 seuil, chemin, URL, version v0.7.3, timeout 30) -> detection 5/5, puis suppression (0 residu).

**Decision de conception** : l outil est un SIGNAL (avertissement), pas une erreur bloquante - les donnees en dur sont parfois legitimes (limite de parcours), le doute doit inciter l agent a verifier et choisir le bon format de stockage.

## [LECON] 2026-08-15 -- BARRIERES DE PASSAGE NON-REGRESSION v0.4.0 (Vulcain)

**Contexte** : demande utilisateur - revoir la philosophie de la suite anti-regression : des BARRIERES DE PASSAGE entre les series. Ordre par IMPORTANCE (FONDATIONS D ABORD, decision utilisateur) + mode SERIE STRICTE (decision utilisateur : plus direct, plus lisible qu un pool).

**Outils modifies** : tester-lancer-non-regression v0.3.4 -> v0.4.0 (py + md + catalogue).
- SERIES reorganisees par fondations : a=FONDATIONS (nommage/ASCII-LF/template/protections : test-007/029/030/042/043/044/049/050/052/054/055), b=PARCOURS ET VALIDATEURS (test-009/012/013/014/015/016/018/021/026/033/034/037/048), c=OUTILS ET COMBOS (test-001/002/003/004/005/006/008/010/011/017/019/020/022/023/040), d=REGISTRE ET TRACES (test-025/027/031/036/038/039/045/046/047/051), e=ANTI-RECURRENCE (test-024/028/032/035/041). Couverture 55 tests, 0 hors-serie, 0 doublon.
- NOUVEAU DEFAUT = mode BARRIERES : chaque serie s execute (executer_lot), il faut 100% VERT pour FRANCHIR la barriere (message BARRIERE FRANCHIE), si KO la barriere appelle la protection STOP (fail-fast) -> la suite s ARRETE (message BARRIERE BLOQUEE, series suivantes non lancees), rapport de la serie fourni pour constater/analyser/reparer, on relance. Toutes les barrieres passees -> rapport GLOBAL POSITIF.
- Options conservees : --parallele (ancien pool de workers round 12), --serial (passe serie simple sans barrieres, echelon de secours).

**Preuves realisees** (faux tests temporaires, jamais les vrais - regle delegation) :
1. Couverture : 55 tests, 0 hors-serie, 0 doublon (script temp d import des constantes).
2. Preuve serie verte : 1 OK / 0 KO, 0 non-lance.
3. Preuve KO en serie : fail_fast -> STOP, 1 non-lance.
4. Preuve flux global : KO en serie C -> A/B franchies, C BLOQUEE, D/E non lancees ; tout vert -> 5 barrieres franchies.
5. Normes 0/0 (py + md + catalogue), catalogue 156, py_compile OK.

**Lecons** :
1. LA PHILOSOPHIE BARRIERE : le KO doit ARRETER la suite immediatement (constater, analyser, reparer) au lieu de continuer betement - c est la protection STOP appliquee au niveau SERIE (et non plus seulement au niveau test).
2. IMPORTANCE > THEMATIQUE : les series etaient thematiques (combos, parcours...) ; elles sont desormais classees par FONDATIONS - ce qui protege la BASE (nommage, ASCII/LF, template, protections) passe en premier car si une fondation casse, tout est invalide.
3. SERIE STRICTE > POOL pour la lisibilite : l utilisateur a choisi la serie stricte (plus longue mais plus directe) - le pool reste en option --parallele, le mode par defaut change (decision utilisateur 2026-08-15).
4. TESTS A ADAPTER (Morpheus, liste fournie) : test-027 (point 4 version + point 7 Defaut = pool -> Defaut = barrieres), test-032 (point 2 Defaut = pool -> barrieres), test-031 (point 1 version), test-024 (point 6 version), test-051 (point 1 version). VERSION BUMP : 0.3.4 -> 0.4.0 (grep dans les 6 tests qui figent la version).
5. EDITER-FICHIER ne supporte pas les gros blocs multi-lignes avec accents dans la cible : utiliser un script temp passe par l entonnoir (ancre ASCII + decoupe par positions) pour remplacer une section entiere de doc.
## [LECON] 2026-08-15 -- VERROU D HABILITATION proteger-verrou-habilitation (Vulcain, round 19)

**Contexte** : demande utilisateur - une protection 'verrou' : quand un agent
utilise un outil, s il n est pas dans la liste des agents autorises, il est
prevenu qu il n est pas habilite et doit activer l agent habilite. Choix
utilisateur : verrou DIRECT (bloquant) + --agent obligatoire.

**Outil cree** : cerveau-projet/agents/tools/proteger/proteger-verrou-habilitation/
(.py + .md, categorie Proteger). Le verrou lit les CARTES de decision
(indices outil des parcours) comme source de verite - aucune liste en dur
(anti-derive, philosophie test-035/037/045). Verdict : OK (rc=0) si l outil
est dans la carte de l agent, BLOQUE (rc=1) sinon avec la liste des habilites
et la commande exacte d activation (cycle Cerberus -> agent habilite).

**Preuves reelles** : janus->non-regression OK, cerberus->non-regression
BLOQUE (rc=1 + commande d activation), hygie->supprimer-fichier OK (seule
carte avec supprimer-*), cerberus->supprimer-fichier BLOQUE, outil inconnu
BLOQUE, --agent manquant rc=2, --liste table complete, test-035 8/8 (aucun
OUTIL_HORS_CARTE : le verrou est une protection transversale, assignation
decidee plus tard), normes 0/0.

**Lecons** :
1. LA CARTE EST LA REGLE : le verrou ne stocke AUCUNE liste en dur - il lit
   les parcours a chaque appel. Une regle exclusive qui change = une carte qui
   change ; le verrou suit automatiquement (anti-derive).
2. DIRECT BLOQUANT > ALTERNATIVE : chaque fois qu un choix etait laisse a
   l agent (continuer quand meme), l agent a derive. Le verrou bloque sans
   option de contournement et donne LA commande d activation de l agent
   habilite (transformer un blocage en action correcte).
3. CODE DE SORTIE SIGNIFIANT : rc=0 OK / rc=1 BLOQUE / rc=2 usage - les
   combos et scripts peuvent brancher le verrou en preambule et arreter net
   (protection STOP) si rc != 0.
4. CATEGORIE NOUVELLE Proteger : l index-tools et le catalogue acceptent une
   categorie supplementaire (sections alphabetiques, stats, total 174->175,
   catalogue 156->157) - verifier les tests qui figent les compteurs
   (test-007, test-024) + le badge README (135->136, mission Clio).

**A faire par Morpheus** : garde-fou test (le verrou existe, compile, bloque
un agent non habilite en PREUVE NEGATIVE, laisse passer l habilite) +
adaptation test-007 (156->157, 174->175) et test-024 (156->157). Badge README
135->136 : mission Clio (regle exclusive). Non-regression : Janus.


## [LECON] 2026-08-15 -- VERROU HABILITATION BRANCHE DANS LES OUTILS CRITIQUES (Vulcain)

**Contexte** : demande utilisateur - chaque outil critique exige --agent et
appelle proteger-verrou-habilitation AVANT d agir (verrou DIRECT bloquant,
decision utilisateur : direct + --agent obligatoire).

**Outils branches (4 fichiers, source de verite = cartes, aucun doublon de
table)** :
1. tester-lancer-non-regression 0.4.0 -> 0.4.1 : --agent deja present
   (journalisation), ajout appel verrou au debut de main() AVANT toute action.
2. supprimer-fichier 0.3.1 -> 0.3.2 : --agent OBLIGATOIRE ajoute (parsing
   manuel restructure en boucle indexee) + verrou avant la suppression.
3. supprimer-dossier 0.2.0-py -> 0.2.1-py : idem (boucle indexee existante).
4. combos-maj-readme-massive 0.1.4 -> 0.1.5 : --agent ajoute a argparse +
   verrou avant l etape 1.

**Patterns reutilises** : fonction verrouiller_habilitation(agent, outil) qui
appelle le verrou via subprocess ([sys.executable, verrou, --agent, --outil]),
detecte la racine AGENTS.md en remontant depuis __file__, rc 0 = habilite,
1 = bloque (affiche la sortie du verrou : qui est habilite + commande
d activation), 2 = --agent absent.

**Preuves reelles (rc attendus)**
- lanceur : janus rc=0 / cerberus rc=1 BLOQUE + commande / absent rc=2
- supprimer-fichier : hygie rc=0 / cerberus rc=1 / absent rc=2
- supprimer-dossier : hygie rc=0 / cerberus rc=1 / absent rc=2
- combos-maj : clio rc=0 (combo execute, badge README 133->136 aligne
  automatiquement) / buffy rc=1 / absent rc=2
- valider-cartes 13/13 CONFORME, test-056 8/8, test-037 6/6, test-045 15/15
  (verts : utilisent le verrou correctement)

**Impacts tests (mission Morpheus, seul habite a ecrire les tests)** :
les tests qui appellent les outils branches SANS --agent cassent (verrou rc=2) :
- test-020 (8 KO : version 0.1.4->0.1.5 + appels combos-maj sans --agent)
- test-024 (1 KO), test-027 (5 KO), test-031 (2 KO), test-051 (2 KO)
Les tests VERTs (ne pas casser) : test-029, 030, 034, 037, 045, 056.

**Lecons** :
1. Le catalogue ne porte la version que de 3 commandes (editer-fichier-agents,
   generateurs-case, generateurs-case-convertir) - les 4 outils branches n y
   sont pas versionnes, la version vit dans .py/.md. Ne pas chercher a bumper
   le catalogue pour eux.
2. Une seule mention d outil dans un message (combos-analyse-projet,
   generateurs-outil-temporaire) n est PAS un appel - verifier subprocess/run
   reel avant de craindre une casse de chaine.
3. Le verrou bloque aussi les tests qui appellent les outils sans --agent :
   c est le comportement voulu (l agent appelant doit etre connu). Les tests
   doivent passer --agent (janus/hygie/clio) - adaptation Morpheus.
4. --version/--help restent accessibles SANS --agent (innocents) ; toute
   action reelle exige --agent (rc=2 si absent).


## [LECON] 2026-08-15 -- --series MULTI AU LANCEUR DE NON-REGRESSION (Vulcain)

**Contexte** : demande utilisateur - Janus doit pouvoir ne lancer que les
series necessaires (pas toujours la suite complete). Mono --series a deja
existe ; ajout du MULTI (--series a,c).

**Fait (tester-lancer-non-regression 0.4.1 -> 0.4.2)** :
1. --series accepte une liste separee par des virgules (a,c) en plus de mono
   et de tous. Choix argparse retire (validation manuelle -> serie inconnue =
   rc=2 avec message explicite).
2. Les series sont lancees dans l ORDRE D IMPORTANCE (SERIES_ORDRE : A
   Fondations d abord) quel que soit l ordre saisi (--series c,a lance A puis C).
3. FAIL-FAST entre series : si une serie a un KO ou des non-lances, la suivante
   ne se lance pas (philosophie barriere, meme que --tous).
4. Protection du registre UNE fois (comme --tous), pas par serie.
5. Chrono couvre toutes les series ; no_reference=True (comportement mono).
6. Rapport combine (libelle "Series A,C").

**Preuves reelles** :
- --series z : rc=2 "Serie(s) inconnue(s) : z (valides : a,b,c,d,e)"
- --series a (mono) : rc=0 12/12 (regression)
- --series a,c (multi) : rc=0, lance A (12) PUIS C (15)
- --series c,a : lance A PUIS C (ordre d importance)
- --series e,a : lance A PUIS E
- test-032 : 9 OK / 1 KO (seul le point version fige 0.4.1 -> a adapter)

**Impacts tests (mission Morpheus)** :
- test-027 : point 4 version 0.4.1 -> 0.4.2 ; point 5 --series z : attendait
  "usage:" d argparse (choices retire) -> attendre maintenant "Serie(s)
  inconnue(s)" + rc=2 (le message d erreur a change, le comportement rc=2 est
  conserve)
- test-032 : point 1 version 0.4.1 -> 0.4.2 (1 KO)

**Lecon** : retirer choices d argparse change le message d erreur des tests qui
verifiaient l ancien message "usage:" - verifier les tests qui testent les
valeurs invalides lors d un changement de parsing.

**Chaine** : ce round demontre la regle rehabilitee (tout dans le meme round) :
Cerberus -> Vulcain (implemente + preuves) -> Morpheus (tests) -> Janus
(non-regression) -> Cerberus, SANS arret entre les maillons.


## [LECON] 2026-08-15 -- ORDRE DYNAMIQUE DES SERIES PAR TAUX DE KO (Vulcain)

**Contexte** : demande utilisateur - les series qui produisent le plus de KO
doivent passer en premier (critere de classement = frequence de KO, pas
l ordre historique).

**Fait (tester-lancer-non-regression 0.4.2 -> 0.4.3)** :
1. Fonction ordre_series_par_ko(racine, nb_derniers=5) : lit le registre-tests
   (serie + verdict par test), calcule le taux de KO par serie, classe par KO
   decroissant. Seuil de confiance : une serie n est reclassee que si elle a
   >= 5 lancements (sinon position historique conservee - pas assez de donnees
   pour juger).
2. Option --ordre-fixe : force l ordre historique (a,b,c,d,e).
3. Mode barriere : utilise l ordre dynamique (ou fixe), affiche
   "[ORDRE SERIES] X > Y > ..." pour transparence.
4. Mono/multi/fail-fast : conserves (regression test-027/032).

**Preuves reelles** :
- Ordre dynamique (registre : e=3 KO/106, c=2 KO/11) : [ORDRE SERIES] E > C > A > B > D
  -> E et C (les plus de KO) passent en premier, A/B/D (pas assez de donnees)
  restent en ordre historique. REPOND EXACTEMENT a la demande.
- --ordre-fixe : [ORDRE SERIES] A > B > C > D > E
- mono --series a : 12/12 (regression) ; multi --series a,c : A puis C (regression)

**Impacts tests (mission Morpheus)** : 5 tests figent la version lanceur 0.4.2
-> a adapter 0.4.3 : test-024, test-027, test-031, test-032, test-051.
Les tests 005/010/016/022 referencent 0.4.2 d AUTRES outils (atlas,
generateurs-case) - NE PAS y toucher.

**Lecon** : le classement par taux de KO utilise le registre-tests comme source
de verite - les donnees s accumulent a chaque run, l ordre evolue naturellement
vers les series a risque en premier.

## [LECON] 2026-08-15 -- CONFIG PERSISTANTE DES TESTS (tester-lancer-non-regression v0.4.5, Vulcain)

**Contexte** : demande utilisateur - Janus doit pouvoir activer/desactiver des tests par
numero pour ne lancer que les series utiles au controle en cours (ex : on travaille la
fleur rouge, le test de la fleur bleue n a pas besoin d etre lance).

**Implementation** :
1. Fichier persistant `config-tests.json` (gitignore, machine-independante comme
   temps-reference.json) stocke la liste des numeros de tests desactives.
2. Options `--desactiver <a,b>` / `--activer <a,b>` (numeros) + `--etat-tests`
   (affiche l etat de tous les tests puis sort sans rien lancer).
3. Au lancement, la config est lue et les tests desactives sont exclus AVANT le
   decoupage en series -> une serie ne devient jamais vide fautivement.
4. Bilan : les tests desactives apparaissent en `NON LANCE` dans les 2 modes
   (tous + series demandees).
5. Les fonctions pures (charger/sauver/filtrer) sont testables sans le verrou.

**Lecon** : la persistance par fichier gitignore (comme temps-reference.json) est le
bon pattern pour une configuration machine-dependante heritee entre lancements. Les
fonctions pures detachees du flux principal permettent un test unitaire rapide sans
passer par le verrou d habilitation.

**Attention** : 6 tests pincent la version v0.4.4 du lanceur (016, 024, 027, 031, 032,
051) - Morpheus les adaptera a v0.4.5.

## [LECON] 2026-08-15 -- 2 OUTILS D ANALYSE : PERFORMANCE DES TESTS + TOKENS (Vulcain)

**Contexte** : demande utilisateur - (1) un outil de performance qui classe les
tests du plus gros consommateur au moins pour optimiser la suite anti-regression ;
(2) un outil de mesure des tokens (envoyes/recus/encombrement de la fenetre) +
integration templates + migration progressive.

**Outils crees** (categorie analyser) :
1. `analyser-performance-tests` v0.1.0 : lit registre-tests.jsonl, isole le
   DERNIER RUN (fenetre 10 min autour de la date max, --fenetre-minutes),
   classe du plus gros consommateur au moins (--top), rapport markdown avec
   duree cumulee (--rapport). Preuve : registre simule 5 tests -> 032 (38.7s)
   > 028 (25.2s) > 031 (6.3s) > 024 (3.1s) > 001 (1.2s), ordre exact.
2. `analyser-tokens` v0.1.0 : MODELE HYBRIDE (decision utilisateur) - compteurs
   API reels en priorite (TOKENS_SESSION ou metadonnees-session-*.json),
   sinon estimation locale (registres + traces, ~4 car/token, 60/40). Sortie :
   envoyes, recus, total, encombrement %. Preuve : TOKENS_SESSION simule ->
   45000/12000 -> 44.5% sur 128k ; sans metadonnees -> estimation signalee.

**BUG CRITIQUE DECOUVERT (a corriger par Morpheus)** : test-051 (point 8)
nettoie ses preuves en supprimant TOUTES les entrees agent == "janus" du
registre-tests - y compris les VRAIES entrees du run complet de la
non-regression ! Le registre ne garde que l entree de test-051 lui-meme
(journalisee apres son nettoyage). C est pourquoi le registre-tests n a que
106 entrees (dont 105 morpheus isolees) au lieu de milliers. L outil
analyser-performance-tests ne pourra pas analyser les runs complets tant que
ce bug n est pas corrige.

**Templates mis a jour** (bloc tokens PILOTE optionnel, migration progressive) :
template-test.md, outil-template.md, outil-template-python.md,
fiche-agent-template.md, protocole-creation-scripts-temporaires. Tests 029
(14/14) et 044 (15/15) toujours verts - ajout additif sans casser le triplet.

**A adapter par Morpheus** : test-007 (catalogue 159->161, index-tools
177->179). **A faire par Clio** : badge README Outils-138 -> 140 + readme-dev
table Analyser 2 -> 4 (SEUL Clio touche aux README - regle immuable).

**Lecon** : ecrire un .py en write_file avec intention ASCII ne garantit pas
l ASCII (un accent a ete insere dans "reperer") - toujours verifier
non-ascii/crlf apres creation. Le registre-tests est la source de l outil de
performance : sa fiabilite conditionne les decisions d optimisation.
