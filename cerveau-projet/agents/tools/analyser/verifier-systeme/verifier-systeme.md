# Outil — Vérifier le Système

**Catégorie** : Analyser
**Version** : 0.1.1-beta
**Statut** : beta
**Date création** : 2026-08-05
**Propriétaire** : Vulcain (outil partagé)

---

## Objectif

Vérifier le système de l'utilisateur pour collecter ce qui est déjà installé.

**Pourquoi cet outil ?**
- Avant de créer un outil, il faut savoir ce qui est disponible
- Chaque utilisateur a un système différent
- Cet outil automatise la collecte d'informations
- Il permet de choisir les bonnes technologies

---

## Utilisation

```bash
./verifier-systeme.sh [OPTIONS]
```

### Options

| Option | Description |
|---|---|
| `--aide, -h` | Afficher l'aide |
| `--format FORMAT` | Format de sortie: table, json, resume |
| `--detail DETAIL` | Niveau de détail: standard, complet |
| `--version` | Afficher la version |

---

## Résultat

### Format table (défaut)

```markdown
| Catégorie | Élément | Disponible | Version | Chemin |
|---|---|---|---|---|
| Système | OS | Windows 11 | 10.0.22621 | - |
| Shell | Bash | Oui | 5.2.15 | /usr/bin/bash |
| Langage | Python | Oui | 3.11.0 | /c/Users/.../python.exe |
| Langage | Node.js | Oui | 18.0.0 | /c/Program Files/nodejs/node.exe |
| Outil | Git | Oui | 2.40.0 | /c/Program Files/Git/bin/git.exe |
```

### Format résumé

```markdown
**Système** : Windows 11 (x64)
**Shells** : Bash, PowerShell
**Langages** : Python 3.11.0, Node.js 18.0.0
**Outils** : Git 2.40.0, npm 9.6.0
```

---

## Commandes utilisées

### Windows

```powershell
# OS
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"

# Shells
where bash
where powershell

# Langages
python --version
node --version

# Outils
git --version
npm --version
```

### Linux/Mac

```bash
# OS
uname -a
lsb_release -a

# Shells
which bash
which zsh

# Langages
python3 --version
node --version

# Outils
git --version
npm --version
```

---

## Comment ça fonctionne

1. Détecter le système d'exploitation
2. Exécuter les commandes de vérification
3. Parser les résultats
4. Formater selon le paramètre `format`
5. Retourner le résultat

---

## Dépendances

- `bash` ou `powershell` — pour exécuter les commandes
- `systeminfo` ou `uname` — pour les informations système

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-05 | Création initiale |
| 0.1.1-beta | 2026-08-05 | Ajout du script exécutable |

---

## Notes

- Cet outil est ESSENTIEL pour le choix technologique
- Il doit être exécuté AVANT de créer tout outil
- Les résultats sont utilisés par le protocole-technologies
- Il est partagé entre tous les agents
