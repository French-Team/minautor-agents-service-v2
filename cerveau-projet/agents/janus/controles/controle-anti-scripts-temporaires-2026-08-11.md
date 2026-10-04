# Controle croise : Chaine anti-scripts-temporaires

**Date** : 2026-08-11
**Controleur** : Janus (second controle independant)
**Chaine** : Cerberus -> Vulcain -> Morpheus -> Buffy -> Promethee -> Morpheus (2e) -> Janus
**Verdict** : **VALIDE**

---

## Contexte

L'utilisateur a constate que les agents preferent les scripts temporaires
jetables (`.zz-*` / `.tmp-*` a la racine) a nos outils, au point que le
registre d'usage restait a 0 ligne. Demandes : utiliser la tracabilite pour
detecter ce contournement, creer les outils manquants, renforcer le Pattern
outil-temporaire.

## Points verifies

### J1. Les 3 outils + registre enrichi
- `lancer-non-regression` v0.1.0 (tester/) : lance tous les tests, bilan OK/KO fiable, registre protege
- `editer-parcours` v0.1.0 (editer/) : insertion/retrait case + re-pointage + bump, dry-run/backup
- `detecter-usage-scripts-temporaires` v0.1.0 (detecter/) : scan racine/git/lecons + croisement registre
- `enregistrer-usage-outil` v0.2.0 : nouveau mode `script-temporaire`
- Catalogue : 142 -> 145 commandes. Index-tools : +4 lignes (3 outils + editer-fichier-agents qui manquait)

### J2. Les 10 fins outil-temporaire renforcees
athena c20d, atlas c29d, buffy c35d, clio c15d, janus c29d, minerve c20d,
morpheus c16d, promethee c20d, themis c23d, vulcain c18d :
- indice outil `enregistrer-usage-outil` PASSE PAR LE GENERATEUR
- regle DECLARATION (93 car, <= 160) : 10/10, poids 1.0 <= 3.0

### J3. editer-parcours branche dans buffy c10b
10/10 fins + editer-parcours present dans la case de modification de parcours.

### J4. valider-cartes-decision
11/11 agents CONFORMES (0 non conforme). Les ecarts vulcain/clio restants = preexistants.

### J5. Garde-fou + non-regression
- test-024-scripts-temporaires : 12/12 OK. **PREUVE RELLE** : pendant le
  controle, mon propre script temporaire de verification (`.zz-janus-j3-j6.py`)
  a ete detecte par le garde-fou (1 KO), puis tout est revenu vert apres
  suppression - le dispositif fonctionne exactement comme prevu.
- Non-regression complete : 24/24 OK, registre 0 ligne (via l OUTIL lancer-non-regression).

### J6. Protocole creation-scripts-temporaires
v0.1.0 ebauche, format 7 sections (Objectif, Prerequis, Etapes, RVAV,
Exemples, Pieges courants, Liens), reference dans index-regles-general.md,
ASCII 0 / LF 0.

## Verdict

**VALIDE** - la chaine anti-scripts-temporaires est complete et operationnelle :
CREER (generateurs-outil-temporaire) -> DECLARER (enregistrer-usage-outil mode
script-temporaire) -> SUPPRIMER (0 residu) -> DETECTER (detecter-usage-scripts-
temporaires + test-024 garde-fou). Le cycle repond directement a la question de
l'utilisateur : ou et pourquoi les agents preferent les scripts temporaires.

## Observations

- Les ecarts vulcain (c9e/c15e non joignables, c6c/c12c 198 car) et clio
  (c6c 175 car) sont PREEXISTANTS (confirme via git HEAD dans les missions
  precedentes) - hors perimetre.
