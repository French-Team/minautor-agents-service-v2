# Controle croise -- Bug nettoyer-sessions (en-tete ## Sessions LLM)

**Date :** 2026-08-12
**Chaine :** Cerberus -> Vulcain (nettoyer-sessions v0.1.2) -> Morpheus (test-001 + test-025) -> Janus
**Verdict :** VALIDE (J1-J6 verts)

---

## Contexte

Au nettoyage de session du 2026-08-12, `sidentifier` echouait
('Section ## Sessions LLM introuvable dans AGENTS.md') : nettoyer-sessions
v0.1.1 supprimait l'en-tete de section `## Sessions LLM` a tort (hors du
perimetre documente 'etats actifs uniquement').

## Corrections

- **nettoyer-sessions v0.1.1 -> v0.1.2** (py + sh en parite + doc .md) :
  l'en-tete `## Sessions LLM` est PRESERVE, seuls les blocs
  `### Session : session-llm-N` (titre + contenu) et la section
  `## Sessions connues` sont supprimes.
- **test-001-nettoyer-sessions.sh v0.1.0 -> v0.1.2** : version attendue
  0.1.2, assertion 4b INVERSEE (en-tete PRESERVE et non supprime), +
  3 tests d'integration 7c/7d/7e (sidentifier fonctionne sur la copie
  nettoyee et recreer le bloc session).
- **test-025-nettoyer-sessions-garde-fou** cree (py + md) : garde-fou
  anti-recurrence de la boucle COMPLETE nettoyage -> en-tete conserve ->
  sidentifier, sur copies, avec parite py/sh et normes.

## Verifications (J1-J6)

| Controle | Resultat |
|---|---|
| J1. outil v0.1.2 : en-tete preserve, parite py/sh, doc alignee, ASCII/LF | OK |
| J2. test-001 adapte (version 0.1.2 + 4b + 7c/7d/7e) | 35/35 VALIDE |
| J3. garde-fou test-025 (boucle complete) | 11/11 OK |
| J4. non-regression (outil lancer-non-regression) | 25/25 OK, registre 0 ligne |
| J5. lecons Vulcain + Morpheus documentees | OK |
| J6. delegation respectee (Vulcain sans AUCUN fichier de test) | OK |
| Combo controle-outil (ASCII + cartes 11/11 + liens) | TERMINE |

## Verdict

**VALIDE.** La boucle nettoyage -> re-identification est desormais verrouillee
par les tests (test-001 7c/7d/7e + garde-fou test-025) : toute regression
(en-tete supprime, sidentifier casse, parite cassee) fera KO la
non-regression.
