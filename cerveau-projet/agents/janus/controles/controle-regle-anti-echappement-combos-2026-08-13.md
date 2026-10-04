---
titre: Controle croise final de la regle anti-echappement etendue aux combos
date: 2026-08-13
controleur: Janus
verdict: VALIDE
---

# Controle croise final : regle anti-echappement des commandes bash des combos

## Contexte

Buffy a etendu la regle anti-echappement aux commandes bash des combos :
combos-moteur.md v0.3.3 (section ECHAPPEMENT DES VALEURS) + protocole-
creation-scripts-temporaires v0.2.1 (section Commandes bash des combos).
Themis a audite (12/12 VALIDE).

## Verifications J1-J4 (7/7)

| Point | Verification | Resultat |
|---|---|---|
| J1a | Section ECHAPPEMENT DES VALEURS dans combos-moteur.md | VALIDE |
| J1b | Regle d or : quoter {var} | VALIDE |
| J1c | Bump 0.3.3 header + versionning | VALIDE |
| J2a | Protocole v0.2.1 | VALIDE |
| J2b | Section Commandes bash des combos | VALIDE |
| J3 | Moteur non modifie (doc seule, py 0.3.2) | VALIDE |
| J4 | Normes ASCII strict + LF pur (3 fichiers) | VALIDE |

## Non-regression complete (J5)

**41/41 OK** - chrono ameliore : 44.4 s (ancienne reference 44.5 s) ->
reference mise a jour. Aucun KO.

## Verdict

**VALIDE** : la regle est complete, documentee sans toucher au code, et la
non-regression complete passe avec 41/41 tests (record de temps).
