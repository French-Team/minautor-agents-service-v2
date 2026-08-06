# Index — Classeur de Variables
---

## Principe Fondamental
---

## Structure

```
classeur-variables/
|-- index-classeur.md              <- point d'entrée (ce fichier)
|-- schema/                        <- schéma des variables
|   ``-- variables-definition.md    <- définition de chaque variable
|-- stockage/                      <- valeurs actuelles
|   ``-- variables-actuelles.md     <- état courant
``-- historique/                    <- historique des modifications
    ``-- historique-modifications.md
```

---

## Règles

### Règle 1 — Chaque variable a un nom unique

```yaml
variables:
  - nom: "resultat-fonction-1"
    type: "objet"
    description: "Resultat du traitement de la fonction 1"
    source: "fonction-1"
```

### Règle 2 — Chaque variable a un schéma

```markdown
## Variable : resultat-fonction-1

| Champ | Type | Obligatoire | Description |
|---|---|---|---|
| `id` | string | [OK] | Identifiant unique |
| `valeur` | any | [OK] | Valeur de la variable |
| `source` | string | [OK] | Fonction qui a écrit la variable |
| `date_creation` | datetime | [OK] | Date de création |
```

### Règle 3 — Lecture et écriture standardisées

```markdown
## Lire une variable

1. Chercher dans le classeur
2. Vérifier que la variable existe
3. Vérifier que la variable n'est pas expirée
4. Retourner la valeur

## Écrire une variable

1. Vérifier que le schéma est respecté
2. Écrire la valeur dans le classeur
3. Mettre à jour l'historique
4. Noter la source (quelle fonction a écrit)
```

### Règle 4 — Pas de modification directe

```
[NON] Modifier directement une variable dans le classeur
[OUI] Lire -> Modifier dans la fonction -> Réécrire dans le classeur
```

---

## Utilisation

### Créer une variable

1. Définir le schéma dans `schema/variables-definition.md`
2. Initialiser la valeur dans `stockage/variables-actuelles.md`
3. Documenter dans `historique/historique-modifications.md`

### Lire une variable

1. Chercher dans `stockage/variables-actuelles.md`
2. Vérifier que la variable existe
3. Retourner la valeur

### Écrire une variable

1. Vérifier que le schéma est respecté
2. Écrire dans `stockage/variables-actuelles.md`
3. Ajouter une entrée dans `historique/historique-modifications.md`

---

## Navigation

- **Parent** : [index-cerveau.md](../index-cerveau.md)
- **Convention** : [convention-classeur-variables.md](pense-betes/conventions/structures/convention-classeur-variables.md)
- **Structures** : [convention-structures.md](pense-betes/conventions/structures/convention-structures.md)
