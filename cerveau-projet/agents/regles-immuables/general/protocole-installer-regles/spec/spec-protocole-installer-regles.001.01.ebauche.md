---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
# Specification -- Protocole d'Installation des Regles Immuables
---

## Objectif

Garantir que chaque nouveau projet contient toutes les regles immuables fondamentales.

---

## Architecture

```
projet/
|-- regles-immuables/
|   |-- index-regles-immuables.md
|   |-- general/
|   |   |-- index-regles-general.md
|   |   |-- regles-choisir-agent.md
|   |   |-- regles-validation-rigoureuse.md
|   |   |-- regles-emojis-ascii.md
|   |   |-- regles-veracite.md
|   |   ``-- rvav-workflow.md
|   ``-- hierarchie/
|       |-- index-hierarchie.md
|       ``-- regles-hierarchie-par-niveau.md
```

---

## Regles a installer

| Regle | Type | Obligatoire | Emplacement |
|---|---|---|---|
| `regles-choisir-agent.md` | IMMUABLE | [OUI] | `general/` |
| `regles-validation-rigoureuse.md` | IMMUABLE | [OUI] | `general/` |
| `regles-emojis-ascii.md` | IMMUABLE | [OUI] | `general/` |
| `regles-veracite.md` | IMMUABLE | [OUI] | `general/` |
| `rvav-workflow.md` | Fondamental | [OUI] | `general/` |
| `regles-hierarchie-par-niveau.md` | Fondamental | [OUI] | `hierarchie/` |

---

## Dependances

| Regle | Dependances |
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
1. Verifier l'existence des regles
2. Copier les regles depuis le cerveau source
3. Verifier les dependances
4. Mettre a jour les index
5. Valider par RVAV
```

---

## Regles de validation

| Regle | Critere |
|---|---|
| **Completude** | Toutes les regles sont presentes |
| **Integrite** | Le contenu est identique au cerveau source |
| **Dependances** | Toutes les dependances sont satisfaites |
| **Index** | Tous les index sont a jour |
| **Liens** | Tous les liens sont valides |

---

## Statut

- [rechercher] [OK] Dependances identifiees
- [verifier] [NON] Structure validee
- [analyser] [NON] Coherence verifiee
- [valider] [NON] Approuve
