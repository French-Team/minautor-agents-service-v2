---
identite:
  type: routine
  appartient_a: matrice-routines
  commun: true
---

# ROUTINE chien

> Demande createur du 2026-10-03 (`[tache]`, mission MO-564) : "creer le chien".
> Le chien detecte un changement dans un dossier, declenche une routine qui lance
> un combo, fait le travail en arriere-plan, et s eteint jusqu a la prochaine
> demande.

## Le probleme mesure

La correction ASCII etait deja COUVERTE (`corriger-ascii` voit 990 fichiers,
`tmp-optimus` compris) et deja PASSEE (`veille-flux`, toutes les 300 s). Ce qui
manquait etait la LATENCE : un fichier ecrit par le LLM pouvait rester non
corrige jusqu a cinq minutes.

AVANT : 300 s d'attente. APRES : 20 s. Le chemin est divise par 15.

## Le chien ne corrige pas

Il ne fait QUE trois choses :

1. **OBSERVER** : lire l empreinte du disque (chemin, date, taille). Mesure :
   990 fichiers en 68 ms.
2. **COMPARER** a l empreinte precedente, et classer ce qui a bouge en crees,
   modifies et supprimes.
3. **LANCER le combo** si -- et seulement si -- quelque chose a bouge.

La correction elle-meme reste le domaine du combo. Un chien qui corrigerait
lui-meme aurait deux cartes ASCII, donc deux conversions qui divergent en
silence. La convention est laite de ce point : l'agent ne fait rien, la Matrice
fait tout.

## Le silence est un contrat, pas une absence

Le cinquieme cas est le plus important : **rien n a bouge, alors le chien se
tait**. Pas de combo, pas de journal, pas de sortie. Un chien qui relance sur un
dossier immobile ne veille pas, il consomme -- et il le ferait 4 320 fois par
jour.

Le PREMIER passage est un cas a part : c'est la prise de temperature. Il
enregistre ce qu'il voit et n'agit pas. Sans cette neutralite, le chien
viderait le disque de corrections a son allumage, et le dirait comme si c etait
un changement.

## Discret

- aucun processus a nu : le combo passe par `lanceur.py` (contrat EO-428) ;
- aucune fenetre : les drapeaux viennent de `lancement.drapeaux_popen()` ;
- rien n'est envoye vers le LLM : le chien journalise, il ne parle pas.

## Cadence

La cadence vit au PLANNING (decision createur D1, MO-429), comme toute routine de
fond : **20 secondes**. Cout : 68 ms d observation pour 990 fichiers, soit moins
de 0,5 % d'un coeur. L'attente est decoupee en pas de 2 s, donc l'arret
cooperatif est vu en 2 s et non au bout de la cadence.

## Arret

`python3 cerveau-projet/matrix/matrice/routines/chien/main.py arret` pose un drapeau. Le chien ne se tue jamais : il voit le
drapeau a la prochaine tranche de 2 s, le consomme, et sort proprement.

## Ce que le chien NE fait pas

- Il ne remplace pas `veille-flux` : la veille reste le filet de fond, 300 s.
  Le chien est la voie courte, elle ne se substitue pas. Deux chemins pour le
  meme travail se completent -- et chacun se dit.
- Il ne juge pas un caractere sans equivalent : c'est un probleme GRAVE que la
  convention nomme, donc une mission, jamais une correction silencieuse.
- Il ne surveille pas `docs/` : c'est la zone de sources du createur, en lecture
  seule (meme decision que `corriger-ascii`).
