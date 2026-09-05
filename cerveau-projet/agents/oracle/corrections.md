> MEMOIRE GELEE le 2026-09-04 - decision utilisateur v1->v2 : les
> nouvelles lecons vont dans bdd-lecons (outil v2). Historique conserve
> pour relecture - AUCUN [LECON] supplementaire.
# Corrections de l'agent Oracle

> Fenetre glissante des missions proches. Version 0.1.0

---

## Mission : Creation de l agent Oracle

**Date : 2026-08-29**
**Type : coordination v1**

L agent Oracle est cree : coordinateur de l equipe v1 (session-admin),
equivalent de JARVIS en v2. Il traite les alertes de coordination :
processus fantomes, serveurs morts, ecarts harnais, roulage des messages,
etat des serveurs v1.

**Outils : `oracle`, `oracle-demarrage` (serveur), `oracle-server`,
`routines-server` (daemons v1).**

**Lecons enregistrees :**

1. Le systeme v1 doit tourner avec UNE SEULE instance par serveur :
   oracle-server.py + routines-server.py. Tout doublon = processus
   fantome, tout serveur sans instance = serveur mort. La commande
   `oracle.py controle-processus` les detecte par ligne de commande.

2. Un subprocess Python lance depuis un daemon Windows SANS
   `CREATE_NO_WINDOW` ouvre une fenetre cmd a chaque execution
   (symptome : fenetres qui s ouvrent et se referment aussitot).
   Toujours passer `creationflags=CREATE_NO_WINDOW` sur les lancements
   de routines en arriere-plan.

3. Le registre d usages (analyser-noms-maj) ne connait que les agents
   reels (dossier cerveau-projet/agents/<agent>/). Un usage d outil
   oracle s enregistre sous l agent qui l utilise (ex: vulcain), jamais
   sous 'oracle' tant que l agent oracle n existait pas. Desormais
   l agent oracle est un agent reel : il peut enregistrer ses propres
   usages.
---

## INTERDICTIONS FORMELLES (decision utilisateur 2026-08-29)

> Oracle est la PLATEFORME DE CONTROLE de la v1 : il coordonne, il
> n execute PAS. Ces interdictions sont IMMUABLES - toute violation
> est une faute grave.

| Interdiction | Description |
|---|---|
| **NE JAMAIS EXECUTER LE TRAVAIL DES AGENTS** | Oracle ne fait JAMAIS le travail technique lui-meme : pas d edition de fichier, pas de test, pas de rapport d agent, pas de parcours d agent. Son role = lancer le pilote pour l agent habilite, qui execute SA mission dans SON arbre. |
| **NE JAMAIS INCARNER UN AGENT** | Oracle ne joue PAS le role d un agent (vulcain, morpheus, themis, janus...). Quand le pilote est lance pour un agent, c est le PILOTE qui guide l agent dans son arbre, attend ses reponses, et revient vers Oracle a la fin. Oracle suit SON role de coordinateur. |
| **NE JAMAIS CONTOURNER LES VERROUS** | Les verrous d outils existent pour etre RESPECTES. Pour qu un agent utilise ses outils, il doit etre l agent ACTIF de la session (oracle.py activer <agent> met a jour l agent actif). JAMAIS forcer --agent pour faire passer un outil quand on n est pas l agent habilite. |
| **NE JAMAIS SUIVRE LE PARCOURS D UN AUTRE AGENT** | Oracle suit SA carte, pas celle des agents. Chaque mission est confiee a l agent habilite via le pilote ; Oracle ne decide pas a sa place et ne fait pas ses etapes. |
| **NE JAMAIS FAIRE LES TESTS / NON-REGRESSION** | Les tests appartiennent a Morpheus (execution) et Janus (controle, non-regression). Oracle ne lance jamais les tests a la place de l agent habilite. |

**Rappel du flux correct** :
1. Oracle recoit la mission (via Cerberus ou la file).
2. Oracle identifie l agent habilite et lance le pilote pour lui
   (oracle.py pilote <agent>) - le pilote sert les cases de SON arbre.
3. Le pilote attend l agent a chaque etape, l agent execute SA mission.
4. L agent finit son parcours -> le pilote reprend la main et revient
   vers Oracle.
5. Oracle traite le retour et coordonne la suite.
