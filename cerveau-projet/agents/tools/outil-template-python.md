---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# outil-template-python

**Categorie** : Template
**Version** : 0.3.0-beta
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

## REGLE IMMUABLE : protections + options on/off + chrono (v0.1.1)

> **REGLE ABSOLUE (demande utilisateur 2026-08-13)** : TOUT outil Python DOIT
> embarquer le TRIPLET (voir protocole-outils Regle 9) :
>
> 1. **Protections** : `verifier_nommage`, validation des arguments, `--dry-run`
> 2. **Options on/off** : flags pour isoler/desactiver une fonction ou un workflow
>    complet (`--activer`/`--desactiver`, `--isoler N`) sans toucher au code
> 3. **Chrono** : option standard `--chrono` (mesure de duree d execution,
>    bilan en fin) ; `--no-chrono` pour couper
>
> Les durees mesurees alimenteront les futurs outils de suivi. Le template
> `outil-template.py` fournit `--chrono` dans `construire_parser()`.

---

## REGLE IMMUABLE : messages informationnels (v0.3.0, demande utilisateur)

> **REGLE ABSOLUE (demande utilisateur 2026-08-17)** : TOUT outil qui
> ecrit/modifie dans le projet DOIT afficher des MESSAGES INFORMATIONNELS
> dans sa sortie, aux endroits importants : l agent voit TOUJOURS les
> consequences de son action (fichiers compagnons a mettre a jour, regles
> a respecter, etapes suivantes) sans avoir a les deviner.
>
> Le template fournit `afficher_messages_info(messages)` :
> - affiche une section `=== MESSAGES POUR L AGENT ===` avec une ligne
>   ` > ` par message ;
> - l appel est OBLIGATOIRE en fin de main() apres une action reussie
>   (et non dry-run) ;
> - les messages sont TOUJOURS affiches (pas une option) : c est le
>   contrat informationnel.

Exemple (outil qui modifie un fichier) :

```python
if not args.dry_run:
    afficher_messages_info([
        "fichier modifie : indexer dans index-tools.md",
        "fichier modifie : adapter les tests (Morpheus)",
        "fichier modifie : mettre a jour la version (bumper)",
    ])
```

Le precedent existe deja : `mettre-a-jour-versions` affiche
`FICHIERS COMPAGNONS A METTRE A JOUR`, `generateurs-case` affiche des
`RAPPEL ASCII/RVAV/DELEGATION`.

---

## Mesure des tokens (PILOTE, migration progressive v0.1 - optionnel)

> Volet "mesure de la fenetre de contexte" (demande utilisateur 2026-08-15).
> Les outils Python peuvent rendre compte de leur consommation de tokens via
> `analyser-tokens` (modele hybride : registres locaux + compteurs API si
> disponibles). PILOTE optionnel : aucun outil existant n est migre tant que
> le pilote n est pas valide par un test dedie.

## Structure du fichier .py

```
#!/usr/bin/env python3
# -*- coding: ascii -*-
# [nom-outil].py
# [Description courte]
# Version : 0.2.0-beta
# Statut : ebauche

import argparse, os, sys
from pathlib import Path

VERSION = "0.2.0-beta"
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
| `--chrono` | Mesurer la duree d execution (bilan en fin ; `--no-chrono` pour couper) |

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
| 0.3.0-beta | 2026-08-17 | REGLE IMMUABLE messages informationnels : fonction afficher_messages_info (section MESSAGES POUR L AGENT, lignes ' > ') - demande utilisateur, les outils passent des messages contextuels aux agents dans leur sortie |
| 0.2.0-beta | 2026-08-14 | REGLE IMMUABLE documentation obligatoire : bloc DOC OBLIGATOIRE (verifier_doc_presente + exiger_confirmation_doc + --doc + --confirme-doc) - demande utilisateur, severite bloquante |
| 0.1.1-beta | 2026-08-13 | REGLE IMMUABLE protections + options on/off + chrono : option standard `--chrono` (mesure de duree, bilan en fin) - demande utilisateur |
| 0.1.0-beta | 2026-08-07 | Creation initiale : template Python generique (argparse, nommage, couleurs, dry-run) |

---

## Notes

- Le .sh et le .py coexistent dans le meme dossier (aucun ne remplace l'autre)
- Le template .py est la REFERENCE pour toutes les conversions a venir
- Voir aussi : `outil-template.md` (version bash), `outil-template.sh` (script bash)

---
