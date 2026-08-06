# Convention — Classeur de Variables
---

## Principe Fondamental
---

## Pourquoi un classeur ?

| Problème | Solution |
|---|---|
| Fonctions couplées entre elles | Dé-couplage via le classeur |
| Difficile d'insérer une fonction | Le classeur rend l'insertion transparente |
| Données éparpillées | Stockage centralisé et traçable |
| Réorganisation complexe | Réordonner les appels = changer l'ordre de lecture/écriture |

---

## Architecture

```
fonction-1 → [ecrit resultat-1] → classeur → [lit resultat-1] → fonction-2 → [ecrit resultat-2] → classeur → fonction-3
```

### Flux de données

```
1. Fonction-1 reçoit les données d'entrée
2. Fonction-1 traite et écrit le résultat dans le classeur
3. Fonction-2 lit le résultat de Fonction-1 dans le classeur
4. Fonction-2 traite et écrit son résultat dans le classeur
5. Fonction-3 lit le résultat de Fonction-2 dans le classeur
6. etc.
```

---

## Structure du classeur

```
classeur-variables/
├── index-classeur.md              ← point d'entrée global
├── classeur-variables.md          ← orchestrateur principal
├── schema/                        ← schéma des variables
│   └── variables-definition.md    ← définition de chaque variable
├── stockage/                      ← valeurs actuelles
│   └── variables-actuelles.md     ← état courant
└── historique/                    ← historique des modifications
    └── historique-modifications.md
```

**Statut** : Structure complète et opérationnelle.

---

## Règles du classeur

### Règle 1 — Chaque variable a un nom unique

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

### Règle 2 — Chaque variable a un schéma

```markdown
## Variable : resultat-fonction-1

| Champ | Type | Obligatoire | Description |
|---|---|---|---|
| `id` | string | [OK] | Identifiant unique |
| `valeur` | any | [OK] | Valeur de la variable |
| `source` | string | [OK] | Fonction qui a écrit la variable |
| `date_creation` | datetime | [OK] | Date de création |
| `date_modification` | datetime | [NON] | Date de dernière modification |
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
[OUI] Lire → Modifier dans la fonction → Réécrire dans le classeur
```

---

## Exemple concret

### Scénario : Pipeline de traitement

```
1. fonction-chargement → écrit "donnees-brutes" dans le classeur
2. fonction-nettoyage → lit "donnees-brutes" → écrit "donnees-propres"
3. fonction-transformation → lit "donnees-propres" → écrit "donnees-transformees"
4. fonction-export → lit "donnees-transformees" → écrit "fichier-final"
```

### Insertion d'une nouvelle fonction

```
Avant :
fonction-chargement → fonction-nettoyage → fonction-transformation → fonction-export

Apres (insertion entre nettoyage et transformation) :
fonction-chargement → fonction-nettoyage → [NOUVELLE-FONCTION] → fonction-transformation → fonction-export
```

La nouvelle fonction :
1. Lit "donnees-propres" dans le classeur
2. Traite
3. Écrit "donnees-enrichies" dans le classeur

Les autres fonctions n'ont pas besoin de changer !

---

## Relation avec les conventions existantes

| Convention | Lien |
|---|---|
| `convention-structures` | Le classeur suit les mêmes règles de structure |
| `convention-renommage` | Les variables suivent les patterns de nommage |
| `convention-liens` | Les fonctions lient vers le classeur |

---

## Intégration dans le workflow

### Création d'un pipeline

```
1. Définir les variables nécessaires (schéma)
2. Créer les fonctions (une par dossier)
3. Créer la plateforme (orchestrateur)
4. Chaque fonction lit/écrit dans le classeur
5. La plateforme appelle les fonctions dans l'ordre
```

### Réorganisation

```
1. Ouvrir la plateforme (point d'entrée)
2. Modifier l'ordre des appels de fonctions
3. Tester le nouveau flux
4. Valider par RVAV
```

---

## Validation

Avant de valider un pipeline, vérifier :

- [ ] Chaque variable a un schéma défini
- [ ] Chaque fonction lit les bonnes variables
- [ ] Chaque fonction écrit les bonnes variables
- [ ] Pas de modification directe dans le classeur
- [ ] L'historique est documenté
- [ ] Les dépendances entre fonctions sont claires

---

## Navigation

- **Parent** : [index-structures.md](index-structures.md)
- **Sœurs** : [convention-structures.md](convention-structures.md), [convention-renommage.md](../renommage/convention-renommage.md)
- **Règles** : [regles-hierarchie-par-niveau.md](../../regles-immuables/hierarchie/regles-hierarchie-par-niveau.md)
