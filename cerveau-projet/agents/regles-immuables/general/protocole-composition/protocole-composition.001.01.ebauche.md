---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
# Protocole de Composition du Cerveau

Recette pour composer le squelette de base du cerveau-projet.
Chaque etape passe par RVAV (rechercher-verifier-analyser-valider)
defini dans `../rvav-workflow.md`.

**Regles applicables :**
- `regles-veracite.md` -- ne jamais mentir ou inventer
- `regles-emojis-ascii.md` -- bannissement des emojis
- `protocole-recherches-web` -- recherches web
- `protocole-identification` -- identification des agents

## ETAPE 1 -- Creer index-cerveau.md (point d'entree)

1. Creer le fichier `cerveau-projet/index-cerveau.md` a la racine
2. Contenu minimal :
   - Titre du projet
   - Version (ex: v0.0.1)
   - Breve description (1 phrase)
    - Table des matieres dynamique (liens vers agents/ et ses sous-dossiers conventions/, regles-immuables/, outils, et vers pense-betes/ specs/)
3. **RVAV :**
    - [rechercher] Verifier que le nom suit `../../../conventions/renommage/`
   - [verifier] Confirmer que tous les liens internes pointent vers des fichiers existants
   - [analyser] Verifier que la description capture l'essence du projet sans details
   - [valider] L'index est le point d'entree unique -- il doit etre coherent

## ETAPE 2 -- Creer la structure des dossiers

1. Creer `agents/` a la racine de `cerveau-projet/`
2. A l'interieur de `agents/`, creer les sous-dossiers :
    - `conventions/` -- renommage, structures, liens, protocoles
    - `regles-immuables/` -- process, hierarchie, RVAV
    - `classeur-variables/` -- stockage partage des variables
    - `tools/` -- boite a outils
3. Creer `pense-betes/` a la racine de `cerveau-projet/` pour les specs et le travail en cours
    - `specs/` -- definitions techniques et fonctionnelles
4. Creer `recherches-web/` a la racine de `cerveau-projet/`
    - `templates/` -- templates pour les recherches
4. Chaque dossier possede un fichier `index-*.md` a sa racine
5. **RVAV :**
    - [rechercher] Verifier que chaque nom respecte `../../../conventions/renommage/`
    - [verifier] Confirmer qu'aucun dossier n'est vide (au moins un index)
    - [analyser] Verifier que la separation des responsabilites est coherente
    - [valider] La structure peut etre etendue mais pas modifiee en profondeur

## ETAPE 3 -- Verifier les templates de reference

1. Les templates suivants servent de gabarit pour creer de nouveaux fichiers :
   - `pense-betes/pense-bete-template.md` -> modele pour les plateformes de pense-bete
   - `pense-betes/specs/spec-template.md` -> modele pour les specs
   - `pense-betes/specs/todo/todo-template.md` -> modele pour les todos
2. Chaque template reste vide -- il definit la structure, pas le contenu
3. **RVAV :**
   - [rechercher] Verifier que chaque template existe et est bien vide (0 octets)
   - [verifier] Confirmer que le pattern index/template est respecte
   - [analyser] Verifier que les templates sont accessibles depuis le cerveau-projet
   - [valider] Les templates sont la source de verite pour tous les futurs modules
