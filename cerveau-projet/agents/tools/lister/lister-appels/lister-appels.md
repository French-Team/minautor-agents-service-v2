---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# lister-appels

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** lister
**Chemin :** `agents/tools/lister/lister-appels/`
**Proprietaire :** Atlas (outil partage)

---

## Objectif

Lister tous les appels de fonctions dans un fichier donne.

---

## Utilisation

Version Python (recommandee) :

```bash
python3 lister-appels.py [FICHIER] [OPTIONS]
```

### Options

| Option | Description |
|---|---|
| `FICHIER` | Fichier a analyser (defaut: detection auto dans le dossier) |
| `--unique, -u` | Afficher les appels sans doublons |
| `--verbose, -v` | Afficher les details d'execution |
| `--version` | Afficher la version |
| `--aide, -h` | Afficher l'aide |

### Exemples

```bash
python3 lister-appels.py src/main.py
python3 lister-appels.py --unique src/main.py
```

Version bash equivalente : `lister-appels.sh`.

---

## Resultat

Retourne une liste d'appels de fonctions.

```markdown
## Resultat

### Appels trouves
- Ligne 15: `autreFonction(param1, param2)`
- Ligne 23: `utilitaire.format(data)`
- Ligne 45: `this.methodePrivee()`
```

---

## Exemples

### Exemple 1 -- Lister tous les appels

```
lister-appels(fichier="src/main.ts")
```

**Resultat** :
- Ligne 10: `init()`
- Ligne 15: `processData(data)`
- Ligne 20: `save()`

### Exemple 2 -- Lister les appels d'une fonction specifique

```
lister-appels(fichier="src/main.ts", fonction="processData")
```

**Resultat** :
- Ligne 15: `processData(data)` -- appel principal
- Ligne 45: `processData(transformedData)` -- appel recursif

---

## Dependances

- Aucune dependance externe
- Utilise l'analyse de syntaxe du langage cible

---

## Implementation

### Commande bash equivalent

```bash
# Pour les fichiers TypeScript/JavaScript
grep -n "fonction(" fichier.ts

# Pour les fichiers Python
grep -n "fonction(" fichier.py
```

### Implementation

1. Lire le fichier specifie
2. Analyser la syntaxe du langage
3. Extraire les appels de fonctions
4. Retourner la liste avec les positions

---

## Notes

- Cet outil est utile pour analyser les dependances
- Permet de tracer l'utilisation d'une fonction
- Utile pour le refactoring et la maintenance

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-05 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter, VERSION 0.2.0, statut prepare |
| 0.2.0-py | 2026-08-07 | Version Python creee (lister-appels.py), basee sur outil-template.py |
