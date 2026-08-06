# Outil — Valider les Conventions

**Catégorie** : Valider
**Version** : v0.1.0
**Statut** : initial

---

## Objectif

Vérifier que les fichiers respectent les conventions du cerveau-projet.

---

## Utilisation

```
valider-conventions(chemin=".", types="all")
```

---

## Paramètres

| Paramètre | Type | Obligatoire | Description |
|---|---|---|---|
| `chemin` | string | Oui | Chemin du dossier à valider |
| `types` | string | Non | Types de conventions: "all", "structures", "renommage", "liens", "protocoles" (défaut: "all") |

---

## Résultat

Retourne un rapport de validation des conventions.

```markdown
## Résultat

### Conventions respectées
- convention-structures.md -> OK
- convention-renommage.md -> OK
- convention-liens.md -> OK

### Conventions violées
- Fichier sans en-tête YAML
- Lien relatif incorrect

### Statistiques
- Total fichiers : 25
- Conformes : 22
- Non conformes : 3
```

---

## Exemples

### Exemple 1 — Valider toutes les conventions

```
valider-conventions(chemin=".")
```

**Résultat** :
- 25 fichiers analysés
- 22 conformes
- 3 non conformes

### Exemple 2 — Valider uniquement les structures

```
valider-conventions(chemin=".", types="structures")
```

**Résultat** :
- Tous les fichiers respectent la structure

---

## Dépendances

- `lister-fichiers` — Pour trouver les fichiers à valider
- `convention-structures.md` — Pour connaître la structure attendue
- `convention-renommage.md` — Pour connaître les règles de nommage
- `convention-liens.md` — Pour connaître les règles de liens
- `convention-protocoles.md` — Pour connaître les règles de protocoles

---

## Implémentation

### Dans le contexte du cerveau-projet

1. Lire les conventions applicables
2. Analyser chaque fichier
3. Comparer avec les règles
4. Signaler les écarts

---

## Notes

- Cet outil est essentiel pour la qualité du cerveau
- Les conventions sont documentées dans `conventions/`
- Utile avant chaque mise à jour importante

---

