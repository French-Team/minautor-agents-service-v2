# Protocole — Choix des Technologies

**Version** : 0.1.0
**Statut** : Ébauche
**Date création** : 2026-08-05
**Propriétaire** : Vulcain (agent)

---

## Objectif

Définir comment choisir les technologies pour créer des outils réels en fonction du système de l'utilisateur.

**Pourquoi ce protocole ?**
- Les utilisateurs ont des systèmes différents
- Un outil qui ne marche que sur un système est inutile
- La portabilité = plus d'utilisateurs
- Le choix technologique doit être documenté

---

## Le processus de choix

```
SYSTÈME UTILISATEUR -> ANALYSE -> TECHNOLOGIE -> DÉVELOPPEMENT -> TEST
        1                2          3            4           5
```

| Étape | Action | Responsable |
|---|---|---|
| 1 | Vérifier le système utilisateur | Vulcain |
| 2 | Analyser les besoins techniques | Vulcain |
| 3 | Choisir la technologie | Vulcain + Protocole |
| 4 | Développer l'outil | Vulcain |
| 5 | Tester l'outil | Vulcain |

---

## Étape 1 : Vérification du système

### Informations à collecter

| Information | Priorité | Comment la collecter |
|---|---|---|
| **Système d'exploitation** | Haute | `uname -a` ou `ver` |
| **Shell disponible** | Haute | `echo $SHELL` ou `where bash` |
| **Langages installés** | Moyenne | `python --version`, `node --version` |
| **Outils disponibles** | Moyenne | `which`, `where`, `get-command` |

### Commandes de vérification

**Windows** :
```powershell
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
where bash
where python
where node
```

**Linux** :
```bash
uname -a
which bash
which python3
which node
```

**Mac** :
```bash
sw_vers
which bash
which python3
which node
```

---

## Étape 2 : Analyse des besoins

### Questions à se poser

| Question | Impact |
|---|---|
| **L'outil doit-il être rapide ?** | Oui -> Bash/Python natif |
| **L'outil doit-il être portable ?** | Oui -> Python ou Node.js |
| **L'outil doit-il être simple ?** | Oui -> Bash |
| **L'outil doit-il être puissant ?** | Oui -> Python |

### Critères de choix

| Critère | Pondération | Description |
|---|---|---|
| **Disponibilité** | 40% | Est-ce que la technologie est installée ? |
| **Performance** | 30% | Est-ce que c'est assez rapide ? |
| **Facilité** | 20% | Est-ce que c'est facile à développer ? |
| **Portabilité** | 10% | Est-ce que ça marche partout ? |

---

## Étape 3 : Choix technologique

### Matrice de décision

| Besoin | Recommandation |
|---|---|
| **Script simple** | **Bash** |
| **Script complexe** | **Python** |
| **Interface web** | **Node.js** |
| **Manipulation de fichiers** | **Bash** |
| **Analyse de données** | **Python** |
| **API REST** | **Node.js** |

### Technologies recommandées

**Pour les outils simples** : Bash (universel, rapide, simple)
**Pour les outils complexes** : Python ou Node.js (puissant, portable)

---

## Étape 4 : Développement

### Structure d'un outil

```
outils/[nom-outil]/
|-- [nom-outil].sh          # Script Bash
|-- [nom-outil].py          # Script Python
|-- [nom-outil].js          # Script Node.js
|-- README.md               # Documentation
|-- test-[nom-outil].sh     # Tests
``-- spec/
    ``-- spec-[nom-outil].md # Spécification
```

### Conventions de nommage

| Élément | Convention |
|---|---|
| **Nom de l'outil** | `kebab-case` (ex: `lister-agents`) |
| **Extension** | `.sh`, `.py`, `.js` |
| **Tests** | `test-[nom-outil].[ext]` |

---

## Étape 5 : Tests

### Types de tests

| Type | Description | Priorité |
|---|---|---|
| **Test fonctionnel** | Vérifie que l'outil fonctionne | Haute |
| **Test de portabilité** | Vérifie que ça marche sur plusieurs systèmes | Haute |
| **Test de performance** | Vérifie que c'est assez rapide | Moyenne |
| **Test de robustesse** | Vérifie les cas limites | Moyenne |

### Processus de test

```bash
# 1. Test fonctionnel
./outils/[nom-outil]/[nom-outil].sh

# 2. Test de portabilité
# (Tester sur Windows, Linux, Mac)

# 3. Test de performance
time ./outils/[nom-outil]/[nom-outil].sh

# 4. Test de robustesse
# (Tester avec des entrées invalides)
```

---

## Notes importantes

- **Toujours vérifier le système** avant de choisir une technologie
- **Privilégier la portabilité** quand c'est possible
- **Tester sur plusieurs systèmes** avant de valider
- **Documenter les choix** pour la maintenance

---

> **Ce protocole est IMMUABLE.**
