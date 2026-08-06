# Convention de Renommage

## Principe

Chaque nom de fichier contient 3 références pour être **recherchable**, **identifiable** et **traçable** :

1. **ID** — numéro de création (fixe, séquentiel, 3 chiffres)
2. **Class** — numéro de classification (évolue, 2 chiffres, progression RVAV)
3. **Statut** — état actuel (ebauche | prepare | dev | test | valide)

## Pattern des fichiers de contenu — sous-parties (L5+)

`[type]-[thème].[id].[class].[statut].md`

- **type** : `spec` | `todo` | `liens`
- **thème** : nom descriptif, recherche
- **id** : AAA (001, 002, 003...)
- **class** : CC (01, 02, 03...)
- **statut** : ebauche | prepare | dev | test | valide

## Pattern des fichiers de contenu — plateforme (L4)

`[thème].[id].[class].[statut].md`

- **thème** : nom descriptif, recherche (sans prefixe de type)
- Le pense-bête est la plateforme -> il porte le thème directement

### Exemple de cycle de vie

```
protocole-composition.001.01.ebauche.md      <- création
protocole-composition.001.02.dev.md          <- développement
protocole-composition.001.03.test.md          <- test RVAV
protocole-composition.001.04.valide.md        <- validé
protocole-composition.001.05.ebauche.md      <- <- erreur détectée -> boucle de rétroaction
```

## Pattern des fichiers méta

Les fichiers méta (index, templates, conventions, règles) n'ont pas d'ID/class/statut — ils sont des référentiels :

- **Index / plateforme** : `index-[catégorie].md`
- **Template** : `[type]-template.md`
- **Convention** : `convention-[thème].md`
- **Règle immuable** : `regles-[scope]-[contexte].md`
## Référence croisée

- Recherche par thème -> le thème est au début du nom
- Recherche par type -> le type est le préfixe
- Recherche par ID -> `[id].[class]` permet de tracer l'historique
- La boucle RVAV modifie le `class` et le `statut`, jamais l'`id`
