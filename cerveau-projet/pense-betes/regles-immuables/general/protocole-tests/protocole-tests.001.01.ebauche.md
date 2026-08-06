---
# Protocole de Tests avec Protections
# Comment tester les outils du cerveau-projet

protocole:
  nom: "protocole-tests"
  version: "0.2.0"
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
source "$(dirname "$0")/../protections/tester-protection-boucles-infinies.sh"
source "$(dirname "$0")/../protections/tester-protection-erreurs-silencieuses.sh"

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

## Checklist de validation

Avant de valider un test :

- [ ]Les protections sont chargees
- [ ]Chaque test est numerote
- [ ]Le timeout est configure
- [ ]Les erreurs sont capturees
- [ ]Le rapport est genere
- [ ]Les problemes sont identifies
