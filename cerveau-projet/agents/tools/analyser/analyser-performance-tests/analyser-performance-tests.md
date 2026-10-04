---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# analyser-performance-tests

**Categorie** : Analyser
**Version** : 0.1.0
**Statut** : ebauche

---

## Objectif

Analyser la performance de la suite anti-regression : lire le registre des
lancements de tests (`registre-tests.jsonl`) et classer les tests du DERNIER
RUN COMPLET par duree consommee, du plus gros consommateur au moins.

Cet outil sert a repondre a la question : "quels tests dominent le temps de la
suite et meriteraient d etre optimises ?" (ex : test-032, test-028). Il
complemente la section "Tests les plus lents" du lanceur en fournissant un
rapport DEDIE, exploitable pour les decisions d optimisation.

---

## Pourquoi cet outil ?

- Le lanceur affiche un top 10 du run courant, mais rien n analyse l historique
  pour repondre "quel test consomme le plus globalement ?"
- Les decisions d optimisation (reduire le temps total de la suite) ont besoin
  d un classement clair + du cumul pour identifier le seuil d action.
- Le registre-tests.jsonl accumule deja (date, agent, serie, test, verdict,
  duree) a CHAQUE lancement - l outil exploite cette source sans la modifier.

---

## Utilisation

```bash
# Classement du dernier run (defaut : fenetre 10 min autour de la date max)
python3 analyser-performance-tests.py

# Fenetre plus courte (isole mieux un run rapide)
python3 analyser-performance-tests.py --fenetre-minutes 5

# Top 15 des plus gros consommateurs seulement
python3 analyser-performance-tests.py --top 15

# Rapport markdown (classement + cumul)
python3 analyser-performance-tests.py --rapport rapport-perf.md

# Detail (verdicts par test) + chrono coupe
python3 analyser-performance-tests.py --verbose --no-chrono

# Version
python3 analyser-performance-tests.py --version
```

## Options

| Option | Description |
|---|---|
| `--fenetre-minutes <N>` | Fenetre temporelle du dernier run (defaut 10) |
| `--top <N>` | N afficher que les N premiers consommateurs |
| `--rapport <f>` | Ecrit le rapport markdown (classement + cumul) |
| `--verbose` | Detail : verdicts par test |
| `--dry-run` | Affiche sans ecrire le rapport |
| `--no-chrono` | Coupe le chrono de l outil lui-meme |
| `--version` | Affiche la version |

---

## Definition du "dernier run"

Le registre-tests est alimente par `tester-lancer-non-regression` : chaque
test execute est journalise avec sa date. Un run complet dure ~100 s. L outil
isole le dernier run en prenant toutes les entrees dans une fenetre temporelle
(10 min par defaut) autour de la date la plus recente.

> ATTENTION : si le registre-tests est vide ou incomplet (bug historique
> test-051 qui purgeait les entrees janus), l outil affiche ce qu il trouve et
> le rapport le reflete. La correction du registre est traitee par Morpheus.

---

## Sortie

```
=== ANALYSE PERFORMANCE DES TESTS (dernier run) ===
Dernier run : 2026-08-15 19:00:20 (5 entrees, 5 tests distincts, fenetre 0 min)
Duree totale consommee : 74.5 s

#    Duree(s) Test                                                 Serie(s)
1    38.7     test-032-pool-workers.py                           d
2    25.2     test-028-coherence-documentaire.py                 e
...
```

Verdict : l outil classe toujours (0 probleme de structure possible), le
rapport markdown ajoute la colonne DUREE CUMULEE pour identifier le seuil :
les N premiers tests qui representent 80% du temps sont les cibles
d optimisation prioritaires.

---

## Historique

| Version | Date | Description |
|---|---|---|
| 0.1.0 | 2026-08-15 | Creation : classement du dernier run par duree, top, rapport markdown |
