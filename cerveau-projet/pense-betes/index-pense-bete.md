# Index — Pense-bêtes
## Navigation

### Sous-catégories

| Dossier | Description | Plateforme |
|---|---|---|
| [conventions/](conventions/index-conventions.md) | Renommage, structures, liens | index-conventions.md |
| [specs/](specs/index-spec.md) | Définitions techniques et fonctionnelles | index-spec.md |
| [regles-immuables/](regles-immuables/index-regles-immuables.md) | Process, hiérarchie, RVAV | index-regles-immuables.md |

### Templates

| Fichier | Description |
|---|---|
| [pense-bete-template.md](pense-bete-template.md) | Gabarit pour créer un nouveau pense-bête |

### Pense-bêtes existants

| ID | Thème | Statut | Lien |
|---|---|---|---|
| — | — | — | *(aucun pense-bête pour l'instant)* |

## Comment créer un nouveau pense-bête

> **Flux Athena** : Les pense-bêtes sont rédigés par **Athena** (agent dédié).
> Quand une demande doit devenir un pense-bête, l'utilisateur passe par Buffy qui active Athena.
> Voir : `agents/athena/athena.md` et la section « Créer un pense-bête » de `agents/buffy/buffy.md`.

### Flux avec Athena

```
Demande utilisateur
  -> Cerberus active Buffy
  -> Buffy active Athena (mission : Créer un pense-bête)
  -> Athena rédige le pense-bête jusqu'au statut ebauche
  -> Athena réactive Cerberus
```

### Étapes d'Athena (mission : Créer un pense-bête)

1. Lire la demande de l'utilisateur
2. Vérifier le nommage selon la convention : `[thème].[id].[class].[statut].md`
3. Copier le [pense-bete-template.md](pense-bete-template.md)
4. Remplir les sections (idée, problème, contexte, liens, structure, RVAV)
5. Passer par la boucle RVAV
6. S'arrêter au statut **ebauche** (les sous-fichiers spec/todo/liens sont créés plus tard, sur demande)

### Manuel (sans Athena, cas exceptionnel)

1. Copier le [pense-bete-template.md](pense-bete-template.md)
2. Renommer selon la convention : `[thème].[id].[class].[statut].md`
3. Remplir les sections (idée, problème, contexte, liens)
4. Passer par le cycle RVAV
