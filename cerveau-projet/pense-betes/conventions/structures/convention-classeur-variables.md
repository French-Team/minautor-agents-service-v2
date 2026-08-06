# Convention -- Classeur de Variables
---

## Principe Fondamental
---

## Pourquoi un classeur ?

| Probleme | Solution |
|---|---|
| Fonctions couplees entre elles | De-couplage via le classeur |
| Difficile d'inserer une fonction | Le classeur rend l'insertion transparente |
| Donnees eparpillees | Stockage centralise et tracable |
| Reorganisation complexe | Reordonner les appels = changer l'ordre de lecture/ecriture |

---

## Architecture

```
fonction-1 -> [ecrit resultat-1] -> classeur -> [lit resultat-1] -> fonction-2 -> [ecrit resultat-2] -> classeur -> fonction-3
```

### Flux de donnees

```
1. Fonction-1 recoit les donnees d'entree
2. Fonction-1 traite et ecrit le resultat dans le classeur
3. Fonction-2 lit le resultat de Fonction-1 dans le classeur
4. Fonction-2 traite et ecrit son resultat dans le classeur
5. Fonction-3 lit le resultat de Fonction-2 dans le classeur
6. etc.
```

---

## Structure du classeur

```
classeur-variables/
|-- index-classeur.md              <- point d'entree global
|-- classeur-variables.md          <- orchestrateur principal
|-- schema/                        <- schema des variables
|   ``-- variables-definition.md    <- definition de chaque variable
|-- stockage/                      <- valeurs actuelles
|   ``-- variables-actuelles.md     <- etat courant
``-- historique/                    <- historique des modifications
    ``-- historique-modifications.md
```

**Statut** : Structure complete et operationnelle.

---

## Regles du classeur

### Regle 1 -- Chaque variable a un nom unique

```yaml
variables:
  - nom: "resultat-fonction-1"
    type: "objet"
    description: "Resultat du traitement de la fonction 1"
    source: "fonction-1"
    
  - nom: "resultat-fonction-2"
    type: "array"
    description: "Resultat du traitement de la fonction 2"
    source: "fonction-2"
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
| `date_modification` | datetime | [NON] | Date de derniere modification |
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

## Exemple concret

### Scenario : Pipeline de traitement

```
1. fonction-chargement -> ecrit "donnees-brutes" dans le classeur
2. fonction-nettoyage -> lit "donnees-brutes" -> ecrit "donnees-propres"
3. fonction-transformation -> lit "donnees-propres" -> ecrit "donnees-transformees"
4. fonction-export -> lit "donnees-transformees" -> ecrit "fichier-final"
```

### Insertion d'une nouvelle fonction

```
Avant :
fonction-chargement -> fonction-nettoyage -> fonction-transformation -> fonction-export

Apres (insertion entre nettoyage et transformation) :
fonction-chargement -> fonction-nettoyage -> [NOUVELLE-FONCTION] -> fonction-transformation -> fonction-export
```

La nouvelle fonction :
1. Lit "donnees-propres" dans le classeur
2. Traite
3. Ecrit "donnees-enrichies" dans le classeur

Les autres fonctions n'ont pas besoin de changer !

---

## Relation avec les conventions existantes

| Convention | Lien |
|---|---|
| `convention-structures` | Le classeur suit les memes regles de structure |
| `convention-renommage` | Les variables suivent les patterns de nommage |
| `convention-liens` | Les fonctions lient vers le classeur |

---

## Integration dans le workflow

### Creation d'un pipeline

```
1. Definir les variables necessaires (schema)
2. Creer les fonctions (une par dossier)
3. Creer la plateforme (orchestrateur)
4. Chaque fonction lit/ecrit dans le classeur
5. La plateforme appelle les fonctions dans l'ordre
```

### Reorganisation

```
1. Ouvrir la plateforme (point d'entree)
2. Modifier l'ordre des appels de fonctions
3. Tester le nouveau flux
4. Valider par RVAV
```

---

## Validation

Avant de valider un pipeline, verifier :

- [ ] Chaque variable a un schema defini
- [ ] Chaque fonction lit les bonnes variables
- [ ] Chaque fonction ecrit les bonnes variables
- [ ] Pas de modification directe dans le classeur
- [ ] L'historique est documente
- [ ] Les dependances entre fonctions sont claires

---

## Navigation

- **Parent** : [index-structures.md](index-structures.md)
- **Soeurs** : [convention-structures.md](convention-structures.md), [convention-renommage.md](../renommage/convention-renommage.md)
- **Regles** : [regles-hierarchie-par-niveau.md](../../regles-immuables/hierarchie/regles-hierarchie-par-niveau.md)
