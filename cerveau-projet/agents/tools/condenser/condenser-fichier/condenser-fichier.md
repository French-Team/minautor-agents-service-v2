---
identite:
  type: outil
  appartient_a: commun
  commun: true
  combos:
    - combo-corriger-fichier
---
# condenser-fichier

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** condenser
**Chemin :** `agents/tools/condenser/condenser-fichier/`
**Proprietaire :** Buffy (outil partage)

---

## Objectif

Condenser les fichiers markdown en reduisant le contenu non essentiel.

---

## Utilisation

### CLI Python (version 0.2.0-py)

```
python3 condenser-fichier.py <fichier> [options]

Options :
  --analyser    Analyser le fichier uniquement
  --dry-run     Afficher les changements sans les appliquer
  --verbose     Afficher les details
  --backup      Creer une copie de sauvegarde
  --version     Afficher la version
```

### CLI bash (version originale)

```bash
condenser-fichier.sh <fichier> [options]
```

---

## Options

| Option | Description |
|---|---|
| `--analyser` | Analyser le fichier uniquement |
| `--dry-run` | Afficher les changements sans les appliquer |
| `--verbose` | Afficher les details |
| `--backup` | Creer une copie de sauvegarde |

---

## Ce que fait l'outil

| Action | Description |
|---|---|
| Condenser le frontmatter | Garder l'essentiel, supprimer les commentaires |
| Supprimer les commentaires | Dans les blocs de code |
| Reduire les separateurs | Supprimer les separateurs multiples |

---

## Seuils recommandes

| Seuil | Usage |
|---|---|
| **100 lignes** | Fichiers de configuration simples |
| **200 lignes** | Fichiers de contenu standard |
| **250 lignes** | Fichiers de contenu detaille (recommande) |
| **500 lignes** | Fichiers de documentation longue |

---

## Exemples

### Analyser un fichier

```bash
$ condenser-fichier.sh --analyser cerveau-projet/agents/buffy/buffy.md

=== Analyse de buffy.md ===

Lignes totales : 368
Frontmatter : 106 lignes
Sections : 12
Lignes de tableaux : 97
Blocs de code : 368

Problemes detectes :
- Frontmatter trop long (106 lignes, max recommande: 30)
- Trop de tableaux (97 lignes, possible fusion)
- Fichier trop long (368 lignes, seuil: 250)
```

### Condenser (dry-run)

```bash
$ condenser-fichier.sh --dry-run cerveau-projet/agents/buffy/buffy.md

=== Condensation de buffy.md ===

Condensation du frontmatter...
Suppression des commentaires inutiles...
Reduction des separateurs...

=== Resume ===
Lignes avant : 368
Lignes apres : 329
Economie    : 39 lignes

[DRY-RUN] Aucun changement applique
```

### Appliquer

```bash
$ condenser-fichier.sh cerveau-projet/agents/buffy/buffy.md

=== Condensation de buffy.md ===

[APPLIQUE] Fichier mis a jour
```

---

## Difference avec nettoyer-fichier

| Outil | Ce qu'il fait |
|---|---|
| `nettoyer-fichier` | Nettoye le formatage (blockquotes, lignes vides) |
| `condenser-fichier` | Reduit le contenu (frontmatter, commentaires) |

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0-py | 2026-08-07 | Version Python creee (meme dossier, meme nom, base sur outil-template.py) |
| 0.1.0-beta | 2026-08-05 | Creation initiale |

---
