# Protocole Immuable — Identification des Agents
---

## Principe Fondamental
---

## Pourquoi cette méthode ?

| Étape | Avantage | Limite |
|---|---|---|
| **L'utilisateur nomme** | Simple, direct | Nécessite que l'utilisateur connaisse le nom |
| **L'agent lit demarrer.md** | Comprend le processus | Nécessite de lire le fichier |
| **L'agent vérifie AGENTS.md** | Voit qui est actif | Nécessite de lire le fichier |
| **L'agent devient celui qui est nommé** | Simple et efficace | -- |

---

## Étape 1 — Répondre à la salutation
```
1. Lire demarrer.md (ce fichier)
2. Identifier le nom de l'agent dans la salutation
3. Vérifier AGENTS.md :
   a. Si l'agent nommé est déjà actif → confirmer et continuer
   b. Si un autre agent est actif → devenir l'agent nommé
4. Aller à l'étape 2
```

### Format de réponse

```
Bonjour [nom-agent] !
Je suis [nom-agent], [rôle].
Je prends le relais pour cette session.
```

### Exemples

```
Bonjour Buffy !
Je suis Buffy, agent principal -- développeur du cerveau-projet.
Je prends le relais pour cette session.
```

```
Bonjour Atlas !
Je suis Atlas, explorateur et documentaliste.
Je prends le relais pour cette session.
```

---

## Étape 2 — Vérifier et créer la fiche

```
1. Vérifier si une fiche existe pour cet agent :
   - Aller dans agents/
   - Chercher le dossier agents/[nom-agent]/
2. Si le dossier n'existe pas → le créer :
   a. Créer le dossier agents/[nom-agent]/
   b. Copier agents/fiche-agent-template.md → agents/[nom-agent]/[nom-agent].md
   c. Copier agents/corrections-template.md → agents/[nom-agent]/corrections.md
   d. Remplir la fiche avec les informations de l'agent
   e. Laisser les corrections vides
3. Si le dossier existe → aller à l'étape 3
```

---

## Étape 3 — Vérifier l'existence de la fiche

```
1. Aller dans agents/
2. Chercher le dossier agents/[nom-agent]/
3. Si le dossier existe → lire la fiche (étape 4)
4. Si le dossier n'existe pas → le créer (étape 5)
```

---

## Étape 4 — Lire la configuration existante

```
1. Lire agents/[nom-agent]/corrections.md EN PREMIER
2. Lire agents/[nom-agent]/[nom-agent].md
3. Appliquer les surcharges et corrections
4. Noter les règles spécifiques à respecter
```

### Ordre de lecture

| Priorité | Fichier | Contenu |
|---|---|---|
| 1 | `corrections.md` | Règles spécifiques, surcharges, corrections |
| 2 | `[nom-agent].md` | Fiche principale (après surcharge) |

---

## Étape 5 — Créer la fiche (si elle n'existe pas)

```
1. Créer le dossier agents/[nom-agent]/
2. Copier agents/fiche-agent-template.md → agents/[nom-agent]/[nom-agent].md
3. Copier agents/corrections-template.md → agents/[nom-agent]/corrections.md
4. Remplir la fiche avec les informations de l'agent
5. Laisser les corrections vides
```

### Structure créée

```
agents/[nom-agent]/
├── [nom-agent].md        ← fiche de l'agent
└── corrections.md         ← surcharges/corrections (vide)
```

---

## Étape 6 — Mettre à jour AGENTS.md

```
1. Lire AGENTS.md
2. Mettre à jour la section "Agent Principal Actuel"
3. Ajouter/MAJ l'historique des agents
4. Signer : "[nom-agent] -- [date]"
```

---

## Étape 7 — Confirmer l'identification
```
[ ] AGENTS.md est à jour
[ ] La fiche d'agent existe et est lue
[ ] Les corrections sont lues et appliquées
[ ] L'agent s'est présenté
[ ] Les règles spécifiques sont notées
```

---

## Cas particuliers

### Changement d'agent

```
1. L'agent actuel termine sa session
2. Le nouvel agent lit AGENTS.md
3. Le nouvel agent se présente
4. Le nouvel agent lit/crée sa fiche
5. Le nouvel agent met à jour AGENTS.md
6. L'agent précédent conserve ses corrections
```

### Premier démarrage (AGENTS.md vide)

```
1. Lire AGENTS.md (vide ou incomplet)
2. Se présenter
3. Créer sa fiche
4. Remplir AGENTS.md pour la première fois
5. Devenir l'agent principal
```

### Retour après absence

```
1. Lire AGENTS.md
2. Vérifier si on est encore l'agent principal
3. Si oui → lire sa fiche et ses corrections
4. Si non → lire la fiche du nouvel agent
5. Mettre à jour AGENTS.md si nécessaire
```

---

## Validation

Avant de valider l'identification, vérifier :

- [ ] AGENTS.md a été lu
- [ ] L'agent s'est présenté
- [ ] La fiche d'agent existe
- [ ] Les corrections sont lues
- [ ] AGENTS.md est à jour
- [ ] Les règles spécifiques sont notées

---

## Liens

- **Règle** : [regles-choisir-agent.md](../regles-choisir-agent.md) -- choisir le bon agent
- **Protocole** : [protocole-auto-correction](../protocole-auto-correction/) -- auto-correction
- **Template** : [fiche-agent-template.md](../../../../agents/fiche-agent-template.md)
- **Index** : [index-agents.md](../../../../agents/index-agents.md)

---

