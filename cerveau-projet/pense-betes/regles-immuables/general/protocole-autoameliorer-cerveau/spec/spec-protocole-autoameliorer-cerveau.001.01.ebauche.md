# Spec — Protocole Auto-Améliorer le Cerveau
---

## Objectif technique

Permettre au cerveau-projet de s'améliorer de manière automatisée et traçable.

---

## Architecture

```
protocole-autoameliorer-cerveau/
|-- protocole-autoameliorer-cerveau.001.01.ebauche.md  <- le protocole
|-- spec/                                                <- CE FICHIER
``-- todo/                                                <- tâches liées
```

---

## Données d'entrée

| Donnée | Source | Obligatoire |
|---|---|---|
| État actuel du cerveau | `index-cerveau.md` | [OK] |
| Protocoles existants | `regles-immuables/general/` | [OK] |
| Conventions existantes | `conventions/` | [OK] |
| Règles immuables | `regles-immuables/` | [OK] |

---

## Données de sortie

| Donnée | Destination | Format |
|---|---|---|
| Améliorations appliquées | Fichiers concernés | Markdown |
| Historique | Fichiers concernés | Tableau |
| Index mis à jour | `index-cerveau.md` | Liste |

---

## Algorithme

```markdown
1. LIRE index-cerveau.md
2. POUR CHAQUE section :
   a. VÉRIFIER si elle est à jour
   b. VÉRIFIER si elle est cohérente
   c. SI amélioration nécessaire :
      i. CRÉER un pense-bête
      ii. CRÉER une spec (si nécessaire)
      iii. CRÉER un todo
      iv. APPLIQUER l'amélioration
      v. VALIDER par RVAV
3. METTRE À JOUR index-cerveau.md
4. SIGNER : "[nom-agent] -- [date]"
```

---

## Contraintes

| Contrainte | Description |
|---|---|
| **Cohérence** | Toutes les sections doivent rester cohérentes |
| **Traçabilité** | Chaque amélioration doit être documentée |
| **Validation** | Chaque amélioration doit passer par RVAV |
| **Priorisation** | Améliorer d'abord ce qui est critique |

---

## Tests

| Test | Critère |
|---|---|
| **Test de cohérence** | Toutes les sections sont à jour |
| **Test de liens** | Tous les liens sont valides |
| **Test de conventions** | Toutes les conventions sont respectées |
| **Test de protocoles** | Tous les protocoles sont à jour |

---

## Navigation

- **Parent** : [protocole-autoameliorer-cerveau.md](../protocole-autoameliorer-cerveau.001.01.ebauche.md)
- **Todo** : [todo-protocole-autoameliorer-cerveau.md](../todo/todo-protocole-autoameliorer-cerveau.001.01.ebauche.md)

---

*Spécification conforme aux conventions du cerveau-projet*
