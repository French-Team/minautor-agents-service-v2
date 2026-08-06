# Mission — Outil de Décomposition Markdown

**Agent** : Vulcain
**Date** : 2026-08-05
**Statut** : En cours

---

## Objectif

Créer un outil qui décompose les fichiers markdown pour permettre aux agents de voir uniquement ce dont ils ont besoin.

---

## Problème à résoudre

Les fichiers markdown du cerveau-projet sont grands (200-400 lignes). Les agents doivent :
- Lire uniquement les sections pertinentes
- Filtrer le contenu selon leurs besoins
- Comprendre rapidement la structure

---

## Fonctionnalités requises

### 1. Lister les sections

```bash
decomposeur.sh --lister [fichier]
```

**Résultat** :
```
1. ## Principe Fondamental (ligne 4)
2. ## Structure (ligne 18)
3. ## Règles (ligne 56)
   3.1. ### Règle 1 (ligne 58)
   3.2. ### Règle 2 (ligne 71)
4. ## Processus (ligne 154)
```

### 2. Extraire une section

```bash
decomposeur.sh --extraire [fichier] [section]
```

**Exemples** :
```bash
# Extraire la section "Règles"
decomposeur.sh --extraire protocole-outils.md "Règles"

# Extraire la sous-section "Règle 1"
decomposeur.sh --extraire protocole-outils.md "Règle 1"

# Extraire les lignes 56-100
decomposeur.sh --extraire protocole-outils.md 56-100
```

### 3. Filtrer par type de contenu

```bash
decomposeur.sh --filtrer [fichier] [type]
```

**Types disponibles** :
- `titres` — uniquement les titres (##, ###)
- `regles` — uniquement les lignes contenant "RÈGLE", "JAMAIS", "TOUJOURS"
- `tableaux` — uniquement les tableaux
- `code` — uniquement les blocs de code
- `liens` — uniquement les liens

### 4. Afficher le résumé

```bash
decomposeur.sh --resume [fichier]
```

**Résultat** :
```
Fichier : protocole-outils.md
Lignes : 110
Sections : 8
Sous-sections : 12
Tableaux : 4
Blocs de code : 6
```

### 5. Compter le contenu

```bash
decomposeur.sh --compter [fichier]
```

**Résultat** :
```
Lignes : 110
Mots : 450
Caractères : 2500
Sections : 8
```

---

## Spécifications techniques

### Structure de sortie

```bash
# Sortie par défaut : liste des sections
decomposeur.sh [fichier]

# Sortie JSON (pour les agents)
decomposeur.sh --json [fichier]

# Sortie Markdown (pour la documentation)
decomposeur.sh --markdown [fichier]
```

### Options

| Option | Description | Défaut |
|---|---|---|
| `--lister` | Lister les sections | Non |
| `--extraire [section]` | Extraire une section | Non |
| `--filtrer [type]` | Filtrer par type | Non |
| `--resume` | Afficher le résumé | Non |
| `--compter` | Compter le contenu | Non |
| `--json` | Sortie JSON | Non |
| `--markdown` | Sortie Markdown | Non |
| `--verbose` | Détails supplémentaires | Non |

---

## Extensibilité

L'outil doit être préparé pour de futurs ajouts :

### Types de contenu à ajouter

- `definitions` — lignes avec "est", "signifie", "définit"
- `exemples` — blocs de code avec "Exemple"
- `erreurs` — lignes avec "ERREUR", "ATTENTION"
- `validations` — lignes avec "Vérifier", "Tester"

### Actions à ajouter

- `--comparer [fichier1] [fichier2]` — comparer deux fichiers
- `--detecter-doublons [fichier]` — trouver les sections similaires
- `--suggerer-condenser [fichier]` — proposer des réductions

---

## Critères de validation

- [ ] L'outil fonctionne sur tous les fichiers .md du cerveau
- [ ] La sortie est claire et formatée
- [ ] L'outil est rapide (< 1 seconde)
- [ ] L'outil est documenté
- [ ] L'outil est testé
- [ ] L'outil est extensible

---

## Livrables

1. `decomposeur.sh` — dans `agents/tools/analyser/decomposeur/`
2. `decomposeur.md` — documentation
3. `spec-decomposeur.md` — spécifications
4. Tests avec les fichiers du cerveau

---

## Exemple d'utilisation

### Agent Buffy veut voir les règles d'un protocole

```bash
# 1. Lister les sections
decomposeur.sh --lister protocole-outils.md

# 2. Extraire la section "Règles"
decomposeur.sh --extraire protocole-outils.md "Règles"

# 3. Filtrer uniquement les règles
decomposeur.sh --filtrer protocole-outils.md "regles"
```

### Agent Vulcain veut analyser un fichier

```bash
# 1. Voir le résumé
decomposeur.sh --resume protocole-outils.md

# 2. Compter le contenu
decomposeur.sh --compter protocole-outils.md

# 3. Lister les sections
decomposeur.sh --lister protocole-outils.md
```
