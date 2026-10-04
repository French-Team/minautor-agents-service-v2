---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# AUDIT MO-514 / EO-514 -- OU SONT STOCEES LES BDD DE LA v3 ?

Question du createur, telle qu elle est au brin :
"je voudrais savoir ou sont stockes les bdd de la v3 ?"

Posture AUDITEUR : lecture seule. Aucune reparation en douce. Cet audit
repond par la MESURE (les fichiers reels sur disque), pas par la memoire.

## 1. LA REPENSE COURTE

Les BDD de la v3 ne sont pas dans UN lieu : elles sont reparties par FONCTION,
sur deux territoires. Le coeur de la Matrice (`matrice/data/`) porte ce que la
Matrice sait de TOUT le systeme ; la zone privee de l operateur
(`_operateur/optimus-prime/`) porte ce que l operateur Optimus (Flux 2) sait de
LUI-MEME (le raisonnement, sa file, son entonnoir, son registre d integrite).

Une BDD n est donc pas "rangee" : elle a un DOMICILE, et ce domicile est decide
par la question a laquelle elle repond.

## 2. L INVENTAIRE MESURE (sur disque, ce jour)

### Coeur de la Matrice -- ce que TOUT le systeme doit savoir

| BDD | Fichier | Taille | Question a laquelle elle repond |
|---|---|---|---|
| Registre des outils | `matrice/data/registre-outils.json` | 113 956 o | quels outils existent, qui les possede |
| Lecons | `matrice/data/lecons.json` | 223 605 o | quel savoir-faire acquis, reutilisable |
| Sessions | `matrice/data/sessions.json` | 1 449 089 o | le journal de travail : qui a fait quoi, quand |
| Notes de modification | `matrice/data/modifications-par-fichier.json` | 2 004 054 o | le sac-a-dos des fichiers touches |
| Activites recentes | `matrice/data/activites-recentes.json` | 25 231 o | l activite recente, en tete de section |
| Conventions | `matrice/data/conventions-matrice.json` | 16 893 o | les regles de forme (nommage, integrite, prefixes) |
| Regles | `matrice/data/regles-matrice.json` | 6 699 o | les regles immuables |
| Protocoles | `matrice/data/protocoles-matrice.json` | 3 753 o | les protocoles d execution |
| Vivier des themes | `matrice/data/vivier-themes.json` | 11 873 o | les postures et les themes du vivier |
| Classeur de variables | `matrice/data/classeur-variables.json` | 1 867 o | les variables declarees, leur perimetre |
| Corvees | `matrice/data/corvees.json` | 8 753 o | le backlog connu |
| Conservation | `matrice/data/conservation.json` | 7 375 213 o | les points de restauration (reversibilite) |

### Zone privee de l operateur -- ce que Optimus sait de LUI

| BDD | Fichier | Taille | Question a laquelle elle repond |
|---|---|---|---|
| Entonnoir (Flux 2) | `_operateur/optimus-prime/pilote/entonnoir-files-optimus.json` | 397 122 o | le brin, les files, le vrac, les traces |
| File de missions | `_operateur/optimus-prime/pilote/file-missions-optimus.json` | 377 762 o | l etat de chaque mission (MO-xxx) |
| Raisonnement | `_operateur/optimus-prime/raisonnement/segments.json` | 62 147 o | les segments de raisonnement reutilisables (RS-xxx) |
| Registre d integrite | `_operateur/optimus-prime/espions/registre/registre.json` | 20 437 o | les empreintes surveillees (espion-integrite) |
| Pannes declarees | `_operateur/optimus-prime/suivi-pilote/pannes-declarees.json` | 25 409 o | les pannes que le suivi doit surveiller |

Volume total de cet inventaire : 12 123 863 o (~12 Mo). Le gros du poids est
`conservation.json` (7,4 Mo, les points de restauration) et le sac-a-dos des
fichiers (2,0 Mo) -- ce ne sont pas des BDD "de savoir", ce sont des
journaux de securite et d activite.

## 3. L ECART VRAI, MESURE

Il n existe PAS, aujourd hui, de registre unique qui DIRE "voici les BDD de la
v3 et voici leur domicile". Le compte le confirme : 13 fichiers .json au coeur
de `matrice/data/`, 61 dans la zone operateur, et AUCUN index ne les recense
comme un ensemble. Le lecteur doit DEVINER qu un .json de `data/` est une BDD
et qu un .json de la zone operateur en est une autre.

Consequence concrete, honnete : a la question "ou sont les BDD de la v3", il
n y a pas de source de verite unique a pointer. Il y a la convention implicite
"une BDD = un .json/.jsonl de donnees, a son domicile selon sa fonction", et
cette convention n est ecrite nulle part comme carte.

## 4. CE QUE L AUDIT NE FAIT PAS (posture)

- Je ne deplace RIEN et je ne cree aucun registre : un auditeur constate et
  signale, il ne range pas.
- Le point 3 (absence de carte unique) est un ECART SIGNALE, pas un defaut
  corrige. Il revient a la Matrice pour arbitrage : soit on ecrit la carte, soit
  on accepte la convention implicite comme etat normal. C est une DECISION, pas
  une evidence.

## 5. VERDICT

La question a sa reponse, et elle est la premiere qui soit une carte : les BDD
de la v3 sont reparties par FONCTION sur deux territoires (coeur Matrice =
le savoir systeme ; zone operateur = le savoir de l operateur). Chacune a un
domicile unique et sense. L ecart signale : il n existe pas de carte unique qui
les recense, ce qui laisse au lecteur deviner ce qu est une BDD. Signal, non
corrige (posture audit).
