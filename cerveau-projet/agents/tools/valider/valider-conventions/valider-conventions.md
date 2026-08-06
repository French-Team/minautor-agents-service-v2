# Outil -- Valider les Conventions

**Categorie** : Valider
**Version :** 0.2.0
**Statut :** prepare

---

## Objectif

Verifier que les fichiers respectent les conventions du cerveau-projet.

---

## Utilisation

```
valider-conventions(chemin=".", types="all")
```

---

## Parametres

| Parametre | Type | Obligatoire | Description |
|---|---|---|---|
| `chemin` | string | Oui | Chemin du dossier a valider |
| `types` | string | Non | Types de conventions: "all", "structures", "renommage", "liens", "protocoles" (defaut: "all") |

---

## Resultat

Retourne un rapport de validation des conventions.

```markdown
## Resultat

### Conventions respectees
- convention-structures.md -> OK
- convention-renommage.md -> OK
- convention-liens.md -> OK

### Conventions violees
- Fichier sans en-tete YAML
- Lien relatif incorrect

### Statistiques
- Total fichiers : 25
- Conformes : 22
- Non conformes : 3
```

---

## Exemples

### Exemple 1 -- Valider toutes les conventions

```
valider-conventions(chemin=".")
```

**Resultat** :
- 25 fichiers analyses
- 22 conformes
- 3 non conformes

### Exemple 2 -- Valider uniquement les structures

```
valider-conventions(chemin=".", types="structures")
```

**Resultat** :
- Tous les fichiers respectent la structure

---

## Dependances

- `lister-fichiers` -- Pour trouver les fichiers a valider
- `convention-structures.md` -- Pour connaitre la structure attendue
- `convention-renommage.md` -- Pour connaitre les regles de nommage
- `convention-liens.md` -- Pour connaitre les regles de liens
- `convention-protocoles.md` -- Pour connaitre les regles de protocoles

---

## Implementation

### Dans le contexte du cerveau-projet

1. Lire les conventions applicables
2. Analyser chaque fichier
3. Comparer avec les regles
4. Signaler les ecarts

---

## Notes

- Cet outil est essentiel pour la qualite du cerveau
- Les conventions sont documentees dans `conventions/`
- Utile avant chaque mise a jour importante

---

