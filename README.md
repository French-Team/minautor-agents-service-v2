---
identite:
  type: index
  appartient_a: commun
  commun: true
---
# Cerveau-Projet

[![Plateforme](https://img.shields.io/badge/Plateforme-Windows-blue?style=flat)](https://img.shields.io/badge/Plateforme-Windows-blue?style=flat) [![Fait avec](https://img.shields.io/badge/Fait_avec-Bash-orange?style=flat)](https://img.shields.io/badge/Fait_avec-Bash-orange?style=flat) [![Statut](https://img.shields.io/badge/Statut-stable-brightgreen?style=flat)](https://img.shields.io/badge/Statut-stable-brightgreen?style=flat) [![Agents](https://img.shields.io/badge/Agents-19-blue?style=flat)](https://img.shields.io/badge/Agents-19-blue?style=flat) [![Outils](https://img.shields.io/badge/Outils-165-blueviolet?style=flat)](https://img.shields.io/badge/Outils-165-blueviolet?style=flat) [![Tests](https://img.shields.io/badge/Tests-97-red?style=flat)](https://img.shields.io/badge/Tests-97-red?style=flat) [![Protocoles](https://img.shields.io/badge/Protocoles-36-orange?style=flat)](https://img.shields.io/badge/Protocoles-36-orange?style=flat) [![Regles](https://img.shields.io/badge/Regles-75-yellow?style=flat)](https://img.shields.io/badge/Regles-75-yellow?style=flat) [![Version](https://img.shields.io/badge/Version-v1.6.0-blue?style=flat)](https://img.shields.io/badge/Version-v1.6.0-blue?style=flat)


![Logo](cerveau-projet/assets/images/logo.jpg)


Je suis un **systeme agentique** qui peut vous aider a developper votre projet.
Je suis compose de **19 agents** qui s'auto-ameliorent en continu, capables de
detecter les erreurs que les autres agents vont faire, les erreurs dans leurs
fichiers, leurs regles, leurs protocoles, leurs conventions, et bien plus encore.

---

## Qui suis-je ?

Je suis une **structure de travail persistante** qui accompagne votre projet
de developpement. J'organise le travail, j'impose des regles, je fournis
des outils, et je suis anime par des agents IA ayant chacun un role specifique.

**Mon principe fondateur** : je evolue dans votre projet et je me copie dans
le suivant, de plus en plus performant (plus d'agents, plus d'outils, plus de
rigueur).

---

## Ce que je fais

| Capacite | Description |
|---|---|
| **Organiser** | Je structure vos idees, specifications, conventions et regles |
| **Guider** | Mes agents suivent une carte de decision par mission |
| **Controler** | Chaque travail est verifie avant d'etre valide |
| **Outiller** | Des outils partages, crees et ameliores par le systeme lui-meme |
| **Apprendre** | Chaque agent note ses erreurs et ne les refait plus |
| **Tester** | 97 tests automatiques verifient que tout fonctionne |

---

## Mes agents

Je suis anime par **19 agents IA**, chacun avec un role et une carte de decision :

| Agent | Role |
|---|---|
| **Cerberus** | Gardien de l'entree, coordonne les sessions |
| **Buffy** | Developpeur principal du cerveau |
| **Atlas** | Explorateur et documentaliste |
| **Janus** | Second controle - SEUL a lancer la non-regression complete |
| **Vulcain** | Constructeur d'outils reels |
| **Morpheus** | Testeur dedie (tests individuels uniquement) |
| **Athena** | Redactrice de pense-betes |
| **Promethee** | Redacteur de specs |
| **Minerve** | Redactrice de todos |
| **Clio** | Muse de l'histoire - README (public + dev) |
| **Themis** | Evaluatrice croisee - maillon automatique de la chaine |
| **Hygie** | Agent de nettoyage du workspace |
| **Hermes** | Agent de la langue - orthographe, vocabulaire et fautes de francais |
| **Gardien** | Gardien du marbre - securite du code (zones protegees, l'utilisateur valide) |
| **Argus** | Detecteur de contradictions -- cases, regles, protocoles et historique git |
| **Chiron** | Educateur des agents -- formation continue |
| **Socrate** | Conversateur de revision strategique |
| **Redacteur-v2** | Redacteur PRO des docs de la v2 (freelance) |
| **Hades** | Gardien des archives git - SEUL habilite aux commandes git |

### Mon cycle fondamental (par session)

```
CERBERUS -> AGENT -> CERBERUS
    1         2         3
```

1. Cerberus analyse la demande et confie la mission a l'agent adapte
2. L'agent realise sa mission en suivant sa carte de decision (parcours)
3. A la fin, l'agent rend la main a Cerberus (ou passe au suivant de la chaine)
4. En cas d'erreur hors-perimetre, l'agent active l'agent habilite en **inter-round** sans interrompre le round : l'habilite repare, puis reactive l'appelant qui reprend sa mission

### Mes garde-fous (qualite et protection)

Je me protege par des tests automatiques :

- **97 tests** verifient que rien ne casse quand quelque chose change.
  Un seul agent, **Janus**, a le droit de lancer la non-regression complete :
  les autres agents testent uniquement leur propre travail.
- **Aucun fichier temporaire** n'est laisse a la racine du projet apres un travail :
  chaque script temporaire passe par un **controle automatique** (format, qualite)
  avant d'etre execute, puis est supprime en fin de mission.
- **Le gardien Cerberus** ne lance jamais de test lui-meme : il confie cette tache
  aux agents habilites.
- **Les feuilles de route** des agents sont controlees et validees en continu.

---

## Mon classeur de variables

Je conserve des **variables partagees** entre mes agents et mes sessions
(profil de session, etat courant). Elles vivent dans
`cerveau-projet/agents/classeur-variables/` : c'est ma memoire commune.

| Caracteristique | Detail |
|---|---|
| **Persistant** | Les valeurs survivent d'une session a l'autre |
| **Partage** | Chaque agent lit et ecrit les memes variables |
| **Verifie** | La coherence des variables est controlee en continu |

## Mes fondations

Au-dela du classeur, je m'appuie sur des fondations partagees,
conservees dans `cerveau-projet/agents/` :

| Fondation | Role |
|---|---|
| **36 Protocoles** | Les facons de faire communes : ecriture, liens, structures |
| **75 Regles immuables** | Les regles inviolables : veracite, choix des agents, groupes |
| **Traces** | Le journal des usages d'outils, pour auditer et ameliorer en continu |

## Mon amelioration continue

Je m'ameliore en continu, a plusieurs niveaux :

| Niveau | Comment |
|---|---|
| **Les agents** | Chaque agent note ses erreurs et ne les refait plus |
| **Les outils** | Rondes d'amelioration regulieres : robustesse, performance, securite |
| **Le systeme** | A chaque demande, Cerberus active l'agent habilite pour ameliorer |
| **Les tests** | 97 tests verifient que rien ne casse quand quelque chose change |

> Toute demande d'amelioration passe par Cerberus : il active le bon agent, qui
> ameliore, et je suis mis a jour en consequence.

---

## Commencer

Je me pilote par conversation : vous ecrivez une phrase, je reponds et vous
guide etape par etape.

1. **Ouvrez un terminal** dans le dossier du projet
2. **Lancez le guide de demarrage** (le fichier `demarrer.md` a la racine ne se
   lit pas : il se lance) :

   ```
   python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \
     cerveau-projet/demarrage/parcours-demarrage.json
   ```

3. **Repondez aux questions du guide** : il vous demande un identifiant simple
   (par exemple `llm-1`) pour retrouver votre session au prochain lancement
4. **Saluez le gardien** : je me presente. Ecrivez par exemple
   `Bonjour Cerberus` puis decrivez ce que vous voulez faire
5. **Suivez les instructions** : a chaque etape, je vous indique la
   commande exacte a executer et je vous pose les questions au bon moment
6. **En cas de doute** : la section [Vocabulaire](#vocabulaire) ci-dessous
   explique les termes du projet

> **Developpeurs** : la documentation technique complete (demarrer une session, activer un LLM, multi-session, outils, combos, cartes de decision, parcours, workflow RVAV, tests) est dans [cerveau-projet/readme-dev.md](cerveau-projet/readme-dev.md).

---

## Vocabulaire

| Terme | Definition |
|---|---|
| **Agent** | Assistant IA specialise, chacun avec un role precis |
| **Audit** | Verification croisee du travail d'un autre agent |
| **Bumper** | Outil qui met a jour les versions dans les fichiers |
| **Carte de decision** | Lignes de decision par mission dans chaque fiche d'agent |
| **Cerveau-projet** | Structure persistante qui organise et guide le dev |
| **Chrono** | Mesure du temps dexecution des tests et outils |
| **Combo** | Enchainement d'outils pour realiser une tache complete |
| **Convention** | Facons de faire communes : ecriture, liens, structures |
| **Corrections.md** | Memoire d'apprentissage de chaque agent |
| **Garde-fou** | Test ou regle qui protege le systeme contre les erreurs |
| **Idee** | Demande de l'utilisateur, point de depart d'une mission |
| **Non-regression** | Verification que les changements ne cassent rien |
| **Outil** | Petit programme partage que les agents utilisent pour travailler |
| **Parcours** | Feuille de route pas a pas suivie par un agent |
| **Pense-bete** | Idee en cours de developpement |
| **Performance** | Optimisation de la vitesse et des ressources |
| **Philosophie** | Principes de comportement d'un agent |
| **Protection** | Mecanisme de securite contre les erreurs (anti-boucles, anti-blocage) |
| **Protocole** | Regle technique detaillee (comment faire quelque chose) |
| **Recherche** | Demande d'exploration ou de decouverte |
| **Regle immuable** | Regle inviolable du systeme (veracite, choix des agents) |
| **Registre** | Journal des usages d'outils pour auditer et ameliorer |
| **Reflexion reduite** | Analyse avant action : comprendre avant de faire |
| **Rapport** | Document de retour d'un agent apres sa mission |
| **RVAV** | Rechercher - Verifier - Analyser - Valider |
| **Session** | Une conversation de travail avec le systeme |
| **Spec** | Definition technique et fonctionnelle |
| **Statut** | ebauche, prepare, dev, test, valide |
| **Systeme** | L'ensemble du cerveau-projet et ses composants |
| **Template** | Modele de fichier a reproduire |
| **Temporaire** | Script ou fichier cree pour une mission, supprime apres |
| **Todo** | Liste des taches |
| **Verrou** | Mecanisme d'exclusion mutuelle pour la securite des fichiers |
| **Workflow** | Enchainement d'etapes pour accomplir une tache |
| **Inter-round** | Mecanisme de reparation : un agent detecte un KO et active l'agent habilite sans interrompre le round |

| **Socrate** | Le philosophe qui questionne -- discute des revisions avec l'utilisateur et produit une liste de missions pour Cerberus | Selon sa carte de decision |
| **Redacteur-v2** | Le redacteur PRO des docs de la v2 (freelance) -- mode conversation | Sur activation (reste actif en conversation, reactive Cerberus sur "fin de cycle") |
