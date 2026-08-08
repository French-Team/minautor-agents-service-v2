---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# supprimer-ligne

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** supprimer
**Chemin :** `agents/tools/supprimer/supprimer-ligne/`
**Proprietaire :** Buffy (outil partage)

## Description

Supprimer une ligne (ou une plage de lignes) par numero dans un fichier. Outil de precision, complement de `supprimer-fichier` quand on veut retirer uniquement certaines lignes (par exemple apres un `rechercher-texte` qui a localise le probleme).

## Utilisation

Version Python (recommandee) :

```bash
# Supprimer la ligne 42
python3 supprimer-ligne.py fichier.md 42

# Supprimer les lignes 10 a 15
python3 supprimer-ligne.py fichier.md 10 15

# Simuler avant d'appliquer
python3 supprimer-ligne.py --dry-run fichier.md 42

# Avec details
python3 supprimer-ligne.py --verbose fichier.md 10 15
```

Version bash equivalente : `supprimer-ligne.sh` (meme logique).

## Options

| Option | Description | Defaut |
|---|---|---|
| `--dry-run` | Simuler sans modifier | false |
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. Verifie que le fichier existe
2. Valide que les numeros de lignes sont des nombres valides (>= 1)
3. Verifie que la ligne existe dans le fichier
4. Supprime la ligne ou la plage avec `sed` (fichier temporaire puis remplacement)

## Exemples de sortie

```bash
$ supprimer-ligne.sh --dry-run fichier.md 2
[DRY-RUN] Aucune modification appliquee
Lignes qui seraient supprimees :
[contenu de la ligne 2]

$ supprimer-ligne.sh --verbose fichier.md 2
[INFO] Fichier: fichier.md (5 lignes)
[INFO] Suppression des lignes 2 a 2 (1 ligne(s))
[OK] 1 ligne(s) supprimee(s) de fichier.md
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| Retirer une ligne problematique | `supprimer-ligne.sh fichier.md 42` |
| Nettoyer une plage de lignes | `supprimer-ligne.sh fichier.md 100 120` |
| Purger un fichier sans le reecrire | `supprimer-ligne.sh --dry-run fichier.md 5` |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `supprimer-fichier` | Supprimer un fichier entier |
| `rechercher-texte` | Localiser les numeros de lignes a supprimer |
| `lire-lignes` | Verifier le contenu des lignes avant suppression |
| `inserer-contenu-fichier` | Inserer du contenu a une position (operation inverse) |

## Notes de creation

- [x] L'outil a ete teste en `--dry-run` avant application
- [x] L'outil est conforme ASCII (aucun accent, aucun emoji) -- valider avec `valider-conformite-ascii`
- [x] L'outil est reference dans `index-tools.md`
- [x] L'outil est assigne a un agent dans sa carte de decision (protocole-outils Regle 6)
- [ ] Le statut est passe de `ebauche` a `prepare` apres validation RVAV

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-06 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter, VERSION 0.2.0, statut prepare |
| 0.2.0-py | 2026-08-07 | Version Python creee (supprimer-ligne.py), basee sur outil-template.py. Suppression ligne/plage avec validations + --dry-run |

---
