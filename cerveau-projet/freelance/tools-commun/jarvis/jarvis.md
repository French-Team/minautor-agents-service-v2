---
identite:
  nom: JARVIS
  version: 0.5.0
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
| **Version** | 0.1.0 |
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
├── jarvis.md        <- ce fichier (contrat)
├── jarvis.py        <- script (lancement)
├── inbox/           <- messages recus par agent
│   ├── stark.jsonl
│   ├── shuri.jsonl
│   ├── forge.jsonl
│   └── rogers.jsonl
└── outbox/          <- messages envoyes par agent
    ├── stark.jsonl
    ├── shuri.jsonl
    ├── forge.jsonl
    └── rogers.jsonl
```

**Format JSONL** (une ligne = un message) :
```json
{"de": "shuri", "vers": "stark", "priorite": 3, "date": "2026-08-22T20:45:00", "objet": "Rogers cree", "corps": "Rogers opérationnel.", "lu": false, "accuse": false}
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
1. Lire inbox/<agent>.jsonl → afficher messages en attente
2. Si priorite 1 non-lu = BLOQUER (ne pas continuer)
3. Acquitter les messages lus
4. Continuer le parcours
```
