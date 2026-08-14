---
titre: Audit des commandes des combos (variables quotees)
date: 2026-08-13
auditeur: Cerberus
verdict: AUCUN ECART
---

# Audit : les commandes des combos quotent-elles leurs variables ?

## Contexte

Demande utilisateur : verifier les 52 commandes des combos existantes et
corriger celles qui ne quotent pas leurs variables. Suite de la mission
test-042 (8 commandes deja corrigees : {fichier} -> '{fichier}').

## Verifications

| Point | Verification | Resultat |
|---|---|---|
| 1 | Definitions-combo.json : 14 (toutes dans agents/tools/combos/) | OK |
| 2 | Cases avec commande : 51 (toutes de type outil) | OK |
| 3 | Commandes = exactement {var} (commandes entieres generees) : 22 | OK (ne pas quoter) |
| 4 | Commandes sans variable : 21 | OK |
| 5 | Commandes avec {var} NON quote en argument : **0 restante** | OK (8 corrigees par test-042) |
| 6 | .sh des combos : {BLUE}/{RED}/{NC} = variables bash ${...} (couleurs), {var} dans combos-moteur.sh = exemples documentaires | OK (hors perimetre) |
| 7 | Entrees des cases generateur (16) : passent par composer_valeur qui quote si espace ou quoter:true (5 parametres deja quotes : raison activer/reactiver, paire1/paire2 remplacer-texte, contenu remplir-pense-bete) | OK |
| 8 | test-042 (garde-fou) : 4/4 OK, non-regression 42/42 OK | OK |

## Verdict

**AUCUN ECART** : toutes les commandes des combos sont conformes. Les 8
commandes non conformes ont ete corrigees dans la mission test-042 ; le
garde-fou test-042 surveille en permanence (tout futur {var} non quote
serait signale a la non-regression). Aucune nouvelle correction necessaire.
