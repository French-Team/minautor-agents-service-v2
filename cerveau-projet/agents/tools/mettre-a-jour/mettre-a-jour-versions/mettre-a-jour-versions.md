# mettre-a-jour-versions

**Categorie** : Mettre a jour
**Version** : 0.1.6
**Statut** : ebauche
**Agent** : Vulcain
**Date** : 2026-08-15

Le **bumper systematique** : met a jour la version d'une cible sur TOUS ses
fichiers porteurs de version, en un seul passage, avec detection automatique
de la version actuelle, dry-run par defaut et verification de coherence
post-bump.

---

## Objectif

Repondre au besoin des agents : "bump de version facile et systematique".
Les bumps manuels sont partiels et repetitifs : une spec oubliee, un en-tete
perime, un compteur de test casse. Ce bumper garantit que TOUS les fichiers
d'une cible portent la MEME version, avant et apres le bump.

## Formats de version supportes

| Format | Exemple (versions fictives X.Y.Z) |
|---|---|
| Outil .py : en-tete + constante | `# Version : X.Y.Z` + `VERSION = "X.Y.Z"` |
| Outil .sh : en-tete + variable | `# Version : X.Y.Z` + `VERSION="X.Y.Z"` |
| Outil .md / spec .md | `**Version :** X.Y.Z` ou `**Version** : X.Y.Z` (les 2 formats sont couverts) |
| Parcours JSON | `"version": "X.Y.Z"` |
| Fiche agent | `PARCOURS (vX.Y.Z)` |
| Protocole (frontmatter) | `version: "X.Y.Z"` |
| version-readme.txt | `X.Y.Z` |
| Catalogue JSON | `"version": "X.Y.Z"` |

## Cibles

| Cible | Exemple |
|---|---|
| Dossier d'outil (py + sh + md + spec) | `mettre-a-jour-versions.py cerveau-projet/agents/tools/editer/editer-fichier/` |
| Parcours d'agent (JSON + fiche) | `mettre-a-jour-versions.py --parcours cerberus` |
| Protocole | `mettre-a-jour-versions.py --protocole <chemin>` |
| version-readme.txt | `mettre-a-jour-versions.py --version-readme` |
| Catalogue | `mettre-a-jour-versions.py --catalogue` |
| Fichier generique | `mettre-a-jour-versions.py <fichier>` |

## Nouvelles versions

| Mode | Resultat |
|---|---|
| (defaut) | bump PATCH : X.Y.Z -> X.Y.(Z+1) |
| `--nouvelle X.Y.Z` | version explicite |
| `--mineure` | X.(Y+1).0 |
| `--majeure` | (X+1).0.0 |

## Securite

- **Dry-run par defaut** : affiche `ancienne -> nouvelle` par fichier, ne
  modifie RIEN. `--wet` applique reellement.
- **Incoherence detectee avant bump** : si des fichiers de la cible portent
  des versions differentes, KO signale avec le detail par fichier et motif.
- **Verification post-bump** : apres `--wet`, relit tous les fichiers et
  verifie que tous portent la nouvelle version (verdict OK/KO).

## Usage

```
python3 mettre-a-jour-versions.py cerveau-projet/agents/tools/editer/editer-fichier/
python3 mettre-a-jour-versions.py --parcours cerberus --wet
python3 mettre-a-jour-versions.py --catalogue --nouvelle 0.3.0
python3 mettre-a-jour-versions.py --protocole <chemin> --mineure
python3 mettre-a-jour-versions.py --version-readme --wet
python3 mettre-a-jour-versions.py <fichier> --verbose
python3 mettre-a-jour-versions.py --tous              # audit de TOUS les outils
python3 mettre-a-jour-versions.py --tous --wet        # corrige les incoherences
```

Options : `--wet`, `--nouvelle`, `--mineure`, `--majeure`, `--verbose`,
`--rapport <fichier>`, `--version`.

## Mode --tous (audit global des versions)

Scanne TOUS les dossiers outils (`cerveau-projet/agents/tools/*/*/`) et
verifie la coherence des versions par outil. La version de reference est la
constante `VERSION` du `.py` (source de verite a jour) ; les en-tetes `.py`,
les `.sh` et la doc `.md` doivent etre alignes dessus.

- Par defaut (dry-run) : audite et liste les incoherences (verdict KO si
  ecarts, sans rien modifier).
- `--wet` : corrige les en-tetes/versions perimes en les alignant sur la
  reference (le suffixe `-py`/`-sh`/`-beta` est conserve).
- Ne scanne QUE les fichiers principaux d un outil (basename == nom du
  dossier) : les fichiers auxiliaires (`tester-*.sh`, `*-test.md`, `spec/`)
  portent leurs propres versions documentaires et ne sont PAS touches.
- `--rapport <fichier>` : ecrit un rapport markdown de l audit.

## Exemptions documentees (audit --tous)

Quand un fichier compagnon porte VOLONTAIREMENT une version inferieure a la
reference (equivalent PARTIEL : les fonctionnalites recentes du `.py` ne
concernent pas ce format), l audit le compte en **EXEMPT** au lieu de
INCOHERENT. Liste dans `EXEMPTIONS_AUDIT` (chemin, version pinnee, raison).

- **Regle** : une exemption sans raison ecrite dans le code ET dans le
  changelog de l outil concerne = bug de version, pas une exemption.
- **Version pinnee** : si le fichier est bumpe sans retirer l exemption, il
  redevient INCOHERENT (l exemption ne vaut que pour la version documentee).
- Exemple : `activer-agent-principal.sh` (v0.7.4) est l equivalent bash
  PARTIEL du .py (v0.8.2) : les fonctions 0.7.5+ (encart
  AGENTS-activite-recente.md, BDD SQLite, colonnes Grade/Secteur/Debut-Fin)
  sont cote .py uniquement (changelog v0.7.5 : "Parite .sh : non concerne").

## Limites

- Ne gere pas les fichiers de version non standard (uniquement les 8 formats
  ci-dessus). Un fichier sans motif reconnu est signale en KO.
- Le bump catalogue doit rester coherent avec les compteurs de tests
  (test-005/test-007) : apres un bump de version du catalogue, verifier la
  non-regression.

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.6 | 2026-09-02 | EXEMPTIONS .sh PARTIELS ANTI-HEREDOC (round vestiges v1 / non-regression) : creer-fichier.sh (0.3.2), ecrire-fichier.sh (0.3.2) et editer-fichier.sh (0.5.0) declares EXEMPT - les modes anti-heredoc (--contenu-chemin / --remplacements-chemin) sont cote .py uniquement, bumper les .sh serait un mensonge de version. Meme precedent qu activer-agent-principal.sh (0.7.4). Raisons documentees au changelog de chaque outil. |
| 0.1.5 | 2026-08-18 | RESYNC CARTES-LOCK APRES BUMP CARTE (lecon 2026-08-18, cas themis v0.4.10) : un bump --parcours ecrit la carte JSON HORS editer-parcours, ce qui faisait diverger l empreinte de cartes-lock.json et BLOQUAIT toute ecriture ulterieure de la carte par l anti-contournement. Ajout de resynchroniser_cartes_lock (empreinte normalisee LF+rstrip strictement identique a editer-parcours) appellee apres chaque bump --parcours --wet reussi. |
| 0.1.4 | 2026-08-17 | FORMATS .md INVISIBLES COUVERTS (demande utilisateur audit croise) : le motif md_version ne couvrait QUE '**Version :** X.Y.Z' en debut de ligne - les .md en TABLEAU ('| **Version** |'), BLOCKQUOTE ('> **Version** :'), LISTE ('- Version :' / '- **X.Y.Z**') ou section '## Version' etaient declares 'coherent' sans verification. Extension du motif aux 4 formats (priorite au champ standard, toujours en tete). 2 vrais ecarts caches corriges (generateurs-carte .md 0.3.0 -> 0.3.1, generateurs-ligne .md 0.3.1 -> 0.3.0) + 7 .md normalises en champ standard (valider-case, tester-protections, editer-fichier-agents, evaluer-processus, detecter-evaluations-incompletes, verifier-conformite-fiche, generateurs-amelioration). |
| 0.1.3 | 2026-08-16 | PRECISION DES COMPAGNONS : exclusion des corrections.md (lecons des agents = mentions historiques, jamais des pins a adapter - faux positifs du round 0.5.2) + RAPPEL OBLIGATOIRE dans le rapport : lancer le bumper sur chaque outil bumpe AVANT la non-regression (lecon : 5 KO en cascade car le bump 0.5.2 n avait pas ete precede du bumper) |
| 0.1.2 | 2026-08-16 | FICHIERS COMPAGNONS : apres un bump, signale les fichiers du projet qui referencent l ancienne version (tests, docs, corrections) avec verdict KO + detection des 2 formats de doc ('**Version :**' et '**Version** :') - a revele et corrige 11 outils incoherents (19 remplacements) |
| 0.1.0 | 2026-08-15 | Creation : bumper systematique multi-formats (outil, parcours, protocole, catalogue, version-readme) |
