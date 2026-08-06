# Convention -- Outils d'Agent
---

## Principe Fondamental
---

## Pourquoi ?

| Probleme | Solution |
|---|---|
| Outil generique = pas optimise | Outil d'agent = optimise pour nos besoins |
| Impossible d'ameliorer les outils existants | Nos outils evoluent avec nous |
| Copier le cerveau d'un projet a l'autre | Les outils sont transferables |

---

## Regles de creation

### Regle 1 -- Chaque outil est proprietaire

```
Chaque outil a un proprietaire (l'agent qui l'a cree).
Mais il est partage et ameliorable par tous.
```

### Regle 2 -- Chaque outil est documente

```
Chaque outil a :
- Une description (lister-agents.md)
- Une spec technique (spec/spec-*.md)
- Un historique de versions
```

### Regle 3 -- Chaque outil est teste

```
Avant d'etre utilise :
1. Creer l'outil
2. Ecrire les tests
3. Executer les tests
4. Valider par RVAV
```

### Regle 4 -- Chaque outil evolue

```
Les outils ne sont jamais "finis".
Ils evoluent avec nos besoins.
Chaque amelioration est documentee.
```

---

## Structure d'un outil d'agent

```
agents/tools/[categorie]/[nom-outil]/
├── [nom-outil].md           ← documentation principale
├── spec/
│   └── spec-[nom-outil].md  ← specification technique
├── todo/
│   └── todo-[nom-outil].md  ← ameliorations
├── tests/
│   ├── test-[nom-outil].md  ← plan de tests
│   └── resultats/           ← resultats
└── versions/
    ├── beta/                ← version beta
    └── stable/              ← version stable
```

---

## Cycle de vie d'un outil

```
1. Besoin detecte → "J'ai besoin de lister les agents"
2. Creation → Creer l'outil en beta
3. Test → Tester l'outil
4. Integration → L'utiliser dans mes missions
5. Amelioration → Ajouter des fonctionnalites
6. Stabilisation → Version 1.0.0
7. Partage → Les autres agents peuvent l'utiliser
```

---

## Exemple concret

### Besoin

Buffy a besoin de lister les agents频繁ement.

### Solution

```markdown
# Outil : lister-agents

## Objectif
Lister tous les agents avec leurs informations.

## Utilisation
lister-agents(format="table", champs="nom,role,statut")

## Avantages
- Retourne uniquement les agents
- Format table/liste/JSON
- Filtre par statut/role
```

---

## Transferabilite

### Principe
### Ce qui evolue

| Element | Evolution |
|---|---|
| **Agents** | Plus d'agents dedies |
| **Outils** | Plus d'outils performants |
| **Protocoles** | Plus de processus optimises |
| **Conventions** | Plus de regles documentees |

### Ce qui reste

| Element | Constant |
|---|---|
| **Structure** | Meme organisation |
| **Principes** | Meme philosophie |
| **Cycle** | Cerberus → Agent → Cerberus |

---

## Liens

- **Protocole** : `protocole-outils` -- comment creer des outils
- **Convention** : `convention-structures` -- structure des dossiers
- **Regles** : `regles-validation-rigoureuse` -- comment valider

---

> Les agents doivent TOUJOURS creer leurs propres outils.
