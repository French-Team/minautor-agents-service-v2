---
# Template -- README DEVELOPPEUR (readme-dev.md)
# Ce fichier est le MODELE de reference pour rediger le
# cerveau-projet/readme-dev.md (destine aux DEVELOPPEURS).
#
# ============================================================
# DOUBLE README -- repartition des publics
# ============================================================
# README.md (racine)      : GRAND PUBLIC (non-codeurs) -- ce que
#                           fait le cerveau-projet, sans structure
#                           ni detail technique.
# readme-dev.md (cerveau-projet/) : DEVELOPPEURS -- comment
#                           demarrer, activer un LLM, travailler
#                           avec les agents, les outils, les
#                           combos, les cartes de decision, les
#                           parcours, les indices, le workflow
#                           RVAV, les tests, l'auto-amelioration.
#
# REGLES DE REDACTION (immuables) :
#   1. SOURCES DE VERITE UNIQUEMENT : chaque affirmation du
#      readme-dev.md doit etre verifiable dans les sources
#      (AGENTS.md, demarrer.md, index-cerveau.md, parcours/*.json,
#      tools/, regles-immuables/, classeur-variables/). JAMAIS de
#      souvenir, d'hypothese ou d'invention.
#   2. ASCII strict : aucun accent, emoji ou caractere Unicode.
#      Guillemets ASCII uniquement ("..."), jamais de guillemets
#      francais.
#   3. LF pur : fins de ligne Unix (pas de CRLF).
#   4. Riche en TABLEAUX et schemas pour la lisibilite (le public
#      developpeur est technique).
#   5. Le readme-dev.md est ecrit par CLIO (muse de l'histoire),
#      jamais directement par un autre agent. Clio le remplit
#      depuis CE template, case par case, en suivant son parcours
#      (branche 'readme-dev').
# ============================================================

# <Cerveau-Projet - Documentation Developpeur>

> Documentation technique du cerveau-projet, destinee aux
> developpeurs qui travaillent AVEC le systeme d'agents IA.
> Pour une presentation grand public, voir le README.md a la
> racine du projet.

## 1. Vue d'ensemble

| Champ | Valeur |
|---|---|
| **Version** | <version-lue-dans-cerveau-projet/agents/clio/version-readme.txt> |
| **Statut** | <statut-lu-dans-cerveau-projet/agents/clio/statut-projet.txt> |
| **Plateforme** | Windows (bash + Python) |
| **Langages** | Bash, Python, Markdown |
| **Point d'entree** | demarrer.md |

## 2. Concept : le cerveau-projet

<Expliquer avec des tableaux/schemas : structure persistante qui
accompagne un projet, organise le travail, impose des regles,
fournit des outils, anime par des agents IA a roles distincts.
Le principe fondateur : le cerveau evolue dans un projet et se
copie dans le suivant, de plus en plus performant.>

## 3. Demarrer une session

### 3.1 Donner un identifiant au LLM

<Mode ID : chaque LLM possede SON identifiant (ex: llm-1) donne
par l'utilisateur. Commande exacte :

python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py sidentifier <mon-id>

Regle d'alignement : id llm-N -> session session-llm-N. Un id deja
lie = session retrouvee ; id inconnu = prochaine session libre +
liaison. L'outil met a jour AGENTS.md (## Sessions LLM).>

### 3.2 Activer un agent

<Activer un agent : il devient l'agent principal de la session.

python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py activer <session> <agent> <raison> <mission>

Regle fondamentale : activer SANS lire la fiche = inutile. Chaque
agent relit SA fiche et SES corrections avant d'agir.>

### 3.3 Reactiver Cerberus

<python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py reactiver <session> <raison> <agent-precedent>

La fin de mission suit LA CARTE de l'agent (Pattern 13) : activer
le suivant si maillon de chaine, seul le dernier maillon reactive
Cerberus.>

### 3.4 Lancer plusieurs LLM en parallele

<Multi-session : plusieurs LLM peuvent travailler sur le meme
projet. Chaque LLM s'identifie -> SA session (session-llm-N) ->
SON bloc dans AGENTS.md (## Sessions LLM) -> SON agent principal.
Le cycle se deroule DANS la session : activer puis reactiver. Les
sessions sont independantes et visibles entre elles via la table
## Sessions connues.>

## 4. Les agents et leurs roles

<Tableau : agent | role | quand l'activer. Sources : AGENTS.md
(liste des agents) + chaque fiche [agent].md.>

| Agent | Role | Quand l'activer |
|---|---|---|
| <agent> | <role> | <quand> |

## 5. La carte de decision et les parcours

### 5.1 Carte de decision

<Chaque agent suit SA carte de decision : SI [mission] ALORS
[ligne de decision] -> [etapes] -> [protocoles] -> [outils].
Source : regles-immuables/general/regles-choisir-agent.md.>

### 5.2 Parcours (jeu de piste)

<Le parcours est la SOURCE DE VERITE du guidage : fichier JSON
(parcours/parcours-<agent>.json) avec des cases (question, action,
controle, fin) reliees par des branches. Chaque case porte les
indices exacts (outil, fichier, regle). Outil de guidage :

python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py <parcours-json>

Structure d'une case : cid, titre, type, question/branches
(question), suivant (action), indices (outil/fichier/regle/ref).>

### 5.3 Les indices

<Chaque case du parcours donne les indices a appliquer :
- type 'outil' : nom + chemin + commande exacte (outil du cerveau)
- type 'fichier' : chemin + raison (a lire)
- type 'regle' : texte de la regle a appliquer
- type 'ref' : reference a un pattern ou un document>

## 6. Les outils du cerveau

<Boite a outils partagee par action (chaque dossier = ce que fait
l'outil). Source de verite : agents/tools/index-tools.md. Chaque
outil existe en .py et .sh (choix via profil systeme). Tableau :
categorie | outils | usage. Principes : les agents utilisent
UNIQUEMENT leurs outils (regle absolue 4), jamais de commandes
systeme directes.>

## 7. Les combos

<Enchainements d'outils en sequences (Pattern 3). Source :
agents/tools/combos/. Chaque combo a une definition JSON
(definition-combo.json) executee par combos-moteur, ou un
orchestrateur .py/.sh. Exemples : combo-maj-readme (petite MAJ),
combos-maj-readme-massive (grosse MAJ), combos-analyse-projet
(etat reel du projet).>

## 8. Le workflow RVAV (obligatoire)

<Tout fichier passe par 5 statuts : ebauche -> prepare -> dev ->
test -> valide. Chaque transition exige la boucle RVAV :
[R]echercher, [V]erifier, [A]nalyser, [V]alider, [P]urifier.
Source : regles-immuables/general/rvav-workflow.md.>

## 9. Les tests et protections

<Suite de non-regression (tests test-XXX). Seul JANUS lance la
non-regression complete (regle test-037) ; les autres agents
executent des tests individuels. Les tests importent les
protections (tester-protections) : anti-boucle, anti-blocage,
anti-erreurs-silencieuses, chrono par etape, bilan. Source :
agents/tools/tester/.>

## 10. L'auto-amelioration

<Le systeme s'auto-ameliore en continu :
- Chaque agent corrige ses erreurs dans corrections.md (memoire
  persistante, cycle d'apprentissage SESSION 1 -> SESSION 2).
- Les rondes de qualite des outils (robustesse, performance,
  securite, combos, generateurs, registre d usages).
- La demande d'amelioration passe par Cerberus (branche
  ameliorer -> generateurs-amelioration) puis l'agent habilite.
  Source : AGENTS.md + regles-immuables.>

## 11. Sources de verite

| Source | Role |
|---|---|
| AGENTS.md | Sessions LLM, agents actifs, historique |
| AGENTS-historique.md | Historique des interventions |
| demarrer.md | Point de demarrage |
| agents/index-agents.md | Index des agents |
| agents/tools/index-tools.md | Index des outils |
| agents/regles-immuables/ | Regles, protocoles, RVAV |
| agents/classeur-variables/ | Variables partagees |
| agents/<agent>/parcours/ | Cartes de decision (JSON) |

---

# Historique DU TEMPLATE (commentaire -- pas une section du
# readme-dev final) :
#   2026-08-14 | Creation : modele de reference du readme-dev.md
#               (scission public/dev decidee par l'utilisateur)
