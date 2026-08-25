---
identite:
  type: rapport
  appartient_a: atlas
  date: 2026-08-24
  statut: definitif
  categorie: exploration-dossier
---

# DOSSIER : freelance/templates/

> Exploration du dossier `cerveau-projet/freelance/templates/`.
> Chaque fichier : nom, role, ce qu il fait.

## Contenu du dossier (9 fichiers)

| Fichier | Role | Ce qu il fait |
|---|---|---|
| `README.md` | Guide des templates | Source de verite pour la creation d agents v2 (Shuri suit CE template, aucune deviation) : procedure de creation d un agent, definition des themes, creation des fichiers theme et fins, regles absolues, exemple Parker. |
| `template-agent-v2.md` | Fiche agent | Template de la fiche d agent v2 (D17) : frontmatter identite (nom, version, cree, statut, grade, medaille, notation, mot-cles), sections agent/profil/config/surcharges. |
| `template-corrections-v2.md` | Corrections agent | Template des corrections d agent : fenetre glissante, contexte de creation, regles specifiques, philosophie, lecons. |
| `template-arbre-v2.json` | Arbre racine | Template de l arbre des decisions (racine) : choix du theme, branches vers theme-*.json, fins. |
| `template-theme-v2.json` | Un theme | Template d un theme : but + redirects (besoin -> action) + fin vers fins.json. |
| `template-fins-v2.json` | Fins centralisees | Template des fins : fin-theme, fin-stark (via JARVIS), fin-inter-round. |
| `template-outil-v2.md` | Contrat outil | Template du .md d un outil v2 (contrat D7) : frontmatter, vue d ensemble, commandes, regles. |
| `template-outil-v2.py` | Entry point outil | Template du script python d un outil v2 : detection RACINE via os_path (P10), chargement des donnees -data.json (D15). |
| `template-outil-v2-data.json` | Donnees outil | Template du fichier de donnees d un outil : version, description, elements. |

## Notes

- Garde par Shuri (constructrice d agents).
- Regles absolues : PAS de parcours v1, PAS de dependance v1, PAS
  d enregistrement v1, tout passe par JARVIS, theme MARVEL, D17, D15,
  UTF-8/CRLF.
- Le template est la SOURCE DE VERITE : toute deviation est interdite.
