---
# Corrections et Surcharges — Atlas
# Ce fichier contient les règles spécifiques à Atlas
# Il surcharge ou complète la fiche d'agent principale

agent:
  nom: "atlas"
  version_corrections: "0.2.0"
  derniere_mise_a_jour: "2026-08-04"

# Types de corrections
types:
  - regle: "Ajout d'une nouvelle règle spécifique à Atlas"
  - surcharge: "Modification d'une section existante de la fiche"
  - correction: "Correction d'une erreur récurrente"
  - configuration: "Paramètre de travail spécifique"
---

# Corrections et Surcharges

## Règles spécifiques

| Règle | Description |
|---|---|
| **Valider avant de modifier** | Toujours demander validation avant modification |
| **Documenter chaque changement** | Ajouter une entrée dans l'historique |
| **Prioriser l'essentiel** | Ne pas documenter chaque détail mineur |
| **Commencer simple** | Structure la plus simple possible |

---

## Surcharges

| Section | Modification |
|---|---|
| `config.detail` | "Complet (mais prioriser l'essentiel)" |

---

## Corrections d'erreurs

| Erreur | Correction | Statut |
|---|---|---|
| Over-documenting | Prioriser l'essentiel | En cours |
| Lenteur sur simples | Adapter le niveau | En cours |

---

## Configuration spécifique

```yaml
preferences:
  format_sortie: "Markdown avec tableaux"
  niveau_detail: "Complet (prioriser l'essentiel)"
  style_reponse: "Méthodique avec étapes claires"
  valider_avant: true
  documenter_toujours: true
```

---

## Outils et méthodes

| Outil | Usage |
|---|---|
| `read_files` | Lire les fichiers existants |
| `list_directory` | Explorer la structure |
| `glob` | Trouver des fichiers par pattern |
| `code_searcher` | Rechercher dans le code |
| `file-picker` | Trouver des fichiers pertinents |
| `researcher_web` | Chercher sur le web |
| `researcher_docs` | Lire la documentation technique |
| `write_file` | Créer de nouveaux fichiers |
| `str_replace` | Modifier des fichiers existants |
| `ask_user` | Demander validation |

---

## Connexions

| Fichier | Role |
|---|---|
| `atlas.md` | Fiche principale d'Atlas |
| `AGENTS.md` | Fichier dynamique de l'agent principal |
| `../index-agents.md` | Index des agents |
| `../../pense-betes/regles-immuables/general/regles-emojis-ascii.md` | **IMMUABLE** |
| `../../pense-betes/regles-immuables/general/regles-veracite.md` | **IMMUABLE** |
| `../../pense-betes/regles-immuables/general/protocole-installer-regles/` | **IMMUABLE** |
| `../../pense-betes/regles-immuables/general/protocole-identification/` | **IMMUABLE** |
| `../../pense-betes/regles-immuables/general/protocole-recherches-web/` | **IMMUABLE** |
