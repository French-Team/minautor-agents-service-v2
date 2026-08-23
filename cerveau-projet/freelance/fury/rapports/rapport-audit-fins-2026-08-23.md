# Rapport d'audit -- Cases de fin des agents freelance

| Champ | Valeur |
|---|---|
| **Date** | 2026-08-23 |
| **Auditeur** | Fury (hors-round) |
| **Périmètre** | fins.json + themes + corrections.md des 9 agents |
| **Verdict** | **CONFORME AVEC RÉSERVES** (0 violation grave, 5 mentions à enrichir) |

---

## Référence de la règle

Le bilan part D'ABORD vers JARVIS (`--vers jarvis`), JARVIS informe Stark.
SEULE exception légitime : un agent peut ACTIVER Stark en fin de cycle
pour lui rendre le contrôle — mais APRÈS avoir envoyé son bilan à JARVIS.

## Résultats

| Agent | fins.json | themes | fiche/corrections | Verdict |
|---|---|---|---|---|
| vision | ✅ v0.2.0 corrigée ce jour | ✅ traiter aligne | ✅ | CONFORME |
| fury | ✅ rapport → JARVIS | ✅ | ✅ | CONFORME |
| edith | ✅ rapport → JARVIS | ✅ | ✅ | CONFORME |
| shuri | ⚠️ | ⚠️ | ⚠️ corrections.md:21 "j'ACTIVE Stark" sans étape JARVIS | A ENRICHIR |
| forge | ⚠️ | ⚠️ | ⚠️ corrections.md:32 idem | A ENRICHIR |
| rogers | ⚠️ | ⚠️ | ⚠️ corrections.md:32 idem | A ENRICHIR |
| parker | ⚠️ | ⚠️ | ⚠️ corrections.md:31 idem | A ENRICHIR |
| stark | n/a (il EST la destination) | - | - | CONFORME |
| jarvis | n/a (il EST le canal) | - | - | CONFORME |

## Analyse des 5 signalements

Les corrections.md de shuri/forge/rogers/parker disent *"FIN DE CYCLE ->
j'ACTIVE Stark"* sans rappeler que LE BILAN DOIT PARTIR À JARVIS AVANT.
Ce ne sont pas des violations (l'activation de Stark reste l'exception
légitime) mais des cases incomplètes : écrites avant la règle du
protocole 18/19, elles peuvent induire un agent à sauter l'étape JARVIS
comme Vision l'a fait aujourd'hui.

## Recommandation

Enrichir les 4 corrections.md (+ themes si besoin) avec la séquence
complete : **bilan -> JARVIS -> activer Stark**. Mission pour Chiron
(educateur) ou correction directe par chaque agent.

## Conclusion

0 violation grave. Le système tient — mais les cases de fin écrites
avant aujourd'hui doivent être enrichies pour graver la séquence
JARVIS-d'abord partout.
