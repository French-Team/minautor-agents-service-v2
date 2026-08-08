---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# corriger-liens

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** corriger
**Chemin :** `agents/tools/corriger/corriger-liens/`
**Proprietaire :** Buffy (outil partage)

---

## Objectif

Corriger automatiquement les liens casses dans les fichiers Markdown.

---

## Utilisation

### CLI Python (version 0.2.0-py)

```
python3 corriger-liens.py [OPTIONS] <fichier>

Options :
  --dry-run    Simuler sans modifier
  --verbose    Afficher les details
  --version    Afficher la version
```

### API (version originale)

```
corriger-liens(chemin=".", mode="auto", dry-run=false)
```

---

## Parametres

| Parametre | Type | Obligatoire | Description |
|---|---|---|---|
| `chemin` | string | Oui | Chemin du dossier a corriger |
| `mode` | string | Non | Mode: "auto" (automatique), "manual" (manuel) (defaut: "auto") |
| `dry-run` | boolean | Non | Si true, simule sans corriger (defaut: false) |

---

## Resultat

Retourne un rapport de correction.

```markdown
## Resultat

### Liens corriges
- [ancien.md](ancien.md) -> [nouveau.md](nouveau.md)
- dossier/ -> dossier/existant/

### Liens non corriges
- [perdu.md](perdu.md) -> Aucune correspondance trouvee

### Statistiques
- Liens analyses : 15
- Corriges : 3
- Non corriges : 1
```

---

## Exemples

### Exemple 1 -- Simuler les corrections

```
corriger-liens(chemin=".", dry-run=true)
```

**Resultat** :
- 3 liens seraient corriges

### Exemple 2 -- Corriger automatiquement

```
corriger-liens(chemin=".", mode="auto")
```

**Resultat** :
- 3 liens corriges avec succes

---

## Dependances

- `valider-liens` -- Pour identifier les liens casses
- `lister-fichiers` -- Pour trouver les fichiers a corriger
- `lister-dossiers` -- Pour trouver les dossiers disponibles

---

## Implementation

### Dans le contexte du cerveau-projet

1. Utiliser `valider-liens` pour identifier les liens casses
2. Pour chaque lien casse :
   - Chercher un fichier avec un nom similaire
   - Verifier si le fichier existe
   - Si oui, corriger le lien
   - Si non, signaler l'erreur

### Algorithme de correction

```
1. Extraire le chemin cible du lien
2. Si le chemin existe -> OK
3. Sinon :
   a. Chercher dans le dossier parent
   b. Chercher par nom similaire
   c. Si trouve -> corriger
   d. Sinon -> signaler
```

---

## Notes

- Cet outil est essentiel pour la maintenance
- Utiliser `dry-run=true` avant de corriger
- Les corrections sont irreversibles

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0-py | 2026-08-07 | Version Python creee (meme dossier, meme nom, base sur outil-template.py) |
| 0.1.0 | 2026-08-05 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter, VERSION 0.2.0, statut prepare |
