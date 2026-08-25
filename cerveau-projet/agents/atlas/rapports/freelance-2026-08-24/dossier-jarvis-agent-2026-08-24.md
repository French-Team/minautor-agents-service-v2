---
identite:
  type: rapport
  appartient_a: atlas
  date: 2026-08-24
  statut: definitif
  categorie: exploration-dossier
---

# DOSSIER : freelance/jarvis/ (agent)

> Exploration du dossier `cerveau-projet/freelance/jarvis/` (agent JARVIS).
> Chaque fichier : nom, role, ce qu il fait.
> NOTE : ce dossier est l AGENT JARVIS ; le CODE du hub vit dans
> `tools-commun/jarvis/` (voir dossier-tools-commun).

## Contenu du dossier (7 fichiers)

| Fichier | Role | Ce qu il fait |
|---|---|---|
| `jarvis.md` | Fiche agent (143 lignes) | Carte d identite de JARVIS (D17) : grade gold, medailles (pionnier-marvel, outil-nevralgique), notation 95. Role : l intelligence derriere le serveur, transforme les demandes de Stark en missions precises pour les agents, gere les rounds, route les messages, distribue les missions. |
| `corrections.md` | Corrections (49 lignes) | Contexte de creation, regles specifiques, philosophie, lecons. |
| `parcours/arbre-jarvis.json` | Arbre racine | Racine : themes (COORDONNER, DISTRIBUER, REPONDRE, SUIVRE, TRAITER). |
| `parcours/theme-coordonner.json` | Theme COORDONNER | Coordination via le hub. |
| `parcours/theme-distribuer.json` | Theme DISTRIBUER | Distribuer les missions aux agents. |
| `parcours/theme-repondre.json` | Theme REPONDRE | Repondre aux demandes de Stark. |
| `parcours/theme-suivre.json` | Theme SUIVRE | Suivre l etat des missions et des agents. |
| `parcours/theme-traiter.json` | Theme TRAITER | Traiter les messages et les files. |
| `parcours/fins.json` | Fins centralisees | fin-theme, fin-stark via JARVIS. |

## Notes

- JARVIS est le SEUL agent autorise a activer les autres agents freelance
  (SEUL JARVIS distribue, regle M2).
- Vision est le GARDIEN EXCLUSIF de JARVIS : seul habilite a modifier
  jarvis.py / jarvis-server.py / l agent JARVIS.
- Devise : "Comme vous le souhaitez, Monsieur Stark."
