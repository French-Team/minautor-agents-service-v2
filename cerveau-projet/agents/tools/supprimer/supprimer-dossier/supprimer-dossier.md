# supprimer-dossier

**Version :** 0.1.0-beta
**Statut :** ebauche
**Categorie :** Supprimer
**Chemin :** `agents/tools/supprimer/supprimer-dossier/`

## Description

Supprimer un dossier recursivement. Operation destructive : exige une confirmation explicite (--force) et protege contre les chemins sensibles (racine, dossier courant, dossier parent). Complement de `supprimer-fichier` pour les dossiers.

## Utilisation

```bash
# Simuler la suppression (voir ce qui serait supprime)
supprimer-dossier.sh chemin/dossier

# Supprimer avec confirmation forcee
supprimer-dossier.sh --force chemin/dossier

# Avec details
supprimer-dossier.sh --force --verbose chemin/dossier
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--force` | Executer la suppression (sans ce flag : dry-run) | false |
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. Verifie que le dossier existe
2. Bloque les chemins sensibles (/, ., .., dossier racine du projet)
3. Sans `--force` : affiche uniquement ce qui serait supprime (dry-run)
4. Avec `--force` : supprime recursivement
5. Rapporte le nombre de fichiers supprimes

## Exemples de sortie

```bash
$ supprimer-dossier.sh dossier-temporaire

=== supprimer-dossier ===
[DRY-RUN] Aucune suppression effectuee (utiliser --force pour executer)
[INFO] 5 fichiers et 2 dossiers seraient supprimes

$ supprimer-dossier.sh --force dossier-temporaire
[OK] Dossier supprime : dossier-temporaire (5 fichiers, 2 dossiers)
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| Nettoyer un dossier temporaire | `supprimer-dossier.sh --force tmp/` |
| Supprimer une copie erronee | `supprimer-dossier.sh --force mauvais-dossier/` |
| Verifier avant suppression | `supprimer-dossier.sh dossier/` (dry-run) |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `supprimer-fichier` | Supprimer un seul fichier |
| `copier-dossier` | Creer une copie avant suppression |
| `rechercher-dossier` | Verifier que le dossier existe avant suppression |

## Notes de creation

- [ ] L'outil a ete teste en `--dry-run` avant application
- [ ] L'outil est conforme ASCII (aucun accent, aucun emoji)
- [ ] L'outil est reference dans `index-tools.md`
- [ ] Le statut est passe de `ebauche` a `prepare` apres validation RVAV
