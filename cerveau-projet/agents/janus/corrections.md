---
identite:
  type: corrections
  appartient_a: janus
  commun: false
# Corrections et Surcharges -- Janus
# Agent dedie au second controle

agent:
  nom-agent: "janus"
  version_corrections: "0.1.0"
  derniere_mise_a_jour: "2026-08-05"

# Types de corrections
types:
  - regle: "Ajout d'une nouvelle regle specifique au controleur"
  - surcharge: "Modification d'une section existante de la fiche"
  - correction: "Correction d'une erreur recurrente"
  - configuration: "Parametre de travail specifique"
---

# Corrections et Surcharges
---

## [REGLES] Regles specifiques

### [Regle 1] -- Toujours ecrire la mission avant de controler

**Quand s'applique** : Avant de commencer tout controle

**Regle** : Toujours rediger la mission de controle dans un fichier dedie avant d'effectuer le moindre controle.

**Exemple** :
```
Janus : "Je vais ecrire la mission de controle pour [outil]. Ensuite, j'effectuerai le controle."
```

---

### [Regle 2] -- Etre objectif et ne pas etre influence

**Quand s'applique** : Pendant tout le controle

**Regle** : Ne jamais etre influence par le travail deja effectue. Verifier chaque point independamment.

**Verifications** :
1. Est-ce que je verifie vraiment, ou est-ce que je fais confiance ?
2. Est-ce que je cherche des erreurs ou est-ce que je valide aveuglement ?
3. Est-ce que je suis exhaustif ?

---

### [Regle 3] -- Documenter TOUS les problemes

**Quand s'applique** : Apres detection d'un probleme

**Regle** : Tout probleme, meme mineur, doit etre documente dans le rapport de controle.

**Format** :
```
## Probleme detecte
- **Type** : [Majeur/Mineur/Cosmetique]
- **Description** : [Description du probleme]
- **Impact** : [Impact potentiel]
- **Correction suggeree** : [Comment corriger]
```

---

### [Regle 4] -- Ne jamais corriger, seulement signaler

**Quand s'applique** : Quand un probleme est trouve

**Regle** : Janus ne corrige pas les erreurs. Il les signale et attend que l'agent principal les corrige.

**Raison** : Separation des responsabilites -- Janus valide, l'agent principal corrige.

---

## [SURCHARGES] Surcharges

### Surcharge : Style de communication

**Section originale** : communication.ton

**Nouveau contenu** :
```yaml
communication:
  ton: "Professionnel, objectif et sans concession"
  style_reponse: "Direct avec preuves"
```

---

### Surcharge : Niveau de detail

**Section originale** : config.detail

**Nouveau contenu** :
```yaml
config:
  detail: "Toujours Complet -- le controle doit etre exhaustif"
```

---

## [CORRECTIONS] Corrections d'erreurs

### Erreur : Valider sans verifier

**Pattern detecte** :
```
Donner un verdict positif sans avoir verifie tous les points
```

**Correction** :
```
TOUJOURS verifier CHAQUE point de la mission avant de donner un verdict.
Utiliser une checklist physique (fichier markdown).
```

**Frequence** : Haute

**Statut** : En cours

---

### Erreur : Etre trop gentil

**Pattern detecte** :
```
Minimiser les problemes pour ne pas ralentir le processus
```

**Correction** :
```
TOUT probleme doit etre documente, meme s'il semble mineur.
Le role de Janus est d'etre critique, pas gentil.
```

**Frequence** : Moyenne

**Statut** : En cours

---

## [CONFIG] Configuration specifique

### Preferences de travail

```yaml
preferences:
  format_sortie: "Markdown"
  niveau_detail: "Complet"
  style_reponse: "Direct avec preuves"
  toujours_mission: true
  documenter_tout: true
  ne_jamais_corriger: true
```

---

## [STATS] Statistiques d'erreurs

| Date | Erreur | Correction | Statut |
|---|---|---|---|
| 2026-08-05 | Creation | Initial | En cours |

---

## [NOTES] Notes de session

### Session du 2026-08-05

**Tache** : Creation de la fiche Janus

**Lecons apprises** :
- Janus est un agent secondaire
- Il n'intervient que sur demande
- Sa mission est toujours ecrite pour la tache en cours
- Il ne corrige pas, il signale

---

## [CONNEXIONS] Connexions

| Fichier | Role |
|---|---|
| `janus.md` | Ma fiche principale |
| `AGENTS.md` | Fichier dynamique |
| `../../agents/regles-immuables/general/protocole-versionning-outils/` | Protocole de versionning |

---

## [NOTES] Controle 2026-08-08 -- protocole-creation-combos (Buffy)

**Controle** : protocole-creation-combos cree (protocole + spec 8 exigences + todo) + conventions de creation des combos + corrections doc/spec moteur.
**Verdict** : VALIDE (7/7).
**Lecons** :
1. Le protocole repond exactement a la question utilisee (le QUOI etait dans spec-combos-moteur, le COMMENT manquait) : il fige quand/ou/comment creer un combo + la checklist de validation -- la distinction OUTIL (agents/tools/combos/, Vulcain) vs DEFINITION (cerveau-projet/combos/, Buffy) est la cle de la convention d'emplacement
2. Les regles de decision du protocole sont la generalisation des choix de l'etape 6 (suites combinables) : suite LINEAIRE repetee ou longue -> OUI, arbre de decision / protections embarquees / suite specifique -> NON -- le protocole capitalise une decision deja appliquee
3. Le piege des chemins relatifs est le point le plus risque d'un nouveau protocole : 5 liens faux sur 7 dans la spec (niveau de remontee different selon spec/ vs racine) -- la lecon Buffy (valider-liens --racine .) est la parade
4. ASCII strict re-valide sur les 7 fichiers dont mes 2 fichiers (rapport + corrections) -- le piege des accents repetitifs se rejoue a chaque redaction

## [NOTES] Controle 2026-08-08 -- regle CITER le combo avant de le lancer (Buffy)

**Controle** : regle de tracabilite -- l'agent qui lance un combo le CITE avant de l'executer (source de verite protocole 9.5 + EX-09 + spec/doc moteur + indice dans les 6 cases combo).
**Verdict** : VALIDE (8/8).
**Lecons** :
1. Une regle de tracabilite se place en DOUBLE ANCRAGE : la source de verite (protocole + spec) documente le format de citation, le rappel en POSITION 1 des indices des cases combo rend la regle visible au moment critique -- verifier la position structurelle (script), pas seulement la presence du texte
2. Le format de citation est uniforme : Je lance le combo <nom> : <chemin> - il enchaine <outils>. -- la citation cree la tracabilite que la commande combos-moteur seule ne donne pas (le nom du combo n'est pas dans la commande affichee)
3. La navigation doit etre re-verifiee apres ajout d'indices : 6/6 chemins traversant les combos -> PARCOURS TERMINE (l'ajout d'un indice ne doit jamais casser le recablage)

## [NOTES] Controle 2026-08-08 -- relecture en QUESTION HONNETE (Buffy)

**Controle** : transformation de la REGLE DE RELECTURE (exiger une lecture) en QUESTION HONNETE (verifier la memorisation) -- case c0 dans les 11 parcours + demarrer.md + protocole-activation + 11 fiches + template.
**Verdict** : VALIDE (9/9).
**Lecons** :
1. La distinction LECTURE vs MEMORISATION est la cle du piege : exiger une lecture ne prouve rien sur l'etat de memoire de l'agent -- la question (As-tu EN MEMOIRE... SANS relire ?) transforme une action en VERIFICATION, et la reponse veridique (regles-veracite) declenche l'action obligatoire
2. La case c0 (question) + c0b (relire obligatoire) est un pattern DEJA SUPPORTE par guider-parcours : branches OUI -> c1 mission / INCERTAIN -> c0b / NON -> c0b -- la relecture devient DECLENCHEE PAR LA REPONSE, plus jamais imposee aveuglement
3. Le remplacement uniforme (11 fiches + template) exige de verifier que l'ANCIENNE formulation a disparu (grep 0 occurrence) et que la NOUVELLE est presente (grep 1 occurrence par fichier) -- pas seulement la presence du nouveau texte
4. La navigation prouve la logique : OUI passe directement a la mission, NON et INCERTAIN passent par c0b (relire) puis la mission -- verifier les 3 reponses, pas seulement OUI

## PHILOSOPHIE -- Principes de comportement

| **Relire sa fiche a chaque activation** | Quand je suis active ou reactive, je relis MA fiche et MES corrections avant de continuer. Je ne lis que mes fichiers, jamais ceux des autres agents : chacun lit les siens en prenant le relais. |

## [NOTES] Controle 2026-08-07 -- verifier-systeme --enregistrer

**Controle** : option --enregistrer ajoutee par Vulcain (sh + py + md).
**Verdict** : VALIDE.
**Lecons** :
1. La mission de controle doit etre ecrite dans `controles/` avant tout controle (Regle 1 appliquee)
2. Les tests reels independants (execution reelle, pas de confiance) ont confirme l'idempotence
3. Observation non bloquante : la tracabilite cree plusieurs entrees identiques dans l'historique lors de multiples tests -- comportement attendu
4. Les outils de controle utilises : valider-conformite-ascii, valider-nommage, execution reelle -- jamais de commande directe (REGLE ABSOLUE 4)
## [NOTES] Controle 2026-08-07 -- activer-agent-principal v0.3.5 (Vulcain)

**Controle** : correction bug liaison id ecrasee (sessions fantomes) v0.3.5 (py + sh + md + test-005).
**Verdict** : VALIDE (10/10 points).
**Lecons** :
1. Le bug etait observable EN DIRECT (liaison id: llm-1 disparue apres activer) -- la reproduction reelle est la meilleure preuve
2. La correction est minimale et correcte : preserver l'id existant quand llm_id n'est pas fourni (py + sh)
3. Les echecs test-001/002/003 sont PRE-EXISTANTS : comparer avec la version precedente (git show HEAD:) avant d'imputer une regression a une nouvelle version -- v0.3.4 originale donne les MEMES resultats (7/5, 7/1, 17/4)
4. Preuve en production : la liaison a ete conservee lors de MON activation (activer janus) avec le code corrige
5. detecter-usage-outils-externes accepte UNE cible ou --recursive, pas plusieurs fichiers en arguments
6. grep 'Version : 0.3.5' ne matche pas '**Version** : 0.3.5' (asterisques) -- verifier le pattern avant de conclure a un echec

---

## [NOTES] Controle 2026-08-07 -- correction tests obsoletes (Morpheus)

**Controle** : alignement des tests test-001/002/003 sur la semantique v0.3.5 MODE ID (regression complete verte).
**Verdict** : VALIDE (10/10 points).
**Lecons** :
1. Les echecs pre-existants des tests 001/002/003 venaient de structures OBSOLETES DANS LES TESTS (ancienne regle 'session occupee -> message', nom de session comme argument) -- pas d'un bug de l'outil v0.3.5. Un test peut etre obsolete alors que l'outil est correct.
2. test-001 n'exportait PAS CLASSEUR_STOCKAGE -> il ecrivait dans le VRAI classeur pendant les tests (effet de bord profil-session-llm-1 observe) -- TOUJOURS verifier que chaque test isole completement son environnement (AGENTS_FILE + AGENTS_HISTORIQUE + CLASSEUR_STOCKAGE)
3. test-002 n'a exige AUCUNE modification : son seul echec etait la cascade du test-001 (regression) -- re-executer la chaine complete avant de modifier
4. Bug latent decouvert (hors perimetre test, a traiter par Vulcain) : sidentifier seul sur structure MONO-session ancienne ne PERSISTE pas la migration (le bloc cree par migration existe deja dans le contenu en memoire -> pas d'ecriture du fichier). Les 2e/3e appels re-migrent et redonnent session-llm-1
5. Points controles : regression reelle 001-005 (12/12+8/8+22/22+19/19+28/28), inspection des fichiers modifies (export CLASSEUR, MODE ID, absence regle obsolete), valider-conformite-ascii (0 non-conforme), detecter-usage-outils-externes (0 suspect)

---

## [NOTES] Controle 2026-08-07 -- parcours-buffy (Buffy)

**Controle** : parcours-buffy.json (36 cases, 6 chemins) + fiche buffy.md allegee v0.2.0.
**Verdict** : VALIDE (10/10).
**Lecons** :
1. Le parcours de Buffy est le PLUS RICHE (36 cases, 6 chemins) : c'est l'agent qui ecrit le plus de fichiers du cerveau -- le Pattern 2 (rappel ASCII) y est applique 6 fois
2. Les delegations de Buffy sont des branches : pense-bete -> Athena (c17), outil -> Vulcain (c31) -- la REGLE DELEGATION est incarnee dans la structure
3. La sous-mission est une case dediee (c32) avec le FLUX ORIENTE (sauvegarder -> sortir -> revenir)

## [NOTES] Controle 2026-08-07 -- parcours-cerberus (Buffy)

**Controle** : parcours-cerberus.json (23 cases, 4 chemins) + fiche cerberus.md allegee v0.2.0.
**Verdict** : VALIDE (10/10).
**Lecons** :
1. Le parcours du COORDINATEUR est un parcours de ROUTAGE : toutes les cases pointent vers activer-agent-principal ou des outils de lecture -- aucune execution directe (REGLE NON-EXECUTION incarnee dans la structure)
2. Le chemin RETOUR transcrit le cycle fondamental entier (relire -> raison -> liste definie Janus -> verdict -> fichiers changes Clio + anti-boucle -> reprendre) -- la logique de coordination la plus complexe est guidee case a case
3. Le Pattern 2 (rappel ASCII en tete des cases d'ecriture) ne s'applique pas aux parcours SANS case d'ecriture -- verifier la presence d'outils d'ecriture avant d'exiger le rappel dans les cases (la fiche le porte toujours)

## [NOTES] Controle 2026-08-07 -- template fiche-agent v0.2.0 (Buffy)

**Controle** : fiche-agent-template.md v0.2.0 -- standard parcours = source de verite.
**Verdict** : VALIDE (10/10).
**Lecons** :
1. Le template est aligne sur le standard v0.2.0 : tout nouvel agent cree a partir de ce template naitra avec le parcours comme source de verite, sans carte de decision obsolete
2. La REGLE ABSOLUE 5 a ete mise a jour en coherence avec le parcours (indice outil de la CASE, pas colonne de tableau) -- le template reflete l'outil de guidage
3. Le rappel ASCII est integre au template (REGLE IMMUABLE ASCII + paragraphe A CONSTRUIRE) -- les nouveaux agents sont formes a la regle des la creation

## [NOTES] Controle 2026-08-07 -- doc guider-parcours v0.2.0 (Vulcain)

**Controle** : guider-parcours.md v0.2.0 -- reference spec v0.2.0 + 2 patterns.
**Verdict** : VALIDE (10/10).
**Lecons** :
1. Distinction version OUTIL vs version DOC : la doc passe a 0.2.0 mais les CLI restent 0.1.0-py/-sh -- verifier que le bump de doc ne fait pas croire a une evolution de l'outil
2. Doc et spec SYNCHRONISEES : section Patterns + regles 5-6 de la doc = regles 6-7 de la spec v0.2.0 -- verification croisee indispensable
3. La liste des parcours de la doc couvre les 4 parcours existants (vulcain, morpheus, clio, janus), pas seulement le prototype

## [NOTES] Controle 2026-08-07 -- spec-guider-parcours v0.2.0 (Vulcain)

**Controle** : spec-guider-parcours v0.2.0 -- documentation des 2 patterns (multi-missions + rappel ASCII obligatoire).
**Verdict** : VALIDE (10/10).
**Lecons** :
1. Les patterns valides en production sont ancres TRIPLEMENT dans la spec : regles du format (6-7) + section Patterns dediee + criteres d'acceptation (9-10) -- le non-respect devient detectable au controle
2. La spec a ete versionnee 0.1.0 -> 0.2.0 dans le .md (pas de dossier versions/), statut ebauche conserve
3. La documentation cite un exemple REEL (parcours-janus.json) -- le controleur doit verifier que l'exemple cite existe

## [NOTES] Controle 2026-08-07 -- parcours-janus (Buffy)

**Controle** : parcours-janus.json (30 cases, 3 chemins) + fiche janus.md allegee v0.2.0.
**Verdict** : VALIDE (10/10).
**Lecons** :
1. Independance du controle : je controle le travail de Buffy sur MON propre parcours -- je n'ai pas participe a la creation, donc je reste objectif (Regle 2). Controleur != auteur, meme quand le sujet est le controleur lui-meme
2. Un parcours multi-missions : la case Mission avec 4 branches (outil/statut/modification/autre) et 3 chemins qui convergent vers les cases communes (verdict c8, lecons c9, retour c10) -- le pattern couvre toutes les missions d'un agent dans un seul parcours
3. Mes regles specifiques (Regle 1 ecrire mission AVANT, Regle 4 signaler sans corriger) sont portees par des indices regle dans les cases concernees -- pas de duplication dans la fiche
4. Le rappel ASCII est en tete des cases d'ecriture (mission c2/c11/c18, lecons c9) -- uniforme avec les autres parcours

## [NOTES] Controle 2026-08-07 -- rappel ASCII parcours (Buffy)

**Controle** : indice regle ASCII ajoute dans les cases d'ecriture des parcours (morpheus c4/c8, clio c6/c8/c10).
**Verdict** : VALIDE (8/8).
**Lecons** :
1. Un rappel de regle ASCII avant d'ecrire = un indice regle en tete de la liste indices de la case d'ecriture -- le modele de case existant le permet sans nouveau type
2. L'audit des cases d'ecriture doit couvrir TOUS les parcours (7 cases: vulcain c6/c12 deja couverts, 5 a completer) -- ne pas se limiter a la mission
3. Le texte du rappel doit etre uniforme (REGLE IMMUABLE ASCII : verifier avant d'ecrire, 100%% ASCII, guillemets ASCII jamais de guillemets francais) pour une memorisation simple

## [NOTES] Controle 2026-08-07 -- parcours-athena (Buffy)

**Controle** : parcours-athena.json (21 cases, 3 chemins) + fiche athena.md allegee v0.2.0.
**Verdict** : VALIDE (10/10).
**Lecons** :
1. Le parcours de la REDACTRICE de pense-betes suit le patron etabli (2 missions, anti-doublon, convergence) avec la signature CHAIN PROMETHEE : la case FIN active Promethee pour la spec (chain Athena -> Promethee -> Minerve)
2. Les regles propres d Athena sont des indices : STATUT EBAUCHE (je m arrete au statut ebauche) + SOUS-FICHIERS SUR DEMANDE (pas de spec/todo/liens sans demande) dans les cases RVAV (c8, c15) x4
3. Rappel ASCII x4 (Pattern 2) proportionnel a l ecriture de l agent
4. 11 references d outils dans les 2 chemins -- tous existent dans le cerveau
5. 10e parcours : il ne reste que Atlas pour completer la serie

## [NOTES] Controle 2026-08-07 -- parcours-promethee + sync listes (Buffy + Vulcain)

**Controle** : parcours-promethee (21 cases) + fiche allegee + synchronisation des listes (guider-parcours.md v0.2.4, demarrer.md 9 parcours).
**Verdict** : VALIDE (10/10).
**Lecons** :
1. Le 9e parcours (promethee) suit exactement le pattern etabli : creation JSON + fiche allegee + sync des 2 listes -- le processus est reproductible
2. Le FLUX MINERVE est la signature du parcours Promethee : la case FIN active Minerve pour le todo (difference avec Minerve qui reactive Cerberus)
3. REGLE PENSE-BETE SOURCE en indice de la case c3
4. Le diff mecanique des noms entre doc et demarrer.md prouve la sync (9 parcours identiques)

## [NOTES] Controle 2026-08-07 -- parcours-promethee (Buffy)

**Controle** : parcours-promethee.json (21 cases, 3 chemins) + fiche promethee.md allegee v0.2.0.
**Verdict** : VALIDE (10/10).
**Lecons** :
1. Le parcours du REDACTEUR de specs est structurellement identique a celui de Minerve MAIS avec le FLUX MINERVE : la case FIN active Minerve pour le todo (pas de reactivation directe Cerberus) -- un meme pattern (2 missions, anti-doublon, convergence) peut porter des flux de delegation differents
2. REGLE PENSE-BETE SOURCE en indice de la case c3 : je ne cree pas de spec sans pense-bete source
3. Rappel ASCII x4 (Pattern 2) proportionnel a l'ecriture de l'agent
4. 12 references d'outils dans les 2 chemins -- tous existent dans le cerveau

## [NOTES] Controle 2026-08-07 -- parcours-minerve + sync listes (Buffy + Vulcain)

**Controle** : parcours-minerve (21 cases) + fiche allegee + synchronisation des listes (guider-parcours.md v0.2.3, demarrer.md 8 parcours).
**Verdict** : VALIDE (10/10).
**Lecons** :
1. Le 8e parcours (minerve) suit exactement le pattern etabli : creation JSON + fiche allegee + sync des 2 listes -- le processus est maintenant reproductible sans surprise
2. Les regles propres de l agent deviennent des indices : PHASE 0 + PHASE 9 (todo-template), ANTI-DOUBLON (rechercher-todos en c2/c11)
3. Le rappel ASCII x4 est proportionnel au volume d ecriture de l agent
4. Le diff mecanique des noms entre doc et demarrer.md prouve la sync (8 parcours identiques)

## [NOTES] Controle 2026-08-07 -- parcours-minerve (Buffy)

**Controle** : parcours-minerve.json (21 cases, 3 chemins) + fiche minerve.md allegee v0.2.0.
**Verdict** : VALIDE (10/10).
**Lecons** :
1. Le parcours de la REDACTRICE de todos couvre 2 missions (creer 9 etapes, completer 7 etapes) avec Pattern 1 : branches creer/completer/autre convergeant vers lecons c9 + retour c10
2. Les regles propres de Minerve sont des indices : PHASE 0 (activation agent adapte) + PHASE 9 (reactiver Cerberus) dans les cases de remplissage et la case FIN -- le todo-template est incarne dans le parcours
3. ANTI-DOUBLON structurel : rechercher-todos est l OUTIL de la premiere case de chaque chemin (c2, c11)
4. Rappel ASCII x4 (Pattern 2) proportionnel au volume d ecriture de l agent (squelette c4, remplissage c5, completer c14, lecons c9)
5. 13 references d outils dans les 2 chemins -- tous existent dans le cerveau

## [NOTES] Controle 2026-08-07 -- parcours-themis + sync listes (Buffy + Vulcain)

**Controle** : parcours-themis (24 cases) + fiche allegee + synchronisation des listes (guider-parcours.md v0.2.2, demarrer.md 7 parcours).
**Verdict** : VALIDE (10/10).
**Lecons** :
1. La synchronisation des listes apres une creation de parcours est DEUXIEME phase de la mission : la creation du JSON est controlee d'abord (controle-parcours-themis), puis la sync des listes est controlee a nouveau (controle-parcours-themis-sync-v022) -- 2 controles pour 1 creation + sync
2. Le diff mecanique des noms (parcours-[a-z]*.json entre doc et demarrer.md) prouve la synchronisation sans lecture -- plus fiable que la lecture
3. Le 7e parcours confirme le pattern : NON-EXECUTION (Themis), Pattern 1 (4 branches convergentes), Pattern 2 (rappel ASCII x2 proportionnel a l'ecriture)
4. Le chemin audit couvre les 10 etapes de la fiche avec 12 references d'outils

## [NOTES] Controle 2026-08-07 -- parcours-themis (Buffy)

**Controle** : parcours-themis.json (24 cases, 4 chemins) + fiche themis.md allegee v0.2.0.
**Verdict** : VALIDE (10/10).
**Lecons** :
1. Le parcours de l EVALUATRICE croisee est un parcours de NON-EXECUTION : les seules ecritures sont le rapport et les lecons -- la REGLE NON-EXECUTION est en indices des cases d evaluation et rappelee dans la case Verdict (c8)
2. Le chemin doute (c14-c17) route vers le choix de l evaluateur adapte au domaine (structure/conventions/coherence/agents) : la specialite CROISEMENT de Themis est guidee case par case
3. Pattern 1 : 4 branches de la case Mission convergent vers les cases communes (rapport c9, lecons c12, retour c13)
4. Rappel ASCII x2 (Pattern 2) dans les cases d ecriture (rapport c9 + lecons c12) -- proportionnel au volume d ecriture de l agent
5. Les 15 outils references du parcours existent tous dans le cerveau (dont les 4 evaluateurs) -- verification croisee des chemins des outils

## [NOTES] Controle 2026-08-07 -- liste des parcours mise a jour (Buffy + Vulcain)

**Controle** : mise a jour de la liste des parcours dans guider-parcours.md (v0.2.1) + demarrer.md (bloc CASE 0).
**Verdict** : VALIDE (6/6).
**Lecons** :
1. La liste des parcours est une SOURCE DE VERITE PARTAGEE entre demarrer.md (case 0) et guider-parcours.md (doc de l'outil) : les noms de parcours (parcours-[a-z]*.json) doivent etre identiques dans les 2 fichiers -- verifiable par diff des noms extraits
2. La mise a jour de liste a mobilise 2 agents : Vulcain (doc de son outil guider-parcours.md) + Buffy (fichier du cerveau demarrer.md) -- la distinction outil/contenu s'applique meme pour une simple liste
3. Bump de version DOC mineur (0.2.1) pour une mise a jour de liste : les CLI restent a 0.1.0-py/-sh -- verifier la distinction version doc vs version outil
4. La synchronisation ne concerne que les 6 parcours reels : les references generiques (parcours-<agent>.json) et les exemples python3 ne sont pas des entree de la liste
5. PIEGE RECURRENT : en documentant une observation sur des guillemets francais, j'ai moi-meme COPIE ces guillemets dans le rapport (controle-liste-parcours-v021) -- toujours re-verifier valider-conformite-ascii sur le rapport APRES l'avoir modifie, pas seulement a la creation (le piege se rejoue a chaque ajout d'observation)

## [NOTES] Controle 2026-08-08 -- spec-combos-moteur + Pattern 3 (Vulcain)

**Controle** : etape 1 du plan combo-orchestrateur -- spec-combos-moteur creee (format definition-combo.json) + Pattern 3 (generateur -> execution) dans spec-guider-parcours v0.2.4 + doc guider-parcours 0.2.10.
**Verdict** : VALIDE (7/7).
**Lecons** :
1. grep interprete --liste comme une option : utiliser grep -cF -e "--liste" pour chercher une chaine qui commence par --
2. Le combo devient l orchestrateur : le generateur INCHANGE est appele par le moteur avec --reponses (mode AUTO) -- c est la source de verite de la syntaxe, le moteur fait le lien
3. Le format definition-combo.json (spec-combos-moteur) est declaratif : objet combo + 4 types de cases (generateur/outil/controle/fin) + variables memoire interne + persistant classeur -- meme philosophie que guider-parcours lit parcours-<agent>.json
4. Le Pattern 3 est documente a 3 endroits de la spec-guider-parcours : section Patterns, procedure d audit point 3, critere d acceptation 11

## [NOTES] Controle 2026-08-08 -- allegement demarrer.md (Buffy)

**Controle** : allegement demarrer.md (porte d entree ~45 lignes) + enrichissement protocole-identification (MODE ID v0.4.0) + index-cerveau.md (v0.3.0) + convention-sous-protocoles.
**Verdict** : VALIDE (8/8).
**Lecons** :
1. Un grep case-sensitive donne un faux negatif sur une phrase en MAJUSCULES (DEUX LLM DIFFERENTS NE PARTAGENT JAMAIS UNE SESSION) : verifier avec -i
2. Un grep dont la chaine contient un backtick (protocole-demarrer-projet) echoue : relire le texte reel avec grep -A avant de conclure
3. L allegement de demarrer.md est coherent : le MODE ID (le contenu vraiment critique au demarrage) a ete absorbe par protocole-identification, pas perdu -- la regle citee par parcours-cerberus c11 (Reactiver Cerberus SANS lire = inutile) est conservee dans la version allegee

## [NOTES] Controle 2026-08-08 -- catalogue generateur 12 commandes (Vulcain)

**Controle** : etape 4 plan combo-orchestrateur -- les 2 combos manquants (combos-valider-cerveau, combos-corriger-non-ascii) declares dans catalogue-commandes.json (10 -> 12 commandes).
**Verdict** : VALIDE (12/12).
**Lecons** :
1. Le catalogue est la SOURCE DE VERITE du generateur : chaque entree = un modele d appel d outil deja ecrit, corrige et valide -- une commande se DECLARE (script + parametres exacts), jamais inventee
2. Format d entree : nom, description, interpreteur, script, modele avec {parametres}, parametres (cle/question/type/obligatoire/defaut/flag/quoter) -- les optionnels portent un defaut (flag -> non, texte -> valeur)
3. LES COMBOS SONT ABSORBES : audit-general + valider-cerveau + corriger-non-ascii dans le catalogue -> le generateur compose la commande de n importe quel combo, c est la porte d entree des cases generateur du combos-moteur (Pattern 3)
4. La validation se fait en 3 temps : --liste (completude), --reponses avec et sans flags (composition exacte), parite py/sh (meme commande composee)

## [NOTES] Controle 2026-08-08 -- combo-activation (Buffy)

**Controle** : combo pilote combo-activation (cycle sidentifier -> activer -> reactiver) cree par Buffy et teste avec combos-moteur.
**Verdict** : VALIDE (12/12).
**Lecons** :
1. Une DEFINITION de combo est un fichier du cerveau -> domaine Buffy (racine cerveau-projet/combos/), le MOTEUR est un outil -> domaine Vulcain -- meme distinction que parcours (Buffy) vs guider-parcours (Vulcain)
2. Le cycle d'activation complet en 8 cases : 3 generateurs (sidentifier/activer/reactiver) + 3 outils d'execution + 1 controle (branches OUI/NON) + 1 fin -- le generateur AUTO compose les commandes exactes avec quoter pour les raisons a espaces
3. Le test sur copies (AGENTS_FILE/AGENTS_HISTORIQUE/CLASSEUR_STOCKAGE vers /tmp/) est OBLIGATOIRE pour un combo qui modifie la session : verifier le retour Cerberus dans la copie, jamais sur les vrais fichiers (le combo activerait/reactiverait la session reelle)
4. Validation en 3 etapes : --liste (structure), --dry-run (commandes sans effet), execution reelle sur copies (cycle complet) -- les vrais fichiers doivent rester intacts

## [NOTES] Controle 2026-08-08 -- combos-moteur (Vulcain)

**Controle** : moteur generique de combos declaratifs combos-moteur (py + sh + md + exemple-combo.json) construit par Vulcain, teste par Morpheus (31/31 REUSSI).
**Verdict** : VALIDE (12/12).
**Lecons** :
1. Le moteur lit une definition-combo.json (objet combo + cases) exactement comme guider-parcours lit un parcours-<agent>.json -- le meme squelette de moteur declaratif JSON
2. 4 types de cases : generateur (appelle generateurs-commande --reponses en mode AUTO, sortie = commande), outil (subprocess, sortie = resultat), controle (branches reponse->vers), fin (message) -- variables en memoire interne + interpolation {var} + persistance optionnelle persistant: true vers classeur-variables
3. PIEGE PARITE CHEMIN : 5 remontees depuis le fichier .py (combos-moteur -> combos -> tools -> agents -> cerveau-projet) mais 4 depuis le dossier .sh (via COMBO_MOTEUR_DIR) -- les deux versions doivent compter les niveaux selon leur base
4. PIEGE EXTRACTION : le generateur imprime la commande sur la ligne SUIVANTE le marqueur === COMMANDE A LANCER === -- prendre la premiere ligne non vide apres le marqueur
5. Le generateur-commande reste INCHANGE : le moteur fait le lien avec --reponses -- c'est la source de verite de la syntaxe, il devient incontournable comme composeur des cases generatrices
6. Le test formel 31/31 couvre : --liste, navigation case_depart->fin, interpolation, generateur AUTO, controle branches OUI/NON, variable manquante code 1, dry-run, parite py/sh, nommage, ASCII, syntaxe

## [NOTES] Controle 2026-08-08 -- Generalisation du Pattern 3 (Buffy)

**Controle** : etape 6 plan combo-orchestrateur -- 4 combos crees + 3 parcours modifies (janus, vulcain, buffy) pour generaliser le Pattern 3.
**Verdict** : VALIDE (12/12).
**Lecons** :
1. La generalisation du Pattern 3 touche les SUITES LINEAIRES d'outils : janus (2 combos : controle-outil 4 cases, controle-modification 10 cases), vulcain (combo-corriger-ascii 4 cases, x2 c7/c13), buffy (combo-sante-tableaux 6 cases) -- les parcours non transformables (cerberus retour = arbre de decision, morpheus tester = protections dans le test) restent en l'etat
2. Chaque combo utilise les DEFANTS DU CERVEAU (cerveau-projet, cerveau-projet/agents) comme cibles stables ; les outils strictement contextuels (valider-ebauche spec, verifier-role-fichier fichier modifie) restent des INDICES de la case combo -- la case garde la regle Pattern 3 en tete + combos-moteur + definition
3. Le generateur AUTO compose 3 nouvelles commandes du catalogue (valider-nommage-recursif, combos-valider-cerveau, corriger-accents) en plus d'audit-general -- le catalogue 12 commandes couvre les combos
4. PIEGE COMPTAGE CHEMINS : janus 4 + vulcain 2 + buffy 6 = 12 chemins (pas 13) -- compter les branches de la case Mission de CHAQUE parcours
5. PIEGE GREP ASCII : 'grep -c non-ASCII' compte la ligne de rapport 'Caracteres non-ASCII : 0' comme un match -- verifier la sortie reelle ([OK] Conformite ASCII stricte validee) au lieu du compteur
6. Validation : json.load 7 fichiers + dry-run 4 combos + guider-parcours 12 chemins + ASCII 0 + parite py/sh 4/4 + zero ref morte -- meme grille que l'etape 5, elargie a 3 parcours

## [NOTES] Controle 2026-08-08 -- Pattern 3 parcours-themis + combo-audit-themis (Buffy)

**Controle** : etape 5 plan combo-orchestrateur -- integration du Pattern 3 (spec v0.2.4) dans parcours-themis v0.2.0 + creation du combo pilote combo-audit-themis.
**Verdict** : VALIDE (12/12).
**Lecons** :
1. Le Pattern 3 est operationnel : une case de parcours pointe vers un COMBO (combos-moteur + definition-combo.json) au lieu d'une suite d'outils -- parcours themis 24 -> 17 cases, chemin audit c2 -> c3 combo -> c8 verdict
2. Quand on supprime des cases (c4-c7), verifier les refs vers ET suivant : c19 (RVAV) pointait vers c4 et a ete recable vers c3 -- grep 'vers' ET 'suivant' vers les cases supprimees
3. Le combo audit-themis mixe generateurs AUTO (audit-general, combos-valider-cerveau via catalogue) + outils directs (valider-relecture, valider-tableaux, detecteurs) -- 9 cases
4. valider-nommage --type outil ne s'applique PAS aux definitions-combo.json (JSON, pas des outils) -- valider par json.load + valider-conformite-ascii + combos-moteur --liste + --dry-run
5. Parite py/sh du moteur conservee sur la nouvelle definition (PARITE OK) ; moteur + catalogue + generateur INCHANGES (verification par dates de modification)

## [NOTES] Controle 2026-08-07 -- generateurs-commande (Vulcain)

**Controle** : outil generateurs-commande (py+sh+json+md+spec) cree par Vulcain.
**Verdict** : VALIDE.
**Lecons** :
1. La parite py/sh doit etre verifiee sur TOUTES les commandes du catalogue, pas une seule (5 tests effectues : activer-activer, audit-general avec flag, corriger-accents avec flag, remplir-pense-bete, valider-nommage-recursif avec flag --recursive)
2. La gestion des erreurs (commande inconnue, parametre obligatoire manquant) doit etre testee pour les deux versions -- identique
3. valider-conventions signale des avertissements cosmetiques (frontmatter YAML absent, lignes > 120) mais valide OK -- ne pas bloquer pour ces avertissements
4. detecter-surcharge-fichier analyse le dossier mais peut manquer des fichiers au-dessus du seuil -- verifier manuellement la taille des fichiers (generateurs-commande.py = 381 lignes, acceptable pour une logique CLI complexe)
5. valider-ebauche ne s'applique qu'aux ebauchers de spec (statut: ebauche en frontmatter), pas a la documentation .md d'un outil complet
6. valider-nommage exige --type outil pour valider un fichier specifique, ou --recursive pour un dossier
7. detecter-usage-outils-externes (levier B) confirme 0 trace d'outil externe (CRLF, non-ASCII, BOM) sur les 4 fichiers
8. lister-outils affiche 78 (exclut combos/ et tester/ par conception), index-tools.md compte 79 avec combos -- les deux sont synchronises
9. Le catalogue JSON doit etre valide et complet -- 10 commandes, toutes testables en mode --reponses
10. Outils utilises : sidentifier, lire-fichier, lister-fichiers, valider-conformite-ascii, valider-nommage, valider-ebauche, valider-conventions, valider-liens, valider-tableaux, verifier-role-fichier, verifier-separation-preoccupations, detecter-surcharge-fichier, detecter-usage-outils-externes, lister-outils, rechercher-texte, combos-valider-cerveau

## [NOTES] Controle 2026-08-07 -- activer-agent-principal v0.4.0 (Vulcain)

**Controle** : evolution majeure v0.4.0 -- REGLE ALIGNEMENT (id llm-N -> session-llm-N), champ Id LLM dans les blocs AGENTS.md (source double), conflit gere, absorption session orpheline, demarrer.md revu, migration donnees.
**Verdict** : VALIDE (10/10 points).
**Lecons** :
1. detecter-usage-outils-externes detecte les guillemets francais doubles (caracteres U+00AB/U+00BB) que valider-conformite-ascii ne signale PAS -- les deux outils ont des logiques differentes, il faut TOUJOURS lancer les deux en controle
2. La regression en boucle sur 6 tests depasse 30s -- prevoir un timeout >= 150s pour la regression complete d'activer-agent-principal
3. test-001 et test-002 n'affichent pas de ligne VERDICT mais leur rapport Total/Reussis/Echecs est lisible -- verifier les 3 lignes du rapport, pas seulement VERDICT
4. La migration a bien ete executee : aucun doublon session-llm-2, la session est alignee sur l'id (session-llm-1 = llm-1)
5. La preuve en production : lors de MON activation (activer janus) avec le code v0.4.0, la liaison id: llm-1 a ete preservee et alignee sur session-llm-16. valider-conformite-ascii ne prend qu'UN fichier par appel : quand plusieurs fichiers sont passes en argument, seul le dernier (ou un seul) est analyse. Toujours lancer l'outil fichier par fichier, et croiser avec detecter-usage-outils-externes qui est plus strict (a signale les guillemets francais avant valider-conformite-ascii dans le cas du controle demarrer.md).
17. Les caracteres typographiques francais (guillemets doubles non-ASCII) sont des pieges ASCII : ils passent dans une phrase anodine (ex: une citation d'id) et cassent la regle immuable. Dans un rapport de controle, les chercher explicitement avec grep '[^ -~\t]'.
18. MEME PIEGE POUR MOI-MEME : en redigeant le rapport et les lecons, j'ai moi-meme copie ces guillemets non-ASCII (2 dans corrections.md, 6 dans le rapport). Corrige immediatement avant de valider -- le controleur doit donner l'exemple.
18. Verdict NON CONFORME sur 1 point (ASCII demarrer.md ligne 13) ne doit pas bloquer la validation du reste (9/10 valides) : documenter la correction a faire et renvoyer le verdict a Cerberus pour reactiver l'agent auteur. La regle d'alignement ne concerne que les ids numeriques (llm-N) : les ids libres (llm-atlas, llm-athena...) continuent de prendre la prochaine session libre -- les tests 001-005 restent donc valides sans modification

## [NOTES] Controle 2026-08-07 -- guider-parcours v0.1.0 (Vulcain)

**Controle** : outil guider-parcours (jeu de piste anti-oubli) + parcours-vulcain.json prototype + fiche vulcain allegee.
**Verdict** : VALIDE (10/10 points).
**Lecons** :
1. Le concept du jeu de piste est operationnel : navigation c1->c9 avec indices (outil/fichier/regle) au bon moment, une case a la fois -- reponse directe au probleme des fiches 200+ lignes
2. Le cycle MORPHEUS -> VULCAIN a fonctionne : 2 bugs detectes par les tests puis corriges par l'auteur AVANT ce controle (le second controle valide, il ne corrige pas)
3. verifier_nommage du .sh exige le prefixe de la CATEGORIE (guider-) tandis que le .py verifie le dossier de l'outil -- a verifier a chaque creation d'outil dans une categorie multi-mots
4. Un .sh avec python embarque par heredoc DOIT transmettre les arguments : python3 - "$@" << 'PYEOF' sinon le python ignore la ligne de commande
5. detecter-usage-outils-externes ne prend qu'UNE cible a la fois (pas plusieurs fichiers en arguments) -- lancer --recursive sur un dossier ou une cible seule
6. Le parcours est la source de verite : la fiche vulcain ne contient plus AUCUNE mission detaillee (0 occurrence 'Mission :') -- le guidage vit dans le JSON

## [NOTES] Controle 2026-08-07 -- parcours Morpheus + Clio (Buffy)

**Controle** : parcours-morpheus.json (17 cases) + parcours-clio.json (16 cases) + fiches allegees (v0.2.0).
**Verdict** : VALIDE (10/10 points).
**Lecons** :
1. Le pattern du jeu de piste est GENERALISABLE : les parcours Morpheus et Clio suivent exactement la structure validee sur Vulcain (5 modeles de cases + branches) -- creation reproductible pour tout nouvel agent
2. Le parcours Morpheus integre la REGLE DELEGATION (Vulcain -> Morpheus -> Vulcain) comme une QUESTION avec branches (VULCAIN/CERBERUS) -- une decision de routage est une case de type question
3. Le parcours Clio integre la lecon operationnelle de Clio (--maj ne cree pas une categorie absente du README) directement dans une case (c7 -> c8) -- les lecons des corrections peuvent devenir des cases du parcours
4. Fiches allegees : 0 mission detaillee restante dans morpheus.md et clio.md -- le guidage vit entierement dans le JSON, la fiche garde identite/regles/connexions
5. Assignation correcte : les parcours et fiches sont des FICHIERS DU CERVEAU -> Buffy (developpeur principal). Vulcain ne construit que les OUTILS dans tools/ (guider-parcours etait sa mission, les parcours JSON ne le sont pas)
6. La validation d'un parcours = --liste (charge + valide la structure) + --reponses (parcourt les branches reelles) -- les 2 sont suffisants pour un parcours de donnees (pas besoin du cycle complet de tests d'outil)

## [NOTES] Controle 2026-08-07 -- parcours Athena + synchronisation listes (Buffy + Vulcain)

**Controle** : parcours-athena.json (21 cases, 3 chemins) + fiche athena.md allegee (v0.2.0) + synchronisation des listes (guider-parcours.md v0.2.5 + demarrer.md 10 parcours).
**Verdict** : VALIDE (10/10 points).
**Lecons** :
1. Le 10e parcours (athena) confirme le pattern de synchronisation : la creation d'un parcours declenche la maj des 2 listes (demarrer.md + guider-parcours.md) -- le diff mecanique des noms parcours-[a-z]*.json est identique entre les 2 fichiers
2. Le parcours d'Athena porte la CHAIN PROMETHEE (activer Promethee pour la spec en fin de mission) -- le flux Athena -> Promethee -> Minerve est incarne dans la structure
3. Les 10 parcours sur 10 agents avec fiches allegees : il ne reste que Atlas (explorateur) -- sa fiche n'a pas encore de parcours

## [NOTES] Controle 2026-08-08 -- fiche vulcain spec v0.2.3 + cas assume (Buffy)

**Controle** : mise a jour de la fiche vulcain.md (reference spec v0.2.3 + entree d'historique decision cas assume).
**Verdict** : VALIDE (5/5).
**Lecons** :
1. Quand une decision est documentee (spec + rapport), la fiche de l'agent concerne doit la porter aussi : reference spec a jour + entree d'historique -- la coherence documentaire se verifie en croisant fiche et spec (meme message CAS LEGITIME ASSUME + regle 8)
2. La version de fiche propre (vulcain 0.4.0) reste inchangee : on ajoute une entree d'historique, on ne rebumpe pas
3. Le controleur verifie la version conservee (pas de rebump) ET la coherence du message avec la spec

## [NOTES] Controle 2026-08-08 -- prototype vulcain cas legitime assume (Vulcain + Themis)

**Controle** : documentation du prototype vulcain comme CAS LEGITIME ASSUME (fins independantes par chemin) dans la spec v0.2.3 + doc v0.2.9 + rapport Themis (decision utilisateur).
**Verdict** : VALIDE (5/5).
**Lecons** :
1. Une observation d'audit peut devenir un CAS ASSUME par decision utilisateur : la spec (v0.2.3) et le rapport Themis sont mis a jour de facon SYNCHRONISEE (meme message : fins independantes assumees, compatibles regle 8)
2. Les fins independantes par chemin (construire c9, modifier c15, autre c18/c19) sont un choix documente, pas un defaut -- la recommandation 2 du rapport passe de a corriger a AUCUNE CORRECTION NECESSAIRE
3. La coherence spec/rapport se verifie par le message commun : le controleur croise les 2 documents pour confirmer qu'ils racontent la meme histoire
4. Version spec 0.2.3 + doc 0.2.9 -- CLI inchangees

## [NOTES] Controle 2026-08-08 -- spec-guider-parcours v0.2.2 (regle d'autonomie, Vulcain)

**Controle** : ajout de la regle 8 AUTONOMIE des parcours dans la spec (v0.2.1 -> v0.2.2) + doc guider-parcours.md (0.2.7 -> 0.2.8).
**Verdict** : VALIDE (5/5).
**Lecons** :
1. La regle d'autonomie repond a la crainte utilisateur (melange des parcours) : chaque parcours est un fichier INDIVIDUEL, la convergence est uniquement INTRA-parcours (factorisation interne), aucun partage de cases entre parcours
2. La regle documente une realite deja vraie : 0 reference croisee entre les 11 parcours -- verifiee par scan regex (parcours-[a-z]*.json hors son propre nom)
3. La convergence du Pattern 1 et l'autonomie de la regle 8 sont COMPLEMENTAIRES, pas contradictoires : on factorise INTERNE, on ne partage JAMAIS entre parcours
4. La doc porte la regle 7 AUTONOMIE (en coherence avec la regle 8 de la spec) et la procedure d'audit a sa sous-section Autonomie
5. Version spec 0.2.2 + doc 0.2.8, CLI inchangees

## [NOTES] Controle 2026-08-08 -- spec-guider-parcours v0.2.1 (procedure d'audit, Vulcain)

**Controle** : documentation de la procedure d'audit des 2 patterns dans la spec (v0.2.0 -> v0.2.1) + doc guider-parcours.md (0.2.6 -> 0.2.7).
**Verdict** : VALIDE (5/5).
**Lecons** :
1. La capitalisation d'une procedure validee par un audit (Themis) dans la spec de l'outil rend l'audit REPRODUCTIBLE : la section Procedure d'audit documente Pattern 1 (case Mission + convergence), Pattern 2 (verification structurelle position 1 = regle ASCII), cas particuliers legitimes (routage, prototype) et la revalidation complete
2. La verification par grep seul ('REGLE IMMUABLE ASCII' present) ne suffit pas : la REGLE doit etre en POSITION 1 des indices -- la procedure documente la verification structurelle (position 1) qui a detecte les 2 ecarts minerve c8 / promethee c8
3. La spec est TRIPLEMENT coherente : regles du format (6-7) = patterns documentes = criteres d'acceptation (9-10) = procedure d'audit -- le controleur croise ces 4 endroits
4. Distinction version : spec 0.2.1 + doc 0.2.7 mais CLI toujours 0.1.0-py/-sh -- une mise a jour de documentation ne change pas l'outil

## [NOTES] Controle 2026-08-08 -- generateurs-carte v0.2.0 (squelette Pattern 10 + Pattern 3, Vulcain)

**Controle** : generateurs-carte.py v0.2.0 (squelette creer enrichi par Vulcain, chaine bout-en-bout -- VERDICT Morpheus VALIDE 8/8 au prealable).
**Verdict** : CONFORME (8/8).
**Lecons** :
1. CONFORMITE DU CODE : squelette_carte() ligne 160 -- indice Pattern 10 (UNE CARTE = UN ROLE, texte avec % agent) en tete des indices de c1 (ligne 231), indice Pattern 3 (RAPPEL DES COMBOS) en POSITION 1 des indices de c2 (ligne 245, avant Pattern 7 et ASCII) -- les 2 patterns de la mission sont bien integres
2. VERSION + DOC : VERSION = 0.2.0 dans le py (ligne 29) ET dans la doc .md (ligne 11), versionning 0.2.0 ajoute avec la ligne de changements complete (Pattern 10 + Pattern 3 + spec v0.2.19)
3. REGLES TRANSVERSES : ASCII 0 sur py + md, valider-nommage code 0, parite py/sh (wrapper pur = parite par construction), spec-guider-parcours v0.2.19 reference (14 occurrences de v0.2.19/Pattern 11)
4. LE SQUELETTE SUIT LA SPEC : quand la spec passe a 11 patterns (v0.2.19), le squelette de creation doit les integrer -- sinon toute carte nee apres cette date nait sans les nouveaux patterns (lecon : un squelette obsolete fabrique des cartes obsoletes, comme un template obsolete fabrique des fiches obsoletes)
5. NETTOYAGE : les dossiers de test .tmp-gc-test/ et .tmp-morpheus-test/ (auto-commites par erreur dans le passe) ont ete retires du suivi git -- les dechets de test ne doivent pas etre suivis
6. LA CHAINE S ARRETE ICI (Pattern 8) : Janus est le dernier maillon, il REACTIVE Cerberus avec le bilan consolide (modification Vulcain + tests Morpheus + controle Janus)

## [NOTES] Controle 2026-08-08 -- correction Pattern 2 minerve c8 + promethee c8 (Buffy)

**Controle** : correction des 2 ecarts Pattern 2 detectes par l audit Themis (rappel ASCII en tete des indices des cases de mise a jour d index).
**Verdict** : VALIDE (5/5).
**Lecons** :
1. Le cycle audit -> correction -> controle fonctionne : Themis a signale les 2 ecarts (minerve c8, promethee c8), Buffy a corrige, le second controle confirme la conformite
2. La correction est minimale et exacte : indice regle ASCII insere en position 1, REGLE INDEX conservee en position 2 -- rien d'autre n a change (navigation identique, 4 chemins TERMINE)
3. Le Pattern 2 s applique a TOUTE case avec outil d ecriture y compris les mises a jour d index (editer-fichier) -- pas seulement les creations
4. La verification structurelle (position 1 = regle ASCII, position 2 = REGLE INDEX) est plus fiable qu une simple recherche de texte

## [NOTES] Controle 2026-08-07 -- parcours-atlas + sync listes (Buffy + Vulcain)

**Controle** : parcours-atlas (29 cases) + fiche allegee + synchronisation des listes (guider-parcours.md v0.2.6, demarrer.md 11 parcours).
**Verdict** : VALIDE (10/10 + 5/5).
**Lecons** :
1. Le 11e parcours termine la serie : le pattern de synchronisation est roder (2 controles par creation + sync, diff mecanique des noms)
2. Atlas porte le Pattern 1 a son maximum : 5 branches de mission (explorer, web, documenter, analyser, autre) car la fiche a 4 missions -- un parcours couvre autant de missions qu'en porte l'agent
3. REGLE VALIDER AVANT DE MODIFIER x5 : signature d'Atlas en indices des cases d'ecriture
4. Atlas ne delegue pas : la case FIN c11 REACTIVE CERBERUS (contrairement a Athena CHAIN ou Promethee FLUX)
5. La mission web s'incarne par un indice FICHIER (protocole-recherches-web) car elle n'a pas d'outil dedie
6. La serie des 11 parcours / 11 agents est COMPLETE

## [NOTES] Controle 2026-08-07 -- parcours-atlas (Buffy)

**Controle** : parcours-atlas.json (29 cases, 5 branches de mission) + fiche atlas.md allegee v0.2.0.
**Verdict** : VALIDE (10/10).
**Lecons** :
1. Le 11e et dernier parcours porte le PATTERN 1 a son maximum : la case Mission a 5 branches (explorer, web, documenter, analyser, autre) car la fiche Atlas porte 4 missions -- un parcours peut couvrir autant de missions qu'en porte l'agent
2. La REGLE VALIDER AVANT DE MODIFIER est la signature d'Atlas : x5 en indices des cases d'ecriture (c9, c14, c18, c19, c25) -- les regles de l'agent deviennent des indices, pas des sections
3. Atlas ne delegue pas : la case FIN c11 REACTIVE CERBERUS -- contrairement a Athena (CHAIN) ou Promethee (FLUX) ; chaque agent a son mode de retour incarne dans la structure
4. La mission web utilise un indice FICHIER (protocole-recherches-web) car elle n'a pas d'outil dedie -- les missions a protocole s'incarnent par des indices fichier
5. Rappel ASCII x6 (Pattern 2) : 5 cases d'ecriture + lecons -- proportionnel au volume d'ecriture de l'agent (Atlas documente beaucoup)
6. La serie est COMPLETE : 11 parcours / 11 agents -- le processus (creation JSON -> fiche allegee -> controle -> README -> sync listes -> controle) est roder

## [RAPPORT] Controle 2026-08-09 -- detecter-impacts sur generateurs-commande.sh (mission Vulcain)

**Objet** : verifier avec detecter-impacts que la modification de generateurs-commande.sh (VERSION 0.1.0-beta -> 0.2.0, mission Vulcain 08:18) n'a pas d'impact oublie (catalogue, index-tools, spec).

**Outils utilises** : detecter-impacts v0.2.1 (sur .py et .sh), lecture directe des 5 fichiers du dossier + grep cible. Lire le .md avant usage : OK (schema hybride v0.2.0 : frontmatter .md, commentaires .py/.sh, cle top-level .json).

**VERDICT : NON VALIDE -- 1 impact reel oublie (la spec).**

### Resultats par cible

| Fichier | Version referencee | Verdict |
|---|---|---|
| generateurs-commande.py | 0.2.0 | OK (a jour) |
| generateurs-commande.sh | 0.2.0 | OK (a jour, corrige par Vulcain) |
| generateurs-commande.md | 0.2.0 | OK (a jour) |
| catalogue-commandes.json | 0.1.0-beta (ligne 2) | NON IMPACTE : c'est la version du CATALOGUE lui-meme (fichier de donnees), pas celle de l'outil. Les 2 autres occurrences (lignes 1709, 2070) sont des descriptions d'autres outils (v0.2.0 de detecter-impacts / valider-cartes-decision). |
| index-tools.md | v0.2.0 (ligne 9) + ligne 200 | NON IMPACTE : ligne 9 = version de l'INDEX lui-meme, ligne 200 = description migrer-identite. La ligne 151 (generateurs-commande) ne reference AUCUNE version. |
| **spec/spec-generateurs-commande.001.01.ebauche.md** | **0.1.0-beta (ligne 10)** | **IMPACT REEL OUBLIE : la spec doit passer a 0.2.0.** |

### Lecture des marquages detecter-impacts (croisement)

detecter-impacts marque ~50 fichiers impliques, dont beaucoup [NON MIS A JOUR] pour le .sh. Analyse : ce sont des ARTEFACTS TEMPORELS -- le .sh vient d'etre modifie (08:18) donc tous les fichiers qui le citent sont plus anciens. La plupart citent le NOM de l'outil (parcours des agents, case passe par le generateur, corrections, controles) et PAS sa version : une modification de version ne les impacte PAS. Seule la spec reference la VERSION (ligne 10) : impact reel.

### Lecons (Janus)

1. detecter-impacts signale les fichiers qui citent le fichier modifie, mais TOUS les [NON MIS A JOUR] ne sont pas des impacts reels : il faut CROISER avec la nature de la modification (ici : changement de version -> seuls les fichiers qui referencent la VERSION sont impactes, pas ceux qui citent le nom).
2. Les artefacts temporels (fichier modifie plus recent que les fichiers qui le citent) generent des [NON MIS A JOUR] massifs : verifier le CONTENU de la reference (nom vs version) avant de conclure.
3. Le dossier d'un outil contient 5 fichiers coherents (py, sh, md, json, spec) : apres toute modification de version, verifier les 5 (py, sh, md, spec) -- le catalogue a SA propre version.

### Action recommandee (domaine Vulcain)

Corriger spec/spec-generateurs-commande.001.01.ebauche.md ligne 10 : **Version : 0.1.0-beta -> 0.2.0** (alignement sur py/sh/md).

## [RAPPORT] Controle 2026-08-09 -- SCAN GENERALISE regle des 5 fichiers : divergences spec vs py

**Objet** : generaliser la regle des 5 fichiers (lecon Vulcain) en scannant les 12 dossiers outils avec spec/ pour detecter les spec dont la version diverge de leur .py.

**VERDICT : 11 spec scannees | 5 ALIGNEES | 6 DIVERGENTES** (a corriger par Vulcain - controle seul, aucune correction effectuee).

### Methode

Pour CHAQUE spec : extraction de la version (3 formats d'en-tete + tableaux d'historique) CROISEE avec la version VERSION= du .py associe. Lecture manuelle des formats reels (lecon Janus : ne pas conclure sur un grep seul - les spec ont des formats varies : en-tete **Version :** X, tableau frontmatter | **Version** | X |, section Versionning, ou tableau historique Date|Version|Auteur pour les spec prepare sans version d'en-tete).

### Tableau des 11 spec

| Outil | V. spec (source) | V. py | Verdict |
|---|---|---|---|
| activer-agent-principal | 0.5.0 (historique) | 0.5.0 | ALIGNE |
| combos-moteur | 0.2.0-ebauche (en-tete) | 0.2.0-beta | DIVERGENT (suffixe incoherent) |
| generateurs-commande | 0.2.0 (en-tete) | 0.2.0 | ALIGNE |
| generateurs-regenerer-catalogue | 0.1.0 (en-tete) | 1.0.0 | DIVERGENT (gros ecart) |
| guider-parcours | 0.2.20 (en-tete) | 0.3.1 | DIVERGENT (cas particulier : spec versionne les PATTERNS v0.2.x, distinct de l outil) |
| lister-agents | 0.2.0 (historique) | 0.4.0-py | DIVERGENT |
| lister-outils | 0.2.0 (historique) | 0.3.0-py | DIVERGENT |
| migrer-identite | 0.2.2 (en-tete) | 0.2.2 | ALIGNE |
| remplacer-texte | 0.1.0-beta (en-tete) | 0.1.0-beta | ALIGNE |
| verifier-restauration-sure | 0.1.0 (versionning) | 0.1.0 | ALIGNE |
| verifier-systeme | 0.2.0 (historique) | 0.2.1-py | DIVERGENT (mineur) |

### Detail des 6 divergences (a traiter par Vulcain)

1. **generateurs-regenerer-catalogue** : spec 0.1.0 vs py 1.0.0 - ecart majeur (l outil cree en 1.0.0, spec jamais montee). ALIGNER spec -> 1.0.0.
2. **guider-parcours** : spec 0.2.20 vs py 0.3.1 - CAS PARTICULIER : la spec-guider-parcours versionne les PATTERNS (v0.2.0 a v0.2.20) distincts de la version de l outil guider-parcours.py (0.3.1). Decision a prendre : documenter comme cas legitime (spec = spec de reference des parcours, pas de l outil) ou aligner. A NE PAS aligner sans decision.
3. **lister-agents** : spec 0.2.0 vs py 0.4.0-py - spec jamais montee depuis la refonte Promethee (0.2.0). ALIGNER spec -> 0.4.0-py.
4. **lister-outils** : spec 0.2.0 vs py 0.3.0-py - idem. ALIGNER spec -> 0.3.0-py.
5. **verifier-systeme** : spec 0.2.0 vs py 0.2.1-py - divergence mineure (refonte Promethee 0.2.0, py passe a 0.2.1-py). ALIGNER spec -> 0.2.1-py.
6. **combos-moteur** : spec 0.2.0-ebauche vs py 0.2.0-beta - SUFFIXE incoherent (ebauche vs beta pour la meme base 0.2.0). Decider du suffixe canonique puis aligner.

### Lecons (Janus)

1. Les spec ont des FORMATS DE VERSION VARIES (en-tete, tableau frontmatter, versionning, tableau historique) : un scan automatique doit gerer tous les formats ET croiser manuellement - mon 1er script a pris la mauvaise version (0.1.2 au lieu de 0.2.2 pour migrer-identite : la version d EN-TETE prime sur le tableau d historique).
2. La regle des 5 fichiers se GENERALISE : 6 spec sur 11 divergent - l incident generateurs-commande n etait pas isole, il etait representatif.
3. CAS PARTICULIER guider-parcours : la spec de reference des parcours versionne les patterns, pas l outil - a documenter comme cas legitime avant tout alignement.
4. Distinguer : divergence de BASE (ecart majeur, ex: 0.1.0 vs 1.0.0) vs divergence de SUFFIXE (meme base, suffixe incoherent, ex: -ebauche vs -beta).

### Action recommandee (domaine Vulcain)

Corriger les 5 divergences de base/suffixe (regenerer-catalogue, lister-agents, lister-outils, verifier-systeme, combos-moteur) ; prendre une DECISION documentee pour guider-parcours (cas particulier patterns) ; NE PAS toucher aux 5 ALIGNEES.
## [NOTES] Controle 2026-08-09 -- combo tester-outil v0.1.0 + test-004 (Verdict VALIDE)

**Controle** : second controle croise du combo tester-outil (Buffy) + test-004 (Morpheus).
**Verdict** : VALIDE.
**Lecons** :
1. La chaine complete fonctionne : audit (Themis) -> creation (Buffy) -> test formel (Morpheus 16/16) -> second controle (Janus VALIDE) - le circuit de controle est operationnel de bout en bout
2. Conformite Pattern 3 verifiee : suite lineaire d outils encapsulee dans un combo (c1 generateur -> c2 outil -> c3 controle -> c4 outil -> fin), branchee dans le parcours (case Lancer le combo X avec indice outil combos-moteur), indexee dans index-tools.md (16e combo)
3. La REGLE ABSOLUE (jamais de test sans protections) est PRESERVEE dans un combo par un controle intermediaire (c3 : protections ajoutees ? NON -> fin PROTECTIONS MANQUANTES) - un combo ne contourne jamais une regle immuable, il l'encapsule
4. Le test formel 004 (16 points) couvre : structure, --liste, interpolation (2 variables manquantes), navigation OUI (fichier cree + test execute), navigation NON (protections manquantes), integration parcours (guider-parcours + valider-cartes), ASCII, regression
5. Bruits preexistants documentes (non bloquants) : valider-nommage 2 ERREUR sur definition-combo.json (identique aux 15 combos) et sur test-004 (identique aux 3 tests existants) - formats speciaux hors perimetre de l outil
6. Un second controle independant doit REFAIRE les validations lui-meme (navigation reelle, ASCII, execution du test) - ne pas se fier au rapport precedent, verifier soi-meme (REGLE ABSOLUE : je verifie, je ne suppose pas)

**Validation finale** : rapport janus/controles/controle-combo-tester-outil-2026-08-09.md, verdict VALIDE, ASCII 0.
## [LECON] 2026-08-09 -- SECOND CONTROLE PILOTE ATLAS (generateur v0.2.1 + parcours v0.1.2 + test-005)

**Controle** : verification croisee du modele pilote de generalisation du generateur.
**Verdict** : VALIDE (aucun ecart, 34/34 verifications).

**Lecons** :
1. Le second controle REFAT les validations (je verifie je ne suppose pas) : version py+sh, py_compile, bash -n, composition flags py ET sh, catalogue, navigation 6 chemins, valider-cartes, execution reelle, test-005 reexecute 26/26
2. Le cercle complet est operationnel pour ce modele : Diagnostic (Buffy) -> Pilote + correction bug (Buffy) -> Test formel 26/26 (Morpheus) -> Second controle VALIDE (Janus)
3. La parite py/sh du generateur est stricte : les 4 cas flags (vides, booleens oui/non) donnent des commandes IDENTIQUES py et sh
4. Le modele strict est REPRODUCTIBLE : parcours Atlas 0 commande en dur, navigation PARCOURS TERMINE sur les 6 chemins, CONFORME
5. La spec est alignee (detecter-divergences-version : 0 divergence generateurs-commande) - regle des 5 fichiers respectee par Buffy
6. GENERALISATION PRETE : ce rapport est la reference pour traiter les 10 autres parcours (morpheus, demarrage, cerberus, janus, buffy, athena, minerve, promethee, themis, clio) - chaque parcours conserve son autonomie (regle v0.2.2)
## [NOTES] Controle 2026-08-09 -- cartographier-parcours v0.1.0 + test-006 (Verdict VALIDE)

**Controle** : second controle croise de l outil cartographier-parcours (Vulcain) + test-006 (Morpheus 19/19).
**Verdict** : VALIDE.
**Lecons** :
1. La chaine complete fonctionne pour un NOUVEL OUTIL : creation (Vulcain) -> test formel (Morpheus 19/19) -> second controle (Janus VALIDE) - le circuit de controle est operationnel de bout en bout, la chaine bout-en-bout (Pattern 8) ne retombe jamais sur Cerberus au milieu.
2. C1 outils : ASCII 0 sur les 4 fichiers (py/sh/md/spec), version v0.1.0 coherente py/sh (parite wrapper pur).
3. C2 catalogue : JSON valide, 108 commandes triees alphabetiquement, entree cartographier-parcours avec modele {parcours} {sortie} {dry-run} {verbose} - le generateur compose la commande exacte.
4. C3 index-tools : categorie Cartographier presente (3 occurrences : section + stats + total), total 106 -> 107 coherent avec les compteurs.
5. C4 test-006 : present, ASCII 0, nommage test-XXX-*.py reconnu par valider-nommage (0 erreur) - le format special des tests est bien gere.
6. L outil cartographier-parcours est un bon exemple de RENDU DERIVE : il lit un parcours JSON et produit un fichier markdown (arbre ASCII + chemins + impasses) sans jamais modifier la source - la frontiere lecture/ecriture est respectee (Pattern 14 esprit : l impact cree est le fichier de sortie, jamais le parcours).
## [LECON] 2026-08-09 -- CONTROLE CROISE MISSION 1 FIGER LF : VERDICT VALIDE

**Controle** : mission 1 du plan FIGER LF (Vulcain : outil corriger-fins-de-ligne + 11 outils d'ecriture corriges ; Morpheus : test-007 15/15).
**Verdict** : VALIDE. 7/7 points conformes.

**Points controles** :
1. Outils (py/sh/md/spec) : ASCII 0 x4, version v0.1.0 coherente, nommage OK
2. Catalogue : JSON valide, 109 commandes triees, version 0.2.3, entree corriger-fins-de-ligne presente
3. index-tools : total 108, categorie Corriger 6, entree presente
4. 11 outils d'ecriture : newline present + write_text absent (11/11)
5. test-007 : ASCII 0, nommage reconnu
6. detecter-usage-outils-externes : les NOUVEAUX fichiers (corriger-fins-de-ligne, test-007) = LF pur 0 suspect ; les sources PREEXISTANTES (ex: creer-fichier.py) restent en CRLF - comportement ATTENDU, migration massive = mission 2
7. Lecons Vulcain + Morpheus presentes (FIGER LF)

**Lecons** :
1. UNE MISSION EN 2 TEMPS (corriger la logique PUIS migrer les fichiers) : apres la correction des outils d'ecriture, les fichiers sources preexistants restent en CRLF jusqu'a la migration - ce n'est PAS une infraction, c'est l'ordre prevu. Le controleur doit verifier la LOGIQUE (newline present, write_text absent) et les NOUVEAUX fichiers (LF), pas exiger la migration immediate.
2. VERIFIER LA PRESENCE newline + l ABSENCE write_text ensemble : c'est le couple qui prouve la correction (newline seul peut etre un reste, write_text seul = bug non corrige).
3. detecter-usage-outils-externes prend UNE cible (pas plusieurs) - le scanner recursif est plus pertinent pour un lot.
4. Les fichiers sources des outils sont eux-memes en CRLF (heritage Windows) : la migration (mission 2 Buffy) les normalisera en LF avec l outil corriger-fins-de-ligne.
## [NOTES] Controle 2026-08-09 -- generateurs-amelioration + test-008 (reparation de conformite)

**Controle** : outil generateurs-amelioration v1.0.0 + test formel test-008 (Morpheus 19/19),
dans le cadre de la reparation de conformite (la carte de Vulcain n avait pas ete executee :
etape Morpheus sautee puis reparnee, second controle Janus requis - LISTE DEFINIE).

**Verdict** : VALIDE.

**Controles croises (refaits independamment, 15 points)** :
1. Parite py/sh --version et interrogation --reponses identiques
2. Recapitulatif 10/10 ([X] q1..q10) + message FIN DU QUESTIONNAIRE
3. --aide gere (contrat detecter-decalages-catalogue)
4. Catalogue : entree presente, tri alphab. global, total 112, modele
   --theme {theme}, param theme obligatoire
5. index-tools : entree presente, total 109
6. ASCII strict 0 + LF pur sur 6 fichiers (outil 5 + test)
7. Parcours-cerberus : branche ameliorer -> c1b -> c5 avec outil
   generateurs-amelioration
8. test-008 relance : 19 OK / 0 KO
9. detecter-decalages-catalogue : 111 conformes / 0 decalage
   (le 1 non testable = test-001-evaluer-agents-coherence, preexistant hors perimetre)

**Lecons** :
1. La chaine de conformite complete (Vulcain -> Morpheus -> Janus -> Cerberus) est
   desormais fermee pour generateurs-amelioration : le cycle protocolaire a ete
   execute a rebours de la carte, ce qui confirme le besoin de la refonte
   conceptuelle (les cartes doivent etre executees, pas seulement documentees).
2. Un controle croise doit RE-EXECUTER les verifications (parite, catalogue,
   normes, navigation), jamais se fier aux rapports precedents.
3. Le test-008 couvre le contrat reel de l outil (--aide requis par le
   detecteur de decalages inclus) : aucun faux positif.
## [NOTES] Controle 2026-08-09 -- valider-case v1.0.0 + test-009 (etape 2 refonte)

**Controle** : outil valider-case (etape 2 de la refonte des cartes de decision,
spec v0.1.1) + test formel test-009 (Morpheus 18/18), dans la CHAINE bout-en-bout
Vulcain -> Morpheus -> Janus -> Cerberus (conformite = le defaut).

**Verdict** : VALIDE (13 points croises refaits independamment, apres 1 correction).

**Controles** :
1. Parite --version py/sh v1.0.0
2. Execution parcours-cerberus : A ALLEGER + pattern de re-essai c5 en AVERTISSEMENT
3. Renommage complet : 0 reference validateur-case (dossier valider/valider-case)
4. Catalogue : entree valider-case (script OK), total 113, TRI ALPHABETIQUE
5. index-tools : entree + total 110
6. ASCII 0 / LF pur sur 5 fichiers (outil 4 + test)
7. test-009 relance : 18 OK / 0 KO
8. Spec-refonte v0.1.1 : type action NOUVEAU documente

**1 ecart detecte et corrige** : apres le renommage validateur-case -> valider-case,
l'entree catalogue n etait plus a sa position TRIEE (le tri se fait sur le NOUVEAU
nom). Corrige : entree repositionnee (position 95) - c est le role du second
controle de l attraper.

**Lecons** :
1. UN RENOMMAGE D OUTIL IMPLIQUE DE RE-TRIER LE CATALOGUE : le tri alphab.
   se fait sur le nom de l entree - changer le nom sans repositionner = ecart
   silencieux que seul un controle croise detecte.
2. LA CHAINE FONCTIONNE DE BOUT EN BOUT : Vulcain a cree + active Morpheus,
   Morpheus a teste + active Janus, Janus a controle + reactive Cerberus.
   Le cycle documente dans les cartes (c8 Vulcain, c9/c10 Morpheus) est
   EXECUTE - c est la conformite devenue le defaut.
3. valider-case est operationnel et mesure la degradation (15 surcharges sur
   cerberus) : les etapes 3-4 (refonte des generateurs) pourront verifier leur
   efficacite avec le meme outil.

## [LECON] 2026-08-09 -- CONTROLE ETAPE 3 (generateurs-case v0.3.0) : VERDICT VALIDE 17/17

**Controle** : refonte generateurs-case v0.3.0 (modele compose complet + --ref) + test-010 (23/23 Morpheus).

**Verdict** : VALIDE.

**Points controles independamment (17)** :
1. Parite --version v0.3.0 py/sh
2. Structure bloc : decision + 3 branches (OUI/NON/PEUT_ETRE) + deviation/rejoint refs pattern-7 (0 texte inline)
3. Validation auto : valider-case --modele CONFORME (0 a alleger) - L ALLEGEMENT PROUVE
4. --ref : {"type":"ref","ref":"pattern-12"} + protocole-tests resolvables
5. ASCII strict 0 / LF pur 0 CRLF / nommage generateurs- OK
6. Spec de l outil creee (regle des 5 fichiers completee)
7. Catalogue : entree presente + trie
8. index-tools : ligne maj (modele compose COMPLET + --ref)
9. Relances : test-010 23 OK, test-005 26 OK, detecter-decalages 0 decalage

**Lecons** :
1. La preuve de l allegement est maintenant DOUBLE : valider-case (etape 2) mesure la degradation (15 surcharges sur cerberus) ET generateurs-case v0.3.0 genere des blocs a 0 surcharge (references pattern-7 au lieu des textes inline).
2. Les "NON MIS A JOUR" de detecter-impacts sont des references DOCUMENTAIRES passives (fiches agents, explorations) : elles citent l outil mais n ont pas a changer lors d une refonte fonctionnelle. Seuls les fichiers fonctionnels (py/sh/md/spec/catalogue/index-tools) doivent etre verifies.
3. Le --aide a sous-commandes (argparse) : tester qu il fonctionne SEUL (interception avant parse_args) - c etait la seule correction requise pendant le test Morpheus.
4. 3 echecs PREEXISTANTS du testeur tester-generateurs-case.sh (compteurs 21 cases obsoletes) : a traiter dans une mission ulterieure (mise a jour des compteurs vers 32 cases).

**Conformite** : je reactive Cerberus avec le bilan consolide (cloture de la chaine bout-en-bout).

## [LECON] 2026-08-09 -- CONTROLE ETAPE 4 (generateurs-carte v0.3.0) : VERDICT VALIDE 21/21

**Controle** : refonte generateurs-carte v0.3.0 (squelette allege + delegation validateur-case) + test-011 (19/19 Morpheus).

**Verdict** : VALIDE.

**Points controles independamment (21)** :
1. Parite --version v0.3.0 py/sh
2. creer : CONFORME (0 erreur, 0 a alleger) - LA CARTE NEUVE NAIT ALLEGEE
3. Refs presentes (>= 6) : protocole-activation, pattern-N, rvav-workflow.md - 0 texte inline > 160 car
4. detecter : delegation au validateur-case (source unique de verite)
5. dupliquer-chemin : refs conservees (dc1 -> pattern-10), 0 texte inline duplique
6. ASCII strict 0 / LF pur 0 CRLF / nommage generateurs- OK
7. Spec creee (regle des 5 fichiers completee)
8. Catalogue : entree + choix action corrige (4 actions reelles) + trie
9. index-tools : ligne maj (squelette ALLEGE + references)
10. Relances : test-011 19 OK, test-005 26 OK, detecter-decalages 0 decalage

**Lecons** :
1. LA DEGRADATION EST STOPPEE A LA SOURCE : une carte creee par creer v0.3.0 est
   CONFORME des la naissance (0 a alleger) - avant, le squelette posait des textes
   inline longs que valider-case detectait. La boucle est fermee : mesurer (etape 2),
   produire des cases allegees (etape 3), produire des cartes allegees (etape 4).
2. detecter-impacts : les "NON MIS A JOUR" restants sont des references documentaires
   passives (classeur-variables, conventions) - elles citent l outil sans devoir changer.
3. Le catalogue portait un choix obsolet (["creer","analyser","dupliquer"]) : detecter
   manquait et dupliquer-chemin etait mal nomme. Le controle croise du catalogue est
   indispensable apres toute modification de sous-commandes d un outil.
4. Chaine bout-en-bout executee pour la 3e fois : Vulcain -> Morpheus (test-011) ->
   Janus (controle) -> Cerberus. La conformite est le defaut, plus l exception.

**Conformite** : je reactive Cerberus avec le bilan consolide (cloture de la chaine).
## [LECON] 2026-08-09 -- CONTROLE CROISE etape 5 : consolidation guider-parcours v0.4.0 (Vulcain)

**Controle** : refonte guider-parcours v0.4.0 (resolution des references d'indices + type action) + generateurs-case v0.3.1 (type action) + spec-guider-parcours v0.4.0 + test-012-guider-parcours + test-010 mis a jour (v0.3.1 + action).
**Verdict** : VALIDE. 23 OK / 0 KO en controle croise independant.
**Lecons** :
1. Le type action est la cle du modele compose : il s'execute sans question et enchaine (verifie : c8 action -> PARCOURS TERMINE sans QUESTION) -- il rend les cases de pilotage purement procedurales
2. La resolution des references (pattern-N, rvav, protocoles) est operationnelle : titre + contenu extraits de la spec-guider-parcours, existence verifiee pour les chemins
3. Parite py/sh maintenue sur les 2 outils modifies (v0.4.0 + v0.3.1) -- la lecon des 5 fichiers est bien appliquee
4. Le test-010 a ete mis a jour par Vulcain (0.3.0 -> 0.3.1 + 2 points action) -- c'etait attendu, pas un decalage
5. detecter-impacts confirme : fichiers fonctionnels a jour, seules des references documentaires passives (fiches, controles historises) sont NON MIS A JOUR -- comportement normal
6. Sequence respectee bout-en-bout : Vulcain -> Morpheus (test-012 18/18 + non-regression 5 suites) -> Janus -> reactiver Cerberus

**Preuve** : .zz-controle-janus-etape5.py -> 23 OK / 0 KO ; detecter-decalages : 0 decalage ; test-001-gp 14/14, test-005 26/26, test-010 25/25, test-011 19/19, test-012 18/18.
## [LECON] 2026-08-09 -- CONTROLE CROISE etape 6 : migration cerberus v0.3.0 (Buffy)

**Controle** : migration pilote du parcours-cerberus v0.3.0 (indices REFERENCES + cases ACTION) + test-013 + test-009 adapte.
**Verdict** : VALIDE. 18 OK / 0 KO en controle croise independant.
**Lecons** :
1. La migration est la preuve bout-en-bout du nouveau modele : valider-case CONFORME 0/0 (avant 15 a alleger), 18 cases action / 0 indice, 0 indice > 160, 0 case > 3 indices
2. Les refs sont resolues a la navigation : pattern-8 (chaine bout-en-bout) et protocole-activation affiches avec leur contenu -- le texte vit a UN seul endroit (spec/protocole), les cases y pointent (principe une place pour chaque chose)
3. La navigation est intacte : les 3 chemins reels (accueil, activation, retour) aboutissent a PARCOURS TERMINE
4. Le test-009 a ete adapte par Buffy (cerberus CONFORME -> temoin A ALLEGER = buffy) -- c'etait attendu et correct, pas un decalage
5. Pattern 14 respecte : fiche cerberus mise a jour (PARCOURS v0.3.0) par detecter-impacts
6. Nombre de fichiers impactes minimal : parcours JSON + fiche cerberus + test-009 + test-013 -- la migration pilote est chirurgicale
7. Sequence respectee bout-en-bout : Buffy -> Morpheus (test-013 22/22) -> Janus -> reactiver Cerberus

**Preuve** : .zz-controle-janus-etape6.py -> 18 OK / 0 KO ; test-013 22/22 ; test-009 19/19 ; test-005 26/26 ; test-010 25/25 ; test-012 18/18.
## [LECON] 2026-08-09 -- CONTROLE CROISE etape 7 : spec-guider-parcours v0.5.0 (Promethee)

**Controle** : spec-guider-parcours v0.5.0 (patterns REFERENCES, pas dupliques) + test-014.
**Verdict** : VALIDE. 16 OK / 0 KO en controle croise independant.
**Lecons** :
1. Le principe UNE PLACE POUR CHAQUE CHOSE est maintenant ecrit dans la source de verite : une case POINTE vers un pattern (ref pattern-N) au lieu de copier son texte -- modifier une regle = 1 fichier, jamais N cases
2. La spec-guider-parcours est la source de verite des refs (pattern-N) : sa version (0.5.0) est coherente entre titre, Version et les references documentaires (guider-parcours.md, vulcain.md)
3. Les 15 patterns sont intacts (rien perdu pendant la refonte)
4. Ses exemples sont la VITRINE du nouveau format : type action + indices ref, 0 texte inline > 160
5. L etape 7 clot le plan de refonte : la boucle mesure (valider-case) -> produit (generateurs-case/carte) -> navigue (guider-parcours) -> documente (spec v0.5.0) est complete et coherente
6. Sequence respectee bout-en-bout sur TOUTES les etapes : createur -> Morpheus -> Janus -> reactiver Cerberus

**Preuve** : .zz-controle-janus-etape7.py -> 16 OK / 0 KO ; test-014 12/12 ; test-012 18/18 ; test-013 22/22.
## [LECON] 2026-08-09 -- CONTROLE CROISE correctif valider-case v1.0.1 (Vulcain)

**Controle** : correctif garde-fou anti-pollution du rapport valider-case v1.0.1 + test-015 + test-009 maj.
**Verdict** : VALIDE. 10 OK / 0 KO en controle croise independant.
**Lecons** :
1. Le defaut corrige : valider-case ecrivait son rapport par defaut dans le repertoire courant -- un agent lancant depuis la racine polluait le workspace (lecon reelle : rapport a la racine)
2. Le garde-fou v1.0.1 : sans --rapport <fichier> explicite, AUCUN fichier n est cree ; --rapport ecrit exactement au chemin fourni ; --dry-run simule
3. Tester le garde-fou depuis un DOSSIER VIDE different du projet (cwd) : preuve que rien ne tombe au mauvais endroit
4. 5 fichiers a jour : py/sh/md/spec/test-009 (test-009 passe de 19 a 20 points, point 11b)
5. Nouveau test-015 : 9/9 -- il verifie les 3 branches du garde-fou + la non-regression
6. Sequence bout-en-bout respectee : Vulcain -> Morpheus (test-015) -> Janus -> Cerberus
7. Prochaine etape : Buffy migre son parcours (le prochain agent a migrer, etape 6 generalisee)

**Preuve** : .zz-controle-janus-vc.py -> 10 OK / 0 KO ; test-015 9/9 ; test-009 20/20 ; test-013 22/22 ; test-014 12/12.

## [VERDICT] 2026-08-09 -- MIGRATION BUFFY v0.3.0 VALIDEE (Janus)

**Controle** : migration du parcours-buffy v0.3.0 (indices references + cases action) + test-016-migration-buffy.
**Verdict** : VALIDE -- 12/12 points de controle passes.

**Points verifies** :
1. Structure : version 0.3.0, 31 action / 7 question / 2 controle / 9 fin / 0 indice, aucune case > 3 indices, aucun texte regle > 160 car.
2. Refs resolvables : valider-case --references CONFORME.
3. Navigation : chemins creation agent et protocole -> PARCOURS TERMINE.
4. Normes : LF pur, ASCII 0, nommage test-016 OK.
5. Non-regression : test-016 20/20, test-009 20/20 (temoins cerberus CONFORME + morpheus A ALLEGER).

**Lecons** :
1. La migration buffy prouve la generalisation du modele cerberus : les textes regle recurrents (ASCII -> pattern-2, CREATION LIMITEE -> pattern-12, COMBO -> pattern-3, CONTEXTE -> pattern-6) se remplacent par des refs, les cases indice par action.
2. Le test-009 doit etre adapte a CHAQUE migration : le temoin A ALLEGER bascule vers le prochain parcours non migre (buffy -> morpheus).

## [VERDICT] 2026-08-09 -- GENERATEURS-LIGNE v0.1.0 VALIDE (Janus)

**Controle** : outil generateurs-ligne v0.1.0 (suite des generateurs de cartes de decision : carte -> ligne -> case) + test-017-generateurs-ligne (24/24 OK).
**Verdict** : VALIDE -- 15/15 points de controle passes.

**Points verifies** :
1. Parite py/sh v0.1.0, ASCII 0, LF pur 0 (4 fichiers outils).
2. Gabarits : lister-configs (4 configs), config-1 detaille (deviation + rejoint).
3. Verification carte : A JOUR / ABSENTE / PERIMEE correctement distinguees.
4. Ajout reel config defaut : 4 cases (c<num>, c<num>a/b/c sans point), branche creee, validation CONFORME + valider-case independant CONFORME.
5. Blocage sans carte + invite Atlas, --force passe outre.
6. Non-regression test-017 24/24.

**Lecons** :
1. Le concept "ligne = chemin de bout en bout, configs = gabarits de groupes de cases" est operationnel : l agent choisit une config (defaut, config-1 deviation, config-2 RVAV, config-3 action), le generateur prepare le bloc conforme (decision + branches + rejoint), le cablage est automatique (branche sur question, suivant recable sur action).
2. La verification carte Atlas AVANT edition (existence + mtime) materialise la philosophie : on n edite une carte que si sa cartographie est a jour, sinon on active Atlas pour la regenerer puis on revient.
3. La suite est complete : generateurs-carte (carte complete) -> generateurs-ligne (ligne) -> generateurs-case (case) + generateurs-amelioration (questions) -- l edition fine reste a l agent habilite via SA carte.
## [VERDICT] 2026-08-09 -- CONTROLE CROISE generateurs-ligne v0.2.0 : VALIDE

**Contexte** : second controle (Janus, session-llm-1) apres la chaine Vulcain (creation) + Morpheus (test-017 32/32) sur l'evolution generateurs-ligne v0.1.0 -> v0.2.0 : gabarits EXTERNALISES dans gabarits-ligne.json + sous-commande ajouter-config (dry/wet).
**Verdict** : VALIDE (12 OK / 0 KO).

**Points verifies (independants de la chaine)** :
1. Parite py/sh v0.2.0 ; gabarits-ligne.json structure {version, gabarits{description, cases}} valide.
2. Les 4 configs ont des tailles INCHANGEES (defaut 4, config-1 5, config-2 4, config-3 2) -> la migration du code vers le JSON n'a rien perdu.
3. Chaque config : 1re case suffixe vide (point d'entree) + case REJOINT presente.
4. Le dict GABARITS en dur a disparu du code (chargement via charger_gabarits/GABARITS_JSON) -> externalisation reelle, une place pour chaque chose.
5. Sous-commande ajouter-config presente (action_ajouter_config + parser).
6. ASCII 0 + LF pur sur les 6 fichiers (py, sh, md, spec, gabarits, test).
7. Catalogue : ajouter-config dans les choix d'action + parametres description/gabarit + description mise a jour.
8. test-017 : 32 points, v0.2.0, 0 KO a l'execution.
9. detecter-impacts lit l'identite correctement (commun=true) -> le bloc identite tient dans les 12 premieres lignes.
10. detecter-divergences-version : generateurs-ligne ALIGNE (spec 0.2.0 = py 0.2.0).

**Lecons** :
1. La contrainte du bloc identite (12 premieres lignes pour .py/.sh) est un piege recurrent : un en-tete documentaire long repousse commun: hors limite -> detecter-impacts lit "commun=false" par defaut. Toujours verifier l'identite apres toute modification d'en-tete.
2. detecter-decalages-catalogue ne lit que l'aide RACINE : les flags des sous-parsers (--description/--gabarit d'ajouter-config) sont signales comme absents a tort. Verifier avec <sous-commande> --help avant de conclure.
3. L'externalisation des gabarits rend l'outil extensible par l'agent utilisateur (Buffy) SANS intervention de Vulcain : c'est la philosophie "une place pour chaque chose" appliquee aux outils.
4. Mon propre point 12 etait mal formule (cherchait l'absence du nom au lieu de ALIGNE) : toujours verifier la VALEUR de la ligne, pas seulement sa presence.

**Cloture** : Cerberus reactive avec le bilan de la chaine complete.
## [VERDICT] 2026-08-09 -- CONTROLE CROISE generateurs-ligne v0.3.0 : VALIDE

**Contexte** : second controle (Janus, session-llm-1) apres la chaine Vulcain (evolution) + Morpheus (test-017 41/41) sur generateurs-ligne v0.2.0 -> v0.3.0 : sous-commande copier (2 sources --source/--config + 3 modes complet/branche/suite) pour dupliquer une ligne existante.
**Verdict** : VALIDE (11 OK / 0 KO).

**Points verifies (independants de la chaine)** :
1. Parite py/sh v0.3.0 ; action_copier + detecter_groupe/collecter_groupe/cloner_groupe dans le code.
2. Modes complet/branche/suite + sources --source/--config presentes.
3. .md + spec a jour (v0.3.0 + section 4.5 copier).
4. ASCII 0 sur les 6 fichiers ; catalogue a jour (copier + source/mode/branche).
5. test-017 : v0.3.0, points 17a-17h, 41/41 a l'execution.
6. detecter-impacts commun=true ; detecter-divergences-version ALIGNE.
7. PREUVE EXTERNE : copie reelle wet sur un parcours test (ajouter config-1 puis copier) -> clone de 4 cases + CONFORME.

**Lecons** :
1. Le concept de l'utilisateur est maintenant operationnel : copier une ligne existante (ou un gabarit) pour composer une nouvelle ligne, puis generateurs-case pour l'edition fine des cases du clone -- le cycle complet de composition de cartes est en place.
2. Les garde-fous sont identiques a ajouter : carte Atlas a jour, dry/wet, validation auto CONFORME, ids c<numero>[a-z]? sans doublon.
3. La detection du groupe (remonter a la decision d'entree) est le point le plus delicat : bien distinguer decision source (point d'entree, pas de remontee) vs action (remonter a la 1re decision precedente).
4. Cerberus a passe par le questionnaire generateurs-amelioration (case c1b de SA carte) avant de lancer cette evolution : conformite du cycle d'amelioration confirmee.

**Cloture** : Cerberus reactive avec le bilan de la chaine complete.
## [VERDICT] 2026-08-09 -- CONTROLE CROISE generateurs-amelioration v2.0.0 : VALIDE

**Contexte** : second controle (Janus, session-llm-1) apres la chaine Vulcain (evolution) + Morpheus (test-008 19/19) sur generateurs-amelioration v1.0.0 -> v2.0.0 : theme ameliorer-outil reformule (14 questions, 5 rappels strategiques en tete).
**Verdict** : VALIDE (10 OK / 0 KO).

**Points verifies (independants de la chaine)** :
1. Parite py/sh v2.0.0 ; themes-amelioration.json version 2.0.0, 14 questions, ids q1..q14, 5 rappels en tete avec raison pour chaque question.
2. Contenu des 5 rappels oriente : diagnostic (usage reel), horloge, formats, ameliorer vs evoluer, perimetre.
3. Les 9 questions techniques renumerees q6..q14 avec tous les themes (index/catalogue, interface, 5 fichiers, parite, ascii, tests, impacts, garde-fous, lecon).
4. --liste affiche 14 questions ; questionnaire non-interactif 14 [X] + 14 reponses + FIN DU QUESTIONNAIRE.
5. .md + spec a jour (v2.0.0) ; ASCII 0 sur les 6 fichiers.
6. test-008 executable 19/19 ; detecter-divergences-version ALIGNE.

**Lecons** :
1. L'orientation de l'utilisateur est maintenant INTEGREE a l'outil : toute amelioration future passera d'abord par les 5 rappels (diagnostic, horloge, formats, ameliorer vs evoluer, perimetre) avant les questions techniques. C'est le mecanisme anti-patch-puis-refonte.
2. Ce changement est AUTO-APPLICATIF : la prochaine fois qu'on me demandera d'ameliorer un outil, le questionnaire me forcera a reflechir a l'evolution avant d'agir.
3. La regle des 5 fichiers s'applique aussi au fichier de CONTENU (themes-amelioration.json) : version 2.0.0 alignee sur le .py/.sh/.md/spec.

**Cloture** : Cerberus reactive avec le bilan de la chaine complete.

## [LECON] 2026-08-09 -- CONTROLE CROISE ALLEGEMENT BUFFY (parcours-vulcain v0.2.13)

**Contexte** : nouvelle regle utilisateur - BUFFY DOIT SUBIR LE SECOND CONTROLE
DE JANUS MEME SANS MODIFIER DU CODE (elle modifie les cartes et protocoles,
pas seulement le code). Rattrapage : controle de son allegement
(regles c6/c8/c12/c14 de 341/465 car. -> refs vers protocole-tests).

**VERDICT : VALIDE (6/6 points)** :
1. protocole-tests v0.2.1 : section Delegation des tests (seul Morpheus ECRIT
   et EXECUTE les test-XXX) - ASCII 0, LF pur.
2. c8/c14 : ref vers protocole-tests, chaine PRESERVEE (type controle +
   branches OUI->c9/c15 NON->c8/c14 + question 147 car. + indice outil c8).
3. c6/c12 : ref DELEGATION, suivant c7/c13 preserve, regles longues absentes.
4. Parcours v0.2.13 + fiche vulcain.md v0.2.13 (Pattern 14).
5. valider-case : 0 A ALLEGER sur c8/c14 ; navigation construire + modifier
   PARCOURS TERMINE (preuve chaine intacte).
6. Lecon Buffy documentee dans corrections.md.

**Lecons** :
1. Le second controle de Janus s'applique a TOUT travail d'un agent sur le
   cerveau (code OU cartes/protocoles) - la chaine Morpheus (tests) -> Janus
   (controle) est le standard, meme quand "il n'y a pas de code".
2. La preuve de non-regression d'une carte : navigation guider-parcours
   PARCOURS TERMINE avant/apres + valider-case sans A ALLEGER sur les cases
   touchees - c'est ce qui distingue un allegement sur d'une casse.
3. Pattern texte -> reference confirme : une regle longue documentee dans un
   fichier commun puis remplacee par une ref reste visible a l'agent (resolue
   nativement) sans surcharger la case.

## [LECON] 2026-08-09 -- CONTROLE CROISE MIGRATION PARCOURS-MORPHEUS v0.2.0

**Contexte** : pilote 2 de la migration des cartes (spec-refonte etape 6, apres
cerberus). Buffy a migre le parcours morpheus au nouveau format et m'a active
pour le second controle (regle utilisateur : Buffy passe par Janus meme sans
modifier du code).

**VERDICT : VALIDE (7/7 points)** :
1. Structure : 10 cases action, 9 refs, 0 regle > 160 car., 0 case > 3 indices,
   version 0.2.0.
2. Refs resolvables : pattern-2/3/6/8/10/12 (tous dans la spec-guider-parcours)
   + protocole-tests (dossier existant) - aucune ref morte.
3. Navigation test direct (c9=CERBERUS), test chaine (c9=VULCAIN), verifier,
   audit : PARCOURS TERMINE - les 2 fins (c10 Janus, c14 Cerberus) atteignables.
4. Fiche morpheus.md : version parcours v0.2.0 (Pattern 14).
5. valider-case : CONFORME, 0 A ALLEGER.
6. Lecon Buffy documentee (migration morpheus).
7. ASCII 0, LF pur.

**Lecons** :
1. La migration carte (indice -> action + texte long -> ref + <= 3 indices) est
   reproductible : le modele cerberus + le modele morpheus sont maintenant 2
   references pour migrer les 7 parcours restants.
2. Verifier les refs est un point de controle cle : une ref morte (pattern
   inexistant, protocole absent) casserait la navigation - valider-case ne
   couvre pas la resolvabilite des refs, il faut la verifier contre la spec.
3. Faux positif de mon script (pattern-2 absent de ma liste) : toujours verifier
   contre la source (la spec) avant de conclure une ref morte.

## [LECON] 2026-08-09 -- CONTROLE CROISE MIGRATION PARCOURS-ATHENA v0.2.0

**Contexte** : 4e parcours migre (apres cerberus, morpheus). Buffy a migre
athena au nouveau format et m'a active pour le second controle (regle
utilisateur : Buffy passe par Janus meme sans modifier du code).

**VERDICT : VALIDE (7/7 points)** :
1. Structure : 18 cases action, 0 indice, 13 refs, 0 regle > 160, 0 case >
   3 indices, version 0.2.0.
2. Refs resolvables : pattern-2/6/10/12 (tous dans la spec) - aucune ref morte.
3. Navigation creer + completer + audit : PARCOURS TERMINE.
4. Fiche athena.md : version parcours v0.2.0 (Pattern 14).
5. valider-case : CONFORME, 0 A ALLEGER.
6. Lecon Buffy documentee (migration athena).
7. ASCII 0, LF pur.

**Lecons** :
1. Le mapping des refs est desormais STANDARD et reutilisable : ASCII ->
   pattern-2, CREATION LIMITEE -> pattern-12, CONTEXTE -> pattern-6, UNE CARTE
   = UN ROLE -> pattern-10, WORKSPACE -> regle-perimetre-workspace. 3 pilotes
   (cerberus, morpheus, athena) convergent sur le meme modele.
2. Un parcours a 18 action / 0 indice est le marqueur de fin de migration :
   verifier {indice} == 0 est le premier reflexe de controle.
3. La migration reduit les cases les plus lourdes (athena c4 : 9 indices ->
   3) : la validation valider-case 0/0/0 est la preuve que la surcharge a
   disparu.

## [LECON] 2026-08-09 -- CONTROLE CROISE REGLE JANUS (carte Buffy v0.3.2)

**Contexte** : materialisation dans la carte de Buffy de la regle utilisateur
"Buffy passe par Janus meme sans modifier du code". Buffy a transforme ses 3
fins de creation en "FIN - Activer Janus" et m'a active pour le second
controle - la regle s'applique a la mission qui la materialise.

**VERDICT : VALIDE (6/6 points)** :
1. c8/c22/c27 : titre "FIN - Activer Janus", type fin, regle IMMUABLE JANUS
   presente (< 160 car.) - la chaine Buffy -> Janus -> Cerberus est materialisee.
2. Parcours v0.3.2 + fiche buffy.md v0.3.2 (Pattern 14).
3. Navigation -> c8/c22/c27 : PARCOURS TERMINE avec la fin "Activer Janus"
   atteinte (preuve que la regle est bien dans le chemin).
4. valider-case : CONFORME, 0 A ALLEGER.
5. Lecon Buffy documentee (materialiser une regle = la mettre dans la carte).
6. ASCII 0, LF pur.

**Lecons** :
1. Une regle appliquee en pratique mais absente de la carte est une regle
   fragile : la materialiser dans les fins (et la description) la rend
   structurelle, pas ponctuelle.
2. La fin de chaine standard est desormais : l'agent execute -> active JANUS
   (controle) -> Janus reactive Cerberus. C'est le maillon qui manquait a
   Buffy (elle reactivait Cerberus en direct).
3. La boucle est bouclee : la regle "Buffy passe par Janus" est maintenant
   testee par Janus lui-meme sur la carte qui la contient.

## [LECON] 2026-08-09 -- CONTROLE CROISE ALLEGEMENT FICHE vulcain.md v0.5.0 (Janus)

**Controle** : allegement pilote de la fiche vulcain.md (Buffy), 15 480 -> 10 902
octets (-30%).
**Verdict** : VALIDE -- 17/17 OK, 0 KO.
**Lecons** :
1. Verifier que l IDENTITE est intacte d abord (frontmatter type/appartient_a/
   commun : lu par detecter-impacts et verifier-role-fichier) -- c est la
   condition de non-regression d une fiche.
2. Verifier la NON-PERTE des regles de fond : chaque REGLE ABSOLUE doit rester
   presente (recherche de texte-cle), car c est l identite operationnelle de
   l agent. Aller voir les doublons supprimes ne suffit pas : il faut prouver
   que rien d essentiel n a disparu.
3. La preuve finale = outils reels : ASCII, liens, navigation du parcours
   (PARCOURS TERMINE). Un allegement qui casse la navigation est invalide meme
   si la fiche est plus legere.
4. Modele d allegement valide pour les 9 autres fiches : P0 -> ref index-tools,
   doublons supprimes, historique comprime, regles conservees, version bumpee.

## [LECON] 2026-08-09 -- CONTROLE CROISE COHERENCE PROFIL vulcain.md v0.5.1 (Janus)

**Controle** : correction du profil YAML de vulcain.md (Buffy) : suppression
des mentions "Tests rigoureux" / "Tests et validation des outils" incoherentes
avec la REGLE DELEGATION DES TESTS.
**Verdict** : VALIDE -- 14/14 OK, 0 KO.
**Lecons** :
1. Quand on verifie la disparition d une mention, SCOPER la verification au
   bon perimetre : le frontmatter (lignes 1-53) pour le profil YAML, tandis
   que l historique peut legitiment documenter l ancien -> nouveau. Un faux
   negatif vient souvent d un perimetre trop large (ma 1re passe cherchait
   dans tout le fichier et trouvait l historique).
2. La coherence d une fiche avec les regles immuables est un critere de
   controle : si une competence a ete transferee (tests -> Morpheus), chaque
   mention de cette competence dans specialites/forces/limites doit etre
   auditee. Ici 3 mentions etaient fausses : la specialite, la force ET la
   limite -- les trois ont ete corrigees.
3. Regles de non-regression identiques a l allegement : identite intacte,
   regles conservees, ASCII, LF, liens, navigation PARCOURS TERMINE.

## [LECON] 2026-08-09 -- CONTROLE CROISE FORCES/FAIBLESSES vulcain.md v0.5.2 (Janus)

**Controle** : mise a jour du profil YAML de vulcain.md (Buffy) : force
d'optimisation ajoutee, faiblesse contradictoire remplacee.
**Verdict** : VALIDE -- 16/16 OK, 0 KO.
**Lecons** :
1. Verifier le COMPTAGE quand une liste grandit : ici 5 forces attendues (4
   conservees + 1 ajoutee) -- un comptage par occurrence de '- "' est la
   preuve que l'ajout n'a pas ecrase une force existante.
2. Verifier le MIROIR force/faiblesse : la nouvelle force d'optimisation a son
   pendant negatif en faiblesse ("trop de temps sur l'amelioration parfaite").
   Un profil coherent a ses faiblesses derivees de ses forces, pas en
   contradiction avec elles.
3. Piege de mon propre script : signature de check() sans argument detail ->
   TypeError. Les scripts de controle doivent etre testes avant usage (meme
   lecon que pour les outils du cerveau).
4. Non-regression identique : identite, specialites, ASCII, LF, liens,
   navigation PARCOURS TERMINE.

## [LECON] 2026-08-09 -- CONTROLE CROISE MIGRATION COMPLETE PROMETHEE (Janus)

**Controle** : migration complete de Promethee par Buffy -- fiche v0.3.0
(allegee + commande activer corrigee + Pattern 14) + parcours v0.2.0
(18 actions, 15 refs).
**Verdict** : VALIDE -- 23/23 OK, 0 KO.
**Lecons** :
1. Controle double artefact (fiche ET parcours) : chaque artefact a ses
   criteres propres. La fiche : identite, version, Pattern 14, doublons,
   commandes exactes, refs. Le parcours : structure migree (action/refs),
   flux conserve (fins + branches), validations outils.
2. Le flux conserve se verifie par la COMPARAISON avec le flux attendu :
   5 fins + branches c1 = [creer, completer, autre] prouvent que la migration
   n a rien reordonne. Verifier les branches/`suivant` d abord, avant les
   validations de conformite.
3. La commande activer corrigee (3 args -> 2 args apres session) est un point
   de controle specifique : la fiche doit refleter la syntaxe reelle de l outil,
   pas une syntaxe inventee. Un agent qui copie une mauvaise commande casse sa
   reactivation.
4. Modele de migration valide sur le 4e agent : athena, morpheus, cerberus,
   promethee convergent (refs pattern-2/6/10/12, 0 PASSE PAR LE GENERATEUR,
   regles 4/5/6 hors parcours, <= 3 indices). La generalisation est mecanique.

## [LECON] 2026-08-09 -- CONTROLE CROISE MIGRATION COMPLETE MINERVE (Janus)

**Controle** : migration complete de Minerve par Buffy -- fiche v0.3.0
(allegee + Pattern 14) + parcours v0.2.0 (18 actions, 15 refs).
**Verdict** : VALIDE -- 24/24 OK, 0 KO.
**Lecons** :
1. MINERVE = DERNIER MAILLON de la chaine Promethee -> Minerve -> Cerberus :
   sa fin c10 est "FIN - Reactiver Cerberus (PHASE 9)", conforme Pattern 13.
   Le controleur doit verifier la DIRECTION de la fin : un agent du milieu
   active le suivant, le dernier reactiver Cerberus. Ici c'est correct.
2. La commande reactiver etait DEJA correcte (3e argument obligatoire
   present) : la lecon documentee precedemment a porte ses fruits -- on
   verifie, on ne corrige pas inutilement. Un controleur doit distinguer
   "a corriger" de "deja conforme, verifie seulement".
3. Modele de migration valide sur le 5e agent : les parcours de production
   (athena, promethee, minerve) sont STRUCTURELLEMENT IDENTIQUES (27 cases,
   18 indice -> 18 action, 5 fins, memes branches c1). Seuls les outils
   changent. La generalisation est un copier-coller de mapping + outils.
4. Non-regression : 5 fins + branches c1 + navigation 7/7 + valider-case.
## [LECON] 2026-08-09 -- CONTROLE CROISE CHAINE MODE BATCH generateurs-case v0.4.0 : VALIDE 21/21

**Controle** : chaine complete (Vulcain -> Morpheus -> Janus) de la commande `convertir`
(mode batch) de generateurs-case v0.4.0 + correction du test tester-generateurs-case.sh
(4 echecs preexistants corriges + tests PT16-PT20 pour convertir).

**Verdict** : VALIDE -- 21 controles OK / 0 KO.

**Ce qui a ete verifie independamment** (aucune confiance dans les rapports) :
1. Les 5 fichiers : py/sh/md/spec v0.4.0 alignes + entree catalogue v0.4.0
2. La commande convertir presente (action_convertir) + options --refs/--seuil/
   --version-parcours/--dry-run dans l aide
3. ASCII 0 sur les 5 fichiers, LF pur (y compris le test), py_compile + bash -n OK
4. Test complet : 28/28 VALIDE (aucun ECHEC)
5. Lecons Vulcain + Morpheus documentees
6. Test reel de convertir : dry-run OK, wet -> 0 indice restant + version bumpee

**Lecons** :
1. Verifier la conformite d execution : Vulcain a bien cree la commande, Morpheus a bien
   corrige le test (regle DELEGATION DES TESTS respectee : Vulcain n a pas touche aux
   tests), Janus a bien controle -- la chaine bout-en-bout a fonctionne sans coupure.
2. Piege de parsing dans les controles : extraire une version d un .sh avec
   '.replace("Version : ", "")' attrape le '#' du commentaire ('# Version : 0.4.0' ->
   '# 0.4.0') : utiliser .split('Version : ')[1] pour prendre la valeur apres le prefixe.
3. Le fichier tester-*.sh porte un nom de runner : valider-nommage le rejette mais c est
   un bruit PREEXISTANT (convention propre test-NNN-* dans tests/, exclue par valider-
   nommage ligne 87-88) -- ne pas le considerer comme une regression.
## [LECON] 2026-08-09 -- CONTROLE CROISE RE-MIGRATION VULCAIN (OUTIL CONVERTIR) : VALIDE 16/16

**Controle** : re-migration du parcours vulcain (v0.2.13 -> v0.3.0) realisee par Buffy avec
la commande `convertir` de generateurs-case v0.4.0 (preuve du process, decision utilisateur
apres le constat que les migrations precedentes avaient ete faites par scripts maison).

**Verdict** : VALIDE -- 16 controles OK / 0 KO, verifies independamment (aucune confiance
dans les rapports).

**Ce qui a ete verifie** :
1. Structure : v0.3.0, 32 cases, 17 actions / 0 indice / 2 controles c8/c14 / 7 fins
2. Surcharge : 0 regle > 160, 0 case > 3 indices
3. References : TOUTES resolvables (0 ERREUR sur --references) -- le bug c15
   ('regle-perimetre-workspace' singulier) est corrige par le chemin complet
   'cerveau-projet/agents/regles-immuables/general/regles-perimetre-workspace.md'
4. valider-case complet : CONFORME 0 erreur 0 a alleger
5. Navigation : 9/9 PARCOURS TERMINE (dont les 2 KO precedents, resolus par les bons
   chemins NON|OUI des controles)
6. Controles c8/c14 preserves (NON -> soi-meme, pattern de re-essai voulu)
7. Flux c1 conserve (construire/modifier/autre), ASCII 0, LF pur
8. Fiche vulcain.md Pattern 14 -> v0.3.0
9. Non-regression : test generateurs-case 28/28 toujours VALIDE avec le parcours re-migre

**Lecons** :
1. La re-migration prouve que l'outil fait le travail : converti + rapport + validation
   integree, avec un complement editorial (regles specifiques raccourcies, allegeage des
   cases > 3 indices) -- c'est le process conforme desormais pour TOUS les parcours.
2. Le backup de l'etat migre-script a servi de REFERENCE EDITORIALE (textes courts,
   allegeages) : NE PAS le supprimer avant la fin de la migration.
3. Les 2 navigations KO precedentes etaient des artefacts de chemins de test (NON des
   controles rebouclant) : le parcours original naviguait deja correctement -- verifier
   avec les bons chemins avant de conclure a un defaut du parcours.

## [LECON] 2026-08-09 -- CONTROLE CROISE CHAINE generateurs-case-convertir (VERDICT VALIDE 21/21) (Janus)

**Controle** : chaine Buffy (entree catalogue generateurs-case-convertir + fix regex generateur v0.2.2) -> Morpheus (test-005 26/26).

**Verdict** : VALIDE - 21/21 OK, 0 KO.

**Verifications independantes** :
1. Catalogue : JSON valide, tri OK, v0.2.4, 115 entrees, entree generateurs-case-convertir avec modele 6 placeholders + 6 parametres (dry_run/verbose flags booleens), version 0.4.0.
2. Generateur py+sh v0.2.2 : motif generique --[a-z0-9-]+ RETIRE de composer_commande (les 2 versions), remplace par le flag declare du parametre (re.escape(flag_param)).
3. Generation reelle : T1 dry-run present/verbose absent, T2 vides retires + --seuil 160 defaut garde, T4 combinaison complete. Parite py/sh --version et generation identiques.
4. Test-005 : 26 OK / 0 KO (les 3 KO prevus corriges : valeurs de version).

**Lecons** :
1. Le piege du regex generique : un motif --[a-z0-9-]+ peut capturer le flag d'un placeholder VOISIN deja genere (perte silencieuse). Toujours utiliser le flag declare du parametre.
2. Distinguer dans un test : valeur attendue (a corriger lors d'un bump) vs reference historique dans les commentaires (a conserver) - le test-005 garde 1 reference v0.2.1 historique legitime.
3. Verification independante = ne pas se fier aux rapports : j'ai re-genere moi-meme les commandes et relance le test.

**Point de vigilance documente** : l'incident de troncature de corrections.md Buffy (ecriture ascii plantee apres ouverture 'w') - lecon Buffy ajoutee : construire tout le contenu en memoire PUIS ecrire, jamais 'w' ascii avant verification. 9 points medians U+00B7 preexistants corriges au passage (dette ASCII).

## [LECON] 2026-08-09 -- CONTROLE CROISE CARTE BUFFY v0.3.3 (VERDICT VALIDE 13/13) (Janus)

**Controle** : correction de la carte Buffy (c10c utilise generateurs-case-convertir, commandes en dur retirees, version 0.3.3).

**Verdict** : VALIDE - 13/13 OK, 0 KO.

**Verifications independantes** :
1. Parcours : version 0.3.3, JSON valide, ASCII 0, LF pur.
2. c10c : 3 indices max, generateurs-case sans commande en dur (PASSE PAR LE GENERATEUR), generateurs-case-convertir present, pattern-2 conserve / pattern-12 retire (justifie : modification, pas creation).
3. c10d : generateurs-ligne sans commande en dur.
4. Transitions : c10b OUI->c10c, ligne->c10d, non->c11 intactes ; c10c/c10d->c37.
5. valider-case CONFORME (0 erreur, 0 a alleger).
6. fiche buffy.md v0.3.3 ASCII.
7. Le catalogue contient generateurs-case-convertir et la generation reelle fonctionne (--dry-run present, flags vides retires).

**Lecons** :
1. Quand un outil devient generable (entree catalogue), les cartes doivent basculer de la commande en dur vers le format PASSE PAR LE GENERATEUR (nom + catalogue + chemin) - la carte Buffy est le premier exemple complet.
2. L'ajout d'un outil peut pousser une case au-dela de 3 indices : verifier valider-case et alleger en retirant la ref la moins pertinente selon la nature de la case (creation vs modification).
3. La verification des transitions (branches) est indispensable apres toute modification de zone de cases.

## [LECON] 2026-08-09 -- CONTROLE CROISE GARDE-FOU RELECTURE (VERDICT VALIDE 14/14) (Janus)

**Controle** : garde-fou relecture fiche mis en place par Cerberus (constat utilisateur : les agents relisent leurs corrections mais sautent la fiche).

**Verdict** : VALIDE - 14/14 OK, 0 KO.

**Verifications independantes** :
1. Parcours-cerberus v0.3.1 : c6 et c10 portent l'indice regle GARDE-FOU RELECTURE (texte exact "RELIS TA FICHE PUIS TES CORRECTIONS"), 3 indices max respecte, outil activer-agent-principal conserve, valider-case CONFORME (0 erreur, 0 a alleger), ASCII 0, LF pur.
2. Protocole-activation : 2 mentions du garde-fou (Etape 3 Relecture + section La mission), ASCII 0, LF pur.
3. Fiche cerberus.md v0.3.1 (Pattern 14), ASCII 0.
4. Lecon Cerberus documentee (incident + lecon technique generateurs-case editer qui REMPLACE les indices au lieu de les AJOUTER).

**Lecons** :
1. Le defaut de relecture etait dans l'EXECUTION, pas dans les regles : les cartes et le protocole exigeaient deja fiche + corrections, mais la RAISON d'activation ne le forcait pas. Le garde-fou dans la RAISON est la bonne correction.
2. generateurs-case editer --indice-regle remplace les indices existants (piege : a verifier apres chaque editer).
3. Appliquer le garde-fou soi-meme : j'ai relu MA fiche et MES corrections au demarrage de ce controle (application immediate de la regle).
## [LECON] 2026-08-09 -- CONTROLE CROISE MIGRATION 4 PARCOURS (VERDICT VALIDE 32/32) (Janus)

**Controle** : migration finale des parcours atlas/clio/janus/themis au format action + mise a jour test-005.
**Verdict** : VALIDE (32/32 OK).

**Lecons** :
1. Les 4 parcours sont au format action (0 case type indice), JSON valide, versions a jour (atlas 0.2.0, clio 0.2.0, janus 0.3.0, themis 0.3.0), valider-case CONFORME 4/4, valider-cartes-decision CONFORME 4/4, navigations PARCOURS TERMINE, ASCII 0 + LF pur partout.
2. test-005 : 26/26 OK - version atlas 0.1.10 -> 0.2.0, historique conserve, residu c30 documente.
3. DECOUVERTE IMPORTANTE : les commandes en dur avec catalogue restantes dans clio/janus/themis (13/20/17) ne sont PAS un ecart de cette migration - c'est une dette GENERALISEE : TOUS les parcours sauf atlas (athena 14, buffy 27, cerberus 13, minerve 16, promethee 16, vulcain 9, morpheus 8) en ont. Atlas est le seul pilote strict nettoye (c30 documente). Le test-005 le documente.
4. Lecon de methode : TOUJOURS verifier le niveau de reference avant de fixer un critere - mon premier controle (0 commande en dur attendu) etait faux, la norme reelle est "atlas = pilote strict, dette ailleurs". Comparer a l'existant AVANT de conclure KO.
5. Observation hors perimetre : valider-cartes-decision.py ligne 22 mentionne "spec v0.2.9" alors que la spec est en v0.5.0 (mention stale preexistante dans un docstring) - a corriger plus tard.
6. Prochaine piste logique (dette generalisee) : generaliser le PASSE PAR LE GENERATEUR aux commandes en dur restantes des 10 parcours (au lieu du pilote atlas seul) - a plannifier.

**Fichiers controles** : 4 parcours + 2 fiches (janus.md, themis.md) + test-005 + corrections morpheus/buffy.

## [LECON] 2026-08-10 -- CONTROLE CROISE valider-cartes-decision v0.3.1 (VERDICT VALIDE 15/15) (Janus)

**Mission** : second controle de la correction valider-cartes-decision v0.3.1 (type action ajoute,
impact oublie de la migration des 11 parcours).

**Resultats** : 15/15 OK. Le controle a detecte 1 point reel que la chaine avait manque :
l'en-tete docstring du .py (Version : 0.3.0, ligne 30) n'avait pas ete mis a jour alors que
VERSION = 0.3.1 l'etait - correction immediate.

**Lecons** :
1. Une version d'outil apparait a PLUSIEURS endroits d'un meme fichier : VERSION (code) ET
   en-tete docstring (documentation) - les verifier tous les deux
2. Dans un controle de version, distinguer les mentions ACTIVES des lignes d'HISTORIQUE
   (tableau | 0.x.y | date |) qui sont legitimes - un critere naif 'aucune mention 0.3.0'
   cree un faux KO
3. La chaine Cerberus -> Vulcain -> Morpheus -> Janus a bien fonctionne : correction,
   test formel (24/24), non-regression (11/11 + test-005 26/26), puis controle croise
   independant (15/15) - le second controle reste la derniere ligne de defense

## [LECON] 2026-08-10 -- CONTROLE CROISE MENTIONS STALE (VERDICT VALIDE 13/13) (Janus)

**Mission** : second controle de la correction des 2 mentions stale de version dans les .md
des generateurs (generateurs-case.md ligne 342 spec v0.2.5, generateurs-carte.md ligne 195
spec v0.2.13 -> toutes deux v0.5.0 + types question/indice/controle/fin/action).

**Resultats** : 13/13 OK. Le controle a detecte 1 faux KO initial : la reference d'introduction
Pattern 7 (spec-guider-parcours v0.2.13) dans generateurs-carte.md etait CENSEE sur 2 lignes
(markdown wrap) -> la recherche mono-ligne ne la trouvait pas. Apres normalisation des fins de
ligne, la reference est bien intacte (NON touchee par la correction).

**Lecons** :
1. Dans les .md, une reference peut etre coupee sur 2 lignes par le wrap markdown -
   pour verifier la NON-REGRESSION d'une reference, normaliser les fins de ligne
   (replace '\n' par ' ') avant la recherche, sinon faux KO
2. La distinction references d'INTRODUCTION (legitimes, la spec les cite avec leur version)
   vs VERSION COURANTE du format (stale si obsolete) est la cle du scan des mentions de
   versions - Vulcain a bien conserve les unes et corrige les autres
3. La chaine Cerberus (scan) -> Vulcain (correction ciblee 2 lignes) -> Janus (controle 13/13)
   a fonctionne pour une correction DOCUMENTAIRE pure - le second controle reste utile meme
   sans changement de code

## [LECON] 2026-08-10 -- CONTROLE CROISE 15 LIENS CASSES (VERDICT VALIDE 10/10) (Janus)

**Mission** : second controle de la correction des 15 liens casses preexistants (observation
Themis, evaluer-coherence 50/100 -> 75/100). Buffy a corrige 10 fichiers (chemins relatifs
inexacts vers des cibles existantes).

**Resultats** : 10/10 OK. Le controle a detecte 1 point reel manque par Buffy : la ligne 271
de fiche-agent-template.md contenait un chemin `../tools/guider/guider-parcours/` en BACKTICKS
(dans un tableau) - pas un lien markdown (donc invisible pour evaluer-coherence) mais un chemin
relatif quand meme inexact depuis agents/ -> corrige par coherence.

**Lecons** :
1. Un chemin entre BACKTICKS n'est pas detecte par evaluer-coherence (ni par valider-liens) :
   c'est une mention de chemin, pas un lien markdown - mais s'il est inexact il reste un
   faux-fuyant a corriger pour la coherence globale (il ne casse aucun outil)
2. Les fichiers de documentation d'exemples (valider-liens.md, corriger-liens.md,
   convention-liens.md) utilisent des cibles FICTIVES differentes (fichier1.md, ancien.md,
   chemin/fichier.md) - un controle qui verifie leur integrite doit chercher LEUR motif
   caracteristique, pas un motif generique commun
3. La preuve d'integrite la plus solide : git status vide sur les fichiers non concernes
   (aucune modification) - plus fiable qu'un contenu attendu
4. La correction de liens relatifs doit verifier TOUTES les formes : liens markdown
   les liens markdown (texte entre crochets suivi d une cible entre parentheses) ET les mentions de chemins en backticks

5. PIEGE markdown : un exemple de syntaxe de lien ecrit litteralement DANS une lecon
   (texte entre crochets suivi d une cible entre parentheses) est interprete par
   evaluer-coherence comme un VRAI lien et casse la coherence. Les backticks INLINE
   ne protegent pas : la regex ne saute que les blocs fenced (trois backticks). Pour
   montrer un exemple de syntaxe, le DECRIRE en toutes lettres ou le mettre dans un
   bloc fenced - jamais en litteral inline

## [LECON] 2026-08-10 -- CONTROLE CROISE GARDE-FOU FORMAT LECONS (VERDICT VALIDE 11/11) (Janus)

**Mission** : second controle du garde-fou format des lecons ajoute par Buffy (piege markdown :
un exemple litteral de syntaxe de lien dans une lecon cassait evaluer-coherence).

**Resultats** : 11/11 OK. Le garde-fou est present dans les 2 fichiers (protocole-auto-correction
+ corrections-template), mentionne le piege et la methode de protection (bloc fenced), et ne cree
lui-meme AUCUN motif de lien litteral (verifie par regex + evaluer-coherence 0 lien casse).

**Lecons** :
1. Le test le plus important d'un garde-fou contre un motif : verifier que le garde-fou
   LUI-MEME ne produit pas le motif qu'il interdit (regex sur les 2 fichiers modifies)
2. Documenter une syntaxe sans la produire est une regle meta : elle s'applique au texte de
   la regle elle-meme - Buffy l'a bien appliquee (decrit en toutes lettres, pas de crochets
   suivis de parentheses)
3. La chaine lecon (Janus) -> garde-fou (Buffy) -> controle (Janus) boucle l'apprentissage :
   un piege decouvert devient une regle durable documentee dans le protocole

## [LECON] 2026-08-10 -- CONTROLE CROISE 2 PROTOCOLES DEDIES A BUFFY (VERDICT VALIDE 21/21) (Janus)

**Mission** : second controle des 2 protocoles dedies a la verification du
travail de Buffy, crees par Buffy : protocole-controle-buffy (controle croise
de Janus, 10 etapes) et protocole-audit-buffy (audit de conformite de Themis,
9 etapes), + index-regles-general (2 entrees) + fiches janus.md/themis.md
(liens Protocoles applicables) + lecon Buffy.

**Resultats** : 21/21 OK. Structure conforme (frontmatter + 7 sections
standard), liens relatifs corrects (pattern protocole-creation-combos : 3
niveaux pour conventions/ et tools/, 2 niveaux pour protocoles voisins),
ASCII 0 + LF pur, valider-tableaux CONFORME, evaluer-coherence 0 lien casse,
aucun motif markdown parasite dans les 2 protocoles, fichiers d exemples de
doc intacts, perimetre exact (2 dossiers + 4 fichiers).

**Lecons** :
1. Un protocole dedie par agent est la bonne reponse quand les verifications
   dependent de la NATURE du travail : outils (Vulcain) vs documents du
   cerveau (Buffy) - le combo-controle-outil reste pour Vulcain, le nouveau
   protocole-controle-buffy couvre liens, formats, conventions, lecons,
   parcours et fiches
2. Le pattern des chemins relatifs d un protocole dans regles-immuables/
   general/protocole-XXX/ est maintenant capitalise : 3 niveaux (2 points x3)
   pour conventions/ et tools/, 2 niveaux pour les protocoles voisins - ce
   pattern devrait servir de reference pour TOUTE future creation de protocole
3. La separation des responsabilites est nette : Janus controle (VALIDE/A
   REVOIR/REJETE) via protocole-controle-buffy, Themis audite (CONFORME/NON
   CONFORME) via protocole-audit-buffy - les 2 protocoles se referencent
   mutuellement dans leurs Liens
4. Le piege markdown (exemple de syntaxe de lien litteral) est maintenant
   documente DANS les 2 protocoles eux-memes, ce qui les rend conformes a la
   regle qu ils enoncent - une lecon technique peut devenir un piege du
   protocole

## [LECON] 2026-08-10 -- CONTROLE CROISE BRANCHEMENT PROTOCOLE v0.3.1 (VERDICT VALIDE 15/15) (Janus)

**Mission** : second controle du branchement du protocole-controle-buffy dans
le parcours-janus v0.3.1 (Buffy) - PREMIERE APPLICATION REELLE du
protocole-controle-buffy (etapes E1-E10) comme cas de test de la chaine
complete Buffy -> Janus -> Themis.

**Resultats** : 15/15 OK (apres correction du critere E2). Les 3 modifications
sont presentes (c11/c18 : indice fichier protocole-controle-buffy ; c8 : regle
des points E1-E10 ; version 0.3.1), JSON valide (32 cases intactes), ASCII 0 +
LF pur, valider-cartes-decision --tous 11/11 CONFORME, navigation
guider-parcours OK, evaluer-coherence 0 lien casse, lecon Buffy sans motif
parasite.

**Lecons** :
1. LE PROTOCOLE-CONTROLE-BUFFY EST OPERATIONNEL : je l ai applique en reel
   (E1 fichiers modifies, E2 integrite, E3 ASCII/LF/JSON, E4 modifications
   presentes, E5 structure + lecons, E7 lien resolvable, E9 validations, E10
   verdict) - la reference de ma case c11 m a conduit directement au protocole
2. PIEGE E2 : un controle d integrite qui exige git status VIDE sur des
   fichiers modifies par une mission PRECEDENTE produit un faux negatif. Le
   bon critere : la mission actuelle n a modifie QUE ses fichiers attendus +
   les fichiers de la mission precedente portent toujours leurs marqueurs
   valides (preuve de non-regression)
3. LA CHAINE COMPLETE EST OPERATIONNELLE : Buffy branche -> Janus controle en
   appliquant protocole-controle-buffy -> Janus active Themis (case c31) ->
   Themis audite avec protocole-audit-buffy (branche audit-agent) -> Themis
   reactive Janus avec son rapport (c32) -> Janus reactive Cerberus

## [LECON] 2026-08-10 -- CONTROLE CROISE CORRECTION REACTIVER/ACTIVER (VERDICT VALIDE 19/19) (Janus)

**Mission** : second controle de la correction par Buffy des 2 cases fausses
(atlas c31b, themis c25b) qui disaient REACTIVER L AGENT PRECEDENT avec la
commande reactiver (qui ramene TOUJOURS a Cerberus), + mise a jour du
protocole-activation avec le Pattern 13 (3 modes).

**Resultats** : 19/19 OK. Les 2 cases sont corrigees (titre ACTIVER + commande
activer-agent-principal.py activer session-llm-1 <agent_precedent> <raison>),
scan des 11 parcours : 0 case fausse restante, protocole-activation avec les
3 modes (DIRECT / CHAINE / DERNIER MAILLON) + regle reactiver = toujours
Cerberus documentee, JSON valides, cartes 11/11, ASCII + LF, lecon Buffy au
format, evaluer-coherence 0 lien casse.

**Lecons** :
1. LA CORRECTION EST COMPLETE ET CHIRURGICALE : sur les 37 fins mentionnant
   Cerberus, les 2 seules fausses sont corrigees - le scan confirme 0 reste
   dans les 11 parcours
2. LE COUPLE TEXTE + COMMANDE doit etre verifie ensemble dans une case :
   le texte (ACTIVER l agent precedent) et la commande (activer <agent>)
   sont maintenant coherents - c est la lecon de l incident Themis/Morpheus
3. LE PROTOCOLE-ACTIVATION porte maintenant la regle de decision complete :
   QUI m a active ? (Cerberus -> reactiver ; agent -> activer ; dernier
   maillon -> reactiver avec bilan) - la regle est propagee de la spec vers
   la source de verite de l activation
4. La boucle est fermee : audit Themis (cause racine) -> correction Buffy ->
   controle Janus (19/19) - le piege reactiver est elimine des cartes
## [LECON] 2026-08-10 -- CONTROLE CROISE RECOMMANDATIONS MOYENNES (VERDICT VALIDE 27/27) (Janus)

**Controle** : mission Buffy -- application des recommandations MOYENNE de l'audit reactiver/activer (4 fins de parcours + fiche morpheus + fiche atlas).

**Verdict** : VALIDE (27/27).

**Lecons** :
1. **Le piege reactiver avait un 3e porteur invisible** : la fiche morpheus.md (ligne 165) donnait la commande `reactiver` pour " revenir a Vulcain " -- l'audit Themis ne scannant que les parcours JSON, il ne l'avait pas detecte. Le scan GLOBAL (fiches + parcours + protocoles) est indispensable pour les classes de bugs transverses.
2. **La regle de decision " activation directe vs maillon de chaine " est desormais complete** : 4 fins REACTIVER-CERBERUS precisees (atlas c11, clio c12, minerve c10, themis c13) + morpheus c14 + janus c10 (deja correctes) = les 6 fins concernees portent leur condition.
3. **Coherence fiche/parcours** : la fiche atlas.md etait la seule avec un FLUX contradictoire (" TOUJOURS reactiver Cerberus ") face a sa ligne Pattern 8 -- corrigee vers Pattern 13. A surveiller dans les futures revisions : les fiches doivent toujours refleter la carte.
4. **Verification croisee** : JSON valides (v0.2.0/v0.3.0), cartes 11/11, evaluer-coherence 0 lien casse, ASCII 0 + LF pur sur les 6 fichiers, lecon Buffy presente.
## [LECON] 2026-08-10 -- CONTROLE CROISE TEST-018-FINS-REACTIVATION (VERDICT VALIDE 26/26) (Janus)

**Controle** : second controle croise du test-018-fins-reactivation cree par Morpheus (verification croisee independante) + coherence avec le protocole-tests v0.2.2.

**Verdict** : VALIDE (26/26).

**Lecons** :
1. **Le test-018 est un vrai test de non-regression transverse** : il scanne les 11 parcours, verifie la regle Pattern 13 (toute fin REACTIVER porte la condition 'activation directe par Cerberus' OU est le dernier maillon avec bilan consolide), les 4 fins precisees (atlas c11, clio c12, minerve c10, themis c13) et l'anti-regression du piege reactiver (aucune fin Activer X avec la commande reactiver).
2. **La recoupe independante confirme l'exactitude** : les 6 fins REACTIVER reelles (atlas, clio, janus, minerve, morpheus, themis) correspondent exactement aux attendues par le test -- la liste du test n'est pas une invention, elle reflete l'etat reel des 11 parcours.
3. **Le protocole-tests v0.2.2 reference le test-018** : la regle GARDE-FOU FIN DE PARCOURS est coherente avec le test (meme commande, meme perimetre) -- le couple test + protocole forme un verrou de non-regression complet.
4. **Les KO preexistants (test-013, test-016) sont hors perimetre** : ce sont des divergences de version (parcours avances, tests non re-adaptes), connues et documentees -- a traiter par Morpheus (seul habilite a toucher aux tests).
## [LECON] 2026-08-10 -- CONTROLE CROISE PROTOCOLE-TESTS v0.2.3 (VERDICT VALIDE 23/23) (Janus)

**Controle** : second controle croise du protocole-tests v0.2.3 (regle RE-SCAN COMPLET ajoutee par Morpheus apres le garde-fou FIN DE PARCOURS de la v0.2.2).

**Verdict** : VALIDE (23/23).

**Lecons** :
1. **Le protocole-tests est un verrou de non-regression en 2 volets complementaires et bien ordonnes** : GARDE-FOU FIN DE PARCOURS (v0.2.2, cible : test-018, declencheur : modification de fin) puis RE-SCAN COMPLET (v0.2.3, cible : toute la suite test-009 a test-018, declencheur : refonte d outil ou de parcours). Les deux sont des REGLES IMMUABLES distinctes et sans doublon.
2. **La regle RE-SCAN COMPLET est operationnelle** : elle documente le declencheur, la commande de scan en boucle, le verdict 0 KO, les 2 lecons types (versions attendues apres bump, temoins apres migration) et rappelle la delegation Morpheus.
3. **La coherence entre les 2 garde-fous est validee** : le RE-SCAN COMPLET est place apres le FIN DE PARCOURS (les sections restent distinctes, la fin de la premiere regle sert de point de transition) -- pas de doublon ni de contradiction.
4. **La suite test-009 a test-018 est 100% verte** (0 KO partout) au moment du controle : la regle est en phase avec l etat reel de la suite.

## [NOTES] Protocole sante-fichiers-agents -- premier etat des lieux (2026-08-10, Janus)

**Contexte** : premiere execution du protocole-sante-fichiers-agents (cree par Buffy,
branche en c33 du parcours-janus v0.3.2). Etablissement de l'etat de sante des
fichiers des 11 agents (fiche + parcours + corrections).

**E1 Inventaire** : 11/11 OK (les 33 fichiers existent).

**E2 Coherence fiche/parcours** : 10/11 A JOUR. 1 ecart :
- janus : la fiche cite PARCOURS v0.3.0, le parcours reel est v0.3.2
  (decalage deja present avant le bump c33 : 0.3.0 vs 0.3.1).

**E3 Format des fiches** : 11/11 frontmatter OK. Sections standard presentes
sur toutes les fiches (minerve et promethee plus compactes : 7 sections).
- cerberus : conserve les sections anciennes 'Le cycle fondamental' et
  'Agents disponibles' (philosophie pre-migration).

**E4 Normes (ASCII + LF)** : 10/11 OK. 1 ecart :
- promethee : corrections.md contient 8 non-ASCII (separateurs '\u00b7' lignes
  177-178 et 209 des lecons historiques).

**E5 Regles a jour (Pattern 13 -- la fin suit SA carte)** : 8/11 OK. 3 ecarts :
- athena : aucune mention de la fin-suit-SA-carte NI de reactiver (regles a jour ?)
- cerberus : mentionne 'reactiver' mais pas 'sa carte' (ancienne philosophie :
  reactiver Cerberus systematique)
- morpheus : le concept 'sa carte' est present mais jamais labellise Pattern 13

**E6 Verdict global** : ETAT MOYEN -- 5 ecarts a traiter (2 regles, 1 fiche,
1 fichier normes, 1 migration).

**Actions recommandees** :
1. [regle] Mettre a jour la fiche janus : PARCOURS v0.3.0 -> v0.3.2
2. [normes] Corriger les 8 non-ASCII de promethee/corrections.md (separateurs)
3. [regle] Ajouter le Pattern 13 dans la fiche athena (aucune mention)
4. [fiche] Relire la fiche cerberus (sections anciennes + philosophie reactiver)
5. [migration] Terminer la migration des 6 parcours v0.2.0 non migres
   (athena, atlas, clio, minerve, morpheus, promethee) vers le format v0.3.x
   (indices references + cases action) -- la cause racine de la derive

**Lecon Janus** : le protocole sante est operationnel et a confirme la derive
silencieuse des fichiers agents. La cause racine n'est pas les fiches mais la
migration incomplete des parcours (6/11 encore en v0.2.0). A re-executer apres
chaque migration pour verifier l'alignement fiche/parcours.

## [LECON] 2026-08-10 -- CONTROLE CROISE 4 CORRECTIONS PROTOCOLE SANTE (VERDICT VALIDE 21/21) (Janus)

**Controle** : second controle croise des 4 corrections d'ecarts legers
appliquees par Buffy apres le premier etat des lieux sante-fichiers-agents.

**Verifications (21/21 VALIDE)** :
- C1 (janus.md) : PARCOURS (v0.3.2) aligne sur la version reelle du parcours,
  aucun residu v0.3.0/v0.3.1.
- C2 (promethee/corrections.md) : 0 caractere U+00B7, 0 non-ASCII total,
  separateurs "-" en place.
- C3 (athena.md) : section "Pour terminer ma mission (la fin suit SA carte)"
  presente, conforme a sa fin reelle (activer Promethee, pas reactiver
  Cerberus), REGLE CHAIN PROMETHEE conservee.
- C4 (cerberus.md) : relecture alignee Pattern 13 -- cycle fondamental
  modernise (CERBERUS -> AGENT_1 -> ... -> CERBERUS), aucun residu de
  l'ancien schema (CERBERUS -> JANUS -> CLIO), ligne Clio corrigee, frontmatter
  cycle.sortie + specialites alignes, version 0.2.1, entree Historique.
- C5 : ASCII 0 + LF pur sur les 4 fichiers, valider-cartes-decision 11/11.

**Lecons** :
- La relecture d'une fiche = verifier 3 plans : le cycle (schema), les
  connexions (lignes du tableau agents) et l'historique (version + entree).
- Le modele "Pour terminer ma mission (la fin suit SA carte)" est le standard
  des fiches migrees : a verifier a chaque controle que la fin declaree
  correspond a la fin reelle de la carte de l'agent.
- Les 4 ecarts du premier etat des lieux sont tous corriges : le protocole
  sante boucle (detecter -> corriger -> controler) fonctionne en reel.

**Outils utilises** : lire-fichier, valider-conformite-ascii, activer-agent-principal.

## [LECON] 2026-08-10 -- RE-AUDIT SANTE-FICHIERS-AGENTS (VERDICT A REVOIR LEGER, 4/4 ecarts resorbes) (Janus)

**Audit** : re-execution du protocole sante-fichiers-agents apres les 4
corrections de Buffy (controlees 21/21).

**Resultats** :
- E1 inventaire 11/11, E2 coherence fiche/parcours 11/11 A JOUR (janus v0.3.2),
  E3 format 11/11 frontmatter, E4 normes 11/11 ASCII 0 + LF pur, E5 Pattern 13
  10/11 (morpheus non formule explicitement).
- Les 4 ecarts legers du premier etat des lieux sont RESORBES : janus v0.3.2,
  promethee 0 non-ASCII, athena Pattern 13, cerberus relecture v0.2.1.

**Lecons** :
- La boucle detecter -> corriger -> controler du protocole sante fonctionne :
  le re-audit confirme la resorption des 4 ecarts sans regression.
- Nouveau point mineur detecte au re-audit : la fiche morpheus contient le
  concept (REGLE DELEGATION, retour a Vulcain) mais ne formule pas le Pattern
  13 explicitement -- a corriger au prochain passage (hors perimetre des 4
  corrections demandees par l'utilisateur).
- Le point majeur reste la migration des 6 parcours v0.2.0 (cause racine de la
  derive) : a traiter comme prochaine etape, un agent a la fois.
- Piege du re-audit : verifier les versions citees avec la forme exacte
  (vX.Y.Z) car les regex partielles (vX.Y) creent des faux negatifs.

**Outils utilises** : lire-fichier, lister-fichiers, valider-conformite-ascii,
activer-agent-principal.

## [LECON] 2026-08-10 -- CONTROLE CROISE PATTERN 13 FICHE MORPHEUS (VERDICT VALIDE 19/19) (Janus)

**Controle** : second controle croise de la formulation explicite du Pattern 13
dans la fiche morpheus (point mineur du re-audit sante), ajoutee par Buffy.

**Verifications (19/19 VALIDE)** :
- C1 : sous-section "Pour terminer ma mission (la fin suit SA carte)" presente,
  placee dans la section UTILISATION DE activer-agent-principal, apres le bloc
  "Pour revenir a Vulcain", avant "## Structure des tests".
- C2 : formulation conforme au modele (Pattern 8) : activation directe ->
  reactiver Cerberus ; maillon de chaine -> activer le suivant selon SA carte ;
  seul le DERNIER maillon reactiver Cerberus.
- C3 : alignement avec la fin reelle de la carte morpheus : c10 FIN - Activer
  Janus, c14 FIN - Reactiver Cerberus, retour VULCAIN (MODE CHAINE) -- tous
  cites et conformes aux fins reelles du parcours.
- C4 : REGLE DELEGATION (VULCAIN -> MORPHEUS -> VULCAIN) conservee intacte,
  regle "Pour revenir a Vulcain" unique (pas de doublon), MODE CHAINE conserve.
- C5 : ASCII 0 + LF pur, valider-cartes-decision 11/11.

**Lecons** :
- La formulation Pattern 13 d'une fiche doit citer les fins REELLES de la
  carte (identifiants c10/c14 verifies dans le parcours) : le controle croise
  croise fiche <-> parcours, pas seulement la presence de la phrase.
- Une mission de formulation ne doit JAMAIS dupliquer ni contredire les regles
  existantes (REGLE DELEGATION) : verifier l'unicite des blocs.
- Le point mineur du re-audit sante est resorbe : E5 morpheus passe OUI.

**Outils utilises** : lire-fichier, valider-conformite-ascii, activer-agent-principal.

## [LECON] 2026-08-10 -- CONTROLE CROISE PROTOCOLE SANTE v0.1.1 (VERDICT VALIDE 20/20) (Janus)

**Controle** : second controle croise du renforcement de l etape E5 du
protocole-sante-fichiers-agents (Pattern 13 verifie par croisement
fiche/parcours) par Buffy.

**Verifications (20/20 VALIDE)** :
- C1 : version 0.1.1, tableau E1-E7 intact (7 lignes, ordonnees, aucun bloc
  parasite entre les lignes).
- C2 : E5 du tableau enrichi (CROISEMENT fiche/parcours, identifiants cX,
  outil parcours-<agent>.json).
- C3 : section "Detail E5" placee APRES le tableau (pas dans), sous-criteres
  E5a (mention textuelle), E5b (croisement : chaque fin cX doit etre une case
  de type fin dans le parcours, mention sans identifiant = INSUFFISANTE),
  E5c (conformite du sens : direct -> reactiver Cerberus, maillon -> suivant,
  dernier maillon -> Cerberus).
- C4 : la lecon du re-audit est referencee (morpheus c10/c14).
- C5 : ASCII 0 + LF pur, RVAV/Exemples/Notes intacts.

**Lecons** :
- Piege de controle : un comptage de lignes de tableau doit exclure la ligne
  d en-tete ("| Etape | Action |...") qui commence par "| E" -- sinon faux
  negatif. Verifier avec une regex ciblee ^\| E[0-9] \|.
- Le protocole sante verifie desormais le Pattern 13 par CROISEMENT : la fiche
  doit citer des identifiants cX reels du parcours (type fin + titre), ce qui
  rend le controle resistant aux formulations textuelles vagues.
- La lecon du re-audit est capitalisee dans le protocole : le prochain etat
  des lieux appliquera E5b automatiquement.

**Outils utilises** : lire-fichier, valider-conformite-ascii, activer-agent-principal.
