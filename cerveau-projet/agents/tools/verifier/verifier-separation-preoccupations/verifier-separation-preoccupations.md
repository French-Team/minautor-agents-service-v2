# verifier-separation-preoccupations

**Version :** 0.2.0-py
**Statut :** prepare
**Categorie :** verifier
**Chemin :** `agents/tools/verifier/verifier-separation-preoccupations/`
**Proprietaire :** Janus (outil partage)

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
## Prochaines etapes
## TODO
## A faire
## Faire
## Statut
## Statut du
## Historique
## Corrections recentes
```

## Exemples de sortie

```bash
$ verifier-separation-preoccupations.sh cerveau-projet/

=== Verification de la separation des preoccupations ===

--- Verification des index ---
[ERREUR] cerveau-projet/pense-betes/index-pense-bete.md contient une section de suivi
5:## Prochaines etapes

--- Verification des conventions ---
(rien)

--- Verification des protocoles ---
(rien)

=== Termine ===
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
| `nettoyer-fichier` | Purifie les fichiers apres detection |
| `rechercher-fichiers-vides` | Verifier que les fichiers detectes ont du contenu |

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-06 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter, VERSION 0.2.0, statut prepare |

---
