---
identite:
  type: rapport
  appartient_a: atlas
  date: 2026-08-24
  statut: definitif
  categorie: exploration-dossier
---

# DOSSIER : freelance/tools-commun/

> Exploration du dossier `cerveau-projet/freelance/tools-commun/` (outils
> partages par tous les agents freelance). Responsable : Forge.
> Chaque fichier : nom, role, ce qu il fait.

## Contenu du dossier (13 sous-dossiers + README)

| Sous-dossier / fichier | Role | Ce qu il fait |
|---|---|---|
| `README.md` | Index tools-commun | Principe : outil dedie (freelance/<agent>/tools/) vs outil commun (tools-commun/). REGLE : un outil ne vit QUE dans un seul endroit (P5, SSOT). Note : le README liste des categories theoriques (activer/, lire/, consulter/, enregistrer/, valider/) ABSENTES de la structure reelle -- README en retard. |
| `os_path/` | Detection de racine (P10) | entry.py + fonctions (localiser, racine, resoudre) : trouver_racine(__file__) remonte jusqu a AGENTS.md. INTERDIT de compter les niveaux ("../.."). 5 bugs de chemin payes. |
| `encodage/` | Encodage (D4 mecanique) | entry.py lire/detecter : non_ascii, crlf, header_coding, octets. Normalise UTF-8/CRLF (D4). Contient un BOM UTF-8 en tete de son .md. |
| `exec/` | Subprocess standardise | entry.py + fonctions/lancer.py : rc + captures + timeout (douleur quoting PowerShell). |
| `horloge/` | Horodatages | entry.py + fonctions/horloge.py : formats uniques tracables. |
| `jsonl-store/` | JSONL unique | entry.py + fonctions/store.py : lire/ecrire/append (duplication x4 evitee). |
| `rappel/` | Anti-dispersion (proto 20) | entry.py + fonctions/rappels.py + rappels.json (D15) : par contexte (correction-regle, correction-outil...), l agent consulte et signale les pistes. |
| `rating-agents/` | Notation des agents (proto 17) | entry.py noter/lister/problemes + fonctions (noter, paliers, score) + notes-agents.jsonl : paliers COPPER->SILVER->OR (hausse) / A_REVOIR->A_REPARER->DECLASSE (baisse). Seuil de revision : < 40/100. |
| `defcon/` | Serveur DEFCON (proto 15) | defcon-server.py (serveur MCP dedie) : etat_defcon, changer_defcon (5->4->3->2). Demarre a l entree en DEFCON 5, stoppe au retour DEFCON 2. |
| `jarvis/` | LE HUB (voir detail ci-dessous) | jarvis.py + jarvis-server.py + inbox/outbox + files + fonctions/ + serveur/ + combos/ + historique/ + jarvis-data.json. |
| `routines-server/` | Serveur EDITH | mini serveur H24 lecture seule + observations/ (etat-empreintes.json, serveur-log.txt, serveur-log.txt.err, test-detach.log, test-survie.log, trace-debug.log). |
| `routines-server.bak-20260823-1700/` | ARCHIVE | Ancienne version du serveur de routines (remplacee : les routines vivent dans jarvis v0.9.2). A nettoyer (Hygie). |
| `securite/lecteur-de-carte/` | Controle d acces DECIDE | lecteur-de-carte.py verifier --agent --cible : ACCEDE/REFUSE (politique defaut = refuser) + cartes-data.json (D15). |
| `securite/verrou-outils/` | Controle d acces APPLIQUE | verrou-outils.py controler --agent --cible : OUVERT/REFUSE + journal JSONL + verrous-data.json (D15). Fonctionne AVEC le lecteur-de-carte (verrou applique, lecteur decide). |

## Detail : tools-commun/jarvis/ (LE HUB)

| Fichier | Role |
|---|---|
| `jarvis.py` (196 lignes) | POINT D ENTREE v0.9.0 : parsing CLI + dispatch (protocole 14). Commandes : envoyer, recu, lire, acquitter, lister, bloques, activer, historiser, mettre-en-attente, file, reprendre, stop-dev, defcon, changer-defcon, routines-etat, lancer. |
| `jarvis-server.py` (315 lignes) | Serveur MCP (Stdio) v0.9.0 : outils declaratifs qui appellent les MEMES fonctions/. |
| `jarvis.md` | Contrat (v0.5.0) : JARVIS = seul moyen de communication inter-agents. |
| `jarvis-data.json` | Donnees D15 : agents (nom, role, fiche, corrections). |
| `inbox/<agent>.jsonl` | Messages RECUS par agent (forge, fury, jarvis, rogers, shuri, stark, vision). Volumes : jarvis 114, stark 127, vision 35, rogers 25, forge 14, shuri 7, fury 5. |
| `outbox/<agent>.jsonl` | Messages ENVOYES par agent (8 agents, + edith). Volumes : jarvis 121, stark 59, vision 45, rogers 21, forge 13, fury 5, shuri 4, edith 3. Total ~598 lignes. |
| `historique/historique.jsonl` | Trace des actions JARVIS (activer, envoyer). |
| `files/defcon.jsonl` | Journal DEFCON (niveau 5, missions gelees). |
| `files/file-asap.jsonl` | File SUIVANTE/PREPAREE (declencheur [attention]). |
| `files/file-attente.jsonl` | File PRIORITAIRE/EN_ATTENTE/DEFCON5 (declencheurs [urgent]/[attente]/[stop]). |
| `fonctions/` | core, historique, messages, activations, files, defcon, routines, missions (une tache par module, proto 14). |
| `serveur/` | logique_activations, logique_files, logique_messages. |
| `combos/` | entry.py + fonctions (cherche, commun, etat, question_libre, rappelle, resume) + lib_lecture.py + protocole-placeholder.md. |
| `.bak-20260823-*` | jarvis.py.bak-1155, jarvis-server.py.bak-1155, jarvis-server.py.bak-1653 (sauvegardes proto 14, regle 1). |

## Notes

- tools-commun/ est la BIBLIOTHEQUE COMMUNE (proto 18) : chaque douleur
  subie DEUX FOIS devient un outil commun (os_path, encodage, exec,
  jsonl-store, horloge).
- La SECURITE (lecteur-de-carte + verrou-outils) est le controle d acces :
  tout outil protege DOIT passer par le verrou AVANT de s executer.
- `routines-server.bak-20260823-1700/` est une archive a nettoyer (Hygie).
- Le README de tools-commun est en retard sur la structure reelle
  (categories theoriques absentes) -- chantier documentaire.
