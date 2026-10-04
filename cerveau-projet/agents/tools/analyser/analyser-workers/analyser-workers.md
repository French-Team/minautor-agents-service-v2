---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# analyser-workers

**Categorie** : Analyser
**Version** : 0.1.0
**Statut** : ebauche

---

## Objectif

Mesurer le temps d execution de la suite de non-regression (ou d un
sous-ensemble de tests) a DIFFERENTS nombres de workers paralleles, pour
trouver l optimum reel qui minimise le temps total.

Complement dynamique de `configurer-environnement` : la config donne un point
de depart theorique (CPU/RAM), cet outil mesure le point d equilibre REEL
(parallelisme utile vs contention).

---

## Pourquoi cet outil ?

- Le lanceur utilisait `min(cpu_count, 16)` code en dur : rien ne prouve que
  16 workers soit l optimum sur la machine reelle (contention disque, GIL,
  RAM).
- Une etude d echelle (1/2/4/8/16 workers -> temps) fournit la donnee pour
  regler `configurer-environnement` sur une mesure, pas une intuition.

---

## Utilisation

```bash
# Etude sur 2 tests connus, aux 5 paliers par defaut
python3 analyser-workers.py --tests test-028,test-032

# Paliers personnalises
python3 analyser-workers.py --tests test-032 --workers-list 1,2,4,8

# Rapport markdown
python3 analyser-workers.py --tests test-028,test-032 --rapport etude-workers.md

# Voir les commandes sans lancer (--dry-run)
python3 analyser-workers.py --tests test-032 --dry-run

# Version
python3 analyser-workers.py --version
```

## Options

| Option | Description |
|---|---|
| `--tests <liste>` | Tests a mesurer, separes par des virgules |
| `--workers-list <l>` | Nombres de workers a tester (defaut 1,2,4,8,16) |
| `--agent <nom>` | Agent transmis au verrou du lanceur (defaut vulcain) |
| `--rapport <f>` | Ecrit le rapport markdown |
| `--verbose` | Detail des commandes lancees |
| `--dry-run` | Affiche les commandes sans les lancer |
| `--no-chrono` | Coupe le chrono de l outil |
| `--version` | Affiche la version |

---

## Garde-fous integres

- Chaque run est lance avec `--no-reference` (ne touche pas la reference de
  temps globale) et `--journal` (ne touche pas au registre d usage) : une
  etude d echelle ne pollue jamais les metriques de production.
- Le verrou d habilitation du lanceur reste actif : `--agent` est obligatoire
  et doit etre habilite (vulcain = liste blanche developpeur).

---

## Sortie

```
=== ETUDE D ECHELLE DES WORKERS (temps mural par N workers) ===
Workers    Duree(s)     Verdict
1          40.12        OK
2          22.05        OK
4          12.88        OK
8          12.44        OK
16         13.10        OK

RECOMMANDATION : 8 workers (12.44s) - gain 69% vs le pire (1 workers, 40.12s)
```

---

## Historique

| Version | Date | Description |
|---|---|---|
| 0.1.0 | 2026-08-17 | Creation : etude d echelle des workers, recommandation, rapport markdown |
