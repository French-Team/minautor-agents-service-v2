# test-015-valider-case-garde-fou.py

**Testeur** : Morpheus (testeur dedie)
**Date** : 2026-08-11
**Objet** : Test formel du garde-fou anti-pollution de valider-case v1.0.1 (lecon : rapport a la racine cree par une commande sans --rapport). - valider-case v1.0.0 ecrivait son rapport par defaut (rapport-valider-case-<date>.md) dans le repertoire courant quand --rapport et --dry-run etaien

---

## Contexte

Test formel de la suite de non-regression (test-001 a test-021).
Ce test est reference au catalogue generateurs-commande : toute
modification de son perimetre doit etre validee par Morpheus.

## Execution

```bash
python3 test-015-valider-case-garde-fou.py
```
