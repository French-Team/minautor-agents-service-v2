# Outil -- Lister les Outils

**Categorie** : Lister
**Version** : 0.2.0
**Statut** : prepare
**Date creation** : 2026-08-05
**Proprietaire** : Buffy (outil partage)

---

## Objectif

Lister tous les outils partages du cerveau-projet avec leurs informations.

**Pourquoi cet outil ?**
- Cet outil retourne exactement la liste des outils
- Il est optimise pour nos projets futurs
- Il evolue avec nos besoins
- Il est concu pour nos agents et nos projets

---

## Utilisation

```
lister-outils(format="table", categorie="toutes")
```

---

## Parametres

| Parametre | Type | Obligatoire | Description |
|---|---|---|---|
| `format` | string | Non | Format de sortie: "table", "liste", "json" (defaut: "table") |
| `categorie` | string | Non | Filtrer par categorie: "explorer", "valider", "analyser", "corriger" (defaut: "toutes") |
| `champs` | string | Non | Champs a retourner (defaut: "tous") |

---

## Resultat

### Format table (defaut)

```markdown
| Outil | Categorie | Description | Version |
|---|---|---|---|
| lister-dossiers | Explorer | Lister les dossiers d'un chemin | 0.1.0 |
| lister-fichiers | Explorer | Lister les fichiers d'un chemin | 0.1.0 |
| lister-fonctions | Explorer | Lister les fonctions d'un fichier | 0.1.0 |
| lister-appels | Explorer | Lister les appels de fonctions | 0.1.0 |
| lister-agents | Explorer | Lister les agents avec leurs infos | 0.1.0-beta |
| lister-outils | Explorer | Lister les outils partages | 0.1.0-beta |
| valider-liens | Valider | Verifier les liens | 0.1.0 |
| valider-nommage | Valider | Verifier le nommage | 0.1.0 |
| valider-conventions | Valider | Verifier les conventions | 0.1.0 |
| analyser-structure | Analyser | Analyser la structure | 0.1.0 |
| analyser-dependances | Analyser | Analyser les dependances | 0.1.0 |
| corriger-liens | Corriger | Corriger les liens | 0.1.0 |
| corriger-nommage | Corriger | Corriger le nommage | 0.1.0 |
```

### Format liste

```markdown
- **lister-dossiers** (Explorer) : Lister les dossiers [0.1.0]
- **lister-fichiers** (Explorer) : Lister les fichiers [0.1.0]
- **lister-fonctions** (Explorer) : Lister les fonctions [0.1.0]
- **lister-appels** (Explorer) : Lister les appels [0.1.0]
- **lister-agents** (Explorer) : Lister les agents [0.1.0-beta]
- **lister-outils** (Explorer) : Lister les outils [0.1.0-beta]
- **valider-liens** (Valider) : Verifier les liens [0.1.0]
- **valider-nommage** (Valider) : Verifier le nommage [0.1.0]
- **valider-conventions** (Valider) : Verifier les conventions [0.1.0]
- **analyser-structure** (Analyser) : Analyser la structure [0.1.0]
- **analyser-dependances** (Analyser) : Analyser les dependances [0.1.0]
- **corriger-liens** (Corriger) : Corriger les liens [0.1.0]
- **corriger-nommage** (Corriger) : Corriger le nommage [0.1.0]
```

### Format JSON

```json
[
  {"nom": "lister-dossiers", "categorie": "Explorer", "description": "Lister les dossiers", "version": "0.1.0"},
  {"nom": "lister-fichiers", "categorie": "Explorer", "description": "Lister les fichiers", "version": "0.1.0"},
  {"nom": "lister-fonctions", "categorie": "Explorer", "description": "Lister les fonctions", "version": "0.1.0"},
  {"nom": "lister-appels", "categorie": "Explorer", "description": "Lister les appels", "version": "0.1.0"},
  {"nom": "lister-agents", "categorie": "Explorer", "description": "Lister les agents", "version": "0.1.0-beta"},
  {"nom": "lister-outils", "categorie": "Explorer", "description": "Lister les outils", "version": "0.1.0-beta"},
  {"nom": "valider-liens", "categorie": "Valider", "description": "Verifier les liens", "version": "0.1.0"},
  {"nom": "valider-nommage", "categorie": "Valider", "description": "Verifier le nommage", "version": "0.1.0"},
  {"nom": "valider-conventions", "categorie": "Valider", "description": "Verifier les conventions", "version": "0.1.0"},
  {"nom": "analyser-structure", "categorie": "Analyser", "description": "Analyser la structure", "version": "0.1.0"},
  {"nom": "analyser-dependances", "categorie": "Analyser", "description": "Analyser les dependances", "version": "0.1.0"},
  {"nom": "corriger-liens", "categorie": "Corriger", "description": "Corriger les liens", "version": "0.1.0"},
  {"nom": "corriger-nommage", "categorie": "Corriger", "description": "Corriger le nommage", "version": "0.1.0"}
]
```

---

## Exemples

### Exemple 1 -- Lister tous les outils

```
lister-outils()
```

**Resultat** : Liste complete de tous les outils.

### Exemple 2 -- Lister les outils par categorie

```
lister-outils(categorie="explorer")
```

**Resultat** : Uniquement les outils de la categorie Explorer.

### Exemple 3 -- Lister avec champs specifiques

```
lister-outils(champs="nom,description")
```

**Resultat** : Uniquement les noms et descriptions.

---

## Implementation

### Comment ca fonctionne

1. Lire `cerveau-projet/agents/tools/index-tools.md`
2. Extraire la table des outils
3. Formater selon le parametre `format`
4. Appliquer le filtre categorie si specifie
5. Retourner le resultat

### Ce que fait cet outil

| Capacite | Description |
|---|---|
| Format table/liste/JSON | Choisissez le format de sortie |
| Filtre par categorie | Recuperez uniquement les outils d'une categorie |
| Optimise | Concus pour nos agents et nos projets |

---

## Dependances

- `cerveau-projet/agents/tools/index-tools.md` -- source de donnees

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels, corrections, promotion |

---

## Notes

- Cet outil complete lister-agents
- Il est concu pour evoluer avec nos besoins
- Chaque agent peut l'ameliorer selon ses besoins
- Il est partage entre tous les agents

---

