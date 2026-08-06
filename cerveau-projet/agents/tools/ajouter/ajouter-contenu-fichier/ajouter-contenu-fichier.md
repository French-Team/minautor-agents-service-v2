# ajouter-contenu-fichier

**Version :** 0.1.0-beta
**Statut :** ebauche
**Categorie :** Ajouter
**Chemin :** `agents/tools/ajouter/ajouter-contenu-fichier/`

## Description

Ajouter du contenu a la fin d'un fichier (append). Complement de `ecrire-fichier` (qui ecrase) : ici le contenu existant est preserve. Accepte une chaine directe ou un fichier source a ajouter.

## Utilisation

```bash
# Ajouter une chaine a la fin d'un fichier
ajouter-contenu-fichier.sh fichier.md "Nouvelle ligne a ajouter"

# Ajouter le contenu d'un fichier source a la fin
ajouter-contenu-fichier.sh fichier-cible.md --fichier fichier-source.md

# Simuler sans modifier
ajouter-contenu-fichier.sh --dry-run fichier.md "contenu"
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--fichier <src>` | Ajouter le contenu d'un fichier source | - |
| `--dry-run` | Simuler sans modifier | false |
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. Verifie que le fichier cible existe
2. Determine la source du contenu (chaine ou fichier)
3. Ajoute le contenu a la fin (avec retour a la ligne si necessaire)
4. Rapporte le nombre de lignes ajoutees

## Exemples de sortie

```bash
$ ajouter-contenu-fichier.sh fichier.md "Nouvelle ligne"

=== ajouter-contenu-fichier ===
[OK] 1 ligne ajoutee a la fin de fichier.md

=== Resume ===
Fichier : fichier.md
Lignes ajoutees : 1
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| Completer un fichier sans le reecrire | `ajouter-contenu-fichier.sh fichier.md "texte"` |
| Ajouter un bloc a un journal | `ajouter-contenu-fichier.sh journal.md --fichier bloc.md` |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `ecrire-fichier` | Ecrire ou ecraser le contenu complet |
| `inserer-contenu-fichier` | Inserer du contenu a une position precise |
| `creer-fichier` | Creer un nouveau fichier avec du contenu initial |

## Notes de creation

- [ ] L'outil a ete teste en `--dry-run` avant application
- [ ] L'outil est conforme ASCII (aucun accent, aucun emoji)
- [ ] L'outil est reference dans `index-tools.md`
- [ ] Le statut est passe de `ebauche` a `prepare` apres validation RVAV
