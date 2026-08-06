# Spécification — Outil verifier-systeme

**Version** : 0.1.0
**Statut** : Ébauche
**Date création** : 2026-08-05
**Agent** : Vulcain

---

## Objectif

Spécifier l'outil `verifier-systeme` qui vérifie le système de l'utilisateur.

---

## Besoins fonctionnels

### Entrées

| Entrée | Type | Description |
|---|---|---|
| `format` | string | Format de sortie (table, json, resume) |
| `detail` | string | Niveau de détail (standard, complet) |

### Sorties

| Sortie | Type | Description |
|---|---|---|
| `systeme` | objet | Informations sur le système d'exploitation |
| `shells` | liste | Shells disponibles |
| `langages` | liste | Langages de programmation installés |
| `outils` | liste | Outils disponibles |

---

## Besoins techniques

### Détection du système

```python
import platform
import subprocess
import shutil

def detecter_systeme():
    return {
        "os": platform.system(),
        "version": platform.version(),
        "arch": platform.machine()
    }
```

### Vérification des shells

```bash
# Bash
which bash
bash --version

# PowerShell
where powershell
powershell --version
```

### Vérification des langages

```bash
# Python
python --version
python3 --version

# Node.js
node --version
npm --version
```

### Vérification des outils

```bash
# Git
git --version

# npm
npm --version
```

---

## Spécification des tests

### Test 1 : Détection du système

**Entrée** : Aucune
**Résultat attendu** : Objet avec os, version, arch

### Test 2 : Vérification des shells

**Entrée** : Système avec Bash installé
**Résultat attendu** : Liste contenant Bash

### Test 3 : Format de sortie

**Entrée** : `format="json"`
**Résultat attendu** : JSON valide

---

## Architecture

```
verifier-systeme/
├── verifier-systeme.md      # Documentation
├── verifier-systeme.sh      # Script Bash
├── verifier-systeme.py      # Script Python
├── test-verifier-systeme.sh # Tests
└── spec/
    └── spec-verifier-systeme.md  # Cette spécification
```

---

## Contraintes

- Doit fonctionner sur Windows, Linux, Mac
- Ne doit pas nécessiter d'installation supplémentaire
- Doit être rapide (< 5 secondes)
- Doit gérer les erreurs gracieusement

---

## Critères de succès

| Critère | Mesure |
|---|---|
| **Portabilité** | Fonctionne sur 3 systèmes |
| **Performance** | < 5 secondes |
| **Fiabilité** | 100% des cas testés |
| **Documentation** | Complète et claire |

---

