# Outil -- Valider les Liens

**Categorie** : Valider
**Version :** 0.4.0
**Statut :** prepare

---

## Objectif

Verifier que tous les liens dans les fichiers Markdown sont valides.

---

## Utilisation

```
valider-liens(chemin=".", fichiers="*.md", corriger=false)
```

---

## Parametres

| Parametre | Type | Obligatoire | Description |
|---|---|---|---|
| `chemin` | string | Oui | Chemin du dossier a valider |
| `fichiers` | string | Non | Pattern des fichiers a analyser (defaut: "*.md") |
| `corriger` | boolean | Non | Si true, tente de corriger les liens casses (defaut: false) |

---

## Resultat

Retourne un rapport de validation des liens.

```markdown
## Resultat

### Liens valides
- [fichier1.md](fichier1.md) -> OK
- [dossier/](dossier/) -> OK

### Liens casses
- [fichier2.md](fichier2.md) -> Fichier non trouve
- [autre.md](autre.md) -> Chemin invalide

### Statistiques
- Total liens : 15
- Valides : 12
- Casses : 3
```

---

## Exemples

### Exemple 1 -- Valider tous les liens du projet

```
valider-liens(chemin=".")
```

**Resultat** :
- 15 liens trouves
- 12 valides
- 3 casses

### Exemple 2 -- Valider et corriger les liens

```
valider-liens(chemin=".", corriger=true)
```

**Resultat** :
- 3 liens casses corriges automatiquement

---

## Dependances

- `lister-fichiers` -- Pour trouver les fichiers a analyser
- Systeme de fichiers -- Pour verifier l'existence des fichiers

---

## Implementation

### Commande bash equivalent

```bash
# Trouver tous les liens dans les fichiers .md
grep -rn "\[.*\](.*)" *.md

# Verifier si le fichier cible existe
test -f "chemin/cible.md"
```

### Implementation

1. Utiliser `lister-fichiers` pour trouver tous les .md
2. Extraire les liens Markdown de chaque fichier
3. Verifier que chaque cible existe
4. Retourner le rapport de validation

---

## Notes

- Cet outil est essentiel pour la maintenance du cerveau
- Les liens casses peuvent casser la navigation
- Utile avant chaque mise a jour importante

---

