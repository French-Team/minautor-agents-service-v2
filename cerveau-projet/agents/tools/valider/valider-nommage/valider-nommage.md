---
identite:
  type: outil
  appartient_a: commun
  commun: true
  tags: validation, nommage, communs
---
# valider-nommage

**Version :** 0.3.1-py
**Statut :** prepare
**Categorie :** Valider
**Chemin :** `agents/tools/valider/valider-nommage/`
**Proprietaire :** outil partage

## Description

Verifier que le nommage des fichiers respecte les conventions du cerveau-projet.
Inclut la verification du **prefixe du dossier** pour les outils (regle immuable)
et le mode **--mots-seuls** (regle fondamentale "aucun mot seul").

## Utilisation

```bash
# Valider un seul outil
valider-nommage.sh --type outil chemin/vers/outil.sh

# Valider un protocole
valider-nommage.sh --type protocole chemin/vers/protocole.md

# Valider TOUS les outils d'un dossier (mode recursif)
valider-nommage.sh --recursive cerveau-projet/agents/tools/

# Regle fondamentale 'aucun mot seul' sur un fichier
valider-nommage.sh --mots-seuls cerveau-projet/agents/cerberus/cerberus.md

# Regle fondamentale sur tout un dossier (recursif)
valider-nommage.sh --mots-seuls --recursive cerveau-projet/agents/

# Avec details
valider-nommage.sh --recursive --verbose cerveau-projet/agents/tools/
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--type TYPE` | Type de fichier : protocole, convention, agent, outil | - |
| `--recursive, -r` | Valider tous les outils d'un dossier (ignore --type) | false |
| `--mots-seuls` | Regle fondamentale 'aucun mot seul' (YAML/JSON) | false |
| `--verbose, -v` | Afficher les details | false |
| `--help, -h` | Afficher l'aide | - |
| `--version` | Afficher la version | - |

## Mode --mots-seuls (regle fondamentale)

Applique la **REGLE FONDAMENTALE** (convention-renommage.md) :
**tout identifiant doit etre compose d'au moins 2 mots**
(nom-agent, role-agent, statut-cerberus, id-llm...).

Le mode detecte les **identifiants generiques a un seul mot** dans les blocs
YAML d'identification (`agent:`, `profil:`, `identite:`, `session:`) et les
objets JSON equivalents :

| Cle interdite | Doit devenir |
|---|---|
| `nom` | `nom-agent` |
| `role` | `role-agent` |
| `statut` | `statut-<agent>` |
| `id` | `id-llm` |
| `date` | `date-mise-a-jour` |
| `cible` | `cible-audit` |

**Autorisees** (ne sont pas des identifiants) :
- Exceptions structurelles : `type`, `commun`, `tags`, `appartient_a`
- Cles de schema de fiche : `version`, `cree`, `specialites`, `forces`, `faiblesses`...

En mode recursif, les **dossiers de traces historisees** sont ignores :
`controles/`, `rapports/`, `retro-actions/`, `historique/`, `exemples/`
(documents figes qui documentent d'anciennes conventions).

## Types de fichiers

| Type | Format attendu | Exemple |
|---|---|---|
| `protocole` | `nom-protocole.XX.XX.statut.md` | `protocole-outils.001.01.ebauche.md` |
| `agent` | `nom-agent.md` | `buffy.md` |
| `outil` | `nom-outil.sh`, `nom-outil.py` ou `nom-outil.md` | `lire-fichier.sh` |
| `convention` | `convention-nom.md` | `convention-renommage.md` |

## Regle du prefixe dossier (outils)

**REGLE IMMUABLE** : le nom d'un outil DOIT commencer par le prefixe du dossier parent.

- `lire/lire-fichier/` -> `lire-fichier.sh` 
- `rechercher/rechercher-extension-fichier/` -> `rechercher-extension-fichier.sh` 
- `corriger/corriger-dictionnaire-accents/` -> `corriger-dictionnaire-accents.sh` 
- `copier/copier-fichier/` -> `copier-fichier.py` (version Python)

**Regle sans exclusion** : tous les dossiers d'outils suivent cette regle, y compris `generateurs/`, `combos/` et `tester/` (tout a ete renomme avec le prefixe du dossier).

## Mode recursive

Le mode `--recursive` valide tous les outils d'un dossier :
- Valide les fichiers `.sh`, `.py` et `.md` de premier niveau
- Ignore les **sous-dossiers composants** d'un outil : `tests/`, `spec/`,
  `protections/` et `__pycache__/` (leurs fichiers ont leur propre convention
  de nommage : `test-NNN-*`, `spec-*.XX.XX.ebauche.md`)
- Affiche un resume : total, OK, erreurs

```bash
$ valider-nommage.sh --recursive cerveau-projet/agents/tools/
=== Resume ===
  Total : 154
  OK : 154
  Erreurs : 0
```

## Sortie

| Code retour | Signification |
|---|---|
| `0` | Tous les fichiers sont conformes |
| `N` | N fichiers avec des erreurs |

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| Avant de creer un nouvel outil | `valider-nommage.sh --type outil mon-outil.sh` |
| Audit de conformite du dossier tools/ | `valider-nommage.sh --recursive cerveau-projet/agents/tools/` |
| Apres un renommage d'outil | `valider-nommage.sh --recursive --verbose cerveau-projet/agents/tools/creer/` |

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-05 | Creation initiale |
| 0.2.0 | 2026-08-05 | Ajout de la verification du prefixe dossier (regle immuable) |
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels (outil conforme OK, outil sans prefixe detecte), exclusions obsoletees retirees, promotion prepare |
| 0.2.1 | 2026-08-07 | Ajout du support des fichiers `.py` (format + prefixe dossier + mode --recursive) |
| 0.3.0 | 2026-08-08 | Ajout du mode `--mots-seuls` (regle fondamentale : identifiants generiques a un seul mot interdits dans les blocs YAML/JSON, exceptions structurelles et cles de schema autorisees, dossiers de traces ignores en recursif) |
| 0.3.1 | 2026-08-08 | Correction du bruit du scan `--recursive` : les sous-dossiers composants d'un outil (`tests/`, `spec/`, `protections/`, `__pycache__/`) ne sont plus traites comme de faux outils (leurs fichiers `test-*`/`spec-*` etaient signales en ERREUR de prefixe a tort). Parite py/sh |

## Notes de creation

- [x] L'outil a ete teste en `--recursive` sur tools/ (154 fichiers, 0 erreur)
- [x] L'outil est conforme ASCII
- [x] L'outil est reference dans `index-tools.md`
- [x] L'outil est assigne a un agent dans sa carte de decision
- [x] Le statut est passe a `prepare` apres passage V2 (tests reels, doc alignee)
