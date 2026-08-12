---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# supprimer-fichier

**Version :** 0.3.1
**Statut :** prepare
**Categorie :** Supprimer
**Chemin :** `agents/tools/supprimer/supprimer-fichier/`
**Proprietaire :** outil partage

## Description

Supprimer un fichier avec verification.

**Echec explicite** : si le fichier n'existe pas, l'outil retourne un code non nul (1) avec un message clair - jamais 0 silencieux. Option `--backup` pour sauvegarder avant suppression.

## Utilisation

Version Python (recommandee) :

```bash
# Supprimer un fichier
python3 supprimer-fichier.py fichier.md

# Simuler
python3 supprimer-fichier.py --dry-run fichier.md
```

Version bash equivalente : `supprimer-fichier.sh` (meme logique).

## Options

| Option | Description | Defaut |
|---|---|---|
| `--forcer` | Supprimer sans confirmer | false |
| `--dry-run` | Simuler sans supprimer | false |
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-05 | Creation initiale |
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels (suppression, fichier inexistant, --dry-run), promotion prepare |
| 0.2.0-py | 2026-08-07 | Version Python creee (supprimer-fichier.py), basee sur outil-template.py. Suppression avec --dry-run/--forcer/--verbose |
| 0.3.0 | 2026-08-12 | Qualite pro : echec explicite (fichier inexistant -> code 1), protection nommage, option --backup |
| 0.3.1 | 2026-08-12 | SECURITE (round 3) : refus octet nul dans le chemin (la suppression d un lien symbolique reste sure : os.remove ne touche que le lien, jamais la cible) |

## Notes de creation

- [x] L'outil est conforme ASCII
- [x] L'outil est reference dans index-tools.md
- [x] Le statut est passe de `ebauche` a `prepare`