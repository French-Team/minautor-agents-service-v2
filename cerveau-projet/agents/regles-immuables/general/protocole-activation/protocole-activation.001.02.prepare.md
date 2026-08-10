---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
# Protocole Immuable -- Activation des Agents

> L'activation inclut OBLIGATOIREMENT la lecture du fichier de l'agent.

**Portee :** Tous les agents du cerveau-projet
**Prerequis :** AGENTS.md, fiche de l'agent, corrections de l'agent
**Statut :** prepare (class 02)
**Derniere mise a jour :** 2026-08-05

---

## Principe Fondamental

---

## Le Cycle d'Activation

```
CERBERUS -> IDENTIFIER -> LIRE -> ACTIVER -> TRAVAILLER -> REACTIVER -> [SECOND CONTROLE]
    1          2         3       4          5            6                7
```

| Etape | Action | Responsable |
|---|---|---|
| 1 | Cerberus analyse le besoin | Cerberus |
| 2 | Identifier l'agent adapte | Cerberus |
| 3 | Lire la fiche et les corrections | Cerberus |
| 4 | Activer dans AGENTS.md | Cerberus |
| 5 | Agent execute sa mission en lancant SON parcours (carte de decision) | Agent active |
| 6 | Reactiver Cerberus | Agent active |
| 7 | Si la mission figure dans la liste definie : activer Janus | Cerberus |

> **Second controle** : la liste des missions exigeant le second controle est dans la carte de decision de Cerberus. Janus controle, puis reactive Cerberus.

---

## Matrice de decision

| Besoin | Agent | Justification |
|---|---|---|
| Creer/modifier du contenu | Buffy | Developpeur principal |
| Explorer le code | Atlas | Explorateur |
| Valider un travail | Janus | Second controle -- active par Cerberus (liste definie) |
| Coordonner | Cerberus | Gardien de l'entree |

---

## Etape 3 -- Relecture (QUESTION HONNETE)

> **ETAPE OBLIGATOIRE -- Ne pas sauter !**

### La question de relecture

A chaque activation ou reactivation, l'agent se pose la question :

> **"As-tu EN MEMOIRE ta fiche et tes corrections, capables de les appliquer
> **GARDE-FOU RELECTURE** : quand Cerberus active un agent, la RAISON doit ordonner explicitement : RELIS TA FICHE PUIS TES CORRECTIONS avant de commencer (jamais seulement les corrections).
> SANS relire ?"** -- je reponds la VERITE (regles-veracite).

| Reponse (verite) | Action OBLIGATOIRE |
|---|---|
| **OUI** (je les ai en memoire) | Continuer la mission |
| **INCERTAIN** (lu mais pas sur de tout retenir) | RELIRE corrections.md puis fiche avant de continuer |
| **NON** (pas relues cette session) | RELIRE corrections.md puis fiche avant de continuer |

> **REGLE FONDAMENTALE** : Seul OUI prouve la memorisation. Dire "je viens de les
> lire" n'est PAS une preuve de memorisation -- la lecture est un fait passe, la
> memorisation est un etat present. La case c0 de chaque parcours pose cette
> question automatiquement au demarrage (OUI -> mission, INCERTAIN/NON -> c0b
> RELIRE obligatoire).

### CONTEXTE TEMPS REEL -- lecture OBLIGATOIRE de l'historique (meme en memoire)

> **REGLE (Pattern 6, spec-guider-parcours v0.2.8)** : la question honnete
> concerne MA fiche et MES corrections (contenu STATIQUE, memorisable).
> L'historique (AGENTS-historique.md) est un contenu DYNAMIQUE : il change a
> chaque activation des autres agents/LLM -- il est IMPOSSIBLE de l'avoir en
> memoire. Sa lecture est donc OBLIGATOIRE a chaque activation, meme si deja lu :
> c'est le FIL TEMPS REEL du cerveau.
>
> | A faire (obligatoire) | Outil |
> |---|---|
> | Lire les 15 dernieres interventions des agents (date | session | agent | action) | `lire-activite-recente` (categorie lire/) |
> | Lire la section `## Sessions connues` d'AGENTS.md | Lire AGENTS.md -- savoir que les AUTRES LLM existent et leur derniere activite (evite les collisions multi-LLM) |
>
> La case c0c de chaque parcours ordonne cette lecture avant la mission :
> c0 (question honnete) -> c0c (contexte obligatoire) -> mission.

### Pourquoi cette question ?

| Situation | Question | Action |
|---|---|---|
| Premiere activation | Rien en memoire -> NON | RELIRE (decouvrir les regles) |
| Activation apres une longue pause | Memorisation incertaine -> INCERTAIN | RELIRE (se rafraichir) |
| Activation recente et maitrisee | Tout en memoire -> OUI | Continuer |
| Erreur detectee / debug | Toujours RELIRE | Comprendre ce qui a mal tourne |

### Regle

> **Ecrire dans corrections.md TOUJOURS ; relire OBLIGATOIREMENT si la reponse
> a la question n'est pas OUI.**

---

## Etape 4 -- Activation dans AGENTS.md

> **JAMAIS** `str_replace` ou `write_file` pour ce fichier critique.

### Commande d'activation

```bash
python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py activer <session> "Agent" "Raison" "Mission"
```

---

## Etape 5 -- L'agent reprend le controle (SA carte de decision)

> **REGLE FONDAMENTALE -- CERBERUS = ORCHESTRATION UNIQUEMENT** : quand Cerberus
> active un agent, il donne la MISSION (le quoi + le pourquoi + les criteres de
> validation), PAS le comment. Cerberus ne detaille JAMAIS les etapes internes
> de l'agent (relire fiche, lire spec, editer, valider, ecrire la lecon...) :
> ces etapes vivent dans SA carte de decision -- son parcours JSON.

### La reponse a la question : comment l'agent reprend-il le controle ?

1. Cerberus analyse le besoin et active l'agent (etape 4) avec la MISSION :
   La RAISON commence TOUJOURS par : RELIS TA FICHE PUIS TES CORRECTIONS avant de commencer (garde-fou anti-oubli de la fiche).
   le quoi, le pourquoi, les criteres de validation.
2. L'agent active REPREND LE CONTROLE en lancant SON parcours :
   `guider-parcours.py cerveau-projet/agents/<agent>/parcours/parcours-<agent>.json`
3. SA carte de decision le guide case par case : chaque case donne l'indice
   exact (outil a lancer, fichier a lire, regle a appliquer) et les branches
   selon ses reponses. C'est LUI qui decide, pas Cerberus.
4. L'agent termine sa mission et reactive Cerberus (etape 6).

### La todolist de Cerberus = orchestration UNIQUEMENT

| Etape Cerberus | Contenu |
|---|---|
| Analyser + choisir l'agent | La mission (quoi, pourquoi, criteres) |
| Activer l'agent | `activer-agent-principal.py activer` |
| Second controle Janus (liste definie) | Apres le retour de l'agent |
| Bilan + cloture | Reception du retour de l'agent |

> **PIEGE** : une todolist de Cerberus qui detaille les etapes internes de
> l'agent (relire fiche, lire spec, editer, valider...) rend la carte de
> decision inutile -- l'agent n'a plus qu'a suivre la liste de Cerberus au lieu
> de suivre SON parcours. Les etapes internes appartiennent AU PARCOURS.

---

## Etape 6 -- Reactivation de Cerberus

> **JAMAIS** `str_replace` ou `write_file` pour AGENTS.md.

### Commande de reactivation

```bash
python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py reactiver <session> "Raison" "AgentPrecedent"
```

> **3e argument OBLIGATOIRE** : `<AgentPrecedent>` (l agent qui rend la main) est
> INDISPENSABLE. S il est oublie, la commande affiche l AIDE (echec) et le bloc
> session reste sur l agent actif -- verifier la ligne `Session session-llm-1 :
> Cerberus reactive avec succes` pour confirmer le succes.


### Quand ?

```
AVANT de terminer la session.
```

---

## Regles d'Or

| Regle | Description |
|---|---|
| **Activation = Question** | A chaque activation, se poser la question de relecture et repondre la VERITE |
| **OUI seulement continue** | Seul OUI (memorisation prouvee) permet de continuer sans relire |
| **Historique = lecture obligatoire** | Lire TOUJOURS l'historique (lire-activite-recente) + la section Sessions connues, meme en memoire -- le dynamique ne se memorise pas |
| **Corrections = Ecriture** | TOUJOURS ecrire ; relire si la reponse n'est pas OUI |
| **Documenter l'activation** | Raison et mission dans AGENTS.md |
| **Fin de mission = SA carte** | La fin suit SA carte (Pattern 13) : la commande reactiver ramene TOUJOURS a Cerberus (conception de l outil). Regle de decision : QUI m a active ? |
| **MODE DIRECT (active par Cerberus)** | Fin = reactiver <session> <raison> <mon-nom> : ramene a Cerberus (le retour normal) |
| **MODE CHAINE (active par un agent)** | Fin = activer <session> <agent-suivant> <raison> pour enchainer, OU activer <session> <agent-precedent> <raison> pour le retour - l action activer accepte N IMPORTE QUEL agent |
| **DERNIER MAILLON de la chaine** | Fin = reactiver <session> <raison> <mon-nom> avec le bilan consolide de la chaine |

| **Pas de saut** | Ne jamais sauter une etape |
| **Cerberus = orchestration** | Cerberus donne la MISSION (quoi + pourquoi + criteres), l'agent suit SA carte de decision (SON parcours) |
| **Utiliser activer-agent-principal** | Pour toute modification d'AGENTS.md |

---

## Pieges Courants

| Piege | Solution |
|---|---|
| Dire "je viens de les lire" sans pouvoir les appliquer | Ce n'est pas une preuve : la question exige la memorisation, pas la lecture |
| Repondre OUI sans veracite | La reponse engage (regles-veracite) : INCERTAIN/NON declenchent la relecture obligatoire |
| Sauter la question de relecture | La case c0 du parcours la pose automatiquement |
| Sauter la lecture de l'historique ("je l'ai deja lu") | C'est le FIL TEMPS REEL : il change a chaque activation des autres LLM -- la case c0c du parcours la rend obligatoire |
| Oublier de documenter | Mettre a jour AGENTS.md immediatement |
| Ne pas reactiver Cerberus | C'est la DERNIERE action |
| Lire apres avoir agi | Lire AVANT de commencer |
| Cerberus detaille les etapes internes de l'agent dans sa todolist | La carte de decision devient inutile : Cerberus ne prepare QUE l'orchestration, les etapes internes vivent dans le parcours de l'agent |
| Oublier le 3e argument de reactiver (`agent_precedent`) | La commande affiche l aide et ECHOUE EN SILENCE : le bloc session reste sur l agent -- verifier `Session ... : Cerberus reactive avec succes` |

---

## Liens

- **Protocole parent** : `demarrer.md` -- protocole de demarrage
- **Convention** : `convention-protocoles` -- comment creer des protocoles
- **Regle** : `regles-choisir-agent` -- comment choisir le bon agent
