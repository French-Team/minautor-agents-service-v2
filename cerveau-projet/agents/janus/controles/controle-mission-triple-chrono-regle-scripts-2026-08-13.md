# Controle Janus - Mission triple (chrono template + regle immuable + scripts temporaires)

**Date** : 2026-08-13
**Mission controlee** : Buffy -> Themis -> Morpheus (demande utilisateur)
**Verdict** : **VALIDE** (J1-J5)

## J1. Versions et sections (8/8)

| Point | Resultat |
|---|---|
| J1a. template-test.md v0.3.0 (header + frontmatter) | OK |
| J1b. options on/off + chrono (--no-chrono/--isoler/--desactiver, point_actif, bilan_chrono) | OK |
| J1c. protocole-tests v0.3.1 + REGLE IMMUABLE triplet | OK |
| J1d. protocole-outils Regle 9 (IMMUABLE) | OK |
| J1e. outil-template-python v0.1.1-beta + option standard --chrono | OK |
| J1f. outil-template.py : --chrono + bloc regle | OK |
| J1g. protocole scripts temporaires v0.2.2 + deux usages distincts | OK |
| J1h. test-029 adapte au template v0.3.0 (0 v0.2.1 restant) | OK |

## J2. Tests rejoues independamment (3/3)

- test-029 : 14/14 OK (43 tests conformes au template v0.3.0)
- test-030 : 10/10 OK (protections importees intactes)
- test-028 : 8/8 OK (coherence documentaire)

## J3. Normes

- ASCII strict 0/0 + LF pur 0/0 sur les 8 fichiers modifies (7 Buffy + test-029)

## J4. Residus

- 0 residu racine en commande directe (artefact d auto-incrimination ecarte)

## J5. Non-regression complete

- **43/43 OK** -- 44.7s, conforme a la reference (44.2s, +1%)

## Synthese

Le triplet PROTECTIONS + OPTIONS ON/OFF + CHRONO est desormais la REGLE
IMMUABLE de creation de tout fichier (fonctions/tests/workflows), propagee
par les templates (test v0.3.0 + outil v0.1.1-beta) et les protocoles (tests
v0.3.1 + outils Regle 9). La contradiction scripts temporaires est levee
(jetable ephemere vs outil temporaire de mission). Aucun ecart.
