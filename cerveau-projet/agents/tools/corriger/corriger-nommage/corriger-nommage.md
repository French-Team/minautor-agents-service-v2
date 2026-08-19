---
identite:
  type: outil
  appartient_a: commun
  commun: true
  combos:
    - combo-corriger-fichier
    - combos-corriger-non-ascii
---
# corriger-nommage

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** corriger
**Chemin :** `agents/tools/corriger/corriger-nommage/`
**Proprietaire :** Buffy (outil partage)

---

## Objectif

Corriger automatiquement le nommage des fichiers et dossiers.

---

## Utilisation

### CLI Python (version 0.2.0-py)

```
python3 corriger-nommage.py --type <protocole|agent|outil|convention> [OPTIONS] <fichier>

Options :
  --type        Type de fichier (obligatoire)
  --dry-run     Simuler sans modifier
  --verbose     Afficher les details
  --version     Afficher la version
```

### API (version originale)

```
corriger-nommage(chemin=".", convention="kebab-case", dry-run=false)
```

---

## Parametres

| Parametre | Type | Obligatoire | Description |
|---|---|---|---|
| `chemin` | string | Oui | Chemin du dossier a corriger |
| `convention` | string | Non | Convention de nommage (defaut: "kebab-case") |
| `dry-run` | boolean | Non | Si true, simule sans corriger (defaut: false) |

---

## Resultat

Retourne un rapport de correction.

```markdown
## Resultat

### Fichiers renommes
- Buffy.md -> buffy.md
- IndexCerveau.md -> index-cerveau.md

### Fichiers non renommes
- fichier-special.md -> Convention non applicable

### Statistiques
- Fichiers analyses : 20
- Renommes : 2
- Non renommes : 1
```

---

## Exemples

### Exemple 1 -- Simuler les corrections

```
corriger-nommage(chemin=".", dry-run=true)
```

**Resultat** :
- 2 fichiers seraient renommes

### Exemple 2 -- Corriger automatiquement

```
corriger-nommage(chemin=".", convention="kebab-case")
```

**Resultat** :
- 2 fichiers renommes avec succes

---

## Dependances

- `valider-nommage` -- Pour identifier les fichiers mal nommes
- `lister-fichiers` -- Pour trouver les fichiers a corriger
- `lister-dossiers` -- Pour trouver les dossiers a corriger
- `convention-renommage.md` -- Pour connaitre les regles de nommage

---

## Implementation

### Dans le contexte du cerveau-projet

1. Utiliser `valider-nommage` pour identifier les fichiers mal nommes
2. Pour chaque fichier :
   - Appliquer la convention de nommage
   - Renommer le fichier
   - Mettre a jour les liens qui referencent ce fichier

### Algorithme de correction

```
1. Extraire le nom du fichier
2. Appliquer la convention :
   - kebab-case : minuscules, tirets
   - snake_case : minuscules, underscores
3. Si le nom change -> renommer
4. Mettre a jour les liens
```

---

## Notes

- Cet outil est essentiel pour maintenir la coherence
- Utiliser `dry-run=true` avant de corriger
- Les renommages peuvent casser les liens

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0-py | 2026-08-07 | Version Python creee (meme dossier, meme nom, base sur outil-template.py) |
| 0.1.0 | 2026-08-05 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter, VERSION 0.2.0, statut prepare |
