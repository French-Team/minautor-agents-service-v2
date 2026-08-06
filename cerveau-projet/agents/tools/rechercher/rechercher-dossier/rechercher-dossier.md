# rechercher-dossier

**Version :** 0.1.0-beta
**Statut :** ebauche
**Categorie :** Rechercher
**Chemin :** `agents/tools/rechercher/rechercher-dossier/`

## Description

Verifier si un dossier existe. Retourne un code de sortie exploitable en script (0 = existe, 1 = n'existe pas) et affiche un message clair. Complement de `rechercher-fichier` pour les dossiers.

## Utilisation

```bash
# Verifier si un dossier existe
rechercher-dossier.sh chemin/dossier

# Avec details
rechercher-dossier.sh --verbose chemin/dossier

# Usage en script (code de sortie)
if rechercher-dossier.sh chemin/dossier; then
    echo "Le dossier existe"
fi
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. Verifie qu'un chemin est fourni
2. Verifie si le chemin existe et est un dossier
3. Affiche le resultat et retourne 0 (existe) ou 1 (absent)

## Exemples de sortie

```bash
$ rechercher-dossier.sh cerveau-projet/agents/tools
[OK] Le dossier existe : cerveau-projet/agents/tools

$ rechercher-dossier.sh chemin/inexistant
[ERREUR] Le dossier n'existe pas : chemin/inexistant
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| Avant une creation dans un dossier | Verifier que le dossier parent existe |
| Avant une copie de dossier | `rechercher-dossier.sh source` |
| Avant une suppression de dossier | Confirmer que le dossier existe |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `rechercher-fichier` | Verifier l'existence d'un fichier |
| `creer-dossier` (a venir) | Creer un dossier si absent |
| `copier-dossier` / `supprimer-dossier` | Operations sur dossiers |

## Notes de creation

- [ ] L'outil a ete teste en `--dry-run` avant application
- [ ] L'outil est conforme ASCII (aucun accent, aucun emoji)
- [ ] L'outil est reference dans `index-tools.md`
- [ ] Le statut est passe de `ebauche` a `prepare` apres validation RVAV
