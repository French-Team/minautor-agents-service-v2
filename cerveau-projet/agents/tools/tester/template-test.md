---
# Template de Test avec Protections
# Version : 0.1.0
# Statut : ebauche

test:
  nom: "test-XXX-nom-outil"
  version: "0.1.0"
  outil_teste: "nom-de-l-outil"
  cree: "2026-08-06"

---

# Test: [NOM DE L'OUTIL]

## Objectif

Tester les fonctionnalites de l'outil [nom-de-l-outil].

## Protections utilisees

- [ ] tester-protection-boucles-infinies.sh
- [ ] tester-protection-erreurs-silencieuses.sh
- [ ] tester-protection-blocage.sh

## Tests

### Test 1: [Description du test]

**Objectif**: Verifier que...

**Commande**:
```bash
./chemin/vers/outil.sh [options]
```

**Sortie attendue**:
```
[Sortie attendue]
```

**Code de retour**: 0

---

### Test 2: [Description du test]

**Objectif**: Verifier que...

**Commande**:
```bash
./chemin/vers/outil.sh [options]
```

**Sortie attendue**:
```
[Sortie attendue]
```

**Code de retour**: 0

---

## Script de test

```bash
#!/bin/bash
# test-XXX-nom-outil.sh

# Chemin vers les protections
PROTECTIONS_DIR="$(dirname "$0")/../protections"

# Charger les protections
source "$PROTECTIONS_DIR/tester-protection-boucles-infinies.sh"
source "$PROTECTIONS_DIR/tester-protection-erreurs-silencieuses.sh"
source "$PROTECTIONS_DIR/tester-protection-blocage.sh"

# Configuration
OUTIL_DIR="$(dirname "$0")/../../[categorie]/[nom-outil]"
OUTIL="$OUTIL_DIR/[nom-outil].sh"

echo "=== Test: [NOM DE L'OUTIL] ==="
echo "Date: $(date)"
echo ""

# Test 1: [Description]
echo "--- Test 1: [Description] ---"
executer_test_securise "$OUTIL [options]" "Test 1" 0
result1=$?

# Test 2: [Description]
echo "--- Test 2: [Description] ---"
executer_test_securise "$OUTIL [options]" "Test 2" 0
result2=$?

# Rapport final
echo ""
echo "=== Rapport ==="
total=2
passed=0
[ $result1 -eq 0 ] && passed=$((passed + 1))
[ $result2 -eq 0 ] && passed=$((passed + 1))

echo "Total: $total"
echo "Reussis: $passed"
echo "Echecs: $((total - passed))"

# Generer le rapport
generer_rapport "[NOM DU TEST]" $total $passed $((total - passed))

# Sortie
[ $((total - passed)) -eq 0 ] && exit 0 || exit 1
```

## Rapports

Les rapports seront generes dans:
```
/tmp/test-logs/rapport_[nom-test].md
```

## Checklist

Avant de valider les tests:

- [ ] Les protections sont chargees
- [ ] Chaque test est numerote
- [ ] Le timeout est configure
- [ ] Les erreurs sont capturees
- [ ] Le rapport est genere
- [ ] Les problemes sont identifies
