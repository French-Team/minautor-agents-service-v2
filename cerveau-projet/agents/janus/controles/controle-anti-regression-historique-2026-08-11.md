# Controle croise : Anti-regression historique + maillon manquant Cerberus

**Date** : 2026-08-11
**Controleur** : Janus (second controle independant)
**Chaine** : Cerberus -> Buffy -> Morpheus -> Janus
**Verdict** : **VALIDE**

---

## Contexte de la mission

L'utilisateur a constate 2 problemes :
1. **REGRESSION** : AGENTS-historique.md n'est plus mis a jour (les activations passaient par des scripts temporaires qui court-circuitaient l'outil central activer-agent-principal).
2. **MAILLON MANQUANT** : quand le rapport de Janus signale des problemes a resoudre, Cerberus devait lire ce rapport au retour et activer immediatement l'agent habilite.

## Points verifies

### J1. Les 19 fins d'activation ont l'indice outil PASSE PAR LE GENERATEUR
19/19 fins sur 10 parcours portent l'indice `activer-agent-principal` (catalogue, sans commande en dur) :
- athena c10, atlas c11 + c31b, buffy c22/c27/c8, clio c12
- janus cT6-cT10 (ligne trio) + c10 (Reactiver Cerberus, commande reactiver ajoutee)
- minerve c10, morpheus c10 + c14, promethee c10, themis c13 + c25b
- Poids budget <= 3.0 partout (max 1.5)

### J2. Structure du maillon manquant Cerberus
- **c15b** "Rapport de Janus : problemes a resoudre ?" (controle) : OUI -> c15c, NON -> c16
- **c15c** "Activer l agent habilite (problemes a resoudre)" (action, indice outil PASSE PAR LE GENERATEUR) : suivant -> c15b (boucle de verification)
- c15 branche OUI re-pointee -> c15b (au lieu de c16)
- Version cerberus 0.4.0 -> 0.4.1, fiche Pattern 14 alignee

### J3. valider-cartes-decision
11/11 agents CONFORMES (0 non conforme)

### J4. Navigation reelle
- Boucle cerberus : c15b -> OUI -> c15c (Activer) -> retour c15b -> NON -> c16 (Fichiers changes) : OK
- Fin janus cT6 : commande activer-promethee affichee : OK

### J5. Non-regression complete
23/23 tests OK (test-013 adapte par Morpheus : version 0.4.1, 23 actions, 5 controles)
Registre d usage : 0 ligne apres non-regression (propre)

### J6. Normes
cerberus.md : ASCII 0 non-ASCII, 0 CRLF. JSON des 11 parcours : valides, LF, ASCII.

## Verdict

**VALIDE** - la mission est conforme : les activations passeront desormais par l'outil central (anti-recurrence de la regression historique) et Cerberus traite les problemes signales par Janus des leur retour.

## Observations (hors perimetre, preexistantes)

- vulcain : c9e/c15e non joignables + c6c/c12c 198 car (A ALLEGER) - confirmees via git HEAD
- clio : c6c 175 car (A ALLEGER) - preexistante
