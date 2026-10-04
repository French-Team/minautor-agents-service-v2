# Controle croise : badges header generalises (Janus)

- **Date** : 2026-08-13
- **Mission** : combos-maj-readme-massive v0.1.2 (Buffy) + garde-fous test-038 etendu / test-039 (Morpheus)
- **Controleur** : Janus (controle croise final)

## Verifications

| Point | Resultat |
|---|---|
| J1 - Combo v0.1.2 | aligner_badges_header (Outils/Version/Statut + badges statiques) |
| J2 - Sources | version-readme.txt = 0.2.0, statut-projet.txt = stable |
| J3 - Tests | test-038 7/7 OK, test-039 4/4 OK |
| J4 - Affectation | serie d (2 blocs) + DUREES (2 blocs), normes 0 ecart |
| J5 - Non-regression complete | 39/39 OK (44.3 s, nouvelle base avec test-039) |

## Verdict

**VALIDE** - les badges du header sont synchronises sur des sources de
verite dediees (clio/) et les garde-fous test-038/039 protegent la suite.
Les residus accidentels de version (0.2.1, v0.2.6) sont supprimes et
l anti-recurrence est en place.
