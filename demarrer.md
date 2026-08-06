# Démarrage — comment utiliser ce cerveau
---

## 0. Identification de l'agent (OBLIGATOIRE)
### Le processus d'identification

```
1. L'utilisateur dit : "Bonjour [nom-agent]"
   Exemple : "Bonjour Buffy" ou "Bonjour Atlas"

2. L'agent lit demarrer.md (ce fichier)

3. demarrer.md dit : "Si tu es nommé, deviens cet agent"

4. L'agent vérifie AGENTS.md :
   - Si le nom dans AGENTS.md correspond -> tu es déjà actif
   - Si le nom ne correspond pas -> tu dois devenir cet agent

5. L'agent devient l'agent nommé pour la session
```

### Étape 0.1 — Répondre à la salutation
```
1. Lire demarrer.md (ce fichier)
2. Identifier le nom de l'agent dans la salutation
3. Vérifier AGENTS.md :
   a. Si l'agent nommé est déjà actif -> confirmer et continuer
   b. Si un autre agent est actif -> devenir l'agent nommé
4. Aller à l'Étape 0.2
```

**Format de réponse :**
```
Bonjour [nom-agent] !
Je suis [nom-agent], [rôle].
Je prends le relais pour cette session.
```

### Étape 0.2 — Vérifier et créer la fiche

```
1. Vérifier si une fiche existe pour cet agent :
   - Aller dans agents/
   - Chercher le dossier agents/[nom-agent]/
2. Si le dossier n'existe pas -> le créer :
   a. Créer le dossier agents/[nom-agent]/
   b. Copier agents/fiche-agent-template.md -> agents/[nom-agent]/[nom-agent].md
   c. Copier agents/corrections-template.md -> agents/[nom-agent]/corrections.md
   d. Remplir la fiche avec les informations de l'agent
   e. Laisser les corrections vides
3. Si le dossier existe -> aller à l'Étape 0.3
```

### Étape 0.3 — Lire sa configuration

```
1. Lire agents/[nom-agent]/corrections.md EN PREMIER
2. Lire agents/[nom-agent]/[nom-agent].md
3. Appliquer les surcharges et corrections
4. Noter les règles spécifiques à respecter
```

> **RÈGLE FONDAMENTALE** : Activer SANS lire = inutile.

### Étape 0.4 — Mettre à jour AGENTS.md

```
1. Mettre à jour la section "Agent Principal Actuel"
2. Ajouter/MAJ l'historique des agents
3. Confirmer que AGENTS.md reflète votre configuration
4. Signer : "[nom-agent] -- [date]"
```

### Étape 0.5 — Appliquer les corrections

```
1. Pendant le travail, détecter les erreurs ou patterns problématiques
2. Ajouter la correction dans agents/[nom-agent]/corrections.md
3. La correction sera appliquée lors des prochaines sessions
```

---

## 1. Nouveau projet

> **Protocole IMMUABLE** : `cerveau-projet/regles-immuables/general/protocole-demarrer-projet/`

### Résumé du protocole

| Étape | Action | Résultat |
|---|---|---|
| 0 | Identification agent | Agent prêt |
| 1 | Définir le projet | Projet nommé |
| 2 | Créer le cerveau | Fichiers de base |
| 3 | Créer la structure | Dossiers organisés |
| 4 | Créer les conventions | Règles de fonctionnement |
| 5 | Créer les règles immuables | Fondations solides |
| 6 | Créer les templates | Gabarits prêts |
| 7 | Créer templates d'agent | Système d'agent |
| 8 | Vérification finale | Tout validé |

### Lire le protocole complet

```
cerveau-projet/regles-immuables/general/protocole-demarrer-projet/
  ``-- protocole-demarrer-projet.001.01.ebauche.md
```

### Installer les règles immuables

> **Protocole IMMUABLE** : `cerveau-projet/regles-immuables/general/protocole-installer-regles/`

Ce protocole garantit que toutes les règles fondamentales sont présentes dans le projet.

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
| **Incomplet** | Contenu manquant | Comprendre -> Compléter |
| **Cassé** | Erreurs, bugs | Diagnostiquer -> Corriger |
| **À refondre** | Architecture mauvaise | Analyser -> Refondre |
| **Pause** | Reprise après absence | Évaluer -> Continuer |

### Résumé du protocole

| Étape | Action | Résultat |
|---|---|---|
| 0 | Identification agent | Agent prêt |
| 1 | Évaluer l'état | État documenté |
| 2 | Classifier le projet | Cas identifié |
| 3 | Corriger fichiers critiques | Fichiers de base OK |
| 4 | Corriger la structure | Dossiers organisés |
| 5 | Corriger les liens | Références valides |
| 6 | Corriger le nommage | Convention respectée |
| 7 | Appliquer corrections | Problèmes résolus |
| 8 | Vérification finale | Tout validé |

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
- `cerveau-projet/regles-immuables/general/protocole-gestion-defaillances.md` -- **IMMUABLE** : gestion automatique des défaillances
- `cerveau-projet/conventions/renommage/convention-renommage.md`
- `cerveau-projet/conventions/structures/convention-structures.md`
- `cerveau-projet/conventions/structures/convention-classeur-variables.md` -- classeur de variables
- `cerveau-projet/conventions/structures/convention-pipelines.md` -- pipelines de traitement
- `cerveau-projet/conventions/protocoles/convention-protocoles.md`
- `cerveau-projet/conventions/protocoles/distinction-conventions-protocoles.md` -- distinction conventions/protocoles
- `cerveau-projet/conventions/protocoles/convention-autoamelioration.md` -- auto-amélioration continue
- `cerveau-projet/conventions/liens/convention-liens.md`
- `cerveau-projet/regles-immuables/hierarchie/regles-hierarchie-par-niveau.md`
- `cerveau-projet/regles-immuables/general/rvav-workflow.md`

---

## 4. Changement d'agent
### Protocole de passage

1. **L'agent actuel** termine sa session et sauvegarde ses corrections
2. **L'agent actuel** lit `agents/cerberus/corrections.md` EN PREMIER
   -> Les règles de Cerberus s'appliquent dès maintenant
3. **L'agent actuel** lit `agents/cerberus/cerberus.md`
   -> Connaître le rôle et les limites de Cerberus
4. **L'agent actuel** met à jour `AGENTS.md` : Nom = Cerberus
5. **L'agent actuel** documente la fin de mission
6. **Cerberus** reprend le contrôle avec ses instructions

> **RÈGLE FONDAMENTALE** : Réactiver Cerberus SANS lire = inutile.

### Règles de passage

| Règle | Description |
|---|---|
| **Lire avant de réactiver** | Toujours lire corrections.md + fiche de Cerberus |
| **Pas de suppression** | Les corrections de l'agent précédent restent |
| **Pas de partage** | Chaque agent a ses propres corrections |
| **AGENTS.md dynamique** | Seul l'agent principal y écrit |
| **Traçabilité** | L'historique des agents est conservé |

---

## 5. Auto-correction
### Quand corriger ?

| Signal | Action |
|---|---|
| Même erreur 2+ fois | Ajouter dans `corrections.md` |
| Règle nouvelle | Ajouter dans "Règles spécifiques" |
| Section à modifier | Ajouter dans "Surcharges" |
| Configuration spécifique | Ajouter dans "Configuration spécifique" |

### Comment corriger ?

1. Ouvrir `cerveau-projet/agents/[nom-agent]/corrections.md`
2. Ajouter la correction dans la section appropriée
3. La correction sera appliquée automatiquement lors des prochaines sessions

### Types de corrections

| Type | Section | Usage |
|---|---|---|
| **Règle** | Règles spécifiques | Nouvelle règle pour cet agent |
| **Surcharge** | Surcharges | Modifier une section de la fiche |
| **Correction** | Corrections d'erreurs | Corriger un pattern erroné |
| **Config** | Configuration spécifique | Paramètre de travail |

---

## 6. Carte de Décision
### Principe

```
SI [mission] ALORS [ligne] -> [étapes] -> [protocoles à lire]
```

### Pour chaque mission

1. Identifier la mission dans la carte de décision
2. Suivre les étapes dans l'ordre
3. Lire le protocole de CHAQUE étape
4. Ne PAS supposer — VÉRIFIER

### Règle d'or
### Lire le protocole

```
cerveau-projet/regles-immuables/general/protocole-carte-decision/
  ``-- protocole-carte-decision.001.01.ebauche.md
```

---

## 7. Résumé du workflow

```
1. Lire AGENTS.md en premier
2. Se présenter automatiquement
3. Vérifier si la fiche existe
4. Si non -> créer la fiche + corrections
5. Lit corrections.md en priorité
6. Lit sa fiche d'agent
7. Lit sa CARTE DE DÉCISION
8. Met à jour AGENTS.md
9. Effectue des recherches si nécessaire
10. Travaille sur la tâche en suivant la carte
11. Détecte erreurs -> ajoute dans corrections.md
12. Prochaine session -> lit les nouvelles corrections
```

---

## 7. Fichiers clés

| Fichier | Rôle |
|---|---|
| `AGENTS.md` | Agent principal actuel (dynamique) |
| `cerveau-projet/agents/index-agents.md` | Point d'entrée des agents |
| `cerveau-projet/agents/fiche-agent-template.md` | Template pour créer une fiche |
| `cerveau-projet/agents/corrections-template.md` | Template pour les corrections |
| `cerveau-projet/agents/[nom-agent]/[nom-agent].md` | Fiche de l'agent |
| `cerveau-projet/agents/[nom-agent]/corrections.md` | Corrections de l'agent |
| `cerveau-projet/index-cerveau.md` | Point d'entrée du cerveau |
| `cerveau-projet/classeur-variables/index-classeur.md` | Point d'entrée du classeur de variables |
