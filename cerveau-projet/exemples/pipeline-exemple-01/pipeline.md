# Pipeline — Orchestrateur

> **Fichier** : pipeline.md
> **Type** : orchestrateur
> **Role** : Orchestre l'exécution des fonctions du pipeline
> **Convention** : convention-structures

---

## Objectif

Point d'entrée unique pour exécuter le pipeline de traitement de données.

## Flux d'exécution

```
1. charger-donnees()
2. nettoyer-donnees()
3. transformer-donnees()
4. exporter-donnees()
```

---

## Appels de fonctions

### Étape 1 — Charger les données

```
charger-donnees/
└── charger-donnees.md
```

**Entrée** : Aucune (données fictives)
**Sortie** : Variable `donnees-brutes` dans le classeur

### Étape 2 — Nettoyer les données

```
nettoyer-donnees/
└── nettoyer-donnees.md
```

**Entrée** : Variable `donnees-brutes` du classeur
**Sortie** : Variable `donnees-propres` dans le classeur

### Étape 3 — Transformer les données

```
transformer-donnees/
└── transformer-donnees.md
```

**Entrée** : Variable `donnees-propres` du classeur
**Sortie** : Variable `donnees-transformees` dans le classeur

### Étape 4 — Exporter les données

```
exporter-donnees/
└── exporter-donnees.md
```

**Entrée** : Variable `donnees-transformees` du classeur
**Sortie** : Variable `fichier-final` dans le classeur

---

## Réorganisation

Pour réorganiser le pipeline, il suffit de modifier l'ordre des appels :

### Exemple : Inverser nettoyage et transformation

**Avant :**
```
1. charger-donnees()
2. nettoyer-donnees()
3. transformer-donnees()
4. exporter-donnees()
```

**Après :**
```
1. charger-donnees()
2. transformer-donnees()
3. nettoyer-donnees()
4. exporter-donnees()
```

Les fonctions n'ont pas besoin de changer ! Seul l'ordre des appels change.

---

## Validation

Avant de valider le pipeline, vérifier :

- [ ] Chaque fonction lit les bonnes variables
- [ ] Chaque fonction écrit les bonnes variables
- [ ] Pas de dépendance directe entre fonctions
- [ ] Le classeur contient toutes les variables attendues
- [ ] L'historique est documenté

---

## Navigation

- **Parent** : [index-pipeline.md](index-pipeline.md)
- **Classeur** : [../../classeur-variables/index-classeur.md](../../classeur-variables/index-classeur.md)

---

*Orchestrateur conforme aux conventions du cerveau-projet*
