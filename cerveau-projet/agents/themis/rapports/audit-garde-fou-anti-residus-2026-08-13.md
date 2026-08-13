---
type: rapport-audit
agent: themis
date: 2026-08-13
objet: garde-fou anti-residus v0.5.2 activer-agent-principal
verdict: VALIDE
---

# Audit croise -- Garde-fou anti-residus v0.5.2 (activer-agent-principal)

**Contexte** : mission de correction de la cause racine des residus 0.2.1/v0.2.6
(sorties accidentelles de reactiver redirigees vers des fichiers nommes comme des
versions). Buffy a ajoute verifier_residus_racine (py + sh) + regle documentee.

## Verifications (24/24 OK)

| # | Verif | Resultat |
|---|---|---|
| T1a-e | Garde-fou present py + sh, REGEX_RESIDU, declenchement actions reelles (pas aide/--version) | 5/5 OK |
| T2a-d | Preuve sandbox : positif py/sh (WARNING + action executee) + negatif (silence) | 4/4 OK |
| T3a-d | Section doc "Ne jamais rediriger la sortie" + ligne versionning 0.5.2 | 4/4 OK |
| T4a-e | Versions 0.5.2 partout (py, sh, doc, spec) + normes ASCII/LF 0/0 | 8/8 OK |
| T5a-c | test-007 22/22 VALIDE, test-039 4/4, registre usages a jour | 3/3 OK |

## Conclusion

VERDICT : VALIDE. Le garde-fou proactif empeche la recurrence de l accident
(visible immediatement au point d entree, avant commit) et test-039 reste la
surveillance reactive. Aucun impact sur les tests existants.
