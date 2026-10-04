---
identite:
  type: convention
  appartient_a: socrate
  version: "0.1.0"
  cree: "2026-08-20"
---

# Convention : Grille de Priorisation

## Niveaux

| Niveau | Definition | Exemple | Delai |
|---|---|---|---|
| URGENT | Bloque le systeme ou les agents | Garde-fou casse, agent bloque, round rompu | Immediate |
| IMPORTANT | Amelioration majeure de la qualite | Outil manquant, test KO, parcours casse | 24h |
| MOYEN | Amelioration mineure | Refactoring, optimisation, nettoyage | Semaine |
| BAS | Nice-to-have | Cosmetique, documentation, ergonomie | Quand possible |

## Regles de classification

1. **Etre honnete** : ne pas tout mettre en URGENT
2. **Justifier** : ecrire "parce que..." pour chaque classification
3. **Verifier l'impact** : combien d'agents sont affects ?
4. **Considerer les dependances** : un probleme URGENT peut en cacher un autre
5. **Revisiter** : la classification peut changer apres discussion
