---
identite:
  type: outil
  appartient_a: commun
  commun: true
  combos:
    - combos-audit-general
---
# evaluer-agents

**Version :** 0.2.3
**Statut :** prepare
**Categorie :** evaluer
**Chemin :** `agents/tools/evaluer/evaluer-agents/`
**Proprietaire :** Themis (outil partage)

## Description

Evalue le comportement des agents : respect des protocoles, outils, fiches.

## Utilisation

```bash
bash evaluer-agents.sh [DOSSIER]
# Version Python (recommandee)
python3 evaluer-agents.py [DOSSIER]
```

## Ce qu'il verifie

- Chaque agent a une fiche ($agent.md)
- Chaque agent a corrections.md
- Chaque outil est complet (.sh + .md)
- Tous les agents sont declares dans AGENTS.md
- L'agent actif est Cerberus

## Sortie

Rapport markdown sur stdout avec score /100.

## Code retour

| Code | Signification |
|---|---|
| 0 | Le dossier cible existe (meme avec des ecarts signales) |
| 1 | Le dossier cible n'existe pas |

## Dependances

- bash, grep, sed (outils systeme standard)

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-06 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter ajoute, VERSION 0.2.0, en-tete standardise |
| 0.2.0-py | 2026-08-07 | Version Python creee (rapport markdown identique, --version) |
| 0.2.1 | 2026-08-07 | Correction: exclusion des dossiers `__pycache__` (artefacts Python) et des dossiers de categorie du scan des outils incomplets. Score corrige de 23/100 a 96/100. |
| 0.2.1-py | 2026-08-07 | Version Python corrigee (parite sh/py) |
| 0.2.2 | 2026-08-08 | CONVENTION IDENTIFICATION : verification de l'agent actif sur le champ **Nom Agent** (ancien **Nom** accepte en repli -- le grep 'Nom' matcherait desormais **Nom LLM** en premier). py + sh + doc |

---
