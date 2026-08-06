# Outil — Valider les Liens

**Catégorie** : Valider
**Version** : v0.1.0
**Statut** : initial

---

## Objectif

Vérifier que tous les liens dans les fichiers Markdown sont valides.

---

## Utilisation

```
valider-liens(chemin=".", fichiers="*.md", corriger=false)
```

---

## Paramètres

| Paramètre | Type | Obligatoire | Description |
|---|---|---|---|
| `chemin` | string | Oui | Chemin du dossier à valider |
| `fichiers` | string | Non | Pattern des fichiers à analyser (défaut: "*.md") |
| `corriger` | boolean | Non | Si true, tente de corriger les liens cassés (défaut: false) |

---

## Résultat

Retourne un rapport de validation des liens.

```markdown
## Résultat

### Liens valides
- [fichier1.md](fichier1.md) → OK
- [dossier/](dossier/) → OK

### Liens cassés
- [fichier2.md](fichier2.md) → Fichier non trouvé
- [autre.md](autre.md) → Chemin invalide

### Statistiques
- Total liens : 15
- Valides : 12
- Cassés : 3
```

---

## Exemples

### Exemple 1 — Valider tous les liens du projet

```
valider-liens(chemin=".")
```

**Résultat** :
- 15 liens trouvés
- 12 valides
- 3 cassés

### Exemple 2 — Valider et corriger les liens

```
valider-liens(chemin=".", corriger=true)
```

**Résultat** :
- 3 liens cassés corrigés automatiquement

---

## Dépendances

- `lister-fichiers` — Pour trouver les fichiers à analyser
- Système de fichiers — Pour vérifier l'existence des fichiers

---

## Implémentation

### Commande bash equivalent

```bash
# Trouver tous les liens dans les fichiers .md
grep -rn "\[.*\](.*)" *.md

# Vérifier si le fichier cible existe
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
- Les liens cassés peuvent casser la navigation
- Utile avant chaque mise à jour importante

---

