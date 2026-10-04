---
identite:
  type: readme
  appartient_a: matrice
  commun: true
---

# data : BDD DE LA MATRICE

> Une BDD = un fichier (json ou jsonl). La Matrice et le pilote y lisent/ecrivent
> via des outils Python dedies (jamais a la main au milieu d'une mission).

## Les 7 BDD prevues (source : IMPERATIF + fiche)

| BDD | Fichier prevu | Usage | Qui ecrit |
|---|---|---|---|
| lecons | lecons.json | dernieres lecons de mission, tri par TAGS | outil bdd-lecons + pilote (injection) |
| classeur-variables | classeur-variables.json | variables de la Matrice | outils dedies (bdd-variables + machine-defcon pour la cle defcon) |
| historiques-missions | historiques-missions.jsonl | chaque mission : theme, agent, bilan, dates | pilote |
| modifications-par-fichier | modifications-par-fichier.json | ce qui a ete fait sur CHAQUE fichier (+ tags) -- JAMAIS en commentaire dans le fichier | agent (a chaque modification) |
| usages-outils-combos | usages-outils-combos.jsonl | appels des outils et combos (temps, resultat) | sac-a-dos embarque de chaque outil (via outil bdd-usages) + veille-flux |
| activites-recentes | activites-recentes.json | revue PAR SECTIONS a emplacements precis (jamais "a la suite") | outils dedies + veille-flux |
| historique-bdd | historique-bdd.jsonl | historique global avec filtrage (doublons, obsoletes) | outils dedies |

## Regles des BDD

1. Format unique : json pour les registres consultes, jsonl pour les journaux en ajout seul (on n'ajoute des lignes, on ne modifie jamais l'historique).
2. Toute ecriture passe par un outil Python (protections ouverture/fermeture).
3. Deduplication et marquage obsolete : responsabilite de historique-bdd.
4. Integrite : empreinte SHA-256 enregistree a chaque ecriture
   (convention-integrite-sha256.md).
5. Tags obligatoires : lecons, modifications, usages (pour tri et injection).

## FLUX D'ECRITURE (la porte unique)

```
[1] l'agent, apres chaque modification d'un fichier
      |  python main.py noter --fichier <chemin> --action <action> --detail "..." --tags "a,b"
      v
[2] main.py                    DIRIGE : route vers la categorie demandee
      v
[3] <categorie>/entry.py       VALIDE (action permise, champs requis) puis orchestre
      v
[4] <categorie>/fonctions.py   FABRIQUE l'entree {date, action, detail, tags} (une tache chacune)
      v
[5] commun.py                  LIT la BDD, puis ECRIT de facon ATOMIQUE
                               (tmp + remplacement, fins de ligne LF forcees)
      v
[6] le disque                  la BDD (json/jsonl) + l'etalon-or (<nom>.sha256)
      v
[7] le controle en aval        verifier (outil) + espion-integrite :
                               empreinte reelle vs etalon
                               - match  -> silence
                               - ecart  -> ECART signale (jamais repare en douce)
```

Regles du flux : PORTE UNIQUE (toute ecriture passe par l'outil) / ANTI-SURCHARGE
(note APRES modification, jamais en commentaire dans le fichier) / ATOMICITE
(jamais de BDD a moitie ecrite) / DETERMINISME (meme donnee = memes octets,
empreinte stable) / l'espion SIGNALE, ne repare jamais en douce (la reparation
repasse par la porte unique, avec une note reelle).

## Statut : PLAN COMPLETE (7/7 faites)

| BDD | Statut | Outil dedie |
|---|---|---|
| modifications-par-fichier | FAITE (2026-09-06) | outils/bdd-modifications/ (noter, lire, verifier) |
| historiques-missions | FAITE (2026-09-06) | pilote/ (journalise en ajout seul) |
| lecons | FAITE (2026-09-06) | outils/bdd-lecons/ (ajouter, lire, verifier) |
| usages-outils-combos | FAITE (2026-09-06) | outils/bdd-usages/ (noter, lire, verifier) |
| classeur-variables | FAITE (2026-09-06) | outils/bdd-variables/ (definir, lire, verifier) |
| activites-recentes | FAITE (2026-09-06) | outils/bdd-activites/ (noter, lire, verifier) |
| historique-bdd | FAITE (2026-09-06) | outils/bdd-historique/ (noter, lire, marquer-obsolete, verifier) |

## La SEULE BDD SQLite : `frictions.db` (EXCEPTION ASSUMEE, 2026-09-26)

> Decision de l'operateur du 2026-09-26 : frictions.db reste en SQLite. C'est une
> EXCEPTION NOMMEE et BORNEE a la regle < une BDD = un fichier (json ou jsonl) >.
> Cette regle gouverne les BDD DE LA MATRICE ; frictions.db appartient a un autre
> domicile (ci-dessous), et la doctrine ne l'avait jamais NOMMEE -- d'ou la confusion
> qui a fait croire a une < BDD lourde > disparue.

| Fait | Valeur mesuree (2026-09-26) |
|---|---|
| Fichier | `matrice/data/frictions.db` (110 Ko, 93 frictions) |
| Domicile de l'OUTIL | `_operateur/optimus-prime/super-combos/combos/outils/bdd-frictions/` (zone INVISIBLE, L-016) |
| Ce qui la lit | combo `c-007-frictions`, `espions/espion-activite-optimus.py`, `verifier-vocabulaire-etat.py` |
| Integrite | `frictions.db.sha256` (etalon pose par sa porte, comme les 11 autres BDD) |

Ce n'est PAS une exception arbitraire : SQLite n'apporte RIEN a 93 lignes -- les
vraies BDD LOURDES de la v3 sont DEJA en JSON (usages 15,6 Mo, conservation
4,6 Mo, modifications 1,6 Mo). Le modele < json = legere / db = lourde > est donc
REFUTE par la mesure : il n'existe qu'UNE BDD SQLite, et c'est la plus PETITE.

Ce que coute l'exception, et qui est DIT : `rechercher` exclut les binaires
(`constants.py` : `.db`) -- les frictions passees ne sont donc pas cherchees par le
moteur unifie ; elles se lisent par `bdd-frictions lister` / `stats`. `git diff` ne
les montre pas.

REGLE POUR LA SUITE : aucune NOUVELLE BDD en SQLite. Une migration vers
`frictions.json` reste POSSIBLE (mesure : 1 outil de 457 lignes + 3 consommateurs,
dont 2 gardes) mais N'EST PAS RETENUE : elle ne gagne que la recherchabilite et le
diff, au prix de la reecriture d'un instrument PORTEUR. Le jour ou un besoin REEL
l'exige, la migration se fera comme un ROUND dedie, prouve.

## BDD additionnelles (hors plan 7/7)

| BDD | Statut | Outil dedie | Qui ecrit |
|---|---|---|---|
| defcon-historique | FAITE (M-059) | outils/machine-defcon/ (lire, monter, descendre, valider) | machine-defcon (journal append-only des transitions defcon) |
| conservation | FAITE (MO-095) | outils/bdd-conservation/ (proposer, classer, decider, lire, manifeste, verifier) | Optimus, par la porte de conservation ; Flux 1 et cameleon en lecture seule |

Note : la cle defcon du classeur-variables a DEUX ecrivains declares : bdd-variables
(creation initiale via definir) et machine-defcon (transitions, id conserve, empreinte
SHA-256 maintenue apres chaque ecriture). Tout autre ecrivain est un ecart a signaler.

Ordre de construction : modifications-par-fichier -> historiques-missions -> lecons
-> usages-outils-combos -> classeur-variables -> activites-recentes -> historique-bdd.
