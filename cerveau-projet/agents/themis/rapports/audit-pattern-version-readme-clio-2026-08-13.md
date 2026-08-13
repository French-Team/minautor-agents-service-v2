# Controle croise : Pattern version README dans la fiche clio

**Date** : 2026-08-13
**Auditeur** : Themis
**Mission** : documenter la convention de bump de version dans clio.md

## Verifications

| Point | Resultat |
|---|---|
| T1. Section PATTERN VERSION README complete (sources + bump + combo + garde-fous + anti-residus) | OK |
| T2. Version fiche 0.2.1 (frontmatter + tableau, plus de 0.2.0) | OK |
| T3. verifier-conformite-fiche --agent clio CONFORME (section specifique toleree) | OK |
| T4. Normes clio.md 0/0 | OK |
| T5. Parcours clio intact (c6c) + sources intactes (0.2.0 / stable) | OK |

## Verdict

**VALIDE** (5/5 points verts). La fiche clio documente desormais la
convention de maintenance de la version du README : sources de verite
(version-readme.txt, statut-projet.txt), regle de bump a chaque grosse MAJ,
lien avec aligner_badges_header, garde-fous test-038/039, anti-residus.
