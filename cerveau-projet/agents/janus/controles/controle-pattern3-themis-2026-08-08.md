# Controle -- Pattern 3 dans parcours-themis + combo-audit-themis

**Date :** 2026-08-08
**Agent controle :** Buffy (etape 5 plan combo-orchestrateur)
**Objet :** integration du Pattern 3 (spec-guider-parcours v0.2.4) dans le parcours pilote themis + creation du combo pilote combo-audit-themis

---

## Mission de controle

1. Combo cree : cerveau-projet/combos/combo-audit-themis/definition-combo.json
2. Structure du combo : 9 cases (2 generateurs, 6 outils directs, 1 fin)
3. Parcours themis v0.2.0 : 24 cases -> 17, c4-c7 supprimes
4. c3 = case combo Pattern 3 (combos-moteur + definition)
5. c19 RVAV recable vers c3, zero reference morte vers c4-c7
6. json.load OK sur les 2 fichiers
7. guider-parcours --liste : 17 cases
8. guider-parcours --reponses : 4 chemins PARCOURS TERMINE
9. ASCII 0 sur combo + parcours + corrections buffy
10. Parite py/sh combos-moteur OK
11. Moteur + catalogue + generateur INCHANGES
12. Lecon Buffy notee dans corrections.md

## Verdict

**VALIDE (12/12)**

## Resultats

1. Combo cree : cerveau-projet/combos/combo-audit-themis/definition-combo.json -- OK
2. Structure : 9 cases (2 generateurs audit-general + combos-valider-cerveau, 6 outils directs dont 4 uniques, 1 fin) -- OK
3. Parcours themis v0.2.0 : 17 cases (24 avant), c4-c7 supprimes -- OK
4. c3 = case combo Pattern 3 (combos-moteur + definition + indice regle) -- OK
5. c19 RVAV recable vers c3 ; zero ref morte c4-c7 (vers ET suivant vides) -- OK
6. json.load OK sur les 2 fichiers -- OK
7. guider-parcours --liste : 17 cases -- OK
8. guider-parcours --reponses : 4 chemins PARCOURS TERMINE (audit, doute, rvav, autre) -- OK
9. ASCII 0 sur combo + parcours + corrections buffy -- OK
10. Parite py/sh combos-moteur OK -- OK
11. Moteur + catalogue + generateur INCHANGES (dates etapes 2/4, non touches) -- OK
12. Lecon Buffy notee dans corrections.md -- OK

## Remarques

- Le combo audit-themis mixe 2 generateurs AUTO (audit-general, combos-valider-cerveau via catalogue) et 4 outils directs (valider-relecture, valider-tableaux, detecter-local-hors-fonction, detecter-usage-outils-externes) -- le pattern generateur -> execution est respecte
- valider-nommage --type outil ne s'applique pas aux definitions-combo.json (fichiers JSON, pas des outils) -- la validation de definition se fait par json.load + ASCII + --liste + --dry-run
- Le parcours themis passe de 24 a 17 cases : le chemin audit devient c2 -> c3 combo -> c8 verdict (plus lisible, objectif du combo)
