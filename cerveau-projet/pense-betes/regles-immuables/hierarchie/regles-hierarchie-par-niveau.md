# Règles de Hiérarchie par Niveau

## Principe fondamental

La structure repose sur la **profondeur de dossiers** pour définir
le niveau d'imbrication. Chaque dossier est un **niveau**. Chaque niveau possède
une **plateforme** (fichier d'entrée) qui orchestre les niveau(s) inférieur(s).

**Réorganiser = modifier les appels dans la plateforme. Jamais déplacer le code source.**

-> Consulter `../../conventions/structures/convention-structures.md`
pour les règles structurelles universelles.

## Les niveaux

| Niveau | Exemple | Plateforme | Rôle |
|---|---|---|---|
| L0 | `cerveau-projet/` | `index-cerveau.md` | Point d'entrée, config, navigation globale |
| L1 | `pense-betes/` | `index-pense-bete.md` | Conteneur maitre — toutes les idées y vivent |
| L2 | `specs/`, `conventions/`, `regles-immuables/` | `index-[cat].md` | Sous-catégories thématiques |
| L3 | `renommage/`, `structures/`, `general/`, `hierarchie/` | `index-[sub].md` | Spécialisations |
| L4 | `protocole-composition/` | `[thème].md` | Module pense-bête (idée développée) |
| L5 | `spec/`, `todo/`, `liens/` | `[type]-[thème].md` | Sous-modules du pense-bête |
| L6 | `todo/` (niveau profond) | `index-[type].md` | Éléments indivi du sous-module |

## Règles d'or

### 1. Profondeur = Niveau
Le niveau est défini **uniquement** par la profondeur dans l'arbre.
Le nom du dossier n'a aucune incidence sur le niveau.

### 2. Plateforme obligatoire
Chaque dossier **doit** contenir exactement un fichier plateforme :
- Point d'entrée unique du dossier
- Contient les appels aux composants enfants
- Ne contient **jamais** de code inline

### 3. Réorganisation par réordonnancement
Pour changer l'ordre d'exécution :
1. Modifier l'**ordre des appels** dans la plateforme
2. Le code/fichiers restent **physiquement** en place
3. La plateforme orchestre le flux

-> Exemple : déplacer les minutes avant les heures = changer l'ordre des appels
dans le fichier point d'entrée, pas déplacer le code.

### 4. Extension verticale
Un nouveau niveau s'ajoute **uniquement** par un sous-dossier
dans le dossier parent — jamais en plaçant des fichiers directement
au niveau du conteneur.

-> Chaque fichier de contenu vit à l'intérieur d'un dossier.

### 5. Single entry par dossier
Un dossier a **une seule** plateforme. Pas de fichier secondaire.
La plateforme est identifiée par le pattern de renommage.

### 6. Modules autonomes
Un dossier ne partage **jamais** de ressources avec un autre dossier.
Chaque module a ses propres dépendances (ex: `data/` propre).
