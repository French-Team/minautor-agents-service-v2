# tester-lancer-non-regression

**Categorie** : Tester
**Version** : 0.5.3
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

## Affichage en direct des barrieres (round 18b)

En mode barrieres (defaut), le passage des series se voit **EN DIRECT**, sans
attendre la fin de la suite (demande utilisateur 2026-08-15) :

1. **Line buffering** : `sys.stdout.reconfigure(line_buffering=True)` au
   demarrage - en sortie redirigee (pipe, entonnoir, combo), Python bufferise
   stdout et n affiche qu a la fin ; le line buffering force chaque ligne a
   s afficher des qu elle est emise.
2. **Fil de progression** : une ligne `[PROGRESSION] A V > B V > C ...` se
   complete a CHAQUE barriere franchie (V = franchie, X = bloquee) - on voit
   le parcours se construire sous le capot : `[BARRIERE A] lancement...` puis
   `[PROGRESSION] A V`, `[BARRIERE B]` puis `[PROGRESSION] A V > B V`, etc.

Le KO d une barriere est visible immediatement : `[BARRIERE BLOQUEE]` +
`[PROGRESSION] A V > B X` + details des KO - l agent constate, analyse,
repare, relance, sans avoir attendu betement la fin.

## Chrono par test (round 17)

Chaque test execute est **chronometre individuellement** (debut/fin autour de
l execution, en serie comme en pool). En fin de suite, une section
**`=== TESTS LES PLUS LENTS (top 10, chrono par test) ===`** affiche le
classement par duree DECROISSANTE : l agent identifie immediatement les tests
qui dominent le temps total et peut cibler les optimisations (comme le round
dedie a l optimisation de test-028, le goulot historique).

Le rapport markdown (`--rapport`) contient la meme section
(`## Tests les plus lents (chrono par test, top 10)`) pour une trace
persistante exploitable par les missions d optimisation.

## Protection ERREUR-SILENCIEUSE (round 18)

Le timeout interne du lanceur (180 s en serie, 300 s en pool) n est PLUS un
simple filet de securite : c est un **detecteur d erreur silencieuse**
(demande utilisateur 2026-08-15). La logique, pour UN test, UNE serie, LA
SUITE :

1. **REUSSITE** -> le test est affiche OK des qu il se termine (le lanceur
   NE ATTEND JAMAIS la fin du timeout pour continuer : des que le
   sous-processus rend la main, le resultat est affiche et la suite avance) ;
2. **ERREUR** -> verdict KO/ERREUR immediat + protection STOP (fail-fast)
   si activee ;
3. **TIMEOUT** (fin du delai programme SANS reponse ni erreur directe) ->
   verdict explicite `ERREUR SILENCIEUSE (timeout)` (et non un KO banal) :
   c est une erreur silencieuse A TROUVER / A RESOUDRE, puis l agent RELANCE
   le script ou fichier corrige.

Consequence : **les timeouts EXTERIEURS autour de l execution des tests sont
BANNIS** (regle immuable, protocole-tests) : seul le lanceur gere le delai
interne. Un test qui finit vite est affiche vite, un test qui se bloque est
signale comme erreur silencieuse, jamais un timeout exterieur ne coupe une
suite qui progresse normalement.

## Barrieres de passage (round 18 - NOUVEAU DEFAUT)

La philosophie de la suite change (demande utilisateur 2026-08-15) : la
non-regression devient un **parcours de barrieres**. Les 5 series sont
classees par **IMPORTANCE** (FONDATIONS D ABORD) et chaque serie doit etre
**100% verte pour FRANCHIR la barriere** vers la suivante :

| Serie | Niveau (importance) | Tests |
|---|---|---|
| **A** | **FONDATIONS** (nommage, ASCII/LF, template, protections, structure) | test-007, 029, 030, 042, 043, 044, 049, 050, 052, 054, 055 |
| **B** | **PARCOURS ET VALIDATEURS** (le coeur : valider-cartes, guider, migrations) | test-009, 012, 013, 014, 015, 016, 018, 021, 026, 033, 034, 037, 048 |
| **C** | **OUTILS ET COMBOS** (generateurs, combos, outils utilises souvent) | test-001, 002, 003, 004, 005, 006, 008, 010, 011, 017, 019, 020, 022, 023, 040 |
| **D** | **REGISTRE ET TRACES** (registres usages/tests, sessions, chrono) | test-025, 027, 031, 036, 038, 039, 045, 046, 047, 051 |
| **E** | **ANTI-RECURRENCE ET GARDE-FOUS SPECIFIQUES** | test-024, 028, 032, 035, 041 |

Deroulement :

1. La serie **A** (Fondations) s execute d abord : si le moindre test est KO,
   la **barriere appelle la protection STOP** (fail-fast) - la suite
   s ARRETE, le rapport de la serie est fourni (details des KO) pour
   **constater, analyser et reparer**.
2. Serie 100% verte -> **BARRIERE FRANCHIE**, on passe a la serie suivante
   (chacune a sa propre barriere).
3. Quand **toutes les barrieres sont passees** : la suite se termine et
   fournit un rapport **GLOBAL POSITIF**.
4. Janus fournit les OK a Cerberus qui active les agents habilites pour
   corriger les KO bloquants.

Mode **serie stricte** par defaut (decision utilisateur : plus direct, plus
lisible, un KO est visible immediatement sans attendre la fin de la suite).
Options conservees : `--parallele` rejoue l ancien pool de workers (round 12,
mesure reelle 119,9 s -> 91,2 s sur 31 tests) ; `--serial` force une passe
serie simple sans barrieres (echelon de secours).

> **ANTI-DEADLOCK (pool)** : en mode --parallele, chaque test redirige sa
> sortie vers un fichier temp unique (jamais de `Popen(stdout=PIPE)`) - un
> pipe non lu se bloque au-dela de 64 Ko de sortie.

## Utilisation

```bash
# Non-regression complete : BARRIERES (nouveau defaut, serie stricte)
python3 tester-lancer-non-regression.py

# Ancien mode pool de workers (option conservee)
python3 tester-lancer-non-regression.py --parallele

# Passe serie simple sans barrieres (echelon de secours)
python3 tester-lancer-non-regression.py --serial

# Ne lancer qu une serie (ex : fondations)
python3 tester-lancer-non-regression.py --series a

# Filtrer sur certains tests (le filtre est herite)
python3 tester-lancer-non-regression.py --tests test-013-cerberus-migration,test-016-migration-buffy
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
| `--relancer-ko` | MECANISATION KO : relance UNIQUEMENT les tests en KO du DERNIER run journalise (`registre-tests.jsonl`, champ `run_id` ajoute a chaque entree). Workflow : KO -> analyser -> `--relancer-ko` (revalider le correctif sans relancer la suite) -> `--series X` (valider la serie) -> suite complete. Combinaison `--relancer-ko --series X` : ne relance QUE les KO de la serie X (les KO des autres series sont affiches puis ecartes). |
| `--desactiver <a,b>` | Desactiver des tests par numero (ex : 24,32) - persiste dans `config-tests.json`, herite par le lancement suivant |
| `--activer <a,b>` | Reactiver des tests par numero (retire de la config) |
| `--etat-tests` | Affiche l'etat actif/desactive de tous les tests puis sort (ne lance rien) |
| `--no-journal` | Rotation du registre avant les tests (cumul <= 100 usages normaux, par defaut) |
| `--journal` | Ne touche pas au registre |
| `--rapport <f>` | Ecrit le bilan markdown dans un fichier (inclut les details [KO] de chaque test en echec) |
| `--version` | Affiche la version |

## Details des KO (round 16, demande utilisateur)

Quand la suite se termine avec des KO, le lanceur imprime une section
`=== DETAILS DES KO (pour action immediate) ===` : pour CHAQUE test en
echec, le nom + le nombre de points KO + les lignes `[KO]` detaillees
(avec le detail apres `--`). L agent sait immediatement POURQUOI chaque
test a echoue, sans relancer les tests individuellement. La meme
information est ecrite dans le rapport markdown (`--rapport`, section
`Tests en echec (details)`).

## Retour

- `0` : tous les tests sont OK (et registre courant a 0 si `--no-journal`)
- `1` : au moins un test KO
- `2` : aucun test trouve (ou serie inconnue)

## Historique

| Version | Date | Changement |
|---|---|---|
| 0.4.5 | 2026-08-15 | Config persistante des tests : --activer/--desactiver par numero dans config-tests.json (gitignore), heritee au lancement suivant, --etat-tests pour l'afficher, tests desactives = NON LANCE dans le bilan |
| 0.5.3 | 2026-08-16 | FILTRE SERIE (demande utilisateur) : `--relancer-ko --series X` revalide UNIQUEMENT les KO de la serie X du dernier run (les KO des autres series sont affiches puis ecartes) ; sans `--series`, comportement 0.5.2 conserve (tous les KO du dernier run) |
| 0.5.2 | 2026-08-16 | MECANISATION KO (demande utilisateur) : option `--relancer-ko` relance UNIQUEMENT les tests en KO du dernier run - champ `run_id` ajoute a chaque entree de `registre-tests.jsonl` (timestamp du debut du run) pour identifier le lancement ; Janus n a plus a deduire la liste, l outil la calcule (isoler -> revalider -> serie -> suite complete) |
| 0.5.1 | 2026-08-16 | POOL INTRA-SERIE DANS LES BARRIERES (optimisation performance) : chaque serie lance ses tests sur le pool de workers (tri duree decroissante) sauf les exclusifs (test-035 ajoute : registre partage) qui tournent en serie - gain mesure 127.8s -> ~57s |
| 0.5.0 | 2026-08-16 | PROFILS DE TESTS (demande utilisateur) : option --fichiers (auto) et --profil (manuel) - Janus choisit le profil selon les fichiers modifies (cartes, outils, tests, fiches-agents, docs, registre), definition dans profils-tests.json, affichage du profil en debut et fin de run |
| 0.4.7 | 2026-08-15 | ALIGNEMENT MODELE STANDARD (decouvert par evaluer-rating) : ajout du shebang, coding ascii, docstring Usage et option --aide - conformite outil 100% (le lanceur etait note FAIBLE par le rating) |
| 0.4.6 | 2026-08-15 | RATING DES SERIES (demande utilisateur) : le lanceur affiche en fin de run le rating de chaque serie (evaluer-rating --profil serie) et le rating GENERAL du run (--profil test --general) - criteres temps + fiabilite, note ponderee /100 |
| 0.4.4 | 2026-08-15 | GOUVERNANCE : test-057 ajoute a la serie e (marbre, garde-fous specifiques) + aux GARDE_FOUS_GLOBAUX (il ecrit temporairement parcours-cerberus -> jamais en parallele) ; test-058 ajoute a la serie b (SEUL BUFFY CORRIGE LES FICHIERS DES AGENTS, separation des pouvoirs - cartes + registre) |
| 0.4.3 | 2026-08-15 | VERROU D HABILITATION (demande utilisateur) : --agent OBLIGATOIRE + appel a proteger-verrou-habilitation AVANT toute action - seul janus peut lancer la suite, tout autre agent est bloque avec la commande d activation (regle immuable mecanisee a la source). |
| 0.4.0 | 2026-08-15 | Round 18 : BARRIERES DE PASSAGE (demande utilisateur) - series classees par IMPORTANCE (FONDATIONS D ABORD : a=nommage/ASCII-LF/template/protections, b=parcours/validateurs, c=outils/combos, d=registre/traces, e=anti-recurrence), mode serie stricte par defaut avec barriere 100% verte entre les series (STOP fail-fast au premier KO, rapport de la serie pour constater/analyser/reparer), rapport GLOBAL POSITIF quand toutes les barrieres sont passees. --parallele conserve le pool de workers, --serial passe serie simple. |
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
