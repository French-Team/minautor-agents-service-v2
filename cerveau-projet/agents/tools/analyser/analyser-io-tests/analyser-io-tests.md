# analyser-io-tests

**Version :** 0.1.0
**Statut :** ebauche
**Categorie :** analyser
**Source :** [analyser-io-tests.py](analyser-io-tests.py)

## Pourquoi cet outil ?

La suite anti-regression devient longue (~128 s). Pour l optimiser, il faut
savoir CE QUI consomme : le temps par test (duree) ET l I/O disque pendant le
test (lecture/ecriture). Cet outil execute un ou plusieurs tests et mesure en
temps reel l I/O disque du processus + de ses enfants (via psutil.io_counters).

La premiere analyse (2026-08-16) a montre que les goulots (test-032, test-028)
ont quasi ZERO I/O disque mesure : la suite est CPU-bound / spawn-bound
(demarrage de sous-processus Python), pas I/O-bound. C est la piste
d optimisation.

## Utilisation

```bash
python3 cerveau-projet/agents/tools/analyser/analyser-io-tests/analyser-io-tests.py test-032 test-028
python3 cerveau-projet/agents/tools/analyser/analyser-io-tests/analyser-io-tests.py --serie e
python3 cerveau-projet/agents/tools/analyser/analyser-io-tests/analyser-io-tests.py --tous
python3 cerveau-projet/agents/tools/analyser/analyser-io-tests/analyser-io-tests.py <chemin/test.py> ...
python3 cerveau-projet/agents/tools/analyser/analyser-io-tests/analyser-io-tests.py --serie c,d --rapport rapport-io.md
python3 cerveau-projet/agents/tools/analyser/analyser-io-tests/analyser-io-tests.py --verbose
python3 cerveau-projet/agents/tools/analyser/analyser-io-tests/analyser-io-tests.py --version
```

## Options

| Option | Effet |
|---|---|
| `test-032 test-028 ...` | Noms de tests (resolution automatique du dossier) ou chemins directs |
| `--serie <a,b..>` | Tests des series indiquees (definition lue dans le lanceur, synchro auto) |
| `--tous` | Tous les tests du dossier tester/tests/ |
| `--rapport <fichier>` | Rapport markdown (duree + lecture/ecriture par test) |
| `--verbose` | Detail des compteurs par test |
| `--no-chrono` | Coupe le chrono de l outil lui-meme |
| `--version` | Affiche la version |

## Sorties

- Par test : duree (s), lecture (Mo), ecriture (Mo), operations de lecture/ecriture
- Synthese : duree totale, lecture/ecriture totales
- **Top consommateurs ecriture disque** (tri par octets ecrits)
- Verdict d execution par test (OK si rc=0, KO sinon)

## Dependance douce

`psutil` (io_counters) : s il est absent, l outil mesure la duree seule et
affiche un avertissement - jamais bloquant.

## Limites connues

- `io_counters` mesure l I/O reel du processus (pas les acces cache OS) : un
  test qui lit des fichiers deja en cache peut afficher peu d octets lus.
- Les enfants qui meurent entre deux echantillons (poll 20 ms) peuvent etre
  sous-comptes. La mesure est une approximation par defaut, suffisante pour
  classer les tests gourmands.
- Un test peut se comporter differemment en isolation (ex : test-032 echoue
  vite sans le contexte de la suite) : comparer avec la duree du registre-tests.
