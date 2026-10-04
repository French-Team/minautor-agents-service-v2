# Controle non-regression -- 2026-08-21

**Controleur** : Janus
**Contexte** : controle final de la chaine d'outils (garde-fou activer-agent-principal
+ tests). Non-regression complete lancee depuis l etat du working tree.

---

## BILAN GLOBAL

Non-regression complete : **77 OK / 20 KO** au premier passage.

Apres mes reparations immediates (pins de tests obsoletes + registre + bumper) :
les KO passes de **20 a 11**, tous les 11 restants etant des **defauts de cartes**
(domaine Buffy via editer-parcours).

---

## 1. Reparations immediates effectuees (erreurs hors mission, regle utilisateur)

| Test | KO avant | Apres | Cause |
|---|---|---|---|
| test-006-cartographier-parcours | 1 | **19/19 OK** | Pin atlas obsolete : carte bumpee 0.5.1 -> 0.5.3 (49 -> 52 cases, 13 -> 14 chemins) par Buffy (cases cU1-cU3) |
| test-010-generateurs-case | 2 | **24/25** (1 KO carte) | Libelle 'validateur-case' (stderr) vs 'valider-case' (stdout) : test adapte pour lire stdout+stderr ; reste 7b = carte cerberus non conforme |
| test-013-cerberus-migration | 11 | **20/22** (2 KO carte) | Pins obsoletes : version 0.5.5 -> 0.5.8, 24/5/5/3 -> 27/6/7/4 cases, navigation avec cU1 NON ; reste 3a/3b = carte cerberus non conforme |
| test-014-spec-guider-parcours | 1 | **13/13 OK** | Navigation cerberus : ajout NON (cU1) |
| test-016-migration-buffy | 5 | **20/20 OK** | Pins obsoletes : version 0.5.1 -> 0.5.3, 8->9 questions, 10->13 fins, navigation cU1 NON |
| test-018-fins-reactivation | 3 | **11/13** (2 KO cartes socrate) | Pin 16 -> 20 parcours ; reste 1b/2 = fins 'Reactiver Cerberus' dans les 4 parcours socrate |
| test-020-combos-clio | 9 | **47/47 OK** | Pins obsoletes : combos-maj-readme-massive 0.1.6 -> 0.1.7, combo-maj-readme 0.1.0/5 cases -> 0.2.0/7 cases, etapes 5 -> 6, dry-run c2=OUI;c3b=OUI |
| test-021-ligne-trio | 3 | **9/9 OK** | Navigation trio : ajout NON (cU1) |
| test-026-detecter-cablages | 2 | **9/10** (1 KO cartes) | Pin 16 -> 17 parcours d agents ; reste 8 = 3 problemes bloquants : cerberus c45b/c46b orphelines + socrate c1b orpheline |
| test-027-series-garde-fou | 1 | **11/11 OK** | test-099 ajoute a la serie e du lanceur |
| test-046-hermes-fautes | 1 | **10/10 OK** | Pin 16 -> 20 parcours (socrate + 3 revision-*) |
| test-067-bumper-tous-audit | 2 | **8/8 OK** | 3 outils incoherents corriges via bumper --wet : combos-maj-readme-massive, lire-activite-recente, mettre-a-jour-readme |
| test-079-noms-maj | 1 | **15/15 OK** | Registre : 4 entrees 'corriger-symboles' (alias) -> 'corriger-accents-zones-sensibles' (canonique) |
| test-085-processus-residuels | 2 | **8/8 OK seul** | Artefact de parallelisme (test partage des fichiers) : OK en lancement isole |
| test-092-parite-agents-activation | KO | **9/9 OK** (Morpheus) | chiron formate dans .py + socrate ajoute au .sh |
| test-098-historique-format | KO | **7/7 OK** (Morpheus) | Test adapte au format v0.6.1 timeline |
| test-099-activation-relais | - | **6/6 OK** (Morpheus) | Test garde-fou v0.5.22 conforme template |

---

## 2. KO restants : DEFANTS DE CARTES (a corriger par Buffy)

Tous les 11 KO restants proviennent de 2 causes racines :

### A. Carte cerberus (parcours-cerberus.json) -- cases c45/c45b/c46/c46b NON CONFORMES

Ajoutees dans le working tree (absentes du HEAD) avec un format invalide :
- **c45 / c46** (action) : `suivant` ABSENT -> "impasse ?"
- **c45b / c46b** (controle) : `branche_vraie`/`branche_fausse` au lieu de
  `branches: [{reponse: OUI, vers}, {reponse: NON, vers}]` -> "0 branche(s)"

Tests KO lies : test-009 (3a/3b/3e/5/8a/8b), test-010 (7b), test-013 (3a/3b),
test-015 (2/4/5/6/7), test-026 (8 : c45b/c46b orphelines).

**Correction attendue** : reformater c45b/c46b avec `branches` + ajouter
`suivant` a c45/c46, puis bumper la version et resynchroniser.

### B. Integration socrate incomplete

- **4 parcours socrate** (socrate + revision-audit/generale/urgence) : fins
  'FIN - Reactiver Cerberus' (REGLE IMMUABLE JANUS : seul janus a cette fin)
  -> test-018 (1b/2), test-070 (5b).
- **revision-urgence c0** : 1 seul outil lire-fichier (attendu 2 : corrections
  + fiche) -> test-072.
- **cerberus.md** : tableau des agents sans socrate -> test-094.
- **Cartes mermaid** : socrate.mmd/.svg non synchronises (cree 20/08 sans
  regeneration) -> test-096. Aussi : convertir-carte-mermaid non deterministe
  pour socrate (bug outil, a signaler a Vulcain si persiste apres synchro).
- **socrate c1b** : case orpheline (jamais atteignable) -> test-026 (8).

---

## 3. Verdict

**A REVOIR** : la chaine d outils (garde-fou + tests) est valide sur son
perimetre (test-099 6/6, test-092/098 OK, evaluer-processus 0 probleme),
mais la non-regression complete revele 11 KO preexistants lies a des defauts
de cartes (cerberus c45b/c46b + integration socrate) hors mission.

Selon ma carte (c9g - boucle KO) : j active **Buffy** (SEULE habilitee
editer-parcours) pour corriger les cartes, puis elle me reactive pour
re-controle.
