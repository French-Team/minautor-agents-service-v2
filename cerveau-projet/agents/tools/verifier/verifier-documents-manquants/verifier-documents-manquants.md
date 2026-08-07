# verifier-documents-manquants

**Version :** 0.2.0-py
**Statut :** prepare
**Categorie :** verifier
**Chemin :** `agents/tools/verifier/verifier-documents-manquants/`
**Proprietaire :** Buffy (outil partage)

## Description

Verifier que chaque script `.sh` a sa documentation `.md` correspondante dans le meme dossier, et inversement. Tout outil du cerveau-projet doit etre compose d'un script (`.sh`) et de sa documentation (`.md`). Si l'un des deux manque, l'outil le signale.

## Utilisation

```bash
# Verifier dans le dossier courant
verifier-documents-manquants.sh

# Verifier les outils
verifier-documents-manquants.sh cerveau-projet/agents/tools/

# Verifier seulement les .sh sans .md
verifier-documents-manquants.sh --sh-sans-md cerveau-projet/agents/tools/

# Verifier seulement les .md sans .sh
verifier-documents-manquants.sh --md-sans-sh cerveau-projet/agents/tools/

# Inclure aussi les fichiers speciaux (spec/, test-*, index-*, templates)
verifier-documents-manquants.sh --inclure-speciaux cerveau-projet/agents/tools/

# Avec details
verifier-documents-manquants.sh --verbose cerveau-projet/
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--sh-sans-md` | Verifier les .sh sans .md correspondant | on |
| `--md-sans-sh` | Verifier les .md sans .sh correspondant | on |
| `--inclure-speciaux` | Inclure spec/, test-*, index-*, *template* | false |
| `--dry-run` | Simuler sans rien modifier | false |
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. **Scan** - Trouve tous les fichiers `.sh` du dossier
2. **Verifie** - Pour chaque `.sh`, cherche le `.md` du meme nom dans le meme dossier
3. **Scan inverse** - Trouve tous les fichiers `.md` et cherche leur `.sh`
4. **Rapporte** - Liste les documents manquants avec un code de sortie non-zero si probleme

## Definition de "manquant"

| Type | Condition | Exemple |
|---|---|---|
| **Script sans doc** | Un `.sh` existe mais pas de `.md` du meme nom | `tester-protection-blocage.sh` sans `tester-protection-blocage.md` |
| **Doc sans script** | Un `.md` existe mais pas de `.sh` du meme nom | Documentation orpheline |

## Faux positifs ignores (par defaut)

Les fichiers suivants sont des documents de **support** qui n'ont pas besoin d'un script correspondant :

| Type | Exemple | Raison |
|---|---|---|
| `spec/` | `spec-verifier-systeme.001.01.ebauche.md` | Specifications, pas des docs d'outil |
| `test-*.md` | `test-mettre-a-jour-agents-md.md` | Fichiers de test |
| `index-*.md` | `index-tools.md` | Index de navigation |
| `*template*.md` | `template-test.md` | Templates de creation |

Utiliser `--inclure-speciaux` pour tout verifier sans exception.

## Exemples de sortie

```bash
$ verifier-documents-manquants.sh cerveau-projet/agents/tools/

=== Verification des documents manquants ===
Dossier : cerveau-projet/agents/tools/

--- Scripts .sh sans documentation .md ---
  [MANQUANT] cerveau-projet/agents/tools/tester/protections/tester-protection-blocage/tester-protection-blocage.sh
  [MANQUANT] cerveau-projet/agents/tools/tester/protections/tester-protection-boucles-infinies/tester-protection-boucles-infinies.sh
  [MANQUANT] cerveau-projet/agents/tools/tester/protections/tester-protection-erreurs-silencieuses/tester-protection-erreurs-silencieuses.sh
  -> 3 script(s) sans documentation

--- Documentation .md sans script .sh ---
  -> 0 documentation(s) sans script

=== Resume ===
Scripts .sh : 32
Documentations .md : 37
Documents manquants : 3

[ATTENTION] Des documents manquants ont ete detectes
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Audit des outils** | Detecter les outils incomplets (script sans doc ou doc sans script) |
| **Apres creation d'outil** | Verifier que le nouvel outil est complet (script + doc) |
| **Controle de qualite** | Garantir que chaque outil est documente et fonctionnel |
| **Avant test** | Verifier qu'aucun script n'est orphelin avant de tester |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `rechercher-fichiers-vides` | Verifier que les .md trouves ne sont pas vides |
| `rechercher-templates` | Verifier les templates (dont le outil-template) |
| `valider-conformite-ascii` | Verifier la conformite ASCII des documents |
| `lister-outils` | Voir la liste complete des outils |

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0-beta | 2026-08-06 | Version precedente (beta) |
| 0.2.0 | 2026-08-07 | Promotion prepare : passage v2 final |
