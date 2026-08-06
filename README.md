# Cerveau-Projet

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
| **Outiller** | Boite a outils partagee (bash) creee pour les agents, par les agents |
| **Apprendre** | Chaque agent corrige ses erreurs dans `corrections.md` |
| **Tester** | Tests encadres par des protections (anti-boucle, anti-blocage) |

---

## Structure

```
projet/
├── demarrer.md                  # Point de demarrage (a lire en premier)
├── AGENTS.md                    # Agent principal actuel (dynamique)
├── README.md                    # Ce fichier
└── cerveau-projet/
    ├── index-cerveau.md         # Point d'entree du cerveau
    ├── agents/                  # Systeme d'agents + outils partages
    │   ├── index-agents.md
    │   ├── [agent]/[agent].md   # Fiche de chaque agent
    │   ├── [agent]/corrections.md  # Corrections et lecons de l'agent
    │   └── tools/               # Boite a outils (31 outils + protections)
    ├── pense-betes/             # Idees, conventions, regles, specs, todos
    │   ├── index-pense-bete.md
    │   ├── conventions/         # Renommage, structures, liens, protocoles
    │   ├── regles-immuables/    # Regles non negociables + protocoles + RVAV
    │   ├── specs/               # Definitions techniques
    │   └── pense-betes/         # Travail en cours (statuts ebauche->valide)
    ├── classeur-variables/      # Stockage partage de variables
    ├── recherches-web/          # Historique des recherches effectuees
    └── exemples/                # Tests et exemples d'utilisation
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
| **Clio** | Muse de l'histoire — README | Apres chaque mission (fichiers changes) |

### Le cycle fondamental

```
CERBERUS -> AGENT -> CERBERUS
    1         2         3
```

1. Cerberus analyse le besoin et active l'agent adapte
2. L'agent execute sa mission en suivant sa carte de decision
3. L'agent reactive Cerberus a la fin (toujours)

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

## La boite a outils (53 outils)

| Categorie | Outils | Usage |
|---|---|---|
| **Explorer (13)** | lister-agents, lister-appels, lister-dossiers, lister-fichiers, lister-fonctions, lister-outils, lister-statuts, rechercher-accents-sensibles, rechercher-fichiers-vides, rechercher-pense-betes, rechercher-specs, rechercher-templates, rechercher-todos | Decouvrir la structure, eviter les doublons |
| **Valider (14)** | detecter-erreur-statut, valider-cartes-decision, valider-conformite-ascii, valider-conventions, valider-ebauche, valider-liens, valider-nommage, valider-pense-bete, valider-spec, valider-todo, verifier-documents-manquants, verifier-role-fichier, verifier-separation-preoccupations, verifier-surcharge-fichier | Verifier la conformite |
| **Analyser (5)** | analyser-dependances, analyser-structure, decomposeur, lister-prepares, verifier-systeme | Comprendre le code |
| **Corriger (10)** | changer-statut, condenseur, corriger-accents, corriger-emojis, corriger-liens, corriger-nommage, gerer-sous-mission, mettre-a-jour-readme, modifier-agents-md, purifier-fichier | Reparer et ameliorer |
| **Creer (3)** | remplir-pense-bete, remplir-spec, remplir-todo | Creer le contenu des documents |
| **Generateurs (3)** | squelette-pense-bete, squelette-spec, squelette-todo | Generer les squelettes conformes |
| **Tests (4)** | template-test + protections : blocage, boucles-infinies, erreurs-silencieuses | Securiser les tests |

**Principe** : Les agents utilisent exclusivement leurs propres outils, pas des outils generiques. Chaque outil est assigne aux agents concernes dans leur carte de decision.

**Triplet documentaire** : pour chaque type de document (pense-bete, spec, todo) : un **generateur** cree le squelette, un outil **creer** remplit le contenu, un **validateur** verifie l'integrite.

---

## Le workflow complet

### 1. Demarrage d'une session (demarrer.md)

```
1. Lire AGENTS.md (qui est l'agent principal ?)
2. Se presenter automatiquement
3. Verifier si la fiche de l'agent existe (sinon la creer)
4. Lire corrections.md EN PRIORITE
5. Lire la fiche d'agent + sa carte de decision
6. Mettre a jour AGENTS.md
7. Travailler sur la mission
8. Detectar les erreurs -> ajouter dans corrections.md
```

### 2. Identification et activation

- L'utilisateur nomme un agent -> l'agent devient actif pour la session
- **Activer SANS lire la fiche = inutile** (regle fondamentale)
- Le changement d'agent passe TOUJOURS par Cerberus

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
- **Protections** dans `tests/protections/` :
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
