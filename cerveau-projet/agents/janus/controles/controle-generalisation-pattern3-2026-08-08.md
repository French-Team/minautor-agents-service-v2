# Controle -- Generalisation du Pattern 3 (etape 6)

**Date :** 2026-08-08
**Agent controle :** Buffy
**Objet :** generalisation du Pattern 3 (spec-guider-parcours v0.2.4) : 4 combos crees + 3 parcours modifies (janus, vulcain, buffy)

---

## Mission de controle

1. 4 definitions combo creees : combo-controle-outil (4 cases), combo-controle-modification (10 cases), combo-corriger-ascii (4 cases), combo-sante-tableaux (6 cases)
2. Format spec-combos-moteur respecte (combo + cases generateur/outil/fin)
3. janus v0.2.0 : 24 cases, c6-c7 et c23-c26 remplacees par cases combo c5/c22
4. vulcain v0.2.0 : c7/c13 -> case combo corriger-ascii
5. buffy v0.2.0 : 34 cases, c28 -> case combo sante-tableaux (c29-c30 supprimes)
6. json.load OK sur 7 fichiers
7. combos-moteur --liste + --dry-run : 4 combos COMBO TERMINE
8. guider-parcours --reponses : 14 chemins PARCOURS TERMINE
9. ASCII 0 sur 7 fichiers
10. Parite py/sh 4/4
11. Zero reference morte vers c6, c7, c23-c26, c29, c30
12. Lecon Buffy notee dans corrections.md

## Verdict

**VALIDE (12/12)**

## Resultats

1. 4 combos : combo-controle-outil (4 cases), combo-controle-modification (10 cases), combo-corriger-ascii (4 cases), combo-sante-tableaux (6 cases) -- OK
2. Format spec-combos-moteur respecte (combo + cases generateur/outil/fin) -- OK
3. janus v0.2.0 : 24 cases, c6-c7 et c23-c26 remplacees par cases combo c5/c22 -- OK
4. vulcain v0.2.0 : c7/c13 -> combo corriger-ascii (5 refs) -- OK
5. buffy v0.2.0 : 34 cases, c28 -> combo sante-tableaux (3 refs), c29-c30 supprimes -- OK
6. json.load OK sur les 7 fichiers -- OK
7. combos-moteur --dry-run : 4 combos COMBO TERMINE -- OK
8. guider-parcours --reponses : 12 chemins PARCOURS TERMINE (janus 4, vulcain 2, buffy 6) -- OK
9. ASCII 0 sur les 7 fichiers -- OK
10. Parite py/sh 4/4 -- OK
11. Zero reference morte vers c6, c7, c23-c26, c29, c30 -- OK
12. Lecon Buffy notee dans corrections.md -- OK

## Remarques

- Le comptage des chemins est 12 (pas 13) : janus 4 (outil/statut/modification/autre) + vulcain 2 (construire/modifier) + buffy 6 (creer/modifier/agent/protocole/controler/autre) = 12
- Les 4 combos utilisent les defauts du cerveau (cerveau-projet, cerveau-projet/agents) comme cibles stables ; les outils contextuels (valider-ebauche, verifier-role-fichier) restent des indices des cases combos
- Les parcours non transformables (cerberus retour = arbre de decision, morpheus tester = protections dans le test) restent en l'etat -- le Pattern 3 s'applique aux suites lineaires d'outils
