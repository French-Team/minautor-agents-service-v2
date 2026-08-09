---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
# Specification -- Protocole de Creation et Mise en Place des Combos

**Statut :** ebauche
**Version :** 0.1.2-ebauche
**Categorie :** regles-immuables / protocoles
**Date :** 2026-08-08
**Pense-bete source :** [protocole-creation-combos.001.01.ebauche.md](../protocole-creation-combos.001.01.ebauche.md)

---

## 1. Objectif

Definir le PROCESSUS reproductible de creation et de mise en place des combos
(`definition-combo.json`) : regles de decision (quand creer), conventions
(nommage, structure, emplacement), etapes de creation, checklist d'integration
Pattern 3 et validation. Complement operationnel de la spec-combos-moteur
(qui documente le FORMAT) et de la spec-guider-parcours (qui documente
l'INTEGRATION).

---

## 2. Contexte

### 2.1 Origine

6 combos ont ete crees de facto entre 2026-08-08 et 2026-08-08
(combo-activation, combo-audit-themis, combo-controle-outil,
combo-controle-modification, combo-corriger-ascii, combo-sante-tableaux) en
s'appuyant sur les precedents. A chaque creation, les conventions etaient
re-decouvertes : emplacement, nommage, structure, validation. Deux ambiguites
persistantes : l'emplacement canonique (la doc moteur cite 2 emplacements) et
la distinction OUTIL vs DEFINITION avec le dossier `agents/tools/combos/`.

### 2.2 Perimetre

COUVERT : quand creer un combo, ou le placer, comment le nommer et le
structurer, comment le tester, comment l'integrer dans un parcours (Pattern 3),
comment le valider.

HORS PERIMETRE : le format JSON des cases (spec-combos-moteur), le moteur
d'execution (combos-moteur, domaine Vulcain), le catalogue du generateur,
le Pattern 3 dans la spec-guider-parcours, la creation d'OUTILS combos
(combos-*.py/.sh dans agents/tools/combos/, domaine Vulcain).

### 2.3 Public cible

- Buffy (developpeur principal) : cree les definitions de combos
- Les agents dont les parcours utilisent des combos (themis, janus, vulcain, buffy)
- Janus (controleur) : verifie la conformite des combos et des cases Pattern 3
- Cerberus (coordinateur) : route les missions de creation de combos vers Buffy

---

## 3. Exigences Fonctionnelles

### 3.1 EX-01 -- Regle de decision : suite lineaire

| Champ | Description |
|---|---|
| **Priorite** | Haute |
| **Description** | Un combo est cree pour une suite LINEAIRE d'outils de validation/execution, repetee (>= 2 occurrences) ou longue (>= 3 outils). Un arbre de decision, des protections embarquees dans un test et une suite specifique non repetee ne sont PAS combinables. |
| **Critere d'acceptation** | Le combo cree correspond a une suite lineaire ; les parcours non transformables restent en l'etat (documente dans le parcours). |
| **Dependances** | -- |

### 3.2 EX-02 -- Emplacement canonique

| Champ | Description |
|---|---|
| **Priorite** | Haute |
| **Description** | Toute definition de combo est placee dans `cerveau-projet/combos/<combo-nom>/definition-combo.json`. Le dossier `agents/tools/combos/` est reserve aux OUTILS (moteur + combos executables). Le fichier porte TOUJOURS le nom `definition-combo.json`. |
| **Critere d'acceptation** | Toutes les definitions existantes et futures sont dans `cerveau-projet/combos/` ; aucun fichier de definition dans `agents/tools/combos/`. |
| **Dependances** | -- |

### 3.3 EX-03 -- Conventions de nommage et de structure

| Champ | Description |
|---|---|
| **Priorite** | Haute |
| **Description** | Nom : `combo-<action>` (dossier = champ nom). Cases : `c1`..`cn` en ordre, `case_depart: c1`. Titres : `Generer la commande <X>` (generateur), `Executer <X>` (outil), `FIN - <resume>` (fin). Sorties : `cmd1`, `cmd2`... (generateurs), `resultat_<action>` (outils). Version initiale `0.1.0`. |
| **Critere d'acceptation** | Les conventions des 6 combos existants et des combos futurs respectent ce tableau. |
| **Dependances** | EX-02 |

### 3.4 EX-04 -- Cases generateur vs outil direct

| Champ | Description |
|---|---|
| **Priorite** | Haute |
| **Description** | Commande au catalogue du generateur -> case `generateur` (mode AUTO) puis case `outil` avec `{cmd}`. Commande absente du catalogue -> case `outil` directe (commande `python3 <outil> [cible]` complete). Cibles par defaut : `cerveau-projet/agents` (validation) ou `cerveau-projet` (audit global). |
| **Critere d'acceptation** | Les commandes du catalogue passent par le generateur AUTO (verifiable par --dry-run) ; les autres sont des commandes directes. |
| **Dependances** | spec-combos-moteur, catalogue-commandes.json |

### 3.5 EX-05 -- Outils contextuels exclus

| Champ | Description |
|---|---|
| **Priorite** | Moyenne |
| **Description** | Les outils portant sur un FICHIER PRECIS de la mission (valider-ebauche sur une spec donnee, verifier-role-fichier sur un fichier modifie) restent en INDICES de la case du parcours. Le combo enchaine uniquement les outils a perimetre STABLE (dossier par defaut). |
| **Critere d'acceptation** | Aucun outil contextuel dans les definitions ; les cas contextuels apparaissent dans les indices des cases de parcours. |
| **Dependances** | EX-01 |

### 3.6 EX-06 -- Processus de creation en 11 etapes

| Champ | Description |
|---|---|
| **Priorite** | Haute |
| **Description** | Suivre les 11 etapes : audit -> signatures CLI -> conception -> creation -> --liste/--dry-run -> json.load+ASCII -> integration Pattern 3 -> recablage refs -> revalidation chemins -> parite py/sh -> lecon. |
| **Critere d'acceptation** | Chaque combo cree suit les 11 etapes (tracable dans corrections.md de Buffy). |
| **Dependances** | EX-01 a EX-05 |

### 3.7 EX-07 -- Checklist d'integration Pattern 3

| Champ | Description |
|---|---|
| **Priorite** | Haute |
| **Description** | Une case combo de parcours porte : indice REGLE Pattern 3 en tete + indice OUTIL combos-moteur + indice FICHIER definition-combo.json. Refs recablees (`suivant` ET `vers`) sans reference morte. Version du parcours bumpee (0.2.0). |
| **Critere d'acceptation** | La case combo affiche les 3 indices ; zero reference morte ; tous les chemins -> PARCOURS TERMINE. |
| **Dependances** | spec-guider-parcours (Pattern 3), EX-02 |

### 3.9 EX-09 -- Citation obligatoire avant lancement

| Champ | Description |
|---|---|
| **Priorite** | Haute |
| **Description** | Tout lancement d'un combo est ANONCE par l'agent avant execution : `Je lance le combo <nom> : <chemin> - il enchaine <outils>.` Tracabilite des executions pour l'utilisateur, Cerberus et Janus. Le rappel est en tete des indices des cases combo des parcours. |
| **Critere d'acceptation** | Chaque case combo des parcours porte l'indice regle de citation en tete ; les agents citent le combo avant de le lancer. |
| **Dependances** | EX-07 (integration Pattern 3) |

### 3.10 EX-10 -- PIEGE WINDOWS : forward slashes dans les variables de chemins

| Champ | Description |
|---|---|
| **Priorite** | Haute |
| **Description** | Toute VARIABLE de chemin passee via `--var` (ex: `fichier_test=<chemin>`, `chemin=<chemin>`) utilise des FORWARD SLASHES, jamais de backslashes. La commande generee est decoupee par `shlex.split` dans la case `outil` : sur Windows un chemin absolu avec backslashes (`Z:\\...\\x.sh`) est eclate (backslash = echappement) -> fichier non cree. |
| **Critere d'acceptation** | Navigation reelle testee avec un chemin en forward slashes : la case `outil` cree le fichier (ex: combo tester-outil 16/16 VALIDE). Aucun chemin avec backslash dans les entrees des cases generateur. |
| **Dependances** | EX-04 (cases generateur vs outil), combos-moteur (interpolation + shlex) |

### 3.8 EX-08 -- Validation complete

| Champ | Description |
|---|---|
| **Priorite** | Haute |
| **Description** | Checklist : json.load OK, --liste sans ERREUR, --dry-run jusqu'a la fin, ASCII 0, parite py/sh, description mentionnant la suite remplacee + Pattern 3. valider-nommage NON applicable aux definitions JSON. |
| **Critere d'acceptation** | Les 7 points de validation passes avant reactivation Cerberus. |
| **Dependances** | combos-moteur, valider-conformite-ascii, guider-parcours |

---

## 4. Exigences Non-Fonctionnelles

| Categorie | Exigence | Critere de mesure |
|---|---|---|
| **Conformite** | Definitions ASCII strict | valider-conformite-ascii -> 0 non-conforme |
| **Maintenabilite** | Convention stable (dossier = nom = prefixe combo-) | verifiable par lecture du JSON |
| **Compatibilite** | Moteur py/sh parite | --dry-run identique .py et .sh |
| **Coherence** | Emplacement canonique unique | toutes les definitions dans cerveau-projet/combos/ |
| **Reproductibilite** | Processus documente | les 11 etapes applicables a un nouveau combo |

---

## 5. Architecture / Structure Technique

### 5.1 Vue d'ensemble

```
cerveau-projet/
|-- combos/                                  <- DEFINITIONS (domaine Buffy)
|   |-- <combo-nom>/
|   |   `-- definition-combo.json
|-- agents/tools/combos/                     <- OUTILS (domaine Vulcain)
|   |-- combos-moteur/ (moteur py+sh)
|   |-- combos-audit-general/
|   |-- combos-corriger-non-ascii/
|   `-- combos-valider-cerveau/
|-- agents/<agent>/parcours/parcours-<agent>.json  <- cases Pattern 3
```

### 5.2 Composants

| Composant | Role | Dependances |
|---|---|---|
| `definition-combo.json` | Source de verite du combo (objet combo + cases) | combos-moteur |
| `combos-moteur` | Execute la definition case par case | generateurs-commande (mode AUTO) |
| `generateurs-commande` | Compose les commandes du catalogue | catalogue-commandes.json |
| Case Pattern 3 (parcours) | Reference combos-moteur + definition | guider-parcours |

### 5.3 Modeles de donnees

Definition de combo : voir spec-combos-moteur (objet `combo` + `cases`).
Case Pattern 3 de parcours : voir spec-guider-parcours (indices regle/outil/fichier).

### 5.4 Flux / Workflows

```
audit parcours -> suite lineaire repetee ? -> NON : reste dans le parcours
                                            -> OUI : signatures CLI -> conception
       -> creation definition-combo.json -> --liste/--dry-run -> json.load+ASCII
       -> integration Pattern 3 (remplacer suite par case combo + indice CITER en tete)
       -> recablage refs (suivant+vers) -> revalidation chemins -> parite
       -> lecon corrections.md -> reactiver Cerberus
```

---

## 6. Contraintes et Risques

### 6.1 Contraintes

| Contrainte | Impact | Mitigation |
|---|---|---|
| Definitions JSON non validees par valider-nommage | Risque de mauvaise validation | Valider par json.load + ascii + --liste + --dry-run |
| Recablage oublie d'une reference | Reference morte dans le parcours | Verifier suivant ET vers, grep des refs |
| Outil contextuel dans un combo | Combo non reutilisable | EX-05 : rester en indices de la case |

### 6.2 Risques

| Risque | Probabilite | Impact | Mitigation |
|---|---|---|---|
| Combo cree pour une suite non lineaire | Faible | Eleve | EX-01 : regle de decision |
| Emplacement ambigu (tools/combos vs cerveau-projet/combos) | Moyenne | Moyen | EX-02 : emplacement canonique + doc moteur corrigee |
| Conventions derogeantes | Moyenne | Moyen | Controle Janus + checklist EX-08 |

---

## 7. Livrables attendus

| Livrable | Format | Destination |
|---|---|---|
| Protocole (pense-bete) | Markdown | protocole-creation-combos.001.01.ebauche.md |
| Spec technique | Markdown | spec/spec-protocole-creation-combos.001.01.ebauche.md (ce fichier) |
| Todo | Markdown | todo/todo-protocole-creation-combos.001.01.ebauche.md |
| Mise a jour index | Markdown | index-regles-general.md (ligne protocole) |
| Corrections doc moteur | Markdown | combos-moteur.md + spec-combos-moteur (emplacement canonique) |

---

## 8. Plan de validation

### 8.1 Criteres de succes globaux

- [ ] Les 6 combos existants respectent l'emplacement canonique et le nommage
- [ ] Les conventions EX-02 a EX-05 sont documentees dans la doc moteur
- [ ] Le processus EX-06 est applicable a une nouvelle creation (test sur un combo futur)
- [ ] La regle EX-09 (citer avant de lancer) est dans les 6 cases combo des parcours
- [ ] Index mis a jour + liens valides + ASCII 0

### 8.2 Methode de validation

Revue croisee (Janus) : verifier que la spec est coherente avec les 6 combos
existants, la spec-combos-moteur et la spec-guider-parcours.

### 8.3 Responsables

| Role | Responsable |
|---|---|
| Redaction | Buffy |
| Validation technique | Janus (second controle) |
| Validation utilisateur | Utilisateur (arbitre des decisions) |

---

## 9. Liens et References

### 9.1 Pense-bete source

- [protocole-creation-combos.001.01.ebauche.md](../protocole-creation-combos.001.01.ebauche.md)

### 9.2 Specs connexes

- [spec-combos-moteur](../../../../../agents/tools/combos/combos-moteur/spec/spec-combos-moteur.001.01.ebauche.md) -- format des cases
- [spec-guider-parcours](../../../../../agents/tools/guider/guider-parcours/spec/spec-guider-parcours.001.01.ebauche.md) -- Pattern 3

### 9.3 Conventions applicables

- [convention-protocoles.md](../../../../conventions/protocoles/convention-protocoles.md)

### 9.4 Regles immuables

- [regles-emojis-ascii.md](../../regles-emojis-ascii.md) -- ASCII strict
- [regles-validation-rigoureuse.md](../../regles-validation-rigoureuse.md)

---

## 10. RVAV de la spec

- [rechercher] -- les 6 definitions existantes, spec-combos-moteur, spec-guider-parcours
- [verifier] -- la structure est complete (exigences, contraintes, validation)
- [analyser] -- les conventions correspondent aux combos reels
- [valider] -- pret pour le statut `prepare`

---

## Historique des modifications

| Date | Version | Auteur | Description |
|---|---|---|---|
| 2026-08-08 | 0.1.0 | Buffy | Creation : 8 exigences fonctionnelles, emplacement canonique, processus 11 etapes, checklist Pattern 3 |
| 2026-08-08 | 0.1.1 | Buffy | Ajout EX-09 : citation obligatoire avant lancement (tracabilite, decision utilisateur) |
| 2026-08-09 | 0.1.2 | Buffy | Ajout EX-10 : PIEGE WINDOWS forward slashes dans les variables de chemins (decouverte test Morpheus combo tester-outil, section 6.3b du protocole) |
