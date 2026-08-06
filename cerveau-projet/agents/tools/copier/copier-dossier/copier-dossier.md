# copier-dossier

**Version :** 0.1.0-beta
**Statut :** ebauche
**Categorie :** Copier
**Chemin :** `agents/tools/copier/copier-dossier/`

## Description

Copier un dossier recursivement vers une destination. Verifie que la source existe, que la destination n'est pas dans la source, et cree le dossier de destination si besoin.

## Utilisation

```bash
# Copier un dossier (recursif)
copier-dossier.sh dossier-source dossier-destination

# Simuler sans copier
copier-dossier.sh --dry-run dossier-source dossier-destination

# Avec details
copier-dossier.sh --verbose dossier-source dossier-destination
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--dry-run` | Simuler sans copier | false |
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. Verifie que la source existe et est un dossier
2. Verifie que la destination n'est pas dans la source (anti-boucle)
3. Verifie que la destination n'existe pas deja (ou la signale)
4. Copie recursivement avec `cp -r`
5. Rapporte le nombre de fichiers copies

## Exemples de sortie

```bash
$ copier-dossier.sh dossiers-src dossiers-dst

=== copier-dossier ===
[OK] Copie terminee : dossiers-src -> dossiers-dst
[INFO] 12 fichiers copies

=== Resume ===
Source : dossiers-src
Destination : dossiers-dst
Resultat : OK
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| Dupliquer une structure de dossiers | `copier-dossier.sh src dst` |
| Copier le outil-template vers un nouvel outil | `copier-dossier.sh outil-template nouveau` |
| Preparer une copie avant modification | `copier-dossier.sh dossier dossier-sauvegarde` |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `copier-fichier` | Copier un seul fichier |
| `rechercher-dossier` | Verifier l'existence d'un dossier avant copie |
| `supprimer-dossier` | Nettoyer une copie erronee |

## Notes de creation

- [ ] L'outil a ete teste en `--dry-run` avant application
- [ ] L'outil est conforme ASCII (aucun accent, aucun emoji)
- [ ] L'outil est reference dans `index-tools.md`
- [ ] Le statut est passe de `ebauche` a `prepare` apres validation RVAV
