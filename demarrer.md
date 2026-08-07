# Demarrage -- comment utiliser ce cerveau
---

## 0. Identification de l'agent (OBLIGATOIRE)

### Etape 0.0 -- S'identifier (session LLM) - OBLIGATOIRE

> **MULTI-SESSION** : plusieurs LLM peuvent travailler sur le meme projet. Chaque LLM a SON bloc dedie dans AGENTS.md et SON agent principal.

> **REGLE UTILISATEUR (IMMUABLE -- MODE ID)** : chaque LLM possede SON id, donne par l'utilisateur
> au lancement (ex: `llm-atlas`, `llm-2`...). La session d'un LLM est LIEE a son id.
> **UN LLM NE DEDUIT JAMAIS SA SESSION D'AGENTS.md** : la session visible appartient a un AUTRE LLM.
> Sa session est celle que l'outil lui rend via SON id.

```
1. Noter MON id (donne par l'utilisateur au lancement, ex: llm-atlas)
2. Lancer : python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py sidentifier <mon-id>
   -> l'outil compare MON id aux sessions enregistrees (classeur)
   -> id deja lie = MA session retrouvee (ex: session-llm-2) -- redemarrage du meme LLM
   -> id inconnu  = creation de la prochaine session libre + liaison de mon id
   -> met Cerberus comme agent principal de la session (le LLM demarre comme Cerberus)
3. Lire la session RENDUE par l'outil et la noter
4. Utiliser CETTE session pour toutes les activations :
   python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py activer <session> <agent> <raison>
   python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py reactiver <session> <raison> <agent>
```

> **DEUX LLM DIFFERENTS NE PARTAGENT JAMAIS UNE SESSION** : la comparaison se fait sur l'ID.
> Si je n'ai pas d'id, je le DEMANDE a l'utilisateur avant toute action.

**Regle** : chaque session LLM active et desactive SON agent principal dans SON bloc. Les autres sessions ne sont jamais touchees.

### Le processus d'identification

```
1. L'utilisateur dit : "Bonjour [nom-agent]"
   Exemple : "Bonjour Buffy" ou "Bonjour Atlas"

2. L'agent lit demarrer.md (ce fichier)

3. demarrer.md dit : "Si tu es nomme, deviens cet agent"

4. L'agent verifie AGENTS.md :
   - Si le nom dans AGENTS.md correspond -> tu es deja actif
   - Si le nom ne correspond pas -> tu dois devenir cet agent

5. L'agent devient l'agent nomme pour la session
```

### Etape 0.1 -- Repondre a la salutation
```
1. Lire demarrer.md (ce fichier)
2. Identifier le nom de l'agent dans la salutation
3. Verifier AGENTS.md :
   a. Si l'agent nomme est deja actif -> confirmer et continuer
   b. Si un autre agent est actif -> devenir l'agent nomme
4. Aller a l'Etape 0.2
```

**Format de reponse :**
```
Bonjour [nom-agent] !
Je suis [nom-agent], [role].
Je prends le relais pour cette session.
```

### Etape 0.2 -- Verifier et creer la fiche

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
3. Si le dossier existe -> aller a l'Etape 0.3
```

### Etape 0.3 -- Lire sa configuration

```
1. Lire agents/[nom-agent]/corrections.md EN PREMIER
2. Lire agents/[nom-agent]/[nom-agent].md
3. Appliquer les surcharges et corrections
4. Noter les regles specifiques a respecter
```

> **REGLE FONDAMENTALE** : Activer SANS lire = inutile.
> **REGLE DE RELECTURE** : A CHAQUE activation ou reactivation (demarrage, relais, retour a Cerberus),
> l'agent relit SA fiche et SES corrections. Il ne lit jamais les fichiers des autres agents :
> chacun lit les siens en prenant le relais.

### Etape 0.4 -- Mettre a jour AGENTS.md

```
1. Mettre a jour la section "Agent Principal Actuel"
2. Ajouter/MAJ l'historique des agents
3. Confirmer que AGENTS.md reflete votre configuration
4. Signer : "[nom-agent] -- [date]"
```

### Etape 0.5 -- Appliquer les corrections

```
1. Pendant le travail, detecter les erreurs ou patterns problematiques
2. Ajouter la correction dans agents/[nom-agent]/corrections.md
3. La correction sera appliquee lors des prochaines sessions
```

---

## 1. Nouveau projet

> **Protocole IMMUABLE** : `cerveau-projet/regles-immuables/general/protocole-demarrer-projet/`

### Resume du protocole

| Etape | Action | Resultat |
|---|---|---|
| 0 | Identification agent | Agent pret |
| 1 | Definir le projet | Projet nomme |
| 2 | Creer le cerveau | Fichiers de base |
| 3 | Creer la structure | Dossiers organises |
| 4 | Creer les conventions | Regles de fonctionnement |
| 5 | Creer les regles immuables | Fondations solides |
| 6 | Creer les templates | Gabarits prets |
| 7 | Creer templates d'agent | Systeme d'agent |
| 8 | Verification finale | Tout valide |

### Lire le protocole complet

```
cerveau-projet/regles-immuables/general/protocole-demarrer-projet/
  ``-- protocole-demarrer-projet.001.01.ebauche.md
```

### Installer les regles immuables

> **Protocole IMMUABLE** : `cerveau-projet/regles-immuables/general/protocole-installer-regles/`

Ce protocole garantit que toutes les regles fondamentales sont presentes dans le projet.

```
cerveau-projet/regles-immuables/general/protocole-installer-regles/
  ``-- protocole-installer-regles.001.01.ebauche.md
```

---

## 2. Reprise (projet existant)

> **Protocole IMMUABLE** : `cerveau-projet/regles-immuables/general/protocole-reprendre-projet/`

### Cas de figure

| Cas | Description | Approche |
|---|---|---|
| **Fonctionnel** | Tout marche | Comprendre -> Ajouter |
| **Incomplet** | Contenu manquant | Comprendre -> Completer |
| **Casse** | Erreurs, bugs | Diagnostiquer -> Corriger |
| **A refondre** | Architecture mauvaise | Analyser -> Refondre |
| **Pause** | Reprise apres absence | Evaluer -> Continuer |

### Resume du protocole

| Etape | Action | Resultat |
|---|---|---|
| 0 | Identification agent | Agent pret |
| 1 | Evaluer l'etat | Etat documente |
| 2 | Classifier le projet | Cas identifie |
| 3 | Corriger fichiers critiques | Fichiers de base OK |
| 4 | Corriger la structure | Dossiers organises |
| 5 | Corriger les liens | References valides |
| 6 | Corriger le nommage | Convention respectee |
| 7 | Appliquer corrections | Problemes resolus |
| 8 | Verification finale | Tout valide |

### Lire le protocole complet

```
cerveau-projet/regles-immuables/general/protocole-reprendre-projet/
  ``-- protocole-reprendre-projet.001.01.ebauche.md
```

---

## 3. Regles immuables

Avant toute modification, consulter :
- `cerveau-projet/regles-immuables/general/regles-choisir-agent.md` -- **IMMUABLE** : choisir le bon agent
- `cerveau-projet/regles-immuables/general/regles-validation-rigoureuse.md` -- **IMMUABLE** : validation rigoureuse
- `cerveau-projet/regles-immuables/general/regles-emojis-ascii.md` -- **IMMUABLE** : bannissement des emojis, utilisation de ASCII
- `cerveau-projet/regles-immuables/general/regles-veracite.md` -- **IMMUABLE** : ne jamais mentir ou inventer
- `cerveau-projet/regles-immuables/general/protocole-gestion-defaillances.md` -- **IMMUABLE** : gestion automatique des defaillances
- `cerveau-projet/conventions/renommage/convention-renommage.md`
- `cerveau-projet/conventions/structures/convention-structures.md`
- `cerveau-projet/conventions/structures/convention-classeur-variables.md` -- classeur de variables
- `cerveau-projet/conventions/structures/convention-pipelines.md` -- pipelines de traitement
- `cerveau-projet/conventions/protocoles/convention-protocoles.md`
- `cerveau-projet/conventions/protocoles/distinction-conventions-protocoles.md` -- distinction conventions/protocoles
- `cerveau-projet/conventions/protocoles/convention-autoamelioration.md` -- auto-amelioration continue
- `cerveau-projet/conventions/liens/convention-liens.md`
- `cerveau-projet/regles-immuables/hierarchie/regles-hierarchie-par-niveau.md`
- `cerveau-projet/regles-immuables/general/rvav-workflow.md`

---

## 4. Changement d'agent
### Protocole de passage

1. **L'agent actuel** termine sa session et sauvegarde ses corrections
2. **L'agent actuel** lit `agents/cerberus/corrections.md` EN PREMIER
   -> Les regles de Cerberus s'appliquent des maintenant
3. **L'agent actuel** lit `agents/cerberus/cerberus.md`
   -> Connaitre le role et les limites de Cerberus
4. **L'agent actuel** met a jour `AGENTS.md` : Nom = Cerberus
5. **L'agent actuel** documente la fin de mission
6. **Cerberus** reprend le controle avec ses instructions

> **REGLE FONDAMENTALE** : Reactiver Cerberus SANS lire = inutile.

### Regles de passage

| Regle | Description |
|---|---|
| **Lire avant de reactiver** | Toujours lire corrections.md + fiche de Cerberus |
| **Pas de suppression** | Les corrections de l'agent precedent restent |
| **Pas de partage** | Chaque agent a ses propres corrections |
| **AGENTS.md dynamique** | Seul l'agent principal y ecrit |
| **Tracabilite** | L'historique des agents est conserve |

---

## 5. Auto-correction
### Quand corriger ?

| Signal | Action |
|---|---|
| Meme erreur 2+ fois | Ajouter dans `corrections.md` |
| Regle nouvelle | Ajouter dans "Regles specifiques" |
| Section a modifier | Ajouter dans "Surcharges" |
| Configuration specifique | Ajouter dans "Configuration specifique" |

### Comment corriger ?

1. Ouvrir `cerveau-projet/agents/[nom-agent]/corrections.md`
2. Ajouter la correction dans la section appropriee
3. La correction sera appliquee automatiquement lors des prochaines sessions

### Types de corrections

| Type | Section | Usage |
|---|---|---|
| **Regle** | Regles specifiques | Nouvelle regle pour cet agent |
| **Surcharge** | Surcharges | Modifier une section de la fiche |
| **Correction** | Corrections d'erreurs | Corriger un pattern errone |
| **Config** | Configuration specifique | Parametre de travail |

---

## 6. Carte de Decision
### Principe

```
SI [mission] ALORS [ligne] -> [etapes] -> [protocoles a lire]
```

### Pour chaque mission

1. Identifier la mission dans la carte de decision
2. Suivre les etapes dans l'ordre
3. Lire le protocole de CHAQUE etape
4. Ne PAS supposer -- VERIFIER

### Regle d'or
### Lire le protocole

```
cerveau-projet/regles-immuables/general/protocole-carte-decision/
  ``-- protocole-carte-decision.001.01.ebauche.md
```

---

## 7. Resume du workflow

```
1. Lire AGENTS.md en premier
2. S'identifier : python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py sidentifier <mon-id> -> l'outil me rend MA session (retrouvee ou nouvelle)
3. Se presenter automatiquement
4. Verifier si la fiche existe
5. Si non -> creer la fiche + corrections
6. Lit corrections.md en priorite
7. Lit sa fiche d'agent
8. Lit sa CARTE DE DECISION
9. Met a jour SON bloc dans AGENTS.md (avec sa session)
10. Effectue des recherches si necessaire
11. Travaille sur la tache en suivant la carte
12. Detecte erreurs -> ajoute dans corrections.md
13. Prochaine session -> lit les nouvelles corrections

A CHAQUE activation ou reactivation : relire sa fiche et ses corrections (jamais celles des autres).
Chaque session LLM utilise SON identifiant (session-llm-N) pour toutes ses activations.
```

---

## 7. Fichiers cles

| Fichier | Role |
|---|---|
| `AGENTS.md` | Agent principal actuel (dynamique) |
| `cerveau-projet/agents/index-agents.md` | Point d'entree des agents |
| `cerveau-projet/agents/fiche-agent-template.md` | Template pour creer une fiche |
| `cerveau-projet/agents/corrections-template.md` | Template pour les corrections |
| `cerveau-projet/agents/[nom-agent]/[nom-agent].md` | Fiche de l'agent |
| `cerveau-projet/agents/[nom-agent]/corrections.md` | Corrections de l'agent |
| `cerveau-projet/index-cerveau.md` | Point d'entree du cerveau |
| `cerveau-projet/classeur-variables/index-classeur.md` | Point d'entree du classeur de variables |
