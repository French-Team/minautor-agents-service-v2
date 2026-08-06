# Protocole Immuable — Boîte à Outils

> **Ce protocole est immuable.** Les agents doivent CONSTRUIRE leurs outils, pas juste les utiliser.

---

## Principe Fondamental

> **Ne jamais utiliser une commande sans la transformer en outil réutilisable.**

| Problème | Solution |
|---|---|
| Chaque agent recrée les mêmes commandes | Outils réutilisables |
| Les erreurs se répètent | Outils qui vérifient |
| Pas de traçabilité | Outils historisés |

---

## Structure

```
agents/tools/[catégorie]/[nom-outil]/
|-- [nom-outil].md        <- documentation
|-- [nom-outil].sh        <- implémentation
``-- spec/                 <- spécifications
```

---

## Règles

### Règle 1 — Chaque outil est documenté

```markdown
# [Nom de l'outil]
## Objectif
## Utilisation
## Paramètres
## Dépendances
```

### Règle 2 — Chaque outil est testé

```
Créer -> Tester en --dry-run -> Valider le résultat -> Appliquer
```

**Règle obligatoire** :
- TOUJOURS tester avec --dry-run d'abord
- Vérifier que le résultat est acceptable
- NE JAMAIS appliquer sans vérification
- Si problème -> corriger l'outil avant d'appliquer

### Règle 3 — Chaque outil est partagé

```
Créer dans agents/tools/ -> Documenter dans index-tools.md -> Accessible à tous
```

### Règle 4 — Pas de références aux outils tiers

```
JAMAIS : read_files, list_directory, glob, code_searcher, write_file, str_replace
TOUJOURS : Décrire CE QUE L'OUTIL FAIT
```

### Règle 5 — Chaque fichier a un rôle unique

| Type | Rôle | JAMAIS |
|---|---|---|
| `index-*.md` | Navigation | Suivi, TODO |
| `convention-*.md` | Conventions | Suivi |
| `protocole-*.md` | Processus | Historique |
| `corrections.md` | Leçons | Navigation |

### Règle 6 — Chaque outil est assigné à un agent

> **Un outil est assigné à l'agent dont les MISSIONS utilisent cet outil.**

Un outil qui n'est assigné à personne risque de n'être jamais utilisé. Pour assigner un outil, se poser les questions dans l'ordre :

```
1. Cet outil est-il utilisé dans une MISSION existante ?
2. Quelle est la NATURE de l'outil ? (structure / fonctionnalité / exploration...)
3. Quel agent est responsable de cette nature de tâche ?
4. Si aucun agent ne l'utilise -> outil de support -> Buffy (gestion du cerveau)
```

**Répartition par nature** :

| Nature de l'outil | Agent responsable | Exemples |
|---|---|---|
| Coordination, activation | Cerberus | `modifier-agents-md`, `lister-agents` |
| Contrôle, analyse, structure du cerveau | Buffy | `valider-*`, `corriger-*`, `verifier-documents-manquants` |
| Exploration | Atlas | `lister-*`, `rechercher-*` |
| Statuts et validation | Janus | `lister-statuts`, `changer-statut`, `valider-ebauche` |
| Construction d'outils | Vulcain | `verifier-systeme`, `outil-template`, `corriger-accents` |
| Tests fonctionnels | Morpheus | `template-test`, `protection-*` |

> **Règle** : Chaque outil créé doit être assigné à un agent dans sa carte de décision avant d'être référencé dans l'index.

---

## Processus de création

> **RÈGLE OBLIGATOIRE** : Toute création d'outil passe par le **outil-template** (`agents/tools/outil-template/`).

```
1. Identifier le besoin (commande fréquente)
2. Concevoir l'outil (objectif, paramètres)
3. Copier le outil-template vers agents/tools/[catégorie]/[nom-outil]/
4. Remplacer les placeholders [nom-outil] dans le script et la documentation
5. Développer la logique dans [nom-outil].sh
6. Compléter la documentation dans [nom-outil].md
7. Tester en --dry-run
8. Ajouter dans index-tools.md
```

**Pourquoi le outil-template ?**

| Sans template | Avec outil-template |
|---|---|
| Chaque outil a une structure différente | Structure standard garantie |
| Le --dry-run est parfois oublié | --dry-run intégré par défaut |
| Documentation inégale | Sections standard obligatoires |
| Oublis de référencement | Checklist intégrée au modèle |

---

## Utilisation

```
1. Chercher dans index-tools.md
2. Lire la documentation de l'outil
3. Exécuter avec les bons paramètres
4. Vérifier le résultat
```

---

## Boucle de rétroaction

```
Utiliser -> Si problème -> Corriger
         -> Si manque -> Créer
         -> Si incomplet -> Compléter
```

---

## Liens

- **Index** : `agents/tools/index-tools.md`
- **Outil-template** : `agents/tools/outil-template/outil-template.md` — modèle standard de création
- **Classeur** : `classeur-variables/index-classeur.md` (pour stocker les résultats)
- **Règles** : `regles-veracite.md` — ne jamais mentir/supposer
