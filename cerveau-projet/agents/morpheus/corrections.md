---
identite:
  type: corrections
  appartient_a: morpheus
  commun: false
# Corrections de Morpheus

agent: "morpheus"
version: "0.1.0"
derniere_mise_a_jour: "2026-08-06"

---

# Corrections Morpheus

## Corrections en cours

Aucune correction en cours.

---

## Historique des corrections

| Date | Correction | Raison |
|---|---|---|
| 2026-08-06 | Creation | Agent cree pour les tests |
| 2026-08-07 | Tests formels de remplacer-texte (6/6) | Vulcain avait teste lui-meme sans m activer (faute de processus). J ai couvert l etape tests : test-001-remplacer-texte.sh avec les 3 protections sourcees |
| 2026-08-07 | Tests formels de activer-agent-principal v0.3.0 (12/12) | Multi-session LLM : migration, sidentifier, isolation des sessions, parite sh/py, ASCII, historique 4 colonnes. 2 bugs detectes et corriges (persistance de la migration dans le .py, message d identification apres migration) |
| 2026-08-07 | Tests formels de activer-agent-principal v0.3.1 (7/7 + regression 12/12)
| 2026-08-07 | Tests formels de activer-agent-principal v0.3.4 (19/19) | MODE ID : chaque LLM a SON id, sidentifier <llm-id> compare l id aux lignes profil-session du classeur (id: <llm-id>). Id connu = SA session (redemarrage), id inconnu = prochaine session libre + liaison. Isolation garantie par id (jamais 2 LLM sur la meme session). Le test 6b verifie que le mode heritage (sans argument) n ajoute PAS de liaison id. Lecon : quand une regle repose sur une LIAISON persistante, tester le redemarrage (meme id -> meme session) ET la non-collision (2 ids differents -> 2 sessions) |
| 2026-08-07 | Tests formels de activer-agent-principal v0.3.5 (28/28) | CORRECTION BUG MAJEUR (sessions fantomes) : la liaison id<->session posee par sidentifier etait ECRASEE par activer/reactiver (mettre_a_jour_profil_session sans llm_id reecrivait la ligne classeur sans le champ id). Test-005 : liaison id PRESERVEE apres activer + reactiver + redemarrage retrouve SA session (1 seul bloc, pas de doublon profil) + isolation 2 LLM + parite .sh + regressions v0.3.2/0.3.3/0.3.4. LECON : les tests 001/002/003 echouaient sur des cas pre-existants (semantique sidentifier changee en v0.3.3/0.3.4 : l argument n est plus un nom de session mais un id LLM) -- verifie par comparaison v0.3.4 originale (memes echecs, 7/5, 7/1, 17/4) -> echecs PRE-EXISTANTS, pas de regression v0.3.5. Lecon : avant d attribuer un echec de regression a sa correction, TOUJOURS re-executer les memes tests avec la version precedente (git show) pour comparer
| 2026-08-07 | CORRECTION TESTS OBSOLETES test-001/002/003 (regression 001-005 100% VERTE : 12/12 + 8/8 + 22/22 + 19/19 + 28/28) | Mission : aligner les tests 001-003 sur la semantique v0.3.5 (MODE ID - sidentifier <id-llm>). CORRECTIONS : (1) test-001 : structure ANCIENNE mono-session -> structure multi-session VIDE (comme 003/004/005) ; sidentifier session-llm-5 -> sidentifier llm-atlas (prochaine libre + liaison id) ; ajout export CLASSEUR_STOCKAGE (le test-001 ecrivait dans le VRAI classeur sans cet export -> effet de bord profil-session-llm-1 !). (2) test-003 : tests 3/4/7c de l ANCIENNE regle (session occupee -> message 'deja attribuee a un autre LLM', remplacee par MODE ID) -> reecrits : id inconnu = prochaine libre + liaison, redemarrage = retrouvee (pas de fantome), parite .sh idem. (3) test-002 : AUCUNE correction (son seul echec etait le Test 8 = cascade du test-001 echouant). DECOUVERTE (bug latent hors perimetre test) : sidentifier seul sur structure MONO-session ancienne ne PERSISTE pas la migration (le fichier reste mono-session : le bloc cree par migration existe deja dans le contenu en memoire -> pas d ecriture). A signaler a Vulcain. Lecon : quand un test ancien echoue en regression, verifier s il prepare une structure OBSOLETE plutot que de chercher un bug de l outil |
| 2026-08-07 | Tests formels de activer-agent-principal v0.3.3 (21/21) | REGLE UTILISATEUR identification : fichier vide -> 1er LLM = session-llm-1, session occupee -> attribution AUTOMATIQUE de la prochaine libre avec message clair (jamais de reprise d un numero attribue). Tests sur copies. PIEGES DE TEST : grep -A2 trop court pour atteindre le champ Nom d un bloc -> utiliser awk par bloc ; grep -c || echo 0 doublait le 0 -> grep -c | grep ^0$ |
| 2026-08-07 | Tests formels de activer-agent-principal v0.4.0 (26/26) | REGLE ALIGNEMENT : id llm-N -> session-llm-N (le numero de session porte le numero de l'id, llm-1 -> session-llm-1), champ **Id LLM** dans chaque bloc AGENTS.md (reconnaissance par lecture), SOURCE DOUBLE (AGENTS.md champ Id LLM + classeur), CONFLIT si session-llm-N deja liee a un autre id (message ATTENTION + prochaine libre), ABSORPTION d'une session-llm-N orpheline (sans id), id non numerique (llm-atlas) -> prochaine libre, parite .sh, regressions v0.3.5/0.3.4/0.3.3/0.3.2. PIEGES DE TEST : (1) une sortie contenant une apostrophe (ex: 'l id') casse eval dans la fonction verifier -> ecrire la sortie dans un fichier et grep le fichier ; (2) dans un pattern grep, \| est l'ALTERNATION GNU (pas un pipe litteral) -> utiliser | simple entre guillemets pour matcher le champ | **Id LLM** | ; (3) grep -c || echo 0 double le 0 -> NB=$(grep -c ... 2>/dev/null); NB=${NB:-0}
| 2026-08-07 | Tests formels de activer-agent-principal v0.3.2 (8/8 + regression 12/12) | Regle de derivation du nommage : id = profil-session- + partie apres le prefixe session- (session-llm-1 -> profil-session-llm-1). BUG DECOUVERT : session[7:] retirait un caractere de trop ("session-" fait 8 caracteres) -> profil-session--llm-1 (double tiret) ; corriger avec session[len("session-"):]. Ajout d un test negatif (aucune ligne profil-session-session-*) - toujours verifier le NEGATIF pour valider une regle IMMUABLE
| 2026-08-07 | Tests formels de guide-parcours v0.1.0 (13/14 - 1 bug nommage signale) | GUIDE-PARCOURS (jeu de piste, Vulcain) : --liste 19 cases OK, navigation --reponses/branches OK, reponse inconnue -> erreur claire OK, --case OK, JSON invalide refuse OK, branche cassee refusee OK, py_compile + bash -n OK. BUG DETECTE (parite py/sh KO) : verifier_nommage du .sh exige que le nom commence par le PREFIXE DE LA CATEGORIE (dossier guider/ -> prefixe guider-) mais l'outil s'appelle guide-parcours (sans le r) -> le .sh refuse de demarrer. LE .PY accepte car il verifie le dossier de l'outil (guide-parcours -> prefixe guide-) : les deux verifications de nommage ne sont PAS identiques entre template .py et .sh - PIEGE A CONNAITRE pour tout nouvel outil dans une categorie multi-mots. A corriger par Vulcain : renommer en guider-parcours (dossier + fichiers + references + test + index-tools + fiche)
| 2026-08-07 | RETEST guide-parcours renomme guider-parcours (14/14 VALIDE) | 2 BUGS DETECTES ET CORRIGES par Vulcain apres mes retests : (1) NOMMAGE : l'outil guide-parcours dans le dossier guider/ violait verifier_nommage du .sh (prefixe attendu guider-) -> renomme en guider-parcours (dossier + 5 fichiers + references index-tools/fiche). (2) PARITE : executer_python du .sh lancait 'python3 << PYEOF' SANS transmettre $@ -> le script python recevait 0 argument ('chemin du parcours obligatoire'). CORRECTION : 'python3 - "$@" << PYEOF' (le - et $@ transmettent les args dans sys.argv[1:]). LECON : dans un .sh avec python embarque par heredoc, TOUJOURS transmettre les arguments : python3 - "$@" << 'PYEOF' sinon le python ignore completement la ligne de commande. VERDICT FINAL : 14/14 dont parite py/sh identique, --liste 19 cases, branches/reponses/--case/JSON invalide/branche cassee OK, ASCII 0 non-conforme, py_compile + bash -n OK
| 2026-08-07 | Tests formels de test-001-evaluer-agents-coherence (8/8) | Corrections Vulcain: (1) evaluer-agents exclut __pycache__ et dossiers de categorie -> score 23/100 a 97/100, (2) evaluer-coherence utilise projet root pour cible_racine -> faux positif lien structures resolu, (3) evaluer-coherence exclut commandes systeme (cat/grep/sed/basher) -> 0 faux positif. Test Python avec protections et assertions. Version py mise a jour. 
| 2026-08-08 | Tests formels de combos-moteur v0.1.0 (31/31 REUSSI) | MOTEUR DE COMBOS (etape 2 plan combo-orchestrateur, Vulcain) : test-002-combos-moteur.py dans tester/tests/test-002-combos-moteur/. COUVERTURE : --liste (5 cases, 4 types), navigation case_depart->fin (chemins OUI c4 / NON c5), interpolation {var} (sidentifier resolu dans echo), generateur AUTO (appel generateurs-commande --reponses, commande composee avec activer-agent-principal), controle branches via --reponses, variable manquante -> erreur claire code 1, dry-run ([DRY-RUN] affiche + outil PAS execute + navigation jusqu a la fin), parite .py/.sh (liste + navigation identiques), nommage OK, ASCII 0 sur 5 fichiers, bash -n + py_compile OK. BUGS DETECTES ET CORRIGES par Vulcain : (1) chemin_racine remontait 4 niveaux depuis le .py -> agents/agents/tools (il en faut 5 depuis le fichier, 4 depuis le DOSSIER dans le .sh via COMBO_MOTEUR_DIR - PIEGE PARITE fichier vs dossier) ; (2) extraire_commande_generateur prenait le texte sur la MEME ligne que le marqueur === COMMANDE A LANCER === (vide) au lieu de la ligne SUIVANTE ; (3) parite : le .py avec _couleur ajoutait un \n en trop dans === COMBO TERMINE === (double saut absent du .sh). LECON : dans un test, le chemin d appel d un .sh sur Windows doit etre prefixe par bash (run(['bash', MOTEUR_SH, ...]) sinon WinError 193). LECON dry-run : la navigation atteint quand meme la case fin en dry-run (normal) - la bonne assertion est que la COMMANDE OUTIL n est PAS executee, pas que le message de fin est absent. |
| 2026-08-08 | Tests formels de generateurs-case v0.1.0 (21/21 VALIDE) | GENERATEUR DE CASES (categorie generateurs/, Vulcain) : ajouter/editer/supprimer des cases de parcours JSON avec validation auto complete. COUVERTURE : nommage + chargement, py_compile + bash -n, parite --version py/sh, liste (21 cases), ajouter apres c8 (22 cases), editer (titre modifie), supprimer c8 AVEC RECABLAGE AUTO c7->c20 + c8 disparu, supprimer case fin sans --vers -> ERREUR, supprimer case fin avec --vers -> OK, dry-run sans modification, JSON invalide refuse, navigation guider-parcours sur copie modifiee -> PARCOURS TERMINE, ASCII 0 sur 3 fichiers, parite liste py/sh. 2 BUGS DETECTES et CORRIGES par Vulcain avant mes retests : (1) conflit --verbose declare 2 fois (sous-parser liste + boucle finale) -> argparse.ArgumentError ; (2) mode stdin du .sh : le shebang + cookie coding en tete du heredoc python cassait l execution (python3 - ignore le script), et Path(__file__).resolve().parents[2] leve IndexError en stdin (__file__ = <stdin>) -> corrige par env GC_RACINE calculee par le .sh (lecon : PAS de shebang/coding cookie dans un heredoc destine a python3 -, et PAS de __file__ en mode stdin). PIEGE DE TEST DECOUVERT : grep -A7 apres '"c7": {' ne suffit pas quand la case a plusieurs indices (le champ suivant est 24 lignes plus bas) -> utiliser -A30 ou plus (distance case -> champ suivant variable selon le nombre d indices) |
| 2026-08-08 | Tests formels de detecter-impacts v0.1.0 (15/15 VALIDE) | DETECTER-IMPACTS (categorie detecter/, Vulcain) + combo-controle-impacts + extension moteur combos-moteur v0.1.3 (--var). CONCEPT : l identification vit dans chaque fichier (frontmatter identite: type/appartient_a/commun), l outil calcule les impacts (meme appartient_a, ou references si commun) et compare les dates. COUVERTURE sur mini-cerveau /tmp : py_compile + bash -n (2 outils), parite --version py/sh, detection fichier non commun (corrections avec meme appartient_a), statut NON MIS A JOUR (mtime), fichier commun detecte par reference (nom dans le contenu), sans identite -> ERREUR code 2, introuvable -> ERREUR code 2, parite scan py/sh (au MEME instant), moteur --var fichier=<chemin> + combo jusqu a la fin, generateur compose la commande detecter-impacts, ASCII 0 sur les 10 fichiers (outil + moteur + catalogue + combo + index). LIMITE DOCUMENTEE v0.1.0 : l identite n est lue que dans le frontmatter YAML (---), pas dans les .json ni les .py/.sh (schema hybride a la v0.2.0 - decision utilisateur). PIEGE DE TEST DECOUVERT : pour comparer la parite py/sh d un scan, TOUJOURS lancer les 2 versions au MEME instant (une comparaison differee apres un touch modifie le resultat -> faux negatif) |
| 2026-08-08 | RETEST detecter-impacts v0.1.1 (16/16 VALIDE) | CORRECTION BUG usage reel (detecte par Buffy) : le fichier modifie apparait dans les impliques quand on lance SANS --racine. CAUSE : scanner retourne des chemins absolus, args.fichier reste relatif -> l exclusion ne matchait pas. CORRECTION Vulcain : .resolve() des 2 cotes avant comparaison (py + sh parite). RETEST : (1) CAS REEL sans --racine sur cerberus.md : source EXCLU (1 seule occurrence = ligne Fichier modifie), corrections.md detecte, (2) parite py/sh cas reel OK, --version v0.1.1, (3) REGRESSION mini-cerveau : non commun + NON MIS A JOUR, commun par reference, erreurs code 2 (sans identite/introuvable), (4) TEST FORMEL : PT12 ajoute (cas reel : source exclu + corrections detecte) -> 16/16. LECON : tester TOUJOURS un outil de scan dans son MODE REEL (sans --racine) en plus du mini-cerveau - les modes de test peuvent masquer les bugs de chemins (relatif vs absolu) |
| 2026-08-08 | Test formel valider-cartes-decision v0.3.0 (24/24 VALIDE) | CIBLE CHANGEe (Vulcain) : l outil validait la section Carte de Decision des fiches allegees -> --tous = 5/5 NON CONFORME a tort. Nouvelle cible : PARCOURS JSON (source de verite). COUVERTURE : --version py/sh 0.3.0, --tous = 11/11 conformes (avant 5/5 non), --agent cerberus/buffy CONFORME, --fichier parcours CONFORME, --fichier .md = NON CONFORME (mauvaise cible + mentionne le parcours), parcours corrompu = 3 erreurs (type invalide, reference cassee, c0 absente) + NON CONFORME, fichier inexistant = ERREUR, parite py/sh (--tous, --agent, --fichier parcours, --fichier .md), ASCII 0 sur 3 fichiers, nommage OK. LECONS : (1) PIEGE eval + variable a ESPACES : une commande $PY (avec espaces) dans une substitution $(...) passee a eval casse l evaluation -> precalculer la sortie dans une variable simple avant le verifier (compte_16=...) ; (2) PIEGE grep apostrophe : le message 'n existe pas' ecrit sans apostrophe (n existe) ne matche PAS la sortie reelle (n'existe) -> grep le fragment stable 'existe pas' ; (3) le .sh est un WRAPPER pur vers le .py (exec python3 ... "$@", pattern detecter-impacts) : parite stricte garantie par construction, aucun doublon d en-tete |
| 2026-08-08 | RETEST detecter-impacts v0.2.0 schema hybride (22/22 VALIDE) | EXTENSION par Vulcain : lire l identite dans les 3 formats (.md frontmatter YAML, .py/.sh commentaires en tete fenetre 12 lignes, .json cle top-level identite). RETEST : (1) .md frontmatter REGRESSION cas reel sans --racine : identite lue type=fiche-agent, corrections detecte, source exclu, (2) .py SANS bloc identite (detecter-impacts.py lui-meme) -> ERREUR code 2 : FAUX POSITIF ELIMINE (Vulcain a restreint la fenetre 60->12 lignes apres l avoir decouvert en test), (3) .py AVEC bloc identite lignes 3-7 -> identite lue type=outil + detecte comme implique + parite py/sh OK, (4) .json cle top-level (parcours) -> identite lue type=parcours + parite OK, (5) parite py/sh sur 4 formats OK, --version v0.2.0 les 2 versions, (6) REGRESSION mini-cerveau hybride : source .md -> 3 identiques dont le .py, source .py -> 3 impliques, commun par reference OK, (7) TEST FORMEL : PT13a-d (format .py) + PT14a-b (format .json) ajoutes -> 22/22. LECON 1 : la fenetre de 12 lignes pour le bloc identite en commentaires est LA convention (au-dela, un en-tete documentaire peut mentionner identite: et creer un faux positif). LECON 2 (DECOUVERTE UTILISATEUR - CHAINE CASSEE) : quand la carte d un agent se termine par une case FIN passive ("X teste et te reactive"), la delegation coupe la chaine et l agent delegue ne fait rien. La carte doit MATERIALISER la boucle (RELAIS -> RETOUR -> CLOTURE -> FIN). Corrige sur parcours-vulcain v0.2.1 (voir fiche vulcain) |

---

## Surcharges

### Limites

- Je n'ecris que des tests, je ne modifie pas les outils
- Je valide seulement via les tests, pas via l'inspection
- Je dois toujours reactiver Cerberus apres chaque mission
- Je ne suppose jamais, je verifie tout

### Protocoles specifiques

- [protocole-tests](../../agents/regles-immuables/general/protocole-tests/)
- [protocole-versionning-outils](../../agents/regles-immuables/general/protocole-versionning-outils/)

### Outils utilises

- `template-test` : Pour creer des tests
- `tester-protection-boucles-infinies` : Protection contre les boucles infinies
- `tester-protection-erreurs-silencieuses` : Protection contre les erreurs silencieuses
- `tester-protection-blocage` : Protection contre les tests qui bloquent

## [NOTES] Test 2026-08-08 -- CONTEXTE TEMPS REEL v0.4.1 (Vulcain) : lire-activite-recente + Sessions connues

**Mission** : tester 2 livrables de Vulcain (decision utilisateur, contexte temps reel avant la vague 2).
**Verdict** : VALIDE.
**Tests** :
1. lire-activite-recente v0.1.0 (py+sh+md, categorie lire/) : nommage OK (exit 0), py_compile + bash -n OK, --version identique py/sh, --nombre 3 PARITE OK (diff vide), --longueur 40 fonctionne, fichier inexistant -> code 1. L'outil lit les 15 dernieres interventions par defaut au format date | session | agent | action (action tronquee)
2. activer-agent-principal v0.4.1 (py+sh) : section '## Sessions connues' reconstruite a chaque sidentifier/activer/reactiver depuis le classeur (profil-session-*). B2 sidentifier llm-1 -> section creee avec session-llm-1 (id llm-1, agent Cerberus), B3 activer buffy -> agent mis a jour SANS doublon, B4 reactiver -> Cerberus, B5 toutes les sessions du classeur listees (llm-1, 3, 4, 5), B6 parite py/sh (AGENTS.md genere identique, diff vide)
3. REGRESSION : test-006 v0.4.0 rejoue en entier -> 26/26 VALIDE (aucune regression, les tests existants ne verifient pas l absence de la section)
4. ASCII : 0 non-conforme sur les 7 fichiers (py, sh, md x3, index-tools)
**Lecons** :
1. Le faux positif de doublon : grep -c '## Sessions connues' compte aussi la mention du texte dans la raison d'activation copiee dans AGENTS.md -- toujours verifier avec grep -n '^## Sessions connues$' (titre exact) pour confirmer qu'il n'y a qu'UNE section reelle
2. La section est idempotente : 2 activations successives -> toujours 1 seule section (retrait + reinsertion)
3. Le modele boucle Vulcain -> Morpheus -> Vulcain fonctionne : j'ai ete active par Vulcain, je le reactive a la fin (pas Cerberus)

## [NOTES] Test 2026-08-08 -- migrer-identite v0.1.0 (Vague 2, Vulcain)

**Mission** : tester l outil de migration vers le schema hybride v0.2.0 (decision utilisateur : tous commun:true, outil + dry-run, perimetre hors templates/tests).
**Verdict** : VALIDE.
**Tests** :
1. M1 : nommage valider-nommage py+sh OK (exit 0), py_compile + bash -n OK
2. M2 : --version identique py/sh (0.1.0)
3. M3 : mini agents/tools (Z:/tmp/mig-test, 10 fichiers dont 8 cibles) : --liste 8 fichiers types corrects (spec->spec, combos->combo, catalogue->outil, exemple-combo->combo), dry-run 7 migres/1 deja SANS ecriture, migration reelle 7 migres/1 deja, IDEMPOTENCE : 2e passage 0 migre / 8 DEJA
4. M4 : contenu verifie : .py bloc lignes 8-11 (dans les 12), .sh lignes 6-9, .md frontmatter en tete, spec type spec, .json cle top-level, tests/template EXCLUS intacts, PARITE py/sh identique, ASCII 0
5. M5/M5b : detecter-impacts v0.2.0 lit le bloc genere (.sh : type=outil, commun=true, OK)
6. M6/M7 : cas limite .py commencant par du code (sans en-tete) : bloc insere en tete sans casser le code, detecter-impacts lit l identite
**Lecons** :
1. Le chemin /tmp du shell Windows (AppData\Local\Temp) differe du Z:/tmp de write_file : pour tester detecter-impacts sur un fichier cree par script, utiliser le chemin absolu Z:/tmp/... (sinon 'fichier introuvable')
2. Le test M5 (chemin relatif /tmp) a cree un faux negatif : verifier le chemin reel avant de conclure a un bug
3. La boucle de validation complete (outil -> detecter-impacts qui lit le bloc genere) confirme que la migration atteint son but : le schema hybride est operationnel de bout en bout

## [NOTES] RETEST 2026-08-08 -- migrer-identite v0.1.1 (correction bug, Vulcain)

**Mission** : re-valider la correction du bug decouvert au dry-run reel (4 fichiers .md avec frontmatter custom marques DEJA a tort).
**Verdict** : VALIDE.
**Tests** :
1. R1 : py_compile + bash -n OK, --version py/sh = 0.1.1
2. R2 (test-frontmatter-special.py) : cas A frontmatter-sans-identite -> IGNORE et INTACT (pas de double frontmatter, contenu original preserve), cas B md normal -> MIGRE (frontmatter propre), cas C .md dans tests/ -> EXCLU, cas D template-test.md -> EXCLU, PARITE py/sh dry-run OK
3. R3 (regression mini 8 cibles) : --liste 8, dry-run 7/1, reel 7/1, idempotence 2e passage 0 migre/8 DEJA -- aucune regression
4. R4 (dry-run reel agents/tools/) : 281 migres + 5 deja + 1 IGNORE (detecter-usage-outils-externes-test.md) + 0 erreur + total 287 -- les 3 speciaux (template-test, test-001, test-002) hors scan
5. R5 : ASCII 0 sur les 4 fichiers modifies
**Lecons** :
1. Le dry-run reel AVANT application est essentiel : il a revele un bug invisible dans le mini-test (les cas reels de frontmatter custom ne sont pas couverts par un mini-cerveau idealise)
2. La protection frontmatter-sans-identite est la bonne strategie : plutot que de tenter de fusionner les frontmatters (risque), on IGNORE les fichiers speciaux -- aucun risque de double frontmatter
3. Verifier TOUJOURS le dry-run reel avant de laisser Buffy appliquer une migration massive

## [NOTES] RETEST 2026-08-08 -- migrer-identite v0.1.2 (correction long en-tete, Vulcain)

**Mission** : re-valider la correction du bug long en-tete documentaire decouvert par Buffy pendant l application reelle (bloc identite a la ligne 13, hors fenetre 12).
**Verdict** : VALIDE.
**Tests** :
1. M1 : py_compile + bash -n OK, --version py/sh = 0.1.2
2. M2 (test-long-en-tete.py) : bloc insere apres Statut (ligne 6-7, dans les 12) meme avec long en-tete documentaire, re-scan -> DEJA, PARITE py/sh OK
3. M3 (test-reparation.py, copie du VRAI detecter-impacts.py avec bloc a l indice 12) : REPARE-DRY puis REPARE, bloc deplace 12 -> 6, PAS DE DOUBLON (1 seul bloc), py_compile OK, detecter-impacts lit l identite, re-scan -> DEJA
4. M4 (regression frontmatter special) : cas frontmatter-sans-identite toujours IGNORE et INTACT, pas de double frontmatter
5. M5 (regression mini 8 cibles) : idempotence totale (2e passage 0 migre/8 DEJA), aucune regression
6. M6 (dry-run reel) : 17 REPARE-DRY + 269 DEJA + 1 IGNORE + 0 erreur + total 287 (les 17 fichiers a reparer sont bien detectes)
7. M7 : ASCII 0 sur les 4 fichiers
**Lecons** :
1. Le mode REPARER est la bonne strategie pour un bloc mal place : on le DEPLACE (retrait + reinsertion) sans jamais creer de doublon
2. Le test sur une copie du VRAI fichier (detecter-impacts.py a l indice 12) est plus fiable qu un mini-cerveau idealise : il reproduit exactement le bug reel
3. La regle est confirmee : apres reparation, detecter-impacts lit le bloc (le schema hybride est pleinement operationnel)

## [NOTES] RETEST 2026-08-08 -- migrer-identite v0.1.3 (correction commentaires sans ligne vide, Vulcain)

**Mission** : re-valider la correction du bug residuel (en-tete suivi de commentaires documentaires SANS ligne vide -> bloc a la ligne 13 pour 2 .sh).
**Verdict** : VALIDE.
**Tests** :
1. N1 : py_compile + bash -n OK, --version py/sh = 0.1.3
2. N2 (test-v013.py, copies des 2 VRAIS fichiers problematiques) : 2 REPARE-DRY puis 2 REPARE, bloc ligne 6 (generateurs-commande.sh apres # Statut) et ligne 11 (rechercher-accents-sensibles.sh apres # Version), 1 SEUL bloc, re-scan DEJA, PARITE py/sh OK, bash -n OK
3. N3 regressions : test-long-en-tete (parite OK), test-reparation (detecter-impacts lit l identite), test-frontmatter-special (A preserve), test-migrer-identite mini (T5 idempotence exit 0) -- AUCUNE regression
4. N4 dry-run reel : 2 REPARE-DRY (les 2 bons fichiers) + 284 DEJA + 1 IGNORE + 0 erreur + total 287
5. N5 : ASCII 0 sur 4 fichiers
**Lecons** :
1. Un en-tete court peut etre suivi de commentaires documentaires SANS ligne vide : la regle fiable est d inserer APRES la ligne # Statut (ou # Version), pas apres la 1re ligne vide
2. Tester sur des copies des VRAIS fichiers reels (pas seulement un mini-cerveau) revele les cas reels (commentaires sans ligne vide)
3. L outil est desormais robuste sur tous les formats d en-tete rencontres

## [NOTES] RETEST 2026-08-08 -- detecter-impacts v0.2.1 + migrer-identite v0.2.0 (2 livrables vague 3, Vulcain)

**Mission** : valider 2 livrables (decision utilisateur apres verification Cerberus) : (L1) detecter-impacts v0.2.1 - les fichiers des dossiers controles/, rapports/, retro-actions/ sont des TRACES HISTORISEES : marquees [HISTORISE], exclues du verdict ; (L2) migrer-identite v0.2.0 - migration sur TOUT le cerveau : nouveaux types racine/classeur/pense-bete/template/note (appartient_a dynamique), exclusions traces, compatibilite retrograde agents/tools/.
**Verdict** : VALIDE.
**Tests** :
1. M1 : py_compile + bash -n 4/4, --version py/sh identiques (detecter 0.2.1, migrer 0.2.0)
2. M2-M4 detecter v0.2.1 : cas reel outil commun (activer-agent-principal.py) -> 20 traces [HISTORISE] exclues du verdict, synthese ligne dediee 'dont traces historisees', parite py/sh IDENTIQUE (20 traces / 50 non a jour / meme verdict) ; cas entite cerberus.md intact (2 impliques A JOUR, verdict OK)
3. M5-M8 migrer v0.2.0 mini-cerveau (Z:/tmp/m3-morpheus, 7 fichiers) : dry-run types corrects (outil x2, note, classeur, pense-bete, template, controle EXCLU) ; reel 6 MIGRE + 0 erreur ; IDEMPOTENCE 2e passage 0 migre/6 DEJA ; bloc note = appartient_a:vulcain (dossier parent), bloc classeur = commun ; bloc .py/.sh ligne 5 (<= 12) ; detecter-impacts lit les blocs (note, classeur)
4. M9 : ASCII 0 sur 7 fichiers modifies
5. M10 : regression frontmatter-sans-identite -> IGNORE et INTACT (aucun double frontmatter)
6. M11 : protection non-ASCII -> [ERREUR] erreur:non-ascii (fichier NON ecrit)
7. M12 : regression agents/tools dry-run reel -> 0 migre + 286 DEJA + 1 IGNORE + 0 erreur (etat identique a avant : aucune regression)
**Lecons** :
1. La distinction reference vivante vs trace historisee est operationnelle : les rapports dates (controles/rapports/retro-actions) restent VISIBLES ([HISTORISE]) mais ne faussent plus le verdict
2. La parite py/sh des sorties (memes compteurs, meme verdict) est la vraie preuve de parite - plus fiable qu une diff textuelle du code (en-tete documentaire du .py absent du bloc embarque)
3. L extension v0.2.0 est retrocompatible : le dry-run reel sur agents/tools/ donne exactement les memes chiffres qu avant l extension
4. Les nouveaux types couvrent la vague 3 : AGENTS.md -> racine, classeur-variables -> classeur, pense-betes -> pense-bete, -template -> template, missions/resumes/priorites .md -> note (appartient au dossier parent)

## [NOTES] RETEST 2026-08-08 -- migrer-identite v0.2.1 (corrections dry-run reel, Vulcain)

**Mission** : re-valider 4 corrections decouvertes au dry-run reel avant application vague 3 : (1) definition-combo.json dans dossier combos/ -> type combo, (2) exclusions exemples/ + recherches-web/ + sauvegardes/, (3) AGENTS-historique.md -> type historique (commun), (4) reste v0.2.0 inchange.
**Verdict** : VALIDE.
**Tests** :
1. N1 : py_compile + bash -n OK, --version py/sh = 0.2.1
2. N2 mini-cerveau combos+exemples : definition-combo.json -> type combo (dossier combos/), exemples/pollue.md EXCLU du scan (0 erreur non-ascii malgre son accent volontaire)
3. N3 dry-run reel cerveau-projet : 21 migres + 397 deja + 3 ignores + 0 erreur + total 421 (les 8 definition-combo de combos/ types combo, plus AUCUN fichier exemples/ ou recherches-web/)
4. N4 dry-run racine projet : AGENTS.md -> type racine, AGENTS-historique.md -> type historique (commun)
5. N5 : ASCII 0 sur 7 fichiers
**Lecons** :
1. Le dry-run reel AVANT application a encore revele 4 cas non couverts par le mini-cerveau idealise : combos par dossier (pas seulement prefixe), exemples/ et recherches-web/ (fichiers de test pollues et recherches jamais a migrer), sauvegardes/ (artefacts), AGENTS-historique (journal vivant -> type dedie)
2. L exclusion des dossiers hors perimetre (exemples/, recherches-web/, sauvegardes/) est la bonne strategie : elle evite a la fois la pollution des fichiers de test et les erreurs non-ascii volontaires
3. Le type historique (commun) pour AGENTS-historique.md est coherent avec son role de journal partage des activations
4. La chaine est prete pour l application vague 3 par Buffy : 21 fichiers dans cerveau-projet/ + AGENTS.md + AGENTS-historique.md a la racine

## [NOTES] Controle 2026-08-08 -- convention identification v0.5.0 (Vulcain)

**Controle** : 3 outils modifies par Vulcain (activer-agent-principal v0.5.0, lister-agents v0.3.0,
evaluer-agents v0.2.2) pour la convention 'aucun mot seul' (Nom LLM / Nom Agent / Role Agent).
**Verdict** : VALIDE.
**Tests reels (independants)** :
1. M1 test-007 v0.5.0 : 22/22 VALIDE (bloc Nom LLM en tete, migration anciens champs, parite sh)
2. M2 regression test-006 v0.4.0 : 26/26 VALIDE (alignement, source double, conflit, absorption)
3. M3 regression test-002 v0.3.1 : 8/8 (profil session classeur, regression test-001 12/12)
4. M4/M5 parite lister-agents py/sh : lecture identique des fiches actuelles (repli role:/statut:)
5. M6 evaluer-agents py/sh : agent actif lu identiquement (Nom Agent avec repli Nom)
6. ASCII : 14 fichiers outils/tests/docs OK
7. Cas reel : la reactivation de Cerberus a migre le bloc session-llm-1 d AGENTS.md au format
v0.5.0 automatiquement (Nom LLM en tete + table Sessions connues en colonne Nom LLM)
**Lecons** :
1. La reconstruction complete du bloc en ordre canonique est la bonne approche de migration
2. Retrocompat en lecture (ancien nom accepte) obligatoire pendant la transition
3. Piege grep mot seul : chercher le champ complet avant l ancien nom
4. Piege test negatif : inverser la logique grep -q pour les checks AUCUN

## [VERDICT] Validation formelle 2026-08-08 -- tests ecrits par Vulcain (decision utilisateur: les garder mais valides par Morpheus)

**Contexte** : constat 3 utilisateur -- les tests sont le domaine de Morpheus, pas de Vulcain. Les 2 tests existants restent mais recoivent un verdict formel de Morpheus.
**Verdict** : VALIDE (avec correction workspace).
**Points verifies** :
1. tester-valider-nommage-v030.sh : 13/13 Reussis, 0 Echec
2. tester-combos-moteur-v020.sh : 10/10 Reussis, 0 Echec
3. INF RACTION WORSPACE DETECTEE puis CORRIGEE : les 2 tests utilisaient `mktemp -d` (dossier systeme HORS workspace). Corrige : zone temporaire dans le workspace (cerveau-projet/.tmp-test-*) creee et supprimee a la fin -- conforme a la regle immuable regles-perimetre-workspace.md
4. ASCII : 0 caracteres non-ASCII sur les 2 tests
5. Aucune trace restante de mktemp, aucune zone .tmp-test-* laissee
**Lecons** :
1. Tout fichier temporaire de test se cree DANS le workspace, jamais hors workspace (regle immuable) -- meme pour les tests, meme avec mktemp
2. La regle workspace s applique aussi aux scripts de test, pas seulement aux interventions manuelles
3. Un test peut etre ecrit par un autre agent mais sa VALIDATION FORMELLE appartient toujours a Morpheus (regles-choisir-agent)
4. Verifier systematiquement le nettoyage (rm -rf) a la fin de chaque test -- zone temp supprimee ou pas

## [VERDICT] 2026-08-08 -- CORRECTION test-003 (Nom Agent) + TEST FORMEL nettoyer-sessions v0.1.0

**Mission** (decision utilisateur, activation directe Cerberus, 2 livrables).
**Verdict** : VALIDE (les 2 livrables).

**LIVRABLE 1 -- test-003-activer-agent-principal-v033.sh CORRIGE (22/22 VALIDE)** :
1. Etat avant : 20/22 A REVOIR -- 2 echecs (1c, 3d) : la fonction nom_session lisait encore le champ **Nom** (format pre-v0.5.0) alors que les blocs session utilisent **Nom Agent** depuis la convention identification v0.5.0. Problematique PRE-EXISTANTE (git diff du test vide -- la migration v0.5.0 n avait pas ete propagee au test).
2. Correction : nom_session matche maintenant /^\| \*\*(Nom Agent|Nom)\*\* \| / (repli sur l ancien **Nom**), meme style que la fonction equivalent du test-007 v0.5.0.
3. Regression complete activer-agent-principal : test-001 12/12, test-002 8/8, test-003 22/22, test-004 19/19, test-005 28/28, test-006 26/26, test-007 22/22 = 137/137 VALIDE, 0 echec.

**LIVRABLE 2 -- test-001-nettoyer-sessions.sh CREE (26/26 VALIDE)** :
1. N1 compile py+sh OK, N2 --version py/sh identiques v0.1.0
2. N3 dry-run : message [DRY-RUN] + AUCUN fichier modifie (AGENTS + classeur identiques)
3. N4 execution reelle py : blocs ### Session = 0, ## Sessions LLM = 0, ## Sessions connues = 0, profil-session-* = 0
4. N5 preservation : frontmatter identite, entete, Configuration Active, Liste des agents, variable non-session (profil-systeme) PRESERVES
5. N6 AGENTS-historique (journal) JAMAIS modifie (intact dans l espace de test)
6. N7 idempotence : 2e execution AGENTS = 0 ligne, classeur = 0 ligne
7. N8 parite py/sh : fichiers resultants IDENTIQUES (AGENTS + classeur + historique) -- le .sh embarque le meme python
8. N9 messages de sortie presents dans les 2 versions
9. N10 ASCII : test + fichier nettoye 100% ASCII, zone temp supprimee (regle workspace)

**Lecons** :
1. Quand une convention de format de fichier change (migration v0.5.0 : **Nom** -> **Nom Agent**), les tests qui lisent les champs doivent etre alignes DANS LA MEME mission que la convention -- sinon des tests pre-existants echouent en silence a chaque regression
2. Le repli de lecture (pattern alternance awk (Nom Agent|Nom)) rend un test robuste aux migrations : il lit le format courant ET l ancien
3. Le scan --recursive de valider-nommage signale en ERREUR les fichiers des dossiers tests/ et spec/ (structure attendue categorie/outil/fichiers : les sous-dossiers sont traites comme des faux outils de niveau 2) -- comportement PRE-EXISTANT partage par tous les tests et specs (test-001-remplacer-texte.sh et spec-remplacer-texte sont signales pareil) : NE PAS creer de test hors convention pour l eviter, c est un bruit connu du scan
4. DIVERGENCE PARITE DETECTEE (cosmetique, a signaler a Vulcain) : le .py affiche 'Nettoyage termine : N lignes supprimees' (ligne 168) alors que le .sh affiche juste 'Nettoyage termine' (ligne 153) sans le total -- comportement de nettoyage IDENTIQUE (fichiers resultants diff vides), seule la ligne finale differe
5. Un test de nettoyage se teste TOUJOURS sur copies avec les 3 variables redirigees (AGENTS_FILE + CLASSEUR_STOCKAGE) : les vrais fichiers restent intacts (verifie par git status)

## [VERDICT] RETEST 2026-08-08 -- nettoyer-sessions v0.1.1 (correction parite + bug latent, Vulcain)

**Mission** : retester la correction de parite des sorties py/sh (modele boucle Vulcain -> Morpheus -> Vulcain -> Morpheus).
**Verdict** : VALIDE (32/32).

**Contexte** : au test formel 26/26, j avais signale une divergence cosmetique : le .py affichait 'Nettoyage termine : N lignes supprimees' alors que le .sh affichait juste 'Nettoyage termine'. Vulcain a corrige (v0.1.1 : total dans le .sh, harmonisation 0 ligne -> 0 lignes).
**Tests** :
1. RETEST 1 : 29/32 A REVOIR -- la correction de parite a EXPOSE un bug latent du .sh : nb=$(grep -c "profil-session-" "$fichier" 2>/dev/null || echo 0) produit 0\n0 quand il y a 0 occurrence (grep -c affiche 0 ET echo 0 s execute) -> NB_CLASSEUR=0\n0 casse l arithmetique du total ($((NB_AGENTS + NB_CLASSEUR))) -> erreur syntaxe 'line 162: syntax error in expression' en dry-run sur fichiers deja nettoyes. 3 echecs (9b sortie sh 2e passage, 10d parite dry-run, 10f message dry-run sh) TOUS lies a ce bug
2. ENRICHISSEMENT TEST : 6 assertions ajoutees (10-10f) qui figent la parite des SORTIES py/sh (reel + dry-run, CRLF normalise) + version 0.1.1
3. Vulcain a corrige : (1) nb=${nb:-0} sans || echo 0, (2) bloc dry-run AVANT bloc nb=0 (parite dry-run 0 occurrence : le .py affiche [DRY-RUN] Classeur : 0... toujours)
4. RETEST FINAL : 32/32 VALIDE -- parite sorties reelles OK, parite dry-run OK, messages finaux avec total OK, idempotence OK, preservations OK, historique intact, ASCII 0, versions py/sh = 0.1.1
**Lecons** :
1. La parite des SORTIES (messages) est un test plus puissant que la parite des FICHIERS : elle a revele un bug latent (0\n0) invisible dans les tests de contenu -- TOUJOURS comparer les sorties py/sh ligne a ligne, pas seulement les fichiers resultants
2. Le piege grep -c || echo 0 (documente) se manifeste AUSSI quand la valeur entre dans une expression arithmetique -- utiliser nb=${nb:-0} systematiquement
3. Ordre des blocs dans une fonction : un test dry-run doit passer AVANT le test de valeur (0) sinon le message dry-run est omis -- le .py affiche [DRY-RUN] meme avec 0
4. La boucle Vulcain -> Morpheus -> Vulcain -> Morpheus fonctionne : Morpheus detecte, Vulcain corrige, Morpheus revalide -- la parite est maintenant figee par le test

## [VERDICT] Test formel 2026-08-08 -- valider-nommage v0.3.1 (correction bruit scan recursif, Vulcain)

**Mission** : valider la correction du bruit du scan --recursive (modele boucle Vulcain -> Morpheus -> Vulcain).
**Verdict** : VALIDE.

**Contexte** : le scan --recursive traitait les SOUS-DOSSERS COMPOSANTS d un outil (tests/, spec/, protections/, __pycache__/) comme de faux outils de niveau 2 -> leurs fichiers test-*/spec-* etaient signales en ERREUR de prefixe a tort (bruit preexistant : tester/ 14 erreurs, nettoyer/ 1, remplacer/ 2). Vulcain a corrige : constante SOUS_DOSSERS_COMPOSANTS exclue au niveau categorie ET au niveau outil (.py) + parite .sh (grep -vE dans le find).
**Tests** :
1. M1 : test formel existant tester-valider-nommage-v030.sh = 13/13 VALIDE (aucune regression des modes --mots-seuls, --type, parite recursif)
2. M2 : cas du bruit corrige : scan de tester/ nettoyer/ remplacer/ = 0 erreur chacun (avant : 14/1/2)
3. M3 : un vrai outil sous une categorie (activer-agent-principal.py --type outil) reste VALIDE (0 erreur)
4. M4 : parite py/sh des scans identique (Erreurs:0 partout sur les 3 categories)
5. M5 : versions 0.3.1 py/sh identiques, ASCII 0 sur les 3 fichiers
6. M6 : aucune zone temp restante (regle workspace)
**Lecons** :
1. Les sous-dossiers composants d un outil (tests/, spec/, protections/, __pycache__/) ne sont PAS des outils : le scan recursif doit les ignorer aux DEUX niveaux (categorie et outil) sinon leurs fichiers sont valides avec la categorie parente (faux positifs de prefixe)
2. Le bruit etait PRE-EXISTANT et partage par tous les outils avec tests/ ou spec/ : il n etait visible que quand on scannait une CATEGORIE ou un OUTIL directement (pas tools/ entier) -- verifier les 2 usages en regression
3. Le scan global tools/ est inchange (269/267/2) : les 2 erreurs restantes (tester-combos-moteur-v020.sh, tester-valider-nommage-v030.sh) sont des tests a la racine de tester/, HORS perimetre (fichiers de test historiques au mauvais emplacement)

## [VERDICT] Validation formelle 2026-08-08 -- migrer-identite v0.2.2 (retour migrations)

**Contexte** : retour sur les migrations. L outil migrer-identite v0.2.1 avait une regle de detection trop large (`combos- OU dossier combos/` -> type combo) qui typait a tort les 12 OUTILS du dossier combos/ en combo. Decision utilisateur : corriger l outil puis migrer + introduire un NOUVEAU TYPE `test` pour les fichiers tester-*.
**Verdict** : VALIDE.
**Points verifies** :
1. Versions py/sh = 0.2.2 (identiques)
2. Parite py/sh sur --liste : IDENTIQUE
3. Types des 15 fichiers : 12 combos-* = outil, 7 definition-combo.json = combo (intacts), 2 tester-* = test, valider-nommage.sh repare (bloc ligne 5)
4. Tests existants : tester-valider-nommage-v030 13/13 + tester-combos-moteur-v020 10/10 (heredocs INTACTS - la migration manuelle etait la bonne decision, l outil aurait supprime les blocs # identite: des heredocs de test)
5. Idempotence : dry-run cerveau-projet 0 migre + racine 0 migre + 0 erreur
6. ASCII 0 sur 17 fichiers modifies
7. detecter-impacts lit type=test et type=outil correctement
8. BONUS detecte par Cerberus : le deplacement de classeur-variables vers agents/ avait casse les chemins dans 5 outils (activer-agent-principal, verifier-systeme, evaluer-structure, parcours-vulcain) - corriges, l activation reelle fonctionne sans warning
**Lecons** :
1. Une regle de detection trop large (dossier combos/) cree des faux types SILENCIEUX : les 12 outils avaient le mauvais type depuis la vague 2, invisible sans audit par type
2. La priorite tester- doit passer AVANT la regle combos/ (un test dans un dossier outil n est pas un combo)
3. Migrer un fichier de test qui contient des blocs # identite: dans ses HEREDOCS avec l outil le casserait -> migration manuelle obligatoire pour les tester-*
4. Apres tout deplacement de dossier, verifier les chemins en dur dans les outils (grep du chemin ancien) - le warning d activation a revele 5 fichiers casses
5. La distinction combos- (outils) vs combo-*/definition-combo.json (definitions) doit etre ancree dans le code, pas dans l intuition

## [NOTES] VERDICT 2026-08-08 -- generateurs-carte v0.2.0 (squelette Pattern 10 + Pattern 3, Vulcain)

**VERDICT** : VALIDE. 8/8 points passes.
**Controle** : generateurs-carte.py v0.2.0 (modifie par Vulcain, chaine bout-en-bout : squelette creer enrichi -- indice Pattern 10 UNE CARTE = UN ROLE en tete des indices de c1 + indice Pattern 3 RAPPEL DES COMBOS en tete des indices de c2).
**Lecons** :
1. SYNTHESE 4/4 : py_compile OK, ASCII 0 sur py + md, valider-nommage code 0, version --version 0.2.0 (exige une action, comportement pre-existant identique py/sh = parite de comportement).
2. SQUELETTE 4/4 : carte factice creee dans le workspace (.tmp-morpheus-test/ puis supprimee) -- c1 porte l indice Pattern 10 (texte UNE CARTE = UN ROLE + role de l agent), c2 porte l indice Pattern 3 (RAPPEL DES COMBOS) en POSITION 1 (avant Pattern 7 et ASCII), JSON valide, navigation PARCOURS TERMINE, --liste 7 cases, references validees.
3. REGRESSION 3/3 : analyser (6 chemins affiches), detecter sur le squelette de base = 0 anomalie, dupliquer-chemin (--debut c2 --fin c9 --prefixe dup --brancher-debut) = references validees 10 cases. L anomalie detectee apres branchement (c2b INATTEIGNABLE) est le COMPORTEMENT DOCUMENTE de --brancher-debut (la branche c1 est reorientee vers dup-c2, l original devient inatteignable) -- pas une regression de la modification.
4. PIEGE CLI : dupliquer-chemin prend --debut/--fin (pas d arguments positionnels c2/--vers) -- verifier le --help avant d utiliser une sous-commande.
5. PIEGE TEST : les dossiers de test se creent dans le WORKSPACE (.tmp-morpheus-test/) puis se suppriment -- JAMAIS dans /tmp (regle workspace : ecriture = workspace seul).
6. La chaine continue (Pattern 8) : Morpheus termine et ACTIVE Janus pour le controle.

## [VERDICT] Test formel 2026-08-08 -- 3 combos creer-* v0.2.0 (89/89 REUSSI)

**Tache** : tester formellement combo-creer-fichier-cerveau, combo-creer-agent, combo-creer-protocole (convertis en cases generateur Pattern 3 par Buffy).
**Verdict** : VALIDE -- 89/89 REUSSI, 0 ECHEC, code 0.
**Lecons** :
1. Test cree dans tester/tests/test-003-combos-creer/ (test-003-combos-creer.py + .md) sur le modele du test-002-combos-moteur -- 9 cas par combo (structure, --liste, variable manquante, navigation OUI, navigation NON, parite py/sh, dry-run sans effet, nommage, ASCII).
2. Les combos creer-* EXIGENT leurs variables (--var chemin=... / contenu=... / agent=...) : sans elles le moteur renvoie Variable non trouvee code 1 -- protection saine, jamais de commande partielle.
3. La branche NON d un controle ne genere AUCUNE commande creer-fichier : le court-circuit vers la fin fonctionne pour les 3 combos (verifie).
4. PARITE py/sh conservee : memes sorties --liste et meme navigation OUI entre combos-moteur.py et combos-moteur.sh.
5. DRY-RUN SANS EFFET : navigation en --dry-run, aucun fichier cree (cible verifiee absente) -- la protection anti-effets est la base du test de combos qui creent des fichiers.
6. FAUX POSITIFS DE NOMMAGE documentes (2) : (a) definitions combo-* vs convention combos-* identique a tous les combos existants ; (b) fichier de test dans tests/ exige un prefixe tests- absent des tests formels test-XXX-nom-outil, identique a test-002-combos-moteur.py (reference 31/31) -- ne pas corriger.
7. Le test formel confirme les validations rapides de Buffy (json.load, navigation, ASCII) mais ajoute ce qu elles ne couvraient pas : parite py/sh, dry-run sans effet, branches NON, variables manquantes -- la REGLE ABSOLUE (tests = Morpheus) reste operationnelle.
| VERITE | Les combos creer-* sont des chaines generateur->outil : sans leurs variables ils refusent (code 1), avec elles ils composent des commandes correctes et la branche NON court-circuite la creation |

## PHILOSOPHIE -- Principes de comportement

| **Relire sa fiche a chaque activation** | Quand je suis active ou reactive, je relis MA fiche et MES corrections avant de continuer. Je ne lis que mes fichiers, jamais ceux des autres agents : chacun lit les siens en prenant le relais. |
## [RAPPORT] Test 2026-08-08 -- generateurs-commande apres correction des descriptions (VERDICT : VALIDE avec 1 anomalie pre-existante)

**Objet** : tester formellement generateurs-commande apres la correction des 63 descriptions cosmetiques du catalogue (105 commandes) + le nouvel outil generateurs-regenerer-catalogue.
**Tests passes** :
1. T1 --version : generateurs-commande v0.2.0 OK.
2. T2 --liste : 109 lignes, 0 description cosmetique restante sur 105 (pattern Options/Arguments/[--aide]/source destination = 0).
3. T3 generation reelle 6/6 : activer-activer (quote raison OK), valider-nommage, verifier-restauration-sure, creer-fichier, combos-moteur, generateurs-carte - commandes exactes et interpolees.
4. T4 regenerateur : --version v1.0.0, dry-run 86 outils scannes 82 preserves 0 a ajouter, extraction 2 formats (docstring valider-nommage + commentaires copier-fichier + docstring .sh test-001), bout en bout outil fictif propose avec la bonne description puis supprime SANS residu.
5. T5b parite generateurs-regenerer-catalogue py/sh OK.
6. T6 non-regression : --liste 109, ASCII 0 catalogue, workspace propre (0 outil fictif, 0 .tmp).
**BUG CORRIGE (trouve par le test)** : generateurs-carte avait un parametre action de type choix avec LISTE VIDE (heritage parsing piste A) -> generation impossible (Valeur invalide pour action). Corrige : choix = [creer, analyser, dupliquer] (l entree speciale du regenerateur). 1 seul cas sur 105.
**ANOMALIE PRE-EXISTANTE SIGNALEE (non corrigee, domaine Vulcain)** : generateurs-commande.sh affiche v0.1.0-beta alors que le .py affiche v0.2.0 - divergence de parite version, fichier .sh non modifie par les missions recentes (pre-existant). A corriger par Vulcain (mettre a jour VERSION du .sh).
**Lecons** :
1. Le test de generation reelle (--commande + --reponses) est le SEUL moyen de detecter les parametres choix a liste vide (un simple json.load ne suffit pas).
2. Les entrees SPECIALES du regenerateur (generateurs-carte, combos-moteur, verifier-restauration-sure) sont la protection contre les parses d aide imperfectibles - mais le catalogue ACTUEL peut encore contenir des entrees regenerees avec des defauts : scanner les parametres type=choix a liste vide dans tout le catalogue.
3. Le .sh wrapper peut garder une VERSION obsolete sans etre modifie : verifier la parite --version py/sh lors de chaque test.
## [VERDICT] Test formel 2026-08-09 -- combo tester-outil v0.1.0 (16/16 VALIDE)

**Objet** : test formel du combo `tester-outil` (Pattern 3, chemin de test de Morpheus encapsule, cree par Buffy) + integration dans le parcours morpheus v0.1.2.
**Verdict** : VALIDE. 16/16 points passes (test-004-combos-tester-outil.py).
**Lecons** :
1. La navigation du combo tester-outil est complete : --liste 6 cases, chemin OUI (c1 generateur creer-fichier -> c2 outil cree le fichier -> c3 controle protections -> c4 outil commande_test -> c6 FIN), chemin NON (c3=NON -> c5 FIN PROTECTIONS MANQUANTES, la REGLE ABSOLUE jamais de test sans protections est PRESERVEE)
2. L interpolation {var} est robuste : variable manquante (fichier_test en c1, commande_test en c4) -> erreur claire avec la case source (combos-moteur refuse proprement)
3. PIEGE WINDOWS DECOUVERT : un chemin absolu avec backslashes (Z:\...\test-001.sh) passe dans la commande generee par le generateur, puis shlex.split de la case outil ECLATE le backslash -> le fichier n est pas cree. SOLUTION : utiliser des FORWARD SLASHES dans fichier_test (Z:/.../test-001.sh) - Python les accepte, shlex aussi
4. La sortie d une case outil n est affichee que via --verbose (sinon capturee dans la variable mais invisible) - pour verifier une sortie (EXEC-OK), lancer avec --verbose
5. Integration parcours : parcours morpheus v0.1.2, guider-parcours affiche [6/18] Lancer le combo tester-outil puis [7/18] Verifier les resultats, valider-cartes-decision --agent morpheus CONFORME
6. Le test 004 (16 points) est ajoute dans tests/ : .py + .md numerotes conformement au protocole-tests, protections workspace (dossier temporaire .tmp-test004 nettoye en fin de test)
7. Bruit preexistant documente (non bloquant) : valider-nommage signale 2 ERREUR sur test-004 (format invalide test-004-combos-tester-outil.py) - IDENTIQUE aux 3 tests existants (test-001/002/003) : le format test-XXX-nom-outil.py dans tests/ est hors perimetre de l outil

**Validation finale** : test-004 16/16 VALIDE, regression test-003 OK (combos creer-* non casses), ASCII 0 (test py + md), nommage bruit preexistant identique aux 3 tests existants, workspace propre.
## [LECON] 2026-08-09 -- TEST FORMEL 005 generateurs-commande v0.2.1 + parcours-atlas v0.1.2 (26/26 VALIDE)

**Contexte** : test formel du generateur fiabilise (flags optionnels vides) et du parcours Atlas pilote strict, avant generalisation aux 10 autres parcours.
**Verdict** : VALIDE 26/26 (16 generateur + 6 parcours + 4 ASCII).
**Lecons** :
1. RACINE dans un test : le fichier est a cerveau-projet/agents/tools/tester/tests/test-XXX/ -> 6 niveaux de .. pour remonter a la racine du projet (pas 5) - erreur de chemin double cerveau-projet/cerveau-projet au 1er passage
2. PIEGE WINDOWS cmd.exe : dans subprocess shell=True, les guillemets simples ne protegent pas et le pipe | casse la commande -> utiliser subprocess.run(args_liste) SANS shell pour les commandes avec --reponses contenant des pipes
3. Le bug des flags vides est reellement corrige : lire-fichier compose --lignes 3 SANS --debut/--fin vides (avant : argparse code 2), flags booleens oui=flag/non=absent py ET sh, parite py/sh identique
4. Le parcours atlas v0.1.2 en pilote strict : 0 champ commande dans les indices avec catalogue, navigation PARCOURS TERMINE, PASSE PAR LE GENERATEUR affiche sans commande en dur
5. valider-nommage v0.3.2 reconnait maintenant test-XXX-*.py -> 0 ERREUR sur test-005 (plus besoin de documenter le bruit)
6. Le modele est CERTIFIE pour generaliser aux 10 autres parcours : le generateur v0.2.1 compose sans erreur toutes les commandes
## [VERDICT] Test formel 2026-08-09 -- cartographier-parcours v0.1.0 (19/19 VALIDE)

**Objet** : test formel de l outil cartographier-parcours v0.1.0 (categorie cartographier/, cree par Vulcain - Atlas cartographie le parcours d un agent dans un fichier). Test : test-006-cartographier-parcours.py (19 points).
**Verdict** : VALIDE. 19/19 points passes.
**Tests passes** :
1. --version py/sh identiques v0.1.0 (wrapper pur).
2. Generation reelle sur parcours-atlas : fichier cree dans le dossier du parcours, en-tete complet (agent, version 0.1.4, depart c0, 32 cases, 18 chemins), sections arbre/impasses/boucles/chemins presentes.
3. Parite py/sh : fichiers generes IDENTIQUES (diff).
4. --sortie personnalise vers .tmp-* : fichier cree au chemin demande.
5. --dry-run ne cree rien ([DRY-RUN] affiche).
6. Arbre : chaque case apparait UNE fois (c0 x1, c11 x1), convergences marquees [convergence], fins visibles.
7. ASCII 0 sur les 5 fichiers (py, sh, md, spec, genere).
8. JSON invalide -> ERREUR claire (code 1).
9. Parcours inexistant -> ERREUR claire (code 1).
10. valider-nommage --type outil OK.
11. Aucun fichier residuel dans le workspace apres les tests (cartographie-atlas supprime).
**Lecons** :
1. L arbre ASCII de cartographier-parcours est CORRECT apres correction du bug de double affichage : la fonction descendre avec un set affichees (1ere occurrence) + marquage [convergence] evite les cases en double et materialise les rejoints de workflow - c est le comportement attendu d une cartographie (Pattern 7 modele compose : les deviations REJOIGNENT, elles ne bouclent pas).
2. La parite py/sh par wrapper pur (exec python3) rend le test de parite TRIVIAL (fichiers generes identiques) - c est le bon pattern pour les outils dont la logique vit dans le .py.
3. Le test de generation reelle (bout en bout avec sortie par defaut dans le dossier du parcours) verifie AUSSI la protection workspace : le fichier genere doit etre SUPPRIME apres le test (0 residu).
4. La chaine bout-en-bout est respectee : Vulcain m a active, je rends mon verdict et j ACTIVE JANUS (controle croise) - la chaine ne retombe jamais sur Cerberus au milieu.