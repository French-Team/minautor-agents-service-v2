# lister-fonctions

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** lister
**Chemin :** `agents/tools/lister/lister-fonctions/`
**Proprietaire :** Atlas (outil partage)

---

## Objectif

Lister toutes les fonctions d'un fichier donne.

---

## Utilisation

Version Python (recommandee) :

```bash
python3 lister-fonctions.py [FICHIER] [OPTIONS]
```

### Options

| Option | Description |
|---|---|
| `FICHIER` | Fichier a analyser (defaut: detection auto dans le dossier) |
| `--type` | Type de fonctions: "auto", "bash", "python" (defaut: "auto") |
| `--version` | Afficher la version |
| `--aide, -h` | Afficher l'aide |

### Exemples

```bash
python3 lister-fonctions.py script.sh
python3 lister-fonctions.py --type bash script.sh
```

Version bash equivalente : `lister-fonctions.sh`.

---

## Resultat

Retourne une liste de fonctions avec leurs signatures.

```markdown
## Resultat

### Fonctions exportees
- `functionA(param1: type, param2: type): returnType`
- `functionB(): void`

### Fonctions privees
- `helperFunction(): string`
```

---

## Exemples

### Exemple 1 -- Lister toutes les fonctions

```
lister-fonctions(fichier="agents/tools/lister/lister-fichiers/lister-fichiers.md")
```

**Resultat** :
- Fonctions trouvees dans le fichier Markdown (sections)

### Exemple 2 -- Lister les fonctions exportees

```
lister-fonctions(fichier="src/utils.ts", type="export")
```

---

## Dependances

- Aucune dependance externe
- Utilise l'analyse de syntaxe du langage cible

---

## Implementation

### Commande bash equivalent

```bash
# Pour les fichiers TypeScript/JavaScript
grep -n "function\|const.*=\|export" fichier.ts

# Pour les fichiers Python
grep -n "def \|class " fichier.py
```

### Implementation

1. Lire le fichier specifie
2. Analyser la syntaxe du langage
3. Extraire les declarations de fonctions
4. Retourner la liste avec les signatures

---

## Notes

- Cet outil est utile pour comprendre la structure d'un fichier
- Fonctionne avec differents langages (TS, JS, Python, etc.)
- Peut etre utilise pour generer de la documentation

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-05 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter, VERSION 0.2.0, statut prepare |
| 0.2.0-py | 2026-08-07 | Version Python creee (lister-fonctions.py), basee sur outil-template.py |
