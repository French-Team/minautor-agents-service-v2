# OUTIL -- bdd-modifications

> Outil Python dedie a la BDD `modifications-par-fichier.json`.
> Porte la REGLE ANTI-SURCHARGE : chaque modification d'un fichier est notee ICI,
> jamais en commentaire dans le fichier lui-meme.

## Role

- **noter** : enregistrer une modification (action, detail, tags) pour un fichier.
- **corriger** : rectifier EN PLACE une entree deja notee (action, detail, tags),
  sans perdre son horodatage ni son histoire.
- **lire** : consulter la BDD (tout, par fichier, ou par tag).
- **verifier** : controler l'empreinte SHA-256 ET la cle canonique de chaque
  fiche, puis rejouer l'auto-test (`--auto-test`).
- **canoniser** : ramener chaque cle sur SA forme canonique (migration EO-363).

## Options

```
python3 cerveau-projet/matrix/lancer.py bdd-modifications noter --fichier <chemin> --action <cree|modifie|corrige|supprime>
                     --detail "..." --tags "tag1,tag2"
python3 cerveau-projet/matrix/lancer.py bdd-modifications corriger --fichier <chemin> --detail "..."
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

## Architecture (convention-architecture-outils)

| Piece | Role |
|---|---|
| `DESCRIPTION.md` | la facade (ce fichier) |
| `main.py` | point d'entree global : DIRIGE, ne travaille pas |
| `constants.py` | TOUTES les valeurs (zero valeur en dur dans la logique) |
| `commun.py` | fonctions communes : charger, enregistrer (atomique), empreinte, `canoniser_cle` |
| `noter/`, `corriger/`, `lire/`, `verifier/`, `canoniser/` | categories : `entry.py` orchestre, `fonctions.py` fait |

## Protections

- Ecriture atomique : fichier temporaire puis remplacement (jamais de BDD a moitie ecrite).
- Empreinte SHA-256 recalculee et enregistree A CHAQUE ecriture.
- Actions filtrees par liste permise (constants.py).
- Non-perte : la migration `canoniser` compare le RECENSEMENT des entrees (un
  multiset), pas leur nombre -- un compte reste juste si une entree disparait
  pendant qu'une autre est dupliquee.
- Aucun processus residuel : l'outil demarre, travaille, rend la main, s'arrete.
