# Protocole Immuable -- Identification des Agents
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

