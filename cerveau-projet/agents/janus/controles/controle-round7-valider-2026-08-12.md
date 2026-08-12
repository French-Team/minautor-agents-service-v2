# Controle croise -- Round 7 : theme VALIDER (faux positifs/negatifs)

**Date** : 2026-08-12 | **Controleur** : Janus (session-llm-1) | **Agent corrige** : Vulcain
**Verificateur** : Morpheus (non-regression)

---

## Verdict : VALIDE (J1-J7 verts)

| # | Verification | Resultat |
|---|---|---|
| J1 | valider-case v1.1.1 : refs mortes detectees (py + sh + --case), parcours sain CONFORME | 4/4 OK |
| J2 | Versions alignees : valider-case 1.1.1 py/sh/md, cartes-decision 0.4.0 py/sh, liens 0.4.0-py, nommage 0.3.3 | 5/5 OK |
| J3 | valider-nommage v0.3.3 : categorie scannee (Total 40), tools/ 335/335 0 erreur (py + sh), dossier inexistant -> message clair | 4/4 OK |
| J4 | Renommage tester-lancer-non-regression : dossier + catalogue + 0 residu ancien nom | 3/3 OK |
| J5 | test-024 12/12 + non-regression complete 26/26 | OK |
| J6 | Catalogue 146 entrees triees, 0 doublon, dry-run 0 a ajouter, garde-fou 0 cle dupliquee | OK |
| J7 | Normes : ASCII 0 + LF pur sur 19 fichiers | 0/0 |

---

## Corrections verifiees (mesures reelles, pas lectures)

### A. valider-case v1.1.1 -- FAUX NEGATIF GRAVE corrige
Sur une copie de parcours-cerberus.json avec `suivant` -> `case-inexistante-xyz` :
avant : CONFORME rc=0 (silence). apres : NON CONFORME + message nommant la case
et la ref morte. Detecte aussi en mode `--case <id>` et via le wrapper .sh
(parite). La meme detection couvre les branches `vers`.

### B. Versions alignees (regle des 5 fichiers)
- valider-cartes-decision.sh 0.3.2 -> 0.4.0 (py/md deja 0.4.0)
- valider-liens.py 0.2.0-py -> 0.4.0-py (md/sh deja 0.4.0)

### C. valider-nommage v0.3.3 -- faux negatif silencieux corrige
`--recursive` sur une CATEGORIE (tools/valider/) rendait `Total: 0` (rien
scanne, on croit que tout est valide). Detection de categorie : un sous-dossier
outil a un .py/.sh a son nom -> profondeur de scan 1. Parite portee dans le
.sh (implementation parallele). `Total: 40` pour valider/ (13 outils x 3
fichiers).

### D. Faux positifs elimines + renommage (decision utilisateur)
- Formats speciaux LEGITIMES reconnus : combo-*.md, tester-*-v0xx.sh,
  rapport-*.md (regex etendue au suffixe date). Scan tools/ : 11 erreurs -> 0.
- RENOMMAGE COMPLET : lancer-non-regression -> tester-lancer-non-regression
  (dossier tester/ exige le prefixe tester-). Dossier deplace, fichiers
  renommes, catalogue/index-tools/test-024/protocole/auto-refs a jour.
  Remarque : le nouveau nom CONTIENT l ancien (piege de grep naif).

---

## Impacts sur la non-regression (adaptes par Morpheus)
- test-007 : le renommage en place avait casse le TRI du catalogue (tester-
  vient apres valider-) -> re-tri (146, trie, 0 doublon)
- test-009 / test-015 : version valider-case en dur v1.1.0 -> 1.1.1

## Fichiers modifies (19)
valider-case py/sh/md, valider-cartes-decision.sh, valider-liens.py,
valider-nommage py/sh/md, tester-lancer-non-regression py/md (renommes),
catalogue-commandes.json, test-024, test-009, test-015, test-007,
index-tools.md, protocole-creation-scripts-temporaires, corrections vulcain
et morpheus.

## Conclusion
Round 7 VALIDE. Le theme faux positifs/negatifs a produit la correction la plus
importante de la boite : un validateur qui repondait CONFORME sur une carte
cassee (ref morte) est desormais un vrai chien de garde. Les faux positifs
(11) et le faux negatif silencieux (Total 0) ont ete elimines. Le seul ecart de
nommage de la boite est corrige par renommage complet.
