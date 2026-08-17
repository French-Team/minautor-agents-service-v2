---
identite:
  type: historique
  appartient_a: commun
  commun: true
---
# Historique des Agents

> Ce fichier contient l'historique complet des activations d'agents.
> Il est separe d'AGENTS.md pour alleger ce dernier.
> Chaque entree identifie la session LLM (session-llm-N) qui a effectue l'action.
> Les entrees precedant la structure multi-session sont attribuees a session-llm-1.

---

| 2026-08-17 22:15 | session-llm-1 | Cerberus | BILAN FINAL ROUND VERROU AUTO-JOURNALISATION : NON-REGRESSION 87 OK / 0 KO (46.3s, reference amelioree 69.7s -> 46.3s). Corrige en cours de round : (1) test-089 tag derive -> anti-contournement (taxonomie), (2) test-078 point 4 rendu robuste (verifie l incident detecter-troncatures dans le registre stable au lieu de l entree purgee du plafond 150 de l historique). Lecon Morpheus enregistree. Retour a Cerberus. |
| 2026-08-17 22:08 | session-llm-1 | janus | RELANCER LA NON-REGRESSION FINALE (round verrou auto-journalisation) : Morpheus a corrige le tag de test-089 (derive -> anti-contournement). test-089 9/9 vert, test-087 8 OK / 0 KO (taxonomie OK). Janus lance la non-regression complete pour confirmer 87/87 puis reactive Cerberus avec le bilan.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 22:08 | session-llm-1 | morpheus | CORRIGER LE TAG DE test-089 : la non-regression Janus a rendu 86 OK / 1 KO. Le KO = test-087-categories-tags signale que test-089 porte le tag 'derive' non autorise dans la taxonomie categories-tests.json (88 tags autorises). CORRECTION : remplacer 'derive' par 'anti-contournement' (tag autorise, categorie securite) dans la ligne Tags: de test-089. VERIFIER : test-089 vert, test-087 vert (taxonomie OK). PUIS : reactiver Janus pour la relance finale de la non-regression.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 22:08 | session-llm-1 | Cerberus | NON-REGRESSION ROUND VERROU AUTO-JOURNALISATION : 86 OK / 1 KO. SEUL KO = test-087-categories-tags signale le tag 'derive' de test-089 (non autorise dans la taxonomie categories-tests.json). Retour a Cerberus pour activer Morpheus (exclusif reparations de tests). |
| 2026-08-17 21:56 | session-llm-1 | janus | ROUND VERROU AUTO-JOURNALISATION : Vulcain a corrige le bug caller/target + reordonne le marbre avant le verrou, Morpheus a adapte test-045/test-057/test-024/005/007 + cree test-089. Janus lance la non-regression complete pour valider l ensemble.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 21:42 | session-llm-1 | vulcain | CORRIGER LE VERROU AUTO-JOURNALISATION : dans editer-parcours et valider-cartes-decision, le verrou est appele avec args.agent (CIBLE) au lieu de l agent ACTIF (appelant). detecter-cablages-manquants est OK (--agent = agent appelant explicite). BUG : editer-parcours --agent themis et valider-cartes-decision --agent atlas sont BLOQUES par le verrou d identite (session != cible). Tests affectes test-004/005/021/045/046/057. CORRECTION : determiner l agent actif de la session (lire AGENTS.md table Sessions connues, agent le plus recent) et le passer a verrouiller_habilitation(appelant, outil) ; garder --agent comme CIBLE du travail de l outil. VERIFIER : valider-cartes-decision --agent atlas CONFORME sans blocage, editer-parcours --agent themis --bump --dry-run sans blocage identite. PUIS : bump version des 2 outils, adapter les pins tests si besoin, reactiver Morpheus.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 21:21 | session-llm-1 | morpheus | MISSION MORPHEUS : ADAPTER LES TESTS APRES LA GENERALISATION DU VERROU-AUTO + CREER test-089. CONTEXTE : Vulcain a ajoute le verrou (verrouiller_habilitation) a editer-parcours v0.1.5, valider-cartes-decision v0.4.3, detecter-cablages-manquants v0.1.2. detecter-cablages-manquants EXIGE maintenant --agent (obligatoire). Chaque outil journalise verrou-auto si autorise, bloque sinon. A FAIRE : 1) grep global des pins de version des 3 outils dans les tests (editer-parcours 0.1.4->0.1.5, valider-cartes-decision 0.4.2->0.4.3, detecter-cablages-manquants 0.1.1->0.1.2) et les adapter ; 2) adapter les tests qui appellent detecter-cablages-manquants SANS --agent (ajouter --agent <agent habilite>) - attention au verrou IDENTITE : les tests qui lancent le verrou en production doivent tourner avec l agent reellement actif, sinon utiliser --audit si le test est une preuve formelle ; 3) CREER test-089-ecritures-hors-cycle.py (garde-fou anti-recurrence de la derive, deja en attente) qui verifie detecter-ecritures-hors-cycle v0.1.0 (--version, etat propre, preuve negative KO sous Cerberus, exclusions) ; 4) lancer les tests adaptes en reel ; 5) normes ASCII + LF. FIN : lecon Morpheus + ACTIVER JANUS pour la non-regression complete.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 21:17 | session-llm-1 | vulcain | MISSION VULCAIN : GENERALISER L AUTO-JOURNALISATION (mode verrou-auto) AUX 3 OUTILS CRITIQUES QUI ECRIVENT/VALIDENT DANS LE PROJET : editer-parcours, valider-cartes-decision, detecter-cablages-manquants. CONTEXTE : l audit du registre (2026-08-17) a montre que SEUL le mode verrou-auto (auto-journalisation du verrou d habilitation) continue de tracer les usages - les declarations manuelles des agents ont cesse (derive). DECISION : l outil signale LUI-MEME son usage (espionnage), pas l agent. proteger-verrou-habilitation --agent X --outil Y fait DEJA les deux : usage autorise -> registre-usages-outils.jsonl (mode verrou-auto) ; usage non autorise -> BLOQUE + registre-tentatives-bloquees.jsonl. A FAIRE : 1) dans CHACUN des 3 outils, ajouter la fonction verrouiller_habilitation(agent, outil) (modele EXACT de tester-lancer-non-regression.py : appele proteger-verrou-habilitation.py --agent <agent> --outil <outil> en sous-processus, retourne (code, message), code != 0 = sortie bloquee) ; 2) appeler verrouiller_habilitation dans main() AVANT l action, avec l agent passe en --agent et le nom de l outil en dur ; 3) detecter-cablages-manquants : AJOUTER l option --agent (obligatoire) - il ne l a pas encore (editer-parcours et valider-cartes-decision l ont deja) ; 4) bump version de chaque outil + doc .md historique de version, normes ASCII + LF ; 5) VERIFIER la table d habilitation : chaque outil doit etre assigne a au moins une carte (sinon le verrou bloque TOUT le monde) - si un outil n est dans aucune carte, le signaler sans forcer ; 6) TESTS REELS : agent habilite -> usage autorise + entree verrou-auto dans le registre ; agent non habilite -> BLOQUE + entree registre-tentatives-bloquees.jsonl ; --version de chaque outil ; 7) 0 residu, registre trie decroissant. FIN : lecon Vulcain + ACTIVER MORPHEUS pour adapter les tests (versions pinnees des 3 outils + garde-fous d exclusivite impactes + test-089 ecritures-hors-cycle encore en attente).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 21:15 | session-llm-1 | morpheus | MISSION MORPHEUS : CREER LE GARDE-FOU test-089-ecritures-hors-cycle (anti-recurrence de la derive) + ADAPTER LES PINS DU NOUVEL OUTIL. CONTEXTE : Vulcain a cree detecter-ecritures-hors-cycle v0.1.0 (detection combinee git --porcelain -uall + git diff en primaire, mtime en secours, exclusions workspace/classeur-variables/traces/tmp/__pycache__/AGENTS.md/AGENTS-historique.md/.tmpignore). Verdict : KO (code 1) si Cerberus actif + fichiers de travail modifies ; ATTENTION (code 0) si agent de travail actif. Catalogue 178->179 (v0.2.11), index-tools 199->200. A FAIRE : 1) creer test-089-ecritures-hors-cycle.py (modele template-test : protections importees + triplet point_actif/chrono_etape/bilan_chrono, ASCII/LF) qui verifie : a) --version = v0.1.0 ; b) etat propre (--agent vulcain) = ATTENTION ou OK avec code 0 ; c) PREUVE NEGATIVE : creer un fichier de travail temporaire puis --agent cerberus doit retourner KO (code 1) et lister le fichier, puis supprimer la preuve (0 residu) ; d) les exclusions (AGENTS.md, AGENTS-historique.md, traces/, classeur-variables/) ne sont JAMAIS listees ; e) normes ASCII + LF. 2) ADAPTER les pins : test-007 (catalogue 178->179 + version 0.2.10->0.2.11 si pinnee), test-005 (version catalogue 0.2.10->0.2.11), et tout test qui pinne index-tools Total 199->200. 3) lancer test-089 + les tests repinnes en reel. 4) normes ASCII + LF sur tous les fichiers modifies. FIN : lecon Morpheus + ACTIVER JANUS pour la non-regression complete (verrou : seul Janus lance la suite).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 21:09 | session-llm-1 | vulcain | MISSION VULCAIN : CREER L OUTIL DETECTER-ECRITURES-HORS-CYCLE (garde-fou anti-derive). CONTEXTE : la boucle a ete brisee le 2026-08-17 19:47 - l IA a travaille en solo (optimisations test-032/005/031/085) sans activations formelles. DECISION UTILISATEUR : detection combinee - git en source primaire, mtime en secours. OUTIL A CREER : cerveau-projet/agents/tools/detecter/detecter-ecritures-hors-cycle/detecter-ecritures-hors-cycle.py (+ .md, + entree catalogue generateurs-commande, + entree index-tools.md). FONCTIONNALITES : 1) lire le DERNIER horodatage d activation de AGENTS-historique.md (format | YYYY-MM-DD HH:MM | ...) + l agent actif de AGENTS.md (session-llm-1) ; 2) collecter les fichiers modifies - PRIMAIRE git status --porcelain + git diff --name-only HEAD, SECOURS si git indisponible marcher les fichiers du projet et garder ceux dont mtime > dernier horodatage d activation ; 3) EXCLURE .git/ workspace/ tmp-* .tmp-* .zz-* traces/ __pycache__/ AGENTS.md AGENTS-historique.md + chemins couverts par .tmpignore ; 4) VERDICT v1 : KO si des fichiers de travail sont modifies APRES la derniere activation alors que l agent actif est Cerberus (coordination ne doit jamais ecrire de fichier de travail) ; si un agent de travail est actif, lister les fichiers modifies mais verdict ATTENTION (couverture presumee par la mission en cours). 5) Sortie : liste des fichiers hors cycle (chemin + preuve git/mtime + horodatage) + compteur + verdict final (0 = OK sinon KO avec nombre) + resume. OPTIONS : --depuis <horodatage> (remplacer lecture auto), --agent <nom> (forcer l agent actif), --rapport <fichier> (markdown), --verbose, --version, --aide. CONTRAINTES : ASCII strict, LF, argparse, modele outil-template (shebang, coding ascii, docstring Usage), detection racine projet via AGENTS.md, pas de script tiers. TESTS REELS : etat propre (agent de travail actif, rien modifie apres activation) = 0 hors cycle ; preuve negative (modifier un fichier de travail apres le dernier horodatage alors que l agent actif est Cerberus) = detection 100% puis suppression de la preuve (0 residu) ; --version, --aide, --rapport. FIN : lecon Vulcain + catalogue/index-tools a jour + ACTIVER MORPHEUS pour creer le garde-fou test anti-recurrence.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 21:02 | session-llm-1 | Cerberus | REPARATION BOUCLE BRISEE : retour a Cerberus. DIAGNOSTIC : derive de l IA - depuis l activation de janus (19:47, non-regression finale round performance), le travail a continue en solo (optimisations test-032/005/031/085) sans activations formelles via activer-agent-principal. AGENTS.md et l historique etaient figes sur janus. Cycle Cerberus -> agent -> Cerberus retabli. |
| 2026-08-17 19:47 | session-llm-1 | janus | ROUND PERFORMANCE : non-regression finale apres config adaptative + 3 analyseurs (Vulcain v0.6.1, catalogue 178, index 199)

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 19:27 | session-llm-1 | vulcain | MISSION VULCAIN PHASE 1 - FONDATION ENVIRONNEMENT ADAPTATIF. DECISION UTILISATEUR : etablir des configurations adaptables selon le systeme et les ressources disponibles. SYSTEME MESURE : Windows 10 AMD64, 16 coeurs, Python 3.14.4, disque 44.1 Go libre / 46.6 Go (proche saturation). PROBLEME RACINE : le lanceur a les workers CODES EN DUR (min(os.cpu_count(),16) = 16, a 3 endroits) et verifier-systeme ne detecte NI la RAM NI le disque libre NI la charge CPU. A CREER/CORRIGER : 1) verifier-systeme : ajouter la detection de RAM totale/disponible (psutil en dependance douce comme analyser-io-tests, fallback si absent), disque libre (shutil.disk_usage) et charge CPU (psutil.cpu_percent ou loadavg) - bump version ; 2) NOUVEL OUTIL config-environnement : genere/maintient un fichier cerveau-projet/agents/tools/tester/tester-lancer-non-regression/config-environnement.json contenant {cpu_count, ram_totale_mo, ram_disponible_mo, disque_libre_go, workers_recommandes, timeout_test_recommande, date} - workers_recommandes calcule par paliers (ex: 1-2 coeurs=2, 4=4, 8=8, 16+=12 ou 16 selon RAM libre) - avec options --generer (ecrit), --afficher (lit), --reappliquer, --version, --aide, ASCII/LF, modele outil-template ; 3) tester-lancer-non-regression : remplacer les 3 occurrences min(os.cpu_count(),16) par une fonction lire_workers_config() qui lit config-environnement.json (si absent, generer via config-environnement ou fallback min(cpu_count,16)) - bump version 0.6.0 -> 0.6.1 + doc. TESTS REELS : verifier-systeme affiche RAM/disque/charge ; config-environnement --generer cree le JSON (workers_recommandes coherent avec 16 coeurs) ; lanceur --agent vulcain --tests test-007 lit la config (verifier un log/affichage workers). FIN : lecon Vulcain + REACTIVER CERBERUS (phase 2 : analyser-workers).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 19:21 | session-llm-1 | Cerberus | MESSAGE TROMPEUR CORRIGE (v0.5.11) : le rappel apres activer dit desormais "activer le maillon suivant selon SA carte ; seul le DERNIER maillon reactive Cerberus avec le bilan consolide (jamais de reactivation directe a Cerberus en milieu de chaine)" au lieu de "reactiver Cerberus si activation directe". py_compile OK, normes 0/0, aucun test ne pinne 0.5.10. |
| 2026-08-17 19:20 | session-llm-1 | vulcain | MISSION VULCAIN : CORRIGER LE MESSAGE TROMPEUR DE activer-agent-principal (v0.5.10 -> v0.5.11). PROBLEME : la ligne 795 du .py affiche "la fin de mission suit SA carte (Pattern 13) : reactiver Cerberus si activation directe, sinon activer le maillon suivant" - ce message a INDUIT Cerberus a ecrire "reactiver Cerberus" dans des missions alors que la carte des agents dit "Activer Janus". La REGLE IMMUABLE RELEVE MEME ROUND (regles-groupes-agents.md) dit : les agents se transmettent la releve selon SA carte, SEUL le DERNIER maillon reactive Cerberus avec le bilan consolide, JAMAIS de retour a Cerberus en milieu de chaine. CORRECTION : remplacer le message par "la fin de mission suit SA carte (Pattern 13) : activer le maillon suivant selon SA carte ; seul le DERNIER maillon reactive Cerberus avec le bilan consolide (jamais de reactivation directe a Cerberus en milieu de chaine)". Bump VERSION 0.5.10 -> 0.5.11 + historique .md (v0.5.11 : correction du message trompeur). Verifier : py_compile, normes ASCII/LF, --aide sans traceback, aucun test ne pinne 0.5.10 (confirme). FIN : lecon Vulcain + REACTIVER CERBERUS (pas de Morpheus : aucun test ne pinne la version).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 19:17 | session-llm-1 | Cerberus | VERDICT JANUS VALIDE : cycle KO v0.6.0 implemente et valide, non-regression 86/86. Bilan : le lanceur fait maintenant PASSE 1 = balayage complet (--ko nouveau, collecte de la TOTALITE des KO sans arret) et PASSE 2 = serie KO verte = CONTROLE TERMINE (--ko reprendre --ko-puis-stop), suite complete finale seulement si code partage touche (decision Janus). 9 tests repinnes 0.6.0, test-081 renforce (point 1b), fiche Janus eduquee (WORKFLOW CYCLE KO). valider-cartes 16/16, 0 residu, bumper 0 incoherence, chrono 137.8 s (reference amelioree). |
| 2026-08-17 19:14 | session-llm-1 | janus | NON-REGRESSION FINALE APRES CYCLE KO v0.6.0. Vulcain a corrige le lanceur (balayage + CONTROLE TERMINE), Morpheus a adapte 9 tests (0.5.9 -> 0.6.0, test-081 11/11 avec nouveau point 1b), Buffy a eduque ta fiche (WORKFLOW CYCLE KO). A FAIRE : 1) suite complete en barrieres (les tests 027/031/032/051 qui lancent --agent janus doivent maintenant etre VERTS car la session est sur janus) ; 2) verifier 0 residu + bumper --tous + valider-cartes 16/16 + normes ; 3) bilan consolide a Cerberus (lecon + verdict).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 19:13 | session-llm-1 | buffy | MISSION BUFFY : EDUQUER LA FICHE JANUS SUR LE NOUVEAU CYCLE DU LANCEUR (v0.6.0). CONTEXTE : Vulcain a change le cycle KO - l utilisateur a constate que --ko-puis-stop (v0.5.9) n etait pas dans la fiche de Janus (0 occurrence) ET ne correspondait pas a son modele. NOUVEAU CYCLE A DOCUMENTER dans janus.md : PASSE 1 = --ko nouveau = MODE BALAYAGE COMPLET (toutes les series sans arret, collecte de la TOTALITE des KO dans ko-tests.json, bilan "BALAYAGE COMPLET") ; PASSE 2 = --ko reprendre --ko-puis-stop = valider UNIQUEMENT la serie KO, serie KO verte = "SERIE KO VERTE = CONTROLE TERMINE" (plus de "validation finale requise") ; SUITE COMPLETE FINALE = SEULEMENT si le correctif a touche du code partage (outil/carte pinne par plusieurs tests) - decision Janus. CORRECTIONS : 1) ajouter la ligne --ko-puis-stop dans le tableau Options essentielles de janus.md ; 2) reecrire le WORKFLOW SERIE KO PRIORITAIRE (section --ko) pour refleter le cycle balayage -> serie KO -> suite finale conditionnelle ; 3) verifier la coherence avec les sections WORKFLOW KO OBLIGATOIRE et COMPOSITION CIBLEE (elles mentionnent --relancer-ko et la suite complete - les harmoniser avec le nouveau cycle sans casser). 4) normes ASCII/LF sur janus.md. FIN : lecon Buffy + ACTIVER JANUS pour la non-regression finale (verrou : les tests 027/031/032/051 seront verts en session janus).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 19:10 | session-llm-1 | morpheus | MISSION MORPHEUS : ADAPTER LES TESTS APRES LE CYCLE BALAYAGE DU LANCEUR (v0.5.9 -> v0.6.0, Vulcain). CHANGEMENTS : 1) --ko nouveau est devenu MODE BALAYAGE COMPLET (toutes series sans arret, collecte de la TOTALITE des KO, bilan "BALAYAGE COMPLET : X OK / Y KO" + "PASSER A LA REVALIDATION") ; 2) --ko-puis-stop affiche "SERIE KO VERTE = CONTROLE TERMINE" + note conditionnelle (plus de "VALIDATION FINALE REQUISE"). A FAIRE : 1) grep global de toutes les occurrences 0.5.9 dans les tests (lecon du 3e passage : ne pas rater de pins) et les passer a 0.6.0 - pins connus : test-024, 027, 031, 032, 051, 062, 074, 075, 081. 2) Adapter test-081-serie-ko-garde-fou : il pinne le comportement KO, verifier s il reference "VALIDATION FINALE REQUISE" ou l ancien message --ko-puis-stop et l adapter au nouveau message "CONTROLE TERMINE". 3) Verifier que le message "BALAYAGE COMPLET" et le nouveau comportement --ko nouveau sont couverts (ajouter un point de preuve si besoin). 4) Lancer test-081 + les 8 tests repinnes en reel et confirmer VERT (attention : les tests qui lancent le lanceur avec --agent janus seront KO tant que la session nest pas janus - verrou identite - les signaler mais ne pas les casser). 5) normes ASCII/LF. FIN : lecon Morpheus + ACTIVER BUFFY pour eduquer la fiche Janus (nouveau workflow balayage -> serie KO -> suite finale conditionnelle).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 19:04 | session-llm-1 | vulcain | MISSION VULCAIN : CORRIGER LE CYCLE KO DU LANCEUR DE NON-REGRESSION (v0.5.9 -> v0.6.0). DECISION UTILISATEUR : le mode par defaut doit etre : PASSE 1 = balayage complet qui ne s arrete PAS au premier KO (collecte la TOTALITE des KO), puis PASSE 2 = seule la serie KO reste a valider, serie KO verte = CONTROLE TERMINE (plus de "validation finale requise" obligatoire). La suite complete finale n est relancee que SI le correctif a touche du code partage (outil/carte pinne par plusieurs tests) - decision Janus, pas un message en dur.

CORRECTIONS PRECISES dans tester-lancer-non-regression.py :
1. --ko nouveau = MODE BALAYAGE : vider ko-tests.json puis lancer TOUTES les series SANS arret (la boucle des barrieres ne doit PAS faire break au premier KO quand args.ko == nouveau - elle continue toutes les series pour collecter la totalite des KO), les KO collectes dans ko-tests.json a la fin, rapport final "BALAYAGE COMPLET : X OK / Y KO (totalite des KO collectes)".
2. --ko-puis-stop : remplacer le message "VALIDATION FINALE REQUISE : relancer la suite complete sans --ko-puis-stop" par "SERIE KO VERTE = CONTROLE TERMINE" + une note conditionnelle "Si le correctif a touche du code partage (outil/carte pinne par plusieurs tests), relancer la suite complete pour la garantie anti-cascade (decision Janus)."
3. Bump VERSION 0.5.9 -> 0.6.0 + doc .md alignee (option + historique).
4. Garder : --ko reprendre (defaut) relance la serie KO en priorite ; la barriere KO bloquee arrete toujours (retour 1) ; le chrono du run partiel ne touche jamais la reference globale.

TESTS REELS OBLIGATOIRES :
a. --ko nouveau avec un test en KO injecte : le balayage passe TOUTES les series (ne s arrete pas), collecte le KO, affiche "BALAYAGE COMPLET".
b. --ko reprendre --ko-puis-stop sur un test KO corriger : serie KO verte -> message "CONTROLE TERMINE" (plus de "validation finale requise").
c. --ko reprendre --ko-puis-stop sur un KO persistant : barriere KO bloquee, retour 1 (comportement conserve).
d. py_compile + normes ASCII/LF + --aide sans traceback.

FIN : lecon Vulcain + ACTIVER MORPHEUS pour adapter test-081 (pins 0.5.9 -> 0.6.0 + nouveau message CONTROLE TERMINE) et les autres pins 0.5.9.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 18:57 | session-llm-1 | Cerberus | VERDICT JANUS VALIDE : agent Chiron cree et valide, non-regression 86/86. Bilan : Chiron (16e agent, educateur qui detecte les incoherences et re-eduque), protocole-education-continue cree, 9 tests adaptes (15->16 parcours), test-070 renforce (anti-auto-reactivation), test-024 renforce (anti-scripts), test-058 corrige (exclusivite Buffy : Chiron JE DETECTE JE NE CORRIGE PAS). valider-cartes 16/16 CONFORME, 0 residu, bumper 0 incoherence, normes 0/0, chrono 138.7 s (reference amelioree). |
| 2026-08-17 18:53 | session-llm-1 | janus | REVALIDATION JANUS APRES CORRECTION CHIRON (test-058). Buffy a corrige la carte et la fiche de Chiron (retrait de editer-fichier-agents, exclusivite Buffy) : valider-cartes chiron CONFORME, test-058 6/6, test-055 12/12, test-071 7/7, test-072 10/10, verifier-conformite-fiche CONFORME, normes 0/0. A FAIRE : revalider le KO test-058 (cycle rapide --ko reprendre), puis suite complete en barrieres, puis bilan consolide a Cerberus.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 18:50 | session-llm-1 | buffy | MISSION BUFFY: CORRIGER LA CARTE ET LA FICHE DE CHIRON QUI VIOLENT LE TEST-058 (SEUL BUFFY CORRIGE LES FICHIERS DES AGENTS). DIAGNOSTIC Janus (suite non-regression, barriere D) : test-058 KO car la carte de Chiron utilise editer-fichier-agents (outil EXCLUSIF a Buffy) dans c10 (corriger les incoherences simples) et c12 (ecrire les lecons dans les corrections de l agent cible). Chiron est un EDUCATEUR qui DETECTE et SIGNALE, il ne CORRIGE PAS (comme Argus : JE DETECTE JE NE CORRIGE PAS). CORRECTIONS : 1) carte parcours-chiron.json : c10 retirer l outil editer-fichier-agents et reformuler en documenter les corrections proposees (rapport) puis signaler a Buffy ; c12 retirer editer-fichier-agents et reformuler en ecrire MES lecons dans MES corrections uniquement (jamais les fichiers des autres agents) ; c13 reformuler (bumper uniquement MA fiche si modifiee, pas celle des autres). 2) fiche chiron.md : REGLE ABSOLUE 1 remplacer (ne pas modifier les fichiers des agents, je signale a Buffy) ; retirer editer-fichier-agents de la table Outils P0 et du workflow Purifier ; mettre a jour la liste PARCOURS (c10/c12/c13) et la section Limites. 3) verifier : valider-cartes chiron CONFORME, test-058 VERT (6/6), test-055 VERT, test-071 VERT, test-072 VERT, normes ASCII+LF sur carte et fiche. 4) mettre a jour l empreinte Chiron dans cartes-lock.json (la carte change). 5) lecon Buffy + ACTIVER JANUS pour revalidation (commande activer, PAS reactiver).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 18:31 | session-llm-1 | janus | MISSION JANUS : NON-REGRESSION COMPLETE APRES CREATION DE CHIRON + 2 GARDE-FOUS RENFORCES. CONTEXTE : agent Chiron cree (16e, fiche CONFORME, carte CONFORME), 9 tests adaptes (018/024/026/037/046/070/071/072/073), test-070 renforce (check 5b anti-Reactiver + preuve negative 6d), test-024 renforce (check 15 anti-scripts). A FAIRE : 1) suite complete en mode barrieres (les 9 tests doivent passer, y compris les preuves negatives) ; 2) verifier 0 residu + bumper --tous + valider-cartes 16/16 + normes ; 3) bilan consolide a Cerberus (lecon + verdict).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 18:24 | session-llm-1 | morpheus | MISSION MORPHEUS : ADAPTER LES TESTS APRES LA CREATION DE CHIRON + RENFORCER 2 GARDE-FOUS. CONTEXTE : l agent Chiron (educateur) vient d etre cree par Buffy (fiche chiron.md CONFORME, parcours-chiron.json 17 cases CONFORME). L utilisateur a identifie 2 failles de garde-fous : (1) "reactiver Cerberus" ecrit dans les instructions de mission au lieu de "Activer Janus" (la carte des agents cerveau-projet dit "Activer Janus" - REGLE IMMUABLE JANUS) ; (2) les agents creent des scripts Python pour creer/modifier les fichiers du cerveau au lieu d utiliser les outils dedies (creer-fichier, editer-fichier-agents, editer-parcours).

A FAIRE :
1. ADAPTER les tests qui pinent "15 parcours/agents/cartes" en dur -> 16 (Chiron est le 16e) : test-018, test-026, test-037, test-046, test-070, test-071, test-072, test-073 + TOUT autre test avec un compteur 15 lie au nombre de parcours. Le test-070 utilise glob (dynamique) mais sa docstring dit "15 parcours" - verifier et adapter le compteur en dur s il existe.

2. RENFORCER test-070 (anti-auto-reactivation) : ajouter une verification que TOUTES les fins "Reactiver Cerberus" des agents cerveau-projet sont soit absentes soit documentees comme exceptions legitimes (la REGLE IMMUABLE JANUS dit que les agents cerveau-projet activent JANUS en fin, pas Cerberus directement). Preuve negative : injecter une fin "Reactiver Cerberus" fautive dans une copie et verifier qu elle est detectee.

3. RENFORCER test-024 (anti-scripts-temporaires) OU creer un nouveau garde-fou : verifier que les parcours/cartes des agents ne contiennent PAS d instruction "creer un script temporaire pour ecrire/modifier un fichier du cerveau" (interdit par REGLE ABSOLUE 4 : outils du cerveau uniquement). Les agents doivent utiliser creer-fichier / editer-fichier-agents / editer-parcours.

4. NORMES : ASCII strict + LF sur tous les tests modifies. Version bump si necessaire.

5. VERIFIER : les tests adaptes passent (test-070 avec 16 parcours, test-018 avec 16, etc.) + preuve negative de chaque garde-fou renforce.

FIN : lecon Morpheus + activer JANUS pour la non-regression complete.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 18:05 | session-llm-1 | Cerberus | AGENT CHIRON CREE : fiche (template noyau + variante cerveau-projet), parcours (17 cases c0-c14), corrections.md, inscription AGENTS.md, protocole-education-continue dans regles-immuables/general/ + index-regles-general. valider-cartes CONFORME, valider-conformite-fiche 1 ecart (cle agent: absente du frontmatter - a corriger). 2 FAILLES IDENTIFIEES par l utilisateur : (1) le garde-fou anti-instructions-dans-cases ne detecte pas "reactiver Cerberus" dans les cases de fin au lieu de "activer Janus" - a corriger ; (2) les agents ecrivent des scripts pour creer les fichiers au lieu d utiliser les outils (editer-parcours, editer-fichier-agents) - le garde-fou anti-contournement ne fonctionne pas. MISSION : corriger ces 2 garde-fous, valider conformite-fiche chiron (cle agent: frontmatter), puis relancer la non-regression. |
| 2026-08-17 17:37 | session-llm-1 | buffy | MISSION BUFFY : CREER L AGENT CHIRON (educateur des agents). NOM : Chiron (le centaure formateur de la mythologie grecque). ROLE : Analyser les fiches, corrections, cartes, regles et conventions des agents pour y detecter les incoherences nuisant a leur intelligence operationnelle. QUAND un outil est mis a jour, Chiron re-edue les agents qui l utilisent. CONTEXTE : le protocole-education-continue a deja ete cree dans regles-immuables/general/ (Buffy l a fait avant cette activation). CHIRON EST DISTINCT D ARGUS (Argus detecte les contradictions mecaniquement, Chiron EDUCATION : il lit les corrections, verifie les fiches, detecte les incoherences, et applique les corrections de formation via editer-fichier-agents).

A CREER :
1. FICHE chiron.md : template noyau (8 sections) + variante cerveau-projet (Forces/Faiblesses + Style de travail). Famille: cerveau-projet dans le frontmatter. Sections : Vue d ensemble, PARCOURS (v0.1.0), REGLES ABSOLUES (3 regles : ne pas modifier les fiches sans editer-fichier-agents, ne pas modifier les cartes, ne pas declarer d outils hors sa carte), Outils de base P0 (lire-fichier, bumper/mettre-a-jour-versions, detecter-divergences-version, verifier-conformite-fiche, detecter-cablages-manquants, editer-fichier-agents, enregistrer-usage-outil), WORKFLOW RVAV, UTILISATION DE activer-agent-principal, Forces/Faiblesses, Style de travail, Environnement, Limites, Connexions (Themis, Buffy, Janus, Vulcain). Le ROLE : re-eduer les agents quand les outils/regles/protocoles changent.

2. PARCOURS parcours-chiron.json : 15 cases. c0 RELIRE (corrections + fiche), c0b Confirmation, c1 Recevoir la mission (quel agent), c2 Lire la fiche de l agent cible, c3 Lire les corrections de l agent cible, c4 Lire les regles de l agent cible, c5 Verifier les mises a jour d outils (bumper --tous), c6 Detecter les incoherences (rules vs actions reelles), c7 Verifier la conformite de la fiche, c8 Verifier le parcours/carte, c9 Synthetiser les incoherences, c10 Si incoherences simples -> corriger (editer-fichier-agents), c11 Si incoherences complexes -> signaler a Buffy, c12 Documenter les lecons, c13 Bumper si necessaire, c14 FIN - Activer Janus (second controle). Branches : c9 -> OUI (incoherences) c10, NON c12 ; c10 -> suivant c11 ; c14 type fin "FIN - Activer Janus" avec indice regle REGLE IMMUABLE JANUS. Les outils assigns dans chaque case via indices type outil (catalogue + chemin + commande + nom).

3. corrections.md : fiche vide avec uniquement le frontmatter (version 0.1.0, date creation 2026-08-17).

4. INSCRIPTION AGENTS.md :
   - Ajouter une ligne dans la table Agents secondaires :
     | [Chiron](cerveau-projet/agents/chiron/chiron.md) | cerveau-projet/agents/chiron/ | Educateur des agents -- formation continue | Disponible (en attente) |
   - Mettre a jour index-regles-general (ligne dans la table des protocoles : protocole-education-continue | Education continue des agents : re-eduer quand les outils/regles/protocoles changent | actif |

5. VERIFIER : valider-conformite-fiche --agent chiron CONFORME, valider-cartes-decision --agent chiron CONFORME.

6. NORMES : ASCII strict (aucun accent), LF pur sur tous les fichiers crees. Pas de script tiers. Version 0.1.0 sur tous les fichiers.

FIN : lecon Buffy + reactiver Cerberus avec le bilan (liste des fichiers crees, conformites OK).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 08:56 | session-llm-1 | Cerberus | BILAN CONSOLIDE : chaine --ko-puis-stop VALIDEE - 86 OK / 0 KO, toutes barrieres franchies (E V > A V > D V > C V > B V). --ko-puis-stop v0.5.9 implemente (cycle rapide KO : valide la serie KO puis STOPPE avant A-E, rapport VALIDATION FINALE REQUISE, retour 0 si 0 KO - preuves (a)(b)(c) passees par Vulcain, revalide en reel par Janus sur test-081 et test-026 en ~5s). 9 pins de tests adaptes par Morpheus (024/051/062/074/075/032/027/031/081). KO barriere B resolu : cas orphelin c5 de la carte janus (c4 avait perdu son suivant lors de la mission composition ciblee - corrige par Buffy : c4.suivant=c5, carte v0.4.18 CONFORME, detecter-cablages PROPRE). Lecons des 5 agents enregistrees, 0 residu, bumper 0 incoherent, registres propres. Lecon cles : verrou identite reelle = les tests qui lancent le lanceur ne sont verts que par Janus ; grep global de l ancienne version des le depart ; editer-parcours deduit la cible de --agent. |
| 2026-08-17 08:53 | session-llm-1 | janus | MISSION JANUS (3e passage, suite) : REVALIDATION FINALE. CONTEXTE : Buffy a repare la cause racine du KO barriere B - la case c4 de TA carte avait perdu son suivant (c5 orpheline) lors de la mission composition ciblee ; c4.suivant=c5 restaure, carte v0.4.18 CONFORME, detecter-cablages PROPRE, test-026 10/10 vert. A FAIRE : 1) --ko reprendre --ko-puis-stop (ko-tests.json contient test-026 -> revalider) puis suite complete en barrieres ; 2) verifier 0 residu + bumper --tous + normes ; 3) bilan consolide a Cerberus (lecon + verdict).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 08:49 | session-llm-1 | buffy | MISSION BUFFY : REPARER LA CASE c4 DE LA CARTE JANUS (suivant perdu - cas orphelin c5). CONTEXTE : ta mission composition ciblee (carte janus v0.4.17) a ecrase la case c4 avec editer-parcours --contenu (incident documente dans ta lecon : type restaure mais SUIVANT oublie). Resultat detecte par Janus (detecter-cablages-manquants --tous) : la case c5 est ORPHELINE (rien n y pointe) car c4 n a NI suivant NI branches - test-026 KO (barriere B). DIAGNOSTIC : c3 -> c4 -> (manquant) -> c5 -> c8 ; c4 "Verifier les tests" doit suivre vers c5 "Lancer le combo controle-outil". A FAIRE : 1) via editer-parcours (--agent buffy), restaurer c4.suivant=c5 avec la CASE COMPLETE (type action + titre Verifier les tests + les 6 indices existants + suivant c5) - ne pas toucher au reste ; 2) verifier valider-cartes-decision --agent janus CONFORME + detecter-cablages-manquants --tous : 0 cas orphelin (test-026 doit redevenir vert) ; 3) bump version carte janus 0.4.17 -> 0.4.18 + fiche janus (Pattern 14) ; 4) normes ASCII + LF. FIN : lecon + activer JANUS pour la revalidation (--ko reprendre --ko-puis-stop puis suite complete).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 08:45 | session-llm-1 | janus | MISSION JANUS (3e passage) : REVALIDATION CIBLEE puis suite complete. CONTEXTE : Morpheus a adapte TOUS les pins 0.5.8 restants (027, 031, 081) apres le grep global - au total 9 tests adaptes. A FAIRE : 1) --ko reprendre --ko-puis-stop pour revalider test-081 (il sort de ko-tests.json) puis suite complete ; 2) test-027/031/051/032 ne peuvent etre verts que par ta session (verrou identite reelle) ; 3) verifier 0 residu + bumper --tous + normes ; 4) bilan consolide a Cerberus (lecon + verdict).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 08:44 | session-llm-1 | morpheus | MISSION MORPHEUS (3e passage) : ADAPTER TOUS LES PINS 0.5.8 -> 0.5.9 RESTANTS (le grep global en a trouve 3 : test-027-series-garde-fou lignes 190-191, test-031-chrono-reference lignes 24/154-155, test-081-serie-ko-garde-fou lignes 6/22/118/128/131-132). VERIFIER ensuite : les 3 tests doivent etre verts (test-027, test-031, test-081) - attention test-031/027/081 lancent le lanceur avec --agent janus (verrou identite reelle : ils ne seront pleinement verts que par Janus, mais le point --version doit passer seul). NORMES : ASCII strict + LF. FIN : lecon + activer JANUS pour la revalidation (--ko reprendre --ko-puis-stop) puis suite complete.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 08:42 | session-llm-1 | janus | MISSION JANUS (2e passage) : REVALIDATION CIBLEE puis suite complete. CONTEXTE : Morpheus a adapte le pin test-032 (0.5.8 -> 0.5.9) decouvert par ta barriere E. A FAIRE : 1) --ko reprendre pour revalider test-032 (il sort de ko-tests.json) ; 2) suite complete en barrieres - test-032 et test-051 doivent passer (verrou identite reelle : ils ne peuvent etre verts que par ta session) ; 3) verifier 0 residu + bumper --tous + normes ; 4) bilan consolide a Cerberus (lecon + verdict).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 08:41 | session-llm-1 | morpheus | MISSION MORPHEUS (2e passage) : ADAPTER LE PIN 0.5.8 -> 0.5.9 DANS test-032-pool-workers (KO barriere E decouvert par Janus - test-032 pinne encore --version v0.5.8). VERIFIER ensuite : test-032 doit etre vert (10/10). NORMES : ASCII strict + LF. FIN : lecon + activer JANUS pour la revalidation ciblee (--ko reprendre) puis suite complete.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 08:38 | session-llm-1 | janus | MISSION JANUS : VALIDATION FINALE COMPLETE apres la chaine ko-puis-stop (Vulcain lanceur v0.5.9 + Morpheus pins 0.5.9). CONTEXTE : --ko-puis-stop implemente (cycle rapide KO, preuves (a)(b)(c) passees par Vulcain), 5 tests adaptes (024/051/062/074/075), test-066 vert (compagnons 0.5.9 trouves). A FAIRE : 1) revalidation ciblee : --ko reprendre (la serie KO doit etre vide ou se vider) + --relancer-ko pour revalider les KO du dernier run si besoin ; 2) suite complete en mode barrieres - le KO test-051 (verrou identite reelle : ne peut etre vert que par ta session) doit passer ; 3) verifier 0 residu + bumper --tous 0 incoherent + normes ; 4) bilan consolide a Cerberus (lecon + verdict).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 08:36 | session-llm-1 | morpheus | MISSION MORPHEUS : ADAPTER LES 5 PINS 0.5.8 -> 0.5.9 DE tester-lancer-non-regression apres la mission Vulcain (--ko-puis-stop v0.5.9). TESTS A ADAPTER (ils pinent v0.5.8) : test-024-scripts-temporaires (ligne ~255), test-051-registre-tests (ligne ~6), test-062-rating-protection (ligne ~13), test-074-relancer-ko (lignes ~5/21/120/125), test-075-filtre-serie-relancer-ko (lignes ~6/21/127/132). VERIFIER ensuite : test-066-bumper-compagnons-garde-fou doit redevenir VERT (ses 3 KO restants sont causes par les compagnons 0.5.9 introuvables tant que les pins sont a 0.5.8). NORMES : ASCII strict + LF sur les tests modifies. FIN : lecon Morpheus + activer JANUS pour la validation finale complete (mission Janus precedente interrompue a reprendre : revalidation ciblee puis suite complete en barrieres).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 08:31 | session-llm-1 | vulcain | MISSION VULCAIN : IMPLEMENTER --ko-puis-stop DANS tester-lancer-non-regression (cycle rapide KO). CONTEXTE : demande utilisateur + recommandation Cerberus (workflow en 2 temps) - le cycle de correction KO doit pouvoir valider UNIQUEMENT la serie KO persistante puis STOPPER, sans payer les ~90s des series A-E a chaque correctif. FONCTIONNALITE : nouvelle option --ko-puis-stop (avec --ko reprendre, defaut) : apres la BARRIERE KO FRANCHIE (100% verte), la suite s ARRETE avec un rapport clair "serie KO validee - validation finale requise" et retour 0 si 0 KO. Comportements : (1) si le fichier ko-tests.json est VIDE, avertir que --ko-puis-stop est ignore et lancer la suite normalement ; (2) si la barriere KO est BLOQUEE, comportement existant (STOP + retour 1) ; (3) le chrono affiche mode barriere-ko et NE touche PAS la reference globale (run partiel) ; (4) --rapport ecrit le rapport de la serie KO. CONTRAINTES : ASCII strict, LF, bump 0.5.8 -> 0.5.9 (5 tests pinent 0.5.8 : test-024/051/062/074/075 -> mission Morpheus apres), documenter dans le .md (option + versionning), pas de script tiers. TESTS REELS : (a) injecter 1 test KO dans ko-tests.json, lancer --ko reprendre --ko-puis-stop -> la serie KO passe, la suite s arrete AVANT A-E, retour 0 ; (b) barriere KO bloquee -> retour 1 ; (c) fichier KO vide + --ko-puis-stop -> avertissement + suite lancee normalement. FIN : lecon Vulcain + activer MORPHEUS pour adapter les 5 pins + activer JANUS pour la validation finale complete (la mission Janus precedente interrompue sera reprise dans cette validation).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 08:21 | session-llm-1 | janus | MISSION JANUS : REVALIDATION CIBLEE + NON-REGRESSION COMPLETE

CONTEXTE : les 3 KO de la serie E sont corriges : (1) test-028 spec activer-agent-principal alignee 0.5.10 (Janus), (2) test-035 declaration registre fautive retiree (Janus), (3) test-024 pin editer-parcours 0.1.4 adapte (Morpheus, 16/16 OK).

A FAIRE :
1. --ko reprendre : revalider les 3 tests KO en cible (ils doivent sortir de ko-tests.json).
2. Puis suite complete en mode barrieres.
3. Verifier 0 residu + bumper --tous 0 incoherent + normes.

FIN : lecon Janus + REACTIVER CERBERUS avec le bilan consolide (mission outils informationnels v0.3.0).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 08:20 | session-llm-1 | morpheus | MISSION MORPHEUS : ADAPTER LE PIN TEST-024 (editer-parcours v0.1.3 -> v0.1.4)

CONTEXTE : la non-regression (Janus) a detecte 3 KO en serie E, 2 deja resolus par Janus (test-028 spec activer-agent-principal alignee 0.5.10, test-035 declaration registre fautive retiree). Reste test-024 : il pinne 'editer-parcours v0.1.3' (point 5, --version) alors que l outil est passe a 0.1.4 dans la mission outils informationnels.

A FAIRE :
1. Adapter test-024 : remplacer la reference v0.1.3 par v0.1.4 (UNIQUEMENT editer-parcours, verifier le contexte exact).
2. Lancer test-024 pour verifier qu il est vert (16 points).
3. Normes ASCII strict + LF pur.
4. NE PAS lancer la non-regression complete (Janus va relancer --ko reprendre).

FIN : lecon Morpheus + ACTIVER JANUS pour la revalidation ciblee puis suite complete.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 08:14 | session-llm-1 | janus | MISSION JANUS : NON-REGRESSION COMPLETE APRES OUTILS INFORMATIONNELS (v0.3.0)

CONTEXTE : chaine Vulcain -> Morpheus terminee. (1) Vulcain a cree le mecanisme MESSAGES INFORMATIONNELS (template outil-template.py/.sh v0.3.0-beta, fonction afficher_messages_info) et l a branche dans 5 outils critiques : editer-parcours 0.1.4, editer-fichier 0.4.3, activer-agent-principal 0.5.10, creer-fichier 0.3.2, combos-maj-readme-massive 0.1.6. (2) Morpheus a adapte le pin test-020 (combos-maj-readme-massive 0.1.5 -> 0.1.6, 46/46 OK).

A FAIRE :
1. Lancer la non-regression complete en mode barrieres (--agent janus, seul habile).
2. ATTENTION : les 5 outils modifies affichent desormais une section MESSAGES POUR L AGENT en fin de sortie reelle - si un test echoue, verifier si c est une comparaison de sortie entiere (a adapter par Morpheus) ou un vrai KO.
3. Si KO : --relancer-ko apres correctif, puis suite complete.
4. Verifier 0 residu + normes + bumper --tous 0 incoherent.

FIN : lecon Janus + REACTIVER CERBERUS avec le bilan consolide.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 08:11 | session-llm-1 | morpheus | MISSION MORPHEUS : ADAPTER LE PIN TEST-020 (combos-maj-readme-massive 0.1.5 -> 0.1.6)

CONTEXTE : Vulcain a termine la mission OUTILS INFORMATIONNELS (messages contextuels aux agents, template v0.3.0-beta + branche dans 5 outils : editer-parcours 0.1.4, editer-fichier 0.4.3, activer-agent-principal 0.5.10, creer-fichier 0.3.2, combos-maj-readme-massive 0.1.6). Le seul pin de test reel identifie : test-020-combos-clio pinne 'combos-maj-readme-massive 0.1.5' (lignes 14 et 152).

A FAIRE :
1. Adapter test-020 : remplacer '0.1.5' par '0.1.6' (docstring ligne 14 + verification ligne 152-153) UNIQUEMENT pour combos-maj-readme-massive (pas les autres combos).
2. Lancer test-020 pour verifier qu il est vert.
3. ATTENTION : le nouveau mecanisme afficher_messages_info affiche des messages supplementaires dans la sortie des outils modifies - verifier que test-020 ne depend pas d une sortie exacte sans les messages (si le test verifie une sous-chaine, c est OK ; si il compare la sortie entiere, adapter).
4. Normes ASCII strict + LF pur sur le test modifie.
5. NE PAS lancer la non-regression complete (reserve a Janus).

FIN : lecon Morpheus + ACTIVER JANUS pour la non-regression complete en mode barrieres.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 07:49 | session-llm-1 | vulcain | Identification LLM - demarrage de session |
| 2026-08-17 07:37 | session-llm-1 | vulcain | MISSION VULCAIN : RENDRE LES OUTILS INFORMATIONNELS (messages contextuels aux agents)

CONTEXTE (demande utilisateur 2026-08-17) : les outils doivent passer des MESSAGES aux agents dans leur sortie, aux endroits importants. Exemple : 'si vous avez modifie tel fichier, ne pas oublier de modifier tel fichier'. Le but : l agent voit TOUJOURS les consequences de son action (fichiers compagnons a mettre a jour) sans avoir a les deviner. Precurseurs existants : mettre-a-jour-versions affiche deja 'FICHIERS COMPAGNONS A METTRE A JOUR' + 'RAPPEL OBLIGATOIRE', generateurs-case affiche des 'RAPPEL ASCII/RVAV/DELEGATION'. Il faut GENERALISER ce mecanisme.

ETAPE 1 - AUDIT DES OUTILS A MESSAGES (analyser, NE PAS modifier) :
Inventorier les outils qui ECRIVENT/modifient dans le projet et identifier les MESSAGES INFORMATIONNELS qu ils devraient afficher (fichiers compagnons, regles a respecter apres l action, etapes suivantes). Au minimum, auditer ces outils critiques :
- editer-fichier / editer-fichier-agents : apres modification, rappeler que le fichier modifie peut impacter index-tools, README, tests (Morpheus), carte/fiche (Pattern 14) selon le type
- editer-parcours : apres bump de carte, rappeler de synchroniser la fiche (Pattern 14) + verifier valider-cartes-decision
- activer-agent-principal : apres activation, rappeler la regle RELEVE MEME ROUND (l agent active doit enchainer immediatement)
- creer-fichier / ajouter-contenu-fichier : rappeler index-tools + catalogue + doc obligatoire + assignation a un agent
- combos-maj-readme-massive : rappeler version-readme.txt + badge + index-tools
- enregistrer-usage-outil : rien de special a priori (juste confirmation)
- generer un RAPPORT : un tableau de synthese des messages par outil (outil -> message propose)

ETAPE 2 - MECANISME DANS LE TEMPLATE (modifier outil-template.py + outil-template.sh + outil-template-python.md + outil-template.md) :
Ajouter une fonction/bloc standard afficher_messages_info() qui :
- affiche une section '=== MESSAGES POUR L AGENT ===' avec des lignes ' > ' (contextuelles, apres l action reussie)
- est appelable en fin de main() avec une liste de messages simples (aucune logique de detection complexe exigee : chaque outil fournit SES messages statiques contextuels, le template fournit juste l affichage)
- les messages sont TOUJOURS affiches (pas une option) - c est le contrat informationnel
- le .md du template documente la section 'Messages informationnels' avec des exemples

ETAPE 3 - BRANCHER LES MESSAGES DANS LES 5-6 OUTILS CRITIQUES IDENTIFIES A L ETAPE 1 (pas tous, juste les plus importants : editer-parcours, editer-fichier, activer-agent-principal, creer-fichier, combos-maj-readme-massive) en utilisant le mecanisme du template.

CONTRAINTES : ASCII strict, LF, argparse, stdlib, pas de script tiers, prototypes verifier_nommage/verifier_doc_presente conserves, bump version des outils modifies + .md + ligne historique, normes verifiees.

VERIFICATIONS : py_compile des outils modifies, --version OK, un test reel d un outil avec message affiche (capture stdout), bumper --tous 0 incoherent, normes ASCII/LF 0/0.
FIN : lecon Vulcain + ACTIVER MORPHEUS pour adapter les tests qui pinent les versions des outils modifies (signaler lesquels dans le bilan).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 07:33 | session-llm-1 | Cerberus | BILAN BUFFY (mission education Janus composition ciblee) : la fiche janus.md a recu la section WORKFLOW COMPOSITION CIBLEE (immuable, 6 pas : identifier fichiers modifies -> choisir le mode le plus leger --fichiers/--profil/--tags/--series -> desactiver les tests inutiles --desactiver -> valider les series concernees -> reactiver en fin -> suite complete UNIQUEMENT en validation finale). La carte parcours-janus.json v0.4.17 a recu la regle COMPOSITION CIBLEE dans la case c4 (via editer-parcours). Aucun test ne pinne la version janus (0.4.15 introuvable dans les tests). Verifications : valider-cartes --agent janus CONFORME, valider-cartes --tous 15/15, bumper --tous 0 incoherent, normes ASCII/LF 0/0, 0 residu. Lecon Buffy enregistree (editer-parcours --contenu remplace TOUTE la case : toujours fournir type+titre+indices). Pas besoin de Morpheus ni Janus (aucun test modifie). |
| 2026-08-17 07:29 | session-llm-1 | buffy | MISSION BUFFY : RE-EDUQUER JANUS A LA COMPOSITION CIBLEE DE LA NON-REGRESSION

CONTEXTE (demande utilisateur) : Janus lance encore la suite complete par reflexe, meme quand il ne controle qu une petite partie du projet. La suite a POURTANT toutes les briques : --fichiers (profils deduits des fichiers modifies), --profil, --tags, --categorie, --desactiver/--activer (on/off persistant), --etat-tests/--etat-categories, --series. Ce qui manque : la DECISION de composition dans la fiche et la carte de Janus - le workflow qui lui ordonne de ne lancer QUE les tests utiles au fichier teste et de desactiver les inutiles pour alleger le temps total.

ETAT ACTUEL :
- Fiche janus.md : le tableau Options essentielles liste --fichiers/--profil/--desactiver/--tags/--categorie MAIS il n y a AUCUN workflow de decision (comment choisir selon les fichiers modifies, quand desactiver, quand lancer la suite complete).
- Carte parcours-janus.json v0.4.15 : la case c4 (Verifier les tests) a une regle WORKFLOW SERIE KO mais AUCUNE regle de composition ciblee selon les fichiers.

A FAIRE :
1. FICHE janus.md : ajouter une section WORKFLOW COMPOSITION CIBLEE (immuable) apres la section WORKFLOW KO : (a) AVANT de lancer, j identifie les fichiers modifies de la mission ; (b) je choisis le mode le plus leger adapte : --fichiers <fichiers> (deduction auto des profils) OU --profil <profils> OU --tags/--categorie si le besoin est fin ; (c) je DESACTIVE les tests non pertinents pour le controle (--desactiver <nums> / --desactiver-categorie <nom>, persistant) apres avoir consulte --etat-tests/--etat-categories ; (d) je lance les series concernees seulement (--series) ; (e) la SUITE COMPLETE n est lancee QU EN VALIDATION FINALE de la mission (apres que les series ciblees sont 100% vertes) ; (f) je REACTIVE toujours les tests desactives en fin de mission (--activer) pour ne pas polluer les prochains lancements SAUF si la desactivation est voulue durablement.
2. CARTE parcours-janus.json : enrichir la case c4 (Verifier les tests) avec une regle COMPOSITION CIBLEE (meme workflow resume en 3-4 lignes : identifier fichiers modifies -> choisir --fichiers/--profil/--tags -> desactiver les tests inutiles (--desactiver) -> --series concernees -> suite complete uniquement en validation finale -> reactiver en fin). Bump version 0.4.15 -> 0.4.16.
3. Synchroniser la fiche (Pattern 14 : version du parcours) et verifier valider-cartes-decision --agent janus CONFORME.
4. NE PAS toucher au lanceur ni aux tests (mission d education seulement). Pas de test a adapter sauf si un test pinne la version de la carte janus (verifier test-004/test-018 - si pin, signaler dans le bilan pour Morpheus).

VERIFICATIONS : valider-cartes --agent janus CONFORME, normes ASCII strict + LF pur sur fiche + parcours, bumper coherence (mettre-a-jour-versions --tous : 0 incoherent).
FIN : lecon Buffy + ACTIVER MORPHEUS si des pins de version de la carte janus existent (sinon reactiver Cerberus directement avec le bilan).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 07:26 | session-llm-1 | Cerberus | BILAN CONSOLIDE (Janus, chaine bumper v0.1.4) : NON-REGRESSION COMPLETE 86 OK / 0 KO, toutes les barrieres franchies (KO, E, A, D, C, B), chrono 133.9s (base 85 tests). Mission : extension du regex du bumper mettre-a-jour-versions aux formats .md invisibles (tableau/blockquote/liste/## Version) + correction de 2 vrais ecarts caches (generateurs-carte.md 0.3.0->0.3.1, generateurs-ligne.md 0.3.1->0.3.0) + normalisation de 7 .md en champ standard (valider-case, tester-protections, editer-fichier-agents, evaluer-processus, detecter-evaluations-incompletes, verifier-conformite-fiche, generateurs-amelioration) + bump 0.1.3->0.1.4. Tests : pins v0.1.4 adaptes (test-066 11/11, test-067 8/8 preuve negative valide), test-035 corrige (declaration registre fautive vulcain editer-fichier retiree), test-048 vert (lecon Janus). Bumper --tous : 141 outils, 0 incoherent (les 17 formats autrefois invisibles sont desormais verifies). Lecons Vulcain/Morpheus/Janus enregistrees, 0 residu, normes ASCII/LF 0/0. |
| 2026-08-17 07:16 | session-llm-1 | janus | MISSION JANUS : NON-REGRESSION COMPLETE APRES BUMPER v0.1.4

CONTEXTE : chaine Vulcain -> Morpheus terminee. (1) Vulcain a etendu le regex du bumper mettre-a-jour-versions aux formats .md invisibles (tableau/blockquote/liste/## Version), corrige 2 vrais ecarts (generateurs-carte.md 0.3.1, generateurs-ligne.md 0.3.0), normalise 7 .md en champ standard (valider-case, tester-protections, editer-fichier-agents, evaluer-processus, detecter-evaluations-incompletes, verifier-conformite-fiche, generateurs-amelioration) et bumpe le bumper 0.1.3 -> 0.1.4. (2) Morpheus a adapte les pins v0.1.3 -> v0.1.4 dans test-066 (11/11 OK) et test-067 (8/8 OK, preuve negative valide).

A FAIRE :
1. Lancer la non-regression complete en mode barrieres (--agent janus obligatoire, seul habile).
2. Si KO : identifier les tests, les corriger uniquement si c est un pin de version perime directement lie a cette mission (sinon activer l agent habilite), puis --relancer-ko.
3. Rapport final : barriere par barriere, chrono pool, comparaison reference, tests lents si presents.
4. Verifier 0 residu (tmp-*, .zz-*) et normes.

FIN : lecon Janus + REACTIVER CERBERUS avec le bilan consolide.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 07:15 | session-llm-1 | morpheus | MISSION MORPHEUS : ADAPTER LES 2 TESTS PINNEURS DU BUMPER v0.1.4

CONTEXTE : Vulcain vient de terminer sa mission (extension du regex du bumper mettre-a-jour-versions aux formats .md invisibles + correction de 2 ecarts + normalisation de 7 .md + bump 0.1.3 -> 0.1.4). Le bumper a signale 2 fichiers compagnons pinant l ancienne version v0.1.3 : test-066-bumper-compagnons-garde-fou et test-067-bumper-tous-audit (8 et 11 occurrences).

A FAIRE :
1. Adapter test-066 et test-067 : remplacer toutes les references v0.1.3 par v0.1.4 (docstring, verifier 1c --version, etc).
2. Lancer les 2 tests adaptes pour verifier qu ils sont verts (ils lanceront le bumper --tous : doit donner 0 incoherent).
3. ATTENTION : le regex etendu du bumper detecte desormais les formats tableau/blockquote/liste/## Version. Verifier que test-067 reste valide (sa preuve negative injecte un ecart dans la doc du bumper elle-meme - le champ standard '**Version** : 0.1.4' doit rester remplacable).
4. Normes ASCII strict + LF pur sur les 2 tests modifies.
5. NE PAS lancer la non-regression complete (reserve a Janus). Ne pas toucher au bumper ni aux .md (mission Vulcain terminee).

FIN : lecon Morpheus dans corrections.md + ACTIVER JANUS pour la non-regression complete en mode barrieres.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 07:08 | session-llm-1 | vulcain | MISSION VULCAIN : CORRIGER LES 2 ECARTS .md + ETENDRE LE BUMPER AUX FORMATS INVISIBLES

CONTEXTE (demande utilisateur, audit croise Buffy) : l audit des .md vs constante VERSION a revele que le bumper mettre-a-jour-versions a un ANGLE MORT : son regex _RE_MD_VERSION ne couvre QUE '**Version :** X.Y.Z' en debut de ligne. Resultat : --tous declare 'coherent' sans rien verifier pour les .md en format TABLEAU, blockquote, liste, ou section ## Version. 2 VRAIS ecarts existent actuellement, invisibles pour le bumper : generateurs-carte (.py 0.3.1, spec 0.3.1, .md TABLEAU 0.3.0 -> en retard) et generateurs-ligne (.py 0.3.0, spec 0.3.0, .md TABLEAU 0.3.1 -> en avance).

OUTIL A CORRIGER : cerveau-projet/agents/tools/mettre-a-jour/mettre-a-jour-versions/mettre-a-jour-versions.py (+ .md)
1. CORRIGER les 2 .md desalignes (via editer-fichier ou bumper lui-meme) : generateurs-carte.md 0.3.0 -> 0.3.1 (tableau ligne 11), generateurs-ligne.md 0.3.1 -> 0.3.0 (tableau ligne 11). NE PAS toucher au .py ni aux specs (deja bons).
2. ETENDRE la detection des versions .md pour couvrir les formats actuellement invisibles : (a) tableau markdown '| **Version** | X.Y.Z |', (b) blockquote '> **Version** : X.Y.Z', (c) liste '- Version : X.Y.Z' / '- **X.Y.Z**', (d) section '## Version' avec liste '- vX.Y.Z' / '- **X.Y.Z**'. Attention : ne pas creer de faux positifs avec les sections '## Versionning' (tableaux historiques) ni les exemples de commandes '--version'. Le champ 'Version du fichier' de generateurs-amelioration (2.3.0) est la version du fichier JSON de themes, PAS de l outil -> NE PAS le confondre (l outil py est 2.1.0, c est legitime et documente).
3. APRES extension : relancer --tous (dry-run) : les 2 ecarts doivent devenir INCOHERENT une fois corriges ? non -> les 2 .md doivent etre corriges AVANT, donc --tous doit donner 0 incoherent avec les 2 formats tableau DETECTES et verifies. Les 8 .md sans champ standard (valider-case 1.1.1 en liste, tester-protections '- Version : 0.2.0', editer-fichier-agents '> **Version : 0.1.0-beta**', regenerer-catalogue '> **Version** : 1.1.1', evaluer-processus, detecter-evaluations-incompletes, valider-numerotation 0.2.0-py tableau, verifier-conformite-fiche sans version) doivent etre DETECTES et leur version comparee a la reference (suffixe -py/-beta conserve, comme le bumper le fait deja). Si un .md n a VRAIMENT aucune version detectable (verifier-conformite-fiche), l ajouter en champ standard dans le .md pour le rendre verifiable.
4. BUMPER : bump version 0.1.3 -> 0.1.4 (py + md, via le bumper lui-meme) + ligne historique dans le .md. NE PAS toucher aux tests (test-066/test-067 pinent v0.1.3 -> mission Morpheus apres).
5. VERIFICATIONS : py_compile, --version, --tous dry-run = 0 incoherent (les 17 formats autrefois invisibles sont desormais verifies), test-067 ne doit PAS etre lance par toi (artefact session verrou), normes ASCII strict + LF pur sur les fichiers modifies, declarer tes usages au registre (editer-fichier, mettre-a-jour-versions).
FIN : lecon Vulcain dans corrections.md + ACTIVER MORPHEUS pour adapter test-066/test-067 (pins v0.1.3 -> v0.1.4) puis reverdir la non-regression.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 23:43 | session-llm-1 | Cerberus | VALIDATION FINALE TERMINEE : garde-fou reactiver repare et prouve. Bilan consolide : (1) CAUSE RACINE : test-070 v1 ne scannait QUE les cases type fin - etendu v2 a TOUTES les cases (detections REACTIVER_NON_CERBERUS + FORME_FAUTIVE avec exceptions). (2) CORRECTIONS CARTES : 37 cases reactiver fautives corrigees sur 14 parcours (Buffy) - 31 initiales + 6 detectees par le garde-fou etendu - bumps argus 0.1.11, athena 0.3.4, atlas 0.4.7, buffy 0.4.12, cerberus 0.5.3, clio 0.5.11, janus 0.4.15, minerve 0.3.5, morpheus 0.4.12, promethee 0.3.5, themis 0.4.7, vulcain 0.4.26, fiches Pattern 14 synchronisees. (3) TESTS : pins adaptes test-005 atlas 0.4.7, test-013 cerberus 0.5.3, test-016 buffy 0.4.12, test-004 morpheus 0.4.12. (4) NON REGRESSION COMPLETE : 86 OK / 0 KO, toutes les barrieres franchies (E, A, D, C, B), chrono 128.8s base 86 tests, test-035 corrige (mission Morpheus reformulee), bumper 0 incoherent, 0 residu, lecons Buffy/Morpheus/Janus enregistrees. |
| 2026-08-16 23:36 | session-llm-1 | janus | MISSION JANUS : NON REGRESSION COMPLETE en mode barrieres. CONTEXTE : correction des cases reactiver fautives (37 cases au total sur 14 parcours : 31 par Buffy + 6 detectees par le garde-fou etendu), garde-fou test-070 v2 etendu a TOUTES les cases (detections REACTIVER_NON_CERBERUS + FORME_FAUTIVE), pins de version adaptes (test-005 atlas 0.4.7, test-013 cerberus 0.5.3, test-016 buffy 0.4.12, test-004 morpheus 0.4.12), test-070 11 OK, verifications locales 004 16/16, 005 28/0, 013 22/0, 016 20/0, 028 8/0, 030 10/0, 063 11/0, valider-cartes 15/15, bumper 0 incoherent, normes ASCII/LF 0 ecart, 0 residu, lecons Buffy/Morpheus enregistrees. LANCER la suite complete en mode barrieres (--ko reprendre puis suite), traiter les KO eventuels (artefacts session verrou attendus si un autre agent que janus a lance des tests : les relancer sous janus), puis reactiver Cerberus avec le bilan consolide.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 23:33 | session-llm-1 | morpheus | RETOUR MORPHEUS : les 6 cases reactiver residuelles sont corrigees par Buffy (buffy c39, cerberus c15c, janus c32 + cT8/cT9/cT10) avec bumps buffy 0.4.12, cerberus 0.5.3, janus 0.4.15 et fiches Pattern 14 synchronisees. test-070 v2 est VERT (11 OK / 0 KO), valider-cartes 15/15, bumper 0 incoherent, normes 0 ecart. FINALISER : 1) adapter les tests qui pinent les anciennes versions des parcours (005 argus 0.1.10 / athena 0.3.3 / atlas 0.4.6, 012 cerberus 0.5.1, 013 atlas 0.4.6 + cerberus 0.5.1, 016 atlas 0.4.6 + buffy 0.4.10, 018 athena 0.3.3, 028 cerberus 0.5.1, 042 athena 0.3.3, 044 minerve/promethee 0.3.4, 004 morpheus 0.4.11 + buffy 0.4.11/0.4.12 + cerberus 0.5.2/0.5.3 + janus 0.4.14/0.4.15) en verifiant chaque pin ; 2) verifier la non regression locale des tests adaptes ; 3) lecon Morpheus + REVENIR A JANUS pour la non regression complete en mode barrieres.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 23:32 | session-llm-1 | buffy | MISSION BUFFY : CORRIGER LES 6 CASES REACTIVER RESTANTES DETECTEES PAR LE GARDE-FOU ETENDU (test-070 v2 scanne desormais TOUTES les cases). CAS MAJEURS (detectes KO) : 1) buffy c39 'Atlas me REACTIVE en me fournissant sa carte' -> 'Atlas me RE-ACTIVE (commande activer) en me fournissant sa carte' (bump 0.4.11->0.4.12) ; 2) cerberus c15c 'Janus recontrole et me reactive ; je relis son rapport' -> 'Janus recontrole puis REACTIVE Cerberus avec son rapport ; je relis son rapport' (bump 0.5.2->0.5.3) ; 3) janus c32 'Themis me REACTIVE en me fournissant son rapport' -> 'Themis me RE-ACTIVE (commande activer) en me fournissant son rapport' (bump 0.4.14->0.4.15). CAS MINEURS (lever l ambiguite, memes motifs) : 4) janus cT8 'Elle corrige puis me reactive (boucle KO)' ; 5) janus cT9 'Il corrige puis me reactive (boucle KO)' ; 6) janus cT10 'Elle corrige puis me reactive (boucle KO)' -> tous les trois 'me RE-ACTIVE (commande activer) pour re-controle (boucle KO)' en gardant 'PAS reactiver : je suis la chaine, seul le dernier maillon reactive Cerberus'. CONTRAINTES : editer-parcours (barrage n3), bump + fiche Pattern 14 des 3 agents, valider-cartes 15/15, normes ASCII/LF, registre, lecon. REVENIR A MORPHEUS (activer morpheus) pour finaliser les pins de version et la validation.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 23:29 | session-llm-1 | morpheus | MISSION MORPHEUS : REPARER LE GARDE-FOU ANTI-REACTIVER ET ADAPTER LES PINS DE VERSION. CONTEXTE : Buffy a corrige 31 cases fautives 'reactiver X (X != cerberus)' sur 11 parcours (argus 0.1.11, athena 0.3.4, atlas 0.4.7, buffy 0.4.11, cerberus 0.5.2, clio 0.5.11, minerve 0.3.5, morpheus 0.4.12, promethee 0.3.5, themis 0.4.7, vulcain 0.4.26) avec fiches Pattern 14 synchronisees. ETAPE 1 : etendre test-070 (anti-auto-reactivation) pour scanner TOUTES les cases des 15 parcours et pas seulement les cases type fin (la faille) : toute commande reactiver <agent> avec agent != cerberus/session-llm est KO ; toute forme 'me/le/la reactivera(i)' a cible non-Cerberus est KO ; exceptions correctes a garder : 'reactiver ramene toujours a Cerberus', 'PAS reactiver', 'FIN - Reactiver <gardien>', 'reactiver session-llm-1 ... cerberus'. Ajouter une PREUVE NEGATIVE (injecter une violation dans une copie temp et constater le KO). ETAPE 2 : adapter les tests qui pinent les anciennes versions des parcours (005 argus 0.1.10/athena 0.3.3/atlas 0.4.6, 012 cerberus 0.5.1, 013 atlas 0.4.6 + cerberus 0.5.1, 016 atlas 0.4.6 + buffy 0.4.10, 018 athena 0.3.3, 028 cerberus 0.5.1, 042 athena 0.3.3, 044 minerve/promethee 0.3.4, 004 morpheus 0.4.11) en verifiant a chaque fois que le pin est bien une version de parcours. ETAPE 3 : verifier la non regression locale des tests adaptes + valider-cartes 15/15 + normes ASCII/LF + bumper, puis REVENIR A JANUS pour la non regression complete en mode barrieres. FIN : lecon Morpheus + revenir a Janus pour la non regression (Janus reactive Cerberus avec le bilan consolide).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 23:22 | session-llm-1 | buffy | MISSION BUFFY (demande utilisateur, faille garde-fou test-070) : CORRIGER TOUTES LES MENTIONS 'reactiver <agent != cerberus>' DANS LES 15 PARCOURS. CONTEXTE: la regle 'reactiver ramene TOUJOURS a Cerberus' est violee par ~58 segments dans les cases non-fin (test-070 ne scanne que les fins, faille identifiee). LA VERITE : reactiver <session> <raison> <agent_precedent> = reactiver CERBERUS, le 3e arg est informatif. Cas a corriger dans parcours-cerberus.json (le plus touche) : c12b 'DEVIATION : reactiver Buffy' -> 'ACTIVER Buffy (commande activer, PAS reactiver)', c15/c21 'reactiver l'agent d'origine' -> 'ACTIVER l'agent d'origine', c29a/c9d/c10d/c15d/c19d 'il me reactivera avec le bilan' -> 'il m ACTIVERA avec le bilan (activer, pas reactiver - reactiver ramene a Cerberus)', les cases 'Themis me REACTIVE' (c11a/c22a/c27a/c8a/c12a/c10a...) -> 'Themis m ACTIVE (activer session-llm-1 <moi>)', 'je la reactiverai' -> 'je l activerai'. VERIFIER AUSSI les 14 autres parcours (scan reactiver non-cerberus). METHODE : editer-parcours (barrage n3) pour chaque case, bump version parcours, fiche synchronisee (Pattern 14), valider-cartes CONFORME, normes ASCII + LF. NE PAS toucher aux tests ni au lanceur. FIN: lecon Buffy + ACTIVER JANUS (ta carte impose Activer Janus).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 23:19 | session-llm-1 | Cerberus | BILAN CONSOLIDE (Janus, mission Cerberus) : CHAINE OUTILS WEB COMPLETE - VERDICT VALIDE. NON-REGRESSION 86 OK / 0 KO (126.7s, toutes barrieres franchies, y compris la serie KO persistante). Livrables : 2 outils crees par Vulcain (rechercher-web v0.1.0 : recherche DuckDuckGo Lite + lecture page, verrou habilitation, chrono, timeout interne ; detecter-recherches-obsoletes v0.1.0 : fraicheur > 30 j), catalogue 172->174, index-tools 193->195 (+ tableau Statistiques regenere 187->195), carte atlas v0.4.6 (indices c13 rechercher-web + c12 detecter), fiche + carte janus v0.4.14 EDUQUEES (workflow serie KO, --ko/--etat-ko/--tags/--categorie/--ordre-fixe), garde-fou test-088 (recherches-web conformes + fraiches, serie e + profil outils), lanceur 0.5.8, badge README Outils 150->152 (Clio), 10 tests adaptes (005/007/024/027/031/032/051/060/062/074/075/079/081 selon round), 0 residu, bumper coherent, registre journalise. Lecons : Vulcain, Buffy x2, Morpheus x2, Clio, Janus. A NOTER : la mission reelle d Atlas (recherche web Next.js) et la mise a jour readme-dev restent a faire (etapes suivantes non bloquees). |
| 2026-08-16 23:12 | session-llm-1 | janus | REVALIDATION JANUS (3e passage, finale): Clio a corrige le badge Outils du README (150 -> 152 affichage + href), test-038 7/7 OK, normes OK, lecon ecrite. RELANCE : --relancer-ko puis suite complete (86 tests). Verdict attendu : 86 OK / 0 KO. FIN : reactiver Cerberus avec le bilan consolide.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 23:12 | session-llm-1 | Cerberus | Clio a corrige le badge Outils du README (150 -> 152, affichage + href), test-038 7/7 OK, normes OK, lecon ecrite. Relance la suite pour le verdict final. |
| 2026-08-16 23:11 | session-llm-1 | clio | MISSION CLIO: CORRIGER LE BADGE OUTILS DU README (KO test-038). CONTEXTE: Vulcain a cree 2 nouveaux outils (rechercher-web + detecter-recherches-obsoletes) -> le compte reel des outils est passe de 150 a 152. Le README affiche encore badge Outils-150 (affichage + href) -> test-038 KO (affichage=150 reel=152). A FAIRE: 1) corriger le badge en dur du header README.md (affichage + href) 150 -> 152, 2) verifier les autres badges et compteurs du README (categories Detecter/Rechercher si presentes), 3) relancer test-038 : 7/7 OK, 4) normes ASCII + LF. NE PAS toucher au readme-dev ni aux outils (domaine autre). FIN: lecon Clio + ACTIVER JANUS (la carte Clio impose Activer Janus - corrige la fin erronee initiale).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/clio/parcours/parcours-clio.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 23:08 | session-llm-1 | janus | REVALIDATION JANUS (2e passage): Morpheus a corrige les 2 derniers pins de version oublies (test-075 et test-081 : 0.5.7 -> 0.5.8, maintenant 11/11 et 10/10 verts). RELANCE : --relancer-ko puis suite complete finale (86 tests). Verdict attendu : 86 OK / 0 KO. FIN : reactiver Cerberus avec le bilan consolide.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 23:06 | session-llm-1 | janus | CONTROLE JANUS FINAL (suite chaine outils web): Morpheus a corrige les 5 tests (005/007/024/060/079), regenere le tableau Statistiques index-tools (187->195), cree le garde-fou test-088 (recherches-web, serie e + profil outils), bumpe le lanceur 0.5.7->0.5.8 (+ 7 tests pinneurs). Test-030 vert, test-063 vert, bumper coherent. RELANCE : 1) --relancer-ko (KO du dernier run : test-024), 2) --series e (serie anti-recurrence, inclut test-088), 3) suite complete finale. Verifie que les artefacts de session (test-027/031/051 KO en direct sous morpheus) passent sous TA session janus. FIN : verdict + reactiver Cerberus avec le bilan consolide (c est toi le dernier maillon).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 23:06 | session-llm-1 | Cerberus | Morpheus a corrige les 5 tests (005/007/024/060/079), regenere le tableau Statistiques index-tools (187->195), cree le garde-fou test-088 (recherches-web, serie e + profil outils), bumpe le lanceur 0.5.7->0.5.8 (+ 7 tests pinneurs). Test-030 vert, test-063 vert, bumper coherent. RELANCE : --relancer-ko (KO du dernier run : test-024) puis --series e puis suite complete finale. Verifie aussi que les artefacts de session (test-027/031/051 KO en direct sous morpheus) passent sous ta session. FIN : verdict + reactiver Cerberus. |
| 2026-08-16 22:56 | session-llm-1 | morpheus | MISSION MORPHEUS: ADAPTER LES TESTS AUX 2 NOUVEAUX OUTILS WEB (rechercher-web + detecter-recherches-obsoletes) ET AU PARCOURS ATLAS 0.4.6. CONTEXTE: Vulcain a cree les 2 outils (catalogue 172->174, index-tools 195), Buffy a branche les indices dans la carte atlas (0.4.5->0.4.6). KO detectes par Janus (barriere KO) : test-024 point 8 pinne catalogue 172 (nb=174). AUSSI A ADAPTER (pins perimes repertories) : 1) test-007 point 13 catalogue 172->174, 2) test-060 catalogue 172->174, 3) test-079 point 10 catalogue 172->174, 4) test-005 parcours-atlas v0.4.5->0.4.6 (lignes 26/49/190/255), 5) CREER le garde-fou test-088 (recherches-web conformes + fraiches : chaque recherche a un header date, sources citees, index a jour - anti-recurrence du maillon manquant web). APRES: reverdir avec l OUTIL tester-lancer-non-regression --agent janus --relancer-ko (ou la serie E), verifier normes ASCII + LF, ecrire lecon Morpheus, et REACTIVER JANUS pour la suite complete finale. FIN: seul le DERNIER maillon reactiver Cerberus.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 22:55 | session-llm-1 | janus | CONTROLE JANUS (education terminee): ta fiche janus.md et ta carte (v0.4.14, case c4) ont ete mises a jour par Buffy pour te former aux DERNIERES ameliorations de la suite. NOUVEAU WORKFLOW: 1) --etat-ko pour constater la serie KO persistante (ko-tests.json), 2) --ko reprendre (DEFAUT) lance la serie KO EN PRIORITE avec sa barriere - les tests qui passent sortent du fichier, 3) les series normales dans l ordre dynamique par taux de KO (--ordre-fixe pour forcer a,b,c,d,e), 4) suite complete en dernier. Options nouvelles: --tags, --categorie, --desactiver-categorie/--activer-categorie, --etat-categories, --relancer-ko --series X. CONTEXTE SUITE: 1 KO detecte au run precedent (test-024 catalogue 172->174) + test-007/060/079 pinent 172 + test-005 pinne atlas 0.4.5 - ces adaptations sont du domaine Morpheus. LANCE la non-regression en respectant le workflow serie KO, rapporte les KO, active Morpheus pour les adaptations tests puis reverdis, et REACTIVE Cerberus avec le verdict final.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 22:54 | session-llm-1 | buffy | MISSION BUFFY: EDUQUER JANUS SUR LES DERNIERES AMELIORATIONS DE LA SUITE DE NON-REGRESSION. CONTEXTE: demande utilisateur URGENTE - Janus lance encore la suite comme avant et n utilise pas les dernieres capacites. AUDIT PREALABLE (Janus) : la fiche janus.md section 'UTILISATION DE tester-lancer-non-regression' (lignes 184-240) couvre deja BARRIERES, --series, --profil/--fichiers, --desactiver/--activer, --relancer-ko, workflow KO, --rapport. MANQUANT : 1) --ko {nouveau,reprendre} (serie KO persistante PRIORITAIRE - lance D ABORD ko-tests.json avec sa barriere, ceux qui passent sortent du fichier), 2) --etat-ko, 3) --tags, 4) --categorie / --desactiver-categorie / --activer-categorie / --etat-categories (categories-tests.json), 5) --ordre-fixe (classement dynamique par taux de KO par defaut), 6) le workflow 'serie KO en premier puis series normales puis suite complete'. A FAIRE: 1) mettre a jour la fiche janus.md (ajouter les options manquantes au tableau + un paragraphe WORKFLOW SERIE KO : --etat-ko pour constater -> --ko reprendre (defaut) lance la serie KO prioritaire -> valider -> suite complete), 2) mettre a jour la carte parcours-janus.json (case c4 'Verifier les tests' : enrichir la commande de l indice outil tester-lancer-non-regression avec --relancer-ko/--etat-ko ou ajouter une regle qui rappelle le workflow serie KO), bump version parcours janus + fiche synchronisee (Pattern 14), 3) valider-cartes --agent janus CONFORME + navigation reelle, 4) normes ASCII + LF. NE PAS toucher aux tests ni au lanceur (domaine Morpheus/Vulcain). FIN: lecon Buffy + ACTIVER JANUS (la carte Buffy impose Activer Janus) pour qu il relance la suite avec le nouveau workflow.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 22:49 | session-llm-1 | janus | CONTROLE JANUS (suite chaine outils web): Buffy a branche les 2 outils web dans la carte atlas v0.4.6: c13 + indice rechercher-web (case sans outil avant), c12 + indice detecter-recherches-obsoletes (fraicheur avant re-cherche). Fiche atlas synchronisee (PARCOURS v0.4.6), valider-cartes CONFORME, verrou ouvert atlas, navigation c12->c13->c14->c10 OK, normes OK. Vulcain a cree les 2 outils (catalogue 174, index-tools 195, bumper coherent). A VERIFIER: 1) test-005 pinne parcours-atlas v0.4.5 -> KO attendu (adaptation Morpheus), 2) test-007 compteur catalogue 172->174, 3) test-024/060/079 compteurs outils (194->196?), 4) le garde-fou test-088 (recherches-web conformes + fraiches) doit etre CREE par Morpheus, 5) registre: 4 declarations buffy (editer-parcours, valider-cartes-decision, mettre-a-jour-versions) - guider-parcours retire (hors carte), 6) evaluer-processus: FIN_MISSION_ERRONEE corrigee (mission Buffy disait reactiver Cerberus, corrigee en Activer Janus). LANCE la non-regression, rapporte les KO, active Morpheus pour les adaptations tests puis reverdis, et REACTIVE Cerberus avec le verdict final. FIN: seul le DERNIER maillon reactiver Cerberus avec le bilan consolide.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 22:43 | session-llm-1 | buffy | MISSION BUFFY: BRANCHER LES 2 OUTILS WEB DANS LA CARTE ATLAS. Vulcain a cree rechercher-web (recherche + lecture page, verrou, chrono, registre) et detecter-recherches-obsoletes (fraicheur > 30 j), catalogue 174, index-tools 195. A FAIRE: 1) brancher l indice outil rechercher-web dans la case c13 "Executer la recherche" du parcours atlas (celle sans outil aujourd hui) + une case detect pour detecter-recherches-obsoletes (scan fraicheur, modele morpheus c8b ou case detect existante si coherente), 2) bump version parcours atlas, 3) fiche atlas synchronisee (Pattern 14 + bloc FINS REELLES si besoin), 4) valider-cartes --agent atlas CONFORME + navigation reelle, 5) normes ASCII + LF. FIN: lecon Buffy + ACTIVER JANUS (second controle, la carte Buffy impose Activer Janus - corrige la fin erronee initiale qui disait reactiver Cerberus).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 22:35 | session-llm-1 | vulcain | MISSION VULCAIN : CREER LES 2 OUTILS DE RECHERCHE WEB (demande utilisateur : souvenirs vrais et d actualite pour les agents). CONTEXTE : recherches-web/ existe (1 seule recherche badges 2026-08-07), protocole immuable protocole-recherches-web en ebauche mais AUCUN outil web reel dans le cerveau (le protocole reference researcher-web/researcher-docs qui n existent pas). Le user veut un acces web reel pour les agents + une fraicheur mecanisee des recherches (= leur memoire factuelle). OUTILS A CREER : 1) rechercher/rechercher-web/ : recherche web (requete HTTP simple via urllib vers une source fiable, ex DuckDuckGo HTML ou lecture directe d URL officielle) + lecture de page (--url). Options : <requete> ou --url <url>, --rapport <fichier>, --dry-run/--wet, --verbose, --version, --aide. Protections (triplet chrono + point_actif), ASCII strict, LF, argparse, en-tete type outil (modele rechercher-texte), doc .md, entree catalogue generateurs-commande, entree index-tools (categorie Rechercher). 2) detecter/detecter-recherches-obsoletes/ : scan recherches-web/ (statut validee), signale celles a re-verifier (age > 30 jours ou date_validite depassee), --rapport, --version. Doc + catalogue + index-tools (categorie Detecter). CONTRAINTES : ne PAS modifier le protocole immuable (porte du marbre a part), ni les cartes (Buffy), ni les tests (Morpheus). Bumper les 2 outils v0.1.0, verifier catalogue 172 -> 174 (les tests de compteurs seront adaptes par Morpheus). FIN : lecon Vulcain + activer BUFFY pour brancher les indices dans la carte Atlas.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 22:29 | session-llm-1 | Cerberus | BILAN CONSOLIDE Janus (round categories + liste blanche) : NON-REGRESSION 85 OK / 0 KO (127.8s, toutes barrieres franchies). Livrables : categories par tags (85 tests tagges, lanceur v0.5.7 --tags/--categorie, categories-tests.json, recommander-series branche carte vulcain c7b v0.4.25, garde-fou test-087), liste blanche developpeur verrou v0.2.2 (vulcain peut valider ses modifs du lanceur, mode verrou-dev, test-056 preuves 3b/3c, test-037 exception, evaluer-processus ignore verrou-dev), correctifs cascade (test-066 dynamique, 7 pins 0.5.5->0.5.7, test-087 protections+profil outils). Bumper 0 incoherent, 0 residu, lecons Morpheus x3 + Janus. Chain intacte meme round. |
| 2026-08-16 22:22 | session-llm-1 | janus | REVALIDATION FINALE : Morpheus a corrige les 2 KO consequences de test-087 (1) bloc protections standard ajoute a test-087 (test-030 reverdi 10/10), (2) test-087 ajoute au profil outils de profils-tests.json (test-063 reverdi 11/11). LANCE la suite complete 85 tests. Si 0 KO : bilan consolide a Cerberus (round categories par tags + liste blanche developpeur vulcain + correctifs cascade). Si KO : traite via le workflow (rapport -> Morpheus -> revalidation).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 22:20 | session-llm-1 | morpheus | 2 KO CONSEQUENCES DE TEST-087 (85e test ajoute ce round) a corriger : 1) TEST-030 point 2b : test-087-categories-tags n importe PAS les protections (ligne PROTECTIONS = charger_protections() absente). Ajouter le bloc standard (chargeur local charger_protections + PROTECTIONS = charger_protections(), modele test-066, import importlib.util a ajouter). test-087 n execute aucune commande : pas besoin de lancer_protege, la ligne d import suffit. 2) TEST-063 point 5 : test-087 absent des profils (profils-tests.json) - ajouter test-087 au profil "outils" (comme test-064/test-066). VERIFIER ensuite test-030 et test-063 seuls (0 KO) + test-087 (protege) puis reactiver JANUS pour la suite complete finale. Normes ASCII + LF.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 22:18 | session-llm-1 | janus | REVALIDATION apres correctif Morpheus : test-066 point 4 rendu DYNAMIQUE (lit la VERSION du lanceur, cible patch+1 - plus de pin perime) + 7 tests au pins de version PERIMES corriges (027/031/051/062/074/075/081 : 0.5.5 -> 0.5.7, la 2e cascade de ce round - lecon : grep des anciennes versions apres chaque bump). Les KO vus en session morpheus (test-027 5/6a/6b/7/8, test-031 3, test-051 4) sont des artefacts du verrou d identite : ils passent en ta session. RELANCE : 1) --relancer-ko (test-066 revalide), 2) suite complete 85 tests, 3) si 0 KO : bilan consolide a Cerberus (categories par tags + liste blanche developpeur vulcain v0.2.2 + correctifs).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 22:12 | session-llm-1 | morpheus | KO TEST-066 A CORRIGER (non-regression 84 OK / 1 KO, barriere E). POINT 4 : option --nouvelle. Le test pinne la transition PERIMEE "0.5.5 -> 0.5.6" (ecrit quand le lanceur etait en 0.5.5) alors que le lanceur est maintenant en 0.5.7 (bump categories + liste blanche). Le bumper ne detecte que les pinneurs de la version COURANTE (test-032/024), pas les transitions passees - do ou le KO invisible. CORRECTION SOUHAITEE : rendre le point 4 DYNAMIQUE - lire la VERSION courante du lanceur (regex sur tester-lancer-non-regression.py), calculer la cible patch+1, lancer --nouvelle <cible>, attendre "<courante> -> <cible>" - plus jamais de pin perime. Mettre a jour aussi le commentaire du point 4 (qui dit encore "le lanceur est deja a 0.5.5"). VERIFIER ensuite test-066 seul (0 KO) puis reactiver JANUS pour la revalidation --relancer-ko puis suite complete. Normes ASCII + LF. Ne touche qu au test (exclusivite morpheus).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 22:10 | session-llm-1 | janus | NON-REGRESSION FINALE round categories + liste blanche developpeur. Morpheus a tague les 85 tests + cree le garde-fou test-087 (ajoute serie e) ; Vulcain a cree la mecanique tags (lanceur v0.5.7 : --tags/--categorie, categories-tests.json, recommander-series). AUTORISATION UTILISATEUR : liste blanche developpeur dans proteger-verrou-habilitation v0.2.2 - vulcain peut VALIDER ses modifications du lanceur (mode verrou-dev journalise, ignore par evaluer-processus, exception documentee test-037 ; preuves test-056 3b/3c). KO pre-existant corrige : recommander-series branche dans la carte vulcain c7b (parcours 0.4.25, fiche synchronisee, test-035 reverdi). POINTS D ATTENTION : test-032 passe en session janus (artefact verrou sinon) ; catalogue 172 (test-007/024/060/079). Lance la suite complete avec les barrieres, traite les KO via --relancer-ko, puis bilan consolide a Cerberus.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 21:52 | session-llm-1 | morpheus | TAGGER LES 84 TESTS DE LA NON-REGRESSION (demande utilisateur). CONTEXTE: Vulcain a cree la mecanique: le lanceur v0.5.6 lit le bloc "Tags:" de la docstring de chaque test (regex "Tags: ..."), filtre --tags/--categorie, categories-tests.json definit 7 categories: securite (tags: marbre, verrou, habilitation, blocage, anti-contournement, protection), conventions (nommage, ascii, lf, template, fins-de-ligne, budget), agents (parcours, cerberus, janus, morpheus, buffy, vulcain, hygie, themis, clio, argus, garde-fou-agent), outils (combos, generateurs, outil, catalogue, moteur, ligne), registre-traces (registre, ko-tests, traces, processus, usage), performance (chrono, pool, workers, perf, duree, reference-temps), anti-recurrence (anti-recurrence, garde-fou, preuve-negative). TRAVAIL: 1) AJOUTER le bloc "Tags: <tags>" dans la docstring de CHAQUE test-0XX (84 tests) - 1 a 4 tags pertinents par test (ex: test-057 marbre -> Tags: securite, marbre, anti-contournement ; test-031 chrono -> Tags: performance, chrono ; test-029 template -> Tags: conventions, template ; test-013 cerberus -> Tags: agents, parcours, cerberus). Respecter la TAXONOMIE de categories-tests.json (les tags doivent correspondre). 2) CREER le garde-fou test-087-categories-tags: chaque test-0XX a un bloc Tags: valide (au moins 1 tag), les tags sont dans la taxonomie de categories-tests.json, preuve negative (un test sans Tags: detecte), verifie aussi que --etat-categories du lanceur fonctionne. 3) Verifier: recommander-series affiche les tags, le lanceur --tags fonctionne (test reel par Morpheus sur un tag ex --tags securite avec --agent morpheus n est pas autorise -> tester via import ou demander a Janus). 4) Reverdir la non-regression. CONTRAINTES: ASCII strict + LF, bloc Tags: INSERE dans la docstring (apres la description, avant la fin), jamais dans les commentaires, preuve negative obligatoire. FIN: lecon Morpheus + activer JANUS pour la validation finale.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 21:47 | session-llm-1 | vulcain | CREER LA MECANIQUE DE CATEGORISATION DES TESTS PAR TAGS (demande utilisateur). CONTEXTE: le lanceur a 5 series fixes (SERIES a-e) + on/off par test (config-tests.json) + registre-tests.jsonl (date, serie, test, verdict, duree). L utilisateur veut: des tags dans chaque test permettant de categoriser, des categories (securite, conventions, agents, outils, registre-traces, performance, par-agent) contenant des series, pouvoir desactiver un test/une serie/une categorie, et que le RATING/PERFORMANCE aident a reorganiser les series. DECISION STRUCTURE: bloc "Tags:" dans la docstring de chaque test (ex: Tags: securite, conventions, anti-recurrence) - source unique lisible par le lanceur. TRAVAIL: 1) ETENDRE tester-lancer-non-regression.py: - parser les Tags: de la docstring de chaque test (regex sur la docstring) ; - nouvelle option --tags <t1,t2> : ne lancer que les tests portant CES tags (combinaison OR) ; - nouvelle option --categorie <nom> : alias pratique = lancer le groupe de tags predefini (fichier categories-tests.json: nom -> liste de tags) ; - extension de config-tests.json: "desactivees_categories" (persistant, herite) + --desactiver-categorie <nom> / --activer-categorie <nom> / --etat-categories ; - affichage au lancement: "Categorie X: N tests (tags ...) - serie A: ...". 2) CREER l outil recommander-series (categorie analyser/ ou tester/): croise registre-tests.jsonl (duree par test) + tags des docstrings + profils-rating.json -> propose un classement des tests par categorie et par duree (les lents ensembles, les rapides ensembles) avec --rapport. CONTRAINTES: ASCII strict, LF, argparse, 100% stdlib, modele detecter-usage-scripts-temporaires (fonction charger_parcours/racine AGENTS.md). VERIFIER: le lanceur tourne toujours en mode defaut (tous les tests), --tags fonctionne (test reel sur un tag), --desactiver-categorie persiste, categories-tests.json valide. APRES: doc .md + catalogue + index-tools. FIN: lecon Vulcain + activer MORPHEUS pour tagger les 84 tests (ajouter le bloc Tags: dans chaque docstring) + garde-fou test-087 (chaque test a un bloc Tags: + tags valides) + reverdir non-regression.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 21:37 | session-llm-1 | Cerberus | BILAN CONSOLIDE MIGRATION RELECTURE OBLIGATOIRE: 15 parcours migres (c0 action RELIRE + c0b confirmation), valider-cartes 15/15 CONFORME, NON-REGRESSION 84 OK / 0 KO (130.1s), marbre re-empreinte (cerberus.c0/c0b, porte ouverte utilisateur) + lock 14 cartes resynchronise, outils alignes (valider-cartes v0.4.2, generateurs-carte v0.3.1, activer-agent-principal v0.5.9, migrer-cases-relecture v0.1.0), catalogue 171, badge README 150, tests adaptes (004 16/16, 005 28/28, 006 19/19, 007 15/15, 011 19/19, 013 22/22, 016 20/20, 017 41/41, 024 16/16, 028 8/8, 035 10/10, 057 24/24, 060 12/12, 072 10/10, 079 15/15), bumper 0 incoherent, 0 residu, lecons Vulcain/Buffy/Morpheus/Clio/Janus ecrites |
| 2026-08-16 21:28 | session-llm-1 | janus | relance finale non-regression apres badge 150 (Clio)

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 21:28 | session-llm-1 | Cerberus | badge README 150 + readme-dev Migrer 2, test-038 7/7, combos-analyse-projet README A JOUR |
| 2026-08-16 21:27 | session-llm-1 | clio | MISE A JOUR BADGE README : le nouveau outil migrer-cases-relecture (cree par Vulcain) porte le compte reel d outils a 150. test-038 KO: badge affiche 149, compte reel 150. CORRIGER: le badge Outils-N du header README.md (2 occurrences: affichage + href) de 149 vers 150. VERIFIER: test-038 7/7, combos-analyse-projet verdict README A JOUR. CONTRAINTES: ASCII strict + LF. FIN: lecon Clio + reactiver JANUS pour la relance finale.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/clio/parcours/parcours-clio.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 21:18 | session-llm-1 | janus | validation finale apres migration relecture obligatoire: 15 parcours migres (c0 action RELIRE + c0b confirmation), valider-cartes v0.4.2 15/15 CONFORME, generateurs-carte v0.3.1, activer-agent-principal v0.5.9, catalogue 171, tests adaptes (072 10/10, 013 22/22, 016 20/20, 005 28/28, 011 19/19, 007 15/15, 060 12/12, 028 8/8), bumper 0 incoherent. Lancer la non-regression complete avec --agent janus et rendre le verdict.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 21:12 | session-llm-1 | morpheus | ADAPTER LES TESTS APRES LA MIGRATION RELECTURE OBLIGATOIRE (Vulcain + Buffy). CONTEXTE: les 15 parcours ont change de structure : c0 = action RELIRE OBLIGATOIRE (corrections puis fiche) -> c0b, c0b = question confirmation (OUI -> c0c, NON -> c0), c0c conserve. Versions bumpees (cerberus 0.5.1, buffy 0.4.10, etc). valider-cartes v0.4.2 valide la NOUVELLE structure (15/15 CONFORME). TRAVAIL: 1) ADAPTER test-072-c0-c0b-relecture : les invariants changent - c0 doit etre de type action avec titre RELIRE + 2 outils lire-fichier + suivant c0b, c0b doit etre de type question avec branches OUI->c0c et NON->c0 (plus de branches OUI->c0c/INCERTAIN/NON->c0b ni de question EN MEMOIRE). Garder la preuve negative. 2) CREER le garde-fou test-086-relecture-obligatoire (ou adapter test-072 en garde-fou complet) qui verifie la structure cible sur les 15 parcours avec preuve negative. 3) ADAPTER test-013 (cerberus v0.5.0 -> 0.5.1) et test-016 (buffy v0.4.9 -> 0.4.10 si reference) ainsi que tout test qui verifie la structure c0 question (verifier test-012 guider-parcours, test-011 generateurs-carte, test-018, test-033). 4) Verifier les tests des outils modifies : test-005 (catalogue 171), test-028 (versions spec), test-029/030 (normes), test-034 (cerberus sans outils tests). 5) Reverdir la non-regression complete avec l OUTIL tester-lancer-non-regression --agent morpheus. CONTRAINTES: ASCII strict + LF, preuve negative obligatoire pour le garde-fou, jamais de script tiers. FIN: lecon Morpheus + activer JANUS pour la validation finale.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 21:12 | session-llm-1 | buffy | SYNCHRONISER LES 15 FICHES AGENTS : la migration relecture obligatoire (Vulcain) a bumpe les versions des 15 parcours, mais les fiches portent encore l ancienne version -> valider-cartes --tous = 15 NON CONFORME (incoherence fiche/parcours). CONTEXTE: le Pattern 4 de valider-cartes a evolue (c0 = action RELIRE OBLIGATOIRE + c0b = question confirmation) - la carte est conforme sur la structure, seul le NUMERO DE VERSION differe. MISSION: pour chaque fiche cerveau-projet/agents/<agent>/<agent>.md, mettre a jour le bloc PARCOURS (Pattern 14) avec la nouvelle version du parcours. VERSIONS ATTENDUES: argus 0.1.10, athena 0.3.3, atlas 0.4.5, buffy 0.4.10, cerberus 0.5.1, clio 0.5.10, gardien 0.1.3, hermes 0.1.3, hygie 0.1.6, janus 0.4.13, minerve 0.3.4, morpheus 0.4.11, promethee 0.3.4, themis 0.4.6, vulcain 0.4.23. VERIFIER: valider-cartes --tous = 15 CONFORME. CONTRAINTES: editer via editer-fichier-agents (jamais d ecriture directe), ASCII strict + LF, normes 0/0. FIN: lecon Buffy + activer MORPHEUS (adapter test-072 aux nouveaux invariants + creer garde-fou test-086 + adapter tests version parcours 013/016 + reverdir non-regression).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 21:08 | session-llm-1 | vulcain | CREER OUTIL MIGRER-CASES-RELECTURE : la relecture de la fiche doit devenir OBLIGATOIRE + confirmation. CONTEXTE: les 15 parcours ont c0 question (OUI->c0c contourne la lecture) + c0b action RELIRE->c0c (sans confirmation). L utilisateur a valide la structure cible : c0 = action RELIRE OBLIGATOIRE (corrections puis fiche) -> c0b ; c0b = question confirmation As-tu LU et compris ? OUI->c0c, NON->c0 ; c0c = CONTEXTE inchange (suivant conserve). OUTIL A CREER: cerveau-projet/agents/tools/migrer/migrer-cases-relecture/migrer-cases-relecture.py (+ .md doc, + entree catalogue generateurs-commande, + entree index-tools.md categorie Migrer). FONCTIONNALITES: --agent <nom> (1 parcours), plusieurs agents, --tous (15 parcours), --dry-run (affiche sans ecrire), --rapport <fichier>, --verbose, --version. Pour chaque parcours : transformer c0 (question->action, titre RELIRE OBLIGATOIRE : corrections puis fiche, indices = 2 outils lire-fichier vers corrections.md puis <agent>.md, suivant=c0b), c0b (action->question, question confirmation honnete, branches OUI->c0c et NON->c0, indices regle), c0c CONSERVE tel quel (suivant c0d ou c1 inchange). Bumper la version de chaque parcours modifie (0.0.x -> 0.0.x+1 sur le mineur). CONTRAINTES: ASCII strict, LF, argparse, modele des outils existants (en-tete usage, detection racine via AGENTS.md), ecriture JSON avec ensure_ascii=False + newline LF, jamais de script tiers. TESTS REEls: --dry-run sur buffy (affiche les 3 transformations sans ecrire), --tous (15 parcours migres, versions bumpees), re-verification structure cible sur les 15 (script de controle), valider-cartes-decision --tous (15 CONFORME), detecter-cablages-manquants --tous (0 probleme). APRES: doc .md + catalogue + index-tools. FIN: lecon Vulcain + activer MORPHEUS pour adapter test-072 (nouveaux invariants) + creer garde-fou test-086 (structure relecture obligatoire cible : c0 action RELIRE + c0b question confirmation OUI/NON + preuve negative) + reverdir non-regression.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 21:04 | session-llm-1 | Cerberus | bilan consolide maj readmes: 84 OK / 0 KO (120.9s), readme-dev resynchronise (149 outils), ligne Argus corrigee dans README public, lecons Clio+Janus ecrites |
| 2026-08-16 20:56 | session-llm-1 | janus | relance finale apres maj readmes Clio

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 20:48 | session-llm-1 | clio | MISSION CLIO (demande utilisateur : une mise a jour des readmes s impose - RAISON : ajout des outils processus-residuels, combo-nettoyage-hygie v0.1.1, generateurs-commande v0.2.6) : METTRE A JOUR LES 2 READMES (public README.md + technique cerveau-projet/readme-dev.md). SEUL CLIO est habilite (regle immuable) - Cerberus a derive en faisant l analyse lui-meme, il s en excuse et passe la main.

ECARTS CONSTATES (a verifier et corriger par TOI, source de verite index-tools.md + catalogue-commandes.json) :
1. README.md public : badge Outils-149 -> verifier le compte reel (catalogue 170 commandes ? index-tools total 187 ?). La ligne Argus en bas de la table des agents a un FORMAT CASSE (ligne vide parasite + colonne "Selon sa carte de decision" hors tableau).
2. readme-dev.md : compteurs PERIMES - ligne 28 "144 outils dans 36 categories" (reel : total index-tools 187), ligne 57 "134 outils" (incoherent), ligne 218 idem. Tableau des categories a resynchroniser : Analyser 5->6, Corriger 6->7, Detecter 15->16, Nettoyer 3->4 (+ Nettoyer doit citer nettoyer-processus-residuels), Total 144->187. Verifier chaque categorie vs index-tools.md.
3. Verifier que les 2 readmes mentionnent les nouveaux outils (detecter-processus-residuels, nettoyer-processus-residuels) et le combo complet, sans jargon technique dans le README public.

PROTOCOLE : combos-maj-readme (ou massive) selon l ampleur, aligner_badge_header (badge Outils + href), verifier combos-analyse-projet verdict README A JOUR, normes ASCII strict + LF, registre usage. FIN : lecon Clio + activer JANUS (controle croise) qui reactive Cerberus.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/clio/parcours/parcours-clio.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 20:45 | session-llm-1 | Cerberus | BILAN CONSOLIDE (Janus, nettoyage Hygie) : le residu DOUBLE a ete elimine - le dossier docs-dev-cerveau-projet/ duplique A LA RACINE + son rapport egare (rapport-diagnostic-convention-scripts-temporaires-2026-08-16.md) ont ete supprimes par Hygie (snapshot 4642 fichiers, supprimer-dossier --agent hygie, rapport ecrit, lecon 0 non-ASCII, registre 3 declarations). Le VRAI dossier cerveau-projet/docs-dev-cerveau-projet/ est INTACT (amelioration-philosophie.md, analyse-externe.md, spec-refonte-cartes-decision.001.01.ebauche.md). Detection finale : PROPRE (0 residu). Fin de mission. |
| 2026-08-16 20:45 | session-llm-1 | janus | VERIFICATION FINALE (suite nettoyage Hygie) : le dossier duplique docs-dev-cerveau-projet/ a la racine a ete supprime (rapport egare inclus), le vrai dossier cerveau-projet/docs-dev-cerveau-projet/ est intact (3 specs), detection PROPRE, rapport + lecon Hygie ecrits, registre 3 declarations. Verifier rapidement : detecter-residus --tous PROPRE, 0 residu, puis reactiver CERBERUS avec le bilan.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 20:44 | session-llm-1 | hygie | MISSION HYGIE : NETTOYER LE DOSSIER DUPLIQUE A LA RACINE (constat utilisateur + Cerberus).

RESIDU (2 elements) : le dossier docs-dev-cerveau-projet/ A LA RACINE du projet + son fichier rapport-diagnostic-convention-scripts-temporaires-2026-08-16.md (RAPPORT_EGARE). Ce dossier est un DOUBLON du vrai dossier cerveau-projet/docs-dev-cerveau-projet/ (qui contient amelioration-philosophie.md, analyse-externe.md, spec-refonte-cartes-decision.001.01.ebauche.md - a CONSERVER, ne pas y toucher).

SUPPRIMER (seul habilite, avec snapshot) : le dossier complet docs-dev-cerveau-projet/ a la racine (rm -rf du dossier, il ne contient QUE le rapport residu - verifie avant).

PROTOCOLE OBLIGATOIRE (ta carte) : 1) snapshot-nettoyage creer (preuve), 2) detecter-residus avant, 3) supprimer-dossier, 4) detecter-residus apres (doit etre PROPRE), 5) rapport dans hygie/rapports/ + rotation snapshots, 6) lecon dans corrections.md, 7) reactiver Janus.

CONTRAINTES : ne PAS toucher a cerveau-projet/docs-dev-cerveau-projet/ (le vrai dossier), ASCII strict, LF, registre usage, 0 residu final. FIN : lecon Hygie + reactiver JANUS (verification finale rapide).

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/hygie/parcours/parcours-hygie.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 20:22 | session-llm-1 | Cerberus | BILAN CONSOLIDE (Janus, mission combo-nettoyage-hygie) : NON-REGRESSION 84 OK / 0 KO (119.5s), toutes barrieres franchies. Livrable : combo-nettoyage-hygie v0.1.1 (detection FICHIERS detecter-residus + PROCESSUS detecter-processus-residuels + suppression/terminaison par Hygie), generateurs-commande v0.2.6 (CORRECTION booleens des combos : composer_commande accepte True/False - flag du modele gouverne), carte hygie v0.1.5 (c4 + detecter-processus-residuels), test-005 adapte (0.2.6), test-045 etendu (chariot processus), spec generateurs alignee 0.2.6, registre assaini (declaration fautive janus retiree). A NOTER : 1 VRAI residu a nettoyer par Hygie (docs-dev-cerveau-projet/rapport-diagnostic-convention-scripts-temporaires-2026-08-16.md, RAPPORT_EGARE). Lecon Janus enregistree. Fin de mission. |
| 2026-08-16 20:16 | session-llm-1 | janus | MISSION JANUS (suite mission combo-nettoyage-hygie) : LANCER LA NON-REGRESSION COMPLETE (84 tests) --agent janus. Contexte des changements : combo-nettoyage-hygie v0.1.1 (detection fichiers + processus), generateurs-commande v0.2.6 (booleens), carte hygie v0.1.5 (c4 + detecter-processus-residuels), test-005 adapte (0.2.6), test-045 etendu (chariot processus). Verifier : 84 OK / 0 KO, ko-tests vide, registre, 0 residu. NOTE : un VRAI residu existe (docs-dev-cerveau-projet/rapport-diagnostic-convention-scripts-temporaires-2026-08-16.md) - detecter-residus le signale mais ce n est PAS un KO de la suite (le signaler au bilan). FIN : lecon + reactiver Cerberus avec le bilan consolide.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 20:14 | session-llm-1 | morpheus | MISSION MORPHEUS (suite mission combo-nettoyage-hygie) : 
1. ADAPTER test-005-generateurs-commande : version generateurs-commande 0.2.5 -> 0.2.6 (le generateur a ete corrige pour les booleens des combos, bump Vulcain). Verifier le test complet.
2. VERIFIER test-045-hygie-garde-fou : le chariot de Hygie doit inclure detecter-processus-residuels + combo-nettoyage-hygie v0.1.1 (verifier si le test reference les outils ou le chariot - etendre si besoin : ajouter detecter-processus-residuels et nettoyer-processus-residuels au chariot verifie).
3. Verifier que le combo-nettoyage-hygie v0.1.1 est valide (JSON + moteur).
Normes ASCII/LF sur tous les fichiers modifies. FIN : lecon Morpheus + activer JANUS (non-regression complete).

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 20:14 | session-llm-1 | buffy | MISSION BUFFY (suite mission Vulcain combo-nettoyage-hygie) : AJOUTER l indice outil detecter-processus-residuels dans la case c4 Detection compartimentee de la carte HYGIE via editer-parcours (commande : python3 cerveau-projet/agents/tools/detecter/detecter-processus-residuels/detecter-processus-residuels.py --detail). La case c4 a deja detecter-residus + combos-analyse-projet. Bump parcours (0.1.4 -> 0.1.5) + fiche hygie.md (Pattern 14). Verifier : valider-cartes-decision --agent hygie CONFORME, verrou --audit hygie detecter-processus-residuels OK. FIN : lecon Buffy + activer MORPHEUS (adapter test-005 0.2.5->0.2.6, verifier test-045 chariot inclut detecter-processus-residuels) puis JANUS.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 20:10 | session-llm-1 | vulcain | MISSION VULCAIN (demande utilisateur, suite processus-residuels) : ENRICHIR le combo-nettoyage-hygie pour combiner la detection FICHIERS (detecter-residus) ET PROCESSUS (detecter-processus-residuels) dans la mission de nettoyage complete de Hygie.

ETAT ACTUEL : cerveau-projet/agents/tools/combos/combo-nettoyage-hygie/definition-combo.json v0.1.0 - 7 etapes : c1 generateur snapshot-nettoyage -> c2 outil snapshot -> c3 generateur detecter-residus -> c4 outil detecter-residus -> c5 controle "des residus detectes ?" -> c6 fin "Residus a supprimer" / c7 fin "Workspace propre". Le combo NE scanne PAS les processus.

A FAIRE (modele combo-creer-agent pour les etapes generateur/outil) :
1. Ajouter apres c4 (execution detecter-residus) : c4b generateur detecter-processus-residuels (catalogue detecter-processus-residuels, entrees detail=true, sortie cmd3) -> c4c outil {cmd3} (execution, sortie resultat_processus).
2. Etendre le controle c5 : la question doit couvrir fichiers ET processus ("La detection a-t-elle trouve des residus (fichiers temp, rapports egare, caches, OU processus orphelins python/node/bash) ?").
3. Adapter la fin c6 : mentionner que les processus residuels sont termines via nettoyer-processus-residuels (exclusif hygie, --agent hygie --tous --force) et les fichiers via supprimer-fichier/dossier, puis re-verification detecter-residus + detecter-processus-residuels.
4. Bump combo v0.1.0 -> v0.1.1 (+ ligne dans le .md doc si present).
5. VERIFIER le combo : python3 cerveau-projet/agents/tools/combos/combos-moteur/combos-moteur.py --combo combo-nettoyage-hygie --reponses c5=OUI doit derouler les etapes sans erreur (dry-run ou execution).

CONTRAINTES : ASCII strict, LF, JSON valide, ne PAS toucher aux tests (Morpheus apres). FIN : lecon Vulcain + activer BUFFY (ajouter l indice outil detecter-processus-residuels dans la case c4 Detection compartimentee de la carte hygie via editer-parcours + bump parcours) puis MORPHEUS (verifier/etendre test-045 hygie-garde-fou si le chariot doit inclure les processus) puis JANUS (non-regression).

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 20:08 | session-llm-1 | Cerberus | BILAN CONSOLIDE (Janus, mission processus-residuels) : NON-REGRESSION 84 OK / 0 KO (118.5s), toutes barrieres franchies. Livrable : 2 outils processus-residuels v0.1.1 (detecter : PROJET/orphelin, liste blanche freebuff/unsloth protegee ; nettoyer : exclusif hygie via verrou, dry-run, --kill/--tous), carte hygie v0.1.4 (c2 nettoyer + c10 detecter), garde-fou test-085 8/8 (preuve reelle orphelin + verrou + 0 residu), catalogue 170 (trie), index-tools 187, badge README 149 (Clio), test-007/024/060/079 adaptes, registre +3 declarations, ko-tests vide, 0 residu. Lecon Janus enregistree. Fin de mission. |
| 2026-08-16 20:01 | session-llm-1 | janus | RELANCE FINALE (suite mission processus-residuels) : Clio a corrige le badge README (149), test-038 vert 7/7. ko-tests.json contient encore test-038 - le vider puis lancer la non-regression complete --agent janus. Verifier 84/84 OK, registre propre, ko-tests vide, 0 residu. FIN : lecon + reactiver Cerberus avec le bilan consolide.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 20:01 | session-llm-1 | clio | MISSION CLIO (constat Janus, suite mission processus-residuels) : le badge Outils du header README est PERIME : affiche 147, le compte reel est 149 (2 nouveaux outils ajoutes : detecter-processus-residuels + nettoyer-processus-residuels). Le test-038-badge-readme-synchronise verifie : badge affiche == compte reel (149) ET href == 149. CORRIGER : les 2 occurrences de Outils-147 (badge image + lien href) dans README.md ligne 9 -> 149. Verifier : test-038 vert, normes ASCII/LF, registre usage. FIN : lecon Clio + reactiver JANUS (relance finale non-regression).

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/clio/parcours/parcours-clio.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 19:54 | session-llm-1 | janus | RELANCE FINALE (suite mission processus-residuels) : les corrections Morpheus sont faites (test-060 12/12, test-079 15/15, ko-tests vide). Lancer la non-regression complete --agent janus et verifier 84/84 OK, puis registre propre, ko-tests vide, 0 residu. FIN : lecon + reactiver Cerberus avec le bilan consolide.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 19:54 | session-llm-1 | Cerberus | suite mission processus-residuels - corrections Morpheus faites (test-060/079 verts, ko-tests vide) - relance finale |
| 2026-08-16 19:53 | session-llm-1 | morpheus | MISSION MORPHEUS (constat Janus) : 2 tests ont le compteur catalogue PERIME (168) apres l ajout des 2 outils processus-residuels par Vulcain. Corriger :
1. test-060-outils-analyse ligne 237 : len(noms) == 168 -> 170 (+ ajouter les 2 nouveaux noms aux verifications si le test en liste)
2. test-079-noms-maj ligne 231 : idem 168 -> 170
Le catalogue reel est a 170 (trie). L index-tools Total est deja passe a 187 (Janus). Puis reverdir : lancer les 2 tests (doivent etre OK), verifier normes ASCII/LF, vider ko-tests.json (les 3 entrees residuelles : test-060, test-079, test-085 - test-085 est VERT 8/8). FIN : lecon + reactiver JANUS pour la relance finale.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 19:49 | session-llm-1 | janus | MISSION JANUS (suite mission processus-residuels) : LANCER LA NON-REGRESSION COMPLETE (84 tests, test-085 inclus en serie A) et valider l ensemble : 2 outils processus-residuels (detecter + nettoyer), carte hygie v0.1.4 (c2/c10 + fiche), verrou exclusif hygie, test-085 vert, test-007 adapte (170), catalogue trie, index-tools. Verifier aussi : registre usage propre (declarer les outils utilises si besoin via enregistrer-usage-outil), ko-tests vide, 0 residu. FIN : lecon Janus + reactiver CERBERUS avec le bilan consolide.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 19:46 | session-llm-1 | morpheus | MISSION MORPHEUS (suite mission processus-residuels) : CREER LE GARDE-FOU test-085-processus-residuels qui verifie :
1. DETECTION : lancer detecter-processus-residuels (etat PROPRE normalement), puis lancer un vrai processus residuel temporaire (python sleep depuis un dossier tmp-morpheus/) et verifier qu il est DETECTE (justification PROJET), puis le tuer et verifier PROPRE.
2. VERROU : proteger-verrou-habilitation --audit --agent hygie --outil nettoyer-processus-residuels = OK, --agent buffy = BLOQUE.
3. LISTE BLANCHE : l outil ne signale jamais freebuff/unsloth (verifier leur absence de la sortie).
4. PREUVE NEGATIVE : injecter un processus residuel ET verifier qu il est detecte (puis le nettoyer en fin de test - 0 residu, 0 fichier temp laisse).
Structure : modele test-059 (protections importees : global NB_POINTS/NB_OK/NB_KO, point_actif/chrono_etape/bilan_chrono, fin OK/KO). Normes ASCII strict + LF. Nettoyer TOUTES ses preuves en fin de test (anti-residu). Ensuite : ajouter test-085 au lanceur (serie + profil) et reverdir test-007 si le compteur catalogue 170 change quelque chose. FIN : lecon Morpheus + activer JANUS (non-regression complete).

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 19:45 | session-llm-1 | buffy | MISSION BUFFY (suite mission Vulcain processus-residuels) : AJOUTER les 2 nouveaux outils aux indices outil de la carte HYGIE via editer-parcours : detecter-processus-residuels (detection, peut etre aussi dans d autres cartes) et nettoyer-processus-residuels (EXCLUSIF hygie - le verrou bloque les autres). Verifier ensuite : valider-cartes-decision --agent hygie CONFORME, et la preuve verrou : proteger-verrou-habilitation --audit --agent hygie --outil nettoyer-processus-residuels doit PASSER (rc 0) et --agent buffy --outil nettoyer-processus-residuels doit BLOQUER. Bump version parcours hygie + fiche (Pattern 14). FIN : lecon Buffy + activer MORPHEUS (garde-fou test-085).

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 19:39 | session-llm-1 | vulcain | MISSION VULCAIN : CREER LES 2 OUTILS PROCESSUS-RESIDUELS (demande utilisateur, decision : 2 outils separes, kill exclusif Hygie)

CONTEXTE : les scripts temporaires et tests laissent parfois des processus orphelins actifs (python/node/bash) qui ne meurent pas. Diagnostic : sur Windows, ps aux ne montre que les bash ; les vrais residuels sont visibles via tasklist/Get-CimInstance (python.exe/node.exe). Processus legitimes a NE JAMAIS toucher : freebuff (node.exe, le client), unsloth (python.exe studio).

OUTILS A CREER (modele detecter-residus pour le 1er, verrou-habilitation pour le 2e) :

1. DETECTEUR : cerveau-projet/agents/tools/detecter/detecter-processus-residuels/detecter-processus-residuels.py (+ .md doc)
   - Detection (dry-run par defaut, jamais destructif) : processus python/node/bash dont la COMMANDE reference le projet (Z:/analyste-in-console, /z/analyste-in-console, tmp-*, .zz-*, cerveau-projet/) OU processus ORPHELINS (parent mort)
   - LISTE BLANCHE protegee : freebuff, unsloth (jamais signales, jamais tuables)
   - Compatibilite Windows (win32 : Get-CimInstance via powershell ou tasklist) + Linux/macOS (ps)
   - Sortie : PID + nom + commande + justification (PROJET/ORPHELIN) + compteur + verdict (0 = AUCUN RESIDUEL, sinon RESIDUELS DETECTES)
   - Options : --detail, --rapport <fichier>, --verbose, --version, --aide

2. NETTOYEUR : cerveau-projet/agents/tools/nettoyer/nettoyer-processus-residuels/nettoyer-processus-residuels.py (+ .md doc)
   - EXCLUSIF HYGIE : appelle proteger-verrou-habilitation --agent <nom> --outil nettoyer-processus-residuels AVANT toute action (bloque les autres agents)
   - Dry-run par defaut (liste ce qui serait tue) ; --kill <pid,...> pour cibler ; --tous pour tous les detectes ; jamais freebuff/unsloth
   - Verifie que le PID existe encore avant de tuer ; compte les reussites/echecs ; rapport
   - Options : --agent <nom> (obligatoire, verrou), --kill, --tous, --force (confirme sans relance), --verbose, --version, --aide

CONTRAINTES : ASCII strict (aucun accent), LF, argparse, commentaires d en-tete avec usage, detection racine projet via AGENTS.md, pas de script tiers, modele detecter-residus (en-tete identite).

APRES : ajouter les 2 entrees au catalogue generateurs-commande (168->170) + index-tools.md (categorie Detecter + nouvelle categorie Nettoyer si absente). Verifier test-007 (compteur catalogue a adapter par Morpheus apres). FIN : lecon Vulcain + activer BUFFY (ajouter nettoyer-processus-residuels + detecter-processus-residuels aux indices outil de la carte hygie via editer-parcours) puis MORPHEUS (garde-fou test-085 : detection + blocage kill hors hygie, preuve negative) puis JANUS (non-regression).

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 19:22 | session-llm-1 | Cerberus | BILAN CONSOLIDE (Janus, audit --ajouter) : VERDICT VALIDE - NON-REGRESSION 83 OK / 0 KO (113.5s, conforme reference +1%). L audit Argus est confirme OBLIGATOIRE pour les NOUVELLES zones du marbre (mode --ajouter) : la porte v0.1.3 le couvrait deja (zone_audit construit depuis --fichier), test-084 etendu a 11 points avec 3 preuves - 5b ajout zone REGLE = audit Argus lance (RELECTURE + audit Argus PROPRE), 5b2 ajout zone NON-regle = pas d audit, 5c nettoyage zones test du marbre.json (0 residuelle). test-057 24/24. Marbre 8 zones intact, registre propre, ko-tests vide, 0 residu. Toute nouvelle regle immuable (zone existante OU nouvelle) passe desormais la relecture Argus avant gravure. |
| 2026-08-16 19:19 | session-llm-1 | janus | REPRISE JANUS : test-084 etendu a 11 points (audit Argus OBLIGATOIRE pour le mode --ajouter : zone regle = audit lance, zone non-regle = pas d audit, nettoyage marbre verifie). test-057 24/24. Lancer la non-regression complete (mode barriere) et rendre le verdict final a Cerberus.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 19:19 | session-llm-1 | morpheus | MISSION MORPHEUS : ETENDRE test-084 avec la preuve que l audit Argus est OBLIGATOIRE pour le mode --ajouter (nouvelles zones) du marbre. CONTEXTE : la porte proteger-modifier-marbre v0.1.3 couvre deja --ajouter (le bloc relecture construit zone_audit via elif args.ajouter and args.fichier, puis est_zone_regles verifie regles-immuables/) - preuve manuelle faite : --ajouter zone REGLE -> audit lance (RELECTURE affichee), --ajouter zone NON-regle -> pas d audit. A FAIRE dans test-084-relecture-avant-gravure : ajouter 2 points : 1) PREUVE AJOUT REGLE : lancer la porte en mode --ajouter avec un fichier de REGLES (ex regles-general-global.md) + --autorisation UTILISATEUR -> la sortie doit contenir 'RELECTURE' (audit lance) ; 2) PREUVE AJOUT NON-REGLE : --ajouter avec un fichier hors regles-immuables/ (ex buffy/buffy.md) -> la sortie NE doit PAS contenir 'RELECTURE' (pas d audit pour les zones non-regles) ; 3) NETTOYAGE : supprimer les zones ajoutees du marbre.json en fin de test (restauration, comme le point 4b). IMPORTANT : le test ne doit JAMAIS laisser les zones test dans marbre.json (les supprimer dans un finally ou apres verification). Normes ASCII + LF. FIN : lecon Morpheus + reactiver Janus pour la non-regression.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 18:56 | session-llm-1 | Cerberus | BILAN CONSOLIDE (Janus, relecture avant gravure) : VERDICT VALIDE - NON-REGRESSION 83 OK / 0 KO (112.8s, base mise a jour). La relecture obligatoire avant toute nouvelle regle immuable est GRAVEE et MECANISEE : 1) VULCAIN : porte du marbre proteger-modifier-marbre v0.1.3 - toute zone regles-immuables/ lance automatiquement l audit Argus (detecter-contradictions --regles) AVANT d accepter l autorisation ; non PROPRE = BLOQUE (rc=1) meme avec --autorisation ; champ relecture journalise dans marbre-log.jsonl. 2) BUFFY : protocole-securite-marbre v0.1.1 (etape 4 RELECTURE OBLIGATOIRE + regle : toute nouvelle regle immuable majeure DOIT entrer au marbre apres relecture Argus PROPRE). 3) MORPHEUS : test-057 adapte (0.1.3, 24/24) + garde-fou test-084 (8/8) avec preuve negative (doublon de titre IMMUABLE injecte -> Argus 1 CONTRADICTION -> porte BLOQUE malgre autorisation, fichier restaure). Registre propre, ko-tests vide, 0 residu. Desormais, graver une regle contradictoire est IMPOSSIBLE. |
| 2026-08-16 18:54 | session-llm-1 | janus | REPRISE JANUS : relecture obligatoire avant gravure mecanisee et validee - porte marbre v0.1.3 (audit Argus PROPRE obligatoire pour les zones regles-immuables/, BLOQUE meme avec autorisation si contradiction), protocole-securite-marbre v0.1.1 documente, test-057 adapte (24/24), garde-fou test-084 cree (8/8 avec preuve negative doublon IMMUABLE). 83 tests au total. Lancer la non-regression complete (mode barriere) et rendre le verdict final a Cerberus.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 18:52 | session-llm-1 | morpheus | MISSION MORPHEUS (2 taches) : 1) ADAPTER test-057-marbre-garde-fou : la version de proteger-modifier-marbre est passee 0.1.2 -> 0.1.3 (relecture Argus obligatoire avant gravure des zones de regles). Chercher '0.1.2' dans le test et le passer a '0.1.3'. 2) CREER LE GARDE-FOU test-084 (relecture avant gravure) sur le modele test-083/056 (protections importees, triplet chrono) : verifier que la porte proteger-modifier-marbre v0.1.3 1) contient la fonction est_zone_regles + audit_regles_propre (zone regles-immuables/ = audit obligatoire) ; 2) --version affiche v0.1.3 ; 3) sur une zone REGLE (regles-groupes-agents) avec --autorisation UTILISATEUR et audit PROPRE : rc=0 ou 'contenu inchange' (audit lance) ; 4) PREUVE NEGATIVE : injecter un doublon EXACT de titre de section IMMUABLE dans le vrai regles-groupes-agents.md (sauvegarde/restauration obligatoire), lancer la porte avec autorisation -> rc=1 BLOQUE avec 'relecture Argus' (restaurer TOUJOURS + resynchroniser le marbre apres) ; 5) verifier le protocole-securite-marbre v0.1.1 documente la relecture. Ajouter au lanceur serie A + profil regles. Normes ASCII + LF. FIN : lecon Morpheus + reactiver Janus pour la non-regression.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 18:52 | session-llm-1 | buffy | MISSION BUFFY : DOCUMENTER LA RELECTURE OBLIGATOIRE AVANT GRAVURE dans le protocole de securite du marbre. CONTEXTE : Vulcain a mecanise la porte du marbre v0.1.3 (toute zone regles-immuables/ exige l audit Argus detecter-contradictions --regles PROPRE avant gravure, sinon BLOQUE meme avec autorisation). A FAIRE : 1) trouver le protocole de securite du marbre (protocole-securite-marbre ou protocole marbre dans regles-immuables/general/) et y ajouter l etape RELECTURE OBLIGATOIRE : avant la validation utilisateur, l audit Argus doit etre PROPRE (doublons + contradictions + concordance source/protocole) ; 2) verifier que regles-groupes-agents.md (ou le protocole) documente cette relecture - si c est une regle du marbre, la section doit le mentionner ; 3) normes ASCII + LF. NE PAS toucher a l outil (Vulcain) ni aux tests (Morpheus). FIN : lecon Buffy + activer MORPHEUS pour adapter test-057 (version 0.1.2 -> 0.1.3) et creer le garde-fou test-084 (relecture avant gravure).

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 18:49 | session-llm-1 | vulcain | MISSION VULCAIN : MECANISER LA RELECTURE OBLIGATOIRE AVANT GRAVURE (porte du marbre v0.1.2 -> v0.1.3). DEMANDE UTILISATEUR : toute nouvelle regle immuable doit passer l audit Argus (detecter-contradictions --regles : doublons + concordance source/protocole) AVANT la porte du marbre. A FAIRE dans proteger-modifier-marbre.py : 1) ajouter l option --audit-obligatoire (defaut ACTIF pour les zones de regles) : quand la zone a modifier/ajouter est une zone de REGLES (regles-groupes-agents, regles-general-global, constitution, ou toute zone dont le fichier est dans regles-immuables/), la porte appelle detecter-contradictions --regles AVANT d accepter l autorisation et BLOQUE si le verdict n est pas PROPRE ; 2) la sortie de l audit doit etre affichee et journalisee dans marbre-log.jsonl (champ audit: PROPRE/BLOQUE) ; 3) --no-audit pour les cas non-regles (documente) ; 4) bump version 0.1.2 -> 0.1.3 (.py + .md) ; 5) preuves : zone regle avec audit PROPRE = OK, simulation d une contradiction (fichier temp de regles) = BLOQUE. Normes ASCII + LF. FIN : lecon Vulcain + activer BUFFY pour documenter le protocole + MORPHEUS pour le garde-fou test-084.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 18:49 | session-llm-1 | Cerberus | BILAN CONSOLIDE (Janus, garde-fou test-083) : VERDICT VALIDE - NON-REGRESSION 82 OK / 0 KO (112.4s, base mise a jour). Le nouveau garde-fou test-083 (9/9) verifie la synchronisation des 8 regles exclusives IMMUABLE de regles-groupes-agents.md avec leur protocole associe (concordance termes cles + garde-fou cite + preuve negative). Il a detecte 3 ecarts REELS corriges par Buffy : 1) protocole-tests ne citait jamais JANUS (ajout section SEUL JANUS LANCE LA NON-REGRESSION) ; 2) protocole-verification-coherence ne citait jamais CLIO (ajout mention CLIO seul habite a mettre a jour le README) ; 3) sections MODELE DE CONFIANCE + RELEVE MEME ROUND sans garde-fou (ajout test-056/057 + porte du marbre). test-083 ajoute serie A + profil regles. Registre propre, ko-tests vide, 0 residu. |
| 2026-08-16 18:46 | session-llm-1 | janus | REPRISE JANUS : garde-fou test-083 cree (9/9) - synchronisation des regles exclusives source/protocole. 3 ecarts corriges par Buffy (JANUS dans protocole-tests, CLIO dans protocole-verification-coherence, garde-fous des 2 sections + porte du marbre). test-083 ajoute serie A + profil regles, 82 tests au total. Lancer la non-regression complete (mode barriere) et rendre le verdict final a Cerberus.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 18:46 | session-llm-1 | morpheus | REPRISE MORPHEUS : test-083 cree (9/9 vert) + 3 ecarts de synchronisation corriges par Buffy (protocole-tests cite JANUS, protocole-verification-coherence cite CLIO, garde-fous ajoutes aux 2 sections + porte du marbre). test-083 ajoute au lanceur (serie A + profil regles). Verifier test-029 (conformite template) et test-030 (protections importees) sur le nouveau test-083, puis reactiver Janus pour la non-regression complete.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 18:42 | session-llm-1 | buffy | MISSION BUFFY : CORRIGER LES 3 ECARTS DE SYNCHRONISATION DETECTES PAR LE NOUVEAU GARDE-FOU test-083 (protocoles = ton domaine). CONTEXTE : test-083 verifie que chaque regle exclusive IMMUABLE de regles-groupes-agents.md est dupliquee de facon CONCORDANTE dans son protocole associe. 3 ecarts detectes : 1) protocole-tests ne cite JAMAIS JANUS (0 occurrence) alors que la section SEUL JANUS LANCE LA NON-REGRESSION le reference comme protocole de lancement - ajouter la mention que JANUS est le SEUL habilite a lancer la non-regression complete ; 2) protocole-verification-coherence ne cite JAMAIS CLIO (l Agent du protocole est Themis) alors que la section SEUL CLIO MET A JOUR LE README le reference - ajouter CLIO comme proprietaire du README (sections SEUL CLIO + mise a jour du README) ; 3) regles-groupes-agents.md : les sections LE MODELE DE CONFIANCE et RELEVE MEME ROUND n ont PAS de garde-fou test-XXX cite - ajouter le garde-fou reel (verifier quel test les couvre : test-057 marbre pour la constitution, test-052 releve-meme-round ou equivalent, sinon documenter le protocole qui les verifie). CONTRAINTES : editer via outils de ta carte, ASCII strict + LF, NE PAS toucher au test-083 ni aux cartes d agents. FIN : lecon Buffy + reactiver Morpheus pour reverdir test-083 puis Janus pour la non-regression.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 18:39 | session-llm-1 | morpheus | MISSION MORPHEUS : CREER LE GARDE-FOU test-083 (synchronisation des regles exclusives en double). CONTEXTE : la regle 'SEUL MORPHEUS ECRIT LES TESTS' existe a 2 endroits (regles-groupes-agents.md section 112 + protocole-tests.md ligne 257) - duplication source/protocole fragile, aucune relecture automatique ne verifie leur CONCORDANCE. regles-groupes-agents.md a 8 sections exclusives IMMUABLE : SEUL HYGIE SUPPRIME (79, protocole-nettoyage, test-045), SEUL JANUS LANCE LA NON-REGRESSION (98, protocole-tests, test-037), SEUL MORPHEUS ECRIT LES TESTS (112, protocole-tests, test-059), SEUL CLIO MET A JOUR LE README (134, protocole-verification-coherence, test-020), SEUL BUFFY CORRIGE LES FICHIERS DES AGENTS (156, protocole-controle-buffy, test-058), LE MODELE DE CONFIANCE (184), RELEVE MEME ROUND (211, protocole-activation), RELIRE SA FICHE AVANT MISSION (238, protocole-activation). A CREER (modele test-059/056 : protections importees, triplet chrono, fichiers temp) : un test qui 1) liste les sections (IMMUABLE) de regles-groupes-agents.md ; 2) pour chacune, verifie que le protocole ASSOCIE (cite dans la section) contient les MEMES termes cles (ex: 'SEUL MORPHEUS', 'morpheus est le SEUL', 'ecrit', 'test') - concordance source/protocole ; 3) PREUVE NEGATIVE : injecter dans un protocole temp une version divergente (ex 'morpheus ne fait que relire les tests') et constater la detection ; 4) verifier que chaque section cite bien un protocole et un garde-fou (pas de section orpheline). Ajouter au lanceur (serie A ou B selon le temps) + profil. Normes ASCII + LF. FIN : lecon Morpheus + reactiver Janus pour la non-regression.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 18:36 | session-llm-1 | Cerberus | BILAN CONSOLIDE (Janus, mission carte + cle exclusive) : VERDICT VALIDE - NON-REGRESSION 81 OK / 0 KO. Corrections : 1) CARTE JANUS v0.4.12 (Buffy) : c4 'Verifier les tests' sans editer-fichier (Janus VERIFIE, ne modifie pas - Morpheus seul ecrit les tests). Le bumper (mettre-a-jour-versions) etait deja en c33. 2) VERROU v0.2.1 (Vulcain) : option --cible + zone protegee tester/tests/ = EXCLUSIF morpheus (depasse la table des cartes) ; editer-fichier v0.4.2 branche le verrou avec --agent obligatoire ; spec generateurs 0.2.3 alignee (KO test-028 corrige). 3) TEST-056 v0.2.1 (Morpheus) : preuves cle exclusive 11/11b/11c (buffy bloque sur test, morpheus ouvre, hors zone carte). 4) Janus : declaration fautive retiree du registre, editer-fichier .sh re-synchronise, bumper 0 incoherent. Registre propre, ko-tests vide, 0 residu. |
| 2026-08-16 18:29 | session-llm-1 | janus | REPRISE JANUS : carte janus v0.4.12 corrigee (c4 sans editer-fichier), verrou v0.2.1 avec cle exclusive morpheus (--cible, preuve 11/11b/11c dans test-056 15/15), spec generateurs 0.2.3 alignee (test-028 vert), editer-fichier v0.4.2 branche verrou. Lancer la non-regression complete (mode barriere) et rendre le verdict final a Cerberus.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 18:28 | session-llm-1 | morpheus | MISSION MORPHEUS : ADAPTER TEST-056 AU VERROU v0.2.1 (cle exclusive morpheus). CONTEXTE : Vulcain a ajoute --cible au verrou proteger-verrou-habilitation v0.2.1 : toute cible contenant 'tester/tests/' avec un outil de modification (editer-fichier, editer-parcours, creer-fichier, ecrire-fichier, supprimer-*, corriger-*) est EXCLUSIVE a morpheus. editer-fichier v0.4.2 branche le verrou avec --cible et exige --agent. A FAIRE dans test-056-verrou-habilitation : 1) adapter la version 0.2.0 -> 0.2.1 (point 1 + docstring) ; 2) AJOUTER une preuve de la CLE EXCLUSIVE : verrou --audit --agent buffy --outil editer-fichier --cible <chemin tester/tests/...> = BLOQUE avec mention 'EXCLUSIVE a morpheus', et --agent morpheus meme cible = OK ; 3) verifier aussi editer-fichier sans --agent sur une cible test = erreur/refus. Normes ASCII + LF. FIN : lecon Morpheus + reactiver Janus pour la non-regression complete.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 18:24 | session-llm-1 | vulcain | MISSION VULCAIN (2 taches) : 1) GRAVER LA CLE EXCLUSIVE MORPHEUS DANS LE VERROU proteger-verrou-habilitation : la regle immuable 'SEUL MORPHEUS ECRIT/ADAPTE LES TESTS' existe (regles-groupes-agents + test-059) MAIS le verrou se base uniquement sur les cartes - tant que editer-fichier est dans une carte, l exclusivite est contournable. Ajouter une protection SPECIFIQUE : tout outil editer-fichier/editer-parcours/creer-fichier cible sur un fichier de test (chemin contenant tester/tests/) est BLOQUE sauf pour morpheus (et janus seulement en lecture via le lanceur). 2) ALIGNER LA SPEC du generateurs-outil-temporaire : KO test-028 'spec DIVERGENTE' - le bump 0.2.2 -> 0.2.3 n a pas ete repercute dans la spec de l outil (verifier generateurs-outil-temporaire.md spec ou spec correspondante - chercher la spec liee au generateur et aligner 0.2.3). Normes ASCII + LF. FIN : lecon Vulcain + reactiver Janus pour la revalidation.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 18:23 | session-llm-1 | buffy | REPRISE BUFFY (mission carte janus en cours)

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 18:22 | session-llm-1 | buffy | MISSION BUFFY : CORRIGER LA CARTE DE JANUS (v0.4.11 -> v0.4.12) VIA EDITER-PARCOURS UNIQUEMENT. CONTEXTE : Janus a corrige des fichiers de tests au lieu de les renvoyer a Morpheus - la case c4 'Verifier les tests' de parcours-janus.json contient un indice outil editer-fichier (source de la derive). De plus le bumper est ABSENT de la carte de Janus (il ne peut pas l utiliser, le verrou le bloque). A FAIRE : 1) RETIRER l indice editer-fichier de la case c4 (Janus VERIFIE les tests, il ne les EDITE pas - SEUL MORPHEUS ecrit/adapte les tests, regle immuable) ; 2) AJOUTER un indice outil bumper (outil de bump de version) dans une case adaptee de la carte de Janus (ex c9 'Lecons et retour' ou c34 'Enregistrer mes usages') pour que Janus puisse bumper systematiquement ; 3) bumper la version du parcours 0.4.11 -> 0.4.12 ; 4) mettre a jour la fiche janus.md (Pattern 14 : version + bloc FINS REELLES si besoin) ; 5) verifier valider-cartes-decision --agent janus CONFORME + normes ASCII strict + LF. NE PAS toucher aux tests (Morpheus/Janus les gerent). FIN : lecon Buffy + activer VULCAIN pour le verrou.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 18:22 | session-llm-1 | Cerberus | BILAN JANUS (carte a revoir + KO en attente) : 1) CARTE JANUS v0.4.11 : la case c4 'Verifier les tests' contient editer-fichier en indice outil - cela a PERMIS a Janus de corriger des fichiers de tests au lieu de les renvoyer a Morpheus (REGLE 4 non respectee par moi - je signale, je ne corrige pas). 2) BUMPER ABSENT de la carte de Janus (aucun indice bumper) - il ne peut pas l utiliser, le verrou le bloquerait. 3) La regle immuable 'SEUL MORPHEUS ECRIT ET EXECUTE LES TESTS' existe (regles-groupes-agents + garde-fou test-059) MAIS le verrou se base sur les cartes : tant que editer-fichier est en c4 de Janus, l exclusivite est contournable. 4) KO EN ATTENTE non-regression : test-028 (spec divergente - probablement le bump generateur 0.2.3 non repercute dans une spec) + test-024 (tmp-vulcain residuel - PURGE par moi). A DECIDER : Buffy retire editer-fichier de c4 (via editer-parcours) + ajoute bumper a la carte Janus ; Vulcain aligne la spec ; Morpheus revalide les tests. Je ne corrige pas moi-meme. |
| 2026-08-16 18:19 | session-llm-1 | janus | REPRISE JANUS : la course test-050/test-079 est corrigee (generateur v0.2.3 env var CERVEAU_REGISTRE_USAGES + test-050 adapte 18/18, test-079 15/15, preuve parallele OK). Relancer la non-regression complete (mode barriere) et rendre le verdict final a Cerberus.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 18:17 | session-llm-1 | morpheus | MISSION MORPHEUS : ADAPTER TEST-050 AU GENERATEUR v0.2.3 (env var CERVEAU_REGISTRE_USAGES) POUR ELIMINER LA COURSE test-050/test-079. CONTEXTE : Vulcain a ajoute au squelette du generateur l env var CERVEAU_REGISTRE_USAGES (si definie, declarer_usage ajoute --registre <valeur>). Le generateur est passe en 0.2.3 (py + sh + md). A FAIRE dans test-050-triplet-outils-temporaires : 1) au moment d executer le script genere (points 5/6/7, et toute autre execution), definir os.environ[CERVEAU_REGISTRE_USAGES] = <registre temp dans dossier_test> pour que la declaration aille dans le registre temp et JAMAIS dans le registre reel ; 2) adapter les references 0.2.2 -> 0.2.3 (points 1, 9, 11, 12 + docstring) ; 3) le point 17 (nettoyage) doit verifier le REGISTRE TEMP (la preuve ne va plus au reel) ; 4) verifier ensuite test-079 passe toujours (registre reel PROPRE), et lancer test-050 seul. Normes ASCII strict + LF. FIN : lecon Morpheus + reactiver Janus.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 18:16 | session-llm-1 | vulcain | MISSION VULCAIN : ELIMINER LA COURSE test-050/test-079 (KO FLAKY NON-REGRESSION). CONTEXTE : test-050 et test-079 sont dans la meme serie A. test-050 execute le script genere (points 5/6/7) dont le squelette declarer_usage appelle enregistrer-usage-outil SANS --registre -> declaration tmp-t050-preuve.py dans le REGISTRE REEL pendant que test-079 analyse le registre en parallele -> OUTIL_CHEMIN transitoire -> KO flaky (registre propre ensuite, point 17 nettoie). A CORRIGER : 1) ajouter au squelette du generateur (generateurs-outil-temporaire.py + .sh PARITE) le support d une variable d environnement CERVEAU_REGISTRE_USAGES : si definie, declarer_usage ajoute --registre <valeur> a la commande enregistrer-usage-outil ; 2) bump 0.2.2 -> 0.2.3 (py + sh + md) ; 3) normes ASCII strict + LF sur les 3 fichiers. NE PAS toucher aux tests (Morpheus adaptera test-050 ensuite). FIN : lecon Vulcain + reactiver Janus.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 18:09 | session-llm-1 | janus | REPRISE JANUS (suite chaine, evaluer-processus v0.1.5 corrige par Vulcain) : le KO test-035 etait un faux positif (fins_de_la_carte ne reconnaissait pas la fin legitime Themis c25b Activer l agent precedent + a_reactiver jamais utilise). Tout est vert : evaluer-processus 0 probleme, test-035 10/10, 016/037/055/064 verts. RELANCER LA NON-REGRESSION COMPLETE en mode barrieres --agent janus. FIN : lecon Janus + bilan consolide a Cerberus.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 18:07 | session-llm-1 | vulcain | MISSION VULCAIN (KO test-035 decouvert par Janus) : corriger evaluer-processus v0.1.4 - la fonction fins_de_la_carte ne reconnait PAS les fins 'Activer l agent precedent' (themis c25b, atlas) comme des fins de reactivation valides : elle ne detecte a_reactiver que si le titre contient 'Reactiver Cerberus' ou le message 'reactiver session-llm-1'. Resultat : la mission Themis (audit sur demande de Cerberus, fin legitime c25b 'Activer l agent precedent') est signalee FIN_MISSION_ERRONEE a tort -> test-035 KO. CORRECTION : dans fins_de_la_carte, detecter aussi le titre 'Activer l agent precedent' (et variantes) comme a_reactiver=True. Bump 0.1.4 -> 0.1.5 (py + md). VERIFIER : evaluer-processus ne signale plus FIN_MISSION_ERRONEE pour themis ; les tests qui pincent la version (test-035, 016, 037, 055, 064) restent verts ou a adapter. FIN : lecon Vulcain puis REACTIVER JANUS pour relancer la non-regression complete.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 17:59 | session-llm-1 | janus | REPRISE JANUS (suite chaine Themis -> Buffy -> Morpheus) : valider la carte de Cerberus v0.5.0 (habilitations limitees : combos-analyse-projet retire de c10, lire-fichier dedoublonne en c0b, porte du marbre passee avec autorisation utilisateur, lock resynchronise). test-013 adapte 22/22, test-016 vert. LANCER LA NON-REGRESSION COMPLETE en mode barrieres --agent janus. FIN : lecon Janus + bilan consolide a Cerberus.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 17:58 | session-llm-1 | morpheus | MISSION MORPHEUS (suite chaine Buffy, verdict Themis carte Cerberus) : ADAPTER test-013-cerberus-migration apres le bump de la carte de Cerberus 0.4.9 -> 0.5.0 (case c10 : combos-analyse-projet retire, habilitations Cerberus limitees a coordination + lecture). Le test a 1 KO : point 1 'Parcours version 0.4.9' -> passer a 0.5.0. VERIFIER : test-013 vert (tous les points), les autres references 0.4.9 dans les tests (test-016? test-018? test-021?) ne pincent pas la version de la carte cerberus, puis REACTIVER JANUS pour la non-regression complete. FIN : lecon Morpheus.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 17:52 | session-llm-1 | buffy | MISSION BUFFY (verdict Themis, demande utilisateur habilitations Cerberus) : CORRIGER LA CARTE DE CERBERUS (parcours-cerberus.json v0.4.9) pour limiter ses habilitations a la coordination et a la lecture. CORRECTIONS via editer-parcours : (1) M1 MAJEUR - retirer l indice outil combos-analyse-projet de la case c10 (outil d analyse avec rapport ecrit, proprietaire Clio : contraire aux garde-fous c1/c5/c18/c22 AUDIT/ANALYSE -> Themis) ; (2) m1 MINEUR - dedoublonner lire-fichier dans la case c0b (indice present 2 fois, garder 1). BUMP 0.4.9 -> 0.5.0 + fiche cerberus.md Pattern 14. VERIFIER : valider-cartes-decision --agent cerberus CONFORME, aucune reference combos-analyse-projet restante dans la carte cerberus. FIN : lecon Buffy puis ACTIVER MORPHEUS pour adapter test-013-cerberus-migration si necessaire.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 17:52 | session-llm-1 | Cerberus | BILAN CONSOLIDE (Themis, audit carte Cerberus) : VERDICT - carte v0.4.9 globalement CONFORME (garde-fous c1/c5/c18/c22 presents : audit/inventaire/analyse -> Themis, jamais Cerberus) MAIS 1 correction majeure : case c10 contient combos-analyse-projet (outil d analyse avec rapport ecrit, proprietaire Clio) - le trou de la derive du jour. + 1 nettoyage mineur : doublon lire-fichier en c0b. Recommandation : Buffy retire combos-analyse-projet de c10 (editer-parcours) + bump 0.4.9->0.5.0, Morpheus adapte test-013, Janus valide. Rapport : themis/rapports/rapport-audit-carte-cerberus-habilitations-2026-08-16.md. |
| 2026-08-16 17:50 | session-llm-1 | themis | MISSION THEMIS (demande utilisateur, apres derive Cerberus) : AUDITER LA CARTE DE CERBERUS (parcours-cerberus.json v0.4.9, 36 cases) pour verifier que ses habilitations sont limitees a certains outils et en LECTURE. CONTEXTE : Cerberus a fait un diagnostic/audit de la convention des scripts temporaires alors que c est le travail de Themis - la carte contient deja les garde-fous c1/c5/c18/c22 (audit/inventaire/analyse -> Themis, jamais Cerberus) mais ils n ont pas ete respectes. VERIFIER : (1) chaque case avec indice outil (c3 lister-agents, c0c lire-activite-recente, c0d lire doc outil, c24 enregistrer-usage-outil, c1b/c19c generateurs-amelioration) est bien un outil de COORDINATION ou de LECTURE, jamais d audit/diagnostic/analyse ; (2) aucune case n habilite Cerberus a lancer des outils d audit (detecter-*, analyser-*, evaluer-*, valider-*) ; (3) les garde-fous c1/c5/c18/c22 sont contraignants (branchement correct) ; (4) la case c0d ne permet pas d utiliser n importe quel outil. PRODUIRE un rapport d audit (themis/controles/) avec verdict : carte conforme OU cases a corriger (liste precise). FIN : lecon Themis + reactiver Cerberus avec le verdict.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/themis/parcours/parcours-themis.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 17:45 | session-llm-1 | Cerberus | BILAN CONSOLIDE (Janus, chaine anti /tmp systeme) : 81 OK / 0 KO, 107.0s (reference mise a jour). Buffy : protocole creation-scripts-temporaires v0.2.11 (Journalisation et redirections de sortie - toute capture .log dans tmp-AGENT/, jamais /tmp systeme). Morpheus : tester-protection-erreurs-silencieuses corrige (logs dans cerveau-projet/agents/traces/protection-logs/, .py 0.2.1-py, .sh 0.1.1) + garde-fou test-082 (9/9, scan production hors tests/, preuves negatives) + test-057 corrige (classeur temp, profil intact). Janus : registre propre (2 declarations superflues retirees), verites preservees. Plus aucune ecriture /tmp dans le code de production. 0 residu. |
| 2026-08-16 17:41 | session-llm-1 | janus | REPRISE JANUS (suite chaine, test-057 corrige par Morpheus) : relancer la NON-REGRESSION COMPLETE en mode barrieres --agent janus. RAPPEL : (1) protocole v0.2.11 anti /tmp systeme, (2) tester-protection-erreurs-silencieuses logs dans workspace, (3) test-082 garde-fou anti /tmp, (4) test-057 corrige (classeur temp, profil non modifie). Si la serie KO (ko-tests.json) contient test-024, le relancer via --ko reprendre ou le laisser passer s il est vert. FIN : lecon Janus + bilan consolide a Cerberus.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 17:40 | session-llm-1 | morpheus | MISSION MORPHEUS (suite chaine Janus, bug decouvert en non-regression) : test-057-marbre-garde-fou point 10 corrompt le VRAI profil classeur. DIAGNOSTIC Janus : le point 10 fait un reactiver session-llm-1 avec AGENTS_FILE et AGENTS_HISTORIQUE pointant vers des fichiers temp, MAIS CLASSEUR_STOCKAGE pointe vers le VRAI variables-actuelles.md -> la reactivation reecrit le profil avec agent: Cerberus pendant la suite, ce qui casse test-024 (dossier tmp-AGENT non reconnu car le profil dit Cerberus au lieu de janus). CORRECTION : dans le point 10, copier le vrai variables-actuelles.md vers un fichier temp (comme AGENTS_FILE) et pointer CLASSEUR_STOCKAGE vers ce temp ; supprimer le temp dans le finally. VERIFIER : test-057 vert, le profil classeur n est PLUS modifie par le test (avant/apres identiques), test-024 vert. FIN : lecon Morpheus puis REACTIVER JANUS pour relancer la non-regression complete.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 17:36 | session-llm-1 | janus | MISSION JANUS (suite chaine Buffy -> Morpheus, demande utilisateur anti /tmp systeme) : valider la correction + le nouveau garde-fou. CHANGEMENTS : (1) protocole creation-scripts-temporaires v0.2.11 (section Journalisation et redirections de sortie : toute capture .log va dans tmp-AGENT/, jamais /tmp systeme) ; (2) tester-protection-erreurs-silencieuses corrige (.py 0.2.1-py, .sh 0.1.1) : logs dans <racine>/cerveau-projet/agents/traces/protection-logs/ au lieu de /tmp/test-logs ; (3) test-082-pas-de-tmp-systeme-garde-fou cree (9/9, serie A + profil outils) : scan production hors tests/, preuves negatives A/B/C. VERIFIER : test-082 vert, test-029/030 verts, test-035 vert, registre sain, normes 0/0, puis NON-REGRESSION COMPLETE en mode barrieres. FIN : lecon Janus + bilan consolide a Cerberus.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 17:32 | session-llm-1 | morpheus | MISSION MORPHEUS (suite chaine Buffy, demande utilisateur) : les agents ecrivaient leurs .log vers le /tmp systeme au lieu de tmp-AGENT/ - protocole v0.2.11 corrige par Buffy (section Journalisation et redirections de sortie). CREER LE GARDE-FOU anti-recurrence : test-082 (nom a confirmer, prochain libre) qui scanne le code de PRODUCTION des outils et combos (fichiers .py/.sh hors dossiers tests/) et detecte toute redirection d ecriture hors workspace (/tmp/, /tmp/x.log, > /tmp). Les vieux .sh de tests d outils legacy (13 fichiers dans outils/*/*/tests/) sont EXCLUS du scan (dette documentee, hors suite). Le scan ne doit pas casser la suite existante (test-024 reste sur la racine). Ajouter le test a la serie adequate + profil. CONTEXTE : version lanceur 0.5.5, tests jusqu a test-081. FIN : lecon Morpheus puis ACTIVER JANUS pour la non-regression complete.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 17:31 | session-llm-1 | buffy | MISSION BUFFY (demande utilisateur) : les agents ecrivent leurs .log vers le /tmp du systeme au lieu du dossier tmp-AGENT du workspace - constat utilisateur. Le protocole creation-scripts-temporaires (v0.2.10) ne couvre que les SCRIPTS jetables, RIEN sur les journaux et redirections de sortie. AJOUTER au protocole une section explicite JOURNALISATION ET REDIRECTIONS DE SORTIE : toute capture de sortie ou .log doit aller dans tmp-AGENT/fichier.log, JAMAIS vers le /tmp systeme ni ailleurs hors workspace ; bump 0.2.10 vers 0.2.11 ; RVAV ajoutee. CONTEXTE : 13 vieux .sh de tests d outils (activer-agent-principal, detecter-impacts...) utilisent /tmp - dette legacy a DOCUMENTER dans la lecon, pas a migrer. FIN : lecon Buffy puis ACTIVER MORPHEUS pour creer le garde-fou anti-recurrence (scan des outils hors tests pour toute redirection d ecriture hors workspace).

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 17:27 | session-llm-1 | Cerberus | NON-REGRESSION COMPLETE 80 OK / 0 KO (5 barrieres, 108.9s) apres la SERIE KO PRIORITAIRE v0.5.5 (demande utilisateur). BILAN : (1) Vulcain v0.5.5 : ko-tests.json persistant (gitignore, cree au premier lancement), option --ko <nouveau|reprendre> (defaut reprendre) + --etat-ko ; mode REPRENDRE = barriere KO en premier (tests du fichier, ceux qui passent sortent et ne sont PAS relances dans leur serie = idempotence), fantomes purges, KO persistant = barriere bloquee ; mode NOUVEAU = vide le fichier, lance les series, collecte les KO ; ordre KO -> A -> B -> C -> D -> E en parallele ; (2) Morpheus : 9 tests adaptes au bump 0.5.5 (024/027/031/032/051/062/066/074/075, test-066 cible future 0.5.6) + garde-fou test-081 (10/10, serie A + profil tests, preuve negative fantome purge) ; (3) Janus : preuves reelles --etat-ko / --ko nouveau serie A 31 OK / --ko reprendre (test-007 valide non relance) / suite complete 80 OK ; (4) registre propre (141, verites preserves), ko-tests.json vide, 0 residu, normes 0/0. LECONS : la serie KO tenait sa promesse de productivite (revalider les KO sans relancer la suite) ; le verrou d identite protege la suite (preuve test-081 = structure sans dependre du rc) ; l ajout d un test = serie + profil + couverture test-027. SUITE RECOMMANDEE : Janus utilise --ko reprendre dans son workflow quotidien (KO d abord, suite complete quand tout est vert). |
| 2026-08-16 17:23 | session-llm-1 | janus | NON-REGRESSION COMPLETE apres la serie KO prioritaire v0.5.5. CONTEXTE : Vulcain a ajoute la serie KO au lanceur (ko-tests.json persistant, --ko <nouveau|reprendre> defaut reprendre, --etat-ko, barriere KO en premier avec purge des fantomes et idempotence test-valide-non-relance) ; Morpheus a adapte les 9 tests (024/027/031/032/051/062/066/074/075 : 0.5.4 -> 0.5.5, test-066 cible future 0.5.6) et cree le garde-fou test-081 (10/10, serie A + profil tests). PREUVES REALISEES : test-081 10/10, test-030 10/10, test-029 14/14, test-027 point 1 OK (couverture), normes 0/0, registre propre (125), ko-tests.json vide. CONSIGNE : 1) lancer la non-regression COMPLETE (--agent janus, 80 tests), 2) si KO : analyser, activer l agent habilite, relancer, 3) verifier que la serie KO fonctionne en mode reel (--etat-ko, un --ko nouveau), 4) chrono + reference, 5) lecon Janus + reactiver Cerberus avec bilan consolide. IMPORTANT : les tests 027/031/032/051/062/066/074/075/081 qui pincent --version doivent etre verts (0.5.5).

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 17:20 | session-llm-1 | morpheus | ADAPTER LES 9 TESTS AU BUMP LANCEUR 0.5.5 (serie KO prioritaire) + CREER LE GARDE-FOU TEST-081. CONTEXTE : Vulcain a ajoute la serie KO prioritaire au lanceur v0.5.5 : fichier persistant ko-tests.json, option --ko <nouveau|reprendre> (defaut reprendre) + --etat-ko. Mode REPRENDRE : la serie KO (tests du fichier) se lance EN PREMIER avec sa barriere - ceux qui passent sortent du fichier et ne sont PAS relances dans leur serie ; mode NOUVEAU : vide le fichier et lance les series normalement (les KO du run sont collectes). PREUVES REALISEES (Janus) : --etat-ko OK, --ko nouveau serie C 15 OK, --ko reprendre avec test-007 + fantome : barriere KO en premier, test-007 valide non relance, fantome purge ; --ko reprendre avec KO persistant : barriere KO BLOQUEE. TACHE 1 - ADAPTER 9 TESTS qui pincent 0.5.4 : test-024, 027, 031, 032, 051, 062, 066, 074, 075 (0.5.4 -> 0.5.5 ; test-066 : la cible future du bumper doit passer de 0.5.5 a 0.5.6). TACHE 2 - CREER TEST-081 (garde-fou serie KO, template v0.3.0, protections importees, triplet chrono) : verifie (1) --aide contient --ko et --etat-ko, (2) --version = v0.5.5, (3) le fichier ko-tests.json est cree par --ko nouveau et vide, (4) l option --ko accepte nouveau|reprendre (rejet des autres valeurs), (5) --etat-ko affiche le contenu, (6) la fonction lire_ko_tests/ecrire_ko_tests filtre les noms test-0XX, (7) PREUVE NEGATIVE : ecrire un KO fantome dans le fichier, lancer --ko reprendre --tests <un test reel>, verifier que le fantome est purge et que le test reel passe -> fichier vide. AJOUTER test-081 a la serie A + profil outils. VERIFIER : normes ASCII + LF, purge tmp, declaration registre (outils autorises uniquement - NE PAS declarer tester-lancer-non-regression, exclusif janus). FIN : lecon Morpheus + ACTIVER JANUS pour la non-regression complete.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 17:15 | session-llm-1 | janus | PHASE DE TEST RAPIDE de la serie KO prioritaire v0.5.5 (mission Vulcain en cours - retour immediat a Vulcain apres). Objectif : prouver le comportement du lanceur avec --ko nouveau / --ko reprendre avant de finaliser la mission Vulcain. CONSIGNE : 1) lancer --etat-ko (fichier vide), 2) lancer --ko nouveau sur une serie rapide (ex: --series c --ko nouveau) et verifier la collecte des KO dans ko-tests.json, 3) lancer --ko reprendre et verifier que la serie KO passe en premier avec sa barriere, 4) rapporter le comportement a Vulcain (les modifications du lanceur sont en cours, NE PAS lancer la suite complete).

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 17:12 | session-llm-1 | vulcain | CREER LA SERIE KO PRIORITAIRE DANS TESTER-LANCER-NON-REGRESSION (design valide par l utilisateur). CONTEXTE : la non-regression (79 tests, 5 barrieres) est verte mais Janus perd du temps a revalider les KO : il relance la suite complete a chaque correction. DEMANDE : serie KO persistante et PRIORITAIRE. FONCTIONNEMENT : (1) fichier persistant ko-tests.json dans le dossier du lanceur (comme config-tests.json, cree au premier lancement, gitignore si config-tests l est) ; (2) option --ko <nouveau|reprendre> (defaut : reprendre) ; (3) mode NOUVEAU : vide le fichier ko-tests.json (les KO du run precedent sont oublies), lance les series normalement (ordre A,B,C,D,E avec barrieres), collecte les tests en KO dans ko-tests.json ; (4) mode REPRENDRE : lance D ABORD la serie KO (les tests listes dans ko-tests.json) avec SA barriere - les tests KO qui passent sont RETIRES du fichier et ne sont PAS relances dans leur serie d origine (marques valides pour ce run) ; si un test de la serie KO echoue encore, la barriere KO BLOQUE et la suite s arrete (Janus corrige puis relance en reprendre) ; une fois la barriere KO franchie, les series A-E s executent SANS les tests deja valides par la serie KO, et les nouveaux KO rejoignent ko-tests.json ; (5) ordre global : KO (barriere) -> A -> B -> C -> D -> E, chaque serie en parallele ; (6) le mode reprendre doit etre IDEMPOTENT : un test qui repasse vert sort du fichier et ne tourne qu UNE fois par run. CONTRAINTES : ASCII strict, LF, argparse, garder la rotation non destructive v0.5.4 (ne pas casser), ne pas casser les options existantes (--relancer-ko, --series, --activer/--desactiver), compatibilite avec le mode barrieres existant. TESTS REELS : (1) --ko nouveau sur la suite verte : 0 KO, fichier cree vide ; (2) simuler un KO (desactiver volontairement un test ou injecter un echec) puis --ko nouveau : le test KO est dans le fichier ; (3) --ko reprendre : la serie KO se lance en premier, le test passe -> retire du fichier, PAS relance dans sa serie ; (4) --ko reprendre avec un KO persistant : barriere KO bloquee. APRES : bump version 0.5.4 -> 0.5.5 + doc .md + lecon Vulcain. FIN : activer MORPHEUS pour le garde-fou test-081 (verifie le comportement de la serie KO) puis Janus pour la non-regression.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 17:06 | session-llm-1 | Cerberus | NON-REGRESSION COMPLETE 79 OK / 0 KO (5 barrieres, 103.8s) apres le correctif rotation non destructive v0.5.4. BILAN : (1) cause racine KO recidivant test-078 = rotation_registre v0.5.3 du lanceur qui supprimait les usages anciens du registre a chaque lancement (perte generateurs-amelioration) ; (2) Vulcain v0.5.4 : rotation NON DESTRUCTIVE (seul le bruit verrou-auto plafonne, les verites direct/generateur/script-temporaire jamais retirees, idempotente) + restauration registre 227 puis propre 124-139 ; (3) Morpheus : 9 tests adaptes au bump 0.5.4 (024/027/031/032/051/062/066/074/075 - test-066 piege cible future 0.5.5, test-075 oublie au premier passage) ; (4) Janus : declarations fautives retirees (vulcain tester-lancer-non-regression, morpheus test-024), entree tmp-test-declaration normalisee par corriger-noms-maj 0.1.1, test-079 15/15, test-078 7/7, test-035 10/10 ; (5) registre source-de-verite sain (verites preserves), normes 0/0, 0 residu. LECONS : un plafond de rotation qui supprime des donnees de verite est incompatible avec les garde-fous ; une restauration peut ramener d anciens artefacts a re-verifier ; un bump d outil pilier exige un scan exhaustif des tests (test-075 oublie) ; les declarations registre sont soumises aux exclusivites. SUITE RECOMMANDEE : traiter la demande utilisateur serie KO prioritaire (design + implementation lanceur). |
| 2026-08-16 17:04 | session-llm-1 | janus | RELANCER LA NON-REGRESSION COMPLETE apres l adaptation du 9e test (test-075 0.5.4, oublie au premier passage). ETAT : rotation non destructive v0.5.4 (Vulcain), 9 tests adaptes (024/027/031/032/051/062/066/074/075), registre PROPRE (124 entrees, generateurs-amelioration presente, corriger-noms-maj 0.1.1 applique sur tmp-test-declaration), declarations fautives retirees (vulcain tester-lancer-non-regression + morpheus test-024). VERTS : test-078 7/7, test-035 10/10, test-079 15/15, test-075 11/11, normes 0/0. CONSIGNE : 1) relance ciblee serie A puis suite complete, 2) si KO : analyser, activer l agent habilite, relancer, 3) chrono + reference, 4) lecon Janus + reactiver Cerberus avec bilan consolide.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 17:03 | session-llm-1 | morpheus | ADAPTER LE 9e TEST AU BUMP LANCEUR 0.5.4 (test-075 oublie). CONTEXTE : la non-regression complete a trouve un KO test-075-filtre-serie-relancer-ko qui pince encore la version 0.5.3 (7 occurrences : lignes 6, 12, 21, 126, 128, 131, 132) - ce test n etait pas dans la liste des 8 adaptes par Morpheus. Le correctif rotation non destructive v0.5.4 (Vulcain) et l adaptation des 8 autres tests sont deja faits (test-078 7/7, test-035 10/10, test-079 15/15 verts). CONSIGNE : (1) remplacer 0.5.3 -> 0.5.4 dans test-075 (7 occurrences), (2) lancer test-075 pour reverdir, (3) normes ASCII + LF, (4) lecon courte Morpheus. FIN : ACTIVER JANUS pour la relance ciblee (serie A) puis suite complete.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
| 2026-08-16 17:00 | session-llm-1 | janus | REVALIDATION CIBLEE + NON-REGRESSION COMPLETE apres le correctif rotation non destructive v0.5.4 + adaptation des 8 tests. CONTEXTE : le KO test-078 recidivait (rotation_registre v0.5.3 supprimait les usages anciens du registre a chaque lancement - perte generateurs-amelioration). Vulcain a corrige v0.5.4 (seul le bruit verrou-auto est plafonne, les verites ne sont jamais retirees, rotation idempotente 2x = 124) et restaure le registre ; Morpheus a adapte les 8 tests (024/027/031/032/051/062/066/074) au bump 0.5.4 (test-066 cible future 0.5.5). Preuves deja faites : test-078 7/7, test-035 10/10, 062 11/11, 066 11/11, 074 8/8, normes 0/0, 0 residu. CONSIGNE : 1) revalidation ciblee serie A (078/035) puis suite complete, 2) si KO : analyser, activer l agent habilite, relancer, 3) rapporter chrono + reference, 4) lecon Janus + reactiver Cerberus avec bilan consolide.

DEMARRAGE OBLIGATOIRE (v0.5.4) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0 --reponses OUI
(reponds OUI si ta fiche et tes corrections sont en memoire, sinon relance
avec --reponses NON pour relire d abord ; suis ensuite les branches case
par case ; si tu reprends apres une interruption, reprends a la case courante
avec --case <cid> --reponses '<reponse>'). |
