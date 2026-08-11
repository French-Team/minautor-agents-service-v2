# test-023-grep-budget-pondere.py

**Testeur** : Morpheus (testeur dedie)
**Date** : 2026-08-11
**Objet** : Test formel du GREP CROISE des seuils BUDGET PONDERE
(protocole-verification-coherence v0.2.0, etape E7) : garde-fou
non-regression automatique garantissant la coherence des 5 seuils
(100 / 0,5 / 1 / 3,0 / 160) entre specs et outils.

---

## Contexte

Test formel de la suite de non-regression (test-001 a test-023).
Ce test est reference au catalogue generateurs-commande : toute
modification de son perimetre doit etre validee par Morpheus.

Le protocole-verification-coherence v0.2.0 (etape E7) exige que les
5 seuils du budget pondere soient IDENTIQUES dans les 6 fichiers :
- 3 specs : spec-refonte-cartes-decision, spec-valider-case, spec-guider-parcours
- 1 doc d'outil : valider-case.md
- 2 codes : valider-case.py (SEUIL_COURT / BUDGET_INDICES / SEUIL_TEXTE),
  generateurs-case.py (SEUIL_COURT / BUDGET_INDICES / SEUIL_REGLE_DEFAUT)

Anti-recurrence : l'ancienne regle "> 3 indices" / "plus de 3 indices"
doit rester ABSENTE des 6 fichiers (elle decrivait l'ancien modele,
remplace par le budget pondere).

## Points couverts (26)

| # | Verification |
|---|---|
| P1-P4 | spec-refonte : '100 car' / '0,5' / '3,0' / '160' presents |
| P5-P8 | spec-valider-case : idem |
| P9-P12 | spec-guider-parcours : idem |
| P13-P16 | valider-case.md : idem |
| P17 | valider-case.py : 'SEUIL_COURT = 100' present |
| P18 | valider-case.py : 'BUDGET_INDICES = 3.0' present |
| P19 | valider-case.py : 'SEUIL_TEXTE = 160' present |
| P20 | generateurs-case.py : 'SEUIL_COURT = 100' present |
| P21 | generateurs-case.py : 'BUDGET_INDICES = 3.0' present |
| P22 | generateurs-case.py : 'SEUIL_REGLE_DEFAUT = 160' present |
| P23 | Anti-recurrence : '> 3 indices' ABSENT des 6 fichiers |
| P24 | Anti-recurrence : 'plus de 3 indices' ABSENT des 6 fichiers |
| P25 | ASCII strict : 0 non-ASCII (test) |
| P26 | LF pur : 0 CRLF (test) |

## Execution

```bash
python3 test-023-grep-budget-pondere.py
```

## Normes

- ASCII strict : 0 non-ASCII (test)
- LF pur : 0 CRLF (test)
- Le test est AUTONOME : il lit directement les 6 fichiers reels
  (ne depend d'aucun outil externe, stdlib Python uniquement).
