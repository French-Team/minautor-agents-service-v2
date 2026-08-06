# evaluer-coherence

Evalue la coherence inter-fichiers : liens, references croisees, dossiers vides.

## Usage

```bash
bash evaluer-coherence.sh [DOSSIER]
```

## Ce qu'il verifie

- Liens internes casses ([texte](chemin) pointant vers des fichiers inexistants)
- Dossiers vides suspects (hors spec/todo/exemples)
- Agents declares dans AGENTS.md
- Outils references par les agents qui existent reelement

## Sortie

Rapport markdown sur stdout avec score /100.
