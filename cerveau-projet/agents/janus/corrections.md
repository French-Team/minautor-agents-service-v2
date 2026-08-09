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