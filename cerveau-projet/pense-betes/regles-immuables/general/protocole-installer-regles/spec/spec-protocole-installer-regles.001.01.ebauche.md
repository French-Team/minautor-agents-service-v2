# Spécification — Protocole d'Installation des Règles Immuables
---

## Objectif

Garantir que chaque nouveau projet contient toutes les règles immuables fondamentales.

---

## Architecture

```
projet/
├── regles-immuables/
│   ├── index-regles-immuables.md
│   ├── general/
│   │   ├── index-regles-general.md
│   │   ├── regles-choisir-agent.md
│   │   ├── regles-validation-rigoureuse.md
│   │   ├── regles-emojis-ascii.md
│   │   ├── regles-veracite.md
│   │   └── rvav-workflow.md
│   └── hierarchie/
│       ├── index-hierarchie.md
│       └── regles-hierarchie-par-niveau.md
```

---

## Règles à installer

| Règle | Type | Obligatoire | Emplacement |
|---|---|---|---|
| `regles-choisir-agent.md` | IMMUABLE | [OUI] | `general/` |
| `regles-validation-rigoureuse.md` | IMMUABLE | [OUI] | `general/` |
| `regles-emojis-ascii.md` | IMMUABLE | [OUI] | `general/` |
| `regles-veracite.md` | IMMUABLE | [OUI] | `general/` |
| `rvav-workflow.md` | Fondamental | [OUI] | `general/` |
| `regles-hierarchie-par-niveau.md` | Fondamental | [OUI] | `hierarchie/` |

---

## Dépendances

| Règle | Dépendances |
|---|---|
| `regles-choisir-agent.md` | `agents/`, `AGENTS.md` |
| `regles-validation-rigoureuse.md` | `rvav-workflow.md` |
| `regles-emojis-ascii.md` | Aucune |
| `regles-veracite.md` | `recherches-web/`, `protocole-recherches-web/` |
| `rvav-workflow.md` | `conventions/renommage/` |
| `regles-hierarchie-par-niveau.md` | `conventions/structures/` |

---

## Workflow

```
1. Vérifier l'existence des règles
2. Copier les règles depuis le cerveau source
3. Vérifier les dépendances
4. Mettre à jour les index
5. Valider par RVAV
```

---

## Règles de validation

| Règle | Critère |
|---|---|
| **Complétude** | Toutes les règles sont présentes |
| **Intégrité** | Le contenu est identique au cerveau source |
| **Dépendances** | Toutes les dépendances sont satisfaites |
| **Index** | Tous les index sont à jour |
| **Liens** | Tous les liens sont valides |

---

## Statut

- [rechercher] [OK] Dependances identifiees
- [verifier] [NON] Structure validee
- [analyser] [NON] Coherence verifiee
- [valider] [NON] Approuve
