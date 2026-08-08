---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
# Protocole -- Creation et Mise en Place des Combos

**Statut :** ebauche
**Version :** 0.1.1
**ID :** 001
**Class :** 01
**Cree :** 2026-08-08
**Theme :** combos

---

## 1. Idee

Standardiser la CREATION et la MISE EN PLACE des combos (definition-combo.json) :
quand creer un combo, ou le placer, comment le nommer, comment le structurer,
comment le tester et comment l'integrer dans un parcours (Pattern 3).
Le combo remplace les suites d'outils repetees : plus transparent, plus fiable,
plus digeste pour l'agent.

---

## 2. Probleme / Question

6 combos ont ete crees de facto (combo-activation, combo-audit-themis,
combo-controle-outil, combo-controle-modification, combo-corriger-ascii,
combo-sante-tableaux) en s'appuyant sur les precedents. La spec-combos-moteur
documente le FORMAT (le QUOI) mais pas le PROCESSUS (quand/ou/comment creer).
Resultats :
- chaque creation improvise les conventions
- ambiguite d'emplacement : la doc moteur cite 2 emplacements alors que
  `agents/tools/combos/` existe deja pour les OUTILS
- pas de checklist de validation avant integration Pattern 3

Ce protocole fige les conventions issues de l'experience (6 combos + 2 controles
Janus) pour rendre les creations reproductibles.

---

## 3. Distinction fondamentale : OUTIL vs DEFINITION

| Type | Contenu | Emplacement | Domaine |
|---|---|---|---|
| **OUTIL combo** | moteur + combos executables (.py/.sh/.md) | `agents/tools/combos/<outil>/` | Vulcain |
| **DEFINITION combo** | fichier JSON lu par le moteur | `cerveau-projet/combos/<combo-nom>/definition-combo.json` | Buffy |

> **REGLE (IMMUABLE)** : une DEFINITION de combo est un FICHIER DU CERVEAU
> (domaine Buffy). Le MOTEUR et les combos executables sont des OUTILS
> (domaine Vulcain). Ne jamais melanger les deux dossiers.

---

## 4. Regles de decision (quand creer un combo)

| Situation | Combo ? | Exemple |
|---|---|---|
| Suite LINEAIRE d'outils de validation/execution | OUI | controles janus, audit themis |
| Suite REPETEE (>= 2 occurrences, dans un ou plusieurs parcours) | OUI | corriger-accents + ascii (vulcain x2) |
| Suite LONGUE (>= 3 outils a enchainer) | OUI | controle-modification (7 outils) |
| Arbre de decision (branches de coordination) | NON | chemin retour cerberus |
| Protections chargees dans un test (pas des CLI) | NON | chemin tester morpheus |
| Suite SPECIFIQUE non repetee | NON | redacteurs (athena, minerve, promethee) |

> **REGLE (IMMUABLE)** : le Pattern 3 s'applique aux SUITES LINEAIRES d'outils,
> jamais aux decisions ni aux protections embarquees. Si la suite contient des
> etapes conditionnelles liees a la mission, elle reste dans le parcours.

---

## 5. Conventions de nommage

| Element | Convention | Exemple |
|---|---|---|
| Dossier | `cerveau-projet/combos/combo-<action>/` | `combo-controle-outil/` |
| Fichier | `definition-combo.json` (TOUJOURS) | -- |
| Champ `nom` | `combo-<action>` (identique au dossier) | `combo-controle-outil` |
| Champ `version` | `0.1.0` a la creation | -- |
| Champ `case_depart` | `c1` (premiere case) | -- |

Action : verbe + complement court en minuscules, mots separes par `-`
(activation, audit-themis, controle-outil, controle-modification,
corriger-ascii, sante-tableaux).

---

## 6. Conventions de structure

### 6.1 Titres de cases

| Type | Titre attendu | Exemple |
|---|---|---|
| `generateur` | `Generer la commande <X>` | Generer la commande corriger-accents |
| `outil` | `Executer <X>` | Executer valider-tableaux |
| `controle` | Question ou contexte court | La session est-elle identifiee ? |
| `fin` | `FIN - <resume>` | FIN - controle outil termine |

### 6.2 Sorties (variables)

| Type | Convention | Exemple |
|---|---|---|
| `generateur` | `cmd1`, `cmd2`, ... (ordre) | `cmd1` |
| `outil` | `resultat_<action>` | `resultat_ascii` |

### 6.3 Case generateur vs outil direct

- Commande presente au CATALOGUE du generateur (`catalogue-commandes.json`)
  -> case `generateur` (mode AUTO : le moteur appelle `generateurs-commande
  --reponses` alimente par les entrees) puis case `outil` avec `{cmd}`.
- Commande ABSENTE du catalogue -> case `outil` directe avec la commande
  `python3 <chemin-outil.py> [cible]` complete.

### 6.4 Cibles par defaut

| Cible | Quand |
|---|---|
| `cerveau-projet/agents` | Validation des fichiers des agents (nommage, ascii, sante) |
| `cerveau-projet` | Audit global, detecteurs de traces |

> **REGLE** : utiliser les defauts du cerveau comme cibles stables dans les
> combos. Les cibles CONTEXTUELLES (fichier precis de la mission) restent des
> indices de la case du parcours, JAMAIS dans le combo.

### 6.5 Outils contextuels exclus du combo

Les outils qui portent sur un FICHIER PRECIS de la mission (ex: valider-ebauche
sur une spec donnee, verifier-role-fichier sur un fichier modifie) restent en
INDICES de la case du parcours. Le combo enchaine uniquement les outils a
perimetre STABLE (dossier par defaut).

### 6.6 Version

| Element | Version |
|---|---|
| Combo (creation) | `0.1.0` |
| Parcours (a l'integration Pattern 3) | bump vers `0.2.0` |

---

## 7. Processus de creation (etapes)

1. **Auditer** les parcours : identifier la suite LINEAIRE repetee ou longue.
2. **Verifier les signatures CLI** (`--help`) des outils de la suite (cibles,
   options obligatoires) AVANT de composer.
3. **Concevoir** : ordre des cases, generateur vs direct (consulter le
   catalogue), cibles par defaut.
4. **Creer** `cerveau-projet/combos/<combo-nom>/definition-combo.json`.
5. **Tester** avec `combos-moteur` : `--liste` (structure) + `--dry-run`
   (navigation + commandes composees jusqu'a la case fin).
6. **Verifier** : `json.load` OK + ASCII 0 + description mentionnant la suite
   remplacee et le Pattern 3.
7. **Integrer** le Pattern 3 dans le parcours : remplacer la suite d'outils par
   UNE case combo.
8. **Recabler** TOUTES les references (`suivant` ET `vers`) des cases qui
   pointaient vers la suite supprimee ; verifier zero reference morte.
9. **Revalider** : `guider-parcours --reponses` sur TOUS les chemins du
   parcours -> PARCOURS TERMINE.
10. **Verifier la parite** py/sh du moteur sur la nouvelle definition.
11. **Noter la lecon** dans `corrections.md` (Buffy).

---

## 8. Checklist d'integration Pattern 3 (case combo)

- [ ] Indice REGLE Pattern 3 en TETE des indices de la case
- [ ] Indice OUTIL : `combos-moteur` (commande `combos-moteur.py <definition>`)
- [ ] Indice FICHIER : la definition `cerveau-projet/combos/<combo>/definition-combo.json`
- [ ] Refs recablees (`suivant` ET `vers`) sans reference morte
- [ ] `guider-parcours --reponses` -> PARCOURS TERMINE sur tous les chemins
- [ ] Outils contextuels conserves en indices de la case (hors combo)
- [ ] Version du parcours bumpee (0.2.0)

---

## 9. Validation (checklist complete d'un combo)

- [ ] `json.load` OK sur la definition
- [ ] `combos-moteur --liste` : toutes les cases affichees sans ERREUR
- [ ] `combos-moteur --dry-run` : navigation jusqu'a la case fin
- [ ] ASCII 0 (valider-conformite-ascii sur la definition + le parcours)
- [ ] Parite py/sh du moteur (combos-moteur.py = combos-moteur.sh)
- [ ] Description du combo : mentionne la suite remplacee + le Pattern 3
- [ ] valider-nommage NON applicable (les definitions JSON ne sont pas des
      outils .sh/.py/.md -- valider par json.load + ascii + --liste + --dry-run)

---

## 9.5 Regles d'utilisation et tracabilite

> **REGLE (IMMUABLE) -- CITER LE COMBO AVANT DE LE LANCER** : avant d'executer
> un combo, l'agent ANNOUNCE le nom du combo et le chemin de sa definition.
> Format : `Je lance le combo <nom> : <chemin> - il enchaine <outils>.`

**Pourquoi** : l'utilisateur (et Cerberus, Janus) doit pouvoir VOIR quand un
combo est utilise -- tracabilite des executions. La commande `combos-moteur`
seule ne revele pas toujours le nom du combo lance.

**Format de citation** :

```
Je lance le combo <nom> : <chemin-de-la-definition> - il enchaine : outil1 -> outil2 -> ...
```

**Exemple** :

```
Je lance le combo combo-controle-outil : cerveau-projet/combos/combo-controle-outil/definition-combo.json - il enchaine : valider-conformite-ascii -> valider-cartes-decision -> valider-liens.
```

**Ou la regle est rappelee** : en tete des indices de chaque case combo des
parcours (Pattern 3) : themis c3, janus c5/c22, vulcain c7/c13, buffy c28.

---

## 10. Liens

- **Spec moteur** : [spec-combos-moteur](../../../../agents/tools/combos/combos-moteur/spec/spec-combos-moteur.001.01.ebauche.md) -- format JSON (le QUOI)
- **Spec parcours** : [spec-guider-parcours](../../../../agents/tools/guider/guider-parcours/spec/spec-guider-parcours.001.01.ebauche.md) -- Pattern 3 (integration)
- **Doc moteur** : [combos-moteur.md](../../../../agents/tools/combos/combos-moteur/combos-moteur.md) -- conventions d'emplacement
- **Convention protocoles** : [convention-protocoles.md](../../../conventions/protocoles/convention-protocoles.md)
- **Spec technique** : [spec-protocole-creation-combos](spec/spec-protocole-creation-combos.001.01.ebauche.md)
- **Todo** : [todo-protocole-creation-combos](todo/todo-protocole-creation-combos.001.01.ebauche.md)

---

## 11. RVAV du protocole

- [rechercher] -- spec-combos-moteur, spec-guider-parcours, 6 definitions existantes, index-regles-general
- [verifier] -- la structure (idee, probleme, regles, processus, validation) est complete
- [analyser] -- coherent avec le cerveau existant (complement de spec-combos-moteur, pas de doublon)
- [valider] -- pret pour la spec technique (`prepare`)

---

## Historique des modifications

| Date | Version | Auteur | Description |
|---|---|---|---|
| 2026-08-08 | 0.1.0 | Buffy | Creation : regles de decision, conventions nommage/structure, processus en 11 etapes, checklist Pattern 3, validation |
| 2026-08-08 | 0.1.1 | Buffy | Ajout section 9.5 Regles d'utilisation et tracabilite : CITER le combo avant de le lancer (decision utilisateur) |
