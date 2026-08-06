# Regles de Hierarchie par Niveau

## Principe fondamental

La structure repose sur la **profondeur de dossiers** pour definir
le niveau d'imbrication. Chaque dossier est un **niveau**. Chaque niveau possede
une **plateforme** (fichier d'entree) qui orchestre les niveau(s) inferieur(s).

**Reorganiser = modifier les appels dans la plateforme. Jamais deplacer le code source.**

-> Consulter `../../conventions/structures/convention-structures.md`
pour les regles structurelles universelles.

## Les niveaux

| Niveau | Exemple | Plateforme | Role |
|---|---|---|---|
| L0 | `cerveau-projet/` | `index-cerveau.md` | Point d'entree, config, navigation globale |
| L1 | `pense-betes/` | `index-pense-bete.md` | Conteneur maitre -- toutes les idees y vivent |
| L2 | `specs/`, `conventions/`, `regles-immuables/` | `index-[cat].md` | Sous-categories thematiques |
| L3 | `renommage/`, `structures/`, `general/`, `hierarchie/` | `index-[sub].md` | Specialisations |
| L4 | `protocole-composition/` | `[theme].md` | Module pense-bete (idee developpee) |
| L5 | `spec/`, `todo/`, `liens/` | `[type]-[theme].md` | Sous-modules du pense-bete |
| L6 | `todo/` (niveau profond) | `index-[type].md` | Elements indivi du sous-module |

## Regles d'or

### 1. Profondeur = Niveau
Le niveau est defini **uniquement** par la profondeur dans l'arbre.
Le nom du dossier n'a aucune incidence sur le niveau.

### 2. Plateforme obligatoire
Chaque dossier **doit** contenir exactement un fichier plateforme :
- Point d'entree unique du dossier
- Contient les appels aux composants enfants
- Ne contient **jamais** de code inline

### 3. Reorganisation par reordonnancement
Pour changer l'ordre d'execution :
1. Modifier l'**ordre des appels** dans la plateforme
2. Le code/fichiers restent **physiquement** en place
3. La plateforme orchestre le flux

-> Exemple : deplacer les minutes avant les heures = changer l'ordre des appels
dans le fichier point d'entree, pas deplacer le code.

### 4. Extension verticale
Un nouveau niveau s'ajoute **uniquement** par un sous-dossier
dans le dossier parent -- jamais en placant des fichiers directement
au niveau du conteneur.

-> Chaque fichier de contenu vit a l'interieur d'un dossier.

### 5. Single entry par dossier
Un dossier a **une seule** plateforme. Pas de fichier secondaire.
La plateforme est identifiee par le pattern de renommage.

### 6. Modules autonomes
Un dossier ne partage **jamais** de ressources avec un autre dossier.
Chaque module a ses propres dependances (ex: `data/` propre).
