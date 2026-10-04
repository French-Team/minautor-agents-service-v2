---
identite:
  type: spec
  appartient_a: commun
  commun: true
---
# Spec -- Validateur-case (valider et alleger les cartes de decision)

**Version** : 1.1.1
**Statut** : ebauche
**Date creation** : 2026-08-09
**Agent** : Vulcain (creation)
**Historique** : v1.1.1 (alignement spec/outil, round 11 coherence documentaire : version de la spec synchronisee avec la version de l outil 1.1.1) -> v1.1.0 (BUDGET PONDERE des indices : indice COURT <= 100 car. = 0,5 unite, LONG > 100 = 1, budget 3,0 par case -- 2 courts = 1 long, decision utilisateur 2026-08-11 ; le plafond de 160 car. par texte reste inchange) -> v1.0.2 (convention de nommage ETENDUE aux prefixes thematiques majuscules `cT*` -- la ligne trio de Janus utilise cT1..cT10, decision utilisateur 2026-08-11 : conserver ces IDs) -> v1.0.1 (garde-fou rapport : sans --rapport explicite, aucun fichier cree -- lecon rapport a la racine, 2026-08-09) -> v1.0.0 (creation, 2026-08-09)

---

## Objectif

Valider une **carte de decision** (parcours JSON) et **ALLEGER les cases** :
structure, modele compose (branches min 2, deviation = rejoint), surcharge des
indices (budget pondere : court <= 100 car. = 0,5 / long > 100 = 1, budget 3,0 ;
ou texte > 160 caracteres -> proposition de reference),
references (chaque `ref` resolvable), normes (types, nommage, ASCII, LF).
Verdict : **CONFORME / A ALLEGER / NON CONFORME** + rapport markdown.

**Source** : etape 2 de la spec-refonte-cartes-decision v0.1.3 (section 6) --
l'outil qui rend les cartes largement plus lisibles et suivies, dans la vision
utilisateur (catalogues de cases alleges, valider-case).

## Pourquoi cet outil ?

| Probleme | Solution |
|---|---|
| Les cartes se degradent (indices empiles, 45 Ko) | Detection automatique de la surcharge avec proposition de reference |
| Le modele compose n'est pas garanti (branches min 2, deviation = rejoint) | Verification modele sur chaque carte |
| Le nouveau format d'indices references (ref) peut pointer vers rien | Verification que chaque ref resout vers une source existante |
| Cartes non-executees (conformite manquee) | Verdict objectif avant toute mission (une carte saine = executable) |

## Vue d'ensemble

```
parcours-<agent>.json  (source, LECTURE SEULE)
    |
    v
valider-case.py <parcours.json> [--case id] [--surcharge|--modele|--references]
    |  (verifications : structure, modele, allegement, references, normes)
    v
Verdict CONFORME / A ALLEGER / NON CONFORME
    + rapport markdown (rapport-valider-case-<date>.md par defaut)
```

## Interface CLI

```
valider-case.py <parcours.json> [options]
  --complet        Valider TOUTES les cases (defaut)
  --case <id>      Valider UNE case
  --surcharge      Verifier uniquement la surcharge des indices
  --modele         Verifier uniquement le modele compose
  --references     Verifier uniquement les references
  --dry-run        Simuler sans ecrire le rapport
  --rapport <fichier>  Rapport markdown (defaut: rapport-valider-case-<date>.md)
  --version        Afficher la version
  --aide           Afficher l'aide
```

Parite py/sh : le .sh est un wrapper pur (`exec python3 "$PY_SCRIPT" "$@"`) --
aucune divergence de logique possible entre les 2 versions.

## Verifications

### 1. Structure

- ids de cases uniques (par construction du JSON)
- types valides : `question`, `controle`, `indice`, `action`, `fin`
  (`action` = NOUVEAU type du modele cible, spec-refonte v0.1.3, etape 5)
- `case_depart` existe
- chaque `fin` est joignable depuis la case de depart (BFS anti-boucle)

### 2. Modele compose

- decision (`question`/`controle`) : **branches min 2**
- `indice`/`action` : `suivant` requis
- aucune **boucle directe** (branche vers elle-meme)
- **impasses** signalees (case non-fin sans suivant ni branches)
- **deviation sans rejoint** visible = avertissement (BFS du flux)

### 3. Allegement (surcharge)

- **budget pondere** : chaque indice pese 0,5 unite s'il est COURT
  (texte <= 100 car., ou sans texte) et 1 unite s'il est LONG (texte > 100
  car.) ; une case dont le poids total depasse **3,0 unites** = SIGNALEE
  (proposition : combo Pattern 3 ou references). 2 indices courts valent
  1 indice long : 6 courts (3,0) OK, 3 longs (3,0) OK, 2 longs + 2 courts
  (3,0) OK, 4 longs (4,0) SIGNALE.
- texte de regle **> 160 caracteres** = SIGNALEE (proposition : reference
  pattern/protocole) -- plafond absolu d'un indice, independant du budget.

### 4. References

- chaque indice `{type: regle, ref: X}` doit resoudre :
  - `pattern-<N>` -> section `### Pattern N` de spec-guider-parcours
  - chemin relatif -> fichier existant depuis la racine du projet
  - `protocole-<nom>` / `regle-<nom>` -> element existant dans regles-immuables
- les indices texte inline actuels restent VALIDES (le format `ref` est accepte
  et verifie quand present)

### 5. Normes

- nommage des cases : `c[<prefixe-alpha-maj>]<numero>[a-z]?` -- cas normal
  `c<numero>[a-z]?` (ex: c0, c12, c13b) + prefixe thematique MAJUSCULE
  optionnel (ex: `cT1`..`cT10` pour la ligne Trio de Janus)
- titre present sur chaque case
- **ASCII strict** : tout caractere non-ASCII du parcours est signale

## Verdict

| Verdict | Condition |
|---|---|
| CONFORME | aucune erreur, aucune surcharge |
| A ALLEGER | surcharges sans erreur (carte fonctionnelle a alleger) |
| NON CONFORME | au moins une erreur (structure/modele/references/normes) |

Le rapport markdown contient : en-tete, verdict, tableaux de comptage
(erreurs / a alleger / avertissements) et le detail de chaque classe.

## Regles

1. **LECTURE SEULE** : l'outil ne modifie JAMAIS le parcours audite.
2. **ASCII strict** : tout contenu non-ASCII du parcours est signale.
3. **LF** : tous les fichiers de l'outil en LF (standard projet).
4. **Parite py/sh** : wrapper pur, memes resultats sur les memes arguments.
5. **Spec de reference** : spec-refonte-cartes-decision v0.1.3 (etape 2).
6. **Regle des 5 fichiers** : py, sh, md, spec + enregistrements
   (index-tools.md, catalogue generateurs-commande).

## Emplacement des fichiers

| Fichier | Chemin |
|---|---|
| Outil python | `agents/tools/valider/valider-case/valider-case.py` |
| Outil bash | `agents/tools/valider/valider-case/valider-case.sh` |
| Documentation | `agents/tools/valider/valider-case/valider-case.md` |
| Spec | `agents/tools/valider/valider-case/spec/spec-valider-case.001.01.ebauche.md` |
