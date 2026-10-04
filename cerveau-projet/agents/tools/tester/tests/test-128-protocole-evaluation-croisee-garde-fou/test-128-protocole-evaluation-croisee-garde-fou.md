# Test 128 : Protocole Evaluation Croisee Garde-Fou

## Objectif

Verrouiller la conformite du protocole evaluation croisee v1
(`cerveau-projet/agents/regles-immuables/general/protocole-evaluation-croisee/
protocole-evaluation-croisee.001.01.ebauche.md`) cree par Buffy (mission
a42cbb38, volet 2/2 du rapport Themis 2026-09-05-1835) : structure
convention-protocoles, nommage, liens internes, normes ASCII/LF, reference
aux 3 rapports themis reels et index des regles a jour.

## Contexte

Le protocole evaluation croisee v1 etait une reference VERBALE (aucun fichier
dedie) : les rapports `themis/rapports/evaluation-croisee-periodique-*.md`
(2026-09-02 20:35, 2026-09-02 20:45, 2026-09-05 18:35) en etaient les
instances reelles. La mission a42cbb38 a cree le protocole officiel selon la
convention-protocoles. Ce test garantit que les futures evolutions du
protocole (changement de statut, ajout de sections) ne cassent pas la
convention silencieusement.

## Points verifies

| # | Verification |
|---|---|
| 1 | Le fichier protocole existe (CRITIQUE, protection STOP) |
| 2 | Nommage `[nom].[id].[class].[statut]` conforme a la convention |
| 3 | Frontmatter ferme (--- x2) |
| 3b | Frontmatter `type: protocole` + `commun: true` |
| 4 | Les 7 sections de la convention-protocoles presentes (Objectif, Prerequis, Etapes, RVAV, Exemples, Pieges courants, Liens) |
| 5 | Les 3 rapports evaluation croisee reels presents dans themis/rapports/ |
| 5b | Les 3 rapports references dans le protocole |
| 6 | index-regles-general.md reference protocole-evaluation-croisee |
| 7 | Aucun lien casse dans le protocole (evaluer-coherence) |
| 8 | ASCII strict : 0 non-ASCII (protocole + index + test) |
| 8b | LF pur : 0 CRLF (protocole + index + test) |
| 9 | PREUVE NEGATIVE : type corrompu detecte (fixture) |
| 9b | PREUVE NEGATIVE : nommage de la fixture reste conforme (le test n est pas un faux positif) |

## Resultat

- 12 OK / 0 KO (execution directe, protections importees)
- Rating : 64.5/100 (MOYEN)
- 0 residu en fin de test (fixture purgee)
- Enregistre : serie e du lanceur + profils tests/outils

## Historique

- v0.1.0 (2026-09-05) : creation (mission e52e018d, suite protocole cree par Buffy)