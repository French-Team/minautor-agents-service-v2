---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

LE ROLE EST INJECTE : LE SUIVI-T-IL ? (demande du createur, 2026-10-02)
Document de travail, pas une cloture de mission : aucun identifiant de mission n est
ouvert pour ce travail, et la porte `fin` aurait clos une mission qui ne le meritait
pas -- exactement la faute que ce document raconte.
Et la reponse honnete etait NON. Voici ce que j ai mesure et ce que j ai construit.

1. LA MESURE DE DEPART, DITE SANS ARRANGEMENT
   Le role du personnage est dans chaque injection depuis MO-539 (champ
   `role_agent`, NOYAU de la fiche technique, 11 221 tokens sur 12 000).
   Recherche sur toute la zone : RIEN ne le lit ailleurs. Il etait du decor --
   un texte bien ecrit, livre fidelement, jamais repris.
   Un caractere coche n est pas un comportement.

2. CE QUI EST REELLEMENT VERIFIABLE (j ai cherche la, pas l inverse)
   Le role s impose six tests. Un seul etait verifie quelque part, et pas par un
   garde : par un ACCIDENT de la journee meme. J avois clos MO-527 avec le bilan
   de MO-539 (la porte `fin` ne prend pas d id), et AUCUN instrument ne l a vu.
   C est exactement le test du role -- < ma preuve est-elle anterieure a mon
   changement ? > et < ce que je ne sais pas est-il dit ? > -- tombe sur une faute
   reelle, de moi, aujourd hui.

3. LE GARDE : `bilan-adresse-a-autre`
   Fait : un bilan s annonce par son identifiant. Si la PREMIERE ligne d un bilan
   porte un identifiant de mission qui n est pas celui de la mission close, ce
   bilan n a pas ete rendu pour elle.
   Portee : une panne DECLAREE dans `pannes-declarees.json` (partie fin,
   gravite haute) et un detecteur joue par le suivi du pilote -- donc visible a
   chaque passage, avec son remede nomme.
   Mesure : 50 missions closes avec bilan, 1 atteinte. La premiere, c est
   exactement la faute de la journee.

4. LA TETE, ET PAS LE BILAN ENTIER -- c est la partie qui compte
   Version large : la regle cherchait l identifiant dans tout le bilan et
   accusait 2 missions sur 50 -- dont une A TORT (MO-505, sain, commence par un
   titre sans identifiant et cite legitimement un precedent). Restreinte a ce qui
   se PRESENTE, elle n accuse que la mission reellement fautive.
   Une regle qui n accuse pas un innocent n est pas plus faible : c est une regle
   qu on peut laisser allumee en permanence.

5. TROIS PIEGES RENCONTRES, ET ILS MERITENT D ETRE DITS
   a) Le motif de recherche, ecrit par remplacement, s est retrouve dans le
      fichier sous forme d un OCTET RETOUR-ARRIERE (0x08) au lieu de la frontiere
      de mot. Le motif compilait, ne mordait sur rien, et le detecteur rendait
      muet -- alors que le fait existait. Parade : n ecrire aucun echappement, une
      classe de caracteres ne peut pas etre mal transportee.
   b) Apres correction, le detecteur a accuse 49 missions sur 50 : il avait l air
      bavard alors qu il etait faux (je prenais le premier groupe de capture, la
      frontiere, au lieu du second, l identifiant). Le bruit est un signal.
   c) La porte `ecrire` refuse tout fichier non ASCII : elle a refuse mon premier
      jet du fichier de pannes des que j y ai glisse un caractere etranger, avant
      meme que je le voie. Un garde qui a refuse sans que j le sollicite.

6. LES PREUVES (8/8)
   Le cas reel mord. Cinq contre-temoins epargnent : un bilan qui se nomme
   lui-meme ; un bilan sans identifiant en tete (il se presente par son titre) ;
   un bilan qui cite un precedent ET le sien ; une mission EN COURS (elle n est pas
   close, et une mission en cours porte toujours le bilan de la precedente) ; un
   faux ami (`XMO-539` ne compte pas comme identifiant). Le corpus reel complet
   rend 1 seule mission en faute.

7. LA VERITE QUI RESTE, ET QUE JE NE MASQUE PAS
   La trace ne se reecrit pas : MO-527 porte toujours ce bilan etrang. Le garde
   le voit, il le nomme, et sa sortie est ROUGE. J ai donc declare une EXCEPTION
   OUVERTE -- le meme mecanique que `item-qui-dort` (MO-513) : la faute est
   REELLE et reste visible, mais elle est deja REPAREE hors trace (bilan re-depose
   sur MO-539, ligne de journal sur MO-527, travail re-depose en EO-546).
   L exception nomme sa condition de levee : si le compte passe a 2, elle n est
   plus vraie et doit etre levee. La decision par defaut reste le ROUGE.
   Un garde qu on eteint pour passer au vert serait exactement le genre de garde
   dont ce projet a deja souffert.

8. CE QUE JE N AI PAS FAIT, ET QUE JE NE VAUDRAIS PAS PRETENDRE
   Le role a SIX tests ; j en ai rendu UN verifiable. Les cinq autres (la preuve
   anterieure au changement, le veto de la non-regression, la reversibilite des
   suppressions, le dedoublement d un fait, l annonce d une interface inventee)
   restent declaration sans instrument. Les rendre tous est un travail, pas une
   reponse de tour. Je le dis plutot que de laisser croire que le personnage est
   desormais applique.

9. SEGMENT : RS-065.
