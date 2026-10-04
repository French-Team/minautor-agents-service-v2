---
identite:
  type: regle-immuable
  appartient_a: commun
  commun: true
---
# Protocole de formation continue des agents

**Version** : 0.1.0
**Statut** : actif
**Date creation** : 2026-08-17
**Agent** : Buffy (creation)

---

## 1. Objectif

Ce protocole definit le processus de **formation continue** des agents du
cerveau-projet. Un agent est "intelligent" quand il :
- Utilise les bons outils au bon moment (carte, regles, conventions)
- N'entre pas en contradiction avec ses propres regles
- S'adapte quand les outils qu'il utilise evoluent
- Documente ses lecons pour ne pas recommencer les memes erreurs

**Chiron** est l'agent habilite a executer ce protocole. Son role :
analyser les fiches, corrections, cartes, regles et conventions des agents
pour y detecter les incoherences nuisant a leur "intelligence operationnelle".

---

## 2. Quand intervenir (declencheurs)

Chiron intervient dans les cas suivants :

| Declencheur | Action | Priorite |
|---|---|---|
| Mise a jour d'un outil (bumper) | Verifier que les agents qui l'utilisent ont ete re-eduques | HAUTE |
| Creation/modification d'un protocole/regle | Verifier la coherence avec les fiches concernees | HAUTE |
| Nouvel agent cree | Verifier la conformite de sa fiche et la coherence de son parcours | MOYENNE |
| Agent declare un KO repete | Analyser ses corrections et fiches pour trouver la cause racine | HAUTE |
| Mission d'amelioration (generateurs-amelioration) | Audit de coherence apres modification | MOYENNE |
| Audit de Themis signale un ecart | Chiron applique les corrections de formation | BASSE |

---

## 3. Comment intervenir (processus)

### 3.1. Diagnostic

1. **Lire les corrections de l'agent cible** : que sait-il vraiment ? Quelles
   lecons a-t-il documentees ? Y a-t-il des lecons inachevees ou contradictoires ?
2. **Lire la fiche de l'agent** : est-elle conforme au template ? Les outils
   references existent-ils toujours ? Les versions sont-elles a jour ?
3. **Verifier le parcours/carte** : les cases pointent-elles vers des outils
   reellement associes ? Les indices outil sont-ils corrects ?
4. **Verifier les regles et conventions** : y a-t-il des regles qui
   contredisent le comportement reel de l'agent ?
5. **Verifier les mises a jour d'outils** : les outils utilises par l'agent
   ont-ils ete modifies sans que l'agent ait ete re-eduque ?

### 3.2. Detection des incoherences

Types d'incoherences recherches :

| Type | Exemple | Impact |
|---|---|---|
| Fiche non conforme | Section manquante par rapport au template | L'agent ne lit pas les regles manquantes |
| Version outil depassee | Outil bumpe a 0.5.9, fiche dit encore 0.5.8 | L'agent croit utiliser l'ancienne version |
| Regle contredite | La fiche dit "toujours X" mais la carte fait "jamais X" | L'agent ne sait plus quoi faire, sort du flux |
| Outillage manquant dans la carte | Un outil reference dans la fiche n'est pas dans la carte | L'agent ne sait pas comment acceder a l'outil |
| Lecon non documentee | L'agent a fait une erreur mais ne l'a pas documentee | Meme erreur reproduite |
| Protocole absent | Un protocole concerne l'agent mais n'est pas reference dans sa fiche | L'agent ignore le protocole |

### 3.3. Action

1. **Pour chaque incoherence detectee** : documenter dans le rapport de Chiron
   (type, agent, source, impact, correction proposee)
2. **Appliquer les corrections simples** (version, reference, texte) via
   editer-fichier-agents
3. **Signaler les corrections complexes** a Buffy (modification de carte,
   modification de parcours)
4. **Verifier** : valider-conformite-fiche, detecter-cablages, valider-cartes

### 3.4. Documentation

1. **Lecon Chiron** dans corrections.md de Chiron : qu'a-t-il detecte et corrige ?
2. **Lecon dans les corrections de l'agent cible** : l'agent cible doit etre
   notifie de la correction de formation
3. **Notification a Cerberus** : bilan de la mission d'education

---

## 4. Regles de Chiron

> **REGLE ABSOLUE** : Chiron ne modifie JAMAIS les fiches des agents sans
> passer par editer-fichier-agents (outil du cerveau, jamais de script temporaire
> pour les fichiers agents).

> **REGLE ABSOLUE** : Chiron ne modifie JAMAIS les parcours/cartes des agents.
> Il signale les incoherences de carte a Buffy qui les corrige via
> editer-parcours.

> **REGLE ABSOLUE** : Chiron ne declare JAMAIS d'outils hors de sa carte. Il
> utilise les outils P0 (lire-fichier) et les outils assigns dans son parcours.

---

## 5. Connexions

- **Themis** : Themis audite ; Chiron corrige. Si Themis signale un ecart,
  Chiron peut etre active pour l'appliquer.
- **Buffy** : Buffy corrige les fichiers agents. Chiron signale les
  incoherences, Buffy les applique.
- **Janus** : Janus valide. Apres une mission Chiron, Janus verifie que la
  non-regression est toujours verte.
- **Vulcain** : Vulcain cree les outils. Quand Vulcain met a jour un outil,
  Chiron est active pour re-eduer les agents qui l'utilisent.
