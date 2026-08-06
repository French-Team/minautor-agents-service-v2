# Protocole de Composition du Cerveau

Recette pour composer le squelette de base du cerveau-projet.
Chaque étape passe par RVAV (rechercher-vérifier-analyser-valider)
défini dans `../rvav-workflow.md`.

**Règles applicables :**
- `regles-veracite.md` -- ne jamais mentir ou inventer
- `regles-emojis-ascii.md` -- bannissement des emojis
- `protocole-recherches-web` -- recherches web
- `protocole-identification` -- identification des agents

## ÉTAPE 1 — Créer index-cerveau.md (point d'entrée)

1. Créer le fichier `cerveau-projet/index-cerveau.md` à la racine
2. Contenu minimal :
   - Titre du projet
   - Version (ex: v0.0.1)
   - Brève description (1 phrase)
    - Table des matières dynamique (liens vers pense-betes/ et ses sous-dossiers conventions/, specs/, regles-immuables/)
3. **RVAV :**
    - [rechercher] Vérifier que le nom suit `../../../conventions/renommage/`
   - [vérifier] Confirmer que tous les liens internes pointent vers des fichiers existants
   - [analyser] Vérifier que la description capture l'essence du projet sans détails
   - [valider] L'index est le point d'entrée unique — il doit être cohérent

## ÉTAPE 2 — Créer la structure des dossiers

1. Créer `pense-betes/` à la racine de `cerveau-projet/`
2. À l'intérieur de `pense-betes/`, créer les 3 sous-dossiers :
    - `conventions/` — renommage, structures, liens, protocoles
    - `specs/` — définitions techniques et fonctionnelles
    - `regles-immuables/` — process, hiérarchie, RVAV
3. Créer `recherches-web/` à la racine de `cerveau-projet/`
    - `templates/` — templates pour les recherches
4. Chaque dossier possède un fichier `index-*.md` à sa racine
5. **RVAV :**
    - [rechercher] Vérifier que chaque nom respecte `../../../conventions/renommage/`
    - [vérifier] Confirmer qu'aucun dossier n'est vide (au moins un index)
    - [analyser] Vérifier que la séparation des responsabilités est cohérente
    - [valider] La structure peut être étendue mais pas modifiée en profondeur

## ÉTAPE 3 — Vérifier les templates de référence

1. Les templates suivants servent de gabarit pour créer de nouveaux fichiers :
   - `pense-betes/pense-bete-template.md` -> modèle pour les plateformes de pense-bête
   - `pense-betes/specs/spec-template.md` -> modèle pour les specs
   - `pense-betes/specs/todo/todo-template.md` -> modèle pour les todos
2. Chaque template reste vide — il définit la structure, pas le contenu
3. **RVAV :**
   - [rechercher] Vérifier que chaque template existe et est bien vide (0 octets)
   - [vérifier] Confirmer que le pattern index/template est respecté
   - [analyser] Vérifier que les templates sont accessibles depuis le cerveau-projet
   - [valider] Les templates sont la source de vérité pour tous les futurs modules
