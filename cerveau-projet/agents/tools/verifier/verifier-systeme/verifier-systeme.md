---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# verifier-systeme

**Categorie** : Verifier
**Version** : 0.2.1-py
**Statut** : prepare
**Date creation** : 2026-08-05
**Proprietaire** : outil partage

---

## Objectif

Verifier le systeme de l'utilisateur pour collecter ce qui est deja installe.

**Pourquoi cet outil ?**
- Avant de creer un outil, il faut savoir ce qui est disponible
- Chaque utilisateur a un systeme different
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
| `--detail DETAIL` | Niveau de detail: standard, complet |
| `--enregistrer` | Ecrire le profil systeme dans le classeur-variables (variable `profil-systeme`) |
| `--version` | Afficher la version |

---

## Resultat

### Format table (defaut)

```markdown
| Categorie | Element | Disponible | Version | Chemin |
|---|---|---|---|---|
| Systeme | OS | Windows 11 | 10.0.22621 | - |
| Shell | Bash | Oui | 5.2.15 | /usr/bin/bash |
| Langage | Python | Oui | 3.11.0 | /c/Users/.../python.exe |
| Langage | Node.js | Oui | 18.0.0 | /c/Program Files/nodejs/node.exe |
| Outil | Git | Oui | 2.40.0 | /c/Program Files/Git/bin/git.exe |
```

### Format resume

```markdown
**Systeme** : Windows 11 (x64)
**Shells** : Bash, PowerShell
**Langages** : Python 3.11.0, Node.js 18.0.0
**Outils** : Git 2.40.0, npm 9.6.0
```

---

## Commandes utilisees

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

## Comment ca fonctionne

1. Detecter le systeme d'exploitation
2. Executer les commandes de verification
3. Parser les resultats
4. Formater selon le parametre `format`
5. Retourner le resultat
6. Avec `--enregistrer` : ecrire / mettre a jour la variable `profil-systeme`
   dans `classeur-variables/stockage/variables-actuelles.md` + entree dans
   `classeur-variables/historique/historique-modifications.md`

---

## Dependances

- `bash` ou `powershell` -- pour executer les commandes
- `systeminfo` ou `uname` -- pour les informations systeme

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-05 | Creation initiale |
| 0.1.1-beta | 2026-08-05 | Ajout du script executable |
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels (table, resume, json), doublons du resume corriges (Python/Node.js sans redondance), promotion prepare |
| 0.2.0-py | 2026-08-07 | Portage Python : analyse du systeme (3 formats) |
| 0.2.1-py | 2026-08-07 | Option `--enregistrer` (sh + py) : ecrit le profil systeme dans le classeur-variables |

---

## Notes

- Cet outil est ESSENTIEL pour le choix technologique
- Il doit etre execute AVANT de creer tout outil
- Les resultats sont utilises par le protocole-technologies
- Il est partage entre tous les agents
