# Protocole -- Choix des Technologies

**Version** : 0.1.0
**Statut** : Ebauche
**Date creation** : 2026-08-05
**Proprietaire** : Vulcain (agent)

---

## Objectif

Definir comment choisir les technologies pour creer des outils reels en fonction du systeme de l'utilisateur.

**Pourquoi ce protocole ?**
- Les utilisateurs ont des systemes differents
- Un outil qui ne marche que sur un systeme est inutile
- La portabilite = plus d'utilisateurs
- Le choix technologique doit etre documente

---

## Le processus de choix

```
SYSTEME UTILISATEUR -> ANALYSE -> TECHNOLOGIE -> DEVELOPPEMENT -> TEST
        1                2          3            4           5
```

| Etape | Action | Responsable |
|---|---|---|
| 1 | Verifier le systeme utilisateur | Vulcain |
| 2 | Analyser les besoins techniques | Vulcain |
| 3 | Choisir la technologie | Vulcain + Protocole |
| 4 | Developper l'outil | Vulcain |
| 5 | Tester l'outil | Vulcain |

---

## Etape 1 : Verification du systeme

### Informations a collecter

| Information | Priorite | Comment la collecter |
|---|---|---|
| **Systeme d'exploitation** | Haute | `uname -a` ou `ver` |
| **Shell disponible** | Haute | `echo $SHELL` ou `where bash` |
| **Langages installes** | Moyenne | `python --version`, `node --version` |
| **Outils disponibles** | Moyenne | `which`, `where`, `get-command` |

### Commandes de verification

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

## Etape 2 : Analyse des besoins

### Questions a se poser

| Question | Impact |
|---|---|
| **L'outil doit-il etre rapide ?** | Oui -> Bash/Python natif |
| **L'outil doit-il etre portable ?** | Oui -> Python ou Node.js |
| **L'outil doit-il etre simple ?** | Oui -> Bash |
| **L'outil doit-il etre puissant ?** | Oui -> Python |

### Criteres de choix

| Critere | Ponderation | Description |
|---|---|---|
| **Disponibilite** | 40% | Est-ce que la technologie est installee ? |
| **Performance** | 30% | Est-ce que c'est assez rapide ? |
| **Facilite** | 20% | Est-ce que c'est facile a developper ? |
| **Portabilite** | 10% | Est-ce que ca marche partout ? |

---

## Etape 3 : Choix technologique

### Matrice de decision

| Besoin | Recommandation |
|---|---|
| **Script simple** | **Bash** |
| **Script complexe** | **Python** |
| **Interface web** | **Node.js** |
| **Manipulation de fichiers** | **Bash** |
| **Analyse de donnees** | **Python** |
| **API REST** | **Node.js** |

### Technologies recommandees

**Pour les outils simples** : Bash (universel, rapide, simple)
**Pour les outils complexes** : Python ou Node.js (puissant, portable)

---

## Etape 4 : Developpement

### Structure d'un outil

```
agents/tools/[categorie]/[nom-outil]/
|-- [nom-outil].sh          # Script d'implementation (technologie choisie : bash, python ou node)
|-- [nom-outil].md          # Documentation
|-- test-[nom-outil].md     # Tests (optionnel)
``-- spec/                   # Specification (optionnel)
    ``-- spec-[nom-outil].md
```

> La structure de depart est fournie par le **outil-template** (`agents/tools/outil-template.md` + `.sh`).

### Conventions de nommage

| Element | Convention |
|---|---|
| **Nom de l'outil** | `kebab-case` (ex: `lister-agents`) |
| **Extension** | `.sh` (bash), `.py` (python), `.js` (node) -- une seule par outil |
| **Tests** | `test-[nom-outil].[ext]` |

---

## Etape 5 : Tests

### Types de tests

| Type | Description | Priorite |
|---|---|---|
| **Test fonctionnel** | Verifie que l'outil fonctionne | Haute |
| **Test de portabilite** | Verifie que ca marche sur plusieurs systemes | Haute |
| **Test de performance** | Verifie que c'est assez rapide | Moyenne |
| **Test de robustesse** | Verifie les cas limites | Moyenne |

### Processus de test

```bash
# 1. Test fonctionnel
./outils/[nom-outil]/[nom-outil].sh

# 2. Test de portabilite
# (Tester sur Windows, Linux, Mac)

# 3. Test de performance
time ./outils/[nom-outil]/[nom-outil].sh

# 4. Test de robustesse
# (Tester avec des entrees invalides)
```

---

## Notes importantes

- **Toujours verifier le systeme** avant de choisir une technologie
- **Privilegier la portabilite** quand c'est possible
- **Tester sur plusieurs systemes** avant de valider
- **Documenter les choix** pour la maintenance

---

> **Ce protocole est IMMUABLE.**
