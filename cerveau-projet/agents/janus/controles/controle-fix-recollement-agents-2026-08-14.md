# Controle croise : fix bug de recollement activer-agent-principal v0.5.5 (2026-08-14)

**Controleur** : Janus (session-llm-1) -- chaine Cerberus -> Vulcain -> Morpheus -> Janus -> Cerberus

## Verdict : VALIDE (J1-J5)

## J1 - Outil v0.5.5 (py/sh/md/spec alignes, parite)
- --version py = v0.5.5 (prepare) | --version sh = v0.5.5 | spec = 0.5.5
- md changelog v0.5.5 ajoute

## J2 - Garde-fous de l outil
- test-008 v0.5.5 : 9/9 VALIDE (bloc corrompu 4 blocs -> 1 seul DEMARRAGE,
  Raison proprement remplacee, reactiver 0 bloc, Nom LLM preserve, normes)
- test-007 v0.5.0 : 22/22 (regression intacte)

## J3 - AGENTS.md repare
- 1 seul bloc DEMARRAGE (avant corruption : 22) | Raison = mission courante
- tableau orphelin supprime | 6 sections propres | 0 non-ascii | 0 crlf

## J4 - Tests impactes verts
- test-013 22/22 | test-025 11/11 | test-033 9/9 | test-018 13/13
- test-021 9/9 | test-035 8/8 | test-024 15/15 | test-046 13/13

## J5 - Non-regression complete (avec --agent janus)
- 52 OK / 0 KO (pool 46/46 + globaux 6/6) -- 49.1s, conforme reference (+4%)

## Decouverte
- Les dossiers tmp-* des missions terminees (tmp-cerberus/vulcain/morpheus)
  faisaient KO test-024/test-046 en non-regression : supprimes (regle :
  chaque mission supprime son dossier en fin) -> reverdis.
