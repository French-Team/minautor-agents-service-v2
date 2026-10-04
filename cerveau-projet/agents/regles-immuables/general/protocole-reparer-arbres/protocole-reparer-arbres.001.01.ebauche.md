---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
# Protocole -- Reparer les Arbres de Decision

**Version** : 0.1.0
**Statut** : ebauche
**Date creation** : 2026-08-29
**Agent** : Buffy (lecons du round reparation Cerberus/Oracle 2026-08-29)

---

## Contexte -- pourquoi les rounds cassent

Les agents sont diriges par le **PILOTE ORACLE** (maitre d hotel) : a
l activation d une mission, le pilote deduit un TYPE DE MISSION depuis la
raison (`_type_mission_auto` dans `pilote.py`), puis le route dans
l ARBRE de decision de l agent (`_resoudre_racine`). La RACINE de l arbre
propose des branches (ex : TESTER / VERIFIER / AUTRE). Si le type deduit n a
AUCUNE branche correspondante dans la racine, le pilote s arrete net :

```
DECISION LIBRE : theme '<type>' non reconnu dans la racine.
```

L agent recoit sa mission SANS aucun guidage : le round est casse au premier
pas. C est une cause racine des missions qui "ne demarrent plus" (constate
2026-08-29 sur le round Cerberus/Oracle).

Exemple reel (morpheus, hors perimetre de la reparation en cours) : mission
"Resoudre les 5 KO ... corriger ..." -> pilote deduit `modifier` ; la racine
de `arbre-morpheus.json` ne propose que TESTER/VERIFIER/AUTRE -> stall
immediat. Meme classe de defaut pour tous les arbres dont la racine ne couvre
pas le vocabulaire du pilote.

## Source de verite du vocabulaire (a ne PAS dupliquer)

Le vocabulaire vit dans `cerveau-projet/agents/tools/oracle/fonctions/pilote.py` :
- `_type_mission_auto(raison)` : la liste des types deductibles (construire,
  modifier, tester, audit, retour, autre, ...).
- `_resoudre_racine(racine, etat)` : la correspondance type -> branche
  (reponse exacte d abord, puis repli par mots-cles sur la mission, puis
  ACCUEIL/AUTRE si presents).

REGLES DE REPARATION CONTRE CETTE SOURCE :
- On n invente JAMAIS un nouveau type dans un arbre sans l ajouter au
  vocabulaire de `pilote.py` (sinon le pilote ne pourra jamais le choisir).
- On n ajoute JAMAIS une branche de racine que le pilote ne peut pas
  atteindre (branche morte = incoherence).
- On ne retire JAMAIS une branche que le pilote utilise (reponse exacte
  ou mots-cles).

## Le test reel de diagnostic (AVANT toute reparation)

1. Etat de carte : `python3 cerveau-projet/agents/tools/oracle/oracle.py
   activer <agent> "<mission reelle>"`
2. Pilotage : `python3 cerveau-projet/agents/tools/oracle/oracle.py pilote
   <agent> --limite 60`
3. SYMPTOMES a chercher dans la sortie :
   - `theme '<type>' non reconnu dans la racine` -> racine incomplete
   - `DECISION LIBRE` trop tot (avant toute action) -> question non routable
   - `vers <cible> INEXISTANT` / `REPONSE '<x>' sans branche` -> reference
     pendante ou libelle de branche desaligne
4. Audit de couverture : comparer `racine.branches[].reponse` de
   `arbre-<agent>.json` avec les types que `_type_mission_auto` produit pour
   les missions du domaine de l agent.

## Protocole de reparation (UN AGENT A LA FOIS, case par case)

> REGLE DE METHODE (demande utilisateur 2026-08-29) : on ne repare JAMAIS
> plusieurs agents en parallele. Un seul agent a la fois, relu MOT PAR MOT,
> CASE PAR CASE. Une erreur corrigee a la hate se propage partout : si on se
> trompe sur un agent, on se trompe sur tous.

### Etape 1 -- Inventaire de l agent
- Fichiers : `arbre-<agent>.json` (PRIORITAIRE, format v2-like) et/ou
  `parcours-<agent>.json` (format v1), plus les `theme-*.json` references.
- Le pilote choisit l arbre en priorite (`_pilote_parcours_agent` dans
  `oracle.py` : arbre > parcours).

### Etape 2 -- La racine couvre-t-elle le domaine ?
- Lister `racine.branches[].reponse` de l arbre.
- Lister les types deductibles pertinents pour le ROLE de l agent.
- TOUT type pertinent doit avoir UNE branche `reponse` -> `theme-<type>.json`.
- Si un type manque : ajouter la branche, OU router le type vers un theme
  existant pertinent (jamais vers rien). Le theme AUTRE est le filet de
  securite des missions hors domaine.

### Etape 3 -- Chaque branche mene a un theme qui EXISTE
- Verifier que chaque `vers` de la racine pointe vers un `theme-*.json`
  present dans le dossier `parcours/` de l agent.
- Verifier que chaque redirect du theme sert des ETAPES/COMMANDES valides
  (chemins reels) et des regles non contradictoires.

### Etape 4 -- Les deux sens pour les routeurs
- Un ROUTEUR (ex : Cerberus) a DEUX entrees pilotees :
  - sens MISSION (demande utilisateur) -> theme DE-USER (ou equivalent)
  - sens RETOUR (bilan d un agent via Oracle) -> theme DE-ORACLE (ou
    equivalent)
- Pattern Cerberus (pilote.py `_resoudre_racine`) : DE-USER par defaut,
  DE-ORACLE quand la mission est un retour (`RETOUR`/`bilan`/`reactivation`).
  Reproduire ce pattern pour tout routeur ; ne JAMAIS forcer un seul sens.

### Etape 4 bis -- La FIN doit etre precedent-aware
- Un agent qui PEUT etre active en inter-round par un autre agent DOIT avoir :
  - une branche `INTER-ROUND` dans sa racine -> theme-inter-round ;
  - ses fins de mission en `oracle.py reactiver-fin <agent> "<bilan>"` (qui
    lit le `precedent` de l etat de carte et reactive L APPELANT si != cerberus)
    et NON en reactiver cerberus en dur.
- Verifier que chacune de ses fins (ex: fin-tester, fin-verifier,
  fin-inter-round) utilise reactiver-fin, sauf si l agent est un maillon
  terminal qui revient toujours a Cerberus. Voir protocole-fin-mission v0.3.0.

### Etape 5 -- Coherence interne (sur CHAQUE case/redirect)
- Pas de doublon de `reponse` dans une meme question : 2 branches a la meme
  reponse vers des cibles differentes = contradiction "aller a droite puis a
  gauche" (le defaut typique que l agent subit).
- Pas de cible pendante (`suivant`/`vers` vers une case/theme inexistant).
- Pas de boucle involontaire : les boucles d attente (reponse NON -> soi-meme)
  sont legitimes, les boucles sans sortie ne le sont pas.
- Relire le TEXTE des etapes successives : deux instructions consecutives qui
  se contredisent (droite puis gauche) = incoherence a corriger.

### Etape 6 -- Tester reellement
- `oracle.py pilote <agent>` : le round doit avancer case par case jusqu a
  une VRAIE decision libre (delegation) ou la fin. Plus JAMAIS de stall a la
  racine.
- Si l agent est un routeur : tester les DEUX sens (mission + retour).
- Si l agent a un theme-inter-round : verifier que sa fin est precedent-
  aware (`oracle.py reactiver-fin <agent>` quand son precedent est un agent)
  et qu elle reactive l APPELANT et non Cerberus pour un inter-round.

### Etape 7 -- Non-regression
- Lancer les garde-fous des arbres/parcours (verifier les numeros dans
  SERIES du lanceur) : `--tests test-006,test-070,test-071,test-072,test-073`
  + les tests de valider-cartes/tableaux, puis la serie complete.
- Un arbre modifie reste : JSON valide, ASCII pur, LF pur.

## Checklist (a copier dans chaque mission de reparation)

- [ ] arbre OU parcours identifie (arbre prioritaire)
- [ ] les deux sens du routeur (mission + retour) testes
- [ ] si theme-inter-round : fins precedent-aware via reactiver-fin (appelant)
- [ ] racine couvre TOUS les types deductibles du domaine (contre pilote.py)
- [ ] chaque branche de la racine -> theme EXISTANT
- [ ] themes relus mot par mot : etapes/commandes valides, regles coherentes
- [ ] routeurs : sens MISSION + sens RETOUR pilotes (pattern Cerberus)
- [ ] 0 doublon de reponse, 0 cible pendante, 0 boucle sans sortie
- [ ] texte des etapes sans contradiction consecutive
- [ ] pilote teste reellement (mission + retour le cas echeant)
- [ ] garde-fous arbres/parcours verts, JSON valide, ASCII/LF

---

## Historique

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-29 | Creation : protocole de reparation des arbres de decision (aligner la racine sur le vocabulaire du pilote `_type_mission_auto`/`_resoudre_racine`), methode UN AGENT A LA FOIS, test reel de diagnostic, checklist. Lecons du round Cerberus/Oracle (canal mission + retour pilotes). |
