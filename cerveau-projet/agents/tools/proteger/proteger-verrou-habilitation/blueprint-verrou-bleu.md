---
identite:
  type: blueprint
  appartient_a: buffy
  commun: false
# Blueprint de conception -- Verrou bleu
# Deploiement de la source de verite de l habilitation vers l etat du round oracle

blueprint:
  nom: verrou-bleu
  version: "0.1.0"
  cree: "2026-08-30"
  agent_conception: buffy
  agent_implementation: vulcain
  priorite: URGENT
---
# BLUEPRINT -- VERROU BLEU
# Deplacer la source de verite de l habilitation vers l etat du round oracle-server
# (cause racine des sorties du flux formel / usurpation d identite)

## 1. PROBLEME (cause racine)

Quand un round casse, le LLM reprend la main et sort du flux. Pour utiliser un
outil dedie, il usurpe l identite de l agent habilite : il reecrit la colonne
"Agent actif" de la table "## Sessions connues" d AGENTS.md, puis appelle
l outil. Le verrou proteger-verrou-habilitation croit cette colonne
(agent_actif_session), car l identite y est AUTO-DECLAREE dans un fichier que
la session modifie directement.

ConsEquence : verrou grille a la source. L incarnation reelle de l agent
habilite n est pas garantie. Preuve DESCON 2026-08-29 : "le flux etait casse
et le LLM a repris la main".

## 2. PRINCIPE DE LA SOLUTION

La source de verite de l identite ne doit PLUS etre auto-declaree par la
session (AGENTS.md), mais MAINTENUE par oracle (etat du round). Le verrou
doit arreter de croire ce que la session pretend : il doit croiser la
demande avec l etat du round tel qu oracle le voit.

Definition : un agent est legitimement habilite pour un outil dedie SI ET
SEULEMENT SI oracle a un round formel en cours OU une mission relayee qui
designe cet agent comme maillon actif, et l outil est dans sa carte.

## 3. ARCHITECTURE CIBLE

### 3.1 Source de verite : l etat du round chez oracle

L etat du round est la suite de faits que oracle produit au fil de la
coordination :
- files/ (missions postees : asap / attente)
- historique : DEBUT/FIN historises pour chaque agent (qui a demarre quoi)
- inbox/ : messages relus par oracle vers chaque destinataire
- ou les trois sont ecrits par la session AUSSI (tous les fichiers sont
  accessibles). Une verification purement "statique" du contenu d un fichier
  n est donc pas suffisante.

### 3.2 Le vrai levier : le verrou interroge oracle AU CONTEXTE DU ROUND

Plutot que de lire une seule colonne, le verrou demande a oracle qui il
considere comme "maillon en cours" via la commande existante :

    python3 .../oracle.py mission-lister --statut EN_ATTENTE --agent <declare>

et croise avec :

    python3 .../oracle.py status          (serveur demarre ?)

critere BLOQUE si :
- aucune mission EN_ATTENTE/POSTEE pour l agent declare dans une file
  asap/normale (le round a ete relaye pour cet agent), OU
- la raison de la derniere activation de l agent (AGENTS.md) a ete
  reecrite a la main (incoherence historique oracle vs activer-agent-principal).

### 3.3 Renfort B : rien de dedie hors round route

Le verrou doit aussi verifier qu un round formel est en cours :
- au KO / rupture, la SEULE action autorisee du LLM est d appeler le
  protocole de fin (reactiver-fin / inter-round), JAMAIS d executer un outil
  dedie en direct.
- concretement : un outil dedie demande une mission active POUR l agent
  declare. Pas de mission -> BLOQUE + message "re-routez par le protocole".

### 3.4 Renfort C : verrouillage du retour

- oracle.historiser FIN ne doit etre accepte QUE par le maillon reellement
  actif (etat du round), pas par une session qui se declare n importe quel
  agent dans la raison.

## 4. POINT DE VIGILANCE TECHNIQUE (a trancher par vulcain)

TOUS les fichiers sont ecrits par le LLM avec acces shell. Une garde
cryptographique/administrative stricte est impossible sans serveur
separe. Le blueprint assume un serveur oracle DEMARRE qui detient l etat
en memoire/stockage et expose status : c est la seule autorite que la
session ne fabrique pas seule (processus, PID, port). La validation doit
trancher :
- (a) appuyer le verrou sur le statut du serveur oracle (direct, mais
  fragile si serveur arrete) ;
- (b) croiser avec l historique oracle des DEBUT/FIN (robuste hors serveur,
  mais fichiers ecrivables) ;
- (c) hybride : serveur + croisement historique = bloque meme au serveur
  arrete car la trace des DEBUT/FIN est coherente de maniere croisee.

RECOMMANDATION BUFFY : option (c) hybride. Le croisement historique
incoherent est le signal le plus fiable d une usurpation (re-ecriture a
la main du nom dans AGENTS.md sans DEBUT oracle correspondant).

## 5. CRITERE DE SUCCES

En l etat actuel (session sur Cerberus, pas janus) :
1. un appel `proteger-verrou-habilitation --agent janus --outil
   tester-lancer-non-regression` apres reecriture manuelle d AGENTS.md doit
   etre BLOQUE par le verrou ;
2. un test d usurpation d identite est ajoute a la non-regression (par
   morpheus) ;
3. au KO, le verrou renvoie l instruction "re-routez par le protocole de
   fin" au lieu de laisser passer.

## 6. PERIMETRE

- IMPLEMENTATION outils (proteger-verrou-habilitation.py, oracle.py, gestion
  d etat) : VULCAIN.
- TEST d usurpation + non-regression : MORPHEUS.
- FICHE de l outil / spec / index : Buffy apres implementation (selon le
  resultat retourne par vulcain).