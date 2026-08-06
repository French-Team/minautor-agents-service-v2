# Spec -- Protocole Auto-Ameliorer le Cerveau
---

## Objectif technique

Permettre au cerveau-projet de s'ameliorer de maniere automatisee et tracable.

---

## Architecture

```
protocole-autoameliorer-cerveau/
|-- protocole-autoameliorer-cerveau.001.01.ebauche.md  <- le protocole
|-- spec/                                                <- CE FICHIER
``-- todo/                                                <- taches liees
```

---

## Donnees d'entree

| Donnee | Source | Obligatoire |
|---|---|---|
| Etat actuel du cerveau | `index-cerveau.md` | [OK] |
| Protocoles existants | `regles-immuables/general/` | [OK] |
| Conventions existantes | `conventions/` | [OK] |
| Regles immuables | `regles-immuables/` | [OK] |

---

## Donnees de sortie

| Donnee | Destination | Format |
|---|---|---|
| Ameliorations appliquees | Fichiers concernes | Markdown |
| Historique | Fichiers concernes | Tableau |
| Index mis a jour | `index-cerveau.md` | Liste |

---

## Algorithme

```markdown
1. LIRE index-cerveau.md
2. POUR CHAQUE section :
   a. VERIFIER si elle est a jour
   b. VERIFIER si elle est coherente
   c. SI amelioration necessaire :
      i. CREER un pense-bete
      ii. CREER une spec (si necessaire)
      iii. CREER un todo
      iv. APPLIQUER l'amelioration
      v. VALIDER par RVAV
3. METTRE A JOUR index-cerveau.md
4. SIGNER : "[nom-agent] -- [date]"
```

---

## Contraintes

| Contrainte | Description |
|---|---|
| **Coherence** | Toutes les sections doivent rester coherentes |
| **Tracabilite** | Chaque amelioration doit etre documentee |
| **Validation** | Chaque amelioration doit passer par RVAV |
| **Priorisation** | Ameliorer d'abord ce qui est critique |

---

## Tests

| Test | Critere |
|---|---|
| **Test de coherence** | Toutes les sections sont a jour |
| **Test de liens** | Tous les liens sont valides |
| **Test de conventions** | Toutes les conventions sont respectees |
| **Test de protocoles** | Tous les protocoles sont a jour |

---

## Navigation

- **Parent** : [protocole-autoameliorer-cerveau.md](../protocole-autoameliorer-cerveau.001.01.ebauche.md)
- **Todo** : [todo-protocole-autoameliorer-cerveau.md](../todo/todo-protocole-autoameliorer-cerveau.001.01.ebauche.md)

---

*Specification conforme aux conventions du cerveau-projet*
