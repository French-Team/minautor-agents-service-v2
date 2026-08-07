# lister-fichiers

**Categorie** : Explorer
**Version :** 0.2.0
**Statut :** prepare

---

## Objectif

Lister tous les fichiers d'un chemin donne.

---

## Utilisation

Version Python (recommandee) :

```bash
python3 lister-fichiers.py [CHEMIN] [OPTIONS]
```

### Options

| Option | Description |
|---|---|
| `CHEMIN` | Chemin du dossier a explorer (defaut: .) |
| `--recursif, -r` | Explorer les sous-dossiers |
| `--extension` | Filtrer par extension (ex: "md", "py", "sh") |
| `--version` | Afficher la version |
| `--aide, -h` | Afficher l'aide |

### Exemples

```bash
python3 lister-fichiers.py
python3 lister-fichiers.py --recursif --extension md
```

Version bash equivalente : `lister-fichiers.sh`.

---

## Resultat

Retourne une liste de chemins de fichiers.

```markdown
## Resultat

- fichier1.md
- fichier2.md
- sous-dossier/fichier3.md
```

---

## Exemples

### Exemple 1 -- Lister tous les fichiers .md

```
lister-fichiers(chemin=".", pattern="*.md")
```

**Resultat** :
- index-cerveau.md
- demarrer.md
- agents/buffy/buffy.md
- ...

### Exemple 2 -- Lister les fichiers recursivement

```
lister-fichiers(chemin=".", pattern="*.md", recursif=true)
```

---

## Dependances

- Aucune dependance externe
- Utilise les outils du systeme de fichiers

---

## Implementation

### Commande bash equivalent

```bash
# Lister les fichiers .md
find . -name "*.md" -type f

# Lister tous les fichiers
find . -type f
```

### Implementation

1. Parcourir le dossier specifie
2. Appliquer le pattern de filtrage
3. Retourner la liste des fichiers correspondants

---

## Notes

- Cet outil est utilise pour trouver des fichiers specifiques
- Le pattern accepte les wildcards (*, ?)
- Utile pour valider la structure du projet

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter, VERSION 0.2.0, statut prepare |
| 0.2.0-py | 2026-08-07 | Version Python creee (lister-fichiers.py), basee sur outil-template.py |

