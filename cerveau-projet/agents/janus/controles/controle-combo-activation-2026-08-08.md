# Controle Janus -- combo pilote combo-activation (etape 3 plan combo-orchestrateur)

**Date** : 2026-08-08
**Controleur** : Janus (second controle apres Buffy)
**Cible** : cerveau-projet/combos/combo-activation/definition-combo.json

---

## Mission de controle

Verifier que le combo pilote `combo-activation` (cycle sidentifier -> activer ->
reactiver) cree par Buffy est conforme au format `definition-combo.json` de la
spec-combos-moteur v0.1.0 et fonctionne avec le moteur (teste sur copies).

## Verdict attendu

| # | Point | Attendu |
|---|---|---|
| 1 | Fichier existe | cerveau-projet/combos/combo-activation/definition-combo.json (fichier du cerveau, domaine Buffy) |
| 2 | Format spec v0.1.0 | Objet combo (nom/version/case_depart) + cases |
| 3 | Cycle complet | 3 generateurs (sidentifier/activer/reactiver) + 3 outils + 1 controle + 1 fin |
| 4 | Interpolation | {cmd1}/{cmd2}/{cmd3} entre generateur et outil |
| 5 | JSON + ASCII | JSON valide + 0 non-ASCII |
| 6 | --liste | 8 cases affichees |
| 7 | --dry-run | Commandes composees par generateur AUTO, navigation jusqu'a fin |
| 8 | Execution sur copies | Cycle Cerberus -> Buffy -> Cerberus dans la copie AGENTS.md |
| 9 | Vrais fichiers | Intacts (le test n'a touche que les copies) |
| 10 | Lecon Buffy | Notee dans corrections.md |
| 11 | Moteur + generateur | INCHANGES |
| 12 | Dossier combos | cerveau-projet/combos/ cree (nouvelle racine) |

---

## Resultats du controle

| # | Point | Resultat |
|---|---|---|
| 1 | Fichier existe : cerveau-projet/combos/combo-activation/definition-combo.json | [OK] |
| 2 | Format spec v0.1.0 : objet combo (nom/version/case_depart x1, combo-activation x3) | [OK] |
| 3 | Cycle complet : 3 generateurs (sidentifier/activer/reactiver x3) + 3 outils + 1 controle + 1 fin | [OK] |
| 4 | Interpolation {cmd1}/{cmd2}/{cmd3} x6 entre generateur et outil | [OK] |
| 5 | JSON valide + ASCII 0 non-conforme | [OK] |
| 6 | --liste : 8 cases affichees | [OK] |
| 7 | --dry-run : 6 commandes DRY-RUN (composees par generateur AUTO), navigation jusqu'a fin | [OK] |
| 8 | Execution sur copies : fin c8 atteinte, copie AGENTS.md = Cerberus (cycle complet verifie) | [OK] |
| 9 | Vrais fichiers intacts (janus, etat reel) - le test n'a touche que les copies | [OK] |
| 10 | Lecon Buffy notee dans corrections.md | [OK] |
| 11 | combos-moteur + generateurs-commande INCHANGES (versions 0.1.0-beta intactes) | [OK] |
| 12 | Dossier cerveau-projet/combos/ cree (nouvelle racine des combos, combo-activation dedans) | [OK] |

## Verdict final

**VALIDE (12/12)** -- le combo pilote combo-activation est conforme a la spec
v0.1.0 et fonctionne avec combos-moteur. Le cycle complet sidentifier -> activer
-> reactiver est execute sans effet sur les vrais fichiers (test sur copies).

## Lecons

1. Une DEFINITION de combo est un fichier du cerveau (domaine Buffy, racine cerveau-projet/combos/), le MOTEUR est un outil (domaine Vulcain, agents/tools/combos/combos-moteur/) -- meme distinction que parcours (Buffy) vs guider-parcours (Vulcain)
2. Le cycle d'activation complet en 8 cases : 3 generateurs + 3 outils + 1 controle + 1 fin -- le generateur AUTO compose les commandes exactes (quoter pour les raisons a espaces)
3. Le test sur copies (AGENTS_FILE/AGENTS_HISTORIQUE/CLASSEUR_STOCKAGE) est OBLIGATOIRE pour un combo qui modifie la session : verifier le retour Cerberus dans la copie, jamais sur les vrais fichiers
