# Rapport Vulcain -- Correction bug multi-sessions trouver_session_agent

## Mission
Corriger le bug detecte par Janus au controle final D6 : la commande
suggeree par proteger-verrou-habilitation visait la mauvaise session quand
2 sessions portent le meme agent actif.

## Cause racine
`trouver_session_agent` parcourait les blocs `### Session :` d AGENTS.md
dans l ordre du FICHIER et retournait le PREMIER match. Avec AGENTS.md ou
session-llm-4 est en tete de fichier, morpheus (actif dans llm-1 ET llm-4)
resolvait vers session-llm-4 au lieu de session-llm-1 (la plus recente).

## Correctif (v0.4.1 -> v0.4.2)
- `trouver_session_agent` lit la table '## Sessions connues', filtre les
  sessions dont l Agent actif == l agent demande (insensible a la casse) et
  retourne la PLUS RECENTE (Derniere activite max).
- Fallback inchange : session_par_defaut (SESSION_LLM -> classeur -> llm-1).
- Version synchronisee : en-tete py + VERSION + doc .md.

## Tests
- test-056 : pin 0.4.1 -> 0.4.2 + NOUVEAU point 8b (chaque agent de la
  table resout vers SA session la plus recente) -> 18/18 OK.
- Simulation du cas du bug (morpheus llm-1 21:38 / llm-4 20:51 sur copie
  AGENTS.md) : resolution -> session-llm-1 (correct).
- test-028 8/8, test-035 10/10, test-067 8/8 (bumper PROPRE).
- ASCII/LF purs sur les 3 fichiers modifies.

## Lecon
Toute resolution agent -> session doit utiliser la table '## Sessions
connues' triee par Derniere activite (recence = seule source non ambigue),
jamais l ordre des blocs du fichier (independant de la recence).
