# Controle de la mission Vulcain : convertir-carte-mermaid v0.3.0 (mode --arbres)

- **Date** : 2026-08-24
- **Agent controle** : Vulcain (outil) + Morpheus (test-101, inter-round)
- **Mission** : etendre convertir-carte-mermaid aux ARBRES de decision v2
  (freelance/<agent>/parcours/arbre-<agent>.json : racine/branches/fins,
  PAS des cartes v1) -> .mmd + .svg + index.md dans cartes-vues/arbres/

## Points a verifier (AVANT verdict)

1. **Outil** : v0.2.1 -> v0.3.0, fonctions arbres presentes (lister_arbres,
   agent_de_l_arbre, convertir_arbre, verifier_arbres, generer_arbres,
   asciifier), --arbres + --verifier (combine cartes v1 ET arbres v2),
   --sortie par defaut cartes-vues/arbres, fiche-outil a jour.
2. **Livrables** : 9 arbres v2 .mmd + 9 .svg + index.md dans
   cerveau-projet/cartes-vues/arbres/ (edith, forge, fury, jarvis, parker,
   rogers, shuri, stark, vision).
3. **Synchronisation** : --arbres --verifier rc=0, "9 arbres v2 synchronises
   avec leur .mmd et .svg : OK".
4. **Test dedie** : test-101-arbres-mermaid-garde-fou (Morpheus) 11/11 OK,
   preuves negatives .mmd/.svg detectees (rc=1), 0 residu.
5. **Non-regression** : test-096 6 KO pre-existants (baseline stash), aucun
   nouveau KO.
6. **Normes** : ASCII 0/0 sur outil, fiche, test, corrections vulcain et
   morpheus ; LF pur.
7. **Perimetre** : seuls les fichiers de la mission modifies (outil, fiche,
   test-101, cartes-vues/arbres, lecons, registre, AGENTS/historique via
   activations).

## VERDICT : VALIDE (0 defaut)

**Verifications** :
- Outil v0.3.0 (v0.2.1 -> v0.3.0) : fonctions arbres presentes (lister_arbres, agent_de_l_arbre, charger_json, slugifier, convertir_arbre, ids_arbre, verifier_arbres, generer_arbres, asciifier), --arbres + --verifier (combine cartes v1 ET arbres v2), --sortie par defaut cartes-vues/arbres, fiche-outil a jour.
- Livrables : 19 fichiers dans cartes-vues/arbres/ = 9 .mmd + 9 .svg + index.md (edith, forge, fury, jarvis, parker, rogers, shuri, stark, vision).
- Synchronisation : --arbres --verifier rc=0, "9 arbres v2 synchronises avec leur .mmd et .svg : OK".
- Test-101 (Morpheus, inter-round) : 11/11 OK (presents, verifier_arbres rc=0, syntaxe, index 9 agents, ASCII/LF, XML 9/9, determinisme 9/9, 2 preuves negatives detectees rc=1), 0 residu.
- Non-regression : test-096 6 KO pre-existants (baseline stash, hades manquant + svg v1 desynchronises) - aucun nouveau KO.
- Normes : ASCII 0/0 sur outil, fiche, test-101, controle, index.md.
- Combo controle-modification : termine (nommage, liens, separation, sante, tableaux, surcharge, traces externes valides).
- evaluer-processus : 8 problemes TOUS pre-existants (flags mettre-a-jour-readme 06:58, themis valider-cartes-decision deja signale) - aucun cree par cette mission.

**Lecons** :
1. UNE STRUCTURE NOUVELLE (arbres v2 vs cartes v1) EXIGE UN PARSEUR ET UN TEST DEDIES : le mode --arbres de convertir-carte-mermaid est verrouille par test-101 (11 points) - la ligne "9 arbres v2 synchronises" du test-096 vient de l'outil, pas d'un test dedie.
2. verifier_arbres(racine,...) attend la RACINE DU PROJET (contenant cerveau-projet/), pas cerveau-projet/ lui-meme - sinon 0 arbre trouve et les preuves negatives passent a tort (lecon Morpheus confirmee par verification).
3. --verifier combine cartes v1 ET arbres v2 (rc = rc_v1 or rc_v2) : un controle doit isoler les arbres (verifier_arbres direct) car les cartes v1 portent une dette pre-existante (hades, svg desynchronises).

**Preuves** : rapport controle-modification-arbres-v2-2026-08-24.md, test-101 11/11 OK, --arbres --verifier rc=0, evaluer-processus 8 pre-existants, ASCII 0/0.
