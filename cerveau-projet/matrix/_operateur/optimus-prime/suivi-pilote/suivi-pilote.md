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

Mesure du 2026-10-04 18:58:18 | pannes declarees : 20 | detecteurs joues : 17.

Pannes DECLAREES sans detecteur (couverture dite, jamais muette) :
- fenetre-d-absorption-plus-courte-que-le-battement : aucun detecteur ecrit pour cette panne declaree
- injection-refusee : le refus d injection N EST PAS JOURNALISE (mesure du 2026-09-22 : aucun evenement de refus dans l outbox) -- aucune source ne porte le fait
- pilote-muet : couvert par le detecteur serie-stricte-violee (meme lecture : le code de la porte)

## Table 0 -- PANNES (la seule qui crie)

**AUCUNE PANNE CONSTATEE** -- les parties lues ci-dessous sont coherentes.

## Table 1 -- INJECTION (partie injection/)

> Une injection est un INSTANT : aucune duree. La colonne Refus n EXISTE PAS : le refus d injection n est pas journalise (mesure du 2026-09-22) -- une colonne toujours < inconnu > serait un placeholder qui ment.

| Mission | Injectee le | Poids (tok) | Lecons utiles |
|---|---|---|---|
| MO-569 | 2026-10-04 06:24:24 | 10572 | 26 |
| MO-573 | 2026-10-04 06:51:33 | 11208 | 30 |
| MO-574 | 2026-10-04 07:00:47 | 11391 | 27 |
| MO-575 | 2026-10-04 08:11:53 | 11240 | 24 |
| MO-576 | 2026-10-04 08:46:11 | 10857 | 25 |
| MO-577 | 2026-10-04 09:07:34 | 11461 | 28 |
| MO-581 | 2026-10-04 18:26:57 | 10963 | 24 |
| MO-582 | 2026-10-04 18:31:44 | 10880 | 26 |
| MO-583 | 2026-10-04 18:33:53 | 10990 | 25 |
| MO-584 | 2026-10-04 18:36:33 | 10849 | 28 |
| MO-585 | 2026-10-04 18:54:13 | 10687 | 29 |
| MO-586 | 2026-10-04 18:57:19 | 10893 | 27 |

## Table 2 -- FILE (partie file/)

> Silence = l ecart entre l ouverture et le dernier fait : la colonne qui voit une mission ouverte qui n avance plus.

| Mission | Statut | Dernier fait | Silence |
|---|---|---|---|
| MO-586 | en-cours | debut | 1 min |
| MO-587 | en-attente | inconnu | inconnu |
| MO-588 | en-attente | inconnu | inconnu |
| MO-589 | en-attente | inconnu | inconnu |
| MO-590 | en-attente | inconnu | inconnu |
| MO-591 | en-attente | inconnu | inconnu |
| MO-592 | en-attente | inconnu | inconnu |
| MO-593 | en-attente | inconnu | inconnu |
| MO-594 | en-attente | inconnu | inconnu |
| MO-595 | en-attente | inconnu | inconnu |
| MO-596 | en-attente | inconnu | inconnu |
| MO-597 | en-attente | inconnu | inconnu |
| MO-598 | en-attente | inconnu | inconnu |
| MO-599 | en-attente | inconnu | inconnu |
| MO-600 | en-attente | inconnu | inconnu |
| MO-601 | en-attente | inconnu | inconnu |

Colonnes OMISES (constantes, sans verdict) : Dans le lot (16 lignes) ; En attente depuis (16 lignes).

## Table 3 -- LOT (partie file/, a part)

> Panne lue : portee sans tete, ou STOP sans motif. Les colonnes Arme le et Retour consolide n existent PAS : aucune source ne les porte aujourd hui -- une colonne toujours < inconnu > serait un placeholder.

| Lot | Portee | Ecoulees | Retirees | Tete | Enchainement |
|---|---|---|---|---|---|
| lot-21 | 21 | 5 | 0 | MO-586 | MO-586 |

## Table 4 -- ENTONNOIR (files)

> Age : un item qui vieillit est un travail qui dort.

| File |
|---|
| audit |
| cablage |
| cadrage |
| dev |
| doc |
| investigation |
| preparer |
| question |
| reparation |
| revision |

Colonnes OMISES (constantes, sans verdict) : Items (10 lignes) ; Tete (10 lignes) ; Urgence de la tete (10 lignes) ; Age de la tete (10 lignes).

## Table 5 -- BRIN

> Coherence : brin = 0 ; files = 0.

(rien a lire sur cette partie)

## Table 6 -- CLOTURES ET ENCHAINEMENT (partie fin/)

> La DUREE d une mission vit dans suivi-optimus : elle n est PAS recopiee ici. Le verdict d enchainement vient de la FONCTION du pilote (provenance de l item), jamais d une comparaison d ids.

| Mission close | Fin a | Bilan | Enchainement |
|---|---|---|---|
| MO-573 | 2026-10-04 06:52:30 | pose | auto |
| MO-574 | 2026-10-04 07:00:56 | pose | auto |
| MO-575 | 2026-10-04 08:42:54 | pose | STOP |
| MO-576 | 2026-10-04 09:04:36 | pose | STOP |
| MO-577 | 2026-10-04 09:47:56 | pose | STOP |
| MO-579 | 2026-10-04 14:22:30 | pose | STOP |
| MO-580 | 2026-10-04 18:12:13 | pose | STOP |
| MO-581 | 2026-10-04 18:30:46 | pose | auto |
| MO-582 | 2026-10-04 18:33:11 | pose | auto |
| MO-583 | 2026-10-04 18:35:52 | pose | auto |
| MO-584 | 2026-10-04 18:53:28 | pose | auto |
| MO-585 | 2026-10-04 18:56:37 | pose | auto |

## Table 7 -- DEMANDES FILTREES (vrac)

> Panne lue : une demande recue et jamais classee (le vrac ne se vide pas).

| Demande | Recue le | Action posee |
|---|---|---|
| EO-482 | 2026-09-29 08:27:05 | au vrac (non classee) |
| EO-560 | 2026-10-02 20:56:23 | au vrac (non classee) |
| EO-561 | 2026-10-02 21:32:03 | au vrac (non classee) |
| EO-562 | 2026-10-02 22:04:39 | au vrac (non classee) |
| EO-563 | 2026-10-02 22:10:26 | au vrac (non classee) |

Colonnes OMISES (constantes, sans verdict) : Porte visee (5 lignes) ; Urgence (5 lignes).

## Table 8 -- GARDES (pause de session, defcon)

> Panne lue : une pause armee et oubliee -- ou le JOURNAL et l ETAT qui se contredisent (l agent s arrete et personne ne le voit).

| Garde | Etat | Depuis | Motif |
|---|---|---|---|
| pause de session | active | 2026-09-25 06:50:25 | reprise :  |
