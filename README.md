---
identite:
  type: index
  appartient_a: commun
  commun: true
---
# Cerveau-Projet

[![Plateforme](https://img.shields.io/badge/Plateforme-Windows-blue?style=flat)](https://img.shields.io/badge/Plateforme-Windows-blue?style=flat) [![Fait avec](https://img.shields.io/badge/Fait_avec-Bash-orange?style=flat)](https://img.shields.io/badge/Fait_avec-Bash-orange?style=flat) [![Statut](https://img.shields.io/badge/Statut-stable-brightgreen?style=flat)](https://img.shields.io/badge/Statut-stable-brightgreen?style=flat) [![Outils](https://img.shields.io/badge/Outils-133-blueviolet?style=flat)](https://img.shields.io/badge/Outils-133-blueviolet?style=flat) [![Langages](https://img.shields.io/badge/Langages-Bash,_Python,_Markdown-orange?style=flat)](https://img.shields.io/badge/Langages-Bash,_Python,_Markdown-orange?style=flat) [![Version](https://img.shields.io/badge/Version-v1.3.0-blue?style=flat)](https://img.shields.io/badge/Version-v1.3.0-blue?style=flat)


![Logo](cerveau-projet/assets/images/logo.jpg)


Un systeme de developpement guide par des agents IA qui evolue et s'auto-ameliore au fil des projets.

## Ce que c'est

Le cerveau-projet est une **structure de travail persistante** qui accompagne un projet
de developpement. Il organise le travail, impose des regles, fournit des outils, et est
anime par des agents IA ayant chacun un role specifique.

**Principe fondateur** : le cerveau evolue dans un projet et se copie dans le suivant,
de plus en plus performant (plus d'agents, plus d'outils, plus de rigueur).

---

## Ce qu'il fait

| Capacite | Description |
|---|---|
| **Organiser** | Structure les idees, specifications, conventions et regles |
| **Guider** | Les agents suivent une carte de decision par mission |
| **Controler** | Chaque travail est verifie avant d etre valide |
| **Outiller** | Des outils partages, crees et ameliores par le systeme lui-meme |
| **Apprendre** | Chaque agent note ses erreurs et ne les refait plus (voir Vocabulaire) |
| **Tester** | Des tests automatiques verifient que tout fonctionne, sans blocage |

---

## Les agents

Le cerveau-projet est anime par des agents IA, chacun avec un role et une carte de decision :

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

### Le cycle fondamental (par session)

```
CERBERUS -> AGENT -> CERBERUS
    1         2         3
```

1. Cerberus analyse la demande et confie la mission a l'agent adapte
2. L'agent realise sa mission en suivant sa feuille de route
3. A la fin, l'agent rend la main a Cerberus (ou passe au suivant de la chaine)

### Les garde-fous (qualite et protection)

Le cerveau-projet se protege par des tests automatiques :

- **Une suite de 46 tests** verifie que rien ne casse quand quelque chose change.
  Un seul agent, **Janus**, a le droit de la lancer : les autres agents testent
  uniquement leur propre travail.
- **Aucun fichier temporaire** n'est laisse a la racine du projet apres un travail.
- **Le gardien Cerberus** ne lance jamais de test lui-meme : il confie cette tache
  aux agents habilites.
- **Les feuilles de route** des agents sont controlees et validees en continu.

---

## Le classeur de variables

Le cerveau-projet conserve des **variables partagees** entre les agents et les sessions
(profil de session, etat courant). Elles vivent dans
`cerveau-projet/agents/classeur-variables/` : c'est la memoire commune du systeme.

| Caracteristique | Detail |
|---|---|
| **Persistant** | Les valeurs survivent d'une session a l'autre |
| **Partage** | Chaque agent lit et ecrit les memes variables |
| **Verifie** | La coherence des variables est controlee en continu |

## Les fondations du systeme

Au-dela du classeur, le cerveau-projet s'appuie sur des fondations partagees,
conservees dans `cerveau-projet/agents/` :

| Fondation | Role |
|---|---|
| **Conventions** | Les facons de faire communes : ecriture, liens, protocoles, structures |
| **Regles immuables** | Les regles inviolables : veracite, choix des agents, groupes |
| **Traces** | Le journal des usages d'outils, pour auditer et ameliorer en continu |

## Amelioration continue

Le cerveau-projet s'ameliore en continu, a plusieurs niveaux :

| Niveau | Comment |
|---|---|
| **Les agents** | Chaque agent note ses erreurs et ne les refait plus |
| **Les outils** | Rondes d'amelioration regulieres : robustesse, performance, securite |
| **Le systeme** | A chaque demande, Cerberus active l'agent habilite pour ameliorer |
| **Les tests** | Les tests verifient que rien ne casse quand quelque chose change |

> Toute demande d'amelioration passe par Cerberus : il active le bon agent, qui
> ameliore, et le README est mis a jour en consequence.

---

## Commencer

Le cerveau-projet se pilote par conversation : vous ecrivez une phrase, le
systeme repond et vous guide etape par etape.

1. **Ouvrez un terminal** dans le dossier du projet
2. **Lancez le guide de demarrage** (le fichier `demarrer.md` a la racine ne se
   lit pas : il se lance) :

   ```
   python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py \
     cerveau-projet/demarrage/parcours-demarrage.json
   ```

3. **Repondez aux questions du guide** : il vous demande un identifiant simple
   (par exemple `llm-1`) pour retrouver votre session au prochain lancement
4. **Saluez le gardien** : le systeme se presente. Ecrivez par exemple
   `Bonjour Cerberus` puis decrivez ce que vous voulez faire
5. **Suivez les instructions** : a chaque etape, le systeme vous indique la
   commande exacte a executer et vous pose les questions au bon moment
6. **En cas de doute** : la section [Vocabulaire](#vocabulaire) ci-dessous
   explique les termes du projet

> **Developpeurs** : la documentation technique complete (demarrer une session, activer un LLM, multi-session, outils, combos, cartes de decision, parcours, workflow RVAV, tests) est dans [cerveau-projet/readme-dev.md](cerveau-projet/readme-dev.md).

---

## Vocabulaire

| Terme | Definition |
|---|---|
| **Cerveau-projet** | Structure persistante qui organise et guide le dev |
| **Pense-bete** | Idee en cours de developpement |
| **Spec** | Definition technique et fonctionnelle |
| **Todo** | Liste des taches |
| **Carte de decision** | Lignes de decision par mission dans chaque fiche d'agent |
| **RVAV** | Rechercher - Verifier - Analyser - Valider |
| **Statut** | ebauche, prepare, dev, test, valide |
| **Corrections.md** | Memoire d'apprentissage de chaque agent |
| **Agent** | Assistant IA specialise, chacun avec un role precis |
| **Session** | Une conversation de travail avec le systeme |
| **Workflow** | Enchainement d'etapes pour accomplir une tache |
| **Parcours** | Feuille de route pas a pas suivie par un agent |
| **Outil** | Petit programme partage que les agents utilisent pour travailler |
| **Combo** | Enchainement d'outils pour realiser une tache complete |
| **Garde-fou** | Test ou regle qui protege le systeme contre les erreurs |
| **Classeur** | Espace de stockage partage des variables entre les agents |
| **Non-regression** | Verification que les changements ne cassent rien |
| **Test** | Verification automatique qu'un comportement attendu fonctionne |
