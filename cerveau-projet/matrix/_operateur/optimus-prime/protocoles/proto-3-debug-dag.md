---
identite:
  type: protocole
  appartient_a: optimus-prime
  commun: false
---

# PROTOCOLE 3 -- DEBUG D.A.G. (Detection, Analyse, Guide)

> Source : docs/conversation-unslot-gemma-4.md (bloc "De la Creation a l'Audit").
> Changement de paradigme : je passe du mode CREATEUR au mode DETECTIVE.
> Le createur pense "il manque une piece, j'ajoute" -> doublons, spaghetti.
> Le detective pense "le mecanisme ne tourne pas, d'ou vient la faute ?" -> diagnostic cible.

## Regle absolue

Avant d'ecrire la moindre ligne corrective, PROUVER par le code existant que
l'hypothese du probleme est correcte. Ne rien ajouter tant que le probleme
n'est pas prouve. Chercher D'ABORD dans le code source, jamais commencer par
supposer qu'il manque quelque chose (sinon : doublons en collision).

## Etapes obligatoires, dans l'ordre

1. **Detection -- Test d'isolation** : l'erreur vient-elle de l'ENTREE
   (parametre mal forme), du TRAITEMENT (logique interne) ou de
   l'ENVIRONNEMENT (cle manquante) ? Isoler au niveau le plus bas
   (la fonction atomique).
2. **Analyse -- Audit de l'etat** : ne pas deviner. Observer (print, logs,
   points d'arret) la valeur reelle des variables au moment du crash.
   L'etat reel confirme-t-il l'hypothese ? Si l'etat est mauvais, le probleme
   est dans l'entree ou l'environnement, pas dans la logique.
3. **Guide -- Source Unique de Verite (SSOT)** : chaque donnee importante a
   UN SEUL endroit ou elle est definie. Si la valeur est mauvaise, je ne cree
   pas un nouveau parametre : je remonte a la SSOT (config, constante, entree)
   et je corrige l'ORIGINE.

## Verdict

Le code ne doit jamais etre CREE pour reparer un bug ; il doit etre AFFINE
pour reveler l'origine du bug. Un bug jamais seulement detecte : diagnostique
a la source, corrige a la source.
