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