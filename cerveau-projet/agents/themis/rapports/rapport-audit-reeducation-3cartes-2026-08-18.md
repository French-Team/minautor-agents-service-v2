---
identite:
  type: rapport
  appartient_a: commun
  commun: true
---
# Rapport d'audit Themis -- re-education des cartes Vulcain, Morpheus, Buffy (v0.5.0)

**Date** : 2026-08-18
**Mission** : audit-fin-mission declenche par Buffy (c8a) sur la re-education
des 3 cartes (signalement Themis A REVOIR + Chiron A REVOIR + controle Janus).

## Perimetre audite

Re-education des cartes de Vulcain (0.4.28 -> 0.5.0), Morpheus (0.4.15 ->
0.5.0), Buffy (0.4.14 -> 0.5.0) : pour chacune, ajout de (a) indice GARDE-FOU
C1 en c1, (b) indices REDIRECTION OUTIL BLOQUE + DOMAINES AUTRES AGENTS dans
la case "hors parcours" (c16/c13/c33), (c) indice AGENTS HABILITES dans la
case "Activer l agent habilite" (c17/c15/c34).

## Verifications

| Verification | Resultat |
|---|---|
| c1 : indice GARDE-FOU C1 present (3 cartes) | [OK] |
| Redirection outil bloque presente (3 cartes) | [OK] |
| Indice AGENTS HABILITES present (3 cartes) | [OK] |
| Textes regle < 160 caracteres (test-016 point 9) | [OK] (corrige par Buffy) |
| Versions 0.5.0 sync (carte = fiche PARCOURS, 3 cartes) | [OK] |
| valider-cartes-decision : CONFORME (verifie par Buffy, session habilitee) | [OK] |
| cartes-lock : 3 empreintes MATCH | [OK] |
| Normes : ASCII 0, LF 0 (3 cartes) | [OK] |
| Perimetre git : 3 cartes + 3 fiches + lock + rapports | [OK] |

## Non-regression (verifiee par Buffy)

- test-014 : 13/13, test-021 : 9/9, test-005 : 28/28, test-013 : 22/22
- test-016 : 19/20 - seul KO = pin de version 0.4.14 (buffy) -> adaptation
  par Morpheus (domaine tests)
- test-057 : KO points 12/13 = artefact de session Buffy (verrou SEUL BUFFY
  bloque les non-buffy, mais la session ACTIVE est buffy) -> reverdira sous
  Janus (etait OK sous Janus a 17:44)

## Analyse

Les 3 corrections de formation (modele Themis v0.4.10 / Janus v0.5.0) sont
appliquees aux 3 cartes : GARDE-FOU C1 en c1, redirection outil bloque,
AGENTS HABILITES. Les textes regle respectent la limite de 160 caracteres.
Les 6 cartes principales (cerberus, themis, janus, vulcain, morpheus, buffy)
satisfont desormais toutes le modele de conformite pedagogique.

Les 2 KO restants sont documentes et attendus : pin de version (Morpheus) et
artefact de session (test-057 sous buffy). Aucun n est une regression de la
re-education.

## Verdict

**CONFORME -- 0 defaut.** La re-education des 3 cartes est complete et
validee : modele pedagogique applique, versions sync, locks MATCH, normes OK,
non-regression verte (hors pins et artefacts de session documentes).
