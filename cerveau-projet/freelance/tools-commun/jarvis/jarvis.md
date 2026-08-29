---
identite:
  nom: JARVIS
  version: 0.5.2
  cree: 2026-08-22
  type: outil
  appartient_a: forge
  commun: true
  grade: gold
  medaille: ["outil-nevralgique", "communication"]
  notation: 90
  mot-cles: ["communication", "messages", "jarvis", "coordination", "freelance"]
  tags: communication, messages, coordination, freelance, v2
  session: freelance
# JARVIS -- Outil de communication inter-agents (v2)

> COMMANDE FONCTIONS : `python3 cerveau-projet/freelance/tools-commun/jarvis/jarvis.py --help`

---

## Vue d'ensemble

| Champ | Valeur |
|---|---|
| **Nom** | JARVIS |
| **Version** | 0.14.0 (py) -- encart 50 + corps 100 + BDD SQLite 7j (2026-08-26) |
| **Role** | Bus de messages inter-agents |
| **Responsable** | Forge (creation), Stark (usage) |
| **Session** | freelance |

---

## Principe

JARVIS est le **seul** moyen de communication inter-agents.
Pas de messages informels. Tout passe par JARVIS.

**Structure** :
```
tools-commun/jarvis/
|--- jarvis.md        <- ce fichier (contrat)
|--- jarvis.py        <- script (lancement)
|--- inbox/           <- messages recus par agent
|   |--- stark.jsonl
|   |--- shuri.jsonl
|   |--- forge.jsonl
|   +--- rogers.jsonl
+--- outbox/          <- messages envoyes par agent
    |--- stark.jsonl
    |--- shuri.jsonl
    |--- forge.jsonl
    +--- rogers.jsonl
```

**Format JSONL** (une ligne = un message) :
```json
{"de": "shuri", "vers": "stark", "priorite": 3, "date": "2026-08-22T20:45:00", "objet": "Rogers cree", "corps": "Rogers operationnel.", "lu": false, "accuse": false}
```

---

## Commandes

### Envoyer un message
```bash
python3 jarvis.py envoyer --de <expediteur> --vers <destinataire> --priorite <1-5> --objet "<objet>" --corps "<corps>" [--activer] [--session <session>]
```

**`--activer` (v0.3.0, livraison directe v0.6.1)** : le message DECLENCHE
l'activation du destinataire (bloc session AGENTS.md mis a jour +
incarnation obligatoire) ET EST LIVRE PAR AFFICHAGE : marque lu des
l'emission, l'agent DEMARRE DIRECTEMENT - plus de lire/acquitter apres
activation. C'est le mecanisme de continuite du round : le round ne
s'arrete jamais.

```
Round complet :
stark --vers jarvis --activer  ->  jarvis --vers agent --activer  ->
agent travaille -> agent --vers jarvis --activer  (inter-round si besoin) ->
jarvis --vers stark --activer  ->  stark actif, pret pour la suite.
```

### Lire les messages en attente
```bash
python3 jarvis.py lire --agent <agent>
```
Affiche les messages non-lus de l'agent. Si priorite 1 = **bloque** (l'agent ne demarre pas).
**v0.5.0** : les P3-P5 sont AUTO-ACQUITTES a la lecture - seuls P1/P2 exigent un acquittement explicite.

### Lire + acquitter tout en un appel (v0.5.0)
```bash
python3 jarvis.py recu --agent <agent>
```
Fluidite : remplace lire + acquitter xN (2-3 appels -> 1).

### Accuser reception
```bash
python3 jarvis.py acquitter --agent <agent> --id <id_message>
```
Marque le message comme lu + accuse. Le message expire apres accusation.
(Reserve desormais aux P1/P2 - voir auto-accuse v0.5.0.)

### Lister tous les messages
```bash
python3 jarvis.py lister --agent <agent> [--tous]
```
`--tous` = tous les messages (y compris lus). Sans flag = non-lus seulement.

### Verifier les bloquages
```bash
python3 jarvis.py bloques
```
Liste les agents qui ont des messages priorite 1 non-lus (= bloquants).

### Chaine de demarrage (v0.11.0, mission [AT-1])
```bash
python3 jarvis.py demarrage [--session session-freelance]
```
1. Tic des routines (jarvis EST le planificateur, protocole 16)
2. Etat DEFCON (5 = dev gele : escalade utilisateur)
3. Files d'attente + agents bloques
4. Declaration OPERATIONNEL + historisation.
Premier appel : quand Cerberus active Stark en debut de session.

### Arret propre (v0.11.0)
```bash
python3 jarvis.py arret [--session session-freelance]
```
Resume de session (DEFCON, files, routines) + historisation. Les files
sont persistees (JSONL) : rien a vider, la session est recoverable par
`demarrage`.

### Historiser a la demande
```bash
python3 jarvis.py historiser --agent <agent> --raison "<raison>" [--session session-freelance]
```
Trace une etape intermediaire SANS changer d'agent.

**Historisation v0.15.0 (2026-08-26, fichiers v2 SEPARES)** : la v2 est
l evolution de la v1, chaque session a SES fichiers (decision utilisateur) :
1. **AGENTS-activite-recente-v2.md** : encart session-freelance (50 entrees
   max, raison tronquee a 80 car., vue rapide) ; ordre des colonnes
   **Grade | Agent | Raison | Heure | id | Type** (decision utilisateur
   2026-08-26) : la colonne **Grade** (emoji couleur) est en tete - haut
   de grade = bleu/vert, bas de grade = rouge/orange, EDITH = rose
   (grades-v2.json) ;
2. **AGENTS-historique-v2.md** : chronologie body v2 (`## JJ/MM/AAAA` /
   `### agent` / `- HH:MM | id | TYPE | raison`), 100 dernieres actions ;
3. **historique.db** (SQLite) : journal chronologique complet, **texte integral**
   (pas de troncature), **purge automatique apres 7 jours** (lazy cleanup
   a chaque ecriture).

La session-admin (v1) a SES fichiers (ASCII+LF) : AGENTS-activite-recente.md
+ AGENTS-historique.md, geres par activer-agent-principal. Plus aucun
partage v1/v2 : chaque session ecrit dans SON fichier avec SON format
(v2 = UTF8+CRLF, v1 = ASCII+LF). Format de section corps : `## JJ/MM/AAAA`
(JAMAIS ISO YYYY-MM-DD : cree des sections paralleles vides, KO test-098).

**Grades et couleurs (v2, decision utilisateur 2026-08-26)** : la colonne
Grade de l encart affiche l emoji couleur du grade de l agent ou de la
routine (fichier de donnees D15 `tools-commun/grades/grades-v2.json`, jamais
en dur dans le code). Echelle : G1 bleu (jarvis, stark) / G2 vert (vision,
shuri, forge, rogers, parker) / G3 jaune (fury) / G4 rouge (routines de
surveillance) / G5 orange (citations, le plus bas - desactivee en fin de
dev) / SP rose (edith, couleur signature). Les routines historisent sous
LEUR propre nom (decision 2026-08-26 : flux, vigie, notation, harnais,
citations, integrite, orphelins - jamais sous un agent) pour que le grade
s affiche. Inconnu = blanc neutre.

---

## Regles

| Regle | Detail |
|---|---|
| **Priorite 1 = bloquant** | L'agent ne demarre PAS tant que le message n'est pas acquitte. |
| **Prise de relais obligatoire (v0.11.1, remplace incarnation v0.2.0)** | Chaque message d'activation contient : "Tu es l agent <nom>. AVANT DE COMMENCER : lis ta fiche et tes corrections puis PRENDS LE RELAIS." (decision utilisateur 2026-08-24 : le message s'adresse a l'agent lui-meme - il ne s'incarne pas, il EST) |
| **Expiration apres lu** | Un message expire apres avoir ete lu et accuse. |
| **Accuse obligatoire** | Chaque message doit etre acquitte par le destinataire. |
| **Seul canal** | JARVIS est le SEUL moyen de communication inter-agents. |
| **SSOT** | Le message vit dans inbox/ (destinataire) + outbox/ (expediteur). |
| **D15 agents** | La liste des agents valides est lue depuis jarvis-data.json (champ `agents`), pas codee en dur. |

---

## Integration avec les cartes

Dans la case de depart (c0) d'un agent freelance :
```
1. Lire inbox/<agent>.jsonl -> afficher messages en attente
2. Si priorite 1 non-lu = BLOQUER (ne pas continuer)
3. Acquitter les messages lus
4. Continuer le parcours
```
