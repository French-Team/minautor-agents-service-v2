# tester-protection-blocage

**Version :** 0.1.0
**Statut :** ebauche
**Categorie :** Tests (Protections)
**Chemin :** `agents/tools/tester/protections/`

## Description

Protection qui encadre l'execution des tests pour detecter et stopper les tests qui bloquent : processus qui ne tourne plus (CPU quasi nul), absence de sortie pendant plusieurs intervalles, sortie anormalement longue. Elle complete la protection contre les boucles infinies en detectant les blocages silencieux.

## Utilisation

```bash
# Executer une commande avec protection contre le blocage
source tester-tester-protection-blocage.sh
executer_sans_blocage "./mon-outil.sh --test" "Mon test" 60

# Executer une serie de tests
executer_tests_anti_blocage "fichier-de-tests.txt"

# En ligne de commande
tester-tester-protection-blocage.sh "./mon-outil.sh --test" "Mon test" 60
```

## Configuration

| Variable | Description | Defaut |
|---|---|---|
| `PROTECTION_blocage_TIMEOUT` | Delai maximum en secondes | 60 |
| `PROTECTION_blocage_INTERVAL` | Intervalle de surveillance en secondes | 5 |
| `PROTECTION_blocage_MAX_OUTPUT` | Taille max de sortie en octets | 1000 |

## Fonctions

| Fonction | Role |
|---|---|
| `detecter_blocage` | Verifie si un processus est bloque (CPU faible) |
| `executer_sans_blocage` | Execute une commande avec surveillance du blocage |
| `executer_tests_anti_blocage` | Execute une serie de tests anti-blocage |

## Ce que l'outil fait

1. **Lance** - La commande en arriere-plan
2. **Surveille** - L'utilisation CPU et la taille de la sortie
3. **Detecte** - Pas de changement de sortie pendant 3 intervalles (blocage suspect)
4. **Detecte** - Sortie anormalement longue (sortie infinie potentielle)
5. **Intervient** - Tue le processus si le timeout est depasse
6. **Rapporte** - Affiche la sortie partielle et retourne le code d'echec

## Signes de blocage detectes

| Signe | Detection |
|---|---|
| CPU quasi nul pendant longtemps | Processus bloque |
| Sortie inchangee pendant 3 intervalles | Blocage suspect |
| Sortie depassant le maximum | Sortie infinie potentielle |

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Test de scripts qui attendent** | Recommande - les attentes peuvent bloquer |
| **Test de scripts avec I/O** | Recommande - les lectures bloquantes sont frequentes |
| **Tests automatises** | Obligatoire - un test bloque fait attendre tout le monde |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `tester-protection-boucles-infinies` | Detecte les boucles infinies (CPU eleve) |
| `tester-protection-erreurs-silencieuses` | Detecte les erreurs sans message |
| `template-test` | Template qui charge les 3 protections par defaut |
