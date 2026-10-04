---
identite:
  type: outil
  appartient_a: commun
  commun: true
  combos:
    - combo-sante-tableaux
---
# verifier-documents-manquants

**Version :** 0.3.0
**Statut :** prepare
**Categorie :** verifier
**Chemin :** `agents/tools/verifier/verifier-documents-manquants/`
**Proprietaire :** Vulcain (outil partage)

## Description

Verifier que chaque script `.sh` **et** `.py` a sa documentation `.md` correspondante dans le meme dossier, et inversement. Tout outil du cerveau-projet doit etre compose d'un script (`.sh` et/ou `.py`) et de sa documentation (`.md`). Si l'un des deux manque, l'outil le signale.

> **Pattern 9 (LIRE LE .MD AVANT USAGE)** : cet outil est le garant automatique du Pattern 9. La procedure d'audit **4g** de la spec-guider-parcours l'utilise pour verifier que le `.md` deduit existe pour CHAQUE indice outil des parcours, au lieu d'une verification manuelle.

## Utilisation

```bash
# Verifier dans le dossier courant
verifier-documents-manquants.sh

# Verifier les outils (couvre .sh ET .py)
verifier-documents-manquants.sh cerveau-projet/agents/tools/

# Verifier seulement les .sh sans .md
verifier-documents-manquants.sh --sh-sans-md cerveau-projet/agents/tools/

# Verifier seulement les .py sans .md
verifier-documents-manquants.sh --py-sans-md cerveau-projet/agents/tools/

# Verifier seulement les .md sans script (.sh ET .py absents)
verifier-documents-manquants.sh --md-sans-script cerveau-projet/agents/tools/

# Inclure aussi les fichiers speciaux (spec/, tests/, test-*, index-*, templates)
verifier-documents-manquants.sh --inclure-speciaux cerveau-projet/agents/tools/

# Avec details
verifier-documents-manquants.sh --verbose cerveau-projet/
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--sh-sans-md` | Verifier les .sh sans .md correspondant | on |
| `--py-sans-md` | Verifier les .py sans .md correspondant | on |
| `--md-sans-script` | Verifier les .md sans .sh ET sans .py | on |
| `--inclure-speciaux` | Inclure spec/, tests/, test-*, index-*, *template* | false |
| `--dry-run` | Simuler sans rien modifier | false |
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. **Scan .sh** - Trouve tous les fichiers `.sh` du dossier
2. **Scan .py** - Trouve tous les fichiers `.py` du dossier (depuis la v0.3.0)
3. **Verifie** - Pour chaque `.sh` et chaque `.py`, cherche le `.md` du meme nom dans le meme dossier
4. **Scan inverse** - Trouve tous les fichiers `.md` et cherche leur script (`.sh` OU `.py`)
5. **Rapporte** - Liste les documents manquants avec un code de sortie non-zero si probleme

## Definition de "manquant"

| Type | Condition | Exemple |
|---|---|---|
| **Script sans doc** | Un `.sh` ou `.py` existe mais pas de `.md` du meme nom | `verifier-systeme.py` sans `verifier-systeme.md` |
| **Doc sans script** | Un `.md` existe mais ni `.sh` ni `.py` du meme nom | Documentation orpheline |

## Faux positifs ignores (par defaut)

Les fichiers suivants sont des documents de **support** qui n'ont pas besoin d'un script correspondant :

| Type | Exemple | Raison |
|---|---|---|
| `spec/` | `spec-verifier-systeme.001.01.ebauche.md` | Specifications, pas des docs d'outil |
| `tests/` | `tests/tester-detecter-impacts.sh` | Dossiers de tests |
| `test-*` | `test-activer-agent-principal.md` | Fichiers de test |
| `tester-*-v0xx` | `tester-valider-nommage-v030.sh` | Scripts de test versionnes |
| `*-test.md` | `activer-agent-principal-test.md` | Documentations de test |
| `index-*.md` | `index-tools.md` | Index de navigation |
| `outils-base.md` | `agents/tools/outils-base.md` | Document de support racine |
| `*template*.md` | `template-test.md` | Templates de creation |

> **NB** : les outils reels `tester-protection-*` (dossier `tester/protections/`) restent **VERIFIES** : ils sont ecartes uniquement s'ils sont dans un dossier `tests/` ou portent une version (`-v0xx`).

Utiliser `--inclure-speciaux` pour tout verifier sans exception.

## Exemples de sortie

```bash
$ verifier-documents-manquants.sh cerveau-projet/agents/tools/

=== Verification des documents manquants (.sh + .py -> .md) ===
Dossier : cerveau-projet/agents/tools/

--- Scripts .sh sans documentation .md ---
  -> 0 script(s) .sh sans documentation

--- Scripts .py sans documentation .md ---
  -> 0 script(s) .py sans documentation

--- Documentation .md sans script (.sh ET .py absents) ---
  -> 0 documentation(s) sans script

=== Resume ===
Scripts .sh : 110
Scripts .py : 95
Documentations .md : 111
Documents manquants : 0
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Audit des outils** | Detecter les outils incomplets (script sans doc ou doc sans script) |
| **Apres creation d'outil** | Verifier que le nouvel outil est complet (script + doc) |
| **Procedure 4g (Pattern 9)** | Verifier que le `.md` deduit existe pour chaque indice outil des parcours |
| **Controle de qualite** | Garantir que chaque outil est documente et fonctionnel |
| **Avant test** | Verifier qu'aucun script n'est orphelin avant de tester |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `rechercher-fichiers-vides` | Verifier que les .md trouves ne sont pas vides |
| `rechercher-templates` | Verifier les templates (dont le outil-template) |
| `valider-conformite-ascii` | Verifier la conformite ASCII des documents |
| `guider-parcours` | Affiche LIRE AVANT USAGE : <outil.md> pour chaque indice outil |
| `lister-outils` | Voir la liste complete des outils |

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0-beta | 2026-08-06 | Version precedente (beta) |
| 0.2.0-py | 2026-08-07 | Promotion prepare : passage v2 final (py + sh heredoc) |
| 0.3.0 | 2026-08-08 | Extension aux `.py` (py sans md + md sans script), filtre elargi (tests/, tester-*-v0xx, *-test, outils-base), `.sh` converti en wrapper pur, branche dans la procedure 4g du Pattern 9 |
