# evaluer-rating

**Version :** 0.1.0-py
**Statut :** beta
**Categorie :** Evaluer
**Proprietaire :** Themis (outil partage)

## Pourquoi cet outil ?

Les performances, la fiabilite et la qualite doivent etre MESUREES, pas
supposees. `evaluer-rating` attribue une **note ponderee /100** a chaque entite
du cerveau-projet (test, serie, outil, script temporaire, fiche) selon des
criteres definis dans `profils-rating.json` : temps d execution, fiabilite
historique, conformite aux modeles, consommation de tokens, environnement
systeme, usage reel.

Le rating sert de **critere d evaluation** : il devient une protection
integree partout (les tests affichent leur note en fin d execution) et fournit
des donnees objectives pour optimiser la suite de non-regression (goulots,
series faibles).

## Profils et criteres

Les profils vivent dans `profils-rating.json` (fichier JSON dedie). Chaque
profil definit des criteres avec POIDS (somme = 100), une source de donnees et
un mode de score 0-100.

| Profil | Criteres | Poids |
|---|---|---|
| **test** | temps, fiabilite, conformite, tokens, systeme | 35 / 30 / 20 / 10 / 5 |
| **serie** | temps, fiabilite | 50 / 50 |
| **outil** | conformite, temps, tokens, usage | 40 / 30 / 20 / 10 |
| **script-temp** | conformite, tokens, nettoyage | 60 / 20 / 20 |
| **fiche** | conformite, synchro, tokens | 50 / 30 / 20 |

### Modes de score

| Mode | Logique |
|---|---|
| `plus-rapide-mieux` | Bareme absolu : 100 si duree <= base (3s test / 25s serie), decroit de 20 pts par multiple de base |
| `ko-historique` | Fiabilite sur les 10 derniers lancements : 0 KO = 100, KO recent = penalite |
| `presence-marqueurs` | Proportion de marqueurs du modele presents (shebang, coding ascii, triplet, etc.) |
| `moins-tokens-mieux` | Taille du fichier vs base : plus compact = meilleur score |
| `environnement` | profil-systeme present dans le classeur variables-actuelles.md |
| `utilise` | Entrees reelles au registre-usages-outils.jsonl |
| `propre` | Aucun residu dans les dossiers tmp-* |
| `synchro` | Coherence fiche / parcours / AGENTS.md |

## Usage

```
python3 evaluer-rating.py --profil test --cible test-032-pool-workers
python3 evaluer-rating.py --profil test --tous
python3 evaluer-rating.py --profil serie --tous
python3 evaluer-rating.py --profil outil --cible lire-fichier --verbose
python3 evaluer-rating.py --profil serie --tous --rapport rapport-rating.md
```

## Options

| Option | Description |
|---|---|
| `--profil <nom>` | test, serie, outil, script-temp, fiche (defaut: test) |
| `--cible <nom>` | Entite a noter |
| `--tous` | Noter toutes les entites du profil + rating GENERAL |
| `--rapport <fichier>` | Ecrire le rapport markdown (sans couleurs) |
| `--verbose` | Detail des scores par critere |
| `--no-chrono` | Couper le chrono de l outil |
| `--version` | Afficher la version |
| `--aide`, `-h` | Afficher l aide |

## Verdicts

| Note | Verdict |
|---|---|
| >= 85 | EXCELLENT |
| >= 70 | BIEN |
| >= 50 | MOYEN |
| < 50 | FAIBLE |

## Sources de donnees

- `cerveau-projet/agents/traces/registre-tests.jsonl` : durees + verdicts des tests
- `cerveau-projet/agents/traces/registre-usages-outils.jsonl` : usage reel des outils
- `cerveau-projet/agents/classeur-variables/stockage/variables-actuelles.md` : profil-systeme
- Fichiers du projet : conformite aux modeles, tailles

## Exemple

```
$ python3 evaluer-rating.py --profil serie --tous
a : 98.2/100 (EXCELLENT)
b : 100.0/100 (EXCELLENT)
c : 35.0/100 (FAIBLE)      <- serie la plus lente (151s)
d : 83.5/100 (BIEN)
e : 45.0/100 (FAIBLE)      <- serie la plus lente (191s)

=== RATING GENERAL (serie) : 72.3/100 (BIEN) ===
```
