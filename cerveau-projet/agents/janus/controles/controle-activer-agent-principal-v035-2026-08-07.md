# Mission de controle -- correction bug liaison id v0.3.5

**Agent controle** : Vulcain
**Outil** : activer-agent-principal (py + sh + md + tests)
**Date** : 2026-08-07
**Session** : session-llm-2

## Contexte

Bug MAJEUR : la liaison id<->session posee par sidentifier etait ECRASEE par
activer/reactiver (mettre_a_jour_profil_session sans llm_id reecrivait la ligne
classeur sans le champ id) -> sessions fantomes au redemarrage.
Correction v0.3.5 : preserver l'id existant quand llm_id n'est pas fourni.

## Points de controle

| # | Point | Outil | Attendu |
|---|---|---|---|
| 1 | Parite py/sh : la logique de preservation d'id est identique dans les 2 versions | lire-fichier | id existant lu et preserve dans les 2 |
| 2 | Le .py compile et le .sh a une syntaxe valide | execution | py_compile OK + bash -n OK |
| 3 | La doc .md est versionnee 0.3.5 + ligne de versionning ajoutee | lire-fichier | Version: 0.3.5 + entree 0.3.5 |
| 4 | Conformite ASCII des 4 fichiers (py, sh, md, test-005) | valider-conformite-ascii | 0 caractere non-ASCII |
| 5 | Test-005 (28 cas) passe en entier | execution | VERDICT VALIDE |
| 6 | Regression test-004 (19 cas) toujours verte | execution | VERDICT VALIDE |
| 7 | Echecs test-001/002/003 : prouver qu'ils sont pre-existants (v0.3.4 originale) | execution | echecs identiques vs v0.3.4 |
| 8 | Liaison id reelle dans le classeur : profil-session-llm-2 garde id: llm-1 | lire-fichier | id: llm-1 present |
| 9 | Traces d'outils externes sur les fichiers modifies (CRLF, non-ASCII, BOM) | detecter-usage-outils-externes | 0 trace |
| 10 | Le test-005 verifie le cas NEGATIF (redemarrage sans nouvelle session) | lire-fichier | test 4b/4c presents |

## Verdict

**VERDICT : VALIDE**

| # | Point | Resultat |
|---|---|---|
| 1 | Parite py/sh preservation id | OK -- REGLE LIAISON ID presente dans les 2 (py ligne 289/308, sh ligne 202/216), VERSION 0.3.5 dans les 2 |
| 2 | Syntaxe | OK -- py_compile + bash -n valides |
| 3 | Doc versionnee | OK -- Version : 0.3.5 + ligne 0.3.5 dans Versionning |
| 4 | Conformite ASCII (4 fichiers) | OK -- 0 caractere non-ASCII (verifie) |
| 5 | Test-005 (28 cas) | OK -- 28/28 VERDICT VALIDE (re-execute independamment) |
| 6 | Regression test-004 (19 cas) | OK -- 19/19 VERDICT VALIDE |
| 7 | Echecs test-001/002/003 pre-existants | OK -- prouve : v0.3.4 originale donne les memes resultats (7/5, 7/1, 17/4) |
| 8 | Liaison id reelle classeur | OK -- profil-session-llm-2 garde id: llm-1 (preuve en production : conservee lors de MON activation) |
| 9 | Traces outils externes | OK -- 0 suspect sur 10 fichiers (dossier outil) + corrections propre |
| 10 | Test negatif (pas de session fantome) | OK -- present (test 4b/4c) |

**Observations** :
- Le bug etait reel et reproductible : la liaison id: llm-1 disparaissait apres activer (observe en direct).
- La correction preserve l'id existant quand llm_id n'est pas fourni -- approche minimale et correcte.
- Les echecs test-001/002/003 sont PRE-EXISTANTS (semantique sidentifier changee en v0.3.3/0.3.4), NON lies a cette correction -- verifie par comparaison avec v0.3.4 originale (git show).
- Aucun point bloquant.

**Date** : 2026-08-07 -- Janus
