# Proposition v2 - structure du concept freelance

> Proposition de conception (document de travail, rien n'est cree a partir de
> ce fichier). Objectif : repartir quasi de zero dans cerveau-projet/freelance/
> en concevant une nouvelle structure. Les idees des 7 themes d'analyse-externe.md
> sont les principes de base. La v1 (cerveau-projet/agents/) sert de reference
> pour ce qui fonctionne et ce qui doit changer.
>
> Date : 2026-08-21. Statut : PROPOSITION (a valider avec l'utilisateur avant
> toute creation).
> Mise a jour 2026-08-22 : capture des decisions D1-D18 (mode discussion
> + redaction) - arbre des decisions, non-regression separee, activation
> automatisee, standard UTF-8 + CRLF + emojis, inter-round, theme MARVEL,
> transparence, separation code/donnees, JARVIS, cartes identite, markers.

---

## 0. Transmissions utilisateur (2026-08-21) - journal des decisions

> Mode actuel : DISCUSSION + REDACTION des docs necessaires pour ne rien
> oublier des transmissions de l utilisateur. Rien n est construit a partir
> de ce fichier tant que la conception n est pas validee.

Les decisions transmises par l utilisateur (D1 a D18) :

| # | Decision | Enonce |
|---|---|---|
| D1 | **Carte -> Arbre des decisions** | v1 : la carte de decision. v2 : l arbre des decisions (systeme veineux). Ce qui change : les cases. Chaque branche (theme) mene a des categories, qui menent aux cases d execution, qui menent a leur case suivante, jusqu a leur case de fin. |
| D2 | **Non-regression separee** | Les outils doivent toujours etre dynamiques. La suite de non-regression creee pour les agents freelance ne fait PAS partie de la suite actuelle : objectifs et contrats differents. |
| D3 | **Activation automatisee et transparente** | L activation et le saut entre chaque nouvelle case doivent etre automatises. Rendre le systeme TRANSPARENT pour les agents : automatiser les actions qu ils doivent toujours faire dans la v1. |
| D4 | **Standard UTF-8 + CRLF + emojis (perimetre v2/freelance)** | La v1 a cause beaucoup de corrections avec le choix ASCII + LF + bannir les emojis, trop eloigne du standard des LLM. CLARIFIE le 2026-08-22 : la nouvelle regle s'applique au PERIMETRE V2/FREELANCE uniquement (dossier freelance entier adapte ; nouveaux agents freelance et Redacteur-v2 pour leurs ecritures freelance). Le cerveau V1 garde ASCII strict + LF pur sans exception. Deux standards coexistent, chacun dans son perimetre. |
| D5 | **Arbre = redirections vers fichiers** | Au depart l agent choisit UN THEME. Le theme mene a une SUITE DE REDIRECTIONS : si tu as besoin de faire ca -> lance la commande xxx ; -> suis le parcours xxx ; -> execute le combo xxx ; etc. Pour alleger les arbres : un long parcours = UN AUTRE FICHIER (la case devient une simple redirection vers ce fichier) ; les FINS = UN FICHIER unique de toutes les fins possibles (une seule case = lien vers le fichier et sa fin). Si les process automatiques fonctionnent, les passages d un fichier a l autre sont TRANSPARENTS pour l agent. |
| D6 | **Transparence = commande simple + outils formulaire** | Au moment de l activation, l agent lance UNE SIMPLE COMMANDE qui cache PLUSIEURS outils qui se lancent automatiquement (sans que l agent les lance un par un comme dans la v1). Pour un outil : au lieu d ecrire la commande complete, l agent LANCE l outil puis REMPLIT son FORMULAIRE ; quand il a fini, l OUTIL utilise les infos du formulaire, COMPOSE la commande et L ENVOIE a sa place. |
| D7 | **Format du formulaire d outil (champs, validation, contrat)** | Le formulaire d un outil est DECLARATIF : nom de l outil, version, liste de CHAMPS types (nom, type, requis/optionnel, defaut, description, valeurs possibles). VALIDATION : types, requis, plages, enum, coherence entre champs, messages d erreur clairs (l outil refuse un formulaire invalide AVANT d executer). CONTRAT : le formulaire est le contrat de l outil, le .md documente chaque champ (P1). Format propose : JSON. |
| D8 | **Themes concrets de l arbre (branches)** | L arbre des decisions v2 a des THEMES (branches) concrets de premier niveau. Proposition : CREER, MODIFIER, LIRE, VALIDER, TESTER, REDIGER, NETTOYER, COORDONNER, EXPLORER. Chaque theme mene a une suite de redirections (D5) : si besoin de X -> commande / parcours / combo. Les themes sont des PROPOSITIONS a valider et ajuster avec l utilisateur. |
| D9 | **Historique par agent + tokens-historique.md (PAS de trace unique)** | PAS DE TRACE UNIQUE : l utilisateur refuse un historique.jsonl unique - on garde l HISTORIQUE DES AGENTS comme en v1 (historique par agent/session, meme principe que les agents du cerveau). LES OUTILS S ENREGISTRENT EUX-MEMES : l auto-enregistrement des usages (pas l agent qui declare, l OUTIL qui journalise lui-meme). NOUVEAU FICHIER tokens-historique.md : tableau des ACTIVITES RECENTES + TOKENS consommes, envoyes, recus, en cache. |
| D11 | **Flux ROUND / INTER-ROUND / REPRISE (2026-08-22)** | Un round lance est fini ; erreur hors-perimetre = agent habilite + reprise du round. |
| D12 | **Tracabilite R/IR + perimetre par agent + protection combos (2026-08-22)** | Historique type R ou IR ; chacun n'edite que son perimetre ; combos verrouilles. |
| D13 | **Routage de la porte du marbre (2026-08-22)** | STANDARD -> Socrate repond ; EXCEPTIONNEL -> utilisateur. |
| D10 | **BDD des lecons revue : classees, categorisees, consultables comme une bible** | Les lecons sont CLASSEES ET CATEGORISEES pour facilement etre consultees (categories/themes, index, recherche). Une TABLE DES 20 DERNIERES LECONS donne l apercu recent des apprentissages. Des CASES DE L ARBRE permettent de CONSULTER LES LECONS COMME UNE BIBLE au moment ou l agent en a VRAIMENT besoin (theme/branche LECONS, redirections vers la consultation par categorie). |
| D14 | **Theme de nommage des agents freelance : heros MARVEL (2026-08-22)** | Les agents de la session-freelance prendront les noms des SUPER-HEROS de l'univers MARVEL. Chaque nouvel agent freelance sera nomme d'apres un heros Marvel (ex: Stark, Rogers, Parker, Romanoff, Banner, etc.). Le theme MARVEL donne une identite forte et reconnaissable aux agents de la v2, les distinguant clairement des agents du cerveau v1 (noms mythologiques/structurels : Cerberus, Buffy, Vulcain, etc.). |
| D15 | **Separation code/donnees : fichiers distincts editables sans toucher au code (2026-08-22)** | Chaque outil stocke ses donnees (listes de questions, seuils, messages, regles) dans des FICHIERS DISTINCTS editables. Le code source ne contient AUCUNE valeur en dur : il sait OU les trouver. Exemple concret : un outil qui pose une liste de questions stocke cette liste dans `questions.json` — pour ajouter une question, on edite le JSON, pas le `.py`. Les tests de non-regression lisent leurs cas depuis des fichiers de donnees. TOUT comportement modifiable sans reecrire le code source. |
| D16 | **JARVIS : l outil de communication de l equipe freelance (2026-08-22)** | Un outil de communication nomme JARVIS sera mis en place des le debut de la v2. Il permettra aux agents de se laisser des messages qui seront signales dans leur case de debut (demarrage). L agent qui demarre verra les messages en attente avant de commencer sa mission. JARVIS est l outil prioritaire de coordination inter-agents : il remplace les messages informels et les pertes d information entre les rounds. |
| D17 | **Cartes d identite enrichies : grade, medaille, notation, mots-cles (2026-08-22)** | Chaque agent et chaque fichier aura une carte d identite LARGEMENT AMELIOREE contenant des champs supplementaires : `grade` (niveau hierarchique), `medaille` (recompenses/merites), `notation` (score d evaluation), `mot-cles` (tags de recherche). L en-tete (head) de chaque fichier contiendra cette carte d identite detaillee + la commande qui affiche toutes les fonctions contenues dans le fichier. La carte d identite devient le standard de documentation de TOUT fichier v2. |
| D18 | **Outil markers (debut-fin) : isoler des fragments dans les fichiers (2026-08-22)** | Un outil prioritaire de la v2 installera des MARKERS (balises debut-fin) dans les fichiers pour isoler des fragments. Ces fragments marques seront facilement retrouvables avec les outils de recherche. Usage : `<!-- MARKER:nom -->...<!-- /MARKER:nom -->` delimite une zone nommee ; `rechercher-marker --nom <nom>` retrouve instantanement le fragment. Permet de referencer, extraire, modifier des portions de fichiers sans connaitre les numeros de ligne ni le contenu exact. |

---

## 1. Pourquoi une v2 ? (bilan honnete de la v1)

Ce que la v1 a apporte (a conserver) :

- Le cycle Cerberus -> agent -> Cerberus (point d'entree unique).
- Le concept de fiche + corrections + parcours (carte de decision).
- Les outils organises par categories (une categorie = un dossier).
- Les combos (orchestrateurs declaratifs).
- La separation session / agent (multi-LLM).
- Les regles immuables (marbre, veracite) - avec abandon du standard ASCII/LF au profit de UTF-8 + CRLF + emojis (D4).
- Le protocole de lecons (apprentissage continu).

Les problemes de la v1 (a corriger) :

| Probleme | Symptome |
|---|---|
| **Collision de sessions** | Deux sessions utilisent les MEMES agents -> croisements, activations ecrasees, historiques melanges. |
| **Cartes trop complexes** | 68 cases pour Buffy, branches multiples, formats non conformes recurrents (branche_vraie), garde-fous qui se contredisent. |
| **Verrous et garde-fous en cascade** | Verrou habilitation + verrou marbre + lock cartes + anti-contournement : le systeme se protege contre lui-meme. |
| **Outils specifiques par agent** | Un agent doit demander un outil a Vulcain a chaque besoin -> friction. |
| **Historique volumineux** | AGENTS.md + AGENTS-historique.md + traces : 3 sources qui se desynchronisent. DECISION D9 : on garde l historique par agent (comme les agents du cerveau), on SUPPRIME la trace unique, et on ajoute tokens-historique.md pour les activites + tokens. |
| **Noms en collision (alias vs canonique)** | Le catalogue a des alias, les cartes des noms canoniques : garde-fous en conflit. |

**Decision de conception de la v2** : une session = un domaine, avec SES agents
dedies. La session `session-admin` rassemble les agents EXISTANTS (ceux qui
Gerent le cerveau-projet v1) ; la session `session-freelance` rassemble les
NOUVEAUX agents de la v2 (dans freelance/). Chaque session a SES agents
dedies, jamais partages. Plus de croisement possible.

---

## 2. Les 7 principes (issus d'analyse-externe.md)

| Principe | Source | Application v2 |
|---|---|---|
| **P1 - Point d'entree unique** | Theme 1 | Chaque outil = 1 fichier explicatif + 1 entry + fonctions simples par dossier. |
| **P2 - Modularite stricte (SRP)** | Theme 1 | Une categorie = un dossier autonome, isole. |
| **P3 - Separation des preoccupations** | Theme 3 | Structure / presentation / comportement separes (meme pour les docs). |
| **P4 - Zero valeur en dur** | Theme 4 | Constantes + config + .env : le code ne connait pas les valeurs, il sait ou les trouver. |
| **P5 - SSOT (source unique de verite)** | Theme 5 | Avant de creer, chercher dans l'existant. Une donnee = un seul endroit. |
| **P6 - Diagnostic avant creation** | Theme 5 | Un bug = audit de l'existant, jamais "il manque quelque chose". |
| **P7 - Action minimale (anti code fantome)** | Theme 7 | Ne coder QUE ce qui est demande. Tout superflu = dette technique. |

En plus, deux principes techniques de la v1 qu'on garde et generalise :

| Principe | Source | Application v2 |
|---|---|---|
| **P8 - Integrite par SHA-256** | Theme 6 | Toute donnee critique (carte, fiche, config) porte une empreinte verifiee. |
| **P9 - UTF-8 + CRLF + emojis** | Decision D4 (2026-08-21) | Standard actuel : UTF-8, fins de ligne CRLF, emojis autorises. Abandon du choix v1 (ASCII + LF + bannir les emojis) qui a cause de nombreuses corrections. |

---

## 3. Arborescence proposee

```
cerveau-projet/freelance/
|-- README.md                     <- P1 : point d'entree explicatif du concept v2
|-- demarrage.md                  <- R1 : comment demarrer une session freelance
|-- configuration/
|   |-- config.json               <- P4 : parametres (sessions, agents, chemins)
|   |-- constantes.json           <- P4 : valeurs immuables (noms, codes, seuils)
|   `-- .env.example              <- P4 : secrets (jamais dans le code)
|-- noyau/                        <- P5 : SSOT - ce qui ne change jamais
|   |-- regles-immuables/
|   |-- conventions/
|   `-- protocoles/
|-- agents/                       <- les agents, DEDIES par session
|   `-- freelance/               <- session-freelance : NOUVEAUX agents v2
|       |-- fiche-agent.md
|       |-- corrections-agent.md
|       `-- parcours/             <- carte de decision (format simplifie, voir 4)
|-- outils/                       <- P2 : une categorie = un dossier autonome
|   |-- <categorie>/
|   |   |-- <outil>.md            <- P1 : mode d'emploi (le CONTRAT)
|   |   |-- entry.py              <- P1 : point d'entree (orchestrateur)
|   |   `-- fonctions/            <- P1 : fonctions simples (une tache chacune)
|   `-- index-outils.md
|-- combos/                       <- orchestrateurs declaratifs (a simplifier)
|-- historique/                   <- D9 : PAS de trace unique - historique PAR AGENT
|   |-- historique-agents/        <- comme AGENTS-historique.md en v1 (activites par agent/session)
|   |   `-- historique-<agent>.md
|   |-- registre-usages/          <- les outils s ENREGISTRENT EUX-MEMES (auto-journalisation)
|   |   `-- usages-outils.jsonl
|   `-- tokens-historique.md      <- D9 : tableau des activites recentes + tokens (consommes, envoyes, recus, en cache)
`-- docs/                         <- documentation du concept v2
    `-- analyse-externe.md        <- deja nettoye : base des regles
```

---

## 4. L arbre des decisions v2 (systeme veineux)

> DECISION D1 (2026-08-21) : la carte de decision de la v1 (un depart, une fin)
> est remplacee par l ARBRE DES DECISIONS. Ce qui change : les cases.

Probleme v1 : une carte demarre par un choix unique et finit par une fin
unique. Le parcours est lineaire et n est pas specialise par theme.

Concept v2 - le systeme veineux :

- Chaque BRANCHE (theme) mene a des CATEGORIES.
- Chaque categorie mene a des CASES D EXECUTION.
- Chaque case d execution mene a SA CASE SUIVANTE.
- Les cases suivantes menent a la CASE DE FIN de la branche.

Si l agent choisit le bon chemin (theme) des le depart, toutes les cases
suivantes ont ete concues pour ce theme -> la fin est optimale.

Regles de l arbre v2 :

| Regle | Detail |
|---|---|
| **Pas de depart unique** | Une carte ne demarre plus par un choix unique : le depart choisit la branche (theme). |
| **Pas de fin unique** | Une carte ne finit plus par une fin unique : chaque branche a SA case de fin. |
| **Guidage veineux** | branche (theme) -> categories -> cases d execution -> cases suivantes -> case de fin. |
| **Bon chemin** | Le bon theme choisi des le depart garantit des cases concues pour lui -> fin optimale. |
| **Indices outils** | L outil est reference par SON NOM CANONIQUE (P5) - les alias sont INTERDITS. |
| **Fin = relais** | Chaque fin dit QUI activer (agent suivant), jamais reactiver l entree en milieu de chaine. |
| **Validation** | Un valider-arbre v2 : branches resolues, categories joignables, chaque fin atteinte. |
| **Redirections (D5)** | Les cases d un theme sont des REDIRECTIONS : commande / parcours / combo selon le besoin. |
| **Fichiers separes (D5)** | Un long parcours = un AUTRE FICHIER ; la case devient un simple lien vers ce fichier. |
| **Fins centralisees (D5)** | Un fichier unique contient TOUTES les fins possibles ; une seule case = lien vers le fichier et sa fin. |
| **Transparence (D5)** | Si les process automatiques fonctionnent, les passages d un fichier a l autre sont TRANSPARENTS pour l agent (il ne voit pas le changement de fichier). |

Squelette d arbre (a affiner en discussion) :

```
arbre-v2
|-- racine : l agent choisit UN THEME (D5)
|   |-- theme A
|   |   |-- case : besoin de faire X -> lance la commande xxx (redirection)
|   |   |-- case : besoin de faire Y -> suis le parcours YYY (redirection -> fichier parcours-yyy)
|   |   |-- case : besoin de faire Z -> execute le combo ZZZ (redirection)
|   |   `-- fin : lien vers le fichier des fins (fin A)
|   `-- theme B
|       |-- case : besoin de faire W -> suis le parcours WWW (fichier separe)
|       `-- fin : lien vers le fichier des fins (fin B)
```

### Mecanique des redirections (D5)

- **Depart** : l agent choisit UN theme (pas de depart unique dans l absolu,
  mais UN theme choisi = UN chemin dedie).
- **Suite de redirections** : chaque case du theme est un besoin conditionnel
  -> commande, parcours ou combo a lancer.
- **Allegement** : un long parcours n est JAMAIS inline dans l arbre : il vit
  dans son PROPRE FICHIER, la case de l arbre ne contient que le lien.
- **Fins centralisees** : un fichier unique liste toutes les fins possibles ;
  une seule case y renvoie avec la fin choisie.
- **Transparence** : le passage d un fichier a l autre (arbre -> parcours ->
  fins) est automatise et INVISIBLE pour l agent : il voit une suite continue
  de decisions et d actions (D3).

### Benefices attendus

| Benefice | Detail |
|---|---|
| **Arbres legers** | L arbre ne contient que des choix et des liens, jamais de longs enchainements. |
| **Parcours reutilisables** | Un parcours dans son fichier peut etre reference par plusieurs themes. |
| **Fins unifiees** | Toutes les fins dans un fichier = une seule source a maintenir. |
| **Agent fluide** | L agent ne gere pas les fichiers : il choisit, execute, finit. |

### Themes de l arbre (D8) - PROPOSITION a valider

> DECISION D8 (2026-08-21) : 9 themes (branches) de premier niveau, issus
> des activites reelles de la v1. Chaque theme mene a une suite de
> redirections (D5). PROPOSITION : les noms, buts et redirections sont
> ajustables avec l utilisateur.

| Theme | But | Exemples de redirections (D5) |
|---|---|---|
| **CREER** | Creer un fichier, un outil, un agent, une structure | besoin de creer un fichier -> commande creer-fichier ; besoin de creer un outil -> parcours creation-outil ; besoin de creer un agent -> parcours creation-agent |
| **MODIFIER** | Modifier un fichier, corriger une erreur, adapter | besoin de modifier un fichier -> commande editer-fichier ; besoin de corriger des accents -> commande corriger-accents ; besoin de bumper une version -> commande mettre-a-jour-versions |
| **LIRE** | Consulter, chercher, comprendre l existant | besoin de lire un fichier -> commande lire-fichier ; besoin de chercher un texte -> commande rechercher-texte ; besoin de consulter une lecon -> commande consulter-lecons |
| **VALIDER** | Verifier, controler, auditer | besoin de valider une carte -> commande valider-cartes-decision ; besoin de verifier l ASCII -> commande valider-conformite-ascii ; besoin d auditer -> combo audit |
| **TESTER** | Lancer les tests, verifier la non-regression | besoin de lancer un test -> commande tester-lancer-test ; besoin de non-regression -> parcours non-regression (fichier separe) |
| **REDIGER** | Rediger un rapport, une lecon, un doc | besoin d ecrire un rapport -> commande ecrire-rapport ; besoin d enregistrer une lecon -> commande enregistrer-lecon ; besoin d un doc -> parcours redaction-doc |
| **NETTOYER** | Nettoyer le workspace, supprimer les residus | besoin de nettoyer -> parcours nettoyage (fichier separe) ; besoin de lister les residus -> commande detecter-residus |
| **COORDONNER** | Activer un agent, faire le relais, finir | besoin d activer un agent -> commande activer ; besoin de finir -> fin (lien vers fichier des fins) |
| **EXPLORER** | Explorer, diagnostiquer, comprendre un probleme | besoin d explorer -> parcours exploration ; besoin de diagnostiquer -> commande evaluer-processus |
| **LECONS** | Consulter la BDD des lecons (bible) au moment du besoin | besoin de consulter les 20 dernieres lecons -> commande lecons-recentes ; besoin de chercher une lecon par categorie -> commande consulter-lecons-categorie ; besoin de tout parcourir -> parcours lecons-bible (fichier separe) |

Arbre v2 avec themes concrets :

```
arbre-v2
|-- racine : l agent choisit UN THEME
|   |-- CREER
|   |   |-- besoin de creer un fichier -> commande creer-fichier
|   |   |-- besoin de creer un outil -> parcours creation-outil (fichier separe)
|   |   `-- fin -> lien vers fichier des fins
|   |-- MODIFIER
|   |   |-- besoin de modifier -> commande editer-fichier
|   |   `-- fin -> lien vers fichier des fins
|   |-- LIRE -> commandes de lecture -> fin
|   |-- VALIDER -> commandes de validation -> fin
|   |-- TESTER -> parcours non-regression (fichier separe) -> fin
|   |-- REDIGER -> commandes de redaction -> fin
|   |-- NETTOYER -> parcours nettoyage (fichier separe) -> fin
|   |-- COORDONNER -> commande activer -> fin
|   |-- EXPLORER -> parcours exploration -> fin
|   `-- LECONS -> consulter les lecons (bible) -> fin
```

Regles des themes :

| Regle | Detail |
|---|---|
| **Un theme = une suite de redirections** | Chaque case = un besoin conditionnel -> commande / parcours / combo (D5). |
| **Parcours dans des fichiers separes** | Un theme avec un long parcours (TESTER, NETTOYER, EXPLORER) le stocke dans un fichier dedie. |
| **Nommage des themes** | MAJUSCULES, verbe d action (CREER, LIRE, ...), nom canonique unique (P5). |
| **Extensible** | Les themes sont ajoutables/retirables sans casser l arbre (un theme = une branche independante). |
| **Validation utilisateur** | La liste est une PROPOSITION : l utilisateur ajuste avant construction. |

### La BDD des lecons v2 (D10)

> DECISION D10 (2026-08-21) : la BDD des lecons est revue pour etre
> classee, categorisee et consultable comme une bible au moment du besoin.

#### 1. Classification et categorisation

| Regle | Detail |
|---|---|
| **Categories** | Chaque lecon appartient a UNE categorie (outil, protocole, processus, carte, correction, technique, ...). |
| **Sous-themes** | Une categorie peut avoir des sous-themes pour affiner la recherche. |
| **Index** | Un index des lecons par categorie (table des matieres de la bible). |
| **Recherche** | La recherche par mot-cle, categorie, agent ou date est possible. |
| **Tags** | Chaque lecon porte des tags (mots-cles) pour la trouver facilement. |

#### 2. Table des 20 dernieres lecons

- Un apercu des **20 dernieres lecons** (les plus recentes) est toujours
  disponible : heure, agent, categorie, titre.
- L agent voit immediatement ce qui a ete appris recemment par les autres
  (contexte temps reel, comme l encart de AGENTS-historique.md).

Exemple :

```
| # | Date | Agent | Categorie | Titre |
|---|------|-------|-----------|-------|
| 1 | 21/08 | buffy | outil | format du formulaire d outil (D7) |
| 2 | 21/08 | themis | audit | audit D7 formulaire |
| ... | ... | ... | ... | ... |
| 20 | 20/08 | janus | controle | controle alignement cartes |
```

#### 3. Consultation comme une bible (cas de l arbre)

- Le theme LECONS de l arbre (D8) donne acces a la bible au moment du besoin.
- **Cases dediees** : consulter les 20 dernieres / chercher par categorie /
  parcourir la bible complete (D5 : le long parcours lecons-bible vit dans
  un fichier separe).
- **Au moment du besoin** : quand un agent rencontre un probleme, il consulte
  la bible AVANT de re-inventer (P5/P6 : chercher dans l existant avant de
  creer - les lecons sont la memoire des erreurs deja resolues).
- **Bible = reference** : les lecons sont la reference des apprentissages,
  classees et indexees, pas un journal lineaire illisible.

#### 4. Coherence

- D10 complete D9 (historique) : l historique suit les activites, la BDD des
  lecons stocke les apprentissages categorises.
- Coherent avec P5/P6 (chercher dans l existant avant de creer).
- Coherent avec D5 (les redirections menent a la consultation) et D3
  (transparence : consulter une lecon est une simple redirection).

---

## 5. Le concept d'activation v2

Probleme v1 : garde-fou v0.5.19 qui bloque les activations de chaine legitimes
(chaque agent devait reactiver Cerberus au milieu de la boucle).

Proposition v2 - l'activation devient un contrat simple :

```
activer <session> <agent> <raison>
```

| Regle | Detail |
|---|---|
| **Session dediee** | Un agent n'appartient QU'A SA session. Les agents existants (`session-admin`) ne croisent jamais les nouveaux agents (`session-freelance`). |
| **Relais explicite** | Chaque carte v2 a SA fin = "Activer X" (X = le maillon suivant). L'activation de chaine est AUTORISEE par defaut. |
| **Blocage limite** | Le seul blocage : activer un agent d'UNE AUTRE session (collision). Plus de garde-fou contre les chaines internes. |
| **Retour consolide** | Seul le DERNIER maillon reactive l'entree de SA session, avec le bilan consolide. |
| **Automatise + transparent** | D3 (2026-08-21) : l activation et le saut de case sont AUTOMATISES ; les actions recurrentes de la v1 deviennent TRANSPARENTES pour l agent (il ne les voit plus, il fait SON travail). |
| **Commande simple (D6)** | Au moment de l activation, l agent lance UNE SIMPLE COMMANDE qui cache PLUSIEURS outils : ils se lancent automatiquement, l agent ne les lance pas un par un (fini le travail manuel de la v1). |

---

## 6. Les outils v2

| Regle | Detail |
|---|---|
| **Une categorie = un dossier** | P2 (comme v1, ca fonctionne). |
| **Modele 3 fichiers** | `.md` (contrat) + `entry.py` (orchestrateur) + `fonctions/` (atomiques). |
| **Zero valeur en dur** | P4 + D15 : les outils lisent leurs donnees depuis des fichiers distincts (questions.json, cas-tests.json, schema.json...). Aucune valeur, liste, seuil ou regle dans le code source. |
| **Nom canonique partout** | P5 : le catalogue est la SSOT, les alias n'existent plus dans les usages. |
| **Auto-test** | Chaque outil embarque son test (Theme 2 - checklist avant livraison). |
| **Toujours dynamiques** | D2 (2026-08-21) : les outils evoluent en permanence, jamais figes. |
| **Outil = formulaire (D6)** | L agent LANCE l outil puis REMPLIT son FORMULAIRE ; quand il a fini, l OUTIL utilise les infos du formulaire, COMPOSE la commande et L ENVOIE a sa place. L agent ne connait plus la syntaxe de commande. |
| **Auto-enregistrement (D9)** | L OUTIL s ENREGISTRE LUI-MEME : a chaque execution, il journalise son usage (qui, quand, quoi) dans le registre - l agent n a plus a declarer manuellement (fini les oublis de registre de la v1). |
| **Separation code/donnees (D15)** | REGLE IMMUABLE : chaque outil stocke ses donnees (listes, questions, seuils, regles) dans des FICHIERS DISTINCTS editables sans toucher au code. Le code ne contient AUCUNE valeur en dur. Pour modifier le comportement, on edite le fichier de donnees, pas le source. |

### Tokens et activites (D9) - tokens-historique.md

> DECISION D9 (2026-08-21) : fichier `tokens-historique.md` dans historique/.
> Il contient le tableau des ACTIVITES RECENTES et des TOKENS de la session.

| Contenu | Detail |
|---|---|
| **Activites recentes** | Tableau des activites recentes des agents (heure, agent, id, raison) - comme l encart de AGENTS-historique.md en v1. |
| **Tokens consommes** | Total des tokens consommes par la session (suivi en temps reel). |
| **Tokens envoyes** | Tokens envoyes (prompt / requete). |
| **Tokens recus** | Tokens recus (reponse / completion). |
| **Tokens en cache** | Tokens servis depuis le cache (economies realisees). |

Exemple de tableau :

```
| Heure | Agent | Activite | Tokens env. | Tokens rec. | Cache |
|-------|-------|----------|-------------|-------------|-------|
| 10:00 | buffy | redaction D9 | 1200 | 800 | 0 |
| 10:05 | themis | audit D9 | 900 | 1500 | 300 |
```

Regles du suivi des tokens :

| Regle | Detail |
|---|---|
| **Auto-capture** | Le systeme capture les tokens a chaque activite (envoi, reception, cache) sans action de l agent. |
| **Tableau lisible** | tokens-historique.md est un tableau Markdown, lisible par l utilisateur. |
| **Source de verite** | L historique par agent (historique-agents/) reste la source des ACTIVITES ; tokens-historique.md ajoute les TOKENS. |
| **Pas de trace unique** | Les deux coexistent : aucun fichier unique ne remplace l historique par agent (D9). |

### Mecanique de la transparence (D6)

- **Activation = une commande simple** : une seule commande declenche tout le
  lot d outils necessaires au demarrage (relecture, contexte, chrono, etc.)
  sans que l agent les lance individuellement.
- **Outil = formulaire** : l agent lance l outil, remplit les champs du
  formulaire, valide ; l outil compose la commande complete et l execute.
- **L agent ne compose plus** : il n ecrit plus la syntaxe de commande (qui
  etait source d erreurs en v1 : arguments inverses, chemins, options).
- **Le formulaire est le contrat** : les champs = les parametres de l outil ;
  le .md documente chaque champ (P1).

### Format du formulaire d outil (D7)

> DECISION D7 (2026-08-21) : le formulaire est DECLARATIF (JSON). L agent
> remplit un JSON, l outil le valide puis compose et execute la commande.

#### 1. Structure du formulaire

```json
{
  "outil": "<nom-canonique>",
  "version": "<version-de-l-outil>",
  "champs": [
    {
      "nom": "<nom-du-champ>",
      "type": "texte | nombre | boolean | liste | fichier | enum",
      "requis": true | false,
      "defaut": "<valeur-optionnelle>",
      "description": "<ce que fait ce champ>",
      "valeurs": [ "<si enum : liste des valeurs possibles>" ]
    }
  ]
}
```

#### 2. Les champs types

| Propriete | Role | Detail |
|---|---|---|
| **nom** | Identifie le champ | Utilise par l outil pour composer la commande |
| **type** | Contraint la valeur | texte / nombre / boolean / liste / fichier / enum |
| **requis** | Champ obligatoire ? | true = le formulaire est invalide sans lui |
| **defaut** | Valeur pre-remplie | Optionnel ; utilise si l agent ne renseigne pas |
| **description** | Explique le champ | L agent comprend quoi renseigner (P1) |
| **valeurs** | Enum | Liste fermee des valeurs acceptees (si type enum) |

#### 3. La validation

| Regle | Detail |
|---|---|
| **Type** | La valeur doit correspondre au type declare (texte, nombre, ...). |
| **Requis** | Tout champ requis manquant = formulaire refuse. |
| **Plage** | Les nombres peuvent avoir min/max (si definis dans la description). |
| **Enum** | Une valeur hors de la liste `valeurs` = refuse. |
| **Coherence** | Les champs lies sont verifies ensemble (ex : fichier doit exister). |
| **Message clair** | Chaque erreur dit QUEL champ et POURQUOI (pas d erreur cryptique). |
| **Refus AVANT execution** | Un formulaire invalide n est JAMAIS execute : l outil renvoie la liste des erreurs a corriger. |

#### 4. Le contrat

- Le formulaire EST le contrat de l outil : une declaration declarative des
  entrees, sans syntaxe de commande (P1, P5).
- Le .md de l outil documente chaque champ : nom, type, requis, defaut,
  description, valeurs (une source de verite, pas de doc separee).
- Le schema de validation est derive du formulaire : pas de duplication
  entre le contrat et la validation.
- Un formulaire valide = une commande correcte : l outil compose la
  commande a partir des champs, l agent n ecrit jamais la syntaxe (D6).

#### 5. Exemple concret

```json
{
  "outil": "lire-fichier",
  "version": "1.0.0",
  "champs": [
    { "nom": "chemin", "type": "fichier", "requis": true,
      "description": "Chemin du fichier a lire (relatif au workspace)." },
    { "nom": "lignes", "type": "nombre", "requis": false, "defaut": "2000",
      "description": "Nombre maximal de lignes a lire." },
    { "nom": "mode", "type": "enum", "requis": false, "defaut": "texte",
      "description": "Mode de lecture.", "valeurs": [ "texte", "binaire" ] }
  ]
}
```

## 6bis. La suite de non-regression v2 (SEPAREE)

> DECISION D2 (2026-08-21) : la suite de non-regression des agents freelance
> est SEPAREE de la suite actuelle (celle de la v1).

| Regle | Detail |
|---|---|
| **Suite independante** | Les tests freelance ne font PAS partie de la suite actuelle (test-XXX). |
| **Objectifs differents** | Les objectifs et les contrats a respecter ne sont pas les memes que la v1. |
| **Outils dynamiques** | D2 + D15 : les outils restent dynamiques, leur suite de validation evolue avec eux. Les cas de test sont dans des fichiers de donnees (`cas-tests.json`), editables sans toucher au code du test. |
| **Donnees de test editables** | D15 : ajouter un cas de test = ajouter une entree dans `cas-tests.json`. Le code du test lit le fichier et genere les cas dynamiquement. |
| **Pas de croisement** | Lancer la suite v2 ne touche pas la suite v1, et inversement. |

---

## 7. Les combos v2

Probleme v1 : combos nombreux (30+), definitions JSON lourdes, verrous combines.

Proposition v2 :
- Un combo = un ENCHAINEMENT DECLARATIF SIMPLE (liste d'outils a executer).
- Les combos ne verrouillent plus : ils orchestrent (P2 - un combo ne fait que
  diriger, jamais travailler).
- Un combo peut etre remplace par un simple script d'enchainement si < 3 etapes
  (Theme 1 - la simplicite d'abord).

---

## 8. Les sessions v2 (reponse a l'idee session-admin / session-freelance)

| Session | Domaine | Agents | Role |
|---|---|---|---|
| **session-admin** | Gere le cerveau-projet v1 (agents existants : Cerberus, Buffy, Themis, etc.) | Les agents DEJA EXISTANTS | La session qui pilote le cerveau-projet actuel |
| **session-freelance** | Developpe la v2 dans freelance/ | Les NOUVEAUX agents freelance | Sa propre session, isolee de session-admin |

Regles anti-collision :

1. **1 agent = 1 session** : un agent appartient a UNE seule session, c'est sa
   session de rattachement (champ `session` dans sa fiche).
2. **Une session n'active que SES agents** : un agent existant (session-admin)
   ne peut pas activer un agent freelance, et inversement. Le blocage est
   structurel (le champ session est verifie a l'activation), pas un garde-fou
   ajoute apres coup.
3. **Le cerveau-projet v1 est la propriete de session-admin** ; la v2 (dans
   freelance/) est la propriete de session-freelance. Chaque session ne touche
   qu'a son domaine.

---

## 9. Prochaines etapes (a valider avec l'utilisateur)

1. Rester en mode DISCUSSION + REDACTION : capturer toutes les transmissions
   utilisateur dans ce fichier (journal de la section 0) avant toute creation.
2. Valider cette proposition (ou la modifier) : arbre des decisions, activation
   automatisee et transparente, non-regression separee, standard UTF-8 + CRLF
   + emojis (D1-D4).
3. Creer la structure de base : README, configuration/, noyau/ (regles minimales).
4. Creer le premier agent freelance avec SON arbre des decisions (exemple pilote).
5. Ecrire les regles, conventions et protocoles des agents freelance a partir
   des 7 themes d'analyse-externe.md (prochaine mission).
6. Decider du sort de la v1 (conserver en reference ? archiver ?).

---

## Annexe - ce qui est REPRIS de la v1 comme idee

| Idee v1 | Reutilisation v2 |
|---|---|
| Cycle Cerberus -> agent -> Cerberus | Conserve dans session-admin (agents existants) ; session-freelance a son propre cycle |
| Fiche + corrections + parcours | Conserve (format simplifie) |
| Outils par categories | Conserve (modele 3 fichiers renforce) |
| Combos | Simplifies (enchainement declaratif, pas de verrous) |
| Regles immuables (veracite) | Conservees ; ASCII/LF REMPLACES par UTF-8 + CRLF + emojis (D4) |
| Protocole de lecons | Conserve (apprentissage continu) |
| SHA-256 / empreintes | Generalise (P8) |
| Marbre (zones protegees) | Simplifie : le marbre protege le NOYAU, pas les cartes |



## DECISION DU 2026-08-22 - CLARIFICATION DE D4 : PORTEE PERIMETRE V2/FREELANCE

**Contexte** : contradiction signalee par l audit d ecart du jour - la pratique
reelle du cerveau v1 restait ASCII/LF pendant que D4 annoncait UTF-8/CRLF/emojis.

**Decision utilisateur** :
1. La v2 est une version completement revue de la v1. Beaucoup de correctifs
   d agents auraient pu etre evites si la regle d ecriture avait correspondu au
   standard des LLM. Pour la V2 UNIQUEMENT (PAS la v1), l approche change.
2. Le dossier reelance/ ENTIER est adapte a la nouvelle regle :
   UTF-8 + CRLF + emojis autorises.
3. Tous les NOUVEAUX agents du monde freelance respectent cette regle et
   travaillent ensemble avec elle.
4. Redacteur-v2 (agent de la v1) ecrit SES fichiers FREELANCE avec la nouvelle
   regle ; ses fichiers hors freelance (fiche, corrections, rapports, lecons)
   restent en ASCII strict + LF pur.
5. Le cerveau V1 garde ASCII strict + LF pur SANS exception.

**Regles de coexistence des deux standards** :

| Perimetre | Standard | Verificateur |
|---|---|---|
| cerveau v1 (tout sauf freelance/) | ASCII strict + LF pur | valider-conformite-ascii |
| freelance/ (docs et fichiers de la v2) | UTF-8 + CRLF + emojis autorises | a mecaniser pour la v2 (D2 : non-regression freelance separee) |

Les outils de validation actuels verifient le standard v1 : la non-regression
freelance separee (D2) portera le verificateur du standard v2.



## DECISIONS DU 2026-08-22 - MISE A NIVEAU (D3, D11, D12, D13, D14, D15, D16, D17, D18)

### D11 - Le flux ROUND / INTER-ROUND / REPRISE

Un round lance doit etre FINI (bout-en-bout, jamais Cerberus au milieu).
ERREUR HORS-PERIMETRE detectee -> l'agent active L'AGENT HABILITE avec le
rapport de l'erreur (INTER-ROUND) ; a la fin de l'inter-round, l'habilite
reactive l'appelant qui REPREND son round principal. Cascade autorisee entre
habilites. Une erreur n'est JAMAIS 'seulement detectee' : reparation exclusive
par l'habilite. Source : protocole-fin-mission v0.2.0, spec-guider-parcours
v0.6.3 Pattern 13 regle 5.

### D12 - Tracabilite R/IR + nouveaux verrous

- Colonne R (round) ou IR (inter-round) dans AGENTS-historique et l'encart
  Activites recentes (activer-agent-principal v0.5.25 --type r|ir).
- PERIMETRE PAR AGENT : chaque agent n'edite que les fichiers assignes dans
  SON perimetre.json (pilotes : editer-fichier v0.5.0, ecrire-fichier).
- PROTECTION DES COMBOS : definitions = vulcain exclusivement ;
  verrou d'execution par combo en cours.
- Categorie git/ = hades exclusivement.

### D13 - Routage de la porte du marbre

Propositions STANDARDS (alignement sur regle deja validee, correction
obsolete, precision non contradictoire) -> SOCRATE repond au nom de
l'utilisateur. EXCEPTIONNELLES (perimetre, suppression, multi-zones,
nouveaute) -> validation utilisateur directe. Qualification journalisee
(marbre-log.jsonl), veto utilisateur a posteriori.
Source : protocole-securite-marbre v0.2.0.

### D14 - Theme de nommage des agents freelance : heros MARVEL

> DECISION D14 (2026-08-22) : les agents de la session-freelance prendront
> les noms des SUPER-HEROS de l'univers MARVEL.

Le theme MARVEL s'applique a TOUS les nouveaux agents de `cerveau-projet/freelance/`.

| Regle | Detail |
|---|---|
| **Univers** | MARVEL (comics, films, univers etendu) |
| **Source des noms** | Super-heros Marvel : Stark (Iron Man), Rogers (Captain America), Parker (Spider-Man), Romanoff (Black Widow), Banner (Hulk), etc. |
| **Qui est concerne** | Tous les agents de la session-freelance |
| **Qui n'est PAS concerne** | Les agents du cerveau v1 conservent leurs noms actuels (Cerberus, Buffy, Vulcain...) |
| **Format** | Nom propre (majuscule initiale), en anglais, sans accent ni caractere special. Exemples : Stark, Rogers, Parker, Romanoff, Banner, Fury, Strange, Pym, Danvers, Wilson. |

**Justification** :
- Identite forte et reconnaissable pour les agents de la v2.
- Distinction claire avec les agents du cerveau v1 (noms mythologiques/structurels).
- Univers MARVEL riche et universellement connu, facilitant la memorisation.
- 50+ ans de heros : large reservoir de noms pour les futurs agents.

**Coexistence** : les deux themes de nommage coexistent. La session-llm-N
utilise les agents v1 (Cerberus, Buffy...). La session-freelance utilise
les agents MARVEL (Stark, Rogers...). Chaque session a SA liste d'agents
dans son arbre de decisions.

**Agents MARVEL deja construits** :

| Agent | Univers | Role | Statut |
|---|---|---|---|
| **Shuri** | Black Panther | Constructeur des agents de la v2 | Cree le 2026-08-22 -- premier agent MARVEL operationnel |
| **Stark** | Iron Man | Coordinateur, responsable JARVIS (D16) | Cree le 2026-08-22 -- coordonne Shuri (agents) et Forge (outils) |
| **Forge** | Mutant inventeur | Responsable des outils v2 | Cree le 2026-08-22 -- construit les outils freelance (D15) |
| **Rogers** | Captain America | Gardien des regles, conventions et protocoles | Cree le 2026-08-22 -- veille au respect des regles |
| **Parker** | Spider-Man | Explorateur / diagnostiqueur | Cree le 2026-08-22 -- explore et diagnostique les problemes |
| **JARVIS** | Assistant de Stark | Centre de communication (hub des messages) | Cree le 2026-08-22 -- jarvis.py + serveur MCP |
| **Vision** | Synthezoide (ne de JARVIS) | Gardien exclusif de JARVIS (agent + server MCP) | Cree le 2026-08-23 -- SEUL habilite a modifier jarvis.py / jarvis-server.py / l'agent JARVIS |

> **Prochains agents possibles** : Romanoff, Banner, Fury (theme MARVEL D14) -- a construire par Shuri sur demande de Stark.
> responsable JARVIS (D16). Stark prendra le controle de Shuri.

### D3 - Transparence de l activation entre agents

> DECISION D3 (2026-08-21, clarifiee 2026-08-22) : l activation et le passage
> entre les cases et les agents doivent etre TRANSPARENTS et AUTOMATISES.

Dans la v1, l agent doit manuellement :
1. Relire sa fiche et ses corrections a chaque activation (c0).
2. Lancer guider-parcours pour suivre sa carte.
3. Repondre aux questions case par case.
4. Activer l agent suivant avec la commande exacte.
5. Enregistrer ses usages d outils.

Ces 5 actions sont automatiques, previsibles et repetitives. En v2, elles
sont AUTOMATISEES et INVISIBLES pour l agent :

| Action v1 (manuelle) | Devient en v2 (automatique) |
|---|---|
| Relecture fiche + corrections | Executee automatiquement au demarrage (combo activation) |
| Lancer guider-parcours | L arbre est deja actif, pas besoin de le lancer |
| Repondre aux questions | L agent repond, le systeme route automatiquement |
| Activer l agent suivant | Le systeme detecte la fin et active le suivant |
| Enregistrer les usages | L OUTIL s enregistre lui-meme (D9) |

**Principe cle** : l agent ne voit pas la mecanique. Il choisit, il execute,
il recoit le resultat. Les etapes intermediaires (activation, relecture,
parcours, enregistrement) sont encapsulees dans des combos qui se lancent
seuls. L agent est concentre sur SA mission, pas sur la plomberie.

### D15 - Separation code/donnees : fichiers distincts editables

> DECISION D15 (2026-08-22) : TOUT outil stocke ses donnees dans des FICHIERS
> DISTINCTS editables sans toucher au code source. C'est une REGLE IMMUABLE
> de la v2.

**Pourquoi** : en v1, modifier le comportement d un outil signifie editer
son code source — operation risquee, lente, reservee aux agents habilites.
En v2, le comportement est dans des fichiers de donnees, editables par
n importe quel agent autorise.

**Principe** : le code ne contient AUCUNE valeur en dur. Il sait OU les
trouver. Separation stricte :

| Le code (.py/.sh) | Les donnees (fichiers distincts) |
|---|---|
| Logique metier (comment faire) | Valeurs, listes, seuils, messages (quoi faire avec) |
| Algorithmes, parsing, validation | Questions, reponses, regles, parametres |
| Execute, controle, route | Configure, liste, enumere |

**Exemples concrets** :

| Si un outil... | Le fichier de donnees contient... | Edition sans code |
|---|---|---|
| Pose une liste de questions | `questions.json` : la liste des questions, leurs branches, leurs reponses | Ajouter/supprimer/modifier une question = editer le JSON |
| Lance des tests de non-regression | `cas-tests.json` : chaque cas (entree, sortie attendue, seuil) | Ajouter un cas de test = ajouter une entree JSON |
| Valide un formulaire | `schema-validation.json` : champs, types, contraintes, messages d erreur | Changer une regle de validation = editer le JSON |
| Propose un menu a l agent | `menu.json` : options, descriptions, actions associees | Ajouter une option = ajouter une entree JSON |
| Corrige des accents ou du vocabulaire | `dictionnaire.json` : paires incorrect -> correct | Ajouter un mot a corriger = ajouter une entree |

**Regles de la separation code/donnees** :

| Regle | Detail |
|---|---|
| **Zero valeur en dur** | Aucune liste, seuil, message, question, regle dans le code source. Tout est dans un fichier de donnees. |
| **Un fichier = un type de donnees** | `questions.json`, `cas-tests.json`, `schema.json` — nommage explicite (P1). |
| **Format standard** | JSON (lisible, parseable, validable). Le format est documente dans le .md de l outil. |
| **Edition sans habilitation** | Tout agent autorise peut editer un fichier de donnees (pas besoin d etre Vulcain). |
| **Validation avant usage** | L outil valide le fichier de donnees au chargement (structure, types, references). Invalide = refuse avec message clair. |
| **Versionnement** | Les fichiers de donnees sont versionnes avec l outil (meme version semver). |
| **Tests automatiques** | La non-regression inclut des cas qui lisent les fichiers de donnees et verifient que l outil les utilise correctement. |

**Impact sur la non-regression** : les tests ne sont plus figes dans le code.
Chaque `cas-tests.json` est un fichier editable. Ajouter un cas de test =
ajouter une entree, sans reecrire le test. Les outils de test lisent les
fichiers de donnees et generent les cas dynamiquement (D2 : outils dynamiques).

### D16 - JARVIS : l outil de communication de l equipe freelance

> DECISION D16 (2026-08-22) : un outil de communication nomme JARVIS sera
> mis en place des le debut de la v2. Stark (agent de communication) en est
> le responsable.

JARVIS resout un probleme recurrent de la v1 : les agents ne peuvent pas
se laisser de messages. Quand un agent detecte un probleme qu'il ne peut
pas resoudre, il doit activer l'agent habilite en inter-round — mais si
l'agent habilite n'est pas disponible ou si le message doit attendre, il
n'y a pas de file d'attente.

**Fonctionnement** :

| Fonction | Detail |
|---|---|
| **Laisser un message** | `jarvis message --destinataire <agent> --priorite <1-5> "<message>"` |
| **Consulter ses messages** | Affiches automatiquement dans la case de demarrage de l agent (c0) |
| **Priorites** | 1 = critique (bloque le demarrage), 2 = urgent, 3 = normal, 4 = information, 5 = suggestion |
| **Destinataires** | Un agent, un groupe d agents, ou tous (broadcast) |
| **Expiration** | Un message peut avoir une date d expiration (defaut : 24h) |
| **Accuse de lecture** | L agent destinataire confirme la lecture, l expediteur est notifie |

**Integration dans le parcours** :

```
arbre-v2
|-- racine : l agent choisit UN THEME
|   |-- COORDONNER
|   |   |-- besoin de contacter un agent -> jarvis message
|   |   |-- besoin de consulter mes messages -> jarvis consulter
|   |   `-- fin -> lien vers fichier des fins
```

Chaque agent, a sa case de demarrage (c0), voit automatiquement ses
messages JARVIS en attente. Un message de priorite 1 BLOQUE le demarrage
tant qu'il n'est pas lu ET acquitte.

**Stark, agent de communication** : Stark est responsable de JARVIS. Il
surveille la file de messages, debloque les situations, et s assure que
les communications critiques arrivent a destination. Il est le premier
agent MARVEL nomme et operationnel de la v2.

### D17 - Cartes d identite enrichies : le head de chaque fichier

> DECISION D17 (2026-08-22) : chaque agent et chaque fichier de la v2 aura
> une carte d identite LARGEMENT AMELIOREE contenant des metadonnees riches.

**Champs de la carte d identite** :

| Champ | Type | Description |
|---|---|---|
| `nom` | texte | Nom de l agent ou du fichier |
| `version` | semver | Version semantique |
| `cree` | date | Date de creation |
| `statut` | enum | actif, inactif, en formation, en pause |
| `grade` | enum | **NOUVEAU** - Niveau hierarchique : copper, iron, silver, gold, platinum, diamond |
| `medaille` | liste | **NOUVEAU** - Recompenses/merites obtenues (ex: ["bug-hunter", "zero-defaut", "veteran-100-rounds"]) |
| `notation` | nombre (0-100) | **NOUVEAU** - Score d evaluation global (moyenne des audits) |
| `mot-cles` | liste | **NOUVEAU** - Tags de recherche (ex: ["communication", "coordination", "messages"]) |
| `specialites` | liste | Domaines de competence |
| `outils` | liste | Outils que l agent utilise |

**Pour les fichiers** : chaque fichier v2 aura dans son HEAD (frontmatter
ou en-tete) :
1. Sa carte d identite complete (tous les champs ci-dessus)
2. La COMMANDE qui affiche toutes les fonctions contenues dans le fichier
   (equivalent de `--help` ou `--liste-fonctions`)

Exemple de head de fichier agent v2 :

```yaml
---
identite:
  nom: Stark
  version: 0.1.0
  cree: 2026-08-22
  statut: actif
  grade: gold
  medaille: ["pionnier-marvel"]
  notation: 92
  mot-cles: ["communication", "coordination", "jarvis", "messages"]
  specialites:
    - "Communication inter-agents"
    - "Gestion de JARVIS"
    - "Resolution de blocages"
  outils:
    - jarvis
    - activer-agent
---
# Stark — Agent de communication

> COMMANDE FONCTIONS : `stark --liste-fonctions`
```

**Recherche par mot-cles** : les `mot-cles` permettent de retrouver
instantanement les agents et fichiers par tags. `rechercher-mot-cle
--cle "communication"` retourne tous les fichiers tagues.

### D18 - Outil markers : isoler des fragments dans les fichiers

> DECISION D18 (2026-08-22) : un outil prioritaire installe des MARKERS
> (balises debut-fin) dans les fichiers pour isoler des fragments nommes,
> retrouvables instantanement par les outils de recherche.

**Pourquoi** : en v1, pour retrouver un fragment de code ou de doc, il
faut soit connaitre le numero de ligne (fragile, change a chaque edition),
soit faire une recherche texte (lent, bruyant, dependant du contenu exact).
Les markers resolvent ce probleme de maniere structurelle.

**Syntaxe** :

```markdown
<!-- MARKER:description-outil -->
## Description de l outil

L outil JARVIS permet de...
<!-- /MARKER:description-outil -->
```

Dans le code :

```python
# MARKER:init-config
def init_config():
    """Initialiser la configuration."""
    ...
# /MARKER:init-config
```

**Fonctions de l outil markers** :

| Commande | Action |
|---|---|
| `markers poser --fichier <f> --nom <n>` | Ouvre l editeur pour selectionner debut/fin du fragment, puis insere les balises |
| `markers lister --fichier <f>` | Liste tous les markers presents dans le fichier |
| `markers extraire --nom <n>` | Retourne le contenu du fragment nomme (sans les balises) |
| `markers remplacer --nom <n> --contenu <c>` | Remplace le contenu du fragment par un nouveau contenu |
| `markers verifier --fichier <f>` | Verifie que tous les markers sont bien fermes (pas de balise orpheline) |
| `rechercher-marker --nom <n>` | Retrouve instantanement le fragment dans tout le workspace |

**Regles des markers** :

| Regle | Detail |
|---|---|
| **Nommage unique** | Chaque marker a un nom unique dans le fichier |
| **Balises equilibrees** | Chaque `MARKER:nom` a un `/MARKER:nom` correspondant |
| **Imbrication interdite** | Un marker ne peut pas en contenir un autre (simplicite) |
| **Preservation** | Les editeurs et outils de la v2 preservent les markers (pas de suppression accidentelle) |
| **Index** | Un index global (`markers-index.json`) reference tous les markers du workspace : fichier, nom, ligne debut, ligne fin, hash contenu |

**Cas d usage concrets** :

| Usage | Exemple |
|---|---|
| Referencer une section de doc | `<!-- MARKER:decisions-D14 -->...<!-- /MARKER:decisions-D14 -->` retrouve instantanement la section D14 |
| Isoler une fonction dans le code | `# MARKER:init-config`...`# /MARKER:init-config` — `rechercher-marker --nom init-config` |
| Marquer une zone a modifier | Poser un marker temporaire, travailler dessus, le retirer |
| Extraire un fragment pour audit | `markers extraire --nom decisions-D14` affiche le contenu isole |

## LES AMELIORATIONS DU 2026-08-22 POSITIVES POUR LA V2

Ces trois mecanismes resolvent la famille de problemes qui a motive D4
(moins de corrections inutiles) :

1. **Le perimetre par agent** : les fichiers hors du perimetre sont BLOQUES
   a la source -> fini les modifications accidentelles hors domaine qui ont
   genere tant de reparations en v1.
2. **La protection des combos** (plus puissants que les outils) : definitions
   verrouillees, execution habilitite par combo.
3. **Hades, gardien des archives git** : SEUL habilite aux commandes git,
   avec la REGLE D ANCIENNETE (checkout interdit hors fichiers tres recents)
   et sa caisse a outils hades-contexte-git (verdict RECENT/PERIME automatique).
   Le checkout dangereux qui faillit ecraser la session du jour est desormais
   mecaniquement bloque.

**Principe v2 retenu** : tout ce qui a cause une reparation en v1 doit devenir
un garde-fou mecanique en v2 - la discipline ne suffit pas, le verrou si.
