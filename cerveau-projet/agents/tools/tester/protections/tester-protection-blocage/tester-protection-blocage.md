# tester-protection-blocage

**Version :** 0.2.0-py
**Statut :** prepare
**Categorie :** Tests (Protections)
**Chemin :** `agents/tools/tester/protections/tester-protection-blocage/`

## Description

Protection qui encadre l'execution des tests pour detecter et stopper les tests qui bloquent : processus qui ne tourne plus (CPU quasi nul), absence de sortie pendant plusieurs intervalles, sortie anormalement longue. Elle complete la protection contre les boucles infinies en detectant les blocages silencieux.

## Utilisation

```bash
# Executer une commande avec protection contre le blocage (en ligne de commande)
python3 tester-protection-blocage.py "./mon-outil.sh --test" "Mon test" 60
```

```bash
# Depuis un test qui source la protection (version .sh)
source tester-protection-blocage.sh
executer_sans_blocage "./mon-outil.sh --test" "Mon test" 60
```

## Configuration

| Variable | Description | Defaut |
|---|---|---|
| `TIMEOUT_DEFAUT` | Delai maximum en secondes (parametre 3) | 60 |

## Fonctions

| Fonction | Role |
|---|---|
| `executer_sans_blocage` | Execute une commande avec surveillance du blocage |
| `tuer_arbre` | Tue le processus et tout son arbre (cross-platform) |

## Ce que l'outil fait

1. **Lance** - La commande via Popen dans une nouvelle session
2. **Surveille** - Le temps d'execution jusqu'au timeout
3. **Detecte** - Un test qui depasse le delai est considere bloque
4. **Intervient** - Tue l'arbre de processus complet (pas seulement le processus direct)
5. **Rapporte** - Affiche la sortie partielle et retourne le code d'echec

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

---

## Versionning

| Version | Date | Changement |
|---|---|---|
| 0.1.0 | - | Version initiale (bash) |
| 0.2.0-py | 2026-08-07 | Portage Python : Popen + kill d'arbre cross-platform (Windows inclus) |
