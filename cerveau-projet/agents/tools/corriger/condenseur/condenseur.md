# Outil — Condenseur Markdown

**Catégorie** : Corriger
**Version** : 0.1.0-beta
**Statut** : beta
**Date création** : 2026-08-05
**Propriétaire** : Vulcain (outil partagé)

---

## Objectif

Condenser les fichiers markdown en réduisant le contenu non essentiel.

---

## Utilisation

```bash
condenseur.sh <fichier> [options]
```

---

## Options

| Option | Description |
|---|---|
| `--analyser` | Analyser le fichier uniquement |
| `--dry-run` | Afficher les changements sans les appliquer |
| `--verbose` | Afficher les détails |
| `--backup` | Créer une copie de sauvegarde |

---

## Ce que fait l'outil

| Action | Description |
|---|---|
| Condenser le frontmatter | Garder l'essentiel, supprimer les commentaires |
| Supprimer les commentaires | Dans les blocs de code |
| Réduire les séparateurs | Supprimer les séparateurs multiples |

---

## Seuils recommandés

| Seuil | Usage |
|---|---|
| **100 lignes** | Fichiers de configuration simples |
| **200 lignes** | Fichiers de contenu standard |
| **250 lignes** | Fichiers de contenu détaillé (recommandé) |
| **500 lignes** | Fichiers de documentation longue |

---

## Exemples

### Analyser un fichier

```bash
$ condenseur.sh --analyser cerveau-projet/agents/buffy/buffy.md

=== Analyse de buffy.md ===

Lignes totales : 368
Frontmatter : 106 lignes
Sections : 12
Lignes de tableaux : 97
Blocs de code : 368

Problèmes détectés :
- Frontmatter trop long (106 lignes, max recommandé: 30)
- Trop de tableaux (97 lignes, possible fusion)
- Fichier trop long (368 lignes, seuil: 250)
```

### Condenser (dry-run)

```bash
$ condenseur.sh --dry-run cerveau-projet/agents/buffy/buffy.md

=== Condensation de buffy.md ===

Condensation du frontmatter...
Suppression des commentaires inutiles...
Réduction des séparateurs...

=== Résumé ===
Lignes avant : 368
Lignes après : 329
Économie    : 39 lignes

[DRY-RUN] Aucun changement appliqué
```

### Appliquer

```bash
$ condenseur.sh cerveau-projet/agents/buffy/buffy.md

=== Condensation de buffy.md ===

[APPLIQUÉ] Fichier mis à jour
```

---

## Différence avec purifier-fichier

| Outil | Ce qu'il fait |
|---|---|
| `purifier-fichier` | Nettoye le formatage (blockquotes, lignes vides) |
| `condenseur` | Réduit le contenu (frontmatter, commentaires) |

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-05 | Création initiale |

---
