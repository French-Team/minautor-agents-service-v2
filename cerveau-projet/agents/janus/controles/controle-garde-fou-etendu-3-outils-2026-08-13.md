---
type: rapport-controle
agent: janus
date: 2026-08-13
objet: garde-fou anti-residus etendu aux 3 outils critiques
verdict: VALIDE
---

# Controle croise final -- Garde-fou anti-residus etendu (guider-parcours, valider-cartes-decision, editer-parcours)

**Objet** : extension du garde-fou anti-residus (activer-agent-principal v0.5.2) aux
3 outils critiques qui s executent souvent.

## Verifications

| # | Verif | Resultat |
|---|---|---|
| J1 | Garde-fou present dans les 3 .py + versions 0.5.1/0.4.1/0.1.1 + spec guider Version outil 0.5.1 | 4/4 OK |
| J2 | Preuve sandbox positive + negative (3 outils) | 3/3 OK |
| J3 | test-028 8/8, test-012 18/18, normes 0/0 | 3/3 OK |
| J4 | Docs : versions + lignes versionning GARDE-FOU ANTI-RESIDUS (3 docs) | 3/3 OK |
| J5 | NON-REGRESSION COMPLETE : 40/40 OK (45.6 s, +2% vs reference 44.7 s) | OK |

## Bilan

Le garde-fou anti-residus couvre desormais 4 outils critiques (activer-agent-principal,
guider-parcours, valider-cartes-decision, editer-parcours) - les 3 nouveaux via le
pattern auto-contenu (duplication du helper). Les .sh wrappers purs sont couverts par
le .py. Tests adaptes par Morpheus (test-028, test-012, test-024) tous verts.

## Conclusion

VERDICT : VALIDE. La classe d accident "redirection de sortie vers fichier semver" est
desormais detectee au point d entree de TOUS les outils critiques + surveillee par
test-039 (racine) et la non-regression.
