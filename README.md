---
identite:
  type: index
  appartient_a: commun
  commun: true
---
# Cerveau-Projet

[![Plateforme](https://img.shields.io/badge/Plateforme-Windows-blue?style=flat)](https://img.shields.io/badge/Plateforme-Windows-blue?style=flat) [![Fait avec](https://img.shields.io/badge/Fait_avec-Bash-orange?style=flat)](https://img.shields.io/badge/Fait_avec-Bash-orange?style=flat) [![Statut](https://img.shields.io/badge/Statut-stable-brightgreen?style=flat)](https://img.shields.io/badge/Statut-stable-brightgreen?style=flat) [![Outils](https://img.shields.io/badge/Outils-119-blueviolet?style=flat)](https://img.shields.io/badge/Outils-119-blueviolet?style=flat) [![Langages](https://img.shields.io/badge/Langages-Bash,_Python,_Markdown-orange?style=flat)](https://img.shields.io/badge/Langages-Bash,_Python,_Markdown-orange?style=flat) [![Version](https://img.shields.io/badge/Version-v0.2.0-blue?style=flat)](https://img.shields.io/badge/Version-v0.2.0-blue?style=flat)


![Logo](cerveau-projet/assets/images/logo.jpg)


Un systeme de developpement guide par des agents IA qui evolue et s'auto-ameliore au fil des projets.

## Ce que c'est

Le cerveau-projet est une **structure de travail persistante** qui accompagne un projet de developpement. Il organise le travail, impose des regles, fournit des outils, et est anime par des agents IA ayant chacun un role specifique.

**Principe fondateur** : Le cerveau evolue dans un projet et se copie dans le suivant, de plus en plus performant (plus d'agents, plus d'outils, plus de rigueur).

---

## Ce qu'il fait

| Capacite | Description |
|---|---|
| **Organiser** | Structure les idees, specifications, conventions et regles |
| **Guider** | Les agents suivent une carte de decision par mission |
| **Controler** | Chaque travail passe par le workflow RVAV avant validation |
| **Outiller** | Boite a outils partagee (bash + python) creee pour les agents, par les agents |
| **Apprendre** | Chaque agent corrige ses erreurs dans `corrections.md` |
| **Tester** | Tests encadres par des protections (anti-boucle, anti-blocage) |

---

## Structure

```
projet/
|-- demarrer.md                  # Point de demarrage (a lire en premier)
|-- AGENTS.md                    # Sessions LLM -- un bloc et un agent principal par session
|-- README.md                    # Ce fichier
`-- cerveau-projet/
    |-- index-cerveau.md         # Point d'entree du cerveau
    |-- agents/                  # Systeme d'agents + outils partages
    |   |-- index-agents.md
    |   |-- [agent]/[agent].md   # Fiche de chaque agent
    |   |-- [agent]/corrections.md  # Corrections et lecons de l'agent
    |   |-- conventions/         # Renommage, structures, liens, protocoles
    |   |-- regles-immuables/    # Regles non negociables + protocoles + RVAV
    |   |-- classeur-variables/  # Stockage partage de variables
    |   `-- tools/               # Boite a outils (119 outils + protections)
    |-- pense-betes/             # Idees, specs, todos, travail en cours
    |   |-- index-pense-bete.md
    |   |-- specs/               # Definitions techniques
    |   `-- pense-betes/         # Travail en cours (statuts ebauche->valide)
    |-- recherches-web/          # Historique des recherches effectuees
    `-- exemples/                # Tests et exemples d'utilisation
```

---

## Les agents

| Agent | Role | Quand l'activer |
|---|---|---|
| **Cerberus** | Gardien de l'entree, coordonne les sessions | Toujours (debut et fin) |
| **Buffy** | Developpeur principal du cerveau | Creation, modification de contenu |
| **Atlas** | Explorateur et documentaliste | Recherche, decouverte, analyse |
| **Janus** | Second controle (statuts, outils, modifications) | Par Cerberus, si la mission est dans la liste definie |
| **Vulcain** | Constructeur d'outils reels | Transformer un outil.md en outil |
| **Morpheus** | Testeur dedie (avec protections) | Ecrire et executer des tests |
| **Athena** | Redactrice de pense-betes | Demande de pense-bete |
| **Promethee** | Redacteur de specs | Pense-bete termine -> spec |
| **Minerve** | Redactrice de todos | Spec terminee -> todo |
| **Clio** | Muse de l'histoire - README | Apres chaque mission (fichiers changes) |
| **Themis** | Evaluatrice croisee du cerveau-projet | Audit, evaluation, coherence |

| **Classeur-variables** | Agent | Selon sa carte de decision |
| **Conventions** | Agent | Selon sa carte de decision |
| **Philosophie** | Agent | Selon sa carte de decision |
| **Regles-immuables** | Agent | Selon sa carte de decision |
### Le cycle fondamental (par session LLM)

```
CERBERUS -> AGENT -> CERBERUS
    1         2         3
```

1. Cerberus analyse le besoin et active l'agent adapte
2. L'agent execute sa mission en suivant sa carte de decision
3. L'agent reactive Cerberus a la fin (toujours)

**Multi-session** : plusieurs LLM peuvent travailler sur le meme projet. Au demarrage, chaque LLM lance `python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py sidentifier` pour obtenir SA session (`session-llm-N`) et demarrer comme Cerberus. Chaque session possede SON bloc dans AGENTS.md (## Sessions LLM) et SON agent principal. Le cycle se deroule DANS la session : `activer <session> <agent> <raison>` puis `reactiver <session> <raison> <agent>`. L'historique (AGENTS-historique.md) identifie chaque intervention par sa session : `| date | session | agent | raison |`.

### La chaine documentaire (pense-bete -> spec -> todo)

```
CERBERUS -> ATHENA (pense-bete) -> PROMETHEE (spec) -> MINERVE (todo) -> CERBERUS
```

- Athena redige le pense-bete (statut ebauche), puis active Promethee
- Promethee redige la spec, puis active Minerve
- Minerve redige le todo, puis reactive Cerberus
- Chaque agent commence par rechercher les fichiers existants (anti-doublon)

### Fiche d'agent

Chaque agent a :
- **Sa fiche** (`[agent].md`) : role, profil, carte de decision, protocoles
- **Ses corrections** (`corrections.md`) : regles apprises, lecons, surcharges
- **Sa carte de decision** : `SI [mission] ALORS [etapes] -> [protocoles] -> [outils]`

---

## La boite a outils (119 outils)

Les outils sont organises par **action** (chaque dossier = ce que fait l'outil).

| Categorie | Outils | Usage |
|---|---|---|
| **Activer (1)** | activer-agent-principal | Activer/reactiver l agent principal par session (multi-session) |
| **Ajouter (1)** | ajouter-contenu-fichier | Ajouter du contenu a la fin d'un fichier |
| **Analyser (2)** | analyser-dependances, analyser-structure | Comprendre la structure et les dependances |
| **Cartographier (1)** | cartographier-parcours | Cartographier le parcours d un agent (analyse rapide) |
| **Changer (1)** | changer-statut | Changer le statut d'un fichier |
| **Condenser (1)** | condenser-fichier | Reduire la taille des fichiers |
| **Copier (2)** | copier-dossier, copier-fichier | Copier fichiers et dossiers |
| **Corriger (6)** | corriger-accents-zones-sensibles, corriger-dictionnaire-accents, corriger-emojis, corriger-fins-de-ligne, corriger-liens, corriger-nommage | Reparer et ameliorer |
| **Creer (4)** | creer-fichier, creer-remplir-pense-bete, creer-remplir-spec, creer-remplir-todo | Creer fichiers et contenus |
| **Decomposer (1)** | decomposer-fichier | Decomposer les fichiers markdown |
| **Deplacer (1)** | deplacer-fichier | Deplacer ou renommer un fichier |
| **Detecter (7)** | detecter-decalages-catalogue, detecter-divergences-version, detecter-erreur-statut, detecter-impacts, detecter-local-hors-fonction, detecter-surcharge-fichier, detecter-usage-outils-externes | Detecter les erreurs de statut, la surcharge et les local hors fonction |
| **Ecrire (1)** | ecrire-fichier | Ecrire ou ecraser un fichier |
| **Editer (1)** | editer-fichier | Remplacer une chaine dans un fichier |
| **Evaluer (4)** | evaluer-agents, evaluer-coherence, evaluer-conventions, evaluer-structure | Evaluer la coherence du cerveau |
| **Generateurs (10)** | generateurs-amelioration, generateurs-carte, generateurs-case, generateurs-commande, generateurs-ligne, generateurs-outil-temporaire, generateurs-regenerer-catalogue, generateurs-squelette-pense-bete, generateurs-squelette-spec, generateurs-squelette-todo | Generer les squelettes conformes |
| **Gerer (1)** | gerer-sous-mission | Gerer les sorties/reentrees du flux |
| **Guider (1)** | guider-parcours | Guider l agent case par case (jeu de piste) dans son parcours JSON |
| **Inserer (1)** | inserer-contenu-fichier | Inserer du contenu a une position |
| **Lire (4)** | lire-activite-recente, lire-fichier, lire-frontmatter, lire-lignes | Lire le contenu des fichiers |
| **Lister (8)** | lister-agents, lister-appels, lister-dossiers, lister-fichiers, lister-fonctions, lister-outils, lister-prepares, lister-statuts | Decouvrir la structure |
| **Mettre a jour (1)** | mettre-a-jour-readme | Mettre a jour le README depuis les sources |
| **Migrer (1)** | migrer-identite | Migrer l identite d un fichier |
| **Nettoyer (2)** | nettoyer-fichier, nettoyer-sessions | Purifier un fichier |
| **Rechercher (10)** | rechercher-accents-sensibles, rechercher-dossier, rechercher-extension-fichier, rechercher-fichier, rechercher-fichiers-vides, rechercher-pense-betes, rechercher-specs, rechercher-templates, rechercher-texte, rechercher-todos | Rechercher dans le cerveau |
| **Remplacer (1)** | remplacer-texte | Remplacer des paires ancien->nouveau dans plusieurs fichiers (renommages massifs) |
| **Supprimer (3)** | supprimer-dossier, supprimer-fichier, supprimer-ligne | Supprimer fichiers et dossiers |
| **Tester (3)** |  | Securiser les tests |
| **Valider (13)** | valider-cartes-decision, valider-case, valider-conformite-ascii, valider-conventions, valider-ebauche, valider-liens, valider-nommage, valider-numerotation, valider-pense-bete, valider-relecture, valider-spec, valider-tableaux, valider-todo | Verifier la conformite |
| **Verifier (5)** | verifier-documents-manquants, verifier-restauration-sure, verifier-role-fichier, verifier-separation-preoccupations, verifier-systeme | Verifier l'etat reel |
| **Combos (20)** | combo-activation, combo-audit-themis, combo-controle-buffy, combo-controle-impacts, combo-controle-modification, combo-controle-outil, combo-corriger-ascii, combo-corriger-fichier, combo-creer-agent, combo-creer-fichier-cerveau, combo-creer-protocole, combo-maj-readme, combo-sante-tableaux, combo-tester-outil, combos-analyse-projet, combos-audit-general, combos-corriger-non-ascii, combos-maj-readme-massive, combos-moteur, combos-valider-cerveau | Chainer des outils en sequences |
| **Templates (1)** | outil-template | Modele standard de creation d'outils |

**Principe** : Les agents utilisent exclusivement leurs propres outils, pas des outils generiques. Chaque outil est assigne aux agents concernes dans leur carte de decision. Chaque outil existe en 2 versions (.sh et .py) : le choix se fait via le profil systeme stocke dans le classeur-variables (.py si Python dispo, sinon .sh).

**Triplet documentaire** : pour chaque type de document (pense-bete, spec, todo) : un **generateur** cree le squelette, un outil **creer** remplit le contenu, un **validateur** verifie l'integrite.

---

## Le workflow complet

### 1. Demarrage d'une session (demarrer.md)

```
0. S'identifier : python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py sidentifier -> obtenir SA session (session-llm-N)
1. Lire AGENTS.md (agent principal de SA session)
2. Se presenter automatiquement
3. Verifier si la fiche de l'agent existe (sinon la creer)
4. Lire corrections.md EN PRIORITE
5. Lire la fiche d'agent + sa carte de decision
6. Mettre a jour SON bloc dans AGENTS.md (avec sa session)
7. Travailler sur la mission
8. Detectar les erreurs -> ajouter dans corrections.md
```

### 2. Identification et activation

- Chaque LLM s'identifie au demarrage : python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py sidentifier -> obtient SA session (session-llm-N) et demarre comme Cerberus
- L'utilisateur nomme un agent -> l'agent devient actif pour la session
- **Activer SANS lire la fiche = inutile** (regle fondamentale)
- Le changement d'agent passe TOUJOURS par Cerberus, dans SA session

### 3. Execution d'une mission

Chaque agent suit sa **carte de decision** :
```
SI [mission] ALORS [ligne de decision]
  -> [etapes dans l'ordre]
  -> [protocole a lire a CHAQUE etape]
  -> [outil a utiliser a CHAQUE etape]
```

**Regle d'or** : Ne PAS supposer. VERIFIER a chaque etape.

### 4. Le workflow RVAV (obligatoire)

Tout fichier passe par 5 statuts : `ebauche -> prepare -> dev -> test -> valide`

Chaque transition de statut exige une **boucle RVAV complete** :

| Etape | Action |
|---|---|
| **[R]echercher** | Rassembler les references et dependances |
| **[V]erifier** | Checklist : nommage, liens, sous-fichiers |
| **[A]nalyser** | Relire, verifier la coherence interne |
| **[V]alider** | Decider : Avancer / Rester / Reculer |
| **[P]urifier** | Nettoyer le fichier (derniere etape) |

En cas d'erreur : `class` +1, renommage, retour au travail. Jamais d'avancee sans RVAV valide.

### 5. Auto-correction (cycle d'apprentissage)

```
SESSION 1 : erreur -> correction ajoutee dans corrections.md
SESSION 2 : l'agent lit ses corrections -> evite l'erreur
```

Les 4 piliers :
1. **Memoire persistante** : l'agent se souvient de ses erreurs
2. **Amelioration continue** : chaque session rend l'agent meilleur
3. **Personnalisation** : chaque agent a sa propre methodologie
4. **Auto-correction** : l'agent corrige ses propres erreurs

### 6. Tests encadres

- Numerotation : `test-XXX-nom-outil/` avec `test-001-outil.md` et `.sh`
- Chaque test numerote dans le fichier (Test 1, Test 2...)
- **Protections** dans `tester/protections/` :
  - Anti-boucles-infinies (timeout + kill)
  - Anti-erreurs-silencieuses (detection sortie vide + code retour)
  - Anti-blocage (surveillance sortie + temps)
- Les protections englobent les tests et generent un rapport

---

## Les regles immuables

Non negociables. Tout agent doit les respecter :

| Regle | Contenu |
|---|---|
| **regles-veracite** | Ne jamais mentir, inventer ou supposer |
| **regles-emojis-ascii** | Emojis bannis, ASCII uniquement |
| **regles-validation-rigoureuse** | Verifier chaque point avant de valider |
| **regles-choisir-agent** | Choisir le bon agent pour la bonne mission |
| **rvav-workflow** | Chaque transition de statut passe par RVAV |

---

## Commencer

1. Lire `demarrer.md`
2. Nommer un agent (ex: "Bonjour Cerberus")
3. Suivre le workflow de demarrage
4. Pour un nouveau projet : `protocole-demarrer-projet/`
5. Pour reprendre : `protocole-reprendre-projet/`

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
| **Class** | Numero de classification (incremente a chaque boucle) |
| **Corrections.md** | Memoire d'apprentissage de chaque agent |
