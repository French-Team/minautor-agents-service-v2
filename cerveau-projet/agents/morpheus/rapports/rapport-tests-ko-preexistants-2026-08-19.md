# Rapport Morpheus -- Correction des 4 KO tests preexistants

**Date** : 2026-08-19
**Mission** : Corriger les KO preexistants de la non-regression (domaine tests) : test-030, test-024, test-063, test-087.

## Corrections

| Test | Defaut | Correctif |
|---|---|---|
| test-030 (protections) | test-093 n'importait pas les protections + subprocess.run brut | Bloc `PROTECTIONS = charger_protections()` ajoute + `lancer()` passe par `PROTECTIONS.lancer_protege` |
| test-024 (scripts temp) | Pin editer-parcours v0.1.6 obsolete | Pin mis a jour -> v0.1.7 |
| test-063 (profils) | test-092 + test-093 orphelins | Ajoutes au profil `tests` de profils-tests.json |
| test-087 (tags) | `parite-agents` (092) + `dry-obligatoire` (093) hors taxonomie | Remplaces par `garde-fou-agent` (092) + `preuve-negative` (093) |

## Verification

| Test | Avant | Apres |
|---|---|---|
| test-030 | KO (2) | **10 OK / 0 KO** |
| test-024 | KO (1) | **17 OK / 0 KO** |
| test-063 | KO (1) | **11 OK / 0 KO** |
| test-087 | KO (1) | **8 OK / 0 KO** |
| test-092 | -- | **9 OK / 0 KO** |
| test-093 | -- | **17 OK / 0 KO** |

Normes : ASCII 0 / LF 0 sur les 4 fichiers modifies + profils-tests.json.

## Lecon

Un test qui lance des commandes DOIT importer les protections (bloc standard
test-030) et passer par `lancer_protege` ; ses tags doivent appartenir a la
taxonomie ; il doit etre reference dans profils-tests.json.
