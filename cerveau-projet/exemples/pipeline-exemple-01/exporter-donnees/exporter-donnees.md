# exporter-donnees

> **Fichier** : exporter-donnees.md
> **Type** : fonction
> **Role** : Exporter les données transformées
> **Convention** : convention-structures

---

## Objectif

Lire les données transformées du classeur, les exporter dans un fichier (simulé), et écrire le chemin du fichier dans le classeur.

## Entrée / Sortie

| Type | Variable | Description |
|---|---|---|
| **Entrée** | `donnees-transformees` | Données à exporter |
| **Sortie** | `fichier-final` | Chemin du fichier exporté |

---

## Logique

```
1. Lire la variable "donnees-transformees" du classeur
2. Vérifier que la variable existe
3. Exporter les données :
   - Générer un nom de fichier basé sur la date
   - Formater les données en JSON
   - Simuler l'écriture du fichier
4. Écrire la variable "fichier-final" dans le classeur
5. Ajouter une entrée dans l'historique
```

---

## Règles d'export

| Règle | Description |
|---|---|
| **Nom du fichier** | `export-YYYY-MM-DD-HHMMSS.json` |
| **Format** | JSON avec indentation |
| **Emplacement** | `exports/` (simulé) |

---

## Exemple d'export

**Entrée (donnees-transformees) :**
```json
[
  {"id": 1, "nom": "Alice", "age": 25, "tranche_age": "jeune"},
  {"id": 2, "nom": "Bob", "age": 30, "tranche_age": "adulte"}
]
```

**Fichier généré :**
```json
{
  "date_export": "2026-08-04T12:00:00Z",
  "nombre_enregistrements": 2,
  "donnees": [
    {"id": 1, "nom": "Alice", "age": 25, "tranche_age": "jeune"},
    {"id": 2, "nom": "Bob", "age": 30, "tranche_age": "adulte"}
  ]
}
```

---

## Écriture dans le classeur

### Variable `fichier-final`

| Champ | Valeur |
|---|---|
| `id` | `"fichier-final-001"` |
| `valeur` | `"exports/export-2026-08-04-120000.json"` |
| `source` | `"exporter-donnees"` |
| `date_creation` | *(date actuelle)* |

### Historique

```markdown
## [DATE] — Écriture

- **Variable** : fichier-final
- **Ancienne valeur** : *(aucune)*
- **Nouvelle valeur** : "exports/export-2026-08-04-120000.json"
- **Source** : exporter-donnees
- **Raison** : Export des données transformées
```

---

## Validation

Avant de valider cette fonction, vérifier :

- [ ] La variable `donnees-transformees` existe dans le classeur
- [ ] Le fichier est correctement formaté
- [ ] La variable `fichier-final` est écrite dans le classeur
- [ ] L'historique est documenté
- [ ] Aucune dépendance directe avec d'autres fonctions

---

## Navigation

- **Parent** : [../index-pipeline.md](../index-pipeline.md)
- **Classeur** : [../../../classeur-variables/index-classeur.md](../../../classeur-variables/index-classeur.md)
- **Fonction précédente** : [../transformer-donnees/transformer-donnees.md](../transformer-donnees/transformer-donnees.md)

---

*Fonction conforme aux conventions du cerveau-projet*
