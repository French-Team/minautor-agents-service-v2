# Règle Immuable — Bannissement des Emojis et Utilisation de ASCII

> **Cette règle est IMMUABLE.** Elle s'applique à tout fichier du cerveau-projet.

---

## Principe Fondamental
---

## Pourquoi ?

| Problème | Solution |
|---|---|
| Incompatibilité avec certains outils | ASCII universel |
| Difficulté de recherche/grep | Caractères standards |
| Problèmes d'encodage | ASCII sans ambiguïté |
| Manque de professionnalisme | Convention technique stricte |
| Difficulté de copier/coller | Caractères simples |

---

## Règles détaillées

### Règle 1 — Aucun emoji

Tout type d'emoji est interdit :
- Emojis Unicode ( smiles, coeurs, flèches colorées, etc.)
- Emojis de transport (voitures, avions, etc.)
- Emojis de nourriture (pommes, pizzas, etc.)
- Emojis d'animaux (chiens, chats, etc.)
- Tout caractère Unicode hors ASCII étendu

### Règle 2 — Seuls les caractères ASCII sont autorisés

Les caractères autorisés sont :
- Lettres (a-z, A-Z)
- Chiffres (0-9)
- Ponctuation standard ASCII
- Symboles techniques ASCII

### Règle 3 — Symboles de remplacement

Pour remplacer les emojis, utiliser des symboles ASCII :

| Emoji interdit | Symbole ASCII de remplacement |
|---|---|
| Checkbox coche | `[x]` ou `[X]` |
| Checkbox vide | `[ ]` |
| Flèche droite | `->` ou `-->` |
| Flèche gauche | `<-` ou `<--` |
| Flèche double | `<->` ou `<-->` |
| Coeur | `<3` |
| Point d'exclamation | `!` ou `!!` |
| Point d'interrogation | `?` ou `??` |
| Etoile | `*` |
| Croix | `x` ou `X` |
| Check / OK | `[OK]` ou `OK` |
| Warning | `[WARNING]` ou `ATTENTION` |
| Erreur | `[ERROR]` ou `ERREUR` |

### Règle 4 — Tableaux

Dans les tableaux, utiliser des caractères ASCII :

```markdown
| Statut | Symbole |
|---|---|
| Complet | [OK] |
| En cours | [..] |
| Pas commence | [--] |
| Erreur | [!!] |
```

### Règle 5 — Listes

Dans les listes, utiliser des puces ASCII :

```markdown
- Element 1
- Element 2
  - Sous-element 2.1
  - Sous-element 2.2
* Element 3
```

---

## Exemples de remplacement

### Avant (interdit)

```markdown
# Ma section ✅

- Fait ✔️
- En cours 🔧
- Pas commence ⏳

| Status | Emoji |
|---|---|
| OK | 👍 |
| Error | ❌ |
```

### Apres (autorise)

```markdown
# Ma section [OK]

- Fait [x]
- En cours [..]
- Pas commence [--]

| Status | Symbole |
|---|---|
| OK | [OK] |
| Error | [!!] |
```

---

## Exceptions volontaires

**Par defaut : aucune exception.** Cette règle est absolue pour tous les fichiers du cerveau-projet.

Même dans les commentaires, les notes, les brouillons, les emojis sont interdits.

### Liste des exceptions volontaires

Seuls les fichiers ci-dessous contiennent **volontairement** des emojis ou caracteres non-ASCII. Ils sont marques d'un bandeau `EXCEPTION VOLONTAIRE` dans leur en-tete et ne doivent **jamais** etre purges :

| Fichier | Raison de l'exception |
|---|---|
| `cerveau-projet/agents/tools/corriger/corriger-emojis/dictionnaire-emojis.txt` | Dictionnaire emoji -> ASCII de `corriger-emojis`. Contient les emojis a traduire : c'est sa fonction. |
| `cerveau-projet/agents/tools/corriger/corriger-accents/dictionnaire-accents.txt` | Dictionnaire accent -> ASCII de `corriger-accents`. Contient les caracteres non-ASCII a traduire : c'est sa fonction. |
| `cerveau-projet/pense-betes/regles-immuables/general/regles-emojis-ascii.md` (lui-meme) | Exemples pedagogiques dans le bloc "Avant (interdit)" : montre ce qui est interdit. |

### Exception de dossier : `exemples/`

Le dossier `cerveau-projet/exemples/` est **exclu de la regle** : c'est une zone de test dediee aux outils. Ses fichiers contiennent **volontairement** des problemes (emojis, accents, erreurs, faux statuts) pour tester et valider les outils de correction et de validation.

- **Ne jamais purger** ce dossier : il est fait pour contenir des erreurs.
- **Exclu automatiquement** par les outils de validation (`valider-conformite-ascii`, `rechercher-accents-sensibles`, `corriger-emojis`).
- Les fichiers de ce dossier ne necessitent **ni bandeau, ni declaration** dans le tableau ci-dessus : l'exclusion du dossier suffit.
- Lorsqu'un test est cree, il doit etre place dans ce dossier, jamais dans le reste du cerveau.

### Regles pour les exceptions

1. **Marquage obligatoire** : tout fichier exception doit avoir le bandeau `EXCEPTION VOLONTAIRE` en en-tete.
2. **Enregistrement obligatoire** : tout fichier exception doit etre declare dans ce tableau.
3. **Interdiction d'ajout** : il est interdit d'ajouter un fichier exception sans passer par ce tableau.
4. **Signalement par les outils** : les outils de validation (`valider-conformite-ascii`, `rechercher-accents-sensibles`, `corriger-emojis`) doivent exclure ces fichiers de leur detection.

---

## Validation

Avant de valider tout fichier, verifier :

- [ ] Aucun emoji Unicode present
- [ ] Tous les symboles sont ASCII
- [ ] Les checkboxes utilisent `[x]` et `[ ]`
- [ ] Les flèches utilisent `->` ou `<-`
- [ ] Les tableaux utilisent des caracteres ASCII

---

## Application

Cette regle s'applique a :
- Tous les fichiers `.md` du cerveau
- Tous les fichiers de configuration
- Tous les templates
- Toutes les conventions
- Toutes les regles
- Toutes les specs
- Tous les commentsaires de code

---

## Liens

- [regles-general-global.md](regles-general-global.md) — regles globales
- [regles-choisir-agent.md](regles-choisir-agent.md) — choisir le bon agent
- [regles-validation-rigoureuse.md](regles-validation-rigoureuse.md) — validation rigoureuse
- [convention-renommage.md](../../conventions/renommage/convention-renommage.md) — convention de renommage

---

## Navigation

- **Parent** : [index-regles-general.md](index-regles-general.md)
- **Regles** : [index-regles-immuables.md](../index-regles-immuables.md)
