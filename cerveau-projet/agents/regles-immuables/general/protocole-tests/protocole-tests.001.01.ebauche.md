---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---

# Protocole de Tests avec Protections
# Comment tester les outils du cerveau-projet

protocole:
  nom: "protocole-tests"
  version: "0.2.3"
  statut: "ebauche"
  cree: "2026-08-06"

---

# Protocole de Tests avec Protections

## Objectif

Definir comment tester les outils bash du cerveau-projet avec des protections qui garantissent que les tests ne se bloquent pas.

## Principe fondamental

> **REGLE ABSOLUE** : Les tests doivent etre ENVELOPPES par des protections qui controlent, analysent et interviennent sur leur deroulement.

## Structure des tests

```
tests/
  protections/           # Protections qui englobent les tests
    tester-protection-boucles-infinies.sh
    tester-protection-erreurs-silencieuses.sh
    tester-protection-blocage.sh
  test-001-nom-outil/    # Dossier du test (numerote)
    test-001-outil.md    # Documentation du test
    test-001-outil.sh    # Script du test
  test-002-nom-outil/
    ...
```

## Numerotation des tests

| Element | Format | Exemple |
|---|---|---|
| **Fichier de test** | `test-XXX-nom-outil.md` | `test-001-valider-ascii.md` |
| **Script de test** | `test-XXX-nom-outil.sh` | `test-001-valider-ascii.sh` |
| **Tests dans le fichier** | `Test 1`, `Test 2`, etc. | `Test 1: Detection des accents` |
| **Repertoire du test** | `test-XXX-nom-outil/` | `test-001-valider-ascii/` |

## Protections

### Principe

Les protections sont des fichiers bash qui :
1. **Englobent** les tests
2. **Surveillent** leur deroulement
3. **Detectent** les problemes (boucles, erreurs, blocages)
4. **Interviennent** si necessaire (arreter, rapporter)

### Types de protections

| Protection | Detection | Action |
|---|---|---|
| **Boucles infinies** | Depassement delai | Arreter le processus |
| **Erreurs silencieuses** | Code de retour inatendu | Signaler l'erreur |
| **Tests qui bloquent** | Pas de reponse pendant X sec | Arreter et rapporter |
| **Memoire insuffisante** | Depassement quota | Arreter proprement |
| **Sortie infinie** | Trop de sorties stdout/stderr | Tronquer et signaler |

### Structure d'un fichier de protection

```bash
#!/bin/bash
# protection-xxx.sh
# Protection contre [type de probleme]

TIMEOUT=30  # Delai maximum en secondes

# Demarrer le test avec protection
lancer_avec_protection() {
    local test_cmd="$1"
    local test_name="$2"
    
    # Lancer avec timeout
    timeout $TIMEOUT bash -c "$test_cmd"
    local exit_code=$?
    
    # Verifier si timeout (code 124)
    if [ $exit_code -eq 124 ]; then
        echo "[ERREUR] Timeout: $test_name a depasse ${TIMEOUT}s"
        echo "  -> Le test semble etre en boucle infinie"
        return 1
    fi
    
    return $exit_code
}
```

## Utilisation des protections

### Dans un fichier de test

```bash
#!/bin/bash
# test-001-outil.sh

# Charger les protections
source "$(dirname "$0")/../protections/tester-protection-boucles-infinies/tester-protection-boucles-infinies.sh"
source "$(dirname "$0")/../protections/tester-protection-erreurs-silencieuses/tester-protection-erreurs-silencieuses.sh"

# Test 1: Detection des accents
echo "=== Test 1: Detection des accents ==="
lancer_avec_protection "./outil.sh --test-accent" "Detection accents"
result1=$?

# Test 2: Correction des accents
echo "=== Test 2: Correction des accents ==="
lancer_avec_protection "./outil.sh --test-correction" "Correction accents"
result2=$?

# Rapport final
echo "=== Rapport ==="
echo "Test 1: $([ $result1 -eq 0 ] && echo OK || echo ERREUR)"
echo "Test 2: $([ $result2 -eq 0 ] && echo OK || echo ERREUR)"
```

## Processus de test

### 1. Preparation

- [ ]Verifier que les protections existent
- [ ]Numeroter le fichier de test
- [ ]Creer le dossier de test
- [ ]Ecrire la documentation du test

### 2. Execution

- [ ]Charger les protections
- [ ]Executer chaque test avec protection
- [ ]Capturer les codes de retour
- [ ]Verifier les sorties

### 3. Rapport

- [ ]Generer le rapport de test
- [ ]Identifier les problemes
- [ ]Documenter les erreurs
- [ ]Proposer des corrections

## Codes de retour des protections

| Code | Signification |
|---|---|
| 0 | Test reussi |
| 1 | Test echoue |
| 124 | Timeout (boucle infinie detectee) |
| 137 | Processus tue (blocage detecte) |
| 255 | Erreur de protection |

## Delegation des tests

REGLE IMMUABLE -- DELEGATION : SEUL MORPHEUS ECRIT ET EXECUTE LES TESTS.

- Seul l'agent Morpheus (testeur) cree, adapte et execute les fichiers de test
  `test-XXX-*` : la creation, la mise a jour et meme l'adaptation mineure d'un
  test existant (version, nombre de points, attentes) sont son role.
- Aucun autre agent ne touche a un fichier de test, meme pour une correction
  rapide ou un simple controle (bash -n, py_compile, cas dans exemples/).
- Quand une mission implique des tests, l'agent d'origine transmet le besoin a
  Morpheus dans la mission : test-XXX a creer/adapter + points a couvrir.
- Morpheus donne son verdict uniquement via les tests executes et revient a
  l'agent qui l'a active (chaine bout-en-bout).

### Garde-fous de non-regression

REGLE IMMUABLE -- GARDE-FOU FIN DE PARCOURS : APRES TOUTE MODIFICATION D'UNE FIN
DE PARCOURS, LE TEST-018 DOIT RESTER VERT.

- Une fin de parcours = toute case de type `fin` (titre `FIN - Reactiver Cerberus`
  ou `FIN - Activer X`) dans les 11 parcours agents (parcours-*.json).
- Apres CHAQUE creation, edition ou suppression d'une fin de parcours (titre,
  message, commande, suivant), executer :
  `python3 cerveau-projet/agents/tools/tester/tests/test-018-fins-reactivation/test-018-fins-reactivation.py`
- Le test-018 verifie : regle Pattern 13 (toute fin REACTIVER porte la condition
  `activation directe par Cerberus` OU est le dernier maillon avec bilan
  consolide), les 4 fins precisees (atlas c11, clio c12, minerve c10, themis
  c13) et l'anti-regression du piege reactiver (aucune fin `Activer X` ne doit
  contenir la commande reactiver).
- Verdict attendu : 0 KO. Si KO, corriger la fin modifiee (condition manquante,
  piege reactiver reintroduit) AVANT de valider la mission.
- Ce garde-fou s'ajoute aux tests de navigation existants (test-013, test-016).

REGLE IMMUABLE -- RE-SCAN COMPLET : APRES CHAQUE REFONTE D'OUTIL OU DE PARCOURS,
RE-SCANNER TOUTE LA SUITE (TEST-009 A TEST-018) ET EXIGER 0 KO.

- Une refonte d'outil = bump de version d'un .py/.sh/.md/spec, modification
  d'interface (options, sous-commandes) ou de comportement.
- Une refonte de parcours = migration (indices references + cases action),
  ajout/suppression de cases ou de fins, changement de version du parcours.
- Apres CHAQUE refonte, re-scanner TOUTE la suite formelle (test-009 a
  test-018) :
  `for d in cerveau-projet/agents/tools/tester/tests/test-0*/; do
   python3 $d/$(basename $d).py || break; done`
  (chaque test-0XX-nom/ contient test-0XX-nom.py a executer)
- Verdict attendu : 0 KO partout. Si KO :
  1. versions attendues obsoletes (lecon : verifier apres chaque bump
     d'outil -- la version affichee par --version doit correspondre a celle
     attendue par le test),
  2. temoins de test obsoletes (lecon : verifier apres chaque migration de
     parcours -- un temoin A ALLEGER peut devenir CONFORME).
- Seul Morpheus adapte les tests obsoletes (REGLE IMMUABLE DELEGATION), et
  ce AVANT de valider la mission.

## Checklist de validation

Avant de valider un test :

- [ ]Les protections sont chargees
- [ ]Chaque test est numerote
- [ ]Le timeout est configure
- [ ]Les erreurs sont capturees
- [ ]Le rapport est genere
- [ ]Les problemes sont identifies
