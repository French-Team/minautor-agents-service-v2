# creer-remplir-todo

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** Creer
**Chemin :** `agents/tools/creer/creer-remplir-todo/`
**Proprietaire :** outil partage

## Description

Remplit les sections d'un todo **sans ouvrir le fichier**. L'agent donne la section et le contenu en arguments, l'outil insere le contenu a la bonne place. Complement de `generateurs-squelette-todo` (qui genere la structure) : cet outil cree le contenu des phases.

## Utilisation

```bash
# Remplir le titre
creer-remplir-todo.sh todo-pipeline.001.01.ebauche.md titre "Todo du pipeline"

# Remplir le statut de l'intervention
creer-remplir-todo.sh todo-pipeline.001.01.ebauche.md statut "| **Pense-bete** | cree | [lien] |"

# Remplir une phase (multiligne avec \n)
creer-remplir-todo.sh todo-pipeline.001.01.ebauche.md phase5 "1. Creer le pipeline\n2. Documenter les resultats"

# Remplir l'historique
creer-remplir-todo.sh todo-pipeline.001.01.ebauche.md historique "| 2026-08-06 | Phase 5 | Creation | [OK] |"

# Apercu sans modifier
creer-remplir-todo.sh todo-pipeline.001.01.ebauche.md phase5 "Mon contenu" --dry-run
```

## Arguments

| Argument | Description |
|---|---|
| `fichier` | Chemin du todo a remplir |
| `section` | Section a remplir (voir liste) |
| `contenu` | Contenu a inserer (entre guillemets) |

## Sections disponibles

| Section | Cible |
|---|---|
| `titre` | Titre du todo |
| `statut` | Tableau Statut de l'intervention |
| `phase0` | Phase 0 -- Activation de l'agent |
| `phase1` | Phase 1 -- Analyse de la demande |
| `phase2` | Phase 2 -- Verification du cerveau |
| `phase3` | Phase 3 -- Recherches |
| `phase4` | Phase 4 -- Preparation des outils |
| `phase5` | Phase 5 -- Developpement |
| `phase6` | Phase 6 -- Tests et validation |
| `phase7` | Phase 7 -- Controle secondaire |
| `phase8` | Phase 8 -- Finalisation |
| `phase9` | Phase 9 -- Reactivation de Cerberus |
| `historique` | Tableau Historique |
| `notes` | Section Notes |
| `liens` | Section Liens |

## Ce que l'outil fait

1. **Valide** - La section est connue, le fichier existe
2. **Localise** - Trouve le marqueur de la section dans le fichier
3. **Detecte** - La prochaine section (pour delimiter le remplacement)
4. **Remplace** - Insere le contenu entre la section et la suivante
5. **Protege** - Ne modifie que la section visee, le reste est intact

## Exemples de sortie

```bash
$ creer-remplir-todo.sh todo-pipeline.001.01.ebauche.md phase5 "1. Creer le pipeline"
[OK] Section 'phase5' remplie dans todo-pipeline.001.01.ebauche.md
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Passage todo -> contenu** | Remplir les phases apres generation du squelette |
| **Suivi de mission** | Mettre a jour les phases au fil de l'avancement |
| **Correction d'une phase** | Re-remplir une phase avec le nouveau contenu |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `generateurs-squelette-todo` | Genere le squelette avant de remplir |
| `remplir-pense-bete` | Meme logique pour les pense-betes |
| `remplir-spec` | Meme logique pour les specs |
| `valider-pense-bete` | Modele pour creer un validateur de todo |
