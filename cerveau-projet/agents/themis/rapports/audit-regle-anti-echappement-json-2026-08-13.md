---
titre: Audit croise de la regle anti-echappement JSON des spawn_agents
date: 2026-08-13
auditeur: Themis
verdict: VALIDE
---

# Audit croise : regle anti-echappement JSON (protocole v0.2.0)

## Contexte

Buffy a documente la regle anti-echappement JSON dans
protocole-creation-scripts-temporaires v0.2.0 (section 'Commandes
spawn_agents : eviter les erreurs d echappement JSON').

## Verifications (9/9)

| Point | Verification | Resultat |
|---|---|---|
| T1a | Section 'Commandes spawn_agents' presente | VALIDE |
| T1b | Regle d or : write_file, jamais de commande inline | VALIDE |
| T1c | Cas a risque documentes | VALIDE |
| T1d | Procedure valide (rm -f dans la commande) | VALIDE |
| T1e | Piege test-024 auto-incrimination (commande directe) | VALIDE |
| T2 | Header protocole : version 0.2.0 | VALIDE |
| T3 | Index-regles-general mentionne echappement JSON | VALIDE |
| T4 | Normes ASCII strict + LF pur (2 fichiers) | VALIDE |
| T5 | Plus de 0.1.0 dans le header | VALIDE |

## Verdict

**VALIDE** : la regle est complete, documentee, referencee dans l index et
conforme aux normes. Aucun ecart.
