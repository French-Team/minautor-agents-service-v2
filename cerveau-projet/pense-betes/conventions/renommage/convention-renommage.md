---
identite:
  type: convention
  appartient_a: commun
  commun: true
---
# Convention de Renommage

## REGLE FONDAMENTALE -- Aucun identifiant en mot seul

> **REGLE FONDAMENTALE (2026-08-08, decision utilisateur)** : aucun identifiant
> ne peut etre un MOT SEUL. Tout identifiant (champ YAML, cle JSON, nom de
> fichier, nom de dossier, nom d'outil) doit etre COMPOSE de 2+ mots relies par
> un tiret ou un underscore.

**Pourquoi** : a mesure que le cerveau grandit (agents, outils, fichiers,
parcours, combos), un identifiant en mot seul devient impossible a retrouver
et a distinguer (ex: `nom` de qui ? `role` de quoi ? `lire` quoi ?).

**Champs YAML d'identification** (fiches, frontmatter) :

| Interdit (mot seul) | Obligatoire (compose) |
|---|---|
| `nom:` | `nom-agent:` |
| `role:` | `role-agent:` |
| `statut:` | `statut-<agent>:` (ex: `statut-cerberus`) |
| `version:` | reste `version:` (mot technique normalise, voir exceptions) |

**Cles JSON** (parcours, combos, catalogues) : les cles structurantes comme
`nom`, `type`, `question`, `suivant` sont des MOTS TECHNIQUES du format
(normalises par la spec) -- la regle s'applique aux cles d'IDENTIFICATION
(pas aux mots techniques du schema).

**Noms de fichiers, dossiers et outils** : toujours composes.

| Interdit | Obligatoire |
|---|---|
| `lire.sh` | `lire-fichier.sh` |
| `valider.md` | `valider-nommage.md` |
| `agents/role/` | `agents/controleur/` ou `agents/verificateur/` |

**Exceptions** : les mots techniques normalises par une spec ou un schema
(`version`, `type`, `id`, `class`, `statut` en nom de segment de fichier)
restent autorises -- la regle vise les identifiants SEMANTIQUES, pas les
segments techniques du format.

**Verification** : `valider-nommage` (mode cles) detecte les champs
YAML/JSON en mot seul (`nom:`, `role:`, `statut:`).

---

## Principe

Chaque nom de fichier contient 3 references pour etre **recherchable**, **identifiable** et **tracable** :

1. **ID** -- numero de creation (fixe, sequentiel, 3 chiffres)
2. **Class** -- numero de classification (evolue, 2 chiffres, progression RVAV)
3. **Statut** -- etat actuel (ebauche | prepare | dev | test | valide)

## Pattern des fichiers de contenu -- sous-parties (L5+)

`[type]-[theme].[id].[class].[statut].md`

- **type** : `spec` | `todo` | `liens`
- **theme** : nom descriptif, recherche
- **id** : AAA (001, 002, 003...)
- **class** : CC (01, 02, 03...)
- **statut** : ebauche | prepare | dev | test | valide

## Pattern des fichiers de contenu -- plateforme (L4)

`[theme].[id].[class].[statut].md`

- **theme** : nom descriptif, recherche (sans prefixe de type)
- Le pense-bete est la plateforme -> il porte le theme directement

### Exemple de cycle de vie

```
protocole-composition.001.01.ebauche.md      <- creation
protocole-composition.001.02.dev.md          <- developpement
protocole-composition.001.03.test.md          <- test RVAV
protocole-composition.001.04.valide.md        <- valide
protocole-composition.001.05.ebauche.md      <- <- erreur detectee -> boucle de retroaction
```

## Pattern des fichiers meta

Les fichiers meta (index, templates, conventions, regles) n'ont pas d'ID/class/statut -- ils sont des referentiels :

- **Index / plateforme** : `index-[categorie].md`
- **Template** : `[type]-template.md`
- **Convention** : `convention-[theme].md`
- **Regle immuable** : `regles-[scope]-[contexte].md`
## Pattern des outils (tools/)

`[dossier]-[action].sh` et `[dossier]-[action].md`

**REGLE IMMuable** : le nom de l'outil DOIT commencer par le prefixe du dossier parent (sauf generateurs, combos, tester).

- **Dossier `lire/`** : `lire-fichier`, `lire-lignes`, `lire-frontmatter`
- **Dossier `rechercher/`** : `rechercher-fichier`, `rechercher-texte`, `rechercher-extension-fichier`
- **Dossier `corriger/`** : `corriger-emojis`, `corriger-liens`, `corriger-dictionnaire-accents`
- **Dossier `creer/`** : `creer-fichier`, `creer-remplir-pense-bete`
- **Dossier `mettre-a-jour/`** : `mettre-a-jour-readme`
- **Dossier `activer/`** : `activer-agent-principal`
- **Dossier `remplacer/`** : `remplacer-texte`

**Exclusions** : les dossiers `generateurs/`, `combos/`, `tester/` ne suivent pas cette regle.

**Verification** : utiliser le script `valider-nommage` pour detecter les violations.

## Reference croisee

- Recherche par theme -> le theme est au debut du nom
- Recherche par type -> le type est le prefixe
- Recherche par ID -> `[id].[class]` permet de tracer l'historique
- La boucle RVAV modifie le `class` et le `statut`, jamais l'`id`
