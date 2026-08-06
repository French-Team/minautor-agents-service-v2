# Outil -- Corriger les Liens

**Categorie** : Corriger
**Version** : v0.1.0
**Statut** : initial

---

## Objectif

Corriger automatiquement les liens casses dans les fichiers Markdown.

---

## Utilisation

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

