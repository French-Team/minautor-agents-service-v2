---
identite:
  type: test
  appartient_a: morpheus
  commun: false
---
# test-020-combos-clio

**Version :** 1.0
**Proprietaire :** Morpheus (protocole-tests)
**Cree le :** 2026-08-10
**Cible :** les 3 combos Clio (massive v0.1.1) (test reel de la grosse MAJ du README)

## Description

Test formel des 3 combos crees pour Clio (Pattern 3) :

| Combo | Format | Role |
|---|---|---|
| `combos-analyse-projet` | orchestre py/sh/md | etat reel du projet + ecarts README vs realite |
| `combo-maj-readme` | encapsule definition-combo.json (5 cases) | PETITE MAJ (verifier -> maj -> ascii) |
| `combos-maj-readme-massive` | orchestre py/sh/md | GROSSE MAJ conservative (badge auto) |

## Cas couverts (11)

1. Nommage : py/sh/md des 2 orchestres + definition-combo.json
2. Versions des 3 combos (0.1.0 / 0.1.1)
3. JSON valide (nom, version, case_depart c1, 5 cases)
4. combos-analyse-projet : execution reelle (ETAT REEL + ECARTS + agents + outils)
5. combos-maj-readme-massive : execution reelle (etapes 1-5 + synthese conservative)
6. combos-moteur --liste : cases c1..c5
7. dry-run c2=OUI : verifier -> maj -> ascii -> FIN c5
8. dry-run c2=NON : verifier -> ascii -> FIN c5 (sans maj)
9. Parite .sh : les 2 .sh orchestres deleguent au .py
10. ASCII : 0 non-ASCII sur les 7 fichiers
11. LF pur : 0 CRLF sur les 7 fichiers

## Usage

```bash
python3 test-020-combos-clio.py
```

## Note

Le test execute les combos SANS `--rapport` (aucune creation de fichier dans
`clio/rapports/` pendant les tests). La re-numerotation : test-020 (le test-019
est le dernier existant).
