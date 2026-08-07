# tester-protection-boucles-infinies

**Version :** 0.2.0-py
**Statut :** prepare
**Categorie :** Tests (Protections)
**Chemin :** `agents/tools/tester/protections/tester-protection-boucles-infinies/`

## Description

Protection qui encadre l'execution des tests pour detecter et stopper les boucles infinies. Si un test depasse le delai maximum configure, la protection tue le processus, affiche la sortie partielle et retourne le code 124 (timeout) au lieu de laisser le test tourner indefiniment.

## Utilisation

```bash
# Lancer une commande avec protection contre les boucles infinies (en ligne de commande)
python3 tester-protection-boucles-infinies.py "./mon-outil.sh --test" "Mon test" 30
```

```bash
# Depuis un test qui source la protection (version .sh)
source tester-protection-boucles-infinies.sh
lancer_avec_protection "./mon-outil.sh --test" "Mon test" 30
```

## Configuration

| Variable | Description | Defaut |
|---|---|---|
| `TIMEOUT_DEFAUT` | Delai maximum en secondes (parametre 3) | 30 |

## Fonctions

| Fonction | Role |
|---|---|
| `lancer_avec_protection` | Lance une commande avec timeout et surveillance |
| `tuer_arbre` | Tue le processus et tout son arbre (cross-platform) |

## Ce que l'outil fait

1. **Lance** - La commande via Popen dans une nouvelle session
2. **Surveille** - Le temps d'execution jusqu'au timeout
3. **Detecte** - Si le delai est depasse, le test est en boucle infinie
4. **Intervient** - Tue l'arbre de processus complet (pas seulement le processus direct)
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

---

## Versionning

| Version | Date | Changement |
|---|---|---|
| 0.1.0 | - | Version initiale (bash) |
| 0.2.0-py | 2026-08-07 | Portage Python : Popen + kill d'arbre cross-platform (Windows inclus) |
