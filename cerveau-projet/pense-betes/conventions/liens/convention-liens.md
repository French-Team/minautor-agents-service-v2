# Convention Liens

## Objectif

Standardiser la création de liens pour garantir :
- Une navigation cohérente dans le cerveau
- Une maintenance facilitée
- Une validation automatisable

---

## Types de liens

| Type | Description | Syntaxe |
|---|---|---|
| **Internes** | Liens vers des fichiers du cerveau-projet | `[texte](chemin/fichier.md)` |
| **Relatifs** | Liens utilisant `../` pour remonter | `[parent](../chemin/parent.md)` |
| **Dans tableaux** | Liens intégrés dans les tableaux | `[Nom](chemin) \| Description \| Statut` |

---

## Emplacements des liens

| Emplacement | Obligatoire | Usage |
|---|---|---|
| **Header** | [OK] | Navigation |
| **Sections** | Optionnel | Références |
| **Footer** | Optionnel | Ressources connexes |

---

## Patterns de navigation

### Hiérarchie ascendante

| Depuis | Vers | Syntaxe |
|---|---|---|
| `dossier/fichier.md` | `dossier/index.md` | `[index](index.md)` |
| `dossier/fichier.md` | `parent/index.md` | `[parent](../index.md)` |
| `dossier/fichier.md` | `racine/index.md` | `[racine](../../index.md)` |

### Hiérarchie descendante

| Depuis | Vers | Syntaxe |
|---|---|---|
| `index.md` | `dossier/fichier.md` | `[fichier](dossier/fichier.md)` |
| `index.md` | `sous-dossier/` | `[sous-dossier/](sous-dossier/index.md)` |

### Navigation latérale

| Depuis | Vers | Syntaxe |
|---|---|---|
| `frere-a.md` | `frere-b.md` | `[Frère B](../frere-b/frere-b.md)` |

---

## Format des liens

| Format | Syntaxe |
|---|---|
| **Standard** | `[texte descriptif](chemin/vers/fichier.md)` |
| **Avec ancre** | `[texte](fichier.md#section)` |
| **Dans tableaux** | `[Nom du fichier](chemin/fichier.md) \| Description courte \| Statut` |

---

## Règles de validation

| Critère | Obligatoire | Vérification |
|---|---|---|
| Fichier cible existe | [OK] | Test d'existence |
| Texte descriptif | [OK] | Lecture humaine |
| Chemin relatif | [OK] | Pas de `/` au début |
| Cohérence navigation | [OK] | Parent <-> Enfant |

---

## Anti-patterns

### [NON] Ne pas faire

```markdown
# Absolu (jamais)
[Lien](/chemin/absolu/fichier.md)

# Texte non descriptif
[Lien](fichier.md)
[ici](fichier.md)
[Cliquez ici](fichier.md)

# Liens cassés
[Lien](fichier-inexistant.md)
```

### [OK] Bonnes pratiques

```markdown
# Relatif (toujours)
[Lien relatif](../parent/fichier.md)

# Texte descriptif
[Convention de renommage](../../conventions/renommage/convention-renommage.md)
[Index des règles](../regles-immuables/index-regles-immuables.md)
```

---

## Maintenance des liens

| Action | Étapes |
|---|---|
| **Déplacement** | Mettre à jour tous les liens -> Vérifier index parent -> Valider |
| **Renommage** | Identifier liens -> Mettre à jour -> Vérifier cohérence |
| **Suppression** | Identifier liens -> Supprimer/remplacer -> Mettre à jour index |

---

## Conventions associées

| Convention | Usage |
|---|---|
| [Renommage](../renommage/convention-renommage.md) | Nommage des fichiers |
| [Structures](../structures/convention-structures.md) | Organisation des dossiers |
| [Protocoles](../protocoles/convention-protocoles.md) | Création de protocoles |

---

## Navigation

- **Parent** : [index-conventions.md](../index-conventions.md)
- **Sœurs** : [renommage/](../renommage/convention-renommage.md), [structures/](../structures/index-structures.md), [protocoles/](../protocoles/index-protocoles.md)
- **Règles** : [regles-immuables/](../../regles-immuables/index-regles-immuables.md)
