# Controle Janus - Regle stricte scripts dedies (.agents-tmp)

**Date** : 2026-08-13
**Mission controlee** : Buffy -> Themis (demande utilisateur : les .tmp continuaient d etre crees a la racine)
**Verdict** : **VALIDE** (J1-J5)

## J1. Protocole v0.2.3 (4/4)

- version 0.2.3 + regle stricte (JAMAIS de script temporaire a la racine)
- 0 tolerance racine residuelle (autorisee/tolere/exception absents)
- .agents-tmp partout (20+ mentions : deux usages, spawn_agents, procedure, pieges, RVAV)
- spawn_agents : ECRIRE dans `.agents-tmp/.tmp-<agent>-<sujet>.py`

## J2. Dossier dedie + garde-fous (4/4)

- .gitignore : .agents-tmp/ present
- test-024 : 13/13 OK (dossier invisible pour le scan racine)
- test-039 (residus version racine) + test-041 (outils critiques) verts

## J3. Normes

- protocole : ASCII strict 0/0 + LF pur 0/0

## J4. Residus

- 0 residu racine + .agents-tmp/ vide (commande directe)

## J5. Non-regression complete

- **44/44 OK** -- nouvelle base chrono 44.3s (43 -> 44 tests, test-044 ajoute)

## Synthese

La regle stricte est restauree et PROUVEE : protocole v0.2.3, dossier dedie
.agents-tmp/ (gitignore, invisible pour test-024), 0 .tmp a la racine.
Le point de bascule (v0.2.0 2026-08-13 20:44 / v0.2.2 21:18) est documente.
La pratique est adoptee immediatement par tous les agents (scripts de mission
dans .agents-tmp/).
