# Outil — Lister les Statuts des Fichiers

**Catégorie** : Explorer
**Version** : 0.1.0
**Statut** : stable
**Date création** : 2026-08-05
**Propriétaire** : Vulcain (outil partagé)

---

## Objectif

Lister les fichiers markdown par statut (ebauche, préparé, dev, test, valide).

**Pourquoi cet outil ?**
- Permet de voir l'état d'avancement de tous les fichiers
- Aide à identifier les fichiers en attente de validation
- Utile pour le suivi du workflow RVAV

---

## Utilisation

```bash
./lister-statuts.sh [CHEMIN] [OPTIONS]
```

### Options

| Option | Description |
|---|---|
| `--statut <statut>` | Filtrer par statut (ebauche, préparé, dev, test, valide) |
| `--verbose` | Afficher les détails |
| `--aide` | Afficher l'aide |

### Exemples

```bash
# Lister tous les fichiers avec statut
./lister-statuts.sh

# Lister les fichiers en ebauche
./lister-statuts.sh --statut ebauche

# Lister dans un dossier spécifique
./lister-statuts.sh cerveau-projet/agents

# Lister les ebauche dans cerveau-projet
./lister-statuts.sh --statut ebauche cerveau-projet/
```

---

## Résultat

### Exemple de sortie (sans filtre)

```
cerveau-projet/pense-betes/regles-immuables/general/protocole-auto-correction/protocole-auto-correction.001.01.ebauche.md | ebauche
cerveau-projet/pense-betes/regles-immuables/general/protocole-activation/protocole-activation.001.02.preparé.md | préparé
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
Résumé:
  Total fichiers avec statut: 15
  ebauche: 8
  préparé: 3
  dev: 2
  test: 1
  valide: 1
```

---

## Qui devrait utiliser cet outil ?

| Agent | Quand l'utiliser |
|---|---|
| **Buffy** | Quand elle crée un nouveau fichier (vérifier s'il existe déjà en ebauche) |
| **Janus** | Pour le contrôle des statuts — voir les fichiers en attente de validation |
| **Cerberus** | Pour comprendre l'état du projet quand un utilisateur pose une question |
| **Tout agent** | Avant de commencer une mission — voir l'état des fichiers concernés |

---

## Cas d'utilisation

### 1. Avant de créer un nouveau fichier

```bash
# Vérifier si un fichier avec ce thème existe déjà en ebauche
./lister-statuts.sh --statut ebauche cerveau-projet/ | grep "protocole-nom"
```

### 2. Pour le contrôle des statuts (Janus)

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

1. **[Rechercher]** — Utiliser `lister-statuts` pour voir l'état des fichiers
2. **[Vérifier]** — Utiliser `valider-nommage` pour vérifier la conformité
3. **[Analyser]** — Lire le contenu des fichiers identifiés
4. **[Valider]** — Décider du passage de statut
5. **[Purifier]** — Utiliser `purifier-fichier` ou `condenseur`

---

## Dépendances

- `bash` — pour exécuter les commandes
- `find` — pour chercher les fichiers
- `grep` — pour extraire les statuts

---

## Notes

- Cet outil ne modifie pas les fichiers, il les analyse uniquement
- Les statuts valides sont : ebauche, préparé, dev, test, valide
- Le format de nommage doit respecter `convention-renommage.md`
- Utiliser `valider-nommage` pour vérifier la conformité des noms

---

## Liens

- **Convention** : `convention-renommage.md` — format de nommage des fichiers
- **Workflow** : `rvav-workflow.md` — processus de validation
- **Outil similaire** : `valider-nommage` — vérifie la conformité du nommage
