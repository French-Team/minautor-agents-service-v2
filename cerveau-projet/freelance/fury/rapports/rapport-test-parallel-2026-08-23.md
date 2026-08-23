# Rapport de test reel -- 2 missions en PARALLEL

| Champ | Valeur |
|---|---|
| **Date** | 2026-08-23 13:00 |
| **Testeur** | Fury (hors-round) |
| **Outil** | jarvis.py lancer-missions v0.9.0 |
| **Verdict** | **PASSE** (couche mecanique) |

---

## Scenario

2 missions INDEPENDANTES lancees simultanement via lancer-missions
(mode parallel) : rogers (TEST PARALLEL A) + shuri (TEST PARALLEL B),
chacune avec pour seule tache de confirmer son activation.

## Resultats observes

| # | Verification | Attendu | Observe | Verdict |
|---|---|---|---|---|
| 1 | Les 2 activations partent (rc=0 chacune) | 2 x rc=0 | conforme | PASSE |
| 2 | Message P1 dans inbox/rogers.jsonl | present | ACTIVATION lu=True | PASSE |
| 3 | Message P1 dans inbox/shuri.jsonl | present | ACTIVATION lu=True | PASSE |
| 4 | Livraison directe v0.6.1 | marques lus a l'emission | conformes | PASSE |
| 5 | Bloc session APRES le parallel | dernier ecrivain = shuri | shuri | PASSE |

## Limite honnete (V1-V4)

Le PARALLEL est PHYSIQUE au niveau du lancement (2 sous-processus
simultanes, 2 messages livres) mais LOGIQUE au niveau de l'execution :
un seul LLM incarne ensuite les agents l'un apres l'autre. Le parallel
deviendra physiquement execute avec deux sessions LLM distinctes.
La course sur le bloc session (dernier ecrivain gagne) est documentee
et attendue.

## Conclusion

Le lancement PARALLEL fonctionne mecaniquement de bout en bout :
2 missions independantes declenchees ensemble, toutes deux tracées.
Les confirmations des agents concernes restent a incarner si voulu.
