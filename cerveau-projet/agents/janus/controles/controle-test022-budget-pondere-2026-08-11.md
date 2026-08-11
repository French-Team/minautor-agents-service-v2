# Controle croise -- test-022-budget-pondere (Janus)

**Date** : 2026-08-11
**Mission** : controle croise du test-022-budget-pondere cree par Morpheus (mission Cerberus)
**Verdict** : **VALIDE**

## Points controles

| # | Controle | Resultat |
|---|---|---|
| J1 | Format py : non-ASCII 0, CRLF 0 | OK |
| J2 | Pertinence des cas limites : frontiere exacte 3,0 (3,0 OK / 3,5 KO / 4,0 KO), borne 100/101, plafond 160, refs/outils = 0,5 | OK |
| J3 | Execution reelle : 14/14 OK | OK |
| J4 | Catalogue : test-022 present, total 140, trie | OK |
| J5 | Normes doc md : non-ASCII 0, CRLF 0 | OK |
| J6 | Plage doc test-021.md -> test-001 a test-022 | OK |
| J7 | Non-regression complete : 22/22 OK | OK |

## Lecons

1. Le test-022 couvre la frontiere exacte 3,0 demandee par l utilisateur : 6 courts (3,0) CONFORME, 1 long + 4 courts (3,5) A ALLEGER, 4 longs (4,0) A ALLEGER.
2. Les bornes du seuil court sont testees (6 x 100 car. = 3,0 CONFORME ; 4 x 101 car. = 4,0 A ALLEGER) : la limite du seuil court est exacte.
3. Les indices sans texte (ref/outil) comptent 0,5 : 6 refs = 3,0 CONFORME -- coherence avec le modele implemente.
4. Le catalogue a ete mis a jour (140 commandes, insertion triee) et le test-007 (139->140) reverdi : la non-regression est complete.
