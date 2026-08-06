# Outil — Décomposeur Markdown

**Catégorie** : Analyser
**Version** : 0.1.0-beta
**Statut** : beta
**Date création** : 2026-08-05
**Propriétaire** : Vulcain (outil partagé)

---

## Objectif

Décomposer les fichiers markdown pour permettre aux agents de voir uniquement ce dont ils ont besoin.

---

## Utilisation

```bash
decomposeur.sh <fichier> [options]
```

---

## Actions

| Action | Description | Exemple |
|---|---|---|
| `--lister` | Lister les sections | `decomposeur.sh fichier.md --lister` |
| `--extraire [section]` | Extraire une section | `decomposeur.sh fichier.md --extraire "Règles"` |
| `--filtrer [type]` | Filtrer par type | `decomposeur.sh fichier.md --filtrer regles` |
| `--resume` | Afficher le résumé | `decomposeur.sh fichier.md --resume` |
| `--compter` | Compter le contenu | `decomposeur.sh fichier.md --compter` |

---

## Types de contenu

| Type | Description |
|---|---|
| `titres` | Titres (##, ###) |
| `regles` | Lignes avec RÈGLE, JAMAIS, TOUJOURS |
| `tableaux` | Tableaux Markdown |
| `code` | Blocs de code |
| `liens` | Liens Markdown |

---

## Exemples

### Lister les sections

```bash
$ decomposeur.sh cerveau-projet/pense-betes/regles-immuables/general/protocole-outils/protocole-outils.001.01.ebauche.md --lister

=== Sections de protocole-outils.001.01.ebauche.md ===

4. ## Principe Fondamental
7. ## Pourquoi ?
18. ## Structure
56. ## Règles
   58. ### Règle 1
   71. ### Règle 2
...
```

### Extraire une section

```bash
$ decomposeur.sh cerveau-projet/pense-betes/regles-immuables/general/protocole-outils/protocole-outils.001.01.ebauche.md --extraire "Règles"

=== Section: Règles ===

## Règles

### Règle 1 — Chaque outil est documenté
...
```

### Filtrer par type

```bash
$ decomposeur.sh cerveau-projet/pense-betes/regles-immuables/general/protocole-outils/protocole-outils.001.01.ebauche.md --filtrer regles

4: > **Ne jamais utiliser une commande sans la transformer en outil réutilisable.**
58: ### Règle 1 — Chaque outil est documenté
71: ### Règle 2 — Chaque outil est testé
...
```

### Résumé

```bash
$ decomposeur.sh cerveau-projet/pense-betes/regles-immuables/general/protocole-outils/protocole-outils.001.01.ebauche.md --resume

=== Résumé de protocole-outils.001.01.ebauche.md ===

Lignes       : 110
Sections     : 8
Sous-sections: 12
Tableaux     : 4
Blocs de code: 6
```

---

## Extensibilité

L'outil est préparé pour de futurs ajouts :

| Fonctionnalité | Description |
|---|---|
| `--comparer` | Comparer deux fichiers |
| `--detecter-doublons` | Trouver les sections similaires |
| `--suggerer-condenser` | Proposer des réductions |
| `--filtrer definitions` | Lignes avec "est", "signifie" |
| `--filtrer exemples` | Blocs avec "Exemple" |
| `--filtrer erreurs` | Lignes avec "ERREUR" |

---

## Dépendances

- Aucune dépendance externe
- Utilise uniquement bash, grep, sed, wc

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-05 | Création initiale |

---
