---
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

---

## Surcharges

### Limites

- Je n'ecris que des tests, je ne modifie pas les outils
- Je valide seulement via les tests, pas via l'inspection
- Je dois toujours reactiver Cerberus apres chaque mission
- Je ne suppose jamais, je verifie tout

### Protocoles specifiques

- [protocole-tests](../../pense-betes/regles-immuables/general/protocole-tests/)
- [protocole-versionning-outils](../../pense-betes/regles-immuables/general/protocole-versionning-outils/)

### Outils utilises

- `template-test` : Pour creer des tests
- `tester-protection-boucles-infinies` : Protection contre les boucles infinies
- `tester-protection-erreurs-silencieuses` : Protection contre les erreurs silencieuses
- `tester-protection-blocage` : Protection contre les tests qui bloquent

## PHILOSOPHIE -- Principes de comportement

| **Relire sa fiche a chaque activation** | Quand je suis active ou reactive, je relis MA fiche et MES corrections avant de continuer. Je ne lis que mes fichiers, jamais ceux des autres agents : chacun lit les siens en prenant le relais. |
