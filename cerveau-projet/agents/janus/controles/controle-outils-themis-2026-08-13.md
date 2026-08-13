# Controle croise : amelioration de Themis (axes A/B/C + garde-fous)

**Date** : 2026-08-13
**Verificateur** : Janus (controle croise)
**Verdict** : VALIDE (J1-J6 verts)

## Contexte

Demande utilisateur : ameliorer Themis (evaluatrice croisee) sur 4 axes.
- Axe A (outiller ses lecons) : detecter-evaluations-incompletes v0.1.0
  (scan anti-recurrence 4 sources : validateur, spec, generateurs, tests).
- Axe B (rounds qualite evaluateurs) : les 4 evaluateurs (structure,
  agents, coherence, conventions) ont recu --rapport, --verbose et la
  desactivation auto des couleurs ANSI hors tty.
- Axe C (evaluateur processus) : evaluer-processus v0.2.0 (fins de mission
  erronees, outils hors carte via le registre, coherence fiche/carte).
- Axe D (carte/declencheurs de Themis) : a faire par Buffy apres.
- Garde-fous : test-035 (evaluer-processus) et test-036
  (detecter-evaluations-incompletes), serie D.

## Verifications (J1-J6)

### J1 : Garde-fous des 2 nouveaux outils
- test-035-evaluer-processus : **8 OK / 0 KO** (outil present, compile,
  --agent morpheus/cerberus 0 probleme, scan global 0, --rapport, normes).
- test-036-detecter-evaluations-incompletes : **8 OK / 0 KO** (outil
  present, compile, motif inexistant 0 mention, motif reel >0, --version,
  --rapport, normes).

### J2 : Cartes conformes
- morpheus : CONFORME (c12/c7 indices outils ajoutes, v0.4.3)
- vulcain : CONFORME (c8 + c10 indices ajoutes, v0.4.4)
- janus : CONFORME (c4 indice ajoute, v0.4.2)

### J3 : Catalogue et index coherents
- catalogue generateurs-commande : **149** commandes (147 + evaluer-processus
  + detecter-evaluations-incompletes)
- index-tools : **118** outils (116 + 2)

### J4 : Non-regression complete
- **36 OK / 0 KO** (34 existants + test-035 + test-036), 42.0 s (pool-16)
- Reference de temps recalee 34 -> 36 tests (41.5 s)

### J5 : Normes
- 10 fichiers verifies (outils, tests, lecons, cartes, fiches) :
  0 non-ASCII, 0 CRLF.

### J6 : Bonus auto-application
- evaluer-processus scan global : **0 probleme de processus detecte** (l outil
  verifie sa propre conformite : les usages de Vulcain de ses 2 nouveaux
  outils sont couverts par la carte c10).

## Points notables

1. **Auto-detection** : test-035 a d abord KO car Vulcain utilisait
   evaluer-processus/detecter-evaluations-incompletes sans les avoir dans SA
   carte (l outil se detectait lui-meme). Correction : indices ajoutes a la
   case c10 + bump parcours 0.4.4 + fiche Pattern 14. C est la preuve que
   l outil fonctionne : il s applique a ses propres regles.
2. **Auto-reference evitee** : test-036 construit le motif inexistant par
   concatenation pour qu il n existe jamais dans le fichier de test.
3. **Protections importees** : test-035/036 passent par
   PROTECTIONS.lancer_protege (exigence test-030, aucun subprocess.run brut).

## Lecon Janus

Un garde-fou qui verifie l ETAT (carte + registre) attrape les derives AVANT
qu elles ne deviennent des incidents : evaluer-processus a revele la lacune
de carte de Vulcain au premier run du garde-fou, pas apres une mission.
