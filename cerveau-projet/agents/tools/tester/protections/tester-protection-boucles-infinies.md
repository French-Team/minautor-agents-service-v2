# tester-protection-boucles-infinies

**Version :** 0.1.0
**Statut :** ebauche
**Categorie :** Tests (Protections)
**Chemin :** `agents/tools/tester/protections/`

## Description

Protection qui encadre l'execution des tests pour detecter et stopper les boucles infinies. Si un test depasse le delai maximum configure, la protection tue le processus, affiche la sortie partielle et retourne le code 124 (timeout) au lieu de laisser le test tourner indefiniment.

## Utilisation

```bash
# Lancer une commande avec protection contre les boucles infinies
source tester-tester-protection-boucles-infinies.sh
lancer_avec_protection "./mon-outil.sh --test" "Mon test" 30

# Executer une serie de tests depuis un fichier
executer_tests_avec_protection "fichier-de-tests.txt"

# En ligne de commande
tester-tester-protection-boucles-infinies.sh "./mon-outil.sh --test" "Mon test" 30
```

## Configuration

| Variable | Description | Defaut |
|---|---|---|
| `PROTECTION_TIMEOUT` | Delai maximum en secondes | 30 |
| `PROTECTION_ACTION` | Action au declenchement : kill, signal, log | kill |

## Fonctions

| Fonction | Role |
|---|---|
| `lancer_avec_protection` | Lance une commande avec timeout et surveillance |
| `executer_tests_avec_protection` | Execute une serie de tests depuis un fichier |

## Ce que l'outil fait

1. **Lance** - La commande en arriere-plan avec un timeout
2. **Surveille** - Le processus toutes les secondes
3. **Detecte** - Si le delai est depasse, le test est en boucle infinie
4. **Intervient** - Tue le processus (TERM puis KILL), affiche la sortie partielle
5. **Rapporte** - Retourne le code 124 pour signaler le timeout

## Codes de retour

| Code | Signification |
|---|---|
| 0 | Test passe dans le delai |
| 124 | Timeout - boucle infinie detectee |
| Autre | Echec du test |

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Test d'un outil qui boucle** | Toujours - on ne sait jamais si un test part en boucle |
| **Test de scripts complexes** | Recommande - les boucles sont frequentes |
| **Tests automatises** | Obligatoire - eviter d'attendre indefiniment |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `tester-protection-erreurs-silencieuses` | Detecte les erreurs silencieuses (en plus des boucles) |
| `tester-protection-blocage` | Detecte les tests qui bloquent sans tourner en boucle |
| `template-test` | Template qui charge les 3 protections par defaut |
