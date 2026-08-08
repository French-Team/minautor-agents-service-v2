---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# evaluer-conventions

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** evaluer
**Chemin :** `agents/tools/evaluer/evaluer-conventions/`
**Proprietaire :** Themis (outil partage)

## Description

Evalue le respect des conventions : nommage, ASCII, format.

## Utilisation

```bash
bash evaluer-conventions.sh [DOSSIER]
# Version Python (recommandee)
python3 evaluer-conventions.py [DOSSIER]
```

## Ce qu'il verifie

- Nommage des statuts (pas d'accents dans les statuts de fichiers)
- Conformite ASCII (hors exceptions declarees)
- Bandeaux EXCEPTION VOLONTAIRE sur les dictionnaires
- Exclusion du dossier exemples par les outils
- Format des fichiers agents (chaque agent a sa fiche)

## Sortie

Rapport markdown sur stdout avec score /100.

## Code retour

| Code | Signification |
|---|---|
| 0 | Le dossier cible existe (meme avec des ecarts de conventions signales) |
| 1 | Le dossier cible n'existe pas |

## Dependances

- bash, grep, sed (outils systeme standard)

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-06 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter ajoute, VERSION 0.2.0, en-tete standardise. Bug corrige : motif '\\.(prepare|prepare)\\.' a alternatives identiques (faux positif) remplace par detection Python des noms non-ASCII |
| 0.2.0-py | 2026-08-07 | Version Python creee (rapport markdown identique, --version) |

---
