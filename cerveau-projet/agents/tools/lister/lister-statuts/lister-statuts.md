# lister-statuts

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** lister
**Chemin :** `agents/tools/lister/lister-statuts/`
**Proprietaire :** Janus (outil partage)

---

## Objectif

Lister les fichiers markdown par statut (ebauche, prepare, dev, test, valide).

**Pourquoi cet outil ?**
- Permet de voir l'etat d'avancement de tous les fichiers
- Aide a identifier les fichiers en attente de validation
- Utile pour le suivi du workflow RVAV

---

## Utilisation

```bash
./lister-statuts.sh [CHEMIN] [OPTIONS]
```

### Version Python (recommandee)

```bash
python3 lister-statuts.py [CHEMIN] [OPTIONS]
```

### Options

| Option | Description |
|---|---|
| `--statut <statut>` | Filtrer par statut (ebauche, prepare, dev, test, valide) |
| `--verbose` | Afficher les details |
| `--aide` | Afficher l'aide |

### Exemples

```bash
# Lister tous les fichiers avec statut
./lister-statuts.sh

# Lister les fichiers en ebauche
./lister-statuts.sh --statut ebauche

# Lister dans un dossier specifique
./lister-statuts.sh cerveau-projet/agents

# Lister les ebauche dans cerveau-projet
./lister-statuts.sh --statut ebauche cerveau-projet/
```

---

## Resultat

### Exemple de sortie (sans filtre)

```
cerveau-projet/pense-betes/regles-immuables/general/protocole-auto-correction/protocole-auto-correction.001.01.ebauche.md | ebauche
cerveau-projet/pense-betes/regles-immuables/general/protocole-activation/protocole-activation.001.02.prepare.md | prepare
cerveau-projet/pense-betes/regles-immuables/general/protocole-versionning-outils/protocole-versionning-outils.001.01.ebauche.md | ebauche
```

### Exemple de sortie (avec filtre ebauche)

```
cerveau-projet/pense-betes/regles-immuables/general/protocole-auto-correction/protocole-auto-correction.001.01.ebauche.md | ebauche
cerveau-projet/pense-betes/regles-immuables/general/protocole-versionning-outils/protocole-versionning-outils.001.01.ebauche.md | ebauche
```

### Sortie verbose

```
Recherche dans: cerveau-projet
Filtrage par statut: ebauche
---
cerveau-projet/pense-betes/regles-immuables/general/protocole-auto-correction/protocole-auto-correction.001.01.ebauche.md | ebauche
cerveau-projet/pense-betes/regles-immuables/general/protocole-versionning-outils/protocole-versionning-outils.001.01.ebauche.md | ebauche
---
Resume:
  Total fichiers avec statut: 15
  ebauche: 8
  prepare: 3
  dev: 2
  test: 1
  valide: 1
```

---

## Qui devrait utiliser cet outil ?

| Agent | Quand l'utiliser |
|---|---|
| **Buffy** | Quand elle cree un nouveau fichier (verifier s'il existe deja en ebauche) |
| **Janus** | Pour le controle des statuts -- voir les fichiers en attente de validation |
| **Cerberus** | Pour comprendre l'etat du projet quand un utilisateur pose une question |
| **Tout agent** | Avant de commencer une mission -- voir l'etat des fichiers concernes |

---

## Cas d'utilisation

### 1. Avant de creer un nouveau fichier

```bash
# Verifier si un fichier avec ce theme existe deja en ebauche
./lister-statuts.sh --statut ebauche cerveau-projet/ | grep "protocole-nom"
```

### 2. Pour le controle des statuts (Janus)

```bash
# Voir tous les fichiers en ebauche qui attendent une validation
./lister-statuts.sh --statut ebauche cerveau-projet/

# Voir les fichiers en test qui attendent une validation
./lister-statuts.sh --statut test cerveau-projet/
```

### 3. Pour le suivi du projet (Cerberus)

```bash
# Vue d'ensemble de l'avancement
./lister-statuts.sh --verbose cerveau-projet/
```

---

## Relation avec le workflow RVAV

L'outil `lister-statuts` est essentiel pour le workflow RVAV :

1. **[Rechercher]** -- Utiliser `lister-statuts` pour voir l'etat des fichiers
2. **[Verifier]** -- Utiliser `valider-nommage` pour verifier la conformite
3. **[Analyser]** -- Lire le contenu des fichiers identifies
4. **[Valider]** -- Decider du passage de statut
5. **[Purifier]** -- Utiliser `nettoyer-fichier` ou `condenser-fichier`

---

## Dependances

- `bash` -- pour executer les commandes
- `find` -- pour chercher les fichiers
- `grep` -- pour extraire les statuts

---

## Notes

- Cet outil ne modifie pas les fichiers, il les analyse uniquement
- Les statuts valides sont : ebauche, prepare, dev, test, valide
- Le format de nommage doit respecter `convention-renommage.md`
- Utiliser `valider-nommage` pour verifier la conformite des noms

---

## Liens

- **Convention** : `convention-renommage.md` -- format de nommage des fichiers
- **Workflow** : `rvav-workflow.md` -- processus de validation
- **Outil similaire** : `valider-nommage` -- verifie la conformite du nommage

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-05 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter, VERSION 0.2.0, statut prepare |
| 0.2.0-py | 2026-08-07 | Version Python creee (lister-statuts.py), basee sur outil-template.py |
