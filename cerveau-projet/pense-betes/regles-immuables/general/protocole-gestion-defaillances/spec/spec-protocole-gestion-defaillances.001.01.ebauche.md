# Spec -- Protocole Gestion des Defaillances
---

## Objectif technique

Detecter et corriger automatiquement les defaillances du cerveau-projet.

---

## Architecture

```
protocole-gestion-defaillances/
|-- protocole-gestion-defaillances.001.01.ebauche.md  <- le protocole
|-- spec/                                               <- CE FICHIER
``-- todo/                                               <- taches liees
```

---

## Donnees d'entree

| Donnee | Source | Obligatoire |
|---|---|---|
| Etat du cerveau | `index-cerveau.md` | [OK] |
| Protocoles existants | `regles-immuables/general/` | [OK] |
| Conventions existantes | `conventions/` | [OK] |
| Fichiers d'agent | `agents/` | [OK] |

---

## Donnees de sortie

| Donnee | Destination | Format |
|---|---|---|
| Defaillances detectees | Log interne | Liste |
| Corrections appliquees | Fichiers concernes | Modifications |
| Historique | Fichiers concernes | Entrees |

---

## Algorithme de detection

```markdown
1. LIRE index-cerveau.md
2. POUR CHAQUE fichier reference :
   a. VERIFIER que le fichier existe
   b. VERIFIER que le lien est correct
   c. VERIFIER que le statut est a jour
3. POUR CHAQUE protocole :
   a. VERIFIER que le protocole est a jour
   b. VERIFIER que le protocole est respecte
4. POUR CHAQUE agent :
   a. VERIFIER que la fiche est a jour
   b. VERIFIER que les corrections sont appliquees
5. SI defaillance detectee :
   a. CLASSER la defaillance
   b. APPLIQUER la correction
   c. TRAITER la cause racine
   d. DOCUMENTER
```

---

## Algorithme de correction

```markdown
1. CLASSER la defaillance (oubli, erreur, incoherence, manque, obsolete)
2. EVALUER la priorite (haute, moyenne, basse)
3. APPLIQUER la correction appropriee :
   - Oubli -> Mettre a jour
   - Erreur -> Corriger
   - Incoherence -> Harmoniser
   - Manque -> Creer
   - Obsolete -> Mettre a jour ou archiver
4. VERIFIER que la correction est conforme
5. METTRE A JOUR les fichiers concernes
6. METTRE A JOUR les index
7. DOCUMENTER
```

---

## Contraintes

| Contrainte | Description |
|---|---|
| **Automatique** | La detection doit etre automatique |
| **Immediat** | Les defaillances hautes priorite sont corrigees immediatement |
| **Tracable** | Chaque correction est documentee |
| **Preventif** | Les causes racines sont traitees |

---

## Tests

| Test | Critere |
|---|---|
| **Test de detection** | Les defaillances sont detectees |
| **Test de correction** | Les corrections sont appliquees |
| **Test de tracabilite** | Les corrections sont documentees |
| **Test de prevention** | Les recidives sont evitees |

---

## Navigation

- **Parent** : [protocole-gestion-defaillances.md](../protocole-gestion-defaillances.001.01.ebauche.md)
- **Todo** : [todo-protocole-gestion-defaillances.md](../todo/todo-protocole-gestion-defaillances.001.01.ebauche.md)

---

*Specification conforme aux conventions du cerveau-projet*
