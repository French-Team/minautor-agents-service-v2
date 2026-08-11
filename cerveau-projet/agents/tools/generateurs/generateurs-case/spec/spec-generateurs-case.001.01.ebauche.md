---
identite:
  type: spec
  appartient_a: commun
  commun: true
---
# Spec -- Generateurs-case (modele compose complet + references)

**Version** : 0.4.2
**Statut** : ebauche
**Date creation** : 2026-08-09
**Agent** : Vulcain (refonte etape 3 spec-refonte-cartes-decision)
**Historique** :
- v0.4.2 (budget pondere des indices : court <= 100 car. = 0,5 unite, long > 100 car. = 1 unite, budget 3,0 unites par case, plafond 160 car. inchange, 2026-08-11)
- v0.4.0 (mode batch convertir : indice -> action en masse + regles -> refs via mapping, 2026-08-09)
- v0.3.0 (refonte modele compose complet + option --ref, 2026-08-09)
- v0.2.2 (generateurs-case pre-existant, sans spec dediee)

---

## Objectif

Genere, edite et supprime des cases d'une carte de decision (parcours JSON)
avec recablage automatique des references et validation auto complete.

**Etape 3 de la spec-refonte-cartes-decision (2026-08-09)** :
1. Generaliser `ajouter-bloc` en MODELE COMPOSE COMPLET : une commande cree
   decision + branches (min 2, extensible) + deviation + rejoint ;
2. Ajouter l'option `--ref` pour poser des indices de type REFERENCE
   (au lieu du texte inline) -- c'est l'allegement des cartes ;
3. Verifier le modele apres chaque commande (appel interne au validateur-case
   v1.0.0, cree a l'etape 2).

## Pourquoi cette refonte ?

| Probleme | Solution |
|---|---|
| Les indices deviation/rejoint portaient des textes inline longs (> 160 car.) -> surcharges detectees par valider-case | Indices de type REFERENCE (`pattern-7` par defaut) : lisibles, resolvables, allegent les cartes |
| Le modele compose etait fige a 2 branches (OUI/NON) | `--branche <reponse>:<vers>` repetable : decision a branches min 2, extensible (concept : case 1 doit avoir plusieurs choix) |
| La validation apres commande ne verifiait pas le modele | Appel interne a `valider-case --modele` dans la validation auto |

## Vue d'ensemble

```
generateurs-case.py <parcours.json> <action> [options]
  actions : liste | ajouter | editer | supprimer | ajouter-bloc
  chaque modification -> sauvegarde ASCII strict + validation auto
      (references + guider-parcours --liste + valider-case --modele)
```

## Actions et options

### ajouter

`--type question|indice|controle|fin` (obligatoire), `--case`, `--titre`,
`--question`, `--message`, `--suivant`, `--apres`, `--branche <rep>:<vers>`
(repetable), `--indice-regle <texte>` (repetable), `--ref <ref>` (repetable),
`--indice-outil <nom>:<chemin>[:commande]`, `--indice-fichier <chemin>:<raison>`.

### editer

`<case_id>` + les memes options de modification. `--ref` remplace les indices
par des references. `--remove-indices` vide les indices.

### supprimer

`<case_id>` + `--vers` (recablage) / `--force`. Une fin sans `--vers` est
refusee (Pattern 5 : jamais de fin passive).

### ajouter-bloc (modele compose complet)

Cree 3 cases : decision (question, branches min 2) + deviation (indice,
reference `pattern-7` par defaut) + rejoint (indice, reference `pattern-7`).

| Option | Role |
|---|---|
| `--decision`, `--deviation`, `--rejoint` | Ids (defauts : prochain cN libre + suffixes a/b) |
| `--titre`, `--question` | Titre/question de la decision |
| `--titre-deviation`, `--titre-rejoint` | Titres des 2 autres cases |
| `--suite <id>` | Suite du flux principal (OBLIGATOIRE) |
| `--branche <rep>:<vers>` | Branche supplementaire (repetable, en plus de OUI/NON) |
| `--ref-deviation <ref>` | Reference deviation (defaut: pattern-7) |
| `--ref-rejoint <ref>` | Reference rejoint (defaut: pattern-7) |
| `--apres <id>` | Insertion avec recablage auto |

## Format des references (indices --ref)

Cle `ref` (alignee sur `valider-case --references`) :

| Ref | Source resolue par valider-case |
|---|---|
| `pattern-<N>` | Pattern N de la spec-guider-parcours (`### Pattern N`) |
| `protocole-<x>` / `regle-<x>` | Recherche dans regles-immuables |
| chemin relatif | Fichier existant dans le projet |

Exemple produit : `{"type": "ref", "ref": "pattern-7"}`.

## Validation auto (apres chaque modification)

1. References validees (valider_references interne) ;
2. `guider-parcours --liste` recharge le fichier modifie ;
3. `valider-case <parcours> --modele --dry-run` (spec-refonte 7.1) : un
   verdict NON CONFORME bloque l'operation.

## Garde-fous preserves (v0.2.x)

- Nommage `generateurs-` controle au demarrage ;
- Pattern 5 : jamais de fin passive (message de fin analyse) ;
- REGLES IMMUABLES : rappel ASCII + RVAV + delegation (Morpheus/Janus) sur
  les cases d'ecriture et les fins de delegation ;
- `--dry-run` ne modifie jamais le fichier ;
- ASCII strict + LF pur (`ensure_ascii=True`, newline="\n").

## Criteres d'acceptation

1. `ajouter-bloc` cree decision + branches min 2 + deviation + rejoint en une
   commande, avec indices de type reference (pas de texte inline) ;
2. `--ref` pose des references resolvables (pattern/protocole/chemin) ;
3. Chaque modification declenche `valider-case --modele` et un verdict
   NON CONFORME bloque l'operation ;
4. Parite py/sh (`--version` et sorties identiques) ;
5. ASCII strict + LF pur sur tous les fichiers de l'outil (py, sh, md, spec).
