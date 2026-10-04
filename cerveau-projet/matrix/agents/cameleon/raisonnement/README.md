---
identite:
  type: readme
  appartient_a: cameleon
  commun: true
---

# Domicile du RAISONNEMENT du CAMELEON

> L agent unique de la Matrice raisonne en SEGMENTS : un raisonnement ne s ecrit
> pas d un trait, il s ecrit en PARTIES -- plus courtes que le raisonnement qui
> les produit, TRACEES hors de la fenetre de contexte, et REUTILISABLES sur le
> meme sujet. Cette BDD est PARTAGEE : elle vit dans ce domicile, mais les DEUX
> agents la lisent (le moteur la sert SANS `--prive`). Decision du createur,
> 2026-09-27.

## Ce que ce dossier contient

| Piece | Role |
|---|---|
| `segments-cameleon.json` | la BDD : les segments, un par entree (empreinte SHA-256 a cote) |
| `bdd-raisonnement-cameleon/` | l OUTIL qui ecrit / lit / verifie cette BDD |
| `README.md` | ce mode d emploi |

## Le segment (la forme d une entree)

Une entree porte : `id` (`RC-XXX`), `date`, `segment` (le texte, CONCIS : ce qui
est ETABLI et ce qui RESTE ouvert), `tags` (obligatoires), `source` (la mission).

## Les trois moments

### 1. ECRIRE un segment (pendant une mission)

L outil n est PAS sous `data/outils/` : on donne le CHEMIN de son `main.py`.

```
python3 cerveau-projet/matrix/lancer.py cerveau-projet/matrix/agents/cameleon/raisonnement/bdd-raisonnement-cameleon/main.py ajouter \
  --segment "RC-XXX : <etat du raisonnement> -- etabli : ... ; reste : ..." \
  --tags "raisonnement,<sujet>,RC-XXX" --source "M-XXX"
```

`verifier` controle l empreinte ; `lire [--tag X]` liste (tout ou par tag).

### 2. RETROUVER un raisonnement

Le MOTEUR du projet, jamais un outil natif (regle immuable `moteur-recherche-d-abord`).
La source est DEJA declaree et PARTAGEE (servie sans `--prive`) :

```
python3 cerveau-projet/matrix/matrice/data/outils/rechercher/main.py rechercher \
  --dans bdd --source segments-cameleon --requete "<sujet>"
```

L injection de mission porte AUSSI sa `recherche` (question + commande) : c est
le premier endroit ou un raisonnement deja fait se relit.

### 3. L INJECTION, une fois le cameleon BRANCHE au pilote

AUJOURD HUI le cameleon n est PAS encore branche : l outil et la BDD existent,
mais le pilote ne les sert pas encore a l injection.

Le branchement se fera au MEME endroit que les lecons utiles : l injection de
mission de la Matrice (`matrice/pilote/injection/`, `fonctions.py`,
`charger_lecons_utiles`). Le geste decrit :

1. le pilote lit la BDD par le MOTEUR (source `segments-cameleon`), comme il
   charge deja les lecons et les themes ;
2. il selectionne les segments UTILES a la mission (le sujet, les tags) et les
   PESE dans le PLAFOND de l injection (ce qui ne rentre pas est DIT) ;
3. il les depose dans l injection de mission, A COTE des lecons et des themes :
   le segment dit OU on en est, la lecon dit CE QUI en a ete appris.

Un segment ne remplace NI la lecon, NI le journal de mission -- trois voisins :
le journal porte des EVENEMENTS, la lecon une REGLE generale, le segment un ETAT
de raisonnement sur UN sujet. Le segment et la lecon se consomment ENSEMBLE.

## La limite L-016, a la livraison

Une entree PARTAGEE qui nomme le vocabulaire interdit (le nom de l autre agent,
sa zone invisible) est RETIREE par le moteur a la livraison, MEME dans une source
partagee. Un segment du cameleon ne nomme donc AUCUN acteur invisible : le choix
des mots se MESURE au moteur (lecon L-194).

## Etat

- 2026-09-27 (MO-483) : outil + BDD crees ; 1re entree `RC-001` ; source PARTAGEE
  `segments-cameleon` declaree au moteur (servie sans `--prive`).
- 2026-09-27 (MO-485) : ROUTE `P-005 ROUTE RAISONNEMENT` posee dans les routes de
  la Matrice -- le cameleon la LIT au chargement de chaque mission.
- A FAIRE, quand le cameleon sera branche : integrer l injection de mission
  (catalogue `injection/config.json` + chargeur par phase).

## Ou la regle se LIT, au chargement d une mission

- **`P-005 ROUTE RAISONNEMENT`** : la route de la Matrice (BDD
  `matrice/data/protocoles-matrice.json`, outil `bdd-protocoles-matrice`, lue au
  chargement de CHAQUE mission). Elle dit le geste en trois temps : ecrire un
  segment, le retrouver par le moteur, le consommer AVEC les lecons.
