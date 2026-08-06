# verifier-separation-preoccupations

**Version :** 0.1.0-beta
**Statut :** ebauche
**Categorie :** Valider
**Chemin :** `agents/tools/valider/verifier-separation-preoccupations/`

## Description

Verifier la separation des preoccupations dans tous les fichiers du projet. C'est la version globale de `verifier-role-fichier` : elle scanne tous les index, conventions et protocoles pour detecter les sections de suivi qui n'ont pas leur place (TODO, Prochaines etapes, Historique, Statut).

## Utilisation

```bash
# Verifier tout le projet
verifier-separation-preoccupations.sh

# Verifier un dossier specifique
verifier-separation-preoccupations.sh cerveau-projet/pense-betes/

# Verifier les outils
verifier-separation-preoccupations.sh cerveau-projet/agents/tools/
```

## Ce que l'outil fait

1. **Index** - Cherche les sections de suivi dans tous les `index-*.md`
2. **Conventions** - Cherche les sections de suivi dans tous les `convention-*.md`
3. **Protocoles** - Cherche les sections de suivi dans tous les `protocole-*.md` (ignore les fichiers avec template/modele dans le contenu)
4. **Rapporte** - Liste chaque fichier avec ses sections hors role

## Sections detectees

```
## Prochaines étapes
## TODO
## À faire
## Faire
## Statut
## Statut du
## Historique
## Corrections récentes
```

## Exemples de sortie

```bash
$ verifier-separation-preoccupations.sh cerveau-projet/

=== Vérification de la séparation des préoccupations ===

--- Vérification des index ---
[ERREUR] cerveau-projet/pense-betes/index-pense-bete.md contient une section de suivi
5:## Prochaines étapes

--- Vérification des conventions ---
(rien)

--- Vérification des protocoles ---
(rien)

=== Terminé ===
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Audit global du cerveau** | Detecter tous les fichiers detournes de leur role |
| **Apres une serie de modifications** | Verifier que rien n'a ete ajoute au mauvais endroit |
| **Controle de qualite** | Garantir la separation des preoccupations partout |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `verifier-role-fichier` | Version ciblee sur un seul fichier |
| `purifier-fichier` | Purifie les fichiers apres detection |
| `rechercher-fichiers-vides` | Verifier que les fichiers detectes ont du contenu |
