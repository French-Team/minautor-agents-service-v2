# lire-lignes

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** lire
**Chemin :** `agents/tools/lire/lire-lignes/`
**Proprietaire :** Buffy (outil partage)

## Description

Lire des lignes specifiques d'un fichier (par numero ou plage de numeros). Complement de `lire-fichier` quand on connait deja les numeros de lignes a consulter (par exemple apres un `rechercher-texte`).

## Utilisation

```bash
# Lire la ligne 5
lire-lignes.sh fichier.md 5

# Version Python (recommandee)
python3 lire-lignes.py fichier.md 5

# Lire les lignes 5 a 15
lire-lignes.sh fichier.md 5 15

# Avec details
lire-lignes.sh --verbose fichier.md 10 20
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--verbose` | Afficher les details (total, plage) | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. Verifie que le fichier existe
2. Valide que debut et fin sont des nombres valides (>= 1)
3. Affiche les lignes demandees

## Exemples de sortie

```bash
$ lire-lignes.sh fichier.md 5 7
ligne 5 du fichier
ligne 6 du fichier
ligne 7 du fichier
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| Connaitre le numero de ligne (via rechercher-texte) | `lire-lignes.sh fichier.md 42` |
| Lire un extrait precis | `lire-lignes.sh fichier.md 10 30` |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `lire-fichier` | Lire un fichier complet ou par options (--debut/--fin) |
| `rechercher-texte` | Trouver les numeros de lignes, puis les lire avec cet outil |

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
| 0.2.0-py | 2026-08-07 | Version Python creee (ligne seule / plage, validations, --version) |

---
