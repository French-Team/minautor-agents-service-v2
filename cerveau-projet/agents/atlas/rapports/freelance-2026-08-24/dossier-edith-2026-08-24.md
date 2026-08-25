---
identite:
  type: rapport
  appartient_a: atlas
  date: 2026-08-24
  statut: definitif
  categorie: exploration-dossier
---

# DOSSIER : freelance/edith/

> Exploration du dossier `cerveau-projet/freelance/edith/` (agent EDITH).
> Chaque fichier : nom, role, ce qu il fait.

## Contenu du dossier (6 fichiers)

| Fichier | Role | Ce qu il fait |
|---|---|---|
| `edith.md` | Fiche agent (108 lignes) | Carte d identite d EDITH (D17) : grade silver, medaille (observatrice), notation 85, statut DORMANTE. Role : observatrice HORS-ROUND, son serveur de routines vit H24 (collecte + alertes mecaniques), elle dort jusqu a son reveil puis analyse les observations et rapporte les 4 W (qui/quoi/comment/quand). |
| `corrections.md` | Corrections (22 lignes) | Contexte de creation, regles, philosophie. |
| `parcours/arbre-edith.json` | Arbre racine | Racine : themes (LIRE, OBSERVER, RAPPORTER). |
| `parcours/theme-lire.json` | Theme LIRE | Lire les observations accumulees. |
| `parcours/theme-observer.json` | Theme OBSERVER | Observer (via le serveur, sans LLM). |
| `parcours/theme-rapporter.json` | Theme RAPPORTER | Rapporter les 4 W a l utilisateur via JARVIS. |
| `parcours/fins.json` | Fins centralisees | fin-theme, fin-stark via JARVIS. |
| `rapports/suivi-stark-20260823-1347.md` | Suivi de score Stark | Score 49/100, penalite -1 (travaille seul sans activation tracee), revision NON requise. |
| `rapports/suivi-vision-20260823-1347.md` | Suivi de score Vision | Score 49/100, penalite -1 (round ouvert sans bilan tardif), revision NON requise. |

## Notes

- EDITH ne participe JAMAIS aux rounds : lecture seule, elle signale, ne
  repare pas.
- Son serveur (routines-server) detecte, constitue le rapport forensique et
  depose le message P1 [EDITH-REVEIL] dans l inbox de stark.
- Protocole 16 (cellule dormante) + protocole 17 (evaluation periodique).
