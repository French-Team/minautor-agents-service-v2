# Rapport d'audit -- Cases de fin des agents freelance

| Champ | Valeur |
|---|---|
| **Date** | 2026-08-23 |
| **Auditeur** | Fury (hors-round) |
| **Perimetre** | fins.json + themes + corrections.md des 9 agents |
| **Verdict** | **CONFORME AVEC RESERVES** (0 violation grave, 5 mentions a enrichir) |

---

## Reference de la regle

Le bilan part D'ABORD vers JARVIS (`--vers jarvis`), JARVIS informe Stark.
SEULE exception legitime : un agent peut ACTIVER Stark en fin de cycle
pour lui rendre le controle -- mais APRES avoir envoye son bilan a JARVIS.

## Resultats

| Agent | fins.json | themes | fiche/corrections | Verdict |
|---|---|---|---|---|
| vision | [OK] v0.2.0 corrigee ce jour | [OK] traiter aligne | [OK] | CONFORME |
| fury | [OK] rapport -> JARVIS | [OK] | [OK] | CONFORME |
| edith | [OK] rapport -> JARVIS | [OK] | [OK] | CONFORME |
| shuri | [ATTENTION] | [ATTENTION] | [ATTENTION] corrections.md:21 "j'ACTIVE Stark" sans etape JARVIS | A ENRICHIR |
| forge | [ATTENTION] | [ATTENTION] | [ATTENTION] corrections.md:32 idem | A ENRICHIR |
| rogers | [ATTENTION] | [ATTENTION] | [ATTENTION] corrections.md:32 idem | A ENRICHIR |
| parker | [ATTENTION] | [ATTENTION] | [ATTENTION] corrections.md:31 idem | A ENRICHIR |
| stark | n/a (il EST la destination) | - | - | CONFORME |
| jarvis | n/a (il EST le canal) | - | - | CONFORME |

## Analyse des 5 signalements

Les corrections.md de shuri/forge/rogers/parker disent *"FIN DE CYCLE ->
j'ACTIVE Stark"* sans rappeler que LE BILAN DOIT PARTIR A JARVIS AVANT.
Ce ne sont pas des violations (l'activation de Stark reste l'exception
legitime) mais des cases incompletes : ecrites avant la regle du
protocole 18/19, elles peuvent induire un agent a sauter l'etape JARVIS
comme Vision l'a fait aujourd'hui.

## Recommandation

Enrichir les 4 corrections.md (+ themes si besoin) avec la sequence
complete : **bilan -> JARVIS -> activer Stark**. Mission pour Chiron
(educateur) ou correction directe par chaque agent.

## Conclusion

0 violation grave. Le systeme tient -- mais les cases de fin ecrites
avant aujourd'hui doivent etre enrichies pour graver la sequence
JARVIS-d'abord partout.
