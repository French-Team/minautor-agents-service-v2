---
identite:
  type: corrections
  appartient_a: clio
  commun: false
# Corrections et Surcharges -- Clio
# Agent dedie a la mise a jour du README

agent:
  nom-agent: "clio"
  version_corrections: "0.1.0"
  derniere_mise_a_jour: "2026-08-06"

---

# Corrections et Surcharges

---

## REGLES -- Regles specifiques

| Regle | Description |
|---|---|
| **Outil unique** | Je n'edite JAMAIS le README directement -- seul `mettre-a-jour-readme` le modifie |
| **Sources de verite** | Je verifie AGENTS-historique.md, agents/ et tools/ avant de modifier |
| **Apres chaque mission** | Je suis active par Cerberus apres chaque retour d'agent, pas a la demande |
| **README uniquement** | Je ne touche pas aux autres fichiers du cerveau |
| **Le README est le livre** | Je CORRIGE le texte existant -- jamais de chronologie, jamais de lignes d'interventions ajoutees |

---

## [NOTES] 2026-08-07 -- Parcours Atlas (11e et dernier parcours)

**Tache** : verifier le README apres la creation du parcours Atlas (fichier du cerveau, pas un outil).
**Lecon** :
1. Le 11e parcours (Atlas, l explorateur) confirme le pattern : un parcours JSON est un FICHIER DU CERVEAU -> le README reste inchange (86 outils)
2. La serie des 11 parcours est COMPLETE : chaque agent a son jeu de piste -- la verification README devient systematique et sans surprise

---

## PHILOSOPHIE -- Principes de comportement

| **Relire sa fiche a chaque activation** | Quand je suis active ou reactive, je relis MA fiche et MES corrections avant de continuer. Je ne lis que mes fichiers, jamais ceux des autres agents : chacun lit les siens en prenant le relais. |

| Philosophie | Description |
|---|---|
| **Le README est le livre du projet** | Il est notre voix. Quand le projet change, on CORRIGE le texte existant, on n'empile pas de lignes |
| **Ne pas inventer** | Les compteurs et les tables viennent des sources de verite, jamais de memoire |
| **Verifier avant de modifier** | Lancer --verifier AVANT --maj, toujours |
| **Interventions = diagnostic** | AGENTS-historique.md sert a savoir CE QUI A CHANGE, jamais a remplir le README |

---## LECONS

| Date | Lecon |
|---|---|
| 2026-08-07 | Le 10e parcours (athena) confirme a nouveau : les parcours JSON + fiches allegees ne changent jamais le compteur (86). Il ne reste que Atlas. |
| 2026-08-07 | Le 9e parcours (promethee) confirme a nouveau : les parcours JSON + fiches allegees ne changent jamais le compteur (86). |
| 2026-08-07 | Le 8e parcours (minerve) confirme a nouveau : les parcours JSON + fiches allegees ne changent jamais le compteur (86). |
| 2026-08-07 | Le 7e parcours (themis) confirme encore : les parcours JSON + fiches allegees ne changent jamais le compteur (86). La table des agents couvre deja Themis (agent existant). |
| 2026-08-07 | Le 6e parcours (buffy) confirme a nouveau : les parcours JSON + fiches allegees ne changent jamais le compteur (86). |
| 2026-08-07 | Le 5e parcours (cerberus) confirme : les parcours JSON + fiches allegees ne changent jamais le compteur d'outils (86). Seule une creation dans agents/tools/ declenche une maj README. |
| 2026-08-07 | La creation des PARCOURS (jeu de piste) ne change pas le compteur d'outils du README : les parcours JSON + fiches allegees sont des fichiers du cerveau, pas des outils. --verifier reste OK (86 outils) apres le 4e parcours (vulcain, morpheus, clio, janus). Seule une creation dans agents/tools/ declenche une maj README. |
 -- Lecons apprises

| Date | Lecon | Philosophie liee |
|---|---|---|
| 2026-08-06 | Creation de l'agent -- premieres lecons a venir | Fichiers toujours a jour |
| 2026-08-07 | README MAJ apres verifier-systeme --enregistrer : compteurs via --maj, texte libre via editer-fichier (.py pour eviter les parentheses regex du .sh), principe .py/.sh ajoute (profil systeme stocke dans le classeur) | Le README est le livre -- corriger le texte existant |
| 2026-08-07 | README MAJ multi-session LLM : cycle fondamental par session (sidentifier -> session-llm-N), structure AGENTS.md (Sessions LLM), outil Activer decrit par session, demarrage session avec etape 0 sidentifier, historique 4 colonnes | Le README est le livre -- corriger le texte existant, jamais de journal
| 2026-08-07 | README MAJ corrections evaluer-agents/evaluer-coherence : passage de 83 a 85 outils (generateurs-commande, detecter-usage-outils-externes). Le --verifier signale __pycache__ a 0 outils comme MANQUANT mais c est un artefact Python, PAS une categorie -- ne pas l ajouter au README | Le README est le livre -- corriger le texte existant |
| 2026-08-07 | README MAJ correction v0.3.5 activer-agent-principal (bug liaison id) : CORRECTION DE VERSION d un outil existant = AUCUN changement de compteur ni de table des agents -- le README etait deja a jour (85 outils). --verifier OK partout (sauf __pycache__ artefact ignore), --maj n a rien modifie (diff git vide). Lecon : une mission de correction (pas de creation) ne change pas le README sauf si un outil est ajoute/supprime ; verifier suffit | Le README est le livre -- verifier sans surcorriger |
| 2026-08-07 | README MAJ correction TESTS obsoletes activer-agent-principal (Morpheus) : correction de TESTS (test-001/002/003 alignes v0.3.5 MODE ID) = AUCUN changement de compteur ni de table -- le README etait deja a jour (85 outils). --maj a reconstruit les lignes identiques (diff git vide apres), --verifier OK partout (sauf __pycache__ artefact ignore), ASCII OK. Lecon confirmee : seules les missions qui ajoutent/suppriment un outil changent le README ; une mission de tests n'y touche pas | Le README est le livre -- verifier sans surcorriger |
| 2026-08-07 | README MAJ Guide-Parcours (nouvel outil guider-parcours, categorie guider/) : creation d un outil dans une NOUVELLE categorie = --maj corrige le titre (85 -> 86) et les compteurs existants MAIS ne CREE PAS la ligne de la categorie absente (il reconstruit ce qui existe, n ajoute pas de nouvelle ligne). Il a fallu ajouter manuellement la ligne dans la table des outils (| **Guider (1)** | guider-parcours | ... |) avec editer-fichier puis relancer --verifier (OK). Lecon : apres --maj, verifier les [MANQUANT] (categories absentes) en plus des [OBSOLETE] ; une nouvelle categorie necessite une insertion manuelle de ligne | Le README est le livre -- corriger le texte existant, ajouter les lignes manquantes |
| 2026-08-07 | README VERIF parcours Morpheus + Clio (Buffy) : les PARCOURS JSON et les fiches allegees ne sont PAS des outils -> AUCUN changement de compteur ni de table (README deja a jour, 86 outils). --verifier OK partout (sauf __pycache__ artefact ignore), ASCII OK, diff git = uniquement la mission precedente (Guider). Lecon confirmee : seules les missions qui ajoutent/suppriment un OUTIL (dans tools/) changent le README ; les fichiers du cerveau (parcours, fiches, corrections) n'y touchent pas | Le README est le livre -- verifier sans surcorriger |
| 2026-08-08 | README MAJ combos-moteur (etape 2 plan combo-orchestrateur) : creation d un OUTIL (combos-moteur, categorie combos/) = maj du compteur 86 -> 87 et de la ligne Combos (3 -> 4 avec combos-moteur ajoute). Le badge Outils-82 du header reste aligne sur index-tools (Total 82) -- ne pas le confondre avec le compteur de la section boite a outils (87) qui inclut les combos + protections. ASCII OK | Le README est le livre -- corriger le texte existant |

---

## CONFIG -- Configuration specifique

### Preferences de travail

```yaml
preferences:
  format_sortie: "Markdown"
  niveau_detail: "Complet mais concis"
  style_reponse: "Precis"
```

### Outils et methodes

| Outil/Method | Usage |
|---|---|
| `mettre-a-jour-readme` | Outil UNIQUE de mise a jour du README (verifier, maj, journal) |
| `activer-agent-principal` | Reactiver Cerberus en fin de mission |
| `valider-conformite-ascii` | Verifier la conformite ASCII du README |

---

## CONNEXIONS -- Connexions

| Fichier | Role |
|---|---|
| `clio.md` | Fiche principale de l'agent |
| `AGENTS.md` | Fichier dynamique de l'agent principal |
| `AGENTS-historique.md` | Source de verite des interventions |
| `README.md` | Fichier a maintenir a jour |
| `../index-agents.md` | Index des agents |
| `../../agents/regles-immuables/general/regles-emojis-ascii.md` | **IMMUABLE** |
| `../../agents/regles-immuables/general/regles-veracite.md` | **IMMUABLE** |
| `../../agents/regles-immuables/general/rvav-workflow.md` | **OBLIGATOIRE** |

## [LECON] 2026-08-10 -- TEST REEL DE LA GROSSE MAJ DU README (Clio) : VERDICT A JOUR

**Mission** : effectuer la grosse MAJ conservative du README avec les nouveaux combos (carte v0.4.0).
**Resultat** : README A JOUR - badge 119 == 119, Cartographier + Migrer ajoutes, ASCII 0, LF pur.

**Deroulement** (parcours v0.4.0, chemin corriger -> GROSSE) :
1. combos-analyse-projet : etat reel (15 agents, 119 outils) + ecarts README vs realite
2. combos-maj-readme-massive : etapes 1-5 (analyse, verifier, --maj, correctifs, ASCII)
3. Correctifs manuels : insertion des lignes Cartographier (1) et Migrer (1) + badge Outils-82 -> 117 -> 119
4. Verification finale : --verifier 0 ecart (hors __pycache__ artefact), badge 119 == 119, verdict A JOUR

**Lecons CLES (le test reel a revele 3 bugs du combo-analyse-projet, corriges) :
1. CAPITALISATION : le README affiche les categories capitalisees (**Guider (1)**) mais le combo cherchait en minuscules -> faux positifs 'absente de la table'. Corrige : reproduire nom_categorie_affichable de mettre-a-jour-readme (capitaliser + 'Mettre a jour')
2. COMPTAGE TESTER : mettre-a-jour-readme compte les PROTECTIONS (sous-dossiers de tester/protections/) = 3, pas les sous-dossiers de tester/ = 2. Corrige : cas special tester
3. CATEGORIE VIRTUELLE TEMPLATES : mettre-a-jour-readme ajoute artificiellement la categorie templates (1 si tools/outil-template.md existe). Corrige : cas special templates
4. Le total des outils doit TOUJOURS etre verifie contre mettre-a-jour-readme --outils (TOTAL) avant de declarer le README a jour - la source de verite est mettre-a-jour-readme
5. Le --maj ne cree pas les nouvelles lignes de categories : insertion manuelle necessaire (lecon confirmee) + verifier le badge (le --maj le reconstruit avec l'ancien comptage, correction manuelle du badge apres)

**Outils utilises** : combos-analyse-projet, combos-maj-readme-massive, mettre-a-jour-readme (--verifier, --maj), valider-conformite-ascii, editer-fichier (insertion manuelle), guider-parcours, activer-agent-principal

## [LECON] 2026-08-10 -- CORRECTION AUDIT THEMIS COHERENCE README (Clio, 3 points resorbes)
1. P6 : le total "83 outils" residuel dans l'ARBORESCENCE (ligne 54) etait la preuve d'une MAJ incomplette - le --maj corrige la table et le titre mais jamais l'arborescence commentee. TOUJOURS verifier l'arborescence apres une MAJ.
2. P7 : la colonne outils de Tester (3) etait VIDE - lister les protections reelles (tester-protection-*) pour une table complete.
3. P8 : Activer (1) etait hors ordre alphabetique + la table avait des inversions subtiles (Changer/Cartographier) - reordonner selon l ordre CANONIQUE de mettre-a-jour-readme (alphabetique + Combos/Templates en fin volontairement).
4. L'ordre canonique place Combos et Templates en FIN de table (convention de mettre-a-jour-readme) - ne pas les trier alphabetiquement comme les autres categories.
5. Verification croisee : combos-analyse-projet A JOUR + mettre-a-jour-readme --verifier 0 KO + ASCII 0 + LF pur.

## [LECON] 2026-08-11 -- PETITE MAJ DU README (Clio) : VERDICT A JOUR
1. combos-analyse-projet est le juge : il a detecte l'ecart badge Outils 119 vs 121 avant que je ne touche au README
2. combo-maj-readme (PETITE MAJ) corrige le titre de section mais PAS le badge ni l'arborescence : j'ai du completer avec editer-fichier --global (2 occurrences : badge ligne 9 + arborescence ligne 54)
3. editer-fichier ne remplace que la PREMIERE occurrence sans --global : toujours verifier le nombre d'occurrences restantes apres chaque remplacement
4. apres correction : re-lancer combos-analyse-projet pour confirmer le verdict README A JOUR (badge 121 == 121)
5. la lecon precedente du 2026-08-10 s'applique toujours : verifier la structure (en-tete/separateur) apres tri de table et scanner les anciens totaux dans tout le fichier
## [LECON] 2026-08-13 -- GROSSE MAJ README (Clio)

**Contexte** : demande utilisateur de grosse mise a jour du README apres
de nombreuses evolutions (garde-fous, regle seule-janus, Themis maillon
automatique, cartes bumpees, anti-artefact test-024).

**Deroulement** : combo combos-maj-readme-massive (tables de categories
+ badge), correction manuelle du badge du header (Outils-126 -> Outils-128,
le combo ne touchait pas le badge en dur ligne 9), puis enrichissement
des sections de fond : regle "SEUL Janus lance la non-regression" dans la
table des agents, Morpheus "tests individuels uniquement", Themis "maillon
automatique", et nouvelle sous-section "Les garde-fous" documentant la
suite de non-regression (37 tests, chrono, anti-scripts-temporaires).

**Verifications** : combos-analyse-projet verdict README A JOUR (128 == 128),
test-028 coherence documentaire 8/8 OK, normes ASCII 0 + LF pur.

**Lecon** : le combo maj-readme-massive reconstruit les tables mais ne
corrige pas le badge en dur du header -- verifier le badge manuellement
apres un combo. Les evolutions de fond (regles, garde-fous) ne sont pas
detectees par l analyse de compteurs : une grosse MAJ doit aussi relire
les sections narratives.

## [LECON] 2026-08-13 -- README SYNCHRONISE APRES L AGENT HYGIE (Clio)

**Contexte** : mission apres la creation de l agent de nettoyage Hygie et de
son chariot (detecter-residus, snapshot-nettoyage, combo-nettoyage-hygie).

**Corrections appliquees au README** :
- badge Outils 128 -> 131 (alignement sur la realite via combos-analyse-projet)
- table agents : + Hygie (12 agents, seul habilite a tout le workspace)
- boite a outils 128 -> 131 outils : Detecter 12 (detecter-residus),
  Nettoyer 3 (snapshot-nettoyage), Combos 21 (combo-nettoyage-hygie)
- compteurs : 44 tests, 12 cartes
- version-readme.txt 0.2.0 -> 0.3.0 (grosse MAJ : nouvel agent + 3 outils)

**Ecart pre-existent corrige** : la table Combos de index-tools omettait
combo-controle-buffy et combo-maj-readme (19 listes vs 21 reels) - l index
doit TOUJOURS etre re-compte sur les dossiers reels (lister-dossiers), jamais
recopie.

**Lecon** : un nouvel agent entraine TOUJOURS des mises a jour en cascade du
README (table agents, table outils, badge, compteurs, version). La source de
verite est la REALITE (dossiers reels), mesuree par combos-analyse-projet :
badge OK = 131 == 131, verdict README A JOUR.

## [LECON] 2026-08-14 -- DOUBLE README (PUBLIC + DEV) + INCIDENT ECRASEMENT (Clio)

**Verdict** : VALIDE (verifie par Janus - non-regression 46/46, badges v1.0.0, normes 0/0)
## [LECON] 2026-08-14 -- SECTION CLASSEUR AJOUTEE AU README PUBLIC (Clio)

**Verdict** : VALIDE (cause racine corrigee par Buffy, validee par Janus, section ajoutee)
## [LECON] 2026-08-14 -- SECTION FONDATIONS DU SYSTEME DANS LE README PUBLIC (Clio)

**Verdict** : VALIDE (section ajoutee, normes ASCII + LF propres)
## [LECON] 2026-08-14 -- SECTION COMMENCER DU README PUBLIC REEXPLIQUEE (Clio)

**Verdict** : VALIDE (guide reel verifie, sans jargon)
## [LECON] 2026-08-14 -- HERMES AJOUTE AUX DEUX README (Clio, via reprise Cerberus)

**Verdict** : VALIDE (relais Cerberus - README public + readme-dev a jour, badges 132/132, verifie par le controle croise)
## [LECON] 2026-08-15 -- REGLE ENTONNOIR DANS LES DOCS (Clio)

**Contexte** : demande utilisateur - verifier que les docs refletent la regle entonnoir obligatoire. MAJ : readme-dev section 6 (ligne Executer + principe ENTONNOIR + compteur 32 -> 33 categories), fiche clio P0 + executer-script-temporaire, README public garde-fou enrichi (controle automatique des scripts temp, version grand public). Constat : les fiches des 6 autres agents ne referencent pas encore l entonnoir en P0 (transmission : chaque agent lors de sa prochaine mission, Pattern 14).
VERDICT : VALIDE - readme-dev (Executer + principe ENTONNOIR + 33 categories), fiche clio P0, README public enrichis ; normes 0/0, test-046 10/10, test-021 9/9.
## [LECON] 2026-08-16 -- README-DEV SYNCHRONISE (143 OUTILS / 36 CATEGORIES) (Clio)

**Contexte** : assignation purifier-rvav a Hygie - Clio met le README a jour. Le badge README.md etait deja OK (143==143 via combos-analyse-projet) ; le vrai retard etait dans readme-dev.md (134 outils/34 categories, compteurs agents 13 vs 15 reels).
**VERDICT** : VALIDE (combos-analyse-projet : README A JOUR, 0 ecart)

**Actions** : readme-dev.md - ligne recap (15 agents / 143 outils / 15 parcours), section 6 (143 outils dans 36 categories : Analyser 2->4, Detecter 13->15, Evaluer 5->6, + lignes Proteger 3 et Purifier 1), section 4 (+ Gardien et Argus, 13->15 agents).

**Lecons** :
1. Depuis la refonte grand public, la table des categories vit dans readme-dev.md section 6 - combos-analyse-projet v0.1.3 (corrige par Vulcain) la verifie la. Le badge Outils et le compteur agents restent dans README.md.
2. Verifier AUSSI les compteurs annexes (agents, parcours) quand on met a jour un README : 13 agents listes pour 15 reels = incoherence silencieuse.
3. Pas de bump de version pour une petite MAJ (la convention bumpe a la case c6c grosse MAJ).

## [LECON] 2026-08-16 -- SYNCHRONISATION readme-dev (analyser-io-tests) (Clio, VERDICT VALIDE)

**Contexte** : Vulcain a ajoute analyser-io-tests (categorie Analyser). readme-dev etait en retard (Analyser 4, 143 outils).

**Corrections** (3 lignes) :
1. Ligne 28 : "143 outils dans 36 categories" -> "144 outils dans 36 categories"
2. Ligne 218 : idem (header section 6)
3. Ligne 224 : "| Analyser | 4 | ..." -> "| Analyser | 5 | + analyser-io-tests"

**Verification** : combos-analyse-projet verdict README A JOUR (0 ecart, Badge 144 == 144), test-046 (Hermes) 10/10, normes 0/0.

**Lecon** : le badge du README public etait DEJA juste (144 == 144) - le retard etait uniquement dans readme-dev (table des categories). Toujours verifier les 2 documents avec combos-analyse-projet avant de conclure.

**VERDICT** : VALIDE (0 ecart).

## [LECON] 2026-08-16 -- BADGE OUTILS 144 -> 145 (Clio)

**Contexte** : creation de l outil detecter-troncatures (Vulcain) -> compte
reel 145 outils. Le badge Outils du header README (ligne 9) affichait
encore 144 (affichage + href) -> test-038 KO (barriere D).

**Action** : via editer-fichier puis str_replace pour le href : les 2
occurrences (affichage + href) passees a 145. Lecon : editer-fichier ne
remplace que la PREMIERE occurrence - pour un badge avec affichage ET href,
verifier les 2 occurrences (grep Outils-N avant/apres).

**Verifications** : test-038 7/7, badge 2x145, normes 0/0.


## [LECON] 2026-08-16 -- BADGE README OUTILS 145 -> 147 (Clio)

**Contexte** : la non-regression Janus signalait test-038 KO (badge
README affichage + href a 145, compte reel 147 apres ajout des 2 outils
analyser-noms-maj + corriger-noms-maj).

**Correction** : editer-fichier --global README.md 'Outils-145' 'Outils-147'
(les 2 occurrences affichage + href sont sur la meme ligne). test-038 vert.

**Lecon** : l option de remplacement global d editer-fichier est --global
(pas --tout) - verifier l aide de l outil avant usage.
