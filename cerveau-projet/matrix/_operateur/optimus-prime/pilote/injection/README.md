---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
---

# Porte `injection/` -- injections du pilote Optimus Prime

> **Un seul dossier d'injection.** Le dossier `injections/` (moteur de catalogue
> parallelle, cree le 2026-09-12) a ete **fusionne ici** le 2026-09-13 : deux
> dossiers dont le nom ne differait que d'un `s` etaient un piege (deux
> *namespace packages* voisins, aucun `__init__.py`). Le nom qui fait foi est
> celui de l'architecture officielle (`DESCRIPTION.md`) : `injection/`.

## Les 7 pieces de la porte

| Piece | Role |
|---|---|
| `entry.py` | la porte : verbes `statut`, `injecter`, `enchainer` (et `mission --action`) |
| `cycle.py` | le **cycle** : orchestre les injections par phase (`demarrer`, `mission_debut/pendant/fin`) |
| `fonctions.py` | l'injection de **mission** : ordonnee, filtree L-016, pesee en tokens, deposee dans l'outbox intercom |
| `injecter.py` | le **moteur du catalogue** : sert les injections de DEMARRAGE et de PHASE |
| `modes_emploi.py` | l **extracteur des MODES D EMPLOI** : pour chaque brique, son but et son usage, EXTRAITS de la brique elle-meme (`main.py`, `README.md`) -- jamais une fiche recopiee (M-076). Type de catalogue `modes-emploi` |
| `config.json` | le **catalogue** : quelles sources, pour quelle phase, obligatoires ou non |
| `README.md` | ce fichier |

## Qui appelle quoi (le vrai cablage)

```
python3 cerveau-projet/matrix/_operateur/optimus-prime/pilote/main.py injecter <- ORDRE 2 de demarrer-optimus-prime.md
  -> injection/entry.py  (verbe injecter)
     -> injection/cycle.py (CycleOptimus.demarrer)
        -> injection/injecter.py demarrage  <- le CATALOGUE (fiche + theme de reprise + protocole)
     -> injection/fonctions.py (preparer_injection)
        -> l'injection de MISSION dans l'outbox intercom
```

## Lancer le catalogue directement

```bash
python3 cerveau-projet/matrix/_operateur/optimus-prime/pilote/injection/injecter.py --categories # la liste vient du CATALOGUE
python3 cerveau-projet/matrix/_operateur/optimus-prime/pilote/injection/injecter.py demarrage # fiche + theme de reprise + protocole de reprise
python3 cerveau-projet/matrix/_operateur/optimus-prime/pilote/injection/injecter.py demarrage --format json
python3 cerveau-projet/matrix/_operateur/optimus-prime/pilote/injection/injecter.py mission # les 3 phases d'un coup
python3 cerveau-projet/matrix/_operateur/optimus-prime/pilote/injection/injecter.py avant-mission --peser # MESURE : le poids en tokens de chaque source + le TOTAL
```

## L'entree `role` : la conduite AVANT la mission (MAILLON 2/5, 2026-09-14)

Le cameleon recoit **UNE personnalite par mission** (categorie `PERSONNALITE` du
vivier), jamais choisie par lui. Optimus n'en recevait **aucune** : ses missions
ne portaient qu'un theme de **chantier** (le QUOI toucher) et le catalogue lui
**deversait la fiche entiere** au demarrage.

L'entree `role` est donc la **premiere** de `avant-mission` :

```json
{
  "id": "role",
  "description": "Role d'Optimus pour cette mission (postures du vivier : QUI conduit)",
  "source": "../../../matrice/data/vivier-themes.json",
  "type": "json",
  "obligatoire": true,
  "categorie": "PERSONNALITE"
}
```

- Le filtre `categorie` sert les **postures** du vivier (le **QUI**) ; le
  **QUOI** (theme de chantier) reste porte par la mission et par l'injection de
  mission (`fonctions.py` -> champ `role` : `posture` + `theme` + items declares).
- Le mappage ferme **type -> posture** vit dans `pilote/personnalites.py` et il
  est **porte par le pilote**, jamais par l'agent.
- Le garde `verifier-roles.py` (maillon **22**) exige que cette entree soit
  **declaree** ET **servie**, et que les **deux** chemins d'injection la portent.

> Voir [README-roles.md](../README-roles.md) pour le mappage et ses regles.

## Doctrine : aucune degradation silencieuse (2026-09-13)

| Cas | Comportement |
|---|---|
| source absente, `"obligatoire": true` | **REFUS nomme**, code 2 |
| source absente, `"obligatoire": false` | **ALERTE nommee**, code 0 (on continue) |
| `"obligatoire"` non declare | traite comme **obligatoire** (prudence) + alerte |
| `type` inconnu du moteur | **REFUS nomme**, code 2 |
| `section` demandee et introuvable | **REFUS nomme**, code 2 |
| categorie absente du catalogue | **REFUS nomme**, code 2 |
| filtre `categorie` qui vide le contenu | **ALERTE nommee** (contenu vide signale, jamais muet) |

Types servis : `fichier`, `json`, `bdd`, `dossier`, `outil` (fichier lu, dossier liste).
Les **categories viennent du catalogue** : aucune liste en dur dans le moteur.

> **Historique des reparations du 2026-09-13** (mesurees, pas supposees) :
> 1. **les 11 sources etaient 100 % mortes** -- les chemins portaient un segment
>    `optimus-prime/` en trop (`RACINE/optimus-prime/optimus-prime.md`). Ils sont
>    desormais **relatifs au pilote** (`../optimus-prime.md`), comme ceux du cameleon.
> 2. `"obligatoire"` etait declare sur chaque entree et **jamais lu** : chaque
>    source morte imprimait `[FICHIER INTRUVABLE: ...]` et rendait **code 0**.
> 3. `type: "outil"` (declare **6 fois**) etait **inconnu du moteur** -> "Type inconnu".
> 4. `section` (declaree 1 fois) etait **ignoree** -> extraction markdown ajoutee.
> 5. la categorie `outils` **dupliquait** deux entrees de `avant-mission` (memes id,
>    memes sources) : retiree (deux verites pour un meme besoin).

## Ce que la porte COUTE : la mesure et ses deux plafonds (MO-314)

La mesure est un **verbe du catalogue**, pas un script jetable : elle se rejoue
apres chaque changement de contenu.

```bash
python3 cerveau-projet/matrix/_operateur/optimus-prime/pilote/injection/injecter.py avant-mission --peser
```

Mesure du **2026-09-20** (apres MO-313 et MO-314) : l injection `avant-mission`
pese **7435 tokens**, sur 8 sources -- `role` 700, `fiche-rappel` 1021,
`theme-actif` 1067, les **quatre cartes de modes d emploi** 829 + 264 + 167 + 623 =
**1883**, `garde-perimetre` 1371, `garde-flux2` 1393. Avant le plafond, ces quatre
cartes pesaient **2452** : **31 pour cent** de l injection entiere.

Mesure du **2026-09-21** (MO-331, les DEUX REGISTRES DE FAMILLE servis) :
`avant-mission` pese **8397 tokens** sur 11 sources (`protocoles-disponibles` 640)
et `demarrage` **5963** sur 4 sources (`conventions-disponibles` 589). Pourquoi ce
placement, et pas le meme pour les deux : il a ete **CALCULE**, pas choisi par
symetrie. Chaque document a ete mesure sur deux axes -- a-t-il un DECLENCHEUR (une
route, un theme, un garde qui l invoque) et est-il DEJA garde ailleurs ?

| Famille | Declencheur mesure | Placement | Pourquoi |
|---|---|---|---|
| protocoles | `proto-4` est invoque par le theme `auto-evolution` ; `proto-3` et `proto-5` par `indices.md` ; leurs declencheurs surviennent PENDANT le travail | **`avant-mission`** | trois des quatre orphelins sont des situations de mission, et la troisieme colonne du registre EST ce declencheur |
| conventions | trois des quatre sont **deja gardees** : `zero-valeurs-en-dur` par l etape 20 de la non-regression, `integrite-sha256` par l espion et le PRE-VOL, `architecture-outils` par `verifier-contrat-fondamental` | **`demarrage`** | un garde qui refuse en NOMMANT le remede vaut mieux qu un rappel repete a chaque mission : la carte sert de reference de forme, chargee une fois par session |

Mesure du meme jour, AVANT : les huit documents n apparaissaient dans **AUCUNE**
injection -- 0 occurrence dans le catalogue ET dans le sac-a-dos des **6** dernieres
injections reelles. Un equipement que rien ne nomme est un equipement que l agent ne
peut pas appeler ; et un protocole que rien ne DECLENCHE (mesure : `proto-8` a 0
citation dans le code, 0 dans les routes, 0 dans les gardes) ne sera pas utilise pour
autant : la carte le rend VISIBLE, elle ne fabrique pas son declencheur.


**Deux plafonds**, chacun declare a son domicile, et la coupe est **toujours DITE** :

| Plafond | Domicile | Valeur | Ce que la coupe dit |
|---|---|---|---|
| briques par CARTE | `modes_emploi.py` (`PLAFOND_BRIQUES_CARTE`) | 30 | combien de briques ne sont **pas affichees**, et les deux gestes (`mode-emploi <nom>`, `carte --complet`) |
| outils par MISSION | `pilote/constants.py` (`PLAFOND_OUTILS_MODE_EMPLOI`) | 8 | les noms **ecartes** (`ecartes_par_plafond`) |

Ce que la borne a change, mesure : les quatre cartes pesent **1792** tokens bornees
contre **2373** completes -- **581 economises**, 51 briques servies sur **98**. Les
deux seules racines qui depassent 30 briques (`outils` : 51, `outils-matrice` : 35)
DISENT leur coupe ; `combos` (7) et `super-combos` (5) ne coupent rien.

> Une carte bornee qui se TAISAIT se lirait comme une carte complete (L-055) : le
> **contrat 6** des outils accuse ce silence, et l autotest de l extracteur porte les
> deux sens (carte AU-DELA du plafond : coupee ET la coupe DITE ; carte SOUS le
> plafond : RIEN de coupe).

## La LISTE DES OUTILS d une mission (EO-313)

Les outils joints a une mission etaient une **fonction de son TYPE** (`OUTILS_PAR_TYPE`) :
deux missions `dev` recevaient les MEMES outils. Depuis EO-313, un item peut **declarer**
la liste des outils que SA mission va appeler, et la mission la **porte** :

```
entonnoir preparer --id EO-XXX --outils bdd-modifications,ecrire   <- la liste vit sur l ITEM
  -> pont item -> mission (charger --item, tete du brin, brin entier) : la mission la RECOPIE
     -> charger_modes_emploi(mission) : sert les modes d emploi de CES outils
```

**DEUX VOIES, et la voie est DITE** dans l injection (`voie` + `source`) :

| Voie | Quand | Ce qui est servi |
|---|---|---|
| `item` | la mission porte une liste preparee | EXACTEMENT ces outils, dans l ORDRE declare |
| `type` | aucune liste preparee (repli) | `OUTILS_COMMUNS` + `OUTILS_PAR_TYPE[type]` |

Deux garanties, cote porte et cote garde : un nom **non servable** est refuse A LA POSE
(avec ses proches), une liste plus longue que `PLAFOND_OUTILS_MODE_EMPLOI` aussi -- et le
**contrat 6** accuse toute mission qui declarerait, par un autre chemin, un outil non
servable ou une liste hors plafond.

## Le PROFIL DE L UTILISATEUR dans le sac-a-dos (2026-09-21)

Mesure du jour : la fiche `matrix/USER-PROFIL.md` etait **remplie** (8 champs sur 8)
mais **aucun agent ne la lisait** -- le pilote ne l ouvrait qu au DEMARRAGE
(`injection/cycle.py`), pour tester si la ligne `**Pseudo**` etait remplie, puis
jetait le contenu. Le profil voyage donc desormais **avec la MISSION**, comme la
posture (`role`) et la question (`recherche`) :

```
preparer_injection / enchainer    <- les DEUX chemins d injection
  -> charger_profil_utile()       <- injection/fonctions.py
     -> motif PARTAGE data/commun/fiche_profil.py (chemin, champs ATTENDUS, lecture)
```

Le bloc injecte (champ `profil`, **pese** avec le reste : `CHAMPS_PESES`) :

| Cle | Ce qu elle dit |
|---|---|
| `source` | la fiche lue (jamais un chemin suppose) |
| `present` + `complet` | la fiche est lisible, et aucun champ ATTENDU n est vide |
| `champs` | les champs ATTENDUS remplis, dans l ORDRE du motif |
| `a_remplir` | les champs ATTENDUS vides (l agent peut guider : `main.py profil --guider`) |
| `ecartes_par_plafond` | ce que la borne a coupe -- une coupe MUETTE se lirait comme un profil complet |
| `poids_champs_tokens` + `mesure` | le poids retenu, et l INSTRUMENT qui l a mesure (peseur du domicile, ou repli DECLARE) |
| `avertissement` | fiche absente ou illisible : le bloc le DIT, il ne se vide pas |

**Plafond** `PLAFOND_PROFIL_TOKENS` (300, `pilote/constants.py`) : mesure du
2026-09-21, les 8 champs pesent **30 tokens** quand le sac-a-dos mesure pese **9660 a
9887** -- le plafond vaut donc ~10 fois le contenu reel, et il ne mord que sur une
valeur COLLEE dans un champ (le cas d une fiche ouverte a l ecriture manuelle).

Ce que le plafond borne, et ce qu il ne borne pas (dit, mesure) : il borne la SOMME
des champs retenus. Le **bloc entier coute 127 tokens** dans le sac-a-dos -- 30 de
champs et **97 de CHARPENTE** (chemin absolu de la fiche, cles, listes), soit **1,3
pour cent** d une injection de 9660 a 9887. La charpente est BORNEE par construction
(cles fixes ; `a_remplir` et `ecartes_par_plafond` sont des sous-ensembles des 8
champs ATTENDUS), donc le bloc est borne par le plafond PLUS une charpente constante
et mesuree -- une mesure qui annoncerait moins que ce qu elle livre se lirait comme
un chiffre faux (c est le defaut exact de MO-314).

**Garde** : `verifier-profil-injection.py` (maillon 33 de la non-regression) --
domicile unique, champ pese, DEUX chemins, et un cobaye OBESE qui doit mordre puis
disparaitre (la zone jetable reste vide).

**Choix declare** : le profil n est PAS ajoute au catalogue `avant-mission` -- il
serait alors servi DEUX fois (une fois par le catalogue, une fois par le sac-a-dos),
soit du poids pour un seul besoin.
