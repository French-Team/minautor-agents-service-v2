---
identite:
  type: regle-immuable
  appartient_a: optimus-prime
  commun: false
  decide_par: createur
  date: 2026-09-17
---

# REGLE IMMUABLE -- LES DEMANDES DU CREATEUR ENTRENT DANS L ENTONNOIR

> Consigne du createur, 2026-09-17 : "pense a placer mes demandes dans
> l'entonnoir". Une demande qui ne vit que dans la conversation est une
> demande que le prochain demarrage ne connait pas : elle meurt avec le
> contexte. L'entonnoir est la MEMOIRE DE TRAVAIL du flux 2.

## La regle

1. **Toute demande du createur est DEPOSEE** dans l'entonnoir (porte
   `pilote/entonnoir`, verbe `deposer --theme "..." --objectif "..." --source s`)
   a l'instant ou elle est recue -- jamais "a la fin", jamais "apres la
   mission". Le depot precede le travail.
2. **La source dit d'ou elle vient** : `createur <date>` pour une demande,
   `<friction NN>` ou `<mission>` pour un ecart mesure. Un item sans source est
   un item orphelin : on ne sait plus qui l'a voulu ni pourquoi.
3. **L'urgence est celle de la demande** : `bloquante` seulement si le flux est
   arrete ; `haute` pour la suite directe d'une demande ; `normale` pour un
   ecart mesure ; `basse` pour une proposition en attente de GO.
4. **Un item est CLASSE** (type + role) : un item du vrac n'est pas executable,
   et le classement est ce qui pose le role dont l'injection a besoin.
   **Le classement a un DECLENCHEUR** (decision createur 2026-09-19, EO-192) : il
   ne depend plus de la memoire de qui relit la file.
   - **A LA NAISSANCE** : un item dont le type est **DECLARE** (le crochet du
     createur, ou `--type` -- souverain) est classe A LA SECONDE : il entre dans
     SA file avec sa categorie et son role, poses par les tables et IMPRIMES
     (donc corrigeables). Une **proposition** par mot-cle ne classe PAS : une
     devinette n'ouvre pas un domicile.
   - **SUR DEMANDE** : `classer --id EO-XXX` sans `--type` **CONSOMME** le type
     que l'item PORTE (R5 rendu vrai) et DIT son origine. S'il n'en porte aucun,
     le refus est DIRECTIONNEL (il nomme le geste).
   Le vrac ne garde donc que les items qu'AUCUNE souverainete n'a nommes : ceux
   la attendent une decision -- et le depot les NOMME avec le geste exact.
5. **Un item RESOLU sort du vrac** (`retirer`) : la trace de ce qui l'a resolu
   vit dans la mission, le rapport et le journal -- jamais dans la file, sinon
   la file ment sur ce qui reste a faire.
6. **Une proposition n'est pas une demande** : elle est deposee avec sa source
   (`proposition Optimus`) et ne devient une mission que sur le GO du createur.

## La mesure qui a produit cette regle

Le 2026-09-17, neuf demandes du createur ont ete traitees ou mises en attente
(MO-150 a MO-157) : AUCUNE n'etait passee par l'entonnoir avant ce soir. Elles
ne vivaient que dans la conversation, donc rien ne les aurait retrouvees apres
un redemarrage. La plus lourde -- les perimetres des deux flux (le cameleon
construit dans `workspace/`, sa zone jetable doit y passer) -- a du etre
deposee a la main, apres coup.

Corollaire : un item depose par la VEILLE (ex. EO-135, non-ASCII) peut rester
plusieurs dizaines de minutes sans suite si personne ne relit la file : la
relecture de l'entonnoir fait partie de l'accueil, comme la relecture de la
fiche et des corrections.
