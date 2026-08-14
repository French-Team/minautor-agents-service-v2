---
titre: Controle croise final des preuves reelles apostrophe dans les combos
date: 2026-08-13
controleur: Janus
verdict: VALIDE
---

# Controle croise final : preuve du quoting des combos (raison a apostrophe)

## Contexte

Morpheus a prouve par des tests reels (sandbox hors racine) que le quoting
des combos fonctionne avec une valeur a apostrophe. Themis a audite
(8/8 VALIDE).

## Verifications J1-J4 (5/5)

| Point | Verification | Resultat |
|---|---|---|
| J1a | generateurs-commande : commande composee avec guillemets doubles | VALIDE |
| J1b | shlex.split : raison en 1 argument intact | VALIDE |
| J2a | combos-moteur quote : raison intacte dans la sortie | VALIDE |
| J2b | combos-moteur sans quote : KO 'Commande invalide' | VALIDE |
| J3 | 0 residu a la racine (commande directe) | VALIDE |
| J4 | normes ASCII/LF 0/0 (2 fichiers) | VALIDE |

## Non-regression complete (J5)

**42/42 OK** - chrono ameliore : 44.6 s (ancienne reference 45.9 s) ->
reference mise a jour. Aucun KO.

## Verdict

**VALIDE** : le quoting fonctionne de bout en bout. Une raison a apostrophe
arrive intacte ; sans quoting, la commande echoue avant execution. Le
garde-fou test-042 est justifie et operationnel.
