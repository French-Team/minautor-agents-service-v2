# Controle croise final : non-regression passee a 5 series

**Date** : 2026-08-13
**Controleur** : Janus
**Verdict Themis** : VALIDE (T1-T5)

## Verifications

| Point | Resultat |
|---|---|
| J1. Lanceur : 5 cles SERIES, ordre a-e, choices 6 valeurs (2 copies identiques) | OK |
| J2. Doc md : tableau 5 series + option --series <a,b,c,d,e,tous> | OK |
| J3. test-027 + garde-fous globaux (023/024/025/027) en serie D | OK |
| J4. Normes ASCII/LF 0/0 + aucune reference residuelle a|b|c|d / 4 series | OK |
| J5. Non-regression complete : 40/40 OK (45.2s, conforme reference 44.7s, +1%) | OK |

## Verdict

**VALIDE** (J1-J5 verts). Le passage de 4 a 5 series est conforme et la
suite est stable : pool 36/36 + garde-fous globaux 4/4 = 40/40 OK.
