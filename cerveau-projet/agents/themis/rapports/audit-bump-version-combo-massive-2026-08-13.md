# Controle croise : bump version du combo massive

**Date** : 2026-08-13
**Auditeur** : Themis
**Mission** : le combo combos-maj-readme-massive doit bumper la version du
README dans son rapport quand le README change

## Verifications

| Point | Resultat |
|---|---|
| T1. Combo v0.1.3 : bumper_version + lire_version + snapshot + bump avant badge | OK |
| T2. Rapport : etape 3b + synthese + Contexte mentionnent la version | OK |
| T3. test-020 46/46 OK (adapte 0.1.2 -> 0.1.3) | OK |
| T4. version-readme.txt reel intact (0.2.0, pas de bump README a jour) | OK |
| T5. Normes 0/0 + doc/sh coherents (0.1.3) | OK |

## Verdict

**VALIDE** (5/5 points verts). Le combo bumpe la version MINEURE de la source
de verite quand le README change (detection par snapshot), AVANT d aligner les
badges, et le rapport (console + fichier) mentionne l ancienne -> nouvelle
version ou "inchangee".
