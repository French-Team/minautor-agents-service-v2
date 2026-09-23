---
identite:
  type: convention
  appartient_a: optimus-prime
  commun: false
---

# CONVENTION -- CREDIBILITE D'UNE MISSION ANCIENNE

> Source : demande du createur (2026-09-22 : < quand on reprend des missions anciennes, on
> doit mettre en place un process pour verifier et valider leur credibilite avant de les
> executer >), precisee le meme jour :
>   - < le createur ne doit pas etre inclus dans le process, optimus doit reflechir et
>     decider ; ce process doit etre automatise > ;
>   - < optimus est plus rapide et intelligent et mieux place pour decider a la place
>     du createur > ;
>   - < si les missions existent, elles ont deja ete discutees avec le createur qui les a
>     demandees : ce process doit determiner si elles sont OBSOLETES et, si oui, gerer
>     automatiquement de les supprimer, deplacer, etc >.
>
> Une mission ancienne n'est pas CRUE : elle est MESUREE, JUGEe, et TRAITEE.

## QUI decide : OPTIMUS, SEUL

**L'OPERATEUR (OPTIMUS) decide.** Le CREATEUR n'est PAS dans ce process -- et ce n'est pas
une commodite : **une mission qui existe a DEJA ete demandee et discutee avec lui**. La
question n'est donc JAMAIS < veut-on encore ceci ? > mais **< ceci est-il DEVENU
OBSOLETE ? >**. Cela, OPTIMUS le tranche mieux que personne : il a les faits sous les yeux,
il est plus rapide, et il n'a rien a demander pour agir.

> **Toute demande de decision au createur, dans ce process, est une FAUTE.**

## QUAND : TOUT SEUL, A CHAQUE DEMARRAGE

Le process est **JOUE par le DEMARRAGE du pilote** (`injection/cycle.py`, a cote de la
reprise de session) : il ne depend NI de la memoire de l'agent, NI d'une commande qu'on
oublierait. Ce qui doit se jouer a chaque reprise se joue au demarrage.

Il ne juge que les missions **RESTAUREES** -- dont la charge (`chargee_le`) date d'un jour
ANTERIEUR. Une mission nee du round courant n'est jamais touchee : un process qui crie la ou
rien n'a change cesse de garder.

    python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/outils/verifier-credibilite-missions.py --auto

## Ce qui est MESURE -- et ce qui ne l'est pas

| Fait | Mesure | Ce qu'il vaut |
|---|---|---|
| AGE et REPRISE | jours depuis la charge, et charge anterieure au jour courant | dit si la mission est ANCIENNE, jamais si elle est bonne |
| PREMISSES | les fichiers (extension) que l'objectif nomme existent-ils encore, dans TOUT le depot | un nom MORT rend la mission PERIMEE |
| DOUBLON | une mission plus recente et TERMINEE porte deja le sujet (regle de ressemblance CONSOMMEE de `filtrer/cadrage.py`) | rend la mission DEJA FAITE |
| SOURCE | l'item d'origine est-il encore relisible dans l'entonnoir | INFORME, ne juge pas (memoire bornee) |
| VERDICT | un verdict a-t-il DEJA ete rendu et trace | une mission n'est jamais re-jugee |

## Ce qui est DECIDE, et ce qui est FAIT

| Verdict | Sens | Action |
|---|---|---|
| `credible` | premisses mesurees tenues, aucun doublon | **aucune** : la mission s'execute |
| `deja-faite` | une mission plus recente et terminee porte deja le sujet | **RETRAIT DU LOT**, automatique |
| `perimee` | un nom de fichier de l'objectif n'existe plus nulle part | **RETRAIT DU LOT**, automatique |
| `a-revoir` | l'anciennete n'est pas mesurable | **SIGNALEMENT** : rien n'est supprime -- ce qui n'est pas mesurable ne se jette pas |

Le retrait passe par la **porte du pilote** (`pilote lot retirer --ids <MO-XXX> --motif "..."`) :
la mission **sort du lot**, garde son id, son objectif et son motif, et reste dans la file
sous le statut `retiree`. **C'est ce qui rend l'action automatique : elle est REVERSIBLE.**
Une mission dont l'objectif nommait un fichier simplement deplace se remet en corrigeant
son objectif -- elle n'a jamais ete perdue.

## Reconnaitre une anciennete MUETTE (lecon du 2026-09-22)

Un lot rejoue est charge **EN UNE FOIS** : toutes ses missions portent le **MEME**
`chargee_le`. Le critere d'age seul ne peut donc PAS mordre sur le cas pour lequel il est
ecrit -- la premiere version de l'outil rendait < VERDICT OK : toute mission ANCIENNE porte
un verdict > devant un **journal VIDE**. D'ou la definition :

    ANCIENNE = age >= seuil, OU age illisible, OU RESTAUREE (chargee un jour anterieur).

**Un controle qui ne peut pas mordre rend un vert MUET** (L-163). Avant de declarer un
controle fini, on exige de lui qu'il **morde sur le cas reel**.

## TRACE

Domicile : `cerveau-projet/matrix/_operateur/optimus-prime/credibilite/credibilite-verdicts.jsonl`,
ecrit par la **PORTE ECRIRE** (jamais a la main), une ligne par verdict :

    {mission, verdict, motif, juge_le, par}

Le motif d'un verdict automatique dit ce qui a ete MESURE et ce qui a ete FAIT.
**Un verdict sans motif ne s'explique pas ; un verdict non trace n'existe pas.**

## LIMITES declarees

- `credible` dit : *les premisses MESUREES tiennent et la demande a ete RELUE*. Il ne dit pas
  que la mission est la MEILLEURE facon de faire : une mission credible peut rester mal
  concue, et c'est le round d'execution qui le dit.
- La memoire des items consommes est **BORNEE** (41 entrees au 2026-09-22) : < source non
  relisible > est le cas NORMAL d'une mission ancienne, jamais un verdict.
- La mesure des premisses est **TEXTUELLE** : un nom GABARIT est hors mesure, et un nom
  retrouve ailleurs sur le disque (meme nom, autre dossier) passe. C'est pourquoi un verdict
  ne SUPPRIME rien : il RETIRE, avec son motif.
- Une mission obsolete **hors d'un lot** ne peut pas etre retiree (le verbe du pilote agit
  sur un lot) : elle est SIGNALEE a OPTIMUS.

## Mesure d'ouverture (2026-09-22)

- 35 missions restaurees mesurees et jugees : **34 `credible`**, **1 `deja-faite`**
  (MO-359 : MO-306 portait deja P1, et la rotation joue a la cloture depuis MO-344),
  **0 `perimee`**.
- **MO-359 RETIREE DU LOT AUTOMATIQUEMENT** par le premier passage du mode `--auto`
  (mesure : le lot passe de 37 a 36 ids, la mission garde son id et passe en `retiree`) --
  sans createur, sans question, sans geste d'agent.
