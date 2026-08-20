# Rapport -- Controle final chronometre + integration activation

**Date** : 2026-08-19
**Agent** : Janus (controle croise)
**Mission** : controle final de la chaine Vulcain (construction) ->
Morpheus (garde-fou) -> Janus (controle). Outil chronometrer-duree
v0.1.0 + integration activer-agent-principal v0.5.16.

## Resultat : VALIDE

Non-regression complete : **126/126 OK** (6 profils)
- cartes : 27/27
- outils : 36/36
- tests : 23/23 (apres correction, voir ci-dessous)
- fiches-agents : 17/17
- docs : 5/5
- registre : 18/18

evaluer-processus : 0 probleme de processus
mermaid : 16/16 cartes synchronisees

## BUG CRITIQUE detecte et CORRIGE

**Parse de la duree (activer-agent-principal v0.5.16)** : la 1re
non-regression (profil tests) a revele 2 KO sur test-098 :
- 'table sans repere ### au-dessus' (3 cas)
- 'ligne orpheline: === MESSAGES POUR L AGENT ===' (3 cas)

**Cause racine** : arreter_chrono_session faisait
`sortie.split("|")[1].strip()` mais la sortie de chronometrer-duree est
`agent | duree` SUIVIE des MESSAGES POUR L AGENT sur les lignes
suivantes. Le strip recuperait donc les messages, qui etaient inseres
dans le repere ### de AGENTS-historique (3 lignes parasites par relais).

**Correction** :
- .py : prendre la 1re ligne apres le | (`parties[1].strip().split("\n")[0]`)
- .sh : `echo "$sortie" | head -1`

**Purge** : les messages parasites de la 1re activation reelle (bloc
morpheus 19:22) retires a la main + parentheses du repere fermees.

**Preuve post-correction** : cycle complet py + sh sur copie ->
`cerberus (1s)` / `cerberus (3s)` propres, 0 message parasite, 0 KO.

## Corrections Morpheus verifiees

1. Chemin parents[4] : chronos.jsonl ecrit au bon endroit (traces/), le
   chrono reel fonctionne (preuve : morpheus 9min 11s dans le repere).
2. consulter-combos v0.1.1 : tri du registre maintenu apres journalisation.
3. evaluer-processus v0.1.10 : chronometrer-duree en OUTILS_P0_PARTAGES
   (transverse appele par activer-agent-principal - faux positif
   DECLARATION_FAUTIVE corrige).

## Preexistants (pas des regressions)

- valider-conformite-ascii crashe sur l emoji du dictionnaire-emojis.txt
  (fichier legitime de l outil corriger-emojis, 1171 octets non-ASCII
  identiques au HEAD) - a signaler pour une future mission.
- docs externes non-ASCII (amelioration-philosophie.md, analyse-externe.md)
- evaluer-structure avec chemins obsoletes (pense-betes/regles-immuables)

## Chaine

Vulcain (construction) -> Morpheus (garde-fou) -> Janus (controle) ->
Cerberus (bilan consolide)
