---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# PROPOSITION DE CORRECTION -- docs/IMPERATIF.md (MO-547 / EO-550)

> La Matrice n ecrit JAMAIS dans `docs/` (zone des SOURCES, porte ECRIRE code 2).
> Cette fiche ne corrige donc pas la source : elle livre au createur le texte
> exact, verifie, pret a appliquer en UN geste.

## LE FAUT, CITE

`docs/IMPERATIF.md` ligne 22 :

    la construction dans 'matrix' va etre demarrer de zero. aucun autre agent ne sera creer tant que la matrice ne sera pas complete et operationnel.

## LE TEXTE PROPOSE (remplace la phrase entiere)

    la construction dans 'matrix' a demarre de zero en aout 2026 ; elle se POURSUIT
    aujourd hui sur l existant (points actifs, archives et traces deja poses), et
    aucun autre agent ne sera cree tant que la matrice ne sera pas complete et
    operationnelle.

Trois changements, chacun intentionnel :
1. `va etre demarrer` -> `a demarre ... en aout 2026` : l intention devient un
   fait date, donc un agent ne peut plus la lire comme un ordre de repartir.
2. `se POURSUIT aujourd hui sur l existant` : nomme l existant, qui est la
   premiere chose a preserver (valeur Protection de la vie).
3. `operationnel` -> `operationnelle` : accord avec `la matrice`.

## POURQUOI LA PHRASE ACTUELLE EST DANGEREUSE

Elle ne ment pas : elle decrit ce que le createur voulait en aout 2026. Mais
relue sans contexte par un agent qui ne connait pas l historique, elle se lit
comme une consigne < repars de zero > -- sur 543 points actifs, 366 archives et
125 Mo de traces. C est le SEUL point du fichier qui puisse causer un degat.

## APPLICATION PAR LE CREATEUR (deux gestes)

Depuis la RACINE du workspace :

    git -C . diff --stat -- cerveau-projet/matrix/docs/IMPERATIF.md

Verifier que le SHA du fichier sur disque est bien
`6a622f6796fef1f03739f140c9684377636af979b0bf819f1a337dbd605749fd`
(sinon le createur a deja modifie la source : ne pas ecraser sa version).

Puis remplacer la ligne 22 par le texte propose ci-dessus, et committer.

## CE QUE LA MATRICE A FAIT, ET CE QU ELLE NE FERA PAS

- MESURE : la phrase a ete localisee (ligne 22), le contexte mesure, le
  remplacement propose, les trois modifications justifiees.
- REFUS JOUE : la porte ECRIRE a ete appelee sur `docs/IMPERATIF.md` et a
  refuse en code 2, en nommant la zone et les trois remedes. Le refus est la
  preuve que la frontiere tient.
- La Matrice ne contourne pas, ne ecrit pas a cote, ne reclasse pas le fichier :
  une source du createur se corrige par le createur.

## L AUTRE MOITIE DE LA MISSION (EO-550, geste 2) -- RESOLUE

L audit MO-542 laissait un echec de non-regression : `docs/IMPERATIF.md` signale
modifie hors porte le 2026-10-02 a 08:16, sans note de modification.

Cause racine mesuree : ce n est PAS une ecriture de la Matrice.
- Le SHA-256 du fichier sur disque est IDENTIQUE a celui du commit `f0700252`.
- Le commit `f0700252` (< EVOLUTION PERMANENTE >, French-Team, 2026-10-02 09:49)
  corrige TROIS fautes de frappe du createur : `opererationnel` ->
  `operationnel`, `en suivant ple flux` -> `en suivant le flux`, `n'ariive` ->
  `n'arrive`.
- Le mtime du fichier (08:25:42) est ANTERIEUR a l heure du commit (09:49) :
  le fichier a bien ete edite a la main, puis committe par le createur.

Donc : une ecriture du createur, dans SA zone, actee par LUI. Elle n attend
aucune note de la Matrice -- et la poser aurait accuse le createur d avoir
ecrit dans sa propre source. Le maillon est VERT.

## ETAT

Non-regression : VERTE (0 echec). Attribution : VERDICT OK (0 ecriture non
attribuee). Le seul geste restant est la decision du createur ci-dessus.
