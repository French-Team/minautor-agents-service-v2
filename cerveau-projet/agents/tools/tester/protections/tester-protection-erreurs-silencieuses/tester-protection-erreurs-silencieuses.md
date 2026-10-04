---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# tester-protection-erreurs-silencieuses

**Version :** 0.2.0-py
**Statut :** prepare
**Categorie :** Tests (Protections)
**Chemin :** `agents/tools/tester/protections/tester-protection-erreurs-silencieuses/`

## Description

Protection qui encadre l'execution des tests pour detecter les erreurs silencieuses : code de sortie inattendu, stdout vide, erreurs dans stderr, mots-cles d'erreur dans la sortie. Chaque test est journalise dans `/tmp/test-logs/` et un rapport peut etre genere automatiquement.

## Utilisation

```bash
# Executer un test securise (en ligne de commande)
python3 tester-protection-erreurs-silencieuses.py "./mon-outil.sh --test" "Mon test" 0
```

```bash
# Depuis un test qui source la protection (version .sh)
source tester-protection-erreurs-silencieuses.sh
executer_test_securise "./mon-outil.sh --test" "Mon test" 0
```

## Configuration

| Variable | Description | Defaut |
|---|---|---|
| `LOG_DIR` | Dossier des logs | /tmp/test-logs |
| `MOTS_CLES_ERREUR` | Mots-cles recherches dans la sortie | error, erreur, failed, echec, exception, fatal |

## Fonctions

| Fonction | Role |
|---|---|
| `executer_test_securise` | Execute un test avec verification des erreurs silencieuses |
| `tuer_arbre` | Tue le processus et tout son arbre (cross-platform) |

## Ce que l'outil fait

1. **Execute** - La commande via Popen et capture stdout/stderr
2. **Verifie** - Le code de sortie par rapport a l'attendu
3. **Detecte** - Un stdout vide (erreur silencieuse potentielle)
4. **Detecte** - Les erreurs dans stderr et les mots-cles d'erreur dans stdout
5. **Journalise** - Tout le deroulement dans `/tmp/test-logs/`
6. **Rapporte** - Retourne 0 (succes) ou 1 (echec)

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

---

## Versionning

| Version | Date | Changement |
|---|---|---|
| 0.1.0 | - | Version initiale (bash) |
| 0.2.0-py | 2026-08-07 | Portage Python : Popen + kill d'arbre cross-platform (Windows inclus) |
