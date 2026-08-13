# Audit : badge README header automatique (Themis)

- **Date** : 2026-08-13
- **Mission** : combos-maj-readme-massive v0.1.1 (Buffy) + garde-fou test-038 (Morpheus)
- **Auditrice** : Themis (evaluation croisee)

## Verifications

| Point | Resultat |
|---|---|
| T1 - Combo v0.1.1 | aligner_badge_header present (importlib, etape 4, regex affichage+href) - aligne sur README sain = False (aucune fausse correction) |
| T2 - test-038 | 4/4 OK sur README sain ; preuve negative (href 121) -> KO detecte |
| T3 - Affectation | test-038 dans serie d (2 blocs) + DUREES_CONNUES (2 blocs) |
| T4 - Normes | ASCII 0 / LF pur sur les 7 fichiers (combo, test-020, test-038, lanceur, README) |
| T5 - test-020 | 46/46 OK (execution reelle du combo massive incluse) |

## Verdict

**VALIDE** - le badge Outils-N du README (affichage + href) est desormais
corrige automatiquement par le combo v0.1.1 et surveille par le garde-fou
test-038 (serie d, non-regression).
