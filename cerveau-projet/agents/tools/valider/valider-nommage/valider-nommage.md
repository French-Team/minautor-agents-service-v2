# Outil — Valider le Nommage

**Catégorie** : Valider
**Version** : v0.1.0
**Statut** : initial

---

## Objectif

Vérifier que le nommage des fichiers et dossiers respecte les conventions.

---

## Utilisation

```
valider-nommage(chemin=".", convention="kebab-case")
```

---

## Paramètres

| Paramètre | Type | Obligatoire | Description |
|---|---|---|---|
| `chemin` | string | Oui | Chemin du dossier à valider |
| `convention` | string | Non | Convention de nommage (défaut: "kebab-case") |

---

## Résultat

Retourne un rapport de validation du nommage.

```markdown
## Résultat

### Nommage valide
- agents/buffy/buffy.md -> OK
- cerveau-projet/index-cerveau.md -> OK

### Nommage invalide
- agents/Buffy/Buffy.md -> Doit être en minuscules
- cerveau-projet/IndexCerveau.md -> Doit être en kebab-case

### Statistiques
- Total fichiers : 20
- Valides : 18
- Invalides : 2
```

---

## Exemples

### Exemple 1 — Valider le nommage kebab-case

```
valider-nommage(chemin=".", convention="kebab-case")
```

**Résultat** :
- Tous les fichiers sont en kebab-case

### Exemple 2 — Valider le nommage snake_case

```
valider-nommage(chemin=".", convention="snake_case")
```

**Résultat** :
- 5 fichiers ne respectent pas la convention

---

## Dépendances

- `lister-fichiers` — Pour trouver les fichiers à valider
- `lister-dossiers` — Pour trouver les dossiers à valider
- `convention-renommage.md` — Pour connaître les règles de nommage

---

## Implémentation

### Commande bash equivalent

```bash
# Vérifier le kebab-case
ls | grep -E "^[a-z0-9]+(-[a-z0-9]+)*\.[a-z]+$"

# Vérifier le snake_case
ls | grep -E "^[a-z0-9]+(_[a-z0-9]+)*\.[a-z]+$"
```

### Dans le contexte du cerveau-projet

1. Utiliser `lister-fichiers` et `lister-dossiers`
2. Appliquer les règles de `convention-renommage.md`
3. Signaler les écarts

---

## Notes

- Cet outil est essentiel pour maintenir la cohérence
- Le nommage kebab-case est la convention par défaut
- Utile avant de créer de nouveaux fichiers

---

