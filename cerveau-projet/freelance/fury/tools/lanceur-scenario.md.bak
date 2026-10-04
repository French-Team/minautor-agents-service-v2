# lanceur-scenario

> Le combo de Fury qui declenche des rounds reels et les note.

| Champ | Valeur |
|---|---|
| **Version** | 0.1.0 |
| **Type** | outil dedie Fury (`fury/tools/`) |
| **Proprietaire** | Forge |
| **Cree** | 2026-08-23 |

---

## Les 3 temps

1. Fury donne le scenario (JSON : liste de maillons `de -> vers` + session)
2. L'outil EXECUTE : chaque maillon = `jarvis.py envoyer --activer`
   (objet prefixe `SCENARIO-TEST`) avec collecte des traces
3. Rapport machine-lisible : attendu vs observe, verdict par maillon

## Contrat

```
python3 lanceur-scenario.py --scenario <fichier.json>
python3 lanceur-scenario.py --exemple
```

Verdict global PASSE si tous les maillons sont PASSE (rc=0 ET bloc session
mis a jour vers le destinataire).

## Limites honnetes (V1-V4)

L'outil verifie la PARTIE MECANIQUE uniquement :
routage des messages + mises a jour du bloc session AGENTS.md.
L'incarnation LLM de chaque agent se verifie par les TRACES
(historique, inboxes), jamais simulée ici.
