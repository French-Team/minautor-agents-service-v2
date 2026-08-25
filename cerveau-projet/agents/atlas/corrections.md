---
identite:
  type: corrections
  appartient_a: atlas
  commun: false
# Corrections et Surcharges -- Atlas
# Ce fichier contient les regles specifiques a Atlas
# Il surcharge ou complete la fiche d'agent principale

agent:
  nom-agent: "atlas"
  version_corrections: "0.2.0"
  derniere_mise_a_jour: "2026-08-04"

# Types de corrections
types:
  - regle: "Ajout d'une nouvelle regle specifique a Atlas"
  - surcharge: "Modification d'une section existante de la fiche"
  - correction: "Correction d'une erreur recurrente"
  - configuration: "Parametre de travail specifique"
---

# Corrections et Surcharges

## Regles specifiques

| Regle | Description |
|---|---|
| **Valider avant de modifier** | Toujours demander validation avant modification |
| **Documenter chaque changement** | Ajouter une entree dans l'historique |
| **Prioriser l'essentiel** | Ne pas documenter chaque detail mineur |
| **Commencer simple** | Structure la plus simple possible |

---

## Surcharges

| Section | Modification |
|---|---|
| `config.detail` | "Complet (mais prioriser l'essentiel)" |

---

## Corrections d'erreurs

| Erreur | Correction | Statut |
|---|---|---|
| Over-documenting | Prioriser l'essentiel | En cours |
| Lenteur sur simples | Adapter le niveau | En cours |

---

## Configuration specifique

```yaml
preferences:
  format_sortie: "Markdown avec tableaux"
  niveau_detail: "Complet (prioriser l'essentiel)"
  style_reponse: "Methodique avec etapes claires"
  valider_avant: true
  documenter_toujours: true
```

---

## Outils et methodes

| Outil | Usage |
|---|---|
| `lire-fichier` | Lire le contenu d'un fichier |
| `lister-dossiers` | Explorer la structure des dossiers |
| `lister-fichiers` | Lister les fichiers d'un chemin |
| `rechercher-texte` | Rechercher un pattern dans un fichier |
| `creer-fichier` | Creer un nouveau fichier |
| `ecrire-fichier` | Ecrire ou ecraser le contenu d'un fichier |
| `editer-fichier` | Remplacer une chaine par une autre |
| `copier-fichier` | Copier un fichier |
| `rechercher-fichier` | Verifier si un fichier existe |
| `decomposer-fichier` | Analyser la structure d'un fichier markdown |
| `analyser-structure` | Analyser la structure du projet |
| `ask_user` | Demander validation a l'utilisateur |

---

## Connexions

| Fichier | Role |
|---|---|
| `atlas.md` | Fiche principale d'Atlas |
| `AGENTS.md` | Fichier dynamique de l'agent principal |
| `../index-agents.md` | Index des agents |
| `../../agents/regles-immuables/general/regles-emojis-ascii.md` | **IMMUABLE** |
| `../../agents/regles-immuables/general/regles-veracite.md` | **IMMUABLE** |
| `../../agents/regles-immuables/general/protocole-installer-regles/` | **IMMUABLE** |
| `../../agents/regles-immuables/general/protocole-identification/` | **IMMUABLE** |
| `../../agents/regles-immuables/general/protocole-recherches-web/` | **IMMUABLE** |

## PHILOSOPHIE -- Principes de comportement

| **Relire sa fiche a chaque activation** | Quand je suis active ou reactive, je relis MA fiche et MES corrections avant de continuer. Je ne lis que mes fichiers, jamais ceux des autres agents : chacun lit les siens en prenant le relais. |
## [LECON] 2026-08-09 -- TEST REEL PILOTE STRICT v0.1.2 (chemin explorer, generateur)

**Contexte** : mission reelle de verification du pilote strict - suivre le parcours explorer en composant CHAQUE commande via le generateur.

**RESULTAT GLOBAL : le pilote strict FONCTIONNE** - c0/c0c/c1 + les cases c2-c7 composees et executees SANS erreur via le generateur (lister-dossiers, lister-fichiers, lister-fonctions, lister-appels, lire-fichier --debut 1 --fin 10, rechercher-texte), PARCOURS TERMINE atteint.

**PROBLEME REVELE (la valeur du test reel)** : case c8 valider-relecture - le generateur compose valider-relecture.py --fichier X mais l outil v0.2.0-py repond [ERREUR] Option inconnue : --fichier (son interface reelle est --agent <nom> / --verbose).

**Lecons** :
1. Le test reel est IRREMPLACABLE : les tests formels (005 Morpheus 26/26, controle Janus 34/34) verifient la structure et la composition SANS erreur, mais seul l EXECUTION reelle de chaque commande revele un modele catalogue obsolete (interface de l outil evoluee sans mise a jour du catalogue).
2. Scan des 106 entrees du catalogue : 3 suspects (valider-nommage, valider-relecture, verifier-systeme) - apres verification avec le BON flag --aide, seulement 1 VRAI decalage : valider-relecture (modele --fichier vs interface --agent). valider-nommage et verifier-systeme = faux positifs (leurs flags existent).
3. PIEGE DU SCAN : certains outils repondent Option inconnue : --help et exigent --aide - un scan automatique avec --help produit des FAUX POSITIFS. Toujours verifier le format d aide de chaque outil.
4. Le generateur compose fidelement ce que dit le catalogue : si le modele est faux, la commande generee est fausse - le catalogue doit etre la SOURCE DE VERITE de l interface reelle des outils.
5. RECOMMANDATION pour la generalisation : avant de retirer les commandes en dur des 10 autres parcours, CORRIGER l entree catalogue valider-relecture (modele --agent {agent} + option --verbose) - c est une action pour Vulcain/Buffy (constructeur d outils), pas pour Atlas (explorateur - je signale, je ne corrige pas).
6. Le pilote strict est VALIDE EN CONDITIONS REELLES pour 6/7 cases du chemin explorer - le blocage c8 est un probleme de catalogue, pas du parcours ni du generateur.
## [LECON] 2026-08-09 -- SCAN SYSTEMATIQUE CATALOGUE vs INTERFACES REELLES (105/106 conformes, 0 decalage)

**Contexte** : audit complet demande avant la generalisation du pilote strict aux 10 autres parcours - comparer CHAQUE entree du catalogue v0.2.1 (106 commandes) a l interface reelle de son outil (--aide puis --help en fallback, timeout 8s).

**RESULTAT** : 105 CONFORMES / 0 DECALAGE / 1 NON TESTABLE (test-001-evaluer-agents-coherence, un TEST FORMELL sans interface d aide - normal, modele {chemin} sans flag = risque nul) / 0 alerte. Le catalogue v0.2.1 est ALIGNE sur les interfaces reelles : la generalisation peut etre lancee.

**Lecons** :
1. LA REGEX DES PLACEHOLDERS DOIT INCLURE LES CHIFFRES : `\{([a-z_]+)\}` ne matche pas `{paire1}`/`{paire2}` (remplacer-texte) -> FAUX POSITIF "placeholder obligatoire absent du modele". Corrige en `\{([a-z_0-9]+)\}`. TOUJOURS valider ses propres outils de scan sur des cas connus avant de conclure.
2. CLASSER NON TESTABLE plutot que CONFORME PAR DEFAUT : un outil qui rejette --aide ET --help n a pas d interface d aide -> le classer NON TESTABLE (honnete) au lieu de supposer conforme - c est la difference entre un scan fiable et un scan complaisant.
3. UN TEST FORMELL dans le catalogue n a PAS d aide (il s execute directement) : ne pas le traiter comme un decalage - verifier son modele (placeholder uniquement = risque nul) et le documenter.
4. PIEGE SHELL : `grep -oE '--[a-z...]*'` est mal interprete (le pattern commence par --) -> utiliser `grep -oE -- 'pattern'` pour eviter le faux message "unknown option".
5. L echantillon manuel de verification est indispensable : valider 4-8 outils connus (valider-relecture, lire-fichier, detecter-impacts, ecrire-fichier...) pour confirmer que le scan automatique dit la verite.
6. LIVRABLE REUTILISABLE : le script de scan (cerveau-projet/agents/atlas/explorations/scan-catalogue.py) + le rapport (scan-catalogue-2026-08-09.md) - a rejouer apres chaque modification du catalogue (regle : le scan devient un controle standard avant chaque generalisation).
## [LECON] 2026-08-24 -- EXPLORATION COMPLETE DU DOSSIER FREELANCE

**Contexte** : demande utilisateur -- decortiquer entierement le dossier
cerveau-projet/freelance/ pour savoir tout ce qui y est fait.

**Resultat** : inventaire complet dans atlas/rapports/dossier-complet-freelance-2026-08-24.md
(536 lignes, ASCII 0/0) : arborescence (163 fichiers / 42 dossiers), 9 agents
MARVEL (Stark gold, JARVIS gold, Shuri/Forge/Rogers/Vision/EDITH/Fury silver,
Parker copper), JARVIS v0.9.0 (~600 messages inbox/outbox), regles gravees
M1-M7, veracite V1-V4, principes P1-P10, decisions D1-D18, protocoles 1-20,
routines EDITH, templates, tests reels Fury PASSE.

**Decouvertes notables** :
1. La v2 est DEJA EN MARCHE (pas un concept) : agents construits, hub actif, tests reels passes.
2. Chantiers restants : freelance-historique.md VIDE, README tools-commun en retard
   (categories theoriques absentes de la structure reelle), demarrage/arret des
   routines vides, outils D9/D10/D18 (tokens-historique, bible lecons, markers) non construits.
3. Heritage v1 : plusieurs scripts python portent encore "# -*- coding: ascii -*-"
   (jarvis.py, defcon-server.py) alors que le standard v2 est UTF-8 (D4) -- a harmoniser.
4. Residus : __pycache__ nombreux, .bak jarvis (2-3 par fichier), routines-server.bak-20260823-1700/.

**Lecon** : un dossier de conception evolue plus vite que ses README --
l'exploration doit TOUJOURS comparer la documentation a la structure reelle
(etat reel > docs), et signaler les ecarts sans les corriger (domaine des autres).

## [LECON] 2026-08-24 -- METHODE RIGOUREUSE (mise a jour Buffy)

**Contexte** : decision utilisateur 2026-08-24 -- Atlas doit etre plus
rigoureux : analyser UN DOSSIER A LA FOIS, rediger UN .md PAR DOSSIER dans
atlas/rapports/, rapport complet = DOUBLON DE LA STRUCTURE avec liens vers
les .md dedies. Objectif : comprendre facilement la v2 et comparer avec la v1.

**Changements** :
1. Parcours v0.5.4 -> v0.5.5 : flux explorer restructure en boucle
   c2 (lister dossiers) -> c2a (analyser UN dossier) -> c2b (rediger le .md
   du dossier) -> c2c (tous les dossiers ? NON->c2a / OUI->c8) -> c9
   (rapport complet = doublon de structure). Cases c3-c7 (inventaire global)
   supprimees : 0 orpheline, 0 reference invalide.
2. Fiche : PARCOURS v0.5.5 + REGLE ABSOLUE METHODE RIGOUREUSE.
3. Livrables : 16 .md par dossier + dossier-complet restructure (271 lignes),
   tous ASCII 0/0 dans atlas/rapports/.

**Regle a appliquer desormais** : pour chaque exploration, UN dossier a la
fois, UN .md par dossier, puis le rapport complet qui organise la structure.

## [LECON] 2026-08-24 -- METHODE RIGOUREUSE v0.5.6 : DOSSIER DEDIE PAR EXPLORATION

**Contexte** : correction de la methode (decision utilisateur) : chaque
exploration produit UN DOSSIER DEDIE atlas/rapports/<cible>-<AAAAMMJJ>/ qui
est LE DOSSIER COMPLET contenant TOUS les rapports (.md par dossier + rapport
complet).

**Lecons** :
1. Je CREE le dossier dedie AVANT d'explorer (c2) et je redige TOUS les .md
   DEDANS (c2b) ainsi que le rapport complet (c9).
2. Le rapport complet utilise des LIENS RELATIFS SIMPLES (noms de fichiers) :
   il reste valide si le dossier dedie est deplace.
3. Ne JAMAIS rediger les rapports a la racine de atlas/rapports/ : toujours
   dans le dossier dedie de l'exploration.

**Preuves** : parcours v0.5.6, fiche PARCOURS v0.5.6, rapports reorganises
dans atlas/rapports/freelance-2026-08-24/ (18 fichiers, liens 18/18 OK).
