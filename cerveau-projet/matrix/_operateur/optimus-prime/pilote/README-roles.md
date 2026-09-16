---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
---

# Roles d'Optimus -- QUI conduit la mission

## Pourquoi

Le cameleon a **UNE personnalite par mission**, choisie par la Matrice dans le
VIVIER (categorie `PERSONNALITE`), **jamais par lui**. Optimus n'en avait
**aucune** : ses missions ne portaient qu'un **theme de chantier** (`REPARATION`,
`OUTIL`, `PILOTE`...) -- le **QUOI** toucher, jamais le **QUI** conduit. Et le
catalogue d'injection lui **deversait la fiche ENTIERE** (220 lignes) au
demarrage, au lieu de lui fournir la conduite **au moment ou elle sert**.

Une mission commencee sans posture laisse l'agent improviser sa conduite. C'est
precisement ce que le pilote doit fournir **AVANT** la mission.

## Le mappage ferme (porte par le PILOTE, jamais par l'agent)

Table unique : `pilote/personnalites.py` (`POSTURE_PAR_TYPE`), meme mappage que la
fiche du cameleon -- une seule doctrine de posture pour tout le cerveau-projet.

| Type de mission | Posture (vivier) | Id |
|---|---|---|
| `dev` | CONSTRUCTEUR | TH-017 |
| `reparation` | REPARATEUR | TH-021 |
| `doc` | REDACTEUR | TH-018 |
| `audit` | AUDITEUR | TH-019 |
| `revision` | REVISEUR | TH-020 |

Regles du mappage :

1. **COMPLET** : chaque type de l'entonnoir (`entonnoir/listes.py`, `TYPES`) a
   une posture. Un trou est crie **au chargement** du module (L-037 : un
   garde-fou qui peut etre vide est un garde-fou absent).
2. **REEL** : chaque posture est un theme du VIVIER de categorie `PERSONNALITE`.
   Un theme de **chantier** deguise en posture est **refuse et nomme** (une
   posture dit **QUI**, pas **QUOI**).
3. **DONNE, jamais choisi** : l'agent ne choisit pas sa posture ; il la recoit du
   pilote au debut de sa mission.

## Le ROLE d'une mission : deux choses, chacune nommee

Le ROLE porte **DEUX** champs distincts (`pilote/injection/fonctions.py`,
`charger_role_mission`) :

| Champ | Sens | Source |
|---|---|---|
| `posture` | **QUI** conduit | table fermee `personnalites.py`, deduite du **TYPE** |
| `theme` | **QUOI** toucher | champ `theme` de la mission (deja FERME, le vivier) |

Chaque nom est accompagne de son **item du vivier** (`posture_declaree`,
`chantier_declare`) : le pilote remet la **conduite declaree**, pas une paraphrase.

Si le **type manque**, la posture manque et l'ecart est **DIT** dans le role
(`POSTURE ABSENTE`) : c'est la **carte d'identite de mission** qui doit le poser.

## Ou le role est injecte

| Moment | Ce qui part | Ou |
|---|---|---|
| **avant-mission** | les **postures** du vivier (entree `role` du catalogue) | `pilote/injection/config.json` -> `injecter.py` |
| **la mission** | le **ROLE** compose (`posture` + `theme` + items declares) | `pilote/injection/fonctions.py` -> outbox intercom |

L'injection **simple** (`preparer_injection`) et l'injection de **lot**
(`enchainer`) portent **toutes les deux** le role : deux copies d'un mecanisme
donneraient un chemin protege et l'autre non.

## Le garde

`super-combos/combos/outils/verifier-roles.py` (maillon **22** de la
non-regression, BLOQUANT) verifie les quatre exigences ci-dessus et se **piege**
lui-meme (cobaye 4/4 : table complete acceptee, table trouee accusee, posture
inventee accusee, theme de chantier refuse comme posture).

## Suites du chantier (declare, en serie)

- **MAILLON 3** : la **carte d'identite de mission** (chaque mission porte son
  type, sa categorie et son role -- le pilote peut alors injecter la posture sans
  ecart).
- **MAILLON 4** : le **moteur de recherche** cable dans le catalogue d'injection
  (extraits cibles AVANT / PENDANT / APRES).
- **MAILLON 5** : la **fiche MINIMALE** (`optimus-prime.md` reduit a `agir avec
  le createur + utiliser le pilote`).
