# deplacer-fichier

**Version :** 0.1.0-beta
**Statut :** ebauche
**Categorie :** Deplacer
**Chemin :** `agents/tools/deplacer/deplacer-fichier/`

## Description

Deplacer ou renommer un fichier vers une nouvelle destination. Verifie que la source existe, que la destination n'est pas identique, et cree le dossier parent de destination si besoin. Attention : `changer-statut` reste l'outil dedie au renommage de statut (ebauche -> prepare).

## Utilisation

```bash
# Deplacer un fichier vers un autre dossier
deplacer-fichier.sh fichier-source.md nouvelle/destination/fichier.md

# Renommer un fichier
deplacer-fichier.sh ancien-nom.md nouveau-nom.md

# Simuler sans deplacer
deplacer-fichier.sh --dry-run source.md destination.md
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--dry-run` | Simuler sans deplacer | false |
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. Verifie que la source existe et est un fichier
2. Verifie que la destination n'est pas identique a la source
3. Cree le dossier parent de destination si absent
4. Deplace le fichier avec `mv`
5. Rapporte le deplacement

## Exemples de sortie

```bash
$ deplacer-fichier.sh src/ancien.md dst/nouveau.md

=== deplacer-fichier ===
[OK] Fichier deplace : src/ancien.md -> dst/nouveau.md

=== Resume ===
Source : src/ancien.md
Destination : dst/nouveau.md
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| Reorganiser un fichier | `deplacer-fichier.sh src/x.md dst/x.md` |
| Renommer un fichier (hors statut) | `deplacer-fichier.sh ancien.md nouveau.md` |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `changer-statut` | Renommage dedie aux statuts de fichiers (ebauche, prepare) |
| `copier-fichier` | Copier en gardant l'original |
| `supprimer-fichier` | Supprimer l'original apres copie (equivalent manuel) |

## Notes de creation

- [ ] L'outil a ete teste en `--dry-run` avant application
- [ ] L'outil est conforme ASCII (aucun accent, aucun emoji)
- [ ] L'outil est reference dans `index-tools.md`
- [ ] Le statut est passe de `ebauche` a `prepare` apres validation RVAV
