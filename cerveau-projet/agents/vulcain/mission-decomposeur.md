# Mission -- Outil de Decomposition Markdown

**Agent** : Vulcain
**Date** : 2026-08-05
**Statut** : En cours

---

## Objectif

Creer un outil qui decompose les fichiers markdown pour permettre aux agents de voir uniquement ce dont ils ont besoin.

---

## Probleme a resoudre

Les fichiers markdown du cerveau-projet sont grands (200-400 lignes). Les agents doivent :
- Lire uniquement les sections pertinentes
- Filtrer le contenu selon leurs besoins
- Comprendre rapidement la structure

---

## Fonctionnalites requises

### 1. Lister les sections

```bash
decomposeur.sh --lister [fichier]
```

**Resultat** :
```
1. ## Principe Fondamental (ligne 4)
2. ## Structure (ligne 18)
3. ## Regles (ligne 56)
   3.1. ### Regle 1 (ligne 58)
   3.2. ### Regle 2 (ligne 71)
4. ## Processus (ligne 154)
```

### 2. Extraire une section

```bash
decomposeur.sh --extraire [fichier] [section]
```

**Exemples** :
```bash
# Extraire la section "Regles"
decomposeur.sh --extraire protocole-outils.md "Regles"

# Extraire la sous-section "Regle 1"
decomposeur.sh --extraire protocole-outils.md "Regle 1"

# Extraire les lignes 56-100
decomposeur.sh --extraire protocole-outils.md 56-100
```

### 3. Filtrer par type de contenu

```bash
decomposeur.sh --filtrer [fichier] [type]
```

**Types disponibles** :
- `titres` -- uniquement les titres (##, ###)
- `regles` -- uniquement les lignes contenant "REGLE", "JAMAIS", "TOUJOURS"
- `tableaux` -- uniquement les tableaux
- `code` -- uniquement les blocs de code
- `liens` -- uniquement les liens

### 4. Afficher le resume

```bash
decomposeur.sh --resume [fichier]
```

**Resultat** :
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

**Resultat** :
```
Lignes : 110
Mots : 450
Caracteres : 2500
Sections : 8
```

---

## Specifications techniques

### Structure de sortie

```bash
# Sortie par defaut : liste des sections
decomposeur.sh [fichier]

# Sortie JSON (pour les agents)
decomposeur.sh --json [fichier]

# Sortie Markdown (pour la documentation)
decomposeur.sh --markdown [fichier]
```

### Options

| Option | Description | Defaut |
|---|---|---|
| `--lister` | Lister les sections | Non |
| `--extraire [section]` | Extraire une section | Non |
| `--filtrer [type]` | Filtrer par type | Non |
| `--resume` | Afficher le resume | Non |
| `--compter` | Compter le contenu | Non |
| `--json` | Sortie JSON | Non |
| `--markdown` | Sortie Markdown | Non |
| `--verbose` | Details supplementaires | Non |

---

## Extensibilite

L'outil doit etre prepare pour de futurs ajouts :

### Types de contenu a ajouter

- `definitions` -- lignes avec "est", "signifie", "definit"
- `exemples` -- blocs de code avec "Exemple"
- `erreurs` -- lignes avec "ERREUR", "ATTENTION"
- `validations` -- lignes avec "Verifier", "Tester"

### Actions a ajouter

- `--comparer [fichier1] [fichier2]` -- comparer deux fichiers
- `--detecter-doublons [fichier]` -- trouver les sections similaires
- `--suggerer-condenser [fichier]` -- proposer des reductions

---

## Criteres de validation

- [ ] L'outil fonctionne sur tous les fichiers .md du cerveau
- [ ] La sortie est claire et formatee
- [ ] L'outil est rapide (< 1 seconde)
- [ ] L'outil est documente
- [ ] L'outil est teste
- [ ] L'outil est extensible

---

## Livrables

1. `decomposer-fichier.sh` -- dans `agents/tools/decomposer/decomposer-fichier/`
2. `decomposer-fichier.md` -- documentation
3. `spec-decomposer-fichier.md` -- specifications
4. Tests avec les fichiers du cerveau

---

## Exemple d'utilisation

### Agent Buffy veut voir les regles d'un protocole

```bash
# 1. Lister les sections
decomposeur.sh --lister protocole-outils.md

# 2. Extraire la section "Regles"
decomposeur.sh --extraire protocole-outils.md "Regles"

# 3. Filtrer uniquement les regles
decomposeur.sh --filtrer protocole-outils.md "regles"
```

### Agent Vulcain veut analyser un fichier

```bash
# 1. Voir le resume
decomposeur.sh --resume protocole-outils.md

# 2. Compter le contenu
decomposeur.sh --compter protocole-outils.md

# 3. Lister les sections
decomposeur.sh --lister protocole-outils.md
```
