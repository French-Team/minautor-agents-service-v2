---
identite:
  type: index
  appartient_a: commun
  commun: true
---
# Index -- Conventions de Structures
## Contenu

| Fichier | Description |
|---|---|
| [convention-structures.md](convention-structures.md) | Principes d'architecture universels |
| [convention-classeur-variables.md](convention-classeur-variables.md) | Classeur de variables partage |
| [convention-pipelines.md](convention-pipelines.md) | Pipelines de traitement de donnees |
| [dossiers/index-dossiers.md](dossiers/index-dossiers.md) | Regles pour les dossiers |
| [fichiers/index-fichiers.md](fichiers/index-fichiers.md) | Regles pour les fichiers |

## Navigation

- **Parent** : [index-conventions.md](../index-conventions.md)
- **Soeurs** : [renommage/](../renommage/convention-renommage.md), [liens/](../liens/convention-liens.md)
- **Regles** : [regles-hierarchie-par-niveau.md](../../regles-immuables/hierarchie/regles-hierarchie-par-niveau.md)

## Resume rapide

1. **Racine** = config + demarrage uniquement
2. **Dossier** = niveau inferieur
3. **Fichier** = point d'entree (jamais de code inline)
4. **Fonction** = dossier au niveau inferieur
5. **Reorganisation** = reordonner les appels
6. **Modules autonomes** = pas de partage de dossiers
