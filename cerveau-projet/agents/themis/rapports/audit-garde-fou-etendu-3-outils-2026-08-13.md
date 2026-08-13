---
type: rapport-audit
agent: themis
date: 2026-08-13
objet: garde-fou anti-residus etendu aux 3 outils critiques
verdict: VALIDE
---

# Audit croise -- Garde-fou anti-residus etendu (guider-parcours, valider-cartes-decision, editer-parcours)

**Contexte** : extension du garde-fou anti-residus (cree dans activer-agent-principal
v0.5.2) aux outils qui s executent souvent. Buffy a ajoute verifier_residus_racine
(py) + regle documentee ; Morpheus a adapte les tests.

## Verifications (25/25 OK)

| # | Verif | Resultat |
|---|---|---|
| T1a-b | Garde-fou present dans les 3 .py (fonction + REGEX + VERSION + appel actions reelles) | 6/6 OK |
| T2 | Preuve sandbox positive + negative (3 outils) | 3/3 OK |
| T3a-d | Versions partout (py 0.5.1/0.4.1/0.1.1, .sh, docs + lignes versionning, spec guider Version outil 0.5.1) | 9/9 OK |
| T4a-d | test-028 8/8, test-012 18/18, test-024 13/13 (commande directe), normes 0/0 | 4/4 OK |
| T5a-c | Catalogue intact + JSON valide + parcours cerberus intact | 3/3 OK |

Note : T4c a d abord affiche KO (rc=1) car test-024 etait lance depuis un script
temporaire a la racine (artefact d auto-incrimination connu) - relance en COMMANDE
DIRECTE : 13/13 OK.

## Conclusion

VERDICT : VALIDE. Le garde-fou anti-residus couvre desormais 4 outils critiques
(activer-agent-principal + les 3 nouveaux), avec surveillance par la suite de
non-regression. Aucun impact sur les parcours ni le catalogue.
