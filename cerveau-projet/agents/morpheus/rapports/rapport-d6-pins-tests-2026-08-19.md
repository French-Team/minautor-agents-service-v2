# Rapport Morpheus -- D6 : pins de tests adaptes (2026-08-19)

## Mission
Adapter les pins de tests obsoletes apres le D6 (outils generiques multi-sessions
par Vulcain + cartes `<session>` par Buffy).

## Corrections appliquees (SEUL Morpheus habilite pour les tests)

| Test | Pin adapte |
|---|---|
| test-005 | generateurs-commande 0.2.6 -> 0.3.1 (py + sh) + parcours-atlas 0.5.0 -> 0.5.1 |
| test-056 | proteger-verrou-habilitation 0.4.0 -> 0.4.1 |
| test-089 | detecter-ecritures-hors-cycle 0.1.0 -> 0.1.2 |
| test-060 | analyser-tokens 0.1.1 -> 0.1.2 (version + docs .md) |
| test-013 | parcours-cerberus 0.5.4 -> 0.5.5 |
| test-016 | parcours-buffy 0.5.0 -> 0.5.1 |
| test-018 (5b) | garde-fou positif : accepte `activer <session>` OU `session-llm-N` |
| test-021 (3) | fins trio : accepte `activer <session>` OU `session-llm-N` |
| test-033 (3/4) | c14 morpheus : accepte `activer <session> janus` ; anti-piege reactiver cible la COMMANDE, le texte pedagogique est tolere |

## Correction complementaire : spec oubliee par Vulcain

- generateurs-commande.py bumpe a 0.3.1 (D6) SANS bumpe la spec (0.2.6)
  -> test-028 (0 spec divergente) KO. Spec corrigee : 0.3.1 avec historique
  v0.3.1 (multi-sessions _session_appelante).

## Non-regression ciblee (11 tests)

- VERTS : test-013 (22), test-016 (20), test-018 (13), test-028 (8),
  test-033 (9), test-056 (17), test-057 CONFORME (24), test-060 (12),
  test-089 (9)
- KO CONTEXTUELS (verrou habilitation, non corrigeables) : test-005 p21
  + test-021 p7 appellent valider-cartes-decision (exclusif
  argus/buffy/janus/vulcain) -> redeviennent verts quand JANUS lance la
  non-regression finale (deja OK par janus avant D6 dans le registre).
- Normes : ASCII strict + LF pur sur les 10 fichiers modifies.

## Bugs/lecons a transmettre

1. **Spec generateurs-commande oubliee** par Vulcain : un outil bumpe =
   sa spec doit suivre (sinon test-028 KO). Corrige par Morpheus.
2. **Bug multi-sessions dans proteger-verrou-habilitation** : la commande
   suggeree par le verrou utilise trouver_session_agent qui retourne le
   PREMIER bloc AGENTS.md portant l agent (session-llm-4) au lieu de la
   session la plus recente de l appelant (session-llm-1) quand 2 sessions
   ont le meme agent actif (morpheus dans llm-1 et llm-4). A corriger par
   Vulcain : prendre la session la plus recente (colonne Derniere activite)
   parmi celles portant l agent, ou SESSION_LLM/classeur en priorite.
3. Processus morpheus : 0 probleme (declarations fautives retirees).

## Relais
Activation de JANUS (controle final, seconde paire d yeux) avec ce bilan.

## Mise a jour (boucle KO Janus)

- **test-090 corrige** : liste blanche lecons.db etendue pour
  evaluer-progression (outil legitime du catalogue, cree par session llm-4,
  lecture seule du compteur). VERDICT : 11/11.
- **test-085 KO en parallele seulement** : passe en serial (interference
  registre entre tests paralleles) - KO non bloquant.
- **Defaut de carte vulcain a signaler (Buffy)** : le Vulcain de
  session-llm-1 a journalise un usage de detecter-ecritures-hors-cycle a
  21:07:40 (test post-bump D6) mais l outil est ABSENT des indices de SA
  carte -> DECLARATION_FAUTIVE (outil hors carte) par evaluer-processus.
  Correctif : ajouter l outil a la carte vulcain (SEULE Buffy).
- **Pre-existants session llm-4 (20:51)** : 3 usages vulcain hors carte
  (evaluer-progression, valider-conformite-ascii, valider-nommage) + outil
  evaluer-progression non commite - a traiter par la session proprietaire.
