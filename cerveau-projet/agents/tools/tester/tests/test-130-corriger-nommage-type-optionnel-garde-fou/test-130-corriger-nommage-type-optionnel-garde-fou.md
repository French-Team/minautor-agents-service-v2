---
identite:
  type: test
  appartient_a: commun
  commun: true
---
# test-130-corriger-nommage-type-optionnel-garde-fou

**Numero** : 130
**Date** : 2026-09-05
**Agent** : morpheus (mission 475f36c7, inter-round suite 8ed06172 Vulcain)
**Domaine** : outils -- corriger-nommage v0.3.1

## Objet

Garde-fou du correctif corriger-nommage v0.3.1 : `--type` devient OPTIONNEL
avec auto-detection par le chemin, et les `.json` de parcours v2 ne sont
JAMAIS renommes. Le combo-combo-corriger-fichier (case c1) echouait en code 2
sur TOUT fichier car corriger-nommage exigeait `--type` sans le recevoir.

## Contexte

La case c1 de combo-corriger-fichier lancait corriger-nommage SANS `--type`
alors que l outil l exigeait (required) -> echec code 2 sur TOUT fichier passe
au combo (JSON de parcours comme .md), note corrections.md l.277 et jamais
traite. Correctif Vulcain (8ed06172) : `--type` optionnel + auto-detection par
chemin (agents/tools/ -> outil, agents/conventions/ -> convention,
protocole-* -> protocole, agents/<agent>/ -> agent) + garde anti-renommage par
extension (protocole/agent/convention = .md ; outil = .sh/.py/.md).

## Verifications (19 points)

1. Presence des 3 fichiers de l outil (.py, .sh, .md).
2. Sans `--type` sur un .md d outil (agents/tools/) : rc 0 (plus de code 2).
3. Sans `--type` sur un .json de parcours : rc 0.
4. AUCUN renommage du .json (aucun fichier .md cree a cote).
5. Auto-detection agents/tools/ -> outil.
6. Auto-detection agents/conventions/ -> convention.
7. Auto-detection protocole-* -> protocole.
8. Auto-detection agents/<agent>/ -> agent.
9. `--type` explicite outil .py -> rc 0 (comportement historique conserve).
10. Parite .sh : sans `--type` -> rc 0.
11. Combo-corriger-fichier sur .md -> rc 0 (FIN atteinte).
12. Combo-corriger-fichier sur .json -> rc 0 (FIN atteinte).
13-15. Normes ASCII 0/0 + LF pur sur .py/.sh/.md.
16. PREUVE NEGATIVE : .json sous agents/<agent>/ (classerait 'agent' par le
    chemin) NON renomme -- la garde d extension le protege.
17. PREUVE NEGATIVE : fichier hors agents (type non detectable) -> rc 0 sans
    renommage.

## Methodologie

- Hierarchie TEMPORAIRE (tmp-test130-*) avec copies factices sous
  agents/tools/, agents/conventions/, protocole-*, agents/<agent>/parcours/ :
  JAMAIS les vrais fichiers du cerveau.
- Le .json factice porte un JSON valide (les outils aval du combo ne le
  cassent pas).
- Executions reelles des binaires corriger-nommage (py et sh) et du combo
  (combos-moteur + definition-combo-corriger-fichier).
- Nettoyage du tmp en fin de test (0 residu).

## Resultat

**19 OK / 0 KO** (execution directe). Enregistre dans les registres du
lanceur (serie e) et profils-tests.json. Non-regression liee : test-001.
