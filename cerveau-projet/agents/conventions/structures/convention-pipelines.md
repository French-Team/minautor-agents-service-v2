---
identite:
  type: convention
  appartient_a: commun
  commun: true
---
# Convention -- Pipelines
---

## Principe Fondamental
---

## Pourquoi un pipeline ?

| Probleme | Solution |
|---|---|
| Fonctions couplees entre elles | De-couplage via le classeur |
| Difficile d'inserer une fonction | Le pipeline rend l'insertion transparente |
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

## Structure d'un pipeline

```
pipeline/
|-- index-pipeline.md              <- point d'entree global
|-- pipeline.md                    <- orchestrateur
|-- fonction-1/
|   ``-- fonction-1.md             <- premiere fonction
|-- fonction-2/
|   ``-- fonction-2.md             <- deuxieme fonction
``-- fonction-3/
    ``-- fonction-3.md             <- troisieme fonction
```

---

## Regles des pipelines

### Regle 1 -- Chaque fonction est autonome

```
[NON] Fonction-1 appelle Fonction-2 directement
[OUI] Fonction-1 ecrit dans le classeur, Fonction-2 lit du classeur
```

### Regle 2 -- Communication via le classeur

```
[NON] Passer des donnees en parametres
[OUI] Lire/ecrire dans le classeur de variables
```

### Regle 3 -- Tracabilite complete

Chaque operation de lecture/ecriture doit etre documentee dans l'historique du classeur.

### Regle 4 -- Reorganisation facile

Pour changer l'ordre d'execution, modifier uniquement l'ordre des appels dans l'orchestrateur.

---

## Exemple concret

### Pipeline de traitement de donnees

```
charger-donnees -> nettoyer-donnees -> transformer-donnees -> exporter-donnees
```

### Flux de donnees

```
1. charger-donnees -> ecrit "donnees-brutes" dans le classeur
2. nettoyer-donnees -> lit "donnees-brutes" -> ecrit "donnees-propres"
3. transformer-donnees -> lit "donnees-propres" -> ecrit "donnees-transformees"
4. exporter-donnees -> lit "donnees-transformees" -> ecrit "fichier-final"
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
3. Ecrit "donnees-validees" dans le classeur

Les autres fonctions n'ont pas besoin de changer !

---

## Relation avec les conventions existantes

| Convention | Lien |
|---|---|
| `convention-structures` | Le pipeline suit les memes regles de structure |
| `convention-classeur-variables` | Le pipeline utilise le classeur pour la communication |
| `convention-renommage` | Les fonctions suivent les patterns de nommage |
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

- [ ] Chaque fonction est autonome
- [ ] Chaque fonction lit les bonnes variables
- [ ] Chaque fonction ecrit les bonnes variables
- [ ] Pas de modification directe dans le classeur
- [ ] L'historique est documente
- [ ] Les dependances entre fonctions sont claires
- [ ] La reorganisation est possible

---

## Voir aussi

- [convention-classeur-variables.md](convention-classeur-variables.md) -- stockage partage
- [convention-structures.md](convention-structures.md) -- principes d'architecture
- [classeur-variables/index-classeur.md](../../classeur-variables/index-classeur.md) -- classeur de variables

---

*Convention conforme aux regles du cerveau-projet*
