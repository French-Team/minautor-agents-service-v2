---
identite:
  type: index
  appartient_a: commun
  commun: true
---
# Index des Outils Partages

**Version** : v0.2.0
**Statut** : reorganise
**Protocole** : protocole-outils

---

## Point d'entree

Bienvenue dans la **boite a outils partagee** du cerveau-projet.
Les outils sont organises par **CATEGORIE** (le dossier = ce que fait l'outil : ajouter, analyser, corriger, lister, ...), chaque outil porte le nom de son action.

---

## Categories d'outils (par action)

### Ajouter

| Outil | Description | Chemin |
|---|---|---|
| `ajouter-contenu-fichier` | Ajouter du contenu a la fin d'un fichier (append) | [ajouter/ajouter-contenu-fichier/](ajouter/ajouter-contenu-fichier/) |

### Activer

| Outil | Description | Chemin |
|---|---|---|
| `activer-agent-principal` | Activer/reactiver l agent principal dans AGENTS.md | [activer/activer-agent-principal/](activer/activer-agent-principal/) |

### Analyser

| Outil | Description | Chemin |
|---|---|---|
| `analyser-dependances` | Analyser les dependances | [analyser/analyser-dependances/](analyser/analyser-dependances/) |
| `analyser-io-tests` | Mesurer la lecture/ecriture disque pendant les tests (I/O) | [analyser/analyser-io-tests/](analyser/analyser-io-tests/) |
| `analyser-structure` | Analyser la structure du projet | [analyser/analyser-structure/](analyser/analyser-structure/) |
| `analyser-performance-tests` | Analyser la performance des tests (dernier run) | [analyser/analyser-performance-tests/](analyser/analyser-performance-tests/) |
| `analyser-tokens` | Mesurer les tokens de la session (envoyes/recus/encombrement) | [analyser/analyser-tokens/](analyser/analyser-tokens/) |
| `analyser-noms-maj` | Analyser la casse et la forme des noms references (orphelins, erreurs min/MAJ) dans registre, historique, catalogue, index | [analyser/analyser-noms-maj/](analyser/analyser-noms-maj/) |
| `analyser-workers` | Etude d echelle : temps de la suite a differents nombres de workers paralleles (optimum reel) | [analyser/analyser-workers/](analyser/analyser-workers/) |
| `analyser-fonctions` | Profiler un script (cProfile) et afficher les fonctions les plus couteuses | [analyser/analyser-fonctions/](analyser/analyser-fonctions/) |
| `analyser-round` | Resumer l activite d un round (agents actives, outils utilises, tests lances) | [analyser/analyser-round/](analyser/analyser-round/) |

### Cartographier

| Outil | Description | Chemin |
|---|---|---|
| `cartographier-parcours` | Cartographier le parcours d un agent (arbre ASCII + chemins + impasses) dans un fichier markdown | [cartographier/cartographier-parcours/](cartographier/cartographier-parcours/) |

### Changer

| Outil | Description | Chemin |
|---|---|---|
| `changer-statut` | Changer le statut d'un fichier en le renommant | [changer/changer-statut/](changer/changer-statut/) |

### Combos

| Combo | Description | Chemin |
|---|---|---|
| `combos-audit-general` | Chainage des 4 evaluateurs + synthese | [combos/combos-audit-general/](combos/combos-audit-general/) |
| `combos-corriger-non-ascii` | Chainer rechercher-accents-sensibles + corriger-emojis + corriger-accents-zones-sensibles | [combos/combos-corriger-non-ascii/](combos/combos-corriger-non-ascii/) |
| `combos-valider-cerveau` | Etat de sante du cerveau : relecture + cartes + ASCII en 1 rapport | [combos/combos-valider-cerveau/](combos/combos-valider-cerveau/) |
| `combos-moteur` | Moteur generique de combos declaratifs : execute une definition-combo.json case par case (generateur/outil/controle/fin), variables + interpolation | [combos/combos-moteur/](combos/combos-moteur/) |
| `combo-activation` | Cycle d'activation complet d'une session LLM : sidentifier -> activer -> reactiver (le cycle le plus repete du cerveau, 11 parcours concernes) | [combos/combo-activation/](combos/combo-activation/) |
| `combo-audit-themis` | Suite d'audit croise de Themis (chemin audit du parcours themis) : audit-general -> valider-relecture -> combos-valider-cerveau -> valider-tableaux -> detecteurs | [combos/combo-audit-themis/](combos/combo-audit-themis/) |
| `combo-controle-buffy` | Suite de controle de la mission Buffy (Pattern 3) : mission ecrite, protocole lu, preuve de l etat des fichiers |
| `combo-controle-impacts` | Controle des impacts d'une modification : detecter-impacts (fichiers impliques + statut) -> valider-liens (references croisees). Fichier passe en --var fichier=<chemin> | [combos/combo-controle-impacts/](combos/combo-controle-impacts/) |
| `combo-controle-modification` | Suite de validation d'une modification (chemin modification du parcours janus) : nommage recursif -> liens -> separation -> sante+tableaux -> surcharge -> traces externes | [combos/combo-controle-modification/](combos/combo-controle-modification/) |
| `combo-controle-outil` | Suite de validation d'un outil (chemin outil du parcours janus) : valider-conformite-ascii -> valider-cartes-decision --tous -> valider-liens | [combos/combo-controle-outil/](combos/combo-controle-outil/) |
| `combo-corriger-ascii` | Suite de correction des accents puis validation ASCII (parcours vulcain) : corriger-accents --all --recursive -> valider-conformite-ascii | [combos/combo-corriger-ascii/](combos/combo-corriger-ascii/) |
| `combo-corriger-fichier` | Correction complete d'un fichier du cerveau (chemin modifier du parcours buffy, anciennes cases c12+c13) : corriger-nommage -> corriger-liens -> corriger-emojis -> corriger-accents-zones-sensibles -> condenser-fichier -> nettoyer-fichier. Fichier passe en --var fichier=<chemin> | [combos/combo-corriger-fichier/](combos/combo-corriger-fichier/) |
| `combo-sante-tableaux` | Suite de controle de la sante du cerveau (chemin controler du parcours buffy) : verifier-documents-manquants -> rechercher-fichiers-vides -> combos-valider-cerveau -> valider-tableaux | [combos/combo-sante-tableaux/](combos/combo-sante-tableaux/) |
| `combo-creer-fichier-cerveau` | Creation d'un fichier du cerveau (chemin creer du parcours buffy, v0.3.0) : valider-nommage -> valider-conventions -> rechercher-fichier -> [CONTROLE] -> creer-fichier. Fichier passe en --var chemin=<chemin> --var contenu=<contenu> | [combos/combo-creer-fichier-cerveau/](combos/combo-creer-fichier-cerveau/) |
| `combo-creer-agent` | Creation d'un agent (chemin agent du parcours buffy, v0.3.0) : valider-nommage -> [CONTROLE] -> copier-dossier -> copier-fichier template -> creer-fichier corrections. Agent passe en --var agent=<nom> | [combos/combo-creer-agent/](combos/combo-creer-agent/) |
| `combo-creer-protocole` | Creation d'un protocole (chemin protocole du parcours buffy, v0.3.0) : valider-conventions -> [CONTROLE] -> copier-dossier -> creer-fichier. Chemin passe en --var chemin=<chemin> --var contenu=<contenu> | [combos/combo-creer-protocole/](combos/combo-creer-protocole/) |
| `combo-tester-outil` | Chemin de test de Morpheus encapsule (anciennes cases c4-c6 du parcours morpheus) : ecrire le fichier de test via creer-fichier -> verifier les protections (REGLE ABSOLUE : jamais de test sans protections) -> executer le test. Variables : fichier_test, contenu_test, commande_test | [combos/combo-tester-outil/](combos/combo-tester-outil/) |
| `combo-maj-readme` | Petite mise a jour du README (compteurs et textes cibles) |
| `combos-maj-readme-massive` | Combo grosse MAJ conservative du README : analyse -> verifier -> maj -> correctifs tables/badges -> ASCII | [combos/combos-maj-readme-massive/](combos/combos-maj-readme-massive/) |
| `combos-analyse-projet` | Combo analyse-projet : etat reel du projet + ecarts README vs realite (compteurs, categories, badges) | [combos/combos-analyse-projet/](combos/combos-analyse-projet/) |
| `combo-nettoyage-hygie` | Cycle de nettoyage de Hygie (Pattern 3) : snapshot (preuve) -> detection des residus par zone -> verdict propre / residus a supprimer | [combos/combo-nettoyage-hygie/](combos/combo-nettoyage-hygie/) |

### Condenser

| Outil | Description | Chemin |
|---|---|---|
| `condenser-fichier` | Condenser les fichiers markdown | [condenser/condenser-fichier/](condenser/condenser-fichier/) |

### Configurer

| Outil | Description | Chemin |
|---|---|---|
| `configurer-environnement` | Generer la configuration d environnement adaptative (workers, timeouts) a partir des ressources reelles | [configurer/configurer-environnement/](configurer/configurer-environnement/) |

### Consulter

| Outil | Description | Chemin |
|---|---|---|
| `consulter-lecons` | Consulte la BDD portable des lecons (SQLite, unique et partagee) | [consulter/consulter-lecons/](consulter/consulter-lecons/) |

### Copier

| Outil | Description | Chemin |
|---|---|---|
| `copier-dossier` | Copier un dossier recursivement | [copier/copier-dossier/](copier/copier-dossier/) |
| `copier-fichier` | Copier un fichier vers une destination | [copier/copier-fichier/](copier/copier-fichier/) |

### Corriger

| Outil | Description | Chemin |
|---|---|---|
| `corriger-dictionnaire-accents` | Dictionnaire accent -> ASCII (source de donnees pour corriger-accents-zones-sensibles) | [corriger/corriger-dictionnaire-accents/](corriger/corriger-dictionnaire-accents/) |
| `corriger-accents-zones-sensibles` | Corriger les accents (mode --all : purge totale, regle immuable) | [corriger/corriger-accents-zones-sensibles/](corriger/corriger-accents-zones-sensibles/) |
| `corriger-emojis` | Detecter et remplacer les emojis par des symboles ASCII | [corriger/corriger-emojis/](corriger/corriger-emojis/) |
| `corriger-liens` | Corriger les liens casses | [corriger/corriger-liens/](corriger/corriger-liens/) |
| `corriger-fins-de-ligne` | Convertir les fins de ligne CRLF vers LF (strategie FIGER LF) | [corriger/corriger-fins-de-ligne/](corriger/corriger-fins-de-ligne/) |
| `corriger-nommage` | Corriger le nommage | [corriger/corriger-nommage/](corriger/corriger-nommage/) |
| `corriger-noms-maj` | Corriger la casse et la forme des noms references (normalise le champ outil du registre) | [corriger/corriger-noms-maj/](corriger/corriger-noms-maj/) |

### Creer

| Outil | Description | Chemin |
|---|---|---|
| `creer-fichier` | Creer un nouveau fichier avec verification | [creer/creer-fichier/](creer/creer-fichier/) |
| `creer-remplir-pense-bete` | Creer le contenu des sections d'un pense-bete | [creer/creer-remplir-pense-bete/](creer/creer-remplir-pense-bete/) |
| `creer-remplir-spec` | Creer le contenu des sections d'une spec | [creer/creer-remplir-spec/](creer/creer-remplir-spec/) |
| `creer-remplir-todo` | Creer le contenu des phases d'un todo | [creer/creer-remplir-todo/](creer/creer-remplir-todo/) |

### Decomposer

| Outil | Description | Chemin |
|---|---|---|
| `decomposer-fichier` | Decomposer les fichiers markdown | [decomposer/decomposer-fichier/](decomposer/decomposer-fichier/) |

### Deplacer

| Outil | Description | Chemin |
|---|---|---|
| `deplacer-fichier` | Deplacer ou renommer un fichier | [deplacer/deplacer-fichier/](deplacer/deplacer-fichier/) |

### Detecter

| Outil | Description | Chemin |
|---|---|---|
| `detecter-erreur-statut` | Detecter les fichiers dont le statut ne correspond pas au contenu | [detecter/detecter-erreur-statut/](detecter/detecter-erreur-statut/) |
| `detecter-surcharge-fichier` | Detecter les fichiers qui grossissent trop | [detecter/detecter-surcharge-fichier/](detecter/detecter-surcharge-fichier/) |
| `detecter-local-hors-fonction` | Detecter les local utilises hors fonction dans les scripts bash | [detecter/detecter-local-hors-fonction/](detecter/detecter-local-hors-fonction/) |
| `detecter-usage-outils-externes` | Detecter les traces d'outils externes dans les fichiers (CRLF, non-ASCII, BOM) | [detecter/detecter-usage-outils-externes/](detecter/detecter-usage-outils-externes/) |
| `detecter-convention-nommage` | Detecter les mentions de la convention c<numero>[a-z]? hors contexte etendu cT* (garde-fou anti-recurrence) | [detecter/detecter-convention-nommage/](detecter/detecter-convention-nommage/) |
| `detecter-decalages-catalogue` | Detecter les decalages entre le catalogue du generateur et les interfaces reelles des outils (--aide/--help) | [detecter/detecter-decalages-catalogue/](detecter/detecter-decalages-catalogue/) |
| `detecter-donnees-en-dur` | Detecter les donnees en dur (nombres magiques, chemins, URLs, versions, compteurs) sources de bugs caches + recommander le meilleur format de stockage | [detecter/detecter-donnees-en-dur/](detecter/detecter-donnees-en-dur/) |
| `detecter-fautes-orthographe` | Detecter les fautes d orthographe francaise courantes (dictionnaire extensible, agent Hermes) | [detecter/detecter-fautes-orthographe/](detecter/detecter-fautes-orthographe/) |
| `detecter-evaluations-incompletes` | Scan anti-recurrence : mentions residuelles d'un motif dans les 4 sources (validateur, spec, generateurs, tests) | [detecter/detecter-evaluations-incompletes/](detecter/detecter-evaluations-incompletes/) |
| `detecter-divergences-version` | Detecter les spec/ dont la version diverge de leur .py (regle des 5 fichiers, formats de version varies) | [detecter/detecter-divergences-version/](detecter/detecter-divergences-version/) |
| `detecter-impacts` | Detecter les fichiers impliques par la modification d'un fichier du cerveau (schema identite:) | [detecter/detecter-impacts/](detecter/detecter-impacts/) |
| `detecter-usage-scripts-temporaires` | Mesurer l usage des scripts temporaires (.zz-*/.tmp-*) par les agents et le croiser avec le registre | [detecter/detecter-usage-scripts-temporaires/](detecter/detecter-usage-scripts-temporaires/) |
| `detecter-cablages-manquants` | Detecter les cablages manquants des cartes de decision : cases orphelines, boucles indirectes, references mortes, fins non joignables (complete valider-case) | [detecter/detecter-cablages-manquants/](detecter/detecter-cablages-manquants/) |
| `detecter-residus` | Detecter les residus du workspace, compartimente par zone (cerveau-projet / workspace / tous) : fichiers temp, version egaree, sauvegardes, rapports egare, caches | [detecter/detecter-residus/](detecter/detecter-residus/) |
| `detecter-contradictions` | Croiser les sources (cases, regles, protocoles, git log --all) pour detecter les contradictions - outil d Argus, rapport classe par gravite | [detecter/detecter-contradictions/](detecter/detecter-contradictions/) |
| `detecter-troncatures` | Detecter les elements tronques donc illisibles : fichiers trop longs a lire (binaires ignores), blocs non fermes (JSON/Python/bash invalides), marqueurs de troncature (zones de documentation ignorees), option --exclure | [detecter/detecter-troncatures/](detecter/detecter-troncatures/) |
| `detecter-processus-residuels` | Detecter les processus residuels (python/node/bash) dont la commande reference le projet ou orphelins (parent mort), liste blanche protegee (freebuff, unsloth) | [detecter/detecter-processus-residuels/](detecter/detecter-processus-residuels/) |
| `detecter-recherches-obsoletes` | Detecter les recherches-web obsoletes (age > 30 jours ou date invalidite passee) pour garantir des souvenirs vrais et a jour | [detecter/detecter-recherches-obsoletes/](detecter/detecter-recherches-obsoletes/) |
| `detecter-ecritures-hors-cycle` | Detecter les ecritures de fichiers de travail hors cycle d activation (git + mtime croises avec l historique des activations) | [detecter/detecter-ecritures-hors-cycle/](detecter/detecter-ecritures-hors-cycle/) |

### Ecrire

| Outil | Description | Chemin |
|---|---|---|
| `ecrire-fichier` | Ecrire/echraser le contenu d'un fichier | [ecrire/ecrire-fichier/](ecrire/ecrire-fichier/) |

### Editer

| Outil | Description | Chemin |
|---|---|---|
| `editer-fichier` | Remplacer une chaine par une autre dans un fichier | [editer/editer-fichier/](editer/editer-fichier/) |
| `editer-fichier-agents` | Editer les fiches agents (ligne/bloc, ajouter/supprimer, correcteur ASCII) | [editer/editer-fichier-agents/](editer/editer-fichier-agents/) |
| `editer-parcours` | Editer les parcours de decision JSON de maniere sure (insertion/retrait case, branche, suivant, bump) | [editer/editer-parcours/](editer/editer-parcours/) |

### Evaluer

| Outil | Description | Chemin |
|---|---|---|
| `evaluer-agents` | Verifier que les agents suivent leurs protocoles | [evaluer/evaluer-agents/](evaluer/evaluer-agents/) |
| `evaluer-coherence` | Verifier les liens et references croisees | [evaluer/evaluer-coherence/](evaluer/evaluer-coherence/) |
| `evaluer-conventions` | Verifier le nommage, l'ASCII, le format | [evaluer/evaluer-conventions/](evaluer/evaluer-conventions/) |
| `evaluer-processus` | Detecter les derives de processus (fins, outils hors carte, coherence fiche/carte) | [evaluer/evaluer-processus/](evaluer/evaluer-processus/) |
| `evaluer-rating` | Evaluer la qualite et la performance (note ponderee /100 : tests, series, outils, scripts temp, fiches) | [evaluer/evaluer-rating/](evaluer/evaluer-rating/) |
| `evaluer-structure` | Verifier l'arborescence et les fichiers critiques | [evaluer/evaluer-structure/](evaluer/evaluer-structure/) |

### Enregistrer

| Outil | Description | Chemin |
|---|---|---|
| `enregistrer-lecon` | Enregistre une lecon dans la BDD portable des lecons (SQLite, unique et partagee) | [enregistrer/enregistrer-lecon/](enregistrer/enregistrer-lecon/) |
| `enregistrer-usage-outil` | Enregistre un usage d outil dans le registre JSONL (traces/registre-usages-outils.jsonl) | [enregistrer/enregistrer-usage-outil/](enregistrer/enregistrer-usage-outil/) |

### Executer

| Outil | Description | Chemin |
|---|---|---|
| `executer-script-temporaire` | ENTONNOIR : normalise puis execute un script temporaire (BOM, CRLF, accents) - transparent pour l agent | [executer/executer-script-temporaire/](executer/executer-script-temporaire/) |

---

### Generateurs

| Outil | Description | Chemin |
|---|---|---|
| `generateurs-squelette-pense-bete` | Generer le squelette d'un pense-bete conforme au template | [generateurs/generateurs-squelette-pense-bete/](generateurs/generateurs-squelette-pense-bete/) |
| `generateurs-squelette-spec` | Generer le squelette d'une spec conforme au spec-template | [generateurs/generateurs-squelette-spec/](generateurs/generateurs-squelette-spec/) |
| `generateurs-squelette-todo` | Generer le squelette d'un todo conforme au todo-template | [generateurs/generateurs-squelette-todo/](generateurs/generateurs-squelette-todo/) |
| `generateurs-commande` | Composer et generer une commande complexe en posant une question par parametre | [generateurs/generateurs-commande/](generateurs/generateurs-commande/) |
| `generateurs-amelioration` | Pose une checklist de questions par theme avant toute amelioration d un outil, combo, generateur ou carte | [generateurs/generateurs-amelioration/](generateurs/generateurs-amelioration/) |
| `generateurs-case` | Ajouter, editer, supprimer une case OU ajouter un bloc modele compose COMPLET (decision + branches min 2 + deviation + rejoint, refs pattern-7) d'une carte de decision (parcours JSON) avec recablage auto, --ref (indices reference) et validation auto valider-case --modele | [generateurs/generateurs-case/](generateurs/generateurs-case/) |
| `generateurs-carte` | Agir sur une carte COMPLETE (parcours JSON) : creer un squelette ALLEGE (indices = references, nait CONFORME 0 surcharge), analyser les chemins, detecter les anomalies (structure + delegation validateur-case), dupliquer un chemin (refs conservees) | [generateurs/generateurs-carte/](generateurs/generateurs-carte/) |
| `generateurs-ligne` | Ajouter une LIGNE (chemin de bout en bout) a une carte de decision via des gabarits de groupes de cases (configs : defaut, config-1 deviation, config-2 RVAV, config-3 action), apres verification de la carte Atlas (existence + mtime, blocage + invite a activer Atlas sinon), dry/wet | [generateurs/generateurs-ligne/](generateurs/generateurs-ligne/) |
| `generateurs-outil-temporaire` | Generer un outil temporaire (script Python jetable) dans le workspace : en-tete standard (identite outil-temporaire, ASCII, LF), dry-run par defaut, question de promotion (2e utilisation -> activer Vulcain) | [generateurs/generateurs-outil-temporaire/](generateurs/generateurs-outil-temporaire/) |
| `generateurs-regenerer-catalogue` | Regenerer/synchroniser le catalogue de commandes du generateur a partir des outils reels (descriptions extraites des en-tetes .py, 2 formats) | [generateurs/generateurs-regenerer-catalogue/](generateurs/generateurs-regenerer-catalogue/) |

### Gerer

| Outil | Description | Chemin |
|---|---|---|
| `gerer-sous-mission` | Gerer les sorties/reentrees du flux principal | [gerer/gerer-sous-mission/](gerer/gerer-sous-mission/) |

### Guider

| Outil | Description | Chemin |
|---|---|---|
| `guider-parcours` | Guider l'agent case par case (jeu de piste) dans son parcours JSON : indices outil/fichier/regle + branches selon les reponses | [guider/guider-parcours/](guider/guider-parcours/) |

### Inserer

| Outil | Description | Chemin |
|---|---|---|
| `inserer-contenu-fichier` | Inserer du contenu a une position precise dans un fichier | [inserer/inserer-contenu-fichier/](inserer/inserer-contenu-fichier/) |

### Lire

| Outil | Description | Chemin |
|---|---|---|
| `lire-fichier` | Lire le contenu complet (ou partiel) d'un fichier | [lire/lire-fichier/](lire/lire-fichier/) |
| `lire-lignes` | Lire des lignes specifiques d'un fichier (par numero ou plage) | [lire/lire-lignes/](lire/lire-lignes/) |
| `lire-frontmatter` | Extraire le frontmatter YAML en tete d'un fichier markdown | [lire/lire-frontmatter/](lire/lire-frontmatter/) |
| `lire-activite-recente` | Lire les N dernieres interventions des agents (historique) au format condense date | session | agent | action | [lire/lire-activite-recente/](lire/lire-activite-recente/) |
| `lire-head` | Lire le head (en-tete) d'un fichier sans configurer le nombre de lignes (detection automatique de la fin) et comparer plusieurs heads | [lire/lire-head/](lire/lire-head/) |

### Lister

| Outil | Description | Chemin |
|---|---|---|
| `lister-agents` | Lister les agents avec leurs infos | [lister/lister-agents/](lister/lister-agents/) |
| `lister-appels` | Lister les appels de fonctions | [lister/lister-appels/](lister/lister-appels/) |
| `lister-dossiers` | Lister les dossiers d'un chemin | [lister/lister-dossiers/](lister/lister-dossiers/) |
| `lister-fichiers` | Lister les fichiers d'un chemin | [lister/lister-fichiers/](lister/lister-fichiers/) |
| `lister-fonctions` | Lister les fonctions d'un fichier | [lister/lister-fonctions/](lister/lister-fonctions/) |
| `lister-outils` | Lister les outils partages | [lister/lister-outils/](lister/lister-outils/) |
| `lister-prepares` | Lister les fichiers 'prepare' et verifier les specs | [lister/lister-prepares/](lister/lister-prepares/) |
| `lister-statuts` | Lister les fichiers par statut | [lister/lister-statuts/](lister/lister-statuts/) |

### Migrer

| Outil | Description | Chemin |
|---|---|---|
| `migrer-identite` | Migrer les fichiers vers le schema hybride v0.2.0 (bloc identite type/appartient_a/commun), idempotent avec --dry-run | [migrer/migrer-identite/](migrer/migrer-identite/) |
| `migrer-cases-relecture` | Migrer les parcours vers la relecture obligatoire (c0 action RELIRE + c0b question confirmation) | [migrer/migrer-cases-relecture/](migrer/migrer-cases-relecture/) |

### Mettre a jour

| Outil | Description | Chemin |
|---|---|---|
| `mettre-a-jour-readme` | Mettre a jour le README depuis les sources de verite (agents, outils, chronologie) | [mettre-a-jour/mettre-a-jour-readme/](mettre-a-jour/mettre-a-jour-readme/) |
| `mettre-a-jour-versions` | Bump systematique et coherent des versions (le bumper) | [mettre-a-jour/mettre-a-jour-versions/](mettre-a-jour/mettre-a-jour-versions/) |


### Nettoyer

| Outil | Description | Chemin |
|---|---|---|
| `nettoyer-fichier` | Purifier un fichier en supprimant le contenu non essentiel | [nettoyer/nettoyer-fichier/](nettoyer/nettoyer-fichier/) |
| `nettoyer-sessions` | Supprimer TOUTES les sessions LLM (AGENTS.md blocs + Sessions connues, classeur profil-session-*), le journal historique est conserve | [nettoyer/nettoyer-sessions/](nettoyer/nettoyer-sessions/) |
| `snapshot-nettoyage` | Snapshot de l etat du workspace avant nettoyage (agent Hygie) : creer / consulter / rotation 7 jours / liste - preuve de tracabilite | [nettoyer/snapshot-nettoyage/](nettoyer/snapshot-nettoyage/) |
| `nettoyer-processus-residuels` | Terminer les processus residuels detectes (exclusif Hygie via verrou-habilitation, dry-run par defaut, liste blanche protegee) | [nettoyer/nettoyer-processus-residuels/](nettoyer/nettoyer-processus-residuels/) |

### Proteger

| Outil | Description | Chemin |
|---|---|---|
| `proteger-verrou-habilitation` | Verrou d habilitation : bloque l utilisation d un outil par un agent non habilite (source : cartes de decision) | [proteger/proteger-verrou-habilitation/](proteger/proteger-verrou-habilitation/) |
| `proteger-modifier-marbre` | Modifie une zone du marbre (autorisation utilisateur obligatoire + journal) | [proteger/proteger-modifier-marbre/](proteger/proteger-modifier-marbre/) |
| `proteger-verrou-marbre` | Verifie l integrite des zones protegees du marbre (Constitution + cases critiques) | [proteger/proteger-verrou-marbre/](proteger/proteger-verrou-marbre/) |

### Purifier

| Outil | Description | Chemin |
|---|---|---|
| `purifier-rvav` | Purification RVAV : reduire les fichiers surcharges sans perte (deplacement vers une archive cote a cote) | [purifier/purifier-rvav/](purifier/purifier-rvav/) |


### Rechercher

| Outil | Description | Chemin |
|---|---|---|
| `rechercher-accents-sensibles` | Rechercher les accents dans les zones sensibles (frontmatter, noms, blocs, code, liens) | [rechercher/rechercher-accents-sensibles/](rechercher/rechercher-accents-sensibles/) |
| `rechercher-dossier` | Verifier si un dossier existe (retourne 0/1) | [rechercher/rechercher-dossier/](rechercher/rechercher-dossier/) |
| `rechercher-fichier` | Verifier si un fichier existe (retourne 0/1) | [rechercher/rechercher-fichier/](rechercher/rechercher-fichier/) |
| `rechercher-fichiers-vides` | Rechercher les fichiers markdown vides ou quasi vides | [rechercher/rechercher-fichiers-vides/](rechercher/rechercher-fichiers-vides/) |
| `rechercher-pense-betes` | Rechercher les pense-betes existants (anti-doublon) | [rechercher/rechercher-pense-betes/](rechercher/rechercher-pense-betes/) |
| `rechercher-specs` | Rechercher les specs existantes (anti-doublon) | [rechercher/rechercher-specs/](rechercher/rechercher-specs/) |
| `rechercher-templates` | Rechercher les fichiers template du projet | [rechercher/rechercher-templates/](rechercher/rechercher-templates/) |
| `rechercher-texte` | Rechercher un pattern dans un fichier (grep generique) | [rechercher/rechercher-texte/](rechercher/rechercher-texte/) |
| `rechercher-todos` | Rechercher les todos existants (anti-doublon) | [rechercher/rechercher-todos/](rechercher/rechercher-todos/) |
| `rechercher-web` | Recherche web et lecture de page (acces web reel des agents, garantit des souvenirs vrais et a jour) | [rechercher/rechercher-web/](rechercher/rechercher-web/) |
| `rechercher-extension-fichier` | Extraire l'extension d'un fichier (ou verifier une extension) | [rechercher/rechercher-extension-fichier/](rechercher/rechercher-extension-fichier/) |

### Remplacer

| Outil | Description | Chemin |
|---|---|---|
| `remplacer-texte` | Remplacer une liste de paires ancien->nouveau dans plusieurs fichiers (renommages massifs) | [remplacer/remplacer-texte/](remplacer/remplacer-texte/) |
### Supprimer

| Outil | Description | Chemin |
|---|---|---|
| `supprimer-dossier` | Supprimer un dossier recursivement (avec protections) | [supprimer/supprimer-dossier/](supprimer/supprimer-dossier/) |
| `supprimer-fichier` | Supprimer un fichier avec verification | [supprimer/supprimer-fichier/](supprimer/supprimer-fichier/) |
| `supprimer-ligne` | Supprimer une ligne (ou une plage) par numero dans un fichier | [supprimer/supprimer-ligne/](supprimer/supprimer-ligne/) |

### Valider

| Outil | Description | Chemin |
|---|---|---|
| `valider-cartes-decision` | Verifier les cartes de decision des agents | [valider/valider-cartes-decision/](valider/valider-cartes-decision/) |
| `valider-conformite-ascii` | Valider la conformite ASCII de tous les fichiers | [valider/valider-conformite-ascii/](valider/valider-conformite-ascii/) |
| `valider-conventions` | Verifier que les conventions sont respectees | [valider/valider-conventions/](valider/valider-conventions/) |
| `valider-ebauche` | Verifier les exigences minimales d'un ebauche | [valider/valider-ebauche/](valider/valider-ebauche/) |
| `valider-liens` | Verifier que les liens sont valides | [valider/valider-liens/](valider/valider-liens/) |
| `valider-case` | Valide et allege une carte de decision (parcours JSON) : structure, modele compose, surcharge des indices, references, normes - verdict CONFORME / A ALLEGER / NON CONFORME | [valider/valider-case/](valider/valider-case/) |
| `valider-nommage` | Verifier que le nommage est correct | [valider/valider-nommage/](valider/valider-nommage/) |
| `valider-pense-bete` | Verifier l'integrite d'un pense-bete (structure, sections, ASCII) | [valider/valider-pense-bete/](valider/valider-pense-bete/) |
| `valider-relecture` | Verifier que chaque fiche agent + corrections contient la regle de relecture | [valider/valider-relecture/](valider/valider-relecture/) |
| `valider-numerotation` | Detecter les doublons d'etapes (etape X x2) dans les tableaux de mission des fiches agents | [valider/valider-numerotation/](valider/valider-numerotation/) |
| `valider-tableaux` | Verifier la coherence des tableaux des fiches agents : nombres annonces vs lignes, numerotation continue, completude des listes | [valider/valider-tableaux/](valider/valider-tableaux/) |
| `valider-spec` | Verifier l'integrite d'une spec (structure, sections, ASCII) | [valider/valider-spec/](valider/valider-spec/) |
| `valider-todo` | Verifier l'integrite d'un todo (phases 0-9, obligations) | [valider/valider-todo/](valider/valider-todo/) |

### Verifier

| Outil | Description | Chemin |
|---|---|---|
| `verifier-documents-manquants` | Verifier les .sh sans .md et inversement | [verifier/verifier-documents-manquants/](verifier/verifier-documents-manquants/) |
| `verifier-role-fichier` | Verifier qu'un fichier est utilise pour sa fonction | [verifier/verifier-role-fichier/](verifier/verifier-role-fichier/) |
| `verifier-separation-preoccupations` | Verifier la separation des preoccupations | [verifier/verifier-separation-preoccupations/](verifier/verifier-separation-preoccupations/) |
| `verifier-systeme` | Verifier le systeme utilisateur | [verifier/verifier-systeme/](verifier/verifier-systeme/) |
| `verifier-restauration-sure` | Detecter les fichiers non commites avant restauration git | [verifier/verifier-restauration-sure/](verifier/verifier-restauration-sure/) |
| `verifier-conformite-fiche` | Verifie la conformite des fiches agents au template (noyau + variante par famille, sections lues dynamiquement). | [verifier/verifier-conformite-fiche/](verifier/verifier-conformite-fiche/) |

---

## Comment utiliser un outil

### Via le script bash

```bash
# 1. Chercher dans cet index -> trouver l'outil
# 2. Lire la documentation de l'outil
# 3. Executer le script
./[action]/[outil]/[outil].sh [OPTIONS]
# 4. Verifier le resultat
```

### Exemples

```bash
# Verifier le systeme
cerveau-projet/agents/tools/verifier/verifier-systeme/verifier-systeme.sh

# Lister les dossiers
cerveau-projet/agents/tools/lister/lister-dossiers/lister-dossiers.sh

# Lire un fichier
cerveau-projet/agents/tools/lire/lire-fichier/lire-fichier.sh fichier.md

# Rechercher un pattern
cerveau-projet/agents/tools/rechercher/rechercher-texte/rechercher-texte.sh "mot" fichier.md

# Valider les liens
cerveau-projet/agents/tools/valider/valider-liens/valider-liens.sh fichier.md

# Valider un fichier ebauche
cerveau-projet/agents/tools/valider/valider-ebauche/valider-ebauche.sh fichier.md

# Detecter les erreurs de statut
cerveau-projet/agents/tools/detecter/detecter-erreur-statut/detecter-erreur-statut.sh

# Changer le statut d'un fichier
cerveau-projet/agents/tools/changer/changer-statut/changer-statut.sh fichier.md prepare

# Corriger les emojis
cerveau-projet/agents/tools/corriger/corriger-emojis/corriger-emojis.sh fichier.md

# Corriger les accents (mode --all : purge totale, regle immuable)
cerveau-projet/agents/tools/corriger/corriger-accents-zones-sensibles/corriger-accents-zones-sensibles.sh --all fichier.md

# Lister les fichiers 'prepare'
cerveau-projet/agents/tools/lister/lister-prepares/lister-prepares.sh
```

---

## Comment creer un outil

> **REGLE OBLIGATOIRE** (protocole-outils) : toute creation d'outil passe par le `outil-template` (voir section ci-dessous).

```
1. Identifier le besoin (commande frequente)
2. Concevoir l'outil (objectif, parametres)
3. Copier le outil-template vers agents/tools/[categorie]/[nom-outil]/
4. Remplacer les placeholders [nom-outil] (script + documentation)
5. Developper la logique dans [nom-outil].sh
6. Completer la documentation dans [nom-outil].md
7. Tester en --dry-run (obligatoire)
8. Ajouter dans cet index
9. Assigner l'outil a l'agent concerne (protocole-outils Regle 6)
10. Valider la conformite ASCII (valider-conformite-ascii)
```

---

## Tests et Protections

### Protections (tester/)

| Protection | Description | Chemin |
|---|---|---|
| `tester-protection-blocage` | Protection contre les tests qui bloquent | [tester/protections/tester-protection-blocage/](tester/protections/tester-protection-blocage/) |
| `tester-protection-boucles-infinies` | Protection contre les boucles infinies | [tester/protections/tester-protection-boucles-infinies/](tester/protections/tester-protection-boucles-infinies/) |
| `tester-protection-erreurs-silencieuses` | Protection contre les erreurs silencieuses | [tester/protections/tester-protection-erreurs-silencieuses/](tester/protections/tester-protection-erreurs-silencieuses/) |
| `tester-protections` | Point d entree unique importable des protections (lancer_protege + protection STOP fail-fast) | [tester/tester-protections/](tester/tester-protections/) |

---

| `tester-lancer-non-regression` | Lancer tous les tests formels avec bilan OK/KO et registre protege | [tester/tester-lancer-non-regression/](tester/tester-lancer-non-regression/) |
| `recommander-series` | Croiser tags + durees pour recommander une reorganisation des series de la non-regression | [tester/recommander-series/](tester/recommander-series/) |

### Tests (tester/tests/)

| Test | Description | Chemin |
|---|---|---|
| `test-001-evaluer-agents-coherence` | Test des corrections apportees a evaluer-agents et evaluer-coherence. | [tester/tests/test-001-evaluer-agents-coherence/](tester/tests/test-001-evaluer-agents-coherence/) |
| `test-002-combos-moteur` | Test de l outil combos-moteur (etape 2 du plan combo-orchestrateur). | [tester/tests/test-002-combos-moteur/](tester/tests/test-002-combos-moteur/) |
| `test-003-combos-creer` | Test formel des 3 combos creer-* (cases generateur -> outil, Pattern 3). | [tester/tests/test-003-combos-creer/](tester/tests/test-003-combos-creer/) |
| `test-004-combos-tester-outil` | Test formel du combo tester-outil v0.1.0 (Pattern 3, chemin de test de Morpheus encapsule). | [tester/tests/test-004-combos-tester-outil/](tester/tests/test-004-combos-tester-outil/) |
| `test-005-generateurs-commande` | Test formel du generateur de commande v0.2.4 (fiabilisation des flags optionnels), | [tester/tests/test-005-generateurs-commande/](tester/tests/test-005-generateurs-commande/) |
| `test-006-cartographier-parcours` | Test formel de l'outil cartographier-parcours v0.1.0 (categorie cartographier/). | [tester/tests/test-006-cartographier-parcours/](tester/tests/test-006-cartographier-parcours/) |
| `test-007-figer-lf` | Test formel de la mission 1 du plan FIGER LF. | [tester/tests/test-007-figer-lf/](tester/tests/test-007-figer-lf/) |
| `test-008-generateurs-amelioration` | Test formel de l'outil generateurs-amelioration v2.1.0 (categorie generateurs/). | [tester/tests/test-008-generateurs-amelioration/](tester/tests/test-008-generateurs-amelioration/) |
| `test-009-valider-case` | Test formel de l'outil valider-case v1.1.1 (categorie valider/). | [tester/tests/test-009-valider-case/](tester/tests/test-009-valider-case/) |
| `test-010-generateurs-case` | Test formel de l outil generateurs-case v0.4.2 (categorie generateurs/). | [tester/tests/test-010-generateurs-case/](tester/tests/test-010-generateurs-case/) |
| `test-011-generateurs-carte` | Test formel de l outil generateurs-carte v0.3.0 (categorie generateurs/). | [tester/tests/test-011-generateurs-carte/](tester/tests/test-011-generateurs-carte/) |
| `test-012-guider-parcours` | Test formel de l outil guider-parcours v0.5.0 (categorie guider/). | [tester/tests/test-012-guider-parcours/](tester/tests/test-012-guider-parcours/) |
| `test-013-cerberus-migration` | Test formel de la migration pilote du parcours-cerberus v0.4.3 | [tester/tests/test-013-cerberus-migration/](tester/tests/test-013-cerberus-migration/) |
| `test-014-spec-guider-parcours` | Test formel de la spec-guider-parcours v0.6.2 | [tester/tests/test-014-spec-guider-parcours/](tester/tests/test-014-spec-guider-parcours/) |
| `test-015-valider-case-garde-fou` | Test formel du garde-fou anti-pollution de valider-case v1.1.1 | [tester/tests/test-015-valider-case-garde-fou/](tester/tests/test-015-valider-case-garde-fou/) |
| `test-016-migration-buffy` | Test formel de la migration du parcours-buffy v0.3.0 | [tester/tests/test-016-migration-buffy/](tester/tests/test-016-migration-buffy/) |
| `test-017-generateurs-ligne` | Test formel de l'outil generateurs-ligne v0.3.0 (categorie generateurs/). | [tester/tests/test-017-generateurs-ligne/](tester/tests/test-017-generateurs-ligne/) |
| `test-018-fins-reactivation` | Test formel des fins REACTIVER-CERBERUS precisees dans les 11 parcours. | [tester/tests/test-018-fins-reactivation/](tester/tests/test-018-fins-reactivation/) |
| `test-019-combos-controle-buffy` | Test formel du combo controle-buffy v0.1.0 (Pattern 3, preparation d'une mission | [tester/tests/test-019-combos-controle-buffy/](tester/tests/test-019-combos-controle-buffy/) |
| `test-020-combos-clio` | Test formel des 3 combos Clio (Pattern 3, crees pour le test reel de la | [tester/tests/test-020-combos-clio/](tester/tests/test-020-combos-clio/) |
| `test-021-ligne-trio` | Test formel de la LIGNE TRIO de Janus + boucle de correction du trio. | [tester/tests/test-021-ligne-trio/](tester/tests/test-021-ligne-trio/) |
| `test-022-budget-pondere` | Test formel du BUDGET PONDERE des indices par case (valider-case v1.1.0). | [tester/tests/test-022-budget-pondere/](tester/tests/test-022-budget-pondere/) |
| `test-023-grep-budget-pondere` | Test formel du GREP CROISE des seuils BUDGET PONDERE (protocole-verification- | [tester/tests/test-023-grep-budget-pondere/](tester/tests/test-023-grep-budget-pondere/) |
| `test-024-scripts-temporaires` | Test formel du garde-fou anti-scripts-temporaires v0.1.0 | [tester/tests/test-024-scripts-temporaires/](tester/tests/test-024-scripts-temporaires/) |
| `test-025-nettoyer-sessions-garde-fou` | Test formel du garde-fou anti-recurrence : en-tete ## Sessions LLM PRESERVE | [tester/tests/test-025-nettoyer-sessions-garde-fou/](tester/tests/test-025-nettoyer-sessions-garde-fou/) |
| `test-026-detecter-cablages-manquants-garde-fou` | Garde-fou anti-recurrence du bug des cases ORPHELINES (lecon 2026-08-12). | [tester/tests/test-026-detecter-cablages-manquants-garde-fou/](tester/tests/test-026-detecter-cablages-manquants-garde-fou/) |
| `test-027-series-garde-fou` | mod = importlib.util.module_from_spec(spec) | [tester/tests/test-027-series-garde-fou/](tester/tests/test-027-series-garde-fou/) |
| `test-028-coherence-documentaire` | Garde-fou anti-recurrence des ecarts documentaires (lecon 2026-08-12, round 11). | [tester/tests/test-028-coherence-documentaire/](tester/tests/test-028-coherence-documentaire/) |
| `test-029-conformite-template` | GARDE-FOU : chaque test-0XX doit respecter la structure du TEMPLATE de test | [tester/tests/test-029-conformite-template/](tester/tests/test-029-conformite-template/) |
| `test-030-protections-importees` | GARDE-FOU : chaque test-0XX DOIT importer les protections via le point | [tester/tests/test-030-protections-importees/](tester/tests/test-030-protections-importees/) |
| `test-031-chrono-reference` | GARDE-FOU : le lanceur de non-regression affiche un chrono global et gere | [tester/tests/test-031-chrono-reference/](tester/tests/test-031-chrono-reference/) |
| `test-032-pool-workers` | GARDE-FOU : le lanceur de non-regression utilise un POOL DE WORKERS par | [tester/tests/test-032-pool-workers/](tester/tests/test-032-pool-workers/) |
| `test-033-passage-janus-obligatoire` | GARDE-FOU ANTI-RECURRENCE : la fin de mission de Morpheus passe OBLIGATOIREMENT | [tester/tests/test-033-passage-janus-obligatoire/](tester/tests/test-033-passage-janus-obligatoire/) |
| `test-034-cerberus-sans-outils-tests` | GARDE-FOU ANTI-RECURRENCE : la carte de Cerberus n assigne AUCUN outil de test | [tester/tests/test-034-cerberus-sans-outils-tests/](tester/tests/test-034-cerberus-sans-outils-tests/) |
| `test-035-evaluer-processus` | GARDE-FOU : evaluer-processus detecte les derives de processus (fins de | [tester/tests/test-035-evaluer-processus/](tester/tests/test-035-evaluer-processus/) |
| `test-036-detecter-evaluations-incompletes` | GARDE-FOU : detecter-evaluations-incompletes scan les 4 sources | [tester/tests/test-036-detecter-evaluations-incompletes/](tester/tests/test-036-detecter-evaluations-incompletes/) |
| `test-037-seul-janus-lance-non-regression` | GARDE-FOU ANTI-RECURRENCE : SEUL la carte de Janus assigne | [tester/tests/test-037-seul-janus-lance-non-regression/](tester/tests/test-037-seul-janus-lance-non-regression/) |
| `test-038-badge-readme-synchronise` | GARDE-FOU ANTI-RECURRENCE : le badge Outils-N du README (header) doit etre | [tester/tests/test-038-badge-readme-synchronise/](tester/tests/test-038-badge-readme-synchronise/) |
| `test-039-residus-version-racine` | GARDE-FOU ANTI-RECURRENCE : aucun fichier de version accidentel a la racine | [tester/tests/test-039-residus-version-racine/](tester/tests/test-039-residus-version-racine/) |

## Templates

| Template | Description | Chemin |
|---|---|---|
| `outil-template` | Modele standard de creation d outils (script + doc) | [outil-template.md](outil-template.md) |
| `outils-base.md` | Analyse des outils de base : inventaire des outils P0/P1/P2 | [outils-base.md](outils-base.md) |

## Statistiques

| Categorie | Nombre d'outils |
|---|---|
| Ajouter | 1 |
| Analyser | 9 |
| Cartographier | 1 |
| Changer | 1 |
| Combos | 21 |
| Condenser | 1 |
| Configurer | 1 |
| Copier | 2 |
| Corriger | 7 |
| Creer | 4 |
| Decomposer | 1 |
| Deplacer | 1 |
| Detecter | 18 |
| Ecrire | 1 |
| Editer | 3 |
| Enregistrer | 1 |
| Evaluer | 6 |
| Generateurs | 10 |
| Gerer | 1 |
| Guider | 1 |
| Inserer | 1 |
| Lire | 5 |
| Lister | 8 |
| Migrer | 2 |
| Mettre a jour | 2 |
| Activer | 1 |
| Nettoyer | 4 |
| Purifier | 1 |
| Proteger | 3 |
| Rechercher | 11 |
| Remplacer | 1 |
| Supprimer | 3 |
| Valider | 13 |
| Verifier | 6 |
| Executer | 1 |
| Protections | 6 |
| Tests | 41 |
| **Total** | **203** |

> **Note sur le decompte** : 87 outils d'action + 12 combos + 3 protections + 1 template = 104 au total ; `lister-outils.sh` affiche les outils d'action car il exclut `combos/` et `tester/` de son comptage.

---