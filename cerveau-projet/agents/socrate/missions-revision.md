# Missions de Revision -- 2026-09-02

> Revision strategique (mission 74e0f982). Choix utilisateur (2026-09-02) :
> prioritizer (a) les VESTIGES V1 encore actifs et (c) le REVERSE de la
> non-regression (tests v1 a reclasser). Les missions restantes du round
> (purger P1, encart 'Inconnu', purification) sont en IMPORTANT en attente
> de round.

## Resume

| Niveau | Nombre |
|---|---|
| URGENT | 1 |
| IMPORTANT | 2 |
| MOYEN | 0 |
| BAS | 0 |

## Missions

### [URGENT] Purger les derniers vestiges v1 qui reactivent Cerberus dans les structures v2 (Buffy)

- **Date** : 2026-09-02 (choix utilisateur : priorite vestiges v1 ; detection Vulcain mission 4d5d8c8d)
- **Agent habilite** : buffy (developpeur principal, responsable cerveau-projet)
- **Description** :
  - Basculer vers le modele aero R1/R3 toute fin theme/arbre v2 qui
    reactiverait encore Cerberus en milieu de chaine. Fichiers cibles :
    themes v2 des agents dont les fins pointent une reactivation cerberus
    ou une chaine v1 (pre-aero).
  - Verification : `grep -rn "reactiver.*cerberus|--cible cerberus"` sur
    `cerveau-projet/agents/*/parcours/theme-*.json` et `fins.json` : les
    seuls cerberus autorises sont (1) la regle negative "ma fin va vers
    ORACLE, jamais vers cerberus" dans les fins.json (deja conforme), et
    (2) les messages `oracle.py envoyer oracle cerberus` de coordination
    legitime (theme-processus/delegation d oracle) - aucun fin -cible
    cerberus.
  - Conserver les archives v1 protegees par le marbre (hors perimetre).
- **Raison** : tant qu un theme v2 peut reactiver Cerberus en cours de
  round, un agent sort du flux aero (la fin doit TOUJOURS aller vers
  Oracle, le pilote decide). C est la cause racine des sorties de flux
  (DEFCON 5 repetes) partiellement traitee : la purge restante est un
  verrou de conformite.
- **Dependances** : aucune (audit en parallele avec la mission IMPORTANT
  ci-dessous).
- **Critere de succes** : scan complet des themes v2 : 0 fin a cible
  cerberus (hors coordination legitime) ; test-114 (reverse vestiges v1)
  reste VERT apres correction.

### [IMPORTANT] Reverse complet de la non-regression : reclasser les tests v1 obsoletes (Morpheus)

- **Date** : 2026-09-02 (decision utilisateur : la non-regression devient
  un MOYEN DE RETROUVER LES VESTIGES V1)
- **Agent habilite** : morpheus (testeur, le reverse est son domaine) +
  buffy si fichiers structurels a corriger en consequence
- **Description** :
  - Poursuivre le travail amorce par test-114 : inventaire des tests
    (`cerveau-projet/agents/tools/tester/tests/`) qui referencent encore
    la v1 (guider-parcours, parcours-<agent>.json, cases cXX,
    spec-guider-parcours, parcours-demarrage) et les classer :
    OBSOLETE (couvre un element v1 sans equivalent v2) / A-REFAIRE
    (reecrire contre l equivalent v2 : arbres, themes, guider-arbre) /
    A-CONSERVER (archive protegee legitime ou comportement v1 maintenu).
  - Marquer les tests obsoletes dans la registre (retrait du role actif,
    gardes d archives) - ex. test-013/016/018/072 deja en cours.
  - Produire le rapport du reverse (liste des tests, classification,
    justification) + reecrire les tests a-refaire en v2.
- **Raison** : beaucoup de gardes-fous pinent encore des elements v1 qui
  ne pilotent plus ; ils donnent un faux sentiment de couverture et
  faussent la non-regression (un test v1 obsolete qui passe ne prouve
  rien sur la v2).
- **Dependances** : mission URGENT ci-dessus (les vestiges detectes
  alimentent le reclassement).
- **Critere de succes** : registre a jour (obsolete/a-refaire/a-conserver
  explicites), serie de tests v2 uniquement, rapport de reverse pose dans
  morpheus/rapports.

### [IMPORTANT] Purger les P1 non-acquittes et les alertes de coordination du round (Super-pilote + destinataires)

- **Date** : 2026-09-02 (missions ETAT URGENT / MISE EN ATTENTE du round)
- **Agent habilite** : super-pilote (orchestration) + destinataires en inter-round
- **Description** :
  - Lire puis acquitter les messages P1 restants de chaque destinataire
    (inbox *.jsonl) apres traitement reel : les ETAT URGENT / MISE EN
    ATTENTE generes par flux/verifier-statuts dont la cause est resolue.
  - Les MESSAGES MISSION reels (ex. VESTIGES V1 pour buffy, REVISION pour
    socrate) restent en attente de leur activation - pas d acquittement
    d une mission non executee.
- **Raison** : les P1 non-acquittes accumules declenchent en boucle de
  nouveaux ETAT URGENT (pollution de la file et du DEFCON).
- **Dependances** : aucune.
- **Critere de succes** : 0 message P1 non-lu hors missions reelles en
  attente ; la file asap/attente ne contient plus de ETAT URGENT
  residuel.