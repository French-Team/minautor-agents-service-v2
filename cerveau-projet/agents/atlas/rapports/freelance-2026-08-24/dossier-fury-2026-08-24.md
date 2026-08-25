---
identite:
  type: rapport
  appartient_a: atlas
  date: 2026-08-24
  statut: definitif
  categorie: exploration-dossier
---

# DOSSIER : freelance/fury/

> Exploration du dossier `cerveau-projet/freelance/fury/` (agent Fury).
> Chaque fichier : nom, role, ce qu il fait.

## Contenu du dossier (10 fichiers)

| Fichier | Role | Ce qu il fait |
|---|---|---|
| `fury.md` | Fiche agent (138 lignes) | Carte d identite de Fury (D17) : grade silver, medaille (testeur-reel), notation 85. Role : Nick Fury, directeur du SHIELD, testeur reel HORS-ROUND. Il prend la place de l utilisateur pour lancer des scenarios qui declenchent des rounds reels. |
| `corrections.md` | Corrections (45 lignes) | Contexte de creation, regles specifiques, philosophie, lecons. |
| `parcours/arbre-fury.json` | Arbre racine | Racine : themes (LIRE, RAPPORTER, TESTER). |
| `parcours/theme-lire.json` | Theme LIRE | Lire les scenarios et l etat. |
| `parcours/theme-rapporter.json` | Theme RAPPORTER | Rendre compte a JARVIS avec le lien du rapport. |
| `parcours/theme-tester.json` | Theme TESTER | Lancer les scenarios de test reels. |
| `parcours/fins.json` | Fins centralisees | fin-theme, fin-stark via JARVIS. |
| `rapports/rapport-test-inter-round-2026-08-23.md` | Test inter-round | PASSE (6/6 maillons) : flux inter-round Vision -> Rogers -> Vision. |
| `rapports/rapport-test-parallel-2026-08-23.md` | Test parallel | PASSE : 2 missions independantes en parallel (rogers + shuri). |
| `rapports/rapport-test-protocole13-2026-08-23.md` | Test protocole 13 | PASSE : declencheurs [attention] + [urgent] + files d attente. |
| `rapports/rapport-test-rating-nommage-2026-08-23.md` | Test rating + nommage | PASSE (5/5) : rating-agents + nommage. |
| `rapports/rapport-audit-fins-2026-08-23.md` | Audit fins | CONFORME AVEC RESERVES (0 violation grave, 5 mentions a enrichir). |
| `rapports/scenario-parallel-reel.json` | Scenario parallel reel | 2 missions reelles (rogers + shuri) lancees en parallel. |
| `tools/lanceur-scenario.md` | Doc lanceur | Mode d emploi du lanceur de scenarios. |
| `tools/lanceur-scenario.py` | Lanceur (v0.1.0) | Lance les scenarios de test (rounds reels stark -> jarvis -> agents -> jarvis -> stark). |
| `tools/scenario-exemple.json` | Scenario exemple | Mini-round exemple (stark -> jarvis -> stark). |
| `tools/scenario-inter-round.json` | Scenario inter-round | Scenario du flux inter-round (vision -> rogers -> vision). |

## Notes

- Fury ne fait JAMAIS partie d un round : il observe et teste hors-round.
- Ses rapports ont TOUS un verdict PASSE -- la couche mecanique de la v2
  (activations, files, inter-round, parallel, rating) est operationnelle.
- Devise : "Je ne suis jamais dans le field. Je lance les operations et je
  rends compte."
