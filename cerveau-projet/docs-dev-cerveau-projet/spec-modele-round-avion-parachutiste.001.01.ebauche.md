---
identite:
  type: spec
  appartient_a: commun
  commun: true
---
# Spec -- Modele du round : aero / pilote / avion / parachutiste

**Version** : 0.1.0
**Statut** : ebauche
**Date creation** : 2026-08-30
**Agent** : Buffy (conception, session-admin)
**Historique** : v0.1.0 (creation, 2026-08-30)

---

## 1. Objectif

Refonder le **round** v1 sur une metaphore unifiee et fiable : la communication
passe TOUJOURS par oracle (la plateforme), et c'est le **pilote** (l'outil
d'oracle) qui orchestre les agents -- pas les agents entre eux.

Le probleme constate : les fins des agents renvoient vers **cerberus** ou
**activent automatiquement le suivant**. C'est un vestige de la v1. Dans le
modele cible, toute fin d'agent revient vers **oracle**, qui decide du suivant
via le pilote. Le round ne doit jamais dependre du fait qu'un agent connaisse
le nom du prochain agent.

## 2. Le modele a 4 roles

| Role | Metaphore | Responsabilite |
|---|---|---|
| **oracle** (agent) | **l'aeroport** | Configure la destination + le nombre de parachutistes, lance le pilote, le recupere a la fin de SA mission complete |
| **pilote** (outil) | la partie pilote de l'outil | Suit SA mission propre : largue les parachutistes un a un, attend leur fin, les recupere, continue ; ne revient a l'aeroport qu'une fois TOUTE sa mission terminee |
| **avion** (outil) | la partie parachutistes de l'outil | Transporter / larguer les parachutistes, gerer les agents pendant leur execution |
| **agents** (executants) | les parachutistes | Executent la mission, envoient leur message de fin, sont recuperes par le pilote |

### 2.1 Flux nominal

```
oracle (aeroport)
  -> configure le pilote : destination + liste [agent1, agent2, ...]
  -> lancer le pilote
pilote (avion)
  -> largue agent1
  agent1 execute -> envoie son FIN (vers oracle / le pilote)
  pilote recupere agent1
  -> continue sa mission
  -> largue agent2 ...
  -> quand sa mission est COMPLETEMENT terminee
  -> revient a oracle (aeroport)
oracle recupere le pilote -> termine le round
```

### 2.2 Orchestration pilotee

Le pilote **largue** et **recupere**. Ce n'est PAS l'agent qui decide "qui est
le suivant" : c'est le pilote, selon SA mission configuree au depart.

## 3. Regles cibles

### R1 -- Toute fin d'agent va vers oracle

Une fin de mission d'un agent (et les erreurs inter-round) revennent vers
**oracle** (l'aeroport), jamais vers cerberus, jamais vers un agent suivant.
Le pilote (oracle) decide de la suite.

### R2 -- Le pilote a SON arbre de mission

Le pilote possede son propre parcours de mission (distinct des arbres des
agents). Oracle le configure au lancement : destination + agents a larguer.
Lance une fois, il ne revient a oracle qu'a la fin de TOUT son cycle (peu
importe 1, 2, 3+ agents largues).

### R3 -- Les agents ne connaissent pas le suivant

Aucune fin d'agent n'encode "activer <prochain agent>". C'est du vestige v1.
Un agent sait seulement : j'execute MA mission, j'envoie mon FIN, je suis
recupere.

### R4 -- Separation montant / descendant (a reflechir)

Les flux qui remontent (retour vers oracle) et ceux qui descendent (vers les
agents) ne doivent pas melanger leurs arbres / themes / cases. Un theme
"montant" ne doit pas contenir de parcours "descendant". A structurer en v0.2.

## 4. Ce qu'il faut changer (chantier a decomposer)

| Element | Etat actuel | Cible |
|---|---|---|
| Fins des agents | reactiver cerberus / activer le suivant | revenir vers oracle |
| Pilote | suit l'arbre de l'agent (--parcours arbre-<agent>.json) | suivre SON arbre de mission configure par oracle |
| Orchestration | selon SA carte (Pattern 8/13) | orchestration pilotee (largue/recupere) |
| Role cerberus | point de retour | reste "avant" oracle (entree utilisateur) ; ne recoit plus les fins directes des agents |

## 5. Outils / test

- Les tests de non-regression du round devront verifier : une fin d'agent ne
  reference ni cerberus ni un maillon suivant (R1, R3).
- Le pilote aura son propre parcours de mission auditable par la suite de
  non-regression (R2).

## 6. Verification de compatibilite reactiver-fin (2026-08-30) -- INCOMPATIBLE

Resultat de la verification demandee AVANT toute migration large :

**1. Le pilote ignore cible=oracle** : dans pilote.py `_executer_fin_oracle`,
une fin action=reactiver avec cible=oracle tombe dans le 'else' generique
(historise FIN puis s arrete). Le pilote ne dit jamais a l agent de
retourner vers ORACLE.

**2. reactiver-fin ne lit PAS la fin, il lit le precedent** : `reactiver-fin`
appelle `_reactiver_maillon` qui utilise `_maillon_precedent(etat)` :
precedent=cerberus -> reactive CERBERUS (R1 violee) ; precedent=buffy ->
reactive BUFFY (modele v1). La commande des fins reconstruites ignore
cible=oracle.

**3. Consequence** : une fin reconstruite vers oracle est cosmetiquement
conforme (audit F4 passe) mais fonctionnellement cassee (l agent reactive
cerberus/precedent en executant sa commande de fin).

**Verdict initial : INCOMPATIBLE - CORRIGE le 2026-08-30.**

Corrections appliquees (pilote.py v0.2.1, oracle.py, reconstruire-arbre.py) :
  1. `_executer_fin_oracle` : cas cible=="oracle" -> message retour vers
     ORACLE (au lieu du else generique). FAIT.
  2. `_reactiver_maillon` : parametre cible_forcee ; quand la fin porte
     cible=oracle, reactiver ORACLE (activer_agent + etat de carte oracle
     mission_type=coordination), pas le precedent/cerberus. FAIT.
  3. `oracle.py reactiver-fin --cible <cible>` : option transmise a
     _reactiver_maillon. FAIT.
  4. Fins reconstruites : la commande porte --cible oracle. FAIT
     (reconstruire-arbre.py passe F4b).

## 7. Etat de mise en oeuvre (2026-08-30)

### R2 LIVRE : arbre de mission du pilote cree

`cerveau-projet/agents/tools/oracle/pilote/parcours/` :
  - arbre-pilote.json (racine : MISSION / LARGUER / RECUPERER / RETOUR)
  - theme-mission.json (charger destination + liste d agents configuree par oracle)
  - theme-larguer.json (larguer UN agent, attendre sa fin)
  - theme-recuperer.json (recuperer l agent, passer au suivant)
  - theme-retour.json (revenir a ORACLE quand TOUTE la mission est terminee)
  - fins.json (fin-mission-chargee, fin-agent-largue, fin-agent-recupere,
    fin-retour-oracle)

Valide : 6 JSON coherents (racine -> themes -> fins), ASCII 0 / LF 0,
navigation pilote de bout en bout (racine -> theme-mission -> larguer).

### TEST REEL ROUND AERO COMPLET (2026-08-30) : PASSE

Sequence testee (pilote pilote son arbre, oracle configure chaque etape) :
  1. ORACLE CONFIGURE -> theme-mission (destination + liste d agents) OK
  2. PILOTE LARGUE argus -> theme-larguer (activation + attente fin) OK
  3. PILOTE RECUPERE argus -> theme-recuperer (bilan) OK
  4. PILOTE LARGUE chiron -> theme-larguer OK
  5. PILOTE RECUPERE chiron -> theme-recuperer OK
  6. PILOTE REVIENT A ORACLE -> theme-retour -> 'revenu vers ORACLE
     (modele aero R1, reactiver-fin oracle)' - FIN DU ROUND OK

Etat nettoye apres test (etat-cartes/pilote.json supprime), FLUX OK,
0 trace de test dans activite-recente/historique.

### TEST REEL ROUND INTEGRE CERBERUS -> ORACLE -> PILOTE -> AGENT -> RETOUR
(2026-08-30) : PASSE

Mission reelle deposee (oracle.py mission-ajouter, file asap, agent argus)
puis chaine pilotee arbre par arbre :
  1. CERBERUS depose la mission vers Oracle (theme-vers-oracle, file asap) OK
  2. ORACLE-AGENT lit la mission + identifie l agent (theme-coordination) OK
  3. ORACLE configure le PILOTE (theme-mission : destination + argus) OK
  4. PILOTE LARGUE argus (theme-larguer : activation + attente) OK
  5. ARGUS execute SON arbre (theme-detecter, 10 besoins) OK
  6. ARGUS termine -> FIN 'revenu vers ORACLE (R1, reactiver-fin oracle)' OK
  7. PILOTE RECUPERE argus (theme-recuperer : bilan) OK
  8. PILOTE REVIENT A ORACLE (theme-retour) -> ORACLE remonte a CERBERUS
     (fin coordination, Pattern 13) -> FIN DU ROUND OK

Etats nettoyes, mission test terminee, FLUX OK, 0 trace.

### Points restants
  1. Corrections pilote.py (section 6) : cible=oracle non gere
     (INCOMPATIBLE) -> CORRIGE (pilote v0.2.1, voir section 6).
  2. Garde-fou R7 de verifier-flux-securite : exige 'apres FIN -> Cerberus',
     -> CORRIGE (v0.2.0) : accepte Cerberus OU Oracle (modele aero). Teste
     sur 3 scenarios (FIN->Oracle PASSE, FIN->Cerberus PASSE,
     FIN->autre agent KO).
  3. reactiver-fin : transmettre la cible oracle -> CORRIGE (--cible).

## 8. Prochaine etape

Appliquer les corrections pilote (agent habilite), aligner le garde-fou R7,
puis migrer agent par agent. L aero ne doit jamais voler seul : chaque
changement est valide par un test reel de bout en bout.