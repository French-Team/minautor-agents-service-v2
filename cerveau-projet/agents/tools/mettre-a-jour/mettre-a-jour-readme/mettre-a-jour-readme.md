---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# mettre-a-jour-readme

**Version :** 0.4.0
**Statut :** prepare
**Categorie :** mettre-a-jour
**Chemin :** `agents/tools/mettre-a-jour/mettre-a-jour-readme/`
**Proprietaire :** Clio (agent dedie au README)

## Description

Corriger le README pour qu'il reflete l'etat reel du projet, et inserer un logo et des badges en tete.

> **PHILOSOPHIE -- LE README EST LE LIVRE DU PROJET** : le README est la voix du projet, pas un carnet de suivi. Quand on ajoute, modifie ou supprime quelque chose (agent, outil, fonction), le **texte existant du README doit etre corrige** pour parler de la realite. L'outil ne fait JAMAIS d'ajout de lignes d'historique ou de chronologie.

## Utilisation

Version Python (recommandee) :

```bash
# Verifier les ecarts entre l'etat reel et le README (dry-run)
python3 mettre-a-jour-readme.py --verifier

# Corriger le texte du README (tables, compteurs)
python3 mettre-a-jour-readme.py --maj

# Inserer une image (logo) en tete du README, apres le titre H1
python3 mettre-a-jour-readme.py --logo <chemin-image>

# Inserer des badges statiques Shields en tete (label=message:couleur;...)
python3 mettre-a-jour-readme.py --badges "Plateforme=Windows:blue;Statut=stable:brightgreen"

# Consulter les interventions recentes pour savoir CE QUI A CHANGE (diagnostic)
python3 mettre-a-jour-readme.py --journal

# Compter les agents reels
python3 mettre-a-jour-readme.py --agents

# Compter les outils reels par categorie
python3 mettre-a-jour-readme.py --outils
```

Version bash equivalente : `mettre-a-jour-readme.sh` (meme logique).

## Options

| Option | Description | Defaut |
|---|---|---|
| `--verifier` | Comparer l'etat reel au README, lister les ecarts sans modifier | - |
| `--maj` | Corriger le texte du README (agents, outils, compteurs) | - |
| `--logo CHEMIN` | Inserer une image (logo) en tete du README, apres le titre H1 (idempotent) | - |
| `--badges SPEC` | Inserer des badges statiques Shields en tete (format `label=message:couleur;...`), apres le titre H1 (idempotent) | - |
| `--journal [N]` | Consulter les N dernieres interventions (diagnostic, NON inscrit au README) | 10 |
| `--agents` | Afficher le compte reel des agents | - |
| `--outils` | Afficher le compte reel des outils par categorie | - |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. **Consulte** - Les interventions de `AGENTS-historique.md` pour savoir CE QUI A CHANGE
2. **Compare** - L'etat reel (agents, outils par categorie) avec le contenu du README
3. **Corrige** - Le texte existant du README :
   - Table des agents : ajoute les agents manquants
   - Boite a outils : corrige les compteurs par categorie et le total
   - Liste des outils : ajoute les outils manquants dans leur categorie
4. **Logo** - Insere une image (`--logo`) juste apres le titre H1 du README, au format
   d'une image Markdown (texte alternatif "Logo" + chemin fourni a l'option,
   chemin et texte alternatif en ASCII, regle immuable). Idempotent :
   si le chemin est deja present, rien n'est insere.
5. **Badges** - Insere des badges statiques Shields (`--badges`) juste apres le titre H1,
   au format `label=message:couleur` separes par `;`. Chaque badge est une image
   Markdown liee (clic) vers `img.shields.io/badge/...?style=flat`. ASCII strict
   (label, message, couleur), idempotent (aucun doublon), absence de H1 et spec
   invalide geres (exit 1).
6. **Rapporte** - Les ecarts detectes et les corrections appliquees

## Ce que l'outil ne fait JAMAIS

- Il n'ajoute AUCUNE section de chronologie ou d'historique au README
- Il n'empile PAS de lignes d'interventions
- Il ne touche pas aux descriptions redigees (la voix du livre est preservee)

## Sources de verite

| Source | Utilisation |
|---|---|
| `agents/` | Agents reels et leurs roles (lus dans les fiches) |
| `agents/tools/[categorie]/` | Outils reels par categorie |
| `AGENTS-historique.md` | Diagnostic : ce qui a change (jamais affiche dans le README) |

## Exemples de sortie

```bash
$ mettre-a-jour-readme.sh --verifier

=== ETAT REEL DU PROJET ===

Agents reels : 10

Outils par categorie :
  explorer      : 12
  ...
  TOTAL         : 52

=== ECARTS AVEC LE README ===

  [OK] Tous les agents sont dans la table
  [OBSOLETE] Titre : 'La boite a outils (51 outils)' -> devrait etre 52
  [OBSOLETE] Corriger : README dit 9, reel = 10
  ...

Utilisez --maj pour corriger le texte du README.
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Apres chaque mission** | Clio lance `--verifier` puis `--maj` apres chaque retour d'agent |
| **Ajout/modification du projet** | Nouvel agent, nouvel outil, nouvelle structure |
| **Avant une session** | Verifier que le README reflete l'etat reel |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `activer-agent-principal` | Met a jour AGENTS-historique.md (source de diagnostic) |
| `lister-agents` | Verifier les agents listes |
| `lister-outils` | Verifier les outils listes |
| `rechercher-*` | Verifier les documents par type |

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0-beta | 2026-08-06 | Version precedente (beta) |
| 0.2.0 | 2026-08-07 | Promotion prepare : passage v2 final |
| 0.2.0-py | 2026-08-07 | Version Python creee (mettre-a-jour-readme.py), basee sur outil-template.py. Portage fidele : verifier/maj/journal/agents/outils, cas speciaux tester/combos/templates, reconstruction des lignes outils en 3 colonnes |
| 0.3.0 | 2026-08-07 | Ajout option `--logo CHEMIN` : inserer une image (logo) en tete du README, apres le titre H1. Idempotent (aucun doublon), fichier manquant et absence de H1 geres (exit 1). Ajoute dans les versions Python (0.3.0-py) et bash (0.3.0) |
| 0.4.0 | 2026-08-07 | Ajout option `--badges SPEC` : inserer des badges statiques Shields en tete du README (format `label=message:couleur;...`), apres le titre H1. Images Markdown liees (clic) `img.shields.io/badge/...?style=flat`. Encodage espace/tiret, validation ASCII stricte (label, message, couleur), idempotent, spec invalide et absence de H1 geres (exit 1). Base : recherche Atlas (recherches-web/badges-github-shields/). Versions Python (0.4.0-py) et bash (0.4.0) |
