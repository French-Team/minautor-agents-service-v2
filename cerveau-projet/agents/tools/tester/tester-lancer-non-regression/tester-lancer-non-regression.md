# tester-lancer-non-regression

**Categorie** : Tester
**Version** : 0.3.1
**Statut** : ebauche
**Agent** : Vulcain
**Date** : 2026-08-11

Lance **tous les tests formels** du cerveau-projet (`tester/tests/test-0XX/`)
et produit un bilan OK/KO fiable avec comptage robuste des `[OK]`/`[KO]`.

---

## Objectif

Remplacer les **scripts temporaires de non-regression** (`.zz-nonreg-*.py`)
que les agents ecrivaient a la main. Une commande, un bilan fiable, et le
**registre d'usage en rotation** : par defaut l'outil applique une ROTATION
(`--no-journal`) qui CUMULE les usages reels des agents (memoire longue,
decision utilisateur 2026-08-14) jusqu'a un plafond de **100 entrees
normales** -- les plus anciennes sont retirees au-dela, les entrees
`script-temporaire` sont toujours preservees et ne comptent pas dans le
plafond. Le registre est donc la SOURCE DE VERITE des usages (plus jamais
vide) : evaluer-processus (test-035) ne verifie que la fenetre recente
(7 jours) pour ignorer les usages historiques.

## Chrono et reference de temps (round 11)

Un **chrono global** demarre au debut de la premiere serie et s arrete a la
fin de la derniere : le temps ecoule est affiche a la fin de chaque passe
(mono-serie comme suite complete).

Le temps de la suite complete est compare a une **reference persistee** dans
`temps-reference.json` (dossier de l outil) :

- pas de reference -> enregistree comme base ;
- temps ameliore (plus bas) -> reference **mise a jour automatiquement** ;
- temps trop eloigne (depassement > `--seuil`, defaut 25 %) -> **SIGNAL**
  de ralentissement affiche (la reference n est PAS ecrasee par un temps
  plus lent) ;
- nombre de tests different de la reference -> **nouvelle base** enregistree
  sans SIGNAL (la suite a change, la comparaison n aurait pas de sens) ;
- `--rebase-reference` force la mise a jour ;
- `--no-reference` (sous-processus paralleles) : jamais de course sur le
  fichier - seul le processus parent lit/ecrit la reference.

Le chrono permet de **mesurer le gain reel** du mode parallele et de signaler
une regression de performance (suite qui ralentit) des qu elle depasse le
seuil par rapport au meilleur temps enregistre.

## Pool de workers (round 12)

Le mode par defaut est un **pool de workers** (`--workers <N>`, defaut
`min(cpu_count, 16)`) : les tests (hors garde-fous globaux) sont tries par
**duree decroissante** (les plus longs partent en premier) puis distribues sur
N sous-processus simultanes. Les **garde-fous globaux** (test-023/024/025/027 :
registre, sessions, scripts temporaires) tournent en serie a la fin, jamais en
parallele. `--serial` ou `--workers 1` force l ancien mode serie complet.

Mesure reelle (machine 16 coeurs, 2026-08-13) : **119,9 s -> 91,2 s (-24 %)**
pour la suite complete de 31 tests. Le goulot est test-028 (88 s, scan
documentaire) : le pool le fait tourner en parallele des autres tests.

> **ANTI-DEADLOCK** : chaque test redirige sa sortie vers un fichier temp
> unique (jamais de `Popen(stdout=PIPE)`) - un pipe non lu se bloque au-dela
> de 64 Ko de sortie (deadlock decouvert lors du round 12).

## Series (round 10)

La suite est decoupee en **5 series thematiques** pour rester rapide a mesure
que le nombre de tests grandit :

| Serie | Theme | Tests |
|---|---|---|
| **A** | Combos et coherence | test-001, 002, 003, 004, 019, 020 |
| **B** | Parcours et validateurs | test-006, 009, 012, 013, 014, 015, 016, 018, 021, 022 |
| **C** | Generateurs et catalogue | test-005, 007, 008, 010, 011, 017 |
| **D** | Registre et garde-fous | test-023, 024, 025, 026, 027, 030, 031 |
| **E** | Coherence et anti-recurrence | test-028, 029, 032, 033, 034, 035, 036, 037, 038, 039, 040 |`--series <a|b|c|d|e>` lance une seule serie ; le mode **parallele est le
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
| `--series <a,b,c,d,e,tous>` | Ne lancer qu'une serie (defaut : tous) |
| `--agent <nom>` | Nom de l'agent qui lance les tests : journalise CHAQUE test execute dans `registre-tests.jsonl` (date, agent, serie, test, verdict, duree) - sans `--agent`, aucune trace |
| `--workers <N>` | Nombre de workers paralleles (defaut : min(cpu_count, 16)) |
| `--parallele` | Mode pool de workers (defaut : distribue les tests, longs d abord) |
| `--serial` | Force le mode serie complet (ancien comportement) |
| `--seuil <pct>` | Depassement tolere avant SIGNAL de ralentissement (defaut 25) |
| `--rebase-reference` | Force la mise a jour de la reference de temps |
| `--no-reference` | Ne pas lire/ecrire la reference (sous-processus paralleles) |
| `--tests <a,b>` | Filtrer par noms de tests (separes par des virgules) |
| `--no-journal` | Rotation du registre avant les tests (cumul <= 100 usages normaux, par defaut) |
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
| 0.3.1 | 2026-08-14 | TRI du registre-tests par date/heure DECROISSANT apres chaque ajout (le plus recent en premier, meme regle que registre-usages-outils) - lignes non-JSON conservees en fin. FIX (controle Janus) : rotation_registre re-trie globalement par date apres rotation (les scripts temporaires gardes en tete cassaient le tri global du registre-usages) |
| 0.3.0 | 2026-08-14 | REGISTRE-TESTS : option `--agent <nom>` - chaque test execute est journalise dans `cerveau-projet/agents/traces/registre-tests.jsonl` (date, agent, serie, test, verdict OK/KO/ERREUR, duree secondes) sur les 2 chemins (serie et pool). Registre distinct de `registre-usages-outils.jsonl`. Sans `--agent` : aucune trace |
| 0.2.0 | 2026-08-13 | Round 12 : POOL DE WORKERS (defaut) - tests tries par duree decroissante distribues sur N workers (--workers, defaut min(cpu,16)), garde-fous globaux (test-023/024/025/027) en serie finale, anti-deadlock pipe (sortie vers fichier temp unique par test). Gain reel mesure : 119,9s -> 91,2s (-24%) |
| 0.1.6 | 2026-08-13 | Round 11b : si le nombre de tests change, nouvelle base enregistree sans SIGNAL (anti-faux positif) |
| 0.1.5 | 2026-08-12 | Round 11 : chrono global (debut premiere serie -> fin derniere) + reference de temps persistee (temps-reference.json, mise a jour auto quand meilleur, SIGNAL si depassement > --seuil, --rebase-reference, --no-reference sous-processus) |
| 0.1.4 | 2026-08-12 | Protection STOP --fail-fast : des le premier test KO, la suite est stoppee (tests restants non lances) |
| 0.1.3 | 2026-08-12 | Round 10b : le mode parallele devient le DEFAUT (--serial force l'ancien mode serie) + le filtre --tests est herite par les sous-processus paralleles |
| 0.1.2 | 2026-08-12 | Round 10 : series thematiques (--series a/b/c/d/tous) + execution parallele (--parallele) - A/B/C en sous-processus isoles (--journal), D en serie en dernier, registre protege par le parent, hors-serie signale |
| 0.1.1 | 2026-08-12 | Round 8 : archive au lieu de purger (registre-usages-outils.historique.jsonl) - SUPPRIME le 14/08 (decision utilisateur : un seul registre) |
| 0.1.0 | 2026-08-11 | Creation : non-regression complete, --no-journal protege le registre |
