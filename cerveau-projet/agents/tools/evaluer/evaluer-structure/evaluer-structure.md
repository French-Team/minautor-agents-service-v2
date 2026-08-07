# evaluer-structure

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** evaluer
**Chemin :** `agents/tools/evaluer/evaluer-structure/`
**Proprietaire :** Themis (outil partage)

## Description

Evalue la structure du cerveau-projet : dossiers, fichiers critiques, arborescence.

## Utilisation

```bash
bash evaluer-structure.sh [DOSSIER]
# Version Python (recommandee)
python3 evaluer-structure.py [DOSSIER]
```

## Ce qu'il verifie

- Dossiers critiques (agents, tools, pense-betes, conventions, etc.)
- Fichiers critiques (demarrer.md, AGENTS.md, README.md, etc.)
- Categories d'outils (valider, explorer, corriger, analyser, etc.)
- Dossiers de chaque agent
- Contenu des categories (pas vides)

## Sortie

Rapport markdown sur stdout avec tableau de statuts (OK/ERREUR/AVERTISSEMENT) et score /100.

## Code retour

| Code | Signification |
|---|---|
| 0 | Le dossier cible existe (meme avec des erreurs structurelles signalees) |
| 1 | Le dossier cible n'existe pas |

## Dependances

- bash, find, wc (outils systeme standard)

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-06 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter ajoute, VERSION 0.2.0, en-tete standardise |
| 0.2.0-py | 2026-08-07 | Version Python creee (rapport markdown identique, --version) |

---
