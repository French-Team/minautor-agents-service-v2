# CONTROLE DEVIATION 3 LOTS - 2026-08-24

## Mission de controle (ecrite AVANT, regle 1)

Controle du bilan consolide de la deviation Pattern 7 (3 lots) :
1. **CARTES** : buffy 0.5.6 (+detecter-residus, +corriger-fins-de-ligne en c14), morpheus 0.5.8 (+valider-conformite-ascii en c7) - editer-parcours, Pattern 14 fiche sync, lock a jour.
2. **OUTIL** : mettre-a-jour-readme 0.4.5 - verifier()/dry_run() py+sh adaptes a la nouvelle norme README public (badge Outils-N + compteurs via readme-dev).
3. **README-DEV** : categorie Git (hades-contexte-git) ajoutee au tableau section 6 - somme 165 = total 165.

## Verifications prevues
- valider-cartes-decision buffy + morpheus : CONFORME
- Versions outil coherentes py/sh/md (0.4.5)
- verifier readme : [OK] somme 165
- Registres usages (buffy, vulcain, morpheus, clio)
- ASCII des fichiers modifies

## Verdict : (a remplir)

## VERIFICATIONS EXECUTEES

### CONFORMES
1. **Cartes** : valider-cartes-decision buffy CONFORME (0.5.6, fiche PARCOURS sync) + morpheus CONFORME (0.5.8) - Pattern 14 OK.
2. **Outils** : mettre-a-jour-readme 0.4.5 coherent py/sh/md (0.4.5-py / 0.4.5 / 0.4.5).
3. **Readme-dev** : verifier [OK] 40 categories, somme 165 = total reel 165 (categorie Git ajoutee).
4. **ASCII** : 0/0 sur les 6 fichiers modifies (readme-dev, py, sh, md, 2 cartes JSON).
5. **Registres** : buffy (11 usages direct 07:02), vulcain (07:00), morpheus (06:58) complets pour la deviation.
6. **Lecons** : buffy x2, vulcain, morpheus enregistrees BDD + corrections.md (ASCII 0).

### DEFAUT D1 (perimetre mission Clio)
- **Registre Clio INCOMPLET pour la mission P1 (24/08)** : aucun usage declare pour guider-parcours, lire-fichier, lire-activite-recente, combos-moteur, editer-fichier (bloque). Lecon P1 manquante (ni corrections.md ni BDD).
- Contexte : Clio a ete activee pour P1 mais editer-fichier VERROUILLE pour elle -> redirection verrou vers buffy (habilitee) qui a applique la ligne Git. Clio a donc fait du diagnostic (verifier, combo) sans correction effective - mais ses usages d outils de demarrage/analyse auraient du etre declares (convention).

## VERDICT : A REVOIR (1 defaut mineur D1 - registre Clio incomplet + lecon P1 manquante)

## PRE-CONTROLE (avant boucle KO)
- Agent habilite pour reparer D1 : Clio (complete SON registre + sa lecon).

## RE-CONTROLE (apres inter-round Clio)

- D1 RE-CONTROLE : registre clio COMPLET pour la mission P1 (9 usages 24/08 dont guider-parcours, lire-fichier, lire-activite-recente, combos-moteur, mettre-a-jour-readme + enregistrer-lecon/usage). Lecon P1 ecrite BDD + corrections.md (ASCII 0).
- VERDICT FINAL : VALIDE (0 defaut restant).

## POINTS HORS PERIMETRE A SIGNALER
- P-A : Clio n est pas habilitee a editer-fichier (verrou) -> redirection vers buffy pour les corrections ciblees hors mettre-a-jour-readme. A surveiller : soit ajouter editer-fichier aux habilitations clio, soit accepter la redirection systematique (decision Cerberus/utilisateur).
