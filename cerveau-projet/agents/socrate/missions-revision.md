# Missions de Revision -- 2026-08-20

## Resume

| Niveau | Nombre |
|---|---|
| URGENT | 1 |
| IMPORTANT | 1 |
| MOYEN | 0 |
| BAS | 0 |

## Missions

### [URGENT] Corriger le mecanisme d'action dans les parcours

- **Agent habilite** : buffy
- **Description** : Les cases d'action dans les parcours affichent des indices mais ne forcent pas l'execution. Le LLM lit les instructions et passe a la case suivante sans faire le travail. Corriger le parcours Buffy pour que les actions soient executees avant de passer au controle suivant.
- **Raison** : Ce probleme BLOQUE le systeme -- les agents ne suivent plus leurs parcours, les rounds se cassent, et la qualite se degrade a chaque amelioration.
- **Dependances** : Aucune
- **Critere de succes** : Le LLM execute reellement les actions (lire-fichier, creer-fichier, etc.) avant de repondre au controle suivant. Test reel : activer un agent et verifier qu'il suit toutes les etapes.

### [IMPORTANT] Creer test-101 : verification d'execution des actions

- **Agent habilite** : morpheus
- **Description** : Creer un test qui verifie que pour chaque case d'action dans un parcours, l'outil correspondant est reellement appele (pas seulement affiche). Le test doit detecter les parcours ou les actions sont sautees.
- **Raison** : Sans ce test, le probleme se reproduira silencieusement a chaque modification de parcours.
- **Dependances** : Mission URGENT terminee (buffy a corrige le mecanisme)
- **Critere de succes** : Le test detecte les parcours non conformes et reve un rapport clair.
