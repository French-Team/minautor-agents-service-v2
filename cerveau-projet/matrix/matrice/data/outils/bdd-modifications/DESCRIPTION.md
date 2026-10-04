---
identite:
  type: outil
  appartient_a: matrice-data-outils
  commun: true
---

# OUTIL -- bdd-modifications -- note et corrige chaque modification de fichier

> Outil Python dedie a la BDD `modifications-par-fichier.json`.
> Porte la REGLE ANTI-SURCHARGE : chaque modification d'un fichier est notee ICI,
> jamais en commentaire dans le fichier lui-meme.

## Role

- **noter** : enregistrer une modification (action, detail, tags) pour un fichier,
  avec l'EMPREINTE DU CONTENU qu'elle atteste (posee automatiquement, jamais
  demandee a l'appelant -- une note qui ne l'a pas ne peut rien attester).
- **corriger** : rectifier EN PLACE une entree deja notee (tags, action et/ou
  detail), sans perdre son horodatage ni son histoire -- on peut corriger
  UNIQUEMENT l'action d'une note fautive, ou UNIQUEMENT ses tags.
- **retirer** : RETIRER une entree fautive ; le retrait est TRACE et REVERSIBLE
  (l'entree retiree survit ENTIERE dans le champ `retraits` de la fiche), et
  l'ambiguite est REFUSEE (`--index` desambigue).
- **lire** : consulter la BDD (tout, par fichier, ou par tag).
- **verifier** : controler l'empreinte SHA-256 ET la cle canonique de chaque
  fiche, puis rejouer l'auto-test (`--auto-test`).
- **canoniser** : ramener chaque cle sur SA forme canonique (migration EO-363).

## Options

```
python3 cerveau-projet/matrix/lancer.py bdd-modifications noter --fichier <chemin> --action <cree|modifie|corrige|supprime>
                     --detail "..." --tags "tag1,tag2"
python3 cerveau-projet/matrix/lancer.py bdd-modifications corriger --fichier <chemin> --extrait "..." [--tags "a,b" | --action <cree|modifie|corrige|supprime> | --detail "..."] [--motif "..."] [--index N]
python3 cerveau-projet/matrix/lancer.py bdd-modifications retirer --fichier <chemin> --extrait "..." [--index N] [--motif "..."]
python3 cerveau-projet/matrix/lancer.py bdd-modifications lire [--fichier <chemin>] [--tag <tag>]
python3 cerveau-projet/matrix/lancer.py bdd-modifications verifier [--auto-test]
python3 cerveau-projet/matrix/lancer.py bdd-modifications canoniser [--simuler oui]
```

- `--fichier` : chemin RELATIF A LA RACINE DE LA MATRICE (ex:
  `matrice/data/data-readme.md`, `_operateur/optimus-prime/pilote/commun.py`).
- `--tags` : liste separee par des virgules (tri et injection futurs).

## UN SEUL DOMICILE DE CLE (EO-363, 2026-09-22)

La cle d'une fiche est TOUJOURS relative a la racine de la Matrice. Avant EO-363
la BDD portait DEUX cles pour un meme fichier (935 cles mesurees = 232 prefixees
`cerveau-projet/matrix/` + 703 relatives, dont 158 fichiers sous les DEUX formes) :
la fiche d'un fichier ne montrait que la MOITIE de son histoire, et la vue pouvait
le lister deux fois. La cause etait que la porte enregistrait la cle TELLE QUELLE,
donc la forme dependait du repertoire courant de l'appelant.

- La REGLE vit dans UN SEUL domicile : `commun.canoniser_cle` (les formes
  reconnues viennent de `cible.NOMS_MATRICE`, consommees et jamais recopiees).
- `noter` et `corriger` canonisent ce qu'ils ecrivent ; `verifier` REFUSE une cle
  posee autrement (`ECART ... remede : bdd-modifications canoniser`).
- `canoniser` REUNIT les deux histoires et REFUSE d'ecrire si le recensement des
  entrees change (perte = refus nomme, pas un silence).

## UNE NOTE ATTESTE SON CONTENU (empreinte, 2026-09-23)

Une note disait CE QU'ON A FAIT et QUAND -- jamais SUR QUOI. Le controle
d'attribution (`controle-attribution.py`) ne pouvait donc comparer que des DATES :
une note ecrite pour une AUTRE ecriture blanchissait n'importe quel changement
posterieur, et le controle, qui IMPRIMAIT les deux empreintes sans les comparer,
ne pouvait pas s'en apercevoir.

Depuis, chaque note porte `empreinte` : le SHA-256 du fichier AU MOMENT de la note.
- La porte la MESURE elle-meme (`--fichier` est re-ancre sur la racine de la
  Matrice par `commun.chemin_de_cle`, l'inverse de `canoniser_cle`) : rien a
  passer en option, donc rien a oublier. Le compte-rendu le DIT a chaque note :
  `Contenu atteste : <16 caracteres>...` -- l'empreinte de la CIBLE, celle que le
  controle compare ; puis `empreinte BDD :` -- l'empreinte du DOMICILE des notes.
  Deux choses differentes, deux noms differents (on ne les confond plus).
- Une cible absente, illisible ou HORS de la Matrice rend une empreinte ABSENTE :
  la porte le DIT, la note reste valable (une suppression se note), et le controle
  compte cette fiche au lieu de lui faire confiance.
- Les notes ANTERIEURES a cette mesure ne portent pas d'empreinte : elles ne
  peuvent plus attester un changement, et la pose comme la verification les
  COMPTENT (jamais un silence, L-104).
- Le nom du champ vit dans `constants.py` (`CHAMP_EMPREINTE`) et le controle le
  CONSOMME : un nom recopie divergerait en silence (M-076).

## Architecture (convention-architecture-outils)

| Piece | Role |
|---|---|
| `DESCRIPTION.md` | la facade (ce fichier) |
| `main.py` | point d'entree global : DIRIGE, ne travaille pas |
| `constants.py` | TOUTES les valeurs (zero valeur en dur dans la logique) |
| `commun.py` | fonctions communes : charger, enregistrer (atomique), empreinte, `canoniser_cle` et son INVERSE `chemin_de_cle` (une cle canonique rend le chemin a LIRE) |
| `noter/`, `corriger/`, `lire/`, `verifier/`, `canoniser/`, `retirer/` | categories : `entry.py` orchestre, `fonctions.py` fait |

## Protections

- Ecriture atomique : fichier temporaire puis remplacement (jamais de BDD a moitie ecrite).
- Empreinte SHA-256 recalculee et enregistree A CHAQUE ecriture.
- Actions filtrees par liste permise (constants.py).
- Non-perte : la migration `canoniser` compare le RECENSEMENT des entrees (un
  multiset), pas leur nombre -- un compte reste juste si une entree disparait
  pendant qu'une autre est dupliquee.
- Aucun processus residuel : l'outil demarre, travaille, rend la main, s'arrete.
