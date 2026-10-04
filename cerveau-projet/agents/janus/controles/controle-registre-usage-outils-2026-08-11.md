# Controle croise : registre d usage des outils (enregistrer-usage-outil v0.1.0)

**Date** : 2026-08-11
**Controleur** : Janus (second controle, chaine Cerberus -> Vulcain -> Morpheus -> Janus)
**Objet** : verification croisee du nouveau registre d usage des outils (demande utilisateur URGENTE : tracer QUI utilise QUEL outil pour detecter les contournements d outils) + adaptation test-005

---

## Verdict : VALIDE

## Controles J1-J8

| # | Controle | Resultat |
|---|---|---|
| J1 | Outil complet (py + sh + md + spec), normes 0 non-ASCII/0 CRLF, compile OK, --version OK | OK |
| J2 | Registre JSONL existe, purge (0 entree de test), ASCII strict + LF pur | OK |
| J3 | Journalisation AUTO via generateurs-commande : 1 ligne mode generateur | OK |
| J4 | Outil dedie : 1 ligne mode combo | OK |
| J5 | Catalogue 142 trie + entree enregistrer-usage-outil ; index-tools Enregistrer 1 + Total 111 ; test-007 15/15 | OK |
| J6 | test-005 reverdi 28/28 + parite py/sh v0.2.3 | OK |
| J7 | Non-regression complete | OK (23/23) |
| J8 | Registre purge en fin de controle (0 ligne) | OK |

## Detail du travail verifie

1. **enregistrer-usage-outil v0.1.0** (Vulcain) : append JSONL (date, agent,
   outil, mode generateur|direct|combo, commande, contexte). --dry-run.
   NE VALIDE PAS l outil (usage reel : detecte les commandes en dur / outils
   hors catalogue). py + sh (wrapper) + md + spec. Registre :
   cerveau-projet/agents/traces/registre-usages-outils.jsonl.
2. **generateurs-commande v0.2.3** (Vulcain) : journalise automatiquement
   chaque commande generee (mode generateur) apres composer_commande.
   --agent optionnel (defaut : agent actif lu dans AGENTS.md session-llm-1,
   corrige : le decoupage sur "\n---" evite de couper au separateur du
   tableau markdown). --no-journal pour desactiver. Discret (stderr).
3. **test-005** (Morpheus) : 10 occurrences v0.2.2 -> v0.2.3. KO de parite
   decouvert : le .sh de generateurs-commande est une implementation bash
   PARALLELE avec VERSION en dur -> 2 occurrences corrigees -> parite v0.2.3.

## OBSERVATION IMPORTANTE (recommandation pour la suite)

La journalisation auto du generateur pollue le registre pendant la
NON-REGRESSION : les tests qui passent par generateurs-commande (test-005,
test-021, etc.) ajoutent leurs commandes au registre (88 lignes observees
pendant la non-regression). RECOMMANDATIONS :
1. Faire passer aux tests de la suite le flag `--no-journal` (Morpheus)
   pour ne pas polluer la source de verite pendant les tests.
2. OU purger le registre en fin de non-regression (nettoyage).
3. Le registre est la source de verite des usages REELS (agents) : les
   entrees de test doivent en etre exclues.

## Lecons Janus

1. Le registre d usage cree la source de verite manquante : les controles
   pourront croiser les rapports de mission avec les traces reelles.
2. La journalisation auto est operationnelle (mode generateur + direct/combo)
   et discret (ne casse pas la sortie du generateur).
3. Pollution tests : a traiter en priorite (--no-journal dans les tests).

## Fichiers verifies

- cerveau-projet/agents/tools/enregistrer/enregistrer-usage-outil/ (py + sh + md + spec)
- cerveau-projet/agents/traces/registre-usages-outils.jsonl (vide, propre)
- cerveau-projet/agents/tools/generateurs/generateurs-commande/generateurs-commande.py (v0.2.3)
- cerveau-projet/agents/tools/generateurs/generateurs-commande/generateurs-commande.sh (v0.2.3)
- cerveau-projet/agents/tools/generateurs/generateurs-commande/catalogue-commandes.json (142)
- cerveau-projet/agents/tools/index-tools.md (Enregistrer 1, Total 111)
- cerveau-projet/agents/tools/tester/tests/test-005-generateurs-commande/ (28/28)
- cerveau-projet/agents/tools/tester/tests/test-007-figer-lf/ (15/15)
