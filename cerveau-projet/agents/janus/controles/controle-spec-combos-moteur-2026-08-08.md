# Controle -- Spec-combos-moteur + Pattern 3 (Vulcain)

**Date** : 2026-08-08
**Agent controle** : Vulcain
**Session** : session-llm-1 (id: llm-1)

## Mission de controle (ecrite AVANT de controler -- Regle 1 Janus)

Controle du second controle apres l'etape 1 du plan combo-orchestrateur :
spec-combos-moteur creee (format definition-combo.json) + Pattern 3
(generateur -> execution) documente dans spec-guider-parcours v0.2.4.

## Points a verifier

| # | Point | Methode |
|---|---|---|
| 1 | spec-combos-moteur.001.01.ebauche.md creee dans combos/combos-moteur/spec/ | existence |
| 2 | Format definition-combo.json complet : objet combo (nom/version/case_depart), 4 types de cases (generateur AUTO via generateurs-commande --reponses, outil subprocess, controle branches, fin), variables memoire interne + persistant classeur, interpolation {var} | inspection |
| 3 | Modes CLI : --liste, --reponses, --dry-run, --version + parite py/sh + tests requis + livrables | inspection |
| 4 | Pattern 3 dans spec-guider-parcours v0.2.4 : section Patterns + procedure d audit point 3 + critere 11 | grep + inspection |
| 5 | Doc guider-parcours 0.2.10 + ref spec v0.2.4 + regle 8 | grep |
| 6 | Coherence : generateur INCHANGE (le moteur fait le lien avec --reponses) | inspection |
| 7 | ASCII 0 sur les 4 fichiers (spec-combos, spec-guider, doc, corrections vulcain) | valider-conformite-ascii |

## Verdict

**VERDICT : VALIDE (7/7)**

| # | Point | Resultat |
|---|---|---|
| 1 | spec-combos-moteur.001.01.ebauche.md creee dans combos/combos-moteur/spec/ | OK |
| 2 | Format definition-combo.json : case_depart x2, 4 types de cases (generateur x5, outil x2, controle x1, fin x3), mode AUTO x2, memoire interne, persistant x3, interpolation {var} x2 | OK |
| 3 | Modes CLI : --liste x5, --reponses x12, --dry-run x4, --version x3 + parite x2 + tests requis | OK |
| 4 | Pattern 3 dans spec-guider v0.2.4 (x8) : section ### Pattern 3 -- Combo + audit point 3 + 13 refs combos-moteur | OK |
| 5 | Doc guider-parcours 0.2.10 (x2) + ref (v0.2.4) + regle 8 (Pattern 3, v0.2.4) | OK |
| 6 | Generateur INCHANGE (le moteur fait le lien avec --reponses) documente | OK |
| 7 | ASCII 0 sur les 4 fichiers (spec-combos, spec-guider, doc, corrections vulcain) | OK |

**Lecon** :
1. grep interprete --liste comme une option : utiliser grep -cF -e "--liste" pour chercher une chaine commencant par --
2. Le combo devient l orchestrateur : le generateur INCHANGE est appele par le moteur avec --reponses (mode AUTO) -- c est la source de verite de la syntaxe
3. La spec-combos-moteur est le format du futur outil combos-moteur : declaratif (JSON) + moteur generique, meme philosophie que guider-parcours
