# Rapport Buffy -- Correction carte themis (D2 + D5)

**Date** : 2026-08-19
**Mission** : corriger la carte themis signalee par le rapport d'audit Themis (rapport-audit-tokens-vulcain-2026-08-19.md), activee par Vulcain.
**Chaine** : Vulcain -> Buffy -> Vulcain

## Corrections appliquees

### D2 -- chemins c3/c25 (combo audit-themis)
- Avant : `cerveau-projet/combos/combo-audit-themis/definition-combo.json` (INEXISTANT)
- Apres : `cerveau-projet/agents/tools/combos/combo-audit-themis/definition-combo.json` (reel)
- Via editer-parcours --modifier-case c3 + c25

### D5 -- outils d'audit absents (DECLARATION_FAUTIVE)
- Ajoute aux indices de c17 (Croiser avec relecture et tableaux) :
  - `evaluer-processus` (commande --agent <agent>)
  - `valider-cartes-decision` (commande --agent <agent>)
- Via editer-parcours --modifier-case c17

### Version + synchro
- Bump parcours : 0.5.0 -> 0.5.1 (editer-parcours --bump)
- Fiche themis.md : PARCOURS (v0.5.0) -> PARCOURS (v0.5.1) (Pattern 14)
- .mmd/.svg resynchronises : convertir-carte-mermaid --agent themis --svg

## Verifications

| Controle | Resultat |
|---|---|
| valider-cartes-decision --tous | 16/16 CONFORME |
| verifier-conformite-fiche --agent themis | 1 CONFORME / 0 ECART |
| evaluer-processus --agent themis | 0 probleme (DECLARATION_FAUTIVE RESOLUES) |
| test-058 (seul Buffy corrige les cartes) | 6/6 CONFORME |
| test-013 / test-016 / test-006 | 22/22 / 20/20 / VALIDE |
| convertir-carte-mermaid --verifier | 16/16 synchronisees |
| test-067 (bumper) | PROPRE |
| ASCII/LF | parcours + fiche + mermaid purs |
| evaluer-processus --agent buffy | 0 probleme |
| registre | 805 lignes, 0 inversion |

## Note

D1 (combo audit-themis + catalogue-commandes) a ete corrige par Vulcain avant cette mission : c'est lui qui a rendu les chemins de la carte themis valides (le couple carte+combo etait mutuellement incoherent).
