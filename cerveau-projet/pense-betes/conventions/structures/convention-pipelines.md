# Convention — Pipelines
---

## Principe Fondamental
---

## Pourquoi un pipeline ?

| Problème | Solution |
|---|---|
| Fonctions couplées entre elles | Dé-couplage via le classeur |
| Difficile d'insérer une fonction | Le pipeline rend l'insertion transparente |
| Données éparpillées | Stockage centralisé et traçable |
| Réorganisation complexe | Réordonner les appels = changer l'ordre de lecture/écriture |

---

## Architecture

```
fonction-1 -> [ecrit resultat-1] -> classeur -> [lit resultat-1] -> fonction-2 -> [ecrit resultat-2] -> classeur -> fonction-3
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

## Structure d'un pipeline

```
pipeline/
|-- index-pipeline.md              <- point d'entrée global
|-- pipeline.md                    <- orchestrateur
|-- fonction-1/
|   ``-- fonction-1.md             <- première fonction
|-- fonction-2/
|   ``-- fonction-2.md             <- deuxième fonction
``-- fonction-3/
    ``-- fonction-3.md             <- troisième fonction
```

---

## Règles des pipelines

### Règle 1 — Chaque fonction est autonome

```
[NON] Fonction-1 appelle Fonction-2 directement
[OUI] Fonction-1 écrit dans le classeur, Fonction-2 lit du classeur
```

### Règle 2 — Communication via le classeur

```
[NON] Passer des données en paramètres
[OUI] Lire/écrire dans le classeur de variables
```

### Règle 3 — Traçabilité complète

Chaque opération de lecture/écriture doit être documentée dans l'historique du classeur.

### Règle 4 — Réorganisation facile

Pour changer l'ordre d'exécution, modifier uniquement l'ordre des appels dans l'orchestrateur.

---

## Exemple concret

### Pipeline de traitement de données

```
charger-donnees -> nettoyer-donnees -> transformer-donnees -> exporter-donnees
```

### Flux de données

```
1. charger-donnees -> écrit "donnees-brutes" dans le classeur
2. nettoyer-donnees -> lit "donnees-brutes" -> écrit "donnees-propres"
3. transformer-donnees -> lit "donnees-propres" -> écrit "donnees-transformees"
4. exporter-donnees -> lit "donnees-transformees" -> écrit "fichier-final"
```

### Insertion d'une nouvelle fonction

```
Avant :
charger-donnees -> nettoyer-donnees -> transformer-donnees -> exporter-donnees

Apres (insertion entre nettoyage et transformation) :
charger-donnees -> nettoyer-donnees -> [VALIDER-DONNEES] -> transformer-donnees -> exporter-donnees
```

La nouvelle fonction :
1. Lit "donnees-propres" dans le classeur
2. Traite
3. Écrit "donnees-validees" dans le classeur

Les autres fonctions n'ont pas besoin de changer !

---

## Relation avec les conventions existantes

| Convention | Lien |
|---|---|
| `convention-structures` | Le pipeline suit les mêmes règles de structure |
| `convention-classeur-variables` | Le pipeline utilise le classeur pour la communication |
| `convention-renommage` | Les fonctions suivent les patterns de nommage |
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

- [ ] Chaque fonction est autonome
- [ ] Chaque fonction lit les bonnes variables
- [ ] Chaque fonction écrit les bonnes variables
- [ ] Pas de modification directe dans le classeur
- [ ] L'historique est documenté
- [ ] Les dépendances entre fonctions sont claires
- [ ] La réorganisation est possible

---

## Voir aussi

- [convention-classeur-variables.md](convention-classeur-variables.md) -- stockage partagé
- [convention-structures.md](convention-structures.md) -- principes d'architecture
- [../../classeur-variables/index-classeur.md](../../classeur-variables/index-classeur.md) -- classeur de variables

---

*Convention conforme aux règles du cerveau-projet*
