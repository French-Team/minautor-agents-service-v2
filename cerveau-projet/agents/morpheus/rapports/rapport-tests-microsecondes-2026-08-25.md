---
agent: morpheus
date: 2026-08-25
mission: tester la correction des timestamps (microsecondes 6 -> millisecondes 3) dans activer-agent-principal (v0.7.3)
delegue_par: vulcain
---

# Rapport de mission Morpheus : tests correction microsecondes

## 1. Contexte

Vulcain a corrige `activer-agent-principal` (v0.7.3) : les timestamps d historique
etaient ecrits a 6 chiffres (`%f`, microsecondes) au lieu de 3 (millisecondes).
Correction : troncature `[:-3]` dans le .py (4 occurrences) et `%3N` dans le .sh.
Le precedent correctif (commit 4fbd28f) n avait corrige que les donnees, pas l outil.

## 2. Verdict sur la correction Vulcain

**0 regression.** La correction est VALIDE :

- Test reel en conditions (copie AGENTS_FILE) : le .py et le .sh ecrivent
  `HH:MM:SS.mmm` a 3 chiffres.
- test-099 (activation relais, garde-fou) : 6/6 OK.
- test-098 (format historique) : KO preexistants documentes (dictionnaire v1
  non propage a la v2), regex compatible avec 3 chiffres : 0 impact.
- test-092 (parite py/sh) : KO preexistants documentes (ferrari manquant,
  stark mort dans le dictionnaire v1) : 0 impact.
- Tests .sh de l outil (test-001/002/003/008) : KO preexistants verifies a la
  baseline par stash (test-001 Test 7 pinne l ancien format 4 colonnes obsolete
  depuis v0.6.1 ; test-008 pinne v0.5.7 jamais adapte ; test-002/003 dependance
  CWD). Aucun lie aux microsecondes.

## 3. Garde-fou cree : test-102 (timestamps millisecondes)

- Fichier : `cerveau-projet/agents/tools/tester/tests/test-102-timestamps-millisecondes/`
- Verifie : 6 points (aucun `%f` sans troncature dans le .py, `%3N` dans le .sh,
  execution reelle .py et .sh avec AGENTS_FILE surcharge, pas de `%3f` litteral
  (invalide en Python), normes ASCII/LF).
- Resultat : 6/6 OK. Preuve negative validee (retrait de la troncature ->
  detection des 6 chiffres).
- Enregistre : serie e du lanceur + profils-tests.json (profils "outils" et "tests").

## 4. BUG PREEXISTANT CORRIGE : glob de detection du lanceur

Decouverte pendant la mission : le glob `test-0*` du lanceur de non-regression
NE MATCHAIT PAS les tests numerotes 100+ (test-100, test-101 crees le 24/08,
et mon test-102) : ils n etaient JAMAIS executes par la non-regression.

- Correction : `test-0*` -> `test-*` dans `tester-lancer-non-regression.py`
  (detection) et `test-027-series-garde-fou.py` (meme logique de couverture).
- Detection apres correction : 100 tests (avant : 97). test-027 point 1
  (couverture des series) : OK.
- test-100 et test-101 ajoutes a la serie e (garde-fous specifiques) pour
  satisfaire la couverture.
- Lanceur verifie : `--version` v0.6.2 OK. Le lanceur est verrouille Janus
  (test-027 points 5-8 KO = comportement attendu pour Morpheus).

## 5. DEFECT PREEXISTANT DETECTE (a reparer par l habilite) : desynchronisation des arbres

Le correctif glob a rendu test-101 (arbres mermaid, jamais execute auparavant)
actif dans la non-regression. Resultat : **2 KO reels** :

- test-101 point 2 (verifier_arbres rc=1) : `edith.mmd` non synchronise,
  `stark.mmd` non synchronise, `stark.svg` non synchronise.
- test-101 point 7 (determinisme) : diff=['stark'].

Causes (mtimes) :
- `arbre-stark.json` modifie 2026-08-25 07:25, vues generees 2026-08-24 18:47 :
  l arbre est plus recent que ses vues.
- `arbre-edith.json` (2026-08-23) et vues (2026-08-24) : vues non synchronisees
  avec l arbre actuel.

Reparation attendue (domaine Vulcain) : regenerer les vues edith et stark via
`convertir-carte-mermaid --arbres` (rendu deterministe octet a octet).

**RESOLUTION (inter-round Vulcain, meme round)** : verifier_arbres a montre que
seul stark etait encore desynchronise (edith resynchronise entre-temps,
probablement par le serveur EDITH H24). Vulcain a regenere les vues stark
(convertir-carte-mermaid --arbres --agent stark : stark.mmd 4 lignes + stark.svg
1170 octets). Resultat : 9 arbres v2 synchronises OK, **test-101 11/11 OK**.
Lecon Vulcain ajoutee (toute modification d un arbre doit regenerer ses vues).

## 6. Fichiers modifies par Morpheus

- `cerveau-projet/agents/tools/tester/tests/test-102-timestamps-millisecondes/`
  (cree : test + normes ASCII/LF)
- `cerveau-projet/agents/tools/tester/tester-lancer-non-regression/tester-lancer-non-regression.py`
  (glob + serie e)
- `cerveau-projet/agents/tools/tester/tests/test-027-series-garde-fou/test-027-series-garde-fou.py`
  (glob)
- `cerveau-projet/agents/tools/tester/profils-tests.json` (test-102)

## 7. Lecons

Voir corrections.md + BDD (lecon enregistree).
