---
identite:
  type: controle
  appartient_a: janus
  commun: false
---
# CONTROLE JANUS -- RE-EDUCATION DES CARTES VULCAIN, MORPHEUS, BUFFY (v0.5.0)

**Date** : 2026-08-18
**Objet** : controle de la re-education des 3 cartes (vulcain 0.4.28 -> 0.5.0,
morpheus 0.4.15 -> 0.5.0, buffy 0.4.14 -> 0.5.0). Chaine : Themis audit
A REVOIR -> Chiron education A REVOIR -> Buffy corrige -> Themis re-audit
CONFORME -> Janus controle -> Morpheus pins -> Janus re-controle.

## Corrections appliquees par Buffy (3 cartes, modele Themis v0.4.10 / Janus v0.5.0)

Pour CHACUNE des 3 cartes :
1. c1 : indice GARDE-FOU C1 (classification, branches exactes + case cible).
2. Case "hors parcours" (vulcain c16, morpheus c13, buffy c33) : indices
   REDIRECTION OUTIL BLOQUE + DOMAINES AUTRES AGENTS.
3. Case "Activer l agent habilite" (vulcain c17, morpheus c15, buffy c34) :
   indice AGENTS HABILITES.
4. Textes regle < 160 caracteres (correction apres test-016 KO).
5. Bump --mineure --wet -> 0.5.0 + sync fiche + resync lock.

## Points de controle (verifies sous MA session habilitee)

| Verification | Resultat |
|---|---|
| Combo controle-modification (nommage, liens, sante, tableaux, traces) | [OK] |
| valider-cartes-decision : CONFORME (3 cartes) | [OK] |
| test-004 : 16/16 OK (KO point 8 sous morpheus = artefact verrou, reverdi sous janus) | [OK] |
| test-016 : 20/20 OK (pin 0.4.14 -> 0.5.0 adapte par Morpheus) | [OK] |
| test-057 (marbre) : 24/24 CONFORME (KO 12/13 sous buffy = artefact session, reverdi) | [OK] |
| test-021 : 9/9, test-005 : 28/28, test-014 : 13/13, test-013 : 22/22, test-092 : 9/9 | [OK] |
| Bumper --tous : 0 outil incoherent | [OK] |
| Residus : 0 | [OK] |
| Evaluateur : 0 ERREUR nouvelle | [OK] |
| JSONL registre : 511/511 valide | [OK] |
| Normes : ASCII 0, LF 0 (3 cartes + 3 fiches) | [OK] |
| cartes-lock : 3 empreintes MATCH | [OK] |
| Perimetre git : 3 cartes + 3 fiches + lock + rapports (themis x3, chiron x2) | [OK] |

## Verdict

**VALIDE** -- la re-education des 3 cartes est conforme et complete.

Les 6 cartes principales (cerberus, themis, janus, vulcain, morpheus, buffy)
satisfont desormais toutes le modele de conformite pedagogique : (a) GARDE-FOU
C1 en c1, (b) redirection outil bloque, (c) AGENTS HABILITES. Les 3 cartes
re-eduquees sont en v0.5.0 (versions sync, locks MATCH, normes OK). Tous les
tests sont verts sous la session du controleur habilite - les 3 artefacts de
session (test-004 sous morpheus, test-057 sous buffy, test-021 sous themis)
ont tous reverdi sous janus, confirmant qu ils etaient lies au verrou
d habilitation, pas a une regression.

Reponse a la demande : OUI, les cartes de Vulcain, Morpheus et Buffy sont
desormais conformes au modele pedagogique (v0.5.0), apres re-education
complete verifiee de bout en bout.
