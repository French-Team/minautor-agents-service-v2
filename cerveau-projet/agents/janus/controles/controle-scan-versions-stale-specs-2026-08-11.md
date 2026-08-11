# Controle croise -- Scan versions stale dans les specs (Janus)

**Date** : 2026-08-11
**Mission** : controle croise du scan des versions stale dans les specs (Promethee) + adaptation du test-014 (Morpheus)
**Verdict** : **VALIDE** (6 points J1-J6 verts, non-regression 22/22)

## Points controles

| # | Controle | Resultat |
|---|---|---|
| J1 | detecter-divergences-version : 1 DIVERGENT restant = guider-parcours (cas inverse py 0.5.0 vs spec 0.6.2, observation pour Vulcain) | OK |
| J2 | Balayage : 0 spec restante avec ancienne version (valider-case v1.0.2, spec-refonte v0.1.1, v0.2.2/v0.2.0 actuel) | OK |
| J3 | Normes : 8 specs + test-014, tous 0 non-ASCII / 0 CRLF | OK |
| J4 | test-014-spec-guider-parcours reverdi : 13/13 OK | OK |
| J5 | Non-regression complete : 22/22 OK | OK |
| J6 | spec-combos-moteur : en-tete 0.3.0 + GARDE-FOU v0.3.0 documente + 6 mentions v0.2.1 conservees (references historiques legitimes de la regle KO test-003) | OK |

## Corrections validees (8 specs + 1 test)

| Fichier | Correction |
|---|---|
| spec-refonte-cartes-decision | 7.1 generateurs-case v0.2.2->v0.4.2, 7.2 generateurs-carte v0.2.0->v0.3.0 |
| spec-valider-case | 3 refs spec-refonte v0.1.1 -> v0.1.3 |
| spec-detecter-convention-nommage | valider-case v1.0.2 -> v1.1.0 |
| spec-generateurs-ligne | 4 mentions valider-case v1.0.2 -> v1.1.0 |
| spec-combos-moteur | 0.2.1 -> 0.3.0 (garde-fou implante documente) |
| spec-detecter-decalages-catalogue | 0.1.0 -> 0.1.1 (section COMBOS) |
| spec-generateurs-case | 0.4.0 -> 0.4.2 (budget pondere) + historique + \n parasite corrige |
| spec-guider-parcours | 2 mentions valider-case v1.0.2 -> v1.1.0 |
| test-014-spec-guider-parcours | 2 occurrences v1.0.2 -> v1.1.0 (adaptation Morpheus) |

## Lecons

1. L'outil detecter-divergences-version est le scan de reference spec vs py : 3 specs non bumpees ont ete alignees (combos-moteur, detecter-decalages, generateurs-case). Le seul DIVERGENT restant est le cas INVERSE (guider-parcours) : ce n'est pas une spec stale mais un py en retard -- observation pour une mission Vulcain (bump de code).
2. Les references historiques (ex: spec-combos-moteur v0.2.1 dans le py et la spec = version de la SPEC qui a etabli la regle) sont LEGITIMES et ne doivent pas etre confondues avec la version du catalogue (0.2.9).
3. Corriger une version dans une spec peut casser un test formel qui verifie le texte exact : la chaine Promethee (spec) -> Morpheus (test) -> Janus (controle) est la bonne reponse, et la non-regression complete confirme l'absence d'effet de bord.
