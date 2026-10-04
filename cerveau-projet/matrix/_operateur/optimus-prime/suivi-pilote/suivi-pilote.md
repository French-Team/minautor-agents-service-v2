---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# SUIVI DU PILOTE -- la vue derivee

> Regeneree par la porte `suivi-pilote` (T2 de PB-003/SP-003/TD-003).
> Jamais editee a la main : elle se RECALCULE. Les faits du pilote vivent
> dans suivi-optimus, file-missions, entonnoir, cycle-historique, outbox et
> le journal des pauses -- ici, seulement ce que l instrument a JUGE.

Mesure du 2026-10-04 17:51:00 | pannes declarees : 20 | detecteurs joues : 17.

Pannes DECLAREES sans detecteur (couverture dite, jamais muette) :
- fenetre-d-absorption-plus-courte-que-le-battement : aucun detecteur ecrit pour cette panne declaree
- injection-refusee : le refus d injection N EST PAS JOURNALISE (mesure du 2026-09-22 : aucun evenement de refus dans l outbox) -- aucune source ne porte le fait
- pilote-muet : couvert par le detecteur serie-stricte-violee (meme lecture : le code de la porte)

## Table 0 -- PANNES (la seule qui crie)

| Gravite | Panne | Constat | Silence | Porte qui repare |
|---|---|---|---|---|
| normale | item-qui-dort | 21 item(s) du brin dorment (le plus vieux : EO-507, rang 2/21) | 2026-09-30 09:43:14 | servir le brin par la tete, une par une (file consommer) : le plus vieux dort au rang 2/21 -- il part apres les 1 item(s) qui le precedent |

Motifs : item-qui-dort -- 21 dormeur(s) sur 21 items, au-dela de 1.0 j ; le plus vieux (EO-507) est depose depuis 4.3 j et occupe le rang 2 de la file.

OUVERTES (constatees, deposees, suivies -- jamais tues) :
- item-qui-dort : item MO-513 (EO-490, decision createur du 2026-09-29, confirmee par arbitrage le 2026-10-01) -- VERTE PAR JUSTIFICATION (demande createur 2026-10-01), pas par extinction. Un item au brin qui attend son tour dans une file SERIEUSE, dont la TETE AVANCE, est dans l etat ATTENDU de la regle < servir par la tete, un par une > : attendre est la contrepartie normale de la serie stricte, donc l accelerer n est pas un defaut. Mesure du 2026-10-01 qui le prouve : la tete (rang 1) a 23,3 h et descend, les 7 dormeurs sont a 36 h et PLUS, situes aux rangs 8 a 33 -- ils attendent derriere des items plus frais, donc la file COULE. Avant cette inversion, chaque passage PAYAIT une re-verification : l agent devait redemander pourquoi c etait rouge et reconclure que c etait juste (le faux positif recurrent le mieux documente du projet). La DETECTION et le CODE ne sont pas touches (d etection inchangee, meme mesure, meme remede nomme) : seule la COULEUR DU VERDICT est inversee. Le signal reste ENTier et reste muet sur rien : la sortie nomme toujours le nombre, le plus vieux et son rang. CETTE EXCEPTION EST UN ETAT VIVANT : elle couvre la file qui COULE. Si un jour la tete elle-meme s arretait au-dela du seuil, l item deviendrait un BLOQUAGE et cette exception serait levee (retirer ce champ) ; la decision par defaut reste le ROUGE de la panne.

## Table 1 -- INJECTION (partie injection/)

> Une injection est un INSTANT : aucune duree. La colonne Refus n EXISTE PAS : le refus d injection n est pas journalise (mesure du 2026-09-22) -- une colonne toujours < inconnu > serait un placeholder qui ment.

| Mission | Injectee le | Poids (tok) | Lecons utiles |
|---|---|---|---|
| MO-534 | 2026-10-03 08:06:33 | 11197 | 30 |
| MO-551 | 2026-10-03 09:49:59 | 11261 | 25 |
| MO-552 | 2026-10-03 10:12:58 | 11531 | 26 |
| MO-553 | 2026-10-03 10:38:44 | 11037 | 26 |
| MO-566 | 2026-10-04 05:06:33 | 10945 | 26 |
| MO-565 | 2026-10-04 05:24:45 | 11156 | 26 |
| MO-569 | 2026-10-04 06:24:24 | 10572 | 26 |
| MO-573 | 2026-10-04 06:51:33 | 11208 | 30 |
| MO-574 | 2026-10-04 07:00:47 | 11391 | 27 |
| MO-575 | 2026-10-04 08:11:53 | 11240 | 24 |
| MO-576 | 2026-10-04 08:46:11 | 10857 | 25 |
| MO-577 | 2026-10-04 09:07:34 | 11461 | 28 |

## Table 2 -- FILE (partie file/)

> Silence = l ecart entre l ouverture et le dernier fait : la colonne qui voit une mission ouverte qui n avance plus.

(rien a lire sur cette partie)

## Table 3 -- LOT (partie file/, a part)

> Panne lue : portee sans tete, ou STOP sans motif. Les colonnes Arme le et Retour consolide n existent PAS : aucune source ne les porte aujourd hui -- une colonne toujours < inconnu > serait un placeholder.

| Lot | Portee | Ecoulees | Retirees | Tete | Enchainement |
|---|---|---|---|---|---|
| lot-0 | 0 | 0 | 0 | EO-559 | EO-559 |

## Table 4 -- ENTONNOIR (files)

> Age : un item qui vieillit est un travail qui dort.

| File | Items | Tete | Urgence de la tete | Age de la tete |
|---|---|---|---|---|
| audit | 0 | inconnu | inconnu | inconnu |
| cablage | 0 | inconnu | inconnu | inconnu |
| cadrage | 8 | EO-511 | normale | 4.3 j |
| dev | 0 | inconnu | inconnu | inconnu |
| doc | 0 | inconnu | inconnu | inconnu |
| investigation | 0 | inconnu | inconnu | inconnu |
| preparer | 1 | EO-529 | normale | 4.3 j |
| question | 6 | EO-507 | normale | 4.3 j |
| reparation | 6 | EO-559 | normale | 1.9 j |
| revision | 0 | inconnu | inconnu | inconnu |

## Table 5 -- BRIN

> Coherence : brin = 21 ; files = 21.

| Rang | Item | Categorie | Depose le | Age |
|---|---|---|---|---|
| 1 | EO-559 | routine | 2026-10-02 20:41:28 | 1.9 j |
| 2 | EO-507 | reponse | 2026-09-30 09:43:14 | 4.3 j |
| 3 | EO-511 | plan | 2026-09-30 09:43:15 | 4.3 j |
| 4 | EO-529 | plan | 2026-09-30 09:43:20 | 4.3 j |
| 5 | EO-564 | autre | 2026-10-03 08:00:08 | 1.4 j |
| 6 | EO-510 | reponse | 2026-09-30 09:43:15 | 4.3 j |
| 7 | EO-513 | plan | 2026-09-30 09:43:16 | 4.3 j |
| 8 | EO-566 | outil | 2026-10-03 09:43:48 | 1.3 j |
| 9 | EO-536 | reponse | 2026-09-30 09:43:22 | 4.3 j |
| 10 | EO-520 | plan | 2026-09-30 09:43:17 | 4.3 j |
| 11 | EO-570 | bdd | 2026-10-03 10:15:15 | 1.3 j |
| 12 | EO-547 | reponse | 2026-10-02 08:20:29 | 2.4 j |
| 13 | EO-526 | plan | 2026-09-30 09:43:19 | 4.3 j |
| 14 | EO-572 | outil | 2026-10-03 10:15:43 | 1.3 j |
| 15 | EO-549 | reponse | 2026-10-02 08:34:36 | 2.4 j |
| 16 | EO-527 | plan | 2026-09-30 09:43:19 | 4.3 j |
| 17 | EO-574 | autre | 2026-10-03 10:24:16 | 1.3 j |
| 18 | EO-558 | reponse | 2026-10-02 19:56:50 | 1.9 j |
| 19 | EO-528 | plan | 2026-09-30 09:43:20 | 4.3 j |
| 20 | EO-530 | plan | 2026-09-30 09:43:20 | 4.3 j |
| 21 | EO-535 | plan | 2026-09-30 09:43:21 | 4.3 j |

Colonnes OMISES (constantes, sans verdict) : Urgence (21 lignes).

## Table 6 -- CLOTURES ET ENCHAINEMENT (partie fin/)

> La DUREE d une mission vit dans suivi-optimus : elle n est PAS recopiee ici. Le verdict d enchainement vient de la FONCTION du pilote (provenance de l item), jamais d une comparaison d ids.

| Mission close | Fin a | Bilan | Enchainement |
|---|---|---|---|
| MO-567 | 2026-10-03 19:52:29 | pose | STOP |
| MO-568 | 2026-10-03 20:06:36 | pose | STOP |
| MO-569 | 2026-10-03 21:10:18 | pose | auto |
| MO-570 | 2026-10-03 21:24:21 | pose | STOP |
| MO-571 | 2026-10-04 04:55:43 | pose | STOP |
| MO-572 | 2026-10-04 05:47:10 | pose | STOP |
| MO-573 | 2026-10-04 06:52:30 | pose | auto |
| MO-574 | 2026-10-04 07:00:56 | pose | auto |
| MO-575 | 2026-10-04 08:42:54 | pose | STOP |
| MO-576 | 2026-10-04 09:04:36 | pose | STOP |
| MO-577 | 2026-10-04 09:47:56 | pose | STOP |
| MO-579 | 2026-10-04 14:22:30 | pose | STOP |

## Table 7 -- DEMANDES FILTREES (vrac)

> Panne lue : une demande recue et jamais classee (le vrac ne se vide pas).

| Demande | Recue le | Action posee | Urgence |
|---|---|---|---|
| EO-444 | 2026-09-26 09:04:01 | au vrac (non classee) | bloquante |
| EO-482 | 2026-09-29 08:27:05 | au vrac (non classee) | normale |
| EO-495 | 2026-09-30 09:26:46 | au vrac (non classee) | bloquante |
| EO-496 | 2026-09-30 09:26:47 | au vrac (non classee) | bloquante |
| EO-497 | 2026-09-30 09:26:47 | au vrac (non classee) | bloquante |
| EO-498 | 2026-09-30 09:26:47 | au vrac (non classee) | bloquante |
| EO-499 | 2026-09-30 09:26:48 | au vrac (non classee) | bloquante |
| EO-500 | 2026-09-30 09:26:48 | au vrac (non classee) | bloquante |
| EO-540 | 2026-10-01 08:08:06 | au vrac (non classee) | bloquante |
| EO-541 | 2026-10-01 08:08:06 | au vrac (non classee) | bloquante |
| EO-560 | 2026-10-02 20:56:23 | au vrac (non classee) | normale |
| EO-561 | 2026-10-02 21:32:03 | au vrac (non classee) | normale |
| EO-562 | 2026-10-02 22:04:39 | au vrac (non classee) | normale |
| EO-563 | 2026-10-02 22:10:26 | au vrac (non classee) | normale |
| EO-578 | 2026-10-04 11:30:25 | au vrac (non classee) | bloquante |

Colonnes OMISES (constantes, sans verdict) : Porte visee (15 lignes).

## Table 8 -- GARDES (pause de session, defcon)

> Panne lue : une pause armee et oubliee -- ou le JOURNAL et l ETAT qui se contredisent (l agent s arrete et personne ne le voit).

| Garde | Etat | Depuis | Motif |
|---|---|---|---|
| pause de session | active | 2026-09-25 06:50:25 | reprise :  |
