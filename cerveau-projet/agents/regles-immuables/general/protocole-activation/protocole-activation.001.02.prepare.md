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
**Derniere mise a jour :** 2026-08-15

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
| 6 | La fin de l agent suit SA carte (modele aero : reactiver-fin --cible oracle) ; le pilote decide du suivant | Agent active |
| 7 | Si la mission figure dans la liste definie : le pilote largue Janus | Pilote (Oracle) |

> **Second controle** : la liste des missions exigeant le second controle est dans la carte de decision de Cerberus. Le pilote largue Janus ; sa fin suit SA carte (reactiver-fin janus --cible oracle).

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
> question automatiquement au demarrage (OUI -> c0c contexte -> mission, INCERTAIN/NON -> c0b
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
2. L'agent actif REPREND LE CONTROLE : Oracle (pilote) le dirige selon SON
   arbre de decision v2 -- `oracle.py pilote <agent>` charge l'arbre
   (`arbre-<agent>.json` + themes `theme-*.json` + `fins.json`) et sert chaque
   etape de travail dans l inbox de l agent (maitre d hotel, vision
   2026-08-27). Tous les agents ont un arbre v2 : l etat de carte pointe vers
   `arbre-<agent>.json`. Les parcours v1 (`guider-parcours.py ...
   parcours-<agent>.json`) sont des ARCHIVES protegees par le marbre : ils ne
   pilotent plus le guidage.
3. SA carte (arbre v2) le guide redirect par redirect / case par case :
   chaque redirect/case donne l'indice exact (outil a lancer, fichier a
   lire, regle a appliquer) et les branches selon ses reponses. C'est LUI qui
   decide, pas Cerberus. Les fins sont precedent-aware : un agent active en
   inter-round rend la main a son appelant via `oracle.py reactiver-fin`
   (protocole-fin-mission v0.3.0).
4. L'agent EXECUTE IMMEDIATEMENT apres l'activation, DANS LE MEME ROUND
   (regle RELEVE MEME ROUND) : jamais d'arret, jamais de bilan intermediaire
   pour attendre l'utilisateur. L'activation EST l'ordre d'execution.
5. L'agent termine sa mission ; sa fin suit SA carte (modele aero : reactiver-fin <agent> --cible oracle).

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
| **RELEVE MEME ROUND (IMMUABLE)** | Apres activation, l agent active EXECUTE IMMEDIATEMENT dans le meme round (activation + execution dans le meme message) : jamais d arret pour attendre l utilisateur. Il suit SA carte ; sa fin va vers ORACLE (reactiver-fin --cible oracle), le pilote decide du suivant. Reference : regles-groupes-agents.md (RELEVE MEME ROUND) |
| **OUI seulement continue** | Seul OUI (memorisation prouvee) permet de continuer sans relire |
| **Historique = lecture obligatoire** | Lire TOUJOURS l'historique (lire-activite-recente) + la section Sessions connues, meme en memoire -- le dynamique ne se memorise pas |
| **Corrections = Ecriture** | TOUJOURS ecrire ; relire si la reponse n'est pas OUI |
| **Documenter l'activation** | Raison et mission dans AGENTS.md |
| **Fin de mission = SA carte (modele aero R1/R3)** | La fin suit SA carte : reactiver-fin <agent> --cible oracle, JAMAIS reactiver Cerberus directement, JAMAIS activer un autre agent. C est le pilote qui decide du suivant. |
| **MODE DIRECT (active par Cerberus)** | Fin = reactiver-fin <agent> "<bilan>" --cible oracle : le pilote ramene a Cerberus en fin de round (le retour normal) |
| **MODE CHAINE (active par un agent)** | Fin = reactiver-fin <agent> "<bilan>" --cible oracle : le pilote enchaIne sur le maillon suivant OU renvoie l appelant (inter-round) |
| **DERNIER MAILLON de la chaine** | Fin = reactiver-fin <agent> "<bilan consolide>" --cible oracle : le pilote ramene le bilan consolide a Cerberus en fin de round |

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
| Ne pas rendre sa fin | La fin est OBLIGATOIRE : reactiver-fin <agent> --cible oracle (modele aero) - jamais de mission sans fin vers ORACLE |
| Lire apres avoir agi | Lire AVANT de commencer |
| Cerberus detaille les etapes internes de l'agent dans sa todolist | La carte de decision devient inutile : Cerberus ne prepare QUE l'orchestration, les etapes internes vivent dans le parcours de l'agent |
| Oublier le 3e argument de reactiver (`agent_precedent`) | La commande affiche l aide et ECHOUE EN SILENCE : le bloc session reste sur l agent -- verifier `Session ... : Cerberus reactive avec succes` |
| S arreter apres une activation (brisure de chaine) | L activation EST l ordre d execution (regle RELEVE MEME ROUND) : l agent active enchainE IMMEDIATEMENT SA mission dans le meme round -- jamais de bilan intermediaire, jamais de fin vers Cerberus en milieu de chaine (toute fin va vers ORACLE) |

---

## Liens

- **Protocole parent** : `demarrer.md` -- protocole de demarrage
- **Convention** : `convention-protocoles` -- comment creer des protocoles
- **Regle** : `regles-choisir-agent` -- comment choisir le bon agent

