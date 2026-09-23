# OUTIL -- registre-outils

> Le REGISTRE DES OUTILS (EO-314) : une BDD **UNIQUE** qui dit ce que le parc des
> briques **EST maintenant** (nom, proprietaire, domicile, chemin, origine, but,
> snippet, empreinte, statut), et la **PROPOSITION** d une liste d outils pour une
> mission -- chaque outil avec **SON MOTIF**.
>
> Il ne remplace ni l extracteur (`pilote/injection/modes_emploi.py`, qui LIT l usage
> dans la brique) ni la porte `entonnoir preparer` (qui POSE la liste sur l item). Il
> les relie : le registre **propose**, l operateur **decide**, la porte **pose**.

## Pourquoi une BDD unique (et pas trois)

L injection croise **deja** les flux pour une seule mission : une mission `dev` recoit
des outils d **Optimus** ET de la **Matrice**. Trois domiciles (optimus / matrice /
cameleon) = trois lectures a chaque proposition, et deux endroits ou le meme outil peut
etre declare deux fois. Une seule BDD, une colonne **`proprietaire`**, trois **vues**
(`lire --proprietaire`).

## Ce que le registre N EST PAS

`usages-outils-combos.jsonl` (16 140 lignes) est un **JOURNAL d appels** : des
EVENEMENTS, en ajout seul. Le registre est un **ETAT** : ce que le parc dit de lui-meme,
regenerable a l identique. Deux natures, deux domiciles, **aucun recouvrement** -- le
registre ne duplique pas le journal.

## L usage reste EXTRAIT de la brique (M-076 / L-032)

Le `but` et le `snippet` ranges ici sont une **COPIE**, et l **empreinte** est le PRIX
de ce confort : quand le texte servi bouge, `verifier` l **ACCUSE**, au lieu de laisser
une description morte fonder une proposition. L empreinte couvre **ce qui est range**
(`but` + `snippet`), pas le fichier entier : une correction de code qui ne change pas le
texte servi n est **pas** un ecart (mesure du 2026-09-20 -- empreindre le document
entier fabriquait un faux ecart a chaque correction).

## Portes

```
python3 cerveau-projet/matrix/lancer.py registre-outils rafraichir
python3 cerveau-projet/matrix/lancer.py registre-outils verifier
python3 cerveau-projet/matrix/lancer.py registre-outils lire [--proprietaire <optimus|matrice|cameleon>] [--servis]
python3 cerveau-projet/matrix/lancer.py registre-outils proposer --theme "..." --objectif "..." [--plafond N]
```

| Verbe | Ce qu il fait | Code |
|---|---|---|
| `rafraichir` | Inventorie le parc et **ECRIT** la BDD (regeneree, jamais editee a la main) ; repose l **empreinte etalon** | 0, ou 2 si l extracteur manque |
| `verifier` | Les **quatre** ecarts : perimes, disparus, non enregistres, muets | 0 si rien, 1 sinon, 2 si l extracteur manque |
| `lire` | La BDD, filtrable par proprietaire ; `--servis` ne montre que ce que l injection sert | 0, ou 1 si la BDD manque |
| `proposer` | La **PROPOSITION** d une liste d outils (motif par outil), bornee par le **plafond de l injection** ; **n ecrit rien** | 0, 1 si rien a proposer, 2 si le refus ou la BDD manque |

## Schema d une entree

`nom`, `proprietaire`, `domicile`, `chemin`, `servi_a_l_injection`, `origine`, `but`,
`snippet`, `empreinte_texte`, `statut`. La BDD porte aussi `identite`, `genere_le`,
`perimetre` (proprietaire + servi + nombre par domicile) et `homonymes` (un nom dans
deux domiciles : lequel l injection sert **vraiment**).

## Perimetre : LU, pas recopie

Les **racines servies** sont LUES dans l extracteur (`RACINES`) : la colonne
`servi_a_l_injection` decrit donc ce que le pilote sert **vraiment**, et non une liste
tenue a cote (deux verites pour un perimetre divergeraient). S y ajoutent des domiciles
**inventories, non servis**, ou l extracteur ne va pas : le pilote d Optimus, les
routines, et le pilote du **cameleon**. Mesure du 2026-09-20 : le cameleon n a **pas**
de domicile de briques distinct des outils de la Matrice -- ses propres briques sont son
pilote (`matrice/pilote/`), et c est le `proprietaire` `cameleon` qui le dit.

## Protections

- **Un seul domicile par valeur** : perimetre, proprietaire, empreinte et plafond sont
  declares une fois et CONSOMMES (zero-valeur-en-dur).
- **Le plafond est celui de l injection**, LU a son domicile (`PLAFOND_OUTILS_MODE_EMPLOI`)
  : une proposition non bornee se lirait comme un conseil ferme. Illisible = **REFUS**.
- **Les ecartees par le plafond sont DITES** avec leur motif (un plafond muet se lirait
  comme une liste complete, L-055).
- **La proposition n ecrit RIEN** : elle imprime le geste exact (`entonnoir preparer`).
- **Une brique non SERVIE n est jamais proposee** : la porte de preparation refuserait son
  nom -- deux avis contradictoires pour la meme question seraient un piege.
- **Une brique MUETTE est enregistree ET accusee** : un silence enregistre se repare, un
  silence absent ne se voit pas.
- **Ecriture atomique** (tmp + `os.replace`, LF forces) et **empreinte etalon** reposee a
  chaque publication : la BDD est declaree au registre de l espion d integrite.
- **Le chargeur ne recopie aucune regle de brique** : l extracteur est charge par CHEMIN
  (les deux zones ont des modules homonymes) ; ses refus sont NOMMES.

## Architecture (convention-architecture-outils)

| Piece | Role |
|---|---|
| DESCRIPTION.md | la facade (ce fichier) |
| main.py | point d entree global : DIRIGE |
| constants.py | perimetre, cible, forme de l empreinte, cles et statuts |
| etat.py | charger / enregistrer / empreindre (l etat de la BDD) |
| extraction.py | le PARC : l inventorier, et le verifier contre la BDD |
| proposition.py | la PROPOSITION : mots utiles + motifs, bornee par le plafond |
