# Controle -- Marbre : exception pilote Chiron (Janus)

- **Date** : 2026-08-18
- **Controleur** : Janus (second controle, active par Gardien c9)
- **Objet** : controle de la modification de la zone protegee
  regles-groupes-agents (exception pilote Chiron : auto-correction de SA
  carte via editer-parcours)
- **Verdict** : **CONFORME** (avec suite de chaine identifiee)

## Verifications

1. **Proposition Gardien** : rapport proposition-exception-chiron-auto-
   correction-2026-08-18.md present (zone + raison + impact).
2. **Validation utilisateur** : acquise via ask_user 2026-08-18 (choix
   "Auto-correction complete").
3. **Contenu modifie** : regles-groupes-agents.md contient la section
   "EXCEPTION PILOTE -- CHIRON (2026-08-18, decision utilisateur)" apres la
   section "Nuance (lecons OK)". ASCII 0, LF pur.
4. **Porte executee** : proteger-modifier-marbre --zone
   regles-groupes-agents, audit Argus PROPRE (0 contradiction), re-empreinte
   33429f9f -> 320274ff, journalisee dans marbre-log.jsonl.
5. **Verrou marbre** : proteger-verrou-marbre --tous = 8/8 conforme.
6. **Bumper** : 0 outil incoherent.

## Verifications complementaires (branche verrou + tests)

7. **Verrou habilitation (Vulcain)** : proteger-verrou-habilitation v0.4.0
   avec cle exclusive CHIRON_AUTO_CORRECTION (chiron -> editer-parcours sur
   parcours-chiron.json UNIQUEMENT). editer-parcours v0.1.7 passe la cible au
   verrou. Tests manuels sous audit : chiron sur SA carte -> OK ; chiron sur
   une autre carte (atlas) -> BLOQUE (exclusif buffy).
8. **test-056 (verrou)** : pin 0.2.2 -> 0.4.0 adapte par Morpheus, 17/17 OK
   sous session janus.
9. **test-058 (SEUL BUFFY)** : adapte pour l'exception chiron (carte chiron
   autorisee a porter editer-parcours) + mentions pedagogiques des indices
   AGENTS HABILITES gerees, 6/6 OK.
10. **Non-regression** : test-057 24/24, test-037 6/6, bumper 0/0,
    evaluateur = 15 liens protocole-X preexistants (0 nouveau), marbre 8/8.

## Defauts identifies (suite de la chaine)

1. **test-058 KO point 2** : les indices AGENTS HABILITES ajoutes lors de la
   re-education des cartes secondaires mentionnent "editer-parcours" dans le
   texte de 10 cartes (atlas, argus, hygie, clio, hermes, gardien, janus,
   athena, promethee, minerve) -> le garde-fou anti-usurpation le detecte.
   Correction : alleger les indices (retirer la mention litterale de
   l'outil) OU adapter test-058 pour l'exception chiron.
2. **Verrou d'habilitation** : l'exception chiron exige une cle exclusive
   par cible dans proteger-verrou-habilitation (chiron -> editer-parcours
   sur parcours-chiron.json UNIQUEMENT), comme la cle exclusive tests pour
   morpheus. Sans cela, ajouter editer-parcours a la carte chiron
   habiliterait chiron sur TOUTES les cartes (violation SEUL BUFFY).
3. **Carte de Chiron** : a construire (parcours d'auto-correction +
   indice editer-parcours restreint).

## Suite de la chaine

Gardien (fait) -> **Vulcain** (verrou cle exclusive chiron, fait) ->
**Morpheus** (test-056 + test-058, fait) -> **Buffy** (carte chiron :
parcours auto-correction) -> **Themis** (audit de la re-education) ->
**Janus** (re-controle) -> Cerberus (bilan consolide).

## Verdict (branche verrou + tests)

**CONFORME** -- le verrou d'habilitation (cle exclusive chiron par cible,
editer-parcours v0.1.7) et les tests (test-056 17/17, test-058 6/6) sont
valides et non regressifs. Il reste a construire la carte de Chiron
(parcours d'auto-correction + indice editer-parcours restreint) -- maillon
suivant : Buffy.
