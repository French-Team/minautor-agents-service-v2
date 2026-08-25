---
identite:
  type: rapport
  appartient_a: atlas
  date: 2026-08-24
  statut: definitif
  categorie: exploration-dossier
---

# DOSSIER : freelance/routines/

> Exploration du dossier `cerveau-projet/freelance/routines/`.
> Chaque fichier : nom, role, ce qu il fait.

## Contenu du dossier (7 fichiers)

| Fichier | Role | Ce qu il fait |
|---|---|---|
| `README.md` | Index routines | Explique le systeme de surveillance d EDITH : scripts mecaniques (sans LLM) executes par le mini serveur routines-server selon le manifest.json (D15). Regles : les routines lisent/observent sans modifier, une alerte = rapport + message P1, le serveur n active jamais un agent, ajouter une routine = editer manifest.json. |
| `manifest.json` | Manifest D15 | Quelles routines tournent quand + seuils d alerte : intervalle boucle 600s, routines demarrage (verifier-integrite), arret (detecter-orphelins), surveillance (surveiller-flux-jarvis 600s, surveiller-modifications 60s, evaluer-agents 600s), seuils (p1_non_acquitte, inbox_croissance_par_heure=20, modification_perimetre_edith), perimetre edith surveille = tools-commun/routines-server/. |
| `etat-executions.json` | Etat des executions | Dernieres executions des routines (surveiller-flux-jarvis, surveiller-modifications, evaluer-agents a 18:08:35 le 23/08). |
| `demarrage/` | Routines de demarrage | VIDE -- script verifier-integrite.py attendu (manifest le reference). |
| `arret/` | Routines d arret | VIDE -- script detecter-orphelins.py attendu (manifest le reference). |
| `surveillance/detection.py` | Detection de modifications | Detection de changements dans le perimetre surveille. |
| `surveillance/evaluer-agents.py` | Evaluation periodique | Protocole 17 : reveil d EDITH pour le cycle d evaluation des agents (questionnaire standard, +/- points). |
| `surveillance/surveiller-flux-jarvis.py` | Surveillance flux JARVIS | Surveille les flux JARVIS (inbox, activations, files). |
| `surveillance/surveiller-modifications.py` | Detection post-modification | Protocole 18 : apres chaque modification detectee, heuristiques prudentes (niveaux comptes, header coding, caracteres interdits, valeurs en dur). |

## Notes

- Les dossiers `demarrage/` et `arret/` sont des chantiers : les scripts
  references par manifest.json n existent pas encore.
- Le systeme est mecanique : AUCUN LLM dans la boucle de collecte.
- La detection du 23/08 a produit des alertes [EDITH-REVEIL] (perimetre
  modifie, P1 non-acquitte chez stark) -- voir routines-server/observations/.
