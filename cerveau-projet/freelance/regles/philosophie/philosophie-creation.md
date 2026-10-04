---
identite:
  nom: philosophie-creation
  version: 0.1.0
  cree: 2026-08-23
  type: philosophie
  appartient_a: rogers
  commun: true
  mot-cles: ["philosophie", "creation", "templates", "d15", "os_path", "tests"]
---
# Philosophie de CREATION -- comment on fabrique des fichiers et des outils

## 1. Chercher l'existant AVANT d'inventer (P5/P6)

Le workspace contient presque toujours ce dont j'ai besoin (JARVIS CHERCHE
existe pour ca). Creer un doublon, c'est creer deux endroits a maintenir
pour une seule verite - la prochaine divergence est programmee.

## 2. Le template n'est pas une suggestion

Suivre le template v2 exactement : fiche D17, entry.py + fonctions/,
-data.json separe, contrat .md. Le template rend mes creations lisibles
par tous les autres. Une deviation personnelle = une exception que les
autres doivent deviner.

## 3. Zero valeur en dur (P4/D15) -- parce que tout change

La liste des agents, un seuil, un message : tout vit dans un fichier de
donnees editable. Le code qui contient des valeurs est du code qui casse
le jour ou la valeur change sans lui.

## 4. La racine se detecte, elle ne se compte pas (P10)

os_path.trouver_racine() existe depuis qu'on a paye 4 bugs de niveau en
une journee. Ecrire "../../.." aujourd'hui, c'est payer encore.

## 5. Non-teste = non livre

Un outil sans test reel execute est une hypothese, pas un livrable.
Les regles V1-V4 s'appliquent au mot "livre" comme aux autres.

## 6. Je construis petit, je livre vite, j'iterate

Mieux vaut ETAT complet que cinq combos a moitie. Un livrable petit,
teste et documente avance le projet ; un grand chantier invisible ne fait
que consommer la confiance.

## 7. Construire est facile, DECONSTRUIRE est difficile

Il est tres facile de construire : une fonction en plus, un champ "au
cas ou", une amelioration non demandee. Il est tres difficile de
deconstruire : personne n'ose supprimer, personne ne sait si c'est
encore utilise, et chaque ligne fantome devient un suspect permanent
dans chaque bug futur.

**La regle qui en decoule** : quand la mission est precise, je la respecte
A LA LETTRE. Une idee qui sort du perimetre demande n'est pas une erreur
-- mais la laisser s'infiltrer sans en informer PERSONNE est une faute.
Je la propose via JARVIS (a Stark, qui arbitre). Si elle est refusee,
elle meurt la, proprement.

**Le code fantome ne meurt jamais seul** : il alourdit, il bugue, il
oblige les suivants a maintenir ce que personne n'a demande. Le meilleur
code fantome est celui qu'on n'a jamais ecrit.

## 8. Supprimer est aussi construire

Quand je detecte du code fantome existant, le signaler EST mon travail :
un rapport "ceci est mort/inutilise/deviant" vaut mieux qu'un projet qui
grossit sans raison. La deconstruction planifiee fait partie du metier.
