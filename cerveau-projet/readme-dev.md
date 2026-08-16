---
identite:
  type: index
  appartient_a: commun
  commun: true
---
# Cerveau-Projet -- Documentation Developpeur

> Documentation technique du cerveau-projet, destinee aux developpeurs
> qui travaillent AVEC le systeme d'agents IA. Chaque affirmation est
> verifiable dans les sources de verite (voir section 11).
> Pour une presentation grand public, voir le [README.md](../README.md)
> a la racine du projet.

---

## 1. Vue d'ensemble

| Champ | Valeur |
|---|---|
| **Version** | 0.3.0 (source : `cerveau-projet/agents/clio/version-readme.txt`) |
| **Statut** | stable (source : `cerveau-projet/agents/clio/statut-projet.txt`) |
| **Plateforme** | Windows (bash + Python) |
| **Langages** | Bash, Python, Markdown |
| **Point d'entree** | `demarrer.md` (a lire en premier) |
| **Fichiers racine** | `AGENTS.md` (sessions), `README.md` (public), `cerveau-projet/` (le cerveau) |
| **Agents** | 15 agents + classeur-variables (voir section 4) |
| **Outils** | 144 outils dans 36 categories (voir section 6) |
| **Cartes de decision** | 15 parcours JSON (voir section 5) |

---

## 2. Concept : le cerveau-projet

Le cerveau-projet est une **structure de travail persistante** qui accompagne
un projet de developpement. Il organise le travail, impose des regles,
fournit des outils, et est anime par des agents IA ayant chacun un role
specifique.

**Principe fondateur** : le cerveau evolue dans un projet et se copie dans
le suivant, de plus en plus performant (plus d'agents, plus d'outils, plus
de rigueur).

```
projet/
|-- demarrer.md                  # Point de demarrage (a lire en premier)
|-- AGENTS.md                    # Sessions LLM -- un bloc par session
|-- README.md                    # Presentation grand public
`-- cerveau-projet/
    |-- index-cerveau.md         # Point d'entree du cerveau
    |-- readme-dev.md            # Ce fichier (documentation developpeur)
    |-- agents/                  # Systeme d'agents + outils partages
    |   |-- index-agents.md
    |   |-- [agent]/[agent].md   # Fiche de chaque agent
    |   |-- [agent]/corrections.md  # Corrections et lecons de l'agent
    |   |-- regles-immuables/    # Regles non negociables + protocoles
    |   `-- tools/               # Boite a outils (134 outils)
    |-- pense-betes/             # Idees, specs, todos
    |-- recherches-web/          # Historique des recherches
    `-- exemples/                # Tests et exemples d'utilisation
```

---

## 3. Demarrer une session

### 3.1 S'identifier (mode ID)

Chaque LLM possede SON identifiant (ex : `llm-1`), donne par l'utilisateur
au demarrage. Au demarrage d'une session :

```bash
python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py sidentifier <mon-id>
```

Regle d'alignement : `id llm-N` -> session `session-llm-N` (le numero de
session porte le numero de l'id). L'outil compare l'id aux sessions
enregistrees :
- id deja lie = session retrouvee
- id inconnu `llm-N` = prochaine session libre `session-llm-N` + liaison

Chaque session possede SON bloc dans `AGENTS.md` (section `## Sessions LLM`)
et SON agent principal. Le bloc porte le champ `| **Id LLM** | <id> |` :
le LLM se reconnait en lisant AGENTS.md (source double : AGENTS.md +
classeur-variables synchronises).

### 3.2 Activer un agent

L'utilisateur nomme un agent -> l'agent devient l'agent principal de la
session :

```bash
python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py activer <session> <agent> <raison> <mission>
```

Regle fondamentale : **activer SANS lire la fiche = inutile**. Chaque agent
relit SA fiche et SES corrections avant d'agir (jamais celles des autres).

### 3.3 Reactiver Cerberus (fin de mission)

```bash
python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py reactiver <session> <raison> <agent-precedent>
```

La fin de mission suit **LA CARTE de l'agent** (Pattern 13) : activation
directe par Cerberus -> reactiver Cerberus ; maillon d'une chaine ->
activer le suivant selon SA carte ; seul le DERNIER maillon reactive
Cerberus avec le bilan consolide. La chaine ne retombe JAMAIS sur Cerberus
au milieu.

### 3.4 Lancer plusieurs LLM en parallele

Le systeme est **multi-session** : plusieurs LLM peuvent travailler sur le
meme projet. Chaque LLM s'identifie -> obtient SA session (`session-llm-N`)
-> demarre comme Cerberus. Le cycle se deroule DANS la session :
`activer <session> <agent> <raison>` puis `reactiver <session> <raison>
<agent>`. L'historique (`AGENTS-historique.md`) identifie chaque
intervention par sa session : `| date | session | agent | raison |`.

| Etape | Action |
|---|---|
| 1 | Le LLM s'identifie (`sidentifier`) -> SA session |
| 2 | Il consulte SA session dans `AGENTS.md` (son bloc) |
| 3 | Cerberus analyse le besoin et active l'agent habilite |
| 4 | L'agent execute sa mission en suivant SA carte |
| 5 | La fin suit SA carte (reactiver Cerberus ou activer le suivant) |

---

## 4. Les agents et leurs roles

Source : `AGENTS.md` (liste des agents) + chaque fiche `[agent].md`.

| Agent | Role | Quand l'activer |
|---|---|---|
| **Cerberus** | Gardien de l'entree, coordonne les sessions | Toujours (debut et fin) |
| **Buffy** | Developpeur principal du cerveau | Creation, modification de contenu |
| **Atlas** | Explorateur et documentaliste | Recherche, decouverte, analyse |
| **Janus** | Second controle - SEUL lance la non-regression | Par les agents, en fin de mission |
| **Vulcain** | Constructeur d'outils reels | Transformer un outil.md en outil |
| **Morpheus** | Testeur dedie (tests individuels uniquement) | Ecrire et executer des tests |
| **Athena** | Redactrice de pense-betes | Demande de pense-bete |
| **Promethee** | Redacteur de specs | Pense-bete termine -> spec |
| **Minerve** | Redactrice de todos | Spec terminee -> todo |
| **Clio** | Muse de l'histoire - README (public + dev) | Apres chaque mission (fichiers changes) |
| **Themis** | Evaluatrice croisee - maillon automatique de la chaine | Audit, evaluation, coherence |
| **Hygie** | Agent de nettoyage du workspace | Nettoyage : snapshot, detection, suppression tracee |
| **Hermes** | Agent de la langue - orthographe, vocabulaire, fautes | Correction orthographique, veille vocabulaire |
| **Gardien** | Gardien du marbre - securite du code (zones protegees) | Modification de zone marbre (porte du marbre) |
| **Argus** | Detecteur de contradictions - cases, regles, protocoles, historique git | Doute sur la coherence des regles / protocoles / cases |

> **Note** : le dossier `cerveau-projet/agents/classeur-variables/` est un
> agent-stockage (variables partagees), pas un agent d'action.

---

## 5. La carte de decision et les parcours

### 5.1 Carte de decision

Chaque agent suit SA **carte de decision** (Pattern 8) :

```
SI [mission] ALORS [ligne de decision]
  -> [etapes dans l'ordre]
  -> [protocole a lire a CHAQUE etape]
  -> [outil a utiliser a CHAQUE etape]
```

Source : `cerveau-projet/agents/regles-immuables/general/regles-choisir-agent.md`
(matrice qui fait quoi).

### 5.2 Parcours (jeu de piste)

Le parcours est la **SOURCE DE VERITE du guidage** : un fichier JSON
(`parcours/parcours-<agent>.json`) ou l'agent avance case par case avec
l'outil `guider-parcours` :

```bash
python3 cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py <chemin-du-parcours-json>
```

**13 parcours existants** : athena, atlas, buffy, cerberus, clio, hermes,
hygie, janus, minerve, morpheus, promethee, themis, vulcain.

### 5.3 Structure d'une case

| Champ | Type | Role |
|---|---|---|
| `titre` | texte | Nom de la case |
| `type` | enum | `question` (branches), `action` (suivant), `controle` (branches OUI/NON), `fin` |
| `question` | texte | Question posee (si type question/controle) |
| `branches` | liste | Reponses possibles -> `vers` (case suivante) |
| `suivant` | texte | Case suivante (si type action) |
| `indices` | liste | Indices a appliquer : outil / fichier / regle / ref |
| `message` | texte | Message de fin (si type fin) |

### 5.4 Les indices

Chaque case porte les indices exacts a appliquer :

| Type d'indice | Contenu |
|---|---|
| `outil` | nom + catalogue + chemin + commande exacte (outil du cerveau) |
| `fichier` | chemin + raison (fichier a lire) |
| `regle` | texte de la regle a appliquer |
| `ref` | reference a un pattern (ex : `pattern-3`) ou un document |

> **Regle d'or** : ne PAS supposer. VERIFIER a chaque etape.

---

## 6. Les outils du cerveau

Boite a outils partagee, organisee par **action** (chaque dossier = ce que
fait l'outil). Source de verite : `cerveau-projet/agents/tools/index-tools.md`.

**144 outils dans 36 categories** :

| Categorie | Nb | Exemples |
|---|---|---|
| Activer | 1 | activer-agent-principal |
| Ajouter | 1 | ajouter-contenu-fichier |
| Analyser | 5 | analyser-dependances, analyser-io-tests, analyser-structure, analyser-performance-tests, analyser-tokens |
| Cartographier | 1 | cartographier-parcours |
| Changer | 1 | changer-statut |
| Combos | 21 | combos-moteur, combo-maj-readme, combos-analyse-projet |
| Condenser | 1 | condenser-fichier |
| Copier | 2 | copier-dossier, copier-fichier |
| Corriger | 6 | corriger-accents, corriger-liens, corriger-nommage |
| Creer | 4 | creer-fichier, creer-remplir-* |
| Decomposer | 1 | decomposer-fichier |
| Deplacer | 1 | deplacer-fichier |
| Detecter | 15 | detecter-cablages-manquants, detecter-residus, detecter-fautes-orthographe |
| Ecrire | 1 | ecrire-fichier |
| Editer | 3 | editer-fichier, editer-parcours |
| Enregistrer | 1 | enregistrer-usage-outil |
| Evaluer | 6 | evaluer-processus, evaluer-agents |
| Executer | 1 | executer-script-temporaire (ENTONNOIR) |
| Generateurs | 10 | generateurs-commande, generateurs-amelioration |
| Gerer | 1 | gerer-sous-mission |
| Guider | 1 | guider-parcours |
| Inserer | 1 | inserer-contenu-fichier |
| Lire | 4 | lire-fichier, lire-activite-recente |
| Lister | 8 | lister-agents, lister-outils |
| Mettre a jour | 2 | mettre-a-jour-readme, mettre-a-jour-versions |
| Migrer | 1 | migrer-identite |
| Nettoyer | 3 | nettoyer-fichier, snapshot-nettoyage |
| Proteger | 3 | proteger-verrou-habilitation, proteger-verrou-marbre, proteger-modifier-marbre |
| Purifier | 1 | purifier-rvav |
| Rechercher | 10 | rechercher-texte, rechercher-fichier |
| Remplacer | 1 | remplacer-texte |
| Supprimer | 3 | supprimer-fichier, supprimer-ligne |
| Templates | 1 | outil-template |
| Tester | 3 | tester-protection-blocage, tester-protection-boucles-infinies, tester-protection-erreurs-silencieuses |
| Valider | 13 | valider-cartes-decision, valider-case |
| Verifier | 6 | verifier-conformite-fiche, verifier-systeme |

**Principes** :
- Les agents utilisent **exclusivement leurs propres outils** (regle absolue 4),
  jamais de commandes systeme directes (`cat`, `grep`, `sed`, `python -c`...).
- Chaque outil existe en 2 versions (`.sh` et `.py`) : le choix se fait via
  le profil systeme stocke dans le classeur-variables (`.py` si Python dispo,
  sinon `.sh`).
- Chaque outil est assigne aux agents concernes dans leur carte de decision.
- **ENTONNOIR obligatoire** : tout script temporaire passe par
  `executer-script-temporaire` avant execution (normalisation BOM/CRLF/accents +
  controle compilation + protection de sortie LF) - jamais de `python3` direct
  sur un script de `tmp-<agent>/` (protocole-creation-scripts-temporaires v0.2.10).

---

## 7. Les combos

Les combos sont des **enchainements d'outils en sequences** (Pattern 3).
Source : `cerveau-projet/agents/tools/combos/`.

| Combo | Usage |
|---|---|
| `combos-moteur` | Execute une definition de combo (JSON) |
| `combos-analyse-projet` | Etat reel du projet + ecarts README |
| `combo-maj-readme` | Petite MAJ du README (verifier -> maj -> ASCII) |
| `combos-maj-readme-massive` | Grosse MAJ conservative du README (5 etapes) |
| `combo-activation` | Chaine d'activation d'un agent |
| `combo-controle-buffy` | Controle de mission |
| `combos-valider-cerveau` | Validation du cerveau |

Exemple d'execution d'un combo :

```bash
python3 cerveau-projet/agents/tools/combos/combos-moteur/combos-moteur.py <chemin-definition-combo.json>
```

---

## 8. Le workflow RVAV (obligatoire)

Tout fichier passe par 5 statuts : `ebauche -> prepare -> dev -> test ->
valide`. Chaque transition de statut exige une **boucle RVAV complete** :

| Etape | Action |
|---|---|
| **[R]echercher** | Rassembler les references et dependances |
| **[V]erifier** | Checklist : nommage, liens, sous-fichiers |
| **[A]nalyser** | Relire, verifier la coherence interne |
| **[V]alider** | Decider : Avancer / Rester / Reculer |
| **[P]urifier** | Nettoyer le fichier (derniere etape) |

En cas d'erreur : `class` +1, renommage, retour au travail. Jamais
d'avancee sans RVAV valide.

Source : `cerveau-projet/agents/regles-immuables/general/rvav-workflow.md`.

---

## 9. Les tests et protections

### 9.1 La suite de non-regression

- **46 tests** organises en series thematiques (a, b, c, d, e), lances en
  **parallele** sur un pool de workers (les garde-fous globaux tournent en
  serie apres le pool).
- **Chrono** : mesure le temps total, compare au temps de reference, met a
  jour la reference quand un meilleur temps est atteint.
- **Seul JANUS lance la non-regression complete** (test-037) : les autres
  agents (dont Morpheus) executent uniquement des tests individuels.

```bash
python3 cerveau-projet/agents/tools/tester/tester-lancer-non-regression/tester-lancer-non-regression.py
```

### 9.2 Les protections

Chaque test importe les protections (`tester-protections`) :

| Protection | Role |
|---|---|
| Anti-boucles-infinies | Timeout + kill |
| Anti-erreurs-silencieuses | Detection sortie vide + code retour |
| Anti-blocage | Surveillance sortie + temps |
| STOP fail-fast | Un test en erreur arrete la suite et signale |
| Chrono par etape | Mesure du temps de chaque etape + bilan |

Source : `cerveau-projet/agents/tools/tester/template-test.md` (le template
que chaque test DOIT suivre, v0.3.0 : triplet point_actif/chrono_etape/
bilan_chrono).

---

## 10. L'auto-amelioration

Le systeme s'auto-ameliore en continu :

### 10.1 Cycle d'apprentissage des agents

```
SESSION 1 : erreur -> correction ajoutee dans corrections.md
SESSION 2 : l'agent lit ses corrections -> evite l'erreur
```

Les 4 piliers :
1. **Memoire persistante** : l'agent se souvient de ses erreurs
2. **Amelioration continue** : chaque session rend l'agent meilleur
3. **Personnalisation** : chaque agent a sa propre methodologie
4. **Auto-correction** : l'agent corrige ses propres erreurs

### 10.2 Rondes de qualite des outils

Les outils passent par des rondes d'amelioration continues : robustesse,
performance (parallele), securite des chemins, messages d'erreur, combos
fluides, generateurs fiables et journalisation du registre d'usages.

### 10.3 Le flux d'amelioration (via Cerberus)

Toute demande d'amelioration passe par Cerberus (branche `ameliorer` de sa
carte) :

```
UTILISATEUR -> CERBERUS (c1 ameliorer)
  -> generateurs-amelioration (checklist, themes-amelioration.json)
  -> activation de l'agent habilite
  -> retour -> CLIO met a jour le README public (section Amelioration)
```

Source : `AGENTS.md` + `cerveau-projet/agents/tools/generateurs/
generateurs-amelioration/themes-amelioration.json`.

---

## 11. Sources de verite

| Source | Role |
|---|---|
| `AGENTS.md` | Sessions LLM, agents actifs, historique |
| `AGENTS-historique.md` | Historique des interventions |
| `demarrer.md` | Point de demarrage |
| `cerveau-projet/index-cerveau.md` | Point d'entree du cerveau |
| `cerveau-projet/agents/index-agents.md` | Index des agents |
| `cerveau-projet/agents/tools/index-tools.md` | Index des outils |
| `cerveau-projet/agents/regles-immuables/` | Regles, protocoles, RVAV |
| `cerveau-projet/agents/classeur-variables/` | Variables partagees |
| `cerveau-projet/agents/<agent>/parcours/` | Cartes de decision (12 JSON) |
| `cerveau-projet/agents/clio/version-readme.txt` | Version du README |
| `cerveau-projet/agents/clio/statut-projet.txt` | Statut du projet |

---

## 12. Prise en main rapide (checklist developpeur)

1. Lire `demarrer.md`
2. S'identifier : `activer-agent-principal.py sidentifier <mon-id>`
3. Lire `AGENTS.md` (bloc de MA session)
4. Demarrer comme Cerberus (gardien de l'entree)
5. Nommer un agent pour une mission -> Cerberus active l'agent habilite
6. L'agent suit SA carte (`guider-parcours`) et reactivera selon SA carte
7. Apres une mission qui modifie des fichiers, Cerberus active Clio qui met
   a jour ce readme-dev.md et le README public
8. Janus controle (verdict), Cerberus cloture
