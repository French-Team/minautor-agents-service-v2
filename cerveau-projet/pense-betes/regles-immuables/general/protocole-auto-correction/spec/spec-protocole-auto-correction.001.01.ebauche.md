# Spécification — Protocole d'Auto-Correction des Agents
---

## Objectif

Définir un système permettant aux agents de :
1. S'identifier de manière unique
2. Corriger automatiquement leurs erreurs
3. Surcharger leur configuration sans impacter les autres
4. Devenir l'agent principal dynamiquement

---

## Architecture

```
projet-futur/
├── AGENTS.md                    ← fichier dynamique (agent principal)
├── cerveau-projet/
│   └── agents/
│   ├── index-agents.md          ← point d'entrée
│   ├── fiche-agent-template.md  ← template de fiche
│   ├── corrections-template.md  ← template de corrections
│   └── [nom-agent]/
│       ├── [nom-agent].md       ← fiche de l'agent
│       └── corrections.md       ← surcharges/corrections
```

---

## Format des fichiers

### Fiche d'agent

| Section | Format | Obligatoire |
|---|---|---|
| En-tete YAML | YAML | [OK] |
| Vue d'ensemble | Markdown | [OK] |
| Specialites | Markdown | [OK] |
| Forces | Tableau | [OK] |
| Faiblesses | Tableau | [OK] |
| Style de travail | Markdown | [OK] |
| Limites | Liste | [OK] |
| Connexions | Tableau | [OK] |
| Historique | Tableau | [OK] |

### Corrections

| Section | Format | Obligatoire |
|---|---|---|
| En-tete YAML | YAML | [OK] |
| Regles specifiques | Markdown | [NON] |
| Surcharges | Markdown + YAML | [NON] |
| Corrections d'erreurs | Markdown | [NON] |
| Configuration specifique | YAML | [NON] |
| Statistiques | Tableau | [NON] |
| Notes de session | Markdown | [NON] |

---

## Workflow

```
1. Agent visite agents/
2. Vérifie existence de sa fiche
3. Si non → crée la fiche + corrections
4. Lit sa configuration (corrections en priorité)
5. Met à jour AGENTS.md
6. Travaille
7. Détecte erreurs → ajoute dans corrections.md
8. Prochaine session → lit les nouvelles corrections
```

---

## Règles de validation

| Règle | Critère |
|---|---|
| **Unicité** | Chaque agent a un seul dossier |
| **Autonomie** | Pas de partage de corrections |
| **Persistance** | Les corrections restent entre les sessions |
| **Dynamisme** | AGENTS.md est mis à jour à chaque session |
| **Traçabilité** | L'historique est conservé |

---

## Dépendances

| Dépendance | Type |
|---|---|
| `agents/` | Dossier obligatoire |
| `AGENTS.md` | Fichier obligatoire |
| Templates | Fichiers obligatoires |
| Convention protocoles | Référence |
| `protocole-installer-regles` | Protocole pour installer les règles immuables |
| `protocole-recherches-web` | Protocole pour les recherches web |

---

## Statut

- [rechercher] [OK] Dependances identifiees
- [verifier] [NON] Structure validee
- [analyser] [NON] Coherence verifiee
- [valider] [NON] Approuve
