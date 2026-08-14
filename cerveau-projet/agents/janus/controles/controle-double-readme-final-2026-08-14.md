# Controle croise final : double README + outillage (Buffy -> Clio -> Morpheus -> Janus)

**Date** : 2026-08-14
**Agent controle** : Janus (verdict final + non-regression)

## Contexte

Scission du README en 2 fichiers (decision utilisateur) :
- README.md (racine) = GRAND PUBLIC (titres revus, sans structure ni detail technique,
  section 'Amelioration continue' ajoutee, lien vers readme-dev.md)
- cerveau-projet/readme-dev.md = DEVELOPPEURS (12 sections, 15 Ko, sources de verite)

## Chaine complete

| Agent | Realisation |
|---|---|
| Buffy | Outillage : template readme-dev, parcours clio 0.5.5 (branche readme-dev + case c20), carte cerberus 0.4.4 (indice amelioration c1b) |
| Clio | Contenu : readme-dev.md complet + README public allege, version 0.3.0 -> 1.0.0 -> 1.1.0 (bump combo), badges synchronises |
| Buffy | Correction poids des cases (c1b 2.5, c20 3.0 - valider-case CONFORME) |
| Morpheus | Adaptation test-013 (version 0.4.4) |
| Janus | Controles 13/13 puis 16/16 puis 8/8 + NON-REGRESSION COMPLETE |

## Verifications finales

| Test | Resultat |
|---|---|
| Non-regression complete (46 tests) | **46 OK / 0 KO** |
| Chrono | 47.3 s vs reference 46.0 s (+3%, conforme) |
| test-013 (carte cerberus 0.4.4) | 22/22 |
| test-038 (badges README v1.1.0) | 7/7 |
| test-020 (combos clio) | 46/46 |
| valider-case cerberus + clio | CONFORME |
| Normes ASCII + LF (README, readme-dev, template, test-013) | 0/0 |

## Verdict

**VALIDER : non-regression 46/46 OK** - double README termine, outillage conforme,
tests reverdis. 0 residu (tmp-janus supprime a la fin).
