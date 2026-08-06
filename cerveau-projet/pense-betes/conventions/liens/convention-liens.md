# Convention Liens

## Objectif

Standardiser la creation de liens pour garantir :
- Une navigation coherente dans le cerveau
- Une maintenance facilitee
- Une validation automatisable

---

## Types de liens

| Type | Description | Syntaxe |
|---|---|---|
| **Internes** | Liens vers des fichiers du cerveau-projet | `[texte](chemin/fichier.md)` |
| **Relatifs** | Liens utilisant `../` pour remonter | `[parent](../chemin/parent.md)` |
| **Dans tableaux** | Liens integres dans les tableaux | `[Nom](chemin) \| Description \| Statut` |

---

## Emplacements des liens

| Emplacement | Obligatoire | Usage |
|---|---|---|
| **Header** | [OK] | Navigation |
| **Sections** | Optionnel | References |
| **Footer** | Optionnel | Ressources connexes |

---

## Patterns de navigation

### Hierarchie ascendante

| Depuis | Vers | Syntaxe |
|---|---|---|
| `dossier/fichier.md` | `dossier/index.md` | `[index](index.md)` |
| `dossier/fichier.md` | `parent/index.md` | `[parent](../index.md)` |
| `dossier/fichier.md` | `racine/index.md` | `[racine](../../index.md)` |

### Hierarchie descendante

| Depuis | Vers | Syntaxe |
|---|---|---|
| `index.md` | `dossier/fichier.md` | `[fichier](dossier/fichier.md)` |
| `index.md` | `sous-dossier/` | `[sous-dossier/](sous-dossier/index.md)` |

### Navigation laterale

| Depuis | Vers | Syntaxe |
|---|---|---|
| `frere-a.md` | `frere-b.md` | `[Frere B](../frere-b/frere-b.md)` |

---

## Format des liens

| Format | Syntaxe |
|---|---|
| **Standard** | `[texte descriptif](chemin/vers/fichier.md)` |
| **Avec ancre** | `[texte](fichier.md#section)` |
| **Dans tableaux** | `[Nom du fichier](chemin/fichier.md) \| Description courte \| Statut` |

---

## Regles de validation

| Critere | Obligatoire | Verification |
|---|---|---|
| Fichier cible existe | [OK] | Test d'existence |
| Texte descriptif | [OK] | Lecture humaine |
| Chemin relatif | [OK] | Pas de `/` au debut |
| Coherence navigation | [OK] | Parent <-> Enfant |

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

# Liens casses
[Lien](fichier-inexistant.md)
```

### [OK] Bonnes pratiques

```markdown
# Relatif (toujours)
[Lien relatif](../parent/fichier.md)

# Texte descriptif
[Convention de renommage](../../conventions/renommage/convention-renommage.md)
[Index des regles](../regles-immuables/index-regles-immuables.md)
```

---

## Maintenance des liens

| Action | Etapes |
|---|---|
| **Deplacement** | Mettre a jour tous les liens -> Verifier index parent -> Valider |
| **Renommage** | Identifier liens -> Mettre a jour -> Verifier coherence |
| **Suppression** | Identifier liens -> Supprimer/remplacer -> Mettre a jour index |

---

## Conventions associees

| Convention | Usage |
|---|---|
| [Renommage](../renommage/convention-renommage.md) | Nommage des fichiers |
| [Structures](../structures/convention-structures.md) | Organisation des dossiers |
| [Protocoles](../protocoles/convention-protocoles.md) | Creation de protocoles |

---

## Navigation

- **Parent** : [index-conventions.md](../index-conventions.md)
- **Soeurs** : [renommage/](../renommage/convention-renommage.md), [structures/](../structures/index-structures.md), [protocoles/](../protocoles/index-protocoles.md)
- **Regles** : [regles-immuables/](../../regles-immuables/index-regles-immuables.md)
