---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# detecter-cablages-manquants

**Categorie** : Detecter
**Version** : 0.1.2
**Statut** : ebauche
**Agent** : Vulcain
**Date** : 2026-08-12

Detecte les **cablages manquants** des cartes de decision (parcours JSON) qui
echappent a `valider-case` (qui ne verifie QUE les fins non joignables). Cet
outil complete `valider-case` en detectant :

| # | Type | Ce qui est detecte |
|---|---|---|
| 1 | `CASE_DEPART` | `case_depart` manquante ou inexistante dans les cases |
| 2 | `FIN_NON_JOIGNABLE` | Une case `type: fin` jamais atteignable depuis la case de depart |
| 3 | `CAS_ORPHELINE` | TOUTE case (pas seulement les fins) jamais atteignable depuis la case de depart |
| 4 | `BOUCLE_BLOQUANTE` | Cycle SANS sortie entre 2+ cases (ou `suivant` vers soi-meme) |
| 5 | `REF_MORTE` | Champ `suivant` ou branche `vers` pointant vers une case inexistante |

---

## Pourquoi cet outil ?

Le bug des questions orphelines (vulcain c9b/c15b "Ameliorations possibles"
inaccessibles) a montre que `valider-case` ne detecte QUE les **fins** non
joignables : une case orpheline non-fin passe inapercue, et une boucle
indirecte (c22 -> c9b -> c22) n'est pas signalee. Cet outil ferme le trou en
analysant le graphe complet depuis la case de depart.

## Boucles de re-travail (avertissements, pas erreurs)

Une boucle de re-travail est un cycle **avec sortie** (une case du cycle pointe
vers une case hors du cycle) : c'est le cas d'un controle NON -> soi-meme suivi
d'une sortie par OUI. Ces boucles sont **voulues** (re-essai) et signalees en
`BOUCLE_RE_TRAVAIL` (avertissement), pas en probleme bloquant. Un cycle SANS
sortie est un `BOUCLE_BLOQUANTE` (probleme).

## Utilisation

```bash
# Un parcours
python3 detecter-cablages-manquants.py cerveau-projet/agents/clio/parcours/parcours-clio.json

# Plusieurs parcours
python3 detecter-cablages-manquants.py parcours-1.json parcours-2.json

# TOUS les parcours des agents
python3 detecter-cablages-manquants.py --tous

# Rapport markdown + detail
python3 detecter-cablages-manquants.py --tous --rapport rapport-cablages.md --verbose
```

## Options

| Option | Description |
|---|---|
| `parcours...` | Chemins des parcours JSON a verifier |
| `--tous` | Scanne `cerveau-projet/agents/*/parcours/parcours-*.json` |
| `--rapport <fichier>` | Ecrit un rapport markdown |
| `--verbose` | Affiche depart / total / atteignables par parcours |
| `--version` | Affiche la version |

## Retour

- `0` : aucun probleme bloquant (verdict `PROPRE`)
- `1` : au moins un probleme bloquant detecte
- `2` : aucun parcours fourni (aide affichee)

## Cas d'usage (garde-fou)

- **Controle croise** (Janus/Themis) : `--tous` doit donner 0 probleme sur les
  11 parcours -- toute case orpheline ou reference morte fait KO.
- **Apres modification d'un parcours** : verifier qu'aucune case n'est
  devenue orpheline et qu'aucune reference morte n'a ete creee.
