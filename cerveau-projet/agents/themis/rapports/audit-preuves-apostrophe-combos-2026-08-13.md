---
titre: Audit croise des preuves reelles apostrophe dans les combos
date: 2026-08-13
auditeur: Themis
verdict: VALIDE
---

# Audit croise : preuve du quoting des combos avec une raison a apostrophe

## Contexte

Morpheus a prouve par des tests reels (sandbox hors racine) que le quoting
des combos fonctionne avec une valeur a apostrophe.

## Verifications (8/8)

| Point | Verification | Resultat |
|---|---|---|
| T1a | generateurs-commande compose la commande avec guillemets doubles | VALIDE |
| T1b | shlex.split OK : raison en 1 argument intact | VALIDE |
| T1c | sans quoting : shlex.split ECHEC (preuve de necessite) | VALIDE |
| T2a | combos-moteur quote double : raison intacte dans la sortie | VALIDE |
| T2b | combos-moteur sans quote : KO 'Commande invalide' | VALIDE |
| T3 | sandbox nettoye (0 residu) | VALIDE |
| T4 | 0 residu a la racine (verifie en commande directe) | VALIDE |
| T5 | normes ASCII/LF (lecon Morpheus) | VALIDE |

## Verdict

**VALIDE** : le quoting fonctionne de bout en bout (generateur -> commande
composee -> shlex.split -> execution). Une raison a apostrophe arrive
intacte. Sans quoting, la commande echoue avant execution - le garde-fou
test-042 est justifie.
