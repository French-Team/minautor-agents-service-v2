# Detection Automatique des Defaillances
---

## Verifications obligatoires

### 1. Fichier AGENTS.md

| Verification | Critere | Action si echec |
|---|---|---|
| **AGENTS.md existe** | Fichier present a la racine | Creer le fichier |
| **Agent principal identifie** | Section "Agent Principal Actuel" remplie | Mettre a jour |
| **Agent actuel identifie** | Mon nom est dans le fichier | Se presenter |
| **Historique a jour** | Derniere entree recente | Ajouter une entree |

### 2. Fiche d'agent

| Verification | Critere | Action si echec |
|---|---|---|
| **Fiche existe** | `agents/[nom]/[nom].md` existe | Creer la fiche |
| **Fiche a jour** | Derniere session documentee | Mettre a jour |
| **Corrections lues** | `corrections.md` lu en priorite | Lire les corrections |
| **Corrections appliquees** | Regles specifiques appliquees | Appliquer les regles |

### 3. Index principaux

| Verification | Critere | Action si echec |
|---|---|---|
| **index-cerveau.md** | Statut a jour | Mettre a jour |
| **index-regles-general.md** | Tous les protocoles listes | Ajouter les manquants |
| **index-conventions.md** | Toutes les conventions listees | Ajouter les manquantes |

### 4. Conventions

| Verification | Critere | Action si echec |
|---|---|---|
| **Fichiers existent** | Tous les fichiers references existent | Creer les fichiers |
| **Liens valides** | Tous les liens pointent vers des fichiers existants | Corriger les liens |
| **Statut a jour** | Statut correct dans chaque fichier | Mettre a jour |

### 5. Protocoles

| Verification | Critere | Action si echec |
|---|---|---|
| **Protocoles existent** | Tous les protocoles references existent | Creer les protocoles |
| **Protocoles a jour** | Derniere modification documentee | Mettre a jour |
| **Protocoles respectes** | Les etapes sont suivies | Suivre le protocole |

---

## Verifications periodiques

### Hebdomadaires

| Verification | Critere | Action si echec |
|---|---|---|
| **Coherence generale** | Toutes les sections coherentes | Harmoniser |
| **Liens casses** | Tous les liens valides | Corriger |
| **Statuts a jour** | Tous les statuts corrects | Mettre a jour |

### Mensuelles

| Verification | Critere | Action si echec |
|---|---|---|
| **Archivage** | Elements obsoletes archives | Archiver |
| **Amelioration** | Protocoles ameliores si necessaire | Ameliorer |
| **Documentation** | Documentation complete | Completer |

---

## Declencheurs automatiques

### Declenchement immediat

| Declencheur | Action |
|---|---|
| **AGENTS.md manquant** | Creer immediatement |
| **Fiche agent manquante** | Creer immediatement |
| **Incoherence majeure** | Corriger immediatement |
| **Protocole non suivi** | Appliquer immediatement |

### Declenche a la prochaine session

| Declencheur | Action |
|---|---|
| **Index pas a jour** | Mettre a jour |
| **Lien casse** | Corriger |
| **Statut incorrect** | Corriger |

### Declenche quand possible

| Declencheur | Action |
|---|---|
| **Amelioration mineure** | Appliquer |
| **Documentation incomplete** | Completer |
| **Archivage necessaire** | Archiver |

---

## Comment signaler une defaillance

### Si tu detectes une defaillance

```
1. Noter la defaillance :
   - Type (oubli, erreur, incoherence, manque, obsolete)
   - Fichier concerne
   - Priorite (haute, moyenne, basse)
   - Description

2. Appliquer la correction si possible

3. Si la correction necessite une validation :
   - Creer un pense-bete
   - Demander validation a l'utilisateur

4. Documenter la defaillance et la correction
```

### Si tu es l'auteur de la defaillance

```
1. Accepter la defaillance
2. Appliquer la correction
3. Ajouter une regle dans corrections.md si necessaire
4. Documenter l'amelioration
```

---

## Priorites

| Priorite | Delai | Exemple |
|---|---|---|
| **Haute** | Immediat | AGENTS.md manquant, incoherence majeure |
| **Moyenne** | Avant prochaine session | Index pas a jour, lien casse |
| **Basse** | Quand possible | Amelioration mineure |

---

## Navigation

- **Parent** : [protocole-gestion-defaillances.md](protocole-gestion-defaillances.001.01.ebauche.md)
- **Protocoles** : [index-regles-general.md](../index-regles-general.md)

---

*Detection automatique conforme aux conventions du cerveau-projet*
