---
identite:
  type: index
  appartient_a: commun
  commun: true
---
# Index -- Pense-betes
## Navigation

### Sous-categories

| Dossier | Description | Plateforme |
|---|---|---|
| [conventions/](../agents/conventions/index-conventions.md) | Renommage, structures, liens | index-conventions.md |
| [specs/](specs/index-spec.md) | Definitions techniques et fonctionnelles | index-spec.md |
| [regles-immuables/](../agents/regles-immuables/index-regles-immuables.md) | Process, hierarchie, RVAV | index-regles-immuables.md |

### Templates

| Fichier | Description |
|---|---|
| [pense-bete-template.md](pense-bete-template.md) | Gabarit pour creer un nouveau pense-bete |

### Pense-betes existants

| ID | Theme | Statut | Lien |
|---|---|---|---|
| 001 | Veille de volume v2 (inbox JARVIS qui grossissent) | ebauche | [veille-volume-v2.001.01.ebauche.md](veille-volume-v2.001.01.ebauche.md) |

## Comment creer un nouveau pense-bete

> **Flux Athena** : Les pense-betes sont rediges par **Athena** (agent dedie).
> Quand une demande doit devenir un pense-bete, l'utilisateur passe par Buffy qui active Athena.
> Voir : `agents/athena/athena.md` et la section " Creer un pense-bete " de `agents/buffy/buffy.md`.

### Flux avec Athena

```
Demande utilisateur
  -> Cerberus active Buffy
  -> Buffy active Athena (mission : Creer un pense-bete)
  -> Athena redige le pense-bete jusqu'au statut ebauche
  -> Athena reactive Cerberus
```

### Etapes d'Athena (mission : Creer un pense-bete)

1. Lire la demande de l'utilisateur
2. Verifier le nommage selon la convention : `[theme].[id].[class].[statut].md`
3. Copier le [pense-bete-template.md](pense-bete-template.md)
4. Remplir les sections (idee, probleme, contexte, liens, structure, RVAV)
5. Passer par la boucle RVAV
6. S'arreter au statut **ebauche** (les sous-fichiers spec/todo/liens sont crees plus tard, sur demande)

### Manuel (sans Athena, cas exceptionnel)

1. Copier le [pense-bete-template.md](pense-bete-template.md)
2. Renommer selon la convention : `[theme].[id].[class].[statut].md`
3. Remplir les sections (idee, probleme, contexte, liens)
4. Passer par le cycle RVAV
