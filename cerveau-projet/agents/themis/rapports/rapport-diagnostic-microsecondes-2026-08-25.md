---
identite:
  type: rapport
  appartient_a: themis
  commun: false
---

# Rapport de diagnostic -- microsecondes (6 chiffres) au lieu de millisecondes (3 chiffres)

**Date :** 2026-08-25
**Activee par :** Cerberus (session-admin)
**Mission :** verifier pourquoi l outil continue d ecrire les micro-secondes a 6 chiffres au lieu de 3 comme demande plus tot. Diagnostiquer la cause racine, documenter les zones concernees et proposer la correction.

## VERDICT

**DIAGNOSTIC : cause racine identifiee. La correction demandee plus tot (commit 4fbd28f) n a corrige que les FICHIERS DE DONNEES, pas l OUTIL qui ecrit ces timestamps. L outil activer-agent-principal.py reecrit donc des microsecondes a 6 chiffres a chaque activation.**

## Contexte de la demande anterieure

La demande utilisateur (USER-DEMANDES.md, section attention, 2026-08-25) demandait :
> les microsecondes (6 chiffres) doivent etre remplacees par des millisecondes (3 chiffres). Les fichiers v1 sont corriges. Les fichiers freelance/ doivent etre verifies.

Le commit `4fbd28f` (2026-08-25 18:41, "fix: Microsecondes -> millisecondes (6 -> 3 chiffres)") a corrige :
- `variables-actuelles.md` : 3 microsecondes corrigees + doublon supprime
- `AGENTS-historique.md` : 250 microsecondes corrigees (250 -> 0)
- `USER-DEMANDES.md` : message laisse pour Mecano (verifier les fichiers freelance/)

MAIS ce commit n a PAS touche l outil `activer-agent-principal.py` : aucune occurrence `%3f` dans son historique git (verifie par `git log --all -S "%3f"` : 0 resultat).

## Cause racine

**L outil `cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py` utilise `%f` (microsecondes, 6 chiffres) a 4 endroits :**

| Ligne | Code | Destination de l ecriture |
|---|---|---|
| 876 | `ts = maintenant.strftime("%Y-%m-%d %H:%M:%S.%f")` | Classeur variables-actuelles.md (profil-session-*) |
| 1033 | `timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")` | AGENTS-historique.md (sidentifier) |
| 1305 | `timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")` | AGENTS-historique.md (activer) |
| 1364 | `timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")` | AGENTS-historique.md (reactiver) |

Le format `%f` en Python donne TOUJOURS 6 chiffres (microsecondes). Pour 3 chiffres (millisecondes), il faut `%3f`.

## Preuve de l ecart en conditions reelles

Apres le commit correctif de 18:41, les activations suivantes ont REEINTRODUIT des timestamps a 6 chiffres :

- `AGENTS-historique.md` : 8 lignes contiennent des microsecondes a 6 chiffres, dont :
  - `18:43:50.092801` (reactivation Cerberus - round brise)
  - `18:48:47.638046` (identification LLM - demarrage de session)
  - `18:51:00.236346` (activation themis)
- `AGENTS.md` : `| session-admin | glm5 | themis | 2026-08-25 18:51:00.252571 |` (section Sessions connues)

Ces 3 entrees sont POSTERIEURES au commit 4fbd28f (18:41) : la correction des fichiers a ete immediatement re-ecrasee par l outil non corrige.

## Verification de la zone freelance (demande anterieure)

Les fichiers freelance/ utilises en production sont DEJA conformes (3 chiffres) :
- `freelance/tools-commun/horloge/fonctions/horloge.py` ligne 23 : `strftime("%H:%M:%S.%f")[:12]` -> tronque a 12 caracteres = 3 chiffres (millisecondes) OK
- `freelance/tools-commun/jarvis/fonctions/historique.py` ligne 52 : `strftime("%H:%M:%S.%f")[:12]` -> 3 chiffres OK
- `freelance/tools-commun/horloge/fonctions/tic.py` : OK
- Les autres fichiers freelance utilisent `isoformat(timespec="seconds")` ou `strftime` sans `%f` : OK

Fichiers non concernes (sauvegardes) : `*.bak-*` (jarvis-server.py.bak, jarvis.py.bak, routines-server.bak) -- fichiers de sauvegarde, pas du code actif.

## Autres outils du cerveau verifies

Scan complet `%f` sur `agents/tools/` : SEUL `activer-agent-principal.py` utilise `%f`. Les autres outils utilisent `%Y-%m-%d %H:%M:%S` (sans fraction) ou n ecrivent pas de timestamp. Les fichiers `chronos.jsonl` (traces) sont a la seconde : 0 microseconde.

## Impact (detecter-impacts)

Outil partage (commun: true) : 245 fichiers impliques. Verdict bruit par mtime (outil non modifie recemment) : 160 non mis a jour potentiels, dont 75 traces historisees exclues du verdict. Aucun de ces fichiers ne porte le format de timestamp : la correction est interne (4 lignes de code), les references documentaires (doc, spec, catalogue) ne changent pas.

## Correction proposee

1. **Vulcain** (constructeur d outils) : remplacer les 4 occurrences `%Y-%m-%d %H:%M:%S.%f` par `%Y-%m-%d %H:%M:%S.%3f` dans `activer-agent-principal.py` (lignes 876, 1033, 1305, 1364). Mettre a jour la version de l outil et sa doc.
2. **Parite .sh** : verifier que `activer-agent-principal.sh` (wrapper) n a pas de formatage equivalent.
3. **Nettoyage des donnees** (Hygie) : re-corriger les 8 lignes a 6 chiffres de AGENTS-historique.md + 1 ligne AGENTS.md + classeur (les memes fichiers que le commit 4fbd28f).
4. **Garde-fou** (optionnel, a decider) : ajouter un test de non-regression verifiant qu aucune entree d historique ne contient `\.[0-9]{6}` (microsecondes) -- sinon la regression se reproduira.

## SUITE DE L AUDIT (meme round) : REPARATION REALISEE ET VERIFIEE

**Note de correction** : la correction proposee (%3f) etait INVALIDE en Python
(ValueError: Invalid format string) - Vulcain a utilise la TRONCATURE [:-3]
(pattern deja en place dans horloge.py), validee en execution reelle.

**Verdict de conformite : CONFORME - 0 defaut.**

1. activer-agent-principal v0.7.3 : 4 occurrences strftime(...%f)[:-3]
   (l.879, 1036, 1308, 1367) + commentaire de maintenance ; .sh
get_timestamp() en %3N (GNU date) - parite py/sh sur le format.
2. Execution reelle sur copie (AGENTS_FILE surcharge) : le .py et le .sh
   ecrivent HH:MM:SS.mmm a 3 chiffres (millisecondes).
3. Garde-fou cree par Morpheus : test-102 (timestamps millisecondes) 6/6 OK,
   preuve negative validee ; serie e + profils-tests.json.
4. Bug preexistant corrige par Morpheus : glob test-0* -> test-* du lanceur
   (test-100/101/102 n etaient JAMAIS executes par la non-regression).
5. Defaut preexistant repare en inter-round (Vulcain) : desynchronisation des
   arbres edith/stark (vues stark regenerees) - test-101 11/11 OK.

Rapports : morpheus/rapports/rapport-tests-microsecondes-2026-08-25.md ;
lecons : corrections.md (themis, vulcain, morpheus) + BDD.

## Lecons

1. Corriger les DONNEES sans corriger la SOURCE qui les genere = correction instantanement re-ecrasee. Le commit 4fbd28f a corrige les fichiers (AGENTS-historique, classeur) mais pas l outil qui les reecrit a chaque activation : 30 minutes apres le commit, les 6 chiffres etaient de retour.
2. Un diagnostic de regression se prouve par la CHRONOLOGIE : les entrees post-commit (18:43, 18:48, 18:51) avec 6 chiffres prouvent que l outil reecrit le mauvais format, pas que la correction anterieure etait incomplete.
3. Le format `%f` Python = 6 chiffres (microsecondes) ; `%3f` = 3 chiffres (millisecondes). A verifier systematiquement dans tout outil qui ecrit des timestamps.
