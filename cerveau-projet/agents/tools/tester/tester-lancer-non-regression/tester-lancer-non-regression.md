# tester-lancer-non-regression

**Categorie** : Tester
**Version** : 0.1.3
**Statut** : ebauche
**Agent** : Vulcain
**Date** : 2026-08-11

Lance **tous les tests formels** du cerveau-projet (`tester/tests/test-0XX/`)
et produit un bilan OK/KO fiable avec comptage robuste des `[OK]`/`[KO]`.

---

## Objectif

Remplacer les **scripts temporaires de non-regression** (`.zz-nonreg-*.py`)
que les agents ecrivaient a la main. Une commande, un bilan fiable, et le
**registre d'usage protege** : par defaut l'outil ARCHIVE le registre courant
vers `registre-usages-outils.historique.jsonl` (append, jamais ecrase) puis le
vide (`--no-journal`) - la memoire des declarations passees est conservee et
le detecteur-usage-scripts-temporaires reste verifiable.

## Series (round 10)

La suite est decoupee en **4 series thematiques** pour rester rapide a mesure
que le nombre de tests grandit :

| Serie | Theme | Tests |
|---|---|---|
| **A** | Combos et coherence | test-001, 002, 003, 004, 019, 020 |
| **B** | Parcours et validateurs | test-006, 009, 012, 013, 014, 015, 016, 018, 021, 022 |
| **C** | Generateurs et catalogue | test-005, 007, 008, 010, 011, 017 |
| **D** | Registre et garde-fous | test-023, 024, 025, 026, 027 |`--series <a|b|c|d>` lance une seule serie ; le mode **parallele est le
defaut** (round 10b) : les series A/B/C tournent en sous-processus isoles
(avec `--journal`) puis la serie **D en dernier** (registre et garde-fous :
jamais en parallele). `--serial` force l'ancien mode serie complet (echelon
de secours pour debug). Le filtre `--tests` est herite par les sous-processus
paralleles (un filtre cible ne lance jamais une serie complete). Le registre
d'usage est archive + efface **une seule fois** par le processus parent. Un
test sans serie affectee est signale et lance en queue (jamais oublie).

## Utilisation

```bash
# Non-regression complete (par defaut : --no-journal ET parallele)
python3 tester-lancer-non-regression.py

# Forcer l'ancien mode serie complet (debug)
python3 tester-lancer-non-regression.py --serial

# Ne lancer qu'une serie (ex : garde-fous)
python3 tester-lancer-non-regression.py --series d

# Parallelisme explicite (deja le defaut)
python3 tester-lancer-non-regression.py --parallele

# Filtrer sur certains tests (le filtre est herite par les series paralleles)
python3 tester-lancer-non-regression.py --tests test-013-cerberus-migration,test-016-migration-buffy

# Ecrire le bilan dans un rapport markdown
python3 tester-lancer-non-regression.py --rapport rapport-nonreg.md

# Laisser le registre intact (pour un usage isole)
python3 tester-lancer-non-regression.py --journal
```

## Options

| Option | Description |
|---|---|
| `--series <a,b,c,d,tous>` | Ne lancer qu'une serie (defaut : tous) |
| `--parallele` | Series A/B/C en parallele puis D en serie (defaut) |
| `--serial` | Force le mode serie complet (ancien comportement) |
| `--tests <a,b>` | Filtrer par noms de tests (separes par des virgules) |
| `--no-journal` | Archive le registre dans l'historique + vide le courant (par defaut) |
| `--journal` | Ne touche pas au registre |
| `--rapport <f>` | Ecrit le bilan markdown dans un fichier |
| `--version` | Affiche la version |

## Retour

- `0` : tous les tests sont OK (et registre courant a 0 si `--no-journal`)
- `1` : au moins un test KO
- `2` : aucun test trouve (ou serie inconnue)

## Historique

| Version | Date | Changement |
|---|---|---|
| 0.1.3 | 2026-08-12 | Round 10b : le mode parallele devient le DEFAUT (--serial force l'ancien mode serie) + le filtre --tests est herite par les sous-processus paralleles |
| 0.1.2 | 2026-08-12 | Round 10 : series thematiques (--series a/b/c/d/tous) + execution parallele (--parallele) - A/B/C en sous-processus isoles (--journal), D en serie en dernier, registre protege par le parent, hors-serie signale |
| 0.1.1 | 2026-08-12 | Round 8 : archive au lieu de purger (registre-usages-outils.historique.jsonl, append dedoublonne) - la memoire des declarations est conservee |
| 0.1.0 | 2026-08-11 | Creation : non-regression complete, --no-journal protege le registre |
