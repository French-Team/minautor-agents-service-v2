# Controle croise -- Renforcement du passage obligatoire par Janus

**Date** : 2026-08-13
**Controleur** : Janus (dernier maillon, active par Morpheus - regle respectee)
**Objet** : verifier le renforcement du passage obligatoire par Janus en fin de
mission de Morpheus (suite a la derive detectee)
**Verdict** : **VALIDE** (J1-J6 verts)

---

## J1 - Garde-fou test-033-passage-janus-obligatoire

- **9 OK / 0 KO** : carte c10/c14 = FIN - Activer Janus + commande exacte
  `activer session-llm-1 janus` (pas reactiver) + REGLE ABSOLUE dans la fiche
  + clause erronee retiree + normes

## J2 - Fiche morpheus.md

- REGLE ABSOLUE -- PASSAGE PAR JANUS : **presente** (1 occurrence)
- Clause erronee (Je ne reactive CERBERUS que si j ai ete active directement
  par Cerberus) : **0 occurrence (retiree)**

## J3 - Carte conforme (test-018)

- **13 OK / 0 KO** : la seule fin REACTIVER legitime reste janus (dernier
  maillon)

## J4 - Non-regression complete

- **33 OK / 0 KO** en **45.6 s** (pool-16) - temps ameliore, reference
  mise a jour automatiquement (56.2 s -> 45.6 s)

## J5 - Normes ASCII/LF

- test-033, lanceur, fiche, corrections : **0 non-ASCII / 0 CRLF**

## J6 - Lecons

- Lecon Morpheus enregistree (la fin suit la carte, jamais la consigne ;
  regle de fiche erronee = dette) - verifiee
- Lecon Janus precedente (derive) enregistree - verifiee

---

## Constat de cloture

La chaine est reparee : **Morpheus a bien ACTIVE Janus en fin de mission**
(commande activer session-llm-1 janus, conformement a sa carte c10/c14 et a la
nouvelle REGLE ABSOLUE). Le garde-fou test-033 rend le passage par Janus
verifiable automatiquement (anti-recurrence).

Rapport redige par Janus - dernier maillon : reactiver Cerberus avec le bilan.
