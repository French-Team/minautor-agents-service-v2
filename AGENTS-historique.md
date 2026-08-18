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

| 2026-08-18 19:14 | session-llm-1 | themis | Audit conformite carte Janus: l utilisateur se demande si Janus a ete eduque et si sa carte est conforme (il a enumere les choses et suivi sa carte). Verifier: 1) version de la carte janus vs les cartes a jour (cerberus, vulcain, morpheus), 2) presence des garde-fous C1 (classification), c21/c22 (redirection outil bloque + agents habilites) comme la re-education de Themis v0.4.10, 3) coherence carte/fiche, 4) historique des educations de Janus (corrections.md + BDD lecons).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/themis/parcours/parcours-themis.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 19:12 | session-llm-1 | Cerberus | BILAN CONSOLIDE - garde-fou parite agents: test-092 cree par Morpheus (parite py/sh/AGENTS.md activer-agent-principal, preuve negative, normes) a DETECTE le vrai defaut (argus+gardien absents du .sh, signalement Janus jamais corrige depuis branchement-chiron), signale a Vulcain qui a corrige (bump 0.5.13, py/sh/md/spec + versionning). test-092 reverdi 9/9, tests lies 10/10, Themis audit CONFORME (rapport-audit-parite-agents-test092), Janus VERDICT VALIDE (controle-garde-fou-parite-agents). Bumper --tous 0/0, residus 0, evaluateur 0 ERREUR nouvelle, normes OK, JSONL 377/377. Le 3e oubli de branchement est desormais impossible a reproduire. |
| 2026-08-18 19:11 | session-llm-1 | janus | Controle fin de chaine garde-fou parite agents: test-092 cree (parite py/sh/AGENTS.md activer-agent-principal, preuve negative, normes) - a DETECTE le vrai defaut (argus+gardien absents du .sh, signalement Janus jamais corrige), signale a Vulcain qui a corrige (bump 0.5.13), test reverdi 9/9. Themis: audit CONFORME 0 defaut (rapport-audit-parite-agents-test092). Tests lies 10/10 OK, bumper --tous 0/0. A verifier: coherence test-092, parite complete py/sh/AGENTS.md, versions 0.5.13, normes, perimetre git (test-092 nouveau + 4 fichiers .sh/.py/.md/spec).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 19:10 | session-llm-1 | morpheus | Audit CONFORME (0 defaut) - rapport: cerveau-projet/agents/themis/rapports/rapport-audit-parite-agents-test092-2026-08-18.md. Verifie: parite .sh complete (argus/gardien 3 fonctions), test-092 9/9 OK, versions 0.5.13 coherentes, bumper --tous 0/0, normes ASCII/LF, perimetre propre, non-regression 10 tests verts. Reprends ta mission : continue ta carte jusqu a ta fin (controle Janus puis Cerberus).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 19:09 | session-llm-1 | themis | Audit fin de mission Morpheus: garde-fou test-092 cree (parite py/sh/AGENTS.md activer-agent-principal, preuve negative, normes), defaut detecte (argus+gardien absents du .sh) signale a Vulcain qui a corrige (bump 0.5.13). test-092 9/9 OK apres correction, tests lies 10/10 OK, bumper --tous 0 incoherent. Verifier: coherence test-092, parite complete, normes.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/themis/parcours/parcours-themis.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 19:08 | session-llm-1 | morpheus | Correction appliquee (parite sh complete): argus + gardien ajoutes aux 3 case statements du sh, bump 0.5.12 -> 0.5.13 (py/sh/md/spec + entree versionning), test-092 9/9 OK, tests lies 10/10 OK, bumper --tous 0 incoherent, normes ASCII/LF OK, lecon + BDD. Re-verification de ton cote : relancer test-092 (vert) puis continuer ta carte (fin -> Janus -> Cerberus).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 19:02 | session-llm-1 | vulcain | CORRECTION OUTIL (signalement Morpheus, protocole : probleme detecte signale a l agent d origine) : le garde-fou test-092 (parite agents/activation) a DETECTE que le .sh de activer-agent-principal manque 'argus' et 'gardien' dans ses 3 fonctions (get_agent_role, get_agent_fiche, get_agent_corrections) - signalement Janus de la mission branchement-chiron JAMAIS corrige. Le .py les a (16 agents), le .sh n en a que 14. Mission : ajouter les case statements argus + gardien dans les 3 fonctions du .sh (modele chiron/hermes). Puis me RE-ACTIVER (Morpheus) : je relancerai test-092 (doit devenir 100% vert) puis j ACTIVERAI Janus.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 18:56 | session-llm-1 | morpheus | CREER LE GARDE-FOU DE PARITE AGENTS <-> DICTIONNAIRE AGENTS DE activer-agent-principal (recommandation Janus, controle branchement-chiron v0.5.12 : 2e oubli Argus v0.5.8 + Chiron v0.5.12, AUCUN test ne verifie cette parite, 3e oubli a eviter). Mission : ecrire un test-0XX (protocole-tests, template v0.4.0, protections) qui verifie que TOUT agent de AGENTS.md (liste des agents) est present dans le dictionnaire AGENTS du .py ET les case statements du .sh de activer-agent-principal (parite py/sh incluse), et reciproquement (pas d agent mort dans l outil). Le test doit detecter l oubli : simuler un agent absent de l outil -> KO. Puis ACTIVER Janus (controle) qui REACTIVE Cerberus avec le bilan consolide.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 18:54 | session-llm-1 | Cerberus | BILAN CONSOLIDE (dernier maillon Janus) : controle de la chaine Vulcain -> Themis -> Morpheus -> Buffy sur la modification de mettre-a-jour-versions v0.1.5 (resynchroniser_cartes_lock apres bump --parcours --wet, lecon 2026-08-18 cas themis v0.4.10). VERDICT : VALIDE. 1) Vulcain : code correct (empreinte LF+rstrip identique editer-parcours), bump 0.1.4->0.1.5. 2) Themis : audit CONFORME 0 defaut. 3) Morpheus : pins 0.1.5 adaptes (test-066 11/11, test-067 8/8), test-007 15/15, test-057 24/24 (marbre), test-005 28/28 sous janus. 4) Buffy : correction fiche vulcain (table P0 ajoutee, signalement Janus resolu), evaluateur 0 probleme, test-014 13/13. Verifs : bumper --tous 0/0, divergences 0, residus 0, ASCII/LF 0, JSONL 337/337, lock themis MATCH. Rapports : themis/rapports/rapport-audit-mettre-a-jour-versions-resync-2026-08-18.md + janus/controles/controle-mettre-a-jour-versions-resync-2026-08-18.md. AUTO-CORRECTIONS : 2 usages hors carte retires du registre (vulcain guider-parcours, morpheus tester). |
| 2026-08-18 18:54 | session-llm-1 | janus | RETOUR CORRECTION FICHE (boucle KO c9f) : table P0 ajoutee dans vulcain.md (modele morpheus.md : guider-parcours, lire-activite-recente + outils de base), regles ETAPE SYSTEME/SESSION conservees. Verifie : evaluer-processus 0 probleme, test-014 13/13 (refs guider-parcours v0.6.2 intactes), ASCII 0, LF pur. Lecon ajoutee (corrections.md + BDD). Je te laisse re-controler puis REACTIVER Cerberus avec le bilan consolide (dernier maillon).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 18:53 | session-llm-1 | buffy | CORRECTION FICHE (c9f Janus, regle 4 : je signale je ne corrige pas) : la fiche vulcain.md section '## Outils de base (P0)' est en PROSE sans tableau -> les P0 partages (guider-parcours, lire-activite-recente) ne sont pas reconnus par evaluer-processus pour vulcain (OUTIL_HORS_CARTE a tort, contrairement a morpheus qui a une table P0). Mission : ajouter la table P0 (modele morpheus.md : ,  + outils de base) dans vulcain.md. Rapport : janus/controles/controle-mettre-a-jour-versions-resync-2026-08-18.md. Puis me RE-ACTIVER (Janus) avec le bilan, je re-controle et je REACTIVE Cerberus (dernier maillon).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 18:49 | session-llm-1 | janus | CONTROLE (c10 Morpheus, chaine bout-en-bout) : verifier la chaine Vulcain -> Themis -> Morpheus sur la modification de mettre-a-jour-versions v0.1.5 (ajout resynchroniser_cartes_lock apres bump --parcours --wet, lecon 2026-08-18 cas themis v0.4.10). VERDICT TESTS : test-066 11/11, test-067 8/8 (pins 0.1.4 -> 0.1.5 adaptes, ligne 10 exemple historique preservee), test-007 15/15, test-057 24/24 (marbre/lock intacts), test-005 27/28 (1 KO = artefact de verrou valider-cartes-decision, reverdira sous toi). Audit Themis : CONFORME (rapport themis/rapports/rapport-audit-mettre-a-jour-versions-resync-2026-08-18.md). A verifier : versions 0.1.5 py+md, bumper --tous 0/0, lock themis MATCH, normes ASCII/LF, evaluer-coherence, registre usages, perimetre git.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 18:44 | session-llm-1 | morpheus | TESTS (c15 Vulcain, chaine bout-en-bout) : verifier la non-regression apres modification de mettre-a-jour-versions v0.1.5 (ajout resynchroniser_cartes_lock, audit Themis CONFORME). Points a adapter : test-066 et test-067 pinent encore v0.1.4 (8 + 11 occurrences) -> les mettre a jour vers v0.1.5. Verifier aussi qu aucun test ne casse (le resync ne touche que le mode --parcours --wet). Puis ACTIVER Janus (controle) qui REACTIVE Cerberus avec le bilan consolide.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 18:44 | session-llm-1 | vulcain | RETOUR AUDIT THEMIS (c25b) : audit-fin-mission CONFORME -- 0 defaut. Rapport : themis/rapports/rapport-audit-mettre-a-jour-versions-resync-2026-08-18.md. Verifications : code OK (resync normalisee identique editer-parcours), versions 0.1.5 coherentes (py+md+--version, bumper --tous 0/0), normes ASCII 0 / LF 0 / py_compile OK, preuve reelle (empreinte lock themis MATCH + test perturbation), perimetre propre (aucun test touche). Points : test-066/067 pinent 0.1.4 -> Morpheus les adaptera a la non-regression. Je reprends ma mission : reponse c15g OUI puis c15 (MORPHEUS ACTIVE).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 18:42 | session-llm-1 | themis | AUDIT-FIN-MISSION (c15f Vulcain, evaluation croisee) : auditer ma modification de mettre-a-jour-versions v0.1.5 (ajout resynchroniser_cartes_lock : empreinte normalisee LF+rstrip identique a editer-parcours, appelee apres chaque bump --parcours --wet, lecon 2026-08-18 cas themis v0.4.10). RVAV passe : ASCII 0, LF 0, py_compile OK, bumper --tous coherent 0/0. Outils utilises : guider-parcours, lire-fichier, mettre-a-jour-versions, ajouter-contenu-fichier, enregistrer-lecon, enregistrer-usage-outil, activer-agent-principal. Si aucun defaut : me RE-ACTIVER (c25b, commande activer) avec ton rapport ; si defaut : m'activer pour correction (c12f/c12g).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/themis/parcours/parcours-themis.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 18:30 | session-llm-1 | vulcain | AMELIORATION OUTIL (Pattern 17, deleguee par Buffy) : mettre-a-jour-versions --parcours ecrit la carte HORS editer-parcours -> cartes-lock.json diverge et bloque les ecritures suivantes. Mission : ajouter la resynchronisation de cartes-lock.json apres bump d'une carte (empreinte normalisee, modele proteger-modifier-marbre) + lecon + bump version. Buffy me reactivera : NON, je suis DERNIER maillon -> reactiver Cerberus avec le bilan.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 18:22 | session-llm-1 | buffy | RELIS TA FICHE PUIS TES CORRECTIONS avant de commencer. CORRIGER LA CARTE THEMIS

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 18:21 | session-llm-1 | janus | RELIS TA FICHE PUIS TES CORRECTIONS avant de commencer. CONTROLE REEDUCATION THEMIS

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 18:15 | session-llm-1 | chiron | RELIS TA FICHE PUIS TES CORRECTIONS avant de commencer. REEDUCATION DE THEMIS

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/chiron/parcours/parcours-chiron.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 18:15 | session-llm-1 | Cerberus | CONTROLE BRANCHEMENT CHIRON VALIDE - bilan consolide |
| 2026-08-18 18:11 | session-llm-1 | janus | RELIS TA FICHE PUIS TES CORRECTIONS avant de commencer. CONTROLE BRANCHEMENT CHIRON

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 18:09 | session-llm-1 | morpheus | RELIS TA FICHE PUIS TES CORRECTIONS avant de commencer. TESTER LE BRANCHEMENT CHIRON

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 18:08 | session-llm-1 | vulcain | RETOUR VULCAIN apres preuve de branchement chiron - poursuite mission

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 18:08 | session-llm-1 | chiron | TEST BRANCHEMENT CHIRON - verifier resolution

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/chiron/parcours/parcours-chiron.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 17:59 | session-llm-1 | vulcain | RELIS TA FICHE PUIS TES CORRECTIONS avant de commencer. BRANCHER CHIRON A L ACTIVATION

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 17:48 | session-llm-1 | Cerberus | BILAN CONSOLIDE (dernier maillon) - VERDICT VALIDE pour la chaine lire-head. CHAINE : Vulcain a cree l outil lire-head v0.1.1 (head auto sans configurer le nb de lignes : front-matter YAML / bloc commentaires / premiere ligne vide / borne --max-lignes, comparaison --info-commune PRESENT/ABSENT) + catalogue 181->182 (v0.2.13) + index-tools 202->203. Morpheus a cree test-091 (13/13) + adapte les pins (test-005/007/024/060/079) + serie e. Themis a audite (rapport audit-chaine-lire-head). Janus a controle : evaluer-processus 0 probleme (3 declarations fautives morpheus retirees du registre + OUTIL_HORS_CARTE generateurs-commande corrige par Buffy : indice c20/c21 carte morpheus + bump 0.4.15), boucles KO reverdies (test-004 pin 0.4.15, test-091 au profil outils, tag lecture taxonomie, residus tmp-morpheus + rapport-decalages nettoyes par Hygie, lecons janus+vulcain ajoutees test-048, marbre regles-groupes-agents restaure apres pollution preuve negative test-084), NON-REGRESSION FINALE 89 OK / 0 KO, marbre 8/8 conforme, workspace PROPRE, rapport controle-modification-lire-head-2026-08-18.md VERDICT VALIDE. OUTILS UTILISES (janus) : valider-cartes-decision, tester-lancer-non-regression (verrou-auto), evaluer-processus, detecter-residus, activer-agent-principal. SIGNALEMENT : (1) residu RECURRENT detecter-decalages-catalogue (rapport egare a la racine, 3e fois 08-13/08-14/08-18) - a corriger par Vulcain (ecrire le rapport dans un dossier dedie) ; (2) artefacts de course inter-sessions avec session-llm-2 (kilo-llm) observes (verrou identite, verrouillage registre-tests.jsonl) - non bloquants en fenetre propre, a surveiller si les 2 sessions tournent en parallele. |
| 2026-08-18 17:46 | session-llm-1 | janus | non-regression finale (2e tentative apres crash fichier)

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 17:44 | session-llm-1 | janus | relance non-regression (course inter-sessions avec session-llm-2/kilo-llm): refresh du timestamp pour le verrou d identite.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 17:43 | session-llm-2 | themis | Inventaire et audit des outils de performance (tests, fonction, worker, workflow, flux, round, session) : analyser l environnement de travail (OS, ressources, parallelisme) puis lister les outils necessaires et possibles pour ameliorer les performances, afin d etablir des configurations adaptables selon le systeme et les ressources disponibles

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/themis/parcours/parcours-themis.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 17:42 | session-llm-1 | janus | reprise de la non-regression finale apres restauration du fichier marbre pollue par test-084 (preuve negative): verrou marbre 8/8 conforme, test-068 9/9, test-084 11/11. Je relance la non-regression.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 17:41 | session-llm-2 | Cerberus | Identification LLM - demarrage de session |
| 2026-08-18 17:37 | session-llm-1 | janus | lecon ajoutee (boucle KO test-048 terminee): lecon de la mission lire-head (2026-08-18) ajoutee dans vulcain/corrections.md avec VERDICT VALIDE dans le titre, ASCII 0, LF pur, temp supprime. Je t active pour relancer la non-regression finale.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 17:36 | session-llm-1 | vulcain | lecon manquante (boucle KO test-048): la non-regression finale echoue sur test-048 point 5: ta mission du 2026-08-18 08:22 (creation de lire-head) n a AUCUNE lecon datee du jour avec verdict dans vulcain/corrections.md (les lecons s arretent au 2026-08-17). TACHE: ajouter TA lecon de la mission lire-head (creation de l outil, bump versions, delegation tests a Morpheus) dans vulcain/corrections.md avec UN MOT DE VERDICT (VERDICT/VALIDE/CONFORME...) dans le texte (test-048 le verifie), verifier ASCII + LF, puis me REACTIVER (commande activer janus) pour relancer la non-regression. Garde-fou: relis TA fiche et TES corrections avant d'agir.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 17:32 | session-llm-1 | janus | nettoyage termine (boucle KO): 2 residus supprimes avec tracabilite - tmp-morpheus/ (TEMP, consultation pre-mission) + rapport-detecter-decalages-catalogue-2026-08-18.md (RAPPORT_EGARE racine). OUTILS UTILISES (bilan): snapshot-nettoyage (creer+consulter+rotation, 5797 fichiers), detecter-residus (2 residus -> PROPRE apres), supprimer-dossier --agent hygie --force, supprimer-fichier --agent hygie, creer-fichier (rapport nettoyage-2026-08-18-1731.md), ajouter-contenu-fichier (lecon), enregistrer-usage-outil (5 usages). VERIFIE: detecter-residus PROPRE (0 residu), ASCII 0. LECON: residu RECURRENT detecter-decalages-catalogue (3e fois: 08-13/08-14/08-18) - comportement d outil a corriger par Vulcain (rapport ecrit a la racine). Je t active pour relancer la non-regression.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 17:31 | session-llm-1 | hygie | nettoyage de residus (boucle KO non-regression): la non-regression (serie E) echoue sur test-024 point 2b: dossier tmp-* residuel a la racine. RESIDUS A NETTOYER: (1) tmp-morpheus/ a la racine (contient consultation-pre-mission.md, residu de la consultation pre-mission Morpheus); (2) rapport-detecter-decalages-catalogue-2026-08-18.md a la racine (residu de detecter-decalages-catalogue, deja signale par Themis/Janus). TACHE: supprimer ces residus (ton domaine exclusif), verifier 0 residu (test-024 point 2b vert si pertinent), puis me REACTIVER (commande activer janus) pour relancer la non-regression. Garde-fou: relis TA fiche et TES corrections avant d'agir.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/hygie/parcours/parcours-hygie.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 17:31 | session-llm-1 | janus | taxonomie corrigee (boucle KO): tag 'lecture' ajoute a la categorie 'outils' de categories-tests.json (domaine lire/ legitime). VERIFIE: test-087 8/8 OK (0 KO), JSON valide, ASCII 0, LF pur. RESTE (domaine hygie): residu tmp-morpheus/ a la racine (test-024 point 2b KO) + rapport-detecter-decalages-catalogue-2026-08-18.md - a nettoyer par Hygie. Je t active pour la suite de la non-regression.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 17:30 | session-llm-1 | morpheus | correction taxonomie tags (boucle KO non-regression): serie E test-087-categories-tags point 3 KO: 88 tags autorises -- ['test-091-lire-head-garde-fou.py:lecture']. test-091 porte Tags: outils, lecture, garde-fou, preuve-negative -- le tag 'lecture' est ABSENT de la taxonomie categories-tests.json (categories: securite/conventions/agents/outils/registre-traces/performance/anti-recurrence). TACHE: soit ajouter 'lecture' aux tags autorises (categorie 'outils' par exemple, domaine lire/ legitime), soit adapter le tag de test-091 vers un tag existant. VERIFIER: test-087 100% vert, JSON valide, ASCII/LF, puis me REACTIVER (commande activer janus) pour relancer la non-regression. Garde-fou: relis TA fiche et TES corrections avant d'agir.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 17:29 | session-llm-1 | janus | orphelin profils corrige (boucle KO terminee): test-091 ajoute au profil 'outils' de profils-tests.json (apres test-090, ordre alphabetique). VERIFIE: JSON valide, test-063 11/11 (point 5 couverture vert, 0 orphelin), ASCII 0, LF pur. Test-085 notifie: KO transitoire lors du premier run (processus residuel du parallelisme, passe 8/8 individuellement) - a re-verifier dans la non-regression. Je t active pour relancer la non-regression complete.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 17:29 | session-llm-1 | morpheus | correction orphelin profils (boucle KO non-regression): la non-regression (barriere A) revele test-063 point 5 KO: orphelins=test-091 (test-091-lire-head-garde-fou ajoute en serie e mais absent de profils-tests.json). TACHE: ajouter test-091 au profil approprie de cerveau-projet/agents/tools/tester/tester-lancer-non-regression/profils-tests.json (profil 'outils' probablement, a juger par la semantique des profils - tout test reel doit etre couvert par au moins un profil), verifier test-063 11/11 (point 5 couverture vert), ASCII/LF, puis me REACTIVER (commande activer janus) avec ton bilan pour relancer la non-regression. Garde-fou: relis TA fiche et TES corrections avant d'agir.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 17:27 | session-llm-1 | janus | pins adaptes (boucle KO terminee): test-004 point 7a + docstring adaptes 0.4.14 -> 0.4.15 (seul test pinant le parcours morpheus). VERIFIE: test-004 15/16 (KO point 8 = artefact verrou valider-cartes-decision bloque pour morpheus, agents habilites janus/argus/buffy/vulcain -> vert sous toi), test-016 NON IMPACTE (il pinne le parcours BUFFY 0.4.14 inchange) : mon adaptation initiale etait fausse, REVERTEE a l identique (git diff vide, 20/20 vert). NORMES: ASCII 0, LF pur sur test-004. LECON ajoutee dans morpheus/corrections.md (piege faux positif grep: verifier la constante PARCOURS du test avant d adapter). Je t active pour la non-regression complete et le verdict.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 17:26 | session-llm-1 | morpheus | adaptation de pins de tests (boucle KO apres correction carte): la correction Buffy a bumpe le parcours morpheus 0.4.14 -> 0.4.15 (ajout indice generateurs-commande c20/c21). IMPACT TESTS (domaine morpheus): (1) test-004-combos-tester-outil point 7a ligne 203 + docstring ligne 19 pinent 0.4.14 -> attendent 0.4.15; (2) test-016-migration-buffy point 1 lignes 171-172 + docstring ligne 32 pinent 0.4.14 -> attendent 0.4.15. Aucun autre test ne pinne cette version (test-029/033/059 referencent le contenu). TACHE: adapter les 2 tests (0.4.14 -> 0.4.15), executer test-004 et test-016 pour verifier 0 KO, verifier ASCII/LF, puis me REACTIVER (commande activer janus) avec ton bilan pour re-controle et non-regression complete. Garde-fou: relis TA fiche et TES corrections avant d'agir.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 17:25 | session-llm-1 | janus | correction appliquee (boucle KO): carte morpheus corrigee. OUTILS UTILISES (bilan): editer-parcours (modifier-case c20 + c21 + bump 0.4.14 -> 0.4.15, lock resynchronise), editer-fichier-agents (morpheus.md ligne 81 -> v0.4.15, Pattern 14), valider-case CONFORME (0 erreur), valider-cartes-decision 10/10 CONFORME, valider-conformite-ascii 0 (parcours + morpheus.md + corrections.md), ajouter-contenu-fichier (lecon buffy dans corrections.md), enregistrer-usage-outil (6 usages declares au registre). VERIFICATION: evaluer-processus = 0 probleme (OUTIL_HORS_CARTE generateurs-commande resolu). IMPACT A TRAITER PAR MORPHEUS (delegation tests): test-004 point 7a et test-016 point 1 pinent la version parcours morpheus 0.4.14 -> attendent desormais 0.4.15. Residu connu inchange: rapport-detecter-decalages-catalogue-2026-08-18.md (nettoyage Hygie). Je t active pour re-controle.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 17:22 | session-llm-1 | buffy | verrou editer-parcours: seul buffy habilite. Ecart carte morpheus detecte par l evaluateur (OUTIL_HORS_CARTE): l indice generateurs-commande est absent des cases c20/c21 du parcours morpheus alors que ses messages ordonnent via le generateur (PASSE PAR LE GENERATEUR) et que des usages reels sont declares au registre (2026-08-18 08:36). Correction: ajouter l indice outil generateurs-commande (nom/catalogue/chemin) en tete des indices de c20 et c21 via editer-parcours --modifier-case, bump version parcours 0.4.14 -> 0.4.15, mettre a jour la reference v0.4.14 ligne 81 de morpheus.md, lancer valider-case + verifier ASCII/LF. BOUCLE KO: Buffy corrige puis REACTIVE janus (commande activer) pour re-controle. Garde-fou: relis TA fiche et TES corrections avant d'agir.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 08:42 | session-llm-1 | janus | RELIS TA FICHE PUIS TES CORRECTIONS avant de commencer. MISSION JANUS : NON-REGRESSION COMPLETE + VERDICT FINAL pour la chaine lire-head. RECAPITULATIF : Vulcain a cree lire-head v0.1.1 (lire le head d un fichier sans configurer le nombre de lignes : detection auto front-matter YAML / bloc de commentaires / premiere ligne vide, comparaison --info-commune PRESENT/ABSENT). Catalogue 181 -> 182 (v0.2.12 -> 0.2.13), index-tools Total 202 -> 203 (Lire 4 -> 5). Morpheus a cree test-091 (13/13 OK) et adapte les pins : test-007 (182 + Total 203 + lire-head), test-024 (182 + lire-head), test-060 (182 + 203), test-079 (182 + 203 + lire-head), test-005 (version catalogue 0.2.13), test-040 (5/5). test-091 ajoute a la serie e du lanceur. Themis a audite : VERDICT CONFORME 96/100 (rapport themis/rapports/rapport-audit-chaine-lire-head-2026-08-18.md), 2 residus mineurs (rapport-detecter-decalages-catalogue-2026-08-18.md + tmp-morpheus/) a nettoyer par Hygie. ATTENTION : les tests 005 point 21 et 027 points 5-8 font KO quand executes en tant que Morpheus (artefacts de verrou d habilitation : valider-cartes-decision et tester-lancer-non-regression reserves a janus) - TOI, agent actif janus, tu es habilite : ils doivent passer. A FAIRE : lancer la non-regression complete, constater les KO eventuels, signaler (Morpheus pour les tests, Vulcain pour les outils), reverdir, puis REACTIVER CERBERUS avec le bilan consolide (dernier maillon).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 08:42 | session-llm-1 | morpheus | RELIS TA FICHE PUIS TES CORRECTIONS avant de continuer. RAPPORT THEMIS RECU (audit chaine lire-head) : VERDICT CONFORME 96/100. Outil lire-head v0.1.1 conforme (nommage lire-, ASCII 0, LF, catalogue 182 v0.2.13, index 203, versions alignees). Test-091 13/13 verifie independamment par Themis. Pins exacts. 2 residus mineurs a nettoyer par Hygie (rapport-detecter-decalages-catalogue + tmp-morpheus). Correction de chaine : Themis a reactive Cerberus par erreur au lieu de m activer (violation Pattern 8) - la chaine est relancee au maillon manquant. MA CARTE ORDONNE : activer JANUS pour la non-regression complete et le verdict final (seul Janus lance la suite).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 08:41 | session-llm-1 | Cerberus | RAPPORT THEMIS : AUDIT CHAINE LIRE-HEAD VERDICT CONFORME (96/100). Outil lire-head v0.1.1 conforme (nommage lire-, ASCII 0, LF, catalogue 182 v0.2.13, index 203, versions alignees). Test-091 13/13 verifie independamment (invariants + preuve negative + normes). Pins exacts (test-007/024/060/079, test-005, test-040 5/5). 2 residus mineurs a nettoyer par Hygie : rapport-detecter-decalages-catalogue-2026-08-18.md + tmp-morpheus. KO observes en cours de route = artefacts de verrou (valider-cartes-decision reserve a Janus), reverdiront avec Janus. Rapport complet : themis/rapports/rapport-audit-chaine-lire-head-2026-08-18.md. RELIS TA FICHE PUIS TES CORRECTIONS puis poursuis : ta carte ordonne d activer JANUS pour la non-regression complete et le verdict final. |
| 2026-08-18 08:37 | session-llm-1 | themis | RELIS TA FICHE PUIS TES CORRECTIONS avant de commencer. MISSION THEMIS : AUDIT DE LA CHAINE LIRE-HEAD. Vulcain a cree l outil lire-head v0.1.1 (lire le head d un fichier sans configurer le nombre de lignes : detection auto front-matter YAML / bloc de commentaires / premiere ligne vide, comparaison multi-fichiers --info-commune PRESENT/ABSENT). Morpheus a cree le garde-fou test-091 (13/13 OK) et adapte les pins catalogue (test-007/024/060/079 : 181->182 + Total 202->203, test-005 : version 0.2.12->0.2.13). A AUDITER : 1) l outil lire-head est-il conforme (nommage lire-, ASCII, LF, doc, catalogue, index-tools) ? 2) le test-091 couvre-t-il les invariants (detection, comparaison, preuve negative, normes) ? 3) les pins sont-ils corrects et coherents ? 4) evaluer la chaine Vulcain -> Morpheus. FIN : rapport dans ton dossier puis REACTIVER MORPHEUS (c25b).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/themis/parcours/parcours-themis.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 08:31 | session-llm-1 | morpheus | RELIS TA FICHE PUIS TES CORRECTIONS avant de commencer. MISSION MORPHEUS : TESTS POUR L OUTIL LIRE-HEAD. Vulcain a cree lire-head v0.1.1 (categorie lire) : lire le head d un fichier sans configurer le nombre de lignes (detection automatique de la fin : front-matter YAML, bloc de commentaires, ou premiere ligne vide, borne --max-lignes 100) et comparer plusieurs heads avec --info-commune MOTIF (PRESENT/ABSENT par fichier pour reperer celui qui n est pas a jour). A FAIRE : 1) ADAPTER LES PINS : test-007 (catalogue 181 -> 182, index-tools total 202 -> 203) et test-005 (version catalogue 0.2.12 -> 0.2.13). 2) CREER le test pour lire-head : detection front-matter (ex: un .md a identite), detection bloc de commentaires (ex: un .py), detection premiere ligne vide, --lignes force, comparaison multi-fichiers avec --info-commune present et absent (preuve negative : un fichier sans l info = ABSENT), fichier introuvable code 1, --dry-run, --version, parite .sh, normes ASCII + LF. 3) AJOUTER le test a la definition SERIES du lanceur. 4) py_compile + tests cibles verts. FIN : lecon Morpheus + ACTIVER JANUS (non-regression complete + verdict).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 08:22 | session-llm-1 | vulcain | RELIS TA FICHE PUIS TES CORRECTIONS avant de commencer. Mission : creer un outil dedie aux head des fichiers : lire le debut de n importe quel fichier du projet sans configurer le nombre de lignes en reperant automatiquement la fin du head, et comparer plusieurs head pour reperer les fichiers pas a jour.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 08:20 | session-llm-1 | cerberus | Identification LLM - demarrage de session |
| 2026-08-18 08:13 | session-llm-1 | cerberus | BILAN CONSOLIDE (Janus, preuve pollinisation croisee) : VERDICT VALIDE. Preuve reelle obtenue : Morpheus a consulte la BDD des lecons AVANT d agir (case c0e) et a lu la lecon de vulcain 'BDD lecons = memoire longue' (domaine outil) - pollinisation croisee reelle. Traces verifiees : registre (consulter-lecons 08:10:39 mode direct + verrou-auto, enregistrer-lecon 08:11:01 verrou-auto), BDD 2 lecons (vulcain outil + morpheus test), rapport tmp-morpheus/consultation-pre-mission.md, test-006 19/19 OK, normes 0/0. La chaine c0e -> consultation -> mission -> lecon -> transmission fonctionne de bout en bout dans le meme round. |
| 2026-08-18 08:11 | session-llm-1 | janus | CONTROLE DE LA PREUVE POLLINISATION CROISEE (mission micro Morpheus) : verifier 1) les traces registre : consulter-lecons journalise (controle d activite) + enregistrer-lecon journalise, 2) la BDD contient 2 lecons (vulcain outil + morpheus test), 3) le rapport tmp-morpheus/consultation-pre-mission.md existe, 4) test-006 19/19 OK (deja verifie par Morpheus), 5) normes corrections.md 0/0. Verdict attendu : VALIDE. Fin : reactiver Cerberus avec le bilan consolide de la preuve.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 08:10 | session-llm-1 | morpheus | PREUVE REELLE DE POLLINISATION CROISEE : mission micro de test. 1) AU DEMARRAGE (case c0e) : consulter la BDD des lecons AVANT d agir : python3 cerveau-projet/agents/tools/consulter/consulter-lecons/consulter-lecons.py --agent morpheus --domaine outil --toutes --rapport tmp-morpheus/consultation-pre-mission.md - afficher ce que tu trouves (attendu : la lecon de vulcain 'BDD lecons = memoire longue'). 2) MISSION : verifier que test-006-cartographier-parcours est toujours vert (19/19) apres le round c0e. 3) LECON : enregistrer-lecon (domaine test) + corrections.md. 4) FIN (ta carte) : activer Janus pour le controle des traces (registre : consulter-lecons + enregistrer-lecon journalises).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 08:07 | session-llm-1 | cerberus | BILAN CONSOLIDE (Janus, round consultation pre-mission) : NON-REGRESSION 88 OK / 0 KO (87 tests, chrono 53.1s, +4% vs reference conforme). Livre : case c0e (consulter-lecons sur le domaine de la mission) inseree dans les 15 cartes (cerberus via porte du marbre autorisee), 15 fiches synchronisees, valider-cartes-decision v0.4.5 (regle c0b OUI -> c0e -> c0c), tests adaptes : test-004/005/013/016 (pins versions), test-072 (c0e), test-071 (titre consulter = lecture), test-067 (bumper : .sh 0.4.5), test-006 (atlas 49 cases). Lecons : Buffy (porte marbre pour case protegee), Morpheus (test-006 pinne atlas). 0 residu, ko-tests vide, normes 0/0. |
| 2026-08-18 08:06 | session-llm-1 | janus | RELANCER LA NON-REGRESSION COMPLETE (relance finale round consultation pre-mission) : test-006 adapte par Morpheus (49 cases atlas). Les KO precedents (test-071, test-067, test-006) sont corriges. Lancer la suite complete et si 100% vert, reactiver Cerberus avec le bilan consolide du round (c0e dans 15 cartes + fiches + valider-cartes 0.4.5 + 4 tests adaptes).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 08:04 | session-llm-1 | morpheus | ADAPTER TEST-006 APRES AJOUT C0E (consultation pre-mission) : le test-006-cartographier-parcours pinne en dur les compteurs d atlas (48 cases, 13 chemins) mais la carte atlas a maintenant 49 cases (c0e ajoute) pour 13 chemins. CORRIGER : ligne 15 docstring (48 -> 49 cases) et ligne 176 (Nombre de cases | 48 | -> | 49 |). VERIFIER ensuite test-006 vert puis reactiver Janus pour la relance finale de la non-regression. NE PAS toucher aux autres fichiers.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 07:57 | session-llm-1 | janus | RELANCE FINALE NON-REGRESSION : round consultation pre-mission (c0e dans les 15 cartes + valider-cartes 0.4.5). Morpheus a adapte test-004 (morpheus 0.4.14), test-005 (atlas 0.4.9 + 12 commandes + c0e), test-013 (cerberus 0.5.4 + 24 actions), test-016 (buffy 0.4.14 + 41 actions), test-072 (c0b OUI->c0e->c0c). Janus lance la suite complete en barrieres, puis REACTIVE Cerberus avec le bilan consolide.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 07:53 | session-llm-1 | morpheus | MISSION MORPHEUS : adapter les pins de version apres le round consultation pre-mission. Buffy a insere la case c0e dans les 15 cartes (bump : cerberus 0.5.4, buffy 0.4.14, vulcain 0.4.28, morpheus 0.4.14, janus 0.4.20, atlas 0.4.9, clio 0.5.13, themis 0.4.9, hygie 0.1.8, hermes 0.1.5, argus 0.1.12, chiron 0.1.2, athena 0.3.6, promethee 0.3.7, minerve 0.3.7) + valider-cartes-decision 0.4.4->0.4.5. ADAPTER les tests qui pinent ces versions (test-004/005/013/016/018/063...) + test-005 point 18 (atlas commandes en dur : c0e ajoute consulter-lecons -> 11->12, liste + c0e). Verifier aussi test-072 (c0/c0b) et test-070 (anti-auto-reactivation). PUIS reactiver Janus pour la non-regression complete.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 07:42 | session-llm-1 | buffy | MISSION BUFFY (demande utilisateur) : AJOUTER LE DECLENCHEUR DE CONSULTATION PRE-MISSION dans les 15 cartes. Inserer une case c0e (action) apres c0b : c0b OUI -> c0e -> c0c, avec indices [ref protocole-lecons, outil consulter-lecons --agent <MOI> --domaine <domaine de ma mission>]. Via editer-parcours --inserer-case + --branche c0b OUI:c0e + --bump (15 cartes). PUIS synchroniser les 15 fiches (Pattern 14) + verifier valider-cartes 16/16 + budget pondere + normes. PUIS reactiver Janus (non-regression) qui reactivera Cerberus.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 07:21 | session-llm-1 | Cerberus | BILAN CONSOLIDE (Janus, round BDD des lecons) : NON-REGRESSION 88 OK / 0 KO (87 tests). Livre : lecons.db SQLite unique partagee (memoire longue) + enregistrer-lecon + consulter-lecons (verrou P0 partages, anti-usurpation, journalisation), regle immuable BDD lecons gravee au marbre (porte + audit Argus PROPRE), protocole-lecons, corrections.md = memoire courte. KO traites : test-038 (badge README 157->159 + readme-dev 149/35 -> 159/38 par Clio), test-035 (2 outils ajoutes aux 13 cartes + 15 fiches P0 par Buffy), test-024 (catalogue 179->181), test-004/005/016 (pins versions), test-045 (budget pondere allege). valider-cartes 16/16, marbre 8/8, 0 residu, normes 0/0, chrono 50.9s. Lecons Buffy/Morpheus/Clio enregistrees. |
| 2026-08-18 07:17 | session-llm-1 | janus | RELANCE FINALE NON-REGRESSION : Buffy a allege les 6 cases Lecons au budget pondere (hygie c12 CONFORME -> test-045 point 2 regle). Janus relance la suite complete en barrieres pour confirmer 87/87, puis REACTIVE Cerberus avec le bilan consolide du round BDD des lecons.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 07:15 | session-llm-1 | buffy | MISSION BUFFY (Janus, KO test-045) : l ajout des indices lecons a pousse 6 cases Lecons au-dessus du budget pondere 3.0 (valider-case A ALLEGER -> test-045 KO). ALLEGER : retirer les refs redondantes (pattern-12/pattern-2, precedents etablis) + convertir les textes regle >100 car en refs protocole-fin-mission (vulcain c15h, morpheus c8, janus c9, clio c10, themis c12, hygie c12) via editer-parcours. PUIS reactiver Janus.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 07:08 | session-llm-1 | janus | RELANCE NON-REGRESSION (maillon suivant) : Morpheus a adapte test-004 (morpheus 0.4.13), test-005 (atlas 0.4.8 + 11 commandes), test-016 (buffy 0.4.13 + max 5 indices), test-024 (catalogue 181). Janus relance la suite complete en barrieres pour confirmer 87/87, puis REACTIVE Cerberus avec le bilan consolide du round BDD des lecons.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 07:03 | session-llm-1 | morpheus | MISSION MORPHEUS (Janus, KO non-regression) : Buffy a ajoute enregistrer-lecon + consulter-lecons aux cases Lecons des 13 cartes (bump versions : buffy 0.4.13, vulcain 0.4.27, morpheus 0.4.13, janus 0.4.19, atlas 0.4.8, clio 0.5.12, themis 0.4.8, hygie 0.1.7, hermes 0.1.4, chiron 0.1.1, athena 0.3.5, promethee 0.3.6, minerve 0.3.6). ADAPTER les tests qui pinent ces versions (test-004/005/013/016/018/063...) + CORRIGER test-024 pin catalogue 179->181. PUIS reactiver Janus pour relancer la non-regression.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 06:57 | session-llm-1 | buffy | MISSION BUFFY (Janus, KO test-035) : les outils enregistrer-lecon + consulter-lecons (nouveaux P0 partages, round BDD lecons) sont absents des cartes et fiches -> OUTIL_HORS_CARTE pour janus. CORRIGER : (1) ajouter les 2 indices outil (enregistrer-lecon + consulter-lecons) a la case Lecons de CHAQUE carte (14 cartes : buffy c15, vulcain c15h, morpheus c8, janus c9, atlas c10, clio c10, themis c12, hygie c12, hermes c9, chiron c12, athena c9, promethee c9, minerve c9 + chercher cerberus) via editer-parcours --modifier-case + bump, (2) ajouter les 2 outils aux tables P0 des 15 fiches, (3) verifier valider-cartes + normes. PUIS reactiver Janus.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 06:52 | session-llm-1 | janus | RELANCE NON-REGRESSION (maillon suivant) : Clio a corrige le KO test-038 (badge README 157->159 + readme-dev 149/35 -> 159/38). Janus relance la suite complete pour confirmer 87/87, puis REACTIVE Cerberus avec le bilan consolide du round BDD des lecons.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-18 06:52 | session-llm-1 | Cerberus | CORRECTION CLIO TERMINEE : badge README 157->159 (affichage + href), readme-dev 149/35 -> 159/38 (table categories maj : Enregistrer 2, Consulter 1, Configurer 1, Analyser 9, Detecter 19, Rechercher 11). test-038 7/7 OK, normes 0/0. Lecon Clio enregistree. Relance de la non-regression par Janus. |
| 2026-08-18 06:51 | session-llm-1 | clio | MISSION CLIO (Janus, KO non-regression) : le badge Outils du README affiche 157 alors que le compte reel est 159 (2 nouveaux outils : enregistrer-lecon + consulter-lecons, round BDD des lecons). CORRIGER : (1) badge README.md ligne 9 : Outils-157 -> Outils-159 (affichage + href), (2) readme-dev.md : total 149 outils/35 categories -> 159 outils/38 categories (ligne 28, 57, 218) + table des categories (Enregistrer 1->2 avec enregistrer-lecon, ajouter ligne Consulter 1 consulter-lecons, detecter 17->19, rechercher 10->11, etc. via combos-analyse-projet source de verite), (3) verifier test-038 vert + normes ASCII/LF. PUIS reactiver Janus pour relancer la non-regression.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/clio/parcours/parcours-clio.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 22:37 | session-llm-1 | janus | LANCER LA NON-REGRESSION COMPLETE (round BDD des lecons). Vulcain a cree lecons.db + enregistrer-lecon + consulter-lecons (+ catalogue 179->181 v0.2.12, index-tools 200->202), Buffy a grave la regle, Morpheus a adapte test-007/test-005 + cree test-090 (serie e). Janus lance la suite complete, constate les KO eventuels, les signale (Morpheus pour les tests, Vulcain pour les outils), reverdit, puis REACTIVE Cerberus avec le bilan consolide.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/janus/parcours/parcours-janus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 22:32 | session-llm-1 | morpheus | MISSION MORPHEUS : TESTS POUR LA BDD DES LECONS. Vulcain a cree lecons.db SQLite + enregistrer-lecon (anti-usurpation, verrou, ASCII, anti-doublon) + consulter-lecons (verrou, filtres, journalisation). Buffy a grave la regle. A FAIRE : 1) ADAPTER LES PINS : test-007 point 13 (catalogue 179 -> 181) + point 14 (index-tools total 200 -> 202) ; test-005 point 14 (catalogue version 0.2.11 -> 0.2.12). 2) CREER test-090 (garde-fou BDD lecons) : verifie enregistrer-lecon (creation OK, anti-usurpation code 1, non-ASCII refuse code 1, doublon refuse code 1) + consulter-lecons (liste, filtre --domaine/--recherche, --rapport, journalisation directe) + la BDD n est touchee que par les 2 outils. Avec preuve negative. Tags de la taxonomie. 3) AJOUTER test-090 a la definition SERIES du lanceur. 4) py_compile + tests cibles verts. FIN : lecon Morpheus + ACTIVER JANUS (non-regression complete + verdict). NOTE : la migration des lecons existantes (corrections.md -> BDD) est DEFEREE (a un round suivant, besoin d un mode import en masse).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/morpheus/parcours/parcours-morpheus.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 22:29 | session-llm-1 | buffy | MISSION BUFFY : GOUVERNER LA BDD DES LECONS (Vulcain a cree lecons.db SQLite + enregistrer-lecon + consulter-lecons, verrou P0 partages deja en place). A FAIRE : 1) AJOUTER LA REGLE dans regles-groupes-agents.md (niveau regle immuable) : la BDD lecons (cerveau-projet/agents/lecons/lecons.db, SQLite unique partagee) est la MEMOIRE LONGUE des lecons ; corrections.md reste la MEMOIRE COURTE (fenetre glissante des missions proches) ; CHAQUE AGENT N ECRIT QUE SES PROPRES LECONS via enregistrer-lecon (anti-usurpation --agent == agent actif) ; la LECTURE croisee via consulter-lecons est verrouillee + journalisee (controle d activite) ; la BDD n est touchee QUE par ces 2 outils (jamais sqlite3 direct). Si la regle releve du MARBRE (zone protegee), passer par Gardien + validation utilisateur (ne pas modifier en dur sans la porte). 2) METTRE A JOUR les fiches des agents (au minimum le template/les fiches principales) pour referencer enregistrer-lecon/consulter-lecons a la place de la seule append corrections.md. 3) Documenter la fenetre glissante corrections.md (N lecons recentes, le reste en BDD). VERIFIER : normes 0 non-ASCII / 0 CRLF, valider-cartes si cartes touchees. FIN : lecon Buffy + ACTIVER HYGIE (migration des lecons existantes corrections.md -> BDD + elagage corrections.md).

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/buffy/parcours/parcours-buffy.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
| 2026-08-17 22:21 | session-llm-1 | vulcain | MISSION VULCAIN : CREER LA BDD PORTABLE DES LECONS (SQLite) + 2 OUTILS DEDIES. DECISIONS UTILISATEUR : SQLite stdlib (aucune lib tierce), BDD UNIQUE partagee, v1 = stockage + consultation (pas de suggestion). 

1. BDD : cerveau-projet/agents/lecons/lecons.db (fichier unique, portable). Schema auto-init (CREATE TABLE IF NOT EXISTS, idempotent) : table lecons(id INTEGER PK AUTOINCREMENT, date TEXT, agent TEXT, domaine TEXT, tags TEXT, titre TEXT, lecon TEXT, mission TEXT, outils TEXT, verdict TEXT) + index sur agent/date/domaine. La BDD n est touchee QUE par les 2 outils (jamais sqlite3 direct ailleurs).

2. OUTIL enregistrer-lecon (categorie enregistrer) : --agent (obligatoire = auteur), --domaine, --tags, --titre, --lecon (ou --lecon-fichier), --mission, --outils, --verdict, --version, --aide. VERROU : appeler verrouiller_habilitation(agent_actif, 'enregistrer-lecon') + REGLE SPECIFIQUE anti-usurpation : le --agent (auteur) DOIT etre l agent actif de la session (lire AGENTS.md), sinon REFUS code 1. ASCII strict (refus si non-ASCII), LF, anti-doublon (meme agent+titre+date deja present -> signaler). Journalisation registre (mode direct). Retourne l id cree + confirmation.

3. OUTIL consulter-lecons (categorie consulter) : --agent (obligatoire pour verrou), --toutes, --auteur, --domaine, --tags, --recent N, --recherche (LIKE), --rapport (markdown), --version, --aide. VERROU : verrouiller_habilitation(agent_actif, 'consulter-lecons') puis JOURNALISATION D ACTIVITE (qui a consulte quoi, registre mode direct). Sortie liste formatee + compteur. ASCII strict, LF.

4. Doc .md pour chaque outil + entree catalogue-commandes + entree index-tools (categories enregistrer/consulter). Modele outil-template (shebang, coding ascii, docstring Usage, --aide, protections ON/OFF + chrono).

5. TESTS REELS : enregistrer-lecon creation OK (id retourne) + refus non-ASCII + refus usurpation (--agent != agent actif) + doublon detecte ; consulter-lecons liste + filtre --domaine + --recherche + --rapport ; --version/--aide ; normes 0 non-ASCII / 0 CRLF sur tous les fichiers crees.

FIN : lecon Vulcain + ACTIVER BUFFY (regle immuable + verrou table + fiches/cartes). PAS de script temporaire a la racine (entonnoir obligatoire), declaration registre, ASCII strict + LF partout.

DEMARRAGE OBLIGATOIRE (v0.5.5) : lance ta mission depuis la case c0 avec :
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \n  cerveau-projet/agents/vulcain/parcours/parcours-vulcain.json --case c0
(c0 = RELIRE OBLIGATOIRE : lis tes corrections puis ta fiche, puis reponds
a la confirmation c0b : OUI si tu as lu et compris, NON pour relire ; suis
ensuite les branches case par case ; si tu reprends apres une interruption,
reprends a la case courante avec --case <cid> --reponses '<reponse>'). |
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
