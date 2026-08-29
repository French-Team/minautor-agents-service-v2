---
identite:
  type: rapport
  appartient_a: themis
  date: 2026-08-22
  statut: definitif
  categorie: bilan-v1
---

# Bilan V1 -- Ce qu'on garde, ce qu'on laisse, ce qu'on apprend

**Date** : 22 aout 2026
**Agent** : Themis
**Contexte** : Bilan honnete de la v1 pour informer la v2

---

## I. Les chiffres de la v1

| Metrique | Valeur |
|---|---|
| Outils scripts (.py) | 250 |
| Tests de non-regression | 97 |
| Agents | 19 (+ redacteur-v2 freelance) |
| Taille du cerveau-projet | 28 Mo |
| Taille des outils seuls | 11 Mo |
| Lecons enregistrees | 188+ |
| Duree de vie v1 | ~12 jours (10-22 aout 2026) |

---

## II. CE QUI A VRAIMENT MARQUE (les reussites)

### 1. Le systeme de lecons (BDD SQLite)
**Verdict** : EXCELLENT -- le meilleur investissement de la v1.

- 188+ lecons enregistrees par 12 agents differents
- La BDD est devenue la **memoire longue** du projet
- Chaque agent pouvait consulter l'experience des autres (c0e)
- Les lecons ont empeche la reiteration de erreurs
- **A garder en v2** : la BDD de lecons, le flux c0e, la pollinisation croisee

### 2. Les cartes de decision (parcours JSON)
**Verdict** : TRES BON concept, execution imparfaite.

- Chaque agent a une carte qui definit son perimetre
- Le guider-parcours guide l'agent case par case
- Les branches conditionnelles permettent des chemins differents
- **Probleme** : les cartes sont devenues des monstres (30+ cases par carte)
- **A garder en v2** : le concept de carte, mais avec des cartes plus simples
- **A changer** : les cartes doivent etre plus courtes, plus claires, moins de branches

### 3. Le systeme de non-regression
**Verdict** : BON mais trop complexe.

- 97 tests qui verifient que rien ne casse
- Le protocole de tests est rode
- Les pins protegent les versions critiques
- **Probleme** : les tests sont devenus un Far West (97 tests, chacun avec ses regles)
- **A garder en v2** : le principe, mais avec un framework plus simple
- **A changer** : 10-15 tests max, pas 97

### 4. La separation des domaines (3 groupes)
**Verdict** : BONNE regle.

- Coordination (Cerberus) / Cerveau-projet (Buffy+equipe) / Trio projets futurs
- Chaque agent a SON domaine, ne depasse pas
- **Probleme** : les violations etaient frequentes (Buffy activee pour des outils domaine Vulcain)
- **A garder en v2** : le principe des groupes
- **A changer** : les groupes v2 (Coordination / Freelance / Futurs)

### 5. Le marbre (zones protegees)
**Verdict** : BON concept, execution lourde.

- Protege les zones critiques du code
- Agent specialement habilite (Gardien) pour modifier
- **Probleme** : trop de zones protegees, trop de verrous, ralentissait tout
- **A garder en v2** : le principe mais allige

### 6. Le versionning des outils
**Verdict** : UTILE mais trop manuel.

- Chaque outil a un numero de version
- Les pins protegent les versions critiques
- **Probleme** : le bump de version est devenu un rituel de 10 minutes a chaque modification
- **A garder en v2** : le principe
- **A changer** : automatiser le bump

---

## III. CE QUI A FOIRE (les problemes)

### 1. La surcharge d'outils
**Verdict** : CATASTROPHE -- le plus gros probleme de la v1.

- 250 outils pour 19 agents = 13 outils par agent en moyenne
- Beaucoup d'outils se chevauchent (corriger-accents, corriger-emojis, corriger-fins-de-ligne...)
- Les agents ne connaissaient pas tous les outils disponibles
- La maintenance de 250 outils est un cauchemar
- **A corriger en v2** : 20-30 outils max, pas 250

### 2. Le verrou d'habilitation
**Verdict** : PROBLEMATIQUE -- a plus creuse qu'il n'a protege.

- Chaque outil avait un "qui peut l'utiliser"
- Les agents etaient bloque quand ils n'avaient pas les droits
- Les "inter-rounds" etaient des boucles de reparation interminables
- **Lecon** : la securite par restriction excessive paralyse le systeme
- **A changer en v2** : les grades (copper->diamond) definissent les droits, pas des verrous

### 3. L'activation centralisee par Cerberus
**Verdict** : EFFICACE mais limitant.

- Cerberus etait le point d'entree unique -- bon principe
- Mais TOUT passait par Cerberus -- il est devenu un goulet d'etranglement
- Les chaines d'activation (A->B->C) etaient lentes
- **A corriger en v2** : JARVIS route les agents, Cerberus garde l'entree/sortie

### 4. Les corrections interminables
**Verdict** : SPIRALE -- on corrigeait les corrections des corrections.

- Chaque agent avait un fichier corrections.md qui grossissait
- Les corrections etaient parfois contradictoires
- Le systeme devalait plus qu'il n'evaluait
- **A corriger en v2** : corrections courtes, directes, sans spirale

### 5. Le format ASCII/CRLF
**Verdict** : PERTINENT mais trop present.

- La detection de non-ASCII et CRLF etait importante
- Mais elle polluait 80% des rapports d'audit
- **A garder en v2** : le check, pas le bruit
- **A changer** : silencieux sauf en cas de probleme

### 6. Les tests de non-regression
**Verdict** : DEBORDES -- le systeme a depasse son but.

- 97 tests, chacun avec ses pins, ses profils, ses garde-fous
- La maintenance des tests prenait plus de temps que le developpement
- Les tests ont cree des problemes qu'ils etaient censes detecter
- **A corriger en v2** : tests simples, sans pins, sans garde-fous internes

---

## IV. CE QU'IL FAUT GARDER (les fondations v2)

| Element | Pourquoi | Comment v2 |
|---|---|---|
| **BDD lecons** | Memoire longue, pollinisation croisee | Meme principe, meme flux |
| **Cartes de decision** | Guide l'agent, formalise le perimetre | Plus simples, moins de branches |
| **Separation des domaines** | Evite les conflits | Groupes v2 (Coordination/Freelance) |
| **Protocole de fin de mission** | Documentation obligatoire | Meme principe |
| **Marbre (allige)** | Protege les zones critiques | Zones reduites, pas tout |
| **Pattern 8 (chaines)** | Agents activent les suivants | Via JARVIS, pas activer-agent-principal |

---

## V. CE QU'IL FAUT LAISSER (les fardeaux)

| Element | Pourquoi l'abandonner |
|---|---|
| **250 outils** | Trop, chevauchement, maintenance impossible |
| **97 tests** | Trop, les tests creent des problemes |
| **Verrous d'habilitation** | Paralyse le systeme, les grades suffisent |
| **Bumps de version manuels** | Rituel inutile, automatiser |
| **Corrections.md interminables** | Spirale, courtes et directes |
| **Bruit ASCII/CRLF** | Silencieux sauf probleme |
| **Templates v1** | Remplaces par templates MARVEL |
| **Noms mythologiques** | Remplaces par noms MARVEL |

---

## VI. LES LECONS CLES DE LA V1

### Lecon 1 : "Moins c'est plus"
- 250 outils n'est pas mieux que 30
- 97 tests n'est pas mieux que 15
- La complexite est l'ennemi de la fiabilite

### Lecon 2 : "La securite par restriction excessive tue"
- Les verrous d'habilitation ont paralyse les agents
- Les grades (copper->diamond) sont suffisants
- Faire confiance aux agents, pas aux mecanismes

### Lecon 3 : "Les outils doivent etre simples"
- Un outil = un script + un .md + un fichier de donnees
- Pas de base de donnees, pas de serveur
- Editable a la main, pas de framework complexe

### Lecon 4 : "Les tests doivent etre simples"
- Un test = un script qui verifie une chose
- Pas de pins, pas de profils, pas de garde-fous
- Si un test casse, on le corrige, on ne le contourne pas

### Lecon 5 : "La documentation vivante"
- Les corrections.md doivent etre courtes
- Les lecons BDD sont la vraie memoire
- Pas de doubles, pas de contradictoires

### Lecon 6 : "Les outils au bon endroit"
- Chaque agent a ses outils dedies
- Les outils communs restent communs
- Pas de melange, pas de duplication

### Lecon 7 : "JARVIS change tout"
- La communication inter-agents doit etre centralisee
- Pas de signaux directs entre agents
- Tout passe par un hub (JARVIS)

### Lecon 8 : "L'activation doit etre transparente"
- Les agents ne doivent pas savoir comment ils sont actives
- JARVIS gere l'activation, l'historique, les messages
- Stark coordonne, JARVIS execute

---

## VII. RECOMMANDATIONS POUR LA V2

| # | Recommandation | Priorite |
|---|---|---|
| 1 | 20-30 outils max, pas 250 | HAUTE |
| 2 | 10-15 tests max, pas 97 | HAUTE |
| 3 | JARVIS comme hub central | HAUTE |
| 4 | Grades au lieu de verrous | HAUTE |
| 5 | Templates MARVEL (agent + outil) | HAUTE |
| 6 | Cartes simples (< 15 cases) | MOYENNE |
| 7 | BDD lecons conservee | MOYENNE |
| 8 | Marbre allige (zones reduites) | MOYENNE |
| 9 | Corrections courtes et directes | MOYENNE |
| 10 | Outils editables (fichiers de donnees) | BASSSE |

---

## VIII. VERDICT FINAL

La v1 a ete un **laboratoire exceptionnel**. En 12 jours, on a construit un ecosysteme complet de 19 agents, 250 outils, 97 tests, et 188 lecons. Le systeme a fonctionne, a appris, a evolue.

Mais la v1 a aussi ete **victime de son succes** : en voulant tout faire, on a tout complexifie. 250 outils, 97 tests, des verrous partout, des corrections interminables -- c'est le signe qu'on a depasse le stade du prototype.

La v2 doit etre **l'inverse de la v1** : simple, efficace, autonome. JARVIS remplace le routing complexe. Les grades remplacent les verrous. 30 outils remplacent 250. 15 tests remplacent 97.

**Ce qu'on garde** : les lecons, les cartes (simplifiees), la separation des domaines, le protocole de fin de mission.

**Ce qu'on laisse** : la surcharge, les verrous, la complexite, le bruit.

**Ce qu'on construit** : JARVIS, les templates MARVEL, les grades, l'autonomie v2.

---

> "La simplicite est la sophistication supreme." -- Leonard de Vinci
