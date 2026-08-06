# Outil: corriger-accents

> **Catégorie**: Corriger  
> **Version**: 0.1.0-beta  
> **Statut**: Bêta  
> **Chemin**: `agents/tools/corriger/corriger-accents/`

---

## Description

Détecte et corrige les accents et caractères non-ASCII dans les fichiers markdown, conformément à la règle `regles-emojis-ascii.md`.

---

## Fonctionnalités

| Fonction | Description |
|---|---|
| Détection | Identifie les caractères non-ASCII |
| Correction | Remplace par des équivalents ASCII |
| Dictionnaire | Fichier de correspondance extensible |
| Dry-run | Aperçu sans modification |
| Sauvegarde | Crée une copie .bak avant modification |

---

## Utilisation

### Commande de base

```bash
# Corriger les accents d'un fichier
corriger-accents.sh fichier.md

# Aperçu des changements
corriger-accents.sh --dry-run fichier.md

# Détails + aperçu
corriger-accents.sh --verbose --dry-run fichier.md
```

### Options

| Option | Description |
|---|---|
| `--dry-run` | Afficher les changements sans les appliquer |
| `--verbose` | Afficher les détails des remplacements |
| `--dictionnaire` | Chemin vers le dictionnaire personnalisé |
| `--help` | Afficher l'aide |

---

## Dictionnaire

Le dictionnaire par défaut est `dictionnaire-accents.txt` dans le même dossier.

### Format

```
accent|remplacement
```

### Exemples

```
é|e
è|e
ê|e
à|a
â|a
ç|c
'|'
'|'
```

### Ajouter des accents

Éditez le fichier `dictionnaire-accents.txt` et ajoutez des lignes au format:

```
nouvel_accent|remplacement
```

---

## Caractères gérés

| Type | Exemples |
|---|---|
| Accents français | é, è, ê, ë, à, â, î, ï, ô, ù, û, ü, ÿ, ç |
| Apostrophes courbes | ', ', ' |
| Guillemets courbes | ", " |
| Caractères spéciaux | (selon dictionnaire) |

---

## Exemple

### Avant

```markdown
# Titre avec accents
Ceci est un fichier avec des accents : é, è, ê, à, ç.
```

### Après

```markdown
# Titre avec accents
Ceci est un fichier avec des accents : e, e, e, a, c.
```

---

## Sécurité

| Mesure | Description |
|---|---|
| Sauvegarde | Crée `fichier.md.bak` avant modification |
| Dry-run | Aperçu possible sans modification |
| Vérification | Compte les caractères restants |

---

## Dépendances

| Dépendance | Type | Description |
|---|---|---|
| `bash` | Shell | Exécution des scripts |
| `perl` | Standard | Détection et remplacement |
| `diff` | Standard | Affichage des changements |
| `mktemp` | Standard | Fichiers temporaires |

---

## Limitations

- Ne gère pas les caractères Unicode complexes
- Peut nécessiter un dictionnaire personnalisé pour des langues spécifiques
- Les remplacements sont simples (pas de contexte)

---

## Voir aussi

- `corriger-emojis` — Pour les emojis Unicode
- `verifier-role-fichier` — Pour vérifier le rôle d'un fichier
- `regles-emojis-ascii.md` — Règle immuable

---

## Historique

| Version | Date | Changement |
|---|---|---|
| 0.1.0-beta | 2026-08-05 | Création initiale |

---

## Navigation

- **Outil précédent**: [corriger-emojis](../corriger-emojis/corriger-emojis.md)
- **Outil suivant**: [verifier-role-fichier](../valider/verifier-role-fichier/verifier-role-fichier.md)
- **Index**: [index-tools.md](../../index-tools.md)