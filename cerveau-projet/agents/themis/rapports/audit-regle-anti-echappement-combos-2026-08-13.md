---
titre: Audit croise de la regle anti-echappement etendue aux combos
date: 2026-08-13
auditeur: Themis
verdict: VALIDE
---

# Audit croise : regle anti-echappement des commandes bash des combos

## Contexte

Buffy a etendu la regle anti-echappement aux commandes bash des combos :
combos-moteur.md v0.3.3 (section ECHAPPEMENT DES VALEURS) + protocole-
creation-scripts-temporaires v0.2.1 (section Commandes bash des combos).

## Verifications (12/12)

| Point | Verification | Resultat |
|---|---|---|
| T1a | Section ECHAPPEMENT DES VALEURS dans combos-moteur.md | VALIDE |
| T1b | Regle d or : quoter {var} | VALIDE |
| T1c | Exemples MAUVAIS/BON | VALIDE |
| T1d | Cas apostrophe + shlex.split documente | VALIDE |
| T1e | Bump 0.3.3 header | VALIDE |
| T1f | Ligne versionning 0.3.3 | VALIDE |
| T2a | Protocole v0.2.1 | VALIDE |
| T2b | Section Commandes bash des combos | VALIDE |
| T2c | Regle shlex.split + quoter dans le protocole | VALIDE |
| T3 | Normes ASCII strict + LF pur (2 fichiers) | VALIDE |
| T4 | Aucune version fige cassee (0.3.2 non fige) | VALIDE |
| T5 | Moteur inchange (doc seule, py VERSION 0.3.2) | VALIDE |

## Verdict

**VALIDE** : la regle est complete, documentee dans la doc du moteur et le
protocole, sans modification du code. Aucun ecart.
