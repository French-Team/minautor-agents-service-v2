---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# corriger-noms-maj

**Categorie** : Corriger
**Version** : 0.1.1
**Statut** : ebauche

---

## Objectif

Corriger les ecarts de **casse et de forme des NOMS** detectes par
`analyser-noms-maj` dans le registre-usages-outils : normaliser le champ
`outil` (chemin/extension/prefixe temp -> nom kebab-case minuscule).

Complement de `analyser-noms-maj` : l outil analyse (detecte), celui-ci
corrige, avec dry-run et rapport.

---

## Corrections appliquees

| Cas | Avant | Apres |
|---|---|---|
| **OUTIL_CHEMIN** (chemin temp) | `tmp-buffy/resync-lock-et-appliquer.py` | `resync-lock-et-appliquer` |
| **OUTIL_CHEMIN** (fichier a la racine) | `tmp-test-declaration.py` | `test-declaration` |
| **OUTIL_CASSE** (MAJ) | `Tester-Lancer-NonRegression` | `tester-lancer-non-regression` |

Regles de normalisation :
1. chemin -> basename (separateurs `/` et `\`)
2. extension `.py/.sh/.json/.md/.txt` retiree
3. prefixe temp `tmp-`, `.tmp-`, `.zz-` retire (un script temp n est pas
   un outil durable)
4. casse camelCase -> kebab-case, tout en minuscule
5. caracteres non conformes -> tirets

---

## Usage

```bash
# Apercu sans rien ecrire
python3 corriger-noms-maj.py --dry-run

# Application reelle
python3 corriger-noms-maj.py

# Avec rapport markdown
python3 corriger-noms-maj.py --dry-run --rapport rapport-correction.md
python3 corriger-noms-maj.py --rapport rapport-correction.md

# Autre registre
python3 corriger-noms-maj.py --registre chemin/registre.jsonl --dry-run

# Version
python3 corriger-noms-maj.py --version
```

## Options

| Option | Description |
|---|---|
| `--registre <fichier>` | chemin du registre (defaut: `registre-usages-outils.jsonl`) |
| `--dry-run` | affiche les corrections sans ecrire |
| `--rapport <fichier>` | ecrit le rapport markdown |
| `--verbose` | detail |
| `--no-chrono` | coupe le chrono |
| `--version` | affiche la version |

---

## Securite

- `--dry-run` ne modifie JAMAIS le fichier : la sortie est identique a
  l application reelle (verifiez avant d appliquer).
- **GARANTIE DE NON-PERTE (v0.1.1)** : la reecriture s applique ligne par
  ligne sur les lignes BRUTES (jamais par index d entree parsee), et le
  nombre de lignes JSON valides AVANT est compare a celui APRES : si le
  compte change, l ecriture est REFUSEE (code 1). Les lignes vides et
  invalides sont PRESERVEES telles quelles.
- Historique du bug : la v0.1.0 reecrivait par index d entree parsee
  applique aux lignes brutes -> tout decalage (ligne vide, invalide, CRLF)
  ecrasait/decollait des entrees et l ecriture etait perteuse (corruption
  du registre-usages-outils le 2026-08-16, ~115 entrees perdues dont
  generateurs-amelioration). Corrige en v0.1.1.
- Apres correction, relancer `analyser-noms-maj --zone registre` : le
  verdict doit etre PROPRE.
