# Missions de Revision -- 2026-08-30

## Resume

| Niveau | Nombre |
|---|---|
| URGENT | 2 |
| IMPORTANT | 1 |
| MOYEN | 0 |
| BAS | 0 |

### [IMPORTANT] Audit education v1->v2 : residus de pilotage v1 dans les arbres v2 (Chiron)

- **Date** : 2026-08-30 (demande utilisateur : verifier l education des agents passes de la v1 a la v2)
- **Agent habilite** : chiron (educateur) - detecte et documente, corrections appliquees par buffy
- **Constat deja identifie par socrate** : 6 agents (chiron, gardien, hygie, minerve, promethee, socrate) ont dans leur theme-outils.json v2 l instruction "Reprendre a la case d arret : relancer guider-parcours avec --case <cid>" - c est le pilote V1. En v2 le pilote est guider-arbre. Un agent qui suit cette case relancerait le mauvais outil.
- **Description (audit complet par agent)** :
  - Pour CHAQUE agent : verifier fiche + corrections + themes v2 + fins.json - aucun residu v1 ACTIF (pilote, commandes guider-parcours actives) ; archives et lecons historiques CONSERVES.
  - Inventaire des residus detectes (agent par agent, fichier par fichier).
  - Rapport de Chiron : liste des corrections a appliquer par buffy.
- **Raison** : un agent qui suit une instruction v1 dans son arbre v2 sort du flux v2 au pire moment (reprise apres incident).
- **Perimetre (decision utilisateur)** : AUDIT COMPLET par agent - fiche + corrections + themes v2 + fins.json - aucun residu v1 ACTIF (pilote, commandes) ; archives et lecons historiques CONSERVES. Chiron DETECTE et DOCUMENTE (regle absolue 1 : ne corrige pas) - rapport des corrections pour buffy, qui appliquera.

## Missions

### [URGENT] Verrou BLEU : deplacer l habilitation des outils dedies vers l etat oracle (cause racine des sorties de flux)

- **Date** : 2026-08-30 (demande utilisateur "resoudre les problemes qui provoquent les sorties du flux formel")
- **Agent habilite** : buffy (developpeur principal) + retour vers super-combo
- **Constat (cause racine confirmee)** : quand un round casse (KO, boucle, mission avortee), le LLM reprend la main et sort du flux. Pour utiliser un outil dedie, il usurpe l identite de l agent habilite en reecrivant la colonne "Agent actif" de la table "## Sessions connues" d AGENTS.md, que le verrou d habilitation (proteger-verrou-habilitation) croit aveuglement. L identite est auto-declaree dans un fichier que l usurpateur controle -> verrou grille a la source. Evidence dans le log DEFCON 2026-08-29 : "le flux etait casse et le LLM a repris la main".
- **Description (Option 1 - Verrou bleu, choisie par l utilisateur)** :
  - Deplacer la SOURCE DE VERITE de l identite actuelle (AGENTS.md, editable par la session) vers l ETAT DU ROUND maintenu par oracle-server (fichiers files/, stats, processus serveur) quand le serveur est demarre et consomme les missions.
  - Le verrou d habilitation ne doit PLUS croire la session auto-declaree : il doit verifier que la demande a transite par le round formel (Cerberus -> oracle -> pilote) et que l agent est reellement le maillon actif de la session selon oracle-server.
  - B en renfort : aucune action dediee possible hors d un round route (au KO, le LLM doit re-router par le protocole, jamais agir en direct).
  - C en renfort : au ko, la seule action autorisee est l appel au protocole de fin/rupture (inter-round / reactivation), jamais l execution directe.
- **Raison** : arreter les reprises de main du LLM (cause de DEFCON 5 repetes), restaurer l incarnation reelle des agents habilites, faire respecter regles/protocoles/conventions.
- **Dependances** : comprehension de proteger-verrou-habilitation (python3 .../proteger-verrou-habilitation.py --agent <nom> --outil <nom>, source AGENTS.md "## Sessions connues") ; archivage de la mission purge P1 ci-dessous.
- **Critere de succes** : en l etat actuel (session sur Cerberus, pas janus), le verrou BLOQUE un --agent janus reecrit a la main dans AGENTS.md ; un test d usurpation d identite est ajoute a la non-regression (par morpheus) ; au KO, le LLM re-route par le protocole au lieu d agir en direct.

### [URGENT] Purge des P1 non-acquittes du round (super-combo agent par agent)

- **Agent habilite** : super-pilote (orchestration) + chacun des destinataires en inter-round (buffy, janus, cerberus, morpheus, themis, vulcain, oracle, socrate)
- **Description** :
  - Inventaire des 18 P1 non-lus/non-accuses deja dresse (id + destinataire + date + objet).
  - Pour CHAQUE destinataire, lui faire LIRE puis ACQUITTER ses P1 (`oracle.py acquitter <agent> <id>`), un par un, en inter-round court, dans l ordre du plus charge au plus leger :
    - buffy (5 P1 : 705b4ed3, 9792c6e3, verifier-statuts-204006, verifier-statuts-205008, verifier-statuts-205510)
    - janus (5 P1 : 6fedb0fd, 81063597, e558abe1, verifier-statuts-140847, verifier-statuts-144050)
    - cerberus (2 P1 : aed9515a, verifier-statuts-144050)
    - morpheus (2 P1 : fd08904c, fd3d1ea8)
    - themis (1), vulcain (1), oracle (1), socrate (1)
  - Verifier la nominalisation : la routine de surveillance doit nommer precisement qui doit lire/acquitter pour eviter la recidive.
- **Raison** : arreter l escalade DEFCON (monte vers 4, deja eu DEFCON 5) et desengorger les files asap/attente (~60 asap, 34 attente) qui saturent le round.
- **Dependances** : aucune bloquante (infrastructure v2 verte : 107/107 tests OK).
- **Critere de succes** : 0 P1 non-acquitte restant ; files asap/attente sous le seuil ; DEFCON redescendu ; round re-fonctionnel.

## Bilan de la purge (2026-08-30 14:5x)

- SUPER-COMBO purge-p1 lance par le super-pilote : 8 missions postees (asap)
  et relayees chez chaque destinataire (buffy, janus, cerberus, morpheus,
  themis, vulcain, oracle, socrate).
- Purge executee : 0 P1 non-acquitte restant (inventaire complet revu :
  buffy 5, janus 5, cerberus 2, morpheus 2, themis 1, vulcain 1,
  oracle 3, socrate 1 - tous acquittes apres lecture).
- Files : asap 0 EN_ATTENTE ; attente 34 EN_ATTENTE (missions mises en
  attente par les inter-round URGENT passes - a reprendre quand les rounds
  reprennent).
- CRITERE PRINCIPAL ATTEINT : 0 P1 non-acquitte.