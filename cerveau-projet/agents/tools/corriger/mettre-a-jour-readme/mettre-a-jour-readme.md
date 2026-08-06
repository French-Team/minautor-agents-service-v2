# mettre-a-jour-readme

**Version :** 0.2.0-beta
**Statut :** ebauche
**Categorie :** Corriger
**Chemin :** `agents/tools/corriger/mettre-a-jour-readme/`
**Proprietaire :** Clio (agent dedie au README)

## Description

Corriger le README pour qu'il reflete l'etat reel du projet.

> **PHILOSOPHIE — LE README EST LE LIVRE DU PROJET** : le README est la voix du projet, pas un carnet de suivi. Quand on ajoute, modifie ou supprime quelque chose (agent, outil, fonction), le **texte existant du README doit etre corrige** pour parler de la realite. L'outil ne fait JAMAIS d'ajout de lignes d'historique ou de chronologie.

## Utilisation

```bash
# Verifier les ecarts entre l'etat reel et le README (dry-run)
mettre-a-jour-readme.sh --verifier

# Corriger le texte du README (tables, compteurs)
mettre-a-jour-readme.sh --maj

# Consulter les interventions recentes pour savoir CE QUI A CHANGE (diagnostic)
mettre-a-jour-readme.sh --journal

# Compter les agents reels
mettre-a-jour-readme.sh --agents

# Compter les outils reels par categorie
mettre-a-jour-readme.sh --outils
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--verifier` | Comparer l'etat reel au README, lister les ecarts sans modifier | - |
| `--maj` | Corriger le texte du README (agents, outils, compteurs) | - |
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
4. **Rapporte** - Les ecarts detectes et les corrections appliquees

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
| `modifier-agents-md` | Met a jour AGENTS-historique.md (source de diagnostic) |
| `lister-agents` | Verifier les agents listes |
| `lister-outils` | Verifier les outils listes |
| `rechercher-*` | Verifier les documents par type |
