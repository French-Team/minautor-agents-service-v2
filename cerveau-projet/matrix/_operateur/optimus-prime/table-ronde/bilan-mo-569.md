---
identite:
  type: journal
  appartient_a: optimus-prime
  commun: false
---

# BILAN MO-569 -- LA TABLE RONDE DU POST-VOL

> Etat : `A_REPRENDRE`. Je ne le calme pas : la mesure a trouve de quoi le
> justifier, et c'est moi qui l'ai construit. Aucune mission n'est sanctionnee.

## CE QUE LA MISSION ETAIT

MO-569 est le **post-traitement**, celui qui manquait depuis deux jours. Le
2026-10-03, une auto-test a supprime toute la zone `_operateur/` (757 fichiers).
Le travail est revenu par `git checkout`, mais le **bilan** du round, lui, n'a
jamais ete refait : cinq missions s sont ensuite jouees sans lui. Rouverte
aujourd'hui, la question posee par le createur etait : *statut normal + un
controle de coherence des livrables*. Aucun statut `livree-inconstatee` : la
reponse tranchee est un etat, pas un verdict de culpabilite.

## LE PROTOCOLE, ET POURQUOI IL EST ECRIT COMME IL EST

L'agent depose d'abord sa note, **librement**, dans
`table-ronde/auto-note-2026-10-04.md`. Ensuite seulement on mesure. Le
mesureur ne lit pas la note : il ne la cherche meme pas. Un instrument qui lit
la note qu il verifie la corrige en meme temps qu il l examine -- il ne
verifie plus rien. La comparaison des deux se fait apres coup, par un tiers qui
voit les deux.

C est pour cela que la note a ete deposee **avant** le premier essai du
mesureur, et que je ne l ai relue qu une fois la mesure posee.

## LA MESURE

```
etat                      A_REPRENDRE
missions mesurees          538   (51 file active + 487 archive)
portes distinctes          47   (42867 appels lus)
nonsens_publies            1
blames                     CONDITION TOUJOURS VRAIE 1 | BOUCLE VIDE 0
                           | FORMAT DE DATE LITTERAL 0
```

## LES TROIS FAUTES QUE LA MESURE A FAITES SUR ELLE-MEME

C est le fond de ce bilan. Un instrument de mesure qui rend un chiffre faux
est pire que pas d instrument, parce qu on reparaie ce qui n est pas casse.
Trois fois, la mesure a accuse des fichiers qui n avaient rien fait.

**1. Elle a accuse 217 fichiers, dont 213 injustifies.** Le journal des bilans
nomme deux sortes de fichiers melangees : des livrables **durs**, dont le
chemin part de la racine, et des brouillons de **zone jetable**, cites par
leur seul nom -- `mo-571-bilan.md` -- parce qu ils ont ete ecrits dans le
dossier de travail puis purges, **par convention**. Resoudre un nom nu depuis
la racine accuse donc 201 bilans parfaitement effaces, et 8 chemins relatifs
qui se resolvaient sous une autre base. La resolution est desormais
**declaree** (`BASES_RESOLUTION`, rendue dans le rapport), et ce que le champ
ne sait pas resoudre sort en `livrables_indeterminables` : **2544 entrees, non
accusees**. Un accuse a tort est pire qu un silence.

**2. Elle a lu 51 missions sur 538.** La garde `enchainement` l'a prise en
faute, et elle avait raison : elle lisait la file active sans son archive. La
garde nomme celui qui parle, c est a cela qu elle sert. Correction : la file
ET son archive, avec le compte rendu par conteneur.

**3. Elle a conclu a 63 renommages, dont 45 faux.** Retrouver `main.py`
ailleurs ne prouve pas que *ce* fichier-la a ete renomme : le parc en compte
25, et 18 `README.md`. Le renommage n est plus conclu que si le nom de base est
**rare** -- une seule occurrence dans tout le parc. Il en reste **11**, et je
les ai relus un par un :  chacun pointe un fichier reel et unique.

**Ce qui reste accuse : 70 fichiers sur 2614 cites.** Deux sont les miens
(`table-ronde/tables/post-vol-agent-autonote.md`, le dossier d'hier) ; le
tiers, `parcours/themes/theme-crochet.json`.

## LE NONSENS TROUVE

Un seul, et il est reel : `super-combos/sc-006-lacunes/main.py:339`,
`... in sortie or True`. Une condition qui passe toujours, qui lit le fichier
pour rien, et qui etait sous mes yeux depuis le debut de la journee. Les deux
autres familles (boucle vide, format de date litteral) : zero.

C est exactement le reproche que je m etais adresse dans l'auto-note -- *je les
ai vus sur RELECTURE, pas grace a un controle*. Le controle existe maintenant ;
il l'a trouve, et il n'a pas trouve que lui.

## CE QUE LA MESURE NE FAIT PAS

Elle ne note pas l'agent. Elle ne lit pas l'auto-note. Elle ne corrige rien.
Elle n'accuse pas un brouillon purge par convention. La liste des `blames` est
**fermee** : on nomme, on ne penalise pas -- aucun de ces chiffres ne retire un
point, ne ferme une mission et ne banni un outil.

## L AUTO-NOTE CONTREDITE

L'auto-note disait : *je m attends a etre accuse sur au moins un point que je
ne vois pas*. La mesure en a trouve un (`or True` dans `sc-006`), et il etait
la depuis le matin. Elle a aussi confirme les quatre fautes reconnues : deux
assertions fausses ou j accusais d abord le code, trois nonsens vus a la
relecture, des reconstructions sur specification, des scories d'ecriture. Les
deux inconnues -- la divergence de conservation de 237 ecarts, et
l'attribution des six fichiers -- restent ouvertes et consignees.

## CE QUE JE LAISSE OUVERT

- **Les 237 ecarts de conservation** et les 149 archives declarees dont 137
  fichiers absents (~4,2 Mo). Consignes, jamais traites, signales par la porte
  `pilote fin` et jamais par la non-regression.
- **Les 6 fichiers de l'attribution**, le seul KO de la non-regression.
- **Les 70 accuses.** Aucun n est corrige ici : les corriger serait le travail
  du mesureur, et un mesureur qui repare ne peut plus rien mesurer.

## SEGMENT

RS-122 -- Le post-traitement enfin joue, et ses trois faux positifs comptes.
