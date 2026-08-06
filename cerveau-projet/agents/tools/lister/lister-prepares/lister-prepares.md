# Outil -- Lister les Fichiers Prepare

**Categorie** : Lister
**Version** : 0.1.0
**Statut** : beta
**Date creation** : 2026-08-05
**Proprietaire** : Vulcain (outil partage)

---

## Objectif

Lister les fichiers au statut 'prepare' et verifier si une spec existe pour chacun.

**Pourquoi cet outil ?**
- Les fichiers 'prepare' sont prets pour le developpement
- Il faut s'assurer que les specs existent avant de commencer
- Cet outil automatise la verification

---

## Utilisation

```bash
./lister-prepares.sh [DOSSIER] [OPTIONS]
```

### Options

| Option | Description |
|---|---|
| `--creer-spec` | Proposer de creer les specs manquantes |
| `--verbose` | Afficher les details |
| `--aide` | Afficher l'aide |

### Exemples

```bash
# Lister tous les fichiers 'prepare'
./lister-prepares.sh

# Lister dans un dossier
./lister-prepares.sh cerveau-projet/

# Proposer de creer les specs
./lister-prepares.sh --creer-spec
```

---

## Resultat

### Exemple de sortie

```
=== Fichiers 'prepare' ===
Dossier : cerveau-projet/

[OK] protocole-activation.001.02.prepare.md
[OK] protocole-auto-correction.001.02.prepare.md
[SANS SPEC] protocole-versionning-outils.001.02.prepare.md

=== Resumer ===
Fichiers 'prepare' trouves : 3
Specs manquantes : 1

Des specs sont a creer pour les fichiers 'prepare'.
Utiliser le template : cerveau-projet/pense-betes/specs/spec-template.md
```

---

## Comment ca fonctionne

| Etape | Description |
|---|---|
| 1. Chercher les fichiers | Trouver tous les fichiers `*.prepare.md` |
| 2. Verifier les specs | Pour chaque fichier, chercher une spec correspondante |
| 3. Afficher les resultats | Indiquer quels fichiers ont ou n'ont pas de spec |
| 4. Proposer la creation | Si `--creer-spec`, proposer de creer les specs manquantes |

---

## Relation avec le workflow RVAV

Cet outil est utilise a l'etape **[Rechercher]** du workflow RVAV :

```
1. [Rechercher]   -> lister-prepares pour voir les fichiers 'prepare'
2. [Verifier]     -> valider-nommage pour chaque fichier
3. [Analyser]     -> Lire le contenu des fichiers
4. [Valider]      -> valider-ebauche pour chaque fichier
5. [Purifier]     -> nettoyer-fichier ou condenser-fichier
```

---

## Qui devrait utiliser cet outil ?

| Agent | Quand l'utiliser |
|---|---|
| **Buffy** | Avant de commencer le developpement d'un protocole |
| **Janus** | Pour verifier que les specs existent |
| **Tout agent** | Avant de commencer une mission sur un fichier 'prepare' |

---

## Template de spec

Pour creer une spec, utiliser le template :

```
cerveau-projet/pense-betes/specs/spec-template.md
```

---

## Notes

- Cet outil ne modifie pas les fichiers, il les analyse uniquement
- Les fichiers 'prepare' ont une structure complete
- Les specs sont necessaires avant le developpement
- Utiliser `valider-nommage` pour verifier la conformite des noms

---

## Liens

- **Workflow** : `rvav-workflow.md` -- processus de validation
- **Template** : `spec-template.md` -- template de spec
- **Outil similaire** : `lister-statuts` -- lister les fichiers par statut
