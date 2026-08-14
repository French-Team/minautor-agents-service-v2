# Controle croise : tri decroissant du registre-tests (2026-08-14)

**Controleur** : Janus (session-llm-1) -- chaine Vulcain -> Morpheus -> Janus -> Cerberus

## Verdict : VALIDE (J1-J5)

## J1 - Outil v0.3.1 : tri decroissant du registre-tests
- registre-tests.jsonl : 520 entrees, trie decroissant par date : OUI
- plus recent en premier, plus ancien en dernier : OUI
- lignes non-JSON conservees en fin : OUI (code)

## J2 - Test-051 : 9/9 OK
- point 4 adapte au tri (cherche l entree de l agent de test, plus la derniere ligne)
- point 7 anti-regression : registre-tests trie decroissant par date

## J3 - Les 5 tests adaptes verts
- test-031 : 10/10 -- test-032 : 10/10 -- test-024 : 15/15
- test-027 : 11/11 -- test-051 : 9/9
- version lanceur 0.3.1 dans les 5 tests (aucun residu 0.3.0 cote lanceur)

## J4 - Doc + catalogue a jour
- doc lanceur v0.3.1 (entree changelog + FIX rotation)
- catalogue : commande tester-lancer-non-regression presente, parametre agent

## J5 - Non-regression complete (avec --agent janus)
- 52 OK / 0 KO (pool 46/46 + globaux 6/6) -- 48.4s, conforme reference (+3%)
- registre-tests journalise 520 traces reelles (janus), triees decroissant

## Decouvertes traitees
1. FIX rotation_registre : la rotation cassait le tri global (scripts + normales
   non tries en tete) -> re-tri global par date apres rotation (preuve : run reel
   112 entrees triees). Documente dans la doc v0.3.1.
2. CRLF (19) dans corrections.md morpheus signales par detecter-usage-outils-externes
   (test-047) -> corrige en LF pur.
3. Artefact test-051 : preuves tmp-t051 laissees dans registre-tests (5/run),
   nettoyees manuellement ; correction du test (nettoyage en fin) a faire par
   Morpheus dans une mission dediee.

## Lecons
- Janus : enregistree dans corrections.md (tri, rotation, CRLF, artefact test-051).
