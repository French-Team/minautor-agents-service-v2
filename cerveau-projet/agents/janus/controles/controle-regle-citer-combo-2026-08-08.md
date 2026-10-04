# Controle -- Regle CITER le combo avant de le lancer (Buffy)

**Date** : 2026-08-08
**Controleur** : Janus (second controle)
**Objet** : regle de tracabilite -- l'agent qui lance un combo le CITE avant de l'executer.

---

## Mission de controle

Verifier les points suivants :

1. Source de verite : protocole-creation-combos v0.1.1 section 9.5 + spec protocole EX-09
2. spec-combos-moteur + doc moteur 0.1.2 portent la regle
3. Indice CITER en tete des 6 cases combo (themis c3, janus c5/c22, vulcain c7/c13, buffy c28)
4. json.load OK sur les 4 parcours
5. ASCII 0 sur les 8 fichiers modifies/crees
6. Navigation inchangee : 6/6 chemins traversant les combos -> PARCOURS TERMINE
7. Liens valides sur les 4 fichiers a liens
8. Lecon Buffy notee dans corrections.md

## Resultats

### Point 1 -- Source de verite protocole

OK. protocole-creation-combos v0.1.1 : section 9.5 Regles d'utilisation et tracabilite avec la REGLE CITER LE COMBO AVANT DE LE LANCER + format + exemple (3 occurrences). spec-protocole v0.1.1 : exigence EX-09 (citation obligatoire avant lancement) + flux 5.4 mis a jour. Versions 0.1.1 dans les 2 fichiers.

### Point 2 -- Spec-combos-moteur + doc moteur

OK. spec-combos-moteur : section Regle d'utilisation : citer le combo avant de le lancer (1 occurrence). combos-moteur.md v0.1.2 : REGLE TRACABILITE + ligne versionning ajoutee (3 occurrences de TRACABILITE/0.1.2).

### Point 3 -- Indice CITER dans les 6 cases combo

OK. Les 6 cases combo portent l'indice regle CITER en POSITION 1 (verifie par script structurel : type regle + texte commence par REGLE TRACABILITE) : themis c3, janus c5, janus c22, vulcain c7, vulcain c13, buffy c28. La regle est vue juste avant de lancer, comme le rappel ASCII (Pattern 2).

### Point 4 -- json.load 4 parcours

OK. themis 17, janus 24, vulcain 19, buffy 34 cases -- JSON valides.

### Point 5 -- ASCII 8 fichiers

OK. 0 caractere non-ASCII sur les 9 fichiers verifies (4 parcours + protocole + spec protocole + doc moteur + spec moteur + corrections Buffy).

### Point 6 -- Navigation 6 chemins

OK. 6/6 chemins traversant les combos -> PARCOURS TERMINE : themis audit, janus outil + modification, vulcain construire + modifier, buffy controler. Navigation inchangee malgre l'ajout des indices.

### Point 7 -- Liens

OK. Liens invalides : 0 sur les 4 fichiers a liens (protocole, spec protocole, doc moteur, spec moteur).

### Point 8 -- Lecon Buffy

OK. Lecon [NOTES] Regle CITER le combo avant de le lancer 2026-08-08 ajoutee : double ancrage documente (source de verite + rappel en tete des cases), formulation uniforme de citation, position 1 des indices, validation complete.

---

## Verdict

**VALIDE (8/8).** La regle de tracabilite CITER le combo avant de le lancer est correctement integree : source de verite dans le protocole (9.5) et la spec (EX-09) + spec-combos-moteur + doc moteur 0.1.2, rappel operationnel en tete des 6 cases combo des parcours (position 1), navigation inchangee (6/6 chemins TERMINE), JSON valides, ASCII 0, liens 0 invalide, lecons documentees. Les agents verront la regle juste avant de lancer chaque combo, et l'utilisateur pourra voir quel combo est utilise.
