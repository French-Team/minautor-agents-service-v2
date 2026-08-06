# inserer-contenu-fichier

**Version :** 0.1.0-beta
**Statut :** ebauche
**Categorie :** Inserer
**Chemin :** `agents/tools/inserer/inserer-contenu-fichier/`

## Description

Inserer du contenu a une position precise dans un fichier (apres un numero de ligne donne). Complement de `editer-fichier` (remplacement) et `ajouter-contenu-fichier` (fin de fichier) pour les insertions au milieu.

## Utilisation

```bash
# Inserer une ligne apres la ligne 5
inserer-contenu-fichier.sh fichier.md 5 "Contenu a inserer"

# Inserer le contenu d'un fichier source apres la ligne 10
inserer-contenu-fichier.sh fichier.md 10 --fichier bloc.md

# Simuler sans modifier
inserer-contenu-fichier.sh --dry-run fichier.md 5 "contenu"
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--fichier <src>` | Inserer le contenu d'un fichier source | - |
| `--dry-run` | Simuler sans modifier | false |
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. Verifie que le fichier existe et que le numero de ligne est valide
2. Determine la source du contenu (chaine ou fichier)
3. Insere le contenu apres la ligne indiquee (sans la supprimer)
4. Rapporte la position d'insertion

## Exemples de sortie

```bash
$ inserer-contenu-fichier.sh fichier.md 5 "Nouvelle section"

=== inserer-contenu-fichier ===
[OK] Contenu insere apres la ligne 5 de fichier.md

=== Resume ===
Fichier : fichier.md
Position : apres la ligne 5
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| Ajouter une section au milieu d'un document | `inserer-contenu-fichier.sh doc.md 12 "## Section"` |
| Inserer un bloc apres un marqueur connu | Trouver le numero via `rechercher-texte`, puis inserer |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `editer-fichier` | Remplacer une chaine par une autre |
| `ajouter-contenu-fichier` | Ajouter a la fin d'un fichier |
| `rechercher-texte` | Trouver le numero de ligne d'insertion |

## Notes de creation

- [ ] L'outil a ete teste en `--dry-run` avant application
- [ ] L'outil est conforme ASCII (aucun accent, aucun emoji)
- [ ] L'outil est reference dans `index-tools.md`
- [ ] Le statut est passe de `ebauche` a `prepare` apres validation RVAV
