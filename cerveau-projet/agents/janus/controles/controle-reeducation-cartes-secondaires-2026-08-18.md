# Controle -- Re-education 10 cartes secondaires (Janus)

- **Date** : 2026-08-18
- **Controleur** : Janus (second controle, active par Chiron c14 / Buffy c8)
- **Objet** : controle de la re-education des 10 cartes secondaires (atlas,
  argus, hygie, clio, hermes, gardien, chiron, athena, promethee, minerve)
- **Verdict final** : **VALIDE**

## Chaine complete

1. **Cerberus** : demande de verification de conformite des cartes
   secondaires au modele pedagogique -> active Themis (c22).
2. **Themis** (audit initial) : **A REVOIR** -- 10 cartes structurellement
   saines mais pedagogiquement en retard (rapport-audit-cartes-secondaires).
3. **Chiron** (education) : **A REVOIR** -- 3 corrections de formation par
   carte, adaptation pour Chiron (rapport-reeducation-cartes-secondaires),
   lecon 45.
4. **Janus** (controle du defaut) : defaut confirme independamment ->
   boucle KO c9g -> active Buffy.
5. **Buffy** (correction) : pour chaque carte -- c1 + GARDE-FOU C1, case
   "hors parcours" + REDIRECTION OUTIL BLOQUE + DOMAINES, case d'activation +
   AGENTS HABILITES ; Chiron = cas particulier (AGENTS HABILITES en c10).
   Bumps --mineure (atlas 0.5.0, argus/hygie/hermes/gardien/chiron 0.2.0,
   clio 0.6.0, athena/promethee/minerve 0.4.0) + sync fiches + resync locks
   (10 MATCH). Lecon 46.
6. **Themis** (re-audit) : **CONFORME** -- 0 defaut restant
   (rapport-audit-reeducation-cartes-secondaires), lecon 47.
7. **Janus** (re-controle) : boucle KO -> **Morpheus** (pin atlas
   test-005 0.4.9 -> 0.5.0, lecon 48) -> re-controle -> **VALIDE**.

## Verifications sous MA session habilitee

- valider-cartes-decision : 10x CONFORME (atlas, argus, hygie, clio, hermes,
  gardien, chiron, athena, promethee, minerve).
- test-005 : **28/28 OK** (point 17 pin atlas reverdi apres adaptation
  Morpheus ; point 21 artefact de verrou session morpheus, REVERDI sous
  janus).
- test-006 : 19/19, test-020 : 46/46, test-021 : 9/9, test-057 : 24/24
  CONFORME, test-016 : 20/20, test-013 : 22/22, test-014 : 13/13,
  test-092 : 9/9.
- Bumper --tous : 0 outil incoherent. Evaluateur : 15 liens casses
  PREEXISTANTS (protocole-X dans corrections.md, documentes) -- aucune
  ERREUR nouvelle. JSONL 593/593 valide. Residus 0.

## Verdict

**VALIDE** -- les 10 cartes secondaires sont conformes au modele
pedagogique (GARDE-FOU C1, redirection outil bloque, AGENTS HABILITES) avec
l'adaptation Chiron (agent a mission unique). L'ensemble des 16 cartes
(6 principales + 10 secondaires) satisfait desormais le modele de conformite
pedagogique. Tous les tests verts sous session habilitee, aucun defaut
restant.
