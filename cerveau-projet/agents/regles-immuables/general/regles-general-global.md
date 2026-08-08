---
identite:
  type: regle
  appartient_a: commun
  commun: true
---
# Regles Generales Globales

## Principe

Ces regles s'appliquent a **tous** les agents et **tous** les fichiers du cerveau-projet, sans exception.

## Les regles globales

| Regle | Description |
|---|---|
| **Ne jamais supposer** | Verifier chaque point avant d'agir. La verification prime sur l'hypothese. |
| **Ne jamais mentir** | Dire la verite, meme si elle est inconfortable. Ne pas inventer de reponses. |
| **ASCII uniquement** | Les emojis et caracteres non-ASCII sont bannis. Utiliser `[OK]`, `[ERREUR]`, `[ATTENTION]`. |
| **Perimetre workspace** | Ecriture dans le workspace uniquement, hors workspace en lecture seule. Ne jamais creer de fichier temporaire hors du workspace. |
| **RVAV obligatoire** | Chaque transition de statut passe par Rechercher-Verifier-Analyser-Valider. |
| **Cycle Cerberus** | Chaque session commence et se termine par Cerberus. |
| **Lire avant d'agir** | Activer un agent sans lire sa fiche est inutile. |
| **Outils partages** | Utiliser exclusivement nos outils, pas des outils generiques. |
| **Auto-correction** | Chaque erreur detectee devient une lecon dans `corrections.md`. |

## Hierarchie des regles

1. **Regles immuables** -- non negociables (veracite, emojis-ascii, validation-rigoureuse)
2. **Conventions** -- maniere standard de faire (renommage, structures, liens)
3. **Protocoles** -- processus a suivre (demarrer, reprendre, outils)
4. **Cartes de decision** -- choix par mission de chaque agent

En cas de conflit : la regle immuable gagne toujours.

## Navigation

- **Parent** : [index-regles-general.md](index-regles-general.md)
- **Regles liees** : [regles-veracite.md](regles-veracite.md), [regles-emojis-ascii.md](regles-emojis-ascii.md), [regles-perimetre-workspace.md](regles-perimetre-workspace.md), [rvav-workflow.md](rvav-workflow.md)
