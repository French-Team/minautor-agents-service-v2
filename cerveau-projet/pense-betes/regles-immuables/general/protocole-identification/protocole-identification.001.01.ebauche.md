# Protocole Immuable -- Identification des Agents

**Version** : 0.2.0 (MODE ID multi-session -- v0.4.0)
**Statut** : ebauche

---

## EVOLUTION v0.4.0 -- MODE ID MULTI-SESSION (methode actuelle)

> **REGLE UTILISATEUR (IMMUABLE -- MODE ID)** : chaque LLM possede SON id, donne
> par l'utilisateur au lancement (ex: `llm-1`, `llm-atlas`). La session d'un LLM
> est LIEE a son id.
> **REGLE ALIGNEMENT (v0.4.0)** : id `llm-N` -> session `session-llm-N`. Le numero
> de session PORTE le numero de l'id : "je suis llm-1, ma session est session-llm-1".
> **SOURCE DOUBLE** : chaque bloc de session dans AGENTS.md contient le champ
> `| **Id LLM** | <id> |`. Le LLM se reconnait en lisant AGENTS.md : le bloc qui
> porte SON id est SON bloc.

### Le processus (MODE ID)

```
1. Noter MON id (donne par l'utilisateur au lancement, ex: llm-1)
2. Lire AGENTS.md et chercher MON bloc : celui dont le champ **Id LLM** = MON id
   -> trouve = MA session (ex: session-llm-1) -- c'est MA session, redemarrage du meme LLM
   -> absent = je n'ai pas encore de session -> etape 3
3. Lancer : python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py sidentifier <mon-id>
   -> l'outil compare MON id aux sessions enregistrees (AGENTS.md champ Id LLM + classeur)
   -> id deja lie = MA session retrouvee
   -> id inconnu llm-N = creation de session-llm-N (alignement sur l'id) + liaison
   -> id inconnu non numerique = prochaine session libre + liaison
   -> met Cerberus comme agent principal de la session (le LLM demarre comme Cerberus)
4. Lire la session RENDUE par l'outil (ou trouvee dans AGENTS.md) et la noter
5. Utiliser CETTE session pour toutes les activations :
   python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py activer <session> <agent> <raison>
   python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py reactiver <session> <raison> <agent>
```

> **CONFLIT D'ALIGNEMENT** : si session-llm-N est deja liee a un AUTRE id, l'outil
> affiche un message clair et attribue la prochaine session libre.
> **DEUX LLM DIFFERENTS NE PARTAGENT JAMAIS UNE SESSION** : la comparaison se fait
> sur l'ID. Si je n'ai pas d'id, je le DEMANDE a l'utilisateur avant toute action.

> Le contenu ci-dessous (etapes 1-7) documente le processus historique
> d'identification par salutation. La methode actuelle est le **MODE ID** ci-dessus :
> l'identification par salutation complete l'alignement (l'utilisateur nomme
> l'agent apres l'id).

---

## Principe Fondamental
---

## Pourquoi cette methode ?

| Etape | Avantage | Limite |
|---|---|---|
| **L'utilisateur nomme** | Simple, direct | Necessite que l'utilisateur connaisse le nom |
| **L'agent lit demarrer.md** | Comprend le processus | Necessite de lire le fichier |
| **L'agent verifie AGENTS.md** | Voit qui est actif | Necessite de lire le fichier |
| **L'agent devient celui qui est nomme** | Simple et efficace | -- |

---

## Etape 1 -- Repondre a la salutation
```
1. Lire demarrer.md (ce fichier)
2. Identifier le nom de l'agent dans la salutation
3. Verifier AGENTS.md :
   a. Si l'agent nomme est deja actif -> confirmer et continuer
   b. Si un autre agent est actif -> devenir l'agent nomme
4. Aller a l'etape 2
```

### Format de reponse

```
Bonjour [nom-agent] !
Je suis [nom-agent], [role].
Je prends le relais pour cette session.
```

### Exemples

```
Bonjour Buffy !
Je suis Buffy, agent principal -- developpeur du cerveau-projet.
Je prends le relais pour cette session.
```

```
Bonjour Atlas !
Je suis Atlas, explorateur et documentaliste.
Je prends le relais pour cette session.
```

---

## Etape 2 -- Verifier et creer la fiche

```
1. Verifier si une fiche existe pour cet agent :
   - Aller dans agents/
   - Chercher le dossier agents/[nom-agent]/
2. Si le dossier n'existe pas -> le creer :
   a. Creer le dossier agents/[nom-agent]/
   b. Copier agents/fiche-agent-template.md -> agents/[nom-agent]/[nom-agent].md
   c. Copier agents/corrections-template.md -> agents/[nom-agent]/corrections.md
   d. Remplir la fiche avec les informations de l'agent
   e. Laisser les corrections vides
3. Si le dossier existe -> aller a l'etape 3
```

---

## Etape 3 -- Verifier l'existence de la fiche

```
1. Aller dans agents/
2. Chercher le dossier agents/[nom-agent]/
3. Si le dossier existe -> lire la fiche (etape 4)
4. Si le dossier n'existe pas -> le creer (etape 5)
```

---

## Etape 4 -- Lire la configuration existante

```
1. Lire agents/[nom-agent]/corrections.md EN PREMIER
2. Lire agents/[nom-agent]/[nom-agent].md
3. Appliquer les surcharges et corrections
4. Noter les regles specifiques a respecter
```

### Ordre de lecture

| Priorite | Fichier | Contenu |
|---|---|---|
| 1 | `corrections.md` | Regles specifiques, surcharges, corrections |
| 2 | `[nom-agent].md` | Fiche principale (apres surcharge) |

---

## Etape 5 -- Creer la fiche (si elle n'existe pas)

```
1. Creer le dossier agents/[nom-agent]/
2. Copier agents/fiche-agent-template.md -> agents/[nom-agent]/[nom-agent].md
3. Copier agents/corrections-template.md -> agents/[nom-agent]/corrections.md
4. Remplir la fiche avec les informations de l'agent
5. Laisser les corrections vides
```

### Structure creee

```
agents/[nom-agent]/
|-- [nom-agent].md        <- fiche de l'agent
``-- corrections.md         <- surcharges/corrections (vide)
```

---

## Etape 6 -- Mettre a jour AGENTS.md

```
1. Lire AGENTS.md
2. Mettre a jour la section "Agent Principal Actuel"
3. Ajouter/MAJ l'historique des agents
4. Signer : "[nom-agent] -- [date]"
```

---

## Etape 7 -- Confirmer l'identification
```
[ ] AGENTS.md est a jour
[ ] La fiche d'agent existe et est lue
[ ] Les corrections sont lues et appliquees
[ ] L'agent s'est presente
[ ] Les regles specifiques sont notees
```

---

## Cas particuliers

### Changement d'agent

```
1. L'agent actuel termine sa session
2. Le nouvel agent lit AGENTS.md
3. Le nouvel agent se presente
4. Le nouvel agent lit/cree sa fiche
5. Le nouvel agent met a jour AGENTS.md
6. L'agent precedent conserve ses corrections
```

### Premier demarrage (AGENTS.md vide)

```
1. Lire AGENTS.md (vide ou incomplet)
2. Se presenter
3. Creer sa fiche
4. Remplir AGENTS.md pour la premiere fois
5. Devenir l'agent principal
```

### Retour apres absence

```
1. Lire AGENTS.md
2. Verifier si on est encore l'agent principal
3. Si oui -> lire sa fiche et ses corrections
4. Si non -> lire la fiche du nouvel agent
5. Mettre a jour AGENTS.md si necessaire
```

---

## Validation

Avant de valider l'identification, verifier :

- [ ] AGENTS.md a ete lu
- [ ] L'agent s'est presente
- [ ] La fiche d'agent existe
- [ ] Les corrections sont lues
- [ ] AGENTS.md est a jour
- [ ] Les regles specifiques sont notees

---

## Liens

- **Regle** : [regles-choisir-agent.md](../regles-choisir-agent.md) -- choisir le bon agent
- **Protocole** : [protocole-auto-correction](../protocole-auto-correction/) -- auto-correction
- **Template** : [fiche-agent-template.md](../../../../agents/fiche-agent-template.md)
- **Index** : [index-agents.md](../../../../agents/index-agents.md)

---

