# Controle Janus -- combos-moteur (etape 2 plan combo-orchestrateur)

**Date** : 2026-08-08
**Controleur** : Janus (second controle apres Vulcain + Morpheus)
**Cible** : outil combos-moteur (py + sh + md + exemple-combo.json) + index-tools + fiche vulcain + test-002

---

## Mission de controle

Verifier que l'outil `combos-moteur` (moteur generique de combos declaratifs)
construit par Vulcain et teste par Morpheus (31/31 REUSSI) est conforme a la
spec-combos-moteur v0.1.0 et aux conventions du cerveau-projet.

## Verdict attendu

| # | Point | Attendu |
|---|---|---|
| 1 | combos-moteur.py | 4 types de cases + variables + interpolation + persistance + modes CLI + erreur variable manquante |
| 2 | combos-moteur.sh | Parite py/sh (python embarque, transmission $@, COMBO_MOTEUR_DIR) |
| 3 | combos-moteur.md | Documentation complete, version 0.1.0 |
| 4 | exemple-combo.json | 4 types de cases, commandes inoffensives |
| 5 | index-tools.md | combos-moteur dans Combos (4 combos) + total 82 |
| 6 | fiche vulcain | combos-moteur en P0 |
| 7 | test-002-combos-moteur | Cree dans tester/tests/ + verdict 31/31 |
| 8 | spec-combos-moteur | Referencee (v0.1.0) |
| 9 | corrections.md | Lecons Vulcain + Morpheus ajoutees |
| 10 | ASCII | 0 non-conforme sur tous les fichiers |
| 11 | generateurs-commande | INCHANGE |
| 12 | Combo pilote reel | NON cree (etape 3 = Buffy) |

---

## Resultats du controle

| # | Point | Resultat |
|---|---|---|
| 1 | combos-moteur.py : 4 types de cases (generateur/outil/controle/fin x2), modes --liste/--dry-run/--reponses/--verbose/--version, persistance persistant, erreur Variable non trouvee | [OK] |
| 2 | combos-moteur.sh : parite (COMBO_MOTEUR_DIR x2, PYEOF x2, python embarque) | [OK] |
| 3 | combos-moteur.md : doc complete (0.1.0 x7, definition-combo.json x12) | [OK] |
| 4 | exemple-combo.json : 4 types de cases, commandes echo inoffensives | [OK] |
| 5 | index-tools.md : combos-moteur ajoute, Combos 4, Total 82 | [OK] |
| 6 | fiche vulcain : combos-moteur en P0 | [OK] |
| 7 | test-002-combos-moteur cree (py + md) + verdict Morpheus 31/31 REUSSI | [OK] |
| 8 | spec-combos-moteur v0.1.0 referencee dans la doc | [OK] |
| 9 | Lecons Vulcain (Combos-moteur v0.1.0) + Morpheus (combos-moteur) dans corrections.md | [OK] |
| 10 | ASCII 0 non-conforme sur les 10 fichiers crees/modifies | [OK] |
| 11 | generateurs-commande INCHANGE (version 0.1.0-beta, logique intacte) | [OK] |
| 12 | Combo pilote reel NON cree (etape 3 = Buffy, pas de dossier combos pilote) | [OK] |

## Verdict final

**VALIDE (12/12)** -- combos-moteur conforme a la spec v0.1.0 et aux conventions. Test 31/31 REUSSI (Morpheus). Le generateur reste la source de verite (mode AUTO via --reponses), le moteur fait le lien. Etape 3 (combo pilote) = domaine Buffy.

## Lecons

1. La parite py/sh sur le chemin racine : 5 remontees depuis le fichier .py, 4 depuis le dossier .sh (via variable d'environnement) -- toujours compter le nombre de niveaux selon la base
2. L'extraction de la commande du generateur doit prendre la ligne SUIVANTE le marqueur === COMMANDE A LANCER === (le generateur imprime la commande sur la ligne apres)
3. Le test formel 31/31 confirme la couverture complete : liste, navigation, interpolation, generateur AUTO, controle branches, variable manquante, dry-run, parite, nommage, ASCII, syntaxe
