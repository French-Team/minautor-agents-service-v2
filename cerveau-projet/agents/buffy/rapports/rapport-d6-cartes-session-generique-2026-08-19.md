# Rapport Buffy -- D6 : session-llm-1 -> <session> dans les 16 cartes

Date : 2026-08-19

## Corrections appliquees

| Element | Correction |
|---|---|
| 16 cartes de decision | `session-llm-1` -> `<session>` (75 occurrences, 0 restant) via editer-parcours --modifier-case |
| Versions | bump mineur sur chaque carte (ex: themis 0.5.0 -> 0.5.1, cerberus 0.5.4 -> 0.5.5) |
| 16 fiches agents | PARCOURS (vX.Y.Z) synchronisees (Pattern 14) |
| cartes-lock.json | resynchronise : 10 cartes avaient des empreintes obsoletes (etat fantome), + cerberus/vulcain apres modifs |
| marbre cerberus.c10/c14 | zones gravees modifiees avec validation UTILISATEUR + porte proteger-modifier-marbre (marbre-log journalise) |
| mermaid | 16 .mmd + 16 .svg + index resynchronises |

## Verification

- valider-cartes-decision --tous : 16/16 CONFORME
- bumper --tous : 0 incoherent
- ASCII/LF : purs (0 KO)
- test-001 : 11/11 (0 lien casse) ; test-024 : 17/17 ; test-058 CONFORME ; test-072 : 10/10 ; test-079 PROPRE ; test-098 : 7/7

## KO contextuels / pins a adapter par Morpheus

- test-057 points 12b/13 : KO contextuels car l agent actif de la session est buffy (verrou SEUL BUFFY laisse passer) -> redeviendront verts au prochain relais
- test-018 (5b), test-033 (3/4) : pinent la commande `activer session-llm-1 janus` -> doivent accepter `<session>`
- test-013 : cerberus 0.5.4 -> 0.5.5 ; test-016 : buffy 0.5.0 -> 0.5.1
- test-005 : generateurs-commande 0.2.6 -> 0.3.1 ; test-056 : proteger-verrou 0.4.0 -> 0.4.1 ; test-089 : detecter 0.1.0 -> 0.1.2 ; test-060 : analyser-tokens 0.1.1 -> 0.1.2

## Pre-existants (session llm-4, hors perimetre)

- 4 problemes de processus evaluer-processus (usages session llm-4 : combos-corriger-non-ascii, evaluer-progression, valider-conformite-ascii, valider-nommage)
- chrono orphelin session-llm-4/Vulcain (20:22:52, jamais ferme)
