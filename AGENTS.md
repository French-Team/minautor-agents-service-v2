---
identite:
  type: racine
  appartient_a: commun
  commun: true
---
# Agents du Cerveau-Projet

> Ce fichier est mis a jour dynamiquement par les agents principaux.
> Chaque session LLM (session-admin, session-freelance...) possede son bloc dedie et son agent principal.
> L'historique complet est dans [AGENTS-historique.md](AGENTS-historique.md) (v1 / session-admin)
> et [AGENTS-historique-v2.md](AGENTS-historique-v2.md) (v2 / session-freelance) - fichiers
> SEPARES par session (decision 2026-08-26 : la v2 est l evolution de la v1, chaque session
> a SES fichiers avec SON format). Vue rapide : [AGENTS-activite-recente.md](AGENTS-activite-recente.md)
> (v1) + [AGENTS-activite-recente-v2.md](AGENTS-activite-recente-v2.md) (v2).

---

> HERITAGE v1/v2 -- LECTURE SEULE : les blocs de session v1/v2 ci-dessous et le
> MARBRE (protege) appartiennent aux ANCETRES. La v3 lit SON bloc session-matrix
> et son demarrage dedie demarrer-optimus-prime.md. Le census des agents v1/v2
> est ARCHIVE : cerveau-projet/matrix/docs/heritage-v1-v2-AGENTS.md

## Sessions LLM

### Session : session-admin

| Champ | Valeur |
|---|---|
| **Nom LLM** | glm5 |
| **Nom Agent** | Cerberus |
| **Role Agent** | Gardien de l'entree -- analyse et active les agents |
| **Derniere mise a jour** | 2026-09-06 |
| **Fiche** | [cerveau-projet/agents/cerberus/cerberus.md](cerveau-projet/agents/cerberus/cerberus.md) |
| **Corrections** | [cerveau-projet/agents/cerberus/corrections.md](cerveau-projet/agents/cerberus/corrections.md) |
| **Active par** | oracle (retour de mission) |
| **Raison** | Retour fin de chaine: round optimisation optimus |
## Sessions connues

| Session | Nom LLM | Agent actif | Derniere activite |
|---|---|---|---|
| session-admin | glm5 | Cerberus | 2026-09-06 07:27:58.685 |
<!-- session-matrix:DEBUT (v3, gere par l'outil matrice editer-agents-md) -->

### Session : session-matrix (v3 / Matrice)

| Champ | Valeur |
|---|---|
| **Nom LLM** | glm5 |
| **Agent actif** | cameleon |
| **Role Agent** | agent unique de la Matrice (personnalite fournie par le vivier) |
| **Derniere mise a jour** | 2026-09-19 12:08:50 |
| **Raison** | Encart v3 (2026-09-19) : ce bloc est la SEULE zone de la v3 dans ce fichier -- tout le reste (session v1 session-admin, census des agents v1 dont Buffy, cycle Cerberus/Oracle, encart v2) est un HERITAGE en LECTURE SEULE, jamais le demarrage de la v3. Le demarrage v3 est demarrer-optimus-prime.md ; la v3 vit dans cerveau-projet/matrix/. |

Flux v3 : la Matrice accueille au demarrage -> l'operateur fait sa demande ->
la Matrice lance le cameleon pour sa mission (serial stricte).

<!-- session-matrix:FIN -->

## Configuration Active
<!-- MARBRE:DEBUT constitution -->
### Regles specifiques a Cerberus

1. **Ecouter avant de decider** -- comprendre le besoin avant d'activer un agent
2. **Documenter chaque activation** -- raison, mission, agent choisi
3. **Exiger le retour** -- chaque agent doit revenir a Cerberus
4. **Ne jamais sauter Cerberus** -- point d'entree unique

### Le cycle fondamental

```
CERBERUS -> AGENT -> CERBERUS
    1         2         3
```

| Etape | Action |
|---|---|
| 1 | Cerberus accueille l'utilisateur |
| 2 | Cerberus analyse et choisit l'agent |
| 3 | Cerberus active l'agent (mise a jour AGENTS.md) |
| 4 | **L'agent active lit SA fiche et SES corrections** puis execute sa mission |
| 5 | Agent termine : la fin va vers **ORACLE** (modele aero R1, jamais cerberus, jamais un autre agent) via `oracle.py reactiver-fin <agent> --cible oracle` ; le PILOTE decide du suivant. ERREUR HORS-PERIMETRE -> INTER-ROUND (modele aero) : l'agent SIGNALE le besoin a ORACLE (`oracle.py mission-ajouter --agent <habilite>`), MA FIN vers ORACLE, et le **pilote LARGUE l'agent habilite** ; a la fin de l'inter-round, le pilote renvoie l'appelant qui REPREND son round (protocole-fin-mission, modele aero 2026-08-30) |
| 6 | **Cerberus relit SA fiche et SES corrections** puis reprend pour la suite |

> **REGLE DE RELECTURE** : A chaque activation ou reactivation, l'agent relit SA fiche et SES corrections (jamais celles des autres). Activer sans lire = inutile.

### Regles permanentes de round (decision utilisateur 2026-09-02)

1. **REPRISE APRES REDEMARRAGE** : apres CHAQUE redemarrage de session, le
   round interrompu REPREND -- l agent ne repart pas de zero et ne demande
   jamais "Que souhaitez-vous faire ?" : il traite les erreurs bloquantes
   restantes (etats-cartes residuels, daemons morts) puis continue TON
   arbre a l endroit ou il s etait arrete, missions en file comprises.
2. **MODE SINGLE-LLM** : quand l utilisateur dit "single-llm" (ou "mode
   mono"), le LLM incarne TOUS les maillons du round lui-meme (rien ne se
   passe en arriere-plan) : apres chaque activation il joue immediatement le
   role de l agent active (relecture fiche/corrections, mission, fin vers
   ORACLE), jusqu a la fin de chaine (bilan consolide -> Cerberus).
3. **TRAVAIL EN SERIE OBLIGATOIRE (decision utilisateur 2026-09-05)** : en
   mode single-llm, un SEUL agent est incarne a la fois -- le travail en
   parallele n existe PAS. Une seule mission est relayee a la fois : elle
   doit etre TERMINEE (fin vers ORACLE) avant de relayer la suivante.
   Jamais 2 missions relayees simultanement (ex: relayer Atlas ET Clio en
   meme temps = violation). Les missions en file se traitent une par une,
   en serie stricte, jusqu a la fin de chaine (bilan consolide -> Cerberus).

> Ces 3 regles sont aussi gravees dans `demarrer.md` (ORDRE 4 et ORDRE 5) :
> elles sont donc lues a chaque demarrage de session, en plus d ici.
<!-- MARBRE:FIN constitution -->

---

## Heritage v1/v2 -- LECTURE SEULE (pas la v3)

Le census des agents v1/v2, les regles de groupes et les procedures d'activation
(Comment changer d'agent, Depuis Cerberus, Oracle, Fin de mission) ont ete
ARCHIVES le 2026-09-19 (MO-217 / EO-211) : ils ne sont PAS le demarrage de la v3.

    Archive : cerveau-projet/matrix/docs/heritage-v1-v2-AGENTS.md

Un round v3 lit SON bloc (session-matrix, plus haut) et son demarrage dedie
demarrer-optimus-prime.md. Le MARBRE ci-dessus est protege : seul l'agent
Gardien peut en proposer la modification, et le createur valide.
