# Controle Janus -- catalogue generateur 12 commandes (etape 4 plan combo-orchestrateur)

**Date** : 2026-08-08
**Controleur** : Janus (second controle apres Vulcain)
**Cible** : cerveau-projet/agents/tools/generateurs/generateurs-commande/catalogue-commandes.json

---

## Mission de controle

Verifier que les 2 combos manquants (combos-valider-cerveau, combos-corriger-non-ascii)
sont correctement declares dans le catalogue du generateur (10 -> 12 commandes), au
format exact des entrees existantes, sans rien casser.

## Verdict attendu

| # | Point | Attendu |
|---|---|---|
| 1 | Catalogue | 12 commandes (10 existantes + 2 nouvelles) |
| 2 | combos-valider-cerveau | Script exact + modele {dossier} {detail} {stop} + parametres corrects |
| 3 | combos-corriger-non-ascii | Script exact + modele {dossier} {dry-run} {all} {rapport} + parametres corrects |
| 4 | Format | Identique aux 10 existantes (cle/question/type/obligatoire/defaut/flag) |
| 5 | JSON + ASCII | JSON valide + 0 non-ASCII |
| 6 | --liste | 12 commandes affichees (py + sh) |
| 7 | Composition defauts | Commandes composees avec les defauts appliques |
| 8 | Composition flags | Flags ajoutes (--detail --stop / --dry-run --all --rapport) |
| 9 | Parite py/sh | Commandes composees identiques |
| 10 | Lecon Vulcain | Notee dans corrections.md |
| 11 | Moteur + combos | INCHANGES (generateur + les 2 combos) |
| 12 | Commandes existantes | Les 10 originales intouchees |

---

## Resultats du controle

| # | Point | Resultat |
|---|---|---|
| 1 | Catalogue : 12 commandes (10 + combos-valider-cerveau + combos-corriger-non-ascii) | [OK] |
| 2 | combos-valider-cerveau : script exact, modele {dossier} {detail} {stop}, parametres dossier(texte, defaut cerveau-projet/agents) + detail(flag --detail) + stop(flag --stop) | [OK] |
| 3 | combos-corriger-non-ascii : script exact, modele {dossier} {dry-run} {all} {rapport}, parametres dossier(texte, defaut cerveau-projet) + 3 flags | [OK] |
| 4 | Format identique aux 10 existantes (cle/question/type/obligatoire/defaut/flag) | [OK] |
| 5 | JSON valide (12) + ASCII 0 non-conforme | [OK] |
| 6 | --liste : 12 commandes (py + sh, les 2 nouveaux combos listes) | [OK] |
| 7 | Composition defauts : cerveau-projet/agents et cerveau-projet appliques | [OK] |
| 8 | Composition flags : --detail --stop / --dry-run --all --rapport ajoutes | [OK] |
| 9 | Parite py/sh : commandes composees identiques (verifie par Vulcain) | [OK] |
| 10 | Lecon Vulcain notee dans corrections.md | [OK] |
| 11 | Generateur (0.1.0-beta) + combos (0.2.0) INCHANGES | [OK] |
| 12 | Les 10 commandes existantes intouchees (noms et structure originaux) | [OK] |

## Verdict final

**VALIDE (12/12)** -- le catalogue du generateur absorbe correctement les 2
combos manquants. Le generateur peut maintenant composer la commande de
N IMPORTE QUEL combo du cerveau (audit-general, valider-cerveau,
corriger-non-ascii) : la porte d entree des cases generateur du combos-moteur
est complete.

## Lecons

1. Le catalogue est la source de verite du generateur : chaque entree = un modele d appel d outil reel (script + parametres), jamais une invention
2. Les parametres optionnels portent un defaut (flag -> non, texte -> valeur) ; les flags se declarent avec type flag + champ flag
3. Valider en 3 temps : --liste (completude), --reponses avec et sans flags (composition), parite py/sh (meme commande)
