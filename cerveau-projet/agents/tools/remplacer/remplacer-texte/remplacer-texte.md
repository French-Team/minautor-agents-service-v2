---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# remplacer-texte

**Version :** 0.1.0-beta
**Statut :** ebauche
**Categorie :** remplacer
**Chemin :** `agents/tools/remplacer/remplacer-texte/`
**Proprietaire :** outil partage

## Description

Remplacer une liste de paires `ancien -> nouveau` dans plusieurs fichiers d'un dossier (recursif). Cree pour les renommages massifs (ex: renommer un outil et ses ~120 references) sans re-ecrire un script temporaire a chaque fois.

## Utilisation

```bash
# Remplacement simple dans un dossier
remplacer-texte.sh dossier 'ancien=nouveau'

# Plusieurs paires (ordre : les chaines longues d'abord)
remplacer-texte.py dossier 'chemin/ancien=nouveau/chemin' 'ancien=nouveau'

# Simuler sans rien modifier
remplacer-texte.py --dry-run dossier 'ancien=nouveau'
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--dry-run` | Afficher les fichiers qui SERAIENT modifies sans rien ecrire | false |
| `--ext 'md,sh,py'` | Extensions a traiter | `md,sh,py` |
| `--exclu-fichier NOM` | Exclure un fichier (repetable) | `AGENTS-historique.md` |
| `--exclu-dossier NOM` | Exclure un dossier (repetable) | `exemples, .git, __pycache__` |
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |
| `--version` | Afficher la version (version .py) | - |

## Ce que l'outil fait

1. Parcourt recursivement le dossier (exclusions appliquees)
2. Filtre par extension
3. Applique les paires dans l'ordre donne
4. Rapporte le nombre de fichiers analyses et modifies + la liste

## Regles

- **Ordre des paires** : mettre d'abord les chemins complets/chaines longues, puis les noms courts (evite les collisions de sous-chaines)
- **Idempotence** : re-executer une seconde fois ne change rien (le nouveau texte ne contient plus l'ancien)
- **Exclusions par defaut** : `AGENTS-historique.md` (journal historique a preserver), `exemples/` (fichiers de test volontairement defectueux), `.git/`, `__pycache__/`

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| Renommer un outil + toutes ses references | `remplacer-texte.py . 'ancien-nom=nouveau-nom' 'chemin/ancien=chemin/nouveau'` |
| Mettre a jour une reference dans tous les fichiers | `remplacer-texte.py dossier 'ancienne-ref=nouvelle-ref'` |
| Verifier le perimetre avant d'appliquer | `remplacer-texte.py --dry-run dossier 'a=b'` |

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-07 | Creation : remplacement massif multi-fichiers (paires, exclusions, dry-run, rapport). Inspire du script temporaire eprouve lors du renommage de mettre-a-jour-agents-md vers activer-agent-principal |

## Notes de creation

- [x] L'outil est conforme ASCII
- [x] L'outil est reference dans index-tools.md (section Remplacer)
- [x] Tests reels effectues (nominal, dry-run, exclusions, idempotence)
