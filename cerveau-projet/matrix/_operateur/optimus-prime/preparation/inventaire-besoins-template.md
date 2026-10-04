---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# INVENTAIRE DES BESOINS DE TEMPLATE (MO-541 / EO-546) -- LA MESURE

> Demande du createur, inchangee : lister nos besoins de template et creer les
> templates manquants -- lecons, frictions, regles immuables, conventions,
> protocoles, carte d identite, informations systeme, environnement de travail.
> L ENONCE IMPOSE LA MESURE AVANT D ECRIRE : lister ce qui est DEJA sur le disque,
> et ne creer que ce qui manque, en DUPLIQUANT un template existant -- jamais un
> modele neuf invente.
>
> Ce document est la MOITIE `lister` du travail. La moitie `creer` suit, et
> elle est plus etroite que la demande : trois familles seulement.

## LA MESURE BRUTE (8 familles demandees)

| # | Famille demandee | La famille existe-t-elle SUR DISQUE ? | Un TEMPLATE existe-t-il ? | Verdict |
|---|---|---|---|---|
| 1 | lecons | OUI -- `matrice/data/lecons.json` (52 entrees), outil `bdd-lecons` (ajouter/lire/modifier/verifier) | NON -- zero `.moule`, zero `.modele` | PAS DE TEMPLATE, mais pas d artefact a fabriquer non plus |
| 2 | frictions | OUI -- `matrice/data/frictions.db` (table `frictions`, 10 colonnes), outil `bdd-frictions` | NON | idem |
| 3 | regles immuables | OUI -- `_operateur/optimus-prime/regles-immuables/` : 23 regles + 1 readme, toutes avec carte d identite `type: regle-immuable` | NON | **MANQUANT -- a creer** |
| 4 | conventions | OUI -- `_operateur/optimus-prime/conventions/` : 14 conventions + 1 readme, toutes `type: convention` | NON | **MANQUANT -- a creer** |
| 5 | protocoles | OUI -- `_operateur/optimus-prime/protocoles/` : 14 protocoles numerotes + 1 readme, tous `type: protocole` | NON | **MANQUANT -- a creer** |
| 6 | carte d identite | OUI | **OUI DEJA** -- `matrice/templates/carte-identite/` : `carte.modele`, `carte-complete.modele`, `INVENTAIRE-CLES.md`, `README.md` | **DEJA LA -- 4 pieces, reference du projet** |
| 7 | informations systeme | **NON** -- aucune zone, aucun fichier, aucune porte de ce nom. ZERO resultat sur toute la zone, y compris le corpus | - | **LA FAMILLE N EXISTE PAS** |
| 8 | environnement de travail | **NON** -- idem. Le plus proche est `USER-PROFIL.md` (profil UTILISATEUR, injecte sous le champ `profil`) | - | **LA FAMILLE N EXISTE PAS** |

## CE QUI EXISTE DEJA COMME PATRON (le modele a dupliquer, pas a inventer)

Le projet possede DEUX dossiers de templates, et ils ne se confondent pas :

| Dossier | Zone | Consomme par | Regle |
|---|---|---|---|
| `matrice/templates/` | VISIBLE (`matrice/`) | `dupliquer-template` (outil-bdd, theme-bdd, routine) | patron `outil-bdd`, 21 `.moule` |
| `_operateur/optimus-prime/suivi-pilote/templates/` | INVISIBLE | `poser-template-pilote` | L-016 : un moule invisible ne sert QUE de l invisible |

Les trois familles a creer (regles immuables, conventions, protocoles) vivent
TOUTES les trois dans `_operateur/optimus-prime/` : ce sont des artefacts
INVISIBLES. Leur moule appartient donc au dossier du patron `poser-template-pilote`,
jamais a `matrice/templates/`. C est la grammaire de L-016 qui tranche, pas un
gout.

Le patron `.md.moule` a dupliquer est
`suivi-pilote/templates/raisonnement/segment.md.moule` (carte d identite en tete,
jetons `__NOM__`, bloc `POURQUOI UN TEMPLATE` qui cite la mesure qui a fait
naitre le manque). Le contenu, lui, est tire des instances REELLES de chaque
famille -- `serie-stricte.md` et `evolution-decidee.md`,
`convention-crochets.md`, `proto-12-loi-du-round.md` -- jamais d une invention.

## LES TROIS MANQUES, ET POURQUOI ILS SONT ECRITS ICI

Une regle immuable, une convention et un protocole sont trois documents qui
n existent que dans la zone INVISIBLE, et rien dans le projet ne dit de quoi est
fait un de ces documents. On le relit donc en entier pour comprendre sa forme --
c est exactement le risque que la convention des indices nomme. Un patron
existe pour `outil-bdd` (dupliquer-template) ; il n existe pas pour ces trois
familles la.

## LES DEUX FAMILLES SANS OBJET (7 et 8) -- CE QUE JE NE FAIS PAS, ET POURQUOI

`informations systeme` et `environnement de travail` ne sont pas des familles
dont le template manquerait : ce sont des familles dont la ZONE n existe pas.
Zero fichier, zero dossier, zero porte. Ecrire un template pour elles serait
inventer un modele neuf -- ce que l enonce interdit explicitement, et ce que la
regle du moule sans trou refuse deja (`poser-template-pilote` : un moule sans
jeton fabrique une COPIE morte, L-055).

Elles sont donc DEPOSEES EN ITEM, avec la question posee au createur : est-ce que
la zone `informations systeme` doit exister, et sous quelle forme ? Si oui, elle
naquit par une mission propre, et son template sera cree EN MEME TEMPS qu elle --
pas avant.

## LE MEME SORT POUR LES DEUX PREMIERES (lecons, frictions)

`lecons` et `frictions` ont une donnee et un OUTIL, pas un artefact. On n ecrit
pas `lecons.json` a la main : c est la porte `bdd-lecons ajouter` qui ecrit, et
elle refuse les formes mauvaises. Un template de lecon ne fabriquerait donc
RIEN -- il serait un second chemin vers la meme ecriture, donc une divergence de
plus (le meme argument qui a fait refuser une carte `type: role-agent` invente
en MO-540). Ce qui leur manque n est pas un template : c est que leur FORME soit
DECLAREE une fois, la ou la porte la lit. C est une autre mission.

## LE RESULTAT EN UNE LIGNE

Sur 8 familles demandees : 1 existe deja avec 4 pieces, 3 manquent reellement et
recoivent leur moule, 2 n ont pas de zone a documenter, 2 ont une porte qui
ecrit deja leur forme. Les 3 moules crees sont places dans le dossier que la
porte `poser-template-pilote` sait lire -- donc ils sont REELLEMENT posables,
pas des fichiers morts.
