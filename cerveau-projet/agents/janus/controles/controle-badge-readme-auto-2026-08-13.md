# Controle croise : badge README header automatique (Janus)

- **Date** : 2026-08-13
- **Mission** : combos-maj-readme-massive v0.1.1 (Buffy) + garde-fou test-038 (Morpheus)
- **Controleur** : Janus (controle croise final)

## Verifications

| Point | Resultat |
|---|---|
| J1 - Combo v0.1.1 | aligner_badge_header (importlib, etape 4, regex affichage+href) |
| J2 - test-038 | 4/4 OK (README sain) + preuve negative (href 121 -> KO) |
| J3 - Affectation | serie d (2 blocs) + DUREES_CONNUES (2 blocs) |
| J4 - Normes | 0 ecart ASCII/LF sur 6 fichiers |
| J5 - Non-regression complete | 38/38 OK (44.5 s, nouvelle base avec test-038) |

## Verdict

**VALIDE** - le badge Outils-N (affichage + href) est corrige automatiquement
par le combo v0.1.1 et protege par le garde-fou test-038 dans la serie d.
