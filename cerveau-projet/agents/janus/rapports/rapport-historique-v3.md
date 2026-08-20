# Rapport controle final - Historique v0.5.15

Date : 2026-08-19 | Agent : janus

## Non-regression complete (6 profils)
- cartes : 27 OK / 0 KO
- outils : 36 OK / 0 KO
- tests : 23 OK / 0 KO
- fiches-agents : 17 OK / 0 KO
- docs : 5 OK / 0 KO
- registre : 18 OK / 0 KO
- TOTAL : 126/126 OK

## Controles globaux
- evaluer-processus : 0 probleme
- registre JSONL : 736 lignes valides / 736
- mermaid : 16 cartes synchronisees (mmd + svg)
- historique : 150 entrees au format v0.5.15 (repheres + tables)

## KO corriges en route
1. test-078 : regex de l'ancien format -> 0 activation sans KO (faux OK).
   Corrige : regex v0.5.15 + point 2 sur fixture (robuste a la purge 150).
2. Registre : declaration erronee morpheus -> tester-lancer-non-regression
   (verrou janus). Retiree -> test-037 6/6.

## Avertissements preexistants (non regresses)
- docs externes non-ASCII (amelioration-philosophie.md, analyse-externe.md)
- evaluer-structure : chemins obsoletes pense-betes/regles-immuables
