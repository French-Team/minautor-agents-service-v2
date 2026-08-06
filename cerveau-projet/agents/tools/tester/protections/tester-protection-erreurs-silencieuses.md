# tester-protection-erreurs-silencieuses

**Version :** 0.1.0
**Statut :** ebauche
**Categorie :** Tests (Protections)
**Chemin :** `agents/tools/tester/protections/`

## Description

Protection qui encadre l'execution des tests pour detecter les erreurs silencieuses : code de sortie inattendu, stdout vide, erreurs dans stderr, mots-cles d'erreur dans la sortie. Chaque test est journalise dans `/tmp/test-logs/` et un rapport peut etre genere automatiquement.

## Utilisation

```bash
# Executer un test securise
source tester-tester-protection-erreurs-silencieuses.sh
executer_test_securise "./mon-outil.sh --test" "Mon test" 0

# Valider qu'une sortie contient un pattern
valider_sortie "fichier-stdout.log" "pattern attendu" "Description"

# Generer un rapport
generer_rapport "Nom du test" 10 8 2

# En ligne de commande
tester-tester-protection-erreurs-silencieuses.sh "./mon-outil.sh --test" "Mon test" 0
```

## Configuration

| Variable | Description | Defaut |
|---|---|---|
| `PROTECTION_LOG_DIR` | Dossier des logs | /tmp/test-logs |
| `PROTECTION_VERIFY_OUTPUT` | Verifier que le stdout n'est pas vide | true |

## Fonctions

| Fonction | Role |
|---|---|
| `executer_test_securise` | Execute un test avec verification des erreurs silencieuses |
| `valider_sortie` | Verifie qu'un pattern est present dans une sortie |
| `generer_rapport` | Genere un rapport markdown dans le dossier de logs |

## Ce que l'outil fait

1. **Execute** - La commande et capture stdout/stderr dans des fichiers de log
2. **Verifie** - Le code de sortie par rapport a l'attendu
3. **Detecte** - Un stdout vide (erreur silencieuse potentielle)
4. **Detecte** - Les erreurs dans stderr et les mots-cles d'erreur dans stdout
5. **Journalise** - Tout le deroulement dans `/tmp/test-logs/`
6. **Rapporte** - Retourne 0 (succes) ou 1 (echec) et genere le rapport

## Mots-cles d'erreur detectes

```
error, erreur, failed, echec, exception, fatal
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Test d'un outil** | Toujours - un echec silencieux est pire qu'un echec visible |
| **Tests automatises** | Obligatoire - les erreurs silencieuses faussent les resultats |
| **Validation avant integration** | Recommande - garantir qu'aucune erreur ne passe inapercue |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `tester-protection-boucles-infinies` | Detecte les boucles infinies (en plus des erreurs) |
| `tester-protection-blocage` | Detecte les tests qui bloquent sans erreur visible |
| `template-test` | Template qui charge les 3 protections par defaut |
