---
identite:
  type: outil
  appartient_a: matrice
  commun: true
  version: 1
  date: 2026-09-24
  liens: matrice/data/outils/fichiers-travail-cameleon/main.py, matrice/data/commun/zone_tmp.py, _operateur/optimus-prime/super-combos/combos/outils/fichiers-travail.py, matrice/data/manuel-outils.md
---

# OUTIL -- fichiers-travail-cameleon -- nomme, liste et vide les fichiers de travail du flux cameleon

> La porte JUMELLE DU FLUX CAMELEON (MO-378). Le meme besoin que la porte d Optimus
> -- nommer, lister, montrer, vider et journaliser les fichiers de travail d une
> mission -- dans SON domicile : sa zone `workspace/tmp-cameleon`. Elle CONSOMME
> les declarations partagees (`matrice/data/commun/zone_tmp.py` : nom et chemin de
> la zone) ; elle ne copie AUCUN code du jumeau. Sa forme de nom est `M-` (celle de
> son pilote), pas `MO-`.

## Pourquoi une porte jumelle

Le createur ne voyait pas ce que la Matrice faisait de ses fichiers temporaires :
la zone du cameleon n avait ni outil ni trace, et un residu qui y restait apres une
cloture n etait accuse par AUCUN controle (le garde `garde-tmp` juge le domicile et
le README des zones, jamais le CONTENU d une zone remplie). Cette porte rend
VISIBLE ce que la zone a porte et ce qui a ete solde -- deux flux, deux zones, deux
domiciles, un seul moteur de declaration (M-076).

## Verbes

```
python3 cerveau-projet/matrix/lancer.py fichiers-travail-cameleon nommer --mission M-378 --libelle bilan [--extension txt]
python3 cerveau-projet/matrix/lancer.py fichiers-travail-cameleon lister [--mission M-378] [--strict] [--json]
python3 cerveau-projet/matrix/lancer.py fichiers-travail-cameleon montrer m-378-bilan.txt
python3 cerveau-projet/matrix/lancer.py fichiers-travail-cameleon vider [--mission M-378] [--par <qui>]
python3 cerveau-projet/matrix/lancer.py fichiers-travail-cameleon journal [--n 20] [--json]
python3 cerveau-projet/matrix/lancer.py fichiers-travail-cameleon --auto-test
```

- `nommer` : pose le fichier d une mission sous son NOM CANONIQUE. Une pose n ecrase
  JAMAIS un fichier existant (`DEJA POSE`), et l acte est journalise dans les deux
  cas.
- `lister` : la VUE de la zone, element par element, avec sa CLASSE. `--strict`
  rend code 1 s il reste un element hors forme canonique.
- `montrer` : le CONTENU d un element, par son SEUL nom (un separateur est un refus).
- `vider` : solde la zone (ou les elements d UNE mission) et journalise CHAQUE
  retrait avec le solde restant.
- `journal` : les derniers actes (pose, purge) -- voir sans fouiller.
- `--auto-test` : rejoue le cobaye (dossier JETABLE ; aucune epreuve ne touche la
  zone reelle).

## Nom canonique

`<mission minuscule>-<libelle>.<extension>` -- par exemple `m-378-bilan.txt`. Le nom
PORTE la mission, donc la lecture et la purge ciblee n ont plus besoin d une liste
tenue a la main. Trois classes, DITES par `lister` :

| Classe | Sens |
|---|---|
| `canonique` | le nom porte la forme ET la porte l a pose (une ligne `cree` de son journal) |
| `canonique-non-journalise` | la forme est canonique, mais la porte ne l a jamais pose -- un fichier ne hors de la porte |
| `residu` | le nom ne porte AUCUNE forme canonique -- un fichier pose a la main, RENDU VISIBLE |

Extensions admises : `txt`, `md`, `json`, `py`, `log`, `base64`. Une mission hors
forme (`MO-378`), un libelle hors forme ou une extension hors liste sont REFUSES en
NOMMANT le champ fautif.

## Architecture

| Piece | Role |
|---|---|
| `main.py` | DIRIGE (parser, router) ; declare ses verbes (`COMMANDES`) |
| `constants.py` | domiciles (zone, journal), motifs, extensions -- consomme `zone_tmp` |
| `commun.py` | atomes partages : nom canonique, journal, elements de la zone, options |
| `nommer/`, `lister/`, `montrer/`, `vider/`, `journal/` | une categorie par verbe (`entry.py` orchestre, `fonctions.py` fait) |
| `autotest.py` | le cobaye (fixtures JETABLES partagees) |

## Le GARDE anti-residu

Le controle permanent qui rend la lacune impossible vit a cote du garde de
perimetre : `_operateur/optimus-prime/super-combos/combos/outils/garde-residus-zone.py`.
Il ACCUSE tout element qui reste dans une zone jetable (`tmp-optimus`,
`tmp-cameleon`) : un residu, une purge MENTIEUSE (un nom purge mais encore present),
et -- en mode `--cloture` -- TOUT element restant apres une cloture. Il se mesure
sur un cobaye qui le fait CRIER et sur un contre-temoin (zone propre) qui le laisse
MUET.

## Garanties

- Ecriture ATOMIQUE, LF forces (la zone est jetable, mais sa trace est une trace).
- Journal en AJOUT SEUL (`.jsonl`) : aucune ligne reecrite ; une ligne illisible est
  RENDUE sous l action `illisible`, jamais avalee.
- Zero valeur en dur : la zone et son nom viennent de `data/commun/zone_tmp.py`.
- ASCII strict (0 non-ASCII a la publication).

## Codes de sortie

0 ok ; 1 ecart (purge partielle, ou `--strict` devant un residu) ; 2 refus.
