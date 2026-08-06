# Outil -- Lister les Fichiers

**Categorie** : Explorer
**Version :** 0.2.0
**Statut :** prepare

---

## Objectif

Lister tous les fichiers d'un chemin donne.

---

## Utilisation

```
lister-fichiers(chemin=".", pattern="*", recursif=false)
```

---

## Parametres

| Parametre | Type | Obligatoire | Description |
|---|---|---|---|
| `chemin` | string | Oui | Chemin du dossier a explorer |
| `pattern` | string | Non | Pattern de filtrage (defaut: "*") |
| `recursif` | boolean | Non | Si true, explore les sous-dossiers (defaut: false) |

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

