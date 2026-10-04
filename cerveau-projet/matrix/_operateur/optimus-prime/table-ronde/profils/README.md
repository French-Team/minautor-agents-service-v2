---
identite:
  type: convention
  appartient_a: optimus-prime
  commun: false
  maj: 2026-10-02
---

# TABLE RONDE -- les 6 profils et la boucle des 3 rounds

> Demande createur EO-523 (MO-532) : reunir plusieurs profils, chacun dedie a une
> facon de penser, sur 3 rounds, puis une synthese reutilisable.

## LES 6 CARTES (ce dossier EST leur domicile)

| Profil | Sa question | Etat |
|---|---|---|
| `besoin.md` | Que veut VRAIMENT la personne ? | cree (MO-532) |
| `vivant.md` | Qu est-ce qui existe deja, et que je casse ? | cree (MO-532) |
| `duree.md` | Que restera-t-il dans trois mois ? | cree (MO-532) |
| `karpathy.md` | Quel est le MINIMUM qui marche ? | pointe la convention |
| `nemesis.md` | Qu est-ce qui casse, coute, ouvre une breche ? | pointe le PROCESSUS |
| `arbitre.md` | Que tranche-t-on, et que perd-on en tranchant ? | cree (MO-532) |

Les deux derniers ne sont pas copies : leur carte POINTE son domicile
(`conventions/convention-karpathy.md`, `parcours/themes/theme-auto-audit-nemesis.json`).
Une recopie divergerait en silence de ce que le createur edite.

## LA BOUCLE

    sujet -> les 5 profils -> 5 analyses = le CONTENU de la table
    round 2 lit ce contenu -> 5 analyses = le nouveau contenu
    round 3 lit ce contenu -> ARBITRE synthetise

Dans un round, les 5 profils lisent le MEME contenu. Si chacun voyait la
production de celui qui parle avant lui, ce ne serait plus un round mais une file.

## L OUTIL : `sc-007-table-ronde`

    sc-007-table-ronde etat --table <slug>       (ce qui a ete dit, ce qui manque)
    sc-007-table-ronde tour --table <slug>       (qui parle, sur quel contenu)
    sc-007-table-ronde arbitrer --table <slug> <fichier>
    sc-007-table-ronde auto-test

Une analyse se depose par la PORTE, jamais par l outil (qui n ecrit jamais) :

    bdd-raisonnement ajouter --segment "<analyse>"         --source "MO-XXX <slug>" --tags "table-ronde,R<n>,<PROFIL>"

Les 6 refus sont nommes dans le fichier de l outil : table inconnue, profil
inconnu, round en avance, double voix, arbitrage premature, synthese sans verdict.

## LES TABLES JOUEES (ce dossier EST leur domicile)

| Fichier | Sujet | Etat |
|---|---|---|
| `tables/non-delegable-llm.md` | qu est-ce qui ne peut pas etre delegue au LLM | jouee (MO-549, 2026-10-02) -- 15 analyses, 3 verdicts |

La synthese d une table reste sur le disque : le fichier d analyse est lu par
`arbitrer`, puis purge avec la zone jetable -- une decision qui n existe que la
tant qu elle est lue ne survit a rien.
