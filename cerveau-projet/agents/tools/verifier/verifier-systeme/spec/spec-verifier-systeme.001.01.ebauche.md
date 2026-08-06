# Specification -- Outil verifier-systeme

**Version** : 0.1.0
**Statut** : Ebauche
**Date creation** : 2026-08-05
**Agent** : Vulcain

---

## Objectif

Specifier l'outil `verifier-systeme` qui verifie le systeme de l'utilisateur.

---

## Besoins fonctionnels

### Entrees

| Entree | Type | Description |
|---|---|---|
| `format` | string | Format de sortie (table, json, resume) |
| `detail` | string | Niveau de detail (standard, complet) |

### Sorties

| Sortie | Type | Description |
|---|---|---|
| `systeme` | objet | Informations sur le systeme d'exploitation |
| `shells` | liste | Shells disponibles |
| `langages` | liste | Langages de programmation installes |
| `outils` | liste | Outils disponibles |

---

## Besoins techniques

### Detection du systeme

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

### Verification des shells

```bash
# Bash
which bash
bash --version

# PowerShell
where powershell
powershell --version
```

### Verification des langages

```bash
# Python
python --version
python3 --version

# Node.js
node --version
npm --version
```

### Verification des outils

```bash
# Git
git --version

# npm
npm --version
```

---

## Specification des tests

### Test 1 : Detection du systeme

**Entree** : Aucune
**Resultat attendu** : Objet avec os, version, arch

### Test 2 : Verification des shells

**Entree** : Systeme avec Bash installe
**Resultat attendu** : Liste contenant Bash

### Test 3 : Format de sortie

**Entree** : `format="json"`
**Resultat attendu** : JSON valide

---

## Architecture

```
verifier-systeme/
|-- verifier-systeme.md      # Documentation
|-- verifier-systeme.sh      # Script Bash
|-- verifier-systeme.py      # Script Python
|-- test-verifier-systeme.sh # Tests
`-- spec/
    `-- spec-verifier-systeme.md  # Cette specification
```

---

## Contraintes

- Doit fonctionner sur Windows, Linux, Mac
- Ne doit pas necessiter d'installation supplementaire
- Doit etre rapide (< 5 secondes)
- Doit gerer les erreurs gracieusement

---

## Criteres de succes

| Critere | Mesure |
|---|---|
| **Portabilite** | Fonctionne sur 3 systemes |
| **Performance** | < 5 secondes |
| **Fiabilite** | 100% des cas testes |
| **Documentation** | Complete et claire |

---

