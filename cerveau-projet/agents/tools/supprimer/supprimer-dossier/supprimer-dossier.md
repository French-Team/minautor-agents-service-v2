---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# supprimer-dossier

**Version :** 0.2.1
**Statut :** prepare
**Categorie :** supprimer
**Chemin :** `agents/tools/supprimer/supprimer-dossier/`
**Proprietaire :** Buffy (outil partage)

## Description

Supprimer un dossier recursivement. Operation destructive : exige une confirmation explicite (--force) et protege contre les chemins sensibles (racine, dossier courant, dossier parent). Complement de `supprimer-fichier` pour les dossiers.

## Utilisation

Version Python (recommandee) :

```bash
# Simuler la suppression (voir ce qui serait supprime)
python3 supprimer-dossier.py chemin/dossier

# Supprimer avec confirmation forcee
python3 supprimer-dossier.py --force chemin/dossier

# Avec details
python3 supprimer-dossier.py --force --verbose chemin/dossier
```

Version bash equivalente : `supprimer-dossier.sh` (meme logique).

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

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-06 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter, VERSION 0.2.0, statut prepare |
| 0.2.1-py | 2026-08-15 | VERROU D HABILITATION (demande utilisateur) : --agent OBLIGATOIRE + appel a proteger-verrou-habilitation AVANT la suppression - seul hygie peut supprimer, tout autre agent est bloque avec la commande d activation. |
| 0.2.0-py | 2026-08-07 | Version Python creee (supprimer-dossier.py), basee sur outil-template.py. Suppression recursive avec dry-run par defaut, protections chemins sensibles + racine + tools/, --force pour executer |

---
