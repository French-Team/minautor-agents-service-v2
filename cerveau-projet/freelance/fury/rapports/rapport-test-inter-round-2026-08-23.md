# Rapport de test reel -- Flux INTER-ROUND

| Champ | Valeur |
|---|---|
| **Date** | 2026-08-23 09:17 |
| **Testeur** | Fury (hors-round) |
| **Scenario** | inter-round-vision-rogers |
| **Outil** | lanceur-scenario v0.1.0 |
| **Verdict** | **PASSE** (6/6 maillons) |

---

## Scenario teste

Le flux INTER-ROUND v2 : un agent en round (Vision) rencontre une erreur
hors-perimetre -> il active l'agent habilite (Rogers) avec son rapport
(inter-round) -> Rogers repond et reactive Vision qui REPREND son round ->
Vision cloture vers JARVIS -> JARVIS vers Stark.

## Maillons attendus vs observes

| # | Maillon | Attenu | Observe | Verdict | Preuve |
|---|---|---|---|---|---|
| 1 | stark -> jarvis | activation jarvis | bloc session = jarvis | PASSE | msg 3a06a0d6, rc=0 |
| 2 | jarvis -> vision | round principal demarre | bloc session = vision | PASSE | msg 8c86bc7d, rc=0 |
| 3 | vision -> rogers | INTER-ROUND : rapport a l'habilite | bloc session = rogers | PASSE | msg ba8377d7, rc=0 |
| 4 | rogers -> vision | fin d'inter-round : reprise | bloc session = vision | PASSE | msg 1aaa2c85, rc=0 |
| 5 | vision -> jarvis | bilan consolide | bloc session = jarvis | PASSE | msg 72aad0ad, rc=0 |
| 6 | jarvis -> stark | cloture | bloc session = stark | PASSE | msg 36c36617, rc=0 |

## Limitation honnete (V1-V4)

Ce test verifie la PARTIE MECANIQUE du flux inter-round :
routage des messages (`--activer`) et mises a jour du bloc session
AGENTS.md a chaque maillon. La DECISION LLM de declencher l'inter-round
(detection d'une erreur hors-perimetre) n'est pas simulable par script :
elle releve de l'incarnation de chaque agent et se verifie par les traces.
Le comportement LLM complet (detection -> rapport -> reprise) a deja ete
exerce dans cette meme session lors des rounds precedents (missions
Vision/Rogers du 2026-08-23).

## Conclusion

Le cablage mecanique du flux INTER-ROUND v2 est OPERATIONNEL : chaque
maillon du cycle erreur -> habilite -> reprise -> cloture est routable et
trace. Aucun defaut detecte.

## ADDITIF (2026-08-23 09:25) -- correction tracage R/IR

Defaut detecte par l utilisateur apres le premier passage : jarvis.py
tracait TOUTES les interventions en R - la colonne type ne distinguait
pas les inter-rounds. Corrige (jarvis v0.3.1 : option --type R|IR) et
scenario rejoue avec maillons 3-4 en IR : verdict PASSE 6/6, entrees
3 et 4 tracees IR dans l historique (preuves: SCENARIO-TEST maillon 3
et 4 en IR).
Complement 09:25 : l activation par relais tracait aussi R en dur -
corrige et verifie (TEST IR relais : les 2 entrees en IR).
Point ouvert : cmd_activer trace toujours R ; une activation PENDANT un
inter-round pourrait meriter IR - a arbitrer par Rogers/Stark.