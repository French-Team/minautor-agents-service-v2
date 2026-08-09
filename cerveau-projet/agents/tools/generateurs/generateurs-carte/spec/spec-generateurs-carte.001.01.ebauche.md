---
identite:
  type: spec
  appartient_a: commun
  commun: true
---
# Spec -- Generateurs-carte (squelette allege + delegation validateur-case)

**Version** : 0.3.0
**Statut** : ebauche
**Date creation** : 2026-08-09
**Agent** : Vulcain (refonte etape 4 spec-refonte-cartes-decision)
**Historique** :
- v0.3.0 (refonte squelette allege + delegation validateur-case, 2026-08-09)
- v0.2.0 (generateurs-carte pre-existant, sans spec dediee)

---

## Objectif

Agit sur une CARTE DE DECISION COMPLETE (parcours JSON) : creer un squelette,
analyser les chemins de `case_depart` aux fins, detecter les anomalies,
dupliquer un chemin (groupe de cases) avec recablage.

**Etape 4 de la spec-refonte-cartes-decision (2026-08-09)** :
1. `creer` : squelette ALLEGE -- les indices portent des REFERENCES de base
   uniquement (aucun texte de regle inline) : la carte neuve nait a 0 surcharge ;
2. `detecter` / `analyser` : REUTILISER les verifications du validateur-case
   v1.0.0 (etape 2) -- source unique de verite, pas de logique dupliquee ;
3. `dupliquer-chemin` : CONSERVER les references (aucun texte inline a
   dupliquer : la copie porte les memes refs, rien ne derive).

## Pourquoi cette refonte ?

| Probleme | Solution |
|---|---|
| Le squelette portait des textes de regles inline longs (> 160 car.) -> surcharges des la creation | Indices de type REFERENCE (`pattern-N`, `protocole-activation`, chemins) -- la carte nait CONFORME (0 a alleger) |
| `detecter` dupliquait des verifications (modele, surcharge, references) | Delegation au validateur-case v1.0.0 -- source unique, les deux outils ne peuvent pas diverger |
| `dupliquer-chemin` copiait des textes inline qui derivent | Les references sont copiees telles quelles -- la regle vit a UN seul endroit |

## Vue d'ensemble

```
generateurs-carte.py <action> [options]
  actions : creer | analyser | detecter | dupliquer-chemin
  chaque ecriture -> sauvegarde ASCII strict + validation auto
      (references + guider-parcours --liste + validateur-case --modele --references)
```

## Actions et options

### creer

`creer <parcours.json> --agent <nom> [--nom] [--ver 0.1.0] [--description] [--force]`
Cree 7 cases (c0, c0b, c0c, c1, c2, c2b, c9). Indices de type `ref` :
- `protocole-activation` (relecture c0/c0b) ;
- `pattern-6` (contexte temps reel c0c) ;
- `pattern-10` (une carte = un role, c1) ;
- `pattern-3`, `pattern-7`, `pattern-2` (rappels c2) ;
- `cerveau-projet/agents/regles-immuables/general/rvav-workflow.md` (RVAV c2b).

### analyser

`analyser <parcours.json>` : liste tous les chemins de `case_depart` vers les
fins (BFS avec limite anti-boucle). Les impasses sont marquees `[impasse]`.

### detecter

`detecter <parcours.json>` : anomalies structurelles locales (boucles
d'attente, inatteignables, sans sortie, references cassees, decision a branche
unique) PUIS verifications deleguees au validateur-case `--modele --surcharge
--references` (spec-refonte 7.2 : source unique de verite).

### dupliquer-chemin

`dupliquer-chemin <parcours.json> --debut <case> --fin <case> [--prefixe d]
[--brancher-debut]` : duplique le groupe de cases du chemin avec recablage
interne. Les indices REFERENCES sont conserves tels quels (rien a dupliquer).

## References (indices de type ref)

Cle `ref` (alignee sur `valider-case --references`) :

| Ref | Source resolue par valider-case |
|---|---|
| `pattern-<N>` | Pattern N de la spec-guider-parcours (`### Pattern N`) |
| `protocole-<x>` / `regle-<x>` | Recherche par nom dans regles-immuables |
| chemin relatif | Fichier existant dans le projet |

## Validation auto (apres chaque ecriture)

1. References validees (valider_references interne) ;
2. `guider-parcours --liste` recharge le fichier modifie ;
3. `valider-case <parcours> --modele --references --dry-run` (spec-refonte 7.2) :
   un verdict NON CONFORME bloque l'operation.

## Garde-fous preserves (v0.2.x)

- Nommage `generateurs-` controle au demarrage ;
- `--dry-run` ne modifie jamais le fichier ;
- ASCII strict + LF pur (`ensure_ascii=True`, newline="\n").

## Criteres d'acceptation

1. Une carte creee par `creer` est CONFORME des la creation : verdict
   `valider-case` = erreurs 0, a alleger 0 (les indices sont des references) ;
2. `detecter` affiche les verifications du validateur-case (delegation) ;
3. `dupliquer-chemin` conserve les indices references tels quels ;
4. Parite py/sh (`--version` et sorties identiques) ;
5. ASCII strict + LF pur sur tous les fichiers de l'outil (py, sh, md, spec).
