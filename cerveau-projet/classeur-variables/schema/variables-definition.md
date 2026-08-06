# Schema -- Definition des Variables
---

## Variables

### [Aucune variable definie pour l'instant]

Pour ajouter une variable, utiliser le template suivant :

```markdown
## Variable : [nom-variable]

| Champ | Type | Obligatoire | Description |
|---|---|---|---|
| `id` | string | [OK] | Identifiant unique |
| `valeur` | any | [OK] | Valeur de la variable |
| `source` | string | [OK] | Fonction qui a ecrit la variable |
| `date_creation` | datetime | [OK] | Date de creation |
| `date_modification` | datetime | [NON] | Date de derniere modification |
| `description` | string | [NON] | Description de la variable |
```

---

## Types autorises

| Type | Description | Exemple |
|---|---|---|
| `string` | Texte | `"hello"` |
| `number` | Nombre | `42` |
| `boolean` | Booleen | `true` |
| `objet` | Objet JSON | `{"cle": "valeur"}` |
| `array` | Tableau | `[1, 2, 3]` |
| `null` | Valeur nulle | `null` |

---

## Navigation

- **Parent** : [index-classeur.md](../index-classeur.md)
- **Stockage** : [stockage/variables-actuelles.md](../stockage/variables-actuelles.md)
- **Historique** : [historique/historique-modifications.md](../historique/historique-modifications.md)
