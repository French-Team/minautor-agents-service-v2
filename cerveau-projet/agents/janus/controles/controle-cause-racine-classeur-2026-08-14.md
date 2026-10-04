---
identite:
  type: rapport
  appartient_a: commun
  commun: true
---
# Controle croise - Cause racine Classeur absent du README

Date : 2026-08-14
Controleur : Janus (second controle)
Agent controle : Buffy
Verdict : **VALIDE (17/17)**

## Contexte
L utilisateur a remarque que la section Classeur manquait au README public.
Cerberus a diagnostique la cause racine : 2 outils listaient TOUS les dossiers
de agents/ (sauf tools) comme agents (17 au lieu de 12), ce qui faisait
reinjecter 5 lignes cassees ('Selon sa carte de decision') dans la table des
agents du README a chaque passage du combo massif.

## Verifications (J1-J6)

| Point | Resultat |
|---|---|
| J1. Les 2 outils affichent Agents reels : 12 (etait 17) | OK |
| J1c. Aucun 'MANQUANT] Agent' pour les 5 concepts | OK |
| J2. py_compile + bash -n sur les 4 scripts | OK |
| J3. Normes ASCII 0 + LF pur sur les 6 fichiers | OK |
| J4. test-038 (badge README) : 7/7 | OK |
| J5. test-020 : 45 OK / 1 KO (KO = version 0.1.0 en dur, attendu) | OK |
| J6. Aucune reinjection apres relance du combo par test-020 | OK |

## Fichiers modifies (Buffy)
- outils/mettre-a-jour/mettre-a-jour-readme/ (py, sh, md) : v0.4.0 -> v0.4.1
- outils/combos/combos-analyse-projet/ (py, sh, md) : v0.1.0 -> v0.1.1
- fonction lister_agents_reels() et compter_agents() filtrent par parcours JSON

## Impacts
- KO attendu : test-020 'version combos-analyse-projet 0.1.0' (Morpheus adaptera)
- Prochaine etape : Clio retire les 5 lignes cassees du README public et ajoute
  la vraie section Classeur (classeur-variables, stockage partage).
