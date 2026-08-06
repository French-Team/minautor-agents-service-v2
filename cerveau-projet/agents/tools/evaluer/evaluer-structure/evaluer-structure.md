# evaluer-structure

Evalue la structure du cerveau-projet : dossiers, fichiers critiques, arborescence.

## Usage

```bash
bash evaluer-structure.sh [DOSSIER]
```

## Ce qu'il verifie

- Dossiers critiques (agents, tools, pense-betes, conventions, etc.)
- Fichiers critiques (demarrer.md, AGENTS.md, README.md, etc.)
- Categories d'outils (valider, explorer, corriger, analyser, etc.)
- Dossiers de chaque agent
- Contenu des categories (pas vides)

## Sortie

Rapport markdown sur stdout avec tableau de statuts (OK/ERREUR/AVERTISSEMENT) et score /100.

## Dependances

- bash, find, wc (outils systeme standard)
