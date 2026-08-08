---
identite:
  type: classeur
  appartient_a: commun
  commun: true
---
# Index -- Classeur de Variables
---

## Principe Fondamental
---

## Structure

```
classeur-variables/
|-- index-classeur.md              <- point d'entree (ce fichier)
|-- schema/                        <- schema des variables
|   ``-- variables-definition.md    <- definition de chaque variable
|-- stockage/                      <- valeurs actuelles
|   ``-- variables-actuelles.md     <- etat courant
``-- historique/                    <- historique des modifications
    ``-- historique-modifications.md
```

---

## Regles

### Regle 1 -- Chaque variable a un nom unique

```yaml
variables:
  - nom: "resultat-fonction-1"
    type: "objet"
    description: "Resultat du traitement de la fonction 1"
    source: "fonction-1"
```

### Regle 2 -- Chaque variable a un schema

```markdown
## Variable : resultat-fonction-1

| Champ | Type | Obligatoire | Description |
|---|---|---|---|
| `id` | string | [OK] | Identifiant unique |
| `valeur` | any | [OK] | Valeur de la variable |
| `source` | string | [OK] | Fonction qui a ecrit la variable |
| `date_creation` | datetime | [OK] | Date de creation |
```

### Regle 3 -- Lecture et ecriture standardisees

```markdown
## Lire une variable

1. Chercher dans le classeur
2. Verifier que la variable existe
3. Verifier que la variable n'est pas expiree
4. Retourner la valeur

## Ecrire une variable

1. Verifier que le schema est respecte
2. Ecrire la valeur dans le classeur
3. Mettre a jour l'historique
4. Noter la source (quelle fonction a ecrit)
```

### Regle 4 -- Pas de modification directe

```
[NON] Modifier directement une variable dans le classeur
[OUI] Lire -> Modifier dans la fonction -> Reecrire dans le classeur
```

---

## Utilisation

### Creer une variable

1. Definir le schema dans `schema/variables-definition.md`
2. Initialiser la valeur dans `stockage/variables-actuelles.md`
3. Documenter dans `historique/historique-modifications.md`

### Lire une variable

1. Chercher dans `stockage/variables-actuelles.md`
2. Verifier que la variable existe
3. Retourner la valeur

### Ecrire une variable

1. Verifier que le schema est respecte
2. Ecrire dans `stockage/variables-actuelles.md`
3. Ajouter une entree dans `historique/historique-modifications.md`

---

## Navigation

- **Parent** : [index-cerveau.md](../index-cerveau.md)
- **Convention** : [convention-classeur-variables.md](pense-betes/conventions/structures/convention-classeur-variables.md)
- **Structures** : [convention-structures.md](pense-betes/conventions/structures/convention-structures.md)
