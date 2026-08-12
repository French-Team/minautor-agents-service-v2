# Controle croise -- Round 11 : Coherence documentaire (specs vs outils, catalogue)

**Date** : 2026-08-12
**Agent** : Janus (controle croise, dernier maillon de la chaine round 11)
**Mission Cerberus** : verifier les corrections de coherence documentaire
(specs divergentes + decalages catalogue) faites par Vulcain et le garde-fou
test-028 cree par Morpheus.

## Contexte

Le pre-audit du round 11 (demande utilisateur) a revele :
- **8 SPECS DIVERGENTES** : activer-agent-principal (0.5.0 vs 0.5.1),
  combos-moteur (0.3.1 vs 0.3.2), enregistrer-usage-outil (0.1.0 vs 0.2.1),
  generateurs-amelioration (2.0.0 vs 2.1.0), generateurs-commande
  (0.2.2 vs 0.2.4), generateurs-regenerer-catalogue (1.1.0 vs 1.1.1),
  guider-parcours (spec 0.6.2 vs outil 0.5.0 -- spec de conventions),
  valider-case (1.1.0 vs 1.1.1).
- **2 DECALAGES CATALOGUE** : generateurs-case-convertir et generateurs-ligne
  (flags du modele absents de l'aide racine).

## Verifications (J1-J7)

| # | Verification | Resultat |
|---|---|---|
| J1 | detecter-divergences-version : 0 DIVERGENTE | 23 ALIGNEES / 0 DIVERGENTE / 10 SANS VERSION-SPEC (protocoles sans .py) -- OK |
| J2 | detecter-decalages-catalogue : 0 decalage | 139 conformes / 0 decalage / 7 non testables / COMBOS 14 scannes 0 probleme -- OK |
| J3 | test-028 8/8 + test-027 11/11 | 8/8 et 11/11 -- OK |
| J4 | Non-regression complete | 28 OK / 0 KO (28 tests) -- OK |
| J5 | Normes ASCII + LF sur les fichiers modifies | 0/0 sur 19 fichiers (outils, specs, docs, tests, lecons) -- OK |
| J6 | Catalogue : 0 a ajouter | DRY-RUN : 101 outils, 97 preserves, 0 a ajouter -- OK |
| J7 | Registre d usage | 9 lignes : 3 (round 10c) + 3 Vulcain + 3 Morpheus (round 11) -- OK |

## Detail des corrections validees

1. **7 specs bumpees** a la version reelle de leur outil (spec + historique) :
   activer-agent-principal 0.5.1, combos-moteur 0.3.2, enregistrer-usage-outil
   0.2.1, generateurs-amelioration 2.1.0, generateurs-commande 0.2.4,
   generateurs-regenerer-catalogue 1.1.1, valider-case 1.1.1.
2. **guider-parcours (cas particulier)** : la spec versionne les PATTERNS
   (conventions des cartes) a 0.6.2, independamment de l'outil a 0.5.0.
   Le champ `**Version outil** : 0.5.0` declare explicitement la version de
   l'outil ; detecter-divergences-version v0.2.0 le lit en PRIORITE.
3. **detecter-divergences-version v0.2.0** : constante VERSION ajoutee
   (resolvait son propre SANS VERSION) + champ Version outil.
4. **detecter-decalages-catalogue v0.2.0** : scan des SOUS-COMMANDES argparse
   (les 2 decalages etaient des faux positifs : les flags vivent dans les
   sous-commandes `convertir`, `copier`, `ajouter-config`). Variante avec
   prefixe `x` pour les parsers qui consomment la sous-commande comme
   argument positionnel (piege generateurs-case).
5. **verifier-restauration-sure** : ligne `**Version :** 0.1.0` ajoutee a la
   spec (format en tete, priorite 1 du detecteur).
6. **guider-parcours.md** : sections CLI 0.2.0-py/0.2.0-sh -> 0.5.0
   (incoherence interne corrigee).
7. **test-028-coherence-documentaire (Morpheus)** : garde-fou anti-recurrence
   -- 0 spec divergente, 0 spec sans version avec .py, 0 decalage catalogue,
   champ Version outil de guider-parcours present, normes 0/0. Affecte a la
   serie D du lanceur (test-027 11/11 reste vert par import des constantes).

## Verdict

**VALIDE (J1-J7)** -- la coherence documentaire spec/outil/catalogue est
restauree : 0 spec divergente, 0 decalage catalogue, garde-fou en place,
non-regression 28/28. Plus aucune dette documentaire ouverte connue.
