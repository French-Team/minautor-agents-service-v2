---
# Template de Test avec Protections
# Version : 0.1.0
# Statut : ebauche

test:
  nom: "test-002-combos-moteur"
  version: "0.1.0"
  outil_teste: "combos-moteur"
  cree: "2026-08-08"
  spec_reference: "spec-combos-moteur.001.01.ebauche.md (v0.1.0)"

---

# Test: combos-moteur

## Objectif

Tester le moteur generique de combos declaratifs (`combos-moteur`) cree par
Vulcain (etape 2 du plan combo-orchestrateur) : execution d'une
`definition-combo.json` case par case (generateur / outil / controle / fin),
variables + interpolation, persistance optionnelle, modes CLI.

## Protections utilisees

- [x] tester-protection-boucles-infinies (timeout sur chaque subprocess du test)
- [x] tester-protection-erreurs-silencieuses (chaque retour est verifie)
- [x] tester-protection-blocage (timeout global sur chaque commande)

## Tests

### Test 1: --liste affiche toutes les cases

**Objectif**: Verifier que `--liste` affiche les 5 cases de la definition
exemple (c1 a c5) avec les 4 types (generateur, outil, controle, fin).

**Commande**:
```bash
python3 combos-moteur.py exemple-combo.json --liste
```

**Code de retour**: 0

### Test 2: Navigation de case_depart jusqu'a la fin (chemin OUI)

**Objectif**: Verifier que les cases s'enchainent de c1 (depart) jusqu'a une
case fin, avec les reponses des controles fournies via `--reponses`.

**Commande**:
```bash
python3 combos-moteur.py exemple-combo.json --reponses "c3=OUI" --verbose
```

**Sortie attendue**: `COMBO TERMINE` + message "la commande generee est correcte".

**Code de retour**: 0

### Test 3: Interpolation {var}

**Objectif**: Verifier que `{cmd1}` (sortie de la case generateur) est remplace
par la commande generee dans la commande de la case outil suivante.

**Sortie attendue**: la commande generee (avec `sidentifier`) apparait dans la
sortie verbose.

### Test 4: Generateur AUTO

**Objectif**: Verifier que la case generateur appelle `generateurs-commande
--reponses` (mode AUTO, sans interaction) et obtient la commande composee.

**Sortie attendue**: la commande contient `activer-agent-principal` (script du
catalogue) composee automatiquement.

### Test 5: Controle branches

**Objectif**: Verifier que `--reponses "c3=OUI"` emprunte la branche OUI
(c4) et `--reponses "c3=NON"` la branche NON (c5).

**Sortie attendue**: messages de fin differents selon la branche.

### Test 6: Variable manquante

**Objectif**: Verifier qu'une interpolation vers une variable inconnue
(`{inconnue}`) produit une erreur claire et un code retour 1.

**Commande**:
```bash
python3 combos-moteur.py definition-invalide.json
```

**Sortie attendue**: `Variable non trouvee` + code 1.

### Test 7: Fin

**Objectif**: Verifier que le combo s'arrete a la case fin et affiche le
message de fin.

### Test 8: Dry-run

**Objectif**: Verifier que `--dry-run` affiche les commandes (`[DRY-RUN]`) sans
les executer (le message de fin de la case outil n'apparait pas).

**Commande**:
```bash
python3 combos-moteur.py exemple-combo.json --dry-run --reponses "c3=OUI"
```

**Code de retour**: 0

### Test 9: Parite .py/.sh

**Objectif**: Verifier que `combos-moteur.py` et `combos-moteur.sh` produisent
la meme liste et la meme navigation sur la meme definition.

**Commande**:
```bash
python3 combos-moteur.py exemple-combo.json --liste
bash combos-moteur.sh exemple-combo.json --liste
```

### Test 10: Nommage

**Objectif**: Verifier que `valider-nommage --type outil` valide le .py et le .sh
(dossier combos/ -> prefixe combos-).

### Test 11: ASCII

**Objectif**: Verifier 0 caractere non-ASCII sur le .py, le .sh, la doc, le JSON
exemple et la spec.

### Test 12: Syntaxe

**Objectif**: Verifier `bash -n` sur le .sh et `python3 -m py_compile` sur le .py.

## Script de test

Le script principal est `test-002-combos-moteur.py` (les 12 cas sont executes
par Python, chaque retour verifie). Aucun fichier du cerveau n'est modifie par
le test (seule une definition invalide temporaire dans /tmp est creee).

## Rapports

Le verdict est affiche en fin de script :
```
Total: N
Reussis: N
Echecs: 0
VERDICT: REUSSI (combos-moteur valide)
```

## Checklist

- [x] Les protections sont chargees (timeouts + verification des retours)
- [x] Chaque test est numerote (1 a 12)
- [x] Le timeout est configure (60s par commande)
- [x] Les erreurs sont capturees (stdout + stderr verifies)
- [x] Le rapport est genere (verdict en fin de script)
- [x] Les problemes sont identifies (messages ECHEC detailles)
