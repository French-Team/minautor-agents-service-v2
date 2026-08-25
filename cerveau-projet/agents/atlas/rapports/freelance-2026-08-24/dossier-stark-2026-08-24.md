---
identite:
  type: rapport
  appartient_a: atlas
  date: 2026-08-24
  statut: definitif
  categorie: exploration-dossier
---

# DOSSIER : freelance/stark/

> Exploration du dossier `cerveau-projet/freelance/stark/` (agent Stark).
> Chaque fichier : nom, role, ce qu il fait.

## Contenu du dossier (5 fichiers)

| Fichier | Role | Ce qu il fait |
|---|---|---|
| `stark.md` | Fiche agent (198 lignes) | Carte d identite de Stark (D17) : grade gold, medailles (pionnier-marvel, coordinateur-chef, createur-jarvis), notation 90, mot-cles. Role : Tony Stark, createur de JARVIS, coordinateur de l equipe freelance. Sans JARVIS il ne peut rien faire. |
| `corrections.md` | Corrections (73 lignes) | Lecons de Stark : 2 lecons d ERREUR (2026-08-22 et 23) -- "Stark a fait le travail lui-meme" : il ne doit JAMAIS executer le travail des autres, il coordonne via JARVIS (regle M2). |
| `parcours/arbre-stark.json` | Arbre racine | Racine : "Quel theme ?" -> JARVIS (OBLIGATOIRE pour toute mission) / LIRE / EXPLORER. Fins centralisees dans fins.json. |
| `parcours/theme-jarvis.json` | Theme JARVIS | But : envoyer la demande a JARVIS qui traite et distribue. REGLE ABSOLUE : Stark n appelle JAMAIS jarvis.py activer, SEUL JARVIS distribue. |
| `parcours/theme-lire.json` | Theme LIRE | Consulter l activite, les messages JARVIS, l etat de l equipe. |
| `parcours/theme-explorer.json` | Theme EXPLORER | Diagnostiquer un probleme. |
| `parcours/fins.json` | Fins centralisees | Toutes les fins possibles (fin-theme, fin-stark via JARVIS). |

## Notes

- Stark est le coordinateur : il ne construit pas (Shuri), il ne teste pas
  (Forge), il coordonne GRACE a JARVIS.
- FIN DE CYCLE : Stark reactive Cerberus (reactiver, pas activer).
- Sans JARVIS, Stark ne fait RIEN (dependance structurelle).
