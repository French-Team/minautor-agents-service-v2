---
# Test: corrections evaluer-agents et evaluer-coherence
# Version : 0.1.0
# Statut : ebauche

test:
  nom: "test-001-evaluer-agents-coherence"
  version: "0.1.0"
  outil_teste: "evaluer-agents + evaluer-coherence"
  cree: "2026-08-07"
---

# Test: Corrections evaluer-agents et evaluer-coherence

## Objectif

Verifier que les 3 corrections apportees par Vulcain sont efficaces :

1. **evaluer-agents** : les dossiers `__pycache__` ne sont plus comptes comme des outils manquants
2. **evaluer-coherence** : les liens `../pense-betes/...` sont resolus depuis le projet root, pas seulement depuis `cerveau-projet/`
3. **evaluer-coherence** : les commandes systeme (`cat`, `grep`, `sed`, `basher`) ne sont plus signalees comme des "outils casses"

## Protections utilisees

- [x] tester-protection-boucles-infinies/tester-protection-boucles-infinies.sh
- [x] tester-protection-erreurs-silencieuses/tester-protection-erreurs-silencieuses.sh
- [x] tester-protection-blocage/tester-protection-blocage.sh

## Tests

### Test 1: evaluer-agents exclut __pycache__

**Objectif**: Verifier qu'aucun faux positif `__pycache__` n'apparait dans la sortie de `evaluer-agents`.

**Commande**:
```bash
python3 evaluer-agents/evaluer-agents.py
```

**Sortie attendue**: Aucune ligne contenant "Outil `__pycache__`"

**Code de retour**: 0

---

### Test 2: score evaluer-agents > 50/100

**Objectif**: Avant la correction, le score etait 23/100 (79 faux erreurs `__pycache__`). Apres correction, le score doit depasser 50/100.

**Commande**:
```bash
python3 evaluer-agents/evaluer-agents.py | grep "Score agents"
```

**Sortie attendue**: Score agents : 97/100 (ou plus, 1 vrai outil incomplet: generateurs-commande)

**Code de retour**: 0

---

### Test 3: evaluer-coherence exclut les commandes systeme

**Objectif**: Verifier que `cat`, `grep`, `sed`, `basher` ne sont plus signales comme des "outils casses".

**Commande**:
```bash
python3 evaluer-coherence/evaluer-coherence.py
```

**Sortie attendue**: "Tous les outils references existent" (aucune commande systeme signalee)

**Code de retour**: 0

---

### Test 4: faux positifs liens structures resolus

**Objectif**: Les liens `pense-betes/conventions/structures/convention-*.md` existent sous `cerveau-projet/` mais etaient signales comme casses. Apres correction (cible_racine depuis projet root), ils doivent disparaettre.

**Commande**:
```bash
python3 evaluer-coherence/evaluer-coherence.py
```

**Sortie attendue**: Aucun lien contenant "pense-betes/conventions/structures"

**Code de retour**: 0

---

### Test 5: evaluer-coherence dit "Tous les outils references existent"

**Objectif**: Confirmer que la section "Outils references par les agents" est OK.

**Commande**:
```bash
python3 evaluer-coherence/evaluer-coherence.py | grep "Tous les outils"
```

**Sortie attendue**: "Tous les outils references existent"

**Code de retour**: 0

---

## Script de test

- [Python] test-001-evaluer-agents-coherence.py
- [Bash] test-001-evaluer-agents-coherence.sh

## Rapports

Les rapports seront generes dans:
```
/tmp/test-logs/rapport_test-001-evaluer-agents-coherence.md
```

## Checklist

- [x] Les protections sont chargees
- [x] Chaque test est numerote
- [x] Le timeout est configure
- [x] Les erreurs sont capturees
- [x] Le rapport est genere
- [x] Les problemes sont identifies
