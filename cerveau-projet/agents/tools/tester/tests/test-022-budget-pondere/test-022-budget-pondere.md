# test-022-budget-pondere.py

**Testeur** : Morpheus (testeur dedie)
**Date** : 2026-08-11
**Objet** : Test formel du BUDGET PONDERE des indices par case
(valider-case v1.1.0) : verifie la FRONTIERE EXACTE 3,0 avec des cas
limites (poids exactement 3,0 CONFORME / juste au-dessus 3,5 A ALLEGER).

---

## Contexte

Test formel de la suite de non-regression (test-001 a test-022).
Ce test est reference au catalogue generateurs-commande : toute
modification de son perimetre doit etre validee par Morpheus.

Le budget pondere (decision utilisateur 2026-08-11 : 2 indices courts
= 1 indice long) est implemente dans valider-case v1.1.0 et
generateurs-case v0.4.2 :
- indice COURT (texte <= 100 car. ou sans texte) = poids 0,5
- indice LONG (texte > 100 car.) = poids 1
- budget par case = 3,0 unites
- texte > 160 car. = plafond absolu d'un indice (inchange, independant)

## Cas limites couverts (frontiere 3,0)

| Cas | Poids | Verdict attendu |
|---|---|---|
| 6 courts (50 car.) | 3,0 | CONFORME |
| 3 longs (120 car.) | 3,0 | CONFORME |
| 2 longs + 2 courts | 3,0 | CONFORME |
| 1 long + 4 courts | 3,0 | CONFORME |
| 5 courts + 1 long | 3,5 | A ALLEGER |
| 3 longs + 1 court | 3,5 | A ALLEGER |
| 4 longs (120 car.) | 4,0 | A ALLEGER |
| 1 texte 200 car. + 2 courts | 2,0 (mais texte > 160) | A ALLEGER (plafond) |
| 6 x 100 car. exactement | 3,0 | CONFORME (100 = court) |
| 4 x 101 car. | 4,0 | A ALLEGER (101 = long) |
| 6 refs (sans texte) | 3,0 | CONFORME |
| 6 outil (sans texte) | 3,0 | CONFORME |

## Execution

```bash
python3 test-022-budget-pondere.py
```

## Normes

- ASCII strict : 0 non-ASCII (test)
- LF pur : 0 CRLF (test)
- Le test est AUTONOME : il genere ses parcours temoins dans tmp
  (ne depend pas de l'etat des parcours reels).
