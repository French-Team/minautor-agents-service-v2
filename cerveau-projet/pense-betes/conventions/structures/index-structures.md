# Index — Conventions de Structures
## Contenu

| Fichier | Description |
|---|---|
| [convention-structures.md](convention-structures.md) | Principes d'architecture universels |
| [convention-classeur-variables.md](convention-classeur-variables.md) | Classeur de variables partagé |
| [convention-pipelines.md](convention-pipelines.md) | Pipelines de traitement de données |
| [dossiers/index-dossiers.md](dossiers/index-dossiers.md) | Règles pour les dossiers |
| [fichiers/index-fichiers.md](fichiers/index-fichiers.md) | Règles pour les fichiers |

## Navigation

- **Parent** : [index-conventions.md](../index-conventions.md)
- **Sœurs** : [renommage/](../renommage/convention-renommage.md), [liens/](../liens/convention-liens.md)
- **Règles** : [regles-hierarchie-par-niveau.md](../../regles-immuables/hierarchie/regles-hierarchie-par-niveau.md)

## Résumé rapide

1. **Racine** = config + démarrage uniquement
2. **Dossier** = niveau inférieur
3. **Fichier** = point d'entrée (jamais de code inline)
4. **Fonction** = dossier au niveau inférieur
5. **Réorganisation** = réordonner les appels
6. **Modules autonomes** = pas de partage de dossiers
