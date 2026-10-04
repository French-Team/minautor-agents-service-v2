---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
# Todo -- Protocole de Creation et Mise en Place des Combos
---

## Taches en cours

| # | Tache | Statut | Priorite |
|---|---|---|---|
| 1 | Creer le protocole (pense-bete) | [OK] Termine | Haute |
| 2 | Creer la spec technique | [OK] Termine | Haute |
| 3 | Creer les todos | [OK] Termine | Haute |
| 4 | Mettre a jour index-regles-general.md (ligne protocole) | [EN COURS] | Haute |
| 5 | Corriger doc moteur : emplacement canonique (combos-moteur.md) | [EN COURS] | Haute |
| 6 | Corriger spec-combos-moteur (emplacement canonique) | [EN COURS] | Haute |
| 7 | Valider : ASCII 0 + liens + coherence (controle Janus) | [NON COMMENCE] | Haute |

---

## Taches futures

| # | Tache | Statut | Priorite |
|---|---|---|---|
| 8 | Tester le processus sur un nouveau combo (application reelle) | [NON COMMENCE] | Haute |
| 9 | Verifier la conformite des 6 combos existants au protocole | [NON COMMENCE] | Moyenne |
| 10 | Ajouter des exemples de definition conforme | [NON COMMENCE] | Basse |

---

## Dependances

| Tache | Depend de |
|---|---|
| 4 | 1, 2, 3 |
| 5 | 1, 2 |
| 6 | 1, 2 |
| 7 | 4, 5, 6 |

---

## Notes

- Le protocole complete la spec-combos-moteur (le QUOI) par le COMMENT
- La distinction OUTIL (agents/tools/combos/) vs DEFINITION (cerveau-projet/combos/) est la cle
- Le processus doit etre teste sur un combo futur (tache 8) pour valider sa reproductibilite
