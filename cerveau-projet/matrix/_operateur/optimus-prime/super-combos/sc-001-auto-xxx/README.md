---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
---

# Super-Combos AUTO-XXX

## Description

Ce super-combos enchaine intelligement les themes AUTO-XXX dans l'ordre optimal pour garantir la qualite et la securite des modifications.

## Themes enchaines

0. **PREPARATION** : Analyse et comprehension du probleme avant correction
1. **AUTO-CORRECTION** : Correction automatique des erreurs detectees (ASCII, syntaxe, imports, conventions)
2. **AUTO-TESTING** : Tests automatiques post-modification (py_compile, tests unitaires, verification d'integrite)
3. **AUTO-OPTIMISATION** : Optimisation des performances (mesurer avant, optimiser, mesurer apres)
4. **AUTO-PERFORMANCE** : Mesure de performance apres creation (comparer aux seuils, detecter regressions)
5. **AUTO-AUDIT-NEMESIS** : Audit 3 axes avant validation (cas limites, optimisation, securite)

## Utilisation

```bash
# Execution simple
python main.py executer --fichier <fichier>

# Execution complete avec toutes les phases
python main.py executer-complet --fichier <fichier>

# Verification du statut
python main.py status
```

## Outils Associes

### garde-flux2.py
Verifie qu'Optimus ne travaille QUE dans le Flux 2 (maintenance).
```bash
python garde-flux2.py --racine <chemin> [--verbose] [--strict]
```

### watchdog-flux2.py
Monitoring temps reel des violations Flux 2.
```bash
python watchdog-flux2.py --racine <chemin> --interval <sec> --log <fichier>
```

### demarrer-watchdog.py
Script pour demarrer/arreter le watchdog en arriere-plan.
```bash
python demarrer-watchdog.py demarrer [--interval <sec>]
python demarrer-watchdog.py arreter
python demarrer-watchdog.py status
python demarrer-watchdog.py violations [--dernieres <n>]
```

## Ordre d'execution

L'ordre est critique :
0. D'abord comprendre le probleme (PREPARATION)
1. Puis corriger les erreurs (AUTO-CORRECTION)
2. Ensuite tester les corrections (AUTO-TESTING)
3. Puis optimiser si necessaire (AUTO-OPTIMISATION)
4. Mesurer les performances (AUTO-PERFORMANCE)
5. Enfin, audit Nemesis avant validation (AUTO-AUDIT-NEMESIS)

## Garde-fou

- Si l'audit Nemesis echoue, la validation est bloquee
- Chaque phase est executee meme si la precedente a echoue (pour avoir le tableau complet)
- Le rapport final indique le nombre de succes/echecs
- Le watchdog detecte les violations en temps reel
