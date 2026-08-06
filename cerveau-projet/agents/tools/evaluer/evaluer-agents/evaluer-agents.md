# evaluer-agents

Evalue le comportement des agents : respect des protocoles, outils, fiches.

## Usage

```bash
bash evaluer-agents.sh [DOSSIER]
```

## Ce qu'il verifie

- Chaque agent a une fiche ($agent.md)
- Chaque agent a corrections.md
- Chaque outil est complet (.sh + .md)
- Tous les agents sont declares dans AGENTS.md
- L'agent actif est Cerberus

## Sortie

Rapport markdown sur stdout avec score /100.
