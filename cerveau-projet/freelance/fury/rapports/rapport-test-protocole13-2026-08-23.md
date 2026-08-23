# Rapport de test reel -- Protocole 13 (UR-1/AT-1 + files d'attente)

| Champ | Valeur |
|---|---|
| **Date** | 2026-08-23 08:41 |
| **Testeur** | Fury (hors-round) |
| **Declencheur** | Demande utilisateur avec prefixes [attention] + [urgent] |
| **Verdict** | **PASSE** |

---

## Scenario teste

Premiere utilisation REELLE des prefixes par l'utilisateur dans une seule
demande : une tache [attention] (philosophie des agents) et une tache
[urgent] (tester le protocole 13). Le parcours attendu :

1. Stark reconnait les prefixes
2. L'[attention] est PREPAREE et placee en file-asap.jsonl (statut PREPAREE)
3. L'[urgent] passe avant : Stark -> JARVIS -> activation de Fury
4. Fury verifie et rapporte

## Maillons observes

| # | Verif | Attendu | Observe | Verdict |
|---|---|---|---|---|
| 1 | Prefixe [attention] reconnu par Stark | demande placee en file-asap | entree PREPAREE presente, mission complete, agent porteur=rogers, contexte de reprise > 20 chars | PASSE |
| 2 | Priorite [urgent] respectee | l'urgent traite AVANT l'attention | Fury active avant tout travail sur la philosophie | PASSE |
| 3 | Activation de Fury tracee | bloc session = fury + message P1 acquitte via recu | oui (fluidite v0.5.0 utilisee) | PASSE |
| 4 | Round mecanique de controle | lanceur-scenario PASSE | 6/6 maillons PASSE | PASSE |

## Preuves

- files/file-asap.jsonl : entree [AT-1] Philosophie des agents (date
  2026-08-23T08:41:16, statut PREPAREE, agent rogers)
- messages 0b78f6f0 ([urgent] stark->jarvis), f2b0c52a (activation fury)
- lanceur-scenario : scenario-inter-round.json, verdict PASSE 6/6

## Limitation honnete (V1-V4)

La reconnaissance des prefixes est un comportement LLM (Stark/JARVIS) :
elle vient d'etre exercee EN REEL dans cette session mais n'est pas
verifiable par script - les traces ci-dessus en sont la preuve.

## Conclusion

Le protocole 13 fonctionne de bout en bout sur sa premiere utilisation
reelle. La file file-asap contient la mission philosophie preparee, prete
a etre reprise (commande reprendre --file file-asap).
