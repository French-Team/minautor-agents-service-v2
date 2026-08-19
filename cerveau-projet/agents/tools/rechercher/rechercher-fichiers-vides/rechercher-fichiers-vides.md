---
identite:
  type: outil
  appartient_a: commun
  commun: true
  combos:
    - combo-sante-tableaux
---
# rechercher-fichiers-vides

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** rechercher
**Chemin :** `agents/tools/rechercher/rechercher-fichiers-vides/`
**Proprietaire :** Buffy (outil partage)

## Description

Rechercher les fichiers markdown vides ou quasi vides dans le projet. Un fichier est considere comme vide si le nombre de lignes non vides est inferieur au seuil (defaut : 5 lignes).

## Utilisation

Version Python (recommandee) :

```bash
# Rechercher dans un dossier specifique
python3 rechercher-fichiers-vides.py cerveau-projet/

# Fichiers de moins de 10 lignes
python3 rechercher-fichiers-vides.py --seuil 10 cerveau-projet/

# Avec details
python3 rechercher-fichiers-vides.py --verbose cerveau-projet/
```

Version bash equivalente : `rechercher-fichiers-vides.sh` (meme logique).

## Options

| Option | Description | Defaut |
|---|---|---|
| `--seuil <n>` | Taille minimale pour considerer un fichier comme vide | 5 lignes |
| `--extensions` | Extensions a chercher | md |
| `--exclure` | Dossiers a exclure | .git,node_modules,.agents |
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. **Scan** - Trouve tous les fichiers des extensions specifiees
2. **Analyse** - Compte les lignes non vides (ignore les lignes vides et le frontmatter `---`)
3. **Detecte** - Identifie les fichiers sous le seuil
4. **Rapporte** - Liste les fichiers vides avec le nombre de lignes

## Definition de "vide"

Un fichier est considere comme vide si :

```
lignes_non_vides < seuil
```

Ou `lignes_non_vides` exclut :
- Les lignes vides
- Les delimiteurs de frontmatter `---`

## Exemples de sortie

```bash
$ rechercher-fichiers-vides.sh --seuil 10 cerveau-projet/

=== Recherche de fichiers vides ===
Dossier : cerveau-projet/
Seuil : 10 lignes non vides
Extensions : md

  [VIDE] cerveau-projet/exemples/test-abc.md
  [VIDE] cerveau-projet/pense-betes/index.md

=== Resume ===
Fichiers trouves : 150
Fichiers vides ou quasi vides : 2
Fichiers avec contenu : 148

[ATTENTION] Des fichiers vides ont ete trouves
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Audit du projet** | Detecter les fichiers inutiles ou inacheves |
| **Avant commit** | Verifier qu'aucun fichier vide n'est commit |
| **Controle de qualite** | Garantir que tous les fichiers ont du contenu |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `lister-statuts` | Voir le statut des fichiers detectes |
| `detecter-surcharge-fichier` | Detecter les fichiers trop gros (inverse) |
| `valider-ebauche` | Verifier les exigences minimales d'un ebauche |

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-06 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter, VERSION 0.2.0, statut prepare |
| 0.2.0-py | 2026-08-07 | Version Python creee (rechercher-fichiers-vides.py), basee sur outil-template.py. Scan + seuil de lignes non vides, exit 1 si fichiers vides |

---
