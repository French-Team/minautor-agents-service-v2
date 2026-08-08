---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# outil-template-python

**Categorie** : Template
**Version** : 0.1.0-beta
**Statut** : ebauche
**Chemin** : `agents/tools/outil-template-python.md`
**Proprietaire** : Vulcain (constructeur d'outils)

---

## Description

Modele de script **Python** pour creer les versions .py des outils du cerveau-projet.
Chaque outil bash (.sh) aura une version Python (.py) dans le MEME dossier,
avec le meme nom (ex: `lire-fichier/lire-fichier.py` a cote de `lire-fichier.sh`).

---

## REGLE IMMUABLE : prefixe du dossier

Le nom du fichier .py DOIT commencer par le prefixe du dossier de categorie.
Controle automatique par `verifier_nommage()` au demarrage du script.

| Dossier | Prefixe attendu | Exemple |
|---|---|---|
| `rechercher/` | `rechercher-` | `rechercher-texte.py` |
| `lire/` | `lire-` | `lire-fichier.py` |
| `valider/` | `valider-` | `valider-nommage.py` |
| `corriger/` | `corriger-` | `corriger-accents.py` |

---

## REGLE IMMUABLE : compatibilite

| Regle | Detail |
|---|---|
| 100% stdlib Python | Aucune dependance externe (pas de pip install) |
| ASCII strict | Aucun accent, emoji ou Unicode dans le code |
| LF | Fins de ligne Unix (pas de CRLF) |
| Windows/Git Bash | `pathlib` ou `os.path`, pas de `/tmp`, encodage utf-8 explicite |
| Pas de grep -P | Interdit (incompatible Git Bash) -- utiliser Python directement |

---

## Structure du fichier .py

```
#!/usr/bin/env python3
# -*- coding: ascii -*-
# [nom-outil].py
# [Description courte]
# Version : 0.1.0-beta
# Statut : ebauche

import argparse, os, sys
from pathlib import Path

VERSION = "0.1.0-beta"
STATUT = "ebauche"

def _couleur(texte, nom): ...      # couleurs ANSI optionnelles
def verifier_nommage(script_path): # regle immuable prefixe dossier
def afficher_aide(parser): ...     # aide de l'outil
def construire_parser(): ...       # argparse + options standard
def main() -> int: ...             # point d'entree principal

if __name__ == "__main__":
    sys.exit(main())
```

---

## Options standard (presentes dans tous les outils Python)

| Option | Description |
|---|---|
| `--dry-run` | Simuler sans rien modifier |
| `--verbose` | Afficher les details |
| `--help` | Afficher l'aide |
| `--version` | Afficher la version |

Les options specifiques de chaque outil s'ajoutent dans `construire_parser()`.

---

## Utilisation

```bash
python3 agents/tools/[categorie]/[nom-outil]/[nom-outil].py [OPTIONS] [ARGUMENTS]
```

---

## Procedure de conversion (bash -> python)

1. Copier `outil-template.py` vers le dossier de l'outil avec le bon nom
2. Remplacer `[nom-outil]` et `[Description courte]`
3. Traduire la logique du .sh en fonctions Python structurees
4. Adapter `construire_parser()` aux options reelles de l'outil
5. Tester avec `python3 outil.py --dry-run` et les cas reels
6. Verifier ASCII strict, LF, `python3 -m py_compile outil.py`
7. Mettre a jour le .md de l'outil (mention de la version Python)

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-07 | Creation initiale : template Python generique (argparse, nommage, couleurs, dry-run) |

---

## Notes

- Le .sh et le .py coexistent dans le meme dossier (aucun ne remplace l'autre)
- Le template .py est la REFERENCE pour toutes les conversions a venir
- Voir aussi : `outil-template.md` (version bash), `outil-template.sh` (script bash)

---
