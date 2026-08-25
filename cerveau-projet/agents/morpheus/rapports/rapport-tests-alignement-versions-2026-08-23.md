RAPPORT DE TESTS MORPHEUS (inter-round, delegation Vulcain)

Date: 2026-08-23
Objet: adaptation des tests suite a l alignement des versions de 3 outils par Vulcain

CONTEXTE
Vulcain a aligne les sources de verite de 3 outils (detecter-divergences-version -> 0 DIVERGENT) :
(1) activer-agent-principal spec 0.5.23 -> 0.5.30 (alignee sur py/sh/md)
(2) editer-fichier en-tetes py/sh/md 0.4.3 -> 0.5.0 (alignes sur la VERSION constante du code)
(3) valider-cartes-decision md 0.4.6 -> 0.4.7 (aligne sur py/sh)
Ma mission : adapter les tests qui pinent ces versions et executer les tests individuels.

VERIFICATION DES PINS
- Aucun test ne pinne les versions modifiees : les occurrences trouvees dans test-016/056/005 sont DOCUMENTAIRES (historique de version, pas des pins d outil).
- Aucun compagnon (index-tools, generateurs-case, guider-parcours) ne porte de version editer-fichier explicite : les mentions sont nominales.
-> AUCUNE adaptation de test necessaire : les changements Vulcain etaient documentaires (en-tetes alignes sur des constantes deja existantes).

TESTS INDIVIDUELS EXECUTES
- test-016-migration-buffy : 18/20 -- KO 2a = pin nombre de cases carte buffy (42 vs 41 attendues, carte bumpee par Buffy anterieurement) PREEXISTANT, hors perimetre
- test-056-verrou-habilitation : 18/18 OK
- test-005-generateurs-commande : 24/28 -- KO 6/8 (chemins d execution), KO 21 (valider-cartes-decision verrou habilitation: morpheus non habilite, contextuel), KO 23 (commandes activer-* sans .md nominal, preexistant) - aucun lie aux versions
- test-028-coherence-documentaire : 7/8 -- KO 3 = artefact d execution (racine relative inexistante depuis sous-dossier); la verification reelle (detecter-divergences-version) confirme 0 DIVERGENT
- test-040-catalogue-index-synchronise : 4/5 -- KO 3 = entree manquante hades-contexte-git, PREEXISTANT hors perimetre
- test-092-parite-agents-activation : 7/9 -- KO 4/5 = 'stark' considere agent mort (Stark passe en groupe freelance v2, dictionnaire activer-agent-principal non mis a jour) PREEXISTANT, hors perimetre

VERDICT
- Les 3 alignements de version sont CONFORMES (0 DIVERGENT confirme).
- AUCUN test a adapter (changements documentaires, aucun pin).
- Les KO observes sont tous PREEXISTANTS ou CONTEXTUELS (verrous d habilitation, migration v2, artefacts d execution) : aucun n est une regression de la mission.
- Non-regression complete : domaine JANUS (dernier maillon) - je ne la lance pas (REGLE ABSOLUE).

Rapporte a Vulcain (appelant, inter-round) pour reprise de round.
